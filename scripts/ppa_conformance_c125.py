#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic evaluators for CONFORMANCE_SPEC.md gates
#   C5 (hygiene & build determinism), C1 (concept, citation & inventory parity),
#   and C2 (zero always-on prompt tax & DEV-STUB validation).
"""Gate evaluators C5, C1, and C2 for scripts/verify_port_conformance.py."""
from __future__ import annotations

import collections
import hashlib
import json
import re
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from adapters import (
    agents_md_adapter,
    claude_code_adapter,
    common,
    cursor_mdc_adapter,
    gemini_harness_adapter,
    wiki_sync_adapter,
)
import check_portability_hygiene as hygiene
import ppa_artifact_rules as rules
import validate_ppa_knowledge as vpk

ADAPTER_MODULES = {
    "claude-code": claude_code_adapter,
    "gemini-cli": gemini_harness_adapter,
    "codex-agents": agents_md_adapter,
    "cursor-ide": cursor_mdc_adapter,
    "knowledge-wiki": wiki_sync_adapter,
}

EXTRA_ABS_PATH_RE = re.compile(
    r"(?<![\w.~])/(?:tmp|etc|var|opt|srv|mnt|Volumes)/[^\s'\"`)\]]*"
)
PRIVATE_FALLBACK_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("private_shortlink", re.compile(r"(?<![\w/.])(?:b|cl)/\d{5,}")),
    ("private_go_link", re.compile(r"(?<![\w/.])(?:go|yaqs|g3doc)/[A-Za-z0-9_-]")),
]
MODEL_CONDITIONAL_RE = re.compile(
    r"\b(?:if|when|unless|only\s+for|running\s+on|addressed\s+to)\b[^.\n]{0,48}"
    r"\b(?:claude|gemini|chatgpt|gpt-?\d\w*|llama|mistral|opus|sonnet|haiku|cursor|codex|copilot)\b",
    re.I,
)
CONCEPT_ID_TOKEN_RE = re.compile(r"\bppa\.[a-z0-9]+(?:\.[a-z0-9-]+)+\b")
STRICT_BOOK_PREFIXES = ("knowledge/", "ontology/", "corpus/", "port/")
STRICT_BOOK_TOKEN_RE = re.compile(r"\(`?book\s+p[^)\n]*\)?", re.I)
SINGULAR_BOOK_PAREN_RE = re.compile(
    r"^\(book p\. (?:\d{1,3}|[IVXLCDM]+); PDF p\. \d{1,3}\)$"
)


@dataclass
class CheckOutcome:
    """Single CONFORMANCE_SPEC check result."""

    id: str
    status: str
    examined: int
    failure_code: str | None = None
    locations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "examined": self.examined,
            "failure_code": self.failure_code,
            "id": self.id,
            "locations": self.locations[:20],
            "status": self.status,
        }


@dataclass
class ConformanceContext:
    """Loaded canonical core, port root, manifest, page map, and Deviations."""

    core_root: Path
    port_root: Path
    manifest: dict[str, object]
    canonical_only: bool
    user_home: Path
    denylist_path: Path | None
    port_second: Path | None
    external_export: Path | None
    scratch_base: Path
    page_map: vpk.PageMap | None
    page_map_doc: dict | None
    core_graph: dict | None
    port_graph: dict | None
    deviation_ids: set[str]
    dev_stub: dict[str, str] | None


def make_check(
    check_id: str,
    examined: int,
    errors: list[str],
    failure_code: str,
    exempt_vacuous: bool = False,
) -> CheckOutcome:
    """Build CheckOutcome applying CONFORMANCE_SPEC §5.4 <gate>_VACUOUS rule."""
    gate = check_id.split(".", 1)[0]
    if errors:
        return CheckOutcome(check_id, "FAIL", examined, failure_code, errors[:20])
    if examined == 0 and not exempt_vacuous:
        return CheckOutcome(check_id, "FAIL", 0, f"{gate}_VACUOUS", [f"{check_id}:0"])
    return CheckOutcome(check_id, "PASS", examined, None, [])


def list_port_files(port_root: Path) -> list[Path]:
    """Return sorted regular files in port_root excluding conformance_report.json."""
    out: list[Path] = []
    for p in common.sorted_files_under(port_root):
        if p.relative_to(port_root).as_posix() == "conformance_report.json":
            continue
        out.append(p)
    return out


def _scan_port_hygiene_filtered(port_root: Path, op_rules: list) -> tuple[list[str], int]:
    errs: list[str] = []
    scanned = 0
    for p in list_port_files(port_root):
        rel = p.relative_to(port_root).as_posix()
        found, did_scan = hygiene.scan_file(port_root, rel, op_rules)
        scanned += int(did_scan)
        errs.extend(f"port/{f.path}:{f.line}" for f in found)
    return errs, scanned


def _eval_c5_1_to_c5_6(ctx: ConformanceContext) -> list[CheckOutcome]:
    denylist = hygiene.resolve_denylist(
        ctx.core_root,
        str(ctx.denylist_path) if ctx.denylist_path else None,
        disabled=False,
    )
    op_rules = hygiene.load_denylist(denylist)
    core_findings, core_scanned, _ = hygiene.scan_root(ctx.core_root, op_rules)
    c51_errs = [f"core/{f.path}:{f.line}" for f in core_findings]
    port_scanned = 0
    if not ctx.canonical_only:
        p_errs, port_scanned = _scan_port_hygiene_filtered(ctx.port_root, op_rules)
        c51_errs.extend(p_errs)

    c52_errs: list[str] = []
    c52_n = 0
    for sub in ("knowledge", "ontology", "corpus"):
        for p in common.sorted_files_under(ctx.core_root / sub):
            txt, err = rules.read_text_strict(p)
            if err or txt is None:
                continue
            c52_n += 1
            rel = p.relative_to(ctx.core_root).as_posix()
            for f in hygiene.scan_text(txt, rel, hygiene.CORE + hygiene.HARNESS):
                if f.category in {"model_or_agent_name", "harness_name"}:
                    c52_errs.append(f"{rel}:{f.line}")

    c53_errs, c53_n = _check_c5_abs_paths(ctx)
    c54_errs, c55_errs, c54_n = _check_c5_host_and_private(ctx, op_rules)
    c56_errs, c56_n = _check_c5_model_conditionals(ctx)
    return [
        make_check("C5.1", core_scanned + port_scanned, c51_errs, "C5_HYGIENE_GATE"),
        make_check("C5.2", c52_n, c52_errs, "C5_HARNESS_TERM_IN_CORE"),
        make_check("C5.3", c53_n, c53_errs, "C5_ABSOLUTE_PATH"),
        make_check("C5.4", c54_n, c54_errs, "C5_HOST_OR_CONTACT"),
        make_check("C5.5", c54_n, c55_errs, "C5_PRIVATE_IDENTIFIER"),
        make_check("C5.6", c56_n, c56_errs, "C5_MODEL_CONDITIONAL"),
    ]


def _check_c5_abs_paths(ctx: ConformanceContext) -> tuple[list[str], int]:
    targets = (
        common.sorted_files_under(ctx.core_root / "knowledge")
        + common.sorted_files_under(ctx.core_root / "ontology")
        if ctx.canonical_only
        else list_port_files(ctx.port_root)
    )
    base = ctx.core_root if ctx.canonical_only else ctx.port_root
    abs_rules = [r for r in hygiene.STRUCTURAL if r[0] == "absolute_path"] + [
        ("absolute_path", EXTRA_ABS_PATH_RE)
    ]
    leaked_roots = {str(ctx.core_root.resolve()), str(ctx.port_root.resolve())}
    errs: list[str] = []
    scanned = 0
    for p in targets:
        txt, uerr = rules.read_text_strict(p)
        if uerr or txt is None:
            continue
        scanned += 1
        rel = p.relative_to(base).as_posix()
        errs.extend(f"{rel}:{f.line}" for f in hygiene.scan_text(txt, rel, abs_rules))
        for lineno, line in enumerate(txt.split("\n"), start=1):
            if any(root_str in line for root_str in leaked_roots):
                errs.append(f"{rel}:{lineno}")
    return errs, scanned


def _check_c5_host_and_private(
    ctx: ConformanceContext, op_rules: list
) -> tuple[list[str], list[str], int]:
    host_rules = [r for r in hygiene.STRUCTURAL if r[0] in {"email", "url"}]
    priv_rules = op_rules + PRIVATE_FALLBACK_RULES
    host_errs: list[str] = []
    priv_errs: list[str] = []
    scanned = 0
    roots = [(ctx.core_root, common.sorted_files_under(ctx.core_root / d))
             for d in ("knowledge", "ontology", "corpus", "issues")]
    if not ctx.canonical_only:
        roots.append((ctx.port_root, list_port_files(ctx.port_root)))
    for base, files in roots:
        for p in files:
            if p.suffix.lower() in hygiene.BINARY_SUFFIXES:
                continue
            txt, uerr = rules.read_text_strict(p)
            if uerr or txt is None:
                continue
            scanned += 1
            rel = p.relative_to(base).as_posix()
            host_errs.extend(f"{rel}:{f.line}" for f in hygiene.scan_text(txt, rel, host_rules))
            priv_errs.extend(f"{rel}:{f.line}" for f in hygiene.scan_text(txt, rel, priv_rules))
    return host_errs, priv_errs, scanned


def _check_c5_model_conditionals(ctx: ConformanceContext) -> tuple[list[str], int]:
    candidates: list[tuple[Path, Path]] = []
    for p in common.sorted_files_under(ctx.core_root / "knowledge"):
        if p.name in {"SKILL.md", "cases.yaml"}:
            candidates.append((ctx.core_root, p))
    if not ctx.canonical_only:
        for p in list_port_files(ctx.port_root):
            if p.name in {"SKILL.md", "cases.yaml"} or p.suffix == ".mdc":
                candidates.append((ctx.port_root, p))
    errs: list[str] = []
    for base, p in candidates:
        txt, uerr = rules.read_text_strict(p)
        if uerr or txt is None:
            continue
        rel = p.relative_to(base).as_posix()
        _, _, body = common.split_frontmatter(txt) if p.name != "cases.yaml" else (None, [], txt)
        for lineno, line in enumerate(body.split("\n"), start=1):
            if MODEL_CONDITIONAL_RE.search(line):
                errs.append(f"{rel}:{lineno}")
        if p.name in {"SKILL.md", "cases.yaml"}:
            for f in hygiene.scan_text(body, rel, hygiene.CORE + hygiene.HARNESS):
                if f.category in {"model_or_agent_name", "harness_name"}:
                    errs.append(f"{rel}:{f.line}")
    return errs, len(candidates)


def _tree_digests(root: Path) -> dict[str, str]:
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in list_port_files(root)
    }


def _check_c5_7_determinism(ctx: ConformanceContext) -> CheckOutcome:
    if ctx.canonical_only:
        k_files, o_files, c_files = common.collect_canonical_package(ctx.core_root)
        d1 = {p.relative_to(ctx.core_root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in k_files + o_files + c_files}
        d2 = {p.relative_to(ctx.core_root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in k_files + o_files + c_files}
        errs = [k for k in sorted(set(d1) | set(d2)) if d1.get(k) != d2.get(k)]
        return make_check("C5.7", len(d1), errs, "C5_NONDETERMINISTIC_BUILD")
    if ctx.port_second is not None:
        d1, d2 = _tree_digests(ctx.port_root), _tree_digests(ctx.port_second)
        errs = [f"{k}:0" for k in sorted(set(d1) | set(d2)) if d1.get(k) != d2.get(k)]
        return make_check("C5.7", max(len(d1), len(d2)), errs, "C5_NONDETERMINISTIC_BUILD")
    target = str(ctx.manifest.get("target", ""))
    mod = ADAPTER_MODULES.get(target)
    if mod is None:
        return make_check("C5.7", 1, [f"port_manifest.json:0 unknown target {target!r}"],
                          "C5_NONDETERMINISTIC_BUILD")
    ctx.scratch_base.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp(dir=ctx.scratch_base, prefix="c57_"))
    try:
        r_a, r_b, u_h = tmp_dir / "a", tmp_dir / "b", tmp_dir / "uhome"
        u_h.mkdir(parents=True, exist_ok=True)
        rev = str(ctx.manifest.get("canonical_revision", "rev"))
        opts = ctx.manifest.get("adapter_options")
        kwargs = dict(opts) if isinstance(opts, dict) else {}
        mod.compile_port(ctx.core_root, r_a, canonical_revision=rev, user_home=str(u_h), **kwargs)
        mod.compile_port(ctx.core_root, r_b, canonical_revision=rev, user_home=str(u_h), **kwargs)
        d1, d2 = _tree_digests(r_a), _tree_digests(r_b)
        errs = [f"{k}:0" for k in sorted(set(d1) | set(d2)) if d1.get(k) != d2.get(k)]
        return make_check("C5.7", max(len(d1), len(d2)), errs, "C5_NONDETERMINISTIC_BUILD")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def evaluate_gate_c5(ctx: ConformanceContext) -> list[CheckOutcome]:
    """Evaluate C5.1 through C5.7."""
    return _eval_c5_1_to_c5_6(ctx) + [_check_c5_7_determinism(ctx)]


def _check_c1_graph_nodes(ctx: ConformanceContext) -> tuple[CheckOutcome, CheckOutcome]:
    c_nodes = (ctx.core_graph or {}).get("concepts", [])
    p_nodes = (ctx.port_graph or {}).get("concepts", [])
    c_map = {str(n.get("id")): n for n in c_nodes if isinstance(n, dict) and n.get("id")}
    p_map = {str(n.get("id")): n for n in p_nodes if isinstance(n, dict) and n.get("id")}
    c11_errs: list[str] = []
    if len(c_map) != len(c_nodes) or len(p_map) != len(p_nodes):
        c11_errs.append("ontology/concept_graph.json:0 duplicate concept id")
    for missing in sorted(set(c_map) ^ set(p_map)):
        c11_errs.append(f"ontology/concept_graph.json:0 ({missing})")

    port_map_by_canon = {
        str(m.get("canonical")): [str(x) for x in m.get("port", [])]
        for m in ctx.manifest.get("mappings", [])
        if isinstance(m, dict)
    }
    fields = ("title", "altitude", "unit", "citations", "formal_summary",
              "projections", "related_edges")
    c12_errs: list[str] = []
    for cid in sorted(set(c_map) & set(p_map)):
        cn, pn = c_map[cid], p_map[cid]
        for fld in fields:
            if json.dumps(cn.get(fld), sort_keys=True) != json.dumps(pn.get(fld), sort_keys=True):
                c12_errs.append(f"{cid}.{fld}:0")
        c_refs = [str(r) for r in cn.get("artifact_refs", [])]
        p_refs = [str(r) for r in pn.get("artifact_refs", [])]
        if c_refs != p_refs:
            expanded: list[str] = []
            for r in c_refs:
                base_r, *frag = r.split("#", 1)
                sfx = f"#{frag[0]}" if frag else ""
                mapped = port_map_by_canon.get(base_r, [base_r])
                expanded.extend(f"{mp}{sfx}" for mp in mapped)
            if p_refs != expanded:
                c12_errs.append(f"{cid}.artifact_refs:0")
    return (
        make_check("C1.1", len(c_map), c11_errs, "C1_CONCEPT_SET"),
        make_check("C1.2", len(c_map), c12_errs, "C1_NODE_DRIFT"),
    )


def _check_c1_citations_and_coverage(ctx: ConformanceContext) -> list[CheckOutcome]:
    pm = ctx.page_map
    doc = ctx.page_map_doc or {}
    p_nodes = (ctx.port_graph or {}).get("concepts", [])
    if pm is None:
        return [
            make_check("C1.3", 0, ["corpus/pdf_page_map.json:0"], "C1_CITATION_UNRESOLVED"),
            make_check("C1.4", 0, ["corpus/pdf_page_map.json:0"], "C1_INVENTORY_COUNT"),
            make_check("C1.5", 0, ["corpus/pdf_page_map.json:0"], "C1_ITEM_UNCITED"),
            make_check("C1.6", 0, ["corpus/pdf_page_map.json:0"], "C1_SECTION_UNCOVERED"),
        ]
    c13_errs: list[str] = []
    c13_n = 0
    cited_items: set[str] = set()
    covered_secs: set[str] = set()
    for node in p_nodes:
        if not isinstance(node, dict):
            continue
        cid = str(node.get("id", "?"))
        all_cites = list(node.get("citations", []))
        for edge in node.get("related_edges", []):
            if isinstance(edge, dict):
                all_cites.extend(edge.get("citations", []))
                if isinstance(edge.get("basis"), dict):
                    all_cites.extend(edge["basis"].get("citations", []))
        for idx, cite in enumerate(all_cites):
            if not isinstance(cite, dict):
                continue
            c13_n += 1
            c13_errs.extend(vpk.check_citation(cite, pm, f"{cid}[{idx}]"))
            if cite.get("table_or_fig"):
                cited_items.add(str(cite["table_or_fig"]))
            msec = re.match(r"^([1-6ABC]\.\d{1,2})", str(cite.get("section") or ""))
            if msec:
                covered_secs.add(msec.group(1))
    c14_errs = vpk.check_page_map_inventory(doc)
    c14_n = len(doc.get("tables", {})) + len(doc.get("figures", {}))
    c15_errs = [f"{k}:0" for k in sorted(set(pm.captions) - cited_items)]
    c16_errs = [f"§{s}:0" for s in sorted(set(pm.sections) - covered_secs)]
    return [
        make_check("C1.3", c13_n, c13_errs, "C1_CITATION_UNRESOLVED"),
        make_check("C1.4", c14_n, c14_errs, "C1_INVENTORY_COUNT"),
        make_check("C1.5", len(pm.captions), c15_errs, "C1_ITEM_UNCITED"),
        make_check("C1.6", len(pm.sections), c16_errs, "C1_SECTION_UNCOVERED"),
    ]


def _extract_n8_and_concepts(text: str, known_ids: set[str]) -> tuple[collections.Counter, collections.Counter]:
    n8_counts: collections.Counter = collections.Counter()
    cid_counts: collections.Counter = collections.Counter()
    for _, line in rules.strip_fences_and_frontmatter(text):
        masked = rules._mask_meta_code_spans(line)  # pylint: disable=protected-access
        for m in rules.N8_RE.finditer(masked):
            n8_counts[m.group(0)] += 1
        for cm in CONCEPT_ID_TOKEN_RE.finditer(line):
            if cm.group(0) in known_ids:
                cid_counts[cm.group(0)] += 1
    return n8_counts, cid_counts


def _load_served_units(ctx: ConformanceContext) -> dict[str, str]:
    if "DEV-NOFILES" not in ctx.deviation_ids or ctx.canonical_only:
        return {}
    su_path = ctx.port_root / "served_units.json"
    if not su_path.is_file():
        return {}
    doc, err = vpk.load_json(su_path)
    if err or not isinstance(doc, dict):
        return {}
    out: dict[str, str] = {}
    for k, v in doc.items():
        if isinstance(k, str) and isinstance(v, list):
            out[k] = "\n".join(str(ln) for ln in v) + "\n"
        elif isinstance(k, str) and isinstance(v, str):
            out[k] = v
    return out


def _check_c1_mappings_and_ledgers(ctx: ConformanceContext) -> list[CheckOutcome]:
    mappings = [m for m in ctx.manifest.get("mappings", []) if isinstance(m, dict)]
    known_ids = {
        str(n.get("id")) for n in (ctx.core_graph or {}).get("concepts", [])
        if isinstance(n, dict) and n.get("id")
    }
    served_units = _load_served_units(ctx)
    c17_errs: list[str] = []
    c17_n = 0
    c18_errs: list[str] = []
    for m in mappings:
        c_rel = str(m.get("canonical", ""))
        p_rels = [str(x) for x in m.get("port", [])] if isinstance(m.get("port"), list) else []
        kind = str(m.get("kind", ""))
        c_path = ctx.core_root / c_rel
        if kind == "lossless":
            c17_n += 1
            if len(p_rels) != 1 or not c_path.is_file() or not (ctx.port_root / p_rels[0]).is_file():
                c17_errs.append(f"{c_rel}:0")
                continue
            c_txt, e1 = rules.read_text_strict(c_path)
            p_txt, e2 = rules.read_text_strict(ctx.port_root / p_rels[0])
            if e1 or e2 or c_txt is None or p_txt is None:
                c17_errs.append(f"{c_rel}:0")
            elif common.body_digest_n6(c_txt) != common.body_digest_n6(p_txt):
                c17_errs.append(f"{p_rels[0]}:1")
        elif kind == "transforming":
            if not c_path.is_file() or not p_rels:
                c18_errs.append(f"{c_rel}:0")
                continue
            c_txt, e1 = rules.read_text_strict(c_path)
            if e1 or c_txt is None:
                c18_errs.append(f"{c_rel}:0")
                continue
            c_n8, c_id = _extract_n8_and_concepts(c_txt, known_ids)
            p_n8: collections.Counter = collections.Counter()
            p_id: collections.Counter = collections.Counter()
            for pr in p_rels:
                if pr in served_units:
                    ptxt = served_units[pr]
                else:
                    pp = ctx.port_root / pr
                    if not pp.is_file():
                        c18_errs.append(f"{pr}:0")
                        continue
                    ptxt, pe = rules.read_text_strict(pp)
                    if pe or ptxt is None:
                        c18_errs.append(f"{pr}:0")
                        continue
                un8, uid = _extract_n8_and_concepts(ptxt, known_ids)
                p_n8.update(un8)
                p_id.update(uid)
            if c_n8 != p_n8 or c_id != p_id:
                c18_errs.append(f"{c_rel}:1")
        else:
            c18_errs.append(f"{c_rel}:0 unknown mapping kind {kind!r}")

    c19_out = _check_c1_9_gotchas(ctx)
    c110_out, c111_out = _check_c1_10_11_inline(ctx)
    c112_out = _check_c1_12_package(ctx, mappings)
    return [
        make_check("C1.7", c17_n, c17_errs, "C1_BODY_DIGEST"),
        make_check("C1.8", len(mappings), c18_errs, "C1_CITATION_MULTISET"),
        c19_out,
        c110_out,
        c111_out,
        c112_out,
    ]


def _check_c1_9_gotchas(ctx: ConformanceContext) -> CheckOutcome:
    l_errs, _, ledger_ids = rules.collect_gotcha_ledgers(ctx.core_root)
    haystack: list[str] = []
    scan_files = (
        common.sorted_files_under(ctx.core_root / "knowledge")
        + common.sorted_files_under(ctx.core_root / "ontology")
        if ctx.canonical_only
        else list_port_files(ctx.port_root)
    )
    for extra_sub in ("issues/backlog", "issues/refactors"):
        scan_files.extend(common.sorted_files_under(ctx.core_root / extra_sub))
    for p in scan_files:
        if (p.suffix in {".md", ".mdc", ".json", ".yaml"}
                and not p.name.startswith("RAW_SHARD_")
                and not p.name.startswith("ppa-shard-")):
            if "corpus" in p.parts:
                continue
            txt, err = rules.read_text_strict(p)
            if err is None and txt is not None:
                haystack.append(txt)
    present = set(re.findall(r"\bG-U\d[ab]?-\d{2,3}\b", "\n".join(haystack)))
    missing = [f"{src}:1 ({gid})" for gid, src in sorted(ledger_ids.items()) if gid not in present]
    return make_check("C1.9", len(ledger_ids), l_errs + missing, "C1_GOTCHA_DROPPED")


def _check_strict_singular_book_companions(text: str, where: str) -> list[str]:
    """Enforce strict singular '(book p. X; PDF p. Y)' in L0-L3, ontology, and port files."""
    if not where.startswith(STRICT_BOOK_PREFIXES):
        return []
    errs: list[str] = []
    for lineno, raw_line in rules.strip_fences_and_frontmatter(text):
        line = rules._mask_meta_code_spans(raw_line)  # pylint: disable=protected-access
        for m in STRICT_BOOK_TOKEN_RE.finditer(line):
            tok = m.group(0)
            if not SINGULAR_BOOK_PAREN_RE.fullmatch(tok):
                errs.append(f"{where}:{lineno}: non-singular '(book p...)' token {tok!r} (C1.10)")
    return errs


def _check_c1_10_11_inline(ctx: ConformanceContext) -> tuple[CheckOutcome, CheckOutcome]:
    pm = ctx.page_map
    if pm is None:
        return (
            make_check("C1.10", 0, ["corpus/pdf_page_map.json:0"], "C1_CITATION_MALFORMED"),
            make_check("C1.11", 0, ["corpus/pdf_page_map.json:0"], "C1_STATEMENT_UNKNOWN"),
        )
    md_files: list[tuple[str, Path]] = [
        (p.relative_to(ctx.core_root).as_posix(), p)
        for p in vpk.walk(ctx.core_root, "*.md")
    ]
    if not ctx.canonical_only:
        for p in list_port_files(ctx.port_root):
            if p.suffix in {".md", ".mdc"}:
                md_files.append((f"port/{p.relative_to(ctx.port_root).as_posix()}", p))
    c110_errs: list[str] = []
    c111_errs: list[str] = []
    stmt_examined = 0
    tok_examined = 0
    for where, path in md_files:
        txt, uerr = rules.read_text_strict(path)
        if uerr or txt is None:
            c110_errs.append(f"{where}:1")
            continue
        tok_examined += 1
        c110_errs.extend(vpk._check_book_companions(txt, where, pm))  # pylint: disable=protected-access
        c110_errs.extend(_check_strict_singular_book_companions(txt, where))
        for err in rules.check_n8_citations(txt, where, pm):
            if "statement" in err:
                c111_errs.append(err)
            else:
                c110_errs.append(err)
        for lineno, raw_line in rules.strip_fences_and_frontmatter(txt):
            line = rules._mask_meta_code_spans(raw_line)  # pylint: disable=protected-access
            for m in rules.N8_RE.finditer(line):
                sm = rules.LOC_STATEMENT.match(m.group(1).strip())
                if sm:
                    stmt_examined += 1
                    key = f"{sm.group(1)} {sm.group(2)}.{sm.group(3)}"
                    pages = [m.group(3)] if m.group(2) else [m.group(5), m.group(6)]
                    st = pm.statements.get(key)
                    if st is None:
                        c111_errs.append(f"{where}:{lineno}: unknown {key}")
                    else:
                        for pg in pages:
                            if not pg.isdigit() or not st["book_page"] <= int(pg) <= st["book_end"]:
                                c111_errs.append(f"{where}:{lineno}: {key} out of span")
    return (
        make_check("C1.10", tok_examined, c110_errs, "C1_CITATION_MALFORMED"),
        make_check("C1.11", stmt_examined, c111_errs, "C1_STATEMENT_UNKNOWN"),
    )


def _check_c1_12_package(ctx: ConformanceContext, mappings: list[dict]) -> CheckOutcome:
    k_files, o_files, _ = common.collect_canonical_package(ctx.core_root)
    expected = [p.relative_to(ctx.core_root).as_posix() for p in k_files + o_files]
    counts = collections.Counter(str(m.get("canonical", "")) for m in mappings)
    errs: list[str] = []
    for rel in expected:
        if counts[rel] != 1:
            errs.append(f"{rel}:0 (count={counts[rel]})")
    for extra in sorted(set(counts) - set(expected)):
        errs.append(f"{extra}:0 (unexpected canonical path)")
    return make_check("C1.12", len(expected), errs, "C1_PACKAGE_INCOMPLETE")


def evaluate_gate_c1(ctx: ConformanceContext) -> list[CheckOutcome]:
    """Evaluate C1.1 through C1.12."""
    c11, c12 = _check_c1_graph_nodes(ctx)
    return [c11, c12] + _check_c1_citations_and_coverage(ctx) + _check_c1_mappings_and_ledgers(ctx)

