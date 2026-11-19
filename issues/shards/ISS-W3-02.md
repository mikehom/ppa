---
id: ISS-W3-02
title: "W3-2 Ch 3b §3.5–3.6 CFA+DFA, k-CFA, CPA, synthesis + Gate #5"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-3, gate]
milestone: W3
parent_issue: EPIC-001
depends_on: [ISS-W3-01]
blocks: [ISS-W4-01]
ppa_scope: ["§3.5 Adding Data Flow Analysis (book pp. 182–188; PDF pp. 200–206)", "§3.6 Adding Context Information (book pp. 189–210; PDF pp. 207–227)"]
altitudes: [L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: 59
---

## Summary

Extract combined control/data flow lattices, uniform k-CFA and context information; synthesize the Chapter 3 skill; refactor; Gate #5.

## Source Citations & Grounding

- §3.5 Adding Data Flow Analysis (book pp. 182–188; PDF pp. 200–206)
- §3.6 Adding Context Information (book pp. 189–210; PDF pp. 207–227)
- Tables in scope: Table 3.8 (p. 184/PDF 202), Table 3.9 (p. 188/PDF 206), Table 3.10 (p. 192/PDF 210)
- Figures in scope: Figure 3.6 (p. 185/PDF 203)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 182–210 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 3 tables and 1 figure in book pp. 182–210 are anchored (no omissions)
- [x] Artifact `knowledge/skills/ppa-control-flow-and-constraints/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifacts `knowledge/ambient-context/ppa-cfa-and-constraints.md` and `references/{cfa-core-and-coinduction,constraint-generation-and-cubic-solver,polyvariant-kcfa-cpa-and-dfa}.md` exist and pass `scripts/validate_ppa_knowledge.py`
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Chapter 3b extraction (`corpus/shards/RAW_SHARD_03b_kcfa_cpa.md`, `1,106` lines, `30/30` `G-U3b-01..30`, `3/3` `Tables 3.8–3.10`, `1/1` `Figure 3.6`, `9/9` `Statements 3.26–3.34`, `Mini Projects 3.1–3.4`, `Exercises 3.1–3.17`) and full Chapter 3 knowledge package (`ppa-control-flow-and-constraints/`, `ppa-cfa-and-constraints.md`, `16` new `ppa.cfa.*` concepts, `BKL-051..062`, `REF-003`) promoted for Gate #5 (`gate5-v1`).
- 2026-11-19 Round 1 (`gate5-v1`): three-track adversarial panel returned `[DISAGREE]` across `22` findings (`P-SWE`: `5` `BLOCKING`, `2` `PREFERENCE`; `P-ARCH`: `5` `BLOCKING`, `3` `PREFERENCE`; `P-CYBER`: `6` `BLOCKING`, `1` `PREFERENCE`). Remediated all `22/22` findings across `L0`–`L3`, `ontology/`, and `issues/backlog/` (`gate5-v2`).
- 2026-11-19 Round 2 (`gate5-v2`): unanimous `3/3 [ALIGNED gate5-v2]` across `P-SWE`, `P-ARCH`, and `P-CYBER` (`0` `HARD_BLOCK`, `0` `BLOCKING`; #223–#225). Applied all three non-blocking `PREFERENCE` polishes (`F-OJ-508`/`F-CJ-508` single quotes in `BKL-058.md:3` for strict `yaml.safe_load`, `F-FJ-509`/`F-OJ-509`/`F-CJ-509` `new_π` in `SKILL.md:226` & collapsed `[external]` in `polyvariant-kcfa-cpa-and-dfa.md:133-134`).

### Rebuttal & Attribution Summary (Gate #5 Round 1)

| Finding ID | Track | Severity | Disposition & Action Taken | Target Artifact(s) |
| :--- | :--- | :--- | :--- | :--- |
| `F-OJ-501` | `P-SWE` | `BLOCKING` | Fixed `Tables 3.2–3.3` (`[app_fn]`/`[app_fun]` `[x ↦ v₂]` order, `[if₂,₃]`/`[bind₂]` relabelling to `ℓ`, `Example 3.8`, `IExp` branches), `Example 3.3` (3 guesses), `Remark.` p. 145 (`(Var ∪ Lab) → Val̂` & IRs), `Example 3.12` (on `Ex 3.7`), `Mini Project 3.1` `p. 202`, and repurposed `F-U3a-05`/`BKL-052` (no `[app₁]` gap) | `RAW_SHARD_03a_0cfa.md`, `cfa-core-and-coinduction.md`, `BKL-052.md`, `concept_graph.json` |
| `F-OJ-502` | `P-SWE` | `BLOCKING` | Restored Uniform `k`-CFA `Val̂ = 𝒫(Term × CEnv)`, standard `k`-CFA `Cachê = (Lab × CEnv) → Val̂` (`[156, 157, 158]`), Polynomial `k`-CFA `Val̂ = 𝒫(Term × Δ)` (`O(n⁶)` at `k=1`, `p. 195`), verbatim `Table 3.10` `⊨_δ^{ce}`, `Example 3.34` `{(fn y => y^6, ce₀)}`, `[2]` vs `[4]`, and rewrote `BKL-057` around `CEnv` `ce \| FV` & `Ex 3.34` mis-citation (no `ρ̂(x, δ₀)` typo) | `ppa-cfa-and-constraints.md`, `SKILL.md`, `polyvariant-kcfa-cpa-and-dfa.md`, `concept_graph.json`, `BKL-057.md` |
| `F-OJ-503` | `P-SWE` | `BLOCKING` | Fixed `§3.6.2 CPA [app]` `F-U3b-05` (`)` before `^ℓ`, `, δ_b` in `ρ̂(x_i, δ_b)`), `Mini Project 3.1` (`p. 202`, no `[let]`), `Mini Project 3.2` (`p. 203` flat `C(ℓ₁,...,ℓ_n)`), `Mini Project 3.3` (`Label of term * label`), `Mini Project 3.4` (`new_π`/`x := e₀`/`me`, unprinted `[assign]` + `p. 200` `[133]` strong-kill guard), and `Ex 3.2/3.16` | `SKILL.md`, `constraint-generation-and-cubic-solver.md`, `polyvariant-kcfa-cpa-and-dfa.md`, `concept_graph.json`, `BKL-058/060/061/062.md` |
| `F-OJ-504` | `P-SWE` | `BLOCKING` | Fixed `d_c ∈ Data`, `Table 3.8` `[con]` `{d_c}` / `[if]` `d_true`/`d_false`, real `Example 3.27 / Figure 3.6 / Example 3.30 (p. 187) / Example 3.31` terms (`fn y => y^4`, `fn z => 25^6`, `{0}` vs `{0, +}`), Oracle #3, and `evals/cases.yaml` | `polyvariant-kcfa-cpa-and-dfa.md`, `SKILL.md`, `evals/cases.yaml`, `concept_graph.json` |
| `F-OJ-505` | `P-SWE` | `BLOCKING` | Removed bare `⊨` from `notation_index.md` `U-39` (`N1-006` xref) and added `⊨'_{s}`, `⊨'_{D}`, `⊨_{me}`; replaced `U2 -> U5` in `RAW_SHARD_03b`; tagged `[external]` across `L0`–`L3`/graph/BKL (incl. `m-CFA`, `DEXPTIME`, `[2]`/`[9]`/`[156..158]`, `Kleene`, `weak/strong update`) | `notation_index.md`, `RAW_SHARD_03a_0cfa.md`, `RAW_SHARD_03b_kcfa_cpa.md`, `L0`–`L2`, `concept_graph.json`, `BKL-061.md` |
| `F-OJ-506` | `P-SWE` | `PREFERENCE` | Synced bidirectional `Affected concept ids` on `BKL-051`, `BKL-053`, `BKL-062` (`56/56` `BKL` parity) and deduplicated redundant `abstract-0cfa <-> subject-reduction` edge pair | `BKL-051/053/062.md`, `concept_graph.json` |
| `F-OJ-507` | `P-SWE` | `PREFERENCE` | Renumbered `SKILL.md` Procedure 2 step `5. -> 4.` (`U-39` updated cleanly; `U-37` historical W2 note untouched) | `SKILL.md`, `notation_index.md` |
| `F-FJ-501` | `P-ARCH` | `BLOCKING` | Restored Uniform `k`-CFA `Val̂ = 𝒫(Term × CEnv)`, `Table 3.10` `⊨_δ^{ce}`, `Example 3.34` `{(fn y => y^6, ce₀)}`, standard `k`-CFA `Cachê = (Lab × CEnv) → Val̂`, and Polynomial `k`-CFA `Val̂ = 𝒫(Term × Δ)` (`p. 195`) across `L0`–`L2`, Oracle #4, and `concept_graph.json` (`U5` symmetry) | `ppa-cfa-and-constraints.md`, `SKILL.md`, `polyvariant-kcfa-cpa-and-dfa.md`, `concept_graph.json` |
| `F-FJ-502` | `P-ARCH` | `BLOCKING` | Aligned `Example 3.27 / Figure 3.6 / Example 3.31`, Oracle #3, `Table 3.8` (`d_c ∈ Data`, `d_true`/`d_false`), and `evals/cases.yaml` to printed book syntax and output sets | `polyvariant-kcfa-cpa-and-dfa.md`, `SKILL.md`, `evals/cases.yaml`, `concept_graph.json` |
| `F-FJ-503` | `P-ARCH` | `BLOCKING` | Purged fabricated `p. 193` `ρ̂(x, δ₀)`, `p. 197` unbound `e₀`/`Ĉ(ℓ₀, δ)`, and `Ex 3.2`/`3.16` claims; documented genuine `F-U3b-05` (`)` before `^ℓ`, `, δ_b` on `ρ̂(x_i, δ_b)`), `Ex 3.16` `f(x)= e` / `defined in D`, and `Ex 3.17` `"Cartesian Production"` | `polyvariant-kcfa-cpa-and-dfa.md`, `SKILL.md`, `cfa-core-and-coinduction.md`, `concept_graph.json`, `BKL-057/058/062.md` |
| `F-FJ-504` | `P-ARCH` | `BLOCKING` | Corrected `Mini Project 3.1` (`p. 202`, prose line 10 `⊨_s`), `Mini Project 3.2` (`p. 203` flat `C(ℓ₁,...,ℓ_n)`), `Mini Project 3.3` (`Label of term * label`), and `Mini Project 3.4` (`new_π`/`x := e₀`/`me`, unprinted `[assign]` + `p. 200` `[133]`) | `constraint-generation-and-cubic-solver.md`, `polyvariant-kcfa-cpa-and-dfa.md`, `SKILL.md`, `concept_graph.json`, `BKL-060/061.md` |
| `F-FJ-505` | `P-ARCH` | `BLOCKING` | Updated `RAW_SHARD_03a_0cfa.md:11` (`Mini Projects 3.1–3.4`, `Exercises 3.1–3.17`) and enforced `P2` `[external]` tags + `PPA` `Ext`/`Red` terms across `L0`–`L3` and `SKILL.md:3` | `RAW_SHARD_03a_0cfa.md`, `RAW_SHARD_03b_kcfa_cpa.md`, `ppa-cfa-and-constraints.md`, `SKILL.md`, `concept_graph.json` |
| `F-FJ-506` | `P-ARCH` | `PREFERENCE` | Synced `Affected concept ids` in `BKL-051/053/062` (with `Ex 3.6` in `BKL-062`) and deduplicated redundant `subject-reduction <-> abstract-0cfa` edge pair | `BKL-051/053/062.md`, `concept_graph.json` |
| `F-FJ-507` | `P-ARCH` | `PREFERENCE` | Renumbered `SKILL.md` Procedure 2 step `5. -> 4.` cleanly (`1., 2., 3., 4.`) | `SKILL.md` |
| `F-FJ-508` | `P-ARCH` | `PREFERENCE` | Added direct sibling `U4` link `[intraprocedural-analyses-and-frameworks.md]` in `SKILL.md` shared references | `SKILL.md` |
| `F-CJ-501` | `P-CYBER` | `BLOCKING` | Restored `Uniform k-CFA` vs standard `k-CFA` vs `Polynomial k-CFA` (`Val̂` & `Cachê`), `Table 3.10` `⊨_δ^{ce}`, `Example 3.34` `{(fn y => y^6, ce₀)}`, and `U5` symmetric `basis` descriptions | `ppa-cfa-and-constraints.md`, `SKILL.md`, `polyvariant-kcfa-cpa-and-dfa.md`, `concept_graph.json` |
| `F-CJ-502` | `P-CYBER` | `BLOCKING` | Removed fabricated errata in `BKL-057/058/060/061/062` & derived layers; aligned `F-U3b-05`, `Mini Projects 3.1–3.4`, and `Exercises 3.2–3.17` to verified PDFs | `SKILL.md`, `constraint-generation-and-cubic-solver.md`, `polyvariant-kcfa-cpa-and-dfa.md`, `concept_graph.json`, `BKL-057/058/060/061/062.md` |
| `F-CJ-503` | `P-CYBER` | `BLOCKING` | Replaced hallucinated `Example 3.27/3.31` & `Figure 3.6` program/labels/tokens across `L1`, Oracle #3, `evals/cases.yaml`, and `concept_graph.json`, plus `d_c ∈ Data` in `Table 3.8` | `polyvariant-kcfa-cpa-and-dfa.md`, `SKILL.md`, `evals/cases.yaml`, `concept_graph.json` |
| `F-CJ-504` | `P-CYBER` | `BLOCKING` | Corrected `RAW_SHARD_03a_0cfa.md` (`Tables 3.2–3.3`, `Example 3.3`, `Remark.` p. 145, `Example 3.8`, `Example 3.12`, `:11`, `p. 202`) and replaced fabricated `Theorem 3.10` `[app₁]` gap (`F-U3a-05`/`BKL-052`) with `Fact 3.11` & `[if₂,₃]`/`[bind₂]` relabelling invariant | `RAW_SHARD_03a_0cfa.md`, `cfa-core-and-coinduction.md`, `SKILL.md`, `BKL-052.md`, `concept_graph.json` |
| `F-CJ-505` | `P-CYBER` | `BLOCKING` | Fixed `MONOTONICITY_GATE` (`S₁ ∩ S₂` is monotone on `(𝒫(U), ⊆)`; complement `¬S` & variable-LHS `(S₁ ⊆ S₂) ⇒ S₃` break Tarski's Theorem on `p. 201`) and `STRONG_UPDATE_GATE` (`(x := e₀)^ℓ`, `me : Var → Pnt`, `p. 200` `[133]` local stores + ref counts) | `SKILL.md`, `constraint-generation-and-cubic-solver.md`, `polyvariant-kcfa-cpa-and-dfa.md`, `BKL-059/061.md`, `concept_graph.json` |
| `F-CJ-506` | `P-CYBER` | `BLOCKING` | Fixed `[4] -> [2]` (`CPA`), `[159] -> [156, 157, 158]` (`k`-CFA), tagged bibliography-only author attributions `[2]/[9]/[156..158]` and all non-book terms (`DEXPTIME`, `reflection`, `FFI`, `deserialization`, `eval`, `sanitizer`, `weak/strong update`, `π-calculus`, `Kleene`, `post/pre-fixed point`) `[external]` | `RAW_SHARD_03a_0cfa.md`, `RAW_SHARD_03b_kcfa_cpa.md`, `L0`–`L2`, `concept_graph.json`, `BKL-061.md` |
| `F-CJ-507` | `P-CYBER` | `PREFERENCE` | Renumbered `SKILL.md` Procedure 2 `5. -> 4.`, updated `RAW_SHARD_03b` `U2 -> U5`, removed bare `⊨` from `U-39`, and synced `BKL-051/053/062` `Affected concept ids` | `SKILL.md`, `RAW_SHARD_03b_kcfa_cpa.md`, `notation_index.md`, `BKL-051/053/062.md` |

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W3-01; blocks: ISS-W4-01
- `corpus/shards/RAW_SHARD_03b_kcfa_cpa.md`
- `knowledge/skills/ppa-control-flow-and-constraints/SKILL.md`
- `knowledge/skills/ppa-control-flow-and-constraints/references/cfa-core-and-coinduction.md`
- `knowledge/skills/ppa-control-flow-and-constraints/references/constraint-generation-and-cubic-solver.md`
- `knowledge/skills/ppa-control-flow-and-constraints/references/polyvariant-kcfa-cpa-and-dfa.md`
- `knowledge/ambient-context/ppa-cfa-and-constraints.md`
- `ontology/concept_graph.json`
- `ontology/notation_index.md`
- `issues/refactors/REF-003.md`
- `issues/backlog/BKL-056.md` .. `issues/backlog/BKL-062.md`

## Verification Receipts
- 2026-11-19 [in_progress] Gate #5 Round 1 remediation (gate5-v2): 22/22 findings resolved; RAW_SHARD_03a (1,372L), RAW_SHARD_03b (1,106L), ppa-cfa-and-constraints.md (100L), ppa-control-flow-and-constraints (269L SKILL, desc=900 chars, refs 202L/147L/150L), 97-node concept_graph.json (Rule B1 97/97), notation_index.md U-39..U-45, and BKL-051..062 ready for Round 2 verification.
- 2026-11-19 [closed] Gate #5 Round 2 unanimous 3/3 [ALIGNED gate5-v2] (#223-#225); 0 HARD_BLOCK, 0 BLOCKING; 3 PREFERENCE polishes applied; validators, hygiene, and 47/47 unit tests PASS.
