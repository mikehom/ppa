---
id: ISS-W2-03
title: "W2-3 Unit 2 synthesis: dataflow skill, reference and Gate #3"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-2, gate]
milestone: W2
parent_issue: EPIC-001
depends_on: [ISS-W2-01, ISS-W2-02]
blocks: [ISS-W2-04]
ppa_scope: ["Chapter 2 (book pp. 35–139; PDF pp. 54–158)"]
altitudes: [L1, L2]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: 51
---

## Summary

Synthesize Chapter 2 into an actionable L2 skill and L1 reference; cumulative KB refactoring; Gate #3.

## Source Citations & Grounding

- Chapter 2 (book pp. 35–139; PDF pp. 54–158)
- Tables in scope: Table 2.1 (p. 40/PDF 59), Table 2.2 (p. 44/PDF 63), Table 2.3 (p. 47/PDF 66), Table 2.4 (p. 50/PDF 69), Table 2.5 (p. 55/PDF 74), Table 2.6 (p. 56/PDF 75), Table 2.7 (p. 73/PDF 92), Table 2.8 (p. 75/PDF 94), Table 2.9 (p. 76/PDF 95), Table 2.10 (p. 133/PDF 152)
- Figures in scope: Figure 2.1 (p. 38/PDF 57), Figure 2.2 (p. 41/PDF 60), Figure 2.3 (p. 48/PDF 67), Figure 2.4 (p. 61/PDF 80), Figure 2.5 (p. 62/PDF 81), Figure 2.6 (p. 70/PDF 89), Figure 2.7 (p. 85/PDF 104), Figure 2.8 (p. 93/PDF 112), Figure 2.9 (p. 94/PDF 113), Figure 2.10 (p. 95/PDF 114), Figure 2.11 (p. 103/PDF 122), Figure 2.12 (p. 106/PDF 125), Figure 2.13 (p. 112/PDF 131), Figure 2.14 (p. 113/PDF 132), Figure 2.15 (p. 115/PDF 134), Figure 2.16 (p. 116/PDF 135), Figure 2.17 (p. 118/PDF 137), Figure 2.18 (p. 120/PDF 139), Figure 2.19 (p. 123/PDF 142), Figure 2.20 (p. 124/PDF 143), Figure 2.21 (p. 126/PDF 145), Figure 2.22 (p. 127/PDF 146), Figure 2.23 (p. 132/PDF 151)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L1, L2. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

Source slice: book pp. 35–139 (source slices regenerated as untracked working files by `scripts/extract_ppa_structure.py`, never edited).

## Acceptance Gates

- [x] Every section in scope cited with exact `(book_page, pdf_page)` coordinates validated against `corpus/pdf_page_map.json`
- [x] All 10 tables and 23 figures in book pp. 35–139 are anchored (no omissions)
- [x] Artifact `knowledge/skills/ppa-dataflow-and-slicing/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `knowledge/ambient-context/ppa-dataflow-and-shape.md` and `references/{intraprocedural-analyses-and-frameworks,interprocedural-and-correctness,shape-analysis}.md` exist and pass `scripts/validate_ppa_knowledge.py`
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Round 1 (`gate3-v1`): three-track adversarial panel returned `[DISAGREE]` across `20` findings (`P-ARCH`: `6` `BLOCKING`, `1` `PREFERENCE`; `P-SWE`: `5` `BLOCKING`, `2` `PREFERENCE`; `P-CYBER`: `4` `BLOCKING`, `2` `PREFERENCE`). Remediated all `20/20` items (`gate3-v2`).
- 2026-11-19 Round 2 (`gate3-v2`): unanimous `3/3 [ALIGNED gate3-v2]` across `P-SWE`, `P-ARCH`, and `P-CYBER` (`0` `HARD_BLOCK`, `0` `BLOCKING`; all Round 1 findings withdrawn).

### Rebuttal & Attribution Summary (Gate #3 Round 1)

| Finding ID | Track | Severity | Disposition & Action Taken | Target Artifact(s) |
| :--- | :--- | :--- | :--- | :--- |
| `F-FJ-301` | `P-ARCH` | `BLOCKING` | Fixed `kill_x` comprehension guards (`\| (n_V,sel,n_W) ∈ H`, `\| n_X ∈ is`, `p. 117`), `Case 3` guards (`x≠y`, `(y,n_Y)∈S'`, `(n_Y,sel,n_∅)∈H'`), and `[x.sel:=y]` `x,y ∈ dom(S)` + `is' ∪ {n_Y}` | `knowledge/skills/ppa-dataflow-and-slicing/SKILL.md`, `references/shape-analysis.md` |
| `F-FJ-302` | `P-ARCH` | `BLOCKING` | Replaced invented `dom_x(ℋ)` with `σ(x) ∈ Loc ∧ (σ(x), sel) ∈ dom(ℋ)` (`[PPA §2.6.1, p. 107]`) | `references/shape-analysis.md` |
| `F-FJ-303` | `P-ARCH` | `BLOCKING` | Restored distinct `CP_{ℓ₁,ℓ₂}`, `CP_{ℓ₁,ℓ₃}`, `CP_{ℓ_c,ℓ}` heads and all four `VP` rules (`VP_{ℓ₁,ℓ₂} ⟶ ℓ₁`, `VP_{ℓ₁,ℓ₃} ⟶ ℓ₁, VP_{ℓ₂,ℓ₃}`) from `pp. 89–90` | `references/interprocedural-and-correctness.md` |
| `F-FJ-304` | `P-ARCH` | `BLOCKING` | Replaced `\le` with Unicode `≤` (`yaml.safe_load` passes) and aligned `must_mention` to `"y := x * x"` | `knowledge/skills/ppa-dataflow-and-slicing/evals/cases.yaml` |
| `F-FJ-305` | `P-ARCH` | `BLOCKING` | Pointed `L1 anchor` on `BKL-037` and `BKL-038` to `interprocedural-and-correctness.md` | `issues/backlog/BKL-037.md`, `issues/backlog/BKL-038.md` |
| `F-FJ-306` | `P-ARCH` | `BLOCKING` | Raised `ppa.dfa.rd-instrumented-correctness` `altitude` from `"L3"` to `"L1"` (`Rule B1`) | `ontology/concept_graph.json` |
| `F-FJ-307` | `P-ARCH` | `PREFERENCE` | Instantiated `(x ∈ FV(a+1))` to `(a ∈ FV(a+1))` in Oracle A | `knowledge/skills/ppa-dataflow-and-slicing/SKILL.md` |
| `F-OJ-301` | `P-SWE` | `BLOCKING` | Added `label consistent` + `isolated entries` (or `§2.3` unconditional join) precondition on `Shape∘(ℓ)` and `∀ℓ : path∘(ℓ) ≠ ∅` / strictness (`Lemma 2.32`, `Exercise 2.13`) on `MFP = MOP` | `references/shape-analysis.md`, `corpus/shards/RAW_SHARD_02b_interproc_shape.md` |
| `F-OJ-302` | `P-SWE` | `BLOCKING` | Removed `𝒫(path∘(ℓ))` and `§1.5` adjunction misattribution from `p. 82`; recorded `§2.4.2` `𝒫(L)` lifting accurately (`[derived]`/`[external]` note) and deferred `U6` to `§4.5` | `references/intraprocedural-analyses-and-frameworks.md` |
| `F-OJ-303` | `P-SWE` | `BLOCKING` | Replaced untagged/inverted `"post-fixed-point"` with book's `Red(F)` (`reductive`, `F(x) ⊑ x`) vs ascending iteration (`[external: Kleene]`) | `references/interprocedural-and-correctness.md`, `RAW_SHARD_02a_intraproc_dfa.md`, `ontology/concept_graph.json` |
| `F-OJ-304` | `P-SWE` | `BLOCKING` | Added explicit `BKL-037` and `BKL-038` pointers in `interprocedural-and-correctness.md` `§1` alongside fixed `L1 anchor` fields | `references/interprocedural-and-correctness.md`, `BKL-037.md`, `BKL-038.md` |
| `F-OJ-305` | `P-SWE` | `BLOCKING` | Eliminated malformed placeholder citation token in favor of concrete Chapter 2 coordinate example (`C1.10`) | `knowledge/skills/ppa-dataflow-and-slicing/SKILL.md` |
| `F-OJ-306` | `P-SWE` | `PREFERENCE` | Expanded `## Technical Analysis / Mechanism` across `BKL-036..050` with concrete failure traces instead of repeating `Summary` verbatim | `issues/backlog/BKL-036.md`..`BKL-050.md` |
| `F-OJ-307` | `P-SWE` | `PREFERENCE` | Clarified `f_ℓ^SA(SG)` subset parameter overloading (`X ∈ 𝒫(SG)`) from `p. 116` | `references/shape-analysis.md` |
| `F-CJ-301` | `P-CYBER` | `BLOCKING` | Remediated jointly with `F-FJ-301` and `F-FJ-303` (`CP`/`VP` grammars + `kill_x` comprehension guards) | `references/interprocedural-and-correctness.md`, `SKILL.md` |
| `F-CJ-302` | `P-CYBER` | `BLOCKING` | Fixed `SKILL.md:268` (`F-OJ-305`), split `shape-analysis.md:8` `pp. 129–130` to singular `N8` citations, and changed `RAW_SHARD_02b:18` header to `(Book pages 82–139 / PDF pages 101–158)` | `SKILL.md`, `references/shape-analysis.md`, `RAW_SHARD_02b_interproc_shape.md` |
| `F-CJ-303` | `P-CYBER` | `BLOCKING` | Tagged `[external]` on `mod-ref`, `CWE-*`, `zeroization`, `UAF`, `Dyck-stack`, `Kleene` and standardized `Red(F)` (`reductive`) terminology across `L1`–`L3` | `SKILL.md`, `README.md`, `references/*.md`, `RAW_SHARD_02a/02b`, `ontology/concept_graph.json` |
| `F-CJ-304` | `P-CYBER` | `BLOCKING` | Remediated jointly with `F-OJ-301` (`Shape` isolated-entries precondition & `Lemma 2.32` `MFP = MOP` strictness guard) | `references/shape-analysis.md`, `RAW_SHARD_02b_interproc_shape.md` |
| `F-CJ-305` | `P-CYBER` | `PREFERENCE` | Remediated jointly with `F-FJ-306` (`ppa.dfa.rd-instrumented-correctness` `altitude` raised to `"L1"`) | `ontology/concept_graph.json` |
| `F-CJ-306` | `P-CYBER` | `PREFERENCE` | Clarified `Exercise 2.22` covers `[x.sel:=x.sel']^ℓ` in `SKILL.md` and corrected Chapter 2 end page from `140` to `139` | `SKILL.md`, `ISS-W2-02.md`, `ISS-W2-03.md` |

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W2-01, ISS-W2-02; blocks: ISS-W2-04
- `knowledge/skills/ppa-dataflow-and-slicing/SKILL.md`
- `knowledge/skills/ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md`
- `knowledge/skills/ppa-dataflow-and-slicing/references/interprocedural-and-correctness.md`
- `knowledge/skills/ppa-dataflow-and-slicing/references/shape-analysis.md`
- `knowledge/ambient-context/ppa-dataflow-and-shape.md`
- `knowledge/skills/ppa-program-analysis/SKILL.md`
- `ontology/concept_graph.json`
- `issues/refactors/REF-001.md`
- `issues/backlog/BKL-036.md` .. `issues/backlog/BKL-050.md`

## Verification Receipts

- 2026-11-19 [in_progress] `W2-3` synthesis and graph/backlog merge verified (`81` concepts, `10/10` Tables `2.1–2.10`, `23/23` Figures `2.1–2.23`, `BKL-036..050`, `0` errors across `validate_ppa_knowledge.py --strict-gotchas`, `issue_ctl.py validate`, and `check_portability_hygiene.py .`).
- 2026-11-19 [in_progress] `gate3-v2` Round 1 remediation verified across all `20/20` findings (`0` errors across remediation verifier, `validate_ppa_knowledge.py --strict-gotchas`, `issue_ctl.py validate`, `check_portability_hygiene.py .`, and `47/47` unit tests). Ready for Gate #3 Round 2.
- 2026-11-19 [closed] Gate #3 Round 2 unanimous 3/3 [ALIGNED gate3-v2] across P-SWE, P-ARCH, and P-CYBER; 0 HARD_BLOCK, 0 BLOCKING; validators, hygiene, and 47/47 unit tests PASS.
