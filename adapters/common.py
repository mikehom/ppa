#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Shared stdlib-only compilation primitives enforcing LF
#   normalisation (N4-N6), sorted file walks and JSON keys (N7, C5.7), symbolic
#   always-on surface snapshots (C2.1-C2.2, C5.3), and symlink-free output.
# @decision DEC-PPA-009: Ownership of port files is derived from the previous
#   port manifest only; operator pointer stubs on always-on surfaces are detected
#   on disk so a recompilation can never re-baseline adapter-written bytes.
"""Shared deterministic compilation helpers for PPA reference harness adapters."""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

ROUTER_SKILL = "ppa-program-analysis"
SKILL_NAME_RE = re.compile(r"^ppa-[a-z0-9]+(-[a-z0-9]+)*$")

MINIMUM_ALWAYS_ON_SURFACES: dict[str, tuple[str, ...]] = {
    "claude-code": ("CLAUDE.md", ".claude/CLAUDE.md", "~/.claude/CLAUDE.md"),
    "gemini-cli": ("GEMINI.md", "~/.gemini/GEMINI.md", "~/.gemini/rules/*.md"),
    "codex-agents": ("AGENTS.md",),
    "cursor-ide": (".cursorrules",),
    "mcp-graph-rag": ("system_prompt.md", "templates/always.md"),
    "knowledge-wiki": ("system_prompt.md", "templates/default.md"),
}

STUB_START = "<!-- PPA_STUB_START -->"
STUB_END = "<!-- PPA_STUB_END -->"
STUB_MARKERS = (STUB_START, "# PPA On-Demand Knowledge Index")
KNOWLEDGE_BLOCK_START = "<!-- PPA_KNOWLEDGE_START -->"
KNOWLEDGE_BLOCK_END = "<!-- PPA_KNOWLEDGE_END -->"
OWNED_LIST_KEYS = ("extra_units", "index_files", "manifest_files", "notebooklm_bundle")
AMBIENT_DESC_RE = re.compile(r"<!--\s*@description:\s*(.*?)\s*-->", re.S)

SKIP_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".DS_Store",
    ".user_home",
}


class AdapterError(ValueError):
    """Raised when canonical inputs or target paths violate compilation invariants."""


def read_utf8_strict(path: Path) -> str:
    """Decode a file as strict UTF-8 per CONFORMANCE_SPEC N1."""
    try:
        return path.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as exc:
        raise AdapterError(f"{path}: strict UTF-8 read failed: {exc}") from exc


def normalize_lf(text: str) -> str:
    """Convert CRLF and stray CR to LF without mutating trailing content."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def split_lines_n2(text: str) -> list[str]:
    """CONFORMANCE_SPEC N2 physical line split."""
    norm = text.replace("\r\n", "\n")
    if not norm:
        return []
    parts = norm.split("\n")
    return parts[:-1] if parts[-1] == "" else parts


def is_fm_delim(line: str, first: bool = False) -> bool:
    """CONFORMANCE_SPEC N3 YAML frontmatter delimiter test."""
    s = line.lstrip("\ufeff") if first else line
    return s.rstrip(" \t\r") == "---"


def split_frontmatter(text: str) -> tuple[dict[str, str] | None, list[str], str]:
    """Return (parsed_meta_or_None, raw_fm_lines, body_after_frontmatter)."""
    norm = normalize_lf(text)
    lines = norm.split("\n")
    if not lines or not is_fm_delim(lines[0], first=True):
        return None, [], norm
    end_idx: int | None = None
    for idx in range(1, len(lines)):
        if is_fm_delim(lines[idx]):
            end_idx = idx
            break
    if end_idx is None:
        raise AdapterError("unterminated YAML frontmatter (N3)")
    meta: dict[str, str] = {}
    cur_key: str | None = None
    for lineno, line in enumerate(lines[1:end_idx], start=2):
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            cur_key = m.group(1)
            if cur_key in meta:
                raise AdapterError(f"line {lineno}: duplicate frontmatter key {cur_key!r}")
            val = m.group(2).strip()
            meta[cur_key] = "" if val in {">", "|", ">-", "|-"} else val.strip("\"'")
        elif cur_key is not None and line.startswith((" ", "\t")):
            meta[cur_key] = (meta[cur_key] + " " + line.strip()).strip()
        elif line.strip():
            raise AdapterError(f"line {lineno}: invalid frontmatter line {line!r}")
    body = "\n".join(lines[end_idx + 1:])
    return meta, lines[: end_idx + 1], body


def normalized_body_n5(text: str) -> str:
    """CONFORMANCE_SPEC N4+N5: strip frontmatter, per-line trailing ws, trailing blanks."""
    _, _, body = split_frontmatter(text)
    lines = [ln.rstrip(" \t") for ln in body.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def body_digest_n6(text: str) -> str:
    """CONFORMANCE_SPEC N6 lowercase hex SHA-256 of the normalised body."""
    return hashlib.sha256(normalized_body_n5(text).encode("utf-8")).hexdigest()


def write_utf8_lf(dest: Path, content: str) -> None:
    """Write deterministic LF-normalised UTF-8 text, refusing symlinks."""
    if dest.is_symlink():
        raise AdapterError(f"refusing to write through symlink: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(normalize_lf(content).encode("utf-8"))


def sorted_files_under(base: Path, suffixes: set[str] | None = None) -> list[Path]:
    """Return sorted regular files under base, skipping transient caches."""
    if not base.is_dir():
        return []
    out: list[Path] = []
    for path in sorted(base.rglob("*")):
        rel_parts = path.relative_to(base).parts
        if any(p in SKIP_NAMES for p in rel_parts):
            continue
        if path.is_symlink():
            raise AdapterError(f"symlink forbidden in canonical core: {path}")
        if path.is_file() and (suffixes is None or path.suffix.lower() in suffixes):
            out.append(path)
    return out


def collect_canonical_package(repo_root: Path) -> tuple[list[Path], list[Path], list[Path]]:
    """Return sorted (knowledge_files, ontology_files, corpus_text_files)."""
    k_files = sorted_files_under(repo_root / "knowledge")
    o_files = sorted_files_under(repo_root / "ontology")
    c_files = sorted_files_under(repo_root / "corpus", suffixes={".md", ".json"})
    if not k_files or not o_files:
        raise AdapterError(f"incomplete canonical core under {repo_root}")
    return k_files, o_files, c_files


def resolve_canonical_revision(repo_root: Path, explicit: str | None = None) -> str:
    """Resolve deterministic canonical revision string without wall-clock data."""
    if explicit and explicit.strip():
        return explicit.strip()
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except OSError as exc:
        logging.getLogger("ppa_adapters").debug("git rev-parse unavailable: %s", exc)
    hasher = hashlib.sha256()
    k_files, o_files, _ = collect_canonical_package(repo_root)
    for path in k_files + o_files:
        rel = path.relative_to(repo_root).as_posix()
        hasher.update(f"{rel}\0".encode("utf-8"))
        hasher.update(normalize_lf(read_utf8_strict(path)).encode("utf-8"))
        hasher.update(b"\0")
    return f"tree-{hasher.hexdigest()[:16]}"


def resolve_user_home(port_root: Path, explicit_home: str | None = None) -> Path:
    """Resolve user-scope root for '~/' surface checks without leaking paths."""
    if explicit_home:
        return Path(explicit_home).resolve()
    env_home = os.environ.get("PPA_USER_HOME")
    if env_home:
        return Path(env_home).resolve()
    local_home = port_root / ".user_home"
    if local_home.is_dir():
        return local_home.resolve()
    return Path.home().resolve()


def surface_files(port_root: Path, surface: str, user_home: Path) -> list[Path]:
    """Return the existing regular files a surface specification denotes (glob-aware)."""
    if surface.startswith("~/"):
        rel_pattern, anchor = surface[2:], user_home
    else:
        rel_pattern, anchor = surface.lstrip("/"), port_root
    if any(ch in rel_pattern for ch in ("*", "?", "[")):
        return sorted(p for p in anchor.glob(rel_pattern) if p.is_file())
    target_path = anchor / rel_pattern
    return [target_path] if target_path.is_file() else []


def compute_surface_sha256(port_root: Path, surface: str, user_home: Path) -> str | None:
    """Compute raw-byte SHA-256 (or deterministic multi-file glob digest) for a surface.

    A glob surface is digested as SHA-256 over one ``<relative path>:<file sha256>``
    line per matching file, in sorted path order; no match yields None.
    """
    matches = surface_files(port_root, surface, user_home)
    if not matches:
        return None
    is_glob = any(ch in surface for ch in ("*", "?", "["))
    if not is_glob:
        return hashlib.sha256(matches[0].read_bytes()).hexdigest()
    anchor = user_home if surface.startswith("~/") else port_root
    h = hashlib.sha256()
    for m in matches:
        rel_m = m.relative_to(anchor).as_posix()
        file_digest = hashlib.sha256(m.read_bytes()).hexdigest()
        h.update(f"{rel_m}:{file_digest}\n".encode("utf-8"))
    return h.hexdigest()


def surface_stub_markers(port_root: Path, surface: str, user_home: Path) -> list[str]:
    """Return the names of surface files that carry a pointer-stub marker."""
    markers = [marker.encode("utf-8") for marker in STUB_MARKERS]
    return [
        path.name
        for path in surface_files(port_root, surface, user_home)
        if any(marker in path.read_bytes() for marker in markers)
    ]


def discover_extra_always_on(port_root: Path, target: str) -> list[str]:
    """Find pre-existing dynamic always-on surfaces under port_root before install."""
    found: list[str] = []
    if not port_root.is_dir():
        return found
    if target == "codex-agents":
        for p in sorted(port_root.rglob("AGENTS.md")):
            if p.is_file():
                rel = p.relative_to(port_root).as_posix()
                if rel != "AGENTS.md":
                    found.append(rel)
    elif target == "cursor-ide":
        rules_dir = port_root / ".cursor" / "rules"
        if rules_dir.is_dir():
            for p in sorted(rules_dir.glob("*.mdc")):
                if not p.is_file():
                    continue
                meta, _, _ = split_frontmatter(read_utf8_strict(p))
                if meta and meta.get("alwaysApply", "").lower() == "true":
                    found.append(p.relative_to(port_root).as_posix())
    elif target == "knowledge-wiki":
        tmpl_dir = port_root / "templates"
        if tmpl_dir.is_dir():
            for p in sorted(tmpl_dir.glob("default*")):
                if p.is_file():
                    rel = p.relative_to(port_root).as_posix()
                    if rel != "templates/default.md":
                        found.append(rel)
    return found


def snapshot_always_on_surfaces(
    port_root: Path,
    target: str,
    extra_surfaces: list[str] | None,
    user_home: Path,
    baseline_bytes: dict[str, bytes | None] | None = None,
) -> list[dict[str, object]]:
    """Snapshot minimum + dynamic + caller-declared always-on surfaces pre-install.

    ``baseline_bytes`` maps a surface to its content with adapter-written bytes
    removed (None or empty: absent); it replaces the on-disk bytes for that surface
    so a pointer stub written by an earlier run is never recorded as the baseline.
    """
    ordered: list[str] = list(MINIMUM_ALWAYS_ON_SURFACES.get(target, ()))
    for item in discover_extra_always_on(port_root, target):
        if item not in ordered:
            ordered.append(item)
    for item in extra_surfaces or []:
        clean = item.strip()
        if clean and clean not in ordered:
            ordered.append(clean)
    out: list[dict[str, object]] = []
    for surf in ordered:
        if baseline_bytes is not None and surf in baseline_bytes:
            raw = baseline_bytes[surf] or b""
            digest = hashlib.sha256(raw).hexdigest() if raw else None
            size: int | None = len(raw) if raw else None
        else:
            files = surface_files(port_root, surf, user_home)
            digest = compute_surface_sha256(port_root, surf, user_home)
            size = sum(f.stat().st_size for f in files) if files else None
        out.append({"bytes_before": size, "path": surf, "sha256_before": digest})
    return out


def is_safe_rel(rel: str) -> bool:
    """True when rel is a non-empty relative POSIX path with no parent traversal."""
    if not rel or rel.startswith("/") or "\\" in rel or re.match(r"^[A-Za-z]:", rel):
        return False
    return ".." not in rel.split("/")


def load_prior_manifest(port_root: Path) -> dict[str, object] | None:
    """Return the previous port_manifest.json as a dict, or None when absent/unreadable."""
    manifest_path = port_root / "port_manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        return None
    try:
        doc = json.loads(read_utf8_strict(manifest_path))
    except (json.JSONDecodeError, AdapterError) as exc:
        logging.getLogger("ppa_adapters").warning(
            "ignoring unreadable previous port_manifest.json (treated as foreign): %s", exc)
        return None
    return doc if isinstance(doc, dict) else None


def manifest_listed_paths(manifest: dict[str, object]) -> set[str]:
    """File-backed port outputs a manifest declares (mappings and owned-list keys)."""
    listed: set[str] = {"port_manifest.json"}
    mappings = manifest.get("mappings")
    for m in mappings if isinstance(mappings, list) else []:
        ports = m.get("port") if isinstance(m, dict) else None
        listed.update(str(p) for p in (ports if isinstance(ports, list) else []))
    for key in OWNED_LIST_KEYS:
        vals = manifest.get(key)
        listed.update(str(p) for p in (vals if isinstance(vals, list) else []))
    return {p for p in listed if not p.startswith("ppa:")}


def manifest_owned_paths(port_root: Path, manifest: dict[str, object]) -> set[str]:
    """Port-relative paths owned by a manifest: its listed outputs plus the corpus_root tree."""
    owned = {p for p in manifest_listed_paths(manifest) if is_safe_rel(p)}
    corpus_rel = str(manifest.get("corpus_root") or "").strip("/")
    if corpus_rel and is_safe_rel(corpus_rel) and (port_root / corpus_rel).is_dir():
        for dirpath, dirnames, filenames in os.walk(port_root / corpus_rel, followlinks=False):
            here = Path(dirpath)
            linked_dirs = [d for d in dirnames if (here / d).is_symlink()]
            for name in sorted(filenames) + linked_dirs:
                owned.add((here / name).relative_to(port_root).as_posix())
    return owned


def emitted_discovery_names(manifest: dict[str, object]) -> set[str]:
    """Discovery names a port actually emits: skill directories, rule stems, indexed entries."""
    names: set[str] = set()
    mappings = manifest.get("mappings")
    for m in mappings if isinstance(mappings, list) else []:
        ports = m.get("port") if isinstance(m, dict) else None
        for raw in ports if isinstance(ports, list) else []:
            parts = str(raw).split("/")
            if parts[-1].endswith(".mdc"):
                names.add(parts[-1][: -len(".mdc")])
            elif parts[-1] == "SKILL.md" and len(parts) >= 2:
                names.add(parts[-2])
    entries = manifest.get("discovery_entries")
    for e in entries if isinstance(entries, list) else []:
        if isinstance(e, dict) and e.get("name"):
            names.add(str(e["name"]))
    return names


def scan_preexisting_discovery(
    port_root: Path,
    target: str,
    custom_skills_dir: Path | None = None,
    prior: dict[str, object] | None = None,
) -> list[str]:
    """Collect discovery names present before install that no previous port emitted.

    A collision recorded by a previous (forced) run is carried forward: once a
    foreign entry was overwritten, recompiling must not erase the record (C4.8).
    """
    prior_emitted = emitted_discovery_names(prior) if prior else set()
    carried: set[str] = set()
    if prior and isinstance(prior.get("pre_existing_discovery"), list):
        carried = {str(x) for x in prior["pre_existing_discovery"]} & prior_emitted
    if not port_root.is_dir():
        return sorted(carried)
    candidates: set[str] = set()
    search_dirs = {
        "claude-code": [port_root / ".claude" / "skills"],
        "gemini-cli": [custom_skills_dir or (port_root / "skills-local")],
        "codex-agents": [port_root / ".agents" / "skills"],
    }.get(target, [])
    for sdir in search_dirs:
        if sdir.is_dir():
            for child in sorted(sdir.iterdir()):
                if child.is_dir() and (child / "SKILL.md").is_file():
                    candidates.add(child.name)
    if target == "cursor-ide":
        rdir = port_root / ".cursor" / "rules"
        if rdir.is_dir():
            for mdc in sorted(rdir.glob("*.mdc")):
                candidates.add(mdc.stem)
    return sorted((candidates - prior_emitted) | carried)


def ambient_trigger_description(amb_path: Path) -> str:
    """Return the ambient file's discovery description (<=1024 chars, no N8, no lists).

    The canonical ``<!-- @description: ... -->`` directive is lifted verbatim (inner
    whitespace runs collapsed to one space); a title-based sentence is synthesised
    only when the file carries no directive.
    """
    text = read_utf8_strict(amb_path)
    declared = AMBIENT_DESC_RE.search(text)
    if declared:
        desc = " ".join(declared.group(1).split())
        if not desc or len(desc) > 1024 or '"' in desc or "\\" in desc:
            raise AdapterError(
                f"{amb_path.name}: @description must be 1-1024 characters without "
                "double quotes or backslashes")
        return desc
    title = amb_path.stem.replace("-", " ")
    for line in split_lines_n2(text):
        if line.startswith("# "):
            title = line[2:].strip().replace('"', "'")
            break
    slug_words = amb_path.stem.removeprefix("ppa-").replace("-", " ")
    desc = (
        f"Orientation guide for {title} grounded in Principles of Program Analysis. "
        f"Use when orienting on {slug_words} terminology, polarity, and soundness "
        f"assumptions before loading a specialised analysis skill. "
        f"Do not use as a substitute for full rule preconditions in skill references."
    )
    return desc[:1024]


def collect_skill_discovery(repo_root: Path, include_ambient: bool = False) -> list[dict[str, object]]:
    """Build deterministic discovery_entries list from canonical skills (+ ambient)."""
    skills_base = repo_root / "knowledge" / "skills"
    entries: list[dict[str, object]] = []
    if skills_base.is_dir():
        for skill_md in sorted(skills_base.glob("*/SKILL.md")):
            meta, _, _ = split_frontmatter(read_utf8_strict(skill_md))
            if not meta or "name" not in meta or "description" not in meta:
                raise AdapterError(f"{skill_md}: missing name/description frontmatter")
            entries.append({
                "name": meta["name"],
                "description_chars": len(meta["description"]),
            })
    if include_ambient:
        amb_base = repo_root / "knowledge" / "ambient-context"
        if amb_base.is_dir():
            for amb in sorted(amb_base.glob("ppa-*.md")):
                desc = ambient_trigger_description(amb)
                entries.append({
                    "name": amb.name,
                    "description_chars": len(desc),
                })
    return entries


def ensure_safe_subpath(port_root: Path, raw_subpath: str, flag_name: str) -> Path:
    """Resolve a configurable directory inside port_root, rejecting escapes."""
    cand = Path(raw_subpath)
    resolved = (port_root / cand).resolve() if not cand.is_absolute() else cand.resolve()
    root_res = port_root.resolve()
    if resolved != root_res and root_res not in resolved.parents:
        raise AdapterError(f"{flag_name} {raw_subpath!r} escapes port_root")
    return resolved


def base_arg_parser(description: str) -> argparse.ArgumentParser:
    """Construct standard CLI parser shared across all 5 harness adapters."""
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--repo-root", "--core", dest="repo_root", default=".",
                    help="canonical repository root (default: .)")
    ap.add_argument("--port-root", "--port", dest="port_root", required=True,
                    help="destination port root directory")
    ap.add_argument("--canonical-revision", default=None,
                    help="explicit canonical revision identifier")
    ap.add_argument("--always-on-surface", dest="always_on_surfaces", action="append",
                    default=[], help="additional always-on surface path (repeatable)")
    ap.add_argument("--user-home", default=None,
                    help="isolated user-scope home directory for '~/' surface checks")
    ap.add_argument("--force", action="store_true",
                    help="overwrite pre-existing files that no previous port manifest owns")
    return ap


def run_adapter_cli(compile_fn, argv: list[str] | None = None) -> int:
    """Execute an adapter entrypoint and translate AdapterError to exit status 1."""
    try:
        return compile_fn(sys.argv[1:] if argv is None else argv)
    except AdapterError as exc:
        sys.stderr.write(f"adapter error: {exc}\n")
        return 1
