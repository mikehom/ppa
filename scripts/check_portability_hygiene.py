#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001
# @decision DEC-PPA-003: Fail-closed portability gate. Tracked code holds only
#   organisation-agnostic structural rules; operator-specific tokens (people,
#   hosts, private tools, private short-link shapes) are loaded at run time from
#   an untracked denylist file. Anything that cannot be scanned is a finding.
"""Fail-closed portability hygiene scanner.

Usage:
    python3 -B scripts/check_portability_hygiene.py [ROOT] [--json]
        [--denylist FILE] [--no-local-denylist]

File set: when ROOT is the top level of a git work tree, every tracked file plus
every untracked, non-ignored file (`git ls-files --cached --others
--exclude-standard`), so tracked-but-ignored files are still scanned. Otherwise
a directory walk that skips `.git/`, `__pycache__/` and a root-level `tmp/`.

Structural rules (all files): workstation-absolute paths, e-mail addresses,
URLs outside the allowlist. Core rules (knowledge/, ontology/, corpus/,
issues/): model, agent or vendor names and `tmp/` references (conformance check
C5.2); harness product/config names (knowledge/, ontology/, corpus/ only).
Operator rules: tokens and regexes from the denylist file (default
`tmp/local_hygiene_denylist.json` under ROOT, or $PPA_HYGIENE_DENYLIST).

Fail-closed: files that are not valid UTF-8, contain NUL bytes, or exceed 8 MiB
are findings unless their suffix is on the binary allowlist (whose paths are
still scanned). Path strings and symlink targets are scanned; symlinks that
resolve outside ROOT are findings. Exit codes: 0 clean, 1 findings, 2 usage/IO
error.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import logging
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

LOG = logging.getLogger("check_portability_hygiene")

MAX_BYTES = 8 * 1024 * 1024
BINARY_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".gif"}
WALK_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}
CORE_DIRS = {"knowledge", "ontology", "corpus", "issues"}
HARNESS_DIRS = {"knowledge", "ontology", "corpus"}
URL_ALLOWLIST = {"json-schema.org", "example.com", "example.org"}
EMAIL_ALLOWLIST = {"example.com", "example.org"}
DEFAULT_DENYLIST = Path("tmp") / "local_hygiene_denylist.json"
END = r"(?![A-Za-z0-9])"

STRUCTURAL: list[tuple[str, re.Pattern[str]]] = [
    ("absolute_path", re.compile(
        r"(?<![\w.~])/(?:Users|home|usr/local|var/folders|private/var|opt/homebrew|root)/"
        r"[^\s'\"`)\]]*")),
    ("absolute_path", re.compile(r"(?<![\w])[A-Za-z]:\\[^\s'\"`]+")),
    ("absolute_path", re.compile("file:" + r"///[^\s'\"`)]+")),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)")),
    ("url", re.compile(r"[a-z][a-z0-9+.-]*://([^/\s'\"`)\]>]+)", re.I)),
]
CORE: list[tuple[str, re.Pattern[str]]] = [
    ("model_or_agent_name", re.compile(
        r"(?<![A-Za-z0-9])(?:opus|fable|carbon|gemini|claude|chatgpt|gpt-?\d\w*|llama|mistral"
        r"|anthropic|openai|deepmind)" + END, re.I)),
    ("tmp_reference", re.compile(r"(?<![\w./-])tmp/")),
]
HARNESS: list[tuple[str, re.Pattern[str]]] = [
    ("harness_name", re.compile(
        r"(?<![A-Za-z0-9])(?:claude code|gemini cli|codex|cursor rules|agents\.md|\.cursor"
        r"|\.claude|\.gemini|copilot)" + END, re.I)),
]


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    column: int
    category: str
    token: str


def load_denylist(path: Path | None) -> list[tuple[str, re.Pattern[str]]]:
    """Operator rules from an untracked JSON file: {"tokens": [...], "regexes": [...]}."""
    if path is None or not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    rules = [("operator_token",
              re.compile(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z])", re.I))
             for t in data.get("tokens", []) if t]
    rules += [("operator_pattern", re.compile(rx)) for rx in data.get("regexes", []) if rx]
    return rules


def git_file_set(root: Path) -> list[str] | None:
    """Tracked + untracked non-ignored files when root is a git top level."""
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=False)
        if top.returncode != 0 or Path(top.stdout.strip()).resolve() != root.resolve():
            return None
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached",
                              "--others", "--exclude-standard"],
                             capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        LOG.info("git file listing unavailable: %s", exc)
        return None
    return sorted({p for p in out.stdout.decode("utf-8", "surrogateescape").split("\0") if p})


def gitignore_patterns(root: Path) -> list[str]:
    gi = root / ".gitignore"
    if not gi.is_file():
        return []
    return [ln.strip().rstrip("/") for ln in gi.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.strip().startswith(("#", "!"))]


def walk_file_set(root: Path) -> list[str]:
    """Fallback enumeration (non-git roots, e.g. test fixtures)."""
    pats = gitignore_patterns(root)
    out: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        rel_dir = Path(dirpath).relative_to(root)
        keep = []
        for d in dirnames:
            rel = (rel_dir / d).as_posix()
            if d in WALK_SKIP_DIRS or (rel_dir == Path(".") and d == "tmp"):
                continue
            if any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(d, p) for p in pats):
                continue
            keep.append(d)
        dirnames[:] = keep
        for f in filenames:
            rel = (rel_dir / f).as_posix()
            if not any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(f, p) for p in pats):
                out.append(rel)
    return sorted(out)


def rules_for(rel: str, operator: list) -> list[tuple[str, re.Pattern[str]]]:
    top = rel.split("/", 1)[0]
    rules = STRUCTURAL + operator
    if top in CORE_DIRS:
        rules = rules + CORE
    if top in HARNESS_DIRS:
        rules = rules + HARNESS
    return rules


def scan_text(text: str, rel: str, rules: list[tuple[str, re.Pattern[str]]]) -> list[Finding]:
    findings: list[Finding] = []
    for lineno, line in enumerate(text.split("\n"), start=1):
        for category, rx in rules:
            for m in rx.finditer(line):
                host = (m.group(1) if m.groups() else "") or ""
                allow = URL_ALLOWLIST if category == "url" else EMAIL_ALLOWLIST
                if category in {"url", "email"} and host.lower().split(":")[0] in allow:
                    continue
                findings.append(Finding(rel, lineno, m.start() + 1, category, m.group(0)))
    return findings


def scan_file(root: Path, rel: str, operator: list) -> tuple[list[Finding], bool]:
    """Scan one file's path, link target and content. Returns (findings, content_scanned)."""
    rules = rules_for(rel, operator)
    findings = [Finding(rel, 0, f.column, "path_" + f.category, f.token)
                for f in scan_text(rel, rel, rules)]
    path = root / rel
    if path.is_symlink():
        target = os.readlink(path)
        findings += [Finding(rel, 0, f.column, "symlink_" + f.category, f.token)
                     for f in scan_text(target, rel, STRUCTURAL + operator)]
        resolved = path.resolve()
        if root.resolve() not in resolved.parents and resolved != root.resolve():
            findings.append(Finding(rel, 0, 1, "symlink_escape", target))
        return findings, False
    if not path.is_file():
        return findings, False
    if path.suffix.lower() in BINARY_SUFFIXES:
        return findings, False
    size = path.stat().st_size
    if size > MAX_BYTES:
        return findings + [Finding(rel, 0, 1, "unscannable_oversized", f"{size} bytes")], False
    data = path.read_bytes()
    if b"\x00" in data:
        return findings + [Finding(rel, 0, 1, "unscannable_binary", "NUL byte")], False
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return findings + [Finding(rel, 0, 1, "unscannable_encoding", str(exc)[:60])], False
    return findings + scan_text(text, rel, rules), True


def scan_root(root: Path, operator: list) -> tuple[list[Finding], int, int]:
    files = git_file_set(root)
    files = walk_file_set(root) if files is None else files
    findings: list[Finding] = []
    scanned = 0
    for rel in files:
        found, content = scan_file(root, rel, operator)
        findings.extend(found)
        scanned += int(content)
    return findings, scanned, len(files)


def resolve_denylist(root: Path, arg: str | None, disabled: bool) -> Path | None:
    if disabled:
        return None
    if arg:
        return Path(arg)
    env = os.environ.get("PPA_HYGIENE_DENYLIST")
    if env:
        return Path(env)
    cand = root / DEFAULT_DENYLIST
    if cand.is_file():
        return cand
    return Path(__file__).resolve().parent.parent / DEFAULT_DENYLIST


def main(argv: list[str]) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="Fail-closed portability hygiene scanner")
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    ap.add_argument("--denylist", help="operator denylist JSON (untracked)")
    ap.add_argument("--no-local-denylist", action="store_true",
                    help="ignore the default untracked operator denylist")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        LOG.error("root is not a directory: %s", root)
        return 2
    try:
        operator = load_denylist(resolve_denylist(root, args.denylist, args.no_local_denylist))
        findings, scanned, listed = scan_root(root, operator)
    except (OSError, ValueError, re.error) as exc:
        LOG.error("scan failed: %s", exc)
        return 2
    if args.json:
        print(json.dumps({"listed_files": listed, "scanned_files": scanned,
                          "operator_rules": len(operator),
                          "findings": [asdict(f) for f in findings]}, indent=1))
    else:
        for f in findings:
            print(f"{f.path}:{f.line}:{f.column}: [{f.category}] {f.token}")
        status = "FAIL" if findings else "PASS"
        print(f"hygiene {status}: {len(findings)} finding(s) in {scanned} scanned file(s) "
              f"({listed} listed, {len(operator)} operator rule(s))")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
