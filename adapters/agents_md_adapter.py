#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Deterministic Codex / AGENTS.md compiler installing
#   .agents/skills/ (ambient files as router-linked references) with zero default
#   AGENTS.md edits, plus explicit operator-requested DEV-STUB recording
#   (<=12L, <=800B).
# @decision DEC-PPA-009: A pointer stub found on disk is always declared as
#   DEV-STUB and the surface baseline is taken with the stub removed, so a later
#   run without the flag cannot turn a stubbed surface into a clean verdict.
"""Compile canonical PPA knowledge into an AGENTS.md / .agents/ harness port."""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE.parent) not in sys.path:
    sys.path.insert(0, str(_HERE.parent))

from adapters import common, port_plan  # noqa: E402

TARGET = "codex-agents"
STUB_SURFACE = "AGENTS.md"

DEV_STUB_TEXT = (
    f"{common.STUB_START}\n"
    "# PPA On-Demand Knowledge Index\n"
    "- Router: `.agents/skills/ppa-program-analysis/SKILL.md`\n"
    "- Domain skills: `.agents/skills/ppa-*/SKILL.md`\n"
    "- Orientation guides: `.agents/skills/ppa-program-analysis/references/ambient-*.md`\n"
    "- Load only the skill matching the active static analysis task.\n"
    f"{common.STUB_END}\n"
)


def _prior_stub_text(prior: dict[str, object] | None) -> str | None:
    devs = prior.get("deviations") if prior else None
    for item in devs if isinstance(devs, list) else []:
        if (isinstance(item, dict) and item.get("id") == "DEV-STUB"
                and item.get("surface") == STUB_SURFACE and isinstance(item.get("text"), str)):
            return item["text"]
    return None


def _resolve_dev_stub(
    plan: port_plan.PortPlan, emit_dev_stub: bool
) -> tuple[dict[str, str] | None, dict[str, bytes | None]]:
    """Return (DEV-STUB record or None, baseline bytes of the stub surface).

    A stub already on disk is declared whether or not the flag is passed; the
    baseline is the surface with the stub text removed. A marker without a
    recognisable stub text is refused: it cannot be declared faithfully.
    """
    if len(common.split_lines_n2(DEV_STUB_TEXT)) > 12 or len(DEV_STUB_TEXT.encode("utf-8")) > 800:
        raise common.AdapterError("DEV-STUB exceeds 12 lines or 800 bytes")
    agents_md = plan.port_root / STUB_SURFACE
    if agents_md.is_symlink():
        raise common.AdapterError(f"refusing to read or write a symlinked {STUB_SURFACE}")
    raw = agents_md.read_bytes() if agents_md.is_file() else b""
    candidates = [t for t in (_prior_stub_text(plan.prior), DEV_STUB_TEXT) if t]
    for text in candidates:
        blob = text.encode("utf-8")
        if raw.count(blob) == 1:
            remainder = raw.replace(blob, b"", 1)
            return {"id": "DEV-STUB", "surface": STUB_SURFACE, "text": text}, {STUB_SURFACE: remainder}
    if any(marker.encode("utf-8") in raw for marker in common.STUB_MARKERS):
        raise common.AdapterError(
            f"{STUB_SURFACE} carries a modified or repeated PPA pointer stub; restore the "
            "recorded stub text or remove the block before recompiling")
    if not emit_dev_stub:
        return None, {}
    text = ("\n" if raw and not raw.endswith(b"\n") else "") + DEV_STUB_TEXT
    plan.add_bytes(STUB_SURFACE, raw + text.encode("utf-8"), role="merged")
    return {"id": "DEV-STUB", "surface": STUB_SURFACE, "text": text}, {STUB_SURFACE: raw}


def compile_port(
    repo_root: Path,
    port_root: Path,
    canonical_revision: str | None = None,
    extra_surfaces: list[str] | None = None,
    user_home: str | None = None,
    emit_dev_stub: bool = False,
    force: bool = False,
) -> dict[str, object]:
    """Compile canonical core into <port_root>/.agents/ and emit port_manifest.json."""
    repo_root = repo_root.resolve()
    port_root = port_root.resolve()
    plan = port_plan.PortPlan(port_root, TARGET, force=force)
    uhome = common.resolve_user_home(port_root, user_home)
    stub, baseline = _resolve_dev_stub(plan, emit_dev_stub)
    surfaces = common.snapshot_always_on_surfaces(
        port_root, TARGET, extra_surfaces, uhome, baseline_bytes=baseline)
    pre_existing = common.scan_preexisting_discovery(port_root, TARGET, prior=plan.prior)
    k_files, o_files, c_files = common.collect_canonical_package(repo_root)
    rev = common.resolve_canonical_revision(repo_root, canonical_revision)

    mappings = port_plan.plan_skill_tree(plan, repo_root, k_files, ".agents/skills")
    mappings += port_plan.plan_ontology_and_corpus(plan, repo_root, o_files, c_files, ".agents/core")
    manifest: dict[str, object] = {
        "adapter_options": {"emit_dev_stub": stub is not None},
        "always_on_surfaces": surfaces,
        "canonical_revision": rev,
        "corpus_root": ".agents/core/corpus",
        "deviations": [stub] if stub is not None else [],
        "discovery_entries": common.collect_skill_discovery(repo_root, include_ambient=False),
        "mappings": mappings,
        "pre_existing_discovery": pre_existing,
        "spec_version": "1",
        "target": TARGET,
    }
    plan.commit(manifest)
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
        force=args.force,
    )
    return 0


if __name__ == "__main__":
    sys.exit(common.run_adapter_cli(_cli))
