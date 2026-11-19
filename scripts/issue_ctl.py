#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001
# @decision DEC-PPA-002: Per-file Markdown issue tracker guarded by fcntl.flock;
#   strict frontmatter subset parsed with stdlib only; deterministic topological
#   GitHub export manifest (parents/prerequisites before dependents).
"""Issue controller for the repository-local `issues/` tracker.

Usage:
    python3 -B scripts/issue_ctl.py [--root DIR] validate
    python3 -B scripts/issue_ctl.py [--root DIR] set-status ID STATUS [--receipt TEXT]
    python3 -B scripts/issue_ctl.py [--root DIR] export-github --dry-run

See issues/SCHEMA.md for the file format. Exit codes: 0 ok, 1 validation
failure, 2 usage error.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import heapq
import json
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

LOG = logging.getLogger("issue_ctl")

DIR_RULES = {
    "epics": (re.compile(r"^EPIC-\d{3}$"), {"epic"}),
    "shards": (re.compile(r"^ISS-W\d-\d{2}$"), {"shard"}),
    "refactors": (re.compile(r"^REF-\d{3}$"), {"refactor"}),
    "backlog": (re.compile(r"^BKL-\d{3}$"), {"contradiction", "edge_case"}),
}
ISSUE_TYPES = {"epic", "shard", "refactor", "contradiction", "edge_case"}
STATUSES = {"open", "in_progress", "aligned", "closed", "parked"}
PRIORITIES = {"P0", "P1", "P2"}
ALTITUDES = {"L0", "L1", "L2", "L3"}
TRANSITIONS = {
    "open": {"in_progress", "parked"},
    "in_progress": {"aligned", "parked", "open"},
    "aligned": {"closed", "in_progress"},
    "closed": {"in_progress"},
    "parked": {"open", "in_progress"},
}
REQUIRED_KEYS = [
    "id", "title", "issue_type", "status", "priority", "labels", "milestone",
    "parent_issue", "depends_on", "blocks", "ppa_scope", "altitudes",
    "aligned_models", "created_at", "updated_at", "github_issue_number",
]
LIST_KEYS = {"labels", "depends_on", "blocks", "ppa_scope", "altitudes", "aligned_models"}
SECTIONS = [
    "Summary",
    "Source Citations & Grounding",
    "Technical Analysis / Mechanism",
    "Acceptance Gates",
    "3-Model Adversarial Alignment & Rebuttal Log",
    "Cross-Referenced Concepts & Artifacts",
    "Verification Receipts",
]
PLACEHOLDER = "_Pending._"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class IssueError(ValueError):
    """Raised for malformed issue files."""


@dataclass
class Issue:
    path: Path
    meta: dict
    sections: dict[str, str]
    errors: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return str(self.meta.get("id", self.path.stem))


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------

def parse_scalar(raw: str) -> object:
    raw = raw.strip()
    if raw == "null":
        return None
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        return raw[1:-1].replace('\\"', '"')
    return raw


def split_flow_list(body: str) -> list[str]:
    """Split the inside of `[...]` on commas that are outside double quotes."""
    items, buf, quoted = [], [], False
    for ch in body:
        if ch == '"':
            quoted = not quoted
        if ch == "," and not quoted:
            items.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if quoted:
        raise IssueError("unterminated quote in list")
    tail = "".join(buf)
    if tail.strip() or items:
        items.append(tail)
    return [i for i in items if i.strip()]


def parse_value(raw: str) -> object:
    raw = raw.strip()
    if raw.startswith("["):
        if not raw.endswith("]"):
            raise IssueError(f"unterminated list: {raw!r}")
        return [parse_scalar(i) for i in split_flow_list(raw[1:-1])]
    return parse_scalar(raw)


def split_document(text: str) -> tuple[list[str], str]:
    norm = text.replace("\r\n", "\n")
    lines = norm.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if not lines or lines[0].lstrip("\ufeff").rstrip(" \t\r") != "---":
        raise IssueError("file must start with '---' frontmatter delimiter")
    for idx in range(1, len(lines)):
        if lines[idx].rstrip(" \t\r") == "---":
            return lines[1:idx], "\n".join(lines[idx + 1:])
    raise IssueError("frontmatter closing '---' not found")


def parse_frontmatter(lines: list[str]) -> dict:
    meta: dict = {}
    for lineno, line in enumerate(lines, start=2):
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            raise IssueError(f"line {lineno}: comments are not permitted in frontmatter")
        m = re.match(r"^([a-z_]+):(?:\s(.*))?$", line)
        if not m:
            raise IssueError(f"line {lineno}: not a 'key: value' line: {line!r}")
        key = m.group(1)
        if key in meta:
            raise IssueError(f"line {lineno}: duplicate key {key!r}")
        meta[key] = parse_value(m.group(2) or "")
    return meta


def parse_sections(body: str) -> tuple[dict[str, str], list[str], list[str]]:
    """Return section -> content, ordered level-2 headings, and any preamble lines."""
    sections: dict[str, str] = {}
    order: list[str] = []
    preamble: list[str] = []
    current: str | None = None
    buf: list[str] = []
    fence: str | None = None
    for line in body.replace("\r\n", "\n").split("\n"):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
        m = None if fence else re.match(r"^## (?!#)(.+?)\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1)
            order.append(current)
            buf = []
        elif current is not None:
            buf.append(line)
        elif line.strip():
            preamble.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections, order, preamble


def load_issue(path: Path) -> Issue:
    try:
        text = path.read_bytes().decode("utf-8", errors="strict")
        fm_lines, body = split_document(text)
        meta = parse_frontmatter(fm_lines)
    except (IssueError, UnicodeDecodeError) as exc:
        return Issue(path, {}, {}, [str(exc)])
    sections, order, preamble = parse_sections(body)
    issue = Issue(path, meta, sections)
    if preamble:
        issue.errors.append("unexpected preamble text before '## Summary'")
    if order != SECTIONS:
        issue.errors.append(f"sections must be exactly {SECTIONS} in order; got {order}")
    return issue


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def is_empty(content: str | None) -> bool:
    return content is None or not content.strip() or content.strip() == PLACEHOLDER


def check_fields(issue: Issue, dirname: str) -> None:
    meta, errs = issue.meta, issue.errors
    missing = [k for k in REQUIRED_KEYS if k not in meta]
    unknown = sorted(set(meta) - set(REQUIRED_KEYS))
    if missing:
        errs.append(f"missing keys: {missing}")
    if unknown:
        errs.append(f"unknown keys: {unknown}")
    if missing:
        return
    id_re, types = DIR_RULES[dirname]
    if not isinstance(meta["id"], str) or not id_re.match(meta["id"]):
        errs.append(f"id {meta['id']!r} does not match {id_re.pattern} for {dirname}/")
    if meta["id"] != issue.path.stem:
        errs.append(f"id {meta['id']!r} != file stem {issue.path.stem!r}")
    if meta["issue_type"] not in types:
        errs.append(f"issue_type {meta['issue_type']!r} not allowed in {dirname}/ {sorted(types)}")
    for key, allowed in (("issue_type", ISSUE_TYPES), ("status", STATUSES),
                         ("priority", PRIORITIES)):
        if meta[key] not in allowed:
            errs.append(f"{key} {meta[key]!r} not in {sorted(allowed)}")
    for key in LIST_KEYS:
        if not isinstance(meta[key], list) or not all(isinstance(x, str) for x in meta[key]):
            errs.append(f"{key} must be a list of strings")
    if isinstance(meta["altitudes"], list) and not set(meta["altitudes"]) <= ALTITUDES:
        errs.append(f"altitudes must be a subset of {sorted(ALTITUDES)}")
    title = meta["title"]
    if not isinstance(title, str) or not title.strip() or len(title) > 120:
        errs.append("title must be a non-empty string <= 120 chars")
    if not isinstance(meta["milestone"], str) or not meta["milestone"].strip():
        errs.append("milestone must be a non-empty string")
    gh = meta["github_issue_number"]
    if gh is not None and (not isinstance(gh, int) or gh <= 0):
        errs.append("github_issue_number must be null or a positive integer")
    check_dates(issue)
    check_semantics(issue)


def check_dates(issue: Issue) -> None:
    parsed = {}
    for key in ("created_at", "updated_at"):
        val = issue.meta[key]
        try:
            if not isinstance(val, str) or not DATE_RE.match(val):
                raise ValueError(val)
            parsed[key] = dt.date.fromisoformat(val)
        except ValueError:
            issue.errors.append(f"{key} {val!r} is not a YYYY-MM-DD date")
    if len(parsed) == 2 and parsed["updated_at"] < parsed["created_at"]:
        issue.errors.append("updated_at is earlier than created_at")


def check_semantics(issue: Issue) -> None:
    meta, sec, errs = issue.meta, issue.sections, issue.errors
    if meta["status"] == "closed":
        if is_empty(sec.get("Verification Receipts")):
            errs.append("status 'closed' requires non-empty Verification Receipts")
        if "- [ ] " in (sec.get("Acceptance Gates") or ""):
            errs.append("status 'closed' requires all Acceptance Gates checked")
    if meta["status"] == "aligned":
        models = meta.get("aligned_models") or []
        if len(set(models)) < 3 or len(models) != len(set(models)):
            errs.append("status 'aligned' requires >= 3 distinct aligned_models (no duplicates)")
        if is_empty(sec.get("3-Model Adversarial Alignment & Rebuttal Log")):
            errs.append("status 'aligned' requires non-empty Alignment & Rebuttal Log")
    for name in ("Summary", "Acceptance Gates"):
        if name in sec and is_empty(sec[name]):
            errs.append(f"section {name!r} must not be empty")
    if meta["issue_type"] != "epic" and meta["parent_issue"] is None:
        errs.append("non-epic issues require a parent_issue")


def check_graph(issues: dict[str, Issue]) -> list[str]:
    """Reference existence, depends_on/blocks symmetry, acyclicity, gh uniqueness."""
    errs: list[str] = []
    for iid, issue in sorted(issues.items()):
        meta = issue.meta
        refs = list(meta.get("depends_on") or []) + list(meta.get("blocks") or [])
        if meta.get("parent_issue"):
            refs.append(meta["parent_issue"])
        for ref in refs:
            if ref == iid:
                errs.append(f"{iid}: self reference")
            elif ref not in issues:
                errs.append(f"{iid}: unknown reference {ref!r}")
        for dep in meta.get("depends_on") or []:
            if dep in issues and iid not in (issues[dep].meta.get("blocks") or []):
                errs.append(f"{iid}: depends_on {dep} but {dep}.blocks lacks {iid}")
            if (meta.get("issue_type") in {"epic", "shard"} and dep in issues
                    and issues[dep].meta.get("issue_type") in {"contradiction", "edge_case"}):
                errs.append(f"{iid}: epic/shard must not depend on backlog item {dep} (C6.8)")
        for blk in meta.get("blocks") or []:
            if blk in issues and iid not in (issues[blk].meta.get("depends_on") or []):
                errs.append(f"{iid}: blocks {blk} but {blk}.depends_on lacks {iid}")
    try:
        topo_order(issues)
    except IssueError as exc:
        errs.append(str(exc))
    seen: dict[int, str] = {}
    for iid, issue in sorted(issues.items()):
        gh = issue.meta.get("github_issue_number")
        if isinstance(gh, int):
            if gh in seen:
                errs.append(f"{iid}: github_issue_number {gh} duplicates {seen[gh]}")
            seen[gh] = iid
    return errs


def topo_order(issues: dict[str, Issue]) -> list[str]:
    """Kahn topological sort over parent/depends_on edges; ties broken by id."""
    preds: dict[str, set[str]] = {iid: set() for iid in issues}
    for iid, issue in issues.items():
        parent = issue.meta.get("parent_issue")
        if parent in issues:
            preds[iid].add(parent)
        preds[iid].update(d for d in issue.meta.get("depends_on") or [] if d in issues)
    succs: dict[str, set[str]] = {iid: set() for iid in issues}
    for iid, ps in preds.items():
        for p in ps:
            succs[p].add(iid)
    indeg = {iid: len(ps) for iid, ps in preds.items()}
    heap = sorted(iid for iid, d in indeg.items() if d == 0)
    heapq.heapify(heap)
    order: list[str] = []
    while heap:
        cur = heapq.heappop(heap)
        order.append(cur)
        for nxt in succs[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if len(order) != len(issues):
        cyclic = sorted(set(issues) - set(order))
        raise IssueError(f"dependency cycle among: {cyclic}")
    return order


def collect(root: Path) -> tuple[dict[str, Issue], list[str]]:
    """Load and validate every issue file; return issues and all error strings."""
    issues: dict[str, Issue] = {}
    errors: list[str] = []
    base = root / "issues"
    allowed_top = set(DIR_RULES) | {"SCHEMA.md", "export_manifest.json"}
    for entry in sorted(base.iterdir()) if base.is_dir() else []:
        if entry.name.startswith("."):
            continue
        if entry.name not in allowed_top:
            errors.append(f"{entry.relative_to(root).as_posix()}: unexpected entry in issues/")
    for dirname in DIR_RULES:
        dpath = base / dirname
        if not dpath.is_dir():
            continue
        for entry in sorted(dpath.iterdir()):
            if entry.name.startswith("."):
                continue
            if not entry.is_file() or entry.suffix != ".md":
                errors.append(f"{entry.relative_to(root).as_posix()}: expected .md issue file")
                continue
            issue = load_issue(entry)
            if issue.meta:
                check_fields(issue, dirname)
            rel = entry.relative_to(root).as_posix()
            errors.extend(f"{rel}: {e}" for e in issue.errors)
            if issue.id in issues:
                errors.append(f"{rel}: duplicate id {issue.id}")
            issues[issue.id] = issue
    errors.extend(check_graph(issues))
    return issues, errors


# --------------------------------------------------------------------------
# Locking & mutation
# --------------------------------------------------------------------------

@contextlib.contextmanager
def locked(root: Path, exclusive: bool) -> Iterator[None]:
    lock_path = root / "tmp" / "issues.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        try:
            yield
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def find_issue_path(root: Path, iid: str) -> Path:
    for dirname in DIR_RULES:
        path = root / "issues" / dirname / f"{iid}.md"
        if path.is_file():
            return path
    raise IssueError(f"issue {iid!r} not found under issues/")


def rewrite_status(text: str, status: str, date: str, receipt: str | None) -> str:
    """Return text with status/updated_at replaced and an optional receipt appended."""
    fm_lines, _ = split_document(text)
    end = len(fm_lines) + 1
    lines = text.splitlines()
    for idx in range(1, end):
        if lines[idx].startswith("status:"):
            lines[idx] = f"status: {status}"
        elif lines[idx].startswith("updated_at:"):
            lines[idx] = f"updated_at: {date}"
    if receipt:
        head = "## Verification Receipts"
        pos = lines.index(head)
        nxt = next((i for i in range(pos + 1, len(lines)) if lines[i].startswith("## ")),
                   len(lines))
        block = [ln for ln in lines[pos + 1:nxt] if ln.strip() != PLACEHOLDER]
        while block and not block[-1].strip():
            block.pop()
        block.append(f"- {date} [{status}] {receipt}")
        lines = lines[:pos + 1] + block + [""] + lines[nxt:]
    return "\n".join(lines).rstrip("\n") + "\n"


def set_status(root: Path, iid: str, status: str, receipt: str | None,
               date: str | None) -> None:
    if status not in STATUSES:
        raise IssueError(f"unknown status {status!r}; expected {sorted(STATUSES)}")
    date = date or dt.date.today().isoformat()
    with locked(root, exclusive=True):
        path = find_issue_path(root, iid)
        current = load_issue(path)
        if current.errors:
            raise IssueError(f"{iid} is invalid before mutation: {current.errors}")
        old = current.meta["status"]
        if status != old and status not in TRANSITIONS[old]:
            raise IssueError(f"illegal transition {old} -> {status}; allowed: "
                             f"{sorted(TRANSITIONS[old])}")
        new_text = rewrite_status(path.read_text(encoding="utf-8"), status, date, receipt)
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_text(new_text, encoding="utf-8")
        candidate = load_issue(tmp)
        if candidate.meta:
            candidate.path = path
            check_fields(candidate, path.parent.name)
        if candidate.errors:
            tmp.unlink()
            raise IssueError(f"refusing write; result invalid: {candidate.errors}")
        tmp.replace(path)
        LOG.info("%s: %s -> %s", iid, old, status)


# --------------------------------------------------------------------------
# GitHub export
# --------------------------------------------------------------------------

def render_body(issue: Issue) -> str:
    parts = [f"## {name}\n\n{issue.sections.get(name, '').strip() or PLACEHOLDER}"
             for name in SECTIONS]
    meta = {k: issue.meta[k] for k in ("id", "parent_issue", "depends_on", "blocks",
                                       "ppa_scope", "altitudes", "aligned_models",
                                       "created_at", "updated_at")}
    parts.append(f"<!-- ppa-issue-metadata: {json.dumps(meta, sort_keys=True)} -->")
    return "\n\n".join(parts) + "\n"


def normalized_body(text: str) -> str:
    """CONFORMANCE_SPEC N4+N5: body after frontmatter, LF endings, per-line
    trailing whitespace stripped, trailing blank lines removed (no final LF)."""
    _, body = split_document(text.replace("\r\n", "\n").replace("\r", "\n"))
    lines = [ln.rstrip() for ln in body.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def body_sha256(text: str) -> str:
    """CONFORMANCE_SPEC N6 digest of the normalised body."""
    return hashlib.sha256(normalized_body(text).encode("utf-8")).hexdigest()


def export_manifest(root: Path, issues: dict[str, Issue]) -> dict:
    order = topo_order(issues)
    entries = []
    for iid in order:
        issue = issues[iid]
        meta = issue.meta
        source_text = issue.path.read_bytes().decode("utf-8", errors="strict")
        rendered = render_body(issue)
        labels = list(meta["labels"]) + [f"type:{meta['issue_type']}",
                                          f"priority:{meta['priority']}",
                                          f"status:{meta['status']}"]
        labels += [f"altitude:{a}" for a in meta["altitudes"]]
        entries.append({
            "id": iid,
            "source_path": issue.path.relative_to(root).as_posix(),
            "title": meta["title"],
            "body": rendered,
            "labels": sorted(set(labels)),
            "milestone": meta["milestone"],
            "state": "closed" if meta["status"] == "closed" else "open",
            "parent_issue": meta["parent_issue"],
            "depends_on": meta["depends_on"],
            "blocks": meta["blocks"],
            "github_issue_number": meta["github_issue_number"],
            "frontmatter": meta,
            "source_body": normalized_body(source_text),
            "body_sha256": body_sha256(source_text),
            "published_body_sha256": hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
        })
    return {
        "schema_version": 1,
        "dry_run": True,
        "as_of": max(i.meta["updated_at"] for i in issues.values()) if issues else None,
        "count": len(entries),
        "order": order,
        "issues": entries,
    }


def cmd_export(root: Path, dry_run: bool, out_arg: str | None = None) -> int:
    if not dry_run:
        LOG.error("live export is not supported; re-run with --dry-run and feed "
                  "issues/export_manifest.json to an external publisher")
        return 2
    with locked(root, exclusive=True):
        issues, errors = collect(root)
        if errors:
            for err in errors:
                print(f"ERROR {err}")
            print(f"export aborted: {len(errors)} validation error(s)")
            return 1
        manifest = export_manifest(root, issues)
        out = Path(out_arg) if out_arg else root / "issues" / "export_manifest.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False,
                                  sort_keys=True) + "\n", encoding="utf-8")
    print(f"export dry-run OK: {manifest['count']} issue(s) -> {out}")
    return 0


def cmd_validate(root: Path) -> int:
    with locked(root, exclusive=False):
        issues, errors = collect(root)
    for err in errors:
        print(f"ERROR {err}")
    counts: dict[str, int] = {}
    for issue in issues.values():
        key = str(issue.meta.get("issue_type", "unparsed"))
        counts[key] = counts.get(key, 0) + 1
    status = "FAIL" if errors else "PASS"
    print(f"validate {status}: {len(issues)} issue(s) {dict(sorted(counts.items()))}, "
          f"{len(errors)} error(s)")
    return 1 if errors else 0


def main(argv: list[str]) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="issues/ tracker controller")
    ap.add_argument("--root", default=".", help="repository root (default: .)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate", help="validate every issue file")
    sp = sub.add_parser("set-status", help="transition an issue's status")
    sp.add_argument("issue_id")
    sp.add_argument("status")
    sp.add_argument("--receipt", help="append a line to Verification Receipts")
    sp.add_argument("--date", help="override updated_at (YYYY-MM-DD)")
    ep = sub.add_parser("export-github", help="write issues/export_manifest.json")
    ep.add_argument("--dry-run", action="store_true")
    ep.add_argument("--out", help="override manifest output path")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if not (root / "issues").is_dir():
        LOG.error("no issues/ directory under %s", root)
        return 2
    if args.cmd == "validate":
        return cmd_validate(root)
    if args.cmd == "export-github":
        return cmd_export(root, args.dry_run, args.out)
    try:
        set_status(root, args.issue_id, args.status, args.receipt, args.date)
    except IssueError as exc:
        LOG.error("%s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
