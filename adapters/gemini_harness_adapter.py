#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic Gemini CLI compiler installing skills into
#   skills-local/ and ambient topics into memory/topics/ with description: L0
#   frontmatter parity (zero symlinks, zero GEMINI.md mutations).
"""Compile canonical PPA knowledge into a Gemini CLI harness port layout."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))

from adapters import common, port_plan  # noqa: E402

TARGET = "gemini-cli"
AMBIENT_SKILL_LINK_RE = re.compile(
    r"(?<!!)\[([^\]]*)\]\(\.\./skills/(ppa-[a-z0-9-]+/references/[^)\s]+)\)"
)


def _validate_skill_md(skill_md: Path, expected_name: str) -> None:
    meta, _, _ = common.split_frontmatter(common.read_utf8_strict(skill_md))
    if not meta or set(meta) != {"name", "description"} or meta["name"] != expected_name:
        raise common.AdapterError(f"{skill_md}: invalid SKILL.md frontmatter for {expected_name!r}")
    if not 0 < len(meta["description"]) <= 1024:
        raise common.AdapterError(f"{skill_md}: SKILL.md description length out of bounds")


def _compile_memory_topic(
    amb_path: Path, skills_abs: Path, memory_abs: Path
) -> tuple[str, str]:
    """Emit L0 memory topic with description: frontmatter and valid relative links."""
    raw = common.normalize_lf(common.read_utf8_strict(amb_path))
    _, _, body = common.split_frontmatter(raw)
    desc = common.ambient_trigger_description(amb_path)
    rel_to_skills = Path(os.path.relpath(skills_abs, memory_abs)).as_posix()
    rewritten_body = AMBIENT_SKILL_LINK_RE.sub(
        lambda m: f"[{m.group(1)}]({rel_to_skills}/{m.group(2)})",
        body,
    )
    kind = "transforming" if rewritten_body != body else "lossless"
    fm_block = f'---\ndescription: "{desc}"\n---\n'
    compiled = fm_block + rewritten_body
    if len(common.split_lines_n2(compiled)) > 250:
        raise common.AdapterError(f"{amb_path}: L0 memory topic exceeds 250 lines after frontmatter")
    return compiled, kind


def compile_port(
    repo_root: Path,
    port_root: Path,
    canonical_revision: str | None = None,
    extra_surfaces: list[str] | None = None,
    user_home: str | None = None,
    skills_dir: str = "skills-local",
    memory_dir: str = "memory/topics",
    force: bool = False,
    manifest_name: str = common.DEFAULT_MANIFEST_NAME,
) -> dict[str, object]:
    """Compile canonical core into Gemini CLI skills-local/ and memory/topics/."""
    repo_root = repo_root.resolve()
    port_root = port_root.resolve()
    skills_abs = common.ensure_safe_subpath(port_root, skills_dir, "--skills-dir")
    memory_abs = common.ensure_safe_subpath(port_root, memory_dir, "--memory-dir")
    rel_skills = skills_abs.relative_to(port_root)
    rel_memory = memory_abs.relative_to(port_root)

    plan = port_plan.PortPlan(port_root, TARGET, force=force, manifest_name=manifest_name)
    uhome = common.resolve_user_home(port_root, user_home)
    surfaces = common.snapshot_always_on_surfaces(port_root, TARGET, extra_surfaces, uhome)
    pre_existing = common.scan_preexisting_discovery(
        port_root, TARGET, custom_skills_dir=skills_abs, prior=plan.prior)
    k_files, o_files, c_files = common.collect_canonical_package(repo_root)
    rev = common.resolve_canonical_revision(repo_root, canonical_revision)

    mappings: list[dict[str, object]] = []
    for kpath in k_files:
        rel_src = kpath.relative_to(repo_root)
        parts = kpath.relative_to(repo_root / "knowledge").parts
        if parts[0] == "skills":
            if parts[-1] == "SKILL.md":
                _validate_skill_md(kpath, parts[1])
            rel_dst = rel_skills / Path(*parts[1:])
            plan.add_copy(kpath, rel_dst.as_posix())
            kind = "lossless"
        elif parts[0] == "ambient-context":
            rel_dst = rel_memory / Path(*parts[1:])
            content, kind = _compile_memory_topic(kpath, skills_abs, memory_abs)
            plan.add(rel_dst.as_posix(), content)
        else:
            raise common.AdapterError(f"unexpected knowledge path: {rel_src.as_posix()}")
        mappings.append({
            "canonical": rel_src.as_posix(),
            "kind": kind,
            "port": [rel_dst.as_posix()],
        })

    mappings += port_plan.plan_ontology_and_corpus(plan, repo_root, o_files, c_files, "core")
    manifest: dict[str, object] = {
        "adapter_options": {
            "memory_dir": rel_memory.as_posix(),
            "skills_dir": rel_skills.as_posix(),
        },
        "always_on_surfaces": surfaces,
        "canonical_revision": rev,
        "corpus_root": "core/corpus",
        "deviations": [],
        "discovery_entries": common.collect_skill_discovery(repo_root, include_ambient=True),
        "mappings": mappings,
        "pre_existing_discovery": pre_existing,
        "spec_version": "1",
        "target": TARGET,
    }
    plan.commit(manifest)
    return manifest


def _cli(argv: list[str]) -> int:
    ap = common.base_arg_parser("Compile PPA package for Gemini CLI")
    ap.add_argument("--skills-dir", default="skills-local",
                    help="skills subdirectory inside --port-root (default: skills-local)")
    ap.add_argument("--memory-dir", default="memory/topics",
                    help="ambient topics subdirectory inside --port-root (default: memory/topics)")
    args = ap.parse_args(argv)
    compile_port(
        repo_root=Path(args.repo_root),
        port_root=Path(args.port_root),
        canonical_revision=args.canonical_revision,
        extra_surfaces=args.always_on_surfaces,
        user_home=args.user_home,
        skills_dir=args.skills_dir,
        memory_dir=args.memory_dir,
        force=args.force,
        manifest_name=args.manifest_name,
    )
    return 0


if __name__ == "__main__":
    sys.exit(common.run_adapter_cli(_cli))
