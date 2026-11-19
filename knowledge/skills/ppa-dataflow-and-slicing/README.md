# ppa-dataflow-and-slicing

Actionable L2 skill and formal L1 reference bundle for Chapter 2 (*Data Flow Analysis*) of
*Principles of Program Analysis* (F. Nielson, H. R. Nielson, C. Hankin; Springer 1999, corrected second
printing 2005).

## Purpose

Guides engineers and static analysis authors through constructing, debugging, and proving classical
intraprocedural analyses (`AE, RD, VB, LV`), `ud`/`du` slicing, Monotone and Distributive
Frameworks, Constant Propagation, interprocedural call-string and assumption-set extensions, flow-insensitive
side-effect sets (`IAV`, `[external: mod-ref]` summaries), and heap shape analysis with strong updates.

## Layout

| Path | Altitude | Role |
| :--- | :--- | :--- |
| `SKILL.md` | L2 procedural skill (`250–499` lines) | Step-by-step design/debugging workflows, boundary routing, gotcha checks, and verification checklists |
| `references/intraprocedural-analyses-and-frameworks.md` | L1 reference (`<= 450` lines) | `init`/`final`/`flow`/`flow^R`, `Tables 2.1–2.9`, `ud`/`du` chains, Monotone/Distributive hierarchy, `CP`, `MFP` vs `MOP` |
| `references/interprocedural-and-correctness.md` | L1 reference (`<= 450` lines) | `§2.2` LV correctness proof, `Table 2.10` / `Mini Project 2.2`, `§2.5` `CP`/`VP`/`MVP`, call strings, assumption sets, `IAV` |
| `references/shape-analysis.md` | L1 reference (`<= 450` lines) | `§2.6` pointer SOS, `SG = (S, H, is)`, Invariants 1–5, all 8 transfer schemas, Case 3 materialisation, `n_{ℓ,X}` |
| `evals/cases.yaml` | Evaluation data | Positive routing cases (`ppa-dataflow-and-slicing`) and negative sibling boundary cases |
| `SUGGESTED_FIXES.md` | Maintenance | Pending suggestions for this skill |

Channel independence: standalone L0 ambient orientation lives separately in
`knowledge/ambient-context/ppa-dataflow-and-shape.md` (`80–250` lines). Neither channel depends on the other on disk.

## Siblings

- Master router & Foundations: `ppa-program-analysis` (cross-references in `../ppa-program-analysis/references/`)
- Specialised siblings (named boundaries only until authored): `ppa-control-flow-and-constraints`,
  `ppa-abstract-interpretation`, `ppa-types-effects-and-regions`, `ppa-fixedpoint-solvers`,
  `ppa-cyber-vulnerability-analysis`.
