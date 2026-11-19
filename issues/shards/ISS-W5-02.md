---
id: ISS-W5-02
title: "W5-2 Ch 5b §5.4–5.5 effects, exceptions, regions, behaviours + Gate #7"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-5, gate]
milestone: W5
parent_issue: EPIC-001
depends_on: [ISS-W5-01]
blocks: [ISS-W5-03]
ppa_scope: ["§5.4 Effects (book pp. 319–338; PDF pp. 336–355)", "§5.5 Behaviours (book pp. 339–364; PDF pp. 356–380)"]
altitudes: [L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: 89
---

## Summary

Extract side-effect, exception, region-inference and communication analyses; synthesize the Chapter 5 skill; refactor; Gate #7.

## Source Citations & Grounding

- §5.4 Effects (book pp. 319–338; PDF pp. 336–355)
- §5.5 Behaviours (book pp. 339–364; PDF pp. 356–380)
- Tables in scope: Table 5.9 (p. 322/PDF 339), Table 5.10 (p. 328/PDF 345), Table 5.11 (p. 334/PDF 351), Table 5.12 (p. 337/PDF 354), Table 5.13 (p. 338/PDF 355), Table 5.14 (p. 341/PDF 358), Table 5.15 (p. 343/PDF 360), Table 5.16 (p. 346/PDF 363), Table 5.17 (p. 347/PDF 364), Table 5.18 (p. 348/PDF 365)
- Figures in scope: Figure 5.1 (p. 331/PDF 348), Figure 5.2 (p. 340/PDF 357)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 319–364 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 10 tables and 2 figures in book pp. 319–364 are anchored (no omissions)
- [x] Artifact `knowledge/skills/ppa-types-effects-and-regions/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifacts `knowledge/ambient-context/ppa-types-effects-and-regions.md` and `references/{annotated-types-and-cfa-soundness,inference-unification-and-subtyping,effects-exceptions-regions-and-behaviours}.md` exist and pass `scripts/validate_ppa_knowledge.py`
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Chapter 5b extraction (`corpus/shards/RAW_SHARD_05b_effects_regions_behaviours.md`, `1,668L`, `26/26` `G-U5b-01..26`, `Tables 5.9–5.18`, `Figures 5.1–5.2`, `Mini Projects 5.1–5.5`, `Exercises 5.1–5.15`) and full Chapter 5 knowledge package (`ppa-types-effects-and-regions/` `318L` `SKILL.md` / `289L`/`283L`/`275L` `L1` refs, `ppa-types-effects-and-regions.md` `136L`, `18` `ppa.tes.*` nodes in `131`-node `concept_graph.json`, `U-54..U-60` + `π`/`FV` notation, `BKL-073..082` + reconciled `BKL-004/009/011/026/030/031`, `REF-005`) promoted; staged for Gate #7 (`gate7-v1`).
- 2026-11-19 Gate #7 Round 1 reviews (`P-SWE`, `P-ARCH`, `P-CYBER`) returned `[DISAGREE gate7-v1]` (`0` `HARD_BLOCK`, `6` `BLOCKING` across tracks / `4` distinct defects, `4` `PREFERENCE`). Round 1 -> Round 2 (`gate7-v2`) 1-to-1 remediation applied across all `10` findings:
- 2026-11-19 Gate #7 Round 2 (`gate7-v2`): unanimous `3/3 [ALIGNED gate7-v2]` across `P-SWE`, `P-CYBER`, and `P-ARCH` (`0` `HARD_BLOCK`, `0` `BLOCKING`, `0` `PREFERENCE`; #254, #255, #256; all `10/10` findings verified resolved with zero regressions).

| Finding ID | Track | Severity | Disposition & Action Taken | Target Artifact(s) |
| :--- | :--- | :--- | :--- | :--- |
| `F-OJ-701` | `P-SWE` | `BLOCKING` | Deleted `\widehat{τ} com φ` from `U-59`, fixed `:= π` to postfix `π:=` in `U-57`, corrected `U-55` `e_{1}[x ↦ e_{2}]` to capture-free closed substitution (`e_{2}` closed; no bound-variable renaming required, [PPA §5.2.1, p. 293] (book p. 293; PDF p. 310)), and updated `U-54` `⊢_{CA}` to `Γ̂ ⊢_{CA} e : σ̂ & φ` | `ontology/notation_index.md` |
| `F-OJ-702` | `P-SWE` | `BLOCKING` | Replaced `[83, 160, 13]` with `[83, 160, 161]` at both Chapter 5 `L1` subtyping sites | `inference-unification-and-subtyping.md` |
| `F-OJ-703` | `P-SWE` | `PREFERENCE` | Clarified `([71], [external: Palsberg-O'Keefe 1995])` as `([71] Heintze; [external: Palsberg–O'Keefe 1995])` across `L1` and both symmetric `concept_graph.json` nodes | `inference-unification-and-subtyping.md`, `ontology/concept_graph.json` |
| `F-OJ-704` | `P-SWE` | `PREFERENCE` | Added `Λ` (cross-referenced to `N2-026`) in `U-59` and `[PPA Table 5.11, p. 334] (book p. 334; PDF p. 351)` for `ς ⧹⧹ \vec{rn}` in `U-58` | `ontology/notation_index.md` |
| `F-FJ-701` | `P-ARCH` | `BLOCKING` | Remediated jointly with `F-OJ-701` and `F-CJ-701`: removed fabricated `\widehat{τ} com φ` constructor and gloss from `U-59` | `ontology/notation_index.md` |
| `F-FJ-702` | `P-ARCH` | `BLOCKING` | Remediated jointly with `F-OJ-701`: changed `:= π` to postfix `π:=` in `U-57` citing `[PPA Table 5.9, p. 322] (book p. 322; PDF p. 339)` | `ontology/notation_index.md` |
| `F-FJ-703` | `P-ARCH` | `PREFERENCE` | Remediated jointly with `F-OJ-701`: aligned `U-54` `⊢_{CA}` to `Γ̂ ⊢_{CA} e : σ̂ & φ` ([PPA §5.5.1, p. 345] (book p. 345; PDF p. 362); [PPA Table 5.16, p. 346] (book p. 346; PDF p. 363)) and split line `2` `@decision` plural span into singular `book p. 429; PDF p. 443` through `book p. 432; PDF p. 446` | `ontology/notation_index.md` |
| `F-CJ-701` | `P-CYBER` | `BLOCKING` | Remediated jointly with `F-OJ-701`, `F-FJ-701`, `F-OJ-704`: removed `\widehat{τ} com φ`, added `Λ`, and cited `[PPA Table 5.14, p. 341] (book p. 341; PDF p. 358)` alongside `[PPA §5.5.1, p. 344] (book p. 344; PDF p. 361)` in `U-59` | `ontology/notation_index.md` |
| `F-CJ-702` | `P-CYBER` | `BLOCKING` | Applied `P2` `[external]` attribution across Chapter 5 `L0`–`L3` and W5 evals: replaced `Tofte-Talpin` in `SKILL.md` YAML `description` with `stack-based region inference`, tagged `([175, 176], [external: Tofte–Talpin])`, `([174], [external: Tofte–Birkedal])`, and `[2] [external: Agesen]` across `SKILL.md`, `README.md`, `effects-exceptions-regions-and-behaviours.md` (heading slug synced in `concept_graph.json`), `knowledge/ambient-context/ppa-types-effects-and-regions.md`, `RAW_SHARD_05b_effects_regions_behaviours.md`, `concept_graph.json`, and W5 sibling `evals/cases.yaml` | `ppa-types-effects-and-regions/**`, `ppa-types-effects-and-regions.md`, `RAW_SHARD_05b_effects_regions_behaviours.md`, `ontology/concept_graph.json`, W5 `evals/cases.yaml` |
| `F-CJ-703` | `P-CYBER` | `PREFERENCE` | Updated `U-60` to `` `LAnn`, `num^{φ}` (`scale BASE base`) `` (noting `num^{σ BASE β}` on polymorphic operator schemes) and added `[PPA Mini Project 5.4, p. 356] (book p. 356; PDF p. 373)` alongside `[PPA Mini Project 5.5, p. 358] (book p. 358; PDF p. 375)` | `ontology/notation_index.md` |

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W5-01; blocks: ISS-W5-03
- `corpus/shards/RAW_SHARD_05b_effects_regions_behaviours.md`
- `knowledge/skills/ppa-types-effects-and-regions/SKILL.md`
- `knowledge/skills/ppa-types-effects-and-regions/references/annotated-types-and-cfa-soundness.md`
- `knowledge/skills/ppa-types-effects-and-regions/references/inference-unification-and-subtyping.md`
- `knowledge/skills/ppa-types-effects-and-regions/references/effects-exceptions-regions-and-behaviours.md`
- `knowledge/ambient-context/ppa-types-effects-and-regions.md`
- `ontology/concept_graph.json`
- `ontology/notation_index.md`
- `issues/refactors/REF-005.md`
- `issues/backlog/BKL-004.md`, `issues/backlog/BKL-009.md`, `issues/backlog/BKL-011.md`, `issues/backlog/BKL-026.md`, `issues/backlog/BKL-030.md`, `issues/backlog/BKL-031.md`
- `issues/backlog/BKL-073.md` .. `issues/backlog/BKL-082.md`

## Verification Receipts

- 2026-11-19 [in_progress] Unit 5b shard (`1,668L`, `26/26` `G-U5b-01..26`, `Tables 5.9–5.18`, `Figures 5.1–5.2`), `ppa-types-effects-and-regions/` (`318L` SKILL, `289L`/`283L`/`275L` refs), `ppa-types-effects-and-regions.md` (`136L`), `131`-node `concept_graph.json`, `U-54..U-60` notation, `BKL-073..082` + `BKL-004/009/011/026/030/031`, and `REF-005` promoted and staged for Gate #7 (`gate7-v1`).
- 2026-11-19 [in_progress] Gate #7 Round 1 remediation (`gate7-v2`): `10/10` findings (`F-OJ-701..704`, `F-FJ-701..703`, `F-CJ-701..703`) resolved across `ontology/notation_index.md` (`U-54..U-60` + header comment), `inference-unification-and-subtyping.md` (`[83, 160, 161]` + `[71] Heintze`), Chapter 5 `L0`–`L3` + `concept_graph.json` + W5 `evals/cases.yaml` `P2` `[external]` attribution (`Tofte`, `Talpin`, `Birkedal`, `Agesen`), and `REF-005.md`; ready for Gate #7 Round 2.
- 2026-11-19 [aligned] Gate #7 Round 2 unanimous 3/3 [ALIGNED gate7-v2] across P-SWE, P-CYBER, P-ARCH (#254, #255, #256).
- 2026-11-19 [closed] Gate #7 closed after post-remediation validators, hygiene, export parity, and 47/47 unittest passes.
