#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic Knowledge Wiki + NotebookLM transforming
#   compiler emitting pages/{concepts,sources,ppa_index.md,ppa_log.md} and a
#   NotebookLM ingestion bundle (default CONFORMANT; optional --dev-nofiles for
#   fileless API endpoints) while conserving N8 & concept multisets.
# @decision DEC-PPA-009: The wiki root index and log belong to the operator: the
#   adapter owns only PPA-namespaced pages and maintains one bounded block inside
#   pages/index.md and pages/log.md, preserving every other line byte for byte.
"""Compile canonical PPA knowledge into a Knowledge Wiki + NotebookLM layout."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))

from adapters import common, port_plan, wiki_cards  # noqa: E402

TARGET = "knowledge-wiki"
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")
BLOCK_START = common.KNOWLEDGE_BLOCK_START
BLOCK_END = common.KNOWLEDGE_BLOCK_END
INDEX_PREAMBLE = ["# Knowledge Wiki Index", ""]
LOG_PREAMBLE = ["# Knowledge Wiki Log", ""]
DEFAULT_BUNDLE_DIR = "notebooklm_sources_bundle"
UNIT_ORDER = ("U0", "U1", "U2a", "U2b", "U3a", "U3b", "U4a", "U4b", "U5a", "U5b", "U6", "X")


class _WikiOut:
    """Route a compiled wiki unit to the port plan (files) or to the served-unit map."""

    def __init__(self, plan: port_plan.PortPlan, served: dict[str, str] | None) -> None:
        self.plan = plan
        self.served = served

    def put(self, rel_path: str, text: str, role: str = "mapped", max_lines: int | None = None) -> str:
        if max_lines is not None and len(common.split_lines_n2(text)) > max_lines:
            raise common.AdapterError(f"{rel_path}: exceeds {max_lines}-line budget")
        if self.served is None:
            return self.plan.add(rel_path, text, role)
        uri = f"ppa:{rel_path.removeprefix('pages/')}"
        self.served[uri] = common.normalize_lf(text)
        return uri


def _ref_wiki_name(skill_name: str, ref_filename: str) -> str:
    return f"ppa-ref-{skill_name}--{ref_filename}"


def _rewrite_wiki_links(body: str, skill_name: str, from_sources_dir: bool) -> str:
    prefix = "" if from_sources_dir else "../sources/"
    out: list[str] = []
    fence: str | None = None
    for line in body.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = marker if fence is None else (None if fence == marker else fence)
            out.append(line)
            continue
        if fence is not None:
            out.append(line)
            continue

        def _repl(match: re.Match[str]) -> str:
            label, href = match.group(1), match.group(2)
            clean, *frag = href.split("#", 1)
            norm_clean = clean.removeprefix("./")
            suffix = f"#{frag[0]}" if frag else ""
            if not from_sources_dir and skill_name and norm_clean.startswith("references/"):
                ref_file = norm_clean.removeprefix("references/")
                return f"[{label}]({prefix}{_ref_wiki_name(skill_name, ref_file)}{suffix})"
            m_amb = re.match(r"^\.\./skills/(ppa-[a-z0-9-]+)/references/([^/]+\.md)$", norm_clean)
            if m_amb:
                return f"[{label}]({prefix}{_ref_wiki_name(m_amb.group(1), m_amb.group(2))}{suffix})"
            m_sib = re.match(r"^(?:\.\./)+?(ppa-[a-z0-9-]+)/references/([^/]+\.md)$", norm_clean)
            if m_sib:
                return f"[{label}]({prefix}{_ref_wiki_name(m_sib.group(1), m_sib.group(2))}{suffix})"
            if from_sources_dir and skill_name and re.match(r"^[A-Za-z0-9_.-]+\.md$", norm_clean):
                return f"[{label}]({_ref_wiki_name(skill_name, norm_clean)}{suffix})"
            return match.group(0)

        out.append(LINK_RE.sub(_repl, line))
    return "\n".join(out)


def _transform_skill_page(skill_md: Path) -> tuple[str, str]:
    raw = common.read_utf8_strict(skill_md)
    meta, _, body = common.split_frontmatter(raw)
    if not meta or "name" not in meta or "description" not in meta:
        raise common.AdapterError(f"{skill_md}: missing SKILL.md frontmatter")
    name = meta["name"]
    header = f"<!-- skill: {name} -->\n<!-- summary: {meta['description']} -->\n"
    return f"pages/concepts/{name}.md", header + _rewrite_wiki_links(body, name, from_sources_dir=False)


def _transform_ambient_page(amb_path: Path) -> tuple[str, str]:
    raw = common.normalize_lf(common.read_utf8_strict(amb_path))
    _, _, body = common.split_frontmatter(raw)
    rewritten = _rewrite_wiki_links(body, "", from_sources_dir=False)
    slug = amb_path.stem.removeprefix("ppa-")
    return f"pages/concepts/ppa-ambient-{slug}.md", rewritten


def _transform_reference_page(ref_path: Path, skill_name: str) -> tuple[str, str]:
    raw = common.normalize_lf(common.read_utf8_strict(ref_path))
    rewritten = _rewrite_wiki_links(raw, skill_name, from_sources_dir=True)
    return f"pages/sources/{_ref_wiki_name(skill_name, ref_path.name)}", rewritten


def _plan_knowledge_pages(
    out: _WikiOut, repo_root: Path, k_files: list[Path]
) -> tuple[list[dict[str, object]], list[str], list[str]]:
    """Plan skill, ambient, and reference pages; return (mappings, entry pages, reference pages)."""
    mappings: list[dict[str, object]] = []
    entry_pages: list[str] = []
    ref_pages: list[str] = []
    for kpath in k_files:
        rel_src = kpath.relative_to(repo_root).as_posix()
        parts = kpath.relative_to(repo_root / "knowledge").parts
        kind = "transforming"
        if parts[0] == "skills" and parts[-1] == "SKILL.md":
            rel_dst, content = _transform_skill_page(kpath)
            entry_pages.append(rel_dst)
            port_ref = out.put(rel_dst, content)
        elif parts[0] == "ambient-context":
            rel_dst, content = _transform_ambient_page(kpath)
            entry_pages.append(rel_dst)
            port_ref = out.put(rel_dst, content)
        elif parts[0] == "skills" and len(parts) == 4 and parts[2] == "references":
            rel_dst, content = _transform_reference_page(kpath, parts[1])
            ref_pages.append(rel_dst)
            port_ref = out.put(rel_dst, content)
        else:
            port_ref = out.plan.add_copy(kpath, (Path("core") / Path(*parts)).as_posix())
            kind = "lossless"
        mappings.append({"canonical": rel_src, "kind": kind, "port": [port_ref]})
    return mappings, entry_pages, ref_pages


def _emit_concept_node_cards(
    out: _WikiOut, repo_root: Path
) -> tuple[list[tuple[str, str, str, str]], dict[str, str]]:
    """Emit one card per concept node; return (card rows, concept id -> port unit)."""
    graph = json.loads(common.read_utf8_strict(repo_root / "ontology" / "concept_graph.json"))
    emitted: list[tuple[str, str, str, str]] = []
    card_of: dict[str, str] = {}
    for node in sorted(graph.get("concepts", []), key=lambda item: str(item.get("id", ""))):
        rel_out, unit, cid, title, text = wiki_cards.format_node_card(node)
        card_of[cid] = out.put(rel_out, text, role="extra")
        emitted.append((rel_out, unit, cid, title))
    return emitted, card_of


def _chunk_markdown_lines(lines: list[str], header: str) -> list[list[str]]:
    chunks: list[list[str]] = []
    cur: list[str] = []
    fence: str | None = None
    for ln in lines:
        s = ln.lstrip()
        toggles = s.startswith(("```", "~~~"))
        marker = s[:3] if toggles else ""
        if fence is None and ((ln.startswith(("## ", "### ")) and len(cur) >= 320) or len(cur) >= 430):
            chunks.append(cur)
            cur = [f"# {header} (continued)", ""]
        if fence is not None and toggles and marker == fence and len(cur) >= 430:
            cur.append(ln)
            fence = None
            chunks.append(cur)
            cur = [f"# {header} (continued)", ""]
            continue
        if fence is not None and len(cur) >= 445 and not (toggles and marker == fence):
            cur.append(fence)
            chunks.append(cur)
            cur = [f"# {header} (continued)", "", fence]
        cur.append(ln)
        if toggles:
            fence = marker if fence is None else (None if fence == marker else fence)
    if cur:
        chunks.append(cur)
    return chunks


def _emit_shards_and_bundle(out: _WikiOut, repo_root: Path, bundle_rel: str) -> tuple[list[str], list[str]]:
    """Emit chunked shard pages and the ingestion bundle; return (shard pages, bundle paths)."""
    shards_dir = repo_root / "corpus" / "shards"
    shard_pages: list[str] = []
    bundle_names: list[str] = []
    for shard in sorted(shards_dir.glob("RAW_SHARD_*.md")) if shards_dir.is_dir() else []:
        out.plan.add_copy(shard, f"{bundle_rel}/{shard.name}", role="bundle")
        bundle_names.append(shard.name)
        lines = common.split_lines_n2(common.read_utf8_strict(shard))
        stem = shard.stem.lower().replace("raw_shard_", "ppa-shard-")
        for idx, chunk in enumerate(_chunk_markdown_lines(lines, shard.stem), start=1):
            rel_out = f"pages/sources/{stem}-part{idx:02d}.md"
            out.put(rel_out, "\n".join(chunk) + "\n", role="extra")
            shard_pages.append(rel_out)
    notation = repo_root / "ontology" / "notation_index.md"
    if notation.is_file():
        out.plan.add_copy(notation, f"{bundle_rel}/notation_index.md", role="bundle")
        bundle_names.append("notation_index.md")
    out.plan.add(
        f"{bundle_rel}/bundle_manifest.json",
        json.dumps({"sources": sorted(bundle_names)}, indent=2) + "\n",
        role="manifest",
    )
    return shard_pages, sorted(f"{bundle_rel}/{name}" for name in bundle_names)


def _emit_grouped_source_index(out: _WikiOut, rel_path: str, heading: str, targets: list[str]) -> list[str]:
    emitted: list[str] = []
    sorted_t = sorted(targets)
    batches = [sorted_t[i:i + 200] for i in range(0, max(len(sorted_t), 1), 200)]
    for idx, batch in enumerate(batches, start=1):
        out_rel = rel_path if len(batches) == 1 else rel_path.replace(".md", f"-p{idx:02d}.md")
        lines = [f"# {heading}" + (f" (Part {idx})" if len(batches) > 1 else ""), ""]
        lines.extend(f"- [{Path(sp).stem}]({Path(sp).name})" for sp in batch)
        lines.append("")
        out.put(out_rel, "\n".join(lines), role="index", max_lines=250)
        emitted.append(out_rel)
    return emitted


def _emit_ppa_indexes(
    out: _WikiOut,
    rev: str,
    entry_pages: list[str],
    node_cards: list[tuple[str, str, str, str]],
    ref_pages: list[str],
    shard_pages: list[str],
) -> tuple[list[str], list[str], str]:
    """Emit PPA-namespaced indexes and log; return (unit indexes, source indexes, sync line)."""
    unit_groups: dict[str, list[tuple[str, str, str]]] = {}
    for rel_out, unit, cid, title in node_cards:
        unit_groups.setdefault(unit, []).append((rel_out, cid, title))
    unit_rank = {u: i for i, u in enumerate(UNIT_ORDER)}
    node_indexes: list[tuple[str, str, int]] = []
    for unit in sorted(unit_groups, key=lambda u: (unit_rank.get(u, 99), u)):
        sub_rel = f"pages/concepts/ppa-index-{unit.lower()}.md"
        rows = sorted(unit_groups[unit], key=lambda item: item[1])
        sub_lines = [f"# PPA Concept Nodes: Unit {unit}", ""]
        sub_lines.extend(f"- [`{cid}`]({Path(r).name}) — {title}" for r, cid, title in rows)
        sub_lines.append("")
        out.put(sub_rel, "\n".join(sub_lines), role="index", max_lines=250)
        node_indexes.append((unit, sub_rel, len(rows)))
    src_idxs = _emit_grouped_source_index(
        out, "pages/sources/ppa-index-refs.md", "PPA Formal Reference Sources", ref_pages)
    src_idxs += _emit_grouped_source_index(
        out, "pages/sources/ppa-index-shards.md", "PPA Lossless Corpus Shards", shard_pages)
    idx_lines = [
        "# PPA Knowledge Wiki Index",
        "",
        f"Pinned canonical revision: `{rev}`.",
        "",
        "## Skill and Orientation Entry Pages",
        "",
    ]
    idx_lines.extend(f"- [{Path(cp).stem}]({cp.removeprefix('pages/')})" for cp in sorted(entry_pages))
    idx_lines.extend(["", "## Concept Graph Unit Indexes", ""])
    idx_lines.extend(
        f"- [Unit {u} ({n} concepts)]({sub_rel.removeprefix('pages/')})" for u, sub_rel, n in node_indexes)
    idx_lines.extend(["", "## Formal References and Corpus Shards", ""])
    idx_lines.extend(f"- [{Path(p).stem}]({p.removeprefix('pages/')})" for p in src_idxs)
    idx_lines.extend(["", "## Sync Log", "", "- [Sync log for PPA](ppa_log.md)", ""])
    out.put("pages/ppa_index.md", "\n".join(idx_lines), role="index", max_lines=250)
    sync_line = (
        f"- **PPA sync, revision `{rev}`**: compiled {len(entry_pages)} entry pages, "
        f"{len(node_cards)} concept cards ({len(node_indexes)} unit indexes), "
        f"{len(ref_pages)} reference sources, and {len(shard_pages)} shard chunks."
    )
    out.put("pages/ppa_log.md", "\n".join(["# PPA Knowledge Wiki Sync Log", "", sync_line, ""]),
            role="index", max_lines=250)
    return [sub_rel for _, sub_rel, _ in node_indexes], src_idxs, sync_line


def merge_bounded_block(existing: bytes | None, block_lines: list[str], preamble: list[str]) -> tuple[bytes, bool]:
    """Insert or replace the bounded PPA block; return (new bytes, operator content present).

    Bytes outside the block are never altered. A file that does not exist is
    created as ``preamble`` followed by the block.
    """
    block = "\n".join([BLOCK_START] + block_lines + [BLOCK_END]) + "\n"
    if existing is None:
        return ("\n".join(preamble) + "\n" + block).encode("utf-8"), False
    try:
        text = existing.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise common.AdapterError(f"existing wiki page is not UTF-8: {exc}") from exc
    n_start, n_end = text.count(BLOCK_START), text.count(BLOCK_END)
    if n_start == 0 and n_end == 0:
        sep = "" if (not text or text.endswith("\n")) else "\n"
        gap = "\n" if text.strip() else ""
        merged, outside = text + sep + gap + block, text
    elif n_start == 1 and n_end == 1 and text.index(BLOCK_START) < text.index(BLOCK_END):
        start = text.index(BLOCK_START)
        tail = text[text.index(BLOCK_END) + len(BLOCK_END):]
        tail = tail[2:] if tail.startswith("\r\n") else (tail[1:] if tail.startswith("\n") else tail)
        merged, outside = text[:start] + block + tail, text[:start] + tail
    else:
        raise common.AdapterError("existing wiki page carries unbalanced or repeated PPA block markers")
    user_content = outside.replace("\r\n", "\n").strip() != "\n".join(preamble).strip()
    return merged.encode("utf-8"), user_content


def _merge_root_page(plan: port_plan.PortPlan, rel: str, block_lines: list[str], preamble: list[str]) -> None:
    """Plan pages/index.md or pages/log.md: owned when adapter-generated, merged otherwise."""
    dest = plan.port_root / rel
    if dest.is_symlink():
        raise common.AdapterError(f"refusing to merge into symlink: {rel}")
    existing = dest.read_bytes() if dest.is_file() else None
    data, user_content = merge_bounded_block(existing, block_lines, preamble)
    generated = not user_content and (existing is None or plan.owns(rel))
    plan.add_bytes(rel, data, role="index" if generated else "merged")


def _merge_root_index_and_log(plan: port_plan.PortPlan, rev: str, entry_pages: list[str], sync_line: str) -> None:
    skills = sorted(p for p in entry_pages if not Path(p).name.startswith("ppa-ambient-"))
    index_block = [
        "## PPA Knowledge (Principles of Program Analysis)",
        "",
        f"Pinned canonical revision: `{rev}`.",
        "",
        "- [Knowledge index for PPA](ppa_index.md)",
        "- [Sync log for PPA](ppa_log.md)",
        "- [Chronological log](log.md)",
    ]
    index_block.extend(f"- [{Path(p).stem}]({p.removeprefix('pages/')})" for p in skills)
    _merge_root_page(plan, "pages/index.md", index_block, INDEX_PREAMBLE)
    _merge_root_page(plan, "pages/log.md", [sync_line + " See the [sync log for PPA](ppa_log.md)."], LOG_PREAMBLE)


def _is_ppa_config_source(entry: object, prior_bundle: set[str], bundle_rel: str) -> bool:
    prefixes = (f"{DEFAULT_BUNDLE_DIR}/", f"{bundle_rel}/", "pages/sources/ppa-", "pages/concepts/ppa-")
    if isinstance(entry, str):
        return entry in prior_bundle or entry.startswith(prefixes)
    if isinstance(entry, dict):
        for key in ("id", "path", "name"):
            val = str(entry.get(key, ""))
            if val in prior_bundle or val.startswith("ppa-") or val.startswith(prefixes[:3]):
                return True
    return False


def _update_wiki_config(
    plan: port_plan.PortPlan,
    rev: str,
    pages: dict[str, list[str]],
    bundle_paths: list[str],
    bundle_rel: str,
    dev_nofiles: bool = False,
) -> None:
    """Create or merge wiki_config.json while preserving all non-PPA entries."""
    cfg_path = plan.port_root / "wiki_config.json"
    cfg: dict[str, object] = {}
    if cfg_path.is_file():
        try:
            loaded = json.loads(common.read_utf8_strict(cfg_path))
        except json.JSONDecodeError as exc:
            raise common.AdapterError(f"{cfg_path.name}: invalid JSON: {exc}") from exc
        if not isinstance(loaded, dict):
            raise common.AdapterError(f"{cfg_path.name}: top-level JSON must be an object")
        cfg = loaded
    prior_ppa = cfg.get("ppa") if isinstance(cfg.get("ppa"), dict) else {}
    prior_bundle = {str(x) for x in prior_ppa.get("notebooklm_bundle", []) if isinstance(x, str)}
    if isinstance(cfg.get("sources"), list):
        kept = [item for item in cfg["sources"] if not _is_ppa_config_source(item, prior_bundle, bundle_rel)]
        cfg["sources"] = kept + bundle_paths
    cfg["ppa"] = {
        "bundle_manifest": f"{bundle_rel}/bundle_manifest.json",
        "canonical_revision": rev,
        "concept_pages": sorted(pages["concepts"]),
        "index": "pages/ppa_index.md" if not dev_nofiles else "ppa:ppa_index.md",
        "index_pages": sorted(pages["indexes"]),
        "log": "pages/ppa_log.md" if not dev_nofiles else "ppa:ppa_log.md",
        "mode": "dev-nofiles" if dev_nofiles else "filesystem",
        "notebooklm_bundle": bundle_paths,
        "source_pages": sorted(pages["sources"]),
    }
    plan.add("wiki_config.json", json.dumps(cfg, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
             role="merged")


def compile_port(
    repo_root: Path,
    port_root: Path,
    canonical_revision: str | None = None,
    extra_surfaces: list[str] | None = None,
    user_home: str | None = None,
    dev_nofiles: bool = False,
    bundle_dir: str = DEFAULT_BUNDLE_DIR,
    force: bool = False,
) -> dict[str, object]:
    """Compile canonical core into Knowledge Wiki pages/ + NotebookLM bundle."""
    repo_root = repo_root.resolve()
    port_root = port_root.resolve()
    bundle_abs = common.ensure_safe_subpath(port_root, bundle_dir, "--bundle-dir")
    if bundle_abs == port_root:
        raise common.AdapterError("--bundle-dir must name a subdirectory of the port root")
    bundle_rel = bundle_abs.relative_to(port_root).as_posix()
    plan = port_plan.PortPlan(port_root, TARGET, force=force)
    uhome = common.resolve_user_home(port_root, user_home)
    surfaces = common.snapshot_always_on_surfaces(port_root, TARGET, extra_surfaces, uhome)
    pre_existing = common.scan_preexisting_discovery(port_root, TARGET, prior=plan.prior)
    k_files, o_files, c_files = common.collect_canonical_package(repo_root)
    rev = common.resolve_canonical_revision(repo_root, canonical_revision)
    out = _WikiOut(plan, {} if dev_nofiles else None)

    mappings, entry_pages, ref_pages = _plan_knowledge_pages(out, repo_root, k_files)
    mappings += port_plan.plan_ontology_and_corpus(plan, repo_root, o_files, c_files, "core")
    node_cards, card_of = _emit_concept_node_cards(out, repo_root)
    shard_pages, bundle_paths = _emit_shards_and_bundle(out, repo_root, bundle_rel)
    node_idx_pages, src_idx_pages, sync_line = _emit_ppa_indexes(
        out, rev, entry_pages, node_cards, ref_pages, shard_pages)
    if out.served is None:
        _merge_root_index_and_log(plan, rev, entry_pages, sync_line)
    else:
        serialized = {k: common.split_lines_n2(v) for k, v in out.served.items()}
        plan.add("served_units.json",
                 json.dumps(serialized, indent=2, ensure_ascii=False, sort_keys=True) + "\n", role="manifest")
    _update_wiki_config(
        plan, rev,
        {
            "concepts": entry_pages + [r for r, _, _, _ in node_cards] + node_idx_pages,
            "indexes": ["pages/ppa_index.md"] + node_idx_pages + src_idx_pages,
            "sources": ref_pages + shard_pages + src_idx_pages,
        },
        bundle_paths, bundle_rel, dev_nofiles=dev_nofiles,
    )
    manifest: dict[str, object] = {
        "adapter_options": {"bundle_dir": bundle_rel, "dev_nofiles": dev_nofiles},
        "always_on_surfaces": surfaces,
        "canonical_revision": rev,
        "concept_cards": card_of,
        "corpus_root": "core/corpus",
        "deviations": ["DEV-NOFILES"] if dev_nofiles else [],
        "discovery_entries": common.collect_skill_discovery(repo_root, include_ambient=False),
        "mappings": mappings,
        "pre_existing_discovery": pre_existing,
        "spec_version": "1",
        "target": TARGET,
    }
    plan.commit(manifest)
    return manifest


def _cli(argv: list[str]) -> int:
    ap = common.base_arg_parser("Compile PPA package for Knowledge Wiki + NotebookLM")
    ap.add_argument("--dev-nofiles", action="store_true",
                    help="declare DEV-NOFILES for fileless remote/API endpoints (omits pages/ Markdown tree)")
    ap.add_argument("--bundle-dir", default=DEFAULT_BUNDLE_DIR,
                    help="NotebookLM bundle directory inside --port-root, as a relative POSIX path "
                         f"(default: {DEFAULT_BUNDLE_DIR})")
    args = ap.parse_args(argv)
    compile_port(
        repo_root=Path(args.repo_root),
        port_root=Path(args.port_root),
        canonical_revision=args.canonical_revision,
        extra_surfaces=args.always_on_surfaces,
        user_home=args.user_home,
        dev_nofiles=args.dev_nofiles,
        bundle_dir=args.bundle_dir,
        force=args.force,
    )
    return 0


if __name__ == "__main__":
    sys.exit(common.run_adapter_cli(_cli))
