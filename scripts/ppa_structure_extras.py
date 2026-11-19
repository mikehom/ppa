#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001
# @decision DEC-PPA-004: Chapter end-matter ranges and a numbered-statement
#   inventory complete the coordinate map, so section attributions end where
#   Concluding Remarks begin and invented item numbers fail Tier A.
"""End-matter and numbered-statement detection for extract_ppa_structure.py.

Numbering conventions of the book (verified on page images during Units 0-2):
Examples, Lemmas, Theorems, Propositions, Corollaries and Facts share ONE
sequence per chapter/appendix (e.g. 2.1-2.32); Exercises and Mini Projects each
have their own sequence per chapter. Items that the OCR text layer does not
expose are reported as gaps with a page window instead of being guessed.
"""
from __future__ import annotations

import re

END_MATTER = (("concluding_remarks", "Concluding Remarks"),
              ("mini_projects", "Mini Projects"),
              ("exercises", "Exercises"))
SHARED_KINDS = ("Example", "Lemma", "Theorem", "Proposition", "Corollary", "Fact")
TOP_OF_PAGE_LINES = 3
# Headings the OCR text layer does not expose, confirmed on rendered page images:
# (unit, sequence, number) -> (kind, book page).
STATEMENT_OVERRIDES = {
    ("1", "shared", 2): ("Example", 11),
    ("3", "shared", 11): ("Fact", 160),
}
STATEMENT_RE = re.compile(
    r"^(Lemma|Theorem|Proposition|Corollary|Fact|Exa(?:m|rn)ple|Exercise|Mini\s*Project)"
    r"[*⋆]?\s+([1-6ABC])\s*[.,o]\s*([0-9lI])(?:\s?([0-9lIO]))?(?![A-Za-z0-9])")


def _nonblank(page: str) -> list[str]:
    return [ln.strip() for ln in page.splitlines() if ln.strip()]


def _num(a: str, b: str | None) -> int:
    digits = (a + (b or "")).replace("l", "1").replace("I", "1").replace("O", "0")
    return int(digits)


def detect_end_matter(pages: list[str], regions: dict, sections: dict,
                      book_of: dict[int, int]) -> dict[str, dict]:
    """Per chapter/appendix: start of Concluding Remarks, Mini Projects, Exercises."""
    out: dict[str, dict] = {}
    for key, reg in regions.items():
        if not key.startswith(("chapter_", "appendix_")):
            continue
        last_sec = max(s["pdf_start"] for s in sections.values() if s["region"] == key)
        parts: dict[str, dict] = {}
        for part, heading in END_MATTER:
            for pdf in range(last_sec, reg["pdf_end"] + 1):
                idx = [i for i, ln in enumerate(_nonblank(pages[pdf - 1])) if ln == heading]
                if idx:
                    parts[part] = {"title": heading, "region": key, "pdf_start": pdf,
                                   "book_start": book_of[pdf],
                                   "starts_mid_page": max(idx) > TOP_OF_PAGE_LINES}
                    break
        out[key] = parts
    return out


def _candidates(pages, lo: int, hi: int, kinds) -> dict[int, list[tuple[int, str]]]:
    found: dict[int, list[tuple[int, str]]] = {}
    for pdf in range(lo, hi + 1):
        for line in _nonblank(pages[pdf - 1]):
            m = STATEMENT_RE.match(line)
            if not m:
                continue
            kind = re.sub(r"\s+", " ", m.group(1)).replace("Exarnple", "Example")
            if kind in kinds:
                found.setdefault(_num(m.group(3), m.group(4)), []).append((pdf, kind))
    return found


def _select(found: dict, unit: str, window: tuple[int, int], book_of) -> tuple[list, list]:
    """Pick, for numbers 1..max, the earliest occurrence not before its predecessor."""
    chosen, gaps, last = [], [], window[0]
    for n in range(1, max(found, default=0) + 1):
        opts = sorted(c for c in found.get(n, []) if c[0] >= last)
        if not opts:
            gaps.append({"chapter_or_app": unit, "number": n, "pdf_lo": last})
            continue
        pdf, kind = opts[0]
        chosen.append({"kind": kind, "chapter_or_app": unit, "number": n,
                       "pdf_page": pdf, "book_page": book_of[pdf]})
        last = pdf
    return chosen, gaps


def _close(items: list[dict], gaps: list[dict], end_pdf: int, book_of) -> None:
    for i, it in enumerate(items):
        nxt = items[i + 1]["pdf_page"] if i + 1 < len(items) else end_pdf
        it["pdf_end"], it["book_end"] = nxt, book_of[nxt]
    for g in gaps:
        later = [it["pdf_page"] for it in items if it["number"] > g["number"]]
        hi = min(later) if later else end_pdf
        g.update({"book_lo": book_of[g.pop("pdf_lo")], "book_hi": book_of[hi]})


def detect_statements(pages: list[str], regions: dict, end_matter: dict,
                      book_of: dict[int, int]) -> tuple[dict, list]:
    """Inventory of numbered statements with page windows, plus unresolved gaps."""
    items: dict[str, dict] = {}
    gaps: list[dict] = []
    for key, reg in regions.items():
        if not key.startswith(("chapter_", "appendix_")):
            continue
        unit = key.split("_")[1]
        em = end_matter.get(key, {})
        body_end = em["concluding_remarks"]["pdf_start"] if em.get("concluding_remarks") \
            else reg["pdf_end"]
        windows = [("shared", SHARED_KINDS, reg["pdf_start"], body_end)]
        for part, kind, until in (("mini_projects", ("Mini Project",), "exercises"),
                                  ("exercises", ("Exercise",), None)):
            if em.get(part):
                hi = em[until]["pdf_start"] if until and em.get(until) else reg["pdf_end"]
                windows.append((part, kind, em[part]["pdf_start"], hi))
        for seq, kinds, lo, hi in windows:
            found = _candidates(pages, lo, hi, kinds)
            pdf_of = {b: p for p, b in book_of.items()}
            for (o_unit, o_seq, o_num), (o_kind, o_book) in STATEMENT_OVERRIDES.items():
                if o_unit == unit and o_seq == seq and o_num not in found:
                    found[o_num] = [(pdf_of[o_book], o_kind)]
            chosen, seq_gaps = _select(found, unit, (lo, hi), book_of)
            _close(chosen, seq_gaps, hi, book_of)
            for it in chosen:
                items[f"{it['kind']} {unit}.{it['number']}"] = it
            gaps += [dict(g, sequence=seq) for g in seq_gaps]
    ordered = dict(sorted(items.items(), key=lambda kv: (kv[1]["pdf_page"], kv[0])))
    return ordered, gaps
