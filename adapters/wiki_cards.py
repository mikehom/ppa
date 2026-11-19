#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: A compiled concept card reproduces every discrete side
#   condition of its node and, under each corresponds_to edge, the conditions,
#   differences, and citations of the edge basis, so a unification edge is never
#   shown as an unconditional equivalence (ARCHITECTURE 6.3, 7.1).
"""Render concept-graph nodes as Knowledge Wiki concept cards."""
from __future__ import annotations

import re

from adapters import common

CONDITIONS_HEADING = "## Preconditions & Side Conditions"
EDGES_HEADING = "## Related Edges"
CARD_MAX_LINES = 250


def format_concept_cite(cite: dict) -> str:
    """Format one graph citation object as an N8 token with its page companion."""
    ch = str(cite.get("chapter_or_app", ""))
    roman = cite.get("book_page_roman")
    book = cite.get("book_page")
    pdf = cite.get("pdf_page")
    sec = cite.get("section")
    tf = cite.get("table_or_fig")
    if roman and ch in {"Preface", "Contents", "List of Tables", "List of Figures"}:
        return f"[PPA {ch}, p. {roman}] (book p. {roman}; PDF p. {pdf})"
    if tf:
        return f"[PPA {tf}, p. {book}] (book p. {book}; PDF p. {pdf})"
    if sec and re.match(r"^[1-6ABC]\.\d", str(sec)):
        return f"[PPA §{sec}, p. {book}] (book p. {book}; PDF p. {pdf})"
    if sec in {"Concluding Remarks", "Mini Projects", "Exercises"}:
        kind = f"Chapter {ch}" if ch.isdigit() else f"Appendix {ch}"
        return f"[PPA {kind} {sec}, p. {book}] (book p. {book}; PDF p. {pdf})"
    if ch == "Notation":
        return f"[PPA Index of Notation, p. {book}] (book p. {book}; PDF p. {pdf})"
    if ch == "Index":
        return f"[PPA Index, p. {book}] (book p. {book}; PDF p. {pdf})"
    if ch == "Bibliography":
        loc = f"Bibliography {sec}" if (isinstance(sec, str) and sec.startswith("[")) else "Bibliography"
        return f"[PPA {loc}, p. {book}] (book p. {book}; PDF p. {pdf})"
    kind = f"Chapter {ch}" if ch.isdigit() else f"Appendix {ch}"
    return f"[PPA {kind}, p. {book}] (book p. {book}; PDF p. {pdf})"


def _strings(values: object) -> list[str]:
    return [str(v) for v in (values if isinstance(values, list) else []) if str(v).strip()]


def _cites(values: object) -> list[str]:
    return [format_concept_cite(c) for c in (values if isinstance(values, list) else []) if isinstance(c, dict)]


def _edge_lines(edge: dict) -> list[str]:
    """One bullet per edge; a corresponds_to edge carries its full basis underneath."""
    basis = edge.get("basis") if isinstance(edge.get("basis"), dict) else {}
    uid = f" ({basis['unification_id']})" if basis.get("unification_id") else ""
    lines = [f"- `{edge.get('relation')}` -> `{edge.get('target_id')}`{uid}"]
    lines.extend(f"  - **Holds when**: {cond}" for cond in _strings(basis.get("conditions")))
    lines.extend(f"  - **Differs**: {diff}" for diff in _strings(basis.get("differs")))
    cited = _cites(basis.get("citations")) + _cites(edge.get("citations"))
    if cited:
        lines.append(f"  - **Basis**: {'; '.join(cited)}")
    return lines


def format_node_card(node: dict) -> tuple[str, str, str, str, str]:
    """Return (port path, unit, concept id, title, card text) for one concept node."""
    cid = str(node["id"])
    rel_out = f"pages/concepts/ppa-node-{cid.replace('.', '-')}.md"
    proj = node.get("projections", {})
    lines = [
        f"# {node.get('title', cid)}",
        "",
        f"- **Concept ID**: `{cid}`",
        f"- **Altitude**: `{node.get('altitude', '')}` | **Unit**: `{node.get('unit', '')}`",
        f"- **Source Coordinates**: {'; '.join(_cites(node.get('citations')))}",
        "",
        "## Formal Summary",
        "",
        str(node.get("formal_summary", "")),
        "",
        "## Domain Projections",
        "",
        f"- **CS Theory**: {proj.get('cs_theory', '')}",
        f"- **SWE Architecture**: {proj.get('swe_architecture', '')}",
        f"- **Practical Debugging**: {proj.get('practical_debugging', '')}",
        f"- **Cyber**: {proj.get('cyber', '')}",
        "",
    ]
    conditions = _strings(node.get("conditions"))
    if conditions:
        lines.extend([CONDITIONS_HEADING, ""])
        lines.extend(f"- {cond}" for cond in conditions)
        lines.append("")
    edges = [e for e in node.get("related_edges", []) if isinstance(e, dict)]
    if edges:
        lines.extend([EDGES_HEADING, ""])
        for edge in edges:
            lines.extend(_edge_lines(edge))
        lines.append("")
    issue_refs = _strings(node.get("issue_refs"))
    if issue_refs:
        lines.extend(["## Related Issues", ""])
        lines.extend(f"- `{ref}`" for ref in issue_refs)
        lines.append("")
    refs = _strings(node.get("artifact_refs"))
    terms = _strings(node.get("external_terms"))
    lines.extend([
        "## Provenance",
        "",
        "- **Artifacts**: " + ("; ".join(f"`{r}`" for r in refs) if refs else "none recorded"),
        "- **External Terms**: " + ("; ".join(f"`{t}`" for t in terms) if terms else "none"),
        "",
    ])
    if len(lines) > CARD_MAX_LINES:
        raise common.AdapterError(f"{rel_out}: concept card exceeds {CARD_MAX_LINES} lines ({len(lines)})")
    return rel_out, str(node.get("unit", "unknown")), cid, str(node.get("title", cid)), "\n".join(lines) + "\n"
