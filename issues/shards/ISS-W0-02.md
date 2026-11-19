---
id: ISS-W0-02
title: "W0-2 PDF coordinate indexer, concept-graph schema and knowledge validator"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-0]
milestone: W0
parent_issue: EPIC-001
depends_on: [ISS-W0-01]
blocks: [ISS-W1-01]
ppa_scope: ["Whole book (book pp. 1–452; PDF pp. 21–465; 465 PDF pages)"]
altitudes: [L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: null
---

## Summary

Build the deterministic (pdf_page, book_page) coordinate map with section, table, figure and bibliography locations, per-unit text slices, the concept-graph JSON schema, and the Tier-A knowledge validator.

## Source Citations & Grounding

- Whole book (book pp. 1–452; PDF pp. 21–465; 465 PDF pages)
- Tables in scope: Table 1.1 (p. 4/PDF 24), Table 1.2 (p. 19/PDF 39), Table 1.3 (p. 21/PDF 41), Table 1.4 (p. 24/PDF 44), Table 1.5 (p. 26/PDF 46), Table 1.6 (p. 27/PDF 47), Table 2.1 (p. 40/PDF 59), Table 2.2 (p. 44/PDF 63), Table 2.3 (p. 47/PDF 66), Table 2.4 (p. 50/PDF 69), Table 2.5 (p. 55/PDF 74), Table 2.6 (p. 56/PDF 75), Table 2.7 (p. 73/PDF 92), Table 2.8 (p. 75/PDF 94), Table 2.9 (p. 76/PDF 95), Table 2.10 (p. 133/PDF 152), Table 3.1 (p. 146/PDF 164), Table 3.2 (p. 155/PDF 173), Table 3.3 (p. 156/PDF 174), Table 3.4 (p. 158/PDF 176), Table 3.5 (p. 170/PDF 188), Table 3.6 (p. 174/PDF 192), Table 3.7 (p. 178/PDF 196), Table 3.8 (p. 184/PDF 202), Table 3.9 (p. 188/PDF 206), Table 3.10 (p. 192/PDF 210), Table 5.1 (p. 285/PDF 302), Table 5.2 (p. 288/PDF 305), Table 5.3 (p. 290/PDF 307), Table 5.4 (p. 292/PDF 309), Table 5.5 (p. 303/PDF 320), Table 5.6 (p. 305/PDF 322), Table 5.7 (p. 307/PDF 324), Table 5.8 (p. 310/PDF 327), Table 5.9 (p. 322/PDF 339), Table 5.10 (p. 328/PDF 345), Table 5.11 (p. 334/PDF 351), Table 5.12 (p. 337/PDF 354), Table 5.13 (p. 338/PDF 355), Table 5.14 (p. 341/PDF 358), Table 5.15 (p. 343/PDF 360), Table 5.16 (p. 346/PDF 363), Table 5.17 (p. 347/PDF 364), Table 5.18 (p. 348/PDF 365), Table 6.1 (p. 369/PDF 385), Table 6.2 (p. 373/PDF 389), Table 6.3 (p. 376/PDF 392), Table 6.4 (p. 379/PDF 395), Table 6.5 (p. 382/PDF 398), Table 6.6 (p. 384/PDF 400), Table C.1 (p. 421/PDF 436)
- Figures in scope: Figure 1.1 (p. 2/PDF 22), Figure 1.2 (p. 6/PDF 26), Figure 1.3 (p. 15/PDF 35), Figure 2.1 (p. 38/PDF 57), Figure 2.2 (p. 41/PDF 60), Figure 2.3 (p. 48/PDF 67), Figure 2.4 (p. 61/PDF 80), Figure 2.5 (p. 62/PDF 81), Figure 2.6 (p. 70/PDF 89), Figure 2.7 (p. 85/PDF 104), Figure 2.8 (p. 93/PDF 112), Figure 2.9 (p. 94/PDF 113), Figure 2.10 (p. 95/PDF 114), Figure 2.11 (p. 103/PDF 122), Figure 2.12 (p. 106/PDF 125), Figure 2.13 (p. 112/PDF 131), Figure 2.14 (p. 113/PDF 132), Figure 2.15 (p. 115/PDF 134), Figure 2.16 (p. 116/PDF 135), Figure 2.17 (p. 118/PDF 137), Figure 2.18 (p. 120/PDF 139), Figure 2.19 (p. 123/PDF 142), Figure 2.20 (p. 124/PDF 143), Figure 2.21 (p. 126/PDF 145), Figure 2.22 (p. 127/PDF 146), Figure 2.23 (p. 132/PDF 151), Figure 3.1 (p. 148/PDF 166), Figure 3.2 (p. 149/PDF 167), Figure 3.3 (p. 159/PDF 177), Figure 3.4 (p. 179/PDF 197), Figure 3.5 (p. 180/PDF 198), Figure 3.6 (p. 185/PDF 203), Figure 4.1 (p. 218/PDF 235), Figure 4.2 (p. 221/PDF 238), Figure 4.3 (p. 224/PDF 241), Figure 4.4 (p. 226/PDF 243), Figure 4.5 (p. 231/PDF 248), Figure 4.6 (p. 235/PDF 252), Figure 4.7 (p. 238/PDF 255), Figure 4.8 (p. 243/PDF 260), Figure 4.9 (p. 245/PDF 262), Figure 4.10 (p. 276/PDF 293), Figure 5.1 (p. 331/PDF 348), Figure 5.2 (p. 340/PDF 357), Figure 6.1 (p. 374/PDF 390), Figure 6.2 (p. 376/PDF 392), Figure 6.3 (p. 377/PDF 393), Figure 6.4 (p. 379/PDF 395), Figure 6.5 (p. 382/PDF 398), Figure 6.6 (p. 384/PDF 400), Figure A.1 (p. 394/PDF 410), Figure A.2 (p. 400/PDF 416), Figure A.3 (p. 403/PDF 419), Figure C.1 (p. 422/PDF 437), Figure C.2 (p. 423/PDF 438), Figure C.3 (p. 425/PDF 440)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 1–452 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 51 tables and 56 figures in book pp. 1–452 are anchored (no omissions)
- [x] `corpus/pdf_page_map.json` and `ontology/concept_graph.schema.json` pass `python3 -B scripts/validate_ppa_knowledge.py`
- [x] `python3 -B tests/test_wave0_foundation.py` exits 0
- [x] `python3 -B tests/test_artifact_rules.py` exits 0
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

### Rebuttal & Attribution Summary (Gate #0)

| Finding ID | Severity | Target File(s) | Disposition | Anchor After Fix |
| :--- | :--- | :--- | :--- | :--- |
| `F-CJ-002` / `F-FJ-003` | `BLOCKING` | `ontology/concept_graph.schema.json`, `scripts/ppa_artifact_rules.py`, `scripts/validate_ppa_knowledge.py`, `tests/test_artifact_rules.py` | Added Roman front-matter citation support (`Preface`, `Contents`, `List of Tables`, `List of Figures` with `book_page: null` + `book_page_roman` and `[PPA Preface, p. VI]`) | `ontology/concept_graph.schema.json:84-103`; `scripts/ppa_artifact_rules.py:40-46,204-216`; `scripts/validate_ppa_knowledge.py:258-269`; `tests/test_artifact_rules.py:42-60` |
| `F-FJ-004` | `BLOCKING` | `ontology/concept_graph.schema.json`, `scripts/validate_ppa_knowledge.py` | Added symmetric `corresponds_to` relation and `edge_basis` (`unification_id`, `citations`, `conditions`, `differs`) plus edge citation checks | `ontology/concept_graph.schema.json:22,115-153`; `scripts/validate_ppa_knowledge.py:399-402,519-534` |
| `F-FJ-005` / `F-OJ-014` | `BLOCKING` | `scripts/ppa_artifact_rules.py`, `scripts/validate_ppa_knowledge.py`, `tests/test_artifact_rules.py` | Added `N8` page-span support (`pp. A–B`, `<= 15`) and fail-closed `C1.10` detectors for malformed `[PPA` and `(book p` tokens | `scripts/ppa_artifact_rules.py:33-38,255-281`; `scripts/validate_ppa_knowledge.py:38-46,325-349`; `tests/test_artifact_rules.py:85-98` |
| `F-FJ-006` / `F-OJ-016` | `BLOCKING` | `scripts/extract_ppa_structure.py`, `scripts/ppa_structure_extras.py`, `corpus/pdf_page_map.json` | Extracted `end_matter` ranges (`Concluding Remarks`, `Mini Projects`, `Exercises`), closed final numbered sections at `Concluding Remarks`, and replaced blanket `+1` section tolerance with exact `shares_last_page` bounds | `scripts/ppa_structure_extras.py:18-60`; `scripts/extract_ppa_structure.py:322-338,450-460`; `scripts/ppa_artifact_rules.py:181-201`; `tests/test_wave0_foundation.py:427-446` |
| `F-OJ-010` | `BLOCKING` | `scripts/ppa_structure_extras.py`, `corpus/pdf_page_map.json`, `scripts/ppa_artifact_rules.py` | Added complete gap-free `statements` inventory (`342` items across Chapters 1–6 & Appendices A–C, `0` gaps) and enforced `C1.11` statement existence & span checks | `scripts/ppa_structure_extras.py:21-31,63-132`; `scripts/ppa_artifact_rules.py:169-180`; `tests/test_artifact_rules.py:62-83` |
| `F-CJ-005` / `F-FJ-010` | `BLOCKING` | `scripts/validate_ppa_knowledge.py`, `scripts/ppa_artifact_rules.py` | Implemented `C3.11` `artifact_refs` + `#fragment` resolution, `C3.7` link/fragment/root-escape checks, `C3.8` link direction, `C3.9` reachability, and `C1.9` gotcha-ledger coverage | `scripts/validate_ppa_knowledge.py:409-488`; `scripts/ppa_artifact_rules.py:471-522`; `tests/test_wave0_foundation.py:604-629` |
| `F-FJ-011` / `F-OJ-015` | `BLOCKING` | `scripts/ppa_artifact_rules.py`, `scripts/validate_ppa_knowledge.py` | Enforced strict UTF-8 decoding (`N1`, zero replacement) and LF-only line splitting (`N2`, ignoring FF/VT/U+2028) across all checks | `scripts/ppa_artifact_rules.py:75-97`; `tests/test_artifact_rules.py:148-161` |
| `F-CJ-009` / `F-FJ-015` / `F-FJ-017` | `PREFERENCE` | `scripts/ppa_artifact_rules.py` | Enforced router `[50, 100)` floor/ceiling (`C3.1`), `C2.5` description checks, non-router sibling matching (`C4.2`), router `evals/cases.yaml` (`C3.10`), and non-bullet ledger rejection | `scripts/ppa_artifact_rules.py:19,327-340,440-464,491-495` |
| `F-FJ-018` / `F-FJ-019` | `PREFERENCE` | `scripts/ppa_artifact_rules.py` | Added `C3.12` closed `knowledge/` file-tree check, unified BOM/trailing-space `---` detector + duplicate-key error (`N3`), and token-boundary `C4.2` matching | `scripts/ppa_artifact_rules.py:100-125,333-366,395-417`; `tests/test_artifact_rules.py:123-146,177-190` |
| `F-OJ-018` / `F-OJ-019` / `F-FJ-026` | `PREFERENCE` | `scripts/extract_ppa_structure.py`, `scripts/validate_ppa_knowledge.py`, `ontology/concept_graph.schema.json` | Added per-page `basis` provenance (`front_matter`/`header`/`inferred`), explicit `[NOT_IMPLEMENTED]` reporting (`--certify` fails), and optional `conditions`/`issue_refs`/`external_terms` schema properties | `scripts/extract_ppa_structure.py:440-447`; `scripts/validate_ppa_knowledge.py:57-88,554`; `ontology/concept_graph.schema.json:56-82` |

- 2026-11-19 Gate #0 Round 2 `[ALIGNED gate0-v2]` across all 3 independent review tracks (`P-SWE`, `P-ARCH`, `P-CYBER`): all Round 1 blocking findings withdrawn; `F-OJ-R2-001` & `F-CJ-R2-001..003` preference items queued for `ISS-W7-01`.

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W0-01; blocks: ISS-W1-01
- `scripts/extract_ppa_structure.py`
- `scripts/ppa_structure_extras.py`
- `corpus/pdf_page_map.json`
- `ontology/concept_graph.schema.json`
- `scripts/validate_ppa_knowledge.py`
- `tests/test_wave0_foundation.py`
- `scripts/ppa_artifact_rules.py` (CONFORMANCE_SPEC `N1`–`N3`, `N8`, `C1.9`–`C1.11`, `C3.1`–`C3.6`, `C3.10`, `C3.12`, `C4.1`–`C4.2`)
- `tests/test_artifact_rules.py`

## Verification Receipts

- 2026-11-18 [in_progress] Gate #0 remediation verified: `corpus/pdf_page_map.json` regenerated (`342` statements, `0` gaps, `8` offset runs), `python3 -B tests/test_wave0_foundation.py` (`37` tests OK), `python3 -B tests/test_artifact_rules.py` (`10` tests OK), `python3 -B scripts/validate_ppa_knowledge.py` (`PASS`).
- 2026-11-19 [closed] Gate #0 3/3 `[ALIGNED gate0-v2]` confirmed; Wave 0 closure validated (`corpus/pdf_page_map.json` `342` statements / `0` gaps, `47/47` unit tests OK, `validate_ppa_knowledge.py`: PASS).
