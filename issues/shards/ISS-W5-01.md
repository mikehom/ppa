---
id: ISS-W5-01
title: "W5-1 Ch 5a §5.1–5.3 annotated types, natural semantics, W_UL / W_CFA inference"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-5]
milestone: W5
parent_issue: EPIC-001
depends_on: [ISS-W4-02]
blocks: [ISS-W5-02]
ppa_scope: ["§5.1 Control Flow Analysis (book pp. 283–290; PDF pp. 300–307)", "§5.2 Theoretical Properties (book pp. 291–299; PDF pp. 308–316)", "§5.3 Inference Algorithms (book pp. 300–318; PDF pp. 317–335)"]
altitudes: [L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: 82
---

## Summary

Extract the annotated type system for CFA, its soundness via natural semantics, and the inference algorithms with unification.

## Source Citations & Grounding

- §5.1 Control Flow Analysis (book pp. 283–290; PDF pp. 300–307)
- §5.2 Theoretical Properties (book pp. 291–299; PDF pp. 308–316)
- §5.3 Inference Algorithms (book pp. 300–318; PDF pp. 317–335)
- Tables in scope: Table 5.1 (p. 285/PDF 302), Table 5.2 (p. 288/PDF 305), Table 5.3 (p. 290/PDF 307), Table 5.4 (p. 292/PDF 309), Table 5.5 (p. 303/PDF 320), Table 5.6 (p. 305/PDF 322), Table 5.7 (p. 307/PDF 324), Table 5.8 (p. 310/PDF 327)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 283–318 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 8 tables and 0 figures in book pp. 283–318 are anchored (no omissions)
- [x] Artifact `corpus/shards/RAW_SHARD_05a_annotated_types_inference.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Unit 5a shard `corpus/shards/RAW_SHARD_05a_annotated_types_inference.md` (`868L`, `§§5.1–5.3`, `8/8` `Tables 5.1–5.8`, `22/22` `G-U5a-01..22`, `24` Statements `5.1–5.23`) promoted after pre-promotion primary-source & `C1.10` scrub; staged for Gate #7 (`gate7-v1`).
- 2026-11-19 Gate #7 Round 2 (`gate7-v2`): unanimous `3/3 [ALIGNED gate7-v2]` across `P-SWE`, `P-CYBER`, and `P-ARCH` (`0` `HARD_BLOCK`, `0` `BLOCKING`, `0` `PREFERENCE`; #254, #255, #256; `RAW_SHARD_05a_annotated_types_inference.md` passed Rounds 1 and 2 with zero findings).

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W4-02; blocks: ISS-W5-02
- `corpus/shards/RAW_SHARD_05a_annotated_types_inference.md`
- `issues/backlog/BKL-004.md`, `issues/backlog/BKL-011.md`
- `issues/backlog/BKL-073.md` .. `issues/backlog/BKL-077.md`

## Verification Receipts

- 2026-11-19 [in_progress] Unit 5a promoted (`RAW_SHARD_05a_annotated_types_inference.md` 868L, `22/22` `G-U5a-01..22`, `Tables 5.1–5.8`), `BKL-073..077` & `BKL-004`/`011` wired; staged for Gate #7 (`gate7-v1`).
- 2026-11-19 [aligned] Gate #7 Round 2 unanimous 3/3 [ALIGNED gate7-v2] across P-SWE, P-CYBER, P-ARCH (#254, #255, #256).
- 2026-11-19 [closed] Gate #7 closed after post-remediation validators, hygiene, export parity, and 47/47 unittest passes.
