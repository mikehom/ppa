#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-001, REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-001, REQ-PRD-PPA-006
# @decision DEC-PPA-007: Artifact-shape and N1/N2/N3/N8 rules reconciled 1:1 with
#   architecture/CONFORMANCE_SPEC.md live in one importable stdlib module shared
#   by validate_ppa_knowledge.py and downstream port conformance verifiers.
"""Artifact-shape and citation rules for knowledge/, ontology/, and corpus/.

Implements CONFORMANCE_SPEC.md normalisation rules N1-N3, N8 (§3.1 inline
citation grammar + fail-closed C1.10/C1.11 checks), C1.9 gotcha-ledger shape
and coverage, C3.1-C3.6 budgets & frontmatter hygiene, C3.10 evals/cases.yaml
shape, C3.12 closed knowledge/ file tree, and C4.1-C4.2 trigger boundaries.
"""
from __future__ import annotations

import re
from pathlib import Path

ROUTER_SKILL = "ppa-program-analysis"
ROUTER_MIN, ROUTER_MAX = 50, 100       # >= min, < max (C3.1)
SKILL_MIN, SKILL_MAX = 250, 500        # >= min, < max (C3.2)
REFERENCE_MAX = 450                    # <= max (C3.3)
AMBIENT_MIN, AMBIENT_MAX = 80, 250     # inclusive (C3.4)
SKILL_NAME_RE = re.compile(r"^ppa-[a-z0-9]+(-[a-z0-9]+)*$")
AMBIENT_NAME_RE = re.compile(r"^ppa-[a-z0-9]+(-[a-z0-9]+)*\.md$")
EVAL_REQUIRED = {"id", "prompt", "expect_skill"}
EVAL_OPTIONAL = {"must_mention", "must_not_mention", "notes"}
NEGATIVE_MARKERS = ("Do not use", "Don't use")

ROMAN_ORDER = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
    "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI",
]
N8_RE = re.compile(
    r"\[PPA\s+([^\],\[]+(?:\[\d{1,3}\])?),\s*"
    r"(?:(p)\.\s*(\d{1,3}|[IVXLCDM]+)|"
    r"(pp)\.\s*(\d{1,3}|[IVXLCDM]+)\s*[–-]\s*(\d{1,3}|[IVXLCDM]+))\]"
)
RAW_PPA_RE = re.compile(r"\[PPA(?![A-Za-z0-9_-])(?:[^\[\]\n]|\[\d{1,3}\])*\]?")
META_PPA_PLACEHOLDERS = ("<", ">", "§X", "p. N", "p. X", "pp. A", "p. <")

LOC_FRONT = {
    "Preface": "preface",
    "Contents": "contents",
    "List of Tables": "list_of_tables",
    "List of Figures": "list_of_figures",
}
LOC_BACK = {
    "Index of Notation": "index_of_notation",
    "Index": "subject_index",
    "Subject Index": "subject_index",
    "Bibliography": "bibliography",
}
END_PART = {
    "Concluding Remarks": "concluding_remarks",
    "Mini Projects": "mini_projects",
    "Exercises": "exercises",
}
LOC_SECTION = re.compile(r"^§?\s*([1-6ABC])\.(\d{1,2})(?:\.\d{1,2})*(?:\s+\S.*)?$")
LOC_CAPTION = re.compile(r"^(Table|Figure)\s+([1-6ABC])\.(\d{1,2})$")
LOC_STATEMENT = re.compile(
    r"^(Lemma|Theorem|Proposition|Corollary|Fact|Example|Exercise|Mini Project)"
    r"\s+([1-6ABC])\.(\d{1,2})$"
)
LOC_REGION = re.compile(
    r"^(?:(?:Chapter|Ch\.?)\s*([1-6])|(?:Appendix|App\.?)\s*([ABC]))"
    r"(?:\s+(Concluding Remarks|Mini Projects|Exercises))?$"
)
LOC_BIB = re.compile(r"^(?:Bibliography\s*)?\[(\d{1,3})\]$")

LEDGER_HEAD = "## Gotcha Ledger"
LEDGER_ENTRY = re.compile(r"^-\s+(G-U\d[ab]?-\d{2,3}):\s+\S")


# --------------------------------------------------------------------------
# Normalisation helpers (N1, N2, N3)
# --------------------------------------------------------------------------

def read_text_strict(path: Path) -> tuple[str | None, str | None]:
    """N1: decode as strict UTF-8 without replacement."""
    try:
        return path.read_bytes().decode("utf-8", errors="strict"), None
    except (OSError, UnicodeDecodeError) as exc:
        return None, str(exc)


def split_lines_n2(text: str) -> list[str]:
    """N2: convert CRLF to LF; split strictly on LF (never FF/VT/CR/U+2028)."""
    norm = text.replace("\r\n", "\n")
    if not norm:
        return []
    parts = norm.split("\n")
    return parts[:-1] if parts[-1] == "" else parts


def read_lines(path: Path) -> list[str]:
    """Strict UTF-8 + N2 line splitting (raises ValueError on N1 violation)."""
    text, err = read_text_strict(path)
    if err is not None or text is None:
        raise ValueError(f"{path}: invalid UTF-8 ({err})")
    return split_lines_n2(text)


def is_fm_delim(line: str, first: bool = False) -> bool:
    """N3: '---' after ignoring leading BOM (line 0) and trailing whitespace."""
    s = line.lstrip("\ufeff") if first else line
    return s.rstrip(" \t\r") == "---"


def parse_frontmatter_strict(lines: list[str]) -> tuple[dict[str, str] | None, str | None]:
    """N3: parse frontmatter; return (meta, err). Duplicate keys & unclosed fail."""
    if not lines or not is_fm_delim(lines[0], first=True):
        return None, None
    out: dict[str, str] = {}
    key: str | None = None
    for idx, line in enumerate(lines[1:], start=2):
        if is_fm_delim(line):
            return {k: v.strip().strip("\"'") for k, v in out.items()}, None
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            if key in out:
                return None, f"line {idx}: duplicate frontmatter key {key!r} (N3)"
            val = m.group(2).strip()
            out[key] = "" if val in {">", "|", ">-", "|-"} else val
        elif key is not None and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
        elif line.strip():
            return None, f"line {idx}: malformed frontmatter line {line!r} (N3)"
    return None, "unterminated YAML frontmatter (N3)"


def parse_frontmatter(lines: list[str]) -> dict[str, str] | None:
    """Backwards-compatible wrapper returning None when absent or invalid."""
    meta, err = parse_frontmatter_strict(lines)
    return None if err else meta


# --------------------------------------------------------------------------
# N8 inline citations (§3.1 + C1.10 + C1.11)
# --------------------------------------------------------------------------

def _resolve_arabic(loc: str, book: int, pm) -> str | None:
    if book not in pm.pdf_of:
        return f"book p. {book} is absent from the PDF (blank page)"
    m = LOC_CAPTION.match(loc)
    if m:
        cap = pm.captions.get(f"{m.group(1)} {m.group(2)}.{m.group(3)}")
        if cap is None:
            return f"unknown {loc!r} (outside the 51-table / 56-figure inventory)"
        return None if abs(cap["book_page"] - book) <= 1 else (
            f"{loc} is on book p. {cap['book_page']}, not {book}")
    m = LOC_BIB.match(loc)
    if m:
        entry = pm.bib.get(m.group(1))
        if entry is None:
            return f"bibliography entry [{m.group(1)}] does not exist"
        return None if entry["book_page"] <= book <= entry["book_page"] + 1 else (
            f"bibliography entry [{m.group(1)}] is on book p. {entry['book_page']}")
    if loc in LOC_BACK:
        return region_error(LOC_BACK[loc], book, pm, loc)
    m = LOC_STATEMENT.match(loc)
    if m:
        key = f"{m.group(1)} {m.group(2)}.{m.group(3)}"
        statements = getattr(pm, "statements", None)
        if statements:
            st = statements.get(key)
            if st is None:
                return f"unknown statement {key!r} (not in page-map statements inventory)"
            return None if st["book_page"] <= book <= st["book_end"] else (
                f"book p. {book} outside {key} (pp. {st['book_page']}–{st['book_end']})")
        unit = m.group(2)
        return region_error(f"chapter_{unit}" if unit.isdigit() else f"appendix_{unit}",
                            book, pm, loc)
    m = LOC_SECTION.match(loc)
    if m:
        sec = pm.sections.get(f"{m.group(1)}.{m.group(2)}")
        if sec is None:
            return f"unknown section {loc!r}"
        return None if sec["book_start"] <= book <= sec["book_end"] else (
            f"book p. {book} outside §{m.group(1)}.{m.group(2)} "
            f"(pp. {sec['book_start']}–{sec['book_end']})")
    m = LOC_REGION.match(loc)
    if m:
        unit = m.group(1) or m.group(2)
        rkey = f"chapter_{unit}" if unit.isdigit() else f"appendix_{unit}"
        part = m.group(3)
        end_matter = getattr(pm, "end_matter", None)
        if part and end_matter is not None:
            em = end_matter.get(rkey, {}).get(END_PART[part])
            if em is None:
                return f"{rkey} has no {part!r} end-matter section"
            return None if em["book_start"] <= book <= em["book_end"] else (
                f"book p. {book} outside {loc} (pp. {em['book_start']}–{em['book_end']})")
        return region_error(rkey, book, pm, loc)
    return f"unrecognised locator {loc!r}"


def resolve_locator(locator: str, page: int | str, pm) -> str | None:
    """Return an error string if (locator, page) fails §3.1 resolution."""
    loc = locator.strip()
    page_str = str(page).strip()
    if loc in LOC_FRONT:
        front_of = getattr(pm, "front_of", {})
        fmap = front_of.get(LOC_FRONT[loc], {})
        if not re.fullmatch(r"[IVXLCDM]+", page_str):
            return f"front-matter locator {loc!r} requires a Roman page label, got {page_str!r}"
        if fmap and page_str not in fmap:
            return f"Roman label {page_str!r} is not in {loc} ({sorted(fmap)})"
        return None
    if not page_str.isdigit():
        return f"locator {loc!r} requires an Arabic book page, got {page_str!r}"
    return _resolve_arabic(loc, int(page_str), pm)


def region_error(key: str, book: int, pm, loc: str) -> str | None:
    reg = pm.regions[key]
    if reg["book_start"] <= book <= reg["book_end"]:
        return None
    return f"book p. {book} outside {loc} (pp. {reg['book_start']}–{reg['book_end']})"


def _page_rank(token: str) -> int | None:
    if token.isdigit():
        return int(token)
    return ROMAN_ORDER.index(token) + 1 if token in ROMAN_ORDER else None


def strip_fences_and_frontmatter(text: str) -> list[tuple[int, str]]:
    """Yield (1-based lineno, line) outside YAML frontmatter and code fences."""
    lines = split_lines_n2(text)
    start = 0
    if lines and is_fm_delim(lines[0], first=True):
        for idx in range(1, len(lines)):
            if is_fm_delim(lines[idx]):
                start = idx + 1
                break
    out: list[tuple[int, str]] = []
    fence: str | None = None
    for idx in range(start, len(lines)):
        line = lines[idx]
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = marker if fence is None else (None if fence == marker else fence)
            continue
        if fence is None:
            out.append((idx + 1, line))
    return out


def _mask_meta_code_spans(line: str) -> str:
    """Blank inline-code spans that illustrate placeholder citation syntax."""
    def repl(m: re.Match[str]) -> str:
        inner = m.group(1)
        if inner.strip() in {"[PPA", "(book p"} or any(p in inner for p in META_PPA_PLACEHOLDERS):
            return " " * len(m.group(0))
        return m.group(0)
    return re.sub(r"`([^`]+)`", repl, line)


def check_n8_citations(text: str, where: str, pm) -> list[str]:
    """Validate all N8 citations and fail closed on malformed '[PPA...' tokens (C1.10)."""
    errs: list[str] = []
    for lineno, raw_line in strip_fences_and_frontmatter(text):
        line = _mask_meta_code_spans(raw_line)
        valid_spans: list[tuple[int, int]] = []
        for m in N8_RE.finditer(line):
            valid_spans.append(m.span())
            loc = m.group(1)
            if m.group(2):
                err = resolve_locator(loc, m.group(3), pm)
                if err:
                    errs.append(f"{where}:{lineno}: '{m.group(0)}' {err}")
            else:
                lo_s, hi_s = m.group(5), m.group(6)
                r_lo, r_hi = _page_rank(lo_s), _page_rank(hi_s)
                if r_lo is None or r_hi is None or r_lo > r_hi or (r_hi - r_lo) > 15:
                    errs.append(f"{where}:{lineno}: '{m.group(0)}' invalid N8 span "
                                f"(requires A <= B and span <= 15)")
                    continue
                for pg in (lo_s, hi_s):
                    err = resolve_locator(loc, pg, pm)
                    if err:
                        errs.append(f"{where}:{lineno}: '{m.group(0)}' {err}")
        for rm in RAW_PPA_RE.finditer(line):
            if not any( a <= rm.start() and rm.end() <= b for a, b in valid_spans):
                errs.append(f"{where}:{lineno}: malformed '[PPA...]' citation token "
                            f"{rm.group(0)!r} (C1.10)")
    return errs


# --------------------------------------------------------------------------
# Skills, ambient files, frontmatter, closed tree (C3.1-C3.6, C3.12, C4.1-C4.2)
# --------------------------------------------------------------------------

def skill_dirs(root: Path) -> list[Path]:
    base = root / "knowledge" / "skills"
    return sorted(p.parent for p in base.glob("*/SKILL.md")) if base.is_dir() else []


def check_skill(skill_dir: Path, siblings: set[str], root: Path) -> list[str]:
    path = skill_dir / "SKILL.md"
    where = path.relative_to(root).as_posix()
    text, uerr = read_text_strict(path)
    if uerr is not None or text is None:
        return [f"{where}: invalid UTF-8 ({uerr}) (N1)"]
    lines = split_lines_n2(text)
    errs: list[str] = []
    if skill_dir.name == ROUTER_SKILL:
        if not ROUTER_MIN <= len(lines) < ROUTER_MAX:
            errs.append(f"{where}: {len(lines)} lines "
                        f"(must be >= {ROUTER_MIN} and < {ROUTER_MAX}, C3.1)")
    elif not SKILL_MIN <= len(lines) < SKILL_MAX:
        errs.append(f"{where}: {len(lines)} lines "
                    f"(must be >= {SKILL_MIN} and < {SKILL_MAX}, C3.2)")
    fm, fm_err = parse_frontmatter_strict(lines)
    if fm_err or fm is None:
        return errs + [f"{where}: {fm_err or 'missing frontmatter'}"]
    if set(fm) != {"name", "description"}:
        errs.append(f"{where}: frontmatter keys must be exactly name, description; "
                    f"got {sorted(fm)} (C3.5)")
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != skill_dir.name:
        errs.append(f"{where}: name {name!r} != directory {skill_dir.name!r} (C3.5)")
    if not SKILL_NAME_RE.match(name) or len(name) > 64:
        errs.append(f"{where}: name {name!r} must match {SKILL_NAME_RE.pattern} (<= 64 chars)")
    if len(desc) > 1024 or N8_RE.search(desc) or re.search(r"(?:^|\s)\d+\.\s+\S", desc):
        errs.append(f"{where}: description violates C2.5 (<= 1024 chars, no N8 citations or numbered lists)")
    if "Use when" not in desc:
        errs.append(f"{where}: description lacks a 'Use when' trigger clause (C4.1)")
    neg = next((desc.index(m) for m in NEGATIVE_MARKERS if m in desc), None)
    if neg is None:
        errs.append(f"{where}: description lacks a 'Do not use'/'Don't use' clause (C4.1)")
    else:
        targets = siblings - {ROUTER_SKILL, name}
        if targets and not any(
            re.search(rf"(?<![A-Za-z0-9-]){re.escape(s)}(?![A-Za-z0-9-])", desc[neg:])
            for s in targets
        ):
            errs.append(f"{where}: negative clause names no non-router sibling on token "
                        f"boundaries (C4.2)")
    return errs


def check_knowledge_tree(root: Path) -> list[str]:
    """C3.12: closed file-tree check under knowledge/."""
    kroot = root / "knowledge"
    if not kroot.is_dir():
        return []
    errs: list[str] = []
    for p in sorted(kroot.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(kroot).parts
        ok = False
        if len(rel) == 2 and rel[0] == "ambient-context" and AMBIENT_NAME_RE.match(rel[1]):
            ok = True
        elif len(rel) >= 3 and rel[0] == "skills" and SKILL_NAME_RE.match(rel[1]):
            tail = rel[2:]
            ok = (tail in {("SKILL.md",), ("README.md",), ("SUGGESTED_FIXES.md",),
                           ("evals", "cases.yaml")}
                  or (len(tail) == 2 and tail[0] == "references"
                      and tail[1].endswith(".md")))
        if not ok:
            errs.append(f"{p.relative_to(root).as_posix()}: unpermitted file in knowledge/ (C3.12)")
    return errs


def check_artifacts(root: Path) -> list[str]:
    """Line ceilings/floors, closed tree, and frontmatter rules for artifacts."""
    dirs = skill_dirs(root)
    names = {d.name for d in dirs}
    errs = check_knowledge_tree(root)
    for d in dirs:
        errs.extend(check_skill(d, names, root))
        for ref in sorted((d / "references").glob("*.md")):
            where = ref.relative_to(root).as_posix()
            text, uerr = read_text_strict(ref)
            if uerr is not None or text is None:
                errs.append(f"{where}: invalid UTF-8 ({uerr}) (N1)")
                continue
            n = len(split_lines_n2(text))
            if n > REFERENCE_MAX:
                errs.append(f"{where}: {n} lines (must be <= {REFERENCE_MAX}, C3.3)")
    ambient = root / "knowledge" / "ambient-context"
    for amb in sorted(ambient.glob("ppa-*.md")) if ambient.is_dir() else []:
        where = amb.relative_to(root).as_posix()
        text, uerr = read_text_strict(amb)
        if uerr is not None or text is None:
            errs.append(f"{where}: invalid UTF-8 ({uerr}) (N1)")
            continue
        n = len(split_lines_n2(text))
        if not AMBIENT_MIN <= n <= AMBIENT_MAX:
            errs.append(f"{where}: {n} lines (must be {AMBIENT_MIN}-{AMBIENT_MAX}, C3.4)")
    errs.extend(check_forbidden_frontmatter(root))
    return errs


def check_forbidden_frontmatter(root: Path) -> list[str]:
    """C3.6 + B7: references, corpus, ontology/*.md, README, fixes, RAW_* carry none."""
    candidates: set[Path] = set()
    for pattern in ("knowledge/skills/*/references/*.md", "corpus/**/*", "ontology/*.md"):
        candidates.update(p for p in root.glob(pattern) if p.is_file() and p.suffix == ".md")
    for p in root.rglob("*.md"):
        rel_parts = p.relative_to(root).parts
        if rel_parts[0] in {"tmp", ".git"}:
            continue
        if p.name in {"README.md", "SUGGESTED_FIXES.md"} or p.name.startswith("RAW_"):
            candidates.add(p)
    errs: list[str] = []
    for p in sorted(candidates):
        where = p.relative_to(root).as_posix()
        text, uerr = read_text_strict(p)
        if uerr is not None or text is None:
            errs.append(f"{where}: invalid UTF-8 ({uerr}) (N1)")
            continue
        lines = split_lines_n2(text)
        if lines and is_fm_delim(lines[0], first=True):
            errs.append(f"{where}: must not carry YAML frontmatter (C3.6)")
    return errs


# --------------------------------------------------------------------------
# evals/cases.yaml (C3.10)
# --------------------------------------------------------------------------

def parse_cases(lines: list[str]) -> list[dict[str, str]]:
    """Parse a YAML list of flat mappings (nested list values are skipped)."""
    cases: list[dict[str, str]] = []
    key_indent: int | None = None
    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\s*)-\s+([A-Za-z_]\w*)\s*:(.*)$", raw)
        if m and (key_indent is None or len(m.group(1)) + 2 <= key_indent):
            key_indent = len(m.group(1)) + 2
            cases.append({m.group(2): m.group(3).strip()})
            continue
        m = re.match(r"^(\s+)([A-Za-z_]\w*)\s*:(.*)$", raw)
        if m and cases and len(m.group(1)) == key_indent:
            cases[-1][m.group(2)] = m.group(3).strip()
    return cases


def check_evals(root: Path) -> list[str]:
    """C3.10: every skill (router included) has a well-formed evals/cases.yaml."""
    errs: list[str] = []
    for d in skill_dirs(root):
        path = d / "evals" / "cases.yaml"
        where = path.relative_to(root).as_posix()
        if not path.is_file():
            errs.append(f"{where}: missing (C3.10)")
            continue
        text, uerr = read_text_strict(path)
        if uerr is not None or text is None:
            errs.append(f"{where}: invalid UTF-8 ({uerr}) (N1)")
            continue
        cases = parse_cases(split_lines_n2(text))
        if not cases:
            errs.append(f"{where}: no cases found")
        for idx, case in enumerate(cases):
            missing = sorted(k for k in EVAL_REQUIRED if not case.get(k))
            unknown = sorted(set(case) - EVAL_REQUIRED - EVAL_OPTIONAL)
            if missing:
                errs.append(f"{where}: case {idx} missing {missing}")
            if unknown:
                errs.append(f"{where}: case {idx} has unknown keys {unknown}")
    return errs


# --------------------------------------------------------------------------
# Gotcha ledger (C1.9 shape + downstream reference coverage)
# --------------------------------------------------------------------------

def collect_gotcha_ledgers(root: Path) -> tuple[list[str], int, dict[str, str]]:
    """Validate RAW_SHARD_*.md ledgers; return (errors, shard_count, id->file)."""
    errs: list[str] = []
    seen: dict[str, str] = {}
    shards = sorted((root / "corpus" / "shards").glob("RAW_SHARD_*.md"))
    for path in shards:
        where = path.relative_to(root).as_posix()
        text, uerr = read_text_strict(path)
        if uerr is not None or text is None:
            errs.append(f"{where}: invalid UTF-8 ({uerr}) (N1)")
            continue
        lines = split_lines_n2(text)
        heads = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
        if not heads or lines[heads[-1]].strip() != LEDGER_HEAD:
            errs.append(f"{where}: last level-2 section must be '{LEDGER_HEAD}' (C1.9)")
            continue
        tail = lines[heads[-1] + 1:]
        for extra in tail:
            if extra.strip() and not extra.startswith("- "):
                errs.append(f"{where}: non-bullet line in gotcha ledger {extra[:60]!r} (C1.9)")
        entries = [ln for ln in tail if ln.startswith("- ")]
        if not entries:
            errs.append(f"{where}: gotcha ledger is empty")
        for entry in entries:
            m = LEDGER_ENTRY.match(entry)
            if not m:
                errs.append(f"{where}: malformed ledger entry {entry[:60]!r}")
                continue
            if not N8_RE.search(entry):
                errs.append(f"{where}: ledger entry {m.group(1)} lacks an N8 citation")
            if m.group(1) in seen:
                errs.append(f"{where}: ledger id {m.group(1)} duplicates {seen[m.group(1)]}")
            seen[m.group(1)] = where
    return errs, len(shards), seen


def check_gotcha_ledgers(root: Path) -> tuple[list[str], int]:
    """Backwards-compatible shape-only tuple for existing callers."""
    errs, count, _ = collect_gotcha_ledgers(root)
    return errs, count


def check_gotcha_coverage(root: Path, ledger_ids: dict[str, str]) -> list[str]:
    """C1.9: check whether every G-U* id is referenced in knowledge/, ontology/, or issues/."""
    if not ledger_ids:
        return []
    haystack_parts: list[str] = []
    for sub in ("knowledge", "ontology", "issues/backlog", "issues/refactors"):
        base = root / sub
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file() and p.suffix in {".md", ".json", ".yaml"}:
                txt, err = read_text_strict(p)
                if err is None and txt is not None:
                    haystack_parts.append(txt)
    present = set(re.findall(r"\bG-U\d[ab]?-\d{2,3}\b", "\n".join(haystack_parts)))
    return [f"{src}: ledger id {gid} not yet referenced in derived artifacts/issues (C1.9)"
            for gid, src in sorted(ledger_ids.items()) if gid not in present]
