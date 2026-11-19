<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Package overview for Chapter 5 skill ppa-types-effects-and-regions. -->

# ppa-types-effects-and-regions

Actionable `L2` skill and formal `L1` reference bundle for Chapter 5 (*Type and Effect Systems*) of
*Principles of Program Analysis* (F. Nielson, H. R. Nielson, C. Hankin; Springer 1999, corrected second
printing 2005) [PPA Chapter 5, p. 283] (book p. 283; PDF p. 300).

## Purpose

Guides compiler and static-analysis engineers through designing, implementing, verifying, and debugging
annotated type systems (`⊢_UL`, `⊢_CFA`), free-algebra type/annotation reconstruction (`𝒲_CFA`, `𝒰_CFA`,
`SType`, closed-form `θ_A`), shape-conformant polarised subtyping (`≤` with mutable reference/channel
invariance), Hindley/Milner exception effect polymorphism (`β \ {s} = β`, `[gen]` `FV(φ)`
downwards closure), stack-based region inference (`[175, 176]`, `[external: Tofte–Talpin]`: `letregion`, `Observe`, `∀β⃗, [ϱ⃗]`),
Concurrent ML causal communication behaviours (`Table 5.18`), monotone security/binding-time types, and
`[external: abelian-group/affine-torsor]` units of measure.

## Layout

| Path | Altitude | Role |
| :--- | :--- | :--- |
| `SKILL.md` | `L2` procedural skill (`250–499` lines) | Step-by-step design/reconstruction/region/behaviour workflows, boundary dispatch, debugging table, and golden oracles |
| `references/annotated-types-and-cfa-soundness.md` | `L1` reference (`<= 450` lines) | `§§5.1–5.2`: `Tables 5.1–5.4`, `⊢_UL`, `⊢_CFA` subeffecting, `UCAI`, `Fact 5.6`, Natural Semantics `(5.1)`, `Theorem 5.9`, covariant `Typê[τ]` `Proposition 5.12` |
| `references/inference-unification-and-subtyping.md` | `L1` reference (`<= 450` lines) | `§5.3` + `§5.4` core: `Tables 5.5–5.8`, `𝒲_UL`/`𝒰_UL` (`∘ θ₀` fix), `SType` `𝒰_CFA`/`𝒲_CFA`, `Theorems 5.20–5.21`, `θ_A`, contravariant `≤`, `Exercise 5.9`, canonical `U8` |
| `references/effects-exceptions-regions-and-behaviours.md` | `L1` reference (`<= 450` lines) | `§§5.4.1–5.5` + End Matter: `Tables 5.9–5.18`, `Figures 5.1–5.2`, `ref_ϖ` invariance, `β \ {s} = β`, `letregion` + `Observe`, CML behaviours, `Mini Projects 5.1–5.5` |
| `evals/cases.yaml` | Evaluation data | Positive routing cases (`ppa-types-effects-and-regions`) and negative sibling boundary cases (`U8`, `§2.6` shape, AI, solvers, cyber, router) |
| `SUGGESTED_FIXES.md` | Maintenance | Pending review suggestions for this skill |

Channel independence: standalone `L0` ambient orientation lives separately in
`knowledge/ambient-context/ppa-types-effects-and-regions.md` (`80–250` lines). Neither channel depends on the other on disk.

## Siblings

- Master router & Foundations: `ppa-program-analysis` (shared references in `../ppa-program-analysis/references/`)
- Specialised siblings (referenced by exact discovery name): `ppa-dataflow-and-slicing`,
  `ppa-control-flow-and-constraints`, `ppa-abstract-interpretation`, `ppa-fixedpoint-solvers`,
  `ppa-cyber-vulnerability-analysis`.
