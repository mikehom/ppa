<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 2a (Chapter 2 §§2.1-2.4). -->

# RAW_SHARD_02a — Chapter 2 Intraprocedural Data Flow Analysis and Monotone Frameworks (Unit 2a)

Source: *Principles of Program Analysis* (Nielson, Nielson, Hankin), corrected 2nd printing, 2005.
Scope: Chapter 2 opening, §2.1 Intraprocedural Analysis (§2.1.1–§2.1.5), §2.2 Theoretical Properties
(§2.2.1–§2.2.2), §2.3 Monotone Frameworks (§2.3.1–§2.3.3), and §2.4 Equation Solving (§2.4.1–§2.4.2),
spanning book pages 35–82 / PDF pages 54–101, ending immediately above the §2.5 heading on book p. 82.
Interprocedural Analysis (§2.5), Shape Analysis (§2.6), Concluding Remarks, Mini Projects 2.1–2.3, and
Exercises 2.1–2.25 belong to Unit 2b.

Coordinates: PDF page = book page + 19 throughout Chapter 2 (blank verso p. 34 at the end of Chapter 1 is
absent from the PDF). Section starts in Unit 2a: Chapter 2 opening and §2.1 on p. 35 (§2.1.1 on p. 39,
§2.1.2 on p. 43, §2.1.3 on p. 46, §2.1.4 on p. 49, §2.1.5 on p. 52), §2.2 and §2.2.1 on p. 54 (§2.2.2 on
p. 60), §2.3 on p. 65 (§2.3.1 on p. 67, §2.3.2 on p. 70, §2.3.3 on p. 72), and §2.4 and §2.4.1 on p. 74
(§2.4.2 on p. 78, concluding at the top of p. 82 before §2.5) [PPA §2.1, p. 35] (book p. 35; PDF p. 54).

Conventions:

- Every source reference pairs a strict inline locator token with its book/PDF coordinate companion, for
  example [PPA §2.1, p. 35] (book p. 35; PDF p. 54), [PPA Table 2.1, p. 40] (book p. 40; PDF p. 59), or
  [PPA Preface, p. VI] (book p. VI; PDF p. 6).
- Book-numbered items preserve their exact printed kind word and number (`2.1`–`2.32` in one shared
  per-chapter sequence of 19 Examples, 10 Lemmas, 1 Theorem, and 2 Corollaries, plus Tables `2.1`–`2.9`
  and Figures `2.1`–`2.6`; there are no numbered Definitions, Propositions, Facts, or equation displays
  in §§2.1–2.4). Unnumbered definitions, principles, equations, and the three printed `Remark.` blocks
  carry non-book identifiers `[U2a:<section>-<letter>]`.
- Every formula, rule, program, table, and figure is transcribed from rendered page images (PDF pages 54–101)
  rather than the OCR text layer, which drops or scrambles formulas (`isolated entries`, `isolated exits`,
  `use`, `def`, `ud/du` signatures, `LV^⊆`, `{⋂, ⋃} × {→, ←} × {↑, ↓}`, `path∘`, `MOP∘`, and grid tables).
- Terms absent from the book carry `[external]`. Shard-author deductions or proof steps not printed in
  the text carry `[derived]`. Source misprints and internal tensions are transcribed verbatim as printed
  and logged under `Findings` (`F-U2a-NN`, cross-referenced to existing `BKL-*` items where applicable).
- Notation: script `ℓ, ℓ', ℓ''` for labels; `[B]^ℓ` (and `B^ℓ` where printed without brackets) for labelled
  elementary blocks; `S⋆, Lab⋆, Var⋆, Blocks⋆, AExp⋆` with subscript star ("of the program of interest");
  `Lab⋆^? = Lab⋆ ∪ {?}`; `flow^R` for reverse flow; `Analysis∘, Analysis•`, `MFP∘, MFP•`, `MOP∘, MOP•`,
  `path∘, path•` with open/filled circle subscripts; `State^_CP` for bold `State` under a wide hat with
  sans-serif subscript `CP`; `σ̂` for hatted property states; `op_a, op_b, op_r` (italic syntax),
  `**op**_a, **op**_b, **op**_r` (bold semantic operators on `Z` and `T`), and `op^_a` (hatted sans-serif
  lifted operator on `Z^⊤_⊥`); `■` as printed at the end of statements, proofs, remarks, and examples.

## Chapter 2 Opening

Context: Chapter 2 (*Data Flow Analysis*) opens on p. 35 above the §2.1 heading with the scope of the
chapter and five classification axes [PPA Chapter 2, p. 35] (book p. 35; PDF p. 54).

### [U2a:2.0-a] Scope and plan of Chapter 2 (unnumbered remark)
- Statement: Data Flow Analysis is "the traditional form of program analysis which is described in many
  textbooks on compiler writing". Analyses are presented for the simple imperative language `WHILE`
  introduced in Chapter 1 [PPA §1.2, p. 3] (book p. 3; PDF p. 23): classical Data Flow Analyses
  (Available Expressions, Reaching Definitions, Very Busy Expressions, Live Variables), an operational
  semantics for `WHILE` and the correctness of Live Variables Analysis, Monotone Frameworks and how the
  classical examples recast as instances, a worklist algorithm for solving flow equations with its
  termination and correctness properties, and advanced topics (Interprocedural Data Flow Analysis and
  Shape Analysis, treated in §§2.5–2.6).
- Citation: [PPA Chapter 2, p. 35] (book p. 35; PDF p. 54)

### [U2a:2.0-b] Five analysis distinctions (unnumbered remark)
- Statement: throughout the chapter the book clarifies the distinctions between:
  1. *intraprocedural* and *interprocedural* analyses;
  2. *forward* and *backward* analyses;
  3. *may* and *must* analyses ("or union and intersection analyses");
  4. *flow sensitive* and *flow insensitive* analyses; and
  5. *context sensitive* and *context insensitive* analyses.
- Side conditions: Unit 2a (§§2.1–2.4) develops intraprocedural, flow-sensitive forward/backward and
  may/must analyses; interprocedural and context-sensitivity distinctions appear in §2.5
  [PPA §2.5, p. 82] (book p. 82; PDF p. 101).
- Citation: [PPA Chapter 2, p. 35] (book p. 35; PDF p. 54)

### [U2a:2.0-c] Preface exclusions bearing on Chapter 2 (unnumbered remark)
- Statement: the Preface notes that for reasons of space the book omits "single static assignment form, a
  broader treatment of pointer analyses, and the interplay between analysis and transformation and how to
  efficiently recompute analysis information invalidated by the transformation"
  [PPA Preface, p. VI] (book p. VI; PDF p. 6), while noting that §3.5 incorporates Monotone Frameworks
  from §2.3 and Chapter 6 develops worklist algorithms generalising §2.4
  [PPA Preface, p. VII] (book p. VII; PDF p. 7).
- Citation: [PPA Preface, p. VI] (book p. VI; PDF p. 6); [PPA Preface, p. VII] (book p. VII; PDF p. 7)

### Projections (Chapter 2 Opening)
- cs_theory: classical compiler data flow analyses are flow-sensitive fixed-point specifications classified
  along orthogonal direction (forward versus backward) and path-quantification (may/union versus
  must/intersection) axes before lifting to abstract Monotone Frameworks.
- swe_architecture: classify any proposed static check along the five axes up front to fix its control-flow
  graph direction, join operator, and solver requirements; representations outside the book's scope such as
  SSA [external] or incremental pass invalidation [external] must be supplied by external compiler
  infrastructure.
- practical_debugging: misclassifying a property along may versus must or forward versus backward inverts
  either soundness or termination initialisation; verify axis placement before writing transfer equations.
- cyber: vulnerability checks decompose cleanly along the same axes — source-to-sink taint reachability
  [external] is forward-may, mandatory guard/sanitisation dominance [external] is forward-must, inevitable
  post-use secret scrubbing [external] is backward-must, and dead-store zeroisation [external] is driven by
  backward-may liveness.

## 2.1 Intraprocedural Analysis

Context: syntactic flow-graph extraction operators (`init`, `final`, `blocks`, `labels`, `flow`, `flow^R`),
program-of-interest sets, and structural assumptions (`isolated entries`, `isolated exits`,
`label consistency`) for `WHILE` [PPA §2.1, p. 35] (book p. 35; PDF p. 54).

### [U2a:2.1-a] Entry/exit function pairs (unnumbered definition)
- Statement: §2.1 defines example Data Flow Analyses for `WHILE` by pairs of functions mapping labels to
  appropriate sets: one function specifies information true on *entry* to the block, and the second
  specifies information true at the *exit*.
- Citation: [PPA §2.1, p. 35] (book p. 35; PDF p. 54)

### [U2a:2.1-b] Initial label `init` (unnumbered definition)
- Statement: `init : Stmt → Lab` returns the *initial label* of a statement:

```
init([x := a]^ℓ)               = ℓ
init([skip]^ℓ)                 = ℓ
init(S₁; S₂)                   = init(S₁)
init(if [b]^ℓ then S₁ else S₂) = ℓ
init(while [b]^ℓ do S)         = ℓ
```

- Citation: [PPA §2.1, p. 36] (book p. 36; PDF p. 55)

### [U2a:2.1-c] Final labels `final` (unnumbered definition)
- Statement: `final : Stmt → 𝒫(Lab)` returns the set of *final labels* in a statement; whereas a sequence
  of statements has a single entry, it may have multiple exits (as in the conditional):

```
final([x := a]^ℓ)               = {ℓ}
final([skip]^ℓ)                 = {ℓ}
final(S₁; S₂)                   = final(S₂)
final(if [b]^ℓ then S₁ else S₂) = final(S₁) ∪ final(S₂)
final(while [b]^ℓ do S)         = {ℓ}
```

- Side conditions: "Note that the `while`-loop terminates immediately after the test has evaluated to
  false", so the test label `ℓ` is the sole final label of `while [b]^ℓ do S`.
- Citation: [PPA §2.1, p. 36] (book p. 36; PDF p. 55)

### [U2a:2.1-d] Elementary blocks `Blocks` and `blocks` (unnumbered definition)
- Statement: `Blocks` is the set of statements, or *elementary blocks*, of the form `[x := a]^ℓ` or
  `[skip]^ℓ` as well as the set of tests of the form `[b]^ℓ`. The function `blocks : Stmt → 𝒫(Blocks)` is:

```
blocks([x := a]^ℓ)               = {[x := a]^ℓ}
blocks([skip]^ℓ)                 = {[skip]^ℓ}
blocks(S₁; S₂)                   = blocks(S₁) ∪ blocks(S₂)
blocks(if [b]^ℓ then S₁ else S₂) = {[b]^ℓ} ∪ blocks(S₁) ∪ blocks(S₂)
blocks(while [b]^ℓ do S)         = {[b]^ℓ} ∪ blocks(S)
```

- Side conditions: in the first clause of `blocks`, `x` is printed in typewriter face on both sides
  (finding F-U2a-01), whereas `init`, `final`, and `flow` print italic metavariable `x`.
- Citation: [PPA §2.1, p. 36] (book p. 36; PDF p. 55)

### [U2a:2.1-e] Labels `labels` (unnumbered definition)
- Statement: the set of *labels* occurring in a program is given by `labels : Stmt → 𝒫(Lab)` where
  `labels(S) = {ℓ | [B]^ℓ ∈ blocks(S)}`. Clearly `init(S) ∈ labels(S)` and `final(S) ⊆ labels(S)`.
- Citation: [PPA §2.1, p. 37] (book p. 37; PDF p. 56)

### [U2a:2.1-f] Flows `flow` and flow graph (unnumbered definition)
- Statement: `flow : Stmt → 𝒫(Lab × Lab)` maps statements to sets of edges (*flows*) between labels:

```
flow([x := a]^ℓ)               = ∅
flow([skip]^ℓ)                 = ∅
flow(S₁; S₂)                   = flow(S₁) ∪ flow(S₂) ∪ {(ℓ, init(S₂)) | ℓ ∈ final(S₁)}
flow(if [b]^ℓ then S₁ else S₂) = flow(S₁) ∪ flow(S₂) ∪ {(ℓ, init(S₁)), (ℓ, init(S₂))}
flow(while [b]^ℓ do S)         = flow(S) ∪ {(ℓ, init(S))} ∪ {(ℓ', ℓ) | ℓ' ∈ final(S)}
```

  `labels(S)` and `flow(S)` represent the *flow graph* of `S`.
- Citation: [PPA §2.1, p. 37] (book p. 37; PDF p. 56)

### Example 2.1 — Flow graph of the `power` program
- Statement: for the `power` program (computing the `x`-th power of the number stored in `y`)

```
[z:=1]^1; while [x>0]^2 do ([z:=z*y]^3; [x:=x-1]^4)
```

  `init(power) = 1`, `final(power) = {2}`, `labels(power) = {1, 2, 3, 4}`, and
  `flow(power) = {(1,2), (2,3), (3,4), (4,2)}`, corresponding to Figure 2.1. ■
- Citation: [PPA Example 2.1, p. 37] (book p. 37; PDF p. 56)

### [U2a:2.1-g] Forward entry node and `labels(S)` via `flow(S)` (unnumbered property)
- Statement: `flow` is used in the formulation of *forward analyses*. `init(S)` is the (unique) entry node
  for the flow graph with nodes `labels(S)` and edges `flow(S)`. Moreover:

```
labels(S) = {init(S)} ∪ {ℓ | (ℓ, ℓ') ∈ flow(S)} ∪ {ℓ' | (ℓ, ℓ') ∈ flow(S)}
```

- Side conditions: for composite statements (those not simply of the form `[B]^ℓ`), the equation remains
  true when removing the `{init(S)}` component.
- Citation: [PPA §2.1, p. 37] (book p. 37; PDF p. 56)

### Figure 2.1 — Flow graph for the `power` program
- Content: four vertically stacked boxes `[z:=1]^1`, `[x>0]^2`, `[z:=z*y]^3`, `[x:=x-1]^4`. An entry arrow
  from above enters `[z:=1]^1`; an arrow goes from `[z:=1]^1` to `[x>0]^2`; an arrow labelled `yes` goes
  from `[x>0]^2` to `[z:=z*y]^3`; an arrow goes from `[z:=z*y]^3` to `[x:=x-1]^4`; a back-edge leaves the
  bottom of `[x:=x-1]^4`, loops up on the left, and enters the top of `[x>0]^2`; an exit arrow labelled
  `no` leaves `[x>0]^2` to the right.
- Citation: [PPA Figure 2.1, p. 38] (book p. 38; PDF p. 57)

### [U2a:2.1-h] Reverse flows `flow^R` (unnumbered definition)
- Statement: *backward analyses* require *reverse flows* `flow^R : Stmt → 𝒫(Lab × Lab)` defined by
  `flow^R(S) = {(ℓ, ℓ') | (ℓ', ℓ) ∈ flow(S)}`.
- Citation: [PPA §2.1, p. 38] (book p. 38; PDF p. 57)

### Example 2.2 — Reverse flows of `power`
- Statement: for `power` of Example 2.1, `flow^R(power) = {(2,1), (2,4), (3,2), (4,3)}`, corresponding to
  Figure 2.1 with the direction of the arcs reversed. ■
- Citation: [PPA Example 2.2, p. 38] (book p. 38; PDF p. 57)

### [U2a:2.1-i] Backward entry node and `labels(S)` via `flow^R(S)` (unnumbered property)
- Statement: in case `final(S)` contains just one element, that element is the unique entry node for the
  flow graph with nodes `labels(S)` and edges `flow^R(S)`. Moreover:

```
labels(S) = final(S) ∪ {ℓ | (ℓ, ℓ') ∈ flow^R(S)} ∪ {ℓ' | (ℓ, ℓ') ∈ flow^R(S)}
```

- Side conditions: for composite statements, the equation remains true when removing the `final(S)`
  component; when `|final(S)| > 1` (e.g. a trailing conditional), the reversed graph has multiple entry
  nodes.
- Citation: [PPA §2.1, p. 38] (book p. 38; PDF p. 57)

### [U2a:2.1-j] Program of interest `S⋆` and non-trivial expressions (unnumbered definition)
- Statement: `S⋆` denotes the top-level program being analysed, with `Lab⋆ = labels(S⋆)`,
  `Var⋆ = FV(S⋆)`, `Blocks⋆ = blocks(S⋆)`, and `AExp⋆` the set of *non-trivial* arithmetic subexpressions
  in `S⋆` — an expression is *trivial* if it is a single variable or constant. `AExp(a)` and `AExp(b)`
  denote the sets of non-trivial arithmetic subexpressions of a given arithmetic, respectively boolean,
  expression.
- Citation: [PPA §2.1, p. 38] (book p. 38; PDF p. 57); triviality and `AExp(a), AExp(b)` on
  [PPA §2.1, p. 39] (book p. 39; PDF p. 58)

### [U2a:2.1-k] Isolated entries and isolated exits (unnumbered definition)
- Statement: to simplify presentation and follow literature traditions, the book frequently assumes:
  - *isolated entries*: `∀ℓ ∈ Lab : (ℓ, init(S⋆)) ∉ flow(S⋆)` (holds whenever `S⋆` does not start with a
    `while`-loop);
  - *isolated exits*: `∀ℓ₁ ∈ final(S⋆) ∀ℓ₂ ∈ Lab : (ℓ₁, ℓ₂) ∉ flow(S⋆)`.
- Side conditions: dropped completely from the OCR text layer of p. 39; transcribed from the page image.
  [derived] A program ending in `while [b]^ℓ do S` never has isolated exits because `ℓ ∈ final(S⋆)` and
  `(ℓ, init(S)) ∈ flow(S⋆)`.
- Citation: [PPA §2.1, p. 39] (book p. 39; PDF p. 58)

### [U2a:2.1-l] Label consistency and unique labelling (unnumbered definition)
- Statement: a statement `S` is *label consistent* if and only if `[B₁]^ℓ, [B₂]^ℓ ∈ blocks(S)` implies
  `B₁ = B₂`. If all blocks in `S` are *uniquely labelled* (each label occurs only once), then `S` is label
  consistent. When `S` is label consistent, the clause "where `[B]^ℓ ∈ blocks(S)`" unambiguously defines a
  partial function from labels to elementary blocks, and we say that `ℓ` *labels* the block `B`.
- Citation: [PPA §2.1, p. 39] (book p. 39; PDF p. 58)

### Example 2.3 — Structural properties of `power`
- Statement: `power` of Example 2.1 has isolated entries, does *not* have isolated exits, and is both
  label consistent and uniquely labelled. ■
- Citation: [PPA Example 2.3, p. 39] (book p. 39; PDF p. 58)

### Findings (2.1 Opening)
- F-U2a-01: on p. 36 `blocks([x := a]^ℓ) = {[x := a]^ℓ}` prints typewriter `x` on both sides, whereas
  `init`, `final`, and `flow` print italic metavariable `x`. Recorded as printed.
  [PPA §2.1, p. 36] (book p. 36; PDF p. 55)

### Projections (2.1 Opening)
- cs_theory: syntax-directed CFG extraction (`init`, `final`, `flow`) gives every `WHILE` statement a
  single entry label and a non-empty finite set of exit labels, with `flow^R` inverting edge orientation
  so backward analyses share the same graph substrate; syntactic `flow` over-approximates feasible paths
  because branch outcomes are uninterpreted.
- swe_architecture: enforce unique labelling (hence label consistency) as an IR invariant [external] so
  label-indexed transfer tables are well-defined partial maps; avoid assuming isolated entries or exits in
  library solvers unless synthetic entry/exit sentinel nodes [external] or §2.3's `ι^ℓ_E` join form are
  used.
- practical_debugging: when an analysis loses loop-carried facts at `init(S⋆)` or at a trailing `while`
  header (`final(S⋆)`), check whether §2.1's case-split equations were applied to a program violating
  isolated entries or isolated exits (such as `power` in Example 2.3); check `AExp⋆` filters whenever
  variables or constants appear spuriously in expression sets.
- cyber: syntactic `final(while [b]^ℓ do S) = {ℓ}` treats `while [true]^ℓ` identically to terminating
  loops (see `BKL-017` for reachability consequences), so backward must checks over `flow^R` assume loop
  termination and can falsely certify post-loop cleanup or secret scrubbing [external] past an
  attacker-triggerable infinite loop [derived].

## 2.1.1 Available Expressions Analysis

Context: forward, must (`⋂`, greatest-set) analysis tracking non-trivial arithmetic expressions computed on
all paths and not subsequently modified [PPA §2.1.1, p. 39] (book p. 39; PDF p. 58).

### [U2a:2.1.1-a] Aim and restriction of Available Expressions (unnumbered definition)
- Statement: Available Expressions Analysis determines "For each program point, which expressions *must*
  have already been computed, and not later modified, on all paths to the program point." This avoids
  re-computation of an expression; for clarity, the presentation concentrates on arithmetic expressions.
- Citation: [PPA §2.1.1, p. 39] (book p. 39; PDF p. 58)

### Example 2.4 — Available Expressions motivating program
- Statement: in `[x:=a+b]^1; [y:=a*b]^2; while [y>a+b]^3 do ([a:=a+1]^4; [x:=a+b]^5)`, the expression `a+b`
  is available every time execution reaches test `3` in the loop and need not be recomputed. ■
- Citation: [PPA Example 2.4, p. 39] (book p. 39; PDF p. 58)

### Table 2.1 — Available Expressions Analysis
- Content:

```
kill and gen functions
  kill_AE([x := a]^ℓ) = {a' ∈ AExp⋆ | x ∈ FV(a')}
  kill_AE([skip]^ℓ)   = ∅
  kill_AE([b]^ℓ)      = ∅

  gen_AE([x := a]^ℓ)  = {a' ∈ AExp(a) | x ∉ FV(a')}
  gen_AE([skip]^ℓ)    = ∅
  gen_AE([b]^ℓ)       = AExp(b)

data flow equations: AE^=
  AE_entry(ℓ) = ∅                                       if ℓ = init(S⋆)
                ⋂{AE_exit(ℓ') | (ℓ', ℓ) ∈ flow(S⋆)}     otherwise

  AE_exit(ℓ)  = (AE_entry(ℓ) \ kill_AE(B^ℓ)) ∪ gen_AE(B^ℓ)
                where B^ℓ ∈ blocks(S⋆)
```

- Citation: [PPA Table 2.1, p. 40] (book p. 40; PDF p. 59)

### [U2a:2.1.1-b] Signatures, side conditions, and empty intersection (unnumbered definition)
- Statement: `kill_AE, gen_AE : Blocks⋆ → 𝒫(AExp⋆)` and `AE_entry, AE_exit : Lab⋆ → 𝒫(AExp⋆)`, defined in
  Table 2.1 for a label consistent program `S⋆` (with isolated entries). An expression is *killed* if any
  of its variables is modified in the block; it is *generated* if evaluated in the block and none of its
  variables is later modified in the block (hence `x ∉ FV(a')` in `gen_AE([x := a]^ℓ)`). Forward analysis
  seeking the *largest* sets satisfying `AE^=`: nothing is available at program start (`∅`), and at a block
  with no incoming flow edges the empty intersection `⋂∅` evaluates to `AExp⋆`.
- Citation: [PPA §2.1.1, p. 40] (book p. 40; PDF p. 59); direction, largest sets, and empty intersection on
  [PPA §2.1.1, p. 41] (book p. 41; PDF p. 60)

### Figure 2.2 — A schematic flow graph
- Content: three vertically arranged boxes `[···]^ℓ`, `[···]^{ℓ'}`, `[···]^{ℓ''}`: entry arrow from above
  into `[···]^ℓ`, edge to `[···]^{ℓ'}`, edge labelled `yes` down to `[···]^{ℓ''}`, back-edge from bottom of
  `[···]^{ℓ''}` up to `[···]^{ℓ'}`, and exit arrow labelled `no` rightwards from `[···]^{ℓ'}`.
- Citation: [PPA Figure 2.2, p. 41] (book p. 41; PDF p. 60)

### [U2a:2.1.1-c] Motivation for the largest solution (unnumbered example)
- Statement: instantiating Figure 2.2 as `[z:=x+y]^ℓ; while [true]^{ℓ'} do [skip]^{ℓ''}` yields
  `AE_entry(ℓ) = ∅`, `AE_entry(ℓ') = AE_exit(ℓ) ∩ AE_exit(ℓ'')`, `AE_entry(ℓ'') = AE_exit(ℓ')`,
  `AE_exit(ℓ) = AE_entry(ℓ) ∪ {x+y}`, `AE_exit(ℓ') = AE_entry(ℓ')`, `AE_exit(ℓ'') = AE_entry(ℓ'')`,
  simplifying to `AE_entry(ℓ') = {x+y} ∩ AE_entry(ℓ')`. Of the two solutions `{x+y}` and `∅`, `{x+y}` is
  the most informative because `x+y` is available every time `ℓ'` is entered; thus the *largest* solution
  is required.
- Citation: [PPA §2.1.1, p. 41] (book p. 41; PDF p. 60); simplified equation and conclusion on
  [PPA §2.1.1, p. 42] (book p. 42; PDF p. 61)

### Example 2.5 — Available Expressions on Example 2.4
- Statement: for `[x:=a+b]^1; [y:=a*b]^2; while [y>a+b]^3 do ([a:=a+1]^4; [x:=a+b]^5)`:
  - `kill_AE`/`gen_AE`: label `1` `(∅, {a+b})`, `2` `(∅, {a*b})`, `3` `(∅, {a+b})`,
    `4` `({a+b, a*b, a+1}, ∅)`, `5` `(∅, {a+b})`.
  - Equations: `AE_entry(1) = ∅`, `AE_entry(2) = AE_exit(1)`, `AE_entry(3) = AE_exit(2) ∩ AE_exit(5)`,
    `AE_entry(4) = AE_exit(3)`, `AE_entry(5) = AE_exit(4)`, `AE_exit(1) = AE_entry(1) ∪ {a+b}`,
    `AE_exit(2) = AE_entry(2) ∪ {a*b}`, `AE_exit(3) = AE_entry(3) ∪ {a+b}`,
    `AE_exit(4) = AE_entry(4) \ {a+b, a*b, a+1}`, `AE_exit(5) = AE_entry(5) ∪ {a+b}`.
  - Solution via an analogue of Chapter 1's Chaotic Iteration starting with `AExp⋆` rather than `∅`:

| ℓ | AE_entry(ℓ) | AE_exit(ℓ) |
| :-- | :-- | :-- |
| 1 | ∅ | {a+b} |
| 2 | {a+b} | {a+b, a*b} |
| 3 | {a+b} | {a+b} |
| 4 | {a+b} | ∅ |
| 5 | ∅ | {a+b} |

  Even though `a` is redefined in the loop, `a+b` is re-evaluated at `5` so it is always available on loop
  entry `3`, whereas `a*b` is killed at `4` before the next iteration. ■
- Citation: [PPA Example 2.5, p. 42] (book p. 42; PDF p. 61); closing commentary on
  [PPA Example 2.5, p. 43] (book p. 43; PDF p. 62)

### Projections (2.1.1)
- cs_theory: Available Expressions is a forward must-analysis over `𝒫(AExp⋆)` where safe approximation
  errs toward smaller sets (`⊆`); cyclic self-dependence under `∩` admits spurious smaller fixed points
  (`∅`), forcing selection of the greatest fixed point under `⊆` (equivalently least fixed point under `⊇`).
- swe_architecture: drives common subexpression elimination [external] under preconditions of label
  consistency, isolated entries, and pure error-free evaluation; non-extremal states must initialise to
  the finite program universe `AExp⋆` while `init(S⋆)` starts at `∅`.
- practical_debugging: if loop headers report `∅` for invariant expressions, check whether non-extremal
  nodes were initialised to `∅` instead of `AExp⋆`; if `[a := a+1]^4` marks `a+1` available, `gen_AE`
  omitted the post-assignment filter `x ∉ FV(a')`.
- cyber: models mandatory pre-sink security gates or bounds checks (`checked(buf, n)` [external]) that must
  hold on *every* path without subsequent mutation of `buf` or `n`; omitting `x ∉ FV(a')` in `gen_AE` or
  swapping `∩` for `∪` creates a time-of-check-to-time-of-use [external] bypass where a mutated or
  single-branch check masks an unchecked path [derived].

## 2.1.2 Reaching Definitions Analysis

Context: forward, may (`⋃`, smallest-set) analysis tracking variable assignments (and uninitialised status
`?`) that may reach a point along some path [PPA §2.1.2, p. 43] (book p. 43; PDF p. 62).

### [U2a:2.1.2-a] Specification of Reaching Definitions (unnumbered definition)
- Statement: properly called *reaching assignments*, Reaching Definitions Analysis determines "For each
  program point, which assignments *may* have been made and not overwritten, when program execution reaches
  this point along some path." Main application: constructing direct links between value-producing and
  value-using blocks (§2.1.5).
- Citation: [PPA §2.1.2, p. 43] (book p. 43; PDF p. 62)

### Example 2.6 — Reaching Definitions motivating program
- Statement: in `[x:=5]^1; [y:=1]^2; while [x>1]^3 do ([y:=x*y]^4; [x:=x-1]^5)`, all assignments reach the
  entry of `4` (`1` and `2` on the first iteration), while only `1`, `4`, and `5` reach the entry of `5`. ■
- Citation: [PPA Example 2.6, p. 43] (book p. 43; PDF p. 62)

### [U2a:2.1.2-b] Signatures, special label `?`, and side conditions (unnumbered definition)
- Statement: setting `Lab⋆^? = Lab⋆ ∪ {?}` with special label `?` for uninitialised variables (compare
  Chapter 1 [PPA §1.3.1, p. 7] (book p. 7; PDF p. 27), where `?` was placed inside `Lab⋆` itself; see
  `BKL-035`), `kill_RD, gen_RD : Blocks⋆ → 𝒫(Var⋆ × Lab⋆^?)` and
  `RD_entry, RD_exit : Lab⋆ → 𝒫(Var⋆ × Lab⋆^?)` are defined in Table 2.2 for a label consistent program
  `S⋆` (with isolated entries). Only assignments generate definitions; assigning to `x` destroys `(x, ?)`
  and every `(x, ℓ')` assigning `x` in `S⋆`.
- Citation: [PPA §2.1.2, p. 43] (book p. 43; PDF p. 62); isolated-entries assumption on
  [PPA §2.1.2, p. 44] (book p. 44; PDF p. 63)

### Table 2.2 — Reaching Definitions Analysis
- Content:

```
kill and gen functions
  kill_RD([x := a]^ℓ) = {(x, ?)}
                        ∪ {(x, ℓ') | B^{ℓ'} is an assignment to x in S⋆}
  kill_RD([skip]^ℓ)   = ∅
  kill_RD([b]^ℓ)      = ∅

  gen_RD([x := a]^ℓ)  = {(x, ℓ)}
  gen_RD([skip]^ℓ)    = ∅
  gen_RD([b]^ℓ)       = ∅

data flow equations: RD^=
  RD_entry(ℓ) = {(x, ?) | x ∈ FV(S⋆)}                   if ℓ = init(S⋆)
                ⋃{RD_exit(ℓ') | (ℓ', ℓ) ∈ flow(S⋆)}     otherwise

  RD_exit(ℓ)  = (RD_entry(ℓ) \ kill_RD(B^ℓ)) ∪ gen_RD(B^ℓ)
                where B^ℓ ∈ blocks(S⋆)
```

- Citation: [PPA Table 2.2, p. 44] (book p. 44; PDF p. 63)

### [U2a:2.1.2-c] Smallest-solution motivation and empty union (unnumbered example)
- Statement: forward analysis seeking the *smallest* sets satisfying `RD^=`; with no predecessors `⋃∅`
  evaluates to `∅`. On `[z:=x+y]^ℓ; while [true]^{ℓ'} do [skip]^{ℓ''}` (Figure 2.2), the equations simplify
  (with `RD_exit(ℓ)` printed as `(RD_entry(ℓ) \ {(z, ?)}) ∪ {(z, ℓ)}`, finding F-U2a-02) to
  `RD_entry(ℓ') = {(x,?), (y,?), (z,ℓ)} ∪ RD_entry(ℓ')`, which is satisfied by every superset of
  `{(x,?), (y,?), (z,ℓ)}`; because `ℓ'` generates no definitions, the smallest solution is most precise.
- Citation: [PPA §2.1.2, p. 44] (book p. 44; PDF p. 63); simplified equation on
  [PPA §2.1.2, p. 45] (book p. 45; PDF p. 64)

### [U2a:2.1.2-d] Soundness hazard of `RD_entry(init(S⋆)) = ∅` (unnumbered remark)
- Statement: presentations in the literature that set `RD_entry(init(S⋆)) = ∅` rather than
  `{(x, ?) | x ∈ FV(S⋆)}` are "correct only for programs that always assign variables before their first
  use; incorrect optimisations may result if this is not the case". The book's formulation is always
  semantically sound, as emerges in [PPA Mini Project 2.2, p. 133] (book p. 133; PDF p. 152).
- Citation: [PPA §2.1.2, p. 45] (book p. 45; PDF p. 64)

### Example 2.7 — Reaching Definitions on Example 2.6
- Statement: for `[x:=5]^1; [y:=1]^2; while [x>1]^3 do ([y:=x*y]^4; [x:=x-1]^5)`:
  - `kill_RD`/`gen_RD`: `1` `({(x,?), (x,1), (x,5)}, {(x,1)})`, `2` `({(y,?), (y,2), (y,4)}, {(y,2)})`,
    `3` `(∅, ∅)`, `4` `({(y,?), (y,2), (y,4)}, {(y,4)})`, `5` `({(x,?), (x,1), (x,5)}, {(x,5)})`.
  - Solution by Chaotic Iteration:

| ℓ | RD_entry(ℓ) | RD_exit(ℓ) |
| :-- | :-- | :-- |
| 1 | {(x,?), (y,?)} | {(y,?), (x,1)} |
| 2 | {(y,?), (x,1)} | {(x,1), (y,2)} |
| 3 | {(x,1), (y,2), (y,4), (x,5)} | {(x,1), (y,2), (y,4), (x,5)} |
| 4 | {(x,1), (y,2), (y,4), (x,5)} | {(x,1), (y,4), (x,5)} |
| 5 | {(x,1), (y,4), (x,5)} | {(y,4), (x,5)} |

  ■
- Citation: [PPA Example 2.7, p. 45] (book p. 45; PDF p. 64); Chaotic Iteration solution table on
  [PPA Example 2.7, p. 46] (book p. 46; PDF p. 65)

### Projections (2.1.2)
- cs_theory: Reaching Definitions is a forward may-analysis over `(𝒫(Var⋆ × Lab⋆^?), ⊆)` where safe
  approximation errs toward larger sets (`⊇`); the sentinel `?` totalises initial definitions so
  read-before-write executions are represented inside the lattice rather than outside the semantics.
- swe_architecture: serves as the producer pass for def-use indexes (§2.1.5) and Constant Folding (§1.8),
  requiring label consistency and either isolated entries or §2.3's `ι^ℓ_E` join at `init(S⋆)`; never
  substitute `ι = ∅` unless definite assignment has already been verified upstream.
- practical_debugging: if Constant Folding folds a variable that could be uninitialised on one branch,
  inspect `RD_entry(init(S⋆))` and `kill_RD` — both must include `(x, ?)`; if a program starting with a
  `while` loop loses back-edge definitions at `init(S⋆)`, Table 2.2's isolated-entries precondition was
  violated.
- cyber: directly instantiates intraprocedural source-to-sink taint reachability and uninitialised-memory
  detection (`(x, ?) ∈ RD_entry(ℓ)` flags potential read-before-write vulnerabilities [external]); because
  it over-approximates (`⊇`), absence of taint or `(x, ?)` guarantees safety under `WHILE` semantics, while
  alerts may be false positives [external] from infeasible paths.

## 2.1.3 Very Busy Expressions Analysis

Context: backward, must (`⋂`, greatest-set) analysis identifying expressions guaranteed to be evaluated
before any constituent variable is redefined along every path from a point
[PPA §2.1.3, p. 46] (book p. 46; PDF p. 65).

### [U2a:2.1.3-a] Specification and hoisting (unnumbered definition)
- Statement: an expression is *very busy* at the exit from a label if, no matter what path is taken from
  the label, it must always be used before any of the variables occurring in it are redefined. Very Busy
  Expressions Analysis determines "For each program point, which expressions *must* be very busy at the
  exit from the point." Evaluating such an expression at the block and storing its value for later use is
  called *hoisting* the expression.
- Citation: [PPA §2.1.3, p. 46] (book p. 46; PDF p. 65)

### Example 2.8 — Very Busy Expressions motivating program
- Statement: in `if [a>b]^1 then ([x:=b-a]^2; [y:=a-b]^3) else ([y:=b-a]^4; [x:=a-b]^5)`, both `a-b` and
  `b-a` are very busy at the start of the conditional and can be hoisted there to save code size. ■
- Citation: [PPA Example 2.8, p. 46] (book p. 46; PDF p. 65)

### [U2a:2.1.3-b] `kill_VB`, `gen_VB`, and contrast with `gen_AE` (unnumbered definition)
- Statement: `kill_VB, gen_VB : Blocks⋆ → 𝒫(AExp⋆)` and `VB_entry, VB_exit : Lab⋆ → 𝒫(AExp⋆)` are defined
  in Table 2.3 for a label consistent program `S⋆` (with isolated exits). `kill_VB` is equivalent to
  `kill_AE`, whereas "All of the expressions that appear in a block are very busy at the entry to the
  block (unlike what was the case for Available Expressions)" — so `gen_VB([x := a]^ℓ) = AExp(a)` without
  filtering `x ∉ FV(a')`.
- Citation: [PPA §2.1.3, p. 46] (book p. 46; PDF p. 65); `VB_entry, VB_exit` and isolated exits on
  [PPA §2.1.3, p. 47] (book p. 47; PDF p. 66)

### Table 2.3 — Very Busy Expressions Analysis
- Content:

```
kill and gen functions
  kill_VB([x := a]^ℓ) = {a' ∈ AExp⋆ | x ∈ FV(a')}
  kill_VB([skip]^ℓ)   = ∅
  kill_VB([b]^ℓ)      = ∅

  gen_VB([x := a]^ℓ)  = AExp(a)
  gen_VB([skip]^ℓ)    = ∅
  gen_VB([b]^ℓ)       = AExp(b)

data flow equations: VB^=
  VB_exit(ℓ)  = ∅                                         if ℓ ∈ final(S⋆)
                ⋂{VB_entry(ℓ') | (ℓ', ℓ) ∈ flow^R(S⋆)}   otherwise

  VB_entry(ℓ) = (VB_exit(ℓ) \ kill_VB(B^ℓ)) ∪ gen_VB(B^ℓ)
                where B^ℓ ∈ blocks(S⋆)
```

- Side conditions: in `gen_VB([x := a]^ℓ)`, `x` is printed in typewriter face (finding F-U2a-01).
- Citation: [PPA Table 2.3, p. 47] (book p. 47; PDF p. 66)

### [U2a:2.1.3-c] Backward largest-solution motivation (unnumbered example)
- Statement: backward analysis propagating against program flow (`flow^R`) and seeking the *largest* sets
  satisfying `VB^=`; with no successors `⋂∅ = AExp⋆`, and at any `ℓ ∈ final(S⋆)` `VB_exit(ℓ) = ∅`. On
  `(while [x>1]^ℓ do [skip]^{ℓ'}); [x:=x+1]^{ℓ''}` (Figure 2.3), `VB_entry(ℓ'') = {x+1}` (since `x+1` is
  killed and re-added by `gen_VB`) and `VB_exit(ℓ) = VB_exit(ℓ) ∩ {x+1}`, whose subsets `∅` and `{x+1}`
  require selecting the *largest* solution `{x+1}`.
- Citation: [PPA §2.1.3, p. 47] (book p. 47; PDF p. 66); `VB_exit(ℓ)` equation on
  [PPA §2.1.3, p. 48] (book p. 48; PDF p. 67)

### Figure 2.3 — A schematic flow graph (in reverse)
- Content: reversed-arc diagram for `(while [x>1]^ℓ do [skip]^{ℓ'}); [x:=x+1]^{ℓ''}`: `[···]^ℓ` at upper
  left, `[···]^{ℓ'}` below it (`yes` arrow pointing up into `[···]^ℓ`, reverse loop-back arrow from top of
  `[···]^ℓ` down into bottom of `[···]^{ℓ'}`), `[···]^{ℓ''}` at upper right (reverse entry arrow from below
  into `[···]^{ℓ''}`, `no` arrow pointing left into `[···]^ℓ`), and reverse exit arrow leaving `[···]^ℓ`
  upwards.
- Citation: [PPA Figure 2.3, p. 48] (book p. 48; PDF p. 67)

### Example 2.9 — Very Busy Expressions on Example 2.8
- Statement: for `if [a>b]^1 then ([x:=b-a]^2; [y:=a-b]^3) else ([y:=b-a]^4; [x:=a-b]^5)`:
  - `kill_VB` is `∅` at `1..5`; `gen_VB` is `∅` at `1`, `{b-a}` at `2, 4`, and `{a-b}` at `3, 5`.
  - Chaotic Iteration analogue starting with `AExp⋆` yields:

| ℓ | VB_entry(ℓ) | VB_exit(ℓ) |
| :-- | :-- | :-- |
| 1 | {a-b, b-a} | {a-b, b-a} |
| 2 | {a-b, b-a} | {a-b} |
| 3 | {a-b} | ∅ |
| 4 | {a-b, b-a} | {a-b} |
| 5 | {a-b} | ∅ |

  ■
- Citation: [PPA Example 2.9, p. 48] (book p. 48; PDF p. 67); `VB_exit` equations and solution table on
  [PPA Example 2.9, p. 49] (book p. 49; PDF p. 68)

### Projections (2.1.3)
- cs_theory: Very Busy Expressions is the backward dual of Available Expressions (`flow^R`, `E = final(S⋆)`,
  `⋂`, greatest solution under `⊆`), differing asymmetrically in `gen_VB([x := a]^ℓ) = AExp(a)` because
  right-hand-side evaluation precedes left-hand-side state update within an assignment step.
- swe_architecture: drives code-size hoisting passes under preconditions of label consistency, isolated
  exits, and total fault-free operators (`BKL-001`); in languages with division traps or memory faults
  [external], hoisting across a guard or potentially non-terminating loop (`Figure 2.3`) is unsound without
  a separate safety/termination check [derived].
- practical_debugging: copying `gen_AE`'s `x ∉ FV(a')` filter into `gen_VB` misses self-updating expressions
  like `[x := x+1]^{ℓ''}` (`VB_entry(ℓ'')` becomes `∅` instead of `{x+1}`); running Table 2.3 on a program
  ending in a `while` loop drops loop-body uses because `final(S⋆)` overwrites `VB_exit(ℓ)` with `∅`.
- cyber: models post-acquisition obligation checks (verifying that `unlock(m)` or `zeroize(buf)` [external]
  occurs on all paths to `final(S⋆)`), with two critical caveats [derived]: (1) hoisting partial operations
  (`a / y`, `*p` [external]) introduces divide-by-zero or null-dereference crashes (`BKL-001`), and (2)
  syntactic `flow^R` ignores non-terminating loops (`BKL-017`) that prevent cleanup from ever executing.

## 2.1.4 Live Variables Analysis

Context: backward, may (`⋃`, smallest-set) analysis tracking variables whose current value may be read
before redefinition along some path [PPA §2.1.4, p. 49] (book p. 49; PDF p. 68).

### [U2a:2.1.4-a] Specification, exit convention, and Dead Code Elimination (unnumbered definition)
- Statement: a variable is *live* at the exit from a label if there exists a path from the label to a use
  of the variable that does not re-define the variable. Live Variables Analysis determines "For each
  program point, which variables *may* be live at the exit from the point." The book takes the view that no
  variables are live at the end of the program, noting that "for some applications it might be better to
  assume that all variables are live at the end of the program" (missing period as printed; finding
  F-U2a-03). Basis for *Dead Code Elimination*: if `x` is not live at the exit from `ℓ` and `[B]^ℓ` is an
  assignment to `x`, the elementary block can be eliminated.
- Citation: [PPA §2.1.4, p. 49] (book p. 49; PDF p. 68)

### Example 2.10 — Live Variables motivating program
- Statement: in `[x:=2]^1; [y:=4]^2; [x:=1]^3; (if [y>x]^4 then [z:=y]^5 else [z:=y*y]^6); [x:=z]^7`
  (introduced as "the following expression", finding F-U2a-03), `x` is not live at the exit from `1` (the
  first assignment is redundant), whereas both `x` and `y` are live at the exit from `3`. ■
- Citation: [PPA Example 2.10, p. 49] (book p. 49; PDF p. 68)

### [U2a:2.1.4-b] `kill_LV`, `gen_LV`, and side conditions (unnumbered definition)
- Statement: `kill_LV, gen_LV : Blocks⋆ → 𝒫(Var⋆)` and `LV_exit, LV_entry : Lab⋆ → 𝒫(Var⋆)` are defined in
  Table 2.4 for a label consistent program `S⋆` (with isolated exits).
- Citation: [PPA §2.1.4, p. 49] (book p. 49; PDF p. 68); `gen_LV`, `LV_exit, LV_entry`, and isolated exits
  on [PPA §2.1.4, p. 50] (book p. 50; PDF p. 69)

### Table 2.4 — Live Variables Analysis
- Content:

```
kill and gen functions
  kill_LV([x := a]^ℓ) = {x}
  kill_LV([skip]^ℓ)   = ∅
  kill_LV([b]^ℓ)      = ∅

  gen_LV([x := a]^ℓ)  = FV(a)
  gen_LV([skip]^ℓ)    = ∅
  gen_LV([b]^ℓ)       = FV(b)

data flow equations: LV^=
  LV_exit(ℓ)  = ∅                                         if ℓ ∈ final(S⋆)
                ⋃{LV_entry(ℓ') | (ℓ', ℓ) ∈ flow^R(S⋆)}   otherwise

  LV_entry(ℓ) = (LV_exit(ℓ) \ kill_LV(B^ℓ)) ∪ gen_LV(B^ℓ)
                where B^ℓ ∈ blocks(S⋆)
```

- Citation: [PPA Table 2.4, p. 50] (book p. 50; PDF p. 69)

### [U2a:2.1.4-c] Smallest-solution motivation for Live Variables (unnumbered example)
- Statement: backward analysis seeking the *smallest* sets satisfying `LV^=`; with no successors `⋃∅ = ∅`.
  On `(while [x>1]^ℓ do [skip]^{ℓ'}); [x:=x+1]^{ℓ''}` (Figure 2.3), `LV_exit(ℓ) = LV_exit(ℓ) ∪ {x}` is
  solved by any superset of `{x}`; since optimisations rely on *dead* variables, smaller live sets enable
  more optimisations, so `{x}` is chosen. Semantic correctness is established in §2.2.
- Citation: [PPA §2.1.4, p. 50] (book p. 50; PDF p. 69); `LV_exit(ℓ)` calculation and §2.2 forward
  reference on [PPA §2.1.4, p. 51] (book p. 51; PDF p. 70)

### Example 2.11 — Live Variables on Example 2.10
- Statement: for `[x:=2]^1; [y:=4]^2; [x:=1]^3; (if [y>x]^4 then [z:=y]^5 else [z:=y*y]^6); [x:=z]^7`:
  - `kill_LV`/`gen_LV`: `1` `({x}, ∅)`, `2` `({y}, ∅)`, `3` `({x}, ∅)`, `4` `(∅, {x,y})`, `5` `({z}, {y})`,
    `6` `({z}, {y})`, `7` `({x}, {z})`.
  - Chaotic Iteration solution (assuming all variables dead at program end):

| ℓ | LV_entry(ℓ) | LV_exit(ℓ) |
| :-- | :-- | :-- |
| 1 | ∅ | ∅ |
| 2 | ∅ | {y} |
| 3 | {y} | {x,y} |
| 4 | {x,y} | {y} |
| 5 | {y} | {z} |
| 6 | {y} | {z} |
| 7 | {z} | ∅ |

  If variables of interest are output at the end of the program, `LV_exit(7)` should be `{x, y, z}`, making
  `LV_entry(7)`, `LV_exit(5)`, and `LV_exit(6)` all equal `{y, z}`. ■
- Citation: [PPA Example 2.11, p. 51] (book p. 51; PDF p. 70); `LV_exit(5..7)`, solution table, and output
  convention note on [PPA Example 2.11, p. 52] (book p. 52; PDF p. 71)

### Findings (2.1.1–2.1.4)
- F-U2a-02: on p. 44 the schematic equation writes `RD_exit(ℓ) = (RD_entry(ℓ) \ {(z, ?)}) ∪ {(z, ℓ)}` where
  Table 2.2 defines `kill_RD([z:=x+y]^ℓ) = {(z, ?), (z, ℓ)}`; the resulting set is identical because
  `(z, ℓ)` is immediately unioned back in. Recorded as printed. [PPA §2.1.2, p. 44] (book p. 44; PDF p. 63)
- F-U2a-03: on p. 49 the paragraph ending "live at the end of the program" lacks a closing period, and
  Example 2.10 calls its seven-statement program "the following expression". Recorded as printed.
  [PPA §2.1.4, p. 49] (book p. 49; PDF p. 68)

### Projections (2.1.4)
- cs_theory: Live Variables is a backward may-analysis over `(𝒫(Var⋆), ⊆)` where safe approximation errs
  toward larger live sets (`⊇`), dualising Dead Code Elimination safety (a variable may be eliminated only
  when provably absent from the over-approximating live set).
- swe_architecture: parameterise liveness passes by the exit-live boundary set `ι` (`∅` for closed whole
  programs versus return/output/escaped variables `{x, y, z}` for procedures and modules), and enforce
  isolated exits (or §2.3's `ι^ℓ_E` equation) before running Dead Code Elimination.
- practical_debugging: on a program without isolated exits such as
  `while [x>0]^1 do ([x:=x-y]^2; [y:=5]^3)`, Table 2.4's `if ℓ ∈ final(S⋆)` branch forces `LV_exit(1) = ∅`
  and `LV_exit(3) = {x}`, unsoundly marking `[y:=5]^3` dead across loop iterations [derived]; always use
  `LV_exit(ℓ) = ⋃{...} ∪ ι^ℓ_E` in implementations.
- cyber: `LV_exit(final) = ∅` is the exact formal mechanism behind compiler dead-store elimination
  removing trailing cryptographic key/password scrubs (`[key := 0]^7` before return, `BKL-006` / CWE-14 [external])
  unless secret buffers are marked observable in `ι` or scrubbed via volatile/intrinsic barriers
  [external]; conversely, an assigned status variable absent from `LV_exit` detects unchecked security
  return codes (CWE-252 [external]).

## 2.1.5 Derived Data Flow Information

Context: declarative definition-clear paths (`clear`, `use`, `def`) and Use-Definition / Definition-Use
chains (`ud`, `du`), plus constructive `UD`/`DU` from Reaching Definitions
[PPA §2.1.5, p. 52] (book p. 52; PDF p. 71).

### [U2a:2.1.5-a] Use-Definition and Definition-Use chains (unnumbered definition)
- Statement: links associating to each use of a variable all assignments reaching that use are called
  *Use-Definition chains* or *ud*-chains; links associating to each assignment all uses are called
  *Definition-Use chains* or *du*-chains.
- Citation: [PPA §2.1.5, p. 52] (book p. 52; PDF p. 71)

### [U2a:2.1.5-b] Definition-clear path and predicates `clear`, `use`, `def` (unnumbered definition)
- Statement: informally, "`ℓ₁, ···, ℓ_n` is a definition clear path for `x` if none of the blocks labelled
  `ℓ₁, ···, ℓ_n` assigns a value to `x` and if `ℓ_n` uses `x`" (finding F-U2a-04). Formally, for a label
  consistent program `S⋆`:

```
clear(x, ℓ, ℓ') = ∃ℓ₁, ···, ℓ_n :
                    (ℓ₁ = ℓ) ∧ (ℓ_n = ℓ') ∧ (n > 0) ∧
                    (∀i ∈ {1, ···, n-1} : (ℓ_i, ℓ_{i+1}) ∈ flow(S⋆)) ∧
                    (∀i ∈ {1, ···, n-1} : ¬def(x, ℓ_i)) ∧ use(x, ℓ_n)

use(x, ℓ) = (∃B : [B]^ℓ ∈ blocks(S⋆) ∧ x ∈ gen_LV([B]^ℓ))
def(x, ℓ) = (∃B : [B]^ℓ ∈ blocks(S⋆) ∧ x ∈ kill_LV([B]^ℓ))
```

- Side conditions: in the formal formula `¬def(x, ℓ_i)` ranges over `i ∈ {1, ···, n-1}` only, allowing the
  using block `ℓ_n` itself to assign `x` (e.g. `[x := x+1]^{ℓ_n}`).
- Citation: [PPA §2.1.5, p. 52] (book p. 52; PDF p. 71)

### [U2a:2.1.5-c] Non-constructive `ud` and `du` functions (unnumbered definition)
- Statement: printed with signature `ud, du : Var⋆ × Lab⋆ → 𝒫(Lab⋆)` (`[Source Erratum]`, finding F-U2a-05):

```
ud(x, ℓ') = {ℓ | def(x, ℓ) ∧ ∃ℓ'' : (ℓ, ℓ'') ∈ flow(S⋆) ∧ clear(x, ℓ'', ℓ')}
          ∪ {? | clear(x, init(S⋆), ℓ')}

du(x, ℓ)  = {ℓ' | def(x, ℓ) ∧ ∃ℓ'' : (ℓ, ℓ'') ∈ flow(S⋆) ∧ clear(x, ℓ'', ℓ')}   if ℓ ≠ ?
            {ℓ' | clear(x, init(S⋆), ℓ')}                                        if ℓ = ?
```

  `ud(x, ℓ')` returns the labels where an occurrence of `x` at `ℓ'` might have obtained its value (or `?`
  if possibly uninitialised); `du(x, ℓ)` returns the labels where the value assigned to `x` at `ℓ` (or
  uninitialised at `?`) might be used. Stated duality (without proof): `du(x, ℓ) = {ℓ' | ℓ ∈ ud(x, ℓ')}`.
- Citation: [PPA §2.1.5, p. 53] (book p. 53; PDF p. 72)

### Example 2.12 — `ud` and `du` chains
- Statement: for `[x:=0]^1; [x:=3]^2; (if [z=x]^3 then [z:=0]^4 else [z:=x]^5); [y:=x]^6; [x:=y+z]^7`:

| ud(x, ℓ) | x | y | z |
| :-- | :-- | :-- | :-- |
| 1 | ∅ | ∅ | ∅ |
| 2 | ∅ | ∅ | ∅ |
| 3 | {2} | ∅ | {?} |
| 4 | ∅ | ∅ | ∅ |
| 5 | {2} | ∅ | ∅ |
| 6 | {2} | ∅ | ∅ |
| 7 | ∅ | {6} | {4, 5} |

| du(x, ℓ) | x | y | z |
| :-- | :-- | :-- | :-- |
| 1 | ∅ | ∅ | ∅ |
| 2 | {3, 5, 6} | ∅ | ∅ |
| 3 | ∅ | ∅ | ∅ |
| 4 | ∅ | ∅ | {7} |
| 5 | ∅ | ∅ | {7} |
| 6 | ∅ | {7} | ∅ |
| 7 | ∅ | ∅ | ∅ |
| ? | ∅ | ∅ | {3} |

  `x` in block `3` gets its value in block `2`; the value assigned to `x` in block `2` may be used in
  blocks `3`, `5`, and `6`. ■
- Citation: [PPA Example 2.12, p. 53] (book p. 53; PDF p. 72)

### [U2a:2.1.5-d] Applications: Dead Code Elimination and Code Motion (unnumbered remark)
- Statement: in Example 2.12, *Dead Code Elimination* can remove block `1` because there is no use of the
  value assigned to `x` before reassignment in block `2`; *Code Motion* can move block `6` (`[y:=x]^6`) to
  just in front of the conditional because it uses only variables assigned in earlier blocks and the
  conditional does not use `y`.
- Citation: [PPA §2.1.5, p. 53] (book p. 53; PDF p. 72); sentence completion and Code Motion on
  [PPA §2.1.5, p. 54] (book p. 54; PDF p. 73)

### [U2a:2.1.5-e] Constructive `UD` and `DU` from Reaching Definitions (unnumbered definition)
- Statement: `ud` and `du` are not constructive. Re-using `RD_entry` and `gen_LV`, the book defines
  `UD : Var⋆ × Lab⋆ → 𝒫(Lab⋆)` (`[Source Erratum]`, finding F-U2a-05) by:

```
UD(x, ℓ) = {ℓ' | (x, ℓ') ∈ RD_entry(ℓ)}   if x ∈ gen_LV(B^ℓ)
           ∅                               otherwise
```

  Constructive `DU : Var⋆ × Lab⋆ → 𝒫(Lab⋆)` and the formal relationship between `UD`/`DU` and `ud`/`du` are
  left to [PPA Mini Project 2.1, p. 132] (book p. 132; PDF p. 151).
- Citation: [PPA §2.1.5, p. 54] (book p. 54; PDF p. 73)

### Findings (2.1.5)
- F-U2a-04: on p. 52 the informal prose requires that none of `ℓ₁, ···, ℓ_n` assigns `x`, whereas the
  formal predicate `clear(x, ℓ, ℓ')` restricts `¬def(x, ℓ_i)` to `i ∈ {1, ···, n-1}` so `ℓ_n` may both read
  and assign `x`. Recorded as printed. [PPA §2.1.5, p. 52] (book p. 52; PDF p. 71)
- F-U2a-05 (`[Source Erratum]`): on pp. 53–54 `ud, du` and `UD, DU` are declared with `Lab⋆` rather than
  `Lab⋆^? = Lab⋆ ∪ {?}` (defined on p. 43), even though `ud` and `UD` return `?` (`ud(z, 3) = {?}` in
  Example 2.12, requiring codomain `𝒫(Lab⋆^?)`) and `du` branches on `ℓ = ?` (`du(z, ?) = {3}`, requiring
  domain `Var⋆ × Lab⋆^?`). Recorded as printed.
  [PPA §2.1.5, p. 53] (book p. 53; PDF p. 72); [PPA §2.1.5, p. 54] (book p. 54; PDF p. 73)

### Projections (2.1.5)
- cs_theory: `ud` and `du` are mutually transpose binary relations (`ℓ ∈ ud(x, ℓ') ⇔ ℓ' ∈ du(x, ℓ)`) over
  syntactic definition-clear paths; `UD` computes an over-approximating fixed-point realisation from
  `RD_entry` gated by `gen_LV`.
- swe_architecture: expose `UD`/`DU` as a queryable def-use index service over label-consistent IRs so
  client passes (Dead Code Elimination, Code Motion) decouple from the fixed-point solver; type the API
  with `Lab⋆^?` so uninitialised entry uses (`?`) do not cause type/lookup errors (`F-U2a-05`).
- practical_debugging: backward data-only slicing [external] from a wrong value at `ℓ'` walks `UD(x, ℓ')`
  transitively; if `[x := x+1]^ℓ` breaks the chain, check that `clear` excludes `def` only on `1..n-1` and
  not at `ℓ_n`; note that `du(x, 1) = ∅` justifies deleting `[x:=0]^1` only when `x` is also dead at
  program exit or overwritten on all paths (`[x:=3]^2`).
- cyber: transitive `UD` traversal from a dangerous sink (`memcpy` length or SQL query [external]) recovers
  candidate attacker sources and uninitialised reads (`? ∈ UD(z, 3)`), while `DU` from an untrusted input
  maps its forward blast radius [external]; because `UD`/`DU` track explicit data flow only (`x ∈ gen_LV`),
  they miss implicit control-flow leaks (`if [secret=1]^1 then [pub:=1]^2 else [pub:=0]^3` [external])
  unless augmented with control-dependence edges [external].

## 2.2 Theoretical Properties

Context: formal small-step semantics of `WHILE` and the semantic correctness proof of Live Variables
Analysis [PPA §2.2, p. 54] (book p. 54; PDF p. 73).

### [U2a:2.2-a] Purpose of proving semantic correctness (unnumbered remark)
- Statement: §2.2 proves that Live Variables Analysis (§2.1.4) is correct; Reaching Definitions correctness
  is treated in [PPA Mini Project 2.2, p. 133] (book p. 133; PDF p. 152). Although the material may be
  skimmed on a first reading, "it is frequently when conducting the correctness proof that the final and
  subtle errors in the analysis are found and corrected!" Proving semantic correctness is not a dispensable
  development merely for theoreticians.
- Citation: [PPA §2.2, p. 54] (book p. 54; PDF p. 73)

## 2.2.1 Structural Operational Semantics

Context: small-step Structural Operational Semantics (SOS) for `WHILE`, derivation sequences, and
structural shrinking along transitions [PPA §2.2.1, p. 54] (book p. 54; PDF p. 73).

### [U2a:2.2.1-a] Choice of small-step SOS and states `State` (unnumbered definition)
- Statement: a (so-called small step) *Structural Operational Semantics* is chosen because it allows
  reasoning about intermediate stages in a program execution and dealing with non-terminating programs. A
  *state* maps variables to integers: `σ ∈ State = Var → Z`.
- Citation: [PPA §2.2.1, p. 54] (book p. 54; PDF p. 73)

### Table 2.5 — Semantics of expressions in WHILE
- Content:

```
𝒜 : AExp → (State → Z)
  𝒜⟦x⟧σ          = σ(x)
  𝒜⟦n⟧σ          = 𝒩⟦n⟧
  𝒜⟦a₁ op_a a₂⟧σ = 𝒜⟦a₁⟧σ  **op**_a  𝒜⟦a₂⟧σ

ℬ : BExp → (State → T)
  ℬ⟦not b⟧σ      = ¬ℬ⟦b⟧σ
  ℬ⟦b₁ op_b b₂⟧σ = ℬ⟦b₁⟧σ  **op**_b  ℬ⟦b₂⟧σ
  ℬ⟦a₁ op_r a₂⟧σ = 𝒜⟦a₁⟧σ  **op**_r  𝒜⟦a₂⟧σ
```

- Side conditions: bold `**op**_a, **op**_b, **op**_r` are the semantic counterparts of syntactic
  `op_a, op_b, op_r`, and `𝒩 : Num → Z` gives the semantics of numerals. Table 2.5 omits clauses for
  `true` and `false` from §1.2's `BExp` grammar (`[Source Erratum]`, finding F-U2a-06).
- Citation: [PPA Table 2.5, p. 55] (book p. 55; PDF p. 74)

### [U2a:2.2.1-b] Configurations, transitions, and no-errors assumption (unnumbered definition)
- Statement: a *configuration* is either a pair `⟨S, σ⟩` or a state `σ` (a *terminal configuration*).
  One-step *transitions* take the form `⟨S, σ⟩ → σ'` (execution terminates after one step in state `σ'`) or
  `⟨S, σ⟩ → ⟨S', σ'⟩` (`S'` is the rest of the program and `σ'` the updated state).
- Side conditions: "For simplicity we have assumed that no errors can occur; this means that division by 0
  will have to produce an integer for example. One can modify the definition so as to allow errors but this
  will complicate the correctness proof to be performed below" (`BKL-001`).
- Citation: [PPA §2.2.1, p. 55] (book p. 55; PDF p. 74)

### [U2a:2.2.1-c] Expression values depend only on free variables (unnumbered property)
- Statement:
  - if `∀x ∈ FV(a) : σ₁(x) = σ₂(x)` then `𝒜⟦a⟧σ₁ = 𝒜⟦a⟧σ₂`;
  - if `∀x ∈ FV(b) : σ₁(x) = σ₂(x)` then `ℬ⟦b⟧σ₁ = ℬ⟦b⟧σ₂`.
  Proved by structural induction on expressions (or mathematical induction on their size), citing
  [PPA Appendix B, p. 405] (book p. 405; PDF p. 421).
- Citation: [PPA §2.2.1, p. 55] (book p. 55; PDF p. 74); induction remark on
  [PPA §2.2.1, p. 56] (book p. 56; PDF p. 75)

### Table 2.6 — The Structural Operational Semantics of WHILE
- Content:

```
[ass]   ⟨[x := a]^ℓ, σ⟩ → σ[x ↦ 𝒜⟦a⟧σ]
[skip]  ⟨[skip]^ℓ, σ⟩ → σ

            ⟨S₁, σ⟩ → ⟨S₁', σ'⟩
[seq₁]  ───────────────────────────
         ⟨S₁; S₂, σ⟩ → ⟨S₁'; S₂, σ'⟩

              ⟨S₁, σ⟩ → σ'
[seq₂]  ─────────────────────────
         ⟨S₁; S₂, σ⟩ → ⟨S₂, σ'⟩

[if₁]   ⟨if [b]^ℓ then S₁ else S₂, σ⟩ → ⟨S₁, σ⟩                  if ℬ⟦b⟧σ = true
[if₂]   ⟨if [b]^ℓ then S₁ else S₂, σ⟩ → ⟨S₂, σ⟩                  if ℬ⟦b⟧σ = false
[wh₁]   ⟨while [b]^ℓ do S, σ⟩ → ⟨(S; while [b]^ℓ do S), σ⟩       if ℬ⟦b⟧σ = true
[wh₂]   ⟨while [b]^ℓ do S, σ⟩ → σ                                if ℬ⟦b⟧σ = false
```

- Side conditions: state update is `(σ[x ↦ 𝒜⟦a⟧σ])y = 𝒜⟦a⟧σ` if `x = y`, and `σ(y)` otherwise. `[seq₁]`
  applies when `S₁` does not finish in one step; `[seq₂]` when `S₁` terminates in one step; `[wh₁]` unrolls
  the loop once when `b` evaluates to `true`, and `[wh₂]` terminates when `b` evaluates to `false`
  [PPA §2.2.1, p. 57] (book p. 57; PDF p. 76).
- Citation: [PPA Table 2.6, p. 56] (book p. 56; PDF p. 75)

### [U2a:2.2.1-d] Derivation sequences (unnumbered definition)
- Statement: a *derivation sequence* for `S₁` and `σ₁` is either:
  - *finite*: `⟨S₁, σ₁⟩, ···, ⟨S_n, σ_n⟩, σ_{n+1}` with `⟨S_i, σ_i⟩ → ⟨S_{i+1}, σ_{i+1}⟩` for
    `i = 1, ···, n-1` and `⟨S_n, σ_n⟩ → σ_{n+1}` (a terminating computation); or
  - *infinite*: `⟨S₁, σ₁⟩, ···, ⟨S_i, σ_i⟩, ···` with `⟨S_i, σ_i⟩ → ⟨S_{i+1}, σ_{i+1}⟩` for all `i ≥ 1`
    (a looping computation).
- Citation: [PPA §2.2.1, p. 57] (book p. 57; PDF p. 76)

### Example 2.13 — Execution of the factorial program
- Statement: for the factorial program `[y:=x]^1; [z:=1]^2; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6`
  of [PPA Example 1.1, p. 4] (book p. 4; PDF p. 24), writing `σ_{n_x n_y n_z}` for `{x ↦ n_x, y ↦ n_y, z ↦ n_z}`:

```
   ⟨[y:=x]^1; [z:=1]^2; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6, σ₃₀₀⟩
→  ⟨[z:=1]^2; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6, σ₃₃₀⟩
→  ⟨while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6, σ₃₃₁⟩
→  ⟨[z:=z*y]^4; [y:=y-1]^5; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6, σ₃₃₁⟩
→  ⟨[y:=y-1]^5; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6, σ₃₃₃⟩
→  ⟨while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6, σ₃₂₃⟩
→  ⟨[z:=z*y]^4; [y:=y-1]^5; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6, σ₃₂₃⟩
→  ⟨[y:=y-1]^5; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6, σ₃₂₆⟩
→  ⟨while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6, σ₃₁₆⟩
→  ⟨[y:=0]^6, σ₃₁₆⟩
→  σ₃₀₆
```

  "Note that labels have no impact on the semantics: they are merely carried along and never inspected." ■
- Citation: [PPA Example 2.13, p. 57] (book p. 57; PDF p. 76)

### Lemma 2.14 — Structural monotonicity of transitions
- Statement:
  - (i) If `⟨S, σ⟩ → σ'` then `final(S) = {init(S)}`.
  - (ii) If `⟨S, σ⟩ → ⟨S', σ'⟩` then `final(S) ⊇ final(S')`.
  - (iii) If `⟨S, σ⟩ → ⟨S', σ'⟩` then `flow(S) ⊇ flow(S')`.
  - (iv) If `⟨S, σ⟩ → ⟨S', σ'⟩` then `blocks(S) ⊇ blocks(S')` and if `S` is label consistent then so is
    `S'`. ■
- Proof (summary): each part is proved by induction on the shape of the inference tree establishing the
  transition ([PPA Appendix B, p. 405] (book p. 405; PDF p. 421)). Part (i) checks the three non-vacuous
  terminal axioms `[ass]`, `[skip]`, `[wh₂]`. Part (ii) checks the five non-terminal clauses `[seq₁]`,
  `[seq₂]`, `[if₁]`, `[if₂]`, `[wh₁]`. Part (iii) checks the same five cases, using the induction hypothesis
  and (ii) in `[seq₁]` and showing `flow(S; while [b]^ℓ do S) = flow(while [b]^ℓ do S)` in the loop
  unrolling case (misprinted as "The case `[wh₂]`" on p. 59; finding F-U2a-07). Part (iv) is omitted as
  similar to (iii). ■
- Citation: [PPA Lemma 2.14, p. 58] (book p. 58; PDF p. 77); cases (ii)–(iv) on
  [PPA Lemma 2.14, p. 59] (book p. 59; PDF p. 78)

### Findings (2.2.1)
- F-U2a-06 (`[Source Erratum]`): Table 2.5 omits the boolean literal clauses `ℬ⟦true⟧σ = true` and
  `ℬ⟦false⟧σ = false`, although `BExp` includes `true` and `false` in §1.2 and §2.1 uses `[true]^{ℓ'}`.
  Recorded as printed. [PPA Table 2.5, p. 55] (book p. 55; PDF p. 74)
- F-U2a-07: on p. 59 the last case of the proof of Lemma 2.14(iii) is headed "The case `[wh₂]`" while
  proving the unrolling transition `ℬ⟦b⟧σ = true` of `[wh₁]`; p. 58 prose also says the sets "will
  decrease" where `⊇` means non-increasing, and p. 55/57 print "whose definition are given" and "boolean
  expressions evaluates". Recorded as printed.
  [PPA Lemma 2.14, p. 59] (book p. 59; PDF p. 78); [PPA §2.2.1, p. 58] (book p. 58; PDF p. 77)

### Projections (2.2.1)
- cs_theory: small-step SOS represents intermediate continuations explicitly as residual syntax `S'` whose
  control-flow and block sets shrink monotonically (`⊇`, Lemma 2.14), enabling subject-reduction-style
  [external] invariance proofs over both finite and infinite executions.
- swe_architecture: keeping labels semantically passive (carried along and never inspected by Table 2.6)
  decouples instrumentation identities from runtime behaviour; totalising `State = Var → Z` and arithmetic
  (`BKL-001`) simplifies metatheory at the cost of hiding runtime traps and undefined behaviour [external].
- practical_debugging: use small-step traces like Example 2.13 as executable reference oracles when testing
  transfer functions; note that loop unrolling `[wh₁]` duplicates syntax (`S; while [b]^ℓ do S`) while
  preserving `flow`, `blocks`, and `label consistency` (Lemma 2.14(iii)–(iv)), whereas unique labelling
  would *not* be preserved across unrolling [derived]!
- cyber: Lemma 2.14(iv) explains why Chapter 2 weakens Chapter 1's "distinct labels" (`BKL-028`) to *label
  consistency*: unrolling a loop duplicates `[B]^ℓ` with identical `B`, preserving label consistency; meanwhile
  Table 2.5's error-free assumption (`x / 0 ∈ Z`, `BKL-001`) means `WHILE` soundness proofs do not guard
  against panic, trap, or arithmetic-overflow side effects [external].

## 2.2.2 Correctness of Live Variables Analysis

Context: relaxing `LV^=` to the constraint system `LV^⊆`, proving step-preservation of `LV^⊆` solutions and
lockstep preservation of state equivalence `∼_V` [PPA §2.2.2, p. 60] (book p. 60; PDF p. 79).

### [U2a:2.2.2-a] Equation system `LV^=(S⋆)`, constraint system `LV^⊆(S⋆)`, and `⊨` (unnumbered definition)
- Statement: writing `LV^=(S⋆)` for §2.1.4's equation system on a label consistent program `S⋆` (with
  isolated exits), the book modifies `LV^=(S⋆)` into the *constraint system* `LV^⊆(S⋆)` (of the form of
  §1.3.2 [PPA §1.3.2, p. 9] (book p. 9; PDF p. 29)):

```
LV_exit(ℓ)  ⊇ ∅                                         if ℓ ∈ final(S⋆)
              ⋃{LV_entry(ℓ') | (ℓ', ℓ) ∈ flow^R(S⋆)}   otherwise

LV_entry(ℓ) ⊇ (LV_exit(ℓ) \ kill_LV(B^ℓ)) ∪ gen_LV(B^ℓ)
              where B^ℓ ∈ blocks(S⋆)
```

  Rationale: the correctness proof uses the *same* solution `live` (`live_entry, live_exit : Lab⋆ → 𝒫(Var⋆)`)
  for all statements derived from `S⋆`, which is possible for `LV^⊆(S⋆)` and not for `LV^=(S⋆)`. We write
  `live ⊨ LV^=(S)` when `live` satisfies the equations and `live ⊨ LV^⊆(S)` when `live` satisfies the
  constraints (printed on p. 60 with `LV^⊆(S⋆)` at the end of the sentence, finding F-U2a-08).
- Citation: [PPA §2.2.2, p. 60] (book p. 60; PDF p. 79)

### Lemma 2.15 — Equations versus constraints for Live Variables
- Statement: consider a label consistent program `S⋆`. If `live ⊨ LV^=(S⋆)` then `live ⊨ LV^⊆(S⋆)`. The
  least solution of `LV^=(S⋆)` coincides with the least solution of `LV^⊆(S⋆)`. ■
- Proof (summary): the first claim holds because "`⊇`" includes "`=`". For the second, construct `F^S_LV`
  such that `live ⊨ LV^⊆(S)` iff `live ⊒ F^S_LV(live)` and `live ⊨ LV^=(S)` iff `live = F^S_LV(live)`. By
  Tarski's Fixed Point Theorem ([PPA Proposition A.10, p. 402] (book p. 402; PDF p. 418)), `F^S_LV` has a
  least fixed point `lfp(F^S_LV) = ⨅{live | live ⊒ F^S_LV(live)} = ⨅{live | live = F^S_LV(live)}`, and
  `lfp(F^S_LV) = F^S_LV(lfp(F^S_LV))` as well as `lfp(F^S_LV) ⊒ F^S_LV(lfp(F^S_LV))` (implicitly using
  monotonicity of `F^S_LV` on the complete function-space lattice; finding F-U2a-08). ■
- Citation: [PPA Lemma 2.15, p. 60] (book p. 60; PDF p. 79); Tarski step on
  [PPA Lemma 2.15, p. 61] (book p. 61; PDF p. 80)

### Figure 2.4 — Preservation of analysis result
- Content: top row `⟨S, σ₁⟩ → ⟨S', σ₁'⟩ → ··· → ⟨S'', σ₁''⟩ → σ₁'''`; under each of the three non-terminal
  configurations stands `live`, linked by a vertical double-headed arrow labelled `⊨ LV^⊆` (nothing under
  terminal `σ₁'''`). Illustrates Corollary 2.17 for finite computations.
- Citation: [PPA Figure 2.4, p. 61] (book p. 61; PDF p. 80)

### Lemma 2.16 — Sub-statement preservation of `LV^⊆`
- Statement: if `live ⊨ LV^⊆(S₁)` (with `S₁` being label consistent) and `flow(S₁) ⊇ flow(S₂)` and
  `blocks(S₁) ⊇ blocks(S₂)` then `live ⊨ LV^⊆(S₂)` (with `S₂` being label consistent). ■
- Proof (summary): `blocks(S₁) ⊇ blocks(S₂)` preserves label consistency from `S₁` to `S₂`, and `live`
  satisfies each constraint of `LV^⊆(S₂)` (see finding F-U2a-09 on the `final` case-split). ■
- Citation: [PPA Lemma 2.16, p. 61] (book p. 61; PDF p. 80)

### Corollary 2.17 — Step preservation of `LV^⊆`
- Statement: if `live ⊨ LV^⊆(S)` (for `S` being label consistent) and if `⟨S, σ⟩ → ⟨S', σ'⟩` then also
  `live ⊨ LV^⊆(S')`. ■
- Proof (summary): follows from Lemma 2.14 and Lemma 2.16. ■
- Citation: [PPA Corollary 2.17, p. 61] (book p. 61; PDF p. 80)

### Lemma 2.18 — Edge inclusion for `LV^⊆`
- Statement: if `live ⊨ LV^⊆(S)` (with `S` being label consistent) then for all `(ℓ, ℓ') ∈ flow(S)` we have
  `live_exit(ℓ) ⊇ live_entry(ℓ')`. ■
- Proof (summary): stated to follow immediately from the construction of `LV^⊆(S)`.
- Side conditions: `[Source Erratum]` as printed on p. 60, `LV^⊆(S)` imposes the `flow^R(S)` union only when
  `ℓ ∉ final(S)`, so Lemma 2.18 requires either `ℓ ∉ final(S)` (automatic when `S` has isolated exits) or
  §2.3's unconditional union formulation (finding F-U2a-09).
- Citation: [PPA Lemma 2.18, p. 61] (book p. 61; PDF p. 80)

### Figure 2.5 — The correctness result for `live`
- Content: two parallel finite execution rows `⟨S, σ₁⟩ → ⟨S', σ₁'⟩ → ··· → ⟨S'', σ₁''⟩ → σ₁'''` and
  `⟨S, σ₂⟩ → ⟨S', σ₂'⟩ → ··· → ⟨S'', σ₂''⟩ → σ₂'''`, joined column-wise by vertical double-headed arrows
  labelled `∼_V`, `∼_{V'}`, `∼_{V''}`, `∼_{X(ℓ)}` with legends `V = N(init(S))`, `V' = N(init(S'))`,
  `V'' = N(init(S''))`, and `ℓ ∈ final(S)`.
- Citation: [PPA Figure 2.5, p. 62] (book p. 62; PDF p. 81)

### [U2a:2.2.2-b] Correctness relation `∼_V` and abbreviations `N, X` (unnumbered definition)
- Statement: for a set `V` of live variables, the *correctness relation* is:

```
σ₁ ∼_V σ₂   iff   ∀x ∈ V : σ₁(x) = σ₂(x)
```

  expressing that `σ₁` and `σ₂` agree on all live variables (dead variables cannot affect the interesting
  parts of the result). Abbreviations: `N(ℓ) = live_entry(ℓ)` and `X(ℓ) = live_exit(ℓ)`.
- Citation: [PPA §2.2.2, p. 62] (book p. 62; PDF p. 81)

### Example 2.19 — Correctness relation on a single assignment
- Statement: for `[x:=y+z]^ℓ` with `V₁ = {y, z}` and `V₂ = {x}`, if `⟨[x:=y+z]^ℓ, σ₁⟩ → σ₁'` and
  `⟨[x:=y+z]^ℓ, σ₂⟩ → σ₂'`, then `σ₁ ∼_{V₁} σ₂` (`σ₁(y)=σ₂(y) ∧ σ₁(z)=σ₂(z)`) ensures `σ₁' ∼_{V₂} σ₂'`
  (`σ₁'(x)=σ₂'(x)`). ■
- Citation: [PPA Example 2.19, p. 62] (book p. 62; PDF p. 81)

### Lemma 2.20 — Edge transfer of state equivalence
- Statement: assume `live ⊨ LV^⊆(S)` with `S` being label consistent. Then `σ₁ ∼_{X(ℓ)} σ₂` implies
  `σ₁ ∼_{N(ℓ')} σ₂` for all `(ℓ, ℓ') ∈ flow(S)`. ■
- Proof (summary): follows directly from Lemma 2.18 and the definition of `∼_V` (inheriting Lemma 2.18's
  implicit isolated-exits / unconditional-constraint requirement; finding F-U2a-09). ■
- Citation: [PPA Lemma 2.20, p. 63] (book p. 63; PDF p. 82)

### Theorem 2.21 — Single-step correctness of Live Variables Analysis
- Statement (framed in the book): if `live ⊨ LV^⊆(S)` (with `S` being label consistent) then:
  - (i) if `⟨S, σ₁⟩ → ⟨S', σ₁'⟩` and `σ₁ ∼_{N(init(S))} σ₂` then there exists `σ₂'` such that
    `⟨S, σ₂⟩ → ⟨S', σ₂'⟩` and `σ₁' ∼_{N(init(S'))} σ₂'`, and
  - (ii) if `⟨S, σ₁⟩ → σ₁'` and `σ₁ ∼_{N(init(S))} σ₂` then there exists `σ₂'` such that `⟨S, σ₂⟩ → σ₂'`
    and `σ₁' ∼_{X(init(S))} σ₂'`
- Proof (summary): by induction on the shape of the inference tree for `⟨S, σ₁⟩ → ⟨S', σ₁'⟩` and
  `⟨S, σ₁⟩ → σ₁'`:
  - `[ass]`: `N(ℓ) ⊇ (X(ℓ) \ {x}) ∪ FV(a)` and `[U2a:2.2.1-c]` yield `𝒜⟦a⟧σ₁ = 𝒜⟦a⟧σ₂`, so
    `σ₂' = σ₂[x ↦ 𝒜⟦a⟧σ₂]` satisfies `σ₁' ∼_{X(ℓ)} σ₂'`.
  - `[skip]`: `N(ℓ) ⊇ X(ℓ)`, take `σ₂' = σ₂`.
  - `[seq₁]`: Lemma 2.16 gives `live ⊨ LV^⊆(S₁)`, then the induction hypothesis applies since
    `init(S₁; S₂) = init(S₁)` and `init(S₁'; S₂) = init(S₁')`.
  - `[seq₂]`: Lemma 2.16 and the induction hypothesis give `σ₁' ∼_{X(init(S₁))} σ₂'`; Lemma 2.14(i) gives
    `final(S₁) = {init(S₁)}`, so `(init(S₁), init(S₂)) ∈ flow(S₁; S₂)` and Lemma 2.20 yields
    `σ₁' ∼_{N(init(S₂))} σ₂'`.
  - `[if₁]`, `[if₂]`: `N(ℓ) ⊇ FV(b)` and `[U2a:2.2.1-c]` give `ℬ⟦b⟧σ₁ = ℬ⟦b⟧σ₂`, forcing the same branch;
    `N(ℓ) ⊇ X(ℓ)` and Lemma 2.20 on `(ℓ, init(S₁))` (or `(ℓ, init(S₂))`) give the target equivalence.
  - `[wh₁]`: `N(ℓ) ⊇ FV(b)` gives `ℬ⟦b⟧σ₂ = true`, so `σ₂` also unrolls; `N(ℓ) ⊇ X(ℓ)` and Lemma 2.20 on
    `(ℓ, init(S)) ∈ flow(while [b]^ℓ do S)` give `σ₁ ∼_{N(init(S))} σ₂` (see finding F-U2a-09).
  - `[wh₂]`: `N(ℓ) ⊇ FV(b)` gives `ℬ⟦b⟧σ₂ = false`, and `N(ℓ) ⊇ X(ℓ)` gives `σ₁ ∼_{X(ℓ)} σ₂`. ■
- Citation: [PPA Theorem 2.21, p. 63] (book p. 63; PDF p. 82); `[seq₂]`, `[if₁]`, `[if₂]`, `[wh₁]`, `[wh₂]`
  cases on [PPA Theorem 2.21, p. 64] (book p. 64; PDF p. 83)

### Corollary 2.22 — Multi-step correctness of Live Variables Analysis
- Statement: if `live ⊨ LV^⊆(S)` (with `S` being label consistent) then:
  - (i) if `⟨S, σ₁⟩ →* ⟨S', σ₁'⟩` and `σ₁ ∼_{N(init(S))} σ₂` then there exists `σ₂'` such that
    `⟨S, σ₂⟩ →* ⟨S', σ₂'⟩` and `σ₁' ∼_{N(init(S'))} σ₂'`, and
  - (ii) if `⟨S, σ₁⟩ →* σ₁'` and `σ₁ ∼_{N(init(S))} σ₂` then there exists `σ₂'` such that `⟨S, σ₂⟩ →* σ₂'`
    and `σ₁' ∼_{X(ℓ)} σ₂'` for some `ℓ ∈ final(S)`. ■
- Proof (summary): by induction on the length of the derivation sequence, using Theorem 2.21 (and
  Corollary 2.17 at each intermediate step [derived]). ■
- Citation: [PPA Corollary 2.22, p. 64] (book p. 64; PDF p. 83); clause (ii) and proof on
  [PPA Corollary 2.22, p. 65] (book p. 65; PDF p. 84)

### [U2a:2.2.2-c] Remark — Small-step versus big-step operational semantics (unnumbered Remark)
- Statement: printed with bold run-in heading **Remark.** Correctness of Live Variables Analysis was proved
  with respect to a small-step operational semantics; if one relies instead on a big-step (or natural)
  semantics, "it is not so obvious how to express (and prove) the correctness of looping computations: in a
  big step semantics a looping computation is modelled by the absence of an inference tree – in contrast to
  the small step semantics where it is modelled by an infinite derivation sequence." (`BKL-004`) ■
- Citation: [PPA §2.2.2, p. 65] (book p. 65; PDF p. 84)

### Findings (2.2.2)
- F-U2a-08: on p. 60 the definition of `⊨` mixes `S` and `S⋆` ("write `live ⊨ LV^⊆(S)` if `live` solves
  `LV^⊆(S⋆)`"), Lemma 2.15 invokes Proposition A.10 without explicitly stating monotonicity of `F^S_LV`,
  pp. 63–64 print italic `LV^⊆` in three places where sans-serif `LV^⊆` is used elsewhere, and `→*` in
  Corollary 2.22 is used without a local definition on pp. 54–65. Recorded as printed.
  [PPA §2.2.2, p. 60] (book p. 60; PDF p. 79); [PPA Corollary 2.22, p. 64] (book p. 64; PDF p. 83)
- F-U2a-09 (`[Source Erratum]`): on p. 60 `LV^⊆(S⋆)` defines `LV_exit(ℓ) ⊇ ∅` when `ℓ ∈ final(S⋆)` and
  applies `⋃{LV_entry(ℓ') | (ℓ', ℓ) ∈ flow^R(S⋆)}` only `otherwise`. Lemmas 2.16, 2.18, 2.20, Theorem 2.21,
  and Corollary 2.22 state only that `S` is label consistent, omitting isolated exits. [derived] Without
  isolated exits (or §2.3's unconditional `LV_exit(ℓ) ⊇ ⋃{...} ∪ ι^ℓ_E` constraint), `S = while [x>0]^1 do [x:=x-y]^2`
  has `final(S) = {1}` and `(1, 2) ∈ flow(S)`, so the least solution of p. 60's `LV^⊆(S)` has
  `live_exit(1) = ∅ ⊉ {x, y} = live_entry(2)`, refuting Lemma 2.18 and breaking Theorem 2.21(i) in case
  `[wh₁]` (`σ₁ = {x↦1, y↦0}` and `σ₂ = {x↦1, y↦5}` satisfy `σ₁ ∼_{N(1)} σ₂` since `N(1) = {x}`, yet step to
  `S' = [x:=x-y]^2; S` where `N(init(S')) = N(2) = {x, y}` and `σ₁ ≁_{N(2)} σ₂`); moreover in `[seq₁]`/`[seq₂]`
  sub-statement `S₁` can itself be a `while` loop lacking isolated exits even when top-level `S⋆` has
  isolated exits. Using §2.3's unconditional constraint `Analysis^⊑` repairs the entire proof chain without
  needing isolated exits.
  [PPA §2.2.2, p. 60] (book p. 60; PDF p. 79); [PPA Lemma 2.18, p. 61] (book p. 61; PDF p. 80);
  [PPA Theorem 2.21, p. 64] (book p. 64; PDF p. 83)

### Projections (2.2.2)
- cs_theory: relaxing equations `LV^=` to reductive constraint inclusions `LV^⊆` (`Red(F) = {x | F(x) ⊑ x}`, `U1`) preserves the least
  solution via Tarski's theorem (Lemma 2.15) while making solutions monotone under syntactic continuation
  shrinking (Corollary 2.17); Theorem 2.21 is a lockstep 2-run relational simulation [external] over `∼_V`.
- swe_architecture: test and prove static analyses against their constraint formulation `Analysis^⊑` rather
  than `Analysis^=`, using §2.3's unconditional `ι^ℓ_E` join so loop headers in sub-statements never drop
  outgoing flow constraints (`F-U2a-09`).
- practical_debugging: to Differential-Test [external] a liveness pass, run every program twice from states
  randomised on `Var⋆ \ LV_entry(init(S⋆))` and assert lockstep branch choices and equal values on `LV_exit`
  at termination (Corollary 2.22); any divergence witnesses an unsound liveness result.
- cyber: reinterpreting `V = live` as `Low` (publicly observable variables [external]) and `Var⋆ \ V` as
  `High` (secret inputs [external]) makes `σ₁ ∼_V σ₂` exact Low-indistinguishability and turns Theorem 2.21
  plus Corollary 2.22 into a termination- and timing-lockstep non-interference proof [external] where
  `N(ℓ) ⊇ FV(b)` forbids secret-dependent branching unless the guard variables are observable, and the
  p. 65 `Remark.` (`BKL-004`) explains why big-step proofs miss termination/infinite-loop channels [derived].

## 2.3 Monotone Frameworks

Context: unifying the four classical analyses of §2.1 into a language-independent lattice and
transfer-function framework [PPA §2.3, p. 65] (book p. 65; PDF p. 84).

### [U2a:2.3-a] Motivation and overall case-split equation pattern (unnumbered definition)
- Statement: similarities among the §2.1 analyses motivate an underlying framework supporting generic
  equation-solving algorithms (§2.4). Each of §§2.1.1–2.1.4 considers equations for a label consistent
  program `S⋆` of the form:

```
Analysis∘(ℓ) = ι                                       if ℓ ∈ E
               ⨆{Analysis•(ℓ') | (ℓ', ℓ) ∈ F}          otherwise

Analysis•(ℓ) = f_ℓ(Analysis∘(ℓ))
```

  where `⨆` is `⋂` or `⋃` (printed parenthetically "(and `⊔` is `∪` or `∩`)", finding F-U2a-10), `F` is
  `flow(S⋆)` or `flow^R(S⋆)`, `E` is `{init(S⋆)}` or `final(S⋆)`, `ι` specifies the initial or final
  analysis information, and `f_ℓ` is the transfer function associated with `B^ℓ ∈ blocks(S⋆)`.
- Citation: [PPA §2.3, p. 65] (book p. 65; PDF p. 84)

### [U2a:2.3-b] Forward/backward and must/may characterisation (unnumbered principle)
- Statement:
  - *Forward analyses*: `F = flow(S⋆)`, `Analysis∘` concerns entry conditions, `Analysis•` concerns exit
    conditions, and the case-split equation system presupposes isolated entries.
  - *Backward analyses*: `F = flow^R(S⋆)`, `Analysis∘` concerns exit conditions, `Analysis•` concerns entry
    conditions, and the case-split equation system presupposes isolated exits.
  - *Must analyses* (`⨆` is `⋂`): require the *greatest* sets solving the equations and detect properties
    satisfied by *all* execution paths reaching (or leaving) the entry (or exit) of a label.
  - *May analyses* (`⨆` is `⋃`): require the *least* sets solving the equations and detect properties
    satisfied by *at least one* execution path to (or from) the entry (or exit) of a label.
- Citation: [PPA §2.3, p. 66] (book p. 66; PDF p. 85)

### [U2a:2.3-c] Remark — Typology cube collapsing to a four-type square (unnumbered Remark)
- Statement: printed with bold run-in heading **Remark.** Some authors characterise Data Flow Analyses by a
  triple from `{⋂, ⋃} × {→, ←} × {↑, ↓}` (`→` forwards, `←` backwards, `↓` smallest, `↑` largest), giving
  eight types — a cube. Given the association of `⋂` with `↑` and `⋃` with `↓`, the cube collapses to a
  square of the four types `(⋂, →, ↑)` (`AE`), `(⋃, →, ↓)` (`RD`), `(⋂, ←, ↑)` (`VB`), and `(⋃, ←, ↓)`
  (`LV`). ■
- Citation: [PPA §2.3, p. 66] (book p. 66; PDF p. 85)

### [U2a:2.3-d] Unconditional `ι^ℓ_E` reformulation and transition-system scope (unnumbered definition)
- Statement: to avoid assuming isolated entries for forward analyses and isolated exits for backward
  analyses, the equations are reformulated as:

```
Analysis∘(ℓ) = ⨆{Analysis•(ℓ') | (ℓ', ℓ) ∈ F} ⊔ ι^ℓ_E
               where ι^ℓ_E = ι   if ℓ ∈ E
                             ⊥   if ℓ ∉ E

Analysis•(ℓ) = f_ℓ(Analysis∘(ℓ))
```

  where `⊥` satisfies `l ⊔ ⊥ = l` ("hence `⊥` is not really there"). Nothing in §2.3 depends on elementary
  blocks or language constructs, though the techniques do not directly apply to languages with procedures
  (addressed in §2.5 [PPA §2.5, p. 82] (book p. 82; PDF p. 101)). A program is viewed as a *transition
  system* whose nodes represent blocks with associated transfer functions acting on the "input" state
  (entry state for forward analyses, exit state for backward analyses).
- Citation: [PPA §2.3, p. 66] (book p. 66; PDF p. 85); procedures scope and transition-system view on
  [PPA §2.3, p. 67] (book p. 67; PDF p. 86)

## 2.3.1 Basic Definitions

Context: formal definitions of property spaces, ACC, transfer-function spaces, Monotone Frameworks,
Distributive Frameworks, instances, and `Analysis^=` / `Analysis^⊑`
[PPA §2.3.1, p. 67] (book p. 67; PDF p. 86).

### [U2a:2.3.1-a] Property space, combination operator, complete lattice, and ACC (unnumbered definition)
- Statement: the *property space* `L` represents data flow information with *combination operator*
  `⨆ : 𝒫(L) → L`, binary join `l₁ ⊔ l₂ = ⨆{l₁, l₂}`, and least element `⊥ = ⨆∅`. Customarily `L` is a
  *complete lattice* `(L, ⊑)` in which every subset `Y` has a least upper bound `⨆Y`
  ([PPA Appendix A, p. 393] (book p. 393; PDF p. 409)); for implementation `L` is required to satisfy the
  *Ascending Chain Condition* (ACC): every ascending chain `l₁ ⊑ l₂ ⊑ l₃ ⊑ ···` eventually stabilises
  (`∃n : l_n = l_{n+1} = ···`).
- Citation: [PPA §2.3.1, p. 67] (book p. 67; PDF p. 86)

### Example 2.23 — Property space for Reaching Definitions
- Statement: `L = 𝒫(Var⋆ × Lab⋆^?)` partially ordered by `⊆`, with `⨆Y = ⋃Y`, `l₁ ⊔ l₂ = l₁ ∪ l₂`, and
  `⊥ = ∅`. ACC (`l₁ ⊆ l₂ ⊆ ··· ⇒ ∃n : l_n = l_{n+1} = ···`) holds because `Var⋆ × Lab⋆^?` is finite
  (unlike `Var × Lab`). ■
- Citation: [PPA Example 2.23, p. 67] (book p. 67; PDF p. 86)

### Example 2.24 — Property space for Available Expressions
- Statement: `L = 𝒫(AExp⋆)` partially ordered by superset inclusion (`⊑` is `⊇`), with `⨆Y = ⋂Y`,
  `l₁ ⊔ l₂ = l₁ ∩ l₂`, and `⊥ = AExp⋆`. ACC (`l₁ ⊇ l₂ ⊇ ··· ⇒ ∃n : l_n = l_{n+1} = ···`) holds because
  `AExp⋆` is finite (unlike `AExp`). ■
- Citation: [PPA Example 2.24, p. 67] (book p. 67; PDF p. 86)

### [U2a:2.3.1-b] Remark — Join semi-lattice with unit and ACC (unnumbered Remark)
- Statement: printed with bold run-in heading **Remark.** A *join semi-lattice* is a non-empty set `L` with
  an idempotent, commutative, associative binary operation `⊔` (`l ⊔ l = l`, `l₁ ⊔ l₂ = l₂ ⊔ l₁`,
  `(l₁ ⊔ l₂) ⊔ l₃ = l₁ ⊔ (l₂ ⊔ l₃)`, meaning path-combination order does not matter), inducing partial
  order `l₁ ⊑ l₂ iff l₁ ⊔ l₂ = l₂` with least element *unit* `⊥` (`⊥ ⊔ l = l`). By
  [PPA Lemma A.8, p. 401] (book p. 401; PDF p. 417), "join semi-lattice with a unit satisfying ACC" is
  equivalent to "complete lattice satisfying ACC". ■
- Citation: [PPA §2.3.1, p. 67] (book p. 67; PDF p. 86); unit and Lemma A.8 equivalence on
  [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87)

### [U2a:2.3.1-c] Descending Chain Condition and `⨅` duality (unnumbered remark)
- Statement: formulations expressed in terms of property spaces satisfying a *Descending Chain Condition*
  and combination operator `⨅` give the same notion of Monotone Framework by lattice duality (see
  [PPA Chapter 4 Concluding Remarks, p. 270] (book p. 270; PDF p. 287)).
- Citation: [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87)

### [U2a:2.3.1-d] Transfer functions and function space `𝓕` (unnumbered definition)
- Statement: each transfer function `f_ℓ : L → L` (`ℓ ∈ Lab⋆`) must be *monotone* (`l ⊑ l' ⇒ f_ℓ(l) ⊑ f_ℓ(l')`).
  The transfer-function space `𝓕` is a set of monotone functions over `L` such that:
  1. `𝓕` contains all transfer functions `f_ℓ` in question;
  2. `𝓕` contains the identity function `id` (natural because of `skip`); and
  3. `𝓕` is closed under composition of functions (natural because of statement sequencing).
  Smaller `𝓕` than the full monotone function space can admit compact representations. Edge-associated
  transfer functions (used in some formulations) can be obtained via the approach of
  [PPA Exercise 2.11, p. 137] (book p. 137; PDF p. 156).
- Citation: [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87)

### [U2a:2.3.1-e] Monotone Framework `(L, 𝓕)` (unnumbered definition)
- Statement: a *Monotone Framework* consists of a complete lattice `L` satisfying the Ascending Chain
  Condition (with lub operator `⨆`) and a set `𝓕` of monotone functions `L → L` containing `id` and closed
  under function composition.
- Side conditions: `𝓕` is *not* demanded to be a complete lattice or even a partially ordered set (although
  the set of all monotone functions `L → L` is one; [PPA Appendix A, p. 393] (book p. 393; PDF p. 409)).
- Citation: [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87); non-demand on `𝓕` on
  [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88)

### [U2a:2.3.1-f] Distributive Framework (unnumbered definition)
- Statement: a *Distributive Framework* is a Monotone Framework in which additionally every `f ∈ 𝓕` is
  *distributive*:

```
f(l₁ ⊔ l₂) = f(l₁) ⊔ f(l₂)
```

- Side conditions: since `f(l₁ ⊔ l₂) ⊒ f(l₁) ⊔ f(l₂)` already follows from monotonicity, the only additional
  demand is `f(l₁ ⊔ l₂) ⊑ f(l₁) ⊔ f(l₂)`. Notice distributivity here means binary join preservation
  (`additive` in Appendix A; see `BKL-022`), not preservation of `⨆∅ = ⊥` (strictness). "When this condition
  is fulfilled it is sometimes possible to get more efficient algorithms."
- Citation: [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88)

### [U2a:2.3.1-g] Instance `Analysis`, equation system `Analysis^=`, and constraint system `Analysis^⊑` (unnumbered definition)
- Statement: an *instance* `Analysis` (sans-serif) of a Monotone (or Distributive) Framework is a six-tuple
  `(L, 𝓕, F, E, ι, f_·)` consisting of:
  - the complete lattice `L` and function space `𝓕` of the framework;
  - a finite *flow* `F` (typically `flow(S⋆)` or `flow^R(S⋆)`);
  - a finite set of *extremal labels* `E` (typically `{init(S⋆)}` or `final(S⋆)`);
  - an *extremal value* `ι ∈ L` for the extremal labels; and
  - a mapping `f_·` from the labels `Lab⋆` of `F` and `E` to transfer functions in `𝓕`.
  It induces the *set of equations* `Analysis^=` and the *set of constraints* `Analysis^⊑` (printed with
  superscript `⊑` on sans-serif `Analysis`):

```
Analysis^=:
  Analysis∘(ℓ) = ⨆{Analysis•(ℓ') | (ℓ', ℓ) ∈ F} ⊔ ι^ℓ_E    where ι^ℓ_E = ι if ℓ ∈ E, ⊥ if ℓ ∉ E
  Analysis•(ℓ) = f_ℓ(Analysis∘(ℓ))

Analysis^⊑:
  Analysis∘(ℓ) ⊒ ⨆{Analysis•(ℓ') | (ℓ', ℓ) ∈ F} ⊔ ι^ℓ_E    where ι^ℓ_E = ι if ℓ ∈ E, ⊥ if ℓ ∉ E
  Analysis•(ℓ) ⊒ f_ℓ(Analysis∘(ℓ))
```

- Citation: [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88)

### Projections (2.3–2.3.1)
- cs_theory: orienting `⊑` as information growth (`⊆` for may, `⊇` for must) collapses the 8-corner typology
  cube to a 4-cell square where *every* analysis computes a least fixed point from `⊥_L`; ACC + binary
  join + unit `⊥_L` suffices for complete-lattice structure (Lemma A.8), and binary distributivity adds
  `f(l₁ ⊔ l₂) ⊑ f(l₁) ⊔ f(l₂)` without requiring `f(⊥_L) = ⊥_L`.
- swe_architecture: separate the reusable *Framework* `(L, 𝓕)` (domain operations + compact transfer
  representation) from the per-CFG *Instance* `(L, 𝓕, F, E, ι, f_·)` plugged into a single Template-Method
  [external] solver; always implement `Analysis∘(ℓ)` with `⊔ ι^ℓ_E` rather than case-splitting on `ℓ ∈ E`
  so cyclic entry/exit graphs work out of the box.
- practical_debugging: keep `ι` (boundary knowledge on `E`) strictly separate from `⊥_L` (unreached identity
  element elsewhere); non-termination in an `Analysis^=` solver indicates either a transfer rule violating
  monotonicity (`BKL-014`) or an un-finitised carrier violating ACC (`Var` instead of `Var⋆`, `BKL-013`).
- cyber: any custom security lattice (multi-level taint, privilege masks, sanitisation state [external])
  inherits the Monotone Framework termination and least-solution guarantees (Lemma 2.29, Proposition A.10)
  when its transfer rules are monotone (`BKL-014`: ad-hoc negation or "if-not-tainted declassify" rules
  break monotonicity!) and its carrier satisfies ACC (or uses Chapter 4 widening [external to Chapter 2]).

## 2.3.2 The Examples Revisited

Context: instantiating all four classical §2.1 analyses as Distributive Frameworks in Figure 2.6 and
proving Lemma 2.25 [PPA §2.3.2, p. 70] (book p. 70; PDF p. 89).

### Figure 2.6 — Instances for the four classical analyses
- Content:

| | Available Expressions | Reaching Definitions | Very Busy Expressions | Live Variables |
| :--- | :--- | :--- | :--- | :--- |
| `L` | `𝒫(AExp⋆)` | `𝒫(Var⋆ × Lab⋆^?)` | `𝒫(AExp⋆)` | `𝒫(Var⋆)` |
| `⊑` | `⊇` | `⊆` | `⊇` | `⊆` |
| `⨆` | `⋂` | `⋃` | `⋂` | `⋃` |
| `⊥` | `AExp⋆` | `∅` | `AExp⋆` | `∅` |
| `ι` | `∅` | `{(x, ?) \| x ∈ FV(S⋆)}` | `∅` | `∅` |
| `E` | `{init(S⋆)}` | `{init(S⋆)}` | `final(S⋆)` | `final(S⋆)` |
| `F` | `flow(S⋆)` | `flow(S⋆)` | `flow^R(S⋆)` | `flow^R(S⋆)` |
| `𝓕` | `{f : L → L \| ∃l_k, l_g : f(l) = (l \ l_k) ∪ l_g}` (all four columns) | | | |
| `f_ℓ` | `f_ℓ(l) = (l \ kill([B]^ℓ)) ∪ gen([B]^ℓ)` where `[B]^ℓ ∈ blocks(S⋆)` (all four columns) | | | |

- Citation: [PPA Figure 2.6, p. 70] (book p. 70; PDF p. 89)

### [U2a:2.3.2-a] Discussion of Figure 2.6 and lack of universal rule for `ι` (unnumbered remark)
- Statement: for a label consistent `S⋆`, `⊑` is `⊆` where §2.1 used `⋃` and `⊇` where §2.1 used `⋂`; ACC
  is enforced by restricting to the finite sets `AExp⋆, Lab⋆, Var⋆` of `S⋆`. For the extremal value `ι`,
  "there seems to be no general pattern concerning how to define it: it is not always `⊤_L` (nor is it
  always `⊥_L`)" — [derived] `ι = ∅` is `⊤_L` for `AE` and `VB`, `⊥_L` for `LV`, and strictly between `⊥_L`
  and `⊤_L` for `RD` (whenever `FV(S⋆) ≠ ∅` and `Lab⋆ ≠ ∅`).
- Citation: [PPA §2.3.2, p. 70] (book p. 70; PDF p. 89)

### Lemma 2.25 — Monotonicity and distributivity of Figure 2.6 analyses
- Statement: each of the four data flow analyses in Figure 2.6 is a Monotone Framework as well as a
  Distributive Framework. ■
- Proof (summary): for `f(l) = (l \ l_k) ∪ l_g`:
  - *Monotone*: `l ⊑ l' ⇒ (l \ l_k) ⊑ (l' \ l_k) ⇒ ((l \ l_k) ∪ l_g) ⊑ ((l' \ l_k) ∪ l_g)` whether `⊑` is
    `⊆` or `⊇`.
  - *Identity*: take `l_k = l_g = ∅`.
  - *Composition*: for `f(l) = (l \ l_k) ∪ l_g` and `f'(l) = (l \ l_k') ∪ l_g'`,
    `(f ∘ f')(l) = (l \ (l_k' ∪ l_k)) ∪ ((l_g' \ l_k) ∪ l_g)`, preserving the form with
    `l_k'' = l_k' ∪ l_k` and `l_g'' = (l_g' \ l_k) ∪ l_g`.
  - *Distributive*: `f(l ⊔ l') = ((l ⊔ l') \ l_k) ∪ l_g = ((l \ l_k) ⊔ (l' \ l_k)) ∪ l_g = f(l) ⊔ f(l')`
    whether `⊔` is `∪` or `∩`. ■
- Side conditions: the text notes after the proof that the frameworks were made *dependent upon the actual
  program* `S⋆` to enforce ACC; this kill/gen family is named a *Bit Vector Framework* only later in
  [PPA Exercise 2.9, p. 137] (book p. 137; PDF p. 156).
- Citation: [PPA Lemma 2.25, p. 71] (book p. 71; PDF p. 90); program-dependence note on
  [PPA §2.3.2, p. 71] (book p. 71; PDF p. 90)

### Example 2.26 — Available Expressions as a Monotone Framework instance
- Statement: for `[x:=a+b]^1; [y:=a*b]^2; while [y>a+b]^3 do ([a:=a+1]^4; [x:=a+b]^5)` of Examples 2.4 and
  2.5, `L = (𝒫({a+b, a*b, a+1}), ⊇)` with least element `{a+b, a*b, a+1}`, `F = {(1,2),(2,3),(3,4),(4,5),(5,3)}`,
  `E = {1}`, `ι = ∅`, and for `Y ⊆ {a+b, a*b, a+1}`: `f_1^AE(Y) = Y ∪ {a+b}`, `f_2^AE(Y) = Y ∪ {a*b}`,
  `f_3^AE(Y) = Y ∪ {a+b}`, `f_4^AE(Y) = Y \ {a+b, a*b, a+1}`, `f_5^AE(Y) = Y ∪ {a+b}`. ■
- Citation: [PPA Example 2.26, p. 71] (book p. 71; PDF p. 90); transfer functions `f_1^AE..f_5^AE` on
  [PPA Example 2.26, p. 72] (book p. 72; PDF p. 91)

### Projections (2.3.2)
- cs_theory: kill/gen functions `f(l) = (l \ l_k) ∪ l_g` form a composition-closed finite monoid [external]
  that distributes over both `∪` and `∩` simultaneously because set difference and union distribute over
  arbitrary intersections as well as unions.
- swe_architecture: pack `L` into machine bitsets [external] with `(l & ~kill) | gen` and fold straight-line
  basic blocks [external] into a single `(kill, gen)` summary via Lemma 2.25's composition law
  `l_k'' = l_k' ∪ l_k`, `l_g'' = (l_g' \ l_k) ∪ l_g` before running worklist iteration.
- practical_debugging: pay attention to operand order in composition `(f ∘ f')` (`f'` executes *first*, then
  `f`): swapping `l_g' \ l_k` for `l_g \ l_k'` kills facts generated by the second statement instead of the
  first!
- cyber: bitset taint/sanitisation summaries (`(taint \ sanitised) ∪ sourced` [external]) inherit exact
  path-insensitive `MFP = MOP` precision on reachable nodes (Lemma 2.25 + Lemma 2.32) *provided* transfer
  functions remain independent of cross-variable correlations; adding conditional rules ("taint `z` if both
  `x` and `y` are tainted" [external]) exits Figure 2.6's `𝓕` and breaks distributivity [derived].

## 2.3.3 A Non-distributive Example

Context: Constant Propagation (`CP`) over `State^_CP`, demonstrating a Monotone Framework that fails binary
distributivity [PPA §2.3.3, p. 72] (book p. 72; PDF p. 91).

### [U2a:2.3.3-a] Constant Propagation specification and lattice `State^_CP` (unnumbered definition)
- Statement: Constant Propagation Analysis determines "For each program point, whether or not a variable has
  a constant value whenever execution reaches that point" (basis for *Constant Folding*). For program `S⋆`,
  the complete lattice is:

```
State^_CP = ((Var⋆ → Z^⊤)_⊥, ⊑, ⊔, ⊓, ⊥, λx.⊤)
```

  where `Z^⊤ = Z ∪ {⊤}` is ordered by `∀z ∈ Z^⊤ : z ⊑ ⊤` and `∀z₁, z₂ ∈ Z : (z₁ ⊑ z₂) ⇔ (z₁ = z₂)` (`⊤`
  means non-constant; `z ∈ Z` means that constant). An element `σ̂ ∈ Var⋆ → Z^⊤` is a *property state*; least
  element `⊥` ("no information available") is adjoined below `Var⋆ → Z^⊤`:
  - `∀σ̂ ∈ (Var⋆ → Z^⊤)_⊥ : ⊥ ⊑ σ̂`, and `∀σ̂₁, σ̂₂ ∈ Var⋆ → Z^⊤ : σ̂₁ ⊑ σ̂₂ iff ∀x : σ̂₁(x) ⊑ σ̂₂(x)`;
  - `∀σ̂ ∈ (Var⋆ → Z^⊤)_⊥ : σ̂ ⊔ ⊥ = σ̂ = ⊥ ⊔ σ̂`, and `∀σ̂₁, σ̂₂ ∈ Var⋆ → Z^⊤ : ∀x : (σ̂₁ ⊔ σ̂₂)(x) = σ̂₁(x) ⊔ σ̂₂(x)`.
- Citation: [PPA §2.3.3, p. 72] (book p. 72; PDF p. 91); binary lub on
  [PPA §2.3.3, p. 73] (book p. 73; PDF p. 92)

### Table 2.7 — Constant Propagation Analysis
- Content:

```
𝒜_CP : AExp → (State^_CP → Z^⊤_⊥)
  𝒜_CP⟦x⟧σ̂          = ⊥                       if σ̂ = ⊥
                      σ̂(x)                    otherwise
  𝒜_CP⟦n⟧σ̂          = ⊥                       if σ̂ = ⊥
                      n                       otherwise
  𝒜_CP⟦a₁ op_a a₂⟧σ̂ = 𝒜_CP⟦a₁⟧σ̂  op^_a  𝒜_CP⟦a₂⟧σ̂

transfer functions: f_ℓ^CP
  [x := a]^ℓ :  f_ℓ^CP(σ̂) = ⊥                 if σ̂ = ⊥
                            σ̂[x ↦ 𝒜_CP⟦a⟧σ̂]  otherwise
  [skip]^ℓ   :  f_ℓ^CP(σ̂) = σ̂
  [b]^ℓ      :  f_ℓ^CP(σ̂) = σ̂
```

- Side conditions: the numeral clause prints italic `n` rather than `𝒩⟦n⟧` (finding F-U2a-11).
- Citation: [PPA Table 2.7, p. 73] (book p. 73; PDF p. 92)

### [U2a:2.3.3-b] `𝓕_CP`, Constant Propagation instance, and lifted operators `op^_a` (unnumbered definition)
- Statement: in contrast to Figure 2.6, `𝓕_CP = {f | f is a monotone function on State^_CP}` (verifying
  `(State^_CP, 𝓕_CP)` is a Monotone Framework is left to [PPA Exercise 2.8, p. 136] (book p. 136; PDF p. 155)).
  Instance: forward `F = flow(S⋆)`, `E = {init(S⋆)}`, extremal value `ι_CP = λx.⊤`, and `f_·^CP` from
  Table 2.7. Operations on `Z` lift to `Z^⊤_⊥ = Z ∪ {⊥, ⊤}` by:
  - `z₁ op^_a z₂ = z₁ **op**_a z₂` if `z₁, z₂ ∈ Z`;
  - `z₁ op^_a z₂ = ⊥` if `z₁ = ⊥` or `z₂ = ⊥`; and
  - `z₁ op^_a z₂ = ⊤` otherwise.
- Side conditions: [derived] `Z^⊤_⊥` is only a carrier set for `𝒜_CP` results — if a variable is assigned
  when `σ̂ ≠ ⊥`, `σ̂(y) ∈ Z^⊤` for all `y`, so `𝒜_CP⟦a⟧σ̂` never evaluates to `⊥`, keeping `σ̂[x ↦ 𝒜_CP⟦a⟧σ̂]`
  inside `Var⋆ → Z^⊤`.
- Citation: [PPA §2.3.3, p. 73] (book p. 73; PDF p. 92)

### Lemma 2.27 — Constant Propagation is monotone and non-distributive
- Statement: Constant Propagation is a Monotone Framework that is *not* a Distributive Framework. ■
- Proof (summary): Monotone Framework axioms are left to [PPA Exercise 2.8, p. 136] (book p. 136; PDF p. 155).
  Non-distributivity counterexample: for `[y:=x*x]^ℓ` with `σ̂₁(x) = 1` and `σ̂₂(x) = -1`, `(σ̂₁ ⊔ σ̂₂)(x) = ⊤`,
  so `f_ℓ^CP(σ̂₁ ⊔ σ̂₂)(y) = ⊤` (failing to record `y = 1`), whereas `f_ℓ^CP(σ̂₁)(y) = 1` and
  `f_ℓ^CP(σ̂₂)(y) = 1`, so `(f_ℓ^CP(σ̂₁) ⊔ f_ℓ^CP(σ̂₂))(y) = 1`. ■
- Side conditions: semantic correctness of Constant Propagation is deferred to
  [PPA §4.5, p. 258] (book p. 258; PDF p. 275).
- Citation: [PPA Lemma 2.27, p. 73] (book p. 73; PDF p. 92); counterexample and §4.5 forward reference on
  [PPA Lemma 2.27, p. 74] (book p. 74; PDF p. 93)

### Findings (2.3)
- F-U2a-10: on p. 65 "`⨆` is `⋂` or `⋃` (and `⊔` is `∪` or `∩`)" lists the binary operators in the reverse
  order of the set operators; p. 70 omits a comma after `E` in "the extremal labels, `E` are". Recorded as
  printed. [PPA §2.3, p. 65] (book p. 65; PDF p. 84); [PPA §2.3.2, p. 70] (book p. 70; PDF p. 89)
- F-U2a-11: on p. 73 Table 2.7 prints `𝒜_CP⟦n⟧σ̂ = n` (for `σ̂ ≠ ⊥`) where Table 2.5 prints `𝒩⟦n⟧`, mixing
  numeral syntax with integer semantics. Recorded as printed.
  [PPA Table 2.7, p. 73] (book p. 73; PDF p. 92)

### Projections (2.3.3)
- cs_theory: `State^_CP` is a smashed/lifted function space `(Var⋆ → Z^⊤)_⊥` of finite height `2 + |Var⋆|`
  [derived] (hence ACC holds despite infinite `Z`); non-distributivity arises because independent-attribute
  [external] pointwise joins erase correlations across path disjuncts (`x = 1` vs `x = -1`) prior to
  evaluating multi-variable or non-injective operators (`x * x`).
- swe_architecture: distinguish global unreachable `⊥` (`State^_CP`) from per-variable unknown `⊤`
  (`ι_CP = λx.⊤`), and make `op^_a` strict in `⊥` (`⊥ op^_a ⊤ = ⊥`, *not* `⊤`!) so unreachable dead
  branches never pollute live constants at merge points.
- practical_debugging: if Constant Propagation reports `⊤` at a join where every concrete run produces the
  same constant (`[y:=x*x]` or `[y:=x-x]`), this is the expected `MFP ⊐ MOP` precision gap of Lemma 2.27,
  not a solver defect; if unreachable blocks (`if [false]`) poison reachable constants to `⊤`, non-extremal
  nodes were initialised to `λx.⊤` (`ι_CP`) instead of global `⊥`.
- cyber: independent-attribute state joins (`State^_CP`) lose correlated branch invariants (`if (fast)
  {buf=small; n=16} else {buf=big; n=256}; memcpy(buf, src, n)` [external]), producing false-positive
  buffer-overflow alerts (`256 > 16`, CWE-122 [external]) unless relational or disjunctive (`𝒫(L)`, §2.4.2)
  domains are used; never add ad-hoc algebraic simplifications like `a - a → 0` to `𝒜_CP` when `a` can
  trap or carry floating-point `NaN` [external] (`BKL-001`).

## 2.4 Equation Solving

Context: two solution methods for Monotone Framework instances — an iterative worklist algorithm computing
the MFP solution (§2.4.1) and path composition defining the MOP solution (§2.4.2)
[PPA §2.4, p. 74] (book p. 74; PDF p. 93).

### [U2a:2.4-a] Two approaches to obtaining an analysis result (unnumbered remark)
- Statement: (1) an iterative algorithm in the spirit of Chaotic Iteration
  ([PPA §1.7, p. 25] (book p. 25; PDF p. 45)); (2) propagating analysis information more directly along
  paths in the program.
- Citation: [PPA §2.4, p. 74] (book p. 74; PDF p. 93)

## 2.4.1 The MFP Solution

Context: edge-worklist algorithm (Table 2.8), trace (Table 2.9), termination and least-fixed-point
correctness (Lemma 2.29), and `O(e · h)` complexity [PPA §2.4.1, p. 74] (book p. 74; PDF p. 93).

### [U2a:2.4.1-a] Historical name "MFP" versus least fixed point (unnumbered definition)
- Statement: the general iterative algorithm computes the *least* solution to the data flow equations.
  Historically it is called the *MFP solution* (for *Maximal Fixed Point*) although it computes the least
  fixed point, because the classical literature focuses on analyses where `⊔` is `∩` (and the least fixed
  point with respect to `⊑` or `⊇` equals the greatest fixed point with respect to `⊆`).
- Citation: [PPA §2.4.1, p. 74] (book p. 74; PDF p. 93)

### [U2a:2.4.1-b] Data structures of the worklist algorithm (unnumbered definition)
- Statement: given an instance of a Monotone Framework, Table 2.8 maintains:
  - an array `Analysis` (sans-serif), indexed by labels, holding `Analysis∘` for each elementary block; and
  - a *worklist* `W` (sans-serif), a list of flow pairs `(ℓ, ℓ') ∈ F` whose presence indicates that the
    analysis changed at the exit of (or entry to, for backward analyses) `ℓ` and must be recomputed at the
    entry to (or exit from) `ℓ'`.
  A final stage presents `(MFP∘, MFP•)` in the form of the data flow equations.
- Citation: [PPA §2.4.1, p. 74] (book p. 74; PDF p. 93)

### Example 2.28 — Worklist execution on Example 2.26
- Statement: on `[x:=a+b]^1; [y:=a*b]^2; while [y>a+b]^3 do ([a:=a+1]^4; [x:=a+b]^5)` (Example 2.26), write
  italic `W` for `((2,3),(3,4),(4,5),(5,3))` and `U = {a+b, a*b, a+1}`. Step 1 initialises `W` and
  `Analysis` as in row 1 of Table 2.9; in Step 2, rows 2–7 update `Analysis` and `cons` a new pair on top
  of the worklist (inspected in the next iteration), while rows 8–12 make no modification so the worklist
  shrinks; Step 3 produces the solution of Example 2.5. ■
- Citation: [PPA Example 2.28, p. 74] (book p. 74; PDF p. 93); rows 2–12 commentary on
  [PPA Example 2.28, p. 75] (book p. 75; PDF p. 94)

### Table 2.8 — Algorithm for solving data flow equations
- Content:

```
INPUT:   An instance of a Monotone Framework:
         (L, 𝓕, F, E, ι, f_·)

OUTPUT:  MFP∘, MFP•

METHOD:  Step 1: Initialisation (of W and Analysis)
                 W := nil;
                 for all (ℓ, ℓ') in F do
                     W := cons((ℓ, ℓ'), W);
                 for all ℓ in F or E do
                     if ℓ ∈ E then Analysis[ℓ] := ι
                              else Analysis[ℓ] := ⊥_L;

         Step 2: Iteration (updating W and Analysis)
                 while W ≠ nil do
                     ℓ := fst(head(W)); ℓ' = snd(head(W));
                     W := tail(W);
                     if f_ℓ(Analysis[ℓ]) ⋢ Analysis[ℓ'] then
                        Analysis[ℓ'] := Analysis[ℓ'] ⊔ f_ℓ(Analysis[ℓ]);
                        for all ℓ'' with (ℓ', ℓ'') in F do
                            W := cons((ℓ', ℓ''), W);

         Step 3: Presenting the result (MFP∘ and MFP•)
                 for all ℓ in F or E do
                     MFP∘(ℓ) := Analysis[ℓ];
                     MFP•(ℓ) := f_ℓ(Analysis[ℓ])
```

- Side conditions: Step 2 prints `ℓ' = snd(head(W))` with `=` rather than `:=` (finding F-U2a-12); `W` is
  operated as a LIFO stack (`cons`, `head`, `tail`) without membership deduplication (`[derived]`, visible
  in Table 2.9 rows 2–11).
- Citation: [PPA Table 2.8, p. 75] (book p. 75; PDF p. 94)

### Table 2.9 — Iteration steps of the worklist algorithm
- Content (column group header: `Analysis[ℓ] for ℓ being` `1..5`):

| Row | W | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `((1,2),W)` | `∅` | `U` | `U` | `U` | `U` |
| 2 | `((2,3),W)` | `∅` | `{a+b}` | `U` | `U` | `U` |
| 3 | `((3,4),W)` | `∅` | `{a+b}` | `{a+b,a*b}` | `U` | `U` |
| 4 | `((4,5),W)` | `∅` | `{a+b}` | `{a+b,a*b}` | `{a+b,a*b}` | `U` |
| 5 | `((5,3),W)` | `∅` | `{a+b}` | `{a+b,a*b}` | `{a+b,a*b}` | `∅` |
| 6 | `((3,4),W)` | `∅` | `{a+b}` | `{a+b}` | `{a+b,a*b}` | `∅` |
| 7 | `((4,5),W)` | `∅` | `{a+b}` | `{a+b}` | `{a+b}` | `∅` |
| 8 | `((2,3),···)` | `∅` | `{a+b}` | `{a+b}` | `{a+b}` | `∅` |
| 9 | `((3,4),···)` | `∅` | `{a+b}` | `{a+b}` | `{a+b}` | `∅` |
| 10 | `((4,5),···)` | `∅` | `{a+b}` | `{a+b}` | `{a+b}` | `∅` |
| 11 | `((5,3))` | `∅` | `{a+b}` | `{a+b}` | `{a+b}` | `∅` |
| 12 | `()` | `∅` | `{a+b}` | `{a+b}` | `{a+b}` | `∅` |

- Citation: [PPA Table 2.9, p. 76] (book p. 76; PDF p. 95)

### Lemma 2.29 — Termination and correctness of the worklist algorithm
- Statement: the worklist algorithm in Table 2.8 always terminates and it computes the least (or MFP)
  solution to the instance of the framework given as input. ■
- Proof (summary):
  - *Termination*: Steps 1 and 3 loop over finite sets. With `b` labels, `W` initially holds at most `b²`
    pairs; each Step 2 iteration either pops one pair or pushes up to `b` pairs only when
    `f_ℓ(Analysis[ℓ]) ⋢ Analysis[ℓ']` (`⊐` or incomparable), which makes `Analysis[ℓ']` strictly greater;
    by ACC on `L`, strict increases occur only finitely many times.
  - *Correctness*: let `(Analysis∘, Analysis•)` be the least solution.
    - Part (i): `∀ℓ : Analysis[ℓ] ⊑ Analysis∘(ℓ)` is a Step 2 loop invariant (holds after Step 1 since
      `Analysis∘(ℓ) ⊒ ι` for `ℓ ∈ E`, and preserved by monotonicity of `f_ℓ` and fixed-point equality of
      `Analysis∘`).
    - Part (ii): on termination `W = nil`, so by contradiction on the last update to `Analysis[ℓ]`,
      `∀(ℓ, ℓ') ∈ F : Analysis[ℓ'] ⊒ f_ℓ(Analysis[ℓ])`, and `∀ℓ ∈ E : Analysis[ℓ] ⊒ ι`, giving
      `∀ℓ : Analysis[ℓ] ⊒ (⨆{f_{ℓ'}(Analysis[ℓ']) | (ℓ', ℓ) ∈ F}) ⊔ ι^ℓ_E`.
    - Part (iii): by [PPA Proposition A.10, p. 402] (book p. 402; PDF p. 418) and leastness of `Analysis∘`,
      `∀ℓ : MFP∘(ℓ) ⊒ Analysis∘(ℓ)`; combined with (i), `∀ℓ : MFP∘[ℓ] = Analysis∘(ℓ)` (square brackets as
      printed; finding F-U2a-13). ■
- Citation: [PPA Lemma 2.29, p. 75] (book p. 75; PDF p. 94); termination and part (i) on
  [PPA Lemma 2.29, p. 76] (book p. 76; PDF p. 95); parts (ii)–(iii) on
  [PPA Lemma 2.29, p. 77] (book p. 77; PDF p. 96)

### [U2a:2.4.1-c] Complexity upper bound `O(e · h)` (unnumbered result)
- Statement: counting applications of `f_ℓ`, applications of `⊔`, and updates of `Analysis` as basic
  operations, assume:
  1. `F` is represented (e.g. an array of lists) so all `(ℓ', ℓ'')` emanating from `ℓ'` are found in time
     proportional to their number;
  2. `E` and `F` contain at most `b ≥ 1` distinct labels;
  3. `F` contains at most `e ≥ b` pairs; and
  4. `L` has *finite height* at most `h ≥ 1`.
  Then Steps 1 and 3 take `O(b + e)` basic operations, and Step 2 places each pair on `W` at most `O(h)`
  times with `O(1)` basic steps per inspection (excluding pushing new pairs), giving `O(e · h)` total basic
  operations (and `O(b² · h)` since `e ≤ b²`).
- Citation: [PPA §2.4.1, p. 77] (book p. 77; PDF p. 96); Step 2 and total bound on
  [PPA §2.4.1, p. 78] (book p. 78; PDF p. 97)

### Example 2.30 — Complexity of Reaching Definitions
- Statement: for Reaching Definitions with at most `v ≥ 1` variables and `b ≥ 1` labels in `S⋆`:
  - `L = 𝒫(Var⋆ × Lab⋆^?)` has `h ≤ v · b` (finding F-U2a-14), giving `O(v · b³)`;
  - if `S⋆` is label consistent, the variable `x` in `(x, ℓ)` is uniquely determined by `ℓ`, giving `O(b³)`
    (finding F-U2a-14);
  - since `F = flow(S⋆)` constructs at most two pairs with `ℓ` in the first component (`e ≤ 2 · b`), the
    bound refines to `O(b²)`. ■
- Citation: [PPA Example 2.30, p. 78] (book p. 78; PDF p. 97)

### Findings (2.4.1)
- F-U2a-12: on p. 75 Table 2.8 prints `ℓ := fst(head(W)); ℓ' = snd(head(W));` with `=` on the second
  assignment; p. 74 Example 2.28 prints "how the algorithms works". Recorded as printed.
  [PPA Table 2.8, p. 75] (book p. 75; PDF p. 94); [PPA Example 2.28, p. 74] (book p. 74; PDF p. 93)
- F-U2a-13: on p. 77 Lemma 2.29 part (iii) writes `MFP∘[ℓ]` with array brackets where `MFP∘(ℓ)` is used
  two lines earlier and in Table 2.8. Recorded as printed. [PPA Lemma 2.29, p. 77] (book p. 77; PDF p. 96)
- F-U2a-14: on p. 78 Example 2.30 writes `h ≤ v · b` for `𝒫(Var⋆ × Lab⋆^?)`, overlooking the `v` pairs
  `(x, ?)` (`|Var⋆ × Lab⋆^?| = v · (b + 1)`), and under label consistency writes `O(b³)` / `O(b²)` where
  `h ≤ b + v` yields `O(b² · (b + v))` and `O(b · (b + v))` (`O(b³)` / `O(b²)` holds when `v = O(b)`
  [derived]). Recorded as printed. [PPA Example 2.30, p. 78] (book p. 78; PDF p. 97)

### Projections (2.4.1)
- cs_theory: Table 2.8 refines Chapter 1's Chaotic Iteration into dependency-driven Tarski ([external: Kleene])
  ascending iteration terminating at a reductive fixed point in `Red(F)` (`Analysis[ℓ] ⊒ F(Analysis)(ℓ)`, Lemma 2.29(ii)–(iii)); ACC alone guarantees termination (Lemma 2.29), whereas the
  polynomial `O(e · h)` bound requires *finite height* `h` (`Constant Propagation` has ACC and finite
  height `2 + v`, while general ACC lattices can have unbounded finite-chain heights [derived]).
- swe_architecture: store only `Analysis∘` during solving and materialise `MFP•` lazily in Step 3; augment
  `W` with an `in_worklist` bitset [external] and reverse-postorder scheduling (generalised in Chapter 6,
  `U2`) so duplicate edges (`Table 2.9` rows 8–11) do not bloat `|W|` from `≤ e` to `O(e · h)`.
- practical_debugging: two classic solver bugs in Step 2 are (1) overwriting `Analysis[ℓ'] := f_ℓ(...)`
  instead of joining `Analysis[ℓ'] ⊔ f_ℓ(...)` (breaks monotonicity of `Analysis[ℓ']` and causes oscillation)
  and (2) testing `≠` instead of `⋢` (`f_ℓ(Analysis[ℓ]) ⊏ Analysis[ℓ']` triggers spurious re-enqueues
  without advancing `Analysis[ℓ']`); use Table 2.9's 12-row trace as a golden unit test [external].
- cyber: `O(e · h)` governs whether whole-binary or CI taint/constant scanners complete within budget or
  suffer algorithmic complexity denial-of-service [external] on dense indirect-jump CFGs (`e = Θ(b²)`);
  halting Table 2.8 early at an iteration cap leaves `Analysis[ℓ] ⊑ MFP∘(ℓ)` (Lemma 2.29(i)), which is
  *unsound* (under-approximates may-taint and over-claims must-checks [derived])!

## 2.4.2 The MOP Solution

Context: formalising path-based propagation (`path∘`, `path•`, `f_ℓ⃗`, `MOP∘`, `MOP•`), proving Constant
Propagation MOP undecidable (Lemma 2.31), and relating MFP to MOP (Lemma 2.32)
[PPA §2.4.2, p. 78] (book p. 78; PDF p. 97).

### [U2a:2.4.2-a] Historical name "MOP" versus join over paths (unnumbered definition)
- Statement: historically called the *MOP solution* (for *Meet Over all Paths*), this method in fact takes
  the *join* (least upper bound `⨆`) over all paths leading to an elementary block — again because the
  classical literature focuses on analyses where `⊔` is `∩`.
- Citation: [PPA §2.4.2, p. 78] (book p. 78; PDF p. 97)

### [U2a:2.4.2-b] Informal notion of paths (unnumbered remark)
- Statement: forward analyses compose transfer functions along paths from the initial block up to a block's
  entry (state before the block executes); backward analyses compose along paths from a block's exit to a
  final block (state immediately after the block executes). For a large class of analyses, the equational
  approach and the path approach coincide.
- Citation: [PPA §2.4.2, p. 78] (book p. 78; PDF p. 97)

### [U2a:2.4.2-c] Formal path sets `path∘, path•`, path transfer `f_ℓ⃗`, and `MOP∘, MOP•` (unnumbered definition)
- Statement: for an instance `(L, 𝓕, F, E, ι, f_·)` of a Monotone Framework and label sequences
  `ℓ⃗ = [ℓ₁, ···, ℓ_n]` (`n ≥ 0`):

```
path∘(ℓ) = {[ℓ₁, ···, ℓ_{n-1}] | n ≥ 1 ∧ ∀i < n : (ℓ_i, ℓ_{i+1}) ∈ F ∧ ℓ_n = ℓ ∧ ℓ₁ ∈ E}
path•(ℓ) = {[ℓ₁, ···, ℓ_n]     | n ≥ 1 ∧ ∀i < n : (ℓ_i, ℓ_{i+1}) ∈ F ∧ ℓ_n = ℓ ∧ ℓ₁ ∈ E}

f_ℓ⃗ = f_{ℓ_n} ∘ ··· ∘ f_{ℓ₁} ∘ id        (so f_[ ] = id)

MOP∘(ℓ) = ⨆{f_ℓ⃗(ι) | ℓ⃗ ∈ path∘(ℓ)}
MOP•(ℓ) = ⨆{f_ℓ⃗(ι) | ℓ⃗ ∈ path•(ℓ)}
```

- Side conditions: `path∘(ℓ)` collects paths up to *but not including* `ℓ` (when `ℓ ∈ E`, taking `n = 1`
  puts the empty path `[ ]` into `path∘(ℓ)` with `(f_[ ])(ι) = ι` [derived]); `path•(ℓ)` collects paths up to
  *and including* `ℓ`. Both `𝓕`'s closure under `∘` and membership `id ∈ 𝓕` ensure `f_ℓ⃗ ∈ 𝓕` [derived].
- Citation: [PPA §2.4.2, p. 78] (book p. 78; PDF p. 97); `path∘`, `path•`, `f_ℓ⃗`, `MOP∘`, `MOP•` displays on
  [PPA §2.4.2, p. 79] (book p. 79; PDF p. 98)

### [U2a:2.4.2-d] Uncomputability of MOP versus computability of MFP (unnumbered remark)
- Statement: the MOP solution is sometimes uncomputable (undecidable), even though the MFP solution is
  always easily computable because the property space satisfies ACC.
- Citation: [PPA §2.4.2, p. 79] (book p. 79; PDF p. 98)

### Lemma 2.31 — Undecidability of the MOP solution for Constant Propagation
- Statement: the MOP solution for Constant Propagation is undecidable. ■
- Proof (summary): reduces from the *Modified Post Correspondence Problem* (MPCP): given strings
  `u₁, ···, u_n` and `v₁, ···, v_n` over `{1, ···, 9}` ([PPA Appendix C, p. 417] (book p. 417; PDF p. 432)),
  does there exist `i₁, ···, i_m` with `i₁ = 1` such that `u_{i₁} ··· u_{i_m} = v_{i₁} ··· v_{i_n}`
  (misprinted `v_{i_n}` for `v_{i_m}`; finding F-U2a-15)? Writing `|u|` for length and `⟦u⟧` for natural-number
  value, construct (omitting most labels, and omitting `;` before line 5 as printed):

```
x:=⟦u₁⟧; y:=⟦v₁⟧;
while [···] do
  (if [···] then x:=x * 10^|u₁| + ⟦u₁⟧; y:=y * 10^|v₁| + ⟦v₁⟧ else
   ⋮
   if [···] then x:=x * 10^|u_n| + ⟦u_n⟧; y:=y * 10^|v_n| + ⟦v_n⟧ else skip)
[z:=sign((x-y)*(x-y))]^ℓ
```

  where `sign` returns `1` for positive arguments and `0` or `-1` otherwise, and `[···]` guards are
  irrelevant because MOP ranges over all syntactic paths. `MOP•(ℓ)` maps `z` to `1` iff the MPCP instance
  has no solution. Since MPCP is undecidable (entry `[76]` in [PPA Bibliography, p. 444] (book p. 444; PDF p. 457)), MOP for
  Constant Propagation is undecidable — *side condition*: "assuming that our selection of arithmetic
  operations does indeed allow those used to be defined". ■
- Citation: [PPA Lemma 2.31, p. 79] (book p. 79; PDF p. 98); `sign` argument and `[76]` reduction step on
  [PPA Lemma 2.31, p. 80] (book p. 80; PDF p. 99)

### [U2a:2.4.2-e] Orientation of `MFP ⊒ MOP` across must and may analyses (unnumbered remark)
- Statement: MFP safely approximates MOP (`MFP ⊒ MOP`): for `(⋂, →, ↑)` or `(⋂, ←, ↑)` analyses, the MFP
  solution is a *subset* of the MOP solution (`⊒` is `⊆`); for `(⋃, →, ↓)` or `(⋃, ←, ↓)` analyses, the MFP
  solution is a *superset* of the MOP solution.
- Citation: [PPA §2.4.2, p. 80] (book p. 80; PDF p. 99)

### Lemma 2.32 — Safe approximation and coincidence of MFP and MOP
- Statement: consider the MFP and MOP solutions to an instance `(L, 𝓕, F, B, ι, f_·)` (`B` printed for `E`,
  finding F-U2a-16) of a Monotone Framework; then:

```
MFP∘ ⊒ MOP∘   and   MFP• ⊒ MOP•
```

  If the framework is distributive and if `path∘(ℓ) ≠ ∅` for all `ℓ` in `E` and `F` then:

```
MFP∘ = MOP∘   and   MFP• = MOP•
```

  ■
- Proof (summary):
  - *Part 1 (`MFP ⊒ MOP`)*: since `∀ℓ : MOP•(ℓ) ⊑ f_ℓ(MOP∘(ℓ))` (by monotonicity) and
    `∀ℓ : MFP•(ℓ) = f_ℓ(MFP∘(ℓ))`, it suffices to prove `∀ℓ : MOP∘(ℓ) ⊑ MFP∘(ℓ)`. `MFP∘` is the least fixed
    point of functional `F(A∘)(ℓ) = (⨆{f_{ℓ'}(A∘(ℓ')) | (ℓ', ℓ) ∈ F}) ⊔ ι^ℓ_E` (overloading italic `F`;
    finding F-U2a-16). Restricting path length via `MOP∘^n(ℓ) = ⨆{f_ℓ⃗(ι) | ℓ⃗ ∈ path∘(ℓ), |ℓ⃗| < n}` (`n ≥ 0`)
    gives `MOP∘(ℓ) = ⨆_n MOP∘^n(ℓ)`, and numerical induction on `n` using the induction hypothesis and
    monotonicity of `f_{ℓ'}` establishes `∀n : MFP∘ ⊒ MOP∘^n`.
  - *Part 2 (`MFP = MOP`)*: assume the framework is distributive (`f_ℓ(l₁ ⊔ l₂) = f_ℓ(l₁) ⊔ f_ℓ(l₂)`) and
    consider `ℓ` in `E` or `F`. By [PPA Lemma A.9, p. 401] (book p. 401; PDF p. 417) (which uses ACC on `L`),
    `f_ℓ(⨆Y) = ⨆{f_ℓ(l) | l ∈ Y}` *whenever `Y` is non-empty* (`BKL-022`). Because `path∘(ℓ) ≠ ∅` by
    hypothesis, `Y = {f_ℓ⃗(ι) | ℓ⃗ ∈ path∘(ℓ)} ≠ ∅`, yielding `∀ℓ : f_ℓ(MOP∘(ℓ)) = MOP•(ℓ)` and
    `MOP∘(ℓ) = (⨆{f_{ℓ'}(MOP∘(ℓ')) | (ℓ', ℓ) ∈ F}) ⊔ ι^ℓ_E`. Thus `(MOP∘, MOP•)` solves `Analysis^=`; by
    [PPA Proposition A.10, p. 402] (book p. 402; PDF p. 418) and leastness of `(MFP∘, MFP•)`,
    `MOP∘ ⊒ MFP∘` and `MOP• ⊒ MFP•`, giving equality with Part 1. ■
- Side conditions: printed as **Lemma 2.32** (not a Theorem); *both* hypotheses — binary distributivity
  of `𝓕` *and* `path∘(ℓ) ≠ ∅` for all `ℓ` in `E` and `F` — are required by the proof (`BKL-017`, `BKL-022`).
- Citation: [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99); inductive chain and Part 2 proof on
  [PPA Lemma 2.32, p. 81] (book p. 81; PDF p. 100)

### [U2a:2.4.2-f] Program reachability (`Exercise 2.13`) and MOP via powerset `𝒫(L)` (unnumbered remark)
- Statement: [PPA Exercise 2.13, p. 137] (book p. 137; PDF p. 156) shows that `path∘(ℓ) ≠ ∅` (for `ℓ` in
  `E` and `F`) holds when the Monotone Framework is constructed from a `WHILE` program `S⋆` as in earlier
  sections. Regarding the belief that MOP is "the desired solution" and MFP is used only because MOP may be
  uncomputable: validating that belief would require proving MOP semantically correct (immediate for Live
  Variables by distributivity), which the book declines to do "because it is always possible to formulate
  the MOP solution as an MFP solution over a different property space (like `𝒫(L)`)", where `𝒫(L)` satisfies
  ACC when `L` is finite.
- Citation: [PPA §2.4.2, p. 81] (book p. 81; PDF p. 100); semantic correctness discussion and `𝒫(L)`
  formulation on [PPA §2.4.2, p. 82] (book p. 82; PDF p. 101)

### Findings (2.4.2)
- F-U2a-15: on p. 79 the proof of Lemma 2.31 prints `u_{i₁} ··· u_{i_m} = v_{i₁} ··· v_{i_n}` (subscript
  `i_n` instead of `i_m` on the right-hand side) and omits `;` after `else skip)` before
  `[z:=sign((x-y)*(x-y))]^ℓ`. Recorded as printed. [PPA Lemma 2.31, p. 79] (book p. 79; PDF p. 98)
- F-U2a-16 (`[Source Erratum]`): on p. 80 Lemma 2.32 prints `(L, 𝓕, F, B, ι, f_·)` with `B` instead of `E`
  for the fourth component, overloads italic `F` in its proof for both the flow relation and the fixed-point
  functional, and prints "is therefore suffices" for "it therefore suffices". Recorded as printed.
  [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99)

### Projections (2.4.2)
- cs_theory: `MFP ⊒ MOP` (Kam–Ullman [external], Lemma 2.32) separates decidable join-at-merge fixed points
  from potentially undecidable join-over-paths ideals (Lemma 2.31); Lemma 2.32's general equality guarantee
  requires *both* binary distributivity and reachability `path∘(ℓ) ≠ ∅` because Lemma A.9 lifts binary
  additivity only to *non-empty* joins (`BKL-022`), while non-strict transfers satisfy `f_ℓ(⊥) ≠ ⊥`!
- swe_architecture: when non-distributive path merging causes unacceptable precision loss, lift the domain
  toward `𝒫(L)` (disjunctive completion / trace partitioning [external]) while keeping the exact same MFP
  worklist engine; prune unreachable CFG blocks (`path∘(ℓ) = ∅`) before running non-strict analyses so dead
  code cannot inject phantom facts `f_ℓ(⊥)` into `MFP•` (`BKL-017`).
- practical_debugging: even on Figure 2.6's distributive kill/gen analyses, if a raw CFG contains an
  unreachable dead block `[x:=1]^9` (`path∘(9) = ∅`), `MOP•(9) = ⨆∅ = ⊥ = ∅` whereas `MFP•(9) = f_9(∅) = {(x,9)}`,
  and an edge `(9, 2) ∈ F` propagates `(x, 9)` into reachable nodes (`[derived]`, `BKL-017`)!
- cyber: Lemma 2.31 proves no sound static constant/value resolver can avoid path-merge imprecision on all
  programs, and `MFP ⊒ MOP` guarantees that path-merging errs safely (false alarms in may-taint and
  refused proofs in must-sanitisation [external], never missed flows); however, in stripped binaries with
  disconnected dead islands (`path∘(ℓ) = ∅`), `MFP•(ℓ) = f_ℓ(⊥)` manufactures phantom definitions/taints
  absent from `MOP•(ℓ)` unless unreachable blocks are eliminated first [derived].

## Gotcha Ledger

- G-U2a-01: `init(S)` returns a single entry label whereas `final(S)` returns a set of labels because conditionals have multiple exits; for `while [b]^ℓ do S`, `final = {ℓ}` because the loop exits immediately after `[b]^ℓ` evaluates to `false`. [PPA §2.1, p. 36] (book p. 36; PDF p. 55)
- G-U2a-02: In `labels(S) = {init(S)} ∪ {ℓ | (ℓ, ℓ') ∈ flow(S)} ∪ {ℓ' | (ℓ, ℓ') ∈ flow(S)}` (and the dual `flow^R` identity with `final(S)`), removing `{init(S)}` (or `final(S)`) is valid only for composite statements, not single elementary blocks `[B]^ℓ`. [PPA §2.1, p. 37] (book p. 37; PDF p. 56)
- G-U2a-03: The reversed flow graph `(labels(S), flow^R(S))` has a unique entry node in case `final(S)` contains just one element; backward analyses generally have multiple extremal labels. [PPA §2.1, p. 38] (book p. 38; PDF p. 57)
- G-U2a-04: `AExp⋆`, `AExp(a)`, and `AExp(b)` contain only *non-trivial* arithmetic subexpressions; single variables and constants are excluded as trivial. [PPA §2.1, p. 39] (book p. 39; PDF p. 58)
- G-U2a-05: Isolated entries (`∀ℓ ∈ Lab : (ℓ, init(S⋆)) ∉ flow(S⋆)`) holds whenever `S⋆` does not start with a `while`-loop, whereas isolated exits (`∀ℓ₁ ∈ final(S⋆) ∀ℓ₂ ∈ Lab : (ℓ₁, ℓ₂) ∉ flow(S⋆)`) fails on programs ending in a `while`-loop such as `power` in Example 2.3. [PPA Example 2.3, p. 39] (book p. 39; PDF p. 58)
- G-U2a-06: All §2.1 analyses require *label consistency* (`[B₁]^ℓ, [B₂]^ℓ ∈ blocks(S) ⇒ B₁ = B₂`, implied by unique labelling) so "`[B]^ℓ ∈ blocks(S)`" defines an unambiguous partial function from labels to elementary blocks. [PPA §2.1, p. 39] (book p. 39; PDF p. 58)
- G-U2a-07: Tables 2.1 and 2.2 (`AE^=`, `RD^=`) presuppose label consistency and *isolated entries*, while Tables 2.3 and 2.4 (`VB^=`, `LV^=`) presuppose label consistency and *isolated exits*; violating isolation drops edges into `init(S⋆)` or out of `final(S⋆)` unless §2.3's `ι^ℓ_E` join equation is used. [PPA §2.3, p. 66] (book p. 66; PDF p. 85)
- G-U2a-08: `gen_AE([x := a]^ℓ) = {a' ∈ AExp(a) | x ∉ FV(a')}` excludes subexpressions mentioning the assigned variable `x` (such as `a+1` in `[a:=a+1]^4`), whereas backward `gen_VB([x := a]^ℓ) = AExp(a)` includes them because `a` is evaluated before `x` is overwritten. [PPA Table 2.1, p. 40] (book p. 40; PDF p. 59)
- G-U2a-09: Must-analyses (`AE`, `VB`) seek the *largest* sets under `⊆` (`⊥_L = AExp⋆`, empty intersection `⋂∅ = AExp⋆`, Chaotic Iteration initialised at `AExp⋆`), because cyclic equations like `AE_entry(ℓ') = {x+y} ∩ AE_entry(ℓ')` also admit the uninformative fixed point `∅`. [PPA §2.1.1, p. 42] (book p. 42; PDF p. 61)
- G-U2a-10: May-analyses (`RD`, `LV`) seek the *smallest* sets under `⊆` (`⊥_L = ∅`, empty union `⋃∅ = ∅`), because cyclic equations like `LV_exit(ℓ) = LV_exit(ℓ) ∪ {x}` admit every superset of `{x}` and larger live sets block Dead Code Elimination. [PPA §2.1.4, p. 51] (book p. 51; PDF p. 70)
- G-U2a-11: Chapter 2 defines `Lab⋆^? = Lab⋆ ∪ {?}` with `? ∉ Lab⋆` (unlike Chapter 1 p. 7 where `? ∈ Lab⋆`); setting `RD_entry(init(S⋆)) = ∅` instead of `{(x, ?) | x ∈ FV(S⋆)}` is sound only when variables are always assigned before first use and causes incorrect optimisations otherwise. [PPA §2.1.2, p. 45] (book p. 45; PDF p. 64)
- G-U2a-12: Table 2.4 sets `LV_exit(ℓ) = ∅` for `ℓ ∈ final(S⋆)` (assuming all variables dead at program end); when final variable values are observed or output, `LV_exit` at final labels must be set to those output variables (changing upstream sets in Example 2.11). [PPA Example 2.11, p. 52] (book p. 52; PDF p. 71)
- G-U2a-13: In `clear(x, ℓ, ℓ')`, the formal formula restricts `¬def(x, ℓ_i)` to `i ∈ {1, ···, n-1}` so `ℓ_n` may both use and redefine `x` (contrary to the informal prose on p. 52 excluding `def` on `ℓ₁, ···, ℓ_n`). [PPA §2.1.5, p. 52] (book p. 52; PDF p. 71)
- G-U2a-14: The printed signatures `ud, du : Var⋆ × Lab⋆ → 𝒫(Lab⋆)` (p. 53) and `UD, DU : Var⋆ × Lab⋆ → 𝒫(Lab⋆)` (p. 54) omit `?` even though `ud` and `UD` return `?` (`ud(z, 3) = {?}`) and `du` branches on `ℓ = ?` (`du(z, ?) = {3}`); `ud`/`du` are non-constructive while `UD` constructively filters `RD_entry(ℓ)` by `x ∈ gen_LV(B^ℓ)`. [PPA §2.1.5, p. 53] (book p. 53; PDF p. 72)
- G-U2a-15: Table 2.5 assumes total, error-free expression evaluation (for example division by `0` produces an integer) and omits explicit `ℬ⟦true⟧σ` and `ℬ⟦false⟧σ` clauses; allowing runtime errors complicates correctness proofs and hoisting transformations. [PPA Table 2.5, p. 55] (book p. 55; PDF p. 74)
- G-U2a-16: Labels in `WHILE` are semantically passive — carried along by Table 2.6 transitions and never inspected — and `flow(S)`, `final(S)`, `blocks(S)` shrink (`⊇`) while label consistency (unlike unique labelling under `[wh₁]` loop unrolling) is preserved across steps. [PPA Lemma 2.14, p. 58] (book p. 58; PDF p. 77)
- G-U2a-17: In Lemma 2.14(i), `final(S) = {init(S)}` holds for one-step terminal transitions `⟨S, σ⟩ → σ'` (`[ass]`, `[skip]`, `[wh₂]`), and on p. 59 the proof of Lemma 2.14(iii) misprints `[wh₂]` as the heading for the `[wh₁]` loop-unrolling case. [PPA Lemma 2.14, p. 59] (book p. 59; PDF p. 78)
- G-U2a-18: Small-step preservation of a single fixed analysis result across `⟨S, σ⟩ → ⟨S', σ'⟩` (Lemma 2.16, Corollary 2.17) holds for the *constraint* system `LV^⊆(S⋆)`, not the *equation* system `LV^=(S⋆)`, while Lemma 2.15 guarantees both share the same least solution. [PPA Lemma 2.15, p. 60] (book p. 60; PDF p. 79)
- G-U2a-19: Because `LV^⊆(S⋆)` on p. 60 writes `LV_exit(ℓ) ⊇ ∅` when `ℓ ∈ final(S⋆)` (`otherwise` the `flow^R` union), Lemmas 2.16, 2.18, 2.20, Theorem 2.21, and Corollary 2.22 silently fail on statements without isolated exits (such as `while [x>0]^1 do [x:=x-y]^2`) unless §2.3's unconditional union `LV_exit(ℓ) ⊇ ⋃{...} ∪ ι^ℓ_E` is used. [PPA Lemma 2.18, p. 61] (book p. 61; PDF p. 80)
- G-U2a-20: In Corollary 2.22(ii), two terminating runs from states agreeing on `N(init(S))` end in states related by `σ₁' ∼_{X(ℓ)} σ₂'` *for some* `ℓ ∈ final(S)` (not every final label), and small-step SOS is chosen over big-step natural semantics because big-step models looping only by the absence of an inference tree (`Remark.`, p. 65). [PPA Corollary 2.22, p. 65] (book p. 65; PDF p. 84)
- G-U2a-21: Associating `⋂` with `↑` (greatest sets) and `⋃` with `↓` (least sets) collapses the eight-type `{⋂, ⋃} × {→, ←} × {↑, ↓}` cube into the four-type square `(⋂, →, ↑)`, `(⋃, →, ↓)`, `(⋂, ←, ↑)`, `(⋃, ←, ↓)`. [PPA §2.3, p. 66] (book p. 66; PDF p. 85)
- G-U2a-22: Section 2.3's Monotone Framework equations are independent of elementary-block syntax, except that they do *not* directly apply to languages with procedures (deferred to §2.5). [PPA §2.3, p. 66] (book p. 66; PDF p. 85)
- G-U2a-23: A join semi-lattice `(L, ⊔)` with unit `⊥` satisfying ACC is equivalent to a complete lattice satisfying ACC (via Lemma A.8), and DCC + `⨅` formulations define the same notion of Monotone Framework by lattice duality. [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87)
- G-U2a-24: A Monotone Framework `(L, 𝓕)` requires `L` to be a complete lattice with ACC and `𝓕` to be a set of monotone functions containing `id` and closed under composition `∘`; `𝓕` is *not* required to be a lattice or poset, and an *instance* adds the finite program-specific data `(F, E, ι, f_·)` inducing `Analysis^=` and `Analysis^⊑`. [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88)
- G-U2a-25: A Distributive Framework requires only binary join preservation `f(l₁ ⊔ l₂) = f(l₁) ⊔ f(l₂)` (where `⊒` already holds by monotonicity), *not* strictness `f(⊥) = ⊥`. [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88)
- G-U2a-26: In Figure 2.6, `L` is made dependent on the finite program-specific sets `AExp⋆`, `Var⋆`, and `Lab⋆^?` of `S⋆` (unlike infinite `AExp` and `Var × Lab`) to enforce the Ascending Chain Condition, and the extremal value `ι` obeys no universal rule (`ι` is `⊤_L` in `AE`/`VB`, `⊥_L` in `LV`, and neither in `RD` or `CP`). [PPA §2.3.2, p. 70] (book p. 70; PDF p. 89)
- G-U2a-27: In Lemma 2.25, functions of the shape `f(l) = (l \ l_k) ∪ l_g` compose as `(f ∘ f')(l) = (l \ (l_k' ∪ l_k)) ∪ ((l_g' \ l_k) ∪ l_g)` and are monotone and distributive regardless of whether `(⊑, ⊔)` is `(⊆, ∪)` or `(⊇, ∩)`. [PPA Lemma 2.25, p. 71] (book p. 71; PDF p. 90)
- G-U2a-28: Constant Propagation adjoins a global unreachable least element `⊥` below `Var⋆ → Z^⊤` (`State^_CP`), sets extremal value `ι_CP = λx.⊤` (strictly above `⊥`), makes `op^_a`, `𝒜_CP`, and `f_ℓ^CP` strict in `⊥`, takes `𝓕_CP` to be *all* monotone functions on `State^_CP`, and fails distributivity on `[y:=x*x]^ℓ` with `σ̂₁(x)=1, σ̂₂(x)=-1`. [PPA Lemma 2.27, p. 73] (book p. 73; PDF p. 92)
- G-U2a-29: Despite their historical names ("Maximal Fixed Point" and "Meet Over all Paths" from `⊔ = ∩` literature), `MFP` computes the *least* fixed point and `MOP` computes the *join* (`⨆`) over all paths in `(L, ⊑)`. [PPA §2.4.1, p. 74] (book p. 74; PDF p. 93)
- G-U2a-30: Table 2.8 tests `f_ℓ(Analysis[ℓ]) ⋢ Analysis[ℓ']` (not `≠`), updates by joining `Analysis[ℓ'] := Analysis[ℓ'] ⊔ f_ℓ(Analysis[ℓ])` (not overwriting), prints `ℓ' = snd(head(W))` with `=`, and pushes outgoing edges onto LIFO list `W` without deduplication. [PPA Table 2.8, p. 75] (book p. 75; PDF p. 94)
- G-U2a-31: Lemma 2.29 guarantees termination of Table 2.8 under ACC and finite `F, E`, whereas the `O(e · h)` complexity bound additionally requires `L` to have *finite height* `h ≥ 1`, `e ≥ b ≥ 1`, and `F` to enumerate outgoing edges from `ℓ'` in time proportional to out-degree; Example 2.30's `h ≤ v · b` and `O(b²)` bounds for `RD` omit the `v` uninitialised pairs `(x, ?)` (`h ≤ b + v` under label consistency). [PPA §2.4.1, p. 77] (book p. 77; PDF p. 96)
- G-U2a-32: `path∘(ℓ)` collects paths from `E` up to *but not including* `ℓ` (including the empty path `[ ]` with `f_[ ] = id` when `ℓ ∈ E`), while `path•(ℓ)` includes `ℓ`. [PPA §2.4.2, p. 79] (book p. 79; PDF p. 98)
- G-U2a-33: The MOP solution for Constant Propagation is undecidable by reduction from the Modified Post Correspondence Problem `[76]` (assuming the language's arithmetic operators can express those used in the reduction; p. 79 misprints `v_{i_n}` for `v_{i_m}`), even though the MFP solution is always computable under ACC. [PPA Lemma 2.31, p. 79] (book p. 79; PDF p. 98)
- G-U2a-34: Lemma 2.32 (printed as `Lemma 2.32`, with `B` misprinted for `E` in `(L, 𝓕, F, B, ι, f_·)`) proves `MFP∘ ⊒ MOP∘` and `MFP• ⊒ MOP•` (`MFP ⊆ MOP` for `⋂` must-analyses, `MFP ⊇ MOP` for `⋃` may-analyses), and establishes `MFP∘ = MOP∘` and `MFP• = MOP•` when *both* the framework is distributive *and* `path∘(ℓ) ≠ ∅` for all `ℓ` in `E` and `F` (both hypotheses are needed in the proof because Lemma A.9 requires non-empty sets `Y ≠ ∅`). [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99)
- G-U2a-35: The book declines to prove general semantic correctness of MOP directly because MOP can always be formulated as an MFP solution over a richer property space such as `𝒫(L)` (`𝒫(L)` satisfies ACC when `L` is finite). [PPA §2.4.2, p. 82] (book p. 82; PDF p. 101)
