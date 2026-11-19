#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-001, REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-001, REQ-PRD-PPA-006
# @decision DEC-PPA-005: Tier-A deterministic knowledge validator implementing
#   core-applicable checks of architecture/CONFORMANCE_SPEC.md (N1-N3, N8, C1.3,
#   C1.4, C1.9-C1.11, C3.1-C3.12, C4.1-C4.2, C6.1-C6.3, C6.8) and the discrete
#   conditions structure of ARCHITECTURE 7.1; a Tier A rule it does not perform
#   is printed as NOT_IMPLEMENTED in every mode, never as PASS.
# @decision DEC-PPA-011: ARCHITECTURE 7.1 L1 anchor parity and 7.2 signature
#   parity run as Tier A checks in every mode (scripts/ppa_arch_gates.py); a
#   check with nothing to examine is SKIP, and a missing inventory is FAIL.
"""Tier-A validator for the PPA semantic knowledge canonical core.

Usage:
    python3 -B scripts/validate_ppa_knowledge.py [--root DIR]
        [--strict-gotchas] [--certify]
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import issue_ctl  # noqa: E402  pylint: disable=wrong-import-position
import ppa_arch_gates as arch_gates  # noqa: E402  pylint: disable=wrong-import-position
import ppa_artifact_rules as rules  # noqa: E402  pylint: disable=wrong-import-position
import ppa_conformance_parity as parity  # noqa: E402  pylint: disable=wrong-import-position

LOG = logging.getLogger("validate_ppa_knowledge")

SKIP_DIRS = {".git", "tmp", "__pycache__", ".pytest_cache", "node_modules"}
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CITE_SINGLE_RE = re.compile(
    r"book\s+p\.\s*(\d{1,3})\s*[;,/|]\s*PDF\s+p\.\s*(\d{1,3})", re.I)
CITE_ROMAN_RE = re.compile(
    r"book\s+p\.\s*([IVXLCDM]+)\s*[;,/|]\s*PDF\s+p\.\s*(\d{1,2})")
CITE_RANGE_RE = re.compile(
    r"book\s+pp\.\s*(\d{1,3})\s*[–-]\s*(\d{1,3})\s*[;,/|]\s*PDF\s+pp\.\s*(\d{1,3})\s*[–-]\s*(\d{1,3})",
    re.I)
CITE_SHORT_RE = re.compile(r"\bp\.\s*(\d{1,3})\s*/\s*PDF\s+(\d{1,3})\b")
RAW_BOOK_RE = re.compile(r"\(book\s+pp?(?:\.|\s+\d|\s*[;,])[^)\n]*\)?", re.I)
VALID_BOOK_PAREN_RE = re.compile(
    r"^\(book\s+(?:"
    r"p\.\s*(?:\d{1,3}|[IVXLCDM]+);\s*PDF\s+p\.\s*\d{1,3}"
    r"|pp\.\s*\d{1,3}[–-]\d{1,3}(?:;\s*PDF\s+pp\.\s*\d{1,3}[–-]\d{1,3}"
    r"(?:;\s*(?:book\s+pp\.\s*\d{1,3}[–-]\d{1,3};\s*PDF\s+pp\.\s*\d{1,3}[–-]\d{1,3}"
    r"|\d+\s+PDF\s+pages))?)?"
    r")\)$"
)
CHAPTER_REGION = {
    **{str(i): f"chapter_{i}" for i in range(1, 7)},
    **{c: f"appendix_{c}" for c in "ABC"},
    "Notation": "index_of_notation",
    "Index": "subject_index",
    "Bibliography": "bibliography",
}
TABLE_COUNTS = {"1": 6, "2": 10, "3": 10, "5": 18, "6": 6, "C": 1}
FIGURE_COUNTS = {"1": 3, "2": 23, "3": 6, "4": 10, "5": 2, "6": 6, "A": 3, "C": 3}
NOT_IMPLEMENTED_TIER_A: dict[str, list[str]] = {}  # Tier A rules without a script (none at present)
ARCH_GATES = (
    ("arch_7_1_l1_anchor_parity", arch_gates.check_arch_7_1_l1_anchor_parity,
     "no concept node lists conditions"),
    ("arch_7_2_signature_parity", arch_gates.check_arch_7_2_signature_parity,
     "no statement above L3 cites a numbered item"),
)
CONFORMANCE_GATES_HINT = (
    "full C1-C6 gates are evaluated by --certify or scripts/verify_port_conformance.py"
)


class Report:
    """Collects per-check outcomes (PASS / FAIL / WARN / SKIP / NOT_IMPLEMENTED)."""

    def __init__(self, certify: bool = False) -> None:
        self.certify = certify
        self.results: list[tuple[str, str, list[str]]] = []

    def add(self, name: str, errors: list[str], skipped: str | None = None) -> None:
        status = "SKIP" if skipped else ("FAIL" if errors else "PASS")
        self.results.append((name, status, errors or ([skipped] if skipped else [])))

    def add_examined(self, name: str, errors: list[str], examined: int, empty: str) -> None:
        """Record a check that is SKIP, never PASS, when it had nothing to examine."""
        self.add(name, errors[:40], skipped=None if (errors or examined) else empty)

    def add_warn(self, name: str, warnings: list[str], strict: bool = False) -> None:
        if not warnings:
            self.results.append((name, "PASS", []))
        else:
            self.results.append((name, "FAIL" if strict else "WARN", warnings[:20]))

    def add_not_implemented(self, name: str, items: list[str]) -> None:
        """Record a Tier A rule this validator does not perform (never PASS, in any mode)."""
        self.results.append((name, "NOT_IMPLEMENTED", items))

    @property
    def not_implemented(self) -> list[str]:
        return [name for name, status, _ in self.results if status == "NOT_IMPLEMENTED"]

    @property
    def failed(self) -> bool:
        return any(status == "FAIL" for _, status, _ in self.results)

    def render(self) -> str:
        out = []
        for name, status, details in self.results:
            out.append(f"[{status}] {name}")
            out.extend(f"    - {d}" for d in details)
        return "\n".join(out)


def walk(root: Path, pattern: str) -> list[Path]:
    return sorted(p for p in root.rglob(pattern)
                  if p.is_file() and not any(part in SKIP_DIRS
                                             for part in p.relative_to(root).parts))


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def check_line_ceilings(root: Path) -> list[str]:
    """C3.1-C3.6, C3.12, C4.1-C4.2: budgets, closed tree, frontmatter, triggers."""
    return rules.check_artifacts(root)


# --------------------------------------------------------------------------
# JSON Schema subset
# --------------------------------------------------------------------------

TYPE_CHECKS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def resolve_ref(schema_root: dict, ref: str) -> dict:
    if not ref.startswith("#/"):
        raise ValueError(f"only local $ref supported: {ref}")
    node: object = schema_root
    for part in ref[2:].split("/"):
        if not isinstance(node, dict) or part not in node:
            raise ValueError(f"unresolvable $ref {ref}")
        node = node[part]
    if not isinstance(node, dict):
        raise ValueError(f"$ref {ref} does not point at a schema object")
    return node


def check_scalar(value: object, schema: dict, path: str) -> list[str]:
    errs: list[str] = []
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path}: {value!r} not in enum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errs.append(f"{path}: shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append(f"{path}: {value!r} does not match {schema['pattern']}")
    if TYPE_CHECKS["number"](value):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{path}: {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{path}: {value} > maximum {schema['maximum']}")
    return errs


def check_container(value: object, schema: dict, root: dict, path: str) -> list[str]:
    errs: list[str] = []
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errs.append(f"{path}: missing required {key!r}")
        props = schema.get("properties", {})
        for key, sub in value.items():
            if key in props:
                errs.extend(validate_schema(sub, props[key], root, f"{path}.{key}"))
            elif schema.get("additionalProperties", True) is False:
                errs.append(f"{path}: unexpected property {key!r}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errs.append(f"{path}: fewer than {schema['minItems']} items")
        if schema.get("uniqueItems"):
            seen = [json.dumps(v, sort_keys=True) for v in value]
            if len(seen) != len(set(seen)):
                errs.append(f"{path}: items not unique")
        if "items" in schema:
            for idx, item in enumerate(value):
                errs.extend(validate_schema(item, schema["items"], root, f"{path}[{idx}]"))
    return errs


def validate_schema(value: object, schema: dict, root: dict, path: str = "$") -> list[str]:
    """Validate value against a JSON-Schema subset; return error strings."""
    if "$ref" in schema:
        schema = resolve_ref(root, schema["$ref"])
    types = schema.get("type")
    if types is not None:
        types = [types] if isinstance(types, str) else types
        if not any(TYPE_CHECKS[t](value) for t in types):
            return [f"{path}: expected type {types}, got {type(value).__name__}"]
    return check_scalar(value, schema, path) + check_container(value, schema, root, path)


def load_json(path: Path) -> tuple[object | None, str | None]:
    text, uerr = rules.read_text_strict(path)
    if uerr is not None or text is None:
        return None, f"{path.name}: invalid UTF-8 ({uerr}) (N1)"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"{path.name}: {exc}"


def check_schema_file(schema: dict) -> list[str]:
    errs: list[str] = []
    inv = schema.get("x-relation-inverses")
    if not isinstance(inv, dict) or not inv:
        return ["schema: x-relation-inverses missing"]
    for rel_name, inverse in inv.items():
        if inv.get(inverse) != rel_name:
            errs.append(f"schema: inverse of {inverse!r} must be {rel_name!r}")
    try:
        enum = resolve_ref(schema, "#/$defs/edge")["properties"]["relation"]["enum"]
    except (KeyError, ValueError) as exc:
        return errs + [f"schema: cannot locate edge relation enum ({exc})"]
    if set(enum) != set(inv):
        errs.append(f"schema: relation enum and x-relation-inverses differ: "
                    f"{sorted(set(enum) ^ set(inv))}")
    return errs


# --------------------------------------------------------------------------
# Coordinate map & citations (C1.3, C1.4, C1.10, C1.11)
# --------------------------------------------------------------------------

class PageMap:
    """Read-only view over corpus/pdf_page_map.json."""

    def __init__(self, doc: dict) -> None:
        self.doc = doc
        self.pdf_of = {p["book_page"]: p["pdf_page"] for p in doc["pages"]
                       if p["book_page"] is not None}
        self.front_label_of = {p["pdf_page"]: p["label"] for p in doc["pages"]
                               if p["book_page"] is None and p.get("label")}
        self.front_of = {
            fm["name"]: {
                p["label"]: p["pdf_page"]
                for p in doc["pages"]
                if fm["pdf_start"] <= p["pdf_page"] <= fm["pdf_end"] and p.get("label")
            }
            for fm in doc.get("front_matter", [])
        }
        self.regions = doc["regions"]
        self.sections = doc["sections"]
        self.end_matter = doc.get("end_matter", {})
        self.statements = doc.get("statements", {})
        self.captions = {**doc["tables"], **doc["figures"]}
        self.bib = doc["bibliography_entries"]

    def nearest(self, book: int, forward: bool) -> int | None:
        """PDF page for book page, skipping absent (blank) pages in one direction."""
        step = 1 if forward else -1
        for b in range(book, book + 3 * step, step):
            if b in self.pdf_of:
                return self.pdf_of[b]
        return None


def check_page_map_inventory(doc: dict) -> list[str]:
    """C1.4: verify closed 51-table and 56-figure counts per chapter/appendix."""
    errs: list[str] = []
    for label, field, expected in (("tables", "tables", TABLE_COUNTS),
                                   ("figures", "figures", FIGURE_COUNTS)):
        got: dict[str, int] = {}
        for item in doc.get(field, {}).values():
            ch = str(item.get("chapter_or_app"))
            got[ch] = got.get(ch, 0) + 1
        if got != expected:
            errs.append(f"C1.4 {label} distribution {got} != expected {expected}")
    if doc.get("statement_gaps"):
        errs.append(f"page map has unresolved statement_gaps: {doc['statement_gaps']}")
    return errs


def _check_front_citation(cite: dict, pm: PageMap, where: str) -> list[str]:
    loc = str(cite.get("chapter_or_app"))
    roman = cite.get("book_page_roman")
    pdf = cite.get("pdf_page")
    if cite.get("book_page") is not None:
        return [f"{where}: front-matter citation {loc!r} must set book_page=null"]
    if not isinstance(roman, str) or not isinstance(pdf, int):
        return [f"{where}: front-matter citation {loc!r} requires book_page_roman and pdf_page"]
    fmap = pm.front_of.get(rules.LOC_FRONT[loc], {})
    if fmap.get(roman) != pdf:
        return [f"{where}: {loc} p. {roman} is PDF p. {fmap.get(roman)}, not {pdf}"]
    return []


def check_citation(cite: dict, pm: PageMap, where: str) -> list[str]:
    ch = str(cite.get("chapter_or_app"))
    if ch in rules.LOC_FRONT:
        return _check_front_citation(cite, pm, where)
    errs: list[str] = []
    book, pdf = cite.get("book_page"), cite.get("pdf_page")
    if not isinstance(book, int) or not isinstance(pdf, int):
        return [f"{where}: book_page/pdf_page must be integers"]
    if cite.get("book_page_roman") is not None:
        errs.append(f"{where}: book_page_roman only allowed on front-matter citations")
    if book not in pm.pdf_of:
        return [f"{where}: book p. {book} is absent from the PDF (blank page)"]
    if pm.pdf_of[book] != pdf:
        errs.append(f"{where}: book p. {book} is PDF p. {pm.pdf_of[book]}, not {pdf}")
    rkey = CHAPTER_REGION.get(ch, "")
    region = pm.regions.get(rkey)
    if region is None:
        errs.append(f"{where}: unknown chapter_or_app {cite.get('chapter_or_app')!r}")
    elif not region["book_start"] <= book <= region["book_end"]:
        errs.append(f"{where}: book p. {book} outside {ch} "
                    f"(pp. {region['book_start']}–{region['book_end']})")
    section = cite.get("section")
    m = re.match(r"^([1-6ABC]\.\d{1,2})", section or "")
    if m:
        sec = pm.sections.get(m.group(1))
        if sec is None:
            errs.append(f"{where}: unknown section {section!r}")
        elif not sec["book_start"] <= book <= sec["book_end"]:
            errs.append(f"{where}: book p. {book} outside §{m.group(1)} "
                        f"(pp. {sec['book_start']}–{sec['book_end']})")
    elif section in rules.END_PART and pm.end_matter:
        em = pm.end_matter.get(rkey, {}).get(rules.END_PART[section])
        if em is None or not em["book_start"] <= book <= em["book_end"]:
            errs.append(f"{where}: book p. {book} outside {ch} {section}")
    bm = re.match(r"^\[(\d{1,3})\]$", section or "")
    if bm:
        entry = pm.bib.get(bm.group(1))
        if entry is None or not entry["book_page"] <= book <= entry["book_page"] + 1:
            errs.append(f"{where}: bibliography entry {section} not on book p. {book}")
    tf = cite.get("table_or_fig")
    if tf:
        cap = pm.captions.get(tf)
        if cap is None:
            errs.append(f"{where}: unknown {tf!r}")
        elif abs(cap["book_page"] - book) > 1:
            errs.append(f"{where}: {tf} is on book p. {cap['book_page']}, not {book}")
    return errs


def _check_book_companions(text: str, where: str, pm: PageMap) -> list[str]:
    errs: list[str] = []
    for lineno, raw_line in rules.strip_fences_and_frontmatter(text):
        line = rules._mask_meta_code_spans(raw_line)  # pylint: disable=protected-access
        for m in RAW_BOOK_RE.finditer(line):
            tok = m.group(0)
            if not VALID_BOOK_PAREN_RE.match(tok):
                errs.append(f"{where}:{lineno}: malformed '(book p...)' token {tok!r} (C1.10)")
        for rx in (CITE_SINGLE_RE, CITE_SHORT_RE):
            for m in rx.finditer(line):
                book, pdf = int(m.group(1)), int(m.group(2))
                if pm.pdf_of.get(book) != pdf:
                    errs.append(f"{where}:{lineno}: '{m.group(0)}' expected PDF "
                                f"{pm.pdf_of.get(book)} for book p. {book}")
        for m in CITE_ROMAN_RE.finditer(line):
            roman, pdf = m.group(1), int(m.group(2))
            if pm.front_label_of.get(pdf) != roman:
                errs.append(f"{where}:{lineno}: '{m.group(0)}' expected label "
                            f"{pm.front_label_of.get(pdf)!r} at PDF p. {pdf}")
        for m in CITE_RANGE_RE.finditer(line):
            b_lo, b_hi, p_lo, p_hi = (int(g) for g in m.groups())
            exp = (pm.nearest(b_lo, True), pm.nearest(b_hi, False))
            if (p_lo, p_hi) != exp or b_lo > b_hi:
                errs.append(f"{where}:{lineno}: '{m.group(0)}' expected PDF pp. {exp[0]}–{exp[1]}")
    return errs


def check_inline_citations(root: Path, pm: PageMap) -> list[str]:
    """Verify N8 tokens and '(book p. X; PDF p. Y)' pairs across all Markdown files."""
    errs: list[str] = []
    for path in walk(root, "*.md"):
        where = rel(root, path)
        text, uerr = rules.read_text_strict(path)
        if uerr is not None or text is None:
            errs.append(f"{where}: invalid UTF-8 ({uerr}) (N1)")
            continue
        errs.extend(_check_book_companions(text, where, pm))
        errs.extend(rules.check_n8_citations(text, where, pm))
    return errs


# --------------------------------------------------------------------------
# Graph, links, fragments, reachability, artifact_refs, issues
# --------------------------------------------------------------------------

github_slug = arch_gates.github_slug


def headings_of_text(text: str) -> set[str]:
    """Return GitHub-style normalized heading anchor slugs for markdown text."""
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    for _, line in rules.strip_fences_and_frontmatter(text):
        m = re.match(r"^#{1,6}\s+(.+?)\s*#*$", line)
        if m:
            base = github_slug(m.group(1))
            idx = counts.get(base, 0)
            counts[base] = idx + 1
            slugs.add(base if idx == 0 else f"{base}-{idx}")
            slugs.add(re.sub(r"-+", "-", base).strip("-"))
    return slugs


def headings_of(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path in cache:
        return cache[path]
    text, err = rules.read_text_strict(path)
    if err is not None or text is None:
        cache[path] = set()
        return set()
    slugs = headings_of_text(text)
    cache[path] = slugs
    return slugs


def check_graph(concepts: list[dict], inverses: dict[str, str]) -> list[str]:
    errs: list[str] = []
    ids = [c.get("id") for c in concepts]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        errs.append(f"duplicate concept ids: {dupes}")
    edges = {(c.get("id"), e.get("target_id"), e.get("relation"))
             for c in concepts for e in c.get("related_edges", [])}
    known = set(ids)
    for c in concepts:
        for e in c.get("related_edges", []):
            if e.get("relation") == "corresponds_to" and not isinstance(e.get("basis"), dict):
                errs.append(f"{c.get('id')} -> {e.get('target_id')}: corresponds_to requires basis")
    for src, dst, relation in sorted(edges, key=str):
        if dst == src:
            errs.append(f"{src}: self edge ({relation})")
        elif dst not in known:
            errs.append(f"{src}: edge target {dst!r} does not exist")
        elif (dst, src, inverses.get(relation)) not in edges:
            errs.append(f"{src} -[{relation}]-> {dst} lacks inverse "
                        f"{dst} -[{inverses.get(relation)}]-> {src}")
    return errs


def check_artifact_refs(root: Path, concepts: list[dict]) -> list[str]:
    """C3.11: every concept's artifact_refs exist inside root and fragments resolve."""
    errs: list[str] = []
    root_res = root.resolve()
    hcache: dict[Path, set[str]] = {}
    for c in concepts:
        cid = c.get("id", "<unknown>")
        refs = c.get("artifact_refs", [])
        if not refs and not c.get("artifact_exclusion"):
            errs.append(f"{cid}: artifact_refs is empty without artifact_exclusion (C3.11)")
        for ref in refs:
            if not isinstance(ref, str):
                continue
            clean, *frag = ref.split("#", 1)
            dest = (root / clean).resolve()
            if root_res not in dest.parents or not dest.is_file():
                errs.append(f"{cid}: broken artifact_ref {ref!r} (C3.11)")
            elif frag and dest.suffix == ".md" and frag[0] not in headings_of(dest, hcache):
                errs.append(f"{cid}: broken heading fragment in artifact_ref {ref!r} (C3.11)")
    return errs


def _check_knowledge_direction(root: Path, src: Path, dest: Path,
                               lineno: int, target: str) -> list[str]:
    """C3.8 + B2: link direction & package containment inside knowledge/."""
    s_parts = src.relative_to(root).parts
    if s_parts[0] != "knowledge":
        return []
    kroot = (root / "knowledge").resolve()
    where = f"{rel(root, src)}:{lineno}"
    if kroot not in dest.parents and dest != kroot:
        return [f"{where}: knowledge link {target!r} escapes knowledge/ (C3.8)"]
    d_parts = dest.relative_to(root).parts
    if len(s_parts) >= 4 and s_parts[1] == "skills":
        src_skill = s_parts[2]
        if s_parts[3] == "references" and dest.name == "SKILL.md":
            return [f"{where}: reference must not link to SKILL.md ({target!r}, C3.8)"]
        if dest.name == "SKILL.md" and (len(d_parts) < 3 or d_parts[2] != src_skill):
            return [f"{where}: inter-skill SKILL.md link forbidden ({target!r}, C3.8)"]
        if src_skill != rules.ROUTER_SKILL and len(d_parts) >= 2 and d_parts[1] == "ambient-context":
            return [f"{where}: non-router skill must not link to ambient-context ({target!r}, B2)"]
    return []


def check_reachability(root: Path, outbound: dict[Path, set[Path]]) -> list[str]:
    """C3.9: every non-router skill is named in router; every reference is linked from its SKILL.md."""
    errs: list[str] = []
    dirs = rules.skill_dirs(root)
    router_md = root / "knowledge" / "skills" / rules.ROUTER_SKILL / "SKILL.md"
    router_txt = ""
    if router_md.is_file():
        txt, _ = rules.read_text_strict(router_md)
        router_txt = txt or ""
    for d in dirs:
        skill_md = (d / "SKILL.md").resolve()
        if d.name != rules.ROUTER_SKILL and router_md.is_file():
            if not re.search(rf"(?<![A-Za-z0-9-]){re.escape(d.name)}(?![A-Za-z0-9-])", router_txt):
                errs.append(f"{rel(root, router_md)}: missing non-router skill {d.name!r} (C3.9)")
        linked = outbound.get(skill_md, set())
        for ref in sorted((d / "references").glob("*.md")):
            if ref.resolve() not in linked:
                errs.append(f"{rel(root, ref)}: orphan reference not linked from "
                            f"{rel(root, skill_md)} (C3.9)")
    return errs


def check_links(root: Path) -> list[str]:
    """C3.7 + C3.8 + C3.9: relative links, #fragments, direction, reachability."""
    errs: list[str] = []
    root_res = root.resolve()
    hcache: dict[Path, set[str]] = {}
    outbound: dict[Path, set[Path]] = {}
    for path in walk(root, "*.md"):
        where = rel(root, path)
        text, uerr = rules.read_text_strict(path)
        if uerr is not None or text is None:
            errs.append(f"{where}: invalid UTF-8 ({uerr}) (N1)")
            continue
        src_res = path.resolve()
        for lineno, line in rules.strip_fences_and_frontmatter(text):
            for m in LINK_RE.finditer(line):
                target = m.group(1)
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue
                clean, *frag = target.split("#", 1)
                if clean.startswith("/"):
                    errs.append(f"{where}:{lineno}: absolute link {target!r} (C3.7)")
                    continue
                dest = (path.parent / clean).resolve() if clean else src_res
                if root_res not in dest.parents and dest != root_res:
                    errs.append(f"{where}:{lineno}: link escapes root {target!r} (C3.8)")
                elif not dest.exists():
                    errs.append(f"{where}:{lineno}: broken link {target!r} (C3.7)")
                else:
                    outbound.setdefault(src_res, set()).add(dest)
                    errs.extend(_check_knowledge_direction(root, path, dest, lineno, target))
                    if frag and dest.suffix == ".md" and frag[0] not in headings_of(dest, hcache):
                        errs.append(f"{where}:{lineno}: broken heading fragment {target!r} (C3.7)")
    errs.extend(check_reachability(root, outbound))
    return errs


def check_issues(root: Path) -> list[str]:
    if not (root / "issues").is_dir():
        return ["issues/ directory missing"]
    _, errors = issue_ctl.collect(root)
    return errors


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def run_graph_checks(root: Path, report: Report, pm: PageMap | None) -> None:
    schema_path = root / "ontology" / "concept_graph.schema.json"
    graph_path = root / "ontology" / "concept_graph.json"
    schema, err = load_json(schema_path)
    if err or not isinstance(schema, dict):
        report.add("schema", [err or "schema must be a JSON object"])
        return
    schema_errs = check_schema_file(schema)
    if not graph_path.exists():
        report.add("schema", schema_errs)
        report.add("graph", [], skipped="ontology/concept_graph.json not yet created")
        report.add("artifact_refs", [], skipped="no concept graph")
        for name in ("arch_7_1_conditions_parity",) + tuple(gate[0] for gate in ARCH_GATES):
            report.add(name, [], skipped="no concept graph")
        report.add("concept_citations", [], skipped="no concept graph")
        return
    graph, err = load_json(graph_path)
    if err:
        report.add("schema", schema_errs + [err])
        return
    report.add("schema", schema_errs + validate_schema(graph, schema, schema))
    concepts = graph.get("concepts", []) if isinstance(graph, dict) else []
    concepts = [c for c in concepts if isinstance(c, dict)]
    report.add("graph", check_graph(concepts, schema.get("x-relation-inverses", {})))
    report.add("artifact_refs", check_artifact_refs(root, concepts))
    parity_errs, _ = parity.graph_conditions_errors(concepts)
    report.add("arch_7_1_conditions_parity", parity_errs + parity.conditions_home_errors(concepts))
    for name, gate, empty in ARCH_GATES:
        report.add_examined(name, *gate(root, graph), empty)
    if pm is None:
        report.add("concept_citations", [], skipped="no page map")
        return
    cite_errs: list[str] = []
    for c in concepts:
        for idx, cite in enumerate(c.get("citations", [])):
            if isinstance(cite, dict):
                cite_errs.extend(check_citation(cite, pm, f"{c.get('id')}.citations[{idx}]"))
        for eidx, edge in enumerate(c.get("related_edges", [])):
            if not isinstance(edge, dict):
                continue
            for cidx, ec in enumerate(edge.get("citations", [])):
                if isinstance(ec, dict):
                    cite_errs.extend(check_citation(
                        ec, pm, f"{c.get('id')}.related_edges[{eidx}].citations[{cidx}]"))
            basis = edge.get("basis")
            if isinstance(basis, dict):
                for bidx, bc in enumerate(basis.get("citations", [])):
                    if isinstance(bc, dict):
                        cite_errs.extend(check_citation(
                            bc, pm, f"{c.get('id')}.related_edges[{eidx}].basis.citations[{bidx}]"))
    report.add("concept_citations", cite_errs)


def validate(root: Path, strict_gotchas: bool = False, certify: bool = False) -> Report:
    report = Report(certify=certify)
    report.add("line_ceilings", check_line_ceilings(root))
    report.add("evals", rules.check_evals(root))
    ledger_errs, n_shards, ledger_ids = rules.collect_gotcha_ledgers(root)
    report.add("gotcha_ledger", ledger_errs,
               skipped=None if n_shards else "no corpus/shards/RAW_SHARD_*.md yet")
    if n_shards:
        cov = rules.check_gotcha_coverage(root, ledger_ids)
        report.add_warn("gotcha_coverage", cov, strict=strict_gotchas or certify)
    map_path = root / "corpus" / "pdf_page_map.json"
    doc, err = load_json(map_path) if map_path.exists() else (None, None)
    pm = PageMap(doc) if isinstance(doc, dict) else None
    if err:
        report.add("page_map", [err])
    elif pm is None or not isinstance(doc, dict):
        report.add("page_map", ["corpus/pdf_page_map.json missing"])
    else:
        report.add("page_map", check_page_map_inventory(doc))
    run_graph_checks(root, report, pm)
    if pm is not None:
        report.add("inline_citations", check_inline_citations(root, pm))
    report.add("links", check_links(root))
    report.add("issues", check_issues(root))
    if certify:
        import verify_port_conformance as vpc  # noqa: PLC0415
        vpc_rep, vpc_code = vpc.certify(core_root=root, canonical_only=True)
        bad_chks = vpc.failed_check_codes(vpc_rep)
        if vpc_code != 0 and not bad_chks:
            bad_chks = [f"verdict={vpc_rep.get('verdict')}"]
        report.add("conformance_gates_canonical", bad_chks)
    else:
        report.add("conformance_gates_canonical", [], skipped=CONFORMANCE_GATES_HINT)
    for name, items in NOT_IMPLEMENTED_TIER_A.items():
        report.add_not_implemented(name, items)
    return report


def main(argv: list[str]) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="Tier-A PPA knowledge validator")
    ap.add_argument("--root", default=".")
    ap.add_argument("--strict-gotchas", action="store_true",
                    help="fail on unreferenced gotcha-ledger IDs (C1.9 whole-book gate)")
    ap.add_argument("--certify", action="store_true",
                    help="enforce strict gotchas and full C1-C6 canonical conformance gates")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    try:
        report = validate(root, strict_gotchas=args.strict_gotchas, certify=args.certify)
    except (OSError, ValueError, KeyError) as exc:
        LOG.error("validator crashed on malformed input: %s", exc)
        return 1
    print(report.render())
    pending = report.not_implemented
    suffix = f" ({len(pending)} NOT_IMPLEMENTED: {', '.join(pending)})" if pending else ""
    print(f"validate_ppa_knowledge {'FAIL' if report.failed else 'PASS'}{suffix}")
    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
