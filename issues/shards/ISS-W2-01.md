---
id: ISS-W2-01
title: "W2-1 Ch 2a §2.1–2.4 intraprocedural DFA, SOS soundness, monotone frameworks"
issue_type: shard
status: open
priority: P0
labels: [ppa, wave-2]
milestone: W2
parent_issue: EPIC-001
depends_on: [ISS-W1-02]
blocks: [ISS-W2-03]
ppa_scope: ["§2.1 Intraprocedural Analysis (book pp. 35–53; PDF pp. 54–72)", "§2.2 Theoretical Properties (book pp. 54–64; PDF pp. 73–83)", "§2.3 Monotone Frameworks (book pp. 65–73; PDF pp. 84–92)", "§2.4 Equation Solving (book pp. 74–81; PDF pp. 93–100)"]
altitudes: [L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Extract the four classical bit-vector analyses, SOS-based correctness of Live Variables, monotone/distributive frameworks, and MFP vs MOP solutions.

## Source Citations & Grounding

- §2.1 Intraprocedural Analysis (book pp. 35–53; PDF pp. 54–72)
- §2.2 Theoretical Properties (book pp. 54–64; PDF pp. 73–83)
- §2.3 Monotone Frameworks (book pp. 65–73; PDF pp. 84–92)
- §2.4 Equation Solving (book pp. 74–81; PDF pp. 93–100)
- Tables in scope: Table 2.1 (p. 40/PDF 59), Table 2.2 (p. 44/PDF 63), Table 2.3 (p. 47/PDF 66), Table 2.4 (p. 50/PDF 69), Table 2.5 (p. 55/PDF 74), Table 2.6 (p. 56/PDF 75), Table 2.7 (p. 73/PDF 92), Table 2.8 (p. 75/PDF 94), Table 2.9 (p. 76/PDF 95)
- Figures in scope: Figure 2.1 (p. 38/PDF 57), Figure 2.2 (p. 41/PDF 60), Figure 2.3 (p. 48/PDF 67), Figure 2.4 (p. 61/PDF 80), Figure 2.5 (p. 62/PDF 81), Figure 2.6 (p. 70/PDF 89)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 35–81 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [ ] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [ ] All 9 tables and 6 figures in book pp. 35–81 are anchored (no omissions)
- [ ] Artifact `corpus/shards/RAW_SHARD_02a_intraproc_dfa.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W1-02; blocks: ISS-W2-03
- `corpus/shards/RAW_SHARD_02a_intraproc_dfa.md`

## Verification Receipts

_Pending._
