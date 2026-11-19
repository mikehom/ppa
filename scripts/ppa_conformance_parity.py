#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-005, REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-005, REQ-PRD-PPA-006
# @decision DEC-PPA-009: A transforming mapping must conserve more than citations:
#   every substantive canonical body line has to survive in its port units, and a
#   compiled concept card has to carry one list item per discrete side condition
#   (ARCHITECTURE 7.1). Both are literal, deterministic comparisons.
# @decision DEC-PPA-011: Conservation is exact in both directions. The port's
#   normalised body lines and heading texts must equal the canonical multisets
#   up to a closed scaffolding allowlist, so an appended clause, a rewritten
#   heading, or an injected line fails C1.8 without a reference rebuild; a
#   bounded block merged into an operator file must match its recorded digest.
"""Content-conservation checks for transforming mappings and discrete conditions."""
from __future__ import annotations

import collections
import re
from collections.abc import Callable
from pathlib import Path

import ppa_artifact_rules as rules

LINK_TARGET_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}(?:\s|$)")
TABLE_SEPARATOR_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?$")
CONDITIONS_TITLE = "Preconditions & Side Conditions"
EDGES_TITLE = "Related Edges"
FALLBACK_HEADING_TEXT = "Orientation Guides (R1 Fallback)"
ROUTER_CANONICAL = f"knowledge/skills/{rules.ROUTER_SKILL}/SKILL.md"
FRONTMATTER_KEY_RE = re.compile(r"^(name|description|globs|alwaysApply):(?:\s.*)?$")
BLOCK_MARKERS = ("<!-- PPA_KNOWLEDGE_START -->", "<!-- PPA_KNOWLEDGE_END -->")
LINE_KINDS = ("frontmatter", "comment", "heading", "body")


def normalize_line(line: str) -> str:
    """Drop Markdown link targets (keeping labels) and collapse whitespace runs."""
    return " ".join(LINK_TARGET_RE.sub(lambda m: f"[{m.group(1)}]", line).split())


def classify_lines(text: str) -> dict[str, list[str]]:
    """Split a Markdown unit into frontmatter, comment, heading, and body lines.

    Frontmatter lines are raw; the others are normalised (a heading without its
    ``#`` prefix). Blank lines, code-fence delimiters, and table separator rows
    are structural and dropped; lines inside a code fence are body content.
    """
    lines = rules.split_lines_n2(text)
    out: dict[str, list[str]] = {kind: [] for kind in LINE_KINDS}
    start = 0
    if lines and rules.is_fm_delim(lines[0], first=True):
        for idx in range(1, len(lines)):
            if rules.is_fm_delim(lines[idx]):
                out["frontmatter"] = lines[1:idx]
                start = idx + 1
                break
    fence: str | None = None
    in_comment = False
    for line in lines[start:]:
        stripped = line.strip()
        kind = "body"
        if fence is None and in_comment:
            in_comment = "-->" not in stripped
            kind = "comment"
        elif stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = marker if fence is None else (None if fence == marker else fence)
            continue
        elif fence is None and stripped.startswith("<!--"):
            in_comment = "-->" not in stripped
            kind = "comment"
        elif fence is None and TABLE_SEPARATOR_RE.match(stripped):
            continue
        elif fence is None and HEADING_RE.match(line):
            kind, line = "heading", stripped.lstrip("#")
        norm = normalize_line(line)
        if norm:
            out[kind].append(norm)
    return out


def canonical_body_lines(text: str) -> list[str]:
    """Normalised substantive body lines of a canonical file (see classify_lines)."""
    return classify_lines(text)["body"]


def port_text_normalized(texts: list[str]) -> str:
    """Concatenate port units into one whitespace-normalised search text."""
    parts: list[str] = []
    for text in texts:
        parts.extend(normalize_line(ln) for ln in rules.split_lines_n2(text))
    return " ".join(p for p in parts if p)


def scaffold_allowlist(core_root: Path, canonical_rel: str, canonical_text: str) -> dict[str, set[str]]:
    """Closed set of lines a transforming unit may add to its canonical file.

    Comments: the bounded-block markers and the ``skill`` / ``summary`` header that
    repeats the canonical frontmatter. Router only: the orientation fallback heading
    and one link item per canonical ambient file. Port frontmatter is checked by key.
    """
    allowed: dict[str, set[str]] = {"comment": set(BLOCK_MARKERS), "heading": set(), "body": set()}
    meta = rules.parse_frontmatter(rules.split_lines_n2(canonical_text)) or {}
    for key, label in (("name", "skill"), ("description", "summary")):
        if meta.get(key):
            allowed["comment"].add(normalize_line(f"<!-- {label}: {meta[key]} -->"))
    if canonical_rel == ROUTER_CANONICAL:
        allowed["heading"].add(FALLBACK_HEADING_TEXT)
        ambient = core_root / "knowledge" / "ambient-context"
        allowed["body"].update(f"- [{path.name}]" for path in sorted(ambient.glob("ppa-*.md")))
    return allowed


def _frontmatter_injections(fm_lines: list[str]) -> list[str]:
    """Port frontmatter lines outside the discovery keys and their folded description."""
    bad: list[str] = []
    key: str | None = None
    for line in fm_lines:
        match = FRONTMATTER_KEY_RE.match(line)
        if match:
            key = match.group(1)
        elif line.strip() and not (line.startswith((" ", "\t")) and key == "description"):
            bad.append(line.strip())
            key = None
    return bad


def transforming_errors(
    canonical_rel: str, canonical_text: str, port_texts: list[str], allowed: dict[str, set[str]]
) -> tuple[list[str], list[str]]:
    """Exact conservation of one transforming mapping: (lost findings, injected findings).

    The normalised body-line and heading-text multisets of the port units must equal
    the canonical ones; a surplus line passes only when it is in ``allowed`` and
    occurs once. Port comment lines must be canonical comment lines or allowed ones.
    """
    canon = classify_lines(canonical_text)
    port: dict[str, list[str]] = {kind: [] for kind in LINE_KINDS}
    for text in port_texts:
        for kind, lines in classify_lines(text).items():
            port[kind].extend(lines)
    lost: list[str] = []
    injected: list[str] = []
    for kind, label in (("heading", "heading"), ("body", "body line")):
        want, have = collections.Counter(canon[kind]), collections.Counter(port[kind])
        lost.extend(f"{canonical_rel}:0 ({label} lost in port: {line[:80]!r})" for line in want - have)
        injected.extend(
            f"{canonical_rel}:0 (unapproved {label} in port: {line[:80]!r})"
            for line, count in (have - want).items() if not (line in allowed[kind] and count == 1))
    known_comments = set(canon["comment"]) | allowed["comment"]
    injected.extend(f"{canonical_rel}:0 (unapproved comment line in port: {line[:80]!r})"
                    for line in port["comment"] if line not in known_comments)
    injected.extend(f"{canonical_rel}:0 (unapproved frontmatter line in port: {line[:80]!r})"
                    for line in _frontmatter_injections(port["frontmatter"]))
    return lost, injected


def bounded_block_errors(
    port_root: Path, manifest: dict, record_of: Callable[[str], dict | None]
) -> tuple[list[str], int]:
    """Integrity of the bounded blocks a port merged into operator files: (findings, blocks declared).

    Each ``bounded_blocks`` entry must equal the record of the block now on disk, and
    a merged file that carries a block marker must be declared. Text outside the
    block is the operator's and is never compared.
    """
    declared = manifest.get("bounded_blocks")
    declared = declared if isinstance(declared, dict) else {}
    merged = manifest.get("merged_files")
    errs: list[str] = []
    for rel in sorted({str(k) for k in declared} | {str(m) for m in (merged if isinstance(merged, list) else [])}):
        path = port_root / rel
        if rel.startswith("/") or ".." in rel.split("/") or path.is_symlink() or not path.is_file():
            if rel in declared:
                errs.append(f"{rel}:0 (declared bounded block: file missing, linked, or outside the port)")
            continue
        text, err = rules.read_text_strict(path)
        if err or text is None:
            errs.append(f"{rel}:0 (unreadable: {err})")
        elif rel not in declared:
            if "PPA_KNOWLEDGE_" in text:
                errs.append(f"{rel}:0 (bounded block present but not declared in bounded_blocks)")
        elif record_of(text) != declared[rel]:
            errs.append(f"{rel}:0 (bounded block differs from the block the port recorded)")
    return errs, len(declared)


def _section_lines(text: str, title: str) -> list[str]:
    """Lines of the first level-2 section whose heading contains title."""
    out: list[str] = []
    inside = False
    for _, line in rules.strip_fences_and_frontmatter(text):
        if line.startswith("## "):
            if inside:
                break
            inside = title in line
            continue
        if inside:
            out.append(line)
    return out


def card_parity_errors(node: dict, card_text: str, where: str) -> list[str]:
    """ARCHITECTURE 7.1 parity of one compiled concept card against its graph node."""
    errs: list[str] = []
    wanted = collections.Counter(
        normalize_line(str(c)) for c in node.get("conditions", []) if str(c).strip())
    bullets = collections.Counter(
        normalize_line(ln[2:]) for ln in _section_lines(card_text, CONDITIONS_TITLE) if ln.startswith("- "))
    if wanted != bullets:
        errs.append(
            f"{where}:0 (conditions: node has {sum(wanted.values())}, card lists "
            f"{sum(bullets.values())}, {sum((wanted - bullets).values())} missing)")
    edge_text = port_text_normalized(["\n".join(_section_lines(card_text, EDGES_TITLE))])
    for edge in node.get("related_edges", []):
        if not isinstance(edge, dict) or edge.get("relation") != "corresponds_to":
            continue
        basis = edge.get("basis") if isinstance(edge.get("basis"), dict) else {}
        for key in ("conditions", "differs"):
            for item in basis.get(key, []) if isinstance(basis.get(key), list) else []:
                if normalize_line(str(item)) not in edge_text:
                    errs.append(f"{where}:0 (corresponds_to {edge.get('target_id')} basis.{key} missing)")
    return errs


def graph_conditions_errors(nodes: list) -> tuple[list[str], int]:
    """Discrete-conditions structure of the graph (ARCHITECTURE 6.3, 7.1 Tier A).

    Every ``conditions`` entry is a non-empty single-line string, unique within its
    node; every corresponds_to edge carries a basis with a unification id and
    non-empty citations, conditions, and differs. Returns (findings, items examined).
    """
    errs: list[str] = []
    examined = 0
    for node in nodes:
        if not isinstance(node, dict):
            continue
        cid = str(node.get("id", "?"))
        examined += 1
        conds = node.get("conditions", [])
        if not isinstance(conds, list):
            errs.append(f"{cid}.conditions:0 (not a list)")
            conds = []
        seen: set[str] = set()
        for idx, cond in enumerate(conds):
            norm = normalize_line(cond) if isinstance(cond, str) else ""
            if not norm or "\n" in str(cond):
                errs.append(f"{cid}.conditions[{idx}]:0 (empty or multi-line entry)")
            elif norm in seen:
                errs.append(f"{cid}.conditions[{idx}]:0 (duplicate entry)")
            seen.add(norm)
        for eidx, edge in enumerate(node.get("related_edges", [])):
            if not isinstance(edge, dict) or edge.get("relation") != "corresponds_to":
                continue
            examined += 1
            basis = edge.get("basis") if isinstance(edge.get("basis"), dict) else {}
            if not basis.get("unification_id"):
                errs.append(f"{cid}.related_edges[{eidx}].basis:0 (missing unification_id)")
            for key in ("citations", "conditions", "differs"):
                items = basis.get(key)
                if not isinstance(items, list) or not items or any(
                        not item or (isinstance(item, str) and not item.strip()) for item in items):
                    errs.append(f"{cid}.related_edges[{eidx}].basis.{key}:0 (missing or empty)")
    return errs, examined


def conditions_home_errors(nodes: list) -> list[str]:
    """Every node that lists conditions is anchored in an L1 reference or L2 skill artifact."""
    errs: list[str] = []
    for node in nodes:
        if not isinstance(node, dict) or not node.get("conditions"):
            continue
        refs = [str(r) for r in node.get("artifact_refs", [])]
        if not any(r.startswith("knowledge/skills/") for r in refs):
            errs.append(f"{node.get('id', '?')}: conditions listed but no knowledge/skills artifact_refs anchor")
    return errs
