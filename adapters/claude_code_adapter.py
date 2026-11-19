#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic Claude Code (.claude/) compiler mapping
#   skills, ambient orientation files, and core ontology losslessly while adding
#   zero bytes to CLAUDE.md always-on instruction surfaces.
"""Compile canonical PPA knowledge into a Claude Code (.claude/) port layout."""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))

from adapters import common  # noqa: E402

TARGET = "claude-code"


def _map_knowledge_rel(rel_k: Path) -> Path:
    parts = rel_k.parts
    if parts[0] == "skills":
        return Path(".claude") / "skills" / Path(*parts[1:])
    if parts[0] == "ambient-context":
        return Path(".claude") / "ppa-ambient" / Path(*parts[1:])
    raise common.AdapterError(f"unexpected file under knowledge/: {rel_k.as_posix()}")


def compile_port(
    repo_root: Path,
    port_root: Path,
    canonical_revision: str | None = None,
    extra_surfaces: list[str] | None = None,
    user_home: str | None = None,
) -> dict[str, object]:
    """Compile canonical core into <port_root>/.claude/ and emit port_manifest.json."""
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
        rel_dst = _map_knowledge_rel(kpath.relative_to(repo_root / "knowledge"))
        common.copy_lossless(kpath, port_root / rel_dst)
        mappings.append({
            "canonical": rel_src.as_posix(),
            "kind": "lossless",
            "port": [rel_dst.as_posix()],
        })

    for opath in o_files:
        rel_src = opath.relative_to(repo_root)
        rel_dst = Path(".claude") / "core" / "ontology" / opath.relative_to(repo_root / "ontology")
        common.copy_lossless(opath, port_root / rel_dst)
        mappings.append({
            "canonical": rel_src.as_posix(),
            "kind": "lossless",
            "port": [rel_dst.as_posix()],
        })

    common.copy_corpus_closure(repo_root, c_files, port_root / ".claude" / "core" / "corpus")
    manifest: dict[str, object] = {
        "always_on_surfaces": surfaces,
        "canonical_revision": rev,
        "corpus_root": ".claude/core/corpus",
        "deviations": [],
        "discovery_entries": common.collect_skill_discovery(repo_root, include_ambient=False),
        "mappings": mappings,
        "pre_existing_discovery": pre_existing,
        "spec_version": "1",
        "target": TARGET,
    }
    common.write_port_manifest(port_root, manifest)
    return manifest


def _cli(argv: list[str]) -> int:
    ap = common.base_arg_parser("Compile PPA package for Claude Code (.claude/)")
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
