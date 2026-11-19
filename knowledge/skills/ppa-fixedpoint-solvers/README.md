<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Package overview for ppa-fixedpoint-solvers (Chapter 6 + Unit 6 Index/Bibliography concordance). -->

# ppa-fixedpoint-solvers

Actionable L2 skill and formal L1 reference bundle for Chapter 6 (*Algorithms*) and the Unit 6 Subject Index & Bibliography concordance of *Principles of Program Analysis* (F. Nielson, H. R. Nielson, C. Hankin; Springer 1999, corrected second printing 2005).

## Purpose

Guides compiler, `[external: editor IDE]`, and static-analysis engineers through designing, scheduling, accelerating, and verifying fixed-point solvers over monotone inequation systems (`Tables 6.1–6.6`, `Figures 6.1–6.6`, `Lemmas 6.4, 6.11, 6.12`), including `M = 1` join splitting (`Exercise 6.5`), minimal handles (`H_𝒮`), double-buffered RPO (`(W.c, W.p)`), Round-Robin loop-connectedness bounds (`d(G_𝒮, T) + 3`), shadow-free 3-queue strong-component condensation (`(W.c, W.pc, W.pf)`), guarded worklist widening (`Exercise 6.13`), closed-form fastness closures (`Exercise 6.14`), sound `[external: timeout]` degradation, demand-driven local/differential solvers (`Concluding Remarks p. 385`), and elimination methods (`p. 386`).

## Layout

| Path | Altitude | Role |
| :--- | :--- | :--- |
| `SKILL.md` | L2 procedural skill (`250–499` lines) | Solver selection matrix, 4 engineering workflows, diagnostic playbook, golden trace oracles, and verification checklist |
| `references/worklist-and-rpo-algorithms.md` | L1 reference (`<= 450` lines) | `§§6.1–6.2`, `Tables 6.1–6.4`, `Figures 6.1–6.4`, `Lemmas 6.4, 6.11, 6.12`, `U2`/`U3`/`U10` bridges, `Ex 6.5` `M² → M` split, `Ex 6.1–6.9`, `MP 6.1` |
| `references/scc-round-robin-and-advanced-solvers.md` | L1 reference (`<= 450` lines) | `§6.3` `Tables 6.5–6.6`, `Figures 6.5–6.6`, `Table 6.5` shadowing fix, 3-queue `(W.c, W.pc, W.pf)`, `MP 6.2`, `Ex 6.13` `∇`, `Ex 6.14` `f̄`, local/elimination solvers, Index/Bib concordance |
| `evals/cases.yaml` | Evaluation data | Positive solver routing cases and negative sibling boundary cases (`U2`, `U3`, `U7`, `U10`) |
| `SUGGESTED_FIXES.md` | Maintenance | Pending suggestions for this skill |

Channel independence: standalone L0 ambient orientation lives separately in `knowledge/ambient-context/ppa-fixedpoint-solvers.md` (`80–250` lines). Neither channel depends on the other on disk.

## Siblings

- Master router & Foundations: `ppa-program-analysis` (cross-references in `../ppa-program-analysis/references/`)
- Specialised siblings: `ppa-dataflow-and-slicing`, `ppa-control-flow-and-constraints`, `ppa-abstract-interpretation`, `ppa-types-effects-and-regions`, `ppa-cyber-vulnerability-analysis`.
