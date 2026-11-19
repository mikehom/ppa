---
name: ppa-program-analysis
description: >-
  Routes static program analysis tasks grounded in Principles of Program Analysis to the right
  specialised skill, and orients on how Data Flow Analysis, Constraint Based Analysis, Abstract
  Interpretation and Type and Effect Systems relate.
  Use when a task asks which static analysis approach fits, compares the four approaches, asks
  what a safe approximation or least solution is, or needs Chapter 1 formulations or the order,
  induction, coinduction and graph background of Appendices A to C.
  Do not use when the technique is already chosen: use ppa-dataflow-and-slicing for facts per
  program point and slicing, ppa-control-flow-and-constraints for call targets and control flow
  analysis, ppa-abstract-interpretation for abstract domains and widening,
  ppa-types-effects-and-regions for annotated types and effects, ppa-fixedpoint-solvers for
  worklists and iteration order, ppa-cyber-vulnerability-analysis for security properties.
  Do not use for dynamic analysis, testing, fuzzing or parsing.
---

<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-008: L0 master router; routing table only, formal content lives in references/. -->

# PPA Program Analysis: Router

This file only routes. It defines nothing and prescribes no procedure. For safe approximation,
soundness direction, how the Chapter 1 formulations relate, and formal statements with their side
conditions, read one reference from the list under References (a standalone ambient orientation
named `ppa-foundations.md` also exists as an independent install channel, but this skill package is
self-contained without it).

## Decision Table

Pick the first row whose task shape matches. Each row also gives a negative route, which
sends the task elsewhere when the discriminator does not hold.

| Task shape | Route to | Discriminator (one line) | Negative route: not this skill when ... |
| :--- | :--- | :--- | :--- |
| Facts per program point in code whose control flow is known from its syntax: reaching definitions, live/faint variables, available/very busy expressions, def-use chains, constant propagation, interprocedural context, or heap shape graphs | `ppa-dataflow-and-slicing` | Control flow is known syntactically (`§§2.1–2.6` active) | ... call targets are themselves computed values (use `ppa-control-flow-and-constraints`), Chapter 1 comparison or App A–C theory is asked (stay here), or only solver scheduling is in question (use `ppa-fixedpoint-solvers`) |
| Which functions, closures or methods may be called or may reach an expression; higher-order or dynamic dispatch; constraint generation for control flow | `ppa-control-flow-and-constraints` | Control flow is an output of the analysis (`§§3.1–3.6` active) | ... the flow graph is already fixed and per-point facts are wanted (use `ppa-dataflow-and-slicing`) |
| Designing, combining or justifying an abstract domain; abstraction and concretisation; widening and narrowing; proving an analysis correct against a semantics | `ppa-abstract-interpretation` | The question is what to approximate and why it is safe | ... the domain is settled and only iteration order or cost is in question (use `ppa-fixedpoint-solvers`) |
| Expressing an analysis as inference rules over types: annotated types, effects for calls, side effects, exceptions, regions or communication | `ppa-types-effects-and-regions` | The analysis is attached to an underlying type system | ... there is no type system and per-point facts are wanted (use `ppa-dataflow-and-slicing`) |
| Computing a least solution efficiently: worklists, iteration order, strong components, convergence speed of a constraint solver | `ppa-fixedpoint-solvers` | The question is how to compute, not what | ... termination is in doubt because the domain has unbounded chains (use `ppa-abstract-interpretation` for widening) |
| A security property is the starting point: [external: taint], [external: injection], indirect-call reach, disclosure; choosing a technique and reading its alarms or guarantees | `ppa-cyber-vulnerability-analysis` | The task starts from a vulnerability class, not from a technique | ... the technique is already chosen and the question is technical (use that technique's skill from the rows above) |

Stay in this skill when the task compares approaches, asks which one fits, asks about safe
approximation in general, or needs one of the references below.

## Two Discriminating Questions

- Is the control flow an input to the analysis or an output of it?
- Is the task about what to approximate, or about how to compute the approximation?

## Negative Routes for Out-of-Scope Tasks

| Task | Route |
| :--- | :--- |
| Dynamic analysis, testing, fuzzing, profiling, runtime monitoring | None of the PPA skills. The book treats static techniques only |
| Concrete syntax and parsing | None. The book works on abstract syntax only |
| Semantics directed analysis: denotational or logic based formulations shaped directly by the semantics | Not covered by the book (Chapter 1 Concluding Remarks). Answer from general knowledge and label it as external |
| Denotationally based program analysis, projection analysis, logical formulations based on Stone dualities, single static assignment form, fast techniques for implementing type based analyses, a broader treatment of pointer analyses, a deeper treatment of set constraints, efficient recomputation of invalidated analysis information after transformations | Omitted by the Preface. Answer from general knowledge and label it as external |

## References

- [chapter-1-five-formulations.md](references/chapter-1-five-formulations.md): safe approximation, soundness
  direction, and Chapter 1 analyses side by side (equations, constraints, control flow analysis,
  abstract interpretation, annotated types and effects) with every side condition, Tables 1.1 to 1.6,
  and Chapter 1 source errata.
- [appendix-a-posets-lattices-fixed-points.md](references/appendix-a-posets-lattices-fixed-points.md): partial orders,
  complete lattices, chains and fixed points (Appendix A).
- [appendix-b-induction-and-coinduction.md](references/appendix-b-induction-and-coinduction.md): induction and
  coinduction (Appendix B).
- [appendix-c-graphs-dfsf-and-rpo.md](references/appendix-c-graphs-dfsf-and-rpo.md): directed graphs, regular path
  sets, depth-first spanning forests, reverse postorder, loop connectedness and reducibility
  (Appendix C).

## Sibling Reference Modules (Active)

- Chapter 2 (`ppa-dataflow-and-slicing`): [intraprocedural-analyses-and-frameworks.md](../ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md) (`§§2.1, 2.3–2.4`), [interprocedural-and-correctness.md](../ppa-dataflow-and-slicing/references/interprocedural-and-correctness.md) (`§§2.2, 2.5`), and [shape-analysis.md](../ppa-dataflow-and-slicing/references/shape-analysis.md) (`§2.6`).
- Chapter 3 (`ppa-control-flow-and-constraints`): [cfa-core-and-coinduction.md](../ppa-control-flow-and-constraints/references/cfa-core-and-coinduction.md) (`§§3.1–3.3`), [constraint-generation-and-cubic-solver.md](../ppa-control-flow-and-constraints/references/constraint-generation-and-cubic-solver.md) (`§3.4`), and [polyvariant-kcfa-cpa-and-dfa.md](../ppa-control-flow-and-constraints/references/polyvariant-kcfa-cpa-and-dfa.md) (`§§3.5–3.6`).

## Evaluation

Routing cases for this skill are in `evals/cases.yaml`.
