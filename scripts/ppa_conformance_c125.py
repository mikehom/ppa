#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic evaluators for CONFORMANCE_SPEC.md gates
#   C5 (hygiene & build determinism) and C1 (concept, citation & inventory
#   parity), scoped to the files the port manifest owns.
"""Gate evaluators C5 and C1 for scripts/verify_port_conformance.py."""
from __future__ import annotations

import collections
import hashlib
import inspect
import json
import re
import shutil
import tempfile
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
import ppa_conformance_parity as parity
import validate_ppa_knowledge as vpk
from ppa_conformance_scope import (  # noqa: F401  (re-exported for the other gate modules)
    CheckOutcome,
    ConformanceContext,
    make_check,
    merged_paths,
    not_applicable,
    resolve_owned_files,
)

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


def list_port_files(ctx: ConformanceContext) -> list[Path]:
    """Sorted regular files the port manifest owns (foreign files are never read)."""
    return list(ctx.port_files)


def _scan_port_hygiene_filtered(ctx: ConformanceContext, op_rules: list) -> tuple[list[str], int]:
    errs: list[str] = []
    scanned = 0
    for p in list_port_files(ctx):
        rel = p.relative_to(ctx.port_root).as_posix()
        found, did_scan = hygiene.scan_file(ctx.port_root, rel, op_rules)
        scanned += int(did_scan)
        errs.extend(f"port/{f.path}:{f.line}" for f in found)
    return errs, scanned


def _c5_1_outcome(ctx: ConformanceContext, examined: int, errs: list[str]) -> CheckOutcome:
    """C5.1 with structured findings for symlinks or unsafe paths among owned port files."""
    if ctx.symlink_errors:
        return CheckOutcome("C5.1", "FAIL", examined, "C5_SYMLINK_FORBIDDEN", ctx.symlink_errors[:20])
    if ctx.path_errors:
        return CheckOutcome("C5.1", "FAIL", examined, "C5_OWNED_PATH_INVALID", ctx.path_errors[:20])
    return make_check("C5.1", examined, errs, "C5_HYGIENE_GATE")


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
        p_errs, port_scanned = _scan_port_hygiene_filtered(ctx, op_rules)
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
        _c5_1_outcome(ctx, core_scanned + port_scanned, c51_errs),
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
        else list_port_files(ctx)
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
        roots.append((ctx.port_root, list_port_files(ctx)))
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
        for p in list_port_files(ctx):
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


def _tree_digests(root: Path, with_merged: bool = False) -> tuple[dict[str, str], set[str]]:
    """Digests of the files a port root's own manifest owns, plus its merged-file set."""
    doc, err = vpk.load_json(root / "port_manifest.json")
    manifest = doc if (not err and isinstance(doc, dict)) else {}
    files, _, _ = resolve_owned_files(root, manifest)
    merged = set(merged_paths(manifest))
    if with_merged:
        files = files + [root / rel for rel in sorted(merged) if (root / rel).is_file()]
    digests = {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files
    }
    return digests, merged


def _digest_diff(d1: dict[str, str], d2: dict[str, str], skip: set[str], label: str) -> list[str]:
    keys = (set(d1) | set(d2)) - skip
    return [f"{k}:0 ({label})" for k in sorted(keys) if d1.get(k) != d2.get(k)]


def _rebuild_and_compare(ctx: ConformanceContext, mod) -> CheckOutcome:
    """Compile the reference adapter twice; compare the builds with each other and the port."""
    opts = ctx.manifest.get("adapter_options")
    kwargs = dict(opts) if isinstance(opts, dict) else {}
    accepted = set(inspect.signature(mod.compile_port).parameters)
    unknown = sorted(set(kwargs) - accepted)
    if unknown:
        return make_check("C5.7", len(ctx.port_files), [f"port_manifest.json:0 unknown adapter_options {unknown}"],
                          "C5_NONDETERMINISTIC_BUILD")
    ctx.scratch_base.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp(dir=ctx.scratch_base, prefix="c57_"))
    try:
        r_a, r_b, u_h = tmp_dir / "a", tmp_dir / "b", tmp_dir / "uhome"
        u_h.mkdir(parents=True, exist_ok=True)
        rev = str(ctx.manifest.get("canonical_revision", "rev"))
        try:
            mod.compile_port(ctx.core_root, r_a, canonical_revision=rev, user_home=str(u_h), **kwargs)
            mod.compile_port(ctx.core_root, r_b, canonical_revision=rev, user_home=str(u_h), **kwargs)
        except common.AdapterError as exc:
            return make_check("C5.7", len(ctx.port_files), [f"port_manifest.json:0 reference rebuild failed: {exc}"],
                              "C5_NONDETERMINISTIC_BUILD")
        d_a, merged_a = _tree_digests(r_a, with_merged=True)
        d_b, _ = _tree_digests(r_b, with_merged=True)
        errs = _digest_diff(d_a, d_b, set(), "two reference builds differ")
        d_a_owned, _ = _tree_digests(r_a)
        d_port = {
            p.relative_to(ctx.port_root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in list_port_files(ctx)
        }
        skip = {"port_manifest.json"} | merged_a | set(ctx.merged_files)
        errs += _digest_diff(d_a_owned, d_port, skip, "port differs from a fresh reference build")
        return make_check("C5.7", max(len(d_a), len(d_port)), errs, "C5_NONDETERMINISTIC_BUILD")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _check_c5_7_determinism(ctx: ConformanceContext) -> CheckOutcome:
    if ctx.canonical_only:
        return not_applicable("C5.7")
    if ctx.port_second is not None:
        d1 = {
            p.relative_to(ctx.port_root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in list_port_files(ctx)
        }
        d2, merged2 = _tree_digests(ctx.port_second)
        errs = _digest_diff(d1, d2, set(ctx.merged_files) | merged2, "the two builds differ")
        return make_check("C5.7", max(len(d1), len(d2)), errs, "C5_NONDETERMINISTIC_BUILD")
    target = str(ctx.manifest.get("target", ""))
    mod = ADAPTER_MODULES.get(target)
    if mod is None:
        return make_check(
            "C5.7", len(ctx.port_files),
            [f"port_manifest.json:0 target {target!r} has no reference adapter: compile the port "
             "a second time into another root and pass --port-second <dir>"],
            "C5_NONDETERMINISTIC_BUILD")
    return _rebuild_and_compare(ctx, mod)


def evaluate_gate_c5(ctx: ConformanceContext) -> list[CheckOutcome]:
    """Evaluate C5.1 through C5.7."""
    return _eval_c5_1_to_c5_6(ctx) + [_check_c5_7_determinism(ctx)]


def _check_c1_graph_nodes(ctx: ConformanceContext) -> tuple[CheckOutcome, CheckOutcome]:
    if ctx.canonical_only:
        return not_applicable("C1.1"), not_applicable("C1.2")
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


def _read_port_units(
    ctx: ConformanceContext, p_rels: list[str], served: dict[str, str], errs: list[str]
) -> list[str]:
    """Texts of the port units of one mapping; unreadable or missing units are findings."""
    texts: list[str] = []
    for pr in p_rels:
        if pr in served:
            texts.append(served[pr])
            continue
        pp = ctx.port_root / pr
        ptxt, pe = rules.read_text_strict(pp) if pp.is_file() else (None, "missing")
        if pe or ptxt is None:
            errs.append(f"{pr}:0")
        else:
            texts.append(ptxt)
    return texts


def _check_c1_8_transforming(
    ctx: ConformanceContext, mappings: list[dict], served: dict[str, str]
) -> tuple[list[str], list[str], int]:
    """C1.8 on transforming mappings: (multiset findings, lost-line findings, mappings examined)."""
    known_ids = {
        str(n.get("id")) for n in (ctx.core_graph or {}).get("concepts", [])
        if isinstance(n, dict) and n.get("id")
    }
    multiset_errs: list[str] = []
    loss_errs: list[str] = []
    examined = 0
    for m in mappings:
        kind = str(m.get("kind", ""))
        c_rel = str(m.get("canonical", ""))
        if kind == "lossless":
            continue
        if kind != "transforming":
            multiset_errs.append(f"{c_rel}:0 unknown mapping kind {kind!r}")
            continue
        examined += 1
        p_rels = [str(x) for x in m.get("port", [])] if isinstance(m.get("port"), list) else []
        c_path = ctx.core_root / c_rel
        c_txt, e1 = rules.read_text_strict(c_path) if c_path.is_file() else (None, "missing")
        if e1 or c_txt is None or not p_rels:
            multiset_errs.append(f"{c_rel}:0")
            continue
        texts = _read_port_units(ctx, p_rels, served, multiset_errs)
        c_n8, c_id = _extract_n8_and_concepts(c_txt, known_ids)
        p_n8: collections.Counter = collections.Counter()
        p_id: collections.Counter = collections.Counter()
        for ptxt in texts:
            un8, uid = _extract_n8_and_concepts(ptxt, known_ids)
            p_n8.update(un8)
            p_id.update(uid)
        if c_n8 != p_n8 or c_id != p_id:
            multiset_errs.append(f"{c_rel}:1")
        loss_errs.extend(parity.containment_errors(c_rel, c_txt, texts))
    return multiset_errs, loss_errs, examined


def _check_c1_8_cards(ctx: ConformanceContext, served: dict[str, str]) -> tuple[list[str], int]:
    """ARCHITECTURE 7.1 parity of every compiled concept card the manifest declares."""
    declared = ctx.manifest.get("concept_cards")
    cards = {str(k): str(v) for k, v in declared.items()} if isinstance(declared, dict) else {}
    nodes = {
        str(n.get("id")): n for n in (ctx.core_graph or {}).get("concepts", [])
        if isinstance(n, dict) and n.get("id")
    }
    errs: list[str] = []
    card_units = set(cards.values())
    owned = [p.relative_to(ctx.port_root).as_posix() for p in ctx.port_files] + sorted(served)
    for unit in owned:
        if unit.rsplit("/", 1)[-1].startswith("ppa-node-") and unit not in card_units:
            errs.append(f"{unit}:0 (concept card not declared in concept_cards)")
    if cards and set(cards) != set(nodes):
        errs.append(f"port_manifest.json:0 concept_cards covers {len(cards)} of {len(nodes)} concepts")
    for cid, unit in sorted(cards.items()):
        if cid not in nodes:
            continue
        texts = _read_port_units(ctx, [unit], served, errs)
        if texts:
            errs.extend(parity.card_parity_errors(nodes[cid], texts[0], unit))
    return errs, len(cards)


def _check_c1_8(ctx: ConformanceContext, mappings: list[dict]) -> CheckOutcome:
    """C1.8: citation multisets, body-line containment, and discrete-conditions parity."""
    graph_nodes = (ctx.port_graph or {}).get("concepts", [])
    graph_errs, n_graph = parity.graph_conditions_errors(graph_nodes if isinstance(graph_nodes, list) else [])
    if ctx.canonical_only:
        return make_check("C1.8", n_graph, graph_errs, "C1_CONDITIONS_PARITY")
    served = _load_served_units(ctx)
    multiset_errs, loss_errs, n_trans = _check_c1_8_transforming(ctx, mappings, served)
    card_errs, n_cards = _check_c1_8_cards(ctx, served)
    examined = n_trans + n_cards + n_graph
    if multiset_errs:
        return make_check("C1.8", examined, multiset_errs + loss_errs + card_errs, "C1_CITATION_MULTISET")
    if loss_errs:
        return make_check("C1.8", examined, loss_errs + card_errs, "C1_TRANSFORM_CONTENT_LOSS")
    return make_check("C1.8", examined, card_errs + graph_errs, "C1_CONDITIONS_PARITY")


def _check_c1_7_lossless(ctx: ConformanceContext, mappings: list[dict]) -> CheckOutcome:
    if ctx.canonical_only:
        return not_applicable("C1.7")
    errs: list[str] = []
    examined = 0
    for m in mappings:
        if str(m.get("kind", "")) != "lossless":
            continue
        examined += 1
        c_rel = str(m.get("canonical", ""))
        p_rels = [str(x) for x in m.get("port", [])] if isinstance(m.get("port"), list) else []
        c_path = ctx.core_root / c_rel
        if len(p_rels) != 1 or not c_path.is_file() or not (ctx.port_root / p_rels[0]).is_file():
            errs.append(f"{c_rel}:0")
            continue
        c_txt, e1 = rules.read_text_strict(c_path)
        p_txt, e2 = rules.read_text_strict(ctx.port_root / p_rels[0])
        if e1 or e2 or c_txt is None or p_txt is None:
            errs.append(f"{c_rel}:0")
        elif common.body_digest_n6(c_txt) != common.body_digest_n6(p_txt):
            errs.append(f"{p_rels[0]}:1")
    return make_check("C1.7", examined, errs, "C1_BODY_DIGEST")


def _check_c1_mappings_and_ledgers(ctx: ConformanceContext) -> list[CheckOutcome]:
    mappings = [m for m in ctx.manifest.get("mappings", []) if isinstance(m, dict)]
    c110_out, c111_out = _check_c1_10_11_inline(ctx)
    return [
        _check_c1_7_lossless(ctx, mappings),
        _check_c1_8(ctx, mappings),
        _check_c1_9_gotchas(ctx),
        c110_out,
        c111_out,
        _check_c1_12_package(ctx, mappings),
    ]


def _check_c1_9_gotchas(ctx: ConformanceContext) -> CheckOutcome:
    l_errs, _, ledger_ids = rules.collect_gotcha_ledgers(ctx.core_root)
    haystack: list[str] = []
    scan_files = (
        common.sorted_files_under(ctx.core_root / "knowledge")
        + common.sorted_files_under(ctx.core_root / "ontology")
        if ctx.canonical_only
        else list_port_files(ctx)
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
        for p in list_port_files(ctx):
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
    if ctx.canonical_only:
        return not_applicable("C1.12")
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



def evaluate_check_c1_8(ctx: ConformanceContext) -> CheckOutcome:
    """Evaluate C1.8 alone (transforming conservation and discrete-conditions parity)."""
    return _check_c1_8(ctx, [m for m in ctx.manifest.get("mappings", []) if isinstance(m, dict)])
