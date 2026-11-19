#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: A port is certified over the files its manifest owns,
#   never over the whole port root, so a port installed in a real project root
#   is judged on its own files; checks that need a compiled port report N/A in
#   canonical-only mode instead of a self-comparison PASS.
"""Check records, canonical-only scoping, and manifest-owned port file resolution."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from adapters import common

PORT_ONLY_CHECKS = frozenset({
    "C1.1", "C1.2", "C1.7", "C1.12", "C2.1", "C2.2", "C2.3", "C2.4", "C2.6", "C4.8", "C5.7",
})
NA_REASON = "port-only check (requires compiled target port)"
PASSING_STATUSES = frozenset({"PASS", "N/A"})


@dataclass
class CheckOutcome:
    """Single CONFORMANCE_SPEC check result."""

    id: str
    status: str
    examined: int
    failure_code: str | None = None
    locations: list[str] = field(default_factory=list)
    reason: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "examined": self.examined,
            "failure_code": self.failure_code,
            "id": self.id,
            "locations": self.locations[:20],
            "reason": self.reason,
            "status": self.status,
        }


@dataclass
class ConformanceContext:
    """Loaded canonical core, port root, manifest, page map, and deviations."""

    core_root: Path
    port_root: Path
    manifest: dict[str, object]
    canonical_only: bool
    user_home: Path
    denylist_path: Path | None
    port_second: Path | None
    external_export: Path | None
    scratch_base: Path
    page_map: object | None
    page_map_doc: dict | None
    core_graph: dict | None
    port_graph: dict | None
    deviation_ids: set[str]
    dev_stub: dict[str, str] | None
    port_files: list[Path] = field(default_factory=list)
    merged_files: list[str] = field(default_factory=list)
    symlink_errors: list[str] = field(default_factory=list)
    path_errors: list[str] = field(default_factory=list)


def make_check(
    check_id: str,
    examined: int,
    errors: list[str],
    failure_code: str,
    exempt_vacuous: bool = False,
) -> CheckOutcome:
    """Build CheckOutcome applying CONFORMANCE_SPEC 5.4 <gate>_VACUOUS rule."""
    gate = check_id.split(".", 1)[0]
    if errors:
        return CheckOutcome(check_id, "FAIL", examined, failure_code, errors[:20])
    if examined == 0 and not exempt_vacuous:
        return CheckOutcome(check_id, "FAIL", 0, f"{gate}_VACUOUS", [f"{check_id}:0"])
    return CheckOutcome(check_id, "PASS", examined, None, [])


def not_applicable(check_id: str) -> CheckOutcome:
    """Port-only check evaluated without a port: neither PASS nor FAIL."""
    if check_id not in PORT_ONLY_CHECKS:
        raise ValueError(f"{check_id} is not a port-only check")
    return CheckOutcome(check_id, "N/A", 0, None, [], NA_REASON)


def _symlinked_component(port_root: Path, rel: str) -> str | None:
    """Return the first symlinked path component of rel below port_root, if any."""
    cur = port_root
    for part in rel.split("/"):
        cur = cur / part
        if cur.is_symlink():
            return cur.relative_to(port_root).as_posix()
    return None


def resolve_owned_files(
    port_root: Path, manifest: dict[str, object]
) -> tuple[list[Path], list[str], list[str]]:
    """Return (owned regular files, symlink findings, unsafe-path findings).

    Owned paths are the manifest's mapping targets, extra_units, index_files,
    manifest_files, notebooklm_bundle, port_manifest.json, and every file under
    corpus_root. Anything else in the port root is foreign and is not read.
    """
    files: list[Path] = []
    symlinks: list[str] = []
    unsafe: list[str] = []
    listed = common.manifest_listed_paths(manifest)
    for rel in sorted(p for p in listed if not common.is_safe_rel(p)):
        unsafe.append(f"port_manifest.json:0 ({rel!r} is not a relative path inside the port root)")
    for rel in sorted(common.manifest_owned_paths(port_root, manifest)):
        link = _symlinked_component(port_root, rel)
        if link is not None:
            symlinks.append(f"{rel}:0 (symlink at {link})")
        elif (port_root / rel).is_file():
            files.append(port_root / rel)
    return files, symlinks, unsafe


def merged_paths(manifest: dict[str, object]) -> list[str]:
    """Operator-owned files in which the port maintains a bounded block (never scanned whole)."""
    vals = manifest.get("merged_files")
    return sorted(str(v) for v in (vals if isinstance(vals, list) else []) if common.is_safe_rel(str(v)))


def bounded_block_text(text: str) -> str:
    """Blank every line outside the bounded PPA block, keeping line numbers stable."""
    out: list[str] = []
    inside = False
    for line in text.replace("\r\n", "\n").split("\n"):
        stripped = line.strip()
        if stripped == common.KNOWLEDGE_BLOCK_START:
            inside = True
            out.append("")
        elif stripped == common.KNOWLEDGE_BLOCK_END:
            inside = False
            out.append("")
        else:
            out.append(line if inside else "")
    return "\n".join(out)
