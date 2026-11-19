<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 1. -->

# RAW_SHARD_01 — Chapter 1 Introduction (Unit 1)

Source: *Principles of Program Analysis* (Nielson, Nielson, Hankin), corrected 2nd printing, 2005.
Scope: Chapter 1, the chapter opening, §1.1–§1.8, Concluding Remarks, Mini Project 1.1 and
Exercises 1.1–1.11, book pages 1–33 (PDF pages 21–53).

Coordinates: PDF page = book page + 20 throughout the chapter. Book p. 34 is a blank page absent from
the PDF and is never cited. Section starts inside the chapter: §1.3.1 on p. 5, §1.3.2 on p. 8,
§1.6.1 on p. 18, §1.6.2 on p. 22; Table 1.6 is printed at the top of p. 27, before the §1.8 heading on
the same page. Concluding Remarks and the Mini Projects heading are on p. 29; the Exercises heading is
on p. 31.

Conventions:

- Each item is cited twice: an inline `N8` citation and its book/PDF companion pair, e.g.
  [PPA §1.1, p. 1] (book p. 1; PDF p. 21). Concluding Remarks, Mini Projects and Exercises use the
  region locators `Chapter 1 Concluding Remarks`, `Chapter 1 Mini Projects` and `Chapter 1 Exercises`.
- The Preface is roman-paginated and is cited via [PPA Preface, p. VI] (book p. VI; PDF p. 6).
- Items with a book number keep that number exactly. Unnumbered items carry non-book ids
  `[U1:<section>-<letter>]`; these ids are not book numbering. Chapter 1 numbers no definitions,
  lemmas or theorems.
- Math is transcribed from page images, not from the text layer (the text layer drops Example 1.1,
  Example 1.2 and most of Tables 1.3, 1.4 and 1.6). Proofs are summarised.
- Terms the book does not use carry the tag `[external]`. Statements derived by the shard author
  rather than printed in the book are tagged `[derived]`.
- Notation: `ℓ` labels; `[B]^ℓ` a labelled elementary block; `RD⃗` the twelve-tuple (printed `RD` with
  an arrow above); `∅⃗` the tuple of empty sets; `Var⋆`, `Lab⋆`, `S⋆` the star-subscripted sets and
  program "of interest" (a subscript star, not a Kleene star); `Ĉ`, `ρ̂`, `τ̂`, `Γ̂` the hatted symbols.
  `S : Σ --X-->_{RD} Σ` stands for an arrow with `X` printed above and `RD` below;
  `τ̂₁ --φ--> τ̂₂` for an arrow annotated with the effect `φ`. `■` ends an Example, Mini Project or
  Exercise as printed.
- Source errors are recorded as findings `F-U1-NN` and are not corrected in transcriptions. The one
  error that changes a formal result carries the tag `[Source Erratum → BKL]`.

## Chapter 1 Opening

Context: the chapter opens on p. 1 before the §1.1 heading and states the plan of the book
[PPA Chapter 1, p. 1] (book p. 1; PDF p. 21).

### [U1:1.0-a] The four approaches and the purpose of the chapter (unnumbered remark)
- Statement: the book introduces four of the main approaches to program analysis: Data Flow Analysis,
  Constraint Based Analysis, Abstract Interpretation, and Type and Effect Systems. Each of Chapters 2–5
  treats one approach, with more advanced material in later sections. Chapter 1 treats all four "at
  the level of examples"; technical details are worked out, but applying them to related examples may
  need the later chapters. Running theme: "the many similarities between what may at a first glance
  appear to be very unrelated approaches".
- Citation: [PPA Chapter 1, p. 1] (book p. 1; PDF p. 21)

### [U1:1.0-b] Preface scope exclusions that Chapter 1 touches (unnumbered remark)
- Statement: the Preface says the book does not treat, in order to cover the four main approaches to
  some depth, "denotationally based program analysis, projection analysis, and logical formulations
  based on Stone dualities". For reasons of space it also omits "a deeper treatment of set
  constraints, fast techniques for implementing type based analyses, single static assignment form, a
  broader treatment of pointer analyses, and the interplay between analysis and transformation and how
  to efficiently recompute analysis information invalidated by the transformation". The Preface says
  Chapter 1 "is intended to be read quickly" and recommends reading all of it [PPA Preface, p. VI]
  (book p. VI; PDF p. 6).
- Side conditions: Chapter 1 points at these exclusions in three places: semantics directed
  approaches "are not covered in this book" [PPA §1.1, p. 3] (book p. 3; PDF p. 23); the denotational
  and logic based approaches are named in [PPA Chapter 1 Concluding Remarks, p. 29] (book p. 29; PDF p. 49);
  re-use of an analysis across transformations is shown only for Reaching Definitions with Constant
  Folding [PPA §1.8, p. 29] (book p. 29; PDF p. 49), a special case of the excluded "interplay" topic.
- Citation: [PPA Preface, p. VI] (book p. VI; PDF p. 6); [PPA Chapter 1, p. 1] (book p. 1; PDF p. 21)

### Projections (Chapter 1 Opening)
- cs_theory: four specification styles for static analysis share a semantic-soundness backbone across
  Reaching Definitions (§§1.3, 1.5, 1.6.1, 1.7) and functional call-tracking examples (§§1.4, 1.6.2).
- swe_architecture: choose the specification style by its consumer (solver, checker, correctness
  proof) rather than by the property computed; the out-of-scope list (SSA, fast type-based
  implementation, pointer analysis, incremental re-analysis) marks where a design must draw on other
  sources [external].
- practical_debugging: a question that falls in a Preface exclusion has no grounded answer in this
  book; answers drawing on outside knowledge must be labelled [external].
- cyber: the book itself names validation of purchased software against malicious behaviour as an
  application (§1.1); security analyses built from it inherit only the four approaches, not the excluded
  pointer-analysis depth.

## 1.1 The Nature of Program Analysis

Context: what program analysis is, why answers are approximate, and the semantics-based stance
[PPA §1.1, p. 1] (book p. 1; PDF p. 21).

### [U1:1.1-a] Program analysis (unnumbered informal definition)
- Statement: "Program analysis offers static compile-time techniques for predicting safe and
  computable approximations to the set of values or behaviours arising dynamically at run-time when
  executing a program on a computer."
- Applications stated: compilers avoiding *redundant* computations (re-using available results,
  moving loop-invariant computations out of loops) and *superfluous* computations (results known not
  to be needed, or known at compile time); more recently, "validation of software (possibly purchased
  from sub-contractors) to reduce the likelihood of malicious or unintended behaviour". Common to all:
  the need to combine information from different parts of the program.
- Side conditions: the approaches share "a large amount of commonality", which helps in choosing "the
  right approach for the right task" [PPA §1.1, p. 2] (book p. 2; PDF p. 22).
- Citation: [PPA §1.1, p. 1] (book p. 1; PDF p. 21)

### Figure 1.1 — The nature of approximation: erring on the safe side
- Content: a box representing the universe `{d₁, ···, d_N}`. A top brace marks the "true answer"
  `{d₁, ···, d_n}` and the rest `{d_{n+1}, ···, d_N}`; a bottom brace marks the "safe answer"
  `{d₁, ···, d_n, ···, d_{n+m}}`. A solid slanted line marks the true-answer boundary and a dashed line
  the safe-answer boundary. The safe answer contains the true answer and possibly more.
- Citation: [PPA Figure 1.1, p. 2] (book p. 2; PDF p. 22)

### [U1:1.1-b] Approximation and undecidability (unnumbered example)
- Statement: program `read(x); (if x>0 then y:=1 else (y:=2;S)); z:=y`, where `S` contains no
  assignment to `y`. Intuitively the values of `y` reaching `z:=y` are 1 or 2. An analysis saying only
  1 reaches is correct if `S` never terminates when `x ≤ 0` and `y = 2`, but "it is undecidable whether
  or not S terminates", so analyses are not expected to detect this. "In order to remain computable
  one can only provide approximate answers": the analysis gives "a possibly larger set of possibilities
  than what will ever happen". An answer "among 1, 2 or 27" is acceptable; "among 1 or 2" is preferred
  as more precise.
- Side conditions: the book argues only from undecidability of termination of `S`; the general result
  (Rice's theorem [external]) is not named in Chapter 1.
- Citation: [PPA §1.1, p. 2] (book p. 2; PDF p. 22)

### [U1:1.1-c] Useful but imprecise; the "among" wording (unnumbered remark)
- Statement: the challenge is not to produce the safe answer `{d₁, ···, d_N}` too often, "as the
  analysis will then be utterly useless". Even `{1, 2, 27}` shows that `z` is positive and fits in one
  byte. "It is better to say 'the values of y possible at z:=y are among 1 and 2' than the slightly
  shorter and more frequently used 'the values of y possible at z:=y are 1 and 2'".
- Citation: [PPA §1.1, p. 3] (book p. 3; PDF p. 23)

### [U1:1.1-d] Semantics based versus semantics directed (unnumbered principle)
- Statement: "all program analyses should be semantics based": the information obtained "can be
  proved to be safe (or correct) with respect to a semantics of the programming language". New
  analyses "often contain subtle bugs", and a formal justification helps find them "sooner rather than
  later". The book does *not* suggest that analyses be *semantics directed* (the structure of the
  analysis reflects the structure of the semantics); that holds "only for a few approaches which are
  not covered in this book".
- Side conditions: restated, with the semantics directed approaches named, in
  [PPA Chapter 1 Concluding Remarks, p. 29] (book p. 29; PDF p. 49).
- Citation: [PPA §1.1, p. 3] (book p. 3; PDF p. 23)

### Projections (1.1)
- cs_theory: "safe" means over-approximating a set of run-time values or behaviours; precision is the
  secondary objective; undecidability of termination forces approximation (soundness and precision
  [external] in later vocabulary).
- swe_architecture: report analysis results as "among" sets with explicit direction; a semantics-based
  design keeps a reference semantics next to the analysis so safety can be proved or tested against
  it, without forcing the analysis to mirror that semantics.
- practical_debugging: a reported value that never occurs is imprecision, not a defect; a run
  exhibiting a value the analysis excluded is a defect; an analysis that always returns the whole
  universe is useless even though safe.
- cyber: the book names validation of sub-contracted software against "malicious or unintended
  behaviour"; a sound over-approximating checker [external] can prove absence of a bad value (z > 0
  fits in one byte), while an alert may be a false positive [external] drawn from the extra
  `{d_{n+1}, ···, d_{n+m}}`.

## 1.2 Setting the Scene

Context: the WHILE language, elementary blocks and labels, and the running example (Reaching
Definitions on the factorial program) [PPA §1.2, p. 3] (book p. 3; PDF p. 23).

### [U1:1.2-a] Elementary blocks and the distinct-labels assumption (unnumbered assumption)
- Statement: a WHILE program is a statement, normally a sequence of statements. Data flow information
  is associated with single assignment statements, tests in conditionals and loops, and `skip`
  statements; these labelled items are *elementary blocks*. "In this chapter we will assume that
  distinct elementary blocks are initially assigned distinct labels; we could drop this requirement, in
  which case some of the examples would need to be slightly reformulated and the resultant analyses
  would be less accurate".
- Citation: [PPA §1.2, p. 3] (book p. 3; PDF p. 23)

### [U1:1.2-b] Syntactic categories (unnumbered definition)
- Statement:

```
a ∈ AExp    arithmetic expressions      x, y ∈ Var   variables
b ∈ BExp    boolean expressions            n ∈ Num   numerals
S ∈ Stmt    statements                     ℓ ∈ Lab   labels
op_a ∈ Op_a arithmetic operators   op_b ∈ Op_b boolean operators   op_r ∈ Op_r relational operators
```

- Side conditions: some countable set of variables is assumed; numerals, labels and operators are not
  further defined.
- Citation: [PPA §1.2, p. 3] (book p. 3; PDF p. 23); operator categories on [PPA §1.2, p. 4] (book p. 4; PDF p. 24)

### [U1:1.2-c] Abstract syntax of WHILE (unnumbered definition)
- Statement:

```
a ::= x | n | a₁ op_a a₂
b ::= true | false | not b | b₁ op_b b₂ | a₁ op_r a₂
S ::= [x := a]^ℓ | [skip]^ℓ | S₁; S₂ | if [b]^ℓ then S₁ else S₂ | while [b]^ℓ do S
```

- Side conditions: the syntax is abstract (parse trees); the book is not concerned with concrete
  syntax. Parentheses `(···)` disambiguate statements (instead of `begin ··· end` or `{···}`) and other
  categories; the familiar relative precedences of arithmetic, boolean and relational operators apply.
- Citation: [PPA §1.2, p. 4] (book p. 4; PDF p. 24)

### Example 1.1 — The factorial program
- Statement: the program "computes the factorial of the number stored in x and leaves the result in z":

```
[y:=x]^1; [z:=1]^2; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6   ■
```

- Side conditions: the program is absent from the text layer and is transcribed from the page image.
  It is re-used by Figure 1.2, Tables 1.1 and 1.5, Examples 1.3 and 1.4, the trace on p. 13 and the
  p. 9 constraint system.
- Citation: [PPA Example 1.1, p. 4] (book p. 4; PDF p. 24)

### [U1:1.2-d] Reaching Definitions, "reaching assignments" (unnumbered informal definition)
- Statement: distinct labels let the analysis identify the primitive constructs of a program "without
  explicitly constructing a flow graph". The analysis "should be called more properly, reaching
  assignments analysis": "An assignment (called a definition in the classical literature) of the form
  `[x := a]^ℓ` *may reach* a certain program point (typically the entry or exit of an elementary block)
  if there is an execution of the program where `x` was last assigned a value at `ℓ` when the program
  point is reached."
- Conventions: the pair `(y,1)` reaching the entry to 2 means `[y:=x]^1` reaches `[z:=1]^2`. The pair
  `(x,?)` uses "a special label not appearing in the program" to record the possibility of an
  uninitialised variable reaching a program point. The full information is a pair
  `RD = (RD_entry, RD_exit)` of functions.
- Citation: [PPA §1.2, p. 4] (book p. 4; PDF p. 24); the conventions are on [PPA §1.2, p. 5] (book p. 5; PDF p. 25)

### Table 1.1 — Reaching Definitions information for the factorial program
- Content:

| ℓ | RD_entry(ℓ) | RD_exit(ℓ) |
| :-- | :-- | :-- |
| 1 | (x,?), (y,?), (z,?) | (x,?), (y,1), (z,?) |
| 2 | (x,?), (y,1), (z,?) | (x,?), (y,1), (z,2) |
| 3 | (x,?), (y,1), (y,5), (z,2), (z,4) | (x,?), (y,1), (y,5), (z,2), (z,4) |
| 4 | (x,?), (y,1), (y,5), (z,2), (z,4) | (x,?), (y,1), (y,5), (z,4) |
| 5 | (x,?), (y,1), (y,5), (z,4) | (x,?), (y,5), (z,4) |
| 6 | (x,?), (y,1), (y,5), (z,2), (z,4) | (x,?), (y,6), (z,2), (z,4) |

- Side conditions: entry and exit agree for blocks `[b]^ℓ`; for blocks `[x := a]^ℓ` they may differ on
  pairs `(x, ℓ′)` [PPA §1.2, p. 5] (book p. 5; PDF p. 25). Exercise 1.7 shows this is the least
  solution of the §1.3 equations.
- Citation: [PPA Table 1.1, p. 4] (book p. 4; PDF p. 24)

### [U1:1.2-e] Safe and unsafe modifications of Table 1.1 (unnumbered remark)
- Statement: adding `(z,2)` to `RD_entry(5)` and `RD_exit(5)` keeps the information safe but "more
  approximate". Removing `(z,2)` from `RD_entry(6)` and `RD_exit(6)` makes it unsafe: some run of the
  factorial program is not described by `{(x,?),(y,6),(z,4)}` at the exit of 6.
- Side conditions: [derived] the witnessing run is one where the loop body never executes (`x ≤ 1`),
  so `z` was last assigned at 2.
- Citation: [PPA §1.2, p. 5] (book p. 5; PDF p. 25)

### Projections (1.2)
- cs_theory: Reaching Definitions is a may-property [external] over executions; the label `?` makes the
  entry information total, so "possibly uninitialised" is itself a reaching definition.
- swe_architecture: unique labels on elementary blocks are stable identities for program points and
  let an analysis run on the labelled syntax tree without a separate flow-graph pass; uniqueness is a
  precision property, not only a convenience.
- practical_debugging: to test a Reaching Definitions result, adding pairs can only cost precision,
  while a single concrete run contradicting a row (a loop executed zero times) proves a defect.
- cyber: `(x,?) ∈ RD_entry(ℓ)` for a variable read at `ℓ` flags a possibly uninitialised use
  [external: uninitialised-variable weakness classes]; in Table 1.1 `(x,?)` reaches every block, as
  expected for the input variable `x`, while `(y,?)` and `(z,?)` are killed at 1 and 2.

## 1.3 Data Flow Analysis

Context: the program as a graph; §1.3.1 the equational approach (p. 5); §1.3.2 the constraint based
approach (p. 8), a stepping stone to §1.4 [PPA §1.3, p. 5] (book p. 5; PDF p. 25).

### [U1:1.3-a] Program as graph; two classes of equations (unnumbered remark)
- Statement: "It is customary to think of a program as a graph: the nodes are the elementary blocks
  and the edges describe how control might pass from one elementary block to another". The section
  presents the "more common" equational approach and then a constraint based approach. One class of
  equations relates the exit information of a node to its entry information; the other relates the
  entry information of a node to the exit information of the nodes with an edge to it.
- Citation: [PPA §1.3, p. 5] (book p. 5; PDF p. 25); the two classes are introduced in [PPA §1.3.1, p. 5] (book p. 5; PDF p. 25)

### Figure 1.2 — Flow graph for the factorial program
- Content: an entry arrow into `[y:=x]^1`, then `[z:=1]^2`, then `[y>1]^3`. From 3, "yes" leads to
  `[z:=z*y]^4`, then `[y:=y-1]^5`, and a back edge returns to 3; "no" leads to `[y:=0]^6`, followed by an
  exit arrow. Edges: (1,2), (2,3), (3,4), (4,5), (5,3), (3,6).
- Citation: [PPA Figure 1.2, p. 6] (book p. 6; PDF p. 26)

### [U1:1.3.1-a] Equations, class 1: exit from entry (unnumbered display)
- Statement: the six equations

```
RD_exit(1) = (RD_entry(1) \ {(y,ℓ) | ℓ ∈ Lab}) ∪ {(y,1)}
RD_exit(2) = (RD_entry(2) \ {(z,ℓ) | ℓ ∈ Lab}) ∪ {(z,2)}
RD_exit(3) = RD_entry(3)
RD_exit(4) = (RD_entry(4) \ {(z,ℓ) | ℓ ∈ Lab}) ∪ {(z,4)}
RD_exit(5) = (RD_entry(5) \ {(y,ℓ) | ℓ ∈ Lab}) ∪ {(y,5)}
RD_exit(6) = (RD_entry(6) \ {(y,ℓ) | ℓ ∈ Lab}) ∪ {(y,6)}
```

- Schema: for an assignment `[x := a]^ℓ′`, exclude all pairs `(x,ℓ)` from `RD_entry(ℓ′)` and add
  `(x,ℓ′)` to obtain `RD_exit(ℓ′)`; the book adds "this reflects that x is redefined at ℓ" (finding
  F-U1-02). For all other elementary blocks `[···]^ℓ′`, `RD_exit(ℓ′) = RD_entry(ℓ′)`, "reflecting that
  no variables are changed".
- Side conditions: the kill set ranges over all of `Lab`; with `Lab⋆ = {1, ···, 6, ?}` ([U1:1.3.1-c])
  it includes `?`, so `(x,?)` is killed by an assignment to `x`.
- Citation: [PPA §1.3.1, p. 6] (book p. 6; PDF p. 26)

### Findings (1.3.1)
- F-U1-02 (BKL-034): on p. 6 the schema text prints "this reflects that x is redefined at ℓ", while the
  assignment under discussion is `[x := a]^ℓ′` and the added pair is `(x, ℓ′)`; the primes are legible
  elsewhere on the same page image. Recorded, not corrected. [PPA §1.3.1, p. 6] (book p. 6; PDF p. 26)

### [U1:1.3.1-b] Equations, class 2: entry from predecessors' exits (unnumbered display)
- Statement:

```
RD_entry(2) = RD_exit(1)
RD_entry(3) = RD_exit(2) ∪ RD_exit(5)
RD_entry(4) = RD_exit(3)
RD_entry(5) = RD_exit(4)
RD_entry(6) = RD_exit(3)
```

- General form: `RD_entry(ℓ) = RD_exit(ℓ₁) ∪ ··· ∪ RD_exit(ℓ_n)` if `ℓ₁, ···, ℓ_n` are all the labels
  from which control might pass to `ℓ` (made precise in Chapter 2). Initial block:
  `RD_entry(1) = {(x,?) | x is a variable in the program}`, here `{(x,?), (y,?), (z,?)}`.
- Citation: [PPA §1.3.1, p. 6] (book p. 6; PDF p. 26); the remaining equations, the general form and the initial equation are on [PPA §1.3.1, p. 7] (book p. 7; PDF p. 27)

### [U1:1.3.1-c] The equation system as a function F (unnumbered definition)
- Statement: the twelve sets `RD_entry(1), ···, RD_exit(6)` form a tuple `RD⃗`, and the system demands
  `RD⃗ = F(RD⃗)` with
  `F(RD⃗) = (F_entry(1)(RD⃗), F_exit(1)(RD⃗), ···, F_entry(6)(RD⃗), F_exit(6)(RD⃗))`, e.g.
  `F_entry(3)(···, RD_exit(2), ···, RD_exit(5), ···) = RD_exit(2) ∪ RD_exit(5)`.
- Functionality: `F : (𝒫(Var⋆ × Lab⋆))¹² → (𝒫(Var⋆ × Lab⋆))¹²`. Taking `Var⋆ = Var` and `Lab⋆ = Lab`
  would be natural, but the chapter takes `Var⋆` to be a *finite* subset of `Var` containing the
  variables of the program `S⋆` of interest, and similarly `Lab⋆`. Here `Var⋆ = {x, y, z}` and
  `Lab⋆ = {1, ···, 6, ?}`.
- Citation: [PPA §1.3.1, p. 7] (book p. 7; PDF p. 27)

### [U1:1.3.1-d] Ordering; complete lattice (unnumbered definition)
- Statement: `RD⃗ ⊑ RD⃗′ iff ∀i : RD_i ⊆ RD′_i`, where `RD⃗ = (RD₁, ···, RD₁₂)`. This makes
  `(𝒫(Var⋆ × Lab⋆))¹²` a complete lattice (Appendix A) with least element `∅⃗ = (∅, ···, ∅)` and binary
  least upper bounds `RD⃗ ⊔ RD⃗′ = (RD₁ ∪ RD′₁, ···, RD₁₂ ∪ RD′₁₂)`.
- Citation: [PPA §1.3.1, p. 7] (book p. 7; PDF p. 27); the least element and least upper bounds are on [PPA §1.3.1, p. 8] (book p. 8; PDF p. 28)

### [U1:1.3.1-e] Monotonicity of F (unnumbered claim)
- Statement: `RD⃗ ⊑ RD⃗′` implies `F(RD⃗) ⊑ F(RD⃗′)`.
- Proof (summary): typical step: `RD_exit(2) ⊆ RD′_exit(2)` and `RD_exit(5) ⊆ RD′_exit(5)` give
  `RD_exit(2) ∪ RD_exit(5) ⊆ RD′_exit(2) ∪ RD′_exit(5)`; the details are left to the reader.
- Side conditions: [derived] monotonicity holds because `\` only ever removes a constant set
  `{(x,ℓ) | ℓ ∈ Lab}`.
- Citation: [PPA §1.3.1, p. 8] (book p. 8; PDF p. 28)

### [U1:1.3.1-f] Least solution by iteration from ∅⃗ (unnumbered result)
- Statement: `∅⃗ ⊑ F(∅⃗)`; by monotonicity and mathematical induction (Appendix B),
  `Fⁿ(∅⃗) ⊑ Fⁿ⁺¹(∅⃗)` for all `n`. The lattice is a finite set, so the chain cannot consist of distinct
  elements: some `n` has `Fⁿ⁺¹(∅⃗) = Fⁿ(∅⃗)`, i.e. `Fⁿ(∅⃗)` is a fixed point of `F` and a solution. It is
  the *least* solution: if `RD⃗ = F(RD⃗)` then `Fⁿ(∅⃗) ⊑ RD⃗` by induction.
- Side conditions: the least solution "contains the fewest pairs of reaching definitions that are
  consistent with the program"; more pairs keep the analysis semantically sound but "less usable".
  The construction relies on finiteness of `Var⋆` and `Lab⋆`. Kleene iteration [external]; the general
  theorems are in Appendix A.
- Citation: [PPA §1.3.1, p. 8] (book p. 8; PDF p. 28)

### [U1:1.3.2-a] Constraints, class 1: effect of elementary blocks (unnumbered display)
- Statement: the approach extracts "a number of inclusions (or inequations or constraints) out of a
  program"; "it is not a general phenomenon that the constraints are naturally divided into two
  classes as was the case for the equations". For the factorial program:

```
RD_exit(1) ⊇ RD_entry(1) \ {(y,ℓ) | ℓ ∈ Lab}      RD_exit(1) ⊇ {(y,1)}
RD_exit(2) ⊇ RD_entry(2) \ {(z,ℓ) | ℓ ∈ Lab}      RD_exit(2) ⊇ {(z,2)}
RD_exit(3) ⊇ RD_entry(3)
RD_exit(4) ⊇ RD_entry(4) \ {(z,ℓ) | ℓ ∈ Lab}      RD_exit(4) ⊇ {(z,4)}
RD_exit(5) ⊇ RD_entry(5) \ {(y,ℓ) | ℓ ∈ Lab}      RD_exit(5) ⊇ {(y,5)}
RD_exit(6) ⊇ RD_entry(6) \ {(y,ℓ) | ℓ ∈ Lab}      RD_exit(6) ⊇ {(y,6)}
```

- Methodology stated: an assignment `[x := a]^ℓ′` gets one constraint that excludes all pairs `(x,ℓ)`
  from `RD_entry(ℓ′)` in reaching `RD_exit(ℓ′)` and one that incorporates `(x,ℓ′)`; every other block
  `[···]^ℓ′` gets one constraint that lets everything in `RD_entry(ℓ′)` reach `RD_exit(ℓ′)`.
- Citation: [PPA §1.3.2, p. 8] (book p. 8; PDF p. 28); the display and methodology are on [PPA §1.3.2, p. 9] (book p. 9; PDF p. 29)

### [U1:1.3.2-b] Constraints, class 2: control flow; initialisation (unnumbered display)
- Statement, transcribed exactly as printed (five control-flow inclusions):

```
RD_entry(2) ⊇ RD_exit(1)
RD_entry(3) ⊇ RD_exit(2)
RD_entry(3) ⊇ RD_exit(5)
RD_entry(5) ⊇ RD_exit(4)
RD_entry(6) ⊇ RD_exit(3)
```

- General rule stated: "In general, we have a constraint `RD_entry(ℓ) ⊇ RD_exit(ℓ′)` if it is possible
  for control to pass from `ℓ′` to `ℓ`." Initialisation: `RD_entry(1) ⊇ {(x,?), (y,?), (z,?)}` "records
  that we cannot be sure about the definition point of uninitialised variables".
- Note `[Source Erratum → BKL-025]`: the printed list omits `RD_entry(4) ⊇ RD_exit(3)`. The omission is
  present on the page image and in the text layer. The constraint is required by the matching equation
  `RD_entry(4) = RD_exit(3)` on p. 7, by the edge (3,4) of Figure 1.2, by the general rule printed
  directly below the list, and by the p. 10 claim that the equation and constraint systems have the
  same least solution. [derived] Taken literally, the printed system has a least solution with
  `RD_entry(4) = ∅`, which contradicts Table 1.1. Finding F-U1-01.
- Citation: [PPA §1.3.2, p. 9] (book p. 9; PDF p. 29)

### Findings (1.3.2)
- F-U1-01 (BKL-025): the p. 9 control-flow constraint list prints five inclusions and omits
  `RD_entry(4) ⊇ RD_exit(3)`, although p. 7, Figure 1.2 and the p. 10 equivalence claim require it.
  Recorded, not corrected; transcriptions keep the printed five lines. [Source Erratum → BKL-025]
  [PPA §1.3.2, p. 9] (book p. 9; PDF p. 29)

### [U1:1.3.2-c] Equations and inclusions share the least solution (unnumbered result)
- Statement: collecting the constraints with the same left-hand side, e.g.
  `RD_exit(1) ⊇ (RD_entry(1) \ {(y,ℓ) | ℓ ∈ Lab}) ∪ {(y,1)}`, does not change the set of solutions.
  The equational approach demands `RD⃗ = F(RD⃗)`; the constraint based approach demands `RD⃗ ⊒ F(RD⃗)`
  "for the *same* function F". "A solution to the equation system is also a solution to the constraint
  system whereas the converse is not necessarily the case." Both have the same least solution.
- Proof (summary): if `RD⃗ ⊒ F(RD⃗)` then `∅⃗ ⊑ RD⃗`, and monotonicity plus induction give
  `Fⁿ(∅⃗) ⊑ RD⃗`; since `Fⁿ(∅⃗)` also solves the constraint system, it is its least solution.
- Side conditions: the connection "is not always as apparent as it is here": constraints with the same
  left-hand side are often generated at many places in the program, "and therefore it may require
  serious work to collect them". The equivalence holds for the full constraint system (see F-U1-01).
  In lattice terms the constraint solutions are the reductive points [external to Chapter 1; cf.
  Appendix A] of `F`, whose meet is `lfp(F)`.
- Citation: [PPA §1.3.2, p. 10] (book p. 10; PDF p. 30)

### Projections (1.3)
- cs_theory: one monotone `F` on the finite complete lattice `(𝒫(Var⋆ × Lab⋆))¹²`; equations ask for
  its fixed points, inclusions for its reductive points; both have least element `Fⁿ(∅⃗)`.
- swe_architecture: the equational form suits a pass that owns one defining equation per node
  (predecessor lists known up front); the inclusion form suits generators that emit constraints from
  many syntax sites independently, followed by a collection and solving step (constraint-graph
  architecture [external]). The solver can be generic over `F`.
- practical_debugging: compare the number of generated flow constraints with the number of flow-graph
  edges (six for Figure 1.2); a missing edge starves its target (`RD_entry(4) = ∅` under the printed
  p. 9 list), giving an unsound result, not an imprecise one. A kill set that omits `?` leaves `(x,?)`
  alive and produces spurious "possibly uninitialised" reports. A result from a solver seeded with old
  state can be a non-least solution: re-solve from `∅⃗`.
- cyber: rule-based query engines [external: Datalog-style engines] encode each inclusion as a monotone
  rule, so new edges (callbacks, framework entry points [external]) can be added without rewriting
  transfer functions; a missing rule silently yields false negatives [external], exactly the shape of
  the p. 9 omission.

## 1.4 Constraint Based Analysis

Context: Control Flow Analysis for a functional language, expressed as a Constraint Based Analysis
[PPA §1.4, p. 10] (book p. 10; PDF p. 30).

### [U1:1.4-a] Control Flow Analysis: purpose and motivating program (unnumbered remark)
- Statement: the purpose of Control Flow Analysis is "to determine information about what 'elementary
  blocks' may lead to what other 'elementary blocks'". This is "immediately available for the WHILE
  language unlike what is the case for more advanced imperative, functional and object-oriented
  languages". "Often Control Flow Analysis is expressed as a Constraint Based Analysis." Motivating
  program:

```
let  f = fn x => x 1;
     g = fn y => y+2;
     h = fn z => z+3
in   (f g) + (f h)
```

- Side conditions: `x` is bound to `g` and then to `h`; the result is 7. Applying `f` transfers
  control to the body `x 1`, and applying `x` transfers control to the body of whatever `x` is bound
  to, which is not known without knowing how `f` is called. Specification: "For each function
  application, which functions may be applied." In functional languages "elementary blocks" may be
  nested, so *all* subexpressions are labelled. The book does not use the names 0-CFA [external] or
  `FUN` [external] in Chapter 1.
- Citation: [PPA §1.4, p. 10] (book p. 10; PDF p. 30); the program and specification are on [PPA §1.4, p. 11] (book p. 11; PDF p. 31)

### Example 1.2 — Identity applied to identity
- Statement:

```
[[fn x => [x]^1]^2 [fn y => [y]^3]^4]^5
```

  The identity function `fn x => x` is applied to `fn y => y` and evaluates to `fn y => y` (omitting
  all `[···]^ℓ`). ■
- Side conditions: the program is absent from the text layer and is transcribed from the page image.
- Citation: [PPA Example 1.2, p. 11] (book p. 11; PDF p. 31)

### [U1:1.4-b] The analysis pair (Ĉ, ρ̂) (unnumbered definition)
- Statement: information is associated "with the labels themselves, rather than with the entries and
  exits" of blocks, exploiting the absence of side effects. `Ĉ(ℓ)` contains the values that the
  subexpression labelled `ℓ` may evaluate to; `ρ̂(x)` contains the values that `x` can be bound to.
- Citation: [PPA §1.4, p. 11] (book p. 11; PDF p. 31)

### [U1:1.4-c] Three classes of constraints; conditional constraints (unnumbered display)
- Statement:
  1. Abstractions: `{fn x => [x]^1} ⊆ Ĉ(2)` and `{fn y => [y]^3} ⊆ Ĉ(4)`. "A function abstraction
     evaluates to a closure containing the abstraction itself", so an occurrence of `[fn x => e]^ℓ`
     gives `{fn x => e} ⊆ Ĉ(ℓ)`.
  2. Variables: `ρ̂(x) ⊆ Ĉ(1)` and `ρ̂(y) ⊆ Ĉ(3)`. "A variable always evaluates to its value", so each
     occurrence of `[x]^ℓ` gives `ρ̂(x) ⊆ Ĉ(ℓ)`.
  3. Applications: for each application point `[e₁ e₂]^ℓ` and each possible function
     `[fn x => e]^ℓ′` that could be called there: (i) a constraint binding the formal parameter to the
     actual parameter, and (ii) a constraint making the result of the body a possible result of the
     application. The one application `[[···]^2 [···]^4]^5` has two candidates, `Ĉ(2)` being a subset of
     `{fn x => [x]^1, fn y => [y]^3}`, giving the *conditional constraints*:

```
{fn x => [x]^1} ⊆ Ĉ(2) ⇒ Ĉ(4) ⊆ ρ̂(x)
{fn x => [x]^1} ⊆ Ĉ(2) ⇒ Ĉ(1) ⊆ Ĉ(5)
{fn y => [y]^3} ⊆ Ĉ(2) ⇒ Ĉ(4) ⊆ ρ̂(y)
{fn y => [y]^3} ⊆ Ĉ(2) ⇒ Ĉ(3) ⊆ Ĉ(5)
```

- Citation: [PPA §1.4, p. 11] (book p. 11; PDF p. 31); the pattern for abstractions, classes 2 and 3 and the conditional constraints are on [PPA §1.4, p. 12] (book p. 12; PDF p. 32)

### [U1:1.4-d] The least solution (unnumbered result)
- Statement: as in §1.3 the least solution is wanted: "the smaller the sets of values given by Ĉ and
  ρ̂, the more precise the analysis is in predicting which functions are applied". Exercise 1.2 shows
  that the following is a solution (and the least):

```
Ĉ(1) = {fn y => [y]^3}     Ĉ(2) = {fn x => [x]^1}     Ĉ(3) = ∅
Ĉ(4) = {fn y => [y]^3}     Ĉ(5) = {fn y => [y]^3}
ρ̂(x) = {fn y => [y]^3}     ρ̂(y) = ∅
```

- Reading: `fn y => y` is never applied (`ρ̂(y) = ∅`), and the program may only evaluate to
  `fn y => y` (`Ĉ(5) = {fn y => [y]^3}`). Similarity with §1.3.2: "the syntactic structure of the
  program gives rise to a set of constraints whose least solution is desired"; difference: the
  constraints of Control Flow Analysis "have a more complex structure".
- Citation: [PPA §1.4, p. 12] (book p. 12; PDF p. 32); the reading and comparison are on [PPA §1.4, p. 13] (book p. 13; PDF p. 33)

### Projections (1.4)
- cs_theory: conditional set constraints whose least solution answers which abstractions reach each
  application; the Preface omits a deeper treatment of set constraints; Horn-clause or Datalog
  encodings [external] fit the same shape.
- swe_architecture: for higher-order code the call graph is itself an analysis result and data flow
  and control flow are mutually dependent; one program point per labelled expression suffices when
  there are no side effects, while statement-level languages need entry/exit pairs.
- practical_debugging: conditional constraints fire only when their guard holds; if abstraction
  constraints are not generated, `Ĉ` at the operator stays empty and no application constraint fires,
  a silent under-approximation [derived]; imprecision at an operator label multiplies downstream.
- cyber: indirect-call and callback resolution [external: function-pointer and virtual-dispatch
  analysis] uses the same guard-then-flow structure; an empty `Ĉ` at an attacker-reachable call site
  hides reachable targets.

## 1.5 Abstract Interpretation

Context: a collecting semantics over traces, a Galois connection to sets of reaching definitions, and
an induced analysis that is correct by construction [PPA §1.5, p. 13] (book p. 13; PDF p. 33).

### [U1:1.5-a] Abstract Interpretation: stance (unnumbered remark)
- Statement: "a general methodology for calculating analyses rather than just specifying them and then
  relying on a posteriori validation". Its application is to some extent independent of the
  specification style; the chapter uses the Data Flow formulation.
- Citation: [PPA §1.5, p. 13] (book p. 13; PDF p. 33)

### [U1:1.5-b] Traces; semantically reaching definitions SRD; DOM (unnumbered definition)
- Statement: the collecting semantics records the set of traces `tr` that can reach a program point,
  `tr ∈ Trace = (Var × Lab)*`; a trace records where variables obtained their values. Factorial trace
  with the loop body executed twice:
  `((x,?),(y,?),(z,?),(y,1),(z,2),(z,4),(y,5),(z,4),(y,5),(y,6))`.
  *Semantically reaching definitions*: `SRD(tr)(x) = ℓ` iff the rightmost pair `(x,ℓ′)` in `tr` has
  `ℓ = ℓ′`. `DOM(tr)` is the set of variables for which `SRD(tr)` is defined: `x ∈ DOM(tr)` iff some
  pair `(x,ℓ)` occurs in `tr`.
- Citation: [PPA §1.5, p. 13] (book p. 13; PDF p. 33)

### [U1:1.5-c] Correctness requirement for Reaching Definitions (unnumbered definition)
- Statement: if `tr` is a possible trace just before entering the block labelled `ℓ`, then
  `∀x ∈ DOM(tr) : (x, SRD(tr)(x)) ∈ RD_entry(ℓ)`.
- Side conditions: "In later chapters, we will conduct proofs of results like this."
- Citation: [PPA §1.5, p. 14] (book p. 14; PDF p. 34)

### [U1:1.5-d] Collecting semantics CS; the function G (unnumbered display)
- Statement: CS specifies a *superset* of the possible traces, as a twelve-tuple in `(𝒫(Trace))¹²`:

```
CS_exit(1) = {tr : (y,1) | tr ∈ CS_entry(1)}      CS_entry(2) = CS_exit(1)
CS_exit(2) = {tr : (z,2) | tr ∈ CS_entry(2)}      CS_entry(3) = CS_exit(2) ∪ CS_exit(5)
CS_exit(3) = CS_entry(3)                          CS_entry(4) = CS_exit(3)
CS_exit(4) = {tr : (z,4) | tr ∈ CS_entry(4)}      CS_entry(5) = CS_exit(4)
CS_exit(5) = {tr : (y,5) | tr ∈ CS_entry(5)}      CS_entry(6) = CS_exit(3)
CS_exit(6) = {tr : (y,6) | tr ∈ CS_entry(6)}      CS_entry(1) = {((x,?),(y,?),(z,?))}
```

  where `tr : (x,ℓ)` appends an element:
  `((x₁,ℓ₁), ···, (x_n,ℓ_n)) : (x,ℓ) = ((x₁,ℓ₁), ···, (x_n,ℓ_n), (x,ℓ))`.
- Side conditions: with more detailed information about values, `CS_entry(4)` and `CS_entry(6)` could
  be defined more precisely (the test outcome is ignored); the given definitions suffice for
  illustration. The system reads `CS⃗ = G(CS⃗)` with `G : (𝒫(Trace))¹² → (𝒫(Trace))¹²` monotone;
  Appendix A ensures a least solution `lfp(G)`. "Since `(𝒫(Trace))¹²` is not finite we cannot simply
  use the methods of the previous sections in order to construct `lfp(G)`."
- Citation: [PPA §1.5, p. 14] (book p. 14; PDF p. 34); the functionality of G and the finiteness remark are on [PPA §1.5, p. 15] (book p. 15; PDF p. 35)

### Figure 1.3 — The adjunction (α, γ)
- Content: two ovals. Left (the trace side): a point `X` with a point `γ(Y)` above it and a vertical
  `⊆` between them (`X ⊆ γ(Y)`). Right (the reaching-definitions side): a point `Y` with a point `α(X)`
  below it and a vertical `⊆` (`α(X) ⊆ Y`). A solid curved arrow labelled `α` runs from `X` to `α(X)`;
  a dotted curved arrow labelled `γ` runs from `Y` to `γ(Y)`.
- Citation: [PPA Figure 1.3, p. 15] (book p. 15; PDF p. 35)

### [U1:1.5-e] Galois connection: abstraction and concretisation (unnumbered definition)
- Statement: `𝒫(Trace)` and `𝒫(Var × Lab)` are related by the abstraction function `α` (rightwards)
  and the concretisation function `γ` (leftwards):

```
α(X) = {(x, SRD(tr)(x)) | x ∈ DOM(tr) ∧ tr ∈ X}
γ(Y) = {tr | ∀x ∈ DOM(tr) : (x, SRD(tr)(x)) ∈ Y}
α(X) ⊆ Y  ⇔  X ⊆ γ(Y)
```

  `α` "extracts the reachability information present in a set of traces"; `γ` "produces all traces tr
  that are consistent with the given reachability information". "Often it is demanded" that `α` and
  `γ` satisfy the displayed condition; `(α, γ)` is then "an *adjunction*, or a *Galois connection*".
- Side conditions: the verification that this `(α, γ)` fulfils the condition is left to the reader.
  `α` and `γ` are defined over the unstarred `Var × Lab`; the starred sets return only in the
  finiteness remark of [U1:1.5-g].
- Citation: [PPA §1.5, p. 15] (book p. 15; PDF p. 35); the naming and the reader exercise are on [PPA §1.5, p. 16] (book p. 16; PDF p. 36)

### [U1:1.5-f] Induced analysis: calculation for block 4 (unnumbered derivation)
- Statement: the collecting semantics is used "to *calculate* (as opposed to 'guess')" an analysis,
  called an *induced analysis*. With `α⃗(X₁, ···, X₁₂) = (α(X₁), ···, α(X₁₂))`,
  `γ⃗(Y₁, ···, Y₁₂) = (γ(Y₁), ···, γ(Y₁₂))` and
  `α⃗ ∘ G ∘ γ⃗ : (𝒫(Var × Lab))¹² → (𝒫(Var × Lab))¹²`, the clause
  `G_exit(4)(···, CS_entry(4), ···) = {tr : (z,4) | tr ∈ CS_entry(4)}` yields:

```
α(G_exit(4)(γ⃗(···, RD_entry(4), ···)))
 = α({tr : (z,4) | tr ∈ γ(RD_entry(4))})
 = {(x, SRD(tr:(z,4))(x)) | x ∈ DOM(tr:(z,4)), ∀y ∈ DOM(tr) : (y, SRD(tr)(y)) ∈ RD_entry(4)}
 = {(x, SRD(tr:(z,4))(x)) | x ≠ z, x ∈ DOM(tr:(z,4)), ∀y ∈ DOM(tr) : (y, SRD(tr)(y)) ∈ RD_entry(4)}
   ∪ {(x, SRD(tr:(z,4))(x)) | x = z, x ∈ DOM(tr:(z,4)), ∀y ∈ DOM(tr) : (y, SRD(tr)(y)) ∈ RD_entry(4)}
 = {(x, SRD(tr)(x)) | x ≠ z, x ∈ DOM(tr), ∀y ∈ DOM(tr) : (y, SRD(tr)(y)) ∈ RD_entry(4)}
   ∪ {(z,4) | ∀y ∈ DOM(tr) : (y, SRD(tr)(y)) ∈ RD_entry(4)}
 = (RD_entry(4) \ {(z,ℓ) | ℓ ∈ Lab}) ∪ {(z,4)}
```

  Result: `RD_exit(4) = (RD_entry(4) \ {(z,ℓ) | ℓ ∈ Lab}) ∪ {(z,4)}`, as in §1.3; the other equations
  are calculated the same way.
- Side conditions: [derived] the last step relies on the empty trace and the one-pair traces lying in
  `γ(RD_entry(4))` (vacuous or direct satisfaction of the `∀y` condition); the book leaves this
  implicit.
- Citation: [PPA §1.5, p. 16] (book p. 16; PDF p. 36); the result sentence is on [PPA §1.5, p. 17] (book p. 17; PDF p. 37)

### [U1:1.5-g] Least solution and correctness of the induced analysis (unnumbered result)
- Statement: `RD⃗ = (α⃗ ∘ G ∘ γ⃗)(RD⃗)` has a least solution `lfp(α⃗ ∘ G ∘ γ⃗)` (Appendix A); with finite
  `Var⋆` and `Lab⋆` it is obtained as `(α⃗ ∘ G ∘ γ⃗)ⁿ(∅⃗)` as for `F`. Exercise 1.4 shows
  `α⃗ ∘ G ∘ γ⃗ ⊑ F` and `α⃗(Gⁿ(∅⃗)) ⊑ (α⃗ ∘ G ∘ γ⃗)ⁿ(∅⃗) ⊑ Fⁿ(∅⃗)` for all `n`. "In fact"

```
α⃗(lfp(G)) ⊑ lfp(α⃗ ∘ G ∘ γ⃗) ⊑ lfp(F)
```

  so both the induced analysis and the §1.3 analysis are correct with respect to the collecting
  semantics: "we will only need to show that the collecting semantics is correct – the correctness of
  the induced analysis will follow for free".
- Side conditions: "For some analyses one is able to prove the stronger result `α⃗ ∘ G ∘ γ⃗ = F`"; the
  analysis is then *optimal* "(given the choice of approximate properties it operates on)" and
  `lfp(α⃗ ∘ G ∘ γ⃗) = lfp(F)`. Whether this holds here is Exercise 1.4.
- Citation: [PPA §1.5, p. 17] (book p. 17; PDF p. 37)

### Projections (1.5)
- cs_theory: a Galois connection between `𝒫(Trace)` and `𝒫(Var × Lab)` induces `α⃗ ∘ G ∘ γ⃗`; the chain
  `α⃗(lfp G) ⊑ lfp(α⃗ ∘ G ∘ γ⃗) ⊑ lfp F` is fixed-point transfer; optimality (`=`) is separate from
  soundness (`⊑`).
- swe_architecture: derive, do not hand-write: state the most precise observable (traces) and the
  projection `α`, then calculate transfer functions; one correctness proof about the collecting
  semantics covers every induced analysis.
- practical_debugging: an infinite domain such as `(𝒫(Trace))¹²` cannot be iterated to a fixed point;
  abstract to a finite domain first. A hand-written transfer function can be checked clause by clause
  against `α ∘ G_j ∘ γ⃗`; the empty trace in `γ(Y)` explains why `(z,4)` is produced even when
  `RD_entry(4) = ∅`.
- cyber: a custom taint or interval domain [external] is sound only if its transfer functions lie above
  `α ∘ G ∘ γ`; a collecting semantics that ignores test outcomes, as CS does, already loses
  path-sensitivity [external] that sanitiser checks depend on.

## 1.6 Type and Effect Systems

Context: Annotated Type Systems for Reaching Definitions on WHILE (§1.6.1, p. 18) and an Effect System
for call-tracking in a functional language (§1.6.2, p. 22) [PPA §1.6, p. 17] (book p. 17; PDF p. 37).

### [U1:1.6-a] The trivial type system for WHILE (unnumbered rule system)
- Statement: a statement "maps a state to a state (in case it terminates)" and has type `Σ → Σ`, `Σ`
  the type of states; judgement `S : Σ → Σ`. The "utterly trivial system of axioms and inference rules"
  (unnamed in the book):

```
[x := a]^ℓ : Σ → Σ            [skip]^ℓ : Σ → Σ

S₁ : Σ → Σ    S₂ : Σ → Σ      S₁ : Σ → Σ    S₂ : Σ → Σ                 S : Σ → Σ
------------------------      ---------------------------------       -----------------------
    S₁; S₂ : Σ → Σ            if [b]^ℓ then S₁ else S₂ : Σ → Σ        while [b]^ℓ do S : Σ → Σ
```

- Citation: [PPA §1.6, p. 17] (book p. 17; PDF p. 37); the rules are on [PPA §1.6, p. 18] (book p. 18; PDF p. 38)

### [U1:1.6-b] Effect System versus Annotated Type System (unnumbered definition)
- Statement: "Often a Type and Effect System can be viewed as the amalgamation of two ingredients: an
  *Effect System* and an *Annotated Type System*." Effect System: judgements `S : Σ --φ--> Σ`, where
  the *effect* `φ` "tells something about what happens when S is executed" (which errors might occur,
  which exceptions might be raised, which files might be modified). Annotated Type System: judgements
  `S : Σ₁ → Σ₂`, where the `Σᵢ` describe certain *properties of states* (a variable is positive, an
  invariant is maintained). §1.6.1 illustrates the latter on WHILE; §1.6.2 illustrates Effect Systems on
  the functional language.
- Citation: [PPA §1.6, p. 18] (book p. 18; PDF p. 38)

### [U1:1.6.1-a] Annotated base types: judgement; init and final (unnumbered definition)
- Statement: judgements `S : RD₁ → RD₂` with `RD₁, RD₂ ∈ 𝒫(Var × Lab)`, obtained from the trivial
  system and listed in Table 1.2. Any statement `S` has one elementary block at its entry, `init(S)`,
  and one or more at its exit, `final(S)`; for `if [x<y]^1 then [x:=y]^2 else [y:=x]^3`,
  `init(···) = 1` and `final(···) = {2, 3}`.
- Citation: [PPA §1.6.1, p. 18] (book p. 18; PDF p. 38)

### Table 1.2 — Reaching Definitions: annotated base types
- Content:

```
[ass]   [x := a]^ℓ′ : RD → ((RD \ {(x,ℓ) | ℓ ∈ Lab}) ∪ {(x,ℓ′)})
[skip]  [skip]^ℓ′ : RD → RD
        S₁ : RD₁ → RD₂    S₂ : RD₂ → RD₃
[seq]   --------------------------------
           S₁; S₂ : RD₁ → RD₃
        S₁ : RD₁ → RD₂    S₂ : RD₁ → RD₂
[if]    -------------------------------------
        if [b]^ℓ then S₁ else S₂ : RD₁ → RD₂
             S : RD → RD
[wh]    ---------------------------
        while [b]^ℓ do S : RD → RD
        S : RD₂ → RD₃
[sub]   -------------      if RD₁ ⊆ RD₂ and RD₃ ⊆ RD₄
        S : RD₁ → RD₄
```

- Citation: [PPA Table 1.2, p. 19] (book p. 19; PDF p. 39)

### [U1:1.6.1-b] Two readings of S : RD₁ → RD₂ (unnumbered failed attempt and repair)
- Statement: the first "(and not quite successful)" attempt reads `RD₁ = RD_entry(init(S))` and
  `⋃{RD_exit(ℓ) | ℓ ∈ final(S)} = RD₂`. It explains `[ass]` and `[skip]` (the formula after the arrow is
  the §1.3 equation) and `[seq]`, but `[if]` is "more dubious": for
  `if [x<y]^1 then [x:=y]^2 else [y:=x]^3` "it seems impossible to achieve that the then-branch gives
  rise to the same set of reaching definitions as the else-branch". The second "(and successful)"
  attempt reads `RD₁ ⊆ RD_entry(init(S))` and `∀ℓ ∈ final(S) : RD_exit(ℓ) ⊆ RD₂`. It is "closer to" the
  constraint based formulation of §1.3, makes the *subsumption rule* `[sub]` unproblematic, and lets
  `[sub]` repair `[if]` by enlarging both branch results to a common set. `[wh]` expresses "that RD is
  a consistent guess concerning what may reach the entry and exits of S – this expresses a fixed point
  property".
- Side conditions: Exercise 1.5 asks whether Table 1.2 can be changed so that the first reading works.
- Citation: [PPA §1.6.1, p. 18] (book p. 18; PDF p. 38); the failure on `[if]`, the second reading and `[wh]` are on [PPA §1.6.1, p. 19] (book p. 19; PDF p. 39)

### Example 1.3 — The factorial program via Table 1.2
- Statement: with `RD_f = {(x,?),(y,1),(y,5),(z,2),(z,4)}`:

```
[ass]:  [z:=z*y]^4 : RD_f → {(x,?),(y,1),(y,5),(z,4)}
        [y:=y-1]^5 : {(x,?),(y,1),(y,5),(z,4)} → {(x,?),(y,5),(z,4)}
[seq]:  ([z:=z*y]^4; [y:=y-1]^5) : RD_f → {(x,?),(y,5),(z,4)}
[sub]:  since {(x,?),(y,5),(z,4)} ⊆ RD_f:  ([z:=z*y]^4; [y:=y-1]^5) : RD_f → RD_f
[wh]:   while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5) : RD_f → RD_f
[ass]:  [y:=x]^1 : {(x,?),(y,?),(z,?)} → {(x,?),(y,1),(z,?)}
        [z:=1]^2 : {(x,?),(y,1),(z,?)} → {(x,?),(y,1),(z,2)}
        [y:=0]^6 : RD_f → {(x,?),(y,6),(z,2),(z,4)}
[seq], [sub]: since {(x,?),(y,1),(z,2)} ⊆ RD_f:
  ([y:=x]^1; [z:=1]^2; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6) :
      {(x,?),(y,?),(z,?)} → {(x,?),(y,6),(z,2),(z,4)}
```

  "corresponding to the result in Table 1.1". ■
- Side conditions: Table 1.2 "suffices for manually analysing a given program"; an implementation
  would extract a set of constraints and solve them as before, "the idea behind the approach taken in
  Chapter 5". [derived] `RD_f` equals `RD_entry(3)` of Table 1.1; the loop invariant is guessed, not
  computed by the rules.
- Citation: [PPA Example 1.3, p. 20] (book p. 20; PDF p. 40); the implementation remark is in [PPA §1.6.1, p. 20] (book p. 20; PDF p. 40)

### [U1:1.6.1-c] Annotated type constructors: judgement (unnumbered definition)
- Statement: this formulation has "a little bit of the flavour of Effect Systems": the arrow is
  annotated. Judgements `S : Σ --X-->_{RD} Σ`, where "X denotes the set of variables that *definitely*
  will be assigned in S and RD denotes the set of reaching definitions that S *might* produce".
  `RD \ X` means `{(x,ℓ) ∈ RD | x ∉ X}`.
- Citation: [PPA §1.6.1, p. 20] (book p. 20; PDF p. 40); the `X`/`RD` prose and notation `RD \ X` are on [PPA §1.6.1, p. 21] (book p. 21; PDF p. 41)

### Table 1.3 — Reaching Definitions: annotated type constructors
- Content:

```
[ass]   [x := a]^ℓ : Σ --{x}-->_{{(x,ℓ)}} Σ
[skip]  [skip]^ℓ : Σ --∅-->_{∅} Σ
        S₁ : Σ --X₁-->_{RD₁} Σ     S₂ : Σ --X₂-->_{RD₂} Σ
[seq]   -----------------------------------------------
        S₁; S₂ : Σ --X₁∪X₂-->_{(RD₁\X₂)∪RD₂} Σ
        S₁ : Σ --X₁-->_{RD₁} Σ     S₂ : Σ --X₂-->_{RD₂} Σ
[if]    -------------------------------------------------------
        if [b]^ℓ then S₁ else S₂ : Σ --X₁∩X₂-->_{RD₁∪RD₂} Σ
             S : Σ --X-->_{RD} Σ
[wh]    ------------------------------------
        while [b]^ℓ do S : Σ --∅-->_{RD} Σ
        S : Σ --X-->_{RD} Σ
[sub]   ----------------------     if X′ ⊆ X and RD ⊆ RD′
        S : Σ --X′-->_{RD′} Σ
```

- Explanation stated: `[ass]`: `x` is definitely assigned and `(x,ℓ)` is produced. `[seq]`: union of
  reaching definitions after removing entries of `S₁` that `S₂` definitely redefines; union of assigned
  variables. `[if]`: union of reaching definitions but *intersection* of assigned variables "because we
  are not completely sure what path was taken". `[wh]`: `∅` as the intersection of `∅` (body not
  executed) and `X`. `[sub]` is included "because this is normally the case for such systems"; here
  "there is little need for it, and if one excludes it then implementation becomes very
  straightforward: simply perform a syntax directed traversal" computing `X` and `RD` per subprogram.
- Citation: [PPA Table 1.3, p. 21] (book p. 21; PDF p. 41); the explanation is in [PPA §1.6.1, p. 21] (book p. 21; PDF p. 41)

### Example 1.4 — The factorial program via Table 1.3
- Statement:

```
[z:=z*y]^4 : Σ --{z}-->_{{(z,4)}} Σ           [y:=y-1]^5 : Σ --{y}-->_{{(y,5)}} Σ
[seq]: ([z:=z*y]^4; [y:=y-1]^5) : Σ --{y,z}-->_{{(y,5),(z,4)}} Σ
[wh]:  while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5) : Σ --∅-->_{{(y,5),(z,4)}} Σ
       ([y:=x]^1; [z:=1]^2) : Σ --{y,z}-->_{{(y,1),(z,2)}} Σ      [y:=0]^6 : Σ --{y}-->_{{(y,6)}} Σ
[seq]: ([y:=x]^1; [z:=1]^2; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6) :
       Σ --{y,z}-->_{{(y,6),(z,2),(z,4)}} Σ
```

  The program definitely assigns `y` and `z`; the final value of `y` is assigned at 6 and the final
  value of `z` at 2 or 4. ■
- Side conditions: unlike Table 1.1 the result has no `(x,?)`: the judgement records what the
  statement produces, not entry information. The specification "expresses how information present at
  the entry will be *modified* by the statement"; it is "a higher-order formulation of Reaching
  Definitions analysis" [PPA §1.6.1, p. 22] (book p. 22; PDF p. 42).
- Citation: [PPA Example 1.4, p. 21] (book p. 21; PDF p. 41); the example ends on [PPA Example 1.4, p. 22] (book p. 22; PDF p. 42)

### [U1:1.6.2-a] Simple type system for the functional language (unnumbered rule system)
- Statement: expressions are variables `x`, function abstractions `fn_π x => e` (`π` is the name of the
  abstraction) and applications `e₁ e₂`. Judgement `Γ ⊢ e : τ`, `Γ` a *type environment* for the free
  variables of `e`, `τ` the *type*; types are base types such as `int` and `bool`, or function types
  `τ₁ → τ₂`.

```
Γ ⊢ x : τ_x   if Γ(x) = τ_x

  Γ[x ↦ τ_x] ⊢ e : τ                 Γ ⊢ e₁ : τ₂ → τ    Γ ⊢ e₂ : τ₂
-----------------------------        ---------------------------------
Γ ⊢ fn_π x => e : τ_x → τ                     Γ ⊢ e₁ e₂ : τ
```

- Side conditions: the abstraction rule requires a "guess" of `τ_x`; in the application rule `e₁` must
  have a function type, and the two occurrences of `τ₂` force the type of the actual parameter to equal
  the type of the formal parameter.
- Citation: [PPA §1.6.2, p. 22] (book p. 22; PDF p. 42); the rules are on [PPA §1.6.2, p. 23] (book p. 23; PDF p. 43)

### Example 1.5 — Typing (fn_X x => x) (fn_Y y => y)
- Statement: the program of Example 1.2 with names `X` and `Y`. `[y ↦ int] ⊢ y : int`, so
  `[ ] ⊢ fn_Y y => y : int → int`; `[x ↦ int → int] ⊢ x : int → int`, so
  `[ ] ⊢ fn_X x => x : (int → int) → (int → int)`; the application rule gives
  `[ ] ⊢ (fn_X x => x) (fn_Y y => y) : int → int`. ■
- Citation: [PPA Example 1.5, p. 23] (book p. 23; PDF p. 43)

### [U1:1.6.2-b] Call-Tracking Analysis: specification (unnumbered definition)
- Statement: "For each subexpression, which function abstractions may be applied during its
  evaluation." "The set of function names constitutes the *effect* of the subexpression."
- Citation: [PPA §1.6.2, p. 23] (book p. 23; PDF p. 43)

### Table 1.4 — Call-tracking Analysis: Effect System
- Content:

```
[var]   Γ̂ ⊢ x : τ̂_x & ∅     if Γ̂(x) = τ̂_x
              Γ̂[x ↦ τ̂_x] ⊢ e : τ̂ & φ
[fn]    -----------------------------------------
        Γ̂ ⊢ fn_π x => e : τ̂_x --φ∪{π}--> τ̂ & ∅
        Γ̂ ⊢ e₁ : τ̂₂ --φ--> τ̂ & φ₁     Γ̂ ⊢ e₂ : τ̂₂ & φ₂
[app]   ------------------------------------------------
              Γ̂ ⊢ e₁ e₂ : τ̂ & φ₁ ∪ φ₂ ∪ φ
```

- Citation: [PPA Table 1.4, p. 24] (book p. 24; PDF p. 44)

### [U1:1.6.2-c] Annotated types, latent effects, and the rules explained (unnumbered definition)
- Statement: function types are annotated with their *latent effect*: `int --{X}--> int` is a function
  on integers that, when executed, may apply the function named `X`. Annotated types:
  `τ̂ ::= base type | τ̂₁ --φ--> τ̂₂`, `φ` being "the names of the function abstractions that we might
  apply when applying a function of this type". Judgement `Γ̂ ⊢ e : τ̂ & φ`: `Γ̂` gives the annotated
  types of the free variables, `τ̂` is the annotated type of `e`, `φ` the effect of evaluating `e`.
- Rules explained: `[var]` has empty effect "because we assume that the parameter mechanism is
  call-by-value"; `[fn]` has empty effect because "we only construct a closure", and the body's effect
  together with the abstraction's own name `π` annotates the arrow; `[app]` takes the union of the
  operator's effect `φ₁` (the operator is evaluated first), the operand's effect `φ₂` (call-by-value
  evaluates the operand too) and the latent effect `φ` of the function being applied, which the book
  calls "the annotation of the arrow in the type τ̂₂ --φ--> τ̂ of the operand" (finding F-U1-03).
- Citation: [PPA §1.6.2, p. 24] (book p. 24; PDF p. 44); the end of the `[app]` explanation is on [PPA §1.6.2, p. 25] (book p. 25; PDF p. 45)

### Findings (1.6.2)
- F-U1-03 (BKL-026): on p. 25 the `[app]` explanation says the latent effect is "the annotation of the arrow in
  the type τ̂₂ --φ--> τ̂ of the operand"; by Table 1.4 that type belongs to `e₁`, which the same
  paragraph calls the operator. Recorded, not corrected. [PPA §1.6.2, p. 25] (book p. 25; PDF p. 45)

### Example 1.6 — Call-tracking for (fn_X x => x) (fn_Y y => y)
- Statement:

```
[ ] ⊢ fn_Y y => y : int --{Y}--> int & ∅
[ ] ⊢ fn_X x => x : (int --{Y}--> int) --{X}--> (int --{Y}--> int) & ∅
[ ] ⊢ (fn_X x => x) (fn_Y y => y) : int --{Y}--> int & {X}
```

  "This shows that our example program may (in fact it will) apply the function fn x => x but that it
  will not apply the function fn y => y." ■
- Citation: [PPA Example 1.6, p. 25] (book p. 25; PDF p. 45)

### [U1:1.6.2-d] Subsumption and implementation of Effect Systems (unnumbered remark)
- Statement: a more general language needs "some form of subsumption rule in the manner of Tables 1.2
  and 1.3"; "there are different approaches to this". Effect Systems "are often implemented as
  extensions of type inference algorithms"; depending on the form of the effects they may be
  calculated on the fly, or sets of constraints can be generated and solved subsequently (Chapter 5).
- Citation: [PPA §1.6.2, p. 25] (book p. 25; PDF p. 45)

### Projections (1.6)
- cs_theory: three type-based formulations of analyses: annotated base types (pre/post sets with
  subsumption as weakening), annotated type constructors (compositional summaries mixing a must
  component `X` and a may component `RD`), and effect systems with latent effects under call-by-value;
  the Concluding Remarks relate some Annotated Type Systems to Hoare's logic, with `[sub]` in the role of
  the consequence rule [external].
- swe_architecture: Table 1.2 propagates context and needs guessed loop invariants (or constraint
  extraction); Table 1.3 without `[sub]` is a syntax-directed bottom-up summary computation needing no
  entry state; latent effects are interface contracts carried in types and composed by union at call
  sites.
- practical_debugging: if a derivation cannot type a conditional, the equality reading is being used:
  apply `[sub]` to a common set; a Table 1.3 summary lacks `(x,?)` and must be applied to an entry set
  before comparing with Table 1.1; Example 1.6's empty `Y` in the outer effect is correct because the
  returned closure carries `{Y}` latently.
- cyber: the `X` component is a definite-assignment check [external]: intersection at branches and `∅`
  for loops expose a variable left uninitialised on one path or after a zero-trip loop; a call-tracking
  effect is a capability summary [external] of which functions may run, enforceable as a policy on
  untrusted callbacks.

## 1.7 Algorithms

Context: computing the least solution efficiently; Chaotic Iteration [PPA §1.7, p. 25] (book p. 25; PDF p. 45).

### [U1:1.7-a] The problem restated (unnumbered remark)
- Statement: find the least `RD⃗ ∈ (𝒫(Var⋆ × Lab⋆))¹²` with `RD⃗ = F(RD⃗)` or `RD⃗ ⊒ F(RD⃗)`, `F` monotone.
  By finiteness the solution is in both cases `Fⁿ(∅⃗)` for any `n` with `Fⁿ⁺¹(∅⃗) = Fⁿ(∅⃗)`, and such
  an `n` exists. "Naively implementing the above procedure soon turns out to require an overwhelming
  amount of work." *Chaotic Iteration* "lies at the heart of many" of the more efficient algorithms.
- Side conditions: write `RD⃗ = (RD₁, ···, RD₁₂)` and `F(RD⃗) = (F₁(RD⃗), ···, F₁₂(RD⃗))`.
- Citation: [PPA §1.7, p. 25] (book p. 25; PDF p. 45)

### Table 1.5 — Chaotic Iteration for Reaching Definitions
- Content:

```
INPUT:   Example equations for Reaching Definitions
OUTPUT:  The least solution: RD⃗ = (RD₁, ···, RD₁₂)
METHOD:  Step 1: Initialisation
                 RD₁ := ∅; ···; RD₁₂ := ∅
         Step 2: Iteration
                 while RD_j ≠ F_j(RD₁, ···, RD₁₂) for some j
                 do RD_j := F_j(RD₁, ···, RD₁₂)
```

- Citation: [PPA Table 1.5, p. 26] (book p. 26; PDF p. 46)

### [U1:1.7-b] Partial correctness, leastness, termination (unnumbered result)
- Statement: the algorithm is non-deterministic in the choice of `j`. Some `j` has
  `RD_j ≠ F_j(RD₁, ···, RD₁₂)` iff `RD⃗ ≠ F(RD⃗)`, so if it terminates the result is a fixed point.
  The invariant `∅⃗ ⊑ RD⃗ ⊑ F(RD⃗) ⊑ Fⁿ(∅⃗)` (with `Fⁿ⁺¹(∅⃗) = Fⁿ(∅⃗)`) holds initially and is preserved
  (Exercise 1.6), so on termination the result is the least fixed point `Fⁿ(∅⃗)`. Termination: if
  `RD_j ≠ F_j(RD⃗)` then in fact `RD_j ⊂ F_j(RD⃗)` by the invariant, so "the size of RD⃗ increases by at
  least one as we perform each iteration", and `(𝒫(Var⋆ × Lab⋆))¹²` is finite.
- Side conditions: the algorithm is "suitable for *manually* solving data flow equations and
  constraint systems"; an implementation needs "more details about the choice of j so as to avoid an
  extensive search" (Chapters 2 and 6).
- Citation: [PPA §1.7, p. 26] (book p. 26; PDF p. 46)

### Projections (1.7)
- cs_theory: any fair order of local monotone updates from `∅⃗` reaches the same least fixed point;
  the invariant `RD⃗ ⊑ F(RD⃗)` plus finiteness gives termination by strict growth.
- swe_architecture: worklist [external] schedulers, priority orders and incremental updates are pure
  performance choices licensed by Chaotic Iteration; the solver needs only monotone component
  functions `F_j` and a cheap way to pick a changed `j`.
- practical_debugging: assert strict growth `RD_j ⊂ F_j(RD⃗)` on every update; the first violation
  names the broken assumption (non-monotone transfer function, start state not `∅⃗`, or an infinite
  domain). Output that depends on update order indicates a non-least start or a non-monotone `F`.
- cyber: an analyser that caps iterations or starts from stale state can stop below the least fixed
  point and miss flows [derived]; a cap needs a sound jump upward (widening [external to Chapter 1;
  Chapter 4]) rather than early termination.

## 1.8 Transformations

Context: Constant Folding driven by Reaching Definitions. Table 1.6 is printed at the top of p. 27,
before the §1.8 heading [PPA §1.8, p. 27] (book p. 27; PDF p. 47).

### [U1:1.8-a] Constant Folding: purpose and judgement (unnumbered definition)
- Statement: "A major application of program analysis is to transform the program (at the source
  level or at some intermediate level inside a compiler) so as to obtain better performance."
  Constant Folding has two ingredients: replace the use of a variable by a constant "if it is known
  that the value of the variable will always be that constant"; and simplify an expression by partially
  evaluating it: subexpressions that contain no variables can be evaluated. *Source to source
  transformation*: for a program `S⋆` and `RD` "a solution (preferable the least)" to Reaching
  Definitions for `S⋆` (finding F-U1-09), a sub-statement `S` of `S⋆` is transformed into a "better"
  `S′` by judgements `RD ⊢ S ▷ S′`, each "expressing *one step* of the transformation process".
- Citation: [PPA §1.8, p. 27] (book p. 27; PDF p. 47); "one step" is on [PPA §1.8, p. 28] (book p. 28; PDF p. 48)

### Table 1.6 — Constant Folding transformation
- Content:

```
[ass₁]  RD ⊢ [x := a]^ℓ ▷ [x := a[y ↦ n]]^ℓ
           if  y ∈ FV(a) ∧ (y,?) ∉ RD_entry(ℓ) ∧
               ∀(z,ℓ′) ∈ RD_entry(ℓ) : (z = y ⇒ [···]^ℓ′ is [y := n]^ℓ′)
[ass₂]  RD ⊢ [x := a]^ℓ ▷ [x := n]^ℓ
           if  FV(a) = ∅ ∧ a ∉ Num ∧ a evaluates to n
           RD ⊢ S₁ ▷ S₁′                                RD ⊢ S₂ ▷ S₂′
[seq₁]  ----------------------             [seq₂]  ----------------------
        RD ⊢ S₁; S₂ ▷ S₁′; S₂                       RD ⊢ S₁; S₂ ▷ S₁; S₂′
                       RD ⊢ S₁ ▷ S₁′
[if₁]   -------------------------------------------------------------
        RD ⊢ if [b]^ℓ then S₁ else S₂ ▷ if [b]^ℓ then S₁′ else S₂
                       RD ⊢ S₂ ▷ S₂′
[if₂]   -------------------------------------------------------------
        RD ⊢ if [b]^ℓ then S₁ else S₂ ▷ if [b]^ℓ then S₁ else S₂′
                  RD ⊢ S ▷ S′
[wh]    ---------------------------------------
        RD ⊢ while [b]^ℓ do S ▷ while [b]^ℓ do S′
```

- Notation stated: `a[y ↦ n]` is `a` with all occurrences of `y` replaced by `n`; `FV(a)` is the set of
  variables occurring in `a`. `[ass₁]` expresses the first ingredient; `[ass₂]` the second, using the
  fact that an expression without variables always evaluates to the same value [PPA §1.8, p. 28] (book p. 28; PDF p. 48).
- Side conditions: [derived] the `a ∉ Num` condition prevents rewriting a numeral to itself; no rule
  rewrites tests `[b]^ℓ` (Exercise 1.10 asks for boolean expressions).
- Citation: [PPA Table 1.6, p. 27] (book p. 27; PDF p. 47)

### [U1:1.8-b] No prescribed order; neither reflexive nor transitive (unnumbered remark)
- Statement: the last five rules say that if a sub-statement can be transformed then so can the
  statement. The rules (e.g. `[seq₁]` and `[seq₂]`) "do not prescribe a specific transformation order
  and hence many different transformation sequences may exist". "The relation RD ⊢ · ▷ · is neither
  reflexive nor transitive because there are no rules that forces it to be so" (finding F-U1-06).
  "Hence we shall often want to perform an entire sequence of transformations."
- Citation: [PPA §1.8, p. 28] (book p. 28; PDF p. 48)

### Example 1.7 — Constant Folding on [x:=10]^1; [y:=x+10]^2; [z:=y+10]^3
- Statement: the least Reaching Definitions solution:

```
RD_entry(1) = {(x,?),(y,?),(z,?)}
RD_exit(1)  = {(x,1),(y,?),(z,?)}
RD_entry(2) = {(x,1),(y,?),(z,?)}
RD_exit(2)  = {(x,1),(y,2),(z,?)}
RD_entry(3) = {(x,1),(y,2),(z,?)}
RD_exit(3)  = {(x,1),(y,2),(z,3)}
```

  `[ass₁]` gives `RD ⊢ [y:=x+10]^2 ▷ [y:=10+10]^2`, and "the rules for sequencing gives" the step on the
  whole program. The full sequence:

```
RD ⊢ [x:=10]^1; [y:=x+10]^2;  [z:=y+10]^3
   ▷ [x:=10]^1; [y:=10+10]^2; [z:=y+10]^3
   ▷ [x:=10]^1; [y:=20]^2;    [z:=y+10]^3
   ▷ [x:=10]^1; [y:=20]^2;    [z:=20+10]^3
   ▷ [x:=10]^1; [y:=20]^2;    [z:=30]^3
```

  "after which no more steps are possible." ■
- Side conditions: [derived] the third step uses `[ass₁]` with the side condition "`[···]^2` is
  `[y := 20]^2`", which holds of the current program and not of `S⋆`; it is legitimate because the
  same `RD` stays a solution after each step ([U1:1.8-c]).
- Citation: [PPA Example 1.7, p. 28] (book p. 28; PDF p. 48); the closing sentence is on [PPA Example 1.7, p. 29] (book p. 29; PDF p. 49)

### [U1:1.8-c] Successive transformations and re-use of the analysis (unnumbered result)
- Statement: `RD ⊢ S₁ ▷ S₂ ▷ ··· ▷ S_{n+1}` "could be costly because once S₁ has been transformed into
  S₂ we might have to *recompute* Reaching Definitions Analysis for S₂" before transforming it into
  `S₃`, and so on. "It is sometimes possible to use the analysis for S₁ to obtain a reasonable analysis
  for S₂ without performing the analysis from scratch." For Reaching Definitions and Constant Folding
  this is "very easy": if `RD` is a solution to Reaching Definitions for `S_i` and `RD ⊢ S_i ▷ S_{i+1}`,
  then `RD` is also a solution for `S_{i+1}`, because "the transformation only changed things that were
  not observed by the Reaching Definitions Analysis".
- Side conditions: [derived] Table 1.6 changes only right-hand-side expressions; labels, assigned
  variables and flow are unchanged. The general problem of recomputing invalidated information is a
  Preface exclusion ([U1:1.0-b]).
- Citation: [PPA §1.8, p. 29] (book p. 29; PDF p. 49)

### Findings (1.8)
- F-U1-06 (BKL-034): on p. 28 the text prints "there are no rules that forces it to be so" and "the rules for
  sequencing gives" (subject–verb agreement). Recorded, not corrected. [PPA §1.8, p. 28] (book p. 28; PDF p. 48)
- F-U1-09: on p. 27 the text prints "a solution (preferable the least)" for "preferably". Recorded,
  not corrected. [PPA §1.8, p. 27] (book p. 27; PDF p. 47)

### Projections (1.8)
- cs_theory: `▷` is a one-step rewriting relation with order freedom; how many sequences reach the same
  normal form (Exercise 1.9) is a confluence and termination question [external].
- swe_architecture: a transformation driver loops until no rule applies; a pass manager [external]
  must know, per transformation, which analyses stay valid (Reaching Definitions survives Constant
  Folding) and must recompute the rest; label- or flow-changing rewrites (Exercise 1.10) invalidate
  label-indexed results.
- practical_debugging: a wrong fold usually means `[ass₁]` was applied without checking that `(y,?)` is
  absent and that every reaching definition of `y` assigns the same numeral; a stale analysis after a
  rewrite means the rewrite changed something the analysis observes.
- cyber: substituting non-constant expressions (Exercise 1.11) ignores redefinitions of their free
  variables between definition and use [derived], the shape of optimiser-introduced security bugs
  [external]; branch pruning on `if [true]` removes code that a later check may rely on.

## Concluding Remarks (Chapter 1)

### [U1:CR-a] Similarities; Hoare logic; semantics based versus directed (unnumbered remark)
- Statement: the chapter illustrated "a few approaches (but by no means all)". Clearly there are many
  differences, but the main aim "has been to suggest that there are also more *similarities* than one
  would perhaps have expected at first sight: in particular, the interplay between the use of
  equations versus constraints". Some techniques have close connections to other approaches to
  reasoning about programs; "some versions of Annotated Type Systems are closely related to Hoare's
  logic for partial correctness assertions". As mentioned earlier, the approaches in the book are
  *semantics based* rather than *semantics directed*; the semantics directed approaches include "the
  denotational based approaches [27, 86, 115, 117] and logic based approaches [19, 20, 81, 82]".
- Side conditions: bibliography locations: `[27]` [PPA Bibliography, p. 441] (book p. 441; PDF p. 454),
  `[86]` [PPA Bibliography, p. 445] (book p. 445; PDF p. 458), `[115]` [PPA Bibliography, p. 447] (book p. 447; PDF p. 460),
  `[117]` [PPA Bibliography, p. 447] (book p. 447; PDF p. 460), `[19]` [PPA Bibliography, p. 440] (book p. 440; PDF p. 453),
  `[20]` [PPA Bibliography, p. 440] (book p. 440; PDF p. 453), `[81]` [PPA Bibliography, p. 445] (book p. 445; PDF p. 458),
  `[82]` [PPA Bibliography, p. 445] (book p. 445; PDF p. 458).
  Entry titles are not transcribed in this shard.
- Citation: [PPA Chapter 1 Concluding Remarks, p. 29] (book p. 29; PDF p. 49)

### Projections (Concluding Remarks)
- cs_theory: the unifying claim is the equations-versus-constraints interplay; Annotated Type Systems
  relate to Hoare logic; the excluded semantics directed family is denotational or logic based.
- swe_architecture: the same analysis can ship as an equation solver, a constraint solver, an induced
  abstract interpreter or a type checker; the comparison of four forms is a design space, not four
  products.
- practical_debugging: when two formulations of the same analysis disagree, compare least solutions,
  not arbitrary solutions; Annotated Type System derivations can be read as pre/post assertions to
  locate the failing rule.
- cyber: pre/post reading of annotated types [external: Hoare-style contracts] gives auditable
  per-statement security claims; a reviewer can check each `[sub]` step as an explicit weakening.

## Mini Projects (Chapter 1)

### Mini Project 1.1 — Correctness of Reaching Definitions
- Aim: "increase our faith in the Type and Effect System of Table 1.3 by proving that it is correct";
  this requires regular expressions and homomorphisms to the extent covered in Appendix C
  [PPA Chapter 1 Mini Projects, p. 29] (book p. 29; PDF p. 49).
- Statement-to-regular-expression map, by structural induction (Appendix B):

```
𝒮([x:=a]^ℓ)                  = !^ℓ_x
𝒮([skip]^ℓ)                  = Λ
𝒮(S₁; S₂)                    = 𝒮(S₁) · 𝒮(S₂)
𝒮(if [b]^ℓ then S₁ else S₂)  = 𝒮(S₁) + 𝒮(S₂)
𝒮(while b do S)              = (𝒮(S))*
```

  The loop clause is transcribed as printed, without the label of the test (finding F-U1-04). The
  alphabet is `{!^ℓ_x | x ∈ Var⋆, ℓ ∈ Lab⋆}`, where `Var⋆` and `Lab⋆` are finite and non-empty sets that
  contain all the variables and labels of the statement `S⋆` of interest. Example: for
  `S⋆ = if [x>0]^1 then [x:=x+1]^2 else ([x:=x+2]^3; [x:=x+3]^4)`, `𝒮(S⋆) = !^2_x + (!^3_x · !^4_x)`
  [PPA Chapter 1 Mini Projects, p. 30] (book p. 30; PDF p. 50).
- Correctness of X: for each `y ∈ Var⋆` the homomorphism
  `h_y : {!^ℓ_x | x ∈ Var⋆, ℓ ∈ Lab⋆} → {!}*` is `h_y(!^ℓ_x) = !` if `y = x` and `Λ` if `y ≠ x`.
  Example: `h_x(𝒮(S⋆)) = ! + (! · !)` and `h_y(𝒮(S⋆)) = Λ`, using `Λ · Λ = Λ` and `Λ + Λ = Λ`.
  `h_y(𝒮(S)) ⊆ ! · !*` means `ℒ⟦h_y(𝒮(S))⟧ ⊆ ℒ⟦! · !*⟧`; the book states this "is equivalent to"
  `¬∃w ∈ ℒ⟦h_y(𝒮(S))⟧ : h_y(w) = Λ` (as printed; finding F-U1-05) and "intuitively says that y is always
  assigned in S". Prove: if `S : Σ --X-->_{RD} Σ` and `y ∈ X` then `h_y(𝒮(S)) ⊆ ! · !*`, by induction on
  the shape of the inference tree establishing `S : Σ --X-->_{RD} Σ` (Appendix B)
  [PPA Chapter 1 Mini Projects, p. 30] (book p. 30; PDF p. 50).
- Correctness of RD: for each `y ∈ Var⋆` and `ℓ′ ∈ Lab⋆` the homomorphism
  `h^ℓ′_y : {!^ℓ_x | x ∈ Var⋆, ℓ ∈ Lab⋆} → {!, ?}*` is `h^ℓ′_y(!^ℓ_x) = !` if `y = x ∧ ℓ = ℓ′`, `?` if
  `y = x ∧ ℓ ≠ ℓ′`, and `Λ` if `y ≠ x`. Example: `h^2_x(𝒮(S⋆)) = ! + (? · ?)` and `h^5_y(𝒮(S⋆)) = Λ`.
  `h^ℓ′_y(𝒮(S)) ⊆ ((!+?)* · ?) + Λ` is equivalent to `¬∃w ∈ ℒ⟦𝒮(S)⟧ : h^ℓ′_y(w) ends in !` and
  "intuitively means than the last assignment to y could not have been performed at the statement
  labelled ℓ′" (finding F-U1-07). Prove: if `S : Σ --X-->_{RD} Σ` and `(y,ℓ′) ∉ RD` then
  `h^ℓ′_y(𝒮(S)) ⊆ ((!+?)* · ?) + Λ`, by induction on the shape of the inference tree. ■
  [PPA Chapter 1 Mini Projects, p. 31] (book p. 31; PDF p. 51)
- Side conditions: the `?` of the alphabet `{!, ?}` is a letter, distinct from the uninitialised label
  `?` of §1.2.
- Citation: [PPA Chapter 1 Mini Projects, p. 29] (book p. 29; PDF p. 49)

### Findings (Mini Projects)
- F-U1-04 (BKL-027): on p. 30 the loop clause is printed `𝒮(while b do S)`, without the labelled test `[b]^ℓ`
  used by the conditional clause and by the WHILE syntax. Recorded, not corrected.
  [PPA Chapter 1 Mini Projects, p. 30] (book p. 30; PDF p. 50)
- F-U1-05 (BKL-027): on p. 30 the equivalent form of the X-correctness condition quantifies
  `w ∈ ℒ⟦h_y(𝒮(S))⟧` and then applies `h_y` to `w` again (`h_y(w) = Λ`); `h_y` is defined on the
  alphabet `{!^ℓ_x | ...}`, not on `{!}`. The parallel RD condition on p. 31 quantifies over
  `ℒ⟦𝒮(S)⟧`. Recorded, not corrected. [PPA Chapter 1 Mini Projects, p. 30] (book p. 30; PDF p. 50)
- F-U1-07 (BKL-034): on p. 31 the text prints "intuitively means than the last assignment" for "that".
  Recorded, not corrected. [PPA Chapter 1 Mini Projects, p. 31] (book p. 31; PDF p. 51)

### Projections (Mini Projects)
- cs_theory: correctness of a type-based analysis reduced to regular-language inclusion under
  homomorphic projection (Appendix C), proved by rule induction on inference trees (Appendix B).
- swe_architecture: path expressions [external] of a statement, projected per variable, give an
  executable oracle for definite-assignment and reaching-definition summaries.
- practical_debugging: to test a Table 1.3 implementation, compute `𝒮(S)`, project with `h_y` or
  `h^ℓ′_y`, and check the language inclusion; a counterexample word is a concrete path refuting `X` or
  `RD`.
- cyber: projecting path expressions onto security events of one resource and checking inclusion in a
  pattern language flags misuse sequences [external], with the same `!`/`?`/`Λ` erasure discipline.

## Exercises (Chapter 1)

### Exercise 1.1 — Reaching labels
- Statement: a variant of Reaching Definitions replaces `RD ∈ 𝒫(Var × Lab)` by `RL ∈ 𝒫(Lab)`; "the idea
  is that given the program, a label should suffice for finding the variables that may be assigned in
  some elementary block bearing that label". Use this to modify the §1.3 equation system for `RD⃗` into
  one for `RL⃗`. Hint: think of `RD = {(x₁,?), ···, (x_n,?)}` as meaning
  `RD = {(x₁,?_{x₁}), ···, (x_n,?_{x_n})}` and use `RL = {?_{x₁}, ···, ?_{x_n}}`. ■
- Side conditions: [derived] the variant relies on distinct blocks having distinct labels ([U1:1.2-a]).
- Citation: [PPA Chapter 1 Exercises, p. 31] (book p. 31; PDF p. 51)

### Exercise 1.2 — Least solution of the §1.4 constraints
- Statement: show that the solution displayed for the Control Flow Analysis in §1.4 is a solution, and
  that it is in fact the least solution. Hint: consider the demands on `Ĉ(2)`, `Ĉ(4)`, `ρ̂(x)`, `Ĉ(1)`
  and `Ĉ(5)`. ■
- Citation: [PPA Chapter 1 Exercises, p. 31] (book p. 31; PDF p. 51)

### Exercise 1.3 — Adjoints determine each other
- Statement: let `(α, γ)` be an adjunction, or Galois connection, as in §1.5, i.e.
  `α(X) ⊆ Y ⇔ X ⊆ γ(Y)` for all `X` and `Y`. Show that `α` uniquely determines `γ` (`γ = γ′` whenever
  `(α, γ′)` is an adjunction), and that `γ` uniquely determines `α`. ■
- Citation: [PPA Chapter 1 Exercises, p. 31] (book p. 31; PDF p. 51)

### Exercise 1.4 — Induced analysis versus F
- Statement: for `F` as in §1.3 and `α`, `α⃗`, `γ`, `γ⃗` and `G` as in §1.5, show `α⃗ ∘ G ∘ γ⃗ ⊑ F`; this
  involves showing `α(G_j(γ(RD₁), ···, γ(RD₁₂))) ⊆ F_j(RD₁, ···, RD₁₂)` for all `j` and
  `(RD₁, ···, RD₁₂)`. Determine whether or not `F = α⃗ ∘ G ∘ γ⃗`. Prove by numerical induction on `n`
  that `(α⃗ ∘ G ∘ γ⃗)ⁿ(∅⃗) ⊑ Fⁿ(∅⃗)`. Also prove `α⃗(Gⁿ(∅⃗)) ⊑ (α⃗ ∘ G ∘ γ⃗)ⁿ(∅⃗)` using `α⃗(∅⃗) = ∅⃗` and
  `G ⊑ G ∘ γ⃗ ∘ α⃗`. ■
- Citation: [PPA Chapter 1 Exercises, p. 32] (book p. 32; PDF p. 52)

### Exercise 1.5 — The equality reading of Table 1.2
- Statement: consider the Annotated Type System of Table 1.2 and suppose we want to stick to the first
  (and unsuccessful) explanation of what `S : RD₁ → RD₂` means in terms of Data Flow Analysis. Can
  Table 1.2 be changed (by modifying or removing axioms and rules) so that this becomes possible? ■
- Citation: [PPA Chapter 1 Exercises, p. 32] (book p. 32; PDF p. 52)

### Exercise 1.6 — The Chaotic Iteration invariant
- Statement: suppose `∅⃗ ⊑ RD⃗ ⊑ F(RD⃗) ⊑ Fⁿ(∅⃗) = Fⁿ⁺¹(∅⃗)` holds immediately before the assignment to
  `RD_j` in Chaotic Iteration (§1.7); "show that is also holds afterwards" (finding F-U1-08). Hint: write
  `RD⃗′` for `(RD₁, ···, F_j(RD⃗), ···, RD₁₂)` and use monotonicity of `F` and `RD⃗ ⊑ F(RD⃗)` to establish
  `RD⃗ ⊑ RD⃗′ ⊑ F(RD⃗) ⊑ F(RD⃗′)`. ■
- Citation: [PPA Chapter 1 Exercises, p. 32] (book p. 32; PDF p. 52)

### Exercise 1.7 — Table 1.1 is the least fixed point
- Statement: use the Chaotic Iteration scheme of §1.7 to show that the information displayed in
  Table 1.1 is in fact the least fixed point of the function `F` defined in §1.3. ■
- Citation: [PPA Chapter 1 Exercises, p. 32] (book p. 32; PDF p. 52)

### Exercise 1.8 — The power program
- Statement: for `[z:=1]^1; while [x>0]^2 do ([z:=z*y]^3; [x:=x-1]^4)`, "computing the x-th power of
  the number stored in y", formulate data flow equations as in §1.3, use Chaotic Iteration (§1.7) to
  compute the least solution, and present it in a table like Table 1.1. ■
- Citation: [PPA Chapter 1 Exercises, p. 32] (book p. 32; PDF p. 52)

### Exercise 1.9 — Counting Constant Folding sequences
- Statement: perform Constant Folding upon `[x:=10]^1; [y:=x+10]^2; [z:=y+x]^3` so as to obtain
  `[x:=10]^1; [y:=20]^2; [z:=30]^3`. "How many ways of obtaining the result are there?" ■
- Side conditions: block 3 is `[z:=y+x]^3`, not Example 1.7's `[z:=y+10]^3`.
- Citation: [PPA Chapter 1 Exercises, p. 32] (book p. 32; PDF p. 52)

### Exercise 1.10 — Boolean expressions
- Statement: the Constant Folding of §1.8 only considers arithmetic expressions; extend it to deal also
  with boolean expressions. Consider adding axioms like

```
RD ⊢ ([skip]^ℓ; S) ▷ S
RD ⊢ (if [true]^ℓ then S₁ else S₂) ▷ S₁
```

  and discuss what complications arise. ■
- Citation: [PPA Chapter 1 Exercises, p. 33] (book p. 33; PDF p. 53)

### Exercise 1.11 — Substituting expressions
- Statement: consider adding the axiom

```
RD ⊢ [x := a]^ℓ ▷ [x := a[y ↦ a′]]^ℓ
   if  y ∈ FV(a) ∧ (y,?) ∉ RD_entry(ℓ) ∧
       ∀(z,ℓ′) ∈ RD_entry(ℓ) : (y = z ⇒ [···]^ℓ′ is [y := a′]^ℓ′)
```

  to the Constant Folding of §1.8, and discuss whether or not this is a good idea. ■
- Side conditions: the equality is printed `y = z` here and `z = y` in Table 1.6; the two are
  equivalent.
- Citation: [PPA Chapter 1 Exercises, p. 33] (book p. 33; PDF p. 53)

### Findings (Exercises)
- F-U1-08 (BKL-034): on p. 32 Exercise 1.6 prints "show that is also holds afterwards" for "it". Recorded, not
  corrected. [PPA Chapter 1 Exercises, p. 32] (book p. 32; PDF p. 52)

### Projections (Exercises)
- cs_theory: the exercises close the chapter's open proofs: leastness of the CFA solution (1.2),
  uniqueness of adjoints (1.3), soundness and optimality of the induced analysis (1.4), the Chaotic
  Iteration invariant (1.6), and leastness of Table 1.1 (1.7).
- swe_architecture: 1.1 trades a pair representation for a label representation under unique labels;
  1.10 and 1.11 probe which rewrites a pass manager may run without recomputing Reaching Definitions.
- practical_debugging: 1.7 and 1.8 are hand-execution drills for a solver's trace; 1.9 exposes order
  freedom of the rewrite driver; 1.5 shows why the equality reading fails.
- cyber: 1.11 is the pattern of unsound expression propagation in simplifiers and deobfuscators
  [external]; 1.10's branch pruning deletes labels and definitions that a security analysis may still
  reference.

## Gotcha Ledger

- G-U1-01: Chapter 1 assumes distinct elementary blocks carry distinct labels; dropping the assumption needs reformulated examples and gives less accurate analyses. [PPA §1.2, p. 3]
- G-U1-02: All analyses must be semantics based (provably safe with respect to a semantics); the book does not require them to be semantics directed (structured like the semantics) and does not cover the approaches that are. [PPA §1.1, p. 3]
- G-U1-03: Say the values are "among" a set, not "are" that set; the trivially safe answer {d₁, ···, d_N} is safe but utterly useless. [PPA §1.1, p. 3]
- G-U1-04: Precision is bounded by undecidability (termination of S), so an analysis is expected to return a possibly larger set than what happens at run time. [PPA §1.1, p. 2]
- G-U1-05: Adding pairs to a Reaching Definitions result keeps it safe but less precise; removing a pair that some run realises (e.g. (z,2) at 6) makes it unsafe. [PPA §1.2, p. 5]
- G-U1-06: The label ? is not a program label; kill sets range over all labels including ? (Lab⋆ = {1, ···, 6, ?}), so assignments kill (x,?). [PPA §1.3.1, p. 7]
- G-U1-07: Var⋆ and Lab⋆ are restricted to finite sets; the construction Fⁿ(∅⃗) and its termination rely on this finiteness. [PPA §1.3.1, p. 7]
- G-U1-08: The intended result is the least solution, reached from ∅⃗; larger fixed points stay semantically sound but are less usable. [PPA §1.3.1, p. 8]
- G-U1-09: Every solution of the equation system RD⃗ = F(RD⃗) also solves the inclusions RD⃗ ⊒ F(RD⃗) (whereas the converse need not hold), and both systems have the same least solution. [PPA §1.3.2, p. 10]
- G-U1-10: The printed p. 9 control-flow list omits RD_entry(4) ⊇ RD_exit(3); generate flow constraints from the general rule and Figure 1.2, not by copying the list. [PPA §1.3.2, p. 9]
- G-U1-11: Constraints do not in general split into two neat classes, and collecting constraints with the same left-hand side may require serious work. [PPA §1.3.2, p. 10]
- G-U1-12: Control flow is immediately available for WHILE, unlike more advanced imperative, functional and object-oriented languages where it must itself be computed. [PPA §1.4, p. 10]
- G-U1-13: Control Flow Analysis attaches information to labels rather than entries and exits because the language has no side effects; all subexpressions are labelled. [PPA §1.4, p. 11]
- G-U1-14: Application constraints are conditional: a binding or result constraint applies only when the candidate abstraction is in Ĉ at the operator label. [PPA §1.4, p. 12]
- G-U1-15: The collecting semantics ignores test outcomes (CS_entry(4) = CS_exit(3)), so it specifies a superset of the possible traces. [PPA §1.5, p. 14]
- G-U1-16: (𝒫(Trace))¹² is not finite, so lfp(G) exists but cannot be constructed by the iteration of §1.3. [PPA §1.5, p. 15]
- G-U1-17: The adjunction condition is only "often" demanded, and its verification for the given α and γ is left to the reader. [PPA §1.5, p. 16]
- G-U1-18: The induced analysis is below F (α⃗ ∘ G ∘ γ⃗ ⊑ F); equality (optimality) holds only for some analyses and is left open here (Exercise 1.4). [PPA §1.5, p. 17]
- G-U1-19: A WHILE statement maps a state to a state only "in case it terminates". [PPA §1.6, p. 17]
- G-U1-20: The first reading of S : RD₁ → RD₂ as equalities fails on conditionals; the intended reading uses inclusions and is what makes [sub] unproblematic (pp. 18–19). [PPA §1.6.1, p. 18] [PPA §1.6.1, p. 19]
- G-U1-21: [wh] in Table 1.2 asks for RD as "a consistent guess" (a fixed-point property); Table 1.2 suffices for manual analysis, while an implementation extracts constraints and solves them. [PPA §1.6.1, p. 19] [PPA §1.6.1, p. 20]
- G-U1-22: In Table 1.3, X is a definitely-assigned set (intersection at [if], ∅ at [wh], shrinks under [sub]) while RD is a might-produce set (union, grows under [sub]). [PPA Table 1.3, p. 21]
- G-U1-23: Table 1.3 judgements record what a statement produces, not entry facts: Example 1.4's result has no (x,?) and is not a row of Table 1.1. [PPA §1.6.1, p. 22]
- G-U1-24: The call-tracking rules assume call-by-value: mentioning a variable or building a closure has empty effect, and the body's effect is latent on the arrow. [PPA §1.6.2, p. 24]
- G-U1-25: A more general language needs some subsumption rule for effects, and there are different approaches to it. [PPA §1.6.2, p. 25]
- G-U1-26: Chaotic Iteration starts at ∅⃗, establishing the invariant RD⃗ ⊑ F(RD⃗) so the result equals the least fixed point; it is for manual solving, and implementations must choose j without extensive search. [PPA §1.7, p. 26]
- G-U1-27: RD ⊢ · ▷ · is neither reflexive nor transitive (no rule forces it) and prescribes no order; results need an explicit sequence of steps. [PPA §1.8, p. 28]
- G-U1-28: [ass₁] requires y ∈ FV(a), (y,?) ∉ RD_entry(ℓ) and that every reaching definition of y assigns the same numeral n; [ass₂] requires FV(a) = ∅, a ∉ Num and that a evaluates to n. [PPA Table 1.6, p. 27]
- G-U1-29: Re-using RD across Constant Folding steps is valid because the rewrite changes nothing Reaching Definitions observes; in general re-use is only "sometimes" possible. [PPA §1.8, p. 29]
- G-U1-30: Exercise 1.9's program ends [z:=y+x]^3, not Example 1.7's [z:=y+10]^3. [PPA Chapter 1 Exercises, p. 32]
- G-U1-31: The chapter shows "a few approaches (but by no means all)". [PPA Chapter 1 Concluding Remarks, p. 29]
- G-U1-32: In Mini Project 1.1, Var⋆ and Lab⋆ must be finite and non-empty, and ? in the alphabet {!, ?} is a letter, not the uninitialised label. [PPA Chapter 1 Mini Projects, p. 30] [PPA Chapter 1 Mini Projects, p. 31]
- G-U1-33: The Preface declares denotationally based program analysis, projection analysis, Stone dualities, deeper set constraints, fast type-based implementation, single static assignment form, broader pointer analyses, and general recomputation of invalidated analysis information out of scope. [PPA Preface, p. VI]
