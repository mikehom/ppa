---
id: ISS-W6-01
title: "W6-1 Unit 6: Ch 6 worklist, RPO, round-robin, SCC solvers + Gate #9"
issue_type: shard
status: open
priority: P0
labels: [ppa, wave-6, gate]
milestone: W6
parent_issue: EPIC-001
depends_on: [ISS-W5-03]
blocks: [ISS-W6-02]
ppa_scope: ["§6.1 Worklist Algorithms (book pp. 365–373; PDF pp. 381–389)", "§6.2 Iterating in Reverse Postorder (book pp. 374–380; PDF pp. 390–396)", "§6.3 Iterating Through Strong Components (book pp. 381–392; PDF pp. 397–408)", "Subject Index (book pp. 433–438; PDF pp. 447–451)", "Bibliography [1]–[185] (book pp. 439–452; PDF pp. 452–465)"]
altitudes: [L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Extract worklist algorithms and iteration orders, subject index and bibliography; synthesize the solver skill; Gate #9.

## Source Citations & Grounding

- §6.1 Worklist Algorithms (book pp. 365–373; PDF pp. 381–389)
- §6.2 Iterating in Reverse Postorder (book pp. 374–380; PDF pp. 390–396)
- §6.3 Iterating Through Strong Components (book pp. 381–392; PDF pp. 397–408)
- Subject Index (book pp. 433–438; PDF pp. 447–451)
- Bibliography [1]–[185] (book pp. 439–452; PDF pp. 452–465)
- Tables in scope: Table 6.1 (p. 369/PDF 385), Table 6.2 (p. 373/PDF 389), Table 6.3 (p. 376/PDF 392), Table 6.4 (p. 379/PDF 395), Table 6.5 (p. 382/PDF 398), Table 6.6 (p. 384/PDF 400), Table C.1 (p. 421/PDF 436)
- Figures in scope: Figure 6.1 (p. 374/PDF 390), Figure 6.2 (p. 376/PDF 392), Figure 6.3 (p. 377/PDF 393), Figure 6.4 (p. 379/PDF 395), Figure 6.5 (p. 382/PDF 398), Figure 6.6 (p. 384/PDF 400), Figure A.1 (p. 394/PDF 410), Figure A.2 (p. 400/PDF 416), Figure A.3 (p. 403/PDF 419), Figure C.1 (p. 422/PDF 437), Figure C.2 (p. 423/PDF 438), Figure C.3 (p. 425/PDF 440)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 365–452 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [ ] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [ ] All 7 tables and 12 figures in book pp. 365–452 are anchored (no omissions)
- [ ] Artifact `corpus/shards/RAW_SHARD_06_algorithms_bib.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `knowledge/skills/ppa-fixedpoint-solvers/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `knowledge/skills/ppa-fixedpoint-solvers/references/ppa-fixedpoint-solvers.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W5-03; blocks: ISS-W6-02
- `corpus/shards/RAW_SHARD_06_algorithms_bib.md`
- `knowledge/skills/ppa-fixedpoint-solvers/SKILL.md`
- `knowledge/skills/ppa-fixedpoint-solvers/references/ppa-fixedpoint-solvers.md`

## Verification Receipts

_Pending._
