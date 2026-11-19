<!-- @governing: REQ-TECH-PPA-001, REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-001, REQ-PRD-PPA-006 -->

# ppa-control-flow-and-constraints

Chapter 3 (`L2`) procedural skill and (`L1`) formal reference suite for *Principles of Program Analysis*
(Nielson, Nielson, Hankin, 1999 / 2005 printing): higher-order Control Flow Analysis (`0-CFA`), coinductive
acceptability and closure SOS soundness, syntax-directed and conditional subset-constraint generation,
`O(n^3)` dual-observer graph-reachability solving, coupled `CFA + DFA` monotone structures, and polyvariant
context sensitivity (`Uniform k-CFA`, `k-CFA`, `m-CFA` [external], and Agesen's `Cartesian Product Algorithm`).

## Package Contents

- `SKILL.md` (`L2`, `[250, 500)` lines): boundary dispatch, four actionable workflows with carried
  preconditions and violation symptoms, golden regression oracles, debugging table, and anti-degradation checks.
- `references/cfa-core-and-coinduction.md` (`L1`, `<= 450` lines): `FUN` syntax, `Table 3.1` abstract `0-CFA`,
  `gfp(Q)` vs `lfp(Q)` (`Proposition 3.16`), `Tables 3.2-3.4` closure SOS, `Theorem 3.10` subject reduction,
  `Fact 3.11`, Moore families (`Proposition 3.13`), and `Table 3.5` syntax-directed `0-CFA` (`§§3.1-3.3`, `Exercises 3.1-3.12`).
- `references/constraint-generation-and-cubic-solver.md` (`L1`, `<= 450` lines): `Table 3.6` conditional subset
  constraints, `Propositions 3.21-3.24`, `Table 3.7` `O(n^3)` dual-observer worklist solver, `O(n^4)` scalar
  union pitfall, `Corollary 3.25`, open systems (`p. 182`), `Mini Projects 3.1 & 3.3`, `Exercise 3.13`, and
  Set-Constraint / `[9]` (`[external: Aiken et al.]`) lazy expansion (`§3.4`, `Concluding Remarks`).
- `references/polyvariant-kcfa-cpa-and-dfa.md` (`L1`, `<= 450` lines): `Tables 3.8-3.9` coupled powerset and
  complete-lattice `CFA + DFA`, online vs staged `⊨'_D`, `Table 3.10` `Uniform k-CFA` vs `k-CFA` vs polynomial `k`-CFA / `m`-CFA [external]
  vs `CPA`, `U4`/`U5` Chapter 2 bridges, `Mini Projects 3.2 & 3.4`, and `Exercises 3.14-3.17` (`§§3.5-3.6`).
- `evals/cases.yaml`: portable positive and sibling-boundary routing test suite (`C3.10`, `C4.5-C4.7`).
- `SUGGESTED_FIXES.md`: non-blocking source errata and edge-case log (`BKL-007`, `BKL-008`, `BKL-011`, `BKL-051..062`).
