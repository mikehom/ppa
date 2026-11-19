---
id: ISS-W2-03
title: "W2-3 Unit 2 synthesis: dataflow skill, reference and Gate #3"
issue_type: shard
status: open
priority: P0
labels: [ppa, wave-2, gate]
milestone: W2
parent_issue: EPIC-001
depends_on: [ISS-W2-01, ISS-W2-02]
blocks: [ISS-W2-04]
ppa_scope: ["Chapter 2 (book pp. 35–140; PDF pp. 54–158)"]
altitudes: [L1, L2]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Synthesize Chapter 2 into an actionable L2 skill and L1 reference; cumulative KB refactoring; Gate #3.

## Source Citations & Grounding

- Chapter 2 (book pp. 35–140; PDF pp. 54–158)
- Tables in scope: Table 2.1 (p. 40/PDF 59), Table 2.2 (p. 44/PDF 63), Table 2.3 (p. 47/PDF 66), Table 2.4 (p. 50/PDF 69), Table 2.5 (p. 55/PDF 74), Table 2.6 (p. 56/PDF 75), Table 2.7 (p. 73/PDF 92), Table 2.8 (p. 75/PDF 94), Table 2.9 (p. 76/PDF 95), Table 2.10 (p. 133/PDF 152)
- Figures in scope: Figure 2.1 (p. 38/PDF 57), Figure 2.2 (p. 41/PDF 60), Figure 2.3 (p. 48/PDF 67), Figure 2.4 (p. 61/PDF 80), Figure 2.5 (p. 62/PDF 81), Figure 2.6 (p. 70/PDF 89), Figure 2.7 (p. 85/PDF 104), Figure 2.8 (p. 93/PDF 112), Figure 2.9 (p. 94/PDF 113), Figure 2.10 (p. 95/PDF 114), Figure 2.11 (p. 103/PDF 122), Figure 2.12 (p. 106/PDF 125), Figure 2.13 (p. 112/PDF 131), Figure 2.14 (p. 113/PDF 132), Figure 2.15 (p. 115/PDF 134), Figure 2.16 (p. 116/PDF 135), Figure 2.17 (p. 118/PDF 137), Figure 2.18 (p. 120/PDF 139), Figure 2.19 (p. 123/PDF 142), Figure 2.20 (p. 124/PDF 143), Figure 2.21 (p. 126/PDF 145), Figure 2.22 (p. 127/PDF 146), Figure 2.23 (p. 132/PDF 151)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 35–140 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [ ] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [ ] All 10 tables and 23 figures in book pp. 35–140 are anchored (no omissions)
- [ ] Artifact `knowledge/skills/ppa-dataflow-and-slicing/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `knowledge/skills/ppa-dataflow-and-slicing/references/ppa-dataflow-and-shape.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W2-01, ISS-W2-02; blocks: ISS-W2-04
- `knowledge/skills/ppa-dataflow-and-slicing/SKILL.md`
- `knowledge/skills/ppa-dataflow-and-slicing/references/ppa-dataflow-and-shape.md`

## Verification Receipts

_Pending._
