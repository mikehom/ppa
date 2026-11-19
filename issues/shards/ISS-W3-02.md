---
id: ISS-W3-02
title: "W3-2 Ch 3b §3.5–3.6 CFA+DFA, k-CFA, CPA, synthesis + Gate #5"
issue_type: shard
status: open
priority: P0
labels: [ppa, wave-3, gate]
milestone: W3
parent_issue: EPIC-001
depends_on: [ISS-W3-01]
blocks: [ISS-W4-01]
ppa_scope: ["§3.5 Adding Data Flow Analysis (book pp. 182–188; PDF pp. 200–206)", "§3.6 Adding Context Information (book pp. 189–210; PDF pp. 207–227)"]
altitudes: [L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Extract combined control/data flow lattices, uniform k-CFA and context information; synthesize the Chapter 3 skill; refactor; Gate #5.

## Source Citations & Grounding

- §3.5 Adding Data Flow Analysis (book pp. 182–188; PDF pp. 200–206)
- §3.6 Adding Context Information (book pp. 189–210; PDF pp. 207–227)
- Tables in scope: Table 3.8 (p. 184/PDF 202), Table 3.9 (p. 188/PDF 206), Table 3.10 (p. 192/PDF 210)
- Figures in scope: Figure 3.6 (p. 185/PDF 203)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 182–210 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [ ] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [ ] All 3 tables and 1 figures in book pp. 182–210 are anchored (no omissions)
- [ ] Artifact `knowledge/skills/ppa-control-flow-and-constraints/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `knowledge/skills/ppa-control-flow-and-constraints/references/ppa-cfa-and-constraints.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W3-01; blocks: ISS-W4-01
- `knowledge/skills/ppa-control-flow-and-constraints/SKILL.md`
- `knowledge/skills/ppa-control-flow-and-constraints/references/ppa-cfa-and-constraints.md`

## Verification Receipts

_Pending._
