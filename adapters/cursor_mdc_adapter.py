#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic Cursor IDE (.cursor/rules/*.mdc) compiler
#   emitting alwaysApply: false rule files with multiset-preserving N8 citations
#   (C1.8) and lossless L1 references/ontology under .cursor/ppa/.
"""Compile canonical PPA knowledge into Cursor IDE (.cursor/rules/*.mdc) format."""
from __future__ import annotations

import json
import re
import sys
import textwrap
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))

from adapters import common  # noqa: E402

TARGET = "cursor-ide"
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")


def _format_mdc_frontmatter(description: str, target_fm_lines: int) -> str:
    wrapped = textwrap.wrap(description, width=88, break_long_words=False, break_on_hyphens=False)
    if not wrapped:
        wrapped = [description]
    base_lines = ["---", "description: >-"] + [f"  {w}" for w in wrapped] + [
        "globs:",
        "alwaysApply: false",
        "---",
    ]
    while len(base_lines) < target_fm_lines and len(wrapped) > 1:
        longest = max(range(len(wrapped)), key=lambda idx: len(wrapped[idx]))
        words = wrapped[longest].split(" ")
        if len(words) < 2:
            break
        mid = len(words) // 2
        wrapped = wrapped[:longest] + [" ".join(words[:mid]), " ".join(words[mid:])] + wrapped[longest + 1:]
        base_lines = ["---", "description: >-"] + [f"  {w}" for w in wrapped] + [
            "globs:",
            "alwaysApply: false",
            "---",
        ]
    return "\n".join(base_lines)


def _rewrite_skill_links(body: str, skill_name: str) -> str:
    out_lines: list[str] = []
    fence: str | None = None
    for line in body.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = marker if fence is None else (None if fence == marker else fence)
            out_lines.append(line)
            continue
        if fence is not None:
            out_lines.append(line)
            continue

        def _repl(match: re.Match[str]) -> str:
            label, href = match.group(1), match.group(2)
            norm_href = href.removeprefix("./")
            if skill_name and norm_href.startswith("references/"):
                return f"[{label}](../ppa/skills/{skill_name}/{norm_href})"
            m_amb = re.match(r"^\.\./skills/(ppa-[a-z0-9-]+)/references/(.+)$", norm_href)
            if m_amb:
                return f"[{label}](../ppa/skills/{m_amb.group(1)}/references/{m_amb.group(2)})"
            m_sib = re.match(r"^\.\./(ppa-[a-z0-9-]+)/references/(.+)$", norm_href)
            if m_sib:
                return f"[{label}](../ppa/skills/{m_sib.group(1)}/references/{m_sib.group(2)})"
            return match.group(0)

        out_lines.append(LINK_RE.sub(_repl, line))
    return "\n".join(out_lines)


def _compile_skill_mdc(skill_md: Path) -> tuple[str, str]:
    raw = common.read_utf8_strict(skill_md)
    meta, fm_lines, body = common.split_frontmatter(raw)
    if not meta or "name" not in meta or "description" not in meta:
        raise common.AdapterError(f"{skill_md}: invalid SKILL.md frontmatter")
    name = meta["name"]
    desc = meta["description"]
    mdc_rel = (
        ".cursor/rules/ppa-router.mdc"
        if name == common.ROUTER_SKILL
        else f".cursor/rules/ppa-skill-{name.removeprefix('ppa-')}.mdc"
    )
    fm_block = _format_mdc_frontmatter(desc, max(len(fm_lines), 6))
    rewritten_body = _rewrite_skill_links(body, name)
    compiled = fm_block + "\n" + rewritten_body
    n_lines = len(common.split_lines_n2(compiled))
    lo, hi = (50, 100) if name == common.ROUTER_SKILL else (250, 500)
    if not lo <= n_lines < hi:
        single_fm = "\n".join([
            "---",
            f"description: {json.dumps(desc, ensure_ascii=False)}" if ":" in desc else f"description: {desc}",
            "globs:",
            "alwaysApply: false",
            "---",
        ])
        compiled = single_fm + "\n" + rewritten_body
    return mdc_rel, compiled


def _compile_ambient_mdc(amb_path: Path) -> tuple[str, str]:
    raw = common.normalize_lf(common.read_utf8_strict(amb_path))
    _, _, body = common.split_frontmatter(raw)
    desc = common.ambient_trigger_description(amb_path)
    fm_block = "\n".join([
        "---",
        f'description: "{desc}"',
        "globs:",
        "alwaysApply: false",
        "---",
    ])
    compiled = fm_block + "\n" + _rewrite_skill_links(body.lstrip("\n"), "")
    lines = common.split_lines_n2(compiled)
    if len(lines) > 250:
        compact: list[str] = []
        prev_blank = False
        for ln in lines:
            blank = not ln.strip()
            if blank and prev_blank:
                continue
            compact.append(ln)
            prev_blank = blank
        compiled = "\n".join(compact) + "\n"
    slug = amb_path.stem.removeprefix("ppa-")
    return f".cursor/rules/ppa-ambient-{slug}.mdc", compiled


def compile_port(
    repo_root: Path,
    port_root: Path,
    canonical_revision: str | None = None,
    extra_surfaces: list[str] | None = None,
    user_home: str | None = None,
) -> dict[str, object]:
    """Compile canonical core into Cursor .cursor/rules/*.mdc and .cursor/ppa/."""
    repo_root = repo_root.resolve()
    port_root = port_root.resolve()
    uhome = common.resolve_user_home(port_root, user_home)
    surfaces = common.snapshot_always_on_surfaces(port_root, TARGET, extra_surfaces, uhome)
    pre_existing = common.scan_preexisting_discovery(port_root, TARGET)
    k_files, o_files, c_files = common.collect_canonical_package(repo_root)
    rev = common.resolve_canonical_revision(repo_root, canonical_revision)
    port_root.mkdir(parents=True, exist_ok=True)

    mappings: list[dict[str, object]] = []
    for kpath in k_files:
        rel_src = kpath.relative_to(repo_root)
        parts = kpath.relative_to(repo_root / "knowledge").parts
        if parts[0] == "skills" and parts[-1] == "SKILL.md":
            rel_dst_str, mdc_text = _compile_skill_mdc(kpath)
            common.write_utf8_lf(port_root / rel_dst_str, mdc_text)
            mappings.append({
                "canonical": rel_src.as_posix(),
                "kind": "transforming",
                "port": [rel_dst_str],
            })
        elif parts[0] == "ambient-context":
            rel_dst_str, mdc_text = _compile_ambient_mdc(kpath)
            common.write_utf8_lf(port_root / rel_dst_str, mdc_text)
            mappings.append({
                "canonical": rel_src.as_posix(),
                "kind": "transforming",
                "port": [rel_dst_str],
            })
        else:
            rel_dst = Path(".cursor") / "ppa" / Path(*parts)
            common.copy_lossless(kpath, port_root / rel_dst)
            mappings.append({
                "canonical": rel_src.as_posix(),
                "kind": "lossless",
                "port": [rel_dst.as_posix()],
            })

    for opath in o_files:
        rel_src = opath.relative_to(repo_root)
        rel_dst = Path(".cursor") / "ppa" / "ontology" / opath.relative_to(repo_root / "ontology")
        common.copy_lossless(opath, port_root / rel_dst)
        mappings.append({
            "canonical": rel_src.as_posix(),
            "kind": "lossless",
            "port": [rel_dst.as_posix()],
        })

    common.copy_corpus_closure(repo_root, c_files, port_root / ".cursor" / "ppa" / "corpus")
    manifest: dict[str, object] = {
        "always_on_surfaces": surfaces,
        "canonical_revision": rev,
        "corpus_root": ".cursor/ppa/corpus",
        "deviations": [],
        "discovery_entries": common.collect_skill_discovery(repo_root, include_ambient=True),
        "mappings": mappings,
        "pre_existing_discovery": pre_existing,
        "spec_version": "1",
        "target": TARGET,
    }
    common.write_port_manifest(port_root, manifest)
    return manifest


def _cli(argv: list[str]) -> int:
    ap = common.base_arg_parser("Compile PPA package for Cursor IDE (.cursor/rules/)")
    args = ap.parse_args(argv)
    compile_port(
        repo_root=Path(args.repo_root),
        port_root=Path(args.port_root),
        canonical_revision=args.canonical_revision,
        extra_surfaces=args.always_on_surfaces,
        user_home=args.user_home,
    )
    return 0


if __name__ == "__main__":
    sys.exit(common.run_adapter_cli(_cli))
