#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-005, REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-005, REQ-PRD-PPA-006
# @decision DEC-PPA-009: A transforming mapping must conserve more than citations:
#   every substantive canonical body line has to survive in its port units, and a
#   compiled concept card has to carry one list item per discrete side condition
#   (ARCHITECTURE 7.1). Both are literal, deterministic comparisons.
"""Content-conservation checks for transforming mappings and discrete conditions."""
from __future__ import annotations

import collections
import re

import ppa_artifact_rules as rules

LINK_TARGET_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}(?:\s|$)")
TABLE_SEPARATOR_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?$")
CONDITIONS_TITLE = "Preconditions & Side Conditions"
EDGES_TITLE = "Related Edges"


def normalize_line(line: str) -> str:
    """Drop Markdown link targets (keeping labels) and collapse whitespace runs."""
    return " ".join(LINK_TARGET_RE.sub(lambda m: f"[{m.group(1)}]", line).split())


def canonical_body_lines(text: str) -> list[str]:
    """Normalised substantive body lines of a canonical file.

    Skipped as structural: YAML frontmatter, blank lines, HTML comments, Markdown
    headings, code-fence delimiters, and table separator rows. Lines inside a code
    fence are content and are kept.
    """
    lines = rules.split_lines_n2(text)
    start = 0
    if lines and rules.is_fm_delim(lines[0], first=True):
        for idx in range(1, len(lines)):
            if rules.is_fm_delim(lines[idx]):
                start = idx + 1
                break
    out: list[str] = []
    fence: str | None = None
    in_comment = False
    for line in lines[start:]:
        stripped = line.strip()
        if fence is None and in_comment:
            in_comment = "-->" not in stripped
            continue
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = marker if fence is None else (None if fence == marker else fence)
            continue
        if fence is None:
            if stripped.startswith("<!--"):
                in_comment = "-->" not in stripped
                continue
            if not stripped or HEADING_RE.match(line) or TABLE_SEPARATOR_RE.match(stripped):
                continue
        elif not stripped:
            continue
        out.append(normalize_line(line))
    return [ln for ln in out if ln]


def port_text_normalized(texts: list[str]) -> str:
    """Concatenate port units into one whitespace-normalised search text."""
    parts: list[str] = []
    for text in texts:
        parts.extend(normalize_line(ln) for ln in rules.split_lines_n2(text))
    return " ".join(p for p in parts if p)


def containment_errors(canonical_rel: str, canonical_text: str, port_texts: list[str]) -> list[str]:
    """Return one finding per canonical body line missing from the mapped port units."""
    haystack = port_text_normalized(port_texts)
    wanted = collections.Counter(canonical_body_lines(canonical_text))
    errs: list[str] = []
    for line, count in wanted.items():
        if haystack.count(line) < count:
            errs.append(f"{canonical_rel}:0 (body line lost in port: {line[:80]!r})")
    return errs


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
