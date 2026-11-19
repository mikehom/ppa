# ppa-program-analysis

Master router and Unit 1 home for the semantic knowledge distribution of *Principles of Program
Analysis* (F. Nielson, H. R. Nielson, C. Hankin; Springer 1999, corrected second printing 2005).

## Purpose

The skill decides which specialised skill fits a static program analysis task and holds the
references that no single specialised skill owns: the Chapter 1 comparison of formulations and the
order-theory, induction/coinduction, and directed-graph/reverse-postorder background of Appendices
A, B, and C. It routes; it does not prescribe a procedure.

## Layout

| Path | Altitude | Role |
| :--- | :--- | :--- |
| `SKILL.md` | L0 router (under 100 lines) | Decision table from task shape to skill, one routing row per sibling with a discriminator and a negative route; out-of-scope routes; links to self-contained `references/` |
| `references/chapter-1-five-formulations.md` | L1 reference (at most 450 lines) | Safe approximation, soundness direction, Chapter 1 analyses side by side with all side conditions, Tables 1.1 to 1.6 with coordinates, Chapter 1 source errata |
| `references/appendix-a-posets-lattices-fixed-points.md` | L1 reference (at most 450 lines) | Partial orders, complete lattices, chains, fixed points (Appendix A) |
| `references/appendix-b-induction-and-coinduction.md` | L1 reference (at most 450 lines) | Induction and coinduction (Appendix B) |
| `references/appendix-c-graphs-dfsf-and-rpo.md` | L1 reference (at most 450 lines) | Directed graphs, regular path sets, depth-first spanning forests, reverse postorder, loop connectedness, reducibility (Appendix C) |
| `evals/cases.yaml` | Evaluation data | Prompts with expected routing: router cases, one or more per sibling, and out-of-scope cases |
| `SUGGESTED_FIXES.md` | Maintenance | Pending suggestions for this skill |

Channel independence: a standalone L0 ambient orientation file (`ppa-foundations.md`, 80 to 250
lines) is distributed in the separate `ambient-context` channel. Neither install channel links to
or depends on the other on disk.

## Altitude Roles

- **L0 router** answers "which approach and which skill fits this task?" and contains no definitions,
  derivations or procedures.
- **L0 ambient** answers "what is the mental model and vocabulary of this area?" and is usable on its
  own, without the router.
- **L1 references** answer "what exactly is defined, under which side conditions, and how do the
  approaches compare?" Every item carries a canonical citation such as
  `[PPA §1.1, p. 1] (book p. 1; PDF p. 21)`.
- **L3 corpus** holds the verbatim source. The Chapter 1 reference points to its shard
  corpus/shards/RAW_SHARD_01_intro.md; the appendix references point to
  corpus/shards/RAW_SHARD_00_appendices.md.

## Siblings

The router names six specialised skills: `ppa-dataflow-and-slicing`,
`ppa-control-flow-and-constraints`, `ppa-abstract-interpretation`, `ppa-types-effects-and-regions`,
`ppa-fixedpoint-solvers`, `ppa-cyber-vulnerability-analysis`. Links to them are added when they
exist, so that every link resolves.
