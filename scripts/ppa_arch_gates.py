#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-005 @parent: REQ-PRD-PPA-005
# @decision DEC-PPA-011: The two remaining Tier A clauses of ARCHITECTURE 7 are
#   literal, deterministic comparisons. 7.1: every node that lists conditions
#   resolves an L1 reference anchor whose section carries at least as many
#   discrete entries. 7.2: every statement above L3 that cites a numbered item
#   is compared with the cited L3 shard anchor and with a closed list of
#   signature rules; ontology/notation_index.md must parse with its key
#   signature rows intact, so neither check can pass on missing inventories.
"""Tier A checks for ARCHITECTURE 7.1 (L1 anchor parity) and 7.2 (signature parity)."""
from __future__ import annotations

import re
from pathlib import Path

import ppa_artifact_rules as rules

L1_REF_RE = re.compile(r"^(knowledge/skills/[^/#]+/references/[^/#]+\.md)#(.+)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*$")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")
TABLE_SEPARATOR_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?$")
NUMBERED_RE = re.compile(
    r"\b(Lemma|Theorem|Proposition|Corollary|Fact|Table|Exercise)s?\s+((?:\d|[ABC])\.\d+)\b")
THEOREM_KINDS = ("Lemma", "Theorem", "Proposition", "Corollary", "Fact")
IFF_RE = re.compile(r"\biff\b|\bif and only if\b|⇔|⟺", re.I)
L3_EQUIVALENCE_RE = re.compile(
    r"\biff\b|\bif and only if\b|[⇔⟺↔]|\bequivalen|\b(?:exactly|precisely) when\b"
    r"|\bnecessary and sufficient\b", re.I)
L3_IMPLICATION_RE = re.compile(r"\bif\b[^.\n]{0,240}\bthen\b", re.I | re.S)
NEGATION_RE = re.compile(r"\b(?:not|no|never|without|neither|nor)\b", re.I)
SEPARATION_TAG_RE = re.compile(r"\[external\b|\[derived\]")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z`*\[(])")
ABBREVIATION_RE = re.compile(r"(?:\bpp?|\bcf|\be\.g|\bi\.e|\bvs|\bresp|\betc|\bEx|\bFig)\.$")
LOOP_BOUND_RE = re.compile(r"Lemma 6\.12\b|\bd\s*(?:\([^)]*\))?\s*\+\s*3\b")
FAST_DISTRIBUTIVE_RE = re.compile(
    r"\bfast\b[\s,-]*(?:and\s+)?distributive\b|\bdistributive\b[\s,-]*(?:and\s+)?fast\b", re.I)
STRICT_GAIN_RE = re.compile(r"\bstrictly\s+(?:improves?|greater|better|more\s+precise)\b", re.I)
ONLY_UPON_EMPTY_RE = re.compile(r"\bonly\s+(?:upon|when|once|at)\s+W\s*=\s*(?:empty|∅)", re.I)
CERTIFIED_RE = re.compile(r"\b(?:certified|proved|proven|established|guaranteed)\b", re.I)
STRICT_UNDER_RE = re.compile(r"\bstrictly\s+under-?\s*approximat", re.I)
NOT_REDUCTIVE_RE = re.compile(r"Analysis(?:_i|ᵢ)?(?:\[[^\]]*\])?\s*∉\s*Red\b")
REC_BEHAVIOUR_RE = re.compile(r"\brec\s+β")
POSITIVITY_RE = re.compile(r"\bpositiv", re.I)
DUAL_WIDENING_RE = re.compile(r"\bdual[\s-]+widening\b", re.I)
GFP_FROM_ABOVE_RE = re.compile(r"approximat\w*[^.]{0,60}\bgfp\b[^.]{0,60}\bfrom\s+above\b", re.I)
CLOSURE_EQUALITY_RE = re.compile(r"\blfp\([^)]*\)\s*=\s*f̄")
NOTATION_ROW_RE = re.compile(r"^\|\s*(N[123]-\d{3})\s*\|")
NOTATION_INDEX = "ontology/notation_index.md"
SHARDS_DIR = "corpus/shards"
KEY_SIGNATURES: dict[str, tuple[str, str]] = {  # row id -> literals of its (symbol, meaning) cells
    "N1-007": ("∇", "L × L → L"),
    "N3-103": ("gfp", "greatest fixed point"),
    "N3-138": ("lfp", "least fixed point"),
    "N3-144": ("MFP", "least solution"),
    "N3-145": ("MOP", "all paths"),
    "N3-186": ("Red", "f(l) ⊑ l"),
}


def github_slug(heading: str) -> str:
    """GitHub-style anchor slug of one Markdown heading text."""
    s = re.sub(r"`([^`]*)`", r"\1", heading.strip())
    s = re.sub(r"[*_~]", "", s).lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    return re.sub(r"\s", "-", s.strip())


def section_bodies(text: str) -> dict[str, list[str]]:
    """Map each heading slug to its section lines: down to the next same-or-higher heading.

    Subsections belong to their parents; fenced code and YAML frontmatter are excluded.
    """
    bodies: dict[str, list[str]] = {}
    seen: dict[str, int] = {}
    open_sections: list[tuple[int, list[str]]] = []
    for _, line in rules.strip_fences_and_frontmatter(text):
        match = HEADING_RE.match(line)
        if not match:
            for _, body in open_sections:
                body.append(line)
            continue
        level, base = len(match.group(1)), github_slug(match.group(2))
        idx = seen.get(base, 0)
        seen[base] = idx + 1
        body: list[str] = []
        for slug in (base if idx == 0 else f"{base}-{idx}", re.sub(r"-+", "-", base).strip("-")):
            bodies.setdefault(slug, body)
        open_sections = [(lv, b) for lv, b in open_sections if lv < level] + [(level, body)]
    return bodies


def count_discrete_entries(lines: list[str]) -> int:
    """Count bullet items, numbered items, and table data rows (header and separator excluded)."""
    total = 0
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|"):
            if TABLE_SEPARATOR_RE.match(stripped):
                in_table = True
            elif in_table:
                total += 1
            else:
                in_table = True
            continue
        in_table = False
        if LIST_ITEM_RE.match(line):
            total += 1
    return total


def _concepts(graph: object) -> list[dict]:
    nodes = graph.get("concepts", []) if isinstance(graph, dict) else []
    return [n for n in nodes if isinstance(n, dict)] if isinstance(nodes, list) else []


def check_arch_7_1_l1_anchor_parity(root: Path, graph: object) -> tuple[list[str], int]:
    """ARCHITECTURE 7.1 anchor clause; returns (findings, nodes with conditions examined).

    A node with ``conditions`` needs an ``artifact_refs`` entry of the form
    ``knowledge/skills/<skill>/references/<file>.md#<slug>`` that resolves, and every
    such resolving section must carry at least ``len(conditions)`` discrete entries.
    """
    errs: list[str] = []
    examined = 0
    cache: dict[str, dict[str, list[str]]] = {}
    for node in _concepts(graph):
        conds = node.get("conditions")
        wanted = len([c for c in conds if str(c).strip()]) if isinstance(conds, list) else 0
        if not wanted:
            continue
        examined += 1
        cid = str(node.get("id", "?"))
        resolved = 0
        refs = node.get("artifact_refs")
        for ref in refs if isinstance(refs, list) else []:
            match = L1_REF_RE.match(str(ref))
            if not match or ".." in match.group(1).split("/"):
                continue
            rel, slug = match.groups()
            if rel not in cache:
                path = root / rel
                text, err = rules.read_text_strict(path) if path.is_file() else (None, "missing")
                cache[rel] = section_bodies(text) if (text is not None and not err) else {}
            if slug not in cache[rel]:
                continue
            resolved += 1
            carried = count_discrete_entries(cache[rel][slug])
            if carried < wanted:
                errs.append(f"{cid}: {wanted} conditions but L1 anchor {ref} carries "
                            f"{carried} discrete entries")
        if not resolved:
            errs.append(f"{cid}: {wanted} conditions but no resolving L1 reference anchor "
                        "(references/<file>.md#<slug>) in artifact_refs")
    return errs, examined


def _plain(text: str) -> str:
    """Drop code-span and emphasis markers and collapse whitespace for literal matching."""
    return " ".join(re.sub(r"[`*]", "", text).split())


def _labels(text: str) -> list[str]:
    return [f"{m.group(1)} {m.group(2)}" for m in NUMBERED_RE.finditer(text)]


def sentences(text: str) -> list[str]:
    """Split prose into sentences without breaking after page or Latin abbreviations."""
    out: list[str] = []
    for part in SENTENCE_SPLIT_RE.split(text):
        if out and ABBREVIATION_RE.search(out[-1]):
            out[-1] = f"{out[-1]} {part}"
        elif part.strip():
            out.append(part.strip())
    return out


def markdown_items(text: str) -> list[tuple[int, str, list[str]]]:
    """(line, item text, statement units) for headings, list items, table rows, paragraphs.

    A list item or paragraph spans its continuation lines; the units of a table row
    are the sentences of each cell plus the row as a whole, so a claim split across
    cells is still read as one statement.
    """
    items: list[tuple[int, str, list[str]]] = []
    cur: list[str] = []
    start = 0
    for lineno, line in rules.strip_fences_and_frontmatter(text) + [(0, "")]:
        stripped = line.strip()
        boundary = (not stripped or stripped.startswith(("#", "|", "<!--"))
                    or bool(LIST_ITEM_RE.match(line)))
        if boundary and cur:
            joined = " ".join(cur)
            items.append((start, joined, sentences(joined)))
            cur = []
        if not stripped or stripped.startswith("<!--"):
            continue
        if stripped.startswith("|"):
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", stripped) if c.strip()]
            whole = [" ".join(cells)] if len(cells) > 1 else []
            items.append((lineno, stripped, [s for cell in cells for s in sentences(cell)] + whole))
            continue
        if not cur:
            start = lineno
        cur.append(stripped)
    return items


def l3_anchor_index(root: Path) -> dict[str, str]:
    """Numbered item -> text of its L3 anchor in corpus/shards/RAW_SHARD_*.md.

    The anchor is every section whose heading names the item (heading text and
    fenced statements included); an item no heading names falls back to the shard
    lines naming it.
    """
    sections: dict[str, list[str]] = {}
    mentions: dict[str, list[str]] = {}
    shard_dir = root / SHARDS_DIR
    for shard in sorted(shard_dir.glob("RAW_SHARD_*.md")) if shard_dir.is_dir() else []:
        text, err = rules.read_text_strict(shard)
        if err or text is None:
            continue
        open_sections: list[tuple[int, list[str]]] = []
        fence: str | None = None
        for line in rules.split_lines_n2(text):
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                fence = stripped[:3] if fence is None else (None if fence == stripped[:3] else fence)
                continue
            match = HEADING_RE.match(line) if fence is None else None
            if match:
                level = len(match.group(1))
                open_sections = [(lv, ls) for lv, ls in open_sections if lv < level]
                open_sections.append((level, _labels(match.group(2))))
                for label in open_sections[-1][1]:
                    sections.setdefault(label, []).append(match.group(2))
                continue
            for _, labels in open_sections:
                for label in labels:
                    sections.setdefault(label, []).append(line)
            for label in _labels(line):
                mentions.setdefault(label, []).append(line)
    index = {label: "\n".join(lines) for label, lines in mentions.items()}
    index.update({label: "\n".join(lines) for label, lines in sections.items()})
    return index


def notation_index_errors(root: Path) -> tuple[list[str], int]:
    """Parse ontology/notation_index.md; return (findings, rows parsed).

    Every ``N<part>-<nnn>`` row needs a non-empty symbol and index page, ids are
    unique, and each KEY_SIGNATURES row carries its symbol and meaning literal.
    """
    path = root / NOTATION_INDEX
    text, err = rules.read_text_strict(path) if path.is_file() else (None, "missing")
    if err or text is None:
        return [f"{NOTATION_INDEX}:0 (missing or unreadable: signature parity has no inventory)"], 0
    errs: list[str] = []
    rows: dict[str, list[str]] = {}
    for lineno, line in enumerate(rules.split_lines_n2(text), start=1):
        match = NOTATION_ROW_RE.match(line)
        if not match:
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        row_id = match.group(1)
        if row_id in rows:
            errs.append(f"{NOTATION_INDEX}:{lineno} (duplicate row id {row_id})")
        rows[row_id] = cells
        if len(cells) < 6 or not cells[1].strip("` ") or not cells[-1]:
            errs.append(f"{NOTATION_INDEX}:{lineno} ({row_id} lacks a symbol or index page)")
    if not rows:
        return [f"{NOTATION_INDEX}:0 (no N1/N2/N3 rows parsed)"], 0
    for row_id, (symbol, meaning) in sorted(KEY_SIGNATURES.items()):
        cells = rows.get(row_id)
        if cells is None or len(cells) < 4 or symbol not in cells[1] or meaning not in cells[3]:
            errs.append(f"{NOTATION_INDEX}:0 (key signature {row_id} {symbol!r} must state {meaning!r})")
    return errs, len(rows)


def _asserted(sentence: str, pattern: re.Pattern[str]) -> bool:
    """True when pattern occurs in sentence and is not negated within the 60 characters before it."""
    for match in pattern.finditer(sentence):
        if not NEGATION_RE.search(sentence[max(0, match.start() - 60):match.start()]):
            return True
    return False


def _paren_groups(text: str) -> list[tuple[int, ...]]:
    """For each character, the start offsets of the round-bracket groups enclosing it."""
    out: list[tuple[int, ...]] = []
    stack: tuple[int, ...] = ()
    for idx, char in enumerate(text):
        if char == ")" and stack:
            stack = stack[:-1]
        out.append(stack)
        if char == "(":
            stack += (idx,)
    return out


def _biconditional_finding(unit: str, item: str, l3: dict[str, str]) -> str | None:
    """An asserted biconditional whose cited L3 anchors state an implication and no equivalence.

    A numbered item is attributed to a biconditional when it is cited inside the
    round-bracket group that holds the connective (the whole unit when at top level),
    so a parenthesised definition does not inherit citations made outside it.
    """
    groups = _paren_groups(unit)
    for match in IFF_RE.finditer(unit):
        if NEGATION_RE.search(unit[max(0, match.start() - 60):match.start()]):
            continue
        if "Lemma 2.32" in item and "MFP" in unit and "MOP" in unit:
            return "biconditional over Lemma 2.32, which states only 'if ... then MFP = MOP'"
        home = groups[match.start()][-1] if groups[match.start()] else None
        near = [(m.group(1), f"{m.group(1)} {m.group(2)}") for m in NUMBERED_RE.finditer(unit)
                if home is None or home in groups[m.start()]]
        theorems = sorted({label for kind, label in near if kind in THEOREM_KINDS})
        support = [l3[label] for label in {lb for _, lb in near} if label in l3]
        stated = [l3[label] for label in theorems if label in l3]
        if stated and not any(L3_EQUIVALENCE_RE.search(a) for a in support) \
                and any(L3_IMPLICATION_RE.search(a) for a in stated):
            return (f"biconditional over {', '.join(theorems)}, whose L3 anchor states an "
                    "'if ... then' implication and no equivalence")
    return None


def _unit_findings(unit: str, item: str, l3: dict[str, str]) -> list[str]:
    """Signature findings of one statement unit, given its whole item as citation context."""
    biconditional = _biconditional_finding(unit, item, l3)
    found: list[str] = [biconditional] if biconditional else []
    if LOOP_BOUND_RE.search(item) and FAST_DISTRIBUTIVE_RE.search(unit) \
            and not SEPARATION_TAG_RE.search(unit):
        found.append("Lemma 6.12 bound d + 3 widened to fast distributive frameworks without an "
                     "[external ...] or [derived] tag")
    if ("Lemma 4.45" in item or ("§4.5.3" in item and "p. 270" in item)) \
            and _asserted(unit, STRICT_GAIN_RE):
        found.append("strict gain attributed to Lemma 4.45 / §4.5.3 p. 270, which state an equality")
    if re.search(r"Lemma 6\.4\b", item):
        if ONLY_UPON_EMPTY_RE.search(unit) and not CERTIFIED_RE.search(unit):
            found.append("Lemma 6.4: reductiveness 'only upon W = empty' without 'certified' or 'proved'")
        if _asserted(unit, STRICT_UNDER_RE) or _asserted(unit, NOT_REDUCTIVE_RE):
            found.append("Lemma 6.4 proves Analysis_i ⊑ lfp only; strict under-approximation or "
                         "non-membership in Red is not stated")
    if "Table 5.18" in item and REC_BEHAVIOUR_RE.search(unit) and _asserted(unit, POSITIVITY_RE) \
            and "[derived]" not in unit:
        found.append("positivity of rec β.φ attributed to Table 5.18 without [derived]")
    if DUAL_WIDENING_RE.search(unit) and _asserted(unit, GFP_FROM_ABOVE_RE):
        found.append("dual widening said to approximate gfp from above")
    if CLOSURE_EQUALITY_RE.search(unit) and re.search(r"\bEx(?:ercise)?\s+6\.14\b", item) \
            and re.search(r"\bfast\b", item, re.I) and not re.search(r"distributiv", item, re.I):
        found.append("Exercise 6.14 closure lfp(...) = f̄ claimed for fast f without distributivity")
    return found


def _upper_items(root: Path, graph: object) -> list[tuple[str, str, list[str]]]:
    """(location, item, statement units) for every statement item above L3."""
    out: list[tuple[str, str, list[str]]] = []
    for node in _concepts(graph):
        cid = str(node.get("id", "?"))
        fields = [("formal_summary", node.get("formal_summary"))]
        conds = node.get("conditions")
        fields += [(f"conditions[{i}]", c) for i, c in enumerate(conds if isinstance(conds, list) else [])]
        for name, value in fields:
            if isinstance(value, str) and value.strip():
                out.append((f"ontology/concept_graph.json:{cid}.{name}", value, sentences(value)))
    files = [root / "ontology" / "cross_paradigm_matrix.md"]
    files += sorted((root / "knowledge" / "ambient-context").glob("*.md"))
    files += sorted((root / "knowledge" / "skills").glob("*/SKILL.md"))
    files += sorted((root / "knowledge" / "skills").glob("*/references/*.md"))
    for path in files:
        text, err = rules.read_text_strict(path) if path.is_file() else (None, "missing")
        if err or text is None:
            continue
        rel = path.relative_to(root).as_posix()
        out.extend((f"{rel}:{lineno}", item, units) for lineno, item, units in markdown_items(text))
    return out


def check_arch_7_2_signature_parity(root: Path, graph: object) -> tuple[list[str], int]:
    """ARCHITECTURE 7.2 Tier A; returns (findings, cited statement items examined).

    Fails, never passes, when the notation index or the L3 shard anchors are
    missing: the comparison then has no inventory to read.
    """
    errs, _ = notation_index_errors(root)
    l3 = l3_anchor_index(root)
    if not l3:
        errs.append(f"{SHARDS_DIR}:0 (no L3 anchor for any numbered item: signature parity is vacuous)")
    examined = 0
    for where, item, units in _upper_items(root, graph):
        plain_item = _plain(item)
        examined += int(bool(NUMBERED_RE.search(plain_item)))
        reported: set[str] = set()
        for plain_unit in (_plain(unit) for unit in units):
            for finding in _unit_findings(plain_unit, plain_item, l3):
                if finding not in reported:
                    reported.add(finding)
                    errs.append(f"{where} (SIGNATURE_DISTORTION: {finding}): {plain_unit[:120]!r}")
    return errs, examined
