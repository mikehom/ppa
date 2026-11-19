#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic evaluators for CONFORMANCE_SPEC.md gates
#   C3 (progressive disclosure, frontmatter & budgets) and C4 (sibling trigger
#   disambiguation & eval boundaries).
"""Gate evaluators C3 and C4 for scripts/verify_port_conformance.py."""
from __future__ import annotations

import collections
import itertools
import re
from pathlib import Path

from adapters import common
from ppa_conformance_c125 import CheckOutcome, ConformanceContext, _load_served_units, list_port_files, make_check
import ppa_artifact_rules as rules
import validate_ppa_knowledge as vpk

TOKEN4_RE = re.compile(r"[a-z0-9]{4,}")


def _mapped_port_paths(ctx: ConformanceContext, pred) -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    for m in ctx.manifest.get("mappings", []):
        if not isinstance(m, dict):
            continue
        c_rel = str(m.get("canonical", ""))
        if not pred(c_rel):
            continue
        for pr in m.get("port", []) if isinstance(m.get("port"), list) else []:
            out.append((str(pr), ctx.port_root / str(pr)))
    return out


def _check_c3_budgets_and_frontmatter(ctx: ConformanceContext) -> list[CheckOutcome]:
    dev_nofiles = "DEV-NOFILES" in ctx.deviation_ids
    c31_e, c32_e, c33_e, c34_e, c35_e, c36_e = [], [], [], [], [], []
    n_r, n_s, n_ref, n_amb, n_fm, n_nofm = 0, 0, 0, 0, 0, 0

    for d in rules.skill_dirs(ctx.core_root):
        smd = d / "SKILL.md"
        where = smd.relative_to(ctx.core_root).as_posix()
        lines = rules.read_lines(smd)
        if d.name == rules.ROUTER_SKILL:
            n_r += 1
            if not rules.ROUTER_MIN <= len(lines) < rules.ROUTER_MAX:
                c31_e.append(f"{where}:1 ({len(lines)}L)")
        else:
            n_s += 1
            if not rules.SKILL_MIN <= len(lines) < rules.SKILL_MAX:
                c32_e.append(f"{where}:1 ({len(lines)}L)")
        n_fm += 1
        fm, fm_err = rules.parse_frontmatter_strict(lines)
        if (fm_err or fm is None or set(fm) != {"name", "description"}
                or fm.get("name") != d.name or not rules.SKILL_NAME_RE.match(d.name)
                or len(d.name) > 64):
            c35_e.append(f"{where}:1")
        for ref in sorted((d / "references").glob("*.md")):
            n_ref += 1
            rlines = rules.read_lines(ref)
            if len(rlines) > rules.REFERENCE_MAX:
                c33_e.append(f"{ref.relative_to(ctx.core_root).as_posix()}:1 ({len(rlines)}L)")

    amb_dir = ctx.core_root / "knowledge" / "ambient-context"
    for amb in sorted(amb_dir.glob("ppa-*.md")) if amb_dir.is_dir() else []:
        n_amb += 1
        alines = rules.read_lines(amb)
        if not rules.AMBIENT_MIN <= len(alines) <= rules.AMBIENT_MAX:
            c34_e.append(f"{amb.relative_to(ctx.core_root).as_posix()}:1 ({len(alines)}L)")

    c36_e.extend(rules.check_forbidden_frontmatter(ctx.core_root))
    n_nofm += max(len(list((ctx.core_root / "ontology").glob("*.md"))), 1)

    if not ctx.canonical_only:
        _check_c3_port_units(ctx, c31_e, c32_e, c33_e, c34_e, c35_e, c36_e)

    return [
        make_check("C3.1", n_r, c31_e, "C3_ROUTER_BUDGET", exempt_vacuous=dev_nofiles),
        make_check("C3.2", n_s, c32_e, "C3_SKILL_BUDGET", exempt_vacuous=dev_nofiles),
        make_check("C3.3", n_ref, c33_e, "C3_REFERENCE_CEILING", exempt_vacuous=dev_nofiles),
        make_check("C3.4", n_amb, c34_e, "C3_AMBIENT_BUDGET", exempt_vacuous=dev_nofiles),
        make_check("C3.5", n_fm, c35_e, "C3_FRONTMATTER_KEYS"),
        make_check("C3.6", n_nofm, c36_e, "C3_FRONTMATTER_FORBIDDEN", exempt_vacuous=dev_nofiles),
    ]


def _check_dev_nofiles_units(ctx: ConformanceContext, errs: dict[str, list[str]]) -> None:
    has_disk = (ctx.port_root / "pages").is_dir() or any(
        not p.relative_to(ctx.port_root).as_posix().startswith("core/")
        and (p.name == "SKILL.md" or p.suffix == ".mdc")
        for p in list_port_files(ctx.port_root)
    )
    if has_disk:
        errs["C3.1"].append("port_manifest.json:0 (DEV-NOFILES invalid with on-disk pages/ or skill Markdown files)")
        return
    for uri, txt in sorted(_load_served_units(ctx).items()):
        lines = rules.split_lines_n2(txt)
        n = len(lines)
        if uri == f"ppa:concepts/{rules.ROUTER_SKILL}.md":
            if not rules.ROUTER_MIN <= n < rules.ROUTER_MAX:
                errs["C3.1"].append(f"{uri}:1 ({n}L)")
        elif uri.startswith("ppa:concepts/ppa-ambient-"):
            if not rules.AMBIENT_MIN <= n <= rules.AMBIENT_MAX:
                errs["C3.4"].append(f"{uri}:1 ({n}L)")
        elif "ppa-index-" in uri or uri in {"ppa:index.md", "ppa:log.md"}:
            if n > rules.AMBIENT_MAX:
                errs["C3.4"].append(f"{uri}:1 ({n}L)")
        elif uri.startswith("ppa:concepts/ppa-node-") or uri.startswith("ppa:sources/"):
            if n > rules.REFERENCE_MAX:
                errs["C3.3"].append(f"{uri}:1 ({n}L)")
            if lines and rules.is_fm_delim(lines[0], first=True):
                errs["C3.6"].append(f"{uri}:1")
        elif uri.startswith("ppa:concepts/ppa-"):
            if not rules.SKILL_MIN <= n < rules.SKILL_MAX:
                errs["C3.2"].append(f"{uri}:1 ({n}L)")


def _check_c3_port_units(
    ctx: ConformanceContext, c31_e: list[str], c32_e: list[str], c33_e: list[str],
    c34_e: list[str], c35_e: list[str], c36_e: list[str],
) -> None:
    if "DEV-NOFILES" in ctx.deviation_ids:
        _check_dev_nofiles_units(ctx, {"C3.1": c31_e, "C3.2": c32_e, "C3.3": c33_e, "C3.4": c34_e, "C3.6": c36_e})
    r_prefix = f"knowledge/skills/{rules.ROUTER_SKILL}/SKILL.md"
    specs = (
        (lambda c: c == r_prefix, c31_e, rules.ROUTER_MIN, rules.ROUTER_MAX - 1),
        (lambda c: c.startswith("knowledge/skills/") and c.endswith("/SKILL.md") and rules.ROUTER_SKILL not in c,
         c32_e, rules.SKILL_MIN, rules.SKILL_MAX - 1),
        (lambda c: c.startswith("knowledge/ambient-context/"), c34_e, rules.AMBIENT_MIN, rules.AMBIENT_MAX),
    )
    for pred, bucket, lo, hi in specs:
        for pr, pp in _mapped_port_paths(ctx, pred):
            if pp.is_file() and not lo <= len(rules.read_lines(pp)) <= hi:
                bucket.append(f"port/{pr}:1 ({len(rules.read_lines(pp))}L)")
    for pr, pp in _mapped_port_paths(ctx, lambda c: "/references/" in c and c.endswith(".md")):
        if pp.is_file():
            lines = rules.read_lines(pp)
            if len(lines) > rules.REFERENCE_MAX:
                c33_e.append(f"port/{pr}:1 ({len(lines)}L)")
            if lines and rules.is_fm_delim(lines[0], first=True):
                c36_e.append(f"port/{pr}:1")
    for pr, pp in _mapped_port_paths(ctx, lambda c: c.endswith("/SKILL.md")):
        if pp.is_file() and pp.name == "SKILL.md":
            fm, err = rules.parse_frontmatter_strict(rules.read_lines(pp))
            if err or fm is None or set(fm) != {"name", "description"} or fm.get("name") != pp.parent.name:
                c35_e.append(f"port/{pr}:1")
    for p in list_port_files(ctx.port_root):
        rel = p.relative_to(ctx.port_root).as_posix()
        if rel == "pages/index.md" or p.name.startswith("ppa-index-"):
            if len(rules.read_lines(p)) > rules.AMBIENT_MAX:
                c34_e.append(f"port/{rel}:1 ({len(rules.read_lines(p))}L)")
        elif (rel.startswith("pages/sources/") or rel.startswith("pages/concepts/ppa-node-")) and p.suffix == ".md":
            lines = rules.read_lines(p)
            if len(lines) > rules.REFERENCE_MAX:
                c33_e.append(f"port/{rel}:1 ({len(lines)}L)")
            if lines and rules.is_fm_delim(lines[0], first=True):
                c36_e.append(f"port/{rel}:1")


def _scan_links_in_tree(
    base_root: Path,
    files: list[Path],
    skill_entry_by_path: dict[Path, str],
    ref_paths: set[Path],
    ref_owner_by_path: dict[Path, str],
    enforce_kroot: Path | None,
) -> tuple[list[str], list[str], dict[Path, set[Path]], int]:
    broken: list[str] = []
    direction: list[str] = []
    outbound: dict[Path, set[Path]] = {}
    hcache: dict[Path, set[str]] = {}
    root_res = base_root.resolve()
    examined = 0
    for src in files:
        txt, uerr = rules.read_text_strict(src)
        if uerr or txt is None:
            broken.append(f"{src.relative_to(base_root).as_posix()}:1")
            continue
        src_res = src.resolve()
        where = src.relative_to(base_root).as_posix()
        src_skill = skill_entry_by_path.get(src_res) or ref_owner_by_path.get(src_res)
        for lineno, line in rules.strip_fences_and_frontmatter(txt):
            for m in vpk.LINK_RE.finditer(line):
                target = m.group(1)
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue
                examined += 1
                clean, *frag = target.split("#", 1)
                if clean.startswith("/"):
                    broken.append(f"{where}:{lineno}")
                    continue
                dest = (src.parent / clean).resolve() if clean else src_res
                if root_res not in dest.parents and dest != root_res:
                    direction.append(f"{where}:{lineno}")
                    continue
                if enforce_kroot is not None and enforce_kroot not in dest.parents and dest != enforce_kroot:
                    direction.append(f"{where}:{lineno}")
                    continue
                if not dest.exists():
                    broken.append(f"{where}:{lineno}")
                    continue
                outbound.setdefault(src_res, set()).add(dest)
                if frag and dest.suffix in {".md", ".mdc"}:
                    if frag[0] not in vpk.headings_of(dest, hcache):
                        broken.append(f"{where}:{lineno}")
                dst_skill_entry = skill_entry_by_path.get(dest)
                if src_res in ref_paths and (dest.name == "SKILL.md" or dst_skill_entry is not None):
                    direction.append(f"{where}:{lineno}")
                elif src_skill and dst_skill_entry and dst_skill_entry != src_skill:
                    direction.append(f"{where}:{lineno}")
    return broken, direction, outbound, max(examined, len(files))


def _check_c3_links_and_reachability(ctx: ConformanceContext) -> list[CheckOutcome]:
    core_k_md = [p for p in common.sorted_files_under(ctx.core_root / "knowledge", {".md"})]
    core_skill_entries = {(d / "SKILL.md").resolve(): d.name for d in rules.skill_dirs(ctx.core_root)}
    core_ref_owners = {
        r.resolve(): d.name
        for d in rules.skill_dirs(ctx.core_root)
        for r in sorted((d / "references").glob("*.md"))
    }
    c37_e, c38_e, core_out, n_links = _scan_links_in_tree(
        ctx.core_root,
        core_k_md,
        core_skill_entries,
        set(core_ref_owners),
        core_ref_owners,
        (ctx.core_root / "knowledge").resolve(),
    )
    c39_e = vpk.check_reachability(ctx.core_root, core_out)

    if not ctx.canonical_only:
        p_b, p_d, p_r, p_n = _check_port_links_and_reach(ctx)
        c37_e.extend(f"port/{e}" for e in p_b)
        c38_e.extend(f"port/{e}" for e in p_d)
        c39_e.extend(f"port/{e}" for e in p_r)
        n_links += p_n

    return [
        make_check("C3.7", n_links, c37_e, "C3_LINK_BROKEN"),
        make_check("C3.8", n_links, c38_e, "C3_LINK_DIRECTION"),
        make_check("C3.9", len(core_skill_entries) + len(core_ref_owners), c39_e, "C3_ORPHAN_FILE"),
    ]


def _check_wiki_pages_reach(
    port_root: Path, pages_dir: Path, outbound: dict[Path, set[Path]], reach_errs: list[str]
) -> None:
    index_md = (pages_dir / "index.md").resolve()
    if not index_md.is_file():
        reach_errs.append("pages/index.md:0 (missing root wiki index)")
        return
    pages_res = pages_dir.resolve()
    seen: set[Path] = {index_md}
    queue = collections.deque([index_md])
    while queue:
        cur = queue.popleft()
        for dst in outbound.get(cur, set()):
            if dst not in seen and (pages_res in dst.parents or dst == pages_res):
                seen.add(dst)
                queue.append(dst)
    for wp in common.sorted_files_under(pages_dir, {".md"}):
        if wp.resolve() not in seen:
            reach_errs.append(f"{wp.relative_to(port_root).as_posix()}:1 (unreachable from pages/index.md)")


def _check_port_links_and_reach(ctx: ConformanceContext) -> tuple[list[str], list[str], list[str], int]:
    p_skill_entries: dict[Path, str] = {}
    p_ref_owners: dict[Path, str] = {}
    p_files: list[Path] = []
    for m in ctx.manifest.get("mappings", []):
        if not isinstance(m, dict):
            continue
        c_rel = Path(str(m.get("canonical", "")))
        if not c_rel.parts or c_rel.parts[0] != "knowledge":
            continue
        for pr in m.get("port", []) if isinstance(m.get("port"), list) else []:
            pp = (ctx.port_root / str(pr)).resolve()
            if pp.is_file() and pp.suffix in {".md", ".mdc"}:
                p_files.append(pp)
                if c_rel.name == "SKILL.md":
                    p_skill_entries[pp] = c_rel.parent.name
                elif len(c_rel.parts) == 5 and c_rel.parts[3] == "references":
                    p_ref_owners[pp] = c_rel.parts[2]
    pages_dir = ctx.port_root / "pages"
    if pages_dir.is_dir():
        for wp in common.sorted_files_under(pages_dir, {".md"}):
            wp_res = wp.resolve()
            if wp_res not in p_files:
                p_files.append(wp_res)
            if "sources" in wp.relative_to(pages_dir).parts:
                p_ref_owners.setdefault(wp_res, "")

    broken, direction, outbound, n_links = _scan_links_in_tree(
        ctx.port_root, p_files, p_skill_entries, set(p_ref_owners), p_ref_owners, None
    )
    reach_errs: list[str] = []
    router_paths = [p for p, s in p_skill_entries.items() if s == rules.ROUTER_SKILL]
    router_txt = ""
    if router_paths and router_paths[0].is_file():
        t, _ = rules.read_text_strict(router_paths[0])
        router_txt = t or ""
    for p_entry, sname in sorted(p_skill_entries.items(), key=lambda kv: kv[1]):
        if sname != rules.ROUTER_SKILL and router_paths:
            if not re.search(rf"(?<![A-Za-z0-9-]){re.escape(sname)}(?![A-Za-z0-9-])", router_txt):
                reach_errs.append(f"{router_paths[0].relative_to(ctx.port_root).as_posix()}:1 ({sname})")
        linked = outbound.get(p_entry, set())
        for ref_p, owner in sorted(p_ref_owners.items()):
            if owner == sname and ref_p not in linked:
                reach_errs.append(f"{ref_p.relative_to(ctx.port_root).as_posix()}:1")
    if pages_dir.is_dir():
        _check_wiki_pages_reach(ctx.port_root, pages_dir, outbound, reach_errs)
    return broken, direction, reach_errs, n_links


def _check_c3_10_to_12(ctx: ConformanceContext) -> list[CheckOutcome]:
    c310_e = rules.check_evals(ctx.core_root)
    n_evals = len(rules.skill_dirs(ctx.core_root))
    if not ctx.canonical_only:
        for pr, pp in _mapped_port_paths(ctx, lambda c: c.endswith("/evals/cases.yaml")):
            if not pp.is_file():
                c310_e.append(f"port/{pr}:0")
                continue
            cases = rules.parse_cases(rules.read_lines(pp))
            if not cases:
                c310_e.append(f"port/{pr}:1")

    c311_e, c311_n = _check_c3_11_artifact_refs(ctx)
    c312_e = rules.check_knowledge_tree(ctx.core_root)
    c312_n = len(common.sorted_files_under(ctx.core_root / "knowledge"))
    return [
        make_check("C3.10", n_evals, c310_e, "C3_EVALS_SHAPE"),
        make_check("C3.11", c311_n, c311_e, "C3_ARTIFACT_REF"),
        make_check("C3.12", c312_n, c312_e, "C3_UNKNOWN_FILE"),
    ]


def _check_c3_11_artifact_refs(ctx: ConformanceContext) -> tuple[list[str], int]:
    nodes = (ctx.port_graph or {}).get("concepts", [])
    if ctx.canonical_only:
        return vpk.check_artifact_refs(ctx.core_root, nodes), len(nodes)
    map_by_canon = {
        str(m.get("canonical")): [str(p) for p in m.get("port", [])]
        for m in ctx.manifest.get("mappings", [])
        if isinstance(m, dict) and isinstance(m.get("port"), list)
    }
    served = _load_served_units(ctx)
    corpus_root_rel = str(ctx.manifest.get("corpus_root", ""))
    port_res = ctx.port_root.resolve()
    hcache: dict[Path, set[str]] = {}
    errs: list[str] = []
    examined = 0
    for c in nodes:
        if not isinstance(c, dict):
            continue
        cid = str(c.get("id", "?"))
        refs = c.get("artifact_refs", [])
        if not refs and not c.get("artifact_exclusion"):
            errs.append(f"{cid}:0 empty artifact_refs")
        for ref in refs:
            if not isinstance(ref, str):
                continue
            examined += 1
            clean, *frag = ref.split("#", 1)
            raw_ports = map_by_canon.get(clean)
            if raw_ports and all(p.startswith("ppa:") for p in raw_ports):
                if not all(p in served for p in raw_ports):
                    errs.append(f"{cid}:0 ({ref})")
                elif frag and not any(frag[0] in vpk.headings_of_text(served[p]) for p in raw_ports):
                    errs.append(f"{cid}:0 ({ref} fragment)")
                continue
            if raw_ports:
                candidates = [(ctx.port_root / p).resolve() for p in raw_ports]
            elif clean.startswith("corpus/") and corpus_root_rel:
                candidates = [(ctx.port_root / corpus_root_rel / clean.removeprefix("corpus/")).resolve()]
            else:
                candidates = [(ctx.port_root / clean).resolve()]
            if not candidates or not all(port_res in d.parents and d.is_file() for d in candidates):
                errs.append(f"{cid}:0 ({ref})")
            elif frag:
                md_cands = [d for d in candidates if d.suffix in {".md", ".mdc"}]
                if md_cands and not any(frag[0] in vpk.headings_of(d, hcache) for d in md_cands):
                    errs.append(f"{cid}:0 ({ref} fragment)")
    return errs, max(examined, len(nodes))


def evaluate_gate_c3(ctx: ConformanceContext) -> list[CheckOutcome]:
    """Evaluate C3.1 through C3.12."""
    return _check_c3_budgets_and_frontmatter(ctx) + _check_c3_links_and_reachability(ctx) + _check_c3_10_to_12(ctx)


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
    c43_e: list[str],
) -> int:
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
    pair_pool = siblings if len(siblings) >= 2 else sorted(descs)
    n_pairs = 0
    for s1, s2 in itertools.combinations(pair_pool, 2):
        n_pairs += 1
        t1 = {w for w in TOKEN4_RE.findall(descs[s1].lower()) if w != "ppa"}
        t2 = {w for w in TOKEN4_RE.findall(descs[s2].lower()) if w != "ppa"}
        jacc = (len(t1 & t2) / len(t1 | t2)) if (t1 | t2) else 1.0
        if jacc >= 0.50:
            c43_e.append(f"{locs.get(s1, s1)}<->{locs.get(s2, s2)}:1 (jaccard={jacc:.3f})")
    return n_pairs


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
    n_pairs = _check_descs_boundaries(descs, {s: f"{s}/SKILL.md" for s in all_skills}, all_known_siblings, c41_e, c42_e, c43_e)
    n_skills_checked = len(all_skills)
    if not ctx.canonical_only:
        p_descs, p_locs, p_missing = _port_skill_descriptions_map(ctx)
        c41_e.extend(p_missing)
        if p_descs:
            n_pairs += _check_descs_boundaries(p_descs, p_locs, all_known_siblings, c41_e, c42_e, c43_e)
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
    c48_e, c48_n = _check_c4_8_collision(ctx, all_skills)
    return [
        make_check("C4.1", n_skills_checked, c41_e, "C4_BOUNDARY_MISSING"),
        make_check("C4.2", n_skills_checked, c42_e, "C4_NO_REDIRECT"),
        make_check("C4.3", n_pairs, c43_e, "C4_DESCRIPTION_OVERLAP"),
        make_check("C4.4", c44_n, c44_e, "C4_ROUTER_INCOMPLETE"),
        make_check("C4.5", len(evals), c45_e, "C4_EVAL_COVERAGE"),
        make_check("C4.6", c46_n, c46_e, "C4_EVAL_CONTRADICTION"),
        make_check("C4.7", c47_n, c47_e, "C4_ISOMORPHISM_BOUNDARY"),
        make_check("C4.8", c48_n, c48_e, "C4_NAME_COLLISION"),
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
    return errs, max(rows_seen, len(siblings))


def _check_c4_4_router_table(ctx: ConformanceContext, siblings: list[str]) -> tuple[list[str], int]:
    router_path = ctx.core_root / "knowledge" / "skills" / rules.ROUTER_SKILL / "SKILL.md"
    if not router_path.is_file():
        return [f"{rules.ROUTER_SKILL}/SKILL.md:0"], 0
    txt, uerr = rules.read_text_strict(router_path)
    if uerr or txt is None:
        return [f"{rules.ROUTER_SKILL}/SKILL.md:1"], 1
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


def _check_c4_8_collision(ctx: ConformanceContext, canonical_skills: list[str]) -> tuple[list[str], int]:
    if ctx.canonical_only:
        dupes = len(canonical_skills) - len(set(canonical_skills))
        return (["knowledge/skills:0"] if dupes else []), len(canonical_skills)
    pre = {str(x) for x in ctx.manifest.get("pre_existing_discovery", [])}
    disc = {
        str(e.get("name", "")) for e in ctx.manifest.get("discovery_entries", [])
        if isinstance(e, dict)
    }
    amb_dir = ctx.core_root / "knowledge" / "ambient-context"
    amb_stems = {p.stem for p in amb_dir.glob("ppa-*.md")} if amb_dir.is_dir() else set()
    canonical_all = set(canonical_skills) | amb_stems
    errs: list[str] = []
    for coll in sorted(pre & canonical_all):
        errs.append(f"port_manifest.json:0 collision {coll}")
    for s in canonical_skills:
        if s not in disc:
            errs.append(f"port_manifest.json:0 missing/renamed {s}")
    return errs, len(canonical_skills) + len(pre)
