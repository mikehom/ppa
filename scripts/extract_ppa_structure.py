#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001
# @decision DEC-PPA-004: Dynamic (pdf_page, book_page) coordinate map derived
#   from running-header page numbers, validated against independent inventories.
"""Build corpus/pdf_page_map.json and per-unit text slices from ppa.pdf.

Usage:
    python3 -B scripts/extract_ppa_structure.py [--pdf ppa.pdf]
        [--text tmp/full_book.txt] [--map corpus/pdf_page_map.json]
        [--slices tmp/slices] [--reuse-text]
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ppa_structure_extras as extras  # noqa: E402  pylint: disable=wrong-import-position
from ppa_structure_extras import TOP_OF_PAGE_LINES  # noqa: E402

LOG = logging.getLogger("extract_ppa_structure")

TOTAL_PDF_PAGES = 465
LAST_BOOK_PAGE = 452
FIRST_ARABIC_PDF = 21

# Independent inventories transcribed from the book's List of Tables / Figures.
TABLE_COUNTS = {"1": 6, "2": 10, "3": 10, "5": 18, "6": 6, "C": 1}
FIGURE_COUNTS = {"1": 3, "2": 23, "3": 6, "4": 10, "5": 2, "6": 6, "A": 3, "C": 3}
BIB_ENTRIES = 185

# Canonical top-level section titles (Table of Contents); OCR titles are noisy.
SECTION_TITLES = {
    "1.1": "The Nature of Program Analysis", "1.2": "Setting the Scene",
    "1.3": "Data Flow Analysis", "1.4": "Constraint Based Analysis",
    "1.5": "Abstract Interpretation", "1.6": "Type and Effect Systems",
    "1.7": "Algorithms", "1.8": "Transformations",
    "2.1": "Intraprocedural Analysis", "2.2": "Theoretical Properties",
    "2.3": "Monotone Frameworks", "2.4": "Equation Solving",
    "2.5": "Interprocedural Analysis", "2.6": "Shape Analysis",
    "3.1": "Abstract 0-CFA Analysis", "3.2": "Theoretical Properties",
    "3.3": "Syntax Directed 0-CFA Analysis", "3.4": "Constraint Based 0-CFA Analysis",
    "3.5": "Adding Data Flow Analysis", "3.6": "Adding Context Information",
    "4.1": "A Mundane Approach to Correctness", "4.2": "Approximation of Fixed Points",
    "4.3": "Galois Connections", "4.4": "Systematic Design of Galois Connections",
    "4.5": "Induced Operations",
    "5.1": "Control Flow Analysis", "5.2": "Theoretical Properties",
    "5.3": "Inference Algorithms", "5.4": "Effects", "5.5": "Behaviours",
    "6.1": "Worklist Algorithms", "6.2": "Iterating in Reverse Postorder",
    "6.3": "Iterating Through Strong Components",
    "A.1": "Basic Definitions", "A.2": "Construction of Complete Lattices",
    "A.3": "Chains", "A.4": "Fixed Points",
    "B.1": "Proof by Induction", "B.2": "Introducing Coinduction",
    "B.3": "Proof by Coinduction",
    "C.1": "Graphs and Forests", "C.2": "Reverse Postorder",
    "C.3": "Regular Expressions",
}

FRONT_MATTER = [
    ("cover", 1, 1), ("title", 2, 4), ("preface", 5, 10),
    ("contents", 11, 15), ("list_of_tables", 16, 17), ("list_of_figures", 18, 20),
]
ROMAN = ["V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV",
         "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"]

OPENERS = [
    (re.compile(r"^Chapter\s+([1-6])$"), "chapter_{0}"),
    (re.compile(r"^Appendix\s+([ABC])$"), "appendix_{0}"),
    (re.compile(r"^Index\s+of\s+N\s*otation$"), "index_of_notation"),
    (re.compile(r"^Index$"), "subject_index"),
    (re.compile(r"^Bibliography$"), "bibliography"),
]

UNIT_SLICES = [
    ("U0_appendices_notation.txt", [(393, 432)]),
    ("U1_ch1.txt", [(1, 34)]),
    ("U2a_ch2_s1_4.txt", [(35, 81)]),
    ("U2b_ch2_s5_6.txt", [(82, 140)]),
    ("U3a_ch3_s1_4.txt", [(141, 181)]),
    ("U3b_ch3_s5_6.txt", [(182, 210)]),
    ("U4a_ch4_s1_3.txt", [(211, 245)]),
    ("U4b_ch4_s4_5.txt", [(246, 282)]),
    ("U5a_ch5_s1_3.txt", [(283, 318)]),
    ("U5b_ch5_s4_5.txt", [(319, 364)]),
    ("U6_ch6_index_bib.txt", [(365, 392), (433, 452)]),
]

CAPTION_RE = re.compile(
    r"^\s*(Table|Figure)\s+([0-9AC])\s*[.,o]\s*([0-9lI]{1,2})\s*:", re.M)
SECTION_RE = re.compile(
    r"^([1-6ABC])\s*[.]\s*([0-9lI])\s+([A-Zl][A-Za-z0-9 ,'-]{2,60})$")
NUM_LINE_RE = re.compile(r"^\d{1,3}$")
SECTION_NUM_RE = re.compile(r"^[1-6ABC]\s*[.]\s*[0-9lI]$")
RUNNING_HEADER_RE = re.compile(  # e.g. "3 Constraint Based Analysis"
    r"^(?:[1-6]\s+[A-Z]|[ABC]\s+(?:Partially|[Il]nd|Graphs))")
BIB_RE = re.compile(r"^\[(\d{1,3})[\])]")  # OCR renders some ']' as ')'


def fix_digits(token: str) -> str:
    """Map common OCR confusions (l, I) back to the digit 1."""
    return token.replace("l", "1").replace("I", "1")


def run_pdftotext(pdf: Path, out_txt: Path, reuse: bool) -> None:
    """Extract the full book text with a single pdftotext invocation."""
    if reuse and out_txt.exists():
        LOG.info("reusing existing text %s", out_txt)
        return
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["pdftotext", str(pdf), str(out_txt)],
                          capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"pdftotext failed ({proc.returncode}): {proc.stderr}")


def split_pages(text: str) -> list[str]:
    """Split on form feeds; drop the empty chunk after the final form feed."""
    pages = text.split("\x0c")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    if len(pages) != TOTAL_PDF_PAGES:
        raise ValueError(f"expected {TOTAL_PDF_PAGES} pages, got {len(pages)}")
    return pages


def nonblank(page: str) -> list[str]:
    return [ln.strip() for ln in page.splitlines() if ln.strip()]


def detect_offsets(pages: list[str]) -> dict[int, int | None]:
    """Map pdf_page -> detected offset (pdf - book) from header/footer numbers."""
    detected: dict[int, int | None] = {}
    for pdf in range(FIRST_ARABIC_PDF, TOTAL_PDF_PAGES + 1):
        lines = nonblank(pages[pdf - 1])
        cands = [int(x) for x in lines[:2] + lines[-1:] if NUM_LINE_RE.match(x)]
        offs = {pdf - c for c in cands
                if 0 < c <= LAST_BOOK_PAGE and 0 <= pdf - c <= FIRST_ARABIC_PDF}
        detected[pdf] = offs.pop() if len(offs) == 1 else None
    return detected


def assign_offsets(detected: dict[int, int | None],
                   openers: set[int]) -> tuple[dict[int, int], dict]:
    """Corroborate, fill and monotonicity-check the detected offsets.

    A detected offset is trusted only when another detected page within three
    PDF pages agrees. Untrusted/undetected region-opener pages inherit the next
    trusted offset (blank versos are dropped *before* openers); all other
    untrusted pages inherit the previous trusted offset. Since printed pages
    are only ever dropped from the PDF, the offset must be non-increasing; a
    violation raises.
    """
    pdfs = sorted(detected)
    trusted: dict[int, int | None] = {}
    for pdf in pdfs:
        off = detected[pdf]
        peers = [detected.get(p) for p in range(pdf - 3, pdf + 4) if p != pdf]
        trusted[pdf] = off if off is not None and off in peers else None
    nxt_of: dict[int, int | None] = {}
    nxt: int | None = None
    for pdf in reversed(pdfs):
        nxt = trusted[pdf] if trusted[pdf] is not None else nxt
        nxt_of[pdf] = nxt
    assigned: dict[int, int] = {}
    prev: int | None = None
    for pdf in pdfs:
        if trusted[pdf] is not None:
            off = trusted[pdf]
        elif pdf in openers or prev is None:
            off = nxt_of[pdf]
        else:
            off = prev
        if off is None:
            raise ValueError(f"no offset anchor for pdf page {pdf}")
        if prev is not None and off > prev:
            raise ValueError(f"offset increases at pdf page {pdf}")
        assigned[pdf] = prev = off
    stats = {
        "header_detected": sum(1 for v in detected.values() if v is not None),
        "corroborated": sum(1 for v in trusted.values() if v is not None),
        "inferred": sum(1 for v in trusted.values() if v is None),
        "detected_conflicts": sorted(p for p in pdfs if detected[p] is not None
                                     and detected[p] != assigned[p]),
    }
    return assigned, stats


REGION_TITLES = {
    "chapter_1": "Introduction", "chapter_2": "Data Flow Analysis",
    "chapter_3": "Constraint Based Analysis", "chapter_4": "Abstract Interpretation",
    "chapter_5": "Type and Effect Systems", "chapter_6": "Algorithms",
    "appendix_A": "Partially Ordered Sets", "appendix_B": "Induction and Coinduction",
    "appendix_C": "Graphs and Regular Expressions",
    "index_of_notation": "Index of Notation", "subject_index": "Index",
    "bibliography": "Bibliography",
}


def find_openers(pages: list[str]) -> dict[str, int]:
    """Locate chapter/appendix/back-matter opener pages (first match wins)."""
    starts: dict[str, int] = {}
    for pdf in range(FIRST_ARABIC_PDF, TOTAL_PDF_PAGES + 1):
        lines = nonblank(pages[pdf - 1])
        if not lines:
            continue
        for pat, tmpl in OPENERS:
            m = pat.match(lines[0])
            if m:
                key = tmpl.format(*m.groups())
                starts.setdefault(key, pdf)
    missing = sorted(set(REGION_TITLES) - set(starts))
    if missing:
        raise ValueError(f"region openers not found: {missing}")
    return starts


def build_regions(starts: dict[str, int], book_of: dict[int, int]) -> dict[str, dict]:
    """Turn opener pages into contiguous PDF and book page ranges."""
    order = sorted(starts.items(), key=lambda kv: kv[1])
    regions: dict[str, dict] = {}
    for i, (key, pdf_start) in enumerate(order):
        pdf_end = order[i + 1][1] - 1 if i + 1 < len(order) else TOTAL_PDF_PAGES
        book_end = (book_of[order[i + 1][1]] - 1 if i + 1 < len(order)
                    else book_of[TOTAL_PDF_PAGES])
        regions[key] = {
            "title": REGION_TITLES[key], "pdf_start": pdf_start, "pdf_end": pdf_end,
            "book_start": book_of[pdf_start], "book_end": book_end,
        }
    return regions


def region_of(pdf: int, regions: dict[str, dict]) -> str:
    for name, lo, hi in FRONT_MATTER:
        if lo <= pdf <= hi:
            return name
    for key, reg in regions.items():
        if reg["pdf_start"] <= pdf <= reg["pdf_end"]:
            return key
    raise ValueError(f"pdf page {pdf} not covered by any region")


def front_labels(pages: list[str]) -> dict[int, str | None]:
    """Roman page labels for front matter (detected, then back-filled)."""
    labels: dict[int, str | None] = {p: None for p in range(1, FIRST_ARABIC_PDF)}
    for pdf in range(5, FIRST_ARABIC_PDF):
        lines = nonblank(pages[pdf - 1])
        hits = [x for x in lines[:2] + lines[-1:] if x in ROMAN]
        labels[pdf] = hits[0] if hits else None
    for pdf in range(FIRST_ARABIC_PDF - 1, 4, -1):
        nxt = labels.get(pdf + 1)
        if labels[pdf] is None and nxt in ROMAN and ROMAN.index(nxt) > 0:
            labels[pdf] = ROMAN[ROMAN.index(nxt) - 1]
    return labels


def heading_candidates(lines: list[str]) -> list[tuple[int, str]]:
    """(line index, text) of lines past the first header line that may be 'N.M Title'.

    pdftotext usually emits a heading as a bare number line followed by the
    title, sometimes with a page number or OCR debris (<= 4 chars) in between;
    such sequences are joined. Lines ending in '.' are excluded.
    """
    out: list[tuple[int, str]] = []
    for i in range(1, len(lines)):
        line = lines[i]
        if SECTION_NUM_RE.match(line):
            out.extend((i, f"{line} {nxt}") for nxt in lines[i + 1:i + 9]
                       if len(nxt) > 4 and not NUM_LINE_RE.match(nxt)
                       and not RUNNING_HEADER_RE.match(nxt) and not nxt.endswith("."))
        elif not line.endswith("."):
            out.append((i, line))
    return out


def title_matches(ocr: str, canonical: str, threshold: float = 0.85) -> bool:
    """Fuzzy title match tolerant of OCR spacing/letter noise."""
    def norm(s: str) -> str:
        return re.sub(r"[^a-z0-9]", "", s.lower().replace("l", "i"))
    return SequenceMatcher(None, norm(ocr), norm(canonical)).ratio() >= threshold


def detect_sections(pages: list[str], regions: dict[str, dict],
                    book_of: dict[int, int]) -> dict[str, dict]:
    """First body occurrence of each 'N.M Title' heading inside its region."""
    sections: dict[str, dict] = {}
    for key, reg in regions.items():
        if not key.startswith(("chapter_", "appendix_")):
            continue
        unit = key.split("_")[1]
        last_start = reg["pdf_start"]
        for pdf in range(reg["pdf_start"], reg["pdf_end"] + 1):
            cands = heading_candidates(nonblank(pages[pdf - 1]))
            for idx, line in cands:
                m = SECTION_RE.match(line)
                if not m or m.group(1) != unit:
                    continue
                sid = f"{unit}.{fix_digits(m.group(2))}"
                if (sid in sections or sid not in SECTION_TITLES or pdf < last_start
                        or not title_matches(m.group(3), SECTION_TITLES[sid])):
                    continue
                # Odd-page running headers repeat the section title; the body
                # heading is the deepest matching line on the page.
                deepest = max(i for i, ln in cands if (mm := SECTION_RE.match(ln))
                              and f"{mm.group(1)}.{fix_digits(mm.group(2))}" == sid)
                sections[sid] = {"title": SECTION_TITLES[sid],
                                 "title_ocr": m.group(3).strip(), "region": key,
                                 "pdf_start": pdf, "book_start": book_of[pdf],
                                 "starts_mid_page": deepest > TOP_OF_PAGE_LINES}
                last_start = pdf
    missing = sorted(set(SECTION_TITLES) - set(sections))
    if missing:
        raise ValueError(f"section headings not found: {missing}")
    return dict(sorted(sections.items(), key=lambda kv: kv[1]["pdf_start"]))


def close_ranges(items: list[dict], region_end: tuple[int, int]) -> None:
    """Set book_end/pdf_end/shares_last_page for consecutive items in one region.

    An item ends on the page where the next item's heading appears if that
    heading starts mid-page (the page is shared), otherwise on the page before.
    """
    for i, item in enumerate(items):
        nxt = items[i + 1] if i + 1 < len(items) else None
        if nxt is None:
            item["pdf_end"], item["book_end"] = region_end
            item["shares_last_page"] = False
            continue
        shared = nxt["starts_mid_page"]
        item["pdf_end"] = max(item["pdf_start"], nxt["pdf_start"] - (0 if shared else 1))
        item["book_end"] = max(item["book_start"], nxt["book_start"] - (0 if shared else 1))
        item["shares_last_page"] = shared


def detect_captions(pages: list[str], book_of: dict[int, int]) -> dict[str, dict]:
    """Locate numbered Table/Figure captions and check them against inventory."""
    found: dict[str, dict] = {}
    for pdf in range(FIRST_ARABIC_PDF, TOTAL_PDF_PAGES + 1):
        for m in CAPTION_RE.finditer(pages[pdf - 1]):
            kind, unit, num = m.group(1), m.group(2), int(fix_digits(m.group(3)))
            key = f"{kind} {unit}.{num}"
            found.setdefault(key, {"kind": kind.lower(), "chapter_or_app": unit,
                                   "number": num, "pdf_page": pdf,
                                   "book_page": book_of[pdf]})
    for kind, inventory in (("Table", TABLE_COUNTS), ("Figure", FIGURE_COUNTS)):
        expected = {f"{kind} {u}.{n}" for u, c in inventory.items()
                    for n in range(1, c + 1)}
        got = {k for k in found if k.startswith(kind)}
        if expected != got:
            raise ValueError(f"{kind} inventory mismatch: missing="
                             f"{sorted(expected - got)} extra={sorted(got - expected)}")
    return dict(sorted(found.items(), key=lambda kv: (kv[1]["pdf_page"], kv[0])))


def detect_bibliography(pages: list[str], region: dict,
                        book_of: dict[int, int]) -> dict[str, dict]:
    """Locate bibliography entries [1]..[185] (first page of each entry)."""
    entries: dict[str, dict] = {}
    for pdf in range(region["pdf_start"], region["pdf_end"] + 1):
        for line in nonblank(pages[pdf - 1]):
            m = BIB_RE.match(line)
            if m and 1 <= int(m.group(1)) <= BIB_ENTRIES:
                entries.setdefault(m.group(1), {"pdf_page": pdf,
                                                "book_page": book_of[pdf]})
    missing = [n for n in range(1, BIB_ENTRIES + 1) if str(n) not in entries]
    if missing:
        raise ValueError(f"bibliography entries missing: {missing}")
    return dict(sorted(entries.items(), key=lambda kv: int(kv[0])))


def offset_runs(book_of: dict[int, int]) -> list[dict]:
    """Compress the arabic mapping into constant-offset runs."""
    runs: list[dict] = []
    for pdf in sorted(book_of):
        off = pdf - book_of[pdf]
        if runs and runs[-1]["offset"] == off and runs[-1]["pdf_end"] == pdf - 1:
            runs[-1]["pdf_end"], runs[-1]["book_end"] = pdf, book_of[pdf]
        else:
            runs.append({"offset": off, "pdf_start": pdf, "pdf_end": pdf,
                         "book_start": book_of[pdf], "book_end": book_of[pdf]})
    return runs


def clean_page(page: str) -> str:
    """Strip trailing whitespace and collapse runs of blank lines."""
    out: list[str] = []
    for line in page.splitlines():
        line = line.rstrip()
        if not line and (not out or not out[-1]):
            continue
        out.append(line)
    return "\n".join(out).strip("\n")


def write_slices(pages: list[str], book_of: dict[int, int], out_dir: Path) -> dict:
    """Write per-unit slices with [PDF_PAGE=X | BOOK_PAGE=Y] page headers."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_of = {b: p for p, b in book_of.items()}
    stats: dict[str, dict] = {}
    for fname, ranges in UNIT_SLICES:
        chunks: list[str] = []
        pdf_pages: list[int] = []
        absent: list[int] = []
        for lo, hi in ranges:
            for book in range(lo, hi + 1):
                pdf = pdf_of.get(book)
                if pdf is None:
                    absent.append(book)
                    continue
                pdf_pages.append(pdf)
                chunks.append(f"[PDF_PAGE={pdf} | BOOK_PAGE={book}]\n"
                              f"{clean_page(pages[pdf - 1])}\n")
        body = "\n".join(chunks)
        (out_dir / fname).write_text(body, encoding="utf-8")
        stats[fname] = {"book_ranges": [list(r) for r in ranges],
                        "pdf_pages": len(pdf_pages),
                        "pdf_first": min(pdf_pages), "pdf_last": max(pdf_pages),
                        "book_pages_absent_from_pdf": absent,
                        "lines": body.count("\n"), "bytes": len(body.encode())}
    return stats


def build_map(pages: list[str]) -> tuple[dict, dict[int, int]]:
    """Assemble the full coordinate map from extracted page text."""
    detected = detect_offsets(pages)
    openers = find_openers(pages)
    offsets, stats = assign_offsets(detected, set(openers.values()))
    book_of = {pdf: pdf - off for pdf, off in offsets.items()}
    if book_of[FIRST_ARABIC_PDF] != 1 or book_of[TOTAL_PDF_PAGES] != LAST_BOOK_PAGE:
        raise ValueError("anchor check failed: book p.1 must be PDF 21 and "
                         "book p.452 must be PDF 465")
    regions = build_regions(openers, book_of)
    labels = front_labels(pages)
    page_rows = []
    for pdf in range(1, TOTAL_PDF_PAGES + 1):
        book = book_of.get(pdf)
        basis = ("front_matter" if book is None else
                 "header" if detected.get(pdf) == offsets.get(pdf) else "inferred")
        page_rows.append({"pdf_page": pdf, "book_page": book,
                          "label": str(book) if book else labels.get(pdf),
                          "region": region_of(pdf, regions), "basis": basis})
    present = set(book_of.values())
    captions = detect_captions(pages, book_of)
    sections = detect_sections(pages, regions, book_of)
    end_matter = extras.detect_end_matter(pages, regions, sections, book_of)
    rank = {name: i for i, (name, _) in enumerate(extras.END_MATTER, start=1)}
    for key, reg in regions.items():
        parts = end_matter.get(key, {})
        items = sorted([(s["pdf_start"], 0, s) for s in sections.values()
                        if s["region"] == key] +
                       [(p["pdf_start"], rank[n], p) for n, p in parts.items()],
                       key=lambda t: (t[0], t[1]))
        close_ranges([it for _, _, it in items], (reg["pdf_end"], reg["book_end"]))
    statements, gaps = extras.detect_statements(pages, regions, end_matter, book_of)
    if gaps:
        raise ValueError(f"unresolved statement gaps: {gaps}")
    doc = {
        "schema_version": 1,
        "source": {
            "file": "ppa.pdf",
            "title": "Principles of Program Analysis",
            "authors": ["Flemming Nielson", "Hanne Riis Nielson", "Chris Hankin"],
            "publisher": "Springer", "edition": "Corrected 2nd printing, 2005",
            "total_pdf_pages": TOTAL_PDF_PAGES, "total_book_pages": LAST_BOOK_PAGE,
        },
        "extraction_stats": stats,
        "book_pages_absent_from_pdf": [b for b in range(1, LAST_BOOK_PAGE + 1)
                                       if b not in present],
        "offset_runs": offset_runs(book_of),
        "front_matter": [{"name": n, "pdf_start": lo, "pdf_end": hi}
                         for n, lo, hi in FRONT_MATTER],
        "regions": regions,
        "sections": sections,
        "end_matter": end_matter,
        "statements": statements,
        "statement_gaps": gaps,
        "tables": {k: v for k, v in captions.items() if v["kind"] == "table"},
        "figures": {k: v for k, v in captions.items() if v["kind"] == "figure"},
        "bibliography_entries": detect_bibliography(pages, regions["bibliography"],
                                                    book_of),
        "pages": page_rows,
    }
    doc["counts"] = {"tables": len(doc["tables"]), "figures": len(doc["figures"]),
                     "bibliography_entries": len(doc["bibliography_entries"]),
                     "sections": len(doc["sections"]), "statements": len(statements),
                     "statement_gaps": len(gaps)}
    return doc, book_of


def parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pdf", default="ppa.pdf")
    ap.add_argument("--text", default="tmp/full_book.txt")
    ap.add_argument("--map", default="corpus/pdf_page_map.json")
    ap.add_argument("--slices", default="tmp/slices")
    ap.add_argument("--reuse-text", action="store_true",
                    help="reuse an existing --text file instead of re-running pdftotext")
    return ap.parse_args(argv)


def main(argv: list[str]) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args(argv)
    try:
        run_pdftotext(Path(args.pdf), Path(args.text), args.reuse_text)
        pages = split_pages(Path(args.text).read_text(encoding="utf-8",
                                                      errors="replace"))
        doc, book_of = build_map(pages)
        doc["unit_slices"] = write_slices(pages, book_of, Path(args.slices))
    except (RuntimeError, ValueError, OSError) as exc:
        LOG.error("extraction failed: %s", exc)
        return 1
    out = Path(args.map)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    LOG.info("wrote %s: counts=%s runs=%d", out, doc["counts"], len(doc["offset_runs"]))
    LOG.info("absent book pages: %s", doc["book_pages_absent_from_pdf"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
