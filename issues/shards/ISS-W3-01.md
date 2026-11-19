---
id: ISS-W3-01
title: "W3-1 Ch 3a §3.1–3.4 0-CFA formulations, coinduction and cubic solver"
issue_type: shard
status: open
priority: P0
labels: [ppa, wave-3]
milestone: W3
parent_issue: EPIC-001
depends_on: [ISS-W2-04]
blocks: [ISS-W3-02]
ppa_scope: ["§3.1 Abstract 0-CFA Analysis (book pp. 141–152; PDF pp. 159–170)", "§3.2 Theoretical Properties (book pp. 153–167; PDF pp. 171–185)", "§3.3 Syntax Directed 0-CFA Analysis (book pp. 168–172; PDF pp. 186–190)", "§3.4 Constraint Based 0-CFA Analysis (book pp. 173–181; PDF pp. 191–199)"]
altitudes: [L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Extract abstract, syntax-directed and constraint-based 0-CFA, semantic correctness, Moore-family existence of solutions, and the O(n^3) constraint solver.

## Source Citations & Grounding

- §3.1 Abstract 0-CFA Analysis (book pp. 141–152; PDF pp. 159–170)
- §3.2 Theoretical Properties (book pp. 153–167; PDF pp. 171–185)
- §3.3 Syntax Directed 0-CFA Analysis (book pp. 168–172; PDF pp. 186–190)
- §3.4 Constraint Based 0-CFA Analysis (book pp. 173–181; PDF pp. 191–199)
- Tables in scope: Table 3.1 (p. 146/PDF 164), Table 3.2 (p. 155/PDF 173), Table 3.3 (p. 156/PDF 174), Table 3.4 (p. 158/PDF 176), Table 3.5 (p. 170/PDF 188), Table 3.6 (p. 174/PDF 192), Table 3.7 (p. 178/PDF 196)
- Figures in scope: Figure 3.1 (p. 148/PDF 166), Figure 3.2 (p. 149/PDF 167), Figure 3.3 (p. 159/PDF 177), Figure 3.4 (p. 179/PDF 197), Figure 3.5 (p. 180/PDF 198)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 141–181 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [ ] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [ ] All 7 tables and 5 figures in book pp. 141–181 are anchored (no omissions)
- [ ] Artifact `corpus/shards/RAW_SHARD_03a_0cfa.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W2-04; blocks: ISS-W3-02
- `corpus/shards/RAW_SHARD_03a_0cfa.md`

## Verification Receipts

_Pending._
