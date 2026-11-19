# ppa-abstract-interpretation

Actionable L2 skill and formal L1 reference bundle for Chapter 4 (*Abstract Interpretation*) of
*Principles of Program Analysis* (F. Nielson, H. R. Nielson, C. Hankin; Springer 1999, corrected second
printing 2005).

## Purpose

Guides static analysis engineers and researchers through constructing correctness relations and representation
functions, accelerating infinite-height fixed-point convergence via widening and narrowing, proving and extracting
Galois connections and Galois insertions, composing multi-attribute and relational abstract domains (`AB`), and
deriving best induced abstract transformers, generalised Monotone Framework soundness proofs, and concretisation-induced
widenings.

## Layout

| Path | Altitude | Role |
| :--- | :--- | :--- |
| `SKILL.md` | L2 procedural skill (`250–499` lines) | Step-by-step domain-design, widening/narrowing, combinator, and soundness workflows, triage matrix, and golden regression oracles |
| `references/correctness-and-fixed-points.md` | L1 reference (`<= 450` lines) | `§4.1` mundane correctness `(4.1)–(4.6)`, `β`, `§4.2` `Interval`, `Figures 4.1–4.5`, widening `∇`/`∇_K`, narrowing `Δ`/`Δ_N`, `U7`, `Exercises 4.1–4.12` |
| `references/galois-connections-and-insertions.md` | L1 reference (`<= 450` lines) | `§4.3` `(L, α, γ, M)` `(4.8)–(4.10)`, `Figures 4.6–4.10`, `Lemmas 4.22–4.23, 4.27`, reduction `ς`, `[external: uco(L)]`, guard/lattice duality, `Exercises 4.13–4.14` |
| `references/combinators-and-induced-operations.md` | L1 reference (`<= 450` lines) | `§4.4` combinators, `45 -> 29` `AB`, `§4.5` `α ∘ f ∘ γ`, generalised Monotone Frameworks (`U6`), `γ`-widening `(4.11)–(4.15)`, `Mini Projects 4.1–4.3`, `Exercises 4.15–4.24` |
| `evals/cases.yaml` | Evaluation data | Positive routing cases (`ppa-abstract-interpretation`) and negative sibling boundary cases (`U6`, `U7`, and all siblings) |
| `SUGGESTED_FIXES.md` | Maintenance | Pending suggestions for this skill |

Channel independence: standalone L0 ambient orientation lives separately in
`knowledge/ambient-context/ppa-abstract-interpretation.md` (`80–250` lines). Neither channel depends on the other on disk.

## Siblings

- Master router & Foundations: `ppa-program-analysis` (cross-references in `../ppa-program-analysis/references/`)
- Specialised siblings: `ppa-dataflow-and-slicing` (shared `U6`/`U7` cross-references in `../ppa-dataflow-and-slicing/references/`),
  `ppa-control-flow-and-constraints`, `ppa-types-effects-and-regions`, `ppa-fixedpoint-solvers`,
  `ppa-cyber-vulnerability-analysis`.
