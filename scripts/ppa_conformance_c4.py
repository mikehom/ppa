#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic evaluator for CONFORMANCE_SPEC.md gate
#   C4 (sibling trigger disambiguation, eval boundaries, and name collisions).
# @decision DEC-PPA-009: Description overlap is measured over every indexed
#   discovery entry, and a name collision is judged against the names the port
#   actually emits for its target, not against canonical skill names.
"""Gate evaluator C4 for scripts/verify_port_conformance.py."""
from __future__ import annotations

import itertools
import re
from pathlib import Path

from adapters import common
from ppa_conformance_c125 import _load_served_units
from ppa_conformance_c34 import _mapped_port_paths
from ppa_conformance_scope import CheckOutcome, ConformanceContext, make_check, not_applicable
import ppa_artifact_rules as rules

TOKEN4_RE = re.compile(r"[a-z0-9]{4,}")


def _skill_descriptions_map(ctx: ConformanceContext) -> dict[str, str]:
    out: dict[str, str] = {}
    for d in rules.skill_dirs(ctx.core_root):
        fm = rules.parse_frontmatter(rules.read_lines(d / "SKILL.md")) or {}
        out[d.name] = fm.get("description", "")
    return out


def _strip_yaml_scalar(val: str) -> str:
    s = val.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in {'"', "'"}:
        return s[1:-1]
    return s


def _load_all_eval_cases(ctx: ConformanceContext) -> dict[str, list[dict[str, str]]]:
    evals: dict[str, list[dict[str, str]]] = {}
    for d in rules.skill_dirs(ctx.core_root):
        cpath = d / "evals" / "cases.yaml"
        if not cpath.is_file():
            evals[d.name] = []
            continue
        parsed = rules.parse_cases(rules.read_lines(cpath))
        evals[d.name] = [{k: _strip_yaml_scalar(v) for k, v in item.items()} for item in parsed]
    return evals


def _extract_skill_desc(text: str) -> str | None:
    meta, err = rules.parse_frontmatter_strict(rules.split_lines_n2(text))
    if not err and meta and "description" in meta:
        return meta["description"]
    cm = re.search(r"<!--\s*summary:\s*(.*?)\s*-->", text, re.S)
    return cm.group(1) if cm else None


def _port_skill_descriptions_map(ctx: ConformanceContext) -> tuple[dict[str, str], dict[str, str], list[str]]:
    descs: dict[str, str] = {}
    locs: dict[str, str] = {}
    errs: list[str] = []
    served = _load_served_units(ctx)
    for m in ctx.manifest.get("mappings", []):
        if not isinstance(m, dict):
            continue
        c_rel = Path(str(m.get("canonical", "")))
        if not (len(c_rel.parts) == 4 and c_rel.parts[:2] == ("knowledge", "skills") and c_rel.name == "SKILL.md"):
            continue
        sname = c_rel.parts[2]
        ports = m.get("port", [])
        if not isinstance(ports, list) or not ports:
            errs.append(f"port/{sname}/SKILL.md:0")
            continue
        pr = str(ports[0])
        if pr in served:
            txt = served[pr]
            locs[sname] = pr
        else:
            pp = ctx.port_root / pr
            if not pp.is_file():
                if not ("DEV-NOFILES" in ctx.deviation_ids and pr.startswith("ppa:")):
                    errs.append(f"port/{pr}:0")
                continue
            txt, uerr = rules.read_text_strict(pp)
            if uerr or txt is None:
                errs.append(f"port/{pr}:1")
                continue
            locs[sname] = f"port/{pr}"
        desc = _extract_skill_desc(txt)
        if desc is None:
            errs.append(f"{locs[sname]}:1 (missing description)")
        else:
            descs[sname] = desc
    return descs, locs, errs


def _check_descs_boundaries(
    descs: dict[str, str],
    locs: dict[str, str],
    all_known_siblings: set[str],
    c41_e: list[str],
    c42_e: list[str],
) -> None:
    """C4.1 and C4.2 on skill descriptions: positive trigger, negative clause, sibling redirect."""
    siblings = [s for s in sorted(descs) if s != rules.ROUTER_SKILL]
    for sname, desc in sorted(descs.items()):
        where = locs.get(sname, f"{sname}/SKILL.md")
        if "Use when" not in desc or not any(m in desc for m in rules.NEGATIVE_MARKERS):
            c41_e.append(f"{where}:1")
            continue
        neg_idx = min(desc.index(m) for m in rules.NEGATIVE_MARKERS if m in desc)
        neg_clause = desc[neg_idx:]
        targets = (set(siblings) if len(siblings) >= 2 else all_known_siblings) - {sname}
        if not any(re.search(rf"(?<![A-Za-z0-9-]){re.escape(t)}(?![A-Za-z0-9-])", neg_clause) for t in targets):
            c42_e.append(f"{where}:1")


def _check_pairwise_overlap(descs: dict[str, str], locs: dict[str, str], c43_e: list[str]) -> int:
    """C4.3 over every pair of indexed discovery entries (skills, router, indexed ambient files)."""
    n_pairs = 0
    tokens = {
        name: {w for w in TOKEN4_RE.findall(text.lower()) if w != "ppa"} for name, text in descs.items()
    }
    for s1, s2 in itertools.combinations(sorted(descs), 2):
        n_pairs += 1
        t1, t2 = tokens[s1], tokens[s2]
        jacc = (len(t1 & t2) / len(t1 | t2)) if (t1 | t2) else 1.0
        if jacc >= 0.50:
            c43_e.append(f"{locs.get(s1, s1)}<->{locs.get(s2, s2)}:1 (jaccard={jacc:.3f})")
    return n_pairs


def _canonical_ambient_descriptions(ctx: ConformanceContext) -> dict[str, str]:
    """Discovery descriptions the canonical ambient files declare (what an indexing port lifts)."""
    amb_dir = ctx.core_root / "knowledge" / "ambient-context"
    out: dict[str, str] = {}
    for amb in sorted(amb_dir.glob("ppa-*.md")) if amb_dir.is_dir() else []:
        out[amb.name] = common.ambient_trigger_description(amb)
    return out


def _port_ambient_descriptions(ctx: ConformanceContext) -> tuple[dict[str, str], dict[str, str]]:
    """Descriptions of ambient entries the port indexes (manifest discovery_entries)."""
    indexed = {
        str(e.get("name", "")) for e in ctx.manifest.get("discovery_entries", []) if isinstance(e, dict)
    }
    descs: dict[str, str] = {}
    locs: dict[str, str] = {}
    for m in ctx.manifest.get("mappings", []):
        if not isinstance(m, dict):
            continue
        c_rel = Path(str(m.get("canonical", "")))
        if c_rel.parts[:2] != ("knowledge", "ambient-context") or not isinstance(m.get("port"), list):
            continue
        if c_rel.name not in indexed and c_rel.stem not in indexed:
            continue
        for pr in m["port"][:1]:
            pp = ctx.port_root / str(pr)
            txt, uerr = rules.read_text_strict(pp) if pp.is_file() else (None, "missing")
            if uerr or txt is None:
                continue
            meta, _ = rules.parse_frontmatter_strict(rules.split_lines_n2(txt))
            if meta and meta.get("description"):
                descs[c_rel.name] = meta["description"]
                locs[c_rel.name] = f"port/{pr}"
    return descs, locs


def _load_port_eval_cases(ctx: ConformanceContext) -> dict[str, list[dict[str, str]]]:
    evals: dict[str, list[dict[str, str]]] = {}
    for pr, pp in _mapped_port_paths(ctx, lambda c: c.endswith("/evals/cases.yaml")):
        sname = Path(pr).parent.parent.name if pp.parent.name == "evals" else pr
        if not pp.is_file():
            evals[f"port/{sname}"] = []
            continue
        parsed = rules.parse_cases(rules.read_lines(pp))
        evals[f"port/{sname}"] = [{k: _strip_yaml_scalar(v) for k, v in item.items()} for item in parsed]
    return evals


def evaluate_gate_c4(ctx: ConformanceContext) -> list[CheckOutcome]:
    """Evaluate C4.1 through C4.8."""
    descs = _skill_descriptions_map(ctx)
    all_skills = sorted(descs)
    siblings = [s for s in all_skills if s != rules.ROUTER_SKILL]
    all_known_siblings = {
        "ppa-dataflow-and-slicing", "ppa-control-flow-and-constraints",
        "ppa-abstract-interpretation", "ppa-types-effects-and-regions",
        "ppa-fixedpoint-solvers", "ppa-cyber-vulnerability-analysis",
    } | set(siblings)
    c41_e: list[str] = []
    c42_e: list[str] = []
    c43_e: list[str] = []
    core_locs = {s: f"{s}/SKILL.md" for s in all_skills}
    _check_descs_boundaries(descs, core_locs, all_known_siblings, c41_e, c42_e)
    amb_descs = _canonical_ambient_descriptions(ctx)
    core_locs.update({a: f"knowledge/ambient-context/{a}" for a in amb_descs})
    n_pairs = _check_pairwise_overlap({**descs, **amb_descs}, core_locs, c43_e)
    n_skills_checked = len(all_skills)
    if not ctx.canonical_only:
        p_descs, p_locs, p_missing = _port_skill_descriptions_map(ctx)
        c41_e.extend(p_missing)
        if p_descs:
            _check_descs_boundaries(p_descs, p_locs, all_known_siblings, c41_e, c42_e)
            pa_descs, pa_locs = _port_ambient_descriptions(ctx)
            n_pairs += _check_pairwise_overlap({**p_descs, **pa_descs}, {**p_locs, **pa_locs}, c43_e)
            n_skills_checked += len(p_descs)

    c44_e, c44_n = _check_c4_4_router_table(ctx, siblings)
    evals = _load_all_eval_cases(ctx)
    c45_e, c46_e, c46_n = _check_c4_5_6_evals(evals, "knowledge/skills")
    if not ctx.canonical_only and (pevals := _load_port_eval_cases(ctx)):
        p45, p46, p_eval_cnt = _check_c4_5_6_evals(pevals, "port")
        c45_e.extend(p45)
        c46_e.extend(p46)
        c46_n += p_eval_cnt
    c47_e, c47_n = _check_c4_7_isomorphism(ctx, evals)
    return [
        make_check("C4.1", n_skills_checked, c41_e, "C4_BOUNDARY_MISSING"),
        make_check("C4.2", n_skills_checked, c42_e, "C4_NO_REDIRECT"),
        make_check("C4.3", n_pairs, c43_e, "C4_DESCRIPTION_OVERLAP"),
        make_check("C4.4", c44_n, c44_e, "C4_ROUTER_INCOMPLETE"),
        make_check("C4.5", len(evals), c45_e, "C4_EVAL_COVERAGE"),
        make_check("C4.6", c46_n, c46_e, "C4_EVAL_CONTRADICTION"),
        make_check("C4.7", c47_n, c47_e, "C4_ISOMORPHISM_BOUNDARY"),
        _check_c4_8_collision(ctx, all_skills),
    ]


def _check_router_text(txt: str, label: str, siblings: list[str]) -> tuple[list[str], int]:
    route_counts: dict[str, int] = {}
    errs: list[str] = []
    rows_seen = 0
    in_decision = False
    for lineno, line in rules.strip_fences_and_frontmatter(txt):
        if line.startswith("## "):
            in_decision = "Decision" in line or "Routing" in line
            continue
        if not in_decision or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or set(cells[0]) <= {":", "-", " "} or cells[1].lower().startswith("route"):
            continue
        rows_seen += 1
        m_sk = re.findall(r"ppa-[a-z0-9-]+", cells[1])
        if len(m_sk) != 1 or not cells[2] or not cells[3]:
            errs.append(f"{label}:{lineno}")
            continue
        route_counts[m_sk[0]] = route_counts.get(m_sk[0], 0) + 1
    for sib in siblings:
        if route_counts.get(sib, 0) != 1:
            errs.append(f"{label}:1 ({sib} rows={route_counts.get(sib, 0)})")
    return errs, rows_seen


def _check_c4_4_router_table(ctx: ConformanceContext, siblings: list[str]) -> tuple[list[str], int]:
    router_path = ctx.core_root / "knowledge" / "skills" / rules.ROUTER_SKILL / "SKILL.md"
    if not router_path.is_file():
        return [f"{rules.ROUTER_SKILL}/SKILL.md:0"], 0
    txt, uerr = rules.read_text_strict(router_path)
    if uerr or txt is None:
        return [f"{rules.ROUTER_SKILL}/SKILL.md:1"], 0
    errs, total_n = _check_router_text(txt, f"knowledge/skills/{rules.ROUTER_SKILL}/SKILL.md", siblings)
    if not ctx.canonical_only:
        served = _load_served_units(ctx)
        for pr, pp in _mapped_port_paths(ctx, lambda c: c == f"knowledge/skills/{rules.ROUTER_SKILL}/SKILL.md"):
            if pr in served:
                pe, pn = _check_router_text(served[pr], pr, siblings)
                errs.extend(pe)
                total_n += pn
            elif pp.is_file():
                ptxt, perr = rules.read_text_strict(pp)
                if perr or ptxt is None:
                    errs.append(f"port/{pr}:1")
                else:
                    pe, pn = _check_router_text(ptxt, f"port/{pr}", siblings)
                    errs.extend(pe)
                    total_n += pn
    return errs, total_n


def _check_c4_5_6_evals(
    evals: dict[str, list[dict[str, str]]], prefix_base: str = "knowledge/skills"
) -> tuple[list[str], list[str], int]:
    c45_e: list[str] = []
    c46_e: list[str] = []
    prompt_owner: dict[str, tuple[str, str]] = {}
    total_cases = 0
    for sname, cases in sorted(evals.items()):
        bare = sname.removeprefix("port/")
        where = f"{sname}/evals/cases.yaml" if sname.startswith("port/") else f"{prefix_base}/{bare}/evals/cases.yaml"
        pos = sum(1 for c in cases if c.get("expect_skill") == bare)
        neg = sum(1 for c in cases if c.get("expect_skill") and c.get("expect_skill") != bare)
        if pos < 3 or neg < 2:
            c45_e.append(f"{where}:1 (pos={pos}, neg={neg})")
        for idx, c in enumerate(cases, start=1):
            total_cases += 1
            norm_p = common.normalized_body_n5(c.get("prompt", ""))
            exp = c.get("expect_skill", "")
            prev = prompt_owner.get(norm_p)
            if prev is not None and prev[0] != exp:
                c46_e.append(f"{where}:{idx} vs {prev[1]}")
            else:
                prompt_owner[norm_p] = (exp, bare)
    return c45_e, c46_e, total_cases


def _owning_non_router_skills(node: dict) -> set[str]:
    owners: set[str] = set()
    for ref in node.get("artifact_refs", []):
        m = re.search(r"(?:^|/)skills/(ppa-[a-z0-9-]+)(?:/|$)", str(ref))
        if m and m.group(1) != rules.ROUTER_SKILL:
            owners.add(m.group(1))
    return owners


def _check_c4_7_isomorphism(
    ctx: ConformanceContext, evals: dict[str, list[dict[str, str]]]
) -> tuple[list[str], int]:
    nodes = (ctx.port_graph or {}).get("concepts", [])
    by_id = {str(n.get("id")): n for n in nodes if isinstance(n, dict) and n.get("id")}
    errs: list[str] = []
    edges_seen = 0
    for cid, node in sorted(by_id.items()):
        src_skills = _owning_non_router_skills(node)
        for edge in node.get("related_edges", []):
            if not isinstance(edge, dict) or edge.get("relation") != "corresponds_to":
                continue
            edges_seen += 1
            basis = edge.get("basis")
            if not isinstance(basis, dict) or not basis.get("unification_id"):
                errs.append(f"{cid}:0 missing basis.unification_id")
            tgt = by_id.get(str(edge.get("target_id", "")))
            if tgt is None:
                continue
            for s_a in sorted(src_skills):
                for s_b in sorted(_owning_non_router_skills(tgt)):
                    if s_a == s_b:
                        continue
                    has_ab = any(c.get("expect_skill") == s_b for c in evals.get(s_a, []))
                    has_ba = any(c.get("expect_skill") == s_a for c in evals.get(s_b, []))
                    if not (has_ab and has_ba):
                        errs.append(f"{s_a}<->{s_b}:1 ({cid})")
    return errs, edges_seen


def _check_c4_8_collision(ctx: ConformanceContext, canonical_skills: list[str]) -> CheckOutcome:
    """C4.8: names present before installation versus the names this port actually emits."""
    if ctx.canonical_only:
        return not_applicable("C4.8")
    errs: list[str] = []
    raw_pre = ctx.manifest.get("pre_existing_discovery")
    if not isinstance(raw_pre, list):
        errs.append("port_manifest.json:0 missing pre_existing_discovery (use [] when the target was empty)")
        raw_pre = []
    pre = {str(x) for x in raw_pre}
    emitted = common.emitted_discovery_names(ctx.manifest)
    disc = {
        str(e.get("name", "")) for e in ctx.manifest.get("discovery_entries", [])
        if isinstance(e, dict)
    }
    for coll in sorted(pre & emitted):
        errs.append(f"port_manifest.json:0 collision {coll}")
    for s in canonical_skills:
        if s not in disc:
            errs.append(f"port_manifest.json:0 missing/renamed {s}")
    return make_check("C4.8", len(emitted) + len(pre), errs, "C4_NAME_COLLISION")
