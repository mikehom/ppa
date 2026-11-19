<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-008: L0 ambient orientation for program analysis as treated in Principles of Program Analysis (Unit 1). -->
<!-- @description: Orientation on what static program analysis is and why every useful analysis must approximate: undecidability of exact answers, safe over-approximation, semantics-based correctness, and the Chapter 1 survey of formulations, together with the Appendix mathematics of partial orders, complete lattices, Tarski fixed points, ascending chains, induction versus coinduction, and flow graph traversal with dominators and loop connectedness. Use when someone asks which paradigm suits a problem, how least and greatest fixed points differ, or what an order-theoretic term means before choosing a specialised analysis. -->

# Program Analysis Foundations (Orientation)

This file gives the mental model and vocabulary for static program analysis as treated in
*Principles of Program Analysis* (F. Nielson, H. R. Nielson, C. Hankin). It defines no procedure,
states no rule system and contains no proofs. Formal statements, with every side condition, live
in the optional skill references named at the end. Citations use canonical locator tokens such as
`[PPA §1.1, p. 1] (book p. 1; PDF p. 21)` or `[PPA Preface, p. VI] (book p. VI; PDF p. 6)`.

## The Central Question

Program analysis offers "static compile-time techniques for predicting safe and computable
approximations to the set of values or behaviours arising dynamically at run-time when executing a
program on a computer" [PPA §1.1, p. 1] (book p. 1; PDF p. 21).

Three words carry the weight:

- **Static**: the program is not run; every possible run is reasoned about at once.
- **Computable**: the analysis must always terminate with an answer.
- **Safe**: the answer must not exclude anything that can actually happen.

The applications the book names are avoiding redundant computations, avoiding superfluous
computations, and validating software to reduce the likelihood of malicious or unintended
behaviour. What they share is combining information from different parts of a program
[PPA §1.1, p. 1] (book p. 1; PDF p. 21).

## Safe Approximation: "Among", Not "Are"

Exact answers to interesting questions about programs are not computable in general. The book's
example: whether a value of 2 can reach an assignment depends on whether some statement
terminates, and termination is undecidable [PPA §1.1, p. 2] (book p. 2; PDF p. 22). An analysis is
therefore expected to return a set that contains the true answer and possibly more. Figure 1.1
draws the universe of candidates, the true answer inside it, and a safe answer that contains the
true answer [PPA Figure 1.1, p. 2] (book p. 2; PDF p. 22).

Consequences for how results are read and stated:

- It is better to say "the values are **among** 1 and 2" rather than "the values **are** 1 and 2"
  [PPA §1.1, p. 3] (book p. 3; PDF p. 23). Dropping "among" turns a safe statement into a false one.
- The trivially safe answer (every candidate) is useless. Safety is necessary, precision is the
  secondary goal: `{1, 2, 27}` is acceptable, `{1, 2}` is preferred
  [PPA §1.1, p. 2] (book p. 2; PDF p. 22) [PPA §1.1, p. 3] (book p. 3; PDF p. 23) (G-U1-01, G-U1-02).
- Adding facts to a safe result keeps it safe but less precise; removing a fact that some run
  realises makes it unsafe [PPA §1.2, p. 5] (book p. 5; PDF p. 25). Imprecision and unsoundness are
  not symmetric failures.

## Semantics Based, Not Semantics Directed

The book requires analyses to be **semantics based**: the information they produce can be proved
safe with respect to a semantics of the language. New analyses "often contain subtle bugs", and a
formal justification finds them early. The book does **not** require analyses to be **semantics
directed** (shaped like the semantics), and the approaches that are semantics directed are outside
its scope [PPA §1.1, p. 3] (book p. 3; PDF p. 23)
[PPA Chapter 1 Concluding Remarks, p. 29] (book p. 29; PDF p. 49).

## Soundness Direction

"Safe" always has a direction, and the direction depends on the property (BKL-030, G-U1-03, G-U1-19):

- For a **may** property, such as which definitions may reach a point, a larger set is safe and a
  smaller set is more precise. Reaching Definitions is of this kind.
- For a **must** property, such as which variables are definitely assigned (`X` in `State(X)` of
  Table 1.3), a smaller set `X` is safe (`X₂ ⊆ X₁` weakens `State(X₁) ≤ State(X₂)`), a larger set
  `X` is more precise, and enlarging `X` beyond what every run guarantees is **unsound**
  [PPA §1.6.1, p. 20] (book p. 20; PDF p. 40) [PPA Table 1.3, p. 21] (book p. 21; PDF p. 41).

The book mostly uses "safe", "correct" and "precise", though it also prints "semantically unsound"
on p. 8 [PPA §1.3.1, p. 8] (book p. 8; PDF p. 28). Pairing over-approximation with may-analysis and
under-approximation with must-analysis, and noting that a may over-approximation yields false alarms
when hunting defects whereas it yields guarantees when proving absence, is external framing
`[external]`.

## Least Solutions and Property Order

In §§1.3–1.5, the equational, constraint, CFA and induced-AI formulations are all **may**
over-approximations ordered by subset inclusion `⊆`, so they ask for the **least** solution under
`⊆`: smaller sets are more precise, and any larger solution is still safe
[PPA §1.3.1, p. 8] (book p. 8; PDF p. 28) [PPA §1.4, p. 12] (book p. 12; PDF p. 32) (G-U1-08).

Do not generalise "smaller set = more precise, larger set = still sound" outside `⊆`-ordered
may-analyses: for a must-property such as `X` in `State(X)` (`Table 1.3`), larger sets `X` are more
precise and smaller sets are safe (Chapter 2 unifies both by orienting the lattice order `⊑` so
that `⊑` is `⊆` for may and `⊇` for must, making "least in `⊑`" always mean "most precise safe
answer") [PPA §1.6.1, p. 20] (book p. 20; PDF p. 40) (BKL-030, G-U1-19). Likewise, §1.6 specifies
correctness via existence of an annotated-type or effect derivation tree (weakened by subsumption)
rather than directly taking a least fixed point of equations
[PPA §1.6.1, p. 19] (book p. 19; PDF p. 39) [PPA §1.6.2, p. 24] (book p. 24; PDF p. 44).

Equations and inclusions over the same monotone operator `F` have the **same least solution**, while
every equation solution is also a constraint solution (`Fix(F) ⊆ Red(F)`) and the inclusions
additionally admit larger reductive solutions (`Red(F)`, `G-U1-09`)
[PPA §1.3.2, p. 10] (book p. 10; PDF p. 30). Least solutions exist and can be computed by iteration
under conditions (monotone functions, a finite or otherwise suitably bounded lattice, a start at the
least element); those conditions are stated in the Chapter 1 and Appendix A references, not here.

## Four Approaches, One Subject

The book treats four approaches: Data Flow Analysis, Constraint Based Analysis, Abstract
Interpretation, and Type and Effect Systems. Chapter 1 shows all four at the level of examples, and
its theme is that approaches which look unrelated are more similar than expected
[PPA Chapter 1, p. 1] (book p. 1; PDF p. 21). Chapter 1 specifies one analysis, Reaching
Definitions, in several of these styles, then solves it and uses it in a transformation.

| Approach | What it asks for | Information attached to | Chapter |
| :--- | :--- | :--- | :--- |
| Data Flow Analysis | Facts per program point, as equations or inclusions over a flow graph | Entry and exit of each elementary block | 2 |
| Constraint Based Analysis | Least solution of constraints generated from syntax; for higher-order code, which functions reach which call sites | Each labelled subexpression and each variable | 3 |
| Abstract Interpretation | An analysis calculated from a collecting semantics through an abstraction | Whatever the abstraction tracks | 4 |
| Type and Effect Systems | Typing judgements annotated with properties of states or with effects of execution | Each statement or expression, and function types | 5 |

How they relate, in the source's own terms:

- Data flow constraints and control flow constraints both arise from syntax and are solved for their
  least solution; control flow constraints are conditional, so their structure is more complex
  [PPA §1.4, p. 13] (book p. 13; PDF p. 33).
- Abstract Interpretation calculates an analysis rather than guessing it and validating it
  afterwards; the induced Reaching Definitions analysis lies below the equational one, and both are
  correct with respect to the collecting semantics [PPA §1.5, p. 17] (book p. 17; PDF p. 37).
- The inclusion reading of annotated base types is closer to the constraint formulation, with the
  subsumption rule playing the role of inclusion [PPA §1.6.1, p. 19] (book p. 19; PDF p. 39); type and
  effect systems are often implemented by generating and solving constraints, the approach of Chapter 5
  [PPA §1.6.1, p. 20] (book p. 20; PDF p. 40).
- Chaotic Iteration in Chapter 1 lies at the heart of many of the efficient algorithms of Chapters 2
  and 6 [PPA §1.7, p. 25] (book p. 25; PDF p. 45).
- Some annotated type systems are closely related to Hoare's logic for partial correctness
  [PPA Chapter 1 Concluding Remarks, p. 29] (book p. 29; PDF p. 49).

## Vocabulary

| Term | Meaning in this book |
| :--- | :--- |
| Elementary block | An assignment, a `skip`, or the test of a conditional or loop: the unit to which facts attach in WHILE |
| Label | The identity of an elementary block; Chapter 1 assumes distinct blocks carry distinct labels |
| `?` | A special label outside the program, meaning "possibly uninitialised" |
| Reaching definition | An assignment that may be the last one to a variable when a point is reached |
| Flow graph | Nodes are elementary blocks, edges are possible transfers of control |
| Least solution | The smallest result consistent with the program; the most precise safe answer of a formulation |
| Collecting semantics | A semantics that gathers the possible run-time behaviours (traces) at each point |
| Abstraction, concretisation | The maps `α` and `γ` between concrete behaviours and analysis properties |
| Adjunction (Galois connection) | A pair `(α, γ)` with `α(X) ⊆ Y` exactly when `X ⊆ γ(Y)` |
| Induced analysis | An analysis calculated from a collecting semantics through `α` and `γ` |
| Optimal | Induced analysis equal to the specified one, for the chosen properties |
| Annotated type | A type decorated with analysis information, such as a set of reaching definitions |
| Effect | What may happen when a statement or expression runs, such as which functions are applied |
| Latent effect | The effect recorded on a function type, released when the function is applied |
| Subsumption | A rule that weakens a judgement to a less precise but still safe one |
| Transformation | A rewrite justified by analysis results, such as Constant Folding |

Coordinates: [PPA §1.2, p. 3] (book p. 3; PDF p. 23) [PPA §1.2, p. 5] (book p. 5; PDF p. 25)
[PPA §1.5, p. 13] (book p. 13; PDF p. 33) [PPA §1.5, p. 15] (book p. 15; PDF p. 35)
[PPA §1.5, p. 17] (book p. 17; PDF p. 37) [PPA §1.6.1, p. 18] (book p. 18; PDF p. 38)
[PPA §1.6.2, p. 24] (book p. 24; PDF p. 44) [PPA §1.8, p. 27] (book p. 27; PDF p. 47).

## Analyses Feed Transformations

An analysis result is an input to transformations such as Constant Folding. Whether a result stays
valid after a transformation depends on whether the transformation changes anything the analysis
observes. For Reaching Definitions under Constant Folding it does not, so one result serves a whole
sequence of steps; the book does not generalise this [PPA §1.8, p. 29] (book p. 29; PDF p. 49).

## What the Book Does Not Cover

The Preface states that the book does not treat denotationally based program analysis, projection
analysis, or logical formulations based on Stone dualities, and omits for space a deeper treatment
of set constraints, fast techniques for implementing type based analyses, single static assignment
form, a broader treatment of pointer analyses, and the interplay between analysis and
transformation, including efficient recomputation of invalidated analysis information
[PPA Preface, p. VI] (book p. VI; PDF p. 6) (G-U1-33). The Preface also asks that Chapter 1 be read
in full but quickly [PPA Preface, p. VI] (book p. VI; PDF p. 6). Answers on these omitted topics are
external to the book and should be labelled `[external]`.

## Where to Go Next

This ambient file is self-contained as an orientation channel. When the optional `skills/` channel
is also installed, formal details live at plain paths relative to the knowledge root:

- Router (which approach or skill fits a task): skills/ppa-program-analysis/SKILL.md
- Chapter 1 formulations side by side, Tables 1.1 to 1.6, source errata:
  skills/ppa-program-analysis/references/chapter-1-five-formulations.md
- Partial orders, complete lattices, fixed points:
  skills/ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md
- Induction and coinduction:
  skills/ppa-program-analysis/references/appendix-b-induction-and-coinduction.md
- Directed graphs, depth-first spanning forests, reverse postorder, loop connectedness:
  skills/ppa-program-analysis/references/appendix-c-graphs-dfsf-and-rpo.md
- Specialised skills, one per approach or concern: ppa-dataflow-and-slicing,
  ppa-control-flow-and-constraints, ppa-abstract-interpretation, ppa-types-effects-and-regions,
  ppa-fixedpoint-solvers, ppa-cyber-vulnerability-analysis.
