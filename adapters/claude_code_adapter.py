#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic Claude Code (.claude/) compiler mapping
#   skills and core ontology losslessly, installing ambient orientation files as
#   router-linked references (no description-matched ambient channel), and
#   adding zero bytes to CLAUDE.md always-on instruction surfaces.
"""Compile canonical PPA knowledge into a Claude Code (.claude/) port layout."""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))

from adapters import common, port_plan  # noqa: E402

TARGET = "claude-code"


def compile_port(
    repo_root: Path,
    port_root: Path,
    canonical_revision: str | None = None,
    extra_surfaces: list[str] | None = None,
    user_home: str | None = None,
    force: bool = False,
    manifest_name: str = common.DEFAULT_MANIFEST_NAME,
) -> dict[str, object]:
    """Compile canonical core into <port_root>/.claude/ and emit port_manifest.json."""
    repo_root = repo_root.resolve()
    port_root = port_root.resolve()
    plan = port_plan.PortPlan(port_root, TARGET, force=force, manifest_name=manifest_name)
    uhome = common.resolve_user_home(port_root, user_home)
    surfaces = common.snapshot_always_on_surfaces(port_root, TARGET, extra_surfaces, uhome)
    pre_existing = common.scan_preexisting_discovery(port_root, TARGET, prior=plan.prior)
    k_files, o_files, c_files = common.collect_canonical_package(repo_root)
    rev = common.resolve_canonical_revision(repo_root, canonical_revision)

    mappings = port_plan.plan_skill_tree(plan, repo_root, k_files, ".claude/skills")
    mappings += port_plan.plan_ontology_and_corpus(plan, repo_root, o_files, c_files, ".claude/core")
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
    plan.commit(manifest)
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
        force=args.force,
        manifest_name=args.manifest_name,
    )
    return 0


if __name__ == "__main__":
    sys.exit(common.run_adapter_cli(_cli))
