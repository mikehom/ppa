#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Two-phase port compilation. Every output is planned in
#   memory, checked against files that the previous port manifest does not own,
#   and only then written, so a foreign file is never overwritten unless the
#   operator passes --force; targets without an on-demand ambient channel get
#   the orientation files as router-linked references (ARCHITECTURE 4.4).
"""Plan-then-commit write protection and shared mapping steps for the adapters."""
from __future__ import annotations

import json
import re
from pathlib import Path

from adapters import common

ROLE_KEYS = {
    "extra": "extra_units",
    "index": "index_files",
    "manifest": "manifest_files",
    "bundle": "notebooklm_bundle",
    "merged": "merged_files",
}
FALLBACK_HEADING = "## Orientation Guides (R1 Fallback)"
AMBIENT_REF_LINK_RE = re.compile(
    r"(?<!!)\[([^\]]*)\]\(\.\./skills/(ppa-[a-z0-9-]+/references/[^)\s]+)\)"
)


class PortPlan:
    """In-memory set of port outputs, committed only after the collision guard passes."""

    def __init__(self, port_root: Path, target: str, force: bool = False) -> None:
        self.port_root = port_root
        self.target = target
        self.force = force
        loaded = common.load_prior_manifest(port_root)
        # A manifest written for another target confers no ownership and no history.
        self.prior = loaded if (loaded is not None and loaded.get("target") == target) else None
        self._prior_owned: set[str] = (
            common.manifest_owned_paths(port_root, self.prior) if self.prior else set()
        )
        self._outputs: dict[str, tuple[str, bytes]] = {}

    def owns(self, rel: str) -> bool:
        """True when the previous manifest in this port root lists rel as its output."""
        return rel in self._prior_owned

    def add_bytes(self, rel: str, data: bytes, role: str = "mapped") -> str:
        """Plan raw bytes for a port-relative path under one ownership role."""
        if not common.is_safe_rel(rel):
            raise common.AdapterError(f"planned output {rel!r} is not a safe relative path")
        if role != "mapped" and role not in ROLE_KEYS:
            raise common.AdapterError(f"unknown output role {role!r} for {rel}")
        if rel in self._outputs:
            raise common.AdapterError(f"two outputs planned for the same path: {rel}")
        self._outputs[rel] = (role, data)
        return rel

    def add(self, rel: str, content: str, role: str = "mapped") -> str:
        """Plan LF-normalised UTF-8 text for a port-relative path."""
        return self.add_bytes(rel, common.normalize_lf(content).encode("utf-8"), role)

    def add_copy(self, src: Path, rel: str, role: str = "mapped") -> str:
        """Plan a lossless LF-normalised copy of a canonical file."""
        if src.is_symlink():
            raise common.AdapterError(f"canonical source must not be a symlink: {src}")
        return self.add(rel, common.read_utf8_strict(src), role)

    def paths(self, role: str) -> list[str]:
        """Sorted planned paths recorded under one role."""
        return sorted(rel for rel, (r, _) in self._outputs.items() if r == role)

    def collisions(self) -> tuple[list[str], list[str]]:
        """Return (foreign files that --force may overwrite, obstacles that always abort)."""
        foreign: list[str] = []
        fatal: list[str] = []
        root = self.port_root
        for rel, (role, _) in sorted(self._outputs.items()):
            dest = root / rel
            parent = dest.parent
            while parent != root and root in parent.parents:
                if parent.is_symlink():
                    fatal.append(f"{rel} (symlinked directory {parent.relative_to(root).as_posix()})")
                    break
                if parent.exists() and not parent.is_dir():
                    fatal.append(f"{rel} ({parent.relative_to(root).as_posix()} is not a directory)")
                    break
                parent = parent.parent
            if dest.is_symlink():
                fatal.append(f"{rel} (symlink)")
            elif dest.is_dir():
                fatal.append(f"{rel} (directory)")
            elif dest.exists() and role != "merged" and not self.owns(rel):
                foreign.append(rel)
        return foreign, fatal

    def commit(self, manifest: dict[str, object]) -> Path:
        """Record ownership lists in the manifest, run the guard, then write everything."""
        for role, key in ROLE_KEYS.items():
            listed = set(self.paths(role))
            if role == "manifest":
                listed.add("port_manifest.json")
            if listed or role != "bundle":
                manifest[key] = sorted(listed)
        self.add(
            "port_manifest.json",
            json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            role="manifest",
        )
        foreign, fatal = self.collisions()
        if fatal:
            raise common.AdapterError(
                "refusing to write through obstacles (nothing was written): " + "; ".join(fatal[:10]))
        if foreign and not self.force:
            shown = ", ".join(foreign[:10]) + (f" (+{len(foreign) - 10} more)" if len(foreign) > 10 else "")
            raise common.AdapterError(
                f"{len(foreign)} pre-existing file(s) are not owned by a previous port manifest "
                f"for target {self.target!r}: {shown}. Nothing was written; pass --force to overwrite.")
        self.port_root.mkdir(parents=True, exist_ok=True)
        for rel, (_, data) in sorted(self._outputs.items()):
            dest = self.port_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        return self.port_root / "port_manifest.json"


def plan_ontology_and_corpus(
    plan: PortPlan, repo_root: Path, o_files: list[Path], c_files: list[Path], core_dir: str
) -> list[dict[str, object]]:
    """Plan lossless ontology copies (mapped) and the corpus closure (extra units)."""
    mappings: list[dict[str, object]] = []
    for opath in o_files:
        rel_src = opath.relative_to(repo_root).as_posix()
        rel_dst = f"{core_dir}/ontology/{opath.relative_to(repo_root / 'ontology').as_posix()}"
        plan.add_copy(opath, rel_dst)
        mappings.append({"canonical": rel_src, "kind": "lossless", "port": [rel_dst]})
    for cpath in c_files:
        rel_c = cpath.relative_to(repo_root / "corpus").as_posix()
        plan.add_copy(cpath, f"{core_dir}/corpus/{rel_c}", role="extra")
    return mappings


def _router_with_fallback(router_md: Path, ambient: list[Path]) -> str:
    """Append the router-linked orientation section and re-check the router budget."""
    text = common.normalize_lf(common.read_utf8_strict(router_md))
    lines = common.split_lines_n2(text)
    if any(ln.strip() == FALLBACK_HEADING for ln in lines):
        raise common.AdapterError(f"{router_md}: canonical router already carries {FALLBACK_HEADING!r}")
    extra = ([""] if lines and lines[-1].strip() else []) + [FALLBACK_HEADING, ""]
    extra += [f"- [{amb.name}](references/ambient-{amb.stem.removeprefix('ppa-')}.md)" for amb in ambient]
    total = len(lines) + len(extra)
    if not 50 <= total < 100:
        raise common.AdapterError(
            f"{router_md}: router with orientation links is {total} lines (must be 50-99, C3.1)")
    return "\n".join(lines + extra) + "\n"


def plan_skill_tree(
    plan: PortPlan, repo_root: Path, k_files: list[Path], skills_dir: str
) -> list[dict[str, object]]:
    """Plan skills losslessly and ambient files as router-linked references.

    Used by targets with no description-matched ambient channel: each ambient file
    becomes ``<router>/references/ambient-<slug>.md`` and the router gains one link
    per file, so every orientation file stays reachable through an R2 hop.
    """
    kroot = repo_root / "knowledge"
    ambient = [k for k in k_files if k.relative_to(kroot).parts[0] == "ambient-context"]
    router_refs = {k.name for k in k_files
                   if k.relative_to(kroot).parts[:3] == ("skills", common.ROUTER_SKILL, "references")}
    mappings: list[dict[str, object]] = []
    for kpath in k_files:
        rel_src = kpath.relative_to(repo_root).as_posix()
        parts = kpath.relative_to(kroot).parts
        kind = "lossless"
        if parts[0] == "skills" and parts[1:] == (common.ROUTER_SKILL, "SKILL.md") and ambient:
            rel_dst = f"{skills_dir}/{'/'.join(parts[1:])}"
            plan.add(rel_dst, _router_with_fallback(kpath, ambient))
            kind = "transforming"
        elif parts[0] == "skills":
            rel_dst = f"{skills_dir}/{'/'.join(parts[1:])}"
            plan.add_copy(kpath, rel_dst)
        elif parts[0] == "ambient-context" and len(parts) == 2:
            name = f"ambient-{kpath.stem.removeprefix('ppa-')}.md"
            if name in router_refs:
                raise common.AdapterError(f"{rel_src}: router already owns references/{name}")
            rel_dst = f"{skills_dir}/{common.ROUTER_SKILL}/references/{name}"
            body = common.normalize_lf(common.read_utf8_strict(kpath))
            rewritten = AMBIENT_REF_LINK_RE.sub(lambda m: f"[{m.group(1)}](../../{m.group(2)})", body)
            plan.add(rel_dst, rewritten)
            kind = "transforming" if rewritten != body else "lossless"
        else:
            raise common.AdapterError(f"unexpected file under knowledge/: {rel_src}")
        mappings.append({"canonical": rel_src, "kind": kind, "port": [rel_dst]})
    return mappings
