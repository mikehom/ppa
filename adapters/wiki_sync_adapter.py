#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic Knowledge Wiki + NotebookLM transforming
#   compiler emitting pages/{concepts,sources,index.md,log.md} and a NotebookLM
#   ingestion bundle (default CONFORMANT; optional --dev-nofiles for fileless
#   API endpoints) while conserving N8 & concept multisets.
"""Compile canonical PPA knowledge into a Knowledge Wiki + NotebookLM layout."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))

from adapters import common  # noqa: E402

TARGET = "knowledge-wiki"
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")


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
    meta, fm_lines, body = common.split_frontmatter(raw)
    if not meta or "name" not in meta or "description" not in meta:
        raise common.AdapterError(f"{skill_md}: missing SKILL.md frontmatter")
    name = meta["name"]
    desc_lines = [f"<!-- skill: {name} -->"]
    target_hdr = max(len(fm_lines), 2)
    while len(desc_lines) < target_hdr - 1:
        desc_lines.append("<!-- channel: wiki-on-demand -->")
    desc_lines.append(f"<!-- summary: {meta['description']} -->")
    rewritten = _rewrite_wiki_links(body, name, from_sources_dir=False)
    return f"pages/concepts/{name}.md", "\n".join(desc_lines) + "\n" + rewritten


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


def _format_concept_cite(cite: dict) -> str:
    ch = str(cite.get("chapter_or_app", ""))
    roman = cite.get("book_page_roman")
    book = cite.get("book_page")
    pdf = cite.get("pdf_page")
    sec = cite.get("section")
    tf = cite.get("table_or_fig")
    if roman and ch in {"Preface", "Contents", "List of Tables", "List of Figures"}:
        return f"[PPA {ch}, p. {roman}] (book p. {roman}; PDF p. {pdf})"
    if tf:
        return f"[PPA {tf}, p. {book}] (book p. {book}; PDF p. {pdf})"
    if sec and re.match(r"^[1-6ABC]\.\d", str(sec)):
        return f"[PPA §{sec}, p. {book}] (book p. {book}; PDF p. {pdf})"
    if sec in {"Concluding Remarks", "Mini Projects", "Exercises"}:
        kind = f"Chapter {ch}" if ch.isdigit() else f"Appendix {ch}"
        return f"[PPA {kind} {sec}, p. {book}] (book p. {book}; PDF p. {pdf})"
    if ch == "Notation":
        return f"[PPA Index of Notation, p. {book}] (book p. {book}; PDF p. {pdf})"
    if ch == "Index":
        return f"[PPA Index, p. {book}] (book p. {book}; PDF p. {pdf})"
    if ch == "Bibliography":
        loc = f"Bibliography {sec}" if (isinstance(sec, str) and sec.startswith("[")) else "Bibliography"
        return f"[PPA {loc}, p. {book}] (book p. {book}; PDF p. {pdf})"
    kind = f"Chapter {ch}" if ch.isdigit() else f"Appendix {ch}"
    return f"[PPA {kind}, p. {book}] (book p. {book}; PDF p. {pdf})"


def _format_node_card(node: dict) -> tuple[str, str, str, str, str]:
    cid = str(node["id"])
    slug = cid.replace(".", "-")
    rel_out = f"pages/concepts/ppa-node-{slug}.md"
    cites = [_format_concept_cite(c) for c in node.get("citations", []) if isinstance(c, dict)]
    proj = node.get("projections", {})
    lines = [
        f"# {node.get('title', cid)}",
        "",
        f"- **Concept ID**: `{cid}`",
        f"- **Altitude**: `{node.get('altitude', '')}` | **Unit**: `{node.get('unit', '')}`",
        f"- **Source Coordinates**: {'; '.join(cites)}",
        "",
        "## Formal Summary",
        "",
        str(node.get("formal_summary", "")),
        "",
        "## Domain Projections",
        "",
        f"- **CS Theory**: {proj.get('cs_theory', '')}",
        f"- **SWE Architecture**: {proj.get('swe_architecture', '')}",
        f"- **Practical Debugging**: {proj.get('practical_debugging', '')}",
        f"- **Cyber**: {proj.get('cyber', '')}",
        "",
    ]
    conditions = [str(c) for c in node.get("conditions", []) if str(c).strip()]
    if conditions:
        lines.extend(["## Preconditions & Side Conditions", ""])
        lines.extend(f"- {cond}" for cond in conditions)
        lines.append("")
    edges = node.get("related_edges", [])
    if edges:
        lines.extend(["## Related Edges", ""])
        for edge in edges:
            basis = edge.get("basis") or {}
            uid = f" ({basis['unification_id']})" if basis.get("unification_id") else ""
            lines.append(f"- `{edge.get('relation')}` -> `{edge.get('target_id')}`{uid}")
        lines.append("")
    issue_refs = [str(r) for r in node.get("issue_refs", []) if str(r).strip()]
    if issue_refs:
        lines.extend(["## Related Issues", ""])
        lines.extend(f"- `{ref}`" for ref in issue_refs)
        lines.append("")
    if len(lines) > 450:
        raise common.AdapterError(f"{rel_out}: concept card exceeds 450 lines ({len(lines)})")
    return rel_out, str(node.get("unit", "unknown")), cid, str(node.get("title", cid)), "\n".join(lines) + "\n"


def _emit_concept_node_cards(
    repo_root: Path, port_root: Path, served_units: dict[str, str] | None = None
) -> list[tuple[str, str, str, str]]:
    graph = json.loads(common.read_utf8_strict(repo_root / "ontology" / "concept_graph.json"))
    emitted: list[tuple[str, str, str, str]] = []
    for node in sorted(graph.get("concepts", []), key=lambda item: str(item.get("id", ""))):
        rel_out, unit, cid, title, text = _format_node_card(node)
        if served_units is None:
            common.write_utf8_lf(port_root / rel_out, text)
        else:
            served_units[f"ppa:{rel_out.removeprefix('pages/')}"] = text
        emitted.append((rel_out, unit, cid, title))
    return emitted


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


def _emit_chunked_shard_sources(
    repo_root: Path, port_root: Path, served_units: dict[str, str] | None = None
) -> list[str]:
    shards_dir = repo_root / "corpus" / "shards"
    bundle_dir = port_root / "notebooklm_sources_bundle"
    emitted: list[str] = []
    if not shards_dir.is_dir():
        return emitted
    for shard in sorted(shards_dir.glob("RAW_SHARD_*.md")):
        common.copy_lossless(shard, bundle_dir / shard.name)
        lines = common.split_lines_n2(common.read_utf8_strict(shard))
        stem = shard.stem.lower().replace("raw_shard_", "ppa-shard-")
        for idx, chunk in enumerate(_chunk_markdown_lines(lines, shard.stem), start=1):
            rel_out = f"pages/sources/{stem}-part{idx:02d}.md"
            text = "\n".join(chunk) + "\n"
            if served_units is None:
                common.write_utf8_lf(port_root / rel_out, text)
            else:
                served_units[f"ppa:{rel_out.removeprefix('pages/')}"] = text
            emitted.append(rel_out)
    notation = repo_root / "ontology" / "notation_index.md"
    if notation.is_file():
        common.copy_lossless(notation, bundle_dir / "notation_index.md")
    common.write_utf8_lf(
        bundle_dir / "bundle_manifest.json",
        json.dumps({"sources": sorted(p.name for p in bundle_dir.glob("*.md"))}, indent=2) + "\n",
    )
    return emitted


def _write_wiki_page(
    port_root: Path, rel_path: str, text: str, max_lines: int, served_units: dict[str, str] | None
) -> None:
    if len(common.split_lines_n2(text)) > max_lines:
        raise common.AdapterError(f"{rel_path}: exceeds {max_lines}-line budget")
    if served_units is None:
        common.write_utf8_lf(port_root / rel_path, text)
    else:
        served_units[f"ppa:{rel_path.removeprefix('pages/')}"] = text


def _emit_grouped_source_index(
    port_root: Path, rel_path: str, heading: str, targets: list[str], served_units: dict[str, str] | None
) -> list[str]:
    emitted: list[str] = []
    sorted_t = sorted(targets)
    batches = [sorted_t[i:i + 200] for i in range(0, max(len(sorted_t), 1), 200)]
    for idx, batch in enumerate(batches, start=1):
        out_rel = rel_path if len(batches) == 1 else rel_path.replace(".md", f"-p{idx:02d}.md")
        lines = [f"# {heading}" + (f" (Part {idx})" if len(batches) > 1 else ""), ""]
        lines.extend(f"- [{Path(sp).stem}]({Path(sp).name})" for sp in batch)
        lines.append("")
        _write_wiki_page(port_root, out_rel, "\n".join(lines), 250, served_units)
        emitted.append(out_rel)
    return emitted


def _emit_index_and_log(
    port_root: Path,
    rev: str,
    entry_pages: list[str],
    node_cards: list[tuple[str, str, str, str]],
    ref_pages: list[str],
    shard_pages: list[str],
    served_units: dict[str, str] | None = None,
) -> tuple[list[str], list[str]]:
    unit_groups: dict[str, list[tuple[str, str, str]]] = {}
    for rel_out, unit, cid, title in node_cards:
        unit_groups.setdefault(unit, []).append((rel_out, cid, title))
    unit_order = {u: i for i, u in enumerate(
        ("U0", "U1", "U2a", "U2b", "U3a", "U3b", "U4a", "U4b", "U5a", "U5b", "U6", "X")
    )}
    node_indexes: list[tuple[str, str, int]] = []
    for unit in sorted(unit_groups, key=lambda u: (unit_order.get(u, 99), u)):
        sub_rel = f"pages/concepts/ppa-index-{unit.lower()}.md"
        rows = sorted(unit_groups[unit], key=lambda item: item[1])
        sub_lines = [f"# PPA Concept Nodes: Unit {unit}", ""]
        sub_lines.extend(f"- [`{cid}`]({Path(r).name}) — {title}" for r, cid, title in rows)
        sub_lines.append("")
        _write_wiki_page(port_root, sub_rel, "\n".join(sub_lines), 250, served_units)
        node_indexes.append((unit, sub_rel, len(rows)))

    ref_idxs = _emit_grouped_source_index(
        port_root, "pages/sources/ppa-index-refs.md", "PPA Formal Reference Sources", ref_pages, served_units
    )
    shard_idxs = _emit_grouped_source_index(
        port_root, "pages/sources/ppa-index-shards.md", "PPA Lossless Corpus Shards", shard_pages, served_units
    )
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
        f"- [Unit {u} ({n} concepts)]({sub_rel.removeprefix('pages/')})"
        for u, sub_rel, n in node_indexes
    )
    idx_lines.extend(["", "## Formal References and Corpus Shards", ""])
    idx_lines.extend(f"- [{Path(p).stem}]({p.removeprefix('pages/')})" for p in ref_idxs + shard_idxs)
    idx_lines.extend(["", "## Chronological Log", "", "- [Ingest Log](log.md)", ""])
    _write_wiki_page(port_root, "pages/index.md", "\n".join(idx_lines), 250, served_units)

    log_lines = [
        "# PPA Knowledge Wiki Chronological Log",
        "",
        f"- **Revision `{rev}`**: Compiled {len(entry_pages)} entry pages, "
        f"{len(node_cards)} concept cards ({len(node_indexes)} unit indexes), "
        f"{len(ref_pages)} reference sources, and {len(shard_pages)} shard chunks.",
        "",
    ]
    _write_wiki_page(port_root, "pages/log.md", "\n".join(log_lines), 250, served_units)
    return [sub_rel for _, sub_rel, _ in node_indexes], ref_idxs + shard_idxs


def _is_ppa_config_source(entry: object) -> bool:
    if isinstance(entry, str):
        return (
            entry.startswith("notebooklm_sources_bundle/")
            or entry.startswith("pages/sources/ppa-")
            or entry.startswith("pages/concepts/ppa-")
        )
    if isinstance(entry, dict):
        for key in ("id", "path", "name"):
            val = str(entry.get(key, ""))
            if (
                val.startswith("ppa-")
                or val.startswith("notebooklm_sources_bundle/")
                or val.startswith("pages/sources/ppa-")
            ):
                return True
    return False


def _update_wiki_config(
    port_root: Path,
    rev: str,
    concept_pages: list[str],
    source_pages: list[str],
    index_pages: list[str],
    bundle_sources: list[str],
    dev_nofiles: bool = False,
) -> Path:
    """Create or merge wiki_config.json while preserving all non-PPA entries."""
    cfg_path = port_root / "wiki_config.json"
    cfg: dict[str, object] = {}
    if cfg_path.is_file():
        try:
            loaded = json.loads(common.read_utf8_strict(cfg_path))
        except json.JSONDecodeError as exc:
            raise common.AdapterError(f"{cfg_path}: invalid JSON: {exc}") from exc
        if not isinstance(loaded, dict):
            raise common.AdapterError(f"{cfg_path}: top-level JSON must be an object")
        cfg = loaded
    ppa_bundle_paths = sorted(f"notebooklm_sources_bundle/{name}" for name in bundle_sources)
    if isinstance(cfg.get("sources"), list):
        kept = [item for item in cfg["sources"] if not _is_ppa_config_source(item)]
        cfg["sources"] = kept + ppa_bundle_paths
    cfg["ppa"] = {
        "canonical_revision": rev,
        "concept_pages": sorted(concept_pages),
        "index": "pages/index.md" if not dev_nofiles else "ppa:index.md",
        "index_pages": sorted(index_pages),
        "log": "pages/log.md" if not dev_nofiles else "ppa:log.md",
        "mode": "dev-nofiles" if dev_nofiles else "filesystem",
        "notebooklm_bundle": ppa_bundle_paths,
        "source_pages": sorted(source_pages),
    }
    common.write_utf8_lf(cfg_path, json.dumps(cfg, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return cfg_path


def _store_wiki_unit(
    port_root: Path, rel_dst: str, content: str, served_units: dict[str, str] | None
) -> str:
    if served_units is None:
        common.write_utf8_lf(port_root / rel_dst, content)
        return rel_dst
    uri = f"ppa:{rel_dst.removeprefix('pages/')}"
    served_units[uri] = content
    return uri


def compile_port(
    repo_root: Path,
    port_root: Path,
    canonical_revision: str | None = None,
    extra_surfaces: list[str] | None = None,
    user_home: str | None = None,
    dev_nofiles: bool = False,
) -> dict[str, object]:
    """Compile canonical core into Knowledge Wiki pages/ + NotebookLM bundle."""
    repo_root = repo_root.resolve()
    port_root = port_root.resolve()
    uhome = common.resolve_user_home(port_root, user_home)
    surfaces = common.snapshot_always_on_surfaces(port_root, TARGET, extra_surfaces, uhome)
    pre_existing = common.scan_preexisting_discovery(port_root, TARGET)
    k_files, o_files, c_files = common.collect_canonical_package(repo_root)
    rev = common.resolve_canonical_revision(repo_root, canonical_revision)
    port_root.mkdir(parents=True, exist_ok=True)
    served_units: dict[str, str] | None = {} if dev_nofiles else None

    mappings: list[dict[str, object]] = []
    entry_pages: list[str] = []
    ref_pages: list[str] = []

    for kpath in k_files:
        rel_src = kpath.relative_to(repo_root)
        parts = kpath.relative_to(repo_root / "knowledge").parts
        if parts[0] == "skills" and parts[-1] == "SKILL.md":
            rel_dst, content = _transform_skill_page(kpath)
            entry_pages.append(rel_dst)
            port_ref = _store_wiki_unit(port_root, rel_dst, content, served_units)
            mappings.append({"canonical": rel_src.as_posix(), "kind": "transforming", "port": [port_ref]})
        elif parts[0] == "ambient-context":
            rel_dst, content = _transform_ambient_page(kpath)
            entry_pages.append(rel_dst)
            port_ref = _store_wiki_unit(port_root, rel_dst, content, served_units)
            mappings.append({"canonical": rel_src.as_posix(), "kind": "transforming", "port": [port_ref]})
        elif parts[0] == "skills" and len(parts) == 4 and parts[2] == "references":
            rel_dst, content = _transform_reference_page(kpath, parts[1])
            ref_pages.append(rel_dst)
            port_ref = _store_wiki_unit(port_root, rel_dst, content, served_units)
            mappings.append({"canonical": rel_src.as_posix(), "kind": "transforming", "port": [port_ref]})
        else:
            rel_dst = (Path("core") / Path(*parts)).as_posix()
            common.copy_lossless(kpath, port_root / rel_dst)
            mappings.append({"canonical": rel_src.as_posix(), "kind": "lossless", "port": [rel_dst]})

    for opath in o_files:
        rel_src = opath.relative_to(repo_root)
        rel_dst = (Path("core") / "ontology" / opath.relative_to(repo_root / "ontology")).as_posix()
        common.copy_lossless(opath, port_root / rel_dst)
        mappings.append({"canonical": rel_src.as_posix(), "kind": "lossless", "port": [rel_dst]})

    node_cards = _emit_concept_node_cards(repo_root, port_root, served_units)
    shard_pages = _emit_chunked_shard_sources(repo_root, port_root, served_units)
    node_idx_pages, src_idx_pages = _emit_index_and_log(
        port_root, rev, entry_pages, node_cards, ref_pages, shard_pages, served_units
    )
    if served_units is not None:
        serialized = {k: common.split_lines_n2(v) for k, v in served_units.items()}
        common.write_utf8_lf(
            port_root / "served_units.json",
            json.dumps(serialized, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        )
    bundle_dir = port_root / "notebooklm_sources_bundle"
    bundle_sources = sorted(p.name for p in bundle_dir.glob("*.md")) if bundle_dir.is_dir() else []
    all_concepts = entry_pages + [r for r, _, _, _ in node_cards] + node_idx_pages
    all_sources = ref_pages + shard_pages + src_idx_pages
    _update_wiki_config(
        port_root, rev, all_concepts, all_sources, ["pages/index.md"] + node_idx_pages + src_idx_pages,
        bundle_sources, dev_nofiles=dev_nofiles,
    )
    common.copy_corpus_closure(repo_root, c_files, port_root / "core" / "corpus")

    manifest: dict[str, object] = {
        "adapter_options": {"dev_nofiles": dev_nofiles},
        "always_on_surfaces": surfaces,
        "canonical_revision": rev,
        "corpus_root": "core/corpus",
        "deviations": ["DEV-NOFILES"] if dev_nofiles else [],
        "discovery_entries": common.collect_skill_discovery(repo_root, include_ambient=False),
        "mappings": mappings,
        "pre_existing_discovery": pre_existing,
        "spec_version": "1",
        "target": TARGET,
    }
    common.write_port_manifest(port_root, manifest)
    return manifest


def _cli(argv: list[str]) -> int:
    ap = common.base_arg_parser("Compile PPA package for Knowledge Wiki + NotebookLM")
    ap.add_argument("--dev-nofiles", action="store_true",
                    help="declare DEV-NOFILES for fileless remote/API endpoints (omits pages/ Markdown tree)")
    args = ap.parse_args(argv)
    compile_port(
        repo_root=Path(args.repo_root),
        port_root=Path(args.port_root),
        canonical_revision=args.canonical_revision,
        extra_surfaces=args.always_on_surfaces,
        user_home=args.user_home,
        dev_nofiles=args.dev_nofiles,
    )
    return 0


if __name__ == "__main__":
    sys.exit(common.run_adapter_cli(_cli))
