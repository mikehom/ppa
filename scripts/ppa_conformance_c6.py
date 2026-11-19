#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic evaluators for CONFORMANCE_SPEC.md gates
#   C6 (lossless issue, refactor, backlog, and export manifest provenance) and
#   C2 (zero always-on prompt tax, DEV-STUB validation, undeclared-stub detection).
"""Gate evaluators C6 and C2 for scripts/verify_port_conformance.py."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from adapters import common
import issue_ctl
from ppa_conformance_c125 import CheckOutcome, ConformanceContext, _load_served_units, make_check
from ppa_conformance_scope import not_applicable
import ppa_artifact_rules as rules
import validate_ppa_knowledge as vpk

ISSUE_ID_RE = re.compile(r"\b(?:EPIC-\d{3}|ISS-W\d-\d{2}|REF-\d{3}|BKL-\d{3})\b")
REF_ID_RE = re.compile(r"\bREF-\d{3}\b")


def evaluate_gate_c6(ctx: ConformanceContext) -> list[CheckOutcome]:
    """Evaluate C6.1 through C6.10."""
    issues_map, c61_e, c62_e, n_files = _load_issues_for_c6(ctx.core_root)
    c63_e, c68_e, n_epics_shards = _check_c6_3_and_8(issues_map)
    c64_e, c65_e, c610_e, n_man = _check_c6_manifest_and_export(ctx, issues_map)
    c66_e, n_bkl = _check_c6_6_backlog_grounding(ctx, issues_map)
    c67_e, n_ptr = _check_c6_7_pointers(ctx, issues_map)
    c69_e, n_ref = _check_c6_9_refactor_trace(ctx.core_root)
    return [
        make_check("C6.1", n_files, c61_e, "C6_SCHEMA"),
        make_check("C6.2", n_files, c62_e, "C6_ID"),
        make_check("C6.3", len(issues_map), c63_e, "C6_REFERENCE"),
        make_check("C6.4", n_man, c64_e, "C6_MANIFEST_ORDER"),
        make_check("C6.5", n_man, c65_e, "C6_MANIFEST_LOSSY"),
        make_check("C6.6", n_bkl, c66_e, "C6_BACKLOG_UNGROUNDED"),
        make_check("C6.7", n_ptr, c67_e, "C6_POINTER"),
        make_check("C6.8", n_epics_shards, c68_e, "C6_BACKLOG_BLOCKS"),
        make_check("C6.9", n_ref, c69_e, "C6_REFACTOR_TRACE"),
        make_check("C6.10", n_man, c610_e, "C6_EXPORT_COUNT"),
    ]


def _load_issues_for_c6(root: Path) -> tuple[dict[str, issue_ctl.Issue], list[str], list[str], int]:
    issues_map: dict[str, issue_ctl.Issue] = {}
    schema_errs: list[str] = []
    id_errs: list[str] = []
    base = root / "issues"
    n_files = 0
    if not base.is_dir():
        return {}, ["issues:0 missing directory"], [], 0
    allowed = set(issue_ctl.DIR_RULES) | {"SCHEMA.md", "export_manifest.json"}
    for entry in sorted(base.iterdir()):
        if not entry.name.startswith(".") and entry.name not in allowed:
            schema_errs.append(f"{entry.relative_to(root).as_posix()}:0")
    for dirname in issue_ctl.DIR_RULES:
        dpath = base / dirname
        if not dpath.is_dir():
            continue
        for entry in sorted(dpath.iterdir()):
            if entry.name.startswith("."):
                continue
            n_files += 1
            rel = entry.relative_to(root).as_posix()
            if not entry.is_file() or entry.suffix != ".md":
                schema_errs.append(f"{rel}:0")
                continue
            iss = issue_ctl.load_issue(entry)
            if iss.meta:
                issue_ctl.check_fields(iss, dirname)
            for e in iss.errors:
                if "!=" in e and "file stem" in e:
                    id_errs.append(f"{rel}:1")
                else:
                    schema_errs.append(f"{rel}:1 ({e})")
            if iss.meta.get("id") != entry.stem:
                id_errs.append(f"{rel}:1")
            if iss.id in issues_map:
                id_errs.append(f"{rel}:1 (duplicate {iss.id})")
            issues_map[iss.id] = iss
    return issues_map, schema_errs, id_errs, n_files


def _check_c6_3_and_8(issues_map: dict[str, issue_ctl.Issue]) -> tuple[list[str], list[str], int]:
    ref_errs: list[str] = []
    bkl_block_errs: list[str] = []
    n_es = 0
    for iid, iss in sorted(issues_map.items()):
        meta = iss.meta
        itype = meta.get("issue_type")
        if itype in {"epic", "shard"}:
            n_es += 1
        refs = list(meta.get("depends_on") or []) + list(meta.get("blocks") or [])
        if meta.get("parent_issue"):
            refs.append(meta["parent_issue"])
        for ref in refs:
            if ref == iid or ref not in issues_map:
                ref_errs.append(f"issues/{iid}.md:1 ({ref})")
        for dep in meta.get("depends_on") or []:
            if dep in issues_map:
                if iid not in (issues_map[dep].meta.get("blocks") or []):
                    ref_errs.append(f"issues/{iid}.md:1 (asymmetric {dep})")
                if itype in {"epic", "shard"} and (
                    issues_map[dep].meta.get("issue_type") in {"contradiction", "edge_case"}
                    or str(dep).startswith("BKL-")
                ):
                    bkl_block_errs.append(f"issues/{iid}.md:1 (depends_on {dep})")
        for blk in meta.get("blocks") or []:
            if blk in issues_map and iid not in (issues_map[blk].meta.get("depends_on") or []):
                ref_errs.append(f"issues/{iid}.md:1 (asymmetric block {blk})")
    try:
        issue_ctl.topo_order(issues_map)
    except issue_ctl.IssueError as exc:
        ref_errs.append(f"issues:0 ({exc})")
    return ref_errs, bkl_block_errs, n_es


def _check_c6_manifest_and_export(
    ctx: ConformanceContext, issues_map: dict[str, issue_ctl.Issue]
) -> tuple[list[str], list[str], list[str], int]:
    mpath = ctx.core_root / "issues" / "export_manifest.json"
    if not mpath.is_file():
        err = ["issues/export_manifest.json:0 missing"]
        return err, err, err, 0
    doc, jerr = vpk.load_json(mpath)
    if jerr or not isinstance(doc, dict) or not isinstance(doc.get("issues"), list):
        err = [f"issues/export_manifest.json:1 ({jerr or 'invalid'})"]
        return err, err, err, 0
    entries = [e for e in doc["issues"] if isinstance(e, dict)]
    ids_in_order = [str(e.get("id", "")) for e in entries]
    pos_of = {iid: idx for idx, iid in enumerate(ids_in_order)}
    c64_e: list[str] = []
    if len(ids_in_order) != len(set(ids_in_order)) or set(ids_in_order) != set(issues_map):
        c64_e.append("issues/export_manifest.json:1 (issue set mismatch)")
    for idx, iid in enumerate(ids_in_order):
        iss = issues_map.get(iid)
        if iss is None:
            continue
        preds = [p for p in ([iss.meta.get("parent_issue")] + list(iss.meta.get("depends_on") or [])) if p]
        for pred in preds:
            if pos_of.get(pred, idx + 1) >= idx:
                c64_e.append(f"issues/export_manifest.json:1 ({iid} before {pred})")

    c65_e: list[str] = []
    for entry in entries:
        iid = str(entry.get("id", ""))
        iss = issues_map.get(iid)
        if iss is None:
            continue
        if json.dumps(entry.get("frontmatter"), sort_keys=True) != json.dumps(iss.meta, sort_keys=True):
            c65_e.append(f"issues/export_manifest.json:1 ({iid} frontmatter)")
        disk_txt, uerr = rules.read_text_strict(iss.path)
        src_body = entry.get("source_body")
        b_sha = entry.get("body_sha256")
        if (uerr or disk_txt is None or not isinstance(src_body, str)
                or hashlib.sha256(src_body.encode("utf-8")).hexdigest() != b_sha
                or issue_ctl.body_sha256(disk_txt) != b_sha):
            c65_e.append(f"issues/export_manifest.json:1 ({iid} body digest)")

    c610_e = _check_c6_10_external(ctx, entries, issues_map)
    return c64_e, c65_e, c610_e, len(entries)


def _check_c6_10_external(
    ctx: ConformanceContext, entries: list[dict], issues_map: dict[str, issue_ctl.Issue]
) -> list[str]:
    ext_records: list[dict] | None = None
    if ctx.external_export and ctx.external_export.is_file():
        ed, err = vpk.load_json(ctx.external_export)
        if err or not isinstance(ed, list):
            return [f"{ctx.external_export.name}:1"]
        ext_records = [r for r in ed if isinstance(r, dict)]
    gh_nums = [e.get("github_issue_number") for e in entries]
    any_gh = any(n is not None for n in gh_nums)
    if ext_records is None and not any_gh:
        return []
    errs: list[str] = []
    if ext_records is not None:
        if len(ext_records) != len(entries):
            errs.append("external_export:1 (count != manifest)")
        ext_by_id = {str(r.get("id", "")): r.get("external_number") for r in ext_records}
        if set(ext_by_id) != {str(e.get("id", "")) for e in entries}:
            errs.append("external_export:1 (canonical id mismatch)")
        nums = list(ext_by_id.values())
        if any(not isinstance(n, int) or n <= 0 for n in nums) or len(set(nums)) != len(nums):
            errs.append("external_export:1 (non-bijective external numbers)")
        for iid, num in ext_by_id.items():
            if iid in issues_map and issues_map[iid].meta.get("github_issue_number") != num:
                errs.append(f"issues/{iid}.md:1 (github_issue_number != {num})")
    elif any_gh:
        if any(not isinstance(n, int) or n <= 0 for n in gh_nums) or len(set(gh_nums)) != len(gh_nums):
            errs.append("issues/export_manifest.json:1 (partial or duplicate github_issue_number)")
    return errs


def _check_c6_6_backlog_grounding(
    ctx: ConformanceContext, issues_map: dict[str, issue_ctl.Issue]
) -> tuple[list[str], int]:
    pm = ctx.page_map
    known_concepts = {
        str(n.get("id")) for n in (ctx.core_graph or {}).get("concepts", [])
        if isinstance(n, dict) and n.get("id")
    }
    errs: list[str] = []
    bkl_count = 0
    for iid, iss in sorted(issues_map.items()):
        if iss.meta.get("issue_type") not in {"contradiction", "edge_case"} and not iid.startswith("BKL-"):
            continue
        bkl_count += 1
        txt, uerr = rules.read_text_strict(iss.path)
        rel = iss.path.relative_to(ctx.core_root).as_posix()
        if uerr or txt is None or pm is None:
            errs.append(f"{rel}:1")
            continue
        valid_cites = 0
        for _, raw_line in rules.strip_fences_and_frontmatter(txt):
            line = rules._mask_meta_code_spans(raw_line)  # pylint: disable=protected-access
            for m in rules.N8_RE.finditer(line):
                loc = m.group(1)
                pages = [m.group(3)] if m.group(2) else [m.group(5), m.group(6)]
                if all(rules.resolve_locator(loc, pg, pm) is None for pg in pages):
                    valid_cites += 1
        has_concept = any(cm.group(0) in known_concepts for cm in re.finditer(r"\bppa\.[a-z0-9.-]+\b", txt))
        if valid_cites == 0 or not has_concept:
            errs.append(f"{rel}:1 (cites={valid_cites}, concept={has_concept})")
    return errs, bkl_count


def _check_c6_7_pointers(
    ctx: ConformanceContext, issues_map: dict[str, issue_ctl.Issue]
) -> tuple[list[str], int]:
    k_files = common.sorted_files_under(ctx.core_root / "knowledge")
    errs: list[str] = []
    mentioned: set[str] = set()
    for kp in k_files:
        txt, uerr = rules.read_text_strict(kp)
        if uerr or txt is None:
            continue
        rel = kp.relative_to(ctx.core_root).as_posix()
        for lineno, line in enumerate(txt.split("\n"), start=1):
            for m in ISSUE_ID_RE.finditer(line):
                iid = m.group(0)
                mentioned.add(iid)
                if iid not in issues_map:
                    errs.append(f"{rel}:{lineno} ({iid})")
    gpath = ctx.core_root / "ontology" / "concept_graph.json"
    if gpath.is_file():
        gtxt, _ = rules.read_text_strict(gpath)
        if gtxt:
            mentioned.update(ISSUE_ID_RE.findall(gtxt))
    open_bkl = [
        iid for iid, iss in sorted(issues_map.items())
        if (iss.meta.get("issue_type") in {"contradiction", "edge_case"} or iid.startswith("BKL-"))
        and iss.meta.get("status") == "open"
    ]
    for bkl_id in open_bkl:
        if bkl_id not in mentioned:
            errs.append(f"issues/backlog/{bkl_id}.md:1 (unreferenced open backlog)")
    return errs, len(k_files) + len(open_bkl)


def _check_c6_9_refactor_trace(core_root: Path) -> tuple[list[str], int]:
    log_path = core_root / "ontology" / "altitude_alignment_log.md"
    ref_dir = core_root / "issues" / "refactors"
    file_ids = {p.stem for p in ref_dir.glob("REF-*.md")} if ref_dir.is_dir() else set()
    if not log_path.is_file():
        return ["ontology/altitude_alignment_log.md:0 missing"], len(file_ids)
    txt, uerr = rules.read_text_strict(log_path)
    if uerr or txt is None:
        return ["ontology/altitude_alignment_log.md:1"], 0
    log_ids = set(REF_ID_RE.findall(txt))
    diff = sorted(log_ids ^ file_ids)
    errs = [f"ontology/altitude_alignment_log.md:1 ({rid})" for rid in diff]
    return errs, len(log_ids | file_ids)


def _validate_dev_stub(ctx: ConformanceContext) -> tuple[bool, list[str]]:
    stub = ctx.dev_stub
    if stub is None:
        return False, []
    errs: list[str] = []
    surface = stub.get("surface", "")
    text = stub.get("text", "")
    lines = common.split_lines_n2(text)
    raw_len = len(text.encode("utf-8"))
    if not 1 <= len(lines) <= 12 or raw_len > 800:
        errs.append(f"{surface}:1 DEV-STUB size ({len(lines)}L, {raw_len}B)")
    if rules.RAW_PPA_RE.search(text) or vpk.RAW_BOOK_RE.search(text):
        errs.append(f"{surface}:1 DEV-STUB contains citation")
    if re.search(r"(?:^|\n)\s*\d+\.\s+\S", text) or "⊢" in text:
        errs.append(f"{surface}:1 DEV-STUB contains rule or numbered procedure")
    for tok in re.findall(r"`([^`\n]+\.md)`", text):
        if "*" not in tok and not (ctx.port_root / tok).is_file():
            errs.append(f"{surface}:1 DEV-STUB points to missing {tok}")
    return len(errs) == 0, errs


def _canonical_c2(ctx: ConformanceContext) -> list[CheckOutcome]:
    """Canonical-only C2: only C2.5 reads canonical data; surface checks need a port."""
    descs: list[str] = []
    c25_errs: list[str] = []
    for d in rules.skill_dirs(ctx.core_root):
        fm = rules.parse_frontmatter(rules.read_lines(d / "SKILL.md")) or {}
        desc = fm.get("description", "")
        descs.append(desc)
        if not 0 < len(desc) <= 1024 or rules.RAW_PPA_RE.search(desc) or re.search(r"(?:^|\s)\d+\.\s+\S", desc):
            c25_errs.append(f"{d.name}/SKILL.md:1")
    return [
        not_applicable("C2.1"),
        not_applicable("C2.2"),
        not_applicable("C2.3"),
        not_applicable("C2.4"),
        make_check("C2.5", len(descs), c25_errs, "C2_DESCRIPTION_BLOAT"),
        not_applicable("C2.6"),
    ]


def _stub_accounts_for_change(ctx: ConformanceContext, path_spec: str, sha_before: object) -> bool:
    """True when removing the declared stub text (present exactly once) restores the baseline."""
    stub = ctx.dev_stub
    if not stub or path_spec != stub.get("surface") or path_spec.startswith("~/"):
        return False
    surf_file = ctx.port_root / path_spec
    stub_bytes = stub["text"].encode("utf-8")
    raw_after = surf_file.read_bytes() if surf_file.is_file() else b""
    if not stub_bytes or raw_after.count(stub_bytes) != 1:
        return False
    remainder = raw_after.replace(stub_bytes, b"", 1)
    if sha_before is None:
        return remainder == b""
    return hashlib.sha256(remainder).hexdigest() == sha_before


def _undeclared_stub_errors(ctx: ConformanceContext, declared: list[str]) -> list[str]:
    """Surfaces that carry a pointer-stub marker with no DEV-STUB deviation naming them."""
    stub_surface = ctx.dev_stub.get("surface") if ctx.dev_stub else None
    errs: list[str] = []
    for path_spec in declared:
        hits = common.surface_stub_markers(ctx.port_root, path_spec, ctx.user_home)
        if hits and not ("DEV-STUB" in ctx.deviation_ids and path_spec == stub_surface):
            errs.append(f"{path_spec}:1 (pointer stub present without a DEV-STUB deviation)")
    return errs


def evaluate_gate_c2(ctx: ConformanceContext) -> list[CheckOutcome]:
    """Evaluate C2.1 through C2.6."""
    if ctx.canonical_only:
        return _canonical_c2(ctx)
    target = str(ctx.manifest.get("target", ""))
    req_min = set(common.MINIMUM_ALWAYS_ON_SURFACES.get(target, ()))
    declared_list = [s for s in ctx.manifest.get("always_on_surfaces", []) if isinstance(s, dict)]
    declared_map = {str(s.get("path", "")): s.get("sha256_before") for s in declared_list}
    c21_errs = [f"port_manifest.json:0 missing {m}" for m in sorted(req_min - set(declared_map))]
    if not req_min:
        c21_errs.append(f"port_manifest.json:0 unknown target {target!r}")

    stub_valid, stub_errs = _validate_dev_stub(ctx)
    undeclared = _undeclared_stub_errors(ctx, sorted(declared_map))
    c22_errs: list[str] = list(stub_errs)
    modified = 0
    for path_spec, sha_before in sorted(declared_map.items()):
        sha_after = common.compute_surface_sha256(ctx.port_root, path_spec, ctx.user_home)
        if sha_after == sha_before:
            continue
        if stub_valid and _stub_accounts_for_change(ctx, path_spec, sha_before):
            continue
        c22_errs.append(f"{path_spec}:1")
        modified += 1

    c23_errs, c23_n = _check_c2_3_installed(ctx, set(declared_map))
    c24_errs, c25_errs, c24_n = _check_c2_4_5_discovery(ctx)
    taxed = modified > 0 or bool(stub_errs) or bool(undeclared)
    c26_errs = [f"always_on_surfaces:1 (+{modified} modified, {len(undeclared)} undeclared stub)"] if taxed else []
    if undeclared:
        c22_out = CheckOutcome("C2.2", "FAIL", len(declared_map), "C2_UNDECLARED_DEVIATION",
                               (undeclared + c22_errs)[:20])
    else:
        c22_out = make_check("C2.2", len(declared_map), c22_errs, "C2_SURFACE_MODIFIED")
    return [
        make_check("C2.1", len(req_min | set(declared_map)), c21_errs, "C2_SURFACE_UNDECLARED"),
        c22_out,
        make_check("C2.3", c23_n, c23_errs, "C2_INSTALLED_ALWAYS_ON"),
        make_check("C2.4", c24_n, c24_errs, "C2_DISCOVERY_SET"),
        make_check("C2.5", c24_n, c25_errs, "C2_DESCRIPTION_BLOAT"),
        make_check("C2.6", len(declared_map), c26_errs, "C2_NONZERO_TAX"),
    ]


def _check_c2_3_installed(ctx: ConformanceContext, always_on_paths: set[str]) -> tuple[list[str], int]:
    installed = [
        str(p)
        for m in ctx.manifest.get("mappings", []) if isinstance(m, dict)
        for p in (m.get("port", []) if isinstance(m.get("port"), list) else [])
    ]
    forbidden_names = {"CLAUDE.md", "GEMINI.md", "AGENTS.md", ".cursorrules", "system_prompt.md"}
    errs: list[str] = []
    for rel in installed:
        p = ctx.port_root / rel
        if rel in always_on_paths or Path(rel).name in forbidden_names or rel.startswith("templates/default"):
            errs.append(f"{rel}:1")
        if p.suffix == ".mdc" and p.is_file():
            txt, uerr = rules.read_text_strict(p)
            if uerr or txt is None:
                errs.append(f"{rel}:1")
                continue
            meta, _ = rules.parse_frontmatter_strict(rules.split_lines_n2(txt))
            if not meta or meta.get("alwaysApply") != "false":
                errs.append(f"{rel}:1 (alwaysApply must be false)")
            if meta and meta.get("globs", "") in {"*", "**", "**/*"}:
                errs.append(f"{rel}:1 (catch-all globs forbidden)")
    return errs, len(installed)


def _check_c2_4_5_discovery(ctx: ConformanceContext) -> tuple[list[str], list[str], int]:
    skill_names = {d.name for d in rules.skill_dirs(ctx.core_root)}
    amb_dir = ctx.core_root / "knowledge" / "ambient-context"
    amb_stems = {p.stem for p in amb_dir.glob("ppa-*.md")} if amb_dir.is_dir() else set()
    amb_files = {p.name for p in amb_dir.glob("ppa-*.md")} if amb_dir.is_dir() else set()

    entries = [e for e in ctx.manifest.get("discovery_entries", []) if isinstance(e, dict)]
    names = [str(e.get("name", "")) for e in entries]
    name_set = set(names)
    c24_errs: list[str] = []
    if len(names) != len(name_set):
        c24_errs.append("port_manifest.json:0 duplicate discovery entry")
    valid_sets = (skill_names, skill_names | amb_stems, skill_names | amb_files)
    if name_set not in valid_sets:
        c24_errs.append(f"port_manifest.json:0 discovery set mismatch ({sorted(name_set ^ skill_names)})")

    port_descs = _collect_port_descriptions(ctx)
    c25_errs: list[str] = []
    for entry in entries:
        nm = str(entry.get("name", ""))
        chars = entry.get("description_chars")
        actual = port_descs.get(nm)
        if not isinstance(chars, int) or chars <= 0 or chars > 1024:
            c25_errs.append(f"port_manifest.json:0 ({nm} chars={chars})")
        if actual is None:
            c25_errs.append(f"port_manifest.json:0 ({nm} description not found)")
            continue
        if len(actual) != chars or len(actual) > 1024:
            c25_errs.append(f"{nm}:1 (description length {len(actual)} != {chars})")
        if rules.RAW_PPA_RE.search(actual) or re.search(r"(?:^|\s)\d+\.\s+\S", actual) or "⊢" in actual:
            c25_errs.append(f"{nm}:1 (description contains citation, list, or rule)")
    return c24_errs, c25_errs, len(entries)


def _collect_port_descriptions(ctx: ConformanceContext) -> dict[str, str]:
    out: dict[str, str] = {}
    served = _load_served_units(ctx)
    for m in ctx.manifest.get("mappings", []):
        if not isinstance(m, dict):
            continue
        c_rel = Path(str(m.get("canonical", "")))
        p_rels = m.get("port", [])
        if not isinstance(p_rels, list) or not p_rels:
            continue
        pr = str(p_rels[0])
        if pr in served:
            txt = served[pr]
        else:
            pp = ctx.port_root / pr
            if not pp.is_file():
                continue
            txt, err = rules.read_text_strict(pp)
            if err or txt is None:
                continue
        if c_rel.name == "SKILL.md":
            sname = c_rel.parent.name
            meta, _ = rules.parse_frontmatter_strict(rules.split_lines_n2(txt))
            if meta and "description" in meta:
                out[sname] = meta["description"]
            else:
                cm = re.search(r"<!--\s*summary:\s*(.*?)\s*-->", txt)
                if cm:
                    out[sname] = cm.group(1)
        elif len(c_rel.parts) == 3 and c_rel.parts[1] == "ambient-context":
            meta, _ = rules.parse_frontmatter_strict(rules.split_lines_n2(txt))
            if meta and "description" in meta:
                out.setdefault(c_rel.stem, meta["description"])
                out[c_rel.name] = meta["description"]
    return out
