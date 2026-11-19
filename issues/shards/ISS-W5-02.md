---
id: ISS-W5-02
title: "W5-2 Ch 5b §5.4–5.5 effects, exceptions, regions, behaviours + Gate #7"
issue_type: shard
status: open
priority: P0
labels: [ppa, wave-5, gate]
milestone: W5
parent_issue: EPIC-001
depends_on: [ISS-W5-01]
blocks: [ISS-W5-03]
ppa_scope: ["§5.4 Effects (book pp. 319–338; PDF pp. 336–355)", "§5.5 Behaviours (book pp. 339–364; PDF pp. 356–380)"]
altitudes: [L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Extract side-effect, exception, region-inference and communication analyses; synthesize the Chapter 5 skill; refactor; Gate #7.

## Source Citations & Grounding

- §5.4 Effects (book pp. 319–338; PDF pp. 336–355)
- §5.5 Behaviours (book pp. 339–364; PDF pp. 356–380)
- Tables in scope: Table 5.9 (p. 322/PDF 339), Table 5.10 (p. 328/PDF 345), Table 5.11 (p. 334/PDF 351), Table 5.12 (p. 337/PDF 354), Table 5.13 (p. 338/PDF 355), Table 5.14 (p. 341/PDF 358), Table 5.15 (p. 343/PDF 360), Table 5.16 (p. 346/PDF 363), Table 5.17 (p. 347/PDF 364), Table 5.18 (p. 348/PDF 365)
- Figures in scope: Figure 5.1 (p. 331/PDF 348), Figure 5.2 (p. 340/PDF 357)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 319–364 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [ ] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [ ] All 10 tables and 2 figures in book pp. 319–364 are anchored (no omissions)
- [ ] Artifact `knowledge/skills/ppa-types-effects-and-regions/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `knowledge/skills/ppa-types-effects-and-regions/references/ppa-types-effects-and-regions.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W5-01; blocks: ISS-W5-03
- `knowledge/skills/ppa-types-effects-and-regions/SKILL.md`
- `knowledge/skills/ppa-types-effects-and-regions/references/ppa-types-effects-and-regions.md`

## Verification Receipts

_Pending._
