---
id: ISS-W6-01
title: "W6-1 Unit 6: Ch 6 worklist, RPO, round-robin, SCC solvers + Gate #9"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-6, gate]
milestone: W6
parent_issue: EPIC-001
depends_on: [ISS-W5-03]
blocks: [ISS-W6-02]
ppa_scope: ["§6.1 Worklist Algorithms (book pp. 365–373; PDF pp. 381–389)", "§6.2 Iterating in Reverse Postorder (book pp. 374–380; PDF pp. 390–396)", "§6.3 Iterating Through Strong Components (book pp. 381–392; PDF pp. 397–408)", "Subject Index (book pp. 433–438; PDF pp. 447–451)", "Bibliography [1]–[185] (book pp. 439–452; PDF pp. 452–465)"]
altitudes: [L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
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

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 7 tables and 12 figures in book pp. 365–452 are anchored (no omissions)
- [x] Artifact `corpus/shards/RAW_SHARD_06_algorithms_bib.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `knowledge/skills/ppa-fixedpoint-solvers/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifacts `knowledge/ambient-context/ppa-fixedpoint-solvers.md` and `references/{worklist-and-rpo-algorithms,scc-round-robin-and-advanced-solvers}.md` exist and pass `scripts/validate_ppa_knowledge.py`
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Chapter 6 + Unit 6 Subject Index / Bibliography extraction (`corpus/shards/RAW_SHARD_06_algorithms_bib.md`, `586L`, `24/24` `G-U6-01..24`, `Tables 6.1–6.6`, `Figures 6.1–6.6`, `Mini Projects 6.1–6.2`, `Exercises 6.1–6.14`, Subject Index `379` headwords, Bibliography `[1]–[185]`) and Chapter 6 solver package (`ppa-fixedpoint-solvers/` `271L` `SKILL.md` / `140L` & `113L` `L1` refs, `ppa-fixedpoint-solvers.md` `124L`, `12` new nodes in `153`-node symmetric `concept_graph.json`, `U-61..U-66` + `W`/`scc` notation, `BKL-083..092` + reconciled `BKL-002/010..014/016..019/022/023`, `REF-007`) promoted after pre-promotion primary-source & `P2` audit (`#258`); staged for Gate #9 (`gate9-v1`).
- 2026-11-19 Gate #9 Round 1 (`gate9-v1`) produced `8` findings (`5 BLOCKING`, `3 PREFERENCE`, `0 HARD_BLOCK`) resolved into `gate9-v2` (all re-verified across tracked files, `RAW_KNOWLEDGE.md` reassembled, `concept_graph.json` and `BKL-085`/`BKL-088` synced):

| Finding ID | Severity | Resolution Summary (`gate9-v1` -> `gate9-v2`) | Status |
| :--- | :--- | :--- | :--- |
| `F-FJ-901` | `BLOCKING` | Removed untagged bibliography-only eponym `Kam–Ullman` from `ppa.solvers.round-robin-loop-bound.title` (`concept_graph.json:11229`) and `worklist-and-rpo-algorithms.md` `§5.2` heading (`Bit-Vector Loop-Connectedness Bound`), wrapped `[external: Kam–Ullman rapid frameworks] ([92])` in `ppa.solvers.fastness-closure` `cs_theory`, and synced `BKL-088.md` `L1 anchor`. | `RESOLVED -> ACCEPTED` |
| `F-OJ-901` | `BLOCKING` | Verified `PPA` Chapter 4 Concluding Remarks introduces `[41]` as `convex polygons` at `[PPA Chapter 4 Concluding Remarks, p. 272] (book p. 272; PDF p. 289)` (`0` occurrences of `polyhedra` in book); updated `scc-round-robin-and-advanced-solvers.md` (`Interval` `p. 221`, `convex polygons` `p. 272`, `[external: convex polyhedra]`) and tagged `[41]` `[external: convex polyhedra]` in `RAW_SHARD_06_algorithms_bib.md` / `RAW_KNOWLEDGE.md`. | `RESOLVED -> ACCEPTED` |
| `F-CJ-903` | `BLOCKING` | Resolved with `F-OJ-901`; direct `ppa.pdf` (`PDF p. 289`) check confirms `book p. 272` rather than `p. 270`, and both Chapter 4 domains (`Interval`, `convex polygons`) plus `[external: convex polyhedra]` are now accurately cited. | `RESOLVED (book p. 272 verified) -> ACCEPTED` |
| `F-OJ-902` | `BLOCKING` | Disambiguated and tagged all bare editor `IDE` mentions as `[external: editor IDE]` across `ppa-fixedpoint-solvers/SKILL.md` (table + `Procedure 4`), `README.md`, and `ppa.solvers.local-and-elimination-solvers.projections.swe_architecture` to avoid collision with `[147]` (`IDE`). | `RESOLVED -> ACCEPTED` |
| `F-CJ-901` | `BLOCKING` | Fixed `Example 6.1` Step-2 pop counts across `RAW_SHARD_06_algorithms_bib.md`, `RAW_KNOWLEDGE.md`, `ppa-fixedpoint-solvers.md`, `SKILL.md`, both `L1` refs, and `concept_graph.json`: `20` Step-2 pops for reversed `[x₆..x₁]` (`Exercise 6.1`; `x₁` at Step 12, `x₆` popped `5` times total), and `8` Step-2 pops (`9` table rows incl. init, `x₆` once) for deduplicated LIFO (`Exercise 6.3`) and deduplicated RPO (`Exercise 6.6`). | `RESOLVED -> ACCEPTED` |
| `F-CJ-902` | `BLOCKING` | Corrected Subject Index tally from `369` to `379` headwords (`69 + 79 + 80 + 80 + 71` across `book pp. 433–437`) across `RAW_SHARD_06_algorithms_bib.md`, `RAW_KNOWLEDGE.md`, `scc-round-robin-and-advanced-solvers.md`, `concept_graph.json`, `altitude_alignment_log.md`, and `ISS-W6-01.md`. | `RESOLVED -> ACCEPTED` |
| `F-OJ-903` | `PREFERENCE` | Fixed `pp. 367` -> `p. 367` in `worklist-and-rpo-algorithms.md` `§1.3` heading and updated `BKL-085.md` `L1 anchor` fragment (`#13-...-p-367`). | `RESOLVED -> ACCEPTED` |
| `F-CJ-904` | `PREFERENCE` | Retained `section: "[1]"`..`"[185]"` paired with `chapter_or_app: "Bibliography"` in `ppa.bib.bibliography-concordance.citations`: testing `"Bibliography [N]"` fails `ontology/concept_graph.schema.json:95`, whose `section` regex explicitly requires `\[\d{1,3}\]` (`[FAIL] schema`). | `REBUTTED (schema-enforced)` |
- 2026-11-19 Gate #9 Round 2 (`gate9-v2`): unanimous `3/3 [ALIGNED gate9-v2]` across `P-SWE`, `P-CYBER`, and `P-ARCH` (`0 HARD_BLOCK`, `0 BLOCKING`, `0 PREFERENCE`; #270, #271, #272; all `8/8` Round 1 items verified).

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W5-03; blocks: ISS-W6-02
- `corpus/shards/RAW_SHARD_06_algorithms_bib.md`
- `knowledge/skills/ppa-fixedpoint-solvers/SKILL.md`
- `knowledge/skills/ppa-fixedpoint-solvers/references/worklist-and-rpo-algorithms.md`
- `knowledge/skills/ppa-fixedpoint-solvers/references/scc-round-robin-and-advanced-solvers.md`
- `knowledge/ambient-context/ppa-fixedpoint-solvers.md`
- `ontology/concept_graph.json`
- `ontology/notation_index.md`
- `issues/refactors/REF-007.md`
- `issues/backlog/BKL-002.md`, `issues/backlog/BKL-010.md`, `issues/backlog/BKL-011.md`, `issues/backlog/BKL-012.md`, `issues/backlog/BKL-013.md`, `issues/backlog/BKL-014.md`, `issues/backlog/BKL-016.md` .. `issues/backlog/BKL-019.md`, `issues/backlog/BKL-022.md`, `issues/backlog/BKL-023.md`
- `issues/backlog/BKL-083.md` .. `issues/backlog/BKL-092.md`

## Verification Receipts
- 2026-11-19 [in_progress] Unit 6 shard (RAW_SHARD_06_algorithms_bib.md 586L, 24/24 G-U6), ppa-fixedpoint-solvers/ (271L SKILL, 140L/113L refs, 124L ambient), 153-node concept_graph.json (12 new Ch 6 nodes, U2/U3/U10/U7 symmetry), U-61..U-66 + W/scc notation, BKL-083..092 + reconciled BKL-002/010..014/016..019/022/023, and REF-007 promoted; staged for Gate #9 (gate9-v1).
- 2026-11-19 [aligned] Gate #9 Round 2 unanimous 3/3 [ALIGNED gate9-v2] across P-SWE, P-CYBER, P-ARCH (#270, #271, #272); 8/8 Round 1 items verified.
- 2026-11-19 [closed] Closed after unanimous 3/3 [ALIGNED gate9-v2] and full Tier-A/hygiene/conformance/unittest verification.
