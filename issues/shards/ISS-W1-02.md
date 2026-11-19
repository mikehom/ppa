---
id: ISS-W1-02
title: "W1-2 Unit 1: Chapter 1 Introduction, master router + Gate #2"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-1, gate]
milestone: W1
parent_issue: EPIC-001
depends_on: [ISS-W1-01]
blocks: [ISS-W2-01, ISS-W2-02]
ppa_scope: ["Preface (book pp. V–X; PDF pp. 5–10)", "§1.1 The Nature of Program Analysis (book pp. 1–3; PDF pp. 21–23)", "§1.2 Setting the Scene (book pp. 3–5; PDF pp. 23–25)", "§1.3 Data Flow Analysis (book pp. 5–10; PDF pp. 25–30)", "§1.4 Constraint Based Analysis (book pp. 10–13; PDF pp. 30–33)", "§1.5 Abstract Interpretation (book pp. 13–17; PDF pp. 33–37)", "§1.6 Type and Effect Systems (book pp. 17–25; PDF pp. 37–45)", "§1.7 Algorithms (book pp. 25–26; PDF pp. 45–46)", "§1.8 Transformations (book pp. 27–29; PDF pp. 47–49)", "Chapter 1 End Matter (book pp. 29–33; PDF pp. 49–53)"]
altitudes: [L0, L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: null
---

## Summary

Extract the four approaches overview (DFA, CBA, AI, TES), algorithms, transformations, and Preface scope boundaries; author the L0 master router (`ppa-program-analysis/SKILL.md`), L0 ambient orientation (`ppa-foundations.md`), and L1 Chapter 1 reference (`chapter-1-five-formulations.md`); wire `U1` concept nodes and unification edge; run Gate #2.

## Source Citations & Grounding

- `[PPA Preface, p. VI] (book p. VI; PDF p. 6)`
- `[PPA §1.1, p. 1] (book p. 1; PDF p. 21)` through `[PPA §1.1, p. 3] (book p. 3; PDF p. 23)`
- `[PPA §1.2, p. 3] (book p. 3; PDF p. 23)` through `[PPA §1.2, p. 5] (book p. 5; PDF p. 25)`
- `[PPA §1.3, p. 5] (book p. 5; PDF p. 25)` through `[PPA §1.3.2, p. 10] (book p. 10; PDF p. 30)`
- `[PPA §1.4, p. 10] (book p. 10; PDF p. 30)` through `[PPA §1.4, p. 13] (book p. 13; PDF p. 33)`
- `[PPA §1.5, p. 13] (book p. 13; PDF p. 33)` through `[PPA §1.5, p. 17] (book p. 17; PDF p. 37)`
- `[PPA §1.6, p. 17] (book p. 17; PDF p. 37)` through `[PPA §1.6.2, p. 25] (book p. 25; PDF p. 45)`
- `[PPA §1.7, p. 25] (book p. 25; PDF p. 45)` through `[PPA §1.7, p. 26] (book p. 26; PDF p. 46)`
- `[PPA §1.8, p. 27] (book p. 27; PDF p. 47)` through `[PPA §1.8, p. 29] (book p. 29; PDF p. 49)`
- `[PPA Chapter 1 Concluding Remarks, p. 29] (book p. 29; PDF p. 49)` through `[PPA Exercise 1.11, p. 33] (book p. 33; PDF p. 53)`
- Tables in scope: `[PPA Table 1.1, p. 4] (book p. 4; PDF p. 24)`, `[PPA Table 1.2, p. 19] (book p. 19; PDF p. 39)`, `[PPA Table 1.3, p. 21] (book p. 21; PDF p. 41)`, `[PPA Table 1.4, p. 24] (book p. 24; PDF p. 44)`, `[PPA Table 1.5, p. 26] (book p. 26; PDF p. 46)`, `[PPA Table 1.6, p. 27] (book p. 27; PDF p. 47)`
- Figures in scope: `[PPA Figure 1.1, p. 2] (book p. 2; PDF p. 22)`, `[PPA Figure 1.2, p. 6] (book p. 6; PDF p. 26)`, `[PPA Figure 1.3, p. 15] (book p. 15; PDF p. 35)`
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; blank verso p. 34 is omitted from the PDF).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per `architecture/ARCHITECTURE.md` §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pages 1–33 plus Preface p. VI (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 6 tables and 3 figures in Chapter 1 are anchored across `L3`, `L1`, and `ontology/concept_graph.json` (`C1.5` = 0 missing)
- [x] Artifact `corpus/shards/RAW_SHARD_01_intro.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `knowledge/skills/ppa-program-analysis/SKILL.md` (`76` lines, `< 100`L) and `references/chapter-1-five-formulations.md` (`446` lines, `<= 450`L) pass `scripts/validate_ppa_knowledge.py` with full channel independence
- [x] Artifact `knowledge/ambient-context/ppa-foundations.md` (`190` lines, `80–250`L) passes `scripts/validate_ppa_knowledge.py`
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (Round 2 ready)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- **Round 1 (`gate2-v1`)**: Three independent adversarial evaluators audited all Unit 1 deliverables against rendered `ppa.pdf` page images (`PDF pp. 5–10, 21–53`) and `architecture/CONFORMANCE_SPEC.md`, returning `[DISAGREE]` with `0` `HARD_BLOCK` and remediable `BLOCKING` / `PREFERENCE` findings mapped 1-to-1 below.
- **Round 1 Remediation (`gate2-v2` candidate)**: All Unit 1 `BLOCKING` and `PREFERENCE` findings were resolved directly across `corpus/shards/RAW_SHARD_01_intro.md`, `knowledge/skills/ppa-program-analysis/{SKILL.md,README.md,evals/cases.yaml,references/chapter-1-five-formulations.md}`, `knowledge/ambient-context/ppa-foundations.md`, `ontology/notation_index.md`, and `ontology/concept_graph.json`.

### Rebuttal & Attribution Summary (Gate #2)

| Finding ID(s) | Severity | Disposition | Verification Anchor & Remediation Summary |
| :--- | :--- | :--- | :--- |
| `F-CJ-201` | `BLOCKING` | `REMEDIATED` | Enforced `ARCHITECTURE.md` §4.3 channel independence in `knowledge/skills/ppa-program-analysis/SKILL.md:23-27,61-72` and `README.md:17-27`: removed the `../../ambient-context/ppa-foundations.md` relative filesystem link and routed safe-approximation and soundness-direction lookups inside the skill package to `references/chapter-1-five-formulations.md` (§1–§2). |
| `F-CJ-202`, `F-OJ-G2-009` | `BLOCKING` | `REMEDIATED` | Rewrote `ppa.solvers.chaotic-iteration.projections.cs_theory` (`ontology/concept_graph.json:2791-2816`) to state that `Table 1.5` updates only stale components `RD_j ≠ F_j(RD⃗)` from `∅⃗`, so every step strictly increases `RD⃗` and reaches `lfp(F)` on a finite lattice without fairness (scoping fairness to unguarded no-op schedules `[external]`). |
| `F-CJ-203` | `BLOCKING` | `REMEDIATED` | Upgraded `ppa.dfa.rd-equational <-> ppa.dfa.rd-constraint-formulation` (`ontology/concept_graph.json:2345-2365,2430-2450`) from `related_to` to symmetric `corresponds_to` carrying `basis` (`unification_id: "U1"`, `p. 10 / PDF p. 30` citation, `conditions`, `differs`). |
| `F-CJ-204`, `F-OJ-G2-003`, `F-FJ-007` | `BLOCKING` | `REMEDIATED` | Added inline `(BKL-028)`, `(BKL-029)`, `(BKL-031)`, `(BKL-034)`, and `(BKL-035)` pointers across `chapter-1-five-formulations.md:40,120,227,334,438-444`, added `U-33` (`?`) and collision rows in `ontology/notation_index.md:485,545`, and populated `issue_refs` on all affected `U1` nodes in `ontology/concept_graph.json` (`C6.7` = 11/11 covered). |
| `F-CJ-205` | `BLOCKING` | `REMEDIATED` | Rewrote nested bibliography brackets in `RAW_SHARD_01_intro.md:1094-1098` to zero-nesting `[27] [PPA Bibliography, p. 441] (book p. 441; PDF p. 454)` form, added `[PPA Preface, p. VI] (book p. VI; PDF p. 6)` in `RAW_SHARD_01_intro.md:21,60,67`, `ppa-foundations.md:163-170`, and `chapter-1-five-formulations.md:385`, and eliminated all parenthesised multi-page `pp.` ranges and placeholder citation strings across `RAW_SHARD_01_intro.md:8,18`, `chapter-1-five-formulations.md:6-10`, `ppa-foundations.md:9-10`, and `README.md:35-37`. |
| `F-CJ-206` | `BLOCKING` | `REMEDIATED` | Appended `G-U1-33` covering Preface p. VI scope exclusions (`EC-08`) to `RAW_SHARD_01_intro.md:1314`, and tagged `taint` and `capabilities` `[external]` in `ppa.intro.four-approaches.projections.cyber` (`ontology/concept_graph.json:2160`). |
| `F-CJ-207`, `F-OJ-G2-001`, `F-FJ-001` | `BLOCKING` | `REMEDIATED` | Corrected `RAW_SHARD_01_intro.md:1290` (`G-U1-09`), `ontology/concept_graph.json:2408-2416` (`ppa.dfa.rd-constraint-formulation`), and `ppa-foundations.md:92-95` to state that every equation solution solves the constraints (`Fix(F) ⊆ Red(F)`), inclusions admit extra reductive non-fixed-point solutions, and both systems share the same least solution. |
| `F-OJ-G2-002`, `F-FJ-003` | `BLOCKING` | `REMEDIATED` | Updated `knowledge/ambient-context/ppa-foundations.md:58-96` (and added **Soundness direction** at `chapter-1-five-formulations.md:22-24`) to scope `⊆`-least solutions to `§§1.3–1.5` may-analyses, explicitly contrast `Table 1.3` must-component `X` (smaller `X` safe, larger `X` more precise, enlarging `X` unsound) and `§1.6` derivation systems, note printed `"semantically unsound"` (`p. 8`), and tag the defect-finding vs absence-proving framing `[external]`. |
| `F-OJ-G2-004`, `F-FJ-004`, `F-FJ-005` | `BLOCKING` | `REMEDIATED` | In `chapter-1-five-formulations.md`: documented `[derived]` and meta-rule separator `⟹` (`:9`), replaced overloaded meta-`⊢` with `⟹` across `Tables 1.2, 1.3, 1.4, 1.6` (`:264-267,295-298,327-328,372-376`), tagged `[derived]` on `:128` and `:384`, and cited `[PPA §1.6.2, p. 24] (book p. 24; PDF p. 44)` alongside `p. 25` for `[var]`/`[fn]` call-by-value empty effects (`:332-335`). |
| `F-FJ-002`, `F-CJ-210`, `F-OJ-G2-007`, `F-FJ-010` | `BLOCKING` | `REMEDIATED` | Split Chapter 1 Concluding Remarks `"Semantics directed analysis"` (denotational/logic-based) from Preface p. VI exclusions (`projection analysis`, `Stone dualities`, `"single static assignment form"`) in `knowledge/skills/ppa-program-analysis/SKILL.md:57-58`, and removed the false-negative substring blacklist in `evals/cases.yaml:7-13`. |
| `F-FJ-006`, `F-OJ-G2-005` | `BLOCKING` | `REMEDIATED` | Restored `"more advanced imperative, functional and object-oriented languages"` in `chapter-1-five-formulations.md:167-168` and `RAW_SHARD_01_intro.md:1293` (`G-U1-12`). |
| `F-OJ-G2-006`, `F-FJ-011` | `PREFERENCE` | `REMEDIATED` | Scoped `Chapter 1 Opening` `cs_theory` projection (`RAW_SHARD_01_intro.md:70-71`), cited `p. 4` for operators (`:177`) and `p. 21` for `X`/`RD` (`:760`), replaced `"only because"` in `G-U1-13`/`G-U1-26` (`:1294,1307`), and restored `y ∈ FV(a)` and `FV(a) = ∅` in `G-U1-28` (`:1309`). |
| `F-FJ-008` | `PREFERENCE` | `REMEDIATED` | Scoped `12` in `ppa.dfa.rd-equational.formal_summary` to the 6-block `Example 1.1` factorial program (`ontology/concept_graph.json:2315`) and added `chapter-1-five-formulations.md` to `artifact_refs` of `ppa.intro.safe-approximation` and `ppa.intro.semantics-based` (`ontology/concept_graph.json:2092,2138`). |
| `F-FJ-009`, `F-OJ-G2-008` | `PREFERENCE` | `REMEDIATED` | Aligned phrasing and citations on `pp. 2, 3, 19, 25, Preface p. VI` in `ppa-foundations.md:40-44,121-126,163-170`; retained plain non-linked skill paths at `ppa-foundations.md:172-186` to preserve `ARCHITECTURE.md` §4.3 channel independence (`F-CJ-201`) and `C3.9`. |
| `F-CJ-208`, `F-CJ-209`, `F-FJ-012`, `F-FJ-013` | `PREFERENCE` | `REMEDIATED` | Compacted `chapter-1-five-formulations.md` to `446` LF lines (`<= 450` ceiling), added `Var⋆, Lab⋆` non-emptiness (`:311`) and `Exercise 1.9` `[z:=y+x]^3` (`:381`), and cross-referenced all 33 `G-U1-01..33` IDs (`gotcha_coverage` = 0 Unit 1 warnings). |
| `F-OJ-G2-010` | `PREFERENCE` | `DEFERRED (W7-1)` | Router `evals/cases.yaml` (`16` cases) is valid on disk; extending `scripts/ppa_artifact_rules.py:check_evals` to also run on `ROUTER_SKILL` touches frozen Wave 0 tooling and is queued for `ISS-W7-01` conformance verifier integration. |

- 2026-11-19 Gate #2 Round 2 `[ALIGNED gate2-v2]` across all 3 independent review tracks (`P-SWE`, `P-ARCH`, `P-CYBER`): all R1 findings withdrawn, 0 sustained blocking/hard-block findings (`0` `G-U1-01..33` drops, `9/9` Ch 1 tables & figures cited, `11/11` `BKL-025..035` covered, `U1` symmetric `corresponds_to`; `F-CJ-G2R2-001..002` & `F-OJ-G2-R2-001..002` preferences noted).

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W1-01; blocks: ISS-W2-01, ISS-W2-02
- `corpus/shards/RAW_SHARD_01_intro.md`
- `knowledge/skills/ppa-program-analysis/SKILL.md`
- `knowledge/skills/ppa-program-analysis/README.md`
- `knowledge/skills/ppa-program-analysis/evals/cases.yaml`
- `knowledge/skills/ppa-program-analysis/references/chapter-1-five-formulations.md`
- `knowledge/ambient-context/ppa-foundations.md`
- `ontology/concept_graph.json`
- Backlog items: `BKL-025` through `BKL-035`

## Verification Receipts

- `python3 -B scripts/validate_ppa_knowledge.py`: `PASS` on all Unit 1 checks (`SKILL.md` `76`L, `chapter-1-five-formulations.md` `446`L, `ppa-foundations.md` `190`L; `0` Unit 1 `gotcha_coverage` warnings across `G-U1-01..33`; `C1.5` = `9/9` Chapter 1 tables & figures cited; `C6.7` = `11/11` `BKL-025..035` referenced in `knowledge/` and `ontology/`).
- `python3 -B scripts/issue_ctl.py validate`: `PASS (0 errors)`.
- `python3 -B scripts/check_portability_hygiene.py .`: `PASS (0 findings)`.
- 2026-11-19 [closed] Gate #2 3/3 `[ALIGNED gate2-v2]` confirmed; Unit 1 closure validated (`RAW_SHARD_01_intro.md`, `SKILL.md` `76L`, `chapter-1-five-formulations.md` `446L`, `ppa-foundations.md` `190L`, `0` Unit 1 `gotcha_coverage` warnings).
