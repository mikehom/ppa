---
id: ISS-W4-01
title: "W4-1 Ch 4a §4.1–4.3 correctness relations, widening/narrowing, Galois connections"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-4]
milestone: W4
parent_issue: EPIC-001
depends_on: [ISS-W3-02]
blocks: [ISS-W4-02]
ppa_scope: ["§4.1 A Mundane Approach to Correctness (book pp. 211–220; PDF pp. 228–237)", "§4.2 Approximation of Fixed Points (book pp. 221–232; PDF pp. 238–249)", "§4.3 Galois Connections (book pp. 233–245; PDF pp. 250–262)"]
altitudes: [L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
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

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 0 tables and 9 figures in book pp. 211–245 are anchored (no omissions)
- [x] Artifact `corpus/shards/RAW_SHARD_04a_galois_widening.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Chapter 4a extraction merged and pre-audited against rendered page images (`PDF pp. 228–263`) into `corpus/shards/RAW_SHARD_04a_galois_widening.md` (`971` lines, `24/24` `G-U4a-01..24`, `9/9` `Figures 4.1–4.9`, `10/10` displays `(4.1)–(4.10)`, `32/32` contiguous `Statements 4.1–4.32`), integrated into `ppa-abstract-interpretation/`, `BKL-001`, `BKL-002`, `BKL-067..069`, and `113`-node `ontology/concept_graph.json`. Staged for Gate #6 (`gate6-v1`).
- 2026-11-19 Gate #6 Round 1 remediation (`gate6-v2`): converted all `44` plural page-range companion tokens in `RAW_SHARD_04a_galois_widening.md` (`971` lines) to paired singular companions (`F-OJ-603`), tagged `[external: CFG loop-cutset]` in `RAW_SHARD_04a_galois_widening.md:834` and `correctness-and-fixed-points.md:249` (`F-FJ-603`), replaced bogus `BKL-024` spacing note with `ς`/`ϕ`/`Δ` scope collisions and aligned `BKL-024` to `ppa.ai.galois-insertion-and-reduction` (`F-FJ-601`), updated `BKL-013/024/029/033/067..069` (`0` unit-4 staging refs, distinct mechanisms, complete `p. 229` and `§4.2 pp. 223, 226` citations and `L1`/`L2` anchors); full `13`-finding table recorded in `ISS-W4-02.md`.
- 2026-11-19 Round 2 (`gate6-v2`): unanimous `3/3 [ALIGNED gate6-v2]` across `P-SWE`, `P-ARCH`, and `P-CYBER` (`0` `HARD_BLOCK`, `0` `BLOCKING`; #238, #239, #240).

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W3-02; blocks: ISS-W4-02
- `corpus/shards/RAW_SHARD_04a_galois_widening.md`
- `knowledge/skills/ppa-abstract-interpretation/references/correctness-and-fixed-points.md`
- `knowledge/skills/ppa-abstract-interpretation/references/galois-connections-and-insertions.md`
- `issues/backlog/BKL-001.md`, `issues/backlog/BKL-002.md`
- `issues/backlog/BKL-067.md` .. `issues/backlog/BKL-069.md`

## Verification Receipts
- 2026-11-19 [in_progress] Unit 4a shard corpus/shards/RAW_SHARD_04a_galois_widening.md (971L, 24/24 G-U4a-01..24, Figures 4.1-4.9, Statements 4.1-4.32) integrated into ppa-abstract-interpretation/ and 113-node ontology/concept_graph.json for Gate #6 (gate6-v1).
- 2026-11-19 [in_progress] Gate #6 Round 1 remediation (gate6-v2) applied across RAW_SHARD_04a_galois_widening.md (971L, 0 plural book-pp tokens), correctness-and-fixed-points.md (260L), and BKL-013/024/029/033/067..069 for Gate #6 Round 2.
- 2026-11-19 [closed] Gate #6 Round 2 unanimous 3/3 [ALIGNED gate6-v2] (#238, #239, #240); 0 HARD_BLOCK, 0 BLOCKING; RAW_SHARD_04a (971L, 0 plural book-pp), validators, hygiene, and 47/47 unit tests PASS.
