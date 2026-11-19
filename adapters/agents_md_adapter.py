#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic Codex / AGENTS.md compiler installing
#   .agents/skills/ and .agents/ppa-ambient/ with zero default AGENTS.md edits,
#   plus explicit operator-requested DEV-STUB recording (<=12L, <=800B).
"""Compile canonical PPA knowledge into an AGENTS.md / .agents/ harness port."""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))

from adapters import common  # noqa: E402

TARGET = "codex-agents"

DEV_STUB_TEXT = (
    "# PPA On-Demand Knowledge Index\n"
    "- Router: `.agents/skills/ppa-program-analysis/SKILL.md`\n"
    "- Domain skills: `.agents/skills/ppa-*/SKILL.md`\n"
    "- Ambient orientation: `.agents/ppa-ambient/ppa-*.md`\n"
    "- Load only the skill matching the active static analysis task.\n"
)


def _apply_dev_stub(port_root: Path) -> dict[str, str]:
    stub_bytes = DEV_STUB_TEXT.encode("utf-8")
    stub_lines = common.split_lines_n2(DEV_STUB_TEXT)
    if len(stub_lines) > 12 or len(stub_bytes) > 800:
        raise common.AdapterError("DEV-STUB exceeds 12 lines or 800 bytes")
    agents_md = port_root / "AGENTS.md"
    existing = common.read_utf8_strict(agents_md) if agents_md.is_file() else ""
    norm = common.normalize_lf(existing)
    if DEV_STUB_TEXT not in norm:
        common.write_utf8_lf(agents_md, norm + DEV_STUB_TEXT)
    return {
        "id": "DEV-STUB",
        "surface": "AGENTS.md",
        "text": DEV_STUB_TEXT,
    }


def compile_port(
    repo_root: Path,
    port_root: Path,
    canonical_revision: str | None = None,
    extra_surfaces: list[str] | None = None,
    user_home: str | None = None,
    emit_dev_stub: bool = False,
) -> dict[str, object]:
    """Compile canonical core into <port_root>/.agents/ and emit port_manifest.json."""
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
        if parts[0] == "skills":
            rel_dst = Path(".agents") / "skills" / Path(*parts[1:])
        elif parts[0] == "ambient-context":
            rel_dst = Path(".agents") / "ppa-ambient" / Path(*parts[1:])
        else:
            raise common.AdapterError(f"unexpected knowledge path: {rel_src.as_posix()}")
        common.copy_lossless(kpath, port_root / rel_dst)
        mappings.append({
            "canonical": rel_src.as_posix(),
            "kind": "lossless",
            "port": [rel_dst.as_posix()],
        })

    for opath in o_files:
        rel_src = opath.relative_to(repo_root)
        rel_dst = Path(".agents") / "core" / "ontology" / opath.relative_to(repo_root / "ontology")
        common.copy_lossless(opath, port_root / rel_dst)
        mappings.append({
            "canonical": rel_src.as_posix(),
            "kind": "lossless",
            "port": [rel_dst.as_posix()],
        })

    common.copy_corpus_closure(repo_root, c_files, port_root / ".agents" / "core" / "corpus")
    deviations: list[object] = []
    if emit_dev_stub:
        deviations.append(_apply_dev_stub(port_root))

    manifest: dict[str, object] = {
        "adapter_options": {"emit_dev_stub": emit_dev_stub},
        "always_on_surfaces": surfaces,
        "canonical_revision": rev,
        "corpus_root": ".agents/core/corpus",
        "deviations": deviations,
        "discovery_entries": common.collect_skill_discovery(repo_root, include_ambient=False),
        "mappings": mappings,
        "pre_existing_discovery": pre_existing,
        "spec_version": "1",
        "target": TARGET,
    }
    common.write_port_manifest(port_root, manifest)
    return manifest


def _cli(argv: list[str]) -> int:
    ap = common.base_arg_parser("Compile PPA package for AGENTS.md / .agents/ harnesses")
    ap.add_argument("--emit-dev-stub", action="store_true",
                    help="record operator-authorized DEV-STUB pointer block in AGENTS.md")
    args = ap.parse_args(argv)
    compile_port(
        repo_root=Path(args.repo_root),
        port_root=Path(args.port_root),
        canonical_revision=args.canonical_revision,
        extra_surfaces=args.always_on_surfaces,
        user_home=args.user_home,
        emit_dev_stub=args.emit_dev_stub,
    )
    return 0


if __name__ == "__main__":
    sys.exit(common.run_adapter_cli(_cli))
