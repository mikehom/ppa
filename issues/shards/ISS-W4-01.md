---
id: ISS-W4-01
title: "W4-1 Ch 4a §4.1–4.3 correctness relations, widening/narrowing, Galois connections"
issue_type: shard
status: open
priority: P0
labels: [ppa, wave-4]
milestone: W4
parent_issue: EPIC-001
depends_on: [ISS-W3-02]
blocks: [ISS-W4-02]
ppa_scope: ["§4.1 A Mundane Approach to Correctness (book pp. 211–220; PDF pp. 228–237)", "§4.2 Approximation of Fixed Points (book pp. 221–232; PDF pp. 238–249)", "§4.3 Galois Connections (book pp. 233–245; PDF pp. 250–262)"]
altitudes: [L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Extract correctness relations/representation functions, widening and narrowing operators, Galois connections and insertions.

## Source Citations & Grounding

- §4.1 A Mundane Approach to Correctness (book pp. 211–220; PDF pp. 228–237)
- §4.2 Approximation of Fixed Points (book pp. 221–232; PDF pp. 238–249)
- §4.3 Galois Connections (book pp. 233–245; PDF pp. 250–262)
- Figures in scope: Figure 4.1 (p. 218/PDF 235), Figure 4.2 (p. 221/PDF 238), Figure 4.3 (p. 224/PDF 241), Figure 4.4 (p. 226/PDF 243), Figure 4.5 (p. 231/PDF 248), Figure 4.6 (p. 235/PDF 252), Figure 4.7 (p. 238/PDF 255), Figure 4.8 (p. 243/PDF 260), Figure 4.9 (p. 245/PDF 262)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 211–245 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [ ] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [ ] All 0 tables and 9 figures in book pp. 211–245 are anchored (no omissions)
- [ ] Artifact `corpus/shards/RAW_SHARD_04a_galois_widening.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W3-02; blocks: ISS-W4-02
- `corpus/shards/RAW_SHARD_04a_galois_widening.md`

## Verification Receipts

_Pending._
