<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 3a (Chapter 3 §§3.1-3.4). -->

# RAW_SHARD_03a — Chapter 3 Abstract, Syntax-Directed, and Constraint-Based 0-CFA (Unit 3a)

Source: *Principles of Program Analysis* (Nielson, Nielson, Hankin), corrected 2nd printing, 2005.
Scope: Chapter 3 opening, §3.1 Abstract 0-CFA Analysis (§3.1.1–§3.1.2), §3.2 Theoretical Properties
(§3.2.1–§3.2.4), §3.3 Syntax Directed 0-CFA Analysis (§3.3.1–§3.3.2), and §3.4 Constraint Based 0-CFA
Analysis (§3.4.1–§3.4.2), spanning book pages 141–182 / PDF pages 159–200 and ending immediately above
the §3.5 heading on book p. 182. Adding Data Flow Analysis (§3.5), Adding Context Information (§3.6),
Concluding Remarks, Mini Projects 3.1–3.4, and Exercises 3.1–3.17 belong to Unit 3b.

Coordinates: PDF page = book page + 18 throughout Chapter 3 (blank verso p. 140 at the end of Chapter 2
is absent from the PDF). Section starts in Unit 3a: Chapter 3 opening and §3.1 on p. 141 (§3.1.1 on
p. 143, §3.1.2 on p. 150; there is no §3.1.3 in the printed book), §3.2 and §3.2.1 on p. 153 (§3.2.2 on
p. 158, §3.2.3 on p. 162, §3.2.4 on p. 165), §3.3 on p. 168 (§3.3.1 on p. 169, §3.3.2 on p. 171), and
§3.4 on p. 173 (§3.4.1 on p. 175, §3.4.2 on p. 176, concluding at the upper half of p. 182 before §3.5)
[PPA §3.1, p. 141] (book p. 141; PDF p. 159).

Conventions:

- Every source reference pairs a strict inline locator token with its book/PDF coordinate companion, for
  example [PPA §3.1, p. 141] (book p. 141; PDF p. 159), [PPA Table 3.1, p. 146] (book p. 146; PDF p. 164),
  or [PPA Preface, p. VI] (book p. VI; PDF p. 6).
- Book-numbered items preserve their exact printed kind word and number (`3.1`–`3.25` in one shared
  per-chapter sequence of 14 Examples, 1 Theorem, 1 Fact, 1 Lemma, 7 Propositions, and 1 Corollary,
  plus Tables `3.1`–`3.7`, Figures `3.1`–`3.5`, and equation displays `(3.1)`–`(3.7)`; there are no
  numbered Definitions in §§3.1–3.4). Unnumbered definitions, semantic clauses, proof blocks, and the
  printed `Remark.` (p. 145) and `Analogy.` (p. 152) paragraphs carry non-book identifiers
  `[U3a:<section>-<letter>]`.
- Every formula, rule, program, table, and figure is transcribed directly from rendered page images
  (PDF pages 159–200) rather than the OCR text layer, which erases rule premises in Tables 3.2 and 3.3,
  the body of Fact 3.11 on p. 160, the displayed greatest-lower-bound formula in Proposition 3.24 on
  p. 180, and wide-hat / subscript glyphs across `Cachê`, `Env̂`, `Val̂`, `Ĉ`, and `ρ̂`.
- Terms absent from the book carry `[external]`. Deductions, worked counterexamples, and complexity
  refinements not printed in the text carry `[derived]`. Source misprints and internal tensions are
  transcribed verbatim as printed and logged under `Findings` (`F-U3a-NN`).
- Notation: `e ∈ Exp` labelled expressions (`t^ℓ`); `t ∈ Term` unlabelled terms; `ie ∈ IExp` and
  `it ∈ ITerm` intermediate expressions and terms; `f, x ∈ Var` variables; `c ∈ Const` constants;
  `op ∈ Op` syntactic binary operators and bold `**op**` semantic binary operations; `ℓ ∈ Lab` labels;
  `FV(e)` free variables; `v̂ ∈ Val̂ = 𝒫(Term)` abstract values, `ρ̂ ∈ Env̂ = Var → Val̂` abstract
  environments, `Ĉ ∈ Cachê = Lab → Val̂` abstract caches; `(Ĉ, ρ̂) ⊨ e` abstract 0-CFA acceptability
  (Tables 3.1 and 3.4); `𝒬` monotone functional defining `⊨ = gfp(𝒬)` and `⊨' = lfp(𝒬)`; `v ∈ Val` and
  `ρ ∈ Env` concrete values (`c` or `close t in ρ`) and list environments (`[]` or `ρ[x ↦ v]`); `ρ | X`
  environment restriction; `ρ ⊢ ie₁ → ie₂` small-step SOS transition; `ρ ℛ ρ̂` and `v 𝒱 (ρ̂, v̂)`
  correctness relations; `(Ĉ, ρ̂) ⊨_s e` syntax-directed 0-CFA acceptability (Table 3.5) with functional
  `𝒬_s`; `e_⋆` program of interest with finite `Term_⋆`, `Exp_⋆`, `Lab_⋆`, `Var_⋆`, restricted domains
  `Val̂_⋆`, `Cachê_⋆`, `Env̂_⋆`, and top bound `(Ĉ_⋆^⊤, ρ̂_⋆^⊤)`; sans-serif `C(ℓ)` and `r(x)` syntactic
  constraint variables; `𝒞_⋆⟦e_⋆⟧` constraint set (Table 3.6); `(Ĉ, ρ̂)⟦·⟧` constraint-expression
  valuation and `(Ĉ, ρ̂) ⊨_c C` constraint satisfaction; `F_⋆` fixed-point operator on `Cachê_⋆ × Env̂_⋆`;
  sans-serif `W`, `D[q]`, `E[q]`, `Nodes`, and `add(q, d)` graph-solver structures (Table 3.7); `■` as
  printed at the end of statements, proofs, and examples.

## Chapter 3 Opening

Context: Chapter 3 (*Constraint Based Analysis*) opens on p. 141 above the §3.1 heading with the three-stage
plan of the chapter on the functional language `FUN` [PPA Chapter 3, p. 141] (book p. 141; PDF p. 159).

### [U3a:3.0-a] Scope and plan of Chapter 3 (unnumbered remark)
- Statement: Chapter 3 presents *Constraint Based Analysis* for a simple functional language `FUN`:
  1. Specify an abstract *Control Flow Analysis* (§3.1) and establish its theoretical properties (§3.2):
     semantic correctness with respect to a Structural Operational Semantics (§3.2.2) and the existence of
     least solutions so that all programs can be analysed (§3.2.3).
  2. Because the abstract specification cannot directly be turned into an efficient algorithm for computing
     the least solution, reformulate the specification first into a *syntax directed* form (§3.3), next
     into a *constraint based* form (§3.4.1), and finally into an efficient constraint-solving algorithm
     (§3.4.2).
  3. Conclude the chapter (Unit 3b: §§3.5–3.6) by improving precision through Data Flow Analysis
     integration and context information, linking back to Chapter 2
     [PPA §3.5, p. 182] (book p. 182; PDF p. 200).
- Citation: [PPA Chapter 3, p. 141] (book p. 141; PDF p. 159)

### Projections (Chapter 3 Opening)
- cs_theory: Chapter 3 realises the unifying Specification-to-Solver Refinement Spine (`⊨` coinductive
  specification `→` `⊨_s` syntax-directed specification `→` `𝒞_⋆⟦e_⋆⟧` syntactic subset constraints `→`
  `O(n³)` worklist graph solver), decoupling semantic soundness proofs (§3.2) from polynomial-time fixed-point
  computation (§3.4) [PPA Chapter 3, p. 141] (book p. 141; PDF p. 159).
- swe_architecture: Separating declarative acceptability (`⊨`), AST-pass constraint emission (`𝒞_⋆`), and
  generic constraint-graph propagation (Table 3.7) lets language front-ends evolve independently of the
  worklist solver backend [external] [PPA Chapter 3, p. 141] (book p. 141; PDF p. 159).
- practical_debugging: When an interprocedural or higher-order static analyser produces a bad result,
  this layered spine localises the fault cleanly to one of three boundaries: unsound specification (`⊨`),
  over-conservative syntax-directed lowering (`⊨_s` / `𝒞_⋆`), or missing worklist edge registration
  (Table 3.7) [derived] [PPA Chapter 3, p. 141] (book p. 141; PDF p. 159).
- cyber: Higher-order Control Flow Analysis resolves dynamic call targets (closures, function pointers,
  callbacks, virtual dispatch tables, interprocedural taint, capability, or CFI checks [external]) required before any consumer analysis can rely on static call edges
  or reachability scanner can build a sound call graph [PPA §3.1, p. 141] (book p. 141; PDF p. 159).

## 3.1 Abstract 0-CFA Analysis

Context: Section 3.1 motivates Control Flow Analysis via the dynamic dispatch problem, defines the labelled
functional language `FUN`, introduces abstract domains `Val̂`, `Env̂`, and `Cachê`, specifies 0-CFA
acceptability `(Ĉ, ρ̂) ⊨ e` in Table 3.1, and defines `⊨` formally as `gfp(𝒬)` [PPA §3.1, p. 141] (book p. 141; PDF p. 159).

### [U3a:3.1-a] Dynamic dispatch motivation and link to `inter-flow_⋆` (unnumbered remark)
- Statement: Chapter 2 propagated data properties forward along `flow` (`inter-flow_⋆`) or backward along
  `flow^R` (`inter-flow_⋆^R`) [PPA §2.5, p. 85] (book p. 85; PDF p. 104), relying on every program point
  having a small statically known set of successors or predecessors. That assumption fails for imperative
  languages with procedure parameters, functional languages, and object-oriented languages. Section 2.5
  handled calls naming a declared procedure explicitly, but cannot solve the *dynamic dispatch problem*
  where variables denote procedures, illustrated (recalling §1.4
  [PPA §1.4, p. 13] (book p. 13; PDF p. 33)) by:
  ```text
  let f = fn x => x 1;
      g = fn y => y+2;
      h = fn z => z+3
  in (f g) + (f h)
  ```
  At `x 1` inside `f`, `x` is a formal parameter rather than a named procedure. Control Flow Analysis
  solves dynamic dispatch by computing for *each* subexpression a (hopefully small) set of functions that
  it may evaluate to; when the subexpression is the operator of a function application, this determines
  where control may transfer and thereby computes the `inter-flow_⋆` (`IF`) relation presupposed by §2.5.
- Citation: [PPA §3.1, p. 141] (book p. 141; PDF p. 159); [PPA §3.1, p. 142] (book p. 142; PDF p. 160)

### [U3a:3.1-b] Syntax of the `FUN` language (`Exp`, `Term`)
- Statement: `FUN` is the untyped lambda calculus extended with explicit recursion, conditional, local
  definitions, constants, and binary operators. A program fragment with a label is an *expression*; without
  a label it is a *term*:
  ```text
  e    ∈ Exp     expressions (or labelled terms)
  t    ∈ Term    terms (or unlabelled expressions)
  f, x ∈ Var     variables (countable set assumed given)
  c    ∈ Const   constants (unspecified; includes truth values true, false)
  op   ∈ Op      binary operators (unspecified; includes arithmetic, boolean, relational operators)
  ℓ    ∈ Lab     labels (unspecified)

  e ::= t^ℓ
  t ::= c
      | x
      | fn x => e₀
      | fun f x => e₀
      | e₁ e₂
      | if e₀ then e₁ else e₂
      | let x = e₁ in e₂
      | e₁ op e₂
  ```
- Side conditions:
  - Labels serve purely as pointers into syntax; labels are not required to be unique across a program,
    though distinct subexpressions are normally given distinct labels so analysis results can be
    distinguished.
  - Parentheses disambiguate parsing solely at the concrete level and carry no extra labels (so `(t^ℓ)` is
    identified with `t^ℓ`).
  - Free variables `FV(e)` (or `FV(t)`) are defined constructively in the standard way: `fn x => e₀` binds
    `x` in `e₀`; `fun f x => e₀` binds both `f` and `x` in `e₀`; `let x = e₁ in e₂` binds `x` in `e₂`
    (and *not* in `e₁`, so `let` is non-recursive).
- Citation: [PPA §3.1, p. 142] (book p. 142; PDF p. 160); [PPA §3.1, p. 143] (book p. 143; PDF p. 161)

### Example 3.1 — Fully labelled identity self-application
- Statement: Applying the identity function `fn x => x` to itself is written with all five subexpressions
  labelled as:
  ```text
  ((fn x => x^1)^2 (fn y => y^3)^4)^5
  ```
  (with `α`-renaming [external: bound-variable renaming] of the second copy to `y` to keep formal
  parameters distinct for clarity). `■`
- Citation: [PPA Example 3.1, p. 143] (book p. 143; PDF p. 161)

### Example 3.2 — Non-terminating recursive program `loop`
- Statement: Using `fun` for recursive definitions and `let` for binding, the program `loop` is:
  ```text
  let g = (fun f x => (f^1 (fn y => y^2)^3)^4)^5
  in (g^6 (fn z => z^7)^8)^9
  ```
  with top-level label `10`:
  ```text
  (let g = (fun f x => (f^1 (fn y => y^2)^3)^4)^5
   in (g^6 (fn z => z^7)^8)^9)^10
  ```
  Informally, evaluating `loop` binds `g` to `fun f x => ...`, calls `g` on `fn z => z^7` (`f` bound to the
  recursive function itself, `x` bound to `fn z => z^7`), and then loops forever calling `f` with `x`
  rebound to `fn y => y^2` on every subsequent recursive call. `■`
- Citation: [PPA Example 3.2, p. 143] (book p. 143; PDF p. 161); [PPA Example 3.2, p. 144] (book p. 144; PDF p. 162)

### 3.1.1 The Abstract Analysis

### [U3a:3.1.1-a] Abstract value, environment, and cache domains (`Val̂`, `Env̂`, `Cachê`)
- Statement: A *0-CFA analysis* (context-insensitive Control Flow Analysis) produces a pair `(Ĉ, ρ̂)` drawn
  from:
  ```text
  v̂ ∈ Val̂   = 𝒫(Term)         abstract values
  ρ̂ ∈ Env̂   = Var → Val̂       abstract environments
  Ĉ ∈ Cachê = Lab → Val̂       abstract caches
  ```
  - `Ĉ(ℓ)` records the set of *function abstractions* (`fn x => e₀` or `fun f x => e₀`, as unlabelled terms
    in `Term`) that the subexpression(s) labelled `ℓ` may evaluate to (tracking closures via their code
    terms while ignoring captured environments and non-function constants in pure 0-CFA).
  - `ρ̂(x)` records the set of function abstractions that variable `x` may be bound to anywhere during
    evaluation.
- Side conditions:
  - Distinct bound variables that happen to share the same identifier `x` are collapsed in `ρ̂(x)` unless
    renamed apart beforehand (`α`-conversion [external]); renaming all distinct bindings apart generally
    increases 0-CFA precision without changing program meaning (and also avoids spurious capture issues in
    a naive substitution-based view).
- Citation: [PPA §3.1.1, p. 144] (book p. 144; PDF p. 162)

### Example 3.3 — Candidate guesses `(Ĉ_e, ρ̂_e)`, `(Ĉ'_e, ρ̂'_e)`, and `(Ĉ''_e, ρ̂''_e)` for Example 3.1
- Statement: For `((fn x => x^1)^2 (fn y => y^3)^4)^5`, three candidate pairs are considered:
  1. Valid minimal candidate `(Ĉ_e, ρ̂_e)`:
     ```text
     Ĉ_e(1) = {fn y => y^3}     Ĉ_e(2) = {fn x => x^1}     Ĉ_e(3) = ∅
     Ĉ_e(4) = {fn y => y^3}     Ĉ_e(5) = {fn y => y^3}
     ρ̂_e(x) = {fn y => y^3}     ρ̂_e(y) = ∅
     ```
     (and `∅` elsewhere; notice `Ĉ_e(3) = ρ̂_e(y) = ∅` because `fn y => y^3` is passed as an argument and
     returned as the final result at label `5`, but never applied!).
  2. Invalid candidate `(Ĉ'_e, ρ̂'_e)`: identical on labels `1..5`, except `ρ̂'_e(x) = ∅` and `ρ̂'_e(y) = ∅`
     (which violates `(Ĉ'_e, ρ̂'_e) ⊨` because `x` gets bound to `fn y => y^3`).
  3. Valid imprecise candidate `(Ĉ''_e, ρ̂''_e)`: maps every label `1..5` and both variables `x, y` to the
     full pair `{fn x => x^1, fn y => y^3}` (`Ĉ''_e(ℓ) = {fn x => x^1, fn y => y^3}` for `ℓ ∈ {1..5}`,
     `ρ̂''_e(x) = ρ̂''_e(y) = {fn x => x^1, fn y => y^3}`), demonstrating that acceptability allows safe
     over-approximation (`Table 3.1` accepts infinitely many guesses above the least one). `■`
- Citation: [PPA Example 3.3, p. 144] (book p. 144; PDF p. 162); [PPA Example 3.3, p. 145] (book p. 145; PDF p. 163)

### Example 3.4 — Candidate guess `(Ĉ_lp, ρ̂_lp)` for `loop` (Example 3.2)
- Statement: Writing `f = fun f x => (f^1 (fn y => y^2)^3)^4`, `id_y = fn y => y^2`, and
  `id_z = fn z => z^7`, a candidate result `(Ĉ_lp, ρ̂_lp)` for `loop` is:
  ```text
  Ĉ_lp(1)  = {f}       Ĉ_lp(2) = ∅         Ĉ_lp(3) = {id_y}
  Ĉ_lp(4)  = ∅         Ĉ_lp(5) = {f}       Ĉ_lp(6) = {f}
  Ĉ_lp(7)  = ∅         Ĉ_lp(8) = {id_z}    Ĉ_lp(9) = ∅
  Ĉ_lp(10) = ∅
  ρ̂_lp(g)  = {f}       ρ̂_lp(f) = {f}       ρ̂_lp(x) = {id_y, id_z}
  ρ̂_lp(y)  = ∅         ρ̂_lp(z) = ∅
  ```
  Notice `Ĉ_lp(4) = Ĉ_lp(9) = Ĉ_lp(10) = ∅` (since `f` never returns a value) while `ρ̂_lp(x) = {id_y, id_z}`
  merges the initial external call argument `id_z` with the recursive call argument `id_y`. `■`
- Citation: [PPA Example 3.4, p. 145] (book p. 145; PDF p. 163)

### [U3a:3.1.1-c] `ud`-chains analogy, dynamic call graphs, and `Remark.` on `(Var ∪ Lab) → Val̂` and IRs
- Statement:
  - *Prose above `Remark.` (`ud`-chains and dynamic call graphs)*: Unlike imperative languages without
    procedure values (where each call names its callee and Chapter 2 §2.1.5 `ud`-chains directly build a
    *static call graph*), higher-order languages require `Ĉ(ℓ₁)` at each call `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ` to
    over-approximate the *dynamic call graph*.
  - *`Remark.` (p. 145)*: When `Var` and `Lab` are disjoint, `(Ĉ, ρ̂)` can be merged into a single function
    `(Var ∪ Lab) → Val̂` (reappearing as graph nodes `C(ℓ)` and `r(x)` in §3.4); the authors also note that
    labelled expressions correspond closely to compiler intermediate representations (continuation passing style
    `[external]`, A-normal form `[external]`, and three address code `[external]`). `■`
- Citation: [PPA §3.1.1, p. 145] (book p. 145; PDF p. 163)

### Table 3.1 — Abstract Control Flow Analysis (Subsections 3.1.1 and 3.1.2)
- Statement: Acceptability specification `(Ĉ, ρ̂) ⊨ e` with functionality
  `⊨ : (Cachê × Env̂ × Exp) → {true, false}` (writing "always" for "iff *true*"):
  ```text
  [con]  (Ĉ, ρ̂) ⊨ c^ℓ  always

  [var]  (Ĉ, ρ̂) ⊨ x^ℓ  iff  ρ̂(x) ⊆ Ĉ(ℓ)

  [fn]   (Ĉ, ρ̂) ⊨ (fn x => e₀)^ℓ  iff  {fn x => e₀} ⊆ Ĉ(ℓ)

  [fun]  (Ĉ, ρ̂) ⊨ (fun f x => e₀)^ℓ  iff  {fun f x => e₀} ⊆ Ĉ(ℓ)

  [app]  (Ĉ, ρ̂) ⊨ (t₁^{ℓ₁} t₂^{ℓ₂})^ℓ
             iff  (Ĉ, ρ̂) ⊨ t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨ t₂^{ℓ₂}  ∧
                  (∀(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) :
                       (Ĉ, ρ̂) ⊨ t₀^{ℓ₀}  ∧
                       Ĉ(ℓ₂) ⊆ ρ̂(x)  ∧  Ĉ(ℓ₀) ⊆ Ĉ(ℓ))  ∧
                  (∀(fun f x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) :
                       (Ĉ, ρ̂) ⊨ t₀^{ℓ₀}  ∧
                       Ĉ(ℓ₂) ⊆ ρ̂(x)  ∧  Ĉ(ℓ₀) ⊆ Ĉ(ℓ)  ∧
                       {fun f x => t₀^{ℓ₀}} ⊆ ρ̂(f))

  [if]   (Ĉ, ρ̂) ⊨ (if t₀^{ℓ₀} then t₁^{ℓ₁} else t₂^{ℓ₂})^ℓ
             iff  (Ĉ, ρ̂) ⊨ t₀^{ℓ₀}  ∧
                  (Ĉ, ρ̂) ⊨ t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨ t₂^{ℓ₂}  ∧
                  Ĉ(ℓ₁) ⊆ Ĉ(ℓ)  ∧  Ĉ(ℓ₂) ⊆ Ĉ(ℓ)

  [let]  (Ĉ, ρ̂) ⊨ (let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ
             iff  (Ĉ, ρ̂) ⊨ t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨ t₂^{ℓ₂}  ∧
                  Ĉ(ℓ₁) ⊆ ρ̂(x)  ∧  Ĉ(ℓ₂) ⊆ Ĉ(ℓ)

  [op]   (Ĉ, ρ̂) ⊨ (t₁^{ℓ₁} op t₂^{ℓ₂})^ℓ  iff  (Ĉ, ρ̂) ⊨ t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨ t₂^{ℓ₂}
  ```
- Side conditions:
  - Table 3.1 corresponds to an *implicit* specification (checking whether a proposed guess `(Ĉ, ρ̂)` is
    acceptable), whereas §§3.3–3.4 develop *explicit* formulations amenable to iterative solving in the
    spirit of Chaotic Iteration [PPA §1.7, p. 25] (book p. 25; PDF p. 45).
  - `[con]` places no demand on `Ĉ(ℓ)` (equivalently `∅ ⊆ Ĉ(ℓ)`) because pure 0-CFA tracks no non-function
    data values and assumes `Const` contains no functions.
  - `[fn]` and `[fun]` do *not* recursively demand `(Ĉ, ρ̂) ⊨ e₀` at definition sites; instead, `[app]`
    demands `(Ĉ, ρ̂) ⊨ t₀^{ℓ₀}` (and `{fun f x => t₀^{ℓ₀}} ⊆ ρ̂(f)` for recursive functions) only when a
    function term reaches an application operator `Ĉ(ℓ₁)`.
- Citation: [PPA Table 3.1, p. 146] (book p. 146; PDF p. 164); [PPA §3.1.1, p. 147] (book p. 147; PDF p. 165)

### Figure 3.1 — Pictorial illustration of the clauses `[let]` and `[var]`
- Statement: Directed information-flow diagram divided into `Ĉ` (left) and `ρ̂` (right) columns for
  `(let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ` containing a variable reference `x^{ℓ'}` inside the subtree of `t₂^{ℓ₂}`:
  - Solid arrow from subexpression box `t₁^{ℓ₁}` (under `Ĉ`) to variable box `x` (under `ρ̂`), depicting
    `Ĉ(ℓ₁) ⊆ ρ̂(x)` from `[let]`;
  - Solid arrow from variable box `x` (under `ρ̂`) to leaf box `x^{ℓ'}` inside `t₂^{ℓ₂}` (under `Ĉ`),
    depicting `ρ̂(x) ⊆ Ĉ(ℓ')` from `[var]`;
  - Solid arrow from subexpression box `t₂^{ℓ₂}` to enclosing box `(let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ` (both
    under `Ĉ`), depicting `Ĉ(ℓ₂) ⊆ Ĉ(ℓ)` from `[let]`.
- Citation: [PPA Figure 3.1, p. 148] (book p. 148; PDF p. 166)

### Figure 3.2 — Pictorial illustration of the clauses `[app]`, `[fn]` and `[var]`
- Statement: Directed information-flow diagram divided into `Ĉ` (left) and `ρ̂` (right) columns for
  `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ` when `fn x => t₀^{ℓ₀}` reaches `t₁^{ℓ₁}`:
  - Wavy membership arrow from oval `fn x => t₀^{ℓ₀}` into operator box `t₁^{ℓ₁}`, depicting the guard
    `(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁)`;
  - Solid arrow from argument box `t₂^{ℓ₂}` (under `Ĉ`) to formal parameter box `x` (under `ρ̂`),
    depicting `Ĉ(ℓ₂) ⊆ ρ̂(x)`;
  - Solid arrow from `x` (under `ρ̂`) to `x^{ℓ'}` inside the body subtree of `t₀^{ℓ₀}` (under `Ĉ`),
    depicting `ρ̂(x) ⊆ Ĉ(ℓ')`;
  - Solid arrow from body root box `t₀^{ℓ₀}` to application box `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ` (under `Ĉ`),
    depicting `Ĉ(ℓ₀) ⊆ Ĉ(ℓ)`.
- Citation: [PPA Figure 3.2, p. 149] (book p. 149; PDF p. 167)

### Example 3.5 — Checking acceptability and unacceptability on Example 3.3
- Statement: Using Table 3.1 on `((fn x => x^1)^2 (fn y => y^3)^4)^5`:
  - `(Ĉ_e, ρ̂_e) ⊨ ((fn x => x^1)^2 (fn y => y^3)^4)^5` holds because `Ĉ_e(2) = {fn x => x^1}`,
    `(Ĉ_e, ρ̂_e) ⊨ (fn x => x^1)^2`, `(Ĉ_e, ρ̂_e) ⊨ (fn y => y^3)^4`, `(Ĉ_e, ρ̂_e) ⊨ x^1` (via
    `ρ̂_e(x) ⊆ Ĉ_e(1)`), `Ĉ_e(4) ⊆ ρ̂_e(x)`, and `Ĉ_e(1) ⊆ Ĉ_e(5)` (notice `(Ĉ_e, ρ̂_e) ⊨ y^3` is never
    required!).
  - `(Ĉ'_e, ρ̂'_e) ⊭ ((fn x => x^1)^2 (fn y => y^3)^4)^5` because `Ĉ'_e(4) = {fn y => y^3} ⊈ ∅ = ρ̂'_e(x)`. `■`
- Citation: [PPA Example 3.5, p. 148] (book p. 148; PDF p. 166); [PPA Example 3.5, p. 149] (book p. 149; PDF p. 167)

### [U3a:3.1.1-d] Inclusion shapes, unreachable code, flow-insensitivity, and context-insensitivity
- Statement:
  - Every inclusion in Table 3.1 has the shape `lhs ⊆ rhs` where `rhs` is `Ĉ(ℓ)` or `ρ̂(x)` and `lhs` is
    `Ĉ(ℓ)`, `ρ̂(x)`, or `{t}`.
  - Omitting `(Ĉ, ρ̂) ⊨ e₀` from `[fn]` and `[fun]` avoids analysing *unreachable* function bodies (unlike
    type inference in Chapter 5, where even unreachable fragments must type-check) and supports *open
    systems* where functions are supplied by an external environment (crucial for concurrent languages).
  - In the taxonomy of §2.5 [PPA §2.5, p. 82] (book p. 82; PDF p. 101), pure 0-CFA is *flow-insensitive*
    (`FUN` is side-effect-free, and `[app]` analyses operand `t₂^{ℓ₂}` even when `Ĉ(ℓ₁) = ∅`; see
    Exercise 3.3 [PPA Exercise 3.3, p. 206] (book p. 206; PDF p. 224) for reachability-guarded operands)
    and *context-insensitive* (all calls to a function share one formal-parameter entry `ρ̂(x)`; §3.6 adds
    context sensitivity [PPA §3.6, p. 190] (book p. 190; PDF p. 208)).
- Citation: [PPA §3.1.1, p. 149] (book p. 149; PDF p. 167); [PPA §3.1.1, p. 150] (book p. 150; PDF p. 168)

### 3.1.2 Well-definedness of the Analysis

### [U3a:3.1.2-a] Functional `𝒬` and coinductive definition `⊨ = gfp(𝒬)`
- Statement: Clause `[app]` in Table 3.1 is *not* structural-inductive on `e`: checking `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ`
  requires `(Ĉ, ρ̂) ⊨ t₀^{ℓ₀}` for every `(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁)`, where `t₀^{ℓ₀}` need not be a
  syntactic subexpression of `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ`. Following Appendix B
  [PPA Appendix B, p. 405] (book p. 405; PDF p. 421), Table 3.1 is viewed as a monotone functional:
  ```text
  𝒬 : ((Cachê × Env̂ × Exp) → {true, false}) → ((Cachê × Env̂ × Exp) → {true, false})
  ```
  (for example, `𝒬(Q)(Ĉ, ρ̂, (let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ) = Q(Ĉ, ρ̂, t₁^{ℓ₁}) ∧ Q(Ĉ, ρ̂, t₂^{ℓ₂}) ∧ Ĉ(ℓ₁) ⊆ ρ̂(x) ∧ Ĉ(ℓ₂) ⊆ Ĉ(ℓ)`)
  over the complete lattice `((Cachê × Env̂ × Exp) → {true, false}, ⊑)` ordered by implication:
  ```text
  Q₁ ⊑ Q₂   iff   ∀(Ĉ, ρ̂, e) : (Q₁(Ĉ, ρ̂, e) = true) ⇒ (Q₂(Ĉ, ρ̂, e) = true)
  ```
  Since every recursive occurrence of `Q` in Table 3.1 is positive (no negation surrounds `Q`), `𝒬` is
  monotone and Tarski's Theorem [PPA Proposition A.10, p. 402] (book p. 402; PDF p. 418) guarantees fixed
  points. Acceptability is defined *coinductively*:
  ```text
  ⊨  is the greatest fixed point of 𝒬   (⊨ = gfp(𝒬))
  ```
- Citation: [PPA §3.1.2, p. 150] (book p. 150; PDF p. 168); [PPA §3.1.2, p. 151] (book p. 151; PDF p. 169)

### Example 3.6 — Circularity on `loop` resolved by coinduction
- Statement: Verifying `(Ĉ_lp, ρ̂_lp) ⊨ loop` (Examples 3.2 and 3.4) unfolds `[let]`, `[fun]`, and `[app]`
  at `(g^6 (fn z => z^7)^8)^9` (`Ĉ_lp(6) = {f}`), which requires verifying the body of `f`:
  `(Ĉ_lp, ρ̂_lp) ⊨ (f^1 (fn y => y^2)^3)^4`. Since `Ĉ_lp(1) = {f}`, `[app]` requires verifying the exact
  same subgoal `(Ĉ_lp, ρ̂_lp) ⊨ (f^1 (fn y => y^2)^3)^4`! Coinduction (`gfp(𝒬)`) resolves this circularity
  by assuming the obligation at the inner level and establishing it at the outer level (formally choosing an
  extensive relation `Q ⊑ 𝒬(Q)` (`[external: post-fixed point]`) containing the circular triple `[derived]`), whereas the inductive
  interpretation `lfp(𝒬)` has no finite base derivation for the infinite recursion. `■`
- Citation: [PPA Example 3.6, p. 151] (book p. 151; PDF p. 169)

### [U3a:3.1.2-b] `Analogy.` — Procurement specification (`gfp`) vs cheapest bid (`lfp`) (unnumbered remark)
- Statement: A company procuring computers writes a loose specification (`⊨`) so all compliant vendors can
  bid; in arbitration the company can reject a vendor *only* by demonstrating violation of an explicit
  demand in the specification. Under a silly circular specification `(C, ρ) ⊨ P iff (C, ρ) ⊨ P`, *every*
  `(C, ρ)` satisfies the specification — captured *only* by the coinductive `gfp` (`true` everywhere),
  whereas the inductive `lfp` (`false` everywhere) accepts nothing at all. Once the loose acceptability
  universe is defined via `gfp(𝒬)`, choosing the best (cheapest / most precise) compliant bid `(Ĉ, ρ̂)` is a
  separate minimisation solved by *least* fixed points (`lfp`) in §3.4.2.
- Citation: [PPA §3.1.2, p. 152] (book p. 152; PDF p. 170)

### Findings (3.1)
- F-U3a-01: On p. 142, the motivating `let` snippet writes semicolon-separated multi-bindings
  `let f = ...; g = ...; h = ... in ...`, whereas the formal `FUN` grammar on p. 142 provides only
  single-binding `let x = e₁ in e₂` (multi-binding is informal syntactic sugar for nested `let`). Recorded
  as printed. [PPA §3.1, p. 142] (book p. 142; PDF p. 160)
- F-U3a-02: On p. 146, the prose under Table 3.1 prints `"a proposed guess (Ĉ, ρ̂) of an analysis results"`
  (singular/plural mismatch) and `"whether or not a a guess is indeed"` (doubled article `"a a"`). Recorded
  as printed. [PPA §3.1.1, p. 146] (book p. 146; PDF p. 164)

### Projections (3.1)
- cs_theory: Defining acceptability `⊨ = gfp(𝒬)` over `Cachê × Env̂ × Exp → {true, false}` while later
  computing the best solution `(Ĉ, ρ̂) = lfp(F_⋆)` over `Cachê_⋆ × Env̂_⋆` cleanly separates *relational
  specification* (coinduction over potentially cyclic dynamic call chains) from *abstract-domain
  minimisation* (induction over subset constraints) [PPA §3.1.2, p. 152] (book p. 152; PDF p. 170).
- swe_architecture: `Cachê` + `Env̂` is the minimal data model for any AST-indexed points-to / closure-flow
  engine [external: Andersen-style / Shivers 0-CFA]: `Cachê` maps expression node IDs to abstract callable
  values while `Env̂` maps symbol IDs to abstract callable values; distinct bindings should be resolved to
  unique symbol IDs (`α`-renaming) before running 0-CFA so unrelated local variables named `x` do not
  pollute one another [PPA §3.1.1, p. 144] (book p. 144; PDF p. 162).
- practical_debugging: Notice in Example 3.3 that `Ĉ_e(3) = ρ̂_e(y) = ∅` even though `fn y => y^3` flows
  through `x` to the program result `Ĉ_e(5)`: in demand-driven / reachability-aware 0-CFA (Table 3.1), an
  uncalled closure's body has empty cache sets, whereas syntax-directed 0-CFA (Table 3.5) still analyses
  `y^3` (which remains `∅` only because `ρ̂_e(y) = ∅`, and would become non-empty if `y^3` contained a
  nested `fn z => ...`!) [derived] [PPA Example 3.3, p. 144] (book p. 144; PDF p. 162).
- cyber: §3.1.1 (p. 145) directly governs static call-graph recovery for indirect calls (`fptr(arg)` in C,
  callbacks in JS/Python, virtual dispatch / reflection / deserialization `readObject` trampolines `[external: CWE-502]`): any sound reachability or taint scanner `[external]` must over-approximate `Ĉ(ℓ₁)`
  at every indirect call site before interprocedural edges exist [PPA §3.1.1, p. 145] (book p. 145; PDF p. 163).

## 3.2 Theoretical Properties

Context: Section 3.2 equips `FUN` with an explicit-environment small-step Structural Operational Semantics
(Tables 3.2 and 3.3), extends acceptability `⊨` to intermediate expressions (Table 3.4), proves semantic
correctness as a subject-reduction theorem (Theorem 3.10), proves that acceptable solutions form a Moore
family so every program has a least 0-CFA solution (Proposition 3.13), and proves via `Ω` self-application
that replacing `gfp(𝒬)` with `lfp(𝒬)` destroys the Moore-family property (Proposition 3.16)
[PPA §3.2, p. 153] (book p. 153; PDF p. 171).

### 3.2.1 Structural Operational Semantics

### [U3a:3.2.1-a] Explicit environments, closures, and intermediate syntax (`Val`, `Env`, `IExp`, `ITerm`)
- Statement: Substitution-based β-reduction (`e₀[x ↦ v₂]`) fails to preserve the syntactic identity and
  labels of functions (duplicating/mutating subterms inside `e₀`, as revisited in Concluding Remarks
  [PPA Chapter 3, p. 201] (book p. 201; PDF p. 219)). Instead, `FUN` uses explicit environments and
  closures:
  ```text
  v ∈ Val   values         v ::= c | close t in ρ
  ρ ∈ Env   environments   ρ ::= [] | ρ[x ↦ v]
  ```
  Wait-free finite environment lists support `dom(ρ)`, rightmost-wins lookup `ρ(x)`, extension `ρ[x ↦ v]`,
  and restriction `ρ | X` to `X ⊆ Var`. Because closures `close t in ρ` and local environment scopes arise
  dynamically inside subexpressions during small-step evaluation, `Exp` and `Term` are extended to
  *intermediate expressions* `ie ∈ IExp` and *intermediate terms* `it ∈ ITerm`:
  ```text
  ie ::= it^ℓ
  it ::= c | x | fn x => e₀ | fun f x => e₀
       | ie₁ ie₂ | if ie₀ then e₁ else e₂ | let x = ie₁ in e₂ | ie₁ op ie₂
       | bind ρ in ie
       | close t in ρ
  ```
  Note carefully: bodies inside `fn x => e₀`, `fun f x => e₀`, and `close t in ρ` remain *ordinary* source
  `e₀ ∈ Exp` and `t ∈ Term` (`Term ⊆ ITerm`, `Exp ⊆ IExp`), so `close t in ρ` is a finite non-cyclic syntax
  tree; `Val` is identified with the unlabelled value subset of `ITerm`, and `v^ℓ` denotes a labelled value.
  Small-step transitions have the judgement form `ρ ⊢ ie₁ → ie₂` (defined in Tables 3.2 and 3.3).
- Citation: [PPA §3.2.1, p. 153] (book p. 153; PDF p. 171); [PPA §3.2.1, p. 154] (book p. 154; PDF p. 172)

### Table 3.2 — Structural Operational Semantics for `FUN` (part 1)
- Statement: Variable lookup, closure creation, application rules, and local binding frames:
  ```text
  [var]     ρ ⊢ x^ℓ → v^ℓ                          if x ∈ dom(ρ) and v = ρ(x)

  [fn]      ρ ⊢ (fn x => e₀)^ℓ → (close (fn x => e₀) in ρ₀)^ℓ
                where ρ₀ = ρ | FV(fn x => e₀)

  [fun]     ρ ⊢ (fun f x => e₀)^ℓ → (close (fun f x => e₀) in ρ₀)^ℓ
                where ρ₀ = ρ | FV(fun f x => e₀)

                  ρ ⊢ ie₁ → ie'₁
  [app₁]    ---------------------------
            ρ ⊢ (ie₁ ie₂)^ℓ → (ie'₁ ie₂)^ℓ

                  ρ ⊢ ie₂ → ie'₂
  [app₂]    ---------------------------
            ρ ⊢ (v₁^ℓ₁ ie₂)^ℓ → (v₁^ℓ₁ ie'₂)^ℓ

  [app_fn]  ρ ⊢ ((close (fn x => e₁) in ρ₁)^ℓ₁ v₂^ℓ₂)^ℓ → (bind ρ₁[x ↦ v₂] in e₁)^ℓ

  [app_fun] ρ ⊢ ((close (fun f x => e₁) in ρ₁)^ℓ₁ v₂^ℓ₂)^ℓ
                → (bind ρ₂[x ↦ v₂] in e₁)^ℓ
                where ρ₂ = ρ₁[f ↦ close (fun f x => e₁) in ρ₁]

                        ρ₁ ⊢ ie₁ → ie'₁
  [bind₁]   -----------------------------------------
            ρ ⊢ (bind ρ₁ in ie₁)^ℓ → (bind ρ₁ in ie'₁)^ℓ

  [bind₂]   ρ ⊢ (bind ρ₁ in v₁^ℓ₁)^ℓ → v₁^ℓ
  ```
- Side conditions:
  - Evaluation is strict left-to-right call-by-value (`[app₁]` reduces operator `ie₁` to `v₁^{ℓ₁}` before
    `[app₂]` reduces argument `ie₂` to `v₂^{ℓ₂}`).
  - `[fn]` and `[fun]` restrict the captured environment `ρ₀` to free variables `FV(fn x => e₀)` and
    `FV(fun f x => e₀)` (trimming `x` and `f, x` respectively), ensuring every environment captured inside a
    closure was constructed strictly earlier (well-foundedness for Lemma 3.14).
  - In `[app_fun]`, `ρ₁` is extended **first** with `[f ↦ close (fun f x => e₁) in ρ₁]` (`ρ₂`) and **second**
    with `[x ↦ v₂]` (`ρ₂[x ↦ v₂]` has `[x ↦ v₂]` rightmost), so on a degenerate definition `fun x x => e₁`
    the formal parameter `x` takes precedence `[derived]`.
  - In `[bind₂]`, the inner value label `ℓ₁` is replaced by the outer `bind` label `ℓ` (`v₁^{ℓ₁} → v₁^ℓ`),
    which is why `Fact 3.11` (re-labelling monotonicity) is used in Theorem 3.10.
- Citation: [PPA Table 3.2, p. 155] (book p. 155; PDF p. 173)

### Table 3.3 — Structural Operational Semantics for `FUN` (part 2)
- Statement: Conditional, local `let`, and binary operator rules (with bold semantic `**op**` in `[op₃]`):
  ```text
                        ρ ⊢ ie₀ → ie'₀
  [if₁]   ---------------------------------------------------
          ρ ⊢ (if ie₀ then e₁ else e₂)^ℓ → (if ie'₀ then e₁ else e₂)^ℓ

  [if₂]   ρ ⊢ (if true^ℓ₀ then t₁^ℓ₁ else e₂)^ℓ → t₁^ℓ

  [if₃]   ρ ⊢ (if false^ℓ₀ then e₁ else t₂^ℓ₂)^ℓ → t₂^ℓ

                        ρ ⊢ ie₁ → ie'₁
  [let₁]  ---------------------------------------------
          ρ ⊢ (let x = ie₁ in e₂)^ℓ → (let x = ie'₁ in e₂)^ℓ

  [let₂]  ρ ⊢ (let x = v^ℓ₁ in e₂)^ℓ → (bind ρ₀[x ↦ v] in e₂)^ℓ
              where ρ₀ = ρ | FV(e₂)

                 ρ ⊢ ie₁ → ie'₁
  [op₁]   -------------------------------
          ρ ⊢ (ie₁ op ie₂)^ℓ → (ie'₁ op ie₂)^ℓ

                 ρ ⊢ ie₂ → ie'₂
  [op₂]   -------------------------------
          ρ ⊢ (v₁^ℓ₁ op ie₂)^ℓ → (v₁^ℓ₁ op ie'₂)^ℓ

  [op₃]   ρ ⊢ (v₁^ℓ₁ op v₂^ℓ₂)^ℓ → v^ℓ      if v = v₁ **op** v₂ (and v ∈ Const)
  ```
- Side conditions:
  - In `[if₂]` and `[if₃]`, note carefully that the selected branch subterm is **relabelled to the outer `if`
    label `ℓ`** (`t₁^{ℓ₁} → t₁^ℓ` and `t₂^{ℓ₂} → t₂^ℓ`); as explicitly highlighted on p. 157: *"the outermost
    label never changes while inner labels may disappear; see for example the rules `[if₂]` and `[bind₂]`."*
    Thus in `Theorem 3.10`, `Fact 3.11` handles `[if₂]`, `[if₃]`, and `[bind₂]` directly (`Ĉ(ℓ₁) ⊆ Ĉ(ℓ)` /
    `Ĉ(ℓ₂) ⊆ Ĉ(ℓ)` from Table 3.1/3.4 `[if]`/`[bind]`) and congruence rules (`[app₁]`, `[if₁]`, `[let₁]`)
    preserve top labels without any proof gap!
  - In `[let₂]`, `ρ₀ = ρ | FV(e₂)` restricts to `FV(e₂)` rather than `FV(let x = e₁ in e₂) = FV(e₁) ∪ (FV(e₂) \ {x})`,
    retaining any outer binding of `x` underneath `[x ↦ v]` when `x ∈ FV(e₂) ∩ dom(ρ)`.
  - `[op₃]` requires `v = v₁ **op** v₂ ∈ Const` (confirming `op` returns constants, never closures); stuck
    configurations (such as applying a constant `(3 4)^ℓ` or `if 5 then ...`) simply have no outgoing
    transition.
- Citation: [PPA Table 3.3, p. 156] (book p. 156; PDF p. 174)

### Example 3.7 — Small-step SOS trace of Example 3.1
- Statement: Evaluating `((fn x => x^1)^2 (fn y => y^3)^4)^5` in `[]` takes 5 steps (`[app₁]`/`[fn]`,
  `[app₂]`/`[fn]`, `[app_fn]`, `[bind₁]`/`[var]`, `[bind₂]`):
  ```text
  [] ⊢ ((fn x => x^1)^2 (fn y => y^3)^4)^5
     → ((close (fn x => x^1) in [])^2 (fn y => y^3)^4)^5
     → ((close (fn x => x^1) in [])^2 (close (fn y => y^3) in [])^4)^5
     → (bind [x ↦ close (fn y => y^3) in []] in x^1)^5
     → (bind [x ↦ close (fn y => y^3) in []] in (close (fn y => y^3) in [])^1)^5
     → (close (fn y => y^3) in [])^5
  ```
  `■`
- Citation: [PPA Example 3.7, p. 156] (book p. 156; PDF p. 174); [PPA Example 3.7, p. 157] (book p. 157; PDF p. 175)

### Example 3.8 — Infinite small-step SOS trace of `loop` (Example 3.2)
- Statement: Writing `f = fun f x => (f^1 (fn y => y^2)^3)^4`, `id_y = fn y => y^2`, `id_z = fn z => z^7`,
  `ρ_g = [g ↦ close f in []]`, `ρ₁ = [f ↦ close f in []][x ↦ close id_z in []]`, and
  `ρ₂ = [f ↦ close f in []][x ↦ close id_y in []]` (`[x ↦ ...]` rightmost, matching `[app_fun]`),
  `[] ⊢ loop` steps via `[let₁]`/`[fun]`, `[let₂]`, `[bind₁]`×3 (`[var]`, `[fn]`, `[app_fun]`), and
  subsequent `[bind₁]` steps inside `ρ₁` into nested `bind ρ₂ in (f^1 id_y^3)^4` frames ad infinitum:
  ```text
  [] ⊢ loop
     → (let g = (close f in [])^5 in (g^6 id_z^8)^9)^10
     → (bind ρ_g in (g^6 id_z^8)^9)^10
     →* (bind ρ_g in (bind ρ₁ in (f^1 id_y^3)^4)^9)^10
     →* (bind ρ_g in (bind ρ₁ in (bind ρ₂ in (f^1 id_y^3)^4)^4)^9)^10
     → ···
  ```
  `■`
- Citation: [PPA Example 3.8, p. 157] (book p. 157; PDF p. 175)

### 3.2.2 Semantic Correctness

### Table 3.4 — Abstract Control Flow Analysis for intermediate expressions
- Statement: Extending `(Ĉ, ρ̂) ⊨ ie` (`⊨ : Cachê × Env̂ × IExp → {true, false}`, coinductively as `gfp` of
  the extended functional) by keeping all clauses of Table 3.1 (with `ie`/`it` replacing `e`/`t` in outer
  syntax) and adding:
  ```text
  [bind]   (Ĉ, ρ̂) ⊨ (bind ρ in it₀^{ℓ₀})^ℓ
               iff  (Ĉ, ρ̂) ⊨ it₀^{ℓ₀}  ∧  Ĉ(ℓ₀) ⊆ Ĉ(ℓ)  ∧  ρ ℛ ρ̂

  [close]  (Ĉ, ρ̂) ⊨ (close t₀ in ρ)^ℓ
               iff  {t₀} ⊆ Ĉ(ℓ)  ∧  ρ ℛ ρ̂
  ```
- Side conditions:
  - Just like `[fn]` and `[fun]`, `[close]` does *not* require `(Ĉ, ρ̂) ⊨ e₀` for the body inside `t₀`; body
    acceptability is checked by `[app]` only if `t₀ ∈ Ĉ(ℓ₁)` reaches an application operator.
- Citation: [PPA Table 3.4, p. 158] (book p. 158; PDF p. 176)

### [U3a:3.2.2-a] Well-founded correctness relations `ρ ℛ ρ̂` and `v 𝒱 (ρ̂, v̂)`
- Statement: Global abstract environment `ρ̂` models every local concrete environment `ρ` via
  `ℛ : (Env × Env̂) → {true, false}`:
  ```text
  ρ ℛ ρ̂   iff   dom(ρ) ⊆ dom(ρ̂)  ∧  ∀x ∈ dom(ρ) ∀t_x ∀ρ_x :
                    (ρ(x) = close t_x in ρ_x) ⇒ (t_x ∈ ρ̂(x) ∧ ρ_x ℛ ρ̂)
  ```
  Equivalently, splitting out `𝒱 : (Val × (Env̂ × Val̂)) → {true, false}` by mutual recursion:
  ```text
  v 𝒱 (ρ̂, v̂)   iff   ∀t ∀ρ : (v = close t in ρ) ⇒ (t ∈ v̂ ∧ ρ ℛ ρ̂)
  ρ ℛ ρ̂        iff   dom(ρ) ⊆ dom(ρ̂)  ∧  ∀x ∈ dom(ρ) : ρ(x) 𝒱 (ρ̂, ρ̂(x))
  ```
- Side conditions:
  - `ℛ` is well-founded (no coinduction required!) because every recursive appeal `ρ_x ℛ ρ̂` acts on an
    environment `ρ_x` captured strictly earlier when `close t_x in ρ_x` was constructed (syntax trees of
    `Val` and `Env` are finite).
  - Since `Env̂ = Var → Val̂` is a total function space, `dom(ρ̂) = Var`, making `dom(ρ) ⊆ dom(ρ̂)`
    automatically true on `Env̂`, whereas on restricted `Env̂_⋆ = Var_⋆ → Val̂_⋆` in §§3.3–3.4 it enforces
    `dom(ρ) ⊆ Var_⋆` `[derived]`.
  - For any constant `c ∈ Const`, `c 𝒱 (ρ̂, v̂)` holds vacuously for every `v̂` (even `v̂ = ∅`).
- Citation: [PPA §3.2.2, p. 158] (book p. 158; PDF p. 176); [PPA §3.2.2, p. 159] (book p. 159; PDF p. 177)

### Example 3.9 — Unfolding `ρ ℛ ρ̂` on nested closures
- Statement: For `ρ = [x ↦ close t₁ in ρ₁][y ↦ close t₂ in ρ₂]` with `ρ₁ = []`, `ρ₂ = [x ↦ close t₃ in ρ₃]`,
  and `ρ₃ = []`, the relation `ρ ℛ ρ̂` simplifies to `{t₁, t₃} ⊆ ρ̂(x) ∧ {t₂} ⊆ ρ̂(y)`. `■`
- Citation: [PPA Example 3.9, p. 159] (book p. 159; PDF p. 177)

### Figure 3.3 — Preservation of analysis result
- Statement: Commuting invariant diagram over a multi-step evaluation trace
  `ρ ⊢ ie → ie' → ie'' → ··· → v^ℓ`: vertical double-headed arrows connect `ρ` to `ρ̂` via `ℛ` and connect
  each intermediate configuration `ie`, `ie'`, `ie''`, ..., `v^ℓ` to the *same* fixed pair `(Ĉ, ρ̂)` via `⊨`,
  analogous to Corollary 2.17 for Live Variables Analysis in Chapter 2
  [PPA Corollary 2.17, p. 61] (book p. 61; PDF p. 80).
- Citation: [PPA Figure 3.3, p. 159] (book p. 159; PDF p. 177)

### Theorem 3.10 — Subject reduction (semantic correctness of abstract 0-CFA)
- Statement:
  `If ρ ℛ ρ̂ and ρ ⊢ ie → ie' then (Ĉ, ρ̂) ⊨ ie implies (Ĉ, ρ̂) ⊨ ie'.`
- Citation: [PPA Theorem 3.10, p. 159] (book p. 159; PDF p. 177)

### Fact 3.11 — Monotonicity of acceptability under label-cache inclusion
- Statement:
  `If (Ĉ, ρ̂) ⊨ it^{ℓ₁} and Ĉ(ℓ₁) ⊆ Ĉ(ℓ₂) then (Ĉ, ρ̂) ⊨ it^{ℓ₂}.` `■`
- Side conditions: Note that the printed statement writes `it^{ℓ₁}` and `it^{ℓ₂}` (same unlabelled
  intermediate term `it` under two labels `ℓ₁` and `ℓ₂`), and the OCR text layer of `ppa.pdf` completely
  drops the body between `Fact 3.11` and `■` on p. 160! Notice `Fact 3.11` suffices directly for `[bind₂]`,
  `[if₂]`, and `[if₃]` in Theorem 3.10 because Tables 3.2 and 3.3 preserve the outermost label on every
  step (`p. 157`: `[if₂]`/`[if₃]` relabel `t₁^{ℓ₁} → t₁^ℓ` and `t₂^{ℓ₂} → t₂^ℓ`, and `[bind₂]` relabels
  `v₁^{ℓ₁} → v₁^ℓ`).
- Citation: [PPA Fact 3.11, p. 160] (book p. 160; PDF p. 178)

### [U3a:3.2.2-b] Proof of Theorem 3.10 (structural induction on `ρ ⊢ ie → ie'`)
- Statement: By induction on the derivation tree of `ρ ⊢ ie → ie'`, illustrating four representative cases
  `[fn]`, `[app₁]`, `[app_fn]`, and `[bind₂]` (and leaving remaining rules, including `[if₂]`/`[if₃]` using
  `Fact 3.11` and static-scoping / α-renaming invariance, to Exercise 3.7
  [PPA Exercise 3.7, p. 207] (book p. 207; PDF p. 225)):
  1. `[fn]`: `ρ ⊢ (fn x => e₀)^ℓ → (close (fn x => e₀) in ρ₀)^ℓ` with `ρ₀ = ρ | FV(fn x => e₀)`. From
     `(Ĉ, ρ̂) ⊨ ie` we have `fn x => e₀ ∈ Ĉ(ℓ)`; from `ρ ℛ ρ̂` restriction preserves `ρ₀ ℛ ρ̂`; hence `[close]`
     gives `(Ĉ, ρ̂) ⊨ ie'`.
  2. `[app₁]`: `ρ ⊢ (ie₁ ie₂)^ℓ → (ie'₁ ie₂)^ℓ` from `ρ ⊢ ie₁ → ie'₁`. Since every SOS step preserves the
     outermost label (`p. 157`), `ie₁` and `ie'₁` share the exact same outer label `ℓ₁`; by induction
     hypothesis `(Ĉ, ρ̂) ⊨ ie'₁`, and the remaining defining clauses of `(Ĉ, ρ̂) ⊨ (ie'₁ ie₂)^ℓ` are unchanged.
  3. `[app_fn]`: `ρ ⊢ ((close (fn x => t₀^{ℓ₀}) in ρ₁)^{ℓ₁} v₂^{ℓ₂})^ℓ → (bind ρ₁[x ↦ v₂] in t₀^{ℓ₀})^ℓ`.
     From `[close]` on the operator: `(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁)` and `ρ₁ ℛ ρ̂`. From `(Ĉ, ρ̂) ⊨ v₂^{ℓ₂}`:
     either `v₂ = c` (so `v₂ 𝒱 (ρ̂, Ĉ(ℓ₂))` trivially) or `v₂ = close t₂ in ρ₂` (so `[close]` gives
     `t₂ ∈ Ĉ(ℓ₂)` and `ρ₂ ℛ ρ̂`, hence `v₂ 𝒱 (ρ̂, Ĉ(ℓ₂))`). Instantiating `[app]` at `(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁)`
     gives `(Ĉ, ρ̂) ⊨ t₀^{ℓ₀}`, `Ĉ(ℓ₂) ⊆ ρ̂(x)`, and `Ĉ(ℓ₀) ⊆ Ĉ(ℓ)`. Monotonicity of `𝒱` in its second
     component yields `v₂ 𝒱 (ρ̂, ρ̂(x))`, so `ρ₁[x ↦ v₂] ℛ ρ̂`, and `[bind]` gives `(Ĉ, ρ̂) ⊨ ie'`.
  4. `[bind₂]`: `ρ ⊢ (bind ρ₁ in v₁^{ℓ₁})^ℓ → v₁^ℓ`. `[bind]` gives `(Ĉ, ρ̂) ⊨ v₁^{ℓ₁}` and `Ĉ(ℓ₁) ⊆ Ĉ(ℓ)`,
     so `Fact 3.11` gives `(Ĉ, ρ̂) ⊨ v₁^ℓ`. `■`
- Citation: [PPA §3.2.2, p. 160] (book p. 160; PDF p. 178); [PPA §3.2.2, p. 161] (book p. 161; PDF p. 179)

### 3.2.3 Existence of Solutions

### [U3a:3.2.3-a] Complete lattice `(Cachê × Env̂, ⊑)` and trivial top analysis
- Statement: Pointwise subset ordering equips `Val̂ = 𝒫(Term)`, `Cachê = Lab → Val̂`, `Env̂ = Var → Val̂`, and
  `Cachê × Env̂` with complete-lattice structure (cf. Appendix A
  [PPA §A.2, p. 397] (book p. 397; PDF p. 413)):
  ```text
  v̂₁ ⊑ v̂₂   iff  v̂₁ ⊆ v̂₂          ⨅ Y = ⋂ {v̂ | v̂ ∈ Y}    (⨅ ∅ = Term)
  ρ̂₁ ⊑ ρ̂₂   iff  ∀x : ρ̂₁(x) ⊆ ρ̂₂(x)   (⨅ Y)(x) = ⨅ {ρ̂(x) | ρ̂ ∈ Y}
  Ĉ₁ ⊑ Ĉ₂   iff  ∀ℓ : Ĉ₁(ℓ) ⊆ Ĉ₂(ℓ)   (⨅ Y)(ℓ) = ⨅ {Ĉ(ℓ) | Ĉ ∈ Y}
  (Ĉ₁, ρ̂₁) ⊑ (Ĉ₂, ρ̂₂)  iff  (Ĉ₁ ⊑ Ĉ₂) ∧ (ρ̂₁ ⊑ ρ̂₂)
  ⨅ Y = (⨅ {Ĉ | (Ĉ, ρ̂) ∈ Y}, ⨅ {ρ̂ | (Ĉ, ρ̂) ∈ Y})
  ```
  Greatest element `⊤ = ((λℓ. Term), (λx. Term))` (always acceptable for every `ie ∈ IExp`!) and least
  element `⊥ = ((λℓ. ∅), (λx. ∅))` (more informative are smaller elements under `⊑`). Recall from §A.2 that
  `Y ⊆ L` is a *Moore family* iff `∀Y' ⊆ Y : ⨅ Y' ∈ Y` (which is always *non-empty* because `Y' = ∅` puts
  `⨅ ∅ = ⊤ ∈ Y`, and always contains a unique least element `⨅ Y ∈ Y`).
- Citation: [PPA §3.2.3, p. 162] (book p. 162; PDF p. 180)

### Example 3.12 — Checking Theorem 3.10 on Example 3.7 (SOS evaluation vs acceptability)
- Statement: In `Example 3.7`, evaluating the program of `Example 3.1` under empty environment `[]` reaches
  `(close (fn y => y^3) in [])^5` via `[] ⊢ ((fn x => x^1)^2 (fn y => y^3)^4)^5 →* (close (fn y => y^3) in [])^5`.
  Taking the acceptable analysis `(Ĉ_e, ρ̂_e)` from `Example 3.3` (which satisfies `(Ĉ_e, ρ̂_e) ⊨ e`), repeated
  application of `Theorem 3.10` yields `(Ĉ_e, ρ̂_e) ⊨ (close (fn y => y^3) in [])^5`, matching `Table 3.4`
  `[close]` (`Ĉ_e(5) = {fn y => y^3}` and `[] ℛ ρ̂_e`). Note also that in `§3.2.3` prose on p. 162, the
  authors illustrate a Moore family on `𝒫({1, 2, 3})` (`{{1}, {1, 2}, {1, 3}, {1, 2, 3}}` is a Moore family,
  whereas `{{1, 2}, {1, 3}, {1, 2, 3}}` lacks `{1, 2} ∩ {1, 3} = {1}`). `■`
- Citation: [PPA Example 3.12, p. 162] (book p. 162; PDF p. 180)

### Proposition 3.13 — Moore family property of acceptable 0-CFA analyses
- Statement:
  `For all ie ∈ IExp the set {(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨ ie} is a Moore family.`
  Immediate corollaries: every `ie ∈ IExp` admits at least one acceptable 0-CFA (`⨅ ∅ = ⊤`), and every
  `ie ∈ IExp` admits a unique *least* (most precise) acceptable 0-CFA `⨅ {(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨ ie}`.
- Citation: [PPA Proposition 3.13, p. 163] (book p. 163; PDF p. 181)

### Lemma 3.14 — Moore family property for `ℛ` and `𝒱`
- Statement:
  1. `(i)` `For all ρ ∈ Env the set {ρ̂ | ρ ℛ ρ̂} is a Moore family.`
  2. `(ii)` `For all v ∈ Val the set {(ρ̂, v̂) | v 𝒱 (ρ̂, v̂)} is a Moore family.` `■`
  (Proved by well-founded induction on `ρ` for `(i)` and direct unfolding of `𝒱` for `(ii)`.)
- Citation: [PPA Lemma 3.14, p. 163] (book p. 163; PDF p. 181)

### [U3a:3.2.3-b] Coinductive proof of Proposition 3.13 and display `(3.1)`
- Statement: Let `∀i ∈ I : (Ĉ_i, ρ̂_i) ⊨ ie`. Define `Q'` by `(Ĉ', ρ̂') Q' ie'` iff
  `(Ĉ', ρ̂') = ⨅_i (Ĉ_i, ρ̂_i) ∧ ∀i ∈ I : (Ĉ_i, ρ̂_i) ⊨ ie'`. To conclude `Q' ⊑ gfp(𝒬) = ⊨` by coinduction
  [PPA Appendix B, p. 415] (book p. 415; PDF p. 431), verify `Q' ⊑ 𝒬(Q')` by cases on `ie'`. For the crucial
  case `ie' = (it₁^{ℓ₁} it₂^{ℓ₂})^ℓ` and any `(fn x => t₀^{ℓ₀}) ∈ ⋂_i (Ĉ_i(ℓ₁))`, `(fn x => t₀^{ℓ₀}) ∈ Ĉ_i(ℓ₁)`
  holds for *every* `i ∈ I` (including vacuously when `I = ∅`, since `⋂_∅ = Term` and `Ĉ_i` ranges over
  empty index set), giving `(3.1)`:
  ```text
  ⋂_i (Ĉ_i(ℓ₂)) ⊆ ⋂_i (ρ̂_i(x)),   ⋂_i (Ĉ_i(ℓ₀)) ⊆ ⋂_i (Ĉ_i(ℓ)),   ⨅_i (Ĉ_i, ρ̂_i) Q' t₀^{ℓ₀}      (3.1)
  ```
  (Why `[app]` preserves arbitrary meets: the premise `(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁)` sits on the *left* of `⇒`!
  Intersecting `Ĉ_i(ℓ₁)` shrinks the trigger set so every surviving `t` triggered *every* `i ∈ I`.) `■`
- Citation: [PPA §3.2.3, p. 163] (book p. 163; PDF p. 181); [PPA §3.2.3, p. 164] (book p. 164; PDF p. 182)

### Example 3.15 — Intersection of two incomparable over-approximations yields `(Ĉ_e, ρ̂_e)`
- Statement: On `((fn x => x^1)^2 (fn y => y^3)^4)^5`, define two incomparable acceptable analyses
  `(Ĉ'_e, ρ̂'_e)` (note: reuses the symbol `(Ĉ'_e, ρ̂'_e)` from Example 3.3 with a *different* table!) and
  `(Ĉ''_e, ρ̂''_e)` alongside `(Ĉ_e, ρ̂_e)`:

  | Entry | `(Ĉ_e, ρ̂_e)` | `(Ĉ'_e, ρ̂'_e)` | `(Ĉ''_e, ρ̂''_e)` |
  | :--- | :--- | :--- | :--- |
  | `1` | `{fn y => y^3}` | `{fn y => y^3}` | `{fn y => y^3}` |
  | `2` | `{fn x => x^1}` | `{fn x => x^1}` | `{fn x => x^1}` |
  | `3` | `∅` | `{fn x => x^1}` | `{fn y => y^3}` |
  | `4` | `{fn y => y^3}` | `{fn y => y^3}` | `{fn y => y^3}` |
  | `5` | `{fn y => y^3}` | `{fn y => y^3}` | `{fn y => y^3}` |
  | `x` | `{fn y => y^3}` | `{fn y => y^3}` | `{fn y => y^3}` |
  | `y` | `∅` | `{fn x => x^1}` | `{fn y => y^3}` |

  Both `(Ĉ'_e, ρ̂'_e)` and `(Ĉ''_e, ρ̂''_e)` satisfy `⊨`, and their meet `(Ĉ'_e ⊓ Ĉ''_e, ρ̂'_e ⊓ ρ̂''_e)` equals
  the least solution `(Ĉ_e, ρ̂_e)`. `■`
- Citation: [PPA Example 3.15, p. 164] (book p. 164; PDF p. 182); [PPA Example 3.15, p. 165] (book p. 165; PDF p. 183)

### 3.2.4 Coinduction versus Induction

### Proposition 3.16 — Failure of the Moore family property for inductive `⊨' = lfp(𝒬)`
- Statement:
  `There exists e_⋆ ∈ Exp such that {(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨' e_⋆} is not a Moore family.`
- Proof sketch (as printed on pp. 165–167):
  Take the single-label (`Lab_e = {ℓ}`), single-variable (`Var_e = {x}`) self-application `Ω` [external]:
  ```text
  e_⋆ = t_⋆^ℓ,    t_⋆ = (fn x => (x^ℓ x^ℓ)^ℓ)^ℓ (fn x => (x^ℓ x^ℓ)^ℓ)^ℓ
  ```
  Restrict domains to `Term_e = {t_⋆, fn x => (x^ℓ x^ℓ)^ℓ, x^ℓ x^ℓ, x}`, `Exp_e = {t^ℓ | t ∈ Term_e}`
  (misprinted `IExp_e` on p. 165; see `F-U3a-07`), and `Val̂_e = 𝒫({fn x => (x^ℓ x^ℓ)^ℓ})` (2 elements: `∅`
  and `{fn x => (x^ℓ x^ℓ)^ℓ}`). Unfolding `Q = 𝒬(Q)` across the 4 expressions in `Exp_e` reduces fixed points
  to the condition on `(x^ℓ x^ℓ)^ℓ`:
  ```text
  (Ĉ, ρ̂) Q_i (x^ℓ x^ℓ)^ℓ   iff   ρ̂(x) = Ĉ(ℓ)  ∧  (Ĉ(ℓ) ≠ ∅ ⇒ (Ĉ, ρ̂) Q_i (x^ℓ x^ℓ)^ℓ)
  ```
  Among the four candidate predicates `Q₁..Q₄` on the 2-element diagonal `Ĉ(ℓ) = ρ̂(x)`:
  - `Q₁`: `Ĉ(ℓ) = ρ̂(x)` (fixed point; `Q₁ = gfp(𝒬) = ⊨`);
  - `Q₂`: `Ĉ(ℓ) = ρ̂(x) = ∅` (fixed point; `Q₂ = lfp(𝒬) = ⊨'`);
  - `Q₃`: `Ĉ(ℓ) = ρ̂(x) ≠ ∅` (fails at `∅`);
  - `Q₄`: `false` (fails at `∅`).
  Evaluating at `e_⋆ = t_⋆^ℓ` requires `{fn x => (x^ℓ x^ℓ)^ℓ} = Ĉ(ℓ) = ρ̂(x) ∧ (Ĉ, ρ̂) Q_i (x^ℓ x^ℓ)^ℓ`:
  - Under coinductive `Q₁ = ⊨`: `{(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨ e_⋆} = {(Ĉ, ρ̂) | Ĉ(ℓ) = ρ̂(x) = {fn x => (x^ℓ x^ℓ)^ℓ}}`,
    a singleton Moore family.
  - Under inductive `Q₂ = ⊨'`: `(Ĉ, ρ̂) Q₂ t_⋆^ℓ iff false`, so `{(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨' e_⋆} = ∅`, which is
    *not* a Moore family (since every Moore family contains `⨅ ∅ = ⊤` and is never empty!). `■`
- Citation: [PPA Proposition 3.16, p. 165] (book p. 165; PDF p. 183); [PPA Proposition 3.16, p. 166] (book p. 166; PDF p. 184); [PPA Proposition 3.16, p. 167] (book p. 167; PDF p. 185)

### Findings (3.2)
- F-U3a-03: On p. 155, the prose below Table 3.2 prints `"The clauses for application shows"` (subject-verb
  mismatch). Recorded as printed. [PPA §3.2.1, p. 155] (book p. 155; PDF p. 173)
- F-U3a-04: On p. 156, `[let₂]` defines `ρ₀ = ρ | FV(e₂)` without subtracting `x`, so any outer binding of
  `x` remains shadowed underneath `[x ↦ v₁]` when `x ∈ FV(e₂) ∩ dom(ρ)`, whereas `[fn]` and `[fun]` in
  Table 3.2 restrict to `FV(fn x => e₀)` and `FV(fun f x => e₀)` (which already exclude bound `x` and `f, x`).
  Both preserve lookup semantics and `ρ₀ ℛ ρ̂`. [PPA Table 3.3, p. 156] (book p. 156; PDF p. 174)
- F-U3a-05 (`[Grammar Notation & Outermost-Label Relabelling]`): On p. 154, the `ITerm` grammar writes
  `if ie₀ then e₁ else e₂` and `let x = ie₁ in e₂` keeping branches and `let` bodies in `Exp` (matching
  `Table 3.3` `[if₁]`/`[let₁]`). On p. 156, `Table 3.3` `[if₂]`/`[if₃]` relabel the selected branch `t_i^{ℓ_i}`
  to the outer `if` label `ℓ` (like `[bind₂]` in `Table 3.2`), enforcing the p. 157 invariant that outer
  labels never change under `ρ ⊢ ie → ie'`; `Fact 3.11` (whose prose body on p. 160 is erased in OCR)
  therefore discharges `[if₂]`, `[if₃]`, and `[bind₂]` cleanly in `Theorem 3.10`.
  [PPA §3.2.1, p. 154] (book p. 154; PDF p. 172); [PPA Table 3.3, p. 156] (book p. 156; PDF p. 174); [PPA Fact 3.11, p. 160] (book p. 160; PDF p. 178)
- F-U3a-06: Example 3.15 on p. 164 reuses the identifier `(Ĉ'_e, ρ̂'_e)` for an *acceptable* over-approximation
  (`Ĉ'_e(3) = ρ̂'_e(y) = {fn x => x^1}`), whereas Example 3.3 on p. 144 and Example 3.5 on p. 149 used the
  same symbol `(Ĉ'_e, ρ̂'_e)` for an *unacceptable* under-approximation (`ρ̂'_e(x) = ∅`).
  [PPA Example 3.15, p. 164] (book p. 164; PDF p. 182)
- F-U3a-07: In the proof sketch of Proposition 3.16, p. 165 defines `IExp_e = {t^ℓ | t ∈ Term_e}` even
  though `Term_e` contains no `close` or `bind` forms (so `IExp_e` is actually `Exp_e`), and p. 167 writes
  `"candidates Q₁, ···, Q_n"` immediately before listing fixed `n = 4` candidates `Q₁, Q₂, Q₃, Q₄`.
  [PPA Proposition 3.16, p. 165] (book p. 165; PDF p. 183); [PPA Proposition 3.16, p. 167] (book p. 167; PDF p. 185)

### Projections (3.2)
- cs_theory: Theorem 3.10 adapts Wright–Felleisen subject reduction [external] from syntactic type systems
  to relational flow specifications via `IExp` (`close` + `bind`) and well-founded environment simulation
  `ρ ℛ ρ̂`; Proposition 3.13 + Proposition 3.16 establish the foundational duality that *infinite call cycles
  have empty inductive derivations (`lfp(𝒬) = ∅` on `Ω`) and require coinductive `gfp(𝒬)` to preserve the
  Moore-family existence of least solutions* [PPA Proposition 3.16, p. 165] (book p. 165; PDF p. 183).
- swe_architecture: Explicit environments (`close t in ρ` + `bind ρ in ie`) preserve AST node identities
  (`ℓ ∈ Lab_⋆`) intact throughout execution, explaining why practical interpreters, bytecode VMs, and abstract
  machines [external: CEK / SECD machines] pair immutable AST/bytecode pointers with heap-allocated closure
  environments rather than rewriting code trees via substitution [PPA §3.2.1, p. 153] (book p. 153; PDF p. 171).
- practical_debugging: Whenever two independent sound over-approximations `(Ĉ₁, ρ̂₁)` and `(Ĉ₂, ρ̂₂)` (for
  example from two different analysis passes or heuristics) disagree on spurious targets, Proposition 3.13
  guarantees their pointwise intersection `(Ĉ₁ ⊓ Ĉ₂, ρ̂₁ ⊓ ρ̂₂)` is *automatically* a sound 0-CFA solution
  (Example 3.15) — an immediate differential-debugging oracle for testing custom solver passes `[derived]`
  [PPA Proposition 3.13, p. 163] (book p. 163; PDF p. 181).
- cyber: Any call-graph or points-to verifier that attempts to validate mutually recursive callbacks,
  event-loop dispatchers, or self-referential closure chains (`Ω` / `loop`) by *inductive* witness trees
  (`⊨' = lfp(𝒬)`) rejects valid programs with *zero* acceptable models (`∅`, Proposition 3.16); soundness
  certificates for cyclic call graphs must check extensive (`Q ⊑ 𝒬(Q)`, `[external: post-fixed-point]`) invariants coinductively
  [PPA Proposition 3.16, p. 167] (book p. 167; PDF p. 185).

## 3.3 Syntax Directed 0-CFA Analysis

Context: Section 3.3 explains why Proposition 3.13's intersection over all acceptable guesses is not a
polynomial-time algorithm, introduces the three-phase pipeline (`⊨_s` `→` `𝒞_⋆⟦e_⋆⟧` `→` graph worklist
solver) and the general specification-refinement principle `⊨_A ⇐ ⊨_B`, defines syntax-directed 0-CFA
`(Ĉ, ρ̂) ⊨_s e` in Table 3.5, restricts value spaces to finite program subterms `Cachê_⋆ × Env̂_⋆`, and
proves soundness (`Proposition 3.18`) and Moore-family existence (`Proposition 3.19`)
[PPA §3.3, p. 168] (book p. 168; PDF p. 186).

### [U3a:3.3-a] Intractability of naive enumeration, three-phase pipeline, and safe refinement `⊨_A ⇐ ⊨_B`
- Statement: Fix an expression of interest `e_⋆ ∈ Exp`; we seek `(Ĉ, ρ̂)` satisfying `(Ĉ, ρ̂) ⊨ e_⋆` as small
  as possible under:
  ```text
  (Ĉ₁, ρ̂₁) ⊑ (Ĉ₂, ρ̂₂)   iff   (∀ℓ : Ĉ₁(ℓ) ⊆ Ĉ₂(ℓ)) ∧ (∀x : ρ̂₁(x) ⊆ ρ̂₂(x))
  ```
  The algorithm implicit in Proposition 3.13 (enumerate all candidate `(Ĉ, ρ̂)`, test `(Ĉ, ρ̂) ⊨ e_⋆`, take
  `⊓`) does not have polynomial complexity. While one could unfold `(Ĉ, ρ̂) ⊨ e_⋆` with memoisation, the
  book takes a direct **three-phase** route:
  1. `(i)` Reformulate Table 3.1 in a *syntax directed* manner (§3.3.1, Table 3.5).
  2. `(ii)` Turn the syntax-directed specification into an algorithm constructing a finite set of
     constraints (§3.4.1, Table 3.6).
  3. `(iii)` Compute the least solution of that constraint set (§3.4.2, Table 3.7).

  General **specification-refinement principle**: when reformulating `"⊨_A"` into `"⊨_B"`, ensuring
  ```text
  (Ĉ, ρ̂) ⊨_A e_⋆  ⇐  (Ĉ, ρ̂) ⊨_B e_⋆
  ```
  makes `"⊨_B"` a *safe approximation* to `"⊨_A"`: every solution (and in particular the least solution) to
  `"⊨_B e_⋆"` is also a solution to `"⊨_A e_⋆"` and therefore inherits semantic correctness from `"⊨_A"`
  *without* proving a separate subject-reduction result for `⊨_B` (indeed, subject reduction is explicitly
  *not* claimed for `⊨_B`). If additionally
  ```text
  (Ĉ, ρ̂) ⊨_A e_⋆  ⇒  (Ĉ, ρ̂) ⊨_B e_⋆
  ```
  (possibly after restricting `(Ĉ, ρ̂)` to fragments of `e_⋆`), then *no solutions are lost* and the least
  solutions coincide (note: for `⊨_A = ⊨` vs `⊨_B = ⊨_s`, only `⇐` holds in general because `⊨_s` analyses
  unreachable function bodies; see Corollary 3.25, Exercise 3.11
  [PPA Exercise 3.11, p. 208] (book p. 208; PDF p. 226), and Mini Project 3.1
  [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220)).
- Citation: [PPA §3.3, p. 168] (book p. 168; PDF p. 186); [PPA §3.3, p. 169] (book p. 169; PDF p. 187)

### 3.3.1 Syntax Directed Specification

### [U3a:3.3.1-a] Moving body analysis from `[app]` to `[fn]`/`[fun]` and uniqueness of fixed point for `⊨_s`
- Statement:
  - To ensure each function body is analysed *at most once* rather than at every application site where it
    could arrive, Table 3.5 analyses each function body *exactly once* in `[fn]` and `[fun]` (and moves
    `{fun f x => e₀} ⊆ ρ̂(f)` from `[app]` into `[fun]`), at the risk of analysing unreachable fragments
    (avoided in Mini Project 3.1 [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220)).
  - Because semantic correctness was discharged in §3.2, `(Ĉ, ρ̂) ⊨_s e` is defined on *ordinary*
    expressions `e ∈ Exp` only (no `bind` or `close`).
  - Formally `"⊨_s"` is defined as the *largest* relation (`gfp(𝒬_s)`) satisfying Table 3.5, but because
    every recursive appeal in Table 3.5 acts on a strict syntactic subexpression of `e`, there is a
    **unique** relation satisfying Table 3.5 (`lfp(𝒬_s) = gfp(𝒬_s)`, Exercise 3.9
    [PPA Exercise 3.9, p. 207] (book p. 207; PDF p. 225)): inductive and coinductive definitions of `⊨_s`
    coincide!
- Citation: [PPA §3.3.1, p. 169] (book p. 169; PDF p. 187)

### Table 3.5 — Syntax directed Control Flow Analysis
- Statement: Syntax-directed acceptability `(Ĉ, ρ̂) ⊨_s e`:
  ```text
  [con]  (Ĉ, ρ̂) ⊨_s c^ℓ  always

  [var]  (Ĉ, ρ̂) ⊨_s x^ℓ  iff  ρ̂(x) ⊆ Ĉ(ℓ)

  [fn]   (Ĉ, ρ̂) ⊨_s (fn x => e₀)^ℓ
             iff  {fn x => e₀} ⊆ Ĉ(ℓ)  ∧
                  (Ĉ, ρ̂) ⊨_s e₀

  [fun]  (Ĉ, ρ̂) ⊨_s (fun f x => e₀)^ℓ
             iff  {fun f x => e₀} ⊆ Ĉ(ℓ)  ∧
                  (Ĉ, ρ̂) ⊨_s e₀  ∧  {fun f x => e₀} ⊆ ρ̂(f)

  [app]  (Ĉ, ρ̂) ⊨_s (t₁^{ℓ₁} t₂^{ℓ₂})^ℓ
             iff  (Ĉ, ρ̂) ⊨_s t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_s t₂^{ℓ₂}  ∧
                  (∀(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) :
                       Ĉ(ℓ₂) ⊆ ρ̂(x)  ∧  Ĉ(ℓ₀) ⊆ Ĉ(ℓ))  ∧
                  (∀(fun f x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) :
                       Ĉ(ℓ₂) ⊆ ρ̂(x)  ∧  Ĉ(ℓ₀) ⊆ Ĉ(ℓ))

  [if]   (Ĉ, ρ̂) ⊨_s (if t₀^{ℓ₀} then t₁^{ℓ₁} else t₂^{ℓ₂})^ℓ
             iff  (Ĉ, ρ̂) ⊨_s t₀^{ℓ₀}  ∧
                  (Ĉ, ρ̂) ⊨_s t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_s t₂^{ℓ₂}  ∧
                  Ĉ(ℓ₁) ⊆ Ĉ(ℓ)  ∧  Ĉ(ℓ₂) ⊆ Ĉ(ℓ)

  [let]  (Ĉ, ρ̂) ⊨_s (let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ
             iff  (Ĉ, ρ̂) ⊨_s t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_s t₂^{ℓ₂}  ∧
                  Ĉ(ℓ₁) ⊆ ρ̂(x)  ∧  Ĉ(ℓ₂) ⊆ Ĉ(ℓ)

  [op]   (Ĉ, ρ̂) ⊨_s (t₁^{ℓ₁} op t₂^{ℓ₂})^ℓ  iff  (Ĉ, ρ̂) ⊨_s t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_s t₂^{ℓ₂}
  ```
- Citation: [PPA Table 3.5, p. 170] (book p. 170; PDF p. 188)

### Example 3.17 — Non-coinductive verification of `(Ĉ_lp, ρ̂_lp) ⊨_s loop` and displays `(3.2)`–`(3.3)`
- Statement: Verifying `(Ĉ_lp, ρ̂_lp) ⊨_s loop` (Examples 3.2 and 3.4) via `[let]` reduces to `(3.2)` and
  `(3.3)` (since `Ĉ_lp(5) ⊆ ρ̂_lp(g)` and `Ĉ_lp(9) ⊆ Ĉ_lp(10)`):
  ```text
  (Ĉ_lp, ρ̂_lp) ⊨_s (fun f x => (f^1 (fn y => y^2)^3)^4)^5      (3.2)
  (Ĉ_lp, ρ̂_lp) ⊨_s (g^6 (fn z => z^7)^8)^9                      (3.3)
  ```
  - `(3.2)` unfolds `[fun]` (`f ∈ Ĉ_lp(5)` and `f ∈ ρ̂_lp(f)`) to `(Ĉ_lp, ρ̂_lp) ⊨_s (f^1 (fn y => y^2)^3)^4`,
    which by `[app]` (`Ĉ_lp(1) = {f}`, `Ĉ_lp(3) ⊆ ρ̂_lp(x)`, `Ĉ_lp(4) ⊆ Ĉ_lp(4)`) reduces *without any
    circular re-entry into `f`'s body* to `(Ĉ_lp, ρ̂_lp) ⊨_s f^1` and `(Ĉ_lp, ρ̂_lp) ⊨_s (fn y => y^2)^3`
    (then `y^2`).
  - `(3.3)` unfolds `[app]` (`Ĉ_lp(6) = {f}`) to `(Ĉ_lp, ρ̂_lp) ⊨_s g^6` and `(Ĉ_lp, ρ̂_lp) ⊨_s (fn z => z^7)^8`
    (then `z^7`).
  Because Table 3.5 is syntax-directed, *no coinduction is needed*, unlike Example 3.6! `■`
- Citation: [PPA Example 3.17, p. 169] (book p. 169; PDF p. 187); [PPA Example 3.17, p. 170] (book p. 170; PDF p. 188); [PPA Example 3.17, p. 171] (book p. 171; PDF p. 189)

### 3.3.2 Preservation of Solutions

### [U3a:3.3.2-a] Finite subterm restriction `(Ĉ_⋆^⊤, ρ̂_⋆^⊤)` and `Cachê_⋆ × Env̂_⋆`
- Statement: For program `e_⋆` of interest, let `Lab_⋆ ⊆ Lab`, `Var_⋆ ⊆ Var`, `Term_⋆ ⊆ Term`, and `Exp_⋆`
  be the finite sets of labels, variables, unlabelled subterms, and subexpressions occurring in `e_⋆`.
  Define `(Ĉ_⋆^⊤, ρ̂_⋆^⊤) ∈ Cachê × Env̂` by:
  ```text
  Ĉ_⋆^⊤(ℓ) = ∅       if ℓ ∉ Lab_⋆        ρ̂_⋆^⊤(x) = ∅       if x ∉ Var_⋆
  Ĉ_⋆^⊤(ℓ) = Term_⋆  if ℓ ∈ Lab_⋆        ρ̂_⋆^⊤(x) = Term_⋆  if x ∈ Var_⋆
  ```
  Restricting attention to `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` is isomorphic to working directly inside the **finite**
  complete lattice `Cachê_⋆ × Env̂_⋆` where:
  ```text
  Val̂_⋆ = 𝒫(Term_⋆),   Cachê_⋆ = Lab_⋆ → Val̂_⋆,   Env̂_⋆ = Var_⋆ → Val̂_⋆
  ```
- Side conditions: Why is `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` *mandatory* in Proposition 3.18? Because if `Ĉ(ℓ₁)`
  at an application site contained a rogue term `fn x => t₀^{ℓ₀} ∉ Term_⋆` from outside `e_⋆`, Table 3.5's
  `[fn]` pass over `e_⋆` would never visit `t₀^{ℓ₀}`, so `(Ĉ, ρ̂) ⊨_s e_⋆` could hold while `(Ĉ, ρ̂) ⊨ t₀^{ℓ₀}`
  failed in Table 3.1! `[derived]`
- Citation: [PPA §3.3.2, p. 171] (book p. 171; PDF p. 189)

### Proposition 3.18 — Soundness of syntax-directed `⊨_s` with respect to abstract `⊨` and displays `(3.4)`–`(3.5)`
- Statement:
  `If (Ĉ, ρ̂) ⊨_s e_⋆ and (Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤) then (Ĉ, ρ̂) ⊨ e_⋆.`
- Proof (as printed on p. 172):
  1. By syntax-directedness of `⊨_s`, `(Ĉ, ρ̂) ⊨_s e_⋆` immediately gives `(3.4)`:
     ```text
     ∀e ∈ Exp_⋆ : (Ĉ, ρ̂) ⊨_s e                                                      (3.4)
     ```
  2. Write `⊨ = gfp(𝒬)` (Table 3.1) and `⊨_s = gfp(𝒬_s)` (Table 3.5), and define auxiliary relation `⊨^⋆` by
     `(Ĉ', ρ̂') ⊨^⋆ e'` iff `(Ĉ', ρ̂') = (Ĉ, ρ̂) ∧ e' ∈ Exp_⋆`. Establish `(3.5)`:
     ```text
     (𝒬_s(⊨_s) ∩ ⊨^⋆)  ⊆  𝒬(⊨_s ∩ ⊨^⋆)                                             (3.5)
     ```
     Since `⊨_s = 𝒬_s(⊨_s)`, `(3.5)` yields `(⊨_s ∩ ⊨^⋆) ⊆ 𝒬(⊨_s ∩ ⊨^⋆)`, so `(⊨_s ∩ ⊨^⋆) ⊆ gfp(𝒬) = ⊨` by
     coinduction!
  3. Checking `(3.5)` compares Table 3.5 against Table 3.1 on `(Ĉ, ρ̂, e)` with `e ∈ Exp_⋆`: `[con]`, `[var]`,
     `[if]`, `[let]`, `[op]` are immediate since subexpressions stay in `Exp_⋆`; `[fn]` and `[fun]` drop
     extra conjuncts; for `[app]` with `(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁)` (or `fun f x => t₀^{ℓ₀}`), `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)`
     forces `(fn x => t₀^{ℓ₀}) ∈ Term_⋆` so `t₀^{ℓ₀} ∈ Exp_⋆` (and `(fun f x => t₀^{ℓ₀})^ℓ ∈ Exp_⋆` for some
     `ℓ`), whence `(3.4)` supplies both `(Ĉ, ρ̂) ⊨_s t₀^{ℓ₀}` and `{fun f x => t₀^{ℓ₀}} ⊆ ρ̂(f)`. `■`
- Citation: [PPA Proposition 3.18, p. 172] (book p. 172; PDF p. 190)

### Proposition 3.19 — Moore family property on finite `Cachê_⋆ × Env̂_⋆`
- Statement:
  `{(Ĉ, ρ̂) ∈ Cachê_⋆ × Env̂_⋆ | (Ĉ, ρ̂) ⊨_s e_⋆} is a Moore family.`
  Immediate corollaries: every `e_⋆` has a Control Flow Analysis bounded by `(Ĉ_⋆^⊤, ρ̂_⋆^⊤)`, and every
  `e_⋆` has a unique *least* Control Flow Analysis bounded by `(Ĉ_⋆^⊤, ρ̂_⋆^⊤)`.
- Proof (as printed on p. 173):
  Structural induction on `e ∈ Exp_⋆` shows `(a) (Ĉ_⋆^⊤, ρ̂_⋆^⊤) ⊨_s e` and `(b)` closure under binary meet
  `⊓`; since `Cachê_⋆ × Env̂_⋆` is *finite*, any subset `Y = {(Ĉ₁, ρ̂₁), ..., (Ĉ_n, ρ̂_n)}` (`n ≥ 0`) has
  `⨅ Y = (Ĉ_⋆^⊤, ρ̂_⋆^⊤) ⊓ (Ĉ₁, ρ̂₁) ⊓ ··· ⊓ (Ĉ_n, ρ̂_n)`, which belongs to the set by `(a)` and `(b)` (no
  coinduction required!). `■`
- Citation: [PPA Proposition 3.19, p. 172] (book p. 172; PDF p. 190); [PPA Proposition 3.19, p. 173] (book p. 173; PDF p. 191)

### Findings (3.3)
- F-U3a-08: On p. 173, the proof of Proposition 3.19 prints `"and note than one can write Y = {(Ĉ_i, ρ̂_i) | i ∈ {1, ···, n}}"`
  (`"than"` instead of `"that"`). Recorded as printed. [PPA Proposition 3.19, p. 173] (book p. 173; PDF p. 191)

### Projections (3.3)
- cs_theory: Proposition 3.18 exemplifies asymmetric safe refinement (`⊨_s ⇒ ⊨` on `Cachê_⋆ × Env̂_⋆`,
  strictly over-approximating `⊨` on dead closures): moving `(Ĉ, ρ̂) ⊨_s e₀` from `[app]` to `[fn]`/`[fun]`
  converts a non-well-founded dynamic dependency into a structurally inductive AST traversal where
  `lfp(𝒬_s) = gfp(𝒬_s)` [PPA §3.3.1, p. 169] (book p. 169; PDF p. 187).
- swe_architecture: Restricting from infinite `Term` to finite `Term_⋆` (`Cachê_⋆ × Env̂_⋆`) is the formal
  justification for interning all program lambdas/functions into a dense `0 .. |Term_⋆|-1` integer table at
  the start of an analysis pass so abstract values `Val̂_⋆` can be represented as fixed-width bitsets
  `[external]` [PPA §3.3.2, p. 171] (book p. 171; PDF p. 189).
- practical_debugging: Beware that `⊨_s` intentionally gives up subject reduction on `Exp`! For example, if
  `e_⋆ = (if false^0 then ((fn x => (fn z => z^1)^2)^3 5^4)^5 else 7^6)^7` steps at runtime or dead-branch
  elimination drops the `then` branch, `⊨_s` on the original program forced `{fn z => z^1} ⊆ Ĉ(2)` inside the
  dead lambda, whereas `⊨` (Table 3.1) left dead unapplied bodies unconstrained `[derived]`
  [PPA §3.3, p. 168] (book p. 168; PDF p. 186).
- cyber: Analysing every syntactic function body unconditionally (`[fn]`/`[fun]` in Table 3.5) mirrors
  conservative whole-bundle / whole-binary scanning: unused library functions in the bundle still seed
  `Ĉ(ℓ)` and `ρ̂(f)`, inflating false-positive reachability unless dead-code / reachability gating (Mini
  Project 3.1) is enabled [PPA §3.3.1, p. 169] (book p. 169; PDF p. 187).

## 3.4 Constraint Based 0-CFA Analysis

Context: Section 3.4 translates `(Ĉ, ρ̂) ⊨_s e_⋆` into a finite set `𝒞_⋆⟦e_⋆⟧` of unconditional and
conditional subset constraints (Table 3.6), proves solution equivalence `(Ĉ, ρ̂) ⊨_s e_⋆ ⇔ (Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧`
on `Cachê_⋆ × Env̂_⋆` (Proposition 3.21), characterises the least solution via `lfp(F_⋆)` (`O(n⁵)` naive
iteration, Proposition 3.22), develops the `O(n³)` worklist graph solver (Table 3.7, Proposition 3.24), and
concludes with end-to-end soundness `Corollary 3.25` and open-system substitutability on p. 182
[PPA §3.4, p. 173] (book p. 173; PDF p. 191).

### [U3a:3.4-a] Unconditional and conditional constraint syntax (`(3.6)`–`(3.7)`) and `O(n)` / `O(n²)` counts
- Statement: For `e_⋆` of size `n`, construct a finite set `𝒞_⋆⟦e_⋆⟧` of *constraints* `(3.6)` and
  *conditional constraints* `(3.7)`:
  ```text
  lhs ⊆ rhs                        (3.6)
  {t} ⊆ rhs' ⇒ lhs ⊆ rhs           (3.7)
  ```
  where:
  - `rhs` and `rhs'` have the pure syntactic variable form `C(ℓ)` or `r(x)` (sans-serif syntax, distinct from
    semantic sets `Ĉ(ℓ)` and `ρ̂(x)`);
  - `lhs` has the form `C(ℓ)`, `r(x)`, or `{t}`;
  - every `t` is an abstraction `fn x => e₀` or `fun f x => e₀` in `Term_⋆`;
  - `(3.7)` is parsed uniformly as `( {t} ⊆ rhs' ⇒ lhs ) ⊆ rhs`, writing `ls` for both `lhs` and
    `{t} ⊆ rhs' ⇒ lhs` so every constraint in `𝒞_⋆⟦e_⋆⟧` has the uniform shape `ls ⊆ rhs`.
  - **Size bound**: Although syntactically there could be `O(n²)` constraints of form `(3.6)` and `O(n⁴)` of
    form `(3.7)`, inspection of Table 3.6 shows `𝒞_⋆⟦e_⋆⟧` contains **at most `O(n)` unconditional
    constraints `(3.6)` and at most `O(n²)` conditional constraints `(3.7)`**, because each of the `O(n)`
    constituents of `e_⋆` generates `O(1)` constraints of form `(3.6)` and (at `[app]`, ranging over
    `t ∈ Term_⋆` of size `O(n)`) at most `O(n)` constraints of form `(3.7)`.
- Citation: [PPA §3.4, p. 173] (book p. 173; PDF p. 191); [PPA §3.4, p. 174] (book p. 174; PDF p. 192); [PPA §3.4, p. 175] (book p. 175; PDF p. 193)

### Table 3.6 — Constraint based Control Flow Analysis
- Statement: Syntax-directed constraint generator `𝒞_⋆⟦e⟧` (using finite `Term_⋆` of `e_⋆` in `[app]`,
  justified by Propositions 3.18 and 3.19):
  ```text
  [con]  𝒞_⋆⟦c^ℓ⟧ = ∅

  [var]  𝒞_⋆⟦x^ℓ⟧ = {r(x) ⊆ C(ℓ)}

  [fn]   𝒞_⋆⟦(fn x => e₀)^ℓ⟧ = {{fn x => e₀} ⊆ C(ℓ)}
                               ∪ 𝒞_⋆⟦e₀⟧

  [fun]  𝒞_⋆⟦(fun f x => e₀)^ℓ⟧ = {{fun f x => e₀} ⊆ C(ℓ)}
                                   ∪ 𝒞_⋆⟦e₀⟧ ∪ {{fun f x => e₀} ⊆ r(f)}

  [app]  𝒞_⋆⟦(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ⟧ = 𝒞_⋆⟦t₁^{ℓ₁}⟧ ∪ 𝒞_⋆⟦t₂^{ℓ₂}⟧
                                     ∪ {{t} ⊆ C(ℓ₁) ⇒ C(ℓ₂) ⊆ r(x)
                                          | t = (fn x => t₀^{ℓ₀}) ∈ Term_⋆}
                                     ∪ {{t} ⊆ C(ℓ₁) ⇒ C(ℓ₀) ⊆ C(ℓ)
                                          | t = (fn x => t₀^{ℓ₀}) ∈ Term_⋆}
                                     ∪ {{t} ⊆ C(ℓ₁) ⇒ C(ℓ₂) ⊆ r(x)
                                          | t = (fun f x => t₀^{ℓ₀}) ∈ Term_⋆}
                                     ∪ {{t} ⊆ C(ℓ₁) ⇒ C(ℓ₀) ⊆ C(ℓ)
                                          | t = (fun f x => t₀^{ℓ₀}) ∈ Term_⋆}

  [if]   𝒞_⋆⟦(if t₀^{ℓ₀} then t₁^{ℓ₁} else t₂^{ℓ₂})^ℓ⟧ = 𝒞_⋆⟦t₀^{ℓ₀}⟧ ∪ 𝒞_⋆⟦t₁^{ℓ₁}⟧ ∪ 𝒞_⋆⟦t₂^{ℓ₂}⟧
                                                          ∪ {C(ℓ₁) ⊆ C(ℓ)}
                                                          ∪{C(ℓ₂) ⊆ C(ℓ)}

  [let]  𝒞_⋆⟦(let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ⟧ = 𝒞_⋆⟦t₁^{ℓ₁}⟧ ∪ 𝒞_⋆⟦t₂^{ℓ₂}⟧
                                                ∪ {C(ℓ₁) ⊆ r(x)} ∪ {C(ℓ₂) ⊆ C(ℓ)}

  [op]   𝒞_⋆⟦(t₁^{ℓ₁} op t₂^{ℓ₂})^ℓ⟧ = 𝒞_⋆⟦t₁^{ℓ₁}⟧ ∪ 𝒞_⋆⟦t₂^{ℓ₂}⟧
  ```
- Citation: [PPA Table 3.6, p. 174] (book p. 174; PDF p. 192)

### Example 3.20 — Constraint set `𝒞_⋆⟦((fn x => x^1)^2 (fn y => y^3)^4)^5⟧`
- Statement: Since `fn x => x^1` and `fn y => y^3` are the only abstractions in `Term_⋆`, Table 3.6 emits 8
  constraints (4 unconditional, 4 conditional):
  ```text
  𝒞_⋆⟦((fn x => x^1)^2 (fn y => y^3)^4)^5⟧ =
    { {fn x => x^1} ⊆ C(2),
      r(x) ⊆ C(1),
      {fn y => y^3} ⊆ C(4),
      r(y) ⊆ C(3),
      {fn x => x^1} ⊆ C(2) ⇒ C(4) ⊆ r(x),
      {fn x => x^1} ⊆ C(2) ⇒ C(1) ⊆ C(5),
      {fn y => y^3} ⊆ C(2) ⇒ C(4) ⊆ r(y),
      {fn y => y^3} ⊆ C(2) ⇒ C(3) ⊆ C(5) }
  ```
  `■`
- Citation: [PPA Example 3.20, p. 175] (book p. 175; PDF p. 193)

### 3.4.1 Preservation of Solutions

### [U3a:3.4.1-a] Constraint valuation `(Ĉ, ρ̂)⟦·⟧` and satisfaction relation `⊨_c`
- Statement: While `(Ĉ, ρ̂) ⊨_s e_⋆` is a logical formula, `𝒞_⋆⟦e_⋆⟧` is a set of syntactic entities.
  Interpret constraint syntax under `(Ĉ, ρ̂)` via:
  ```text
  (Ĉ, ρ̂)⟦C(ℓ)⟧ = Ĉ(ℓ)
  (Ĉ, ρ̂)⟦r(x)⟧ = ρ̂(x)
  (Ĉ, ρ̂)⟦{t}⟧  = {t}
  (Ĉ, ρ̂)⟦{t} ⊆ rhs' ⇒ lhs⟧ = (Ĉ, ρ̂)⟦lhs⟧    if {t} ⊆ (Ĉ, ρ̂)⟦rhs'⟧
                               ∅               otherwise
  ```
  Define single-constraint and constraint-set satisfaction `⊨_c`:
  ```text
  (Ĉ, ρ̂) ⊨_c (ls ⊆ rhs)   iff   (Ĉ, ρ̂)⟦ls⟧ ⊆ (Ĉ, ρ̂)⟦rhs⟧
  (Ĉ, ρ̂) ⊨_c C            iff   ∀(ls ⊆ rhs) ∈ C : (Ĉ, ρ̂) ⊨_c (ls ⊆ rhs)
  ```
- Citation: [PPA §3.4.1, p. 175] (book p. 175; PDF p. 193); [PPA §3.4.1, p. 176] (book p. 176; PDF p. 194)

### Proposition 3.21 — Exact equivalence of `⊨_s` and `⊨_c 𝒞_⋆⟦e_⋆⟧` under `(Ĉ_⋆^⊤, ρ̂_⋆^⊤)`
- Statement:
  `If (Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤) then (Ĉ, ρ̂) ⊨_s e_⋆ if and only if (Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧.`
  Hence the least solution `(Ĉ, ρ̂)` to `(Ĉ, ρ̂) ⊨_s e_⋆` (in `Cachê_⋆ × Env̂_⋆`) equals the least solution to
  `(Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧`.
- Proof: Structural induction on subexpressions `e` of `e_⋆` proves `(Ĉ, ρ̂) ⊨_s e iff (Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e⟧`,
  using `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` at `[app]` to ensure `Ĉ(ℓ₁) ⊆ Term_⋆` (so quantifying over `t ∈ Term_⋆`
  with `{t} ⊆ Ĉ(ℓ₁)` matches quantifying over `t ∈ Ĉ(ℓ₁)`). `■`
- Citation: [PPA Proposition 3.21, p. 176] (book p. 176; PDF p. 194)

### 3.4.2 Solving the Constraints

### [U3a:3.4.2-a] Fixed-point formulation `F_⋆` and naive `O(n⁵)` fixed-point iteration bound (`[external: Kleene]`)
- Statement: Define `F_⋆ : Cachê_⋆ × Env̂_⋆ → Cachê_⋆ × Env̂_⋆` by `F_⋆(Ĉ, ρ̂) = (F₁(Ĉ, ρ̂), F₂(Ĉ, ρ̂))` where:
  ```text
  F₁(Ĉ, ρ̂)(ℓ) = ⋃ {(Ĉ, ρ̂)⟦ls⟧ | (ls ⊆ C(ℓ)) ∈ 𝒞_⋆⟦e_⋆⟧}
  F₂(Ĉ, ρ̂)(x) = ⋃ {(Ĉ, ρ̂)⟦ls⟧ | (ls ⊆ r(x)) ∈ 𝒞_⋆⟦e_⋆⟧}
  ```
  Since every guard `lhs' ⊆ rhs'` in `𝒞_⋆⟦e_⋆⟧` has constant left-hand side `lhs' = {t}`, `(Ĉ₁, ρ̂₁) ⊑ (Ĉ₂, ρ̂₂)`
  and `{t} ⊆ (Ĉ₁, ρ̂₁)⟦rhs'⟧` imply `{t} ⊆ (Ĉ₂, ρ̂₂)⟦rhs'⟧`, making `F_⋆` monotone on the finite complete
  lattice `Cachê_⋆ × Env̂_⋆`.
- Citation: [PPA §3.4.2, p. 176] (book p. 176; PDF p. 194); [PPA §3.4.2, p. 177] (book p. 177; PDF p. 195)

### Proposition 3.22 — Least fixed point `lfp(F_⋆)` equals least constraint solution
- Statement:
  `lfp(F_⋆) = ⨅ {(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧}`
- Proof: Verify `F_⋆(Ĉ, ρ̂) ⊑ (Ĉ, ρ̂) iff (Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧` (reductive elements `Red(F_⋆)`,
  `[external: pre-fixed points]`, are exactly solutions of `𝒞_⋆⟦e_⋆⟧`) and apply `lfp(f) = ⨅ {x | f(x) ⊑ x}`
  from Appendix A [PPA Proposition A.10, p. 402] (book p. 402; PDF p. 418). `■`
- Naive iterative bound (`p. 177`, `[external: Kleene]`): Viewing `(Ĉ, ρ̂) ∈ Cachê_⋆ × Env̂_⋆` as an `O(n)`-tuple over `Val̂_⋆` of
  height `O(n)` gives lattice height `O(n²)` (misprinted `Cachê_⋆ × Val̂_⋆` on p. 177; see `F-U3a-10`), so
  `lfp(F_⋆) = ⨆_m F_⋆^m(⊥)` takes at most `O(n²)` iterations; scanning all `O(n²)` constraints for each of
  the `O(n)` components per iterant yields naive cost `O(n⁵)`.
- Citation: [PPA Proposition 3.22, p. 177] (book p. 177; PDF p. 195)

### [U3a:3.4.2-b] Graph formulation and dual-observer constraint registration
- Statement: Represent `𝒞_⋆⟦e_⋆⟧` as a directed graph over `Nodes = {C(ℓ) | ℓ ∈ Lab_⋆} ∪ {r(x) | x ∈ Var_⋆}`
  (`|Nodes| = O(n)`) with three main data structures:
  - `W`: *worklist* of nodes whose outgoing edges remain to be traversed;
  - `D[p] ∈ Val̂_⋆`: *data array*, seeded with `{t | ({t} ⊆ p) ∈ 𝒞_⋆⟦e_⋆⟧}` via `add(p, {t})`;
  - `E[p]`: *edge array* of constraints attached to trigger node `p`:
    - unconditional `p₁ ⊆ p₂` registers in `E[p₁]` (edge `p₁ → p₂`);
    - conditional `{t} ⊆ p ⇒ p₁ ⊆ p₂` registers in **both** `E[p₁]` (edge `p₁ → p₂`) **and** `E[p]` (edge
      `p → p₂`)!
- Side conditions: Why *must* `{t} ⊆ p ⇒ p₁ ⊆ p₂` be registered in **both** `E[p₁]` and `E[p]`? Because two
  arrival orders occur dynamically during chaotic worklist propagation:
  1. `t` arrives in `D[p]` *first*, and later new terms arrive in `D[p₁]` (handled when `p₁` is popped and
     scans `E[p₁]`);
  2. `D[p₁]` is already non-empty (`D[p₁] ≠ ∅`) *before* `t` arrives in `D[p]`, and `p₁` never changes again
     (handled *only* when `p` is popped and scans `E[p]`)! Omitting `E[p]` silently drops all pre-existing
     `D[p₁]` values whenever the call target `t` is discovered after the argument `p₁`! `[derived]`
- Citation: [PPA §3.4.2, p. 177] (book p. 177; PDF p. 195); [PPA §3.4.2, p. 178] (book p. 178; PDF p. 196); [PPA §3.4.2, p. 179] (book p. 179; PDF p. 197)

### Table 3.7 — Algorithm for solving constraints
- Statement: Worklist graph-propagation solver computing the least solution `(Ĉ, ρ̂)` of `𝒞_⋆⟦e_⋆⟧`:
  ```text
  INPUT:    𝒞_⋆⟦e_⋆⟧
  OUTPUT:   (Ĉ, ρ̂)

  METHOD:   Step 1: Initialisation
                    W := nil;
                    for q in Nodes do D[q] := ∅;
                    for q in Nodes do E[q] := nil;

            Step 2: Building the graph
                    for cc in 𝒞_⋆⟦e_⋆⟧ do
                      case cc of
                        {t} ⊆ p:
                            add(p, {t});
                        p₁ ⊆ p₂:
                            E[p₁] := cons(cc, E[p₁]);
                        {t} ⊆ p ⇒ p₁ ⊆ p₂:
                            E[p₁] := cons(cc, E[p₁]);
                            E[p]  := cons(cc, E[p]);

            Step 3: Iteration
                    while W ≠ nil do
                      q := head(W); W := tail(W);
                      for cc in E[q] do
                        case cc of
                          p₁ ⊆ p₂:
                              add(p₂, D[p₁]);
                          {t} ⊆ p ⇒ p₁ ⊆ p₂:
                              if t ∈ D[p] then add(p₂, D[p₁]);

            Step 4: Recording the solution
                    for ℓ in Lab_⋆ do Ĉ(ℓ) := D[C(ℓ)];
                    for x in Var_⋆ do ρ̂(x) := D[r(x)];

  USING:    procedure add(q, d) is
                if ¬(d ⊆ D[q])
                then D[q] := D[q] ∪ d;
                     W := cons(q, W);
  ```
- Side conditions: Note that `W` is maintained as a LIFO list via `cons(q, W)` without duplicate checking on
  `W` (though `q` is pushed only when `¬(d ⊆ D[q])`, so at most `|Term_⋆|` pushes per node can ever occur),
  and when `p = p₁` in `{t} ⊆ p ⇒ p ⊆ p₂`, Step 2 prepends `cc` twice into `E[p]` (harmless idempotence, or
  deduplicable in implementations `[derived]`).
- Citation: [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196)

### Figure 3.4 — Initialisation of data structures for example program
- Statement: State of `D[p]` and `E[p]` after Step 2 on Example 3.20 (writing `id_x` for `{fn x => x^1}` and
  `id_y` for `{fn y => y^3}` without braces in the printed table):

  | `p` | `D[p]` | `E[p]` |
  | :--- | :--- | :--- |
  | `C(1)` | `∅` | `[id_x ⊆ C(2) ⇒ C(1) ⊆ C(5)]` |
  | `C(2)` | `id_x` | `[id_y ⊆ C(2) ⇒ C(3) ⊆ C(5), id_y ⊆ C(2) ⇒ C(4) ⊆ r(y), id_x ⊆ C(2) ⇒ C(1) ⊆ C(5), id_x ⊆ C(2) ⇒ C(4) ⊆ r(x)]` |
  | `C(3)` | `∅` | `[id_y ⊆ C(2) ⇒ C(3) ⊆ C(5)]` |
  | `C(4)` | `id_y` | `[id_y ⊆ C(2) ⇒ C(4) ⊆ r(y), id_x ⊆ C(2) ⇒ C(4) ⊆ r(x)]` |
  | `C(5)` | `∅` | `[ ]` |
  | `r(x)` | `∅` | `[r(x) ⊆ C(1)]` |
  | `r(y)` | `∅` | `[r(y) ⊆ C(3)]` |

- Citation: [PPA Figure 3.4, p. 179] (book p. 179; PDF p. 197)

### Example 3.23 — Worklist trace on `((fn x => x^1)^2 (fn y => y^3)^4)^5`
- Statement: Step 2 on Example 3.20 initialises `W = [C(4), C(2)]` and `D, E` as in Figure 3.4; Step 3
  iterates through the six worklist states recorded in Figure 3.5, terminating at `W = [ ]` with the exact
  least solution `(Ĉ_e, ρ̂_e)` of Example 3.5. `■`
- Citation: [PPA Example 3.23, p. 179] (book p. 179; PDF p. 197); [PPA Example 3.23, p. 180] (book p. 180; PDF p. 198)

### Figure 3.5 — Iteration steps of example program
- Statement: Six-column trace of `W` and `D[p]` across Step 3 on Example 3.23:

  | `W` | `[C(4),C(2)]` | `[r(x),C(2)]` | `[C(1),C(2)]` | `[C(5),C(2)]` | `[C(2)]` | `[ ]` |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | `C(1)` | `∅` | `∅` | `id_y` | `id_y` | `id_y` | `id_y` |
  | `C(2)` | `id_x` | `id_x` | `id_x` | `id_x` | `id_x` | `id_x` |
  | `C(3)` | `∅` | `∅` | `∅` | `∅` | `∅` | `∅` |
  | `C(4)` | `id_y` | `id_y` | `id_y` | `id_y` | `id_y` | `id_y` |
  | `C(5)` | `∅` | `∅` | `∅` | `id_y` | `id_y` | `id_y` |
  | `r(x)` | `∅` | `id_y` | `id_y` | `id_y` | `id_y` | `id_y` |
  | `r(y)` | `∅` | `∅` | `∅` | `∅` | `∅` | `∅` |

  (Notice why dual registration mattered right at column 1: `C(4)` is popped *before* `C(2)` while
  `id_x ∈ D[C(2)]` is already true, so `id_x ⊆ C(2) ⇒ C(4) ⊆ r(x)` inside `E[C(4)]` immediately propagates
  `id_y` to `r(x)` → `C(1)` → `C(5)`; when `C(2)` is finally popped at column 5, `¬(d ⊆ D[q])` is false so
  no duplicate work occurs! `[derived]`)
- Citation: [PPA Figure 3.5, p. 180] (book p. 180; PDF p. 198)

### Proposition 3.24 — Termination and least-solution correctness of Table 3.7
- Statement:
  `Given input 𝒞_⋆⟦e_⋆⟧ the algorithm of Table 3.7 terminates and the result (Ĉ, ρ̂) produced by the algorithm satisfies`
  ```text
  (Ĉ, ρ̂) = ⨅ {(Ĉ', ρ̂') | (Ĉ', ρ̂') ⊨_c 𝒞_⋆⟦e_⋆⟧}
  ```
  `and hence it is the least solution to 𝒞_⋆⟦e_⋆⟧.`
  (Note: the OCR text layer of `ppa.pdf` completely drops the displayed `⨅` equation on p. 180!)
- Citation: [PPA Proposition 3.24, p. 180] (book p. 180; PDF p. 198)

### [U3a:3.4.2-c] Proof of Proposition 3.24 and `O(n³)` worst-case complexity
- Statement:
  1. **Termination**: Steps 1, 2, 4 are finite loops; in Step 3, `D[q]` never decreases, can grow at most
     `|Term_⋆| ≤ n` times, `add(q, d)` pushes `q` onto `W` *only* when `D[q]` strictly grows, and each pop
     traverses finitely many outgoing edges `E[q]`.
  2. **Lower-bound invariant (`(Ĉ, ρ̂) ⊑ (Ĉ', ρ̂')`)**: For any solution `(Ĉ', ρ̂') ⊨_c 𝒞_⋆⟦e_⋆⟧`, Step 2 and
     every iteration of Step 3 preserve `∀q ∈ Nodes : D[q] ⊆ (Ĉ', ρ̂')⟦q⟧`.
  3. **Solution invariant at `W = nil` (`(Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧`)**: Step 2 establishes `{t} ⊆ D[p]` for all
     `({t} ⊆ p) ∈ 𝒞_⋆⟦e_⋆⟧` and maintains the worklist invariant:
     - if `(p₁ ⊆ p₂) ∈ 𝒞_⋆⟦e_⋆⟧` and `D[p₁] \ D[p₂] ≠ ∅`, then `p₁ ∈ W`;
     - if `({t} ⊆ p ⇒ p₁ ⊆ p₂) ∈ 𝒞_⋆⟦e_⋆⟧`, `t ∈ D[p]`, and `D[p₁] \ D[p₂] ≠ ∅`, then `p ∈ W` or `p₁ ∈ W`
       (established by checking whichever of `t ∈ D[p]` or the latest element of `D[p₁] \ D[p₂]` was added
       most recently!). When `W = nil`, `D[p₁] \ D[p₂] = ∅` across all active constraints, so `(Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧`. `■`
  4. **`O(n³)` step bound (`p. 181`)**: For `e_⋆` of size `n` (`|Lab_⋆|, |Var_⋆|, |Term_⋆| ≤ n`):
     - Step 1: `O(n)`; Step 2: `O(n²)` (`|𝒞_⋆⟦e_⋆⟧| = O(n²)`); Step 4: `O(n)`.
     - Step 3: each node `q` has `D[q]` extended at most `n` times and therefore enters `W` at most `n`
       times. Summing edge traversals across all nodes in a single pass gives `∑_q |E[q]| ≤ 2 · |𝒞_⋆⟦e_⋆⟧| = O(n²)`,
       so across at most `n` passes per node the inner `case` executes at most **`O(n³)` edge-traversal
       steps**!
- Side conditions (`[derived]` unit-cost subtlety on `add(p₂, D[p₁])`): Note that the book's `O(n³)` count
  treats `add(p₂, D[p₁])` (`¬(D[p₁] ⊆ D[p₂])` and `D[p₂] ∪ D[p₁]`) as `O(1)` per edge traversal! If `D[q]`
  is implemented via naive `O(n)` set operations on `O(n³)` whole-set `add(p₂, D[p₁])` calls, worst-case
  elementary operations are `O(n⁴)` (or `O(n⁴ / w)` with machine-word bitsets of width `w`). True elementary
  `O(n³)` time is achieved in standard implementations `[external: Andersen / Heintze–McAllester worklist]`
  by pushing *individual newly discovered `(q, t)` pairs* onto `W`: then each `(q, t)` pair (`O(n²)` total)
  is popped **once**, `E[q]` has amortised/per-site out-degree `O(n)`, and `add(p₂, {t})` tests single-element
  membership `t ∈ D[p₂]` in `O(1)` bitset/array lookup, giving exact `O(n³)` elementary operations!
- Citation: [PPA §3.4.2, p. 180] (book p. 180; PDF p. 198); [PPA §3.4.2, p. 181] (book p. 181; PDF p. 199)

### Corollary 3.25 — End-to-end semantic soundness of the Table 3.7 constraint solver
- Statement:
  `Given e_⋆ the algorithm of Table 3.7 applied to 𝒞⟦e_⋆⟧ terminates and produces a result (Ĉ, ρ̂) ∈ Cachê_⋆ × Env̂_⋆ that satisfies (Ĉ, ρ̂) ⊨ e_⋆ (when extended with Ĉ(ℓ) = ∅ for ℓ ∉ Lab_⋆ and ρ̂(x) = ∅ for x ∉ Var_⋆).` `■`
- Side conditions: Chaining `Proposition 3.24` (`(Ĉ, ρ̂)` is the least solution of `𝒞_⋆⟦e_⋆⟧` in
  `Cachê_⋆ × Env̂_⋆`) `→` `Proposition 3.21` (`(Ĉ, ρ̂) ⊨_s e_⋆`) `→` `Proposition 3.18` (`(Ĉ, ρ̂) ⊨ e_⋆` after
  zero-extending outside `Lab_⋆, Var_⋆`) `→` `Theorem 3.10` (preserved across every small-step reduction!).
  Note that Corollary 3.25 does **not** claim `(Ĉ, ρ̂)` is the *least* solution of `(Ĉ, ρ̂) ⊨ e_⋆`, because
  `𝒞_⋆⟦e_⋆⟧` analyses unreachable function bodies (Exercise 3.11
  [PPA Exercise 3.11, p. 208] (book p. 208; PDF p. 226)).
- Citation: [PPA Corollary 3.25, p. 182] (book p. 182; PDF p. 200)

### [U3a:3.4.2-d] Open systems and substitutability of external fragments (`e_∘`, `e_⋆`, `e'_⋆`)
- Statement: Suppose an open program `e_∘` contains a placeholder ("hole") filled by an external environment
  fragment, instantiated first as `e_⋆` (using a placeholder stub) and later replaced by another closed tool/library
  fragment yielding `e'_⋆`. If `(Ĉ, ρ̂)` solved on `e_⋆` also satisfies the acceptability clauses for the
  replacement fragment in `e'_⋆`, then `(Ĉ, ρ̂) ⊨ e'_⋆` holds immediately *without re-analysing `e_∘`* —
  provided labels and free/bound variables do not clash unexpectedly. (Section `3.5 Adding Data Flow Analysis`
  starts immediately below this paragraph on p. 182 [PPA §3.5, p. 182] (book p. 182; PDF p. 200).)
- Citation: [PPA §3.4.2, p. 182] (book p. 182; PDF p. 200)

### [U3a:3.4.2-e] OCR Erasure Audit Summary (PDF pp. 159–200)
- Statement: Four critical formal items in Unit 3a are silently corrupted or completely erased in the
  `pdftotext` OCR layer of `ppa.pdf` and must always be read from visual page renders (or this shard):
  1. `Table 3.2` (`[bind₁]`, `[app₁]`, `[app₂]`): inference-rule numerators above horizontal fraction bars
     erased in OCR [PPA Table 3.2, p. 155] (book p. 155; PDF p. 173).
  2. `Table 3.3` (`[if₁]`, `[let₁]`, `[op₁]`, `[op₂]`): inference-rule numerators above horizontal fraction
     bars erased in OCR [PPA Table 3.3, p. 156] (book p. 156; PDF p. 174).
  3. `Fact 3.11`: entire statement body between `Fact 3.11` and `■` erased in OCR
     [PPA Fact 3.11, p. 160] (book p. 160; PDF p. 178).
  4. `Proposition 3.24`: displayed equation `(Ĉ, ρ̂) = ⨅ {(Ĉ', ρ̂') | (Ĉ', ρ̂') ⊨_c 𝒞_⋆⟦e_⋆⟧}` completely
     erased in OCR [PPA Proposition 3.24, p. 180] (book p. 180; PDF p. 198).
- Citation: [PPA Table 3.2, p. 155] (book p. 155; PDF p. 173); [PPA Fact 3.11, p. 160] (book p. 160; PDF p. 178); [PPA Proposition 3.24, p. 180] (book p. 180; PDF p. 198)

### Findings (3.4)
- F-U3a-09 (`[Source Erratum — Wrong Proposition Number]`): At the bottom of p. 176 (§3.4.2 *Fixed point
  formulation*), the book prints `"whose existence is guaranteed by Propositions 3.18 and 3.21."` Proposition
  3.18 proves soundness `⊨_s ⇒ ⊨`, *not* existence of a least solution! Least-solution existence for `⊨_s` on
  `Cachê_⋆ × Env̂_⋆` is **Proposition 3.19** (paired with Proposition 3.21's equivalence `⊨_s ⇔ ⊨_c`).
  [PPA §3.4.2, p. 176] (book p. 176; PDF p. 194)
- F-U3a-10 (`[Source Erratum — Wrong Lattice Product]`): On p. 177 (below Proposition 3.22), the book prints
  `"Since Val̂_⋆ is a lattice of height O(n) this means that Cachê_⋆ × Val̂_⋆ has height O(n²)"` instead of
  `Cachê_⋆ × Env̂_⋆`. Recorded as printed. [PPA §3.4.2, p. 177] (book p. 177; PDF p. 195)
- F-U3a-11: On p. 177 (`D[p] = {t | ({t} ⊆ p) ∈ 𝒞_⋆⟦e_⋆⟧}`) and p. 179 (`"if in fact t ∈ D[p]"`), the
  index `p` inside `D[p]` is typeset in sans-serif `p` while surrounding occurrences of node metavariable `p`
  are typeset in math italic `p`. [PPA §3.4.2, p. 177] (book p. 177; PDF p. 195); [PPA §3.4.2, p. 179] (book p. 179; PDF p. 197)
- F-U3a-12: In Figure 3.4 (p. 179) and Figure 3.5 (p. 180), `id_x` and `id_y` denote singleton sets
  `{fn x => x^1}` and `{fn y => y^3}` (p. 180 explicitly notes `"we have written id_x for {fn x => x^1} and id_y for {fn y => y^3}"`),
  so `E[p]` entries in Figure 3.4 write `id_x ⊆ C(2) ⇒ ...` without braces around `id_x`, unlike `{t} ⊆ p`
  in Table 3.6. [PPA Figure 3.4, p. 179] (book p. 179; PDF p. 197); [PPA Figure 3.5, p. 180] (book p. 180; PDF p. 198)
- F-U3a-13: At the bottom of p. 180 (last line of Proposition 3.24's proof setup), the book prints
  single-bracket `(Ĉ', ρ̂') ⊨_c 𝒞_⋆[e_⋆]` instead of semantic double brackets `𝒞_⋆⟦e_⋆⟧`.
  [PPA §3.4.2, p. 180] (book p. 180; PDF p. 198)
- F-U3a-14: On p. 181 (twice in the complexity discussion) and in Corollary 3.25 on p. 182, the book prints
  unstarred `𝒞⟦e_⋆⟧` instead of `𝒞_⋆⟦e_⋆⟧`. [PPA §3.4.2, p. 181] (book p. 181; PDF p. 199); [PPA Corollary 3.25, p. 182] (book p. 182; PDF p. 200)

### Projections (3.4)
- cs_theory: Conditional subset constraints `{t} ⊆ p ⇒ p₁ ⊆ p₂` compile 1-to-1 into ground Datalog `[external]` Horn
  clauses `Reach(p2, u) :- Reach(p, t), Reach(p1, u).` [external: Reps / Whaley–Lam Datalog program
  analysis], and the `O(n³)` worklist bound in §3.4.2 is the classic *cubic bottleneck* [external: Heintze–McAllester
  1997 BMM / 2NPDA-hardness of 0-CFA] shared by Andersen's pointer analysis `[external]`, 0-CFA, and subtransitive
  control-flow reachability [PPA §3.4.2, p. 181] (book p. 181; PDF p. 199).
- swe_architecture: Table 3.7 is a reactive observer / propagator network [external]: each node `q` owns an
  append-only monotone state cell `D[q]` and subscriber list `E[q]`; to guarantee `O(n³)` elementary time in
  production solvers rather than `O(n⁴)` whole-set union scans, push delta pairs `(q, t)` (or maintain
  per-node unseen-delta bitsets) and dynamically add edge `p₁ → p₂` the first time `t ∈ D[p]` becomes true
  `[derived]` [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196).
- practical_debugging: The single highest-frequency bug in hand-rolled points-to / 0-CFA solvers is
  registering `{t} ⊆ p ⇒ p₁ ⊆ p₂` in `E[p₁]` *only* (or `E[p]` *only*): any test where argument `p₁` is
  populated before callee `p` resolves (such as Example 3.23's LIFO order `W = [C(4), C(2)]` if `C(2)` were
  populated after `C(4)`!) silently drops the call's argument/return flow without crashing `[derived]`
  [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196).
- cyber: Two operational security consequences emerge directly from §3.4.2:
  1. **Scanner DoS (`O(n³)` cubic blowup, `[external: CWE-400]`)**: obfuscated or bundler-generated code with
     thousands of dynamic dispatch sites and candidate callbacks (`|Term_⋆| = Θ(n)`) triggers `Θ(n²)`
     conditional constraints and `Θ(n³)` propagation work unless solver budgets / context-pruning filters are
     enforced [PPA §3.4.2, p. 181] (book p. 181; PDF p. 199).
  2. **Open-system plugin / FFI stubs (`p. 182`, `[external]`)**: modelling an uninspected native library, FFI import, or
     deserialization sink (`e_∘`, `[external]`) via a conservative stub `e_⋆` remains sound under replacement `e'_⋆` *if and
     only if* `(Ĉ, ρ̂)` satisfies the acceptability clauses of the real implementation (every callback invoke
     and closure escape performed by `e'_⋆` is mocked in the stub!) [PPA §3.4.2, p. 182] (book p. 182; PDF p. 200).

## Gotcha Ledger

- G-U3a-01: Section 3.1 contains only two numbered subsections (`§3.1.1` and `§3.1.2`; there is no `§3.1.3`), and Chapter 3 uses a constant page offset `PDF page = book page + 18` because p. 140 is an unnumbered blank verso omitted from the PDF. [PPA §3.1, p. 141] (book p. 141; PDF p. 159)
- G-U3a-02: In `FUN`, every expression `e ∈ Exp` carries a top-level label (`e ::= t^ℓ`) whereas terms `t ∈ Term` are unlabelled, `let x = e₁ in e₂` is non-recursive (`x` bound only in `e₂`, unlike `fun f x => e₀` which binds both `f` and `x` in `e₀`), and parentheses carry no extra labels. [PPA §3.1, p. 142] (book p. 142; PDF p. 160)
- G-U3a-03: Pure 0-CFA tracks only function abstractions in `Val̂ = 𝒫(Term)` (ignoring non-function constants in `[con]` and ignoring closure environments) and merges bindings of identically named variables in `ρ̂(x)`, so `α`-renaming distinct bound variables apart strictly improves or preserves precision. [PPA §3.1.1, p. 144] (book p. 144; PDF p. 162)
- G-U3a-04: In Table 3.1, `[fn]` and `[fun]` do *not* demand `(Ĉ, ρ̂) ⊨ e₀` at definition sites; body acceptability `(Ĉ, ρ̂) ⊨ t₀^{ℓ₀}` (and `{fun f x => t₀^{ℓ₀}} ⊆ ρ̂(f)`) is demanded inside `[app]` *only* when the abstraction belongs to `Ĉ(ℓ₁)`, avoiding analysis of unreachable bodies (unlike Example 3.3 where `Ĉ_e(3) = ρ̂_e(y) = ∅`). [PPA Table 3.1, p. 146] (book p. 146; PDF p. 164)
- G-U3a-05: Pure 0-CFA in Table 3.1 is both *context-insensitive* (all calls to a function share one `ρ̂(x)` and one body cache) and *flow-insensitive* (`FUN` has no side effects, and `[app]` analyses operand `t₂^{ℓ₂}` even when `Ĉ(ℓ₁) = ∅`). [PPA §3.1.1, p. 150] (book p. 150; PDF p. 168)
- G-U3a-06: Table 3.1 cannot be defined by structural induction on `e` because `[app]` checks `(Ĉ, ρ̂) ⊨ t₀^{ℓ₀}` for `t₀^{ℓ₀}` drawn from `Ĉ(ℓ₁)` rather than subexpressions of `e`; acceptability must be defined coinductively as `⊨ = gfp(𝒬)` so cyclic recursive calls like `loop` (Example 3.6) are accepted. [PPA §3.1.2, p. 150] (book p. 150; PDF p. 168)
- G-U3a-07: The specification of acceptable analyses uses a *greatest* fixed point (`⊨ = gfp(𝒬)` on predicates over `Cachê × Env̂ × Exp`), whereas computing the most precise acceptable result uses a *least* fixed point (`lfp(F_⋆)` on `Cachê_⋆ × Env̂_⋆`). [PPA §3.1.2, p. 152] (book p. 152; PDF p. 170)
- G-U3a-08: `FUN`'s SOS (Tables 3.2 and 3.3) uses explicit environments `ρ` and closures `close t in ρ` with `bind ρ in ie` rather than substitution because β-substitution destroys syntactic identity and labels of function abstractions during evaluation. [PPA §3.2.1, p. 153] (book p. 153; PDF p. 171)
- G-U3a-09: In `IExp`/`ITerm`, bodies inside `fn x => e₀`, `fun f x => e₀`, and `close t in ρ` remain ordinary source `e₀ ∈ Exp` and `t ∈ Term`, and `[fn]`/`[fun]` restrict captured environments to `FV(...)`, ensuring closure environments are finite non-cyclic trees so `ρ ℛ ρ̂` is well-founded without coinduction. [PPA §3.2.1, p. 154] (book p. 154; PDF p. 172)
- G-U3a-10: `[bind₂]` steps `(bind ρ₁ in v₁^{ℓ₁})^ℓ → v₁^ℓ` and `[if₂]`/`[if₃]` step `(if true^{ℓ₀} then t₁^{ℓ₁} else e₂)^ℓ → t₁^ℓ` and `(if false^{ℓ₀} then e₁ else t₂^{ℓ₂})^ℓ → t₂^ℓ` — ALL three relabel the returned inner subterm to outer label `ℓ` so outer labels never change (`p. 157`), letting `Fact 3.11` discharge `[if₂]`, `[if₃]`, and `[bind₂]` directly in `Theorem 3.10`. [PPA Table 3.2, p. 155] (book p. 155; PDF p. 173); [PPA Table 3.3, p. 156] (book p. 156; PDF p. 174)
- G-U3a-11: In Table 3.3 `[let₂]`, `ρ₀ = ρ | FV(e₂)` does not subtract `x`, whereas `[fn]` and `[fun]` in Table 3.2 restrict to `FV(fn x => e₀)` and `FV(fun f x => e₀)` (excluding bound variables); in `[app_fun]`, `[x ↦ v₂]` is appended **after** `[f ↦ close ...]` (`ρ₂[x ↦ v₂]` where `ρ₂ = ρ₁[f ↦ close (fun f x => e₁) in ρ₁]`), matching `Example 3.8` (`[f ↦ ...][x ↦ ...]`). [PPA Table 3.2, p. 155] (book p. 155; PDF p. 173); [PPA Table 3.3, p. 156] (book p. 156; PDF p. 174)
- G-U3a-12: The `pdftotext` OCR layer of `ppa.pdf` erases the premises above fraction bars in Tables 3.2 and 3.3, the entire statement body of `Fact 3.11` (`If (Ĉ, ρ̂) ⊨ it^{ℓ₁} and Ĉ(ℓ₁) ⊆ Ĉ(ℓ₂) then (Ĉ, ρ̂) ⊨ it^{ℓ₂}.`) on p. 160, and the displayed `⨅` equation in Proposition 3.24 on p. 180. [PPA Fact 3.11, p. 160] (book p. 160; PDF p. 178)
- G-U3a-13: On total `Env̂ = Var → Val̂`, the conjunct `dom(ρ) ⊆ dom(ρ̂)` in `ρ ℛ ρ̂` is vacuously true (`dom(ρ̂) = Var`), whereas on finite `Env̂_⋆ = Var_⋆ → Val̂_⋆` it enforces `dom(ρ) ⊆ Var_⋆`; constants `c ∈ Const` satisfy `c 𝒱 (ρ̂, v̂)` vacuously even when `v̂ = ∅`. [PPA §3.2.2, p. 158] (book p. 158; PDF p. 176)
- G-U3a-14: Proposition 3.13 holds because in `[app]`, `t ∈ Ĉ(ℓ₁)` sits on the *left* (contravariant premise) of `⇒`: intersecting a family `{Ĉ_i}` shrinks `⋂_i Ĉ_i(ℓ₁)`, so any surviving `t` belonged to every `Ĉ_i(ℓ₁)` and triggered every `(Ĉ_i, ρ̂_i)`. [PPA §3.2.3, p. 164] (book p. 164; PDF p. 182)
- G-U3a-15: Example 3.15 (p. 164) silently reuses the symbol `(Ĉ'_e, ρ̂'_e)` for an *acceptable* over-approximation (`Ĉ'_e(3) = ρ̂'_e(y) = {fn x => x^1}`), whereas Examples 3.3 and 3.5 used `(Ĉ'_e, ρ̂'_e)` for an *unacceptable* under-approximation (`ρ̂'_e(x) = ∅`). [PPA Example 3.15, p. 164] (book p. 164; PDF p. 182)
- G-U3a-16: Replacing coinductive `⊨ = gfp(𝒬)` with inductive `⊨' = lfp(𝒬)` causes self-application `Ω = ((fn x => (x^ℓ x^ℓ)^ℓ)^ℓ (fn x => (x^ℓ x^ℓ)^ℓ)^ℓ)^ℓ` to have **empty** solution set `∅` (not a Moore family, since every Moore family contains `⨅ ∅ = ⊤`, Proposition 3.16). [PPA Proposition 3.16, p. 165] (book p. 165; PDF p. 183)
- G-U3a-17: Reformulating `⊨_A` into `⊨_B` with `⊨_A ⇐ ⊨_B` guarantees every solution of `⊨_B` is semantically sound via `⊨_A` *without* `⊨_B` itself satisfying subject reduction; for `⊨_s` vs `⊨`, only `⊨ ⇐ ⊨_s` holds (not `⇒`) because `⊨_s` analyses unreachable function bodies. [PPA §3.3, p. 168] (book p. 168; PDF p. 186)
- G-U3a-18: Table 3.5 (`⊨_s`) moves `(Ĉ, ρ̂) ⊨_s e₀` (and `{fun f x => e₀} ⊆ ρ̂(f)`) from `[app]` into `[fn]`/`[fun]` so every recursive appeal is on a strict subexpression; consequently `𝒬_s` has a **unique** fixed point (`lfp(𝒬_s) = gfp(𝒬_s)`), requiring no coinduction (Example 3.17). [PPA §3.3.1, p. 169] (book p. 169; PDF p. 187)
- G-U3a-19: The upper bound `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` (restricting all sets to `Term_⋆` and outside `Lab_⋆, Var_⋆` to `∅`) is **essential** in Propositions 3.18 and 3.21: without it, `Ĉ(ℓ₁)` could contain an alien lambda `fn x => t₀^{ℓ₀} ∉ Term_⋆` whose body `t₀^{ℓ₀}` was never checked by `⊨_s e_⋆` or `𝒞_⋆⟦e_⋆⟧`! [PPA Proposition 3.18, p. 172] (book p. 172; PDF p. 190)
- G-U3a-20: Unlike Proposition 3.13 (proved by coinduction over infinite domains), Proposition 3.19 proves the Moore-family property of `⊨_s` on `Cachê_⋆ × Env̂_⋆` purely by structural induction for `⊤` and binary `⊓`, exploiting finiteness of `Cachê_⋆ × Env̂_⋆` to reduce arbitrary `⨅ Y` to finite meets. [PPA Proposition 3.19, p. 173] (book p. 173; PDF p. 191)
- G-U3a-21: Sans-serif `C(ℓ)` and `r(x)` in `𝒞_⋆⟦e_⋆⟧` are *pure syntax* (constraint variables), never to be confused with semantic sets `Ĉ(ℓ)` and `ρ̂(x)`, and conditional constraints `{t} ⊆ rhs' ⇒ lhs ⊆ rhs` only ever place singleton `{t}` (`t ∈ Term_⋆`) in the guard, ensuring `F_⋆` is monotone! [PPA §3.4, p. 174] (book p. 174; PDF p. 192)
- G-U3a-22: For `e_⋆` of size `n`, `𝒞_⋆⟦e_⋆⟧` contains `O(n)` unconditional constraints `(3.6)` and `O(n²)` conditional constraints `(3.7)` (not `O(n²)` and `O(n⁴)`), because each `[app]` node emits only `2` conditional constraints per abstraction in `Term_⋆`. [PPA §3.4, p. 175] (book p. 175; PDF p. 193)
- G-U3a-23: On p. 176 (§3.4.2), the text misprints `"guaranteed by Propositions 3.18 and 3.21"` for least-solution existence (the existence proposition for `⊨_s` is **Proposition 3.19**, not 3.18), and on p. 177 misprints `Cachê_⋆ × Val̂_⋆` for `Cachê_⋆ × Env̂_⋆` in the `O(n²)` height / `O(n⁵)` naive fixed-point iteration bound (`[external: Kleene]`). [PPA §3.4.2, p. 176] (book p. 176; PDF p. 194)
- G-U3a-24: In Table 3.7 Step 2, a conditional constraint `{t} ⊆ p ⇒ p₁ ⊆ p₂` **must** be inserted into **both** `E[p₁]` and `E[p]`: `E[p₁]` handles terms arriving at `p₁` after `t ∈ D[p]`, while `E[p]` handles `t` arriving at `p` when `D[p₁]` is already non-empty (omitting `E[p]` silently loses flows!). [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196)
- G-U3a-25: Table 3.7's `O(n³)` bound counts *edge-traversal steps* (`≤ n` worklist pops per node × `O(n²)` total edges across `E`); achieving `O(n³)` *elementary operations* rather than `O(n⁴)` set-union work requires propagating newly added `(q, t)` elements individually with `O(1)` bitset membership checks. [PPA §3.4.2, p. 181] (book p. 181; PDF p. 199)
- G-U3a-26: Corollary 3.25 proves Table 3.7 computes a *sound* solution `(Ĉ, ρ̂) ⊨ e_⋆` (and the *least* solution of `𝒞_⋆⟦e_⋆⟧` and `⊨_s e_⋆` in `Cachê_⋆ × Env̂_⋆`), **not** necessarily the least solution of `(Ĉ, ρ̂) ⊨ e_⋆` when unreachable function bodies are present; open-system replacement `e_⋆ ↦ e'_⋆` preserves `(Ĉ, ρ̂) ⊨ e'_⋆` whenever `(Ĉ, ρ̂)` satisfies the replacement fragment's clauses without label/variable capture clashes. [PPA Corollary 3.25, p. 182] (book p. 182; PDF p. 200)
