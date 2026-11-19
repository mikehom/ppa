---
id: ISS-W5-03
title: "W5-3 Part II cross-paradigm matrix + Gate #8"
issue_type: shard
status: closed
priority: P1
labels: [ppa, wave-5, gate]
milestone: W5
parent_issue: EPIC-001
depends_on: [ISS-W5-02]
blocks: [ISS-W6-01]
ppa_scope: ["Part II: Ch 3–5 (book pp. 141–364; PDF pp. 159–380)"]
altitudes: [L0, L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: null
---

## Summary

Build the cross-paradigm equivalence matrix across DFA/CBA/AI/TES; cumulative refactoring; Gate #8.

## Source Citations & Grounding

- Part II: Ch 3–5 (book pp. 141–364; PDF pp. 159–380)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [x] Artifact `ontology/cross_paradigm_matrix.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Part II cross-paradigm synthesis `ontology/cross_paradigm_matrix.md` (`221L`, 5 paradigms across 10 axes, `U1`–`U10` + `X1`–`X5`, domain-specific triage workflows, anti-patterns) and holistic Part II refactor `issues/refactors/REF-006.md` promoted (`131`-node symmetric `concept_graph.json`, `0.2605` max active skill Jaccard, `299/299` gotchas covered); staged for Gate #8 (`gate8-v1`).
- 2026-11-19 Gate #8 Round 1 reviews (`P-SWE`, `P-ARCH`, `P-CYBER`) returned `[DISAGREE gate8-v1]` (`0` `HARD_BLOCK`, `9` `BLOCKING` across tracks / `6` distinct defects, `5` `PREFERENCE`). Round 1 -> Round 2 (`gate8-v2`) 1-to-1 remediation applied across all `14` findings:
- 2026-11-19 Gate #8 Round 2 (`gate8-v2`): unanimous `3/3 [ALIGNED gate8-v2]` across `P-SWE`, `P-CYBER`, and `P-ARCH` (`0` `HARD_BLOCK`, `0` `BLOCKING`, `0` `PREFERENCE`; #254, #255, #256; all `14/14` findings verified resolved with zero regressions).

| Finding ID | Track | Severity | Disposition & Action Taken | Target Artifact(s) |
| :--- | :--- | :--- | :--- | :--- |
| `F-OJ-801` | `P-SWE` | `BLOCKING` | Restricted `Lemma 5.22` attribution strictly to `§5.3.4` `SOL(C) = {θ_A | θ_A ⊨ C}` [PPA Lemma 5.22, p. 317] (book p. 317; PDF p. 334), and stated explicitly that `§5.4` contravariant arrow subtyping `≤` breaks unconstrained `Proposition 5.12` Moore families on `Typê[τ]` [PPA Exercise 5.9, p. 361] (book p. 361; PDF p. 378), requiring constrained schemes `∀ζ⃗ [C]. τ̂` (`[83, 160, 161]` [PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367)) | `ontology/cross_paradigm_matrix.md` |
| `F-OJ-802` | `P-SWE` | `BLOCKING` | Removed `[159]` attribution from `𝒰_CFA` (cited [PPA Table 5.7, p. 307] (book p. 307; PDF p. 324), [PPA Exercise 5.8, p. 361] (book p. 361; PDF p. 378), and `[90, 183, 167, 168, 169]`, contrasting non-free equational unification `[159]`), removed `[external]` from book-native `Robinson unification`, and replaced false decidability claim with `§5.4.3` Region Inference (`Algorithms S & R`, `[174]`) being syntactically sound yet incomplete [PPA Chapter 5 Concluding Remarks, p. 352] (book p. 352; PDF p. 369) | `ontology/cross_paradigm_matrix.md` |
| `F-OJ-803` | `P-SWE` | `BLOCKING` | Tagged `[external: Herbrand]` alongside `free-algebra` / `Free` terminology at Axis `Annotated Base / Effect Types` and Axis `4. Lattice & Chain Requirements` | `ontology/cross_paradigm_matrix.md` |
| `F-OJ-804` | `P-SWE` | `PREFERENCE` | Updated `U6` reduction citation to `[PPA Proposition 4.29, p. 244] (book p. 244; PDF p. 261)` alongside `[PPA Fact 4.30, p. 245] (book p. 245; PDF p. 262)` and `[PPA Fact 4.31, p. 246] (book p. 246; PDF p. 263)` | `ontology/cross_paradigm_matrix.md` |
| `F-OJ-805` | `P-SWE` | `PREFERENCE` | Tagged `` `vtable` `[external]` `` in cybersecurity sink enumeration and added `Exercise 5.9`'s Moore-family loss under `§5.4.1` subtyping to `U8` divergences | `ontology/cross_paradigm_matrix.md` |
| `F-FJ-801` | `P-ARCH` | `BLOCKING` | Remediated jointly with `F-OJ-801` and `F-CJ-801` at Axis `9` Ch 5 cell | `ontology/cross_paradigm_matrix.md` |
| `F-FJ-802` | `P-ARCH` | `BLOCKING` | Classified `§5.4.1`, `§5.4.2`, and `§5.4.3` (`Table 5.11` [PPA Table 5.11, p. 334] (book p. 334; PDF p. 351)) strictly as store/exception/region big-step Natural Semantics, reserved evaluation-context small-step SOS strictly for `§5.5` (`Tables 5.14–5.15`), and cited `§5.4.3`/`§5.5` semantic soundness via Concluding Remarks (`[176, 131]`) rather than numbered Subject Reduction/Progress theorems in `PPA` | `ontology/cross_paradigm_matrix.md` |
| `F-FJ-803` | `P-ARCH` | `BLOCKING` | Remediated jointly with `F-OJ-802` and `F-CJ-803` at Axis `8` Ch 5 cell (`[159]` contrast vs `Table 5.7` and `[90, 183, 167, 168, 169]`) | `ontology/cross_paradigm_matrix.md` |
| `F-FJ-804` | `P-ARCH` | `PREFERENCE` | Remediated jointly with `F-OJ-804` (`Proposition 4.29` / `Fact 4.30` / `Fact 4.31` in `U6`) and added `[PPA §5.4.1, p. 324] (book p. 324; PDF p. 341)` for `ref_ϖ` invariance alongside `Table 5.18` in Axis `7` | `ontology/cross_paradigm_matrix.md` |
| `F-FJ-805` | `P-ARCH` | `PREFERENCE` | Disambiguated `IDE` as `` `[external: editor IDE]` `` in practitioner triage row to avoid colliding with Sagiv–Reps–Horwitz `IDE` (`§2.5`) | `ontology/cross_paradigm_matrix.md` |
| `F-CJ-801` | `P-CYBER` | `BLOCKING` | Remediated jointly with `F-OJ-801` and `F-FJ-801` at Axis `9` Ch 5 cell | `ontology/cross_paradigm_matrix.md` |
| `F-CJ-802` | `P-CYBER` | `BLOCKING` | Added omitted `X2` hypotheses requiring a Galois insertion `(L, α, γ, M)` satisfying `γ(⊥_M) = ⊥_L` with finite-height `M` and `∇_M = ⊔_M`, and cited `[PPA §4.5, p. 270] (book p. 270; PDF p. 287)` alongside `[PPA Lemma 4.45, p. 269] (book p. 269; PDF p. 286)` | `ontology/cross_paradigm_matrix.md` |
| `F-CJ-803` | `P-CYBER` | `BLOCKING` | Remediated jointly with `F-OJ-802`, `F-OJ-803`, `F-OJ-804`, `F-FJ-803`, and `F-FJ-804`, plus tagged `[external: integrated form]` in `U2` and `[external: Scott continuity]` in `X5` | `ontology/cross_paradigm_matrix.md` |
| `F-CJ-804` | `P-CYBER` | `PREFERENCE` | Qualified `U8` `Preserved Invariants` to simply-typed non-polymorphic terms without multi-call higher-order argument sharing (`Example 5.4`), and across all simply-typed terms once `§5.4.1` contravariant subtyping `≤` and `(5.2)` tree instrumentation are added ([PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376)) | `ontology/cross_paradigm_matrix.md` |

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W5-02; blocks: ISS-W6-01
- `ontology/cross_paradigm_matrix.md`
- `ontology/concept_graph.json`
- `ontology/altitude_alignment_log.md`
- `issues/refactors/REF-006.md`

## Verification Receipts

- 2026-11-19 [in_progress] `ontology/cross_paradigm_matrix.md` (`221L`) and `issues/refactors/REF-006.md` promoted across Part II (`Ch 3–5`) and `U1–U10`/`X1–X5`; staged for Gate #8 (`gate8-v1`).
- 2026-11-19 [in_progress] Gate #8 Round 1 remediation (`gate8-v2`): `14/14` findings (`F-OJ-801..805`, `F-FJ-801..805`, `F-CJ-801..804`) resolved in `ontology/cross_paradigm_matrix.md` (`§5.3.4` `Lemma 5.22` vs `§5.4` `Exercise 5.9`, `§5.4.1–§5.4.3` big-step vs `§5.5` SOS, `[159]`/`Robinson unification`/`§5.4.3` incompleteness, `X2` `γ(⊥_M)=⊥_L` Galois insertion, `U6` `Proposition 4.29`/`Fact 4.30`–`4.31`, `ref_ϖ` `§5.4.1`, `U8` `Exercise 5.4`/`5.9`, and `[external]` tags); synced to `REF-006.md` and `ontology/altitude_alignment_log.md`; ready for Gate #8 Round 2.
- 2026-11-19 [aligned] Gate #8 Round 2 unanimous 3/3 [ALIGNED gate8-v2] across P-SWE, P-CYBER, P-ARCH (#254, #255, #256).
- 2026-11-19 [closed] Gate #8 closed; Part II holistic matrix, 131-node concept graph, validators, hygiene, export parity, and 47/47 unit tests PASS.
