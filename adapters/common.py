#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Shared stdlib-only compilation primitives enforcing LF
#   normalisation (N4-N6), sorted file walks and JSON keys (N7, C5.7), symbolic
#   always-on surface snapshots (C2.1-C2.2, C5.3), and symlink-free output.
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


def copy_lossless(src: Path, dest: Path) -> None:
    """Copy a canonical UTF-8 file with LF line endings and zero symlinks."""
    if src.is_symlink():
        raise AdapterError(f"canonical source must not be a symlink: {src}")
    write_utf8_lf(dest, read_utf8_strict(src))


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


def compute_surface_sha256(port_root: Path, surface: str, user_home: Path) -> str | None:
    """Compute raw-byte SHA-256 (or deterministic multi-file glob digest) for a surface."""
    if surface.startswith("~/"):
        rel_pattern = surface[2:]
        anchor = user_home
    else:
        rel_pattern = surface.lstrip("/")
        anchor = port_root
    if any(ch in rel_pattern for ch in ("*", "?", "[")):
        matches = sorted(p for p in anchor.glob(rel_pattern) if p.is_file())
        if not matches:
            return None
        h = hashlib.sha256()
        for m in matches:
            rel_m = m.relative_to(anchor).as_posix()
            file_digest = hashlib.sha256(m.read_bytes()).hexdigest()
            h.update(f"{rel_m}:{file_digest}\n".encode("utf-8"))
        return h.hexdigest()
    target_path = anchor / rel_pattern
    if not target_path.is_file():
        return None
    return hashlib.sha256(target_path.read_bytes()).hexdigest()


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
) -> list[dict[str, str | None]]:
    """Snapshot minimum + dynamic + caller-declared always-on surfaces pre-install."""
    ordered: list[str] = list(MINIMUM_ALWAYS_ON_SURFACES.get(target, ()))
    for item in discover_extra_always_on(port_root, target):
        if item not in ordered:
            ordered.append(item)
    for item in extra_surfaces or []:
        clean = item.strip()
        if clean and clean not in ordered:
            ordered.append(clean)
    return [
        {"path": surf, "sha256_before": compute_surface_sha256(port_root, surf, user_home)}
        for surf in ordered
    ]


def scan_preexisting_discovery(
    port_root: Path, target: str, custom_skills_dir: Path | None = None
) -> list[str]:
    """Collect non-manifest discovery names present in port_root prior to install."""
    if not port_root.is_dir():
        return []
    manifest_path = port_root / "port_manifest.json"
    prior_managed: set[str] = set()
    if manifest_path.is_file():
        try:
            prior = json.loads(read_utf8_strict(manifest_path))
            prior_managed = {
                str(e.get("name", "")) for e in prior.get("discovery_entries", [])
                if isinstance(e, dict)
            }
        except json.JSONDecodeError:
            prior_managed = set()
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
    return sorted(candidates - prior_managed)


def ambient_trigger_description(amb_path: Path) -> str:
    """Synthesize a portable <=1024-char ambient description (zero N8 or lists)."""
    text = read_utf8_strict(amb_path)
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


def copy_corpus_closure(repo_root: Path, corpus_files: list[Path], dest_corpus_dir: Path) -> list[str]:
    """Copy text/JSON corpus files into port core for R3 lookup & C3.11 closure."""
    copied: list[str] = []
    for cpath in corpus_files:
        rel_c = cpath.relative_to(repo_root / "corpus")
        out_path = dest_corpus_dir / rel_c
        copy_lossless(cpath, out_path)
        copied.append(rel_c.as_posix())
    return copied


def ensure_safe_subpath(port_root: Path, raw_subpath: str, flag_name: str) -> Path:
    """Resolve a configurable directory inside port_root, rejecting escapes."""
    cand = Path(raw_subpath)
    resolved = (port_root / cand).resolve() if not cand.is_absolute() else cand.resolve()
    root_res = port_root.resolve()
    if resolved != root_res and root_res not in resolved.parents:
        raise AdapterError(f"{flag_name} {raw_subpath!r} escapes port_root")
    return resolved


def write_port_manifest(port_root: Path, manifest: dict[str, object]) -> Path:
    """Serialize deterministic sorted-key port_manifest.json (CONFORMANCE_SPEC N7)."""
    out = port_root / "port_manifest.json"
    write_utf8_lf(out, json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return out


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
    return ap


def run_adapter_cli(compile_fn, argv: list[str] | None = None) -> int:
    """Execute an adapter entrypoint and translate AdapterError to exit status 1."""
    try:
        return compile_fn(sys.argv[1:] if argv is None else argv)
    except AdapterError as exc:
        sys.stderr.write(f"adapter error: {exc}\n")
        return 1
