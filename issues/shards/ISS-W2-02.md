---
id: ISS-W2-02
title: "W2-2 Ch 2b/2c §2.5–2.6 interprocedural context and shape analysis"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-2]
milestone: W2
parent_issue: EPIC-001
depends_on: [ISS-W1-02]
blocks: [ISS-W2-03]
ppa_scope: ["§2.5 Interprocedural Analysis (book pp. 82–103; PDF pp. 101–122)", "§2.6 Shape Analysis (book pp. 104–139; PDF pp. 123–158)"]
altitudes: [L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: 38
---

## Summary

Extract MVP, call strings, assumption sets, flow-(in)sensitivity and shape graphs with their transfer functions.

## Source Citations & Grounding

- §2.5 Interprocedural Analysis (book pp. 82–103; PDF pp. 101–122)
- §2.6 Shape Analysis (book pp. 104–139; PDF pp. 123–158)
- Tables in scope: Table 2.10 (p. 133/PDF 152)
- Figures in scope: Figure 2.7 (p. 85/PDF 104), Figure 2.8 (p. 93/PDF 112), Figure 2.9 (p. 94/PDF 113), Figure 2.10 (p. 95/PDF 114), Figure 2.11 (p. 103/PDF 122), Figure 2.12 (p. 106/PDF 125), Figure 2.13 (p. 112/PDF 131), Figure 2.14 (p. 113/PDF 132), Figure 2.15 (p. 115/PDF 134), Figure 2.16 (p. 116/PDF 135), Figure 2.17 (p. 118/PDF 137), Figure 2.18 (p. 120/PDF 139), Figure 2.19 (p. 123/PDF 142), Figure 2.20 (p. 124/PDF 143), Figure 2.21 (p. 126/PDF 145), Figure 2.22 (p. 127/PDF 146), Figure 2.23 (p. 132/PDF 151)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 82–139 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 1 tables and 17 figures in book pp. 82–139 are anchored (no omissions)
- [x] Artifact `corpus/shards/RAW_SHARD_02b_interproc_shape.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 extraction complete; staged for Gate #3 three-track adversarial panel review (`W2-3` integration merged into `ontology/concept_graph.json`, `ppa-dataflow-and-slicing/`, `BKL-041..050`, and `BKL-003/005`).
- 2026-11-19 Gate #3 Round 2 `[ALIGNED gate3-v2]` across all 3 independent review tracks (`P-SWE`, `P-ARCH`, `P-CYBER`): `0` `HARD_BLOCK`, `0` `BLOCKING`.

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W1-02; blocks: ISS-W2-03
- `corpus/shards/RAW_SHARD_02b_interproc_shape.md`
- `knowledge/skills/ppa-dataflow-and-slicing/references/interprocedural-and-correctness.md`
- `knowledge/skills/ppa-dataflow-and-slicing/references/shape-analysis.md`

## Verification Receipts

- 2026-11-19 [in_progress] Unit 2b extraction verified: `corpus/shards/RAW_SHARD_02b_interproc_shape.md` (`1,486` lines, `G-U2b-01..34` `34/34` covered, `1/1` `Table 2.10`, `17/17` Figures `2.7–2.23`); `validate_ppa_knowledge.py --strict-gotchas` PASS, `check_portability_hygiene.py .` PASS. Ready for Gate #3.
- 2026-11-19 [closed] Gate #3 Round 2 unanimous 3/3 [ALIGNED gate3-v2] across P-SWE, P-ARCH, and P-CYBER; 0 HARD_BLOCK, 0 BLOCKING; validators, hygiene, and 47/47 unit tests PASS.
