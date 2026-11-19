---
id: ISS-W1-01
title: "W1-1 Unit 0: Appendices A–C and Index of Notation + Gate #1"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-1, gate]
milestone: W1
parent_issue: EPIC-001
depends_on: [ISS-W0-01, ISS-W0-02, ISS-W0-03]
blocks: [ISS-W1-02]
ppa_scope: ["§A.1 Basic Definitions (book pp. 393–397; PDF pp. 409–413)", "§A.2 Construction of Complete Lattices (book pp. 397–398; PDF pp. 413–414)", "§A.3 Chains (book pp. 398–401; PDF pp. 414–417)", "§A.4 Fixed Points (book pp. 402–404; PDF pp. 418–420)", "§B.1 Proof by Induction (book pp. 405–407; PDF pp. 421–423)", "§B.2 Introducing Coinduction (book pp. 407–410; PDF pp. 423–426)", "§B.3 Proof by Coinduction (book pp. 411–415; PDF pp. 427–431)", "§C.1 Graphs and Forests (book pp. 417–421; PDF pp. 432–436)", "§C.2 Reverse Postorder (book pp. 421–426; PDF pp. 436–441)", "§C.3 Regular Expressions (book pp. 426–427; PDF pp. 441–442)", "Index of Notation (book pp. 429–432; PDF pp. 443–446)"]
altitudes: [L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: 5
---

## Summary

Extract partially ordered sets, complete lattices, chains, fixed points, induction/coinduction and graph/regular-expression foundations; seed the notation index and concept graph; promote all three Appendix A–C `L1` references into `knowledge/skills/ppa-program-analysis/references/`; run Gate #1.

## Source Citations & Grounding

- `[PPA §A.1, p. 393] (book p. 393; PDF p. 409)` through `[PPA §A.1, p. 397] (book p. 397; PDF p. 413)`
- `[PPA §A.2, p. 397] (book p. 397; PDF p. 413)` through `[PPA §A.2, p. 398] (book p. 398; PDF p. 414)`
- `[PPA §A.3, p. 398] (book p. 398; PDF p. 414)` through `[PPA §A.3, p. 401] (book p. 401; PDF p. 417)`
- `[PPA §A.4, p. 402] (book p. 402; PDF p. 418)` through `[PPA Appendix A Concluding Remarks, p. 404] (book p. 404; PDF p. 420)`
- `[PPA §B.1, p. 405] (book p. 405; PDF p. 421)` through `[PPA §B.1, p. 407] (book p. 407; PDF p. 423)`
- `[PPA §B.2, p. 407] (book p. 407; PDF p. 423)` through `[PPA §B.2, p. 410] (book p. 410; PDF p. 426)`
- `[PPA §B.3, p. 411] (book p. 411; PDF p. 427)` through `[PPA Appendix B Concluding Remarks, p. 415] (book p. 415; PDF p. 431)`
- `[PPA §C.1, p. 417] (book p. 417; PDF p. 432)` through `[PPA §C.1, p. 421] (book p. 421; PDF p. 436)`
- `[PPA §C.2, p. 421] (book p. 421; PDF p. 436)` through `[PPA §C.2, p. 426] (book p. 426; PDF p. 441)`
- `[PPA §C.3, p. 426] (book p. 426; PDF p. 441)` through `[PPA Appendix C Concluding Remarks, p. 427] (book p. 427; PDF p. 442)`
- `[PPA Index of Notation, p. 429] (book p. 429; PDF p. 443)` through `[PPA Index of Notation, p. 432] (book p. 432; PDF p. 446)`
- Tables in scope: `[PPA Table C.1, p. 421] (book p. 421; PDF p. 436)`
- Figures in scope: `[PPA Figure A.1, p. 394] (book p. 394; PDF p. 410)`, `[PPA Figure A.2, p. 400] (book p. 400; PDF p. 416)`, `[PPA Figure A.3, p. 403] (book p. 403; PDF p. 419)`, `[PPA Figure C.1, p. 422] (book p. 422; PDF p. 437)`, `[PPA Figure C.2, p. 423] (book p. 423; PDF p. 438)`, `[PPA Figure C.3, p. 425] (book p. 425; PDF p. 440)`
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; blank versos pp. 416 and 428 are omitted from the PDF).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per `architecture/ARCHITECTURE.md` §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pages 393–432 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 1 table and 6 figures in book pages 393–432 are anchored across `L3`, `L1`, and `ontology/concept_graph.json` (`C1.5` = 0 missing)
- [x] Artifact `corpus/shards/RAW_SHARD_00_appendices.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `ontology/notation_index.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `ontology/concept_graph.json` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] `knowledge/skills/ppa-program-analysis/references/appendix-{a,b,c}*.md` exist (`<= 450` lines each), are linked from `SKILL.md`, and pass `scripts/validate_ppa_knowledge.py`
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (Round 2 ready)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- **Round 1 (`gate1-v1`)**: Three independent adversarial evaluators audited all Unit 0 artifacts against rendered `ppa.pdf` page images (`PDF pp. 409–446`) and `architecture/CONFORMANCE_SPEC.md`, returning `[DISAGREE]` with `0` `HARD_BLOCK` and remediable `BLOCKING` / `PREFERENCE` findings mapped 1-to-1 below.
- **Round 1 Remediation (`gate1-v2` candidate)**: All `BLOCKING` and `PREFERENCE` findings across all three Gate #1 audit streams were resolved directly in `corpus/shards/RAW_SHARD_00_appendices.md`, `ontology/notation_index.md`, `ontology/concept_graph.json`, `knowledge/skills/ppa-program-analysis/references/appendix-{a,b,c}*.md`, `knowledge/skills/ppa-program-analysis/SKILL.md`, and `issues/backlog/BKL-013..024.md`.

### Rebuttal & Attribution Summary (Gate #1)

| Finding ID(s) | Severity | Disposition | Verification Anchor & Remediation Summary |
| :--- | :--- | :--- | :--- |
| `F-CJ-101`, `F-FJ-007` | `BLOCKING` | `REMEDIATED` | Added `"table_or_fig": "Figure C.1"` (`book_page: 422, pdf_page: 437`) and `"Figure C.2"` (`book_page: 423, pdf_page: 438`) on `ppa.graphs.dfsf`, `ppa.graphs.edge-classification`, and `ppa.graphs.reverse-postorder` (`ontology/concept_graph.json:1644-1775`), and promoted `knowledge/skills/ppa-program-analysis/references/appendix-c-graphs-dfsf-and-rpo.md` (linked at `knowledge/skills/ppa-program-analysis/SKILL.md:70`) into `artifact_refs` of all Appendix C concepts (`C1.5` = 0 uncited). |
| `F-CJ-102`, `F-OJ-G1-004`, `F-FJ-012` | `BLOCKING` | `REMEDIATED` | Qualified `ppa.graphs.loop-connectedness` (`ontology/concept_graph.json:1808-1835`) and `ppa.graphs.reverse-postorder` (`ontology/concept_graph.json:1754-1790`) with the explicit `Lemma 6.12` Bit Vector Framework, `DFSF T`, and reverse-postorder preconditions; added well-founded order decrease to `ppa.proof.banach-contractive` (`ontology/concept_graph.json:1091-1115`). |
| `F-CJ-103`, `F-OJ-G1-011`, `F-FJ-011` | `BLOCKING` | `REMEDIATED` | Replaced ambiguous `"post-fixed"` with book-defined `Red(f)` (`f(l) ⊑ l`, `ontology/concept_graph.json:700-725`) and `Ext(ℛ)` (`Rᵢ′ ⊑ ℛᵢ(...)`, `ontology/concept_graph.json:1285-1310`), and tagged all external security/systems vocabulary (`taint`, `sanitizer`, `declassification`, `least privilege`, `obfuscated`, `adversarial`) `[external]` across `U0` projections. |
| `F-CJ-104`, `F-OJ-G1-006`, `F-FJ-010` | `BLOCKING` | `REMEDIATED` | Added inline `(BKL-013)`..`(BKL-024)` pointers across `appendix-a-posets-lattices-fixed-points.md:107,160,218,273,319,348`, `appendix-b-induction-and-coinduction.md:121,144,153,241`, `appendix-c-graphs-dfsf-and-rpo.md:28,92,106,154,255,319,336`, `ontology/notation_index.md:139,485`, and `issue_refs` on all affected `U0` nodes in `ontology/concept_graph.json` (`C6.7` = 12/12 covered). |
| `F-CJ-105`, `F-FJ-013` (locators) | `BLOCKING` | `REMEDIATED` | Replaced abbreviated `App. A/B/C` locators with full `Appendix A/B/C` and `Appendix A/B/C Concluding Remarks` forms, removed parenthesised multi-page `pp.` companion ranges, and replaced meta-convention placeholders with concrete canonical citations in `RAW_SHARD_00_appendices.md:8-18`, `ontology/notation_index.md:7`, `appendix-a-posets-lattices-fixed-points.md:6-17,384`, `appendix-b-induction-and-coinduction.md:6-17,275`, and `appendix-c-graphs-dfsf-and-rpo.md:6-18,388`. |
| `F-CJ-106`, `F-OJ-G1-001`, `F-FJ-001` | `BLOCKING` | `REMEDIATED` | Explicitly stated the Descending Chain Condition hypothesis on Display `(A.3)` in `knowledge/skills/ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md:199-202`. |
| `F-CJ-107`, `F-OJ-G1-005`, `F-FJ-009` | `BLOCKING` | `REMEDIATED` | Updated `issues/backlog/BKL-017.md:3,22,34` (and `appendix-c-graphs-dfsf-and-rpo.md:90-93`) to confirm `Example C.6` holds syntactically and unconditionally for all `WHILE` statements, scoping missing backward exit handles to general CFGs `[external]` with syntactic exit-less sink loops; updated `issues/backlog/BKL-015.md:33-35` to distinguish productive constructor-guarded coinduction `[external]` from well-founded decrease (`lfp = gfp`). |
| `F-OJ-G1-002`, `F-FJ-003` | `BLOCKING` | `REMEDIATED` | Separated ACC finite stabilisation (`∃n : fⁿ(⊥) = lfp(f)`) from continuity chain-supremum equality (`⨆ₙ fⁿ(⊥) = lfp(f)`), removed unprinted `"non-constructive"` attribution, and replaced `"only under"`/`"needs"` with sufficient phrasing across `RAW_SHARD_00_appendices.md:346,996`, `appendix-a-posets-lattices-fixed-points.md:299-306,351-352`, and `ontology/concept_graph.json:864-888`. |
| `F-OJ-G1-003`, `F-FJ-004`, `F-FJ-005` | `BLOCKING` | `REMEDIATED` | Restored `meet-closed (Moore family)` and `affine` in `RAW_SHARD_00_appendices.md:146-152`; restored `total f : L → L` and sufficient phrasing across `RAW_SHARD_00_appendices.md:994,1004` (`G-U0-12`, `G-U0-22`), `appendix-a-posets-lattices-fixed-points.md:348`, and `appendix-b-induction-and-coinduction.md:241-242`. |
| `F-FJ-002`, `F-OJ-G1-007` | `BLOCKING` | `REMEDIATED` | Tagged `Example A.3` failing glb witnesses and the `→` disambiguation note `[derived]`, documented `[derived]` in header conventions, and split `[U0:A.2-a]` (`p. 397`) from `[U0:A.2-b..d]` (`p. 398`) in `appendix-a-posets-lattices-fixed-points.md:9,88-90,160-161,372-373`. |
| `F-FJ-006`, `F-OJ-G1-004` (`BKL-018`) | `BLOCKING` | `REMEDIATED` | Restored `"uniquely labelled"` on `Example C.13` and cited start page `p. 425` (`PDF p. 440`) across `ontology/concept_graph.json:1847-1878`, `appendix-c-graphs-dfsf-and-rpo.md:254-259,355`, and `issues/backlog/BKL-018.md:12,22,29`. |
| `F-FJ-008`, `F-CJ-109`, `F-OJ-G1-008` | `BLOCKING` | `REMEDIATED` | Updated `ontology/notation_index.md` (`:161-163` populated `N3-029` + anomaly #12 at `:524` and `N3-031`; `:460` `U-08` `p. 397`; `:467` `U-15` indexed `Qᵢ` p. 409 vs unindexed `Q = lfp(𝒬)` §B.3 p. 411; `:485-486` added `U-33` `?` and `U-34` `𝒮(S)` plus collision rows). |
| `F-CJ-108`, `F-OJ-G1-010`, `F-FJ-014` | `PREFERENCE` | `REMEDIATED` | Updated `appendix-c-graphs-dfsf-and-rpo.md` (`:31` `Example C.2` p. 417 start; `:88` `[U0:C.1-i]` body anchor; `:128` `Reverse postorder (C.2)` heading; `:264-267,356` `Corollary C.14` strict `<` derivation via `Lemma C.12` + `Corollary C.11` `[derived]`; `:348` `[derived]` tag; `:377-378` `Example C.7` p. 422 / `Figure C.2` p. 423). |
| `F-OJ-G1-009`, `F-FJ-013` (App B) | `PREFERENCE` | `REMEDIATED` | Clarified italic `Q₁ ⊑ Q₂` vs sans `Q₀..Q₃`, bold `D`, and strict-decrease `≻` vs weak-stabilisation DCC phrasing in `appendix-b-induction-and-coinduction.md:81-85,121-122,153,248`. |
| `F-OJ-G1-012` | `PREFERENCE` | `REMEDIATED` | Tightened discrete `ℕ → {0 ⊑ 1}` (`BKL-013.md:32`), non-handle cycle scope (`BKL-016.md:3,31`), `Figure C.3` `d(G,T)=1` note (`BKL-018.md:34`), Lemma A.9 hypotheses (`BKL-022.md:22`), directed `A ⊆ N × N` opposite-edge note (`BKL-023.md:22`), and `pp. 86, 244` citations (`BKL-024.md:12,29-30`). |
| `F-OJ-G1-013` | `PREFERENCE` | `REMEDIATED` | Removed `[external]` from printed `"strong bisimulation"`, noted displays `(B.1)–(B.5)` in Appendix B count, and removed `"only"` overclaims in `G-U0-12, 40, 41, 42` (`RAW_SHARD_00_appendices.md:581,599,994,1022-1024`). |
| `F-CJ-110`, `F-FJ-015`, `F-FJ-016` | `PREFERENCE` | `REMEDIATED` | Added `ppa.notation.index` (`L3`, `ontology/concept_graph.json:1990`), `U9` `corresponds_to` `basis` edges (`ontology/concept_graph.json:755-845`), `Example A.3` & `f : L → L` binder (`ontology/concept_graph.json:225,876`), and cross-referenced all 45 `G-U0-01..45` IDs (`gotcha_coverage` = 0 Unit 0 warnings). |

- 2026-11-19 Gate #1 Round 2 `[ALIGNED gate1-v2]` across all 3 independent review tracks (`P-SWE`, `P-ARCH`, `P-CYBER`): all R1 findings withdrawn, 0 sustained blocking/hard-block findings (`0` `G-U0-01..45` drops, `7/7` Appendix A/C tables & figures cited, `12/12` `BKL-013..024` covered, `appendix-c-graphs-dfsf-and-rpo.md` promoted; `F-CJ-G1R2-001` preference noted).

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W0-01, ISS-W0-02, ISS-W0-03; blocks: ISS-W1-02
- `corpus/shards/RAW_SHARD_00_appendices.md`
- `ontology/notation_index.md`
- `ontology/concept_graph.json`
- `knowledge/skills/ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md`
- `knowledge/skills/ppa-program-analysis/references/appendix-b-induction-and-coinduction.md`
- `knowledge/skills/ppa-program-analysis/references/appendix-c-graphs-dfsf-and-rpo.md`
- Backlog items: `BKL-013` through `BKL-024`

## Verification Receipts

- `python3 -B scripts/validate_ppa_knowledge.py`: `PASS` on all Unit 0 checks (`0` Unit 0 `gotcha_coverage` warnings across `G-U0-01..45`; `C1.5` = `7/7` Appendix A/C tables & figures cited; `C6.7` = `12/12` `BKL-013..024` referenced in `knowledge/` and `ontology/`).
- `python3 -B scripts/issue_ctl.py validate`: `PASS (0 errors)`.
- `python3 -B scripts/check_portability_hygiene.py .`: `PASS (0 findings)`.
- 2026-11-19 [closed] Gate #1 3/3 `[ALIGNED gate1-v2]` confirmed; Unit 0 closure validated (`RAW_SHARD_00_appendices.md`, `appendix-{a,b,c}*.md`, `ontology/notation_index.md`, `0` Unit 0 `gotcha_coverage` warnings).
