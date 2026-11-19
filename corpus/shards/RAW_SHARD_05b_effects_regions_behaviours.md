<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 5b (Chapter 5 §§5.4-5.5, Concluding Remarks, Mini Projects 5.1-5.5, and Exercises 5.1-5.15). -->

# RAW_SHARD_05b — Chapter 5 Effects, Region Inference, Behaviours, and End Matter (Unit 5b)

Source: *Principles of Program Analysis* (Nielson, Nielson, Hankin), corrected 2nd printing, 2005.
Scope: Shared-page boundary note on the top 4 lines of book p. 319 concluding §5.3.4 (whose Corollary 5.23
belongs to Unit 5a `RAW_SHARD_05a_annotated_types_inference.md`), §5.4 Effects (§5.4.1 Side Effect Analysis,
§5.4.2 Exception Analysis, §5.4.3 Region Inference), §5.5 Behaviours (§5.5.1 Communication Analysis),
Chapter 5 Concluding Remarks, Mini Projects 5.1–5.5, and Exercises 5.1–5.15, spanning book pages 319–363 /
PDF pages 336–380 (unnumbered blank verso book p. 364 is absent from the PDF before Chapter 6 on book p. 365 /
PDF p. 381).

Coordinates: PDF page = book page + 17 throughout Chapter 5 (45 rendered pages in Unit 5b, PDF pages 336–380).
Section and end-matter starts in Unit 5b: §5.3.4 carryover (top 4 lines) and §5.4 Effects on p. 319 (§5.4.1
on p. 319, §5.4.2 on p. 325, §5.4.3 on p. 330), §5.5 Behaviours and §5.5.1 Communication Analysis on p. 339,
Concluding Remarks on p. 349, Mini Projects 5.1–5.5 on p. 353, and Exercises 5.1–5.15 on p. 359 (concluding on
p. 363) [PPA §5.4, p. 319] (book p. 319; PDF p. 336); [PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380).

Conventions:

- Every source reference pairs a strict single-page inline locator token with its singular book/PDF coordinate
  companion, for example [PPA §5.4, p. 319] (book p. 319; PDF p. 336), [PPA Table 5.9, p. 322] (book p. 322; PDF p. 339),
  or [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365).
- Book-numbered items preserve their exact printed kind word, number, and caption across Unit 5b's closed
  47-item universe: 14 shared-sequence statements (`Example 5.24`–`Example 5.37`, contiguous with `5.1`–`5.23`
  in Unit 5a; there are no numbered Theorems, Lemmas, Propositions, Corollaries, Facts, or Definitions in
  §§5.4–5.5), 10 tables (`Table 5.9`–`Table 5.18`), 2 figures (`Figure 5.1`–`Figure 5.2`), 5 mini projects
  (`Mini Project 5.1`–`Mini Project 5.5`), 15 exercises (`Exercise 5.1`–`Exercise 5.15`, with `Exercise* 5.4`
  and `Exercise* 5.10` starred in the printed book), and 1 numbered equation display `(5.2)` inside
  `Exercise* 5.4` on p. 359. Unnumbered definitions, semantic rules, proof/remark paragraphs, and the two
  printed `Remark.` blocks (p. 325 and p. 330) carry non-book identifiers `[U5b:<section>-<letter>]`.
- Every grammar, operational semantics rule, inference table, subtyping/behaviour ordering, figure, example,
  mini project, and exercise is transcribed directly from visual inspection of all 45 rendered page images
  (PDF pages 336–380) rather than the PDF OCR text layer, which erases the 3 store SOS rules (`!ξ`, `ξ := e`,
  `e₁ ; e₂`) on p. 320, `[fn]` in Tables 5.9, 5.10, and 5.16, half of Table 5.12, `v₁ op v₂ → v` in Table 5.14,
  9 of the 22 axioms and rules in Table 5.18, subtyping rules on p. 324 and p. 329, and display `(5.2)` on
  p. 359.
- Terms absent from the book carry `[external]`. Deductions, worked counterexamples, and solver/debugging
  refinements not printed in the text carry `[derived]`. Source misprints and internal tensions are transcribed
  verbatim as printed and logged under `Findings` (`F-U5b-01`–`F-U5b-14`).
- Notation: `e ∈ Exp` expressions (`fn_π x => e₀`, `fun_π f x => e₀`); `π ∈ Pnt` program points; `ς ∈ Store`
  concrete store; `ξ ∈ Loc` store locations; `φ ∈ Ann_*` annotations, effects, or behaviours; `ϖ` point sets
  in §5.4.1; `τ̂ ∈ Type_*` annotated types with underlying type `⌊τ̂⌋`; `σ̂ ∈ Scheme_*` type schemes;
  `α ∈ TVar` type variables (`'a`, `'b`), `β ∈ AVar` annotation/effect/behaviour variables (`'1`, `'2`),
  `ϱ ∈ RVar` region variables (`''1`, `''2`); `Γ̂` type environment; `τ̂ ≤ τ̂'` shape-conformant subtyping;
  `s` exception identifier; `rn ∈ RName` (`r1`, `r2`), `r ∈ Reg_*`, `ee ∈ EExp` extended expressions (`at r`,
  `fun_π f [ϱ⃗] x => ee₀ at r`, `ee[r⃗] at r`, `letregion ϱ⃗ in ee`), `τ̂ @ r` extended types (printed tightly
  around `@` in the book), `v ∈ EVal = RName × Offset`, `w ∈ SVal`, `ς ⧹⧹ rn⃗` region deallocation,
  `Observe(Γ̂, τ̂, r')(φ)` effect masking; `ch ∈ Chan` (`chan1`, `chan2`), `p ∈ Proc` (`proc1`, `proc2`),
  `CP ∈ 𝒫_fin(Chan)`, `PP ∈ Proc →_fin Exp`, `E` single-hole evaluation context (`e₁ → e₂`, `e₁ ⇒ e₂`,
  `CP₁, PP₁ ⇒ CP₂, PP₂`); `Λ` silent/empty behaviour, `φ₁ ; φ₂` sequential composition, `φ₁ + φ₂` choice,
  `rec β.φ` recursive behaviour, `τ̂ chan r`, `spawn φ`, `r!τ̂`, `r?τ̂`, `φ₁ ⊑ φ₂` behaviour preorder;
  `ψ ∈ LAnn` call-site label annotations (`Exercise 5.6`); `num^φ` with `φ = scale BASE base` (`Mini Project
  5.5`); `■` end-of-item marker as printed.

---

## 5.3.4 Boundary Carryover and 5.4 Effects

Context: Book p. 319 is shared between the final 4 lines of §5.3.4 (completing Corollary 5.23's least-element
argument from Unit 5a) and the opening of §5.4 (*Effects*), which introduces subtyping, `let`-polymorphism,
and polymorphic recursion across three progressive effect analyses
[PPA §5.3.4, p. 319] (book p. 319; PDF p. 336); [PPA §5.4, p. 319] (book p. 319; PDF p. 336).

### [U5b:5.3.4-z] Shared-page boundary note concluding §5.3.4 (`θ_A` minimality, owned by Unit 5a)
- Statement: The top 4 lines of book p. 319 complete §5.3.4 (`Corollary 5.23`, counted in Unit 5a
  `RAW_SHARD_05a_annotated_types_inference.md` so Chapter 5's shared statement sequence partitions cleanly into
  `5.1`–`5.23` in Unit 5a and `5.24`–`5.37` in Unit 5b): it is immediate that `dom(θ_A) = AV(C)` and `θ_A ⊨ C`;
  if also `dom(θ) = AV(C)` and `θ ⊨ C`, then `∀β : θ β ⊇ θ_A β` (written `θ ⊒ θ_A`), showing that `θ_A` is the
  least element of the Moore family displayed in Lemma 5.22
  [PPA Lemma 5.22, p. 317] (book p. 317; PDF p. 334); [PPA Corollary 5.23, p. 318] (book p. 318; PDF p. 335).
- Citation: [PPA §5.3.4, p. 319] (book p. 319; PDF p. 336)

### [U5b:5.4-a] Section 5.4 roadmap — Subtyping, `let`-polymorphism, and polymorphic recursion
- Statement: The Type and Effect System for Control Flow Analysis in §5.1 is a simple syntax-directed system
  using a form of subeffecting over set annotations. Much more powerful Type and Effect Systems (with more
  demanding implementation techniques) arise by incorporating *subtyping*, *`let`-polymorphism*, or
  *polymorphic recursion*. Although these mechanisms can be combined, §5.4 presents them one at a time:
  1. *Side Effect Analysis* (§5.4.1): `FUN` extended with assignments, using subeffecting and subtyping.
  2. *Exception Analysis* (§5.4.2): `FUN` extended with exceptions, using subeffecting, subtyping, and
     `let`-polymorphism.
  3. *Region Inference* (§5.4.3): stack-based region analysis and translation for `FUN`, using polymorphic
     recursion (over effects and regions).
- Citation: [PPA §5.4, p. 319] (book p. 319; PDF p. 336)

### Findings (5.4)
- F-U5b-01 (`[Domain Restriction on θ_A in §5.3.4 Carryover]`): At the top of p. 319, `θ_A` is defined with
  `dom(θ_A) = AV(C)`; if an unconstrained annotation variable `β ∉ AV(C)` appears in `(θ Γ̂)` or `τ̂` returned
  by `𝒲_CFA` (for example `'1` in `fn_X x => x 1`), `θ_A` leaves `β` uninstantiated unless extended by
  defaulting `β ↦ ∅` over `AV(θ Γ̂, τ̂) \ AV(C)` `[derived]`. [PPA §5.3.4, p. 319] (book p. 319; PDF p. 336)

### Projections (5.4)
- cs_theory: Section 5.4 organises effect-system expressiveness along a clean orthogonal lattice of type-theoretic
  mechanisms — `subeffecting (§5.1) → shape-conformant subtyping (§5.4.1) → Hindley/Milner let-polymorphism
  (§5.4.2) → effect/region-polymorphic recursion with lexical effect masking (§5.4.3)` — while keeping effects
  *restricted* (no types inside effects) so underlying Hindley/Milner type inference stays decoupled from
  effect solving.
- swe_architecture: Presenting subeffecting, subtyping, `let`-polymorphism, and polymorphic recursion as
  modular judgement layers (`Γ̂ ⊢ e : σ̂ & φ`) allows a production static-analysis compiler pass to reuse a
  single AST walker and swap only the constraint solver backend (set-inclusion worklist vs unification +
  polarised subtyping vs fixed-point region solver) `[external]`.
- practical_debugging: When diagnosing false positives in an effect checker, §5.4's hierarchy pinpoints which
  mechanism is missing: cross-branch effect smearing at returns indicates missing subeffecting, callback
  argument smearing indicates missing subtyping (`Example 5.27`), higher-order wrapper smearing indicates
  missing `let`-polymorphism (`Example 5.30`), and recursive accumulator retention indicates missing
  polymorphic recursion (`§5.4.3`) `[derived]`.
- cyber: Effect judgements `Γ̂ ⊢ e : τ̂ & φ` enforce static `[external: capability-safe effect systems]` and
  privilege budgets: latent effects on function arrows `τ̂₁ →^φ τ̂₂` expose dormant I/O, state-mutation,
  exception, or `[external: arena]`-allocation authority carried by higher-order callbacks before execution.

---

## 5.4.1 Side Effect Analysis

Context: Section 5.4.1 extends `FUN` with mutable reference variables (`new_π`, `!x`, `x := e₀`, `e₁ ; e₂`),
specifies a store-passing Natural Semantics and `Table 5.9` (`Γ̂ ⊢_SE e : τ̂ & φ`), introduces shape-conformant
subtyping `τ̂ ≤ τ̂'` with invariant `ref_ϖ τ̂` payloads, and contrasts Effect Systems against Annotated Type
Systems [PPA §5.4.1, p. 319] (book p. 319; PDF p. 336); [PPA §5.4.1, p. 325] (book p. 325; PDF p. 342).

### [U5b:5.4.1-a] Syntax of `FUN` with mutable reference variables
- Statement: Extends `FUN` ([PPA §5.1, p. 283] (book p. 283; PDF p. 300)) with imperative constructs for
  creating, dereferencing, updating, and sequencing reference variables:
  ```text
  e ::= ··· | new_π x := e₁ in e₂ | !x | x := e₀ | e₁ ; e₂
  ```
  - `new_π x := e₁ in e₂` creates a fresh reference variable `x` initialised to the value of `e₁` with lexical
    scope `e₂`; its creation at program point `π` remains visible in the effect *outside* `e₂` so the analysis
    determines whether functions allocate memory.
  - `!x` reads the value of reference variable `x`; `x := e₀` updates `x` to the value of `e₀` (returning the
    assigned value, p. 321); `e₁ ; e₂` evaluates `e₁` for its side effects and then `e₂`.
- Citation: [PPA §5.4.1, p. 319] (book p. 319; PDF p. 336)

### Example 5.24 — Imperative Fibonacci computation in reference cell `r`
- Statement: Computing the Fibonacci number of positive `x` into reference variable `r`:
  ```text
  new_R r:=0
  in let fib = fun_F f z => if z<3 then r:=!r+1
                            else f(z-1); f(z-2)
     in fib x; !r
  ```
  Creates `r` at `R` initialised to `0`, defines recursive `fib`, applies `fib x`, and returns `!r`; each
  execution of `r:=!r+1` increments `r`, so `fib` accesses and assigns the reference variable created at `R`. `■`
- Citation: [PPA Example 5.24, p. 319] (book p. 319; PDF p. 336); [PPA Example 5.24, p. 320] (book p. 320; PDF p. 337)

### [U5b:5.4.1-b] Analysis aim, store-passing Natural Semantics, and `Ann_SE` / `ϖ` / `Type_SE` grammars
- Statement:
  - *Aim*: record, for each subexpression, which locations have been created, accessed, and assigned.
  - *Store-passing Natural Semantics* (`⊢ ⟨e, ς₁⟩ → ⟨v, ς₂⟩`, p. 320 — last 3 rules erased in PDF OCR, restored
    from rendered page image): introduces dynamic *locations* `ξ ∈ Loc` and finite *stores*
    `ς ∈ Store = Loc →_fin Val`, where `Val` includes constants `c`, closed abstractions `fn_π x => e`, and
    locations `ξ ∈ Loc` (finding F-U5b-02). Existing `Table 5.4` clauses ([PPA Table 5.4, p. 292]
    (book p. 292; PDF p. 309)) thread the store left-to-right, e.g. for `let`:
    ```text
    ⊢ ⟨e₁, ς₁⟩ → ⟨v₁, ς₂⟩    ⊢ ⟨e₂[x ↦ v₁], ς₂⟩ → ⟨v₂, ς₃⟩
    ─────────────────────────────────────────────────────────
              ⊢ ⟨let x = e₁ in e₂, ς₁⟩ → ⟨v₂, ς₃⟩
    ```
    Axioms and rules for the imperative constructs:
    ```text
    ⊢ ⟨e₁, ς₁⟩ → ⟨v₁, ς₂⟩    ⊢ ⟨e₂[x ↦ ξ], ς₂[ξ ↦ v₁]⟩ → ⟨v₂, ς₃⟩
    ────────────────────────────────────────────────────────────────   where ξ does not occur in dom(ς₂)
               ⊢ ⟨new_π x := e₁ in e₂, ς₁⟩ → ⟨v₂, ς₃⟩

    ⊢ ⟨!ξ, ς⟩ → ⟨ς(ξ), ς⟩

        ⊢ ⟨e, ς₁⟩ → ⟨v, ς₂⟩
    ─────────────────────────────
    ⊢ ⟨ξ:=e, ς₁⟩ → ⟨v, ς₂[ξ ↦ v]⟩

    ⊢ ⟨e₁, ς₁⟩ → ⟨v₁, ς₂⟩    ⊢ ⟨e₂, ς₂⟩ → ⟨v₂, ς₃⟩
    ─────────────────────────────────────────────────
              ⊢ ⟨e₁; e₂, ς₁⟩ → ⟨v₂, ς₃⟩
    ```
    Note (`p. 321`): `new` creates fresh `ξ ∉ dom(ς₂)`, initialises `ξ` to `v₁`, and syntactically substitutes
    `ξ` for `x` in `e₂` so subsequent dereferences and assignments act on `ξ`; assignment returns the assigned
    value `v`.
  - *Annotations, point sets, and annotated types* (`p. 321`, equal modulo `UCAI`):
    ```text
    φ ∈ Ann_SE  ::= {!π} | {π:=} | {new π} | φ₁ ∪ φ₂ | ∅
    ϖ           ::= π | ϖ₁ ∪ ϖ₂ | ∅                          (written ϖ = {π₁, ···, π_n}; finding F-U5b-03)
    τ̂ ∈ Type_SE ::= int | bool | τ̂₁ →^φ τ̂₂ | ref_ϖ τ̂
    ```
    `!π`, `π:=`, and `new π` record accessing, assigning, and creating a location from program point `π`;
    `ref_ϖ τ̂` types a location created at one of the program points in `ϖ` holding values of annotated type
    `τ̂`; `Γ̂` maps variables to `Type_SE`; typing judgements have the form `Γ̂ ⊢_SE e : τ̂ & φ`.
- Citation: [PPA §5.4.1, p. 320] (book p. 320; PDF p. 337); [PPA §5.4.1, p. 321] (book p. 321; PDF p. 338)

### Example 5.25 — Annotated types for `r` and `fib` in Example 5.24
- Statement: In the Fibonacci program of Example 5.24, `r` has annotated type `ref_{R} int` and `fib` has
  annotated type `int →^{!R, R:=} int`, since `fib` maps integers to integers while accessing and updating a
  reference created at `R`. `■`
- Citation: [PPA Example 5.25, p. 321] (book p. 321; PDF p. 338)

### Table 5.9 — Side Effect Analysis
- Statement: Inference axioms and rules for `Γ̂ ⊢_SE e : τ̂ & φ` (`[fn]` and `[deref]` side condition erased in
  PDF OCR, verified on rendered p. 322):
  ```text
  [con]    Γ̂ ⊢_SE c : τ_c & ∅

  [var]    Γ̂ ⊢_SE x : τ̂ & ∅                                            if Γ̂(x) = τ̂

  [fn]     Γ̂[x ↦ τ̂_x] ⊢_SE e₀ : τ̂₀ & φ₀
           ──────────────────────────────────────────
           Γ̂ ⊢_SE fn_π x => e₀ : τ̂_x →^{φ₀} τ̂₀ & ∅

  [fun]    Γ̂[f ↦ τ̂_x →^{φ₀} τ̂₀][x ↦ τ̂_x] ⊢_SE e₀ : τ̂₀ & φ₀
           ────────────────────────────────────────────────────
           Γ̂ ⊢_SE fun_π f x => e₀ : τ̂_x →^{φ₀} τ̂₀ & ∅

  [app]    Γ̂ ⊢_SE e₁ : τ̂₂ →^{φ₀} τ̂₀ & φ₁    Γ̂ ⊢_SE e₂ : τ̂₂ & φ₂
           ────────────────────────────────────────────────────────
                      Γ̂ ⊢_SE e₁ e₂ : τ̂₀ & φ₁ ∪ φ₂ ∪ φ₀

  [if]     Γ̂ ⊢_SE e₀ : bool & φ₀    Γ̂ ⊢_SE e₁ : τ̂ & φ₁    Γ̂ ⊢_SE e₂ : τ̂ & φ₂
           ────────────────────────────────────────────────────────────────────
                    Γ̂ ⊢_SE if e₀ then e₁ else e₂ : τ̂ & φ₀ ∪ φ₁ ∪ φ₂

  [let]    Γ̂ ⊢_SE e₁ : τ̂₁ & φ₁    Γ̂[x ↦ τ̂₁] ⊢_SE e₂ : τ̂₂ & φ₂
           ──────────────────────────────────────────────────────
                   Γ̂ ⊢_SE let x = e₁ in e₂ : τ̂₂ & φ₁ ∪ φ₂

  [op]     Γ̂ ⊢_SE e₁ : τ_op^1 & φ₁    Γ̂ ⊢_SE e₂ : τ_op^2 & φ₂
           ────────────────────────────────────────────────────
                    Γ̂ ⊢_SE e₁ op e₂ : τ_op & φ₁ ∪ φ₂

  [deref]  Γ̂ ⊢_SE !x : τ̂ & {!π₁, ···, !π_n}                             if Γ̂(x) = ref_{π₁, ···, π_n} τ̂

  [ass]    Γ̂ ⊢_SE e : τ̂ & φ
           ─────────────────────────────────────────                   if Γ̂(x) = ref_{π₁, ···, π_n} τ̂
           Γ̂ ⊢_SE x := e : τ̂ & φ ∪ {π₁:=, ···, π_n:=}

  [new]    Γ̂ ⊢_SE e₁ : τ̂₁ & φ₁    Γ̂[x ↦ ref_{π} τ̂₁] ⊢_SE e₂ : τ̂₂ & φ₂
           ─────────────────────────────────────────────────────────────
                Γ̂ ⊢_SE new_π x := e₁ in e₂ : τ̂₂ & (φ₁ ∪ φ₂ ∪ {new π})

  [seq]    Γ̂ ⊢_SE e₁ : τ̂₁ & φ₁    Γ̂ ⊢_SE e₂ : τ̂₂ & φ₂
           ────────────────────────────────────────────
                   Γ̂ ⊢_SE e₁ ; e₂ : τ̂₂ & φ₁ ∪ φ₂

  [sub]    Γ̂ ⊢_SE e : τ̂ & φ
           ───────────────────                                         if τ̂ ≤ τ̂' and φ ⊆ φ'
           Γ̂ ⊢_SE e : τ̂' & φ'
  ```
- Side conditions:
  - `[con]` and `[var]` have empty effect `∅`; `[fn]` and `[fun]` move body effect `φ₀` onto the arrow
    `τ̂_x →^{φ₀} τ̂₀` while emitting `∅` as the definition-time effect because defining a function causes no
    observable store effects until `[app]` unleashes `φ₁ ∪ φ₂ ∪ φ₀` (p. 323).
- Citation: [PPA Table 5.9, p. 322] (book p. 322; PDF p. 339); [PPA §5.4.1, p. 323] (book p. 323; PDF p. 340)

### Example 5.26 — Enabling `new`-to-`let` demotion via absence of `B:=`
- Statement: Consider:
  ```text
  new_A x:=1
  in (new_B y:=!x in (x:=!y+1; !y+3))
   + (new_C x:=!x in (x:=!x+1; !x+1))
  ```
  Evaluating to `4 + 4 = 8`: the first summand has `int & {new B, !A, A:=, !B}` and the second (where inner `x`
  shadows outer `x`) has `int & {new C, !A, C:=, !C}`, giving overall `int & {new A, A:=, !A, new B, !B, new C,
  C:=, !C}`. Because `B:=` is absent from the effect, `y` (created at `B`) is never reassigned after creation,
  justifying transforming `new_B y:=!x in (x:=!y+1; !y+3)` into `let y=!x in (x:=y+1; y+3)`. `■`
- Citation: [PPA Example 5.26, p. 323] (book p. 323; PDF p. 340)

### [U5b:5.4.1-c] Subeffecting, shape-conformant subtyping `τ̂ ≤ τ̂'`, `ref` invariance, and conservative extension
- Statement: `[sub]` combines a separate *subeffecting* rule (`φ ⊆ φ'` modulo `UCAI`, as in §5.2.3 and
  `Exercise 5.3`) and a separate *subtyping* rule (`τ̂ ≤ τ̂'`), where `τ̂ ≤ τ̂'` is defined inductively by
  (first two rules erased in PDF OCR, restored from p. 324):
  ```text
  τ̂ ≤ τ̂

  τ̂'₁ ≤ τ̂₁    τ̂₂ ≤ τ̂'₂    φ ⊆ φ'
  ─────────────────────────────────
    (τ̂₁ →^φ τ̂₂) ≤ (τ̂'₁ →^{φ'} τ̂'₂)

  τ̂ ≤ τ̂'    τ̂' ≤ τ̂    ϖ ⊆ ϖ'
  ────────────────────────────
      ref_ϖ τ̂ ≤ ref_{ϖ'} τ̂'
  ```
  - *Variance*: `τ̂₁ →^φ τ̂₂` is *contravariant* in argument `τ̂₁` (`τ̂'₁ ≤ τ̂₁`) and *covariant* in `φ` and `τ̂₂`
    (reading `→` and `≤` as logical implication confirms direction); `ref_ϖ τ̂` is *covariant* in `ϖ` and
    **invariant** — both covariant (for `!x` reads) and contravariant (for `x := ···` writes) — in `τ̂`, which
    is essential for semantic correctness.
  - *Shape-conformant subtyping*: `τ̂₁ ≤ τ̂₂ ⇒ ⌊τ̂₁⌋ = ⌊τ̂₂⌋` (identical underlying shapes).
  - *Conservative extension* (`p. 325`): including `[sub]` — or adopting *either* subeffecting alone *or*
    subtyping alone, though **not** omitting both — yields a conservative extension of the underlying type
    system (`Table 5.1`, [PPA Table 5.1, p. 285] (book p. 285; PDF p. 302)).
- Citation: [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341); [PPA §5.4.1, p. 325] (book p. 325; PDF p. 342)

### Example 5.27 — Higher-order reader/writer callbacks under subtyping vs subeffecting
- Statement: Consider (omitting function labels, evaluating to `1 + 1 = 2`):
  ```text
  new_A x:=1
  in (fn f => f (fn y => !x) + f (fn z => (x:=z; z)))
     (fn g => g 1)
  ```
  The two functional arguments to `f` have `int →^{!A} int & ∅` and `int →^{A:=} int & ∅`. Giving `f` type
  `(int →^{!A, A:=} int) →^{!A, A:=} int`, subtyping coerces both arguments at their call sites via
  `(int →^{!A} int) ≤ (int →^{!A, A:=} int)` and `(int →^{A:=} int) ≤ (int →^{!A, A:=} int)`. With subeffecting
  *alone* (applied just before `[fn]`), both arguments themselves must be coarsened to
  `int →^{A:=, !A} int & ∅`. `■`
- Citation: [PPA Example 5.27, p. 324] (book p. 324; PDF p. 341); [PPA Example 5.27, p. 325] (book p. 325; PDF p. 342)

### [U5b:5.4.1-d] `Remark.` — Annotated Type Systems vs Effect Systems (unnumbered remark)
- Statement: Although no sharp formal boundary separates "Annotated Type Systems" and "Effect Systems",
  §5.4.1 is genuinely an *Effect System* because annotations describe internal computation steps rather than
  function inputs or outputs, whereas §5.1's CFA is an *Annotated Type System* because annotations describe
  intensional aspects of the semantic values produced. `■`
- Citation: [PPA §5.4.1, p. 325] (book p. 325; PDF p. 342)

### Findings (5.4.1)
- F-U5b-02 (`[Intermediate Location Syntax Omission]`): On p. 319, `!x` and `x := e₀` restrict their target to
  `x ∈ Var` without adding dynamic locations `ξ ∈ Loc` to `Exp` (unlike §5.5.1 on p. 339, which explicitly adds
  `| ch`), yet `new_π`'s operational rule on p. 320 substitutes `e₂[x ↦ ξ]` and evaluates `!ξ` and `ξ := e`;
  p. 320 also lists closed `fn_π x => e` in `Val` without noting `fun_π` unfolding from Table 5.4.
  [PPA §5.4.1, p. 319] (book p. 319; PDF p. 336); [PPA §5.4.1, p. 320] (book p. 320; PDF p. 337)
- F-U5b-03 (`[Unbraced Point-Set Grammar & Prose Slip]`): On p. 321, `ϖ ::= π | ϖ₁ ∪ ϖ₂ | ∅` omits braces around
  singleton `π` while two lines below writes `ϖ = {π₁, ···, π_n}` and Table 5.9 (`p. 322`) writes
  `ref_{π}` / `ref_{π₁, ···, π_n}`; on p. 323 line 15, the prose explaining `[app]` calls operator `e₁` in
  `e₁ e₂` `"the argument e₁"`. [PPA §5.4.1, p. 321] (book p. 321; PDF p. 338);
  [PPA Table 5.9, p. 322] (book p. 322; PDF p. 339); [PPA §5.4.1, p. 323] (book p. 323; PDF p. 340)

### Projections (5.4.1)
- cs_theory: Shape-conformant subtyping (`τ̂₁ ≤ τ̂₂ ⇒ ⌊τ̂₁⌋ = ⌊τ̂₂⌋`) enables a clean **two-stage inference
  reduction**: Stage 1 solves underlying Hindley/Milner type equalities over a free algebra; Stage 2 decomposes
  each structural inequality `(τ̂₁ →^{β₁} τ̂₂) ≤ (τ̂₃ →^{β₂} τ̂₄)` into contravariant `τ̂₃ ≤ τ̂₁`, covariant
  `τ̂₂ ≤ τ̂₄`, and `β₁ ⊆ β₂`, and each `(ref_{ϖ₁} τ̂₁) ≤ (ref_{ϖ₂} τ̂₂)` into **bidirectional**
  `τ̂₁ ≤ τ̂₂ ∧ τ̂₂ ≤ τ̂₁` plus `ϖ₁ ⊆ ϖ₂`, reducing inference to pure set-inclusion `[external: Horn clauses]`
  `[derived]`.
- swe_architecture: `Example 5.26` (`B:= ∉ φ`) is the exact static foundation of compiler **mutable-box
  unboxing / `let` promotion** (`[external: SML/NJ, OCaml flambda, JVM/V8 scalar replacement]`), while keeping
  `{new π}` unmasked on `new_π` exit (`Table 5.9` `[new]`) provides zero-allocation (`[external: @noalloc]`)
  verification for real-time audio, kernel, and `[external: HFT]` hot paths.
- practical_debugging: Two classic bugs in custom subtyping/effect checkers are (1) implementing arrow domain
  comparison covariantly (`τ̂₁ ≤ τ̂'₁` instead of `τ̂'₁ ≤ τ̂₁`), which unsoundly passes a callback demanding a
  narrow subtype to a caller supplying a wider supertype, and (2) making `ref_ϖ τ̂` covariant in `τ̂`, which
  allows overwriting a `ref_{R} (int →^∅ int)` alias with an impure `int →^{A:=} int` closure via an upcast
  reference `[derived]`.
- cyber: Enforcing payload **invariance** (`τ̂ ≤ τ̂' ∧ τ̂' ≤ τ̂`) on mutable cells `ref_ϖ τ̂` blocks write-side
  type/capability confusion (`[external: CWE-843]`, the exact soundness flaw behind
  `[external: Java/C# covariant ArrayStoreException]` and unsafe `[external: C/C++ T** pointer casts]`):
  without invariance, an attacker-controlled writer holding an upcast `ref` alias can inject a
  `[external: tainted]` or privileged-effect closure that honest readers invoke under a pure/untainted static
  type.

---

## 5.4.2 Exception Analysis

Context: Section 5.4.2 extends `FUN` with named exceptions (`raise s` and `handle s as e₁ in e₂`), defines
short-circuit Natural Semantics (`raise s ∈ Val`), and introduces Hindley–Milner type-and-effect schemes
`∀(ζ₁, ···, ζ_n). τ̂` in `Table 5.10` (`Γ̂ ⊢_ES e : σ̂ & φ`) with syntactic effect subtraction `φ \ {s}`
[PPA §5.4.2, p. 325] (book p. 325; PDF p. 342); [PPA Table 5.10, p. 328] (book p. 328; PDF p. 345).

### [U5b:5.4.2-a] Syntax of `FUN` with exceptions (`raise` and `handle`)
- Statement: Aim: determine, for each expression, which uncaught exceptions might result from evaluating it.
  Syntax extension over string exception names `s`:
  ```text
  e ::= ··· | raise s | handle s as e₁ in e₂
  ```
  If `e₂` raises `s₁`, `handle s₂ as e₁ in e₂` traps `s₁` and evaluates handler `e₁` when `s₁ = s₂`, and
  propagates `s₁` outward when `s₁ ≠ s₂`.
- Citation: [PPA §5.4.2, p. 325] (book p. 325; PDF p. 342); [PPA §5.4.2, p. 326] (book p. 326; PDF p. 343)

### Example 5.28 — Combinatorial `comb` with trapped and untrapped exceptions
- Statement: Computing binomial coefficient `C(x, y)`:
  ```text
  let comb = fun f x => fn y =>
               if x<0 then raise x-out-of-range
               else if y<0 or y>x then raise y-out-of-range
               else if y=0 or y=x then 1
               else f (x-1) y + f (x-1) (y-1)
  in handle x-out-of-range as 0 in comb x y
  ```
  `x-out-of-range` (when `x < 0`) is trapped and yields `0`; `y-out-of-range` (when `y < 0` or `y > x`)
  escapes untrapped. `■`
- Citation: [PPA Example 5.28, p. 326] (book p. 326; PDF p. 343)

### [U5b:5.4.2-b] Exception Natural Semantics and polymorphic `Ann_ES` / `Type_ES` / `Scheme_ES` grammars
- Statement:
  - *Semantics* (`pp. 326–327`): extends `Val` with `raise s` and adds short-circuit propagation clauses to
    `Table 5.4` (for example three `[app]` clauses propagating `raise s` from `e₁`, `e₂`, or `e₀[x ↦ v₂]`:
    `⊢ e₁ → raise s ⇒ ⊢ e₁ e₂ → raise s`; `⊢ e₁ → (fn_π x => e₀) ∧ ⊢ e₂ → raise s ⇒ ⊢ e₁ e₂ → raise s`;
    `⊢ e₁ → (fn_π x => e₀) ∧ ⊢ e₂ → v₂ ∧ ⊢ e₀[x ↦ v₂] → raise s ⇒ ⊢ e₁ e₂ → raise s`), plus:
    ```text
    ⊢ raise s → raise s

             ⊢ e₂ → v₂
    ─────────────────────────────   if v₂ ≠ raise s
    ⊢ handle s as e₁ in e₂ → v₂

    ⊢ e₂ → raise s    ⊢ e₁ → v₁
    ─────────────────────────────
    ⊢ handle s as e₁ in e₂ → v₁
    ```
    Because `raise s' ∈ Val`, when `e₂` raises `s' ≠ s` the middle rule propagates `v₂ = raise s'`, and when
    handler `e₁` raises an exception `v₁ = raise s''` the third rule propagates `v₁`.
  - *Polymorphic annotations, types, and type schemes* (`p. 327`, effects equal modulo `UCAI`):
    ```text
    φ ∈ Ann_ES  ::= {s} | φ₁ ∪ φ₂ | ∅ | β
    τ̂ ∈ Type_ES ::= int | bool | τ̂₁ →^φ τ̂₂ | α
    σ̂           ::= ∀(ζ₁, ···, ζ_n). τ̂
    ```
    where `ζ₁, ···, ζ_n` is a (possibly empty) list of type variables `α ∈ TVar` and annotation variables
    `β ∈ AVar` (`∀(). τ̂` is written `τ̂`).
- Citation: [PPA §5.4.2, p. 326] (book p. 326; PDF p. 343); [PPA §5.4.2, p. 327] (book p. 327; PDF p. 344)

### Example 5.29 — Polymorphic type scheme and instances for `fn_F f => fn_X x => f x`
- Statement: `fn_F f => fn_X x => f x` receives type scheme:
  ```text
  ∀'a, 'b, '1. ('a →^{'1} 'b) →^∅ ('a →^{'1} 'b)
  ```
  with instances such as `(int →^{x-out-of-range} int) →^∅ (int →^{x-out-of-range} int)` and
  `(int →^∅ bool) →^∅ (int →^∅ bool)`. `■`
- Citation: [PPA Example 5.29, p. 327] (book p. 327; PDF p. 344)

### Table 5.10 — Exception Analysis
- Statement: Inference axioms and rules for `Γ̂ ⊢_ES e : σ̂ & φ`, where `Γ̂` maps variables to type schemes
  (`[fn]` in Table 5.10 and subtyping display on p. 329 erased in PDF OCR, verified on rendered pp. 328–329):
  ```text
  [con]     Γ̂ ⊢_ES c : τ_c & ∅

  [var]     Γ̂ ⊢_ES x : σ̂ & ∅                                        if Γ̂(x) = σ̂

  [fn]      Γ̂[x ↦ τ̂_x] ⊢_ES e₀ : τ̂₀ & φ₀
            ──────────────────────────────────────────
            Γ̂ ⊢_ES fn_π x => e₀ : τ̂_x →^{φ₀} τ̂₀ & ∅

  [fun]     Γ̂[f ↦ τ̂_x →^{φ₀} τ̂₀][x ↦ τ̂_x] ⊢_ES e₀ : τ̂₀ & φ₀
            ────────────────────────────────────────────────────
            Γ̂ ⊢_ES fun_π f x => e₀ : τ̂_x →^{φ₀} τ̂₀ & ∅

  [app]     Γ̂ ⊢_ES e₁ : τ̂₂ →^{φ₀} τ̂₀ & φ₁    Γ̂ ⊢_ES e₂ : τ̂₂ & φ₂
            ────────────────────────────────────────────────────────
                       Γ̂ ⊢_ES e₁ e₂ : τ̂₀ & φ₁ ∪ φ₂ ∪ φ₀

  [if]      Γ̂ ⊢_ES e₀ : bool & φ₀    Γ̂ ⊢_ES e₁ : τ̂ & φ₁    Γ̂ ⊢_ES e₂ : τ̂ & φ₂
            ────────────────────────────────────────────────────────────────────
                     Γ̂ ⊢_ES if e₀ then e₁ else e₂ : τ̂ & φ₀ ∪ φ₁ ∪ φ₂

  [let]     Γ̂ ⊢_ES e₁ : σ̂₁ & φ₁    Γ̂[x ↦ σ̂₁] ⊢_ES e₂ : τ̂₂ & φ₂
            ──────────────────────────────────────────────────────
                    Γ̂ ⊢_ES let x = e₁ in e₂ : τ̂₂ & φ₁ ∪ φ₂

  [op]      Γ̂ ⊢_ES e₁ : τ_op^1 & φ₁    Γ̂ ⊢_ES e₂ : τ_op^2 & φ₂
            ────────────────────────────────────────────────────
                     Γ̂ ⊢_ES e₁ op e₂ : τ_op & φ₁ ∪ φ₂

  [raise]   Γ̂ ⊢_ES raise s : τ̂ & {s}

  [handle]  Γ̂ ⊢_ES e₁ : τ̂ & φ₁    Γ̂ ⊢_ES e₂ : τ̂ & φ₂
            ─────────────────────────────────────────────────────
            Γ̂ ⊢_ES handle s as e₁ in e₂ : τ̂ & φ₁ ∪ (φ₂ \ {s})

  [sub]     Γ̂ ⊢_ES e : τ̂ & φ
            ───────────────────                                     if τ̂ ≤ τ̂' and φ ⊆ φ'
            Γ̂ ⊢_ES e : τ̂' & φ'

  [gen]     Γ̂ ⊢_ES e : τ̂ & φ
            ─────────────────────────────                           if ζ₁, ···, ζ_n do not occur free in Γ̂ and φ
            Γ̂ ⊢_ES e : ∀(ζ₁, ···, ζ_n). τ̂ & φ

  [ins]     Γ̂ ⊢_ES e : ∀(ζ₁, ···, ζ_n). τ̂ & φ
            ─────────────────────────────────                       if θ has dom(θ) ⊆ {ζ₁, ···, ζ_n}
            Γ̂ ⊢_ES e : (θ τ̂) & φ
  ```
- Side conditions (`p. 329`):
  - *Syntactic effect subtraction `φ \ {s}`*: `{s} \ {s} = ∅`, `{s'} \ {s} = {s'}` if `s' ≠ s`,
    `(φ ∪ φ') \ {s} = (φ \ {s}) ∪ (φ' \ {s})`, `∅ \ {s} = ∅`, and **`β \ {s} = β`**.
  - *Subtyping `τ̂ ≤ τ̂'`*: `τ̂ ≤ τ̂` and `(τ̂'₁ ≤ τ̂₁ ∧ τ̂₂ ≤ τ̂'₂ ∧ φ ⊆ φ') ⇒ (τ̂₁ →^φ τ̂₂) ≤ (τ̂'₁ →^{φ'} τ̂'₂)`
    (on type variables `α`, only reflexivity `α ≤ α` applies).
  - `[gen]` is typically used just before `[let]` and **must** forbid quantifying variables free in *either*
    `Γ̂` *or* `φ`; `[ins]` is typically used immediately after `[var]`.
- Citation: [PPA Table 5.10, p. 328] (book p. 328; PDF p. 345); [PPA §5.4.2, p. 329] (book p. 329; PDF p. 346)

### Example 5.30 — Effect polymorphism vs monomorphic subtyping on `let f = fn g => fn x => g x`
- Statement: Analysing (evaluating to `1 + 1 = 2`):
  ```text
  let f = fn g => fn x => g x
  in f (fn y => if y < 0 then raise neg else y) (3-2)
   + f (fn z => if z > 0 then raise pos else 0-z) (2-3)
  ```
  - *With polymorphism*: `f` gets `∀'a, 'b, '0. ('a →^{'0} 'b) →^∅ ('a →^{'0} 'b)` (finding F-U5b-04). The two
    functional arguments have `int →^{neg} int & ∅` and `int →^{pos} int & ∅`; instantiating `['a ↦ int;
    'b ↦ int; '0 ↦ {neg}]` and `['a ↦ int; 'b ↦ int; '0 ↦ {pos}]` types the summands separately as `int & {neg}`
    and `int & {pos}`, yielding overall `int & {neg, pos}`.
  - *Without polymorphism*: subeffecting + subtyping must assign `f` the coarser monomorphic type
    `(int →^{neg, pos} int) →^∅ (int →^{neg, pos} int)`, smearing `{neg, pos}` into *both* individual calls
    (even though the top-level union `int & {neg, pos}` happens to coincide here). `■`
- Citation: [PPA Example 5.30, p. 329] (book p. 329; PDF p. 346); [PPA Example 5.30, p. 330] (book p. 330; PDF p. 347)

### [U5b:5.4.2-c] `Remark.` — `σ̂` conclusions (`Exercise 5.15`) and `β \ {s} = β` soundness (unnumbered remark)
- Statement:
  1. Although judgements have the general form `Γ̂ ⊢_ES e : σ̂ & φ`, most rules in `Table 5.10` restrict
     conclusions to `Γ̂ ⊢_ES e : τ̂ & φ`; generalising `[if]`, `[let]`, `[raise]`, `[handle]`, and `[sub]` to
     `σ̂` yields a more liberal system (`Exercise 5.15`).
  2. Defining `β \ {s} = β` in `[handle]` is conservative when `β` is later instantiated to `{s}`, yet
     semantically sound because `β \ {s} ⊆ β` holds for all ground instantiations (matching `[sub]`). A less
     approximate system extends effect syntax with `φ ::= ··· | φ \ {s}` and extends `UCAI` to axiomatise set
     difference. `■`
- Citation: [PPA §5.4.2, p. 330] (book p. 330; PDF p. 347)

### Findings (5.4.2)
- F-U5b-04 (`[AVar Zero-Index & Editorial Typos]`): `Example 5.30` (`p. 329`) writes annotation variable `'0`
  in `∀'a, 'b, '0`, whereas §5.3.2 ([PPA §5.3.2, p. 306] (book p. 306; PDF p. 323)) indexed `AVar` from `'1`
  upward; p. 327 prints `"a (possible empty) list"` (`"possible"` for `"possibly"`), and p. 330 `Remark.`
  prints plural `"Exception Analyses were"`. [PPA §5.4.2, p. 327] (book p. 327; PDF p. 344);
  [PPA Example 5.30, p. 329] (book p. 329; PDF p. 346); [PPA §5.4.2, p. 330] (book p. 330; PDF p. 347)

### Projections (5.4.2)
- cs_theory: `Table 5.10` demonstrates why **effect polymorphism** (`∀'1. ('a →^{'1} 'b) →^∅ ('a →^{'1} 'b)`)
  strictly dominates monomorphic subtyping on higher-order combinators (`Example 5.30`) and anticipates
  `[external: row-polymorphic algebraic effect handlers (Plotkin–Pretnar / Koka / OCaml 5)]`, where `handle s`
  removes label `s` from an effect row while polymorphic row tail `β` passes unhandled effects through.
- swe_architecture: `Example 5.30` explains the notorious ergonomics failure of
  `[external: Java monomorphic checked exceptions]` on higher-order APIs (`Stream.map(Function<T,R>)` cannot
  declare caller-dependent `throws E` without effect variables `'1`, forcing unchecked tunneling), whereas
  Hindley/Milner effect schemes infer precise per-call-site exception sets with zero signature boilerplate.
- practical_debugging: Never simplify `β \ {s}` to `∅` (or drop `s` from constraints on `β` before instantiation)
  in a symbolic exception analyser: if a wrapper `(fn g => handle s as 0 in g 1)` has body effect `β \ {s}` and
  is later called with `g` raising `{s, s'}`, premature simplification loses `s'` (`β \ {s} = β` is mandatory
  unless explicit symbolic difference terms `φ \ {s}` are retained through `[ins]`) `[derived]`.
- cyber: Static uncaught-exception sets `φ` directly audit two high-impact vulnerability classes:
  (1) **Denial-of-Service / crash surfaces (`[external: CWE-755]` Improper Handling of Exceptional Conditions)**
  when parser/`[external: RPC]` entrypoints satisfy `⊢_ES entry : τ̂ & φ` with `φ ≠ ∅`, and (2) **cleanup /
  privilege-drop bypass (`[external: CWE-404]` Improper Resource Shutdown)** when an exception `s ∈ φ₁` in
  `let _ = work() in release_lock()` short-circuits before `release_lock()` without an enclosing `handle`.

---

## 5.4.3 Region Inference

Context: Section 5.4.3 formulates `[175, 176]` (`[external: Tofte–Talpin]`) stack-based *Region Inference* (`Figure 5.1`), translating source
`FUN` expressions `e` into region-annotated *extended expressions* `ee ∈ EExp` (`Table 5.11` Natural Semantics;
`Tables 5.12–5.13` type-and-effect translation `Γ̂ ⊢_RI e ↝ ee : τ̂ @ r & φ`) via restricted polymorphic
recursion (`∀β⃗, [ϱ⃗]`) and lexical effect masking (`Observe`)
[PPA §5.4.3, p. 330] (book p. 330; PDF p. 347); [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355).

### [U5b:5.4.3-a] Stack-of-regions memory model and extended expression syntax `EExp`
- Statement: Replaces heap allocation + garbage collection for `FUN` with a stack-based regime in which memory
  is a stack of dynamic regions `(r1, r2, r3, ···)` (`Figure 5.1`), each an indexed array of boxed values.
  Introduces *region names*, *region variables*, *regions*, and *extended expressions* `ee ∈ EExp`:
  ```text
  rn ∈ RName  ::= r1 | r2 | r3 | ···          region names
  ϱ  ∈ RVar   ::= ''1 | ''2 | ''3 | ···       region variables
  r  ∈ Reg_RI ::= ϱ | rn                      regions

  ee ∈ EExp   ::= c at r | x | fn_π x => ee₀ at r | fun_π f [ϱ⃗] x => ee₀ at r | ee₁ ee₂
                | if ee₀ then ee₁ else ee₂ | let x = ee₁ in ee₂ | ee₁ op ee₂ at r
                | ee[r⃗] at r | letregion ϱ⃗ in ee
  ```
  where `ϱ⃗` (`ϱ₁, ···, ϱ_k`) and `r⃗` (`r₁, ···, r_k`) are possibly empty sequences:
  - Every construct directly producing a runtime value (`c`, `fn_π`, `fun_π`, `op`, `ee[r⃗]`) carries an
    explicit placement `"at r"`.
  - `fun_π f [ϱ⃗] x => ee₀ at r` parameterises recursive `f` over formal region variables `ϱ⃗` so distinct
    recursive invocations can place local data into distinct regions.
  - `ee[r⃗] at r` instantiates a region-polymorphic closure `ee` with actual regions `r⃗` and places the
    resulting specialised closure copy into region `r`.
  - `letregion ϱ⃗ in ee` allocates fresh dynamic regions for `ϱ⃗`, evaluates `ee`, and deallocates `ϱ⃗` on exit.
- Citation: [PPA §5.4.3, p. 330] (book p. 330; PDF p. 347); [PPA §5.4.3, p. 331] (book p. 331; PDF p. 348); [PPA §5.4.3, p. 332] (book p. 332; PDF p. 349)

### Figure 5.1 — The memory model for the stack-based implementation of FUN
- Statement: Depicts dynamic memory as a horizontal stack of vertical extensible arrays `r1`, `r2`, `r3`, `...`:
  ```text
  (r1, o₁) ┌────┐                  (r3, o₃) ┌────┐
     ⋮     │    │   (r2, o₂) ┌────┐    ⋮    │    │
           │    │      ⋮     │    │         │    │
  (r1, 1)  └────┘   (r2, 1)  └────┘ (r3, 1) └────┘   ...
             r1                r2             r3     ...
  ```
  Each active region `ri` holds boxed cells indexed `(ri, 1)` through `(ri, o_i)` of arbitrary current height
  `o_i`, pushed on `letregion` entry and popped as a whole on `letregion` exit.
- Citation: [PPA Figure 5.1, p. 331] (book p. 331; PDF p. 348)

### Example 5.31 — Extended-expression translation of `(let x = 7 in fn_Y y => y+x) 9`
- Statement: Source expression `e = (let x = 7 in fn_Y y => y+x) 9` translates to `ee`:
  ```text
  letregion ϱ₁, ϱ₃, ϱ₄
  in (let x = (7 at ϱ₁)
      in (fn_Y y => (y+x) at ϱ₂) at ϱ₃) (9 at ϱ₄)
  ```
  `7` is placed in `ϱ₁`, result `x+y` (`16`) in `ϱ₂`, closure `Y` in `ϱ₃`, and `9` in `ϱ₄`; on exit, internal
  regions `ϱ₁, ϱ₃, ϱ₄` are deallocated while `ϱ₂` retains `16` (at run time metavariables `ϱ₁, ϱ₃, ϱ₄` are
  concrete `''1, ''2, ''3` and free `ϱ₂` is replaced by a region name such as `r1`). `■`
- Citation: [PPA Example 5.31, p. 332] (book p. 332; PDF p. 349)

### [U5b:5.4.3-b] Semantic domains for `EExp` and region deallocation `ς ⧹⧹ rn⃗`
- Statement: Operational judgements `ρ ⊢ ⟨ee, ς⟩ → ⟨v, ς'⟩` (assuming closed region variables at run time so
  static `r`s have become `rn`s) use domains (`Var_⋆` = finite set of variables in `ee_⋆`):
  ```text
  ρ ∈ Env    = Var_⋆ → EVal
  v ∈ EVal   = RName × Offset                      expressible values (all ordinary values boxed!)
  o ∈ Offset = N
  ς ∈ Store  = RName →_fin (Offset →_fin SVal)     written ς(r, o) for ς(r)(o)
  w ∈ SVal   ::= c | ⟨x, ee, ρ⟩ | ⟨ϱ⃗, x, ee, ρ⟩    constants, closures, region-polymorphic closures
  ```
  Region deallocation `ς ⧹⧹ rn⃗` (`p. 335`): `dom(ς ⧹⧹ rn⃗) = dom(ς) \ {rn⃗}` and
  `∀(rn, o) ∈ dom(ς ⧹⧹ rn⃗) : ς(rn, o) = (ς ⧹⧹ rn⃗)(rn, o)`.
- Citation: [PPA §5.4.3, p. 332] (book p. 332; PDF p. 349); [PPA §5.4.3, p. 333] (book p. 333; PDF p. 350); [PPA §5.4.3, p. 335] (book p. 335; PDF p. 352)

### Table 5.11 — Natural Semantics for extended expressions
- Statement: Environment-and-store evaluation rules `ρ ⊢ ⟨ee, ς⟩ → ⟨v, ς'⟩`:
  ```text
  [con]     ρ ⊢ ⟨c at rn, ς⟩ → ⟨(rn, o), ς[(rn, o) ↦ c]⟩                  if o ∉ dom(ς(rn))

  [var]     ρ ⊢ ⟨x, ς⟩ → ⟨ρ(x), ς⟩

  [fn]      ρ ⊢ ⟨(fn_π x => ee₀) at rn, ς⟩ →
                ⟨(rn, o), ς[(rn, o) ↦ ⟨x, ee₀, ρ⟩]⟩                       if o ∉ dom(ς(rn))

  [fun]     ρ ⊢ ⟨(fun_π f[ϱ⃗] x => ee₀) at rn, ς⟩ →
                ⟨(rn, o), ς[(rn, o) ↦ ⟨ϱ⃗, x, ee₀, ρ[f ↦ (rn, o)]⟩]⟩       if o ∉ dom(ς(rn))

  [app]     ρ ⊢ ⟨ee₁, ς₁⟩ → ⟨(rn₁, o₁), ς₂⟩    ρ ⊢ ⟨ee₂, ς₂⟩ → ⟨v₂, ς₃⟩
            ρ₀[x ↦ v₂] ⊢ ⟨ee₀, ς₃⟩ → ⟨v₀, ς₄⟩
            ──────────────────────────────────────────────────────────────
                           ρ ⊢ ⟨ee₁ ee₂, ς₁⟩ → ⟨v₀, ς₄⟩
            if ς₃(rn₁, o₁) = ⟨x, ee₀, ρ₀⟩

  [if₁]     ρ ⊢ ⟨ee₀, ς₁⟩ → ⟨(rn, o), ς₂⟩    ρ ⊢ ⟨ee₁, ς₂⟩ → ⟨v₁, ς₃⟩
            ──────────────────────────────────────────────────────────     if ς₂(rn, o) = true
                    ρ ⊢ ⟨if ee₀ then ee₁ else ee₂, ς₁⟩ → ⟨v₁, ς₃⟩

  [if₂]     ρ ⊢ ⟨ee₀, ς₁⟩ → ⟨(rn, o), ς₂⟩    ρ ⊢ ⟨ee₂, ς₂⟩ → ⟨v₂, ς₃⟩
            ──────────────────────────────────────────────────────────     if ς₂(rn, o) = false
                    ρ ⊢ ⟨if ee₀ then ee₁ else ee₂, ς₁⟩ → ⟨v₂, ς₃⟩

  [let]     ρ ⊢ ⟨ee₁, ς₁⟩ → ⟨v₁, ς₂⟩    ρ[x ↦ v₁] ⊢ ⟨ee₂, ς₂⟩ → ⟨v₂, ς₃⟩
            ─────────────────────────────────────────────────────────────
                       ρ ⊢ ⟨let x = ee₁ in ee₂, ς₁⟩ → ⟨v₂, ς₃⟩

  [op]      ρ ⊢ ⟨ee₁, ς₁⟩ → ⟨(rn₁, o₁), ς₂⟩    ρ ⊢ ⟨ee₂, ς₂⟩ → ⟨(rn₂, o₂), ς₃⟩
            ────────────────────────────────────────────────────────────────────
                  ρ ⊢ ⟨(ee₁ op ee₂) at rn, ς₁⟩ → ⟨(rn, o), ς₃[(rn, o) ↦ w]⟩
            if ς₃(rn₁, o₁) op ς₃(rn₂, o₂) = w and o ∉ dom(ς₃(rn))

  [place]   ρ ⊢ ⟨ee, ς₁⟩ → ⟨(rn', o'), ς₂⟩
            ────────────────────────────────────────────────────────────────────
            ρ ⊢ ⟨ee[rn⃗] at rn, ς₁⟩ → ⟨(rn, o), ς₂[(rn, o) ↦ ⟨x, ee₀[ϱ⃗ ↦ rn⃗], ρ₀⟩]⟩
            if o ∉ dom(ς₂(rn)) and ς₂(rn', o') = ⟨ϱ⃗, x, ee₀, ρ₀⟩

  [region]  ρ ⊢ ⟨ee[ϱ⃗ ↦ rn⃗], ς₁[rn⃗ ↦ []⃗]⟩ → ⟨v, ς₂⟩
            ────────────────────────────────────────     if {rn⃗} ∩ dom(ς) = ∅
            ρ ⊢ ⟨letregion ϱ⃗ in ee, ς₁⟩ → ⟨v, ς₂ ⧹⧹ rn⃗⟩
  ```
- Side conditions:
  - `[app]` applies only to ordinary closures `⟨x, ee₀, ρ₀⟩`; a region-polymorphic closure `⟨ϱ⃗, x, ee₀, ρ₀⟩`
    must first be specialised into an ordinary closure by `[place]` (`ee[rn⃗] at rn`).
  - Accessing or allocating in a deallocated region `rn ∉ dom(ς)` fails the definedness of `ς(rn)` / `ς(rn, o)`
    and gets stuck; note printed side-condition typo `dom(ς)` for `dom(ς₁)` in `[region]` (finding F-U5b-05).
- Citation: [PPA Table 5.11, p. 334] (book p. 334; PDF p. 351); [PPA §5.4.3, p. 335] (book p. 335; PDF p. 352)

### [U5b:5.4.3-c] Extended types `τ̂ @ r`, `Ann_RI`, `Type_RI` (`β.φ`), and compound vs ordinary `Scheme_RI`
- Statement: An *extended type* is a pair `τ̂ @ r` of an annotated type and the region where its boxed value
  resides:
  ```text
  φ ∈ Ann_RI    ::= {put r} | {get r} | φ₁ ∪ φ₂ | ∅ | β
  τ̂ ∈ Type_RI   ::= int | bool | (τ̂₁ @ r₁) →^{β.φ} (τ̂₂ @ r₂) | α
  σ̂ ∈ Scheme_RI ::= ∀(α₁, ···, α_n), (β₁, ···, β_m), [ϱ₁, ···, ϱ_k]. τ̂    (compound type scheme)
                  | ∀(α₁, ···, α_n), (β₁, ···, β_m). τ̂                    (ordinary type scheme)
  ```
  - *Compound vs ordinary distinction*: `∀(), (). τ̂` is abbreviated `τ̂`, whereas `∀(), (), []. τ̂` **must** be
    written `∀[]. τ̂` so compound schemes (for recursive functions, requiring `[ins₂]` / `[place]`) are always
    syntactically distinguishable from ordinary schemes (`[ins₁]`).
  - *Dot notation `β.φ`* (`pp. 335–336`): related to §5.3 *simple types*; declaratively `β.φ` denotes `β ∪ φ`,
    while the inference algorithm views `β.φ` as imposing constraint `β ⊇ β ∪ φ`.
- Citation: [PPA §5.4.3, p. 335] (book p. 335; PDF p. 352); [PPA §5.4.3, p. 336] (book p. 336; PDF p. 353)

### Example 5.32 — Extended types for subexpressions of Example 5.31
- Statement: In `Example 5.31`'s `ee`, `7 at ϱ₁` has `int @ ϱ₁`, `(fn_Y y => (y+x) at ϱ₂) at ϱ₃` has
  `((int @ ϱ₄) →^{β.φ} (int @ ϱ₂)) @ ϱ₃` where `φ = {get ϱ₄, get ϱ₁, put ϱ₂}`, and the overall expression has
  extended type `int @ ϱ₂` (finding F-U5b-06). `■`
- Citation: [PPA Example 5.32, p. 336] (book p. 336; PDF p. 353)

### [U5b:5.4.3-d] Translation judgements `Γ̂ ⊢_RI e ↝ ee : τ̂ @ r & φ`, polymorphic recursion, and `Observe`
- Statement:
  - *Type-directed translation* (touching upon §1.8, [PPA §1.8, p. 27] (book p. 27; PDF p. 47)): judgements
    `Γ̂ ⊢_RI e ↝ ee : τ̂ @ r & φ` (with `Γ̂` mapping variables to *extended type schemes* `σ̂ @ r`) simultaneously
    infer regions/effects and translate `e ∈ Exp` to `ee ∈ EExp`.
  - *Restricted polymorphic recursion in `[fun]`* (`p. 336`): `[fun]` analyses recursive `f` under compound
    scheme `(∀β⃗, [ϱ⃗]. τ̂) @ r` — polymorphic over *effects and regions* (`β⃗, ϱ⃗`) while **excluding type
    variables `α⃗`** because full type-polymorphic recursion is undecidable (`α⃗` are generalised only outside
    recursion via `[gen₂]`).
  - *Effect-masking function `Observe`* (`pp. 338–339`, split across the page break between p. 338 and p. 339):
    ```text
    Observe(Γ̂, τ̂, r')({put r}) = {put r}    if r occurs in Γ̂, τ̂, or r';   ∅ otherwise
    Observe(Γ̂, τ̂, r')({get r}) = {get r}    if r occurs in Γ̂, τ̂, or r';   ∅ otherwise
    Observe(Γ̂, τ̂, r')(φ₁ ∪ φ₂) = Observe(Γ̂, τ̂, r')(φ₁) ∪ Observe(Γ̂, τ̂, r')(φ₂)
    Observe(Γ̂, τ̂, r')(∅)       = ∅
    Observe(Γ̂, τ̂, r')(β)       = β          if β occurs in Γ̂, τ̂, or r';   ∅ otherwise
    ```
- Citation: [PPA §5.4.3, p. 336] (book p. 336; PDF p. 353); [PPA §5.4.3, p. 338] (book p. 338; PDF p. 355); [PPA §5.4.3, p. 339] (book p. 339; PDF p. 356)

### Table 5.12 — Region Inference Analysis and Translation (part 1)
- Statement: Core translation and inference rules (`[fn]` premise, `[app]` conclusion, `[let]` conclusion, and
  `[op]` premises erased in PDF OCR, verified on rendered p. 337):
  ```text
  [con]  Γ̂ ⊢_RI c ↝ c at r : (τ_c @ r) & {put r}

  [var]  Γ̂ ⊢_RI x ↝ x : σ̂ & ∅                                            if Γ̂(x) = σ̂

  [fn]   Γ̂[x ↦ τ̂_x @ r_x] ⊢_RI e₀ ↝ ee₀ : (τ̂₀ @ r₀) & φ₀
         ─────────────────────────────────────────────────────────────────────────────
         Γ̂ ⊢_RI fn_π x => e₀ ↝ (fn_π x => ee₀) at r : ((τ̂_x @ r_x →^{β.φ₀} τ̂₀ @ r₀) @ r) & {put r}

  [fun]  Γ̂[f ↦ (∀β⃗, [ϱ⃗]. τ̂) @ r] ⊢_RI fn_π x => e₀ ↝ (fn_π x => ee₀) at r : (τ̂ @ r) & φ
         ──────────────────────────────────────────────────────────────────────────────────
         Γ̂ ⊢_RI fun_π f x => e₀ ↝ (fun_π f [ϱ⃗] x => ee₀) at r : ((∀β⃗, [ϱ⃗]. τ̂) @ r) & φ
         if β⃗ and ϱ⃗ do not occur free in Γ̂ and φ

  [app]  Γ̂ ⊢_RI e₁ ↝ ee₁ : ((τ̂₂ @ r₂ →^{β₀.φ₀} τ̂₀ @ r₀) @ r₁) & φ₁
         Γ̂ ⊢_RI e₂ ↝ ee₂ : (τ̂₂ @ r₂) & φ₂
         ─────────────────────────────────────────────────────────────────────────
         Γ̂ ⊢_RI e₁ e₂ ↝ ee₁ ee₂ : (τ̂₀ @ r₀) & φ₁ ∪ φ₂ ∪ φ₀ ∪ β₀ ∪ {get r₁}

  [if]   Γ̂ ⊢_RI e₀ ↝ ee₀ : (bool @ r₀) & φ₀
         Γ̂ ⊢_RI e₁ ↝ ee₁ : (τ̂ @ r) & φ₁    Γ̂ ⊢_RI e₂ ↝ ee₂ : (τ̂ @ r) & φ₂
         ──────────────────────────────────────────────────────────────────────────────
         Γ̂ ⊢_RI if e₀ then e₁ else e₂ ↝ if ee₀ then ee₁ else ee₂ : (τ̂ @ r) & φ₀ ∪ φ₁ ∪ φ₂ ∪ {get r₀}

  [let]  Γ̂ ⊢_RI e₁ ↝ ee₁ : (σ̂₁ @ r₁) & φ₁    Γ̂[x ↦ σ̂₁ @ r₁] ⊢_RI e₂ ↝ ee₂ : (τ̂₂ @ r₂) & φ₂
         ────────────────────────────────────────────────────────────────────────────────────
                     Γ̂ ⊢_RI let x = e₁ in e₂ ↝ let x = ee₁ in ee₂ : (τ̂₂ @ r₂) & φ₁ ∪ φ₂

  [op]   Γ̂ ⊢_RI e₁ ↝ ee₁ : (τ_op^1 @ r₁) & φ₁    Γ̂ ⊢_RI e₂ ↝ ee₂ : (τ_op^2 @ r₂) & φ₂
         ──────────────────────────────────────────────────────────────────────────────────
         Γ̂ ⊢_RI e₁ op e₂ ↝ (ee₁ op ee₂) at r : (τ_op @ r) & φ₁ ∪ φ₂ ∪ {get r₁, get r₂, put r}
  ```
- Citation: [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354)

### Table 5.13 — Region Inference Analysis and Translation (part 2)
- Statement: Subtyping, generalisation, instantiation, and lexical region encapsulation rules (rule names
  `[gen₁]`, `[gen₂]`, `[ins₁]`, `[ins₂]` erased in PDF OCR, verified on rendered p. 338):
  ```text
  [sub]     Γ̂ ⊢_RI e ↝ ee : (τ̂ @ r) & φ
            ─────────────────────────────                              if τ̂ ≤ τ̂' and φ ⊆ φ'
            Γ̂ ⊢_RI e ↝ ee : (τ̂' @ r) & φ'

  [gen₁]    Γ̂ ⊢_RI e ↝ ee : (τ̂ @ r) & φ
            ─────────────────────────────────                          if α⃗ do not occur free in Γ̂ and φ
            Γ̂ ⊢_RI e ↝ ee : ((∀α⃗. τ̂) @ r) & φ

  [gen₂]    Γ̂ ⊢_RI e ↝ ee : ((∀β⃗, [ϱ⃗]. τ̂) @ r) & φ
            ─────────────────────────────────────────                  if α⃗ do not occur free in Γ̂ and φ
            Γ̂ ⊢_RI e ↝ ee : ((∀α⃗, β⃗, [ϱ⃗]. τ̂) @ r) & φ

  [ins₁]    Γ̂ ⊢_RI e ↝ ee : ((∀α⃗, β⃗. τ̂) @ r) & φ
            ─────────────────────────────────────                      if θ has dom(θ) ⊆ {α⃗, β⃗}
            Γ̂ ⊢_RI e ↝ ee : ((θ τ̂) @ r) & φ

  [ins₂]    Γ̂ ⊢_RI e ↝ ee : ((∀α⃗, β⃗, [ϱ⃗]. τ̂) @ r) & φ
            ─────────────────────────────────────────────────────────  if θ has dom(θ) ⊆ {α⃗, β⃗, ϱ⃗}
            Γ̂ ⊢_RI e ↝ ee[θ ϱ⃗] at r' : ((θ τ̂) @ r') & φ ∪ {get r, put r'}

  [region]  Γ̂ ⊢_RI e ↝ ee : (τ̂ @ r) & φ
            ─────────────────────────────────────────────
            Γ̂ ⊢_RI e ↝ letregion ϱ⃗ in ee : (τ̂ @ r) & φ'
            if φ' = Observe(Γ̂, τ̂, r)(φ) and ϱ⃗ occurs in φ but not in φ'
  ```
- Side conditions (`pp. 337–338`):
  - `[gen₁]` and `[gen₂]` generalise only type variables `α⃗` (though p. 337 notes both could also generalise
    additional region and effect variables, keeping type inference separate from region/effect inference).
  - `[ins₁]` (ordinary schemes) is syntactically invisible in `ee`, whereas `[ins₂]` (compound schemes) inserts
    `ee[θ ϱ⃗] at r'` and adds `{get r, put r'}` matching `[place]` in Table 5.11.
- Citation: [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355)

### Example 5.33 — Root region-inference derivation for Example 5.31
- Statement: For `e = (let x = 7 in fn_Y y => y+x) 9` and `ee` from Example 5.31, `Tables 5.12–5.13` derive
  `[] ⊢_RI e ↝ ee : (int @ ϱ₂) & {put ϱ₂}`, with `Observe([], int, ϱ₂)` masking `ϱ₁, ϱ₃, ϱ₄` and arrow effect
  variable `β`. `■`
- Citation: [PPA Example 5.33, p. 339] (book p. 339; PDF p. 356)

### Findings (5.4.3)
- F-U5b-05 (`[Source Erratum — Missing Store Subscript in Table 5.11 [region]]`): In Table 5.11 (`p. 334`),
  `[region]` has input store `ς₁` in `ρ ⊢ ⟨letregion ϱ⃗ in ee, ς₁⟩ → ⟨v, ς₂ ⧹⧹ rn⃗⟩`, yet prints unsubscripted
  `dom(ς)` instead of `dom(ς₁)` in `if {rn⃗} ∩ dom(ς) = ∅` (and leaves pairwise distinctness of fresh `rn⃗` in
  `ς₁[rn⃗ ↦ []⃗]` implicit). [PPA Table 5.11, p. 334] (book p. 334; PDF p. 351)
- F-U5b-06 (`[Omitted Type_RI Subtyping, Extended-Scheme Reuse & Split Observe Clauses]`): Table 5.13 `[sub]`
  (`p. 338`) invokes `τ̂ ≤ τ̂'` on `Type_RI`, but §5.4.3 never states the subtyping rule for
  `(τ̂₁ @ r₁) →^{β.φ} (τ̂₂ @ r₂)` (where `r₁ = r'₁` and `r₂ = r'₂` must be **invariant** since `Reg_RI` has no
  subset order, with `τ̂'₁ ≤ τ̂₁`, `τ̂₂ ≤ τ̂'₂`, and `β ∪ φ ⊆ β' ∪ φ'` `[derived]`); Table 5.12 `[var]` (`p. 337`)
  writes `σ̂` where `Γ̂(x)` holds an *extended* scheme `σ̂ @ r` (`p. 336`), while Example 5.32 (`p. 336`) calls
  `int @ ϱ₁` and `((int @ ϱ₄) →^{β.φ} (int @ ϱ₂)) @ ϱ₃` `"annotated types"` rather than extended types; and
  `Observe(Γ̂, τ̂, r')` splits its five clauses across the p. 338/p. 339 page break (`{put r}`, `{get r}` on
  p. 338; `φ₁ ∪ φ₂`, `∅`, `β` on p. 339), leaving *free* occurrence modulo `∀`-binders in `Γ̂` informal and
  listing `or r'` in the `β` clause even though `r' ∈ Reg_RI` cannot contain `β ∈ AVar`.
  [PPA §5.4.3, p. 335] (book p. 335; PDF p. 352); [PPA Example 5.32, p. 336] (book p. 336; PDF p. 353);
  [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354); [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355);
  [PPA §5.4.3, p. 339] (book p. 339; PDF p. 356)
- F-U5b-07 (`[Section 5.4.3 Editorial Typos]`): p. 332 prints `"a possible empty sequence"` and `"The
  transitions takes"`; p. 333 prints `"explicityly"`; p. 338 prints `"ordinary types schemes"`.
  [PPA §5.4.3, p. 332] (book p. 332; PDF p. 349); [PPA §5.4.3, p. 333] (book p. 333; PDF p. 350);
  [PPA §5.4.3, p. 338] (book p. 338; PDF p. 355)

### Projections (5.4.3)
- cs_theory:
  1. **Decidability boundary (`[fun]` excluding `α⃗`)**: Full `[external: Mycroft polymorphic recursion]` over
     *types* (`∀α⃗`) is equivalent to `[external: semi-unification]` and **undecidable**
     `[external: Kfoury–Tiuryn–Urzyczyn 1993]`; fixing Hindley/Milner underlying types first and restricting
     polymorphic recursion to finite-carrier effects and regions (`∀β⃗, [ϱ⃗]`) keeps Stage 1 decidable while
     `Algorithm R` approximates fixed points soundly (though syntactically incompletely).
  2. **Lexical encapsulation (`§5.4.3` Region Inference vs `§2.6` Shape Analysis)**: `Observe` formalises
     observational state encapsulation (precursor to
     `[external: Launchbury–Peyton Jones Haskell runST :: (∀s. ST s a) -> a]`). Contrasting with §2.6 Shape
     Analysis, §2.6 is *flow-sensitive* over mutable pointer graphs `SG = (S, H, is)` with singleton
     materialisation and in-place `[external: strong updates]` at exponential cost, whereas §5.4.3 is
     *type-directed and lexically scoped*, sacrificing per-cell `[external: strong updates]` to obtain modular
     region-polymorphic summaries and `O(1)` bulk stack deallocation.
- swe_architecture: Comparing `[175, 176]` (`[external: Tofte–Talpin]`) `letregion` (`[external: MLKit]`) with `[external: Cyclone arenas]`
  and `[external: Rust lifetimes / borrowck]`: both statically attach region/`[external: lifetime]` parameters
  (`ϱ` vs `'a`) and forbid escaping references (`Observe` hiding `ϱ` from `Γ̂, τ̂, r` vs outlives constraints
  `'out : 'in`), **except** §5.4.3 allows unrestricted *aliasing* inside a region `r` and bulk-frees `r` only
  when *all* inhabitants of `r` become unreachable (`ς₂ ⧹⧹ rn⃗`), whereas `[external: Rust NLL / Polonius]`
  pairs `[external: lifetimes]` with `[external: affine ownership]` and alias-XOR-mutability (`&T` vs `&mut T`)
  to enable unboxed values, deterministic single-value drop, and safe in-place mutation.
- practical_debugging:
  - *Dangling-region crash (`rn ∉ dom(ς)` in Table 5.11)*: verify (1) `[app]` emits `{get r₁}` for the boxed
    closure container `r₁` and `[if]`/`[op]` emit `{get r₀}`/`{get r₁, get r₂}` (`Table 5.12`), (2) `Observe`
    scans regions nested inside `τ̂`'s latent arrow annotations `β.φ₀`, and (3) `[region]` checks that `ϱ⃗`
    actually **occurs in `φ`** as well as `ϱ⃗ ∉ φ'` (otherwise `x : int @ ϱ₁ & ∅` has `φ = φ' = ∅` and would
    unsoundly wrap `letregion ϱ₁ in x`!) `[derived]`.
  - *Recursive region leak (unbounded `[external: arena]` growth)*: if a tail-recursive or accumulator function
    shares input and output region `r_in = r_out`, `Observe` sees `r_out` escaping in the result type and cannot
    place `letregion` inside the loop; refactor to copy/ping-pong outputs into a caller-supplied destination
    region `[external: Tofte–Birkedal destination-passing style]`.
- cyber: `Observe(Γ̂, τ̂, r)(φ)` acts as a static soundness firewall eliminating
  `[external: arena/pool Use-After-Free (CWE-416)]` (`[external: obstack, ngx_pool_t, apr_pool_t, kernel slab caches]`):
  bulk exit `ς₂ ⧹⧹ rn⃗` is permitted iff no live pointer in `Γ̂`, escaping closure in `τ̂`, or return handle `r`
  can ever dereference `rn⃗`, while missing region-polymorphic `[ins₂]` instantiation on server request loops
  causes unbounded `[external: arena]` retention **Denial-of-Service (`[external: CWE-400]`)**.

---

## 5.5 Behaviours and 5.5.1 Communication Analysis

Context: Section 5.5 moves beyond unordered effect sets to causal *behaviours* recording temporal action
ordering (`;`, `+`, `rec β.φ`, `spawn φ`, `r!τ̂`, `r?τ̂`) for a Concurrent ML fragment in §5.5.1
(*Communication Analysis*), with small-step evaluation-context SOS (`Tables 5.14–5.15`), polymorphic typing
(`Tables 5.16–5.17`), and the 22-rule behaviour preorder `φ₁ ⊑ φ₂` (`Table 5.18`)
[PPA §5.5, p. 339] (book p. 339; PDF p. 356); [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365).

### [U5b:5.5-a] Temporal behaviours motivation and Concurrent ML syntax (`§5.5.1`)
- Statement: Section 5.4's set effects ignore temporal order (for example checking that a variable is assigned
  before being read). Section 5.5 introduces *behaviours* capturing causality in a Concurrent ML fragment
  (`§5.5.1`) extending `FUN` with process creation, channel creation, synchronous communication, sequencing, and
  dynamic channel identifiers `ch ∈ Chan`:
  ```text
  e  ::= ··· | channel_π | spawn e₀ | send e₁ on e₂ | receive e₀ | e₁; e₂ | ch
  ch ∈ Chan ::= chan1 | chan2 | ···
  ```
  Constants `c ∈ Const` include `()` of type `unit` (returned by `spawn` and `send`).
- Citation: [PPA §5.5, p. 339] (book p. 339; PDF p. 356); [PPA §5.5.1, p. 339] (book p. 339; PDF p. 356); [PPA §5.5.1, p. 340] (book p. 340; PDF p. 357)

### Figure 5.2 — The pipeline produced by `pipe [f₁, f₂] inp out`
- Statement: Depicts the linear concurrent stream-processing network wired by `pipe [f₁, f₂] inp out`:
  ```text
       inp      ┌────┐          ┌────┐          ┌────┐      out
      ─────────▶│ f₁ │─────────▶│ f₂ │─────────▶│ id │─────────▶
                └────┘          └────┘          └────┘
  ```
  Two internal `channel_C` channels connect stage `f₁` to `f₂` and `f₂` to the base-case identity process `id`.
- Citation: [PPA Figure 5.2, p. 340] (book p. 340; PDF p. 357)

### Example 5.34 — Concurrent stream pipeline `node` and `pipe`
- Statement: Assuming list operations `isnil e`, `hd e`, and `tl e`, defines `node` and recursive `pipe`:
  ```text
  let node = fn_F f => fn_I inp => fn_O out =>
               spawn ((fun_H h d => let v = receive inp
                                    in send (f v) on out;
                                       h d) ())
  in fun_P pipe fs => fn_I inp => fn_O out =>
       if isnil fs then node (fn_X x =>x) inp out
       else let ch = channel_C
            in (node (hd fs) inp ch; pipe (tl fs) ch out)
  ```
  On an empty function list `fs`, `pipe` spawns a single `node` applying identity `fn_X x =>x` (`id` in
  Figure 5.2). `■`
- Citation: [PPA Example 5.34, p. 340] (book p. 340; PDF p. 357)

### [U5b:5.5.1-a] Substitution values, single-hole evaluation contexts `E`, and concurrent pools `CP, PP`
- Statement:
  - *Values* (`p. 341`, substitution-based without environments or stores): `v ∈ Val ::= c | ch | fn_π x => e₀`.
  - *Evaluation contexts `E`* (`pp. 341–342`, one hole `[]` never inside a binder scope so `E[e]` avoids
    variable capture):
    ```text
    E ::= [] | E e | v E | let x = E in e
        | if E then e₁ else e₂ | E op e | v op E
        | send E on e | send v on E | receive E | E; e
    ```
    Contextual step: `e₁ ⇒ e₂` iff `∃E, e₁₀, e₂₀ : e₁ = E[e₁₀] ∧ e₁₀ → e₂₀ ∧ e₂ = E[e₂₀]` (for example `E op e`
    concisely replaces inference rules like `(e₁₀ → e₂₀) ⇒ (e₁₀ op e₂ → e₂₀ op e₂)` from Table 3.3,
    [PPA Table 3.3, p. 156] (book p. 156; PDF p. 174)).
  - *Concurrent configurations* (`p. 342`): process identifiers `p ∈ Proc ::= proc1 | proc2 | ···`, allocated
    channels `CP ∈ 𝒫_fin(Chan)`, process pool `PP ∈ Proc →_fin Exp` (closed `PP(p)`), with pool update `PP[p : e]`
    having `dom(PP') = dom(PP) ∪ {p}`, `PP'(p) = e`, and `PP'(q) = PP(q)` for `q ≠ p`.
- Citation: [PPA §5.5.1, p. 341] (book p. 341; PDF p. 358); [PPA §5.5.1, p. 342] (book p. 342; PDF p. 359)

### Table 5.14 — The sequential semantics
- Statement: One-step eager left-to-right sequential reductions `e₁ → e₂` (`v₁ op v₂ → v` erased in PDF OCR,
  restored from rendered p. 341):
  ```text
  (fn_π x => e) v → e[x ↦ v]
  let x = v in e → e[x ↦ v]
  v₁ op v₂ → v                                       if v₁ op v₂ = v
  fun_π f x => e → (fn_π x => e)[f ↦ (fun_π f x => e)]
  if true then e₁ else e₂ → e₁
  if false then e₁ else e₂ → e₂
  v; e → e
  ```
- Citation: [PPA Table 5.14, p. 341] (book p. 341; PDF p. 358)

### Table 5.15 — The concurrent semantics
- Statement: Small-step concurrent SOS `CP₁, PP₁ ⇒ CP₂, PP₂`:
  ```text
  [seq]    CP, PP[p : E[e₁]] ⇒ CP, PP[p : E[e₂]]                       if e₁ → e₂

  [chan]   CP, PP[p : E[channel_π]] ⇒ CP ∪ {ch}, PP[p : E[ch]]         if ch ∉ CP

  [spawn]  CP, PP[p : E[spawn e₀]] ⇒ CP, PP[p : E[()]][p₀ : e₀]        if p₀ ∉ dom(PP) ∪ {p}

  [comm]   CP, PP[p₁ : E₁[send v on ch]][p₂ : E₂[receive ch]]
             ⇒ CP, PP[p₁ : E₁[()]][p₂ : E₂[v]]                         if p₁ ≠ p₂
  ```
- Side conditions: `[comm]` enforces synchronous rendezvous between **distinct** processes `p₁ ≠ p₂`, replacing
  `send v on ch` with `()` and `receive ch` with `v`.
- Citation: [PPA Table 5.15, p. 343] (book p. 343; PDF p. 360)

### [U5b:5.5.1-b] Mutually recursive `Type_CA`, `Ann_CA` (behaviours), `Reg_CA`, and `Scheme_CA`
- Statement: Aim: determine for each expression what channels are allocated, what value types are sent and
  received over channels, what spawned processes do, and the causal ordering among actions:
  ```text
  τ̂ ∈ Type_CA   ::= α | bool | int | unit | τ̂₁ →^φ τ̂₂ | τ̂ chan r
  φ ∈ Ann_CA    ::= β | Λ | φ₁; φ₂ | φ₁ + φ₂ | rec β.φ
                  | τ̂ chan r | spawn φ | r!τ̂ | r?τ̂
  r ∈ Reg_CA    ::= {π} | ϱ | r₁ ∪ r₂ | ∅                              (modulo UCAI)
  σ̂ ∈ Scheme_CA ::= ∀(ζ₁, ···, ζ_n). τ̂                                 (ζ_i ∈ TVar ∪ AVar ∪ RVar)
  ```
  - `Λ` = silent/empty non-communicating action (analogous to `ε` in regular expressions or `τ` in process
    calculi); `φ₁; φ₂` = `φ₁` before `φ₂`; `φ₁ + φ₂` = internal/conditional choice; `rec β.φ` = recursive
    behaviour (regarded equal up to α-renaming of bound behaviour variables, p. 349); `τ̂ chan r` = channel
    allocation at a program point in `r`; `spawn φ` = process generation; `r!τ̂` / `r?τ̂` = CSP-style output /
    input of a `τ̂` entity over a `τ̂ chan r` channel.
  - Unlike §5.4.3 (`at r`), static regions `r ∈ Reg_CA` identify sets `{π₁, ···, π_n}` of channel creation
    points and never appear explicitly in source expressions.
- Citation: [PPA §5.5.1, p. 343] (book p. 343; PDF p. 360); [PPA §5.5.1, p. 344] (book p. 344; PDF p. 361)

### Example 5.35 — Intended polymorphic behaviour schemes for `node` and `pipe`
- Statement: Returning to `Example 5.34`:
  - `node` has intended type scheme:
    ```text
    ∀'a, 'b, '1, ''1, ''2. ('a →^{'1} 'b) →^Λ ('a chan ''1) →^Λ ('b chan ''2) →^φ unit
    where φ = spawn(rec '2. (''1?'a; '1; ''2!'b; '2))
    ```
  - `pipe` has intended type scheme (transcribed verbatim with printed unmatched `(` and unbraced `C` in
    `'a chan C` and `C!'a`; finding F-U5b-08):
    ```text
    ∀'a, '1, ''1, ''2. (('a →^{'1} 'a) list →^Λ ('a chan (''1 ∪ {C})) →^Λ ('a chan ''2) →^{φ'} unit
    where φ' = rec '2. (spawn(rec '3. ((''1 ∪ {C})?'a; Λ; ''2!'a; '3))
                        + 'a chan C; spawn(rec '4. ((''1 ∪ {C})?'a; '1; C!'a; '4)); '2)
    ```
    The first summand of `φ'` corresponds to the `then`-branch (`id` has behaviour `Λ`) and the second to the
    `else`-branch (allocating channel `C`, spawning a stage, and recursing). `■`
- Citation: [PPA Example 5.35, p. 345] (book p. 345; PDF p. 362)

### [U5b:5.5.1-c] Communication judgements, mutually recursive `τ̂ ≤ τ̂'` (`chan` invariance), and no `Observe`
- Statement:
  - Judgements `Γ̂ ⊢_CA e : σ̂ & φ` are defined in `Tables 5.16–5.17`. Note `[fun]` does not syntactically force
    `φ₀` to have the form `rec β'.φ'`, instead relying on `[sub]` with `φ[β ↦ rec β.φ] ⊑ rec β.φ` (`p. 345`,
    `p. 349`).
  - Unlike `Tables 5.12–5.13` (`§5.4.3`), there is **no** `[region]` / `Observe` masking rule because
    Communication Analysis must record *all* communications performed during computation (`p. 349`).
  - Mutually recursive type subtyping `τ̂ ≤ τ̂'` (`p. 347`, interpreted mutually recursively with `φ ⊑ φ'` in
    Table 5.18):
    ```text
    τ̂ ≤ τ̂

    τ̂'₁ ≤ τ̂₁    τ̂₂ ≤ τ̂'₂    φ ⊑ φ'
    ─────────────────────────────────
      (τ̂₁ →^φ τ̂₂) ≤ (τ̂'₁ →^{φ'} τ̂'₂)

    τ̂ ≤ τ̂'    τ̂' ≤ τ̂    r ⊆ r'
    ────────────────────────────
      τ̂ chan r ≤ τ̂' chan r'
    ```
    `τ̂ chan r` is covariant in `r` (`r ⊆ r'` modulo `UCAI`) and **invariant** — both covariant (when sending)
    and contravariant (when receiving) — in payload `τ̂` (`pp. 347–348`).
- Citation: [PPA §5.5.1, p. 345] (book p. 345; PDF p. 362); [PPA §5.5.1, p. 347] (book p. 347; PDF p. 364); [PPA §5.5.1, p. 348] (book p. 348; PDF p. 365); [PPA §5.5.1, p. 349] (book p. 349; PDF p. 366)

### Table 5.16 — Communication Analysis (part 1)
- Statement: Sequential core rules for `Γ̂ ⊢_CA e : σ̂ & φ` (`[fn]` erased in PDF OCR, verified on p. 346):
  ```text
  [con]  Γ̂ ⊢_CA c : τ_c & Λ

  [var]  Γ̂ ⊢_CA x : σ̂ & Λ                                              if Γ̂(x) = σ̂

  [fn]   Γ̂[x ↦ τ̂_x] ⊢_CA e₀ : τ̂₀ & φ₀
         ──────────────────────────────────────────
         Γ̂ ⊢_CA fn_π x => e₀ : τ̂_x →^{φ₀} τ̂₀ & Λ

  [fun]  Γ̂[f ↦ τ̂_x →^{φ₀} τ̂₀][x ↦ τ̂_x] ⊢_CA e₀ : τ̂₀ & φ₀
         ────────────────────────────────────────────────────
         Γ̂ ⊢_CA fun_π f x => e₀ : τ̂_x →^{φ₀} τ̂₀ & Λ

  [app]  Γ̂ ⊢_CA e₁ : τ̂₂ →^{φ₀} τ̂₀ & φ₁    Γ̂ ⊢_CA e₂ : τ̂₂ & φ₂
         ────────────────────────────────────────────────────────
                     Γ̂ ⊢_CA e₁ e₂ : τ̂₀ & φ₁; φ₂; φ₀

  [if]   Γ̂ ⊢_CA e₀ : bool & φ₀    Γ̂ ⊢_CA e₁ : τ̂ & φ₁    Γ̂ ⊢_CA e₂ : τ̂ & φ₂
         ────────────────────────────────────────────────────────────────────
                  Γ̂ ⊢_CA if e₀ then e₁ else e₂ : τ̂ & φ₀; (φ₁ + φ₂)

  [let]  Γ̂ ⊢_CA e₁ : σ̂₁ & φ₁    Γ̂[x ↦ σ̂₁] ⊢_CA e₂ : τ̂₂ & φ₂
         ──────────────────────────────────────────────────────
                  Γ̂ ⊢_CA let x = e₁ in e₂ : τ̂₂ & φ₁; φ₂

  [op]   Γ̂ ⊢_CA e₁ : τ_op^1 & φ₁    Γ̂ ⊢_CA e₂ : τ_op^2 & φ₂
         ────────────────────────────────────────────────────
                  Γ̂ ⊢_CA e₁ op e₂ : τ_op & φ₁; φ₂; Λ
  ```
- Citation: [PPA Table 5.16, p. 346] (book p. 346; PDF p. 363)

### Example 5.36 — Soundness necessity of `ζ_i ∉ FV(φ)` in `[gen]`
- Statement: Consider the type-unsafe program:
  ```text
  let ch = channel_A
  in (send 1 on ch; send true on ch)
  ```
  `[chan]` derives `[] ⊢_CA channel_A : 'a chan {A} & 'a chan {A}`. Because `'a` occurs free in the behaviour
  `'a chan {A}`, `[gen]` refuses to generalise `'a`, leaving `ch : 'a chan {A}` monomorphic and rejecting the
  program (`'a` cannot equal both `int` and `bool`). Had `[gen]` checked only `ζ_i ∉ FV(Γ̂)`, `ch` would receive
  `∀'a. 'a chan {A}` and the unsound program would type-check! `■`
- Citation: [PPA Example 5.36, p. 346] (book p. 346; PDF p. 363); [PPA Example 5.36, p. 347] (book p. 347; PDF p. 364)

### Table 5.17 — Communication Analysis (part 2)
- Statement: Concurrency, subtyping, and polymorphism rules for `Γ̂ ⊢_CA e : σ̂ & φ`:
  ```text
  [chan]     Γ̂ ⊢_CA channel_π : τ̂ chan {π} & τ̂ chan {π}

  [spawn]    Γ̂ ⊢_CA e₀ : τ̂₀ & φ₀
             ───────────────────────────────
             Γ̂ ⊢_CA spawn e₀ : unit & spawn φ₀

  [send]     Γ̂ ⊢_CA e₁ : τ̂ & φ₁    Γ̂ ⊢_CA e₂ : τ̂ chan r₂ & φ₂
             ───────────────────────────────────────────────────
                 Γ̂ ⊢_CA send e₁ on e₂ : unit & φ₁; φ₂; r₂!τ̂

  [receive]  Γ̂ ⊢_CA e₀ : τ̂ chan r₀ & φ₀
             ──────────────────────────────
             Γ̂ ⊢_CA receive e₀ : τ̂ & φ₀; r₀?τ̂

  [seq]      Γ̂ ⊢_CA e₁ : τ̂₁ & φ₁    Γ̂ ⊢_CA e₂ : τ̂₂ & φ₂
             ────────────────────────────────────────────
                     Γ̂ ⊢_CA e₁; e₂ : τ̂₂ & φ₁; φ₂

  [ch]       Γ̂ ⊢_CA ch : τ̂ chan r & Λ                                  if τ̂ chan r = Γ̂(ch)

  [sub]      Γ̂ ⊢_CA e : τ̂ & φ
             ───────────────────                                       if τ̂ ≤ τ̂' and φ ⊑ φ'
             Γ̂ ⊢_CA e : τ̂' & φ'

  [gen]      Γ̂ ⊢_CA e : τ̂ & φ
             ─────────────────────────────                             if ζ₁, ···, ζ_n do not occur free in Γ̂ and φ
             Γ̂ ⊢_CA e : ∀(ζ₁, ···, ζ_n). τ̂ & φ

  [ins]      Γ̂ ⊢_CA e : ∀(ζ₁, ···, ζ_n). τ̂ & φ
             ─────────────────────────────────                         if θ has dom(θ) ⊆ {ζ₁, ···, ζ_n}
             Γ̂ ⊢_CA e : (θ τ̂) & φ
  ```
- Citation: [PPA Table 5.17, p. 347] (book p. 347; PDF p. 364)

### Table 5.18 — Ordering on behaviours
- Statement: Complete 22-rule axiomatisation of the behaviour preorder `φ₁ ⊑ φ₂` (`6` preorder/congruence rules,
  `13` monoid/choice/right-distributivity/unfolding axioms, and `3` channel/I/O variance rules — 9 of the 22
  erased in PDF OCR, restored in full from rendered p. 348):
  ```text
  φ ⊑ φ                                              φ₁ ⊑ φ₂    φ₂ ⊑ φ₃
                                                     ──────────────────
                                                          φ₁ ⊑ φ₃

  φ₁ ⊑ φ₂    φ₃ ⊑ φ₄                                 φ₁ ⊑ φ₂    φ₃ ⊑ φ₄
  ──────────────────────                             ──────────────────────
    φ₁; φ₃ ⊑ φ₂; φ₄                                    φ₁ + φ₃ ⊑ φ₂ + φ₄

        φ₁ ⊑ φ₂                                            φ₁ ⊑ φ₂
  ──────────────────────                             ────────────────────
  spawn φ₁ ⊑ spawn φ₂                                rec β.φ₁ ⊑ rec β.φ₂

  φ₁; (φ₂; φ₃) ⊑ (φ₁; φ₂); φ₃                        (φ₁; φ₂); φ₃ ⊑ φ₁; (φ₂; φ₃)
  (φ₁ + φ₂); φ₃ ⊑ (φ₁; φ₃) + (φ₂; φ₃)                (φ₁; φ₃) + (φ₂; φ₃) ⊑ (φ₁ + φ₂); φ₃
  φ ⊑ Λ; φ          Λ; φ ⊑ φ                         φ ⊑ φ; Λ          φ; Λ ⊑ φ
  φ₁ ⊑ φ₁ + φ₂      φ₂ ⊑ φ₁ + φ₂                     φ + φ ⊑ φ
  rec β.φ ⊑ φ[β ↦ rec β.φ]                           φ[β ↦ rec β.φ] ⊑ rec β.φ

  τ̂ ≤ τ̂'    τ̂' ≤ τ̂    r ⊆ r'
  ────────────────────────────
    τ̂ chan r ⊑ τ̂' chan r'

  r₁ ⊆ r₂    τ̂₁ ≤ τ̂₂                                 r₁ ⊆ r₂    τ̂₂ ≤ τ̂₁
  ────────────────────                               ────────────────────
    r₁!τ̂₁ ⊑ r₂!τ̂₂                                      r₁?τ̂₁ ⊑ r₂?τ̂₂
  ```
- Side conditions (`pp. 348–349`):
  - `;` is associative with two-sided identity `Λ` and **right-distributive** over `+` (`(φ₁ + φ₂); φ₃ ≡
    (φ₁; φ₃) + (φ₂; φ₃)`; left-distributivity is intentionally omitted!).
  - `+` is associative, commutative, and idempotent (`φ₁ ⊑ φ₁ + φ₂`, `φ₂ ⊑ φ₁ + φ₂`, `φ + φ ⊑ φ` make `+` the
    join wrt `⊑`).
  - `τ̂ chan r` is covariant in `r` and **invariant** in `τ̂`; send `r!τ̂` is covariant in both `r` and `τ̂`;
    receive `r?τ̂` is covariant in `r` and **contravariant** in `τ̂`.
  - Bound variables in `rec β.φ` are identified up to α-equivalence (`rec β.φ = rec β'.φ'`, p. 349).
- Citation: [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365); [PPA §5.5.1, p. 349] (book p. 349; PDF p. 366)

### Example 5.37 — Verifying `node` and `pipe` via Table 5.18
- Statement: Using `[fun]` and `[sub]` (`Tables 5.16–5.17`) with `φ[β ↦ rec β.φ] ⊑ rec β.φ` (`Table 5.18`) and
  `[gen]`, `node` gets `('a →^{'1} 'b) →^Λ ('a chan ''1) →^Λ ('b chan ''2) →^φ unit` and `pipe` gets
  `(('a →^{'1} 'a) list) →^Λ ('a chan (''1 ∪ {C})) →^Λ ('a chan ''2) →^{φ'} unit`, merging input region `''1`
  with local channel `{C}` (`''1 ∪ {C}`) while keeping output region `''2` separate (repeating `Example 5.35`'s
  unbraced `'a chan C` and `C!'a`; finding F-U5b-08). `■`
- Citation: [PPA Example 5.37, p. 349] (book p. 349; PDF p. 366)

### Findings (5.5.1)
- F-U5b-08 (`[Source Erratum — Unbraced Region C & Unmatched Parenthesis in Examples 5.35 and 5.37]`): `Reg_CA`
  (`p. 344`) defines `r ::= {π} | ϱ | r₁ ∪ r₂ | ∅` and `Table 5.17` `[chan]` (`p. 347`) produces
  `τ̂ chan {π}`, yet both `Example 5.35` (`p. 345`) and `Example 5.37` (`p. 349`) write bare `C` instead of
  `{C}` in `'a chan C` and `C!'a` right beside braced `(''1 ∪ {C})?'a`; `Example 5.35` (`p. 345`) also prints an
  unmatched `(` before `('a →^{'1} 'a) list` in `pipe`'s type scheme (closed properly in `Example 5.37` on
  `p. 349`). [PPA §5.5.1, p. 344] (book p. 344; PDF p. 361); [PPA Example 5.35, p. 345] (book p. 345; PDF p. 362);
  [PPA Table 5.17, p. 347] (book p. 347; PDF p. 364); [PPA Example 5.37, p. 349] (book p. 349; PDF p. 366)
- F-U5b-09 (`[Unrestricted Polarity of Bound β in rec β.φ]`): Mutual recursion between `Type_CA` (`p. 343`) and
  `Ann_CA` (`p. 344`) syntactically allows bound `β` inside `τ̂` in contravariant `r?τ̂` (e.g.
  `r?(τ̂₁ →^β τ̂₂)`) or invariant `τ̂ chan r` (`Table 5.18`, `p. 348`), making `φ ↦ ψ[β ↦ φ]` non-monotone wrt
  `⊑`; well-founded fixed-point semantics requires `rec β.ψ` to bind `β` strictly positively (outside
  contravariant/invariant type positions) `[derived]`. [PPA §5.5.1, p. 343] (book p. 343; PDF p. 360);
  [PPA §5.5.1, p. 344] (book p. 344; PDF p. 361); [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365)
- F-U5b-10 (`[Section 5.5.1 Editorial Typos]`): p. 345 prints `"these types schemes"` and `"by the axiom and
  rules"`; p. 348 below Table 5.18 prints `"'a subset of' of r'"` (doubled `"of"`), `"behaviours in more
  complex"` (`"in"` for `"is"`), and `"axioms for recursion allows"`.
  [PPA Example 5.35, p. 345] (book p. 345; PDF p. 362); [PPA §5.5.1, p. 348] (book p. 348; PDF p. 365)

### Projections (5.5.1)
- cs_theory:
  1. **Directional I/O subtyping & `[external: Session Types]`**: `Table 5.18`'s split between covariant output
     `r₁!τ̂₁ ⊑ r₂!τ̂₂` (`τ̂₁ ≤ τ̂₂`), contravariant input `r₁?τ̂₁ ⊑ r₂?τ̂₂` (`τ̂₂ ≤ τ̂₁`), and invariant bidirectional
     `τ̂ chan r` is the exact type-theoretic core of
     `[external: Pierce–Sangiorgi 1996 input/output π-calculus subtyping]` and
     `[external: Honda–Vasconcelos–Kubo Session Types]`.
  2. **Why `Table 5.18` omits left-distributivity (`[external: branching-time deadlock]` preservation)**:
     `(φ₁ + φ₂); φ₃ ≡ (φ₁; φ₃) + (φ₂; φ₃)` holds because any internal choice already committed before `φ₃`
     continues with `φ₃`, whereas left-distributivity `φ₁; (φ₂ + φ₃) ≡ (φ₁; φ₂) + (φ₁; φ₃)` is **omitted**:
     under synchronous `[comm]`, `c!1; (d?int + e?int)` synchronises on `c` *before* choosing `d` vs `e`,
     whereas `(c!1; d?int) + (c!1; e?int)` commits early and can `[external: deadlock]` against a peer offering
     `c?int; d!7` (`[external: Milner CCS / van Glabbeek branching-time spectrum]`) `[derived]`.
- swe_architecture: `Example 5.36` (`ζ_i ∉ FV(φ)` in `[gen]`) is the **semantic effect-based generalisation** of
  `[external: Wright 1995 ML syntactic value restriction]`: syntactic values (`fn`, `fun`, `c`) emit silent
  behaviour `Λ` (`∅`) and generalise freely at `let`, whereas effectful channel/reference allocations record `'a`
  in `φ = 'a chan {A}` and stay monomorphic without syntactically banning pure helper calls `id x`.
- practical_debugging: Two subtle solver bugs arise in `Tables 5.17–5.18`:
  1. **Unclosed constraint set at `[gen]`**: if `channel_A` emits fresh behaviour variable `β` with side
     constraint `'a chan {A} ⊑ β`, naive syntactic `FV(β) = {β}` misses `'a`! `[gen]` must forbid all variables
     in the **downwards closure** of `FV(Γ̂) ∪ FV(φ)` through the constraint set.
  2. **Non-terminating `rec β.φ` unfolding**: checking `rec β.φ₁ ⊑ rec β.φ₂` by eager `rec β.φ ⊑ φ[β ↦ rec β.φ]`
     diverges unless guarded by coinductive `[external: pair memoisation]` (`visited` cache modulo
     α-equivalence, `[external: Amadio–Cardelli equi-recursive subtyping]`) `[derived]`.
- cyber:
  1. **`[external: IPC]` / channel type confusion (`[external: CWE-843]`)**: omitting `ζ_i ∉ FV(φ)` in `[gen]`
     (`Example 5.36`) or payload invariance on `τ̂ chan r` allows one thread to send raw integer `42` on `ch`
     while another thread receives a function closure or capability handle from `ch`.
  2. **`[external: Deadlock (CWE-833)]` & `[external: TOCTOU (CWE-367)]`**: causal behaviours `φ₁; φ₂` with
     right-only distributivity (`Table 5.18`) and unmasked global visibility expose lock/rendezvous order
     inversions (`r₁!τ̂₁; r₂?τ̂₂` vs `r₂!τ̂₂; r₁?τ̂₁`, `[external: CWE-833]`) and interleaved check-then-act windows
     between `r?τ̂_check` and `r!τ̂_use` (`[external: CWE-367]`) that unordered effect sets (`§5.4`) completely
     erase.

---

## Chapter 5 Concluding Remarks

Context: Historical survey and architectural synthesis covering Type-Based Control Flow Analysis (`U8` subtyping
taxonomy), the five design axes of *Restricted Effects* (`two-stage inference` and `effect masking`), *General
Effects* (types inside effects, `downwards closure` at `[gen]`, constrained schemes, temporal behaviours), and
links to Monotone Frameworks and Abstract Interpretation
[PPA Chapter 5 Concluding Remarks, p. 349] (book p. 349; PDF p. 366);
[PPA Chapter 5 Concluding Remarks, p. 353] (book p. 353; PDF p. 370).

### [U5b:CR-a] Control Flow Analysis, subtyping taxonomy, and `0-CFA` relationship
- Statement:
  - §5.1 embeds subeffecting into `[fn]`/`[fun]` without an explicit `[sub]` rule (`Exercise 5.13`), and avoids
    polymorphism and subtyping (`[49, 50, 71, 18]` survey non-standard CFA type systems).
  - Type systems with subtyping (`[59, 58, 107]`, plus polymorphism `[83, 160, 161]`) distinguish three levels:
    1. *Shape-conformant subtyping* (`⌊τ̂₁⌋ = ⌊τ̂₂⌋`, no subtyping in the underlying type system; note p. 350
       line 15 mis-cites `"Section 5.1"` for `"Section 5.4"`, finding F-U5b-11),
    2. *Atomic subtyping* (ordering imposed on base types), and
    3. *General subtyping* (ordering between arbitrary types, typically requiring explicit constraint sets in
       the inference system).
  - §5.2 formulates semantic correctness as Natural-Semantics subject reduction (`[91]`, history `[114, 116,
    184]`) and proves Moore-family existence (`[114]`, linked to principal types). §5.3 (`[90, 183, 167, 168,
    169]`; `Mini Project 5.1` based on `[169]`) operates over a *free algebra* (`simple types` + constraint sets)
    rather than non-free equational unification (`[159]`).
- Citation: [PPA Chapter 5 Concluding Remarks, p. 349] (book p. 349; PDF p. 366); [PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367)

### [U5b:CR-b] Restricted effects, five design axes, two-stage inference, and Region Inference incompleteness
- Statement:
  - *Restricted effects* (`§§5.1, 5.4`; pioneering works `[88, 102, 89, 90]`): **no type information is recorded
    in effects**, and **effects cannot influence underlying type shapes**.
  - *Five design axes* (`p. 351`): (1) subeffecting, (2) subtyping, (3) `let`-polymorphism, (4) polymorphic
    recursion, and (5) whether constraints are explicit in the inference system (implicitly via `β.φ` in
    §5.4.3).
  - *Two-stage implementation* (`[169, 174]`, `pp. 351–352`): for §5.4.1 (soundness via §5.2; without subtyping,
    §5.3 gives sound and complete inference) and §5.4.2 (soundness via `[173, 167, 168, 15]`), shape-conformant
    subtyping + restricted effects permit **Stage 1** (infer underlying Hindley–Milner types) followed by
    **Stage 2** (solve effect/annotation constraints), yielding syntactically sound and complete inference.
  - *Region Inference* (`§5.4.3`, `[175]` `[external: Tofte–Talpin]`, soundness `[176]`, *effect masking* `[102, 167,
    168]`): uses Stage 1 ordinary type inference followed by `[174]`'s `Algorithm S` (generating effect/region
    variables) and `Algorithm R` (handling effect/region polymorphic recursion), proved **syntactically sound**
    and known **not to be syntactically complete** (sound-and-complete inference under polymorphic recursion
    remains beyond state-of-the-art).
- Citation: [PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367); [PPA Chapter 5 Concluding Remarks, p. 351] (book p. 351; PDF p. 368); [PPA Chapter 5 Concluding Remarks, p. 352] (book p. 352; PDF p. 369)

### [U5b:CR-c] General effects (`downwards closure` at `[gen]`), causal behaviours, and other developments
- Statement:
  - *Type information inside effects* (`p. 352`, `[183, 167, 168]` generalising expansive-expression /
    imperative type-variable disciplines `[173, 166]`): breaks two-stage inference because effects restrict
    which type variables may be generalised! At `[gen]`, forbidden variables must be computed via the
    **downwards closure** wrt the constraint set (`[183, 127]`) or a *principal solution* (`[167, 168]`).
    Combining shape-conformant subtyping + polymorphism + subeffecting (`[127, 134, 15]`, complete constrained
    extension `[13]`) bridges Effect Systems with polymorphic subtyping (`[83, 160, 161]`).
  - *Causal behaviours* (`pp. 352–353`): §5.5 is based on `[131, 132]` with `[119, 120]` (`[14]` adds
    polymorphism; `[13]` gives explicit-constraint sound-and-complete inference; `[128]` validates embedded
    systems).
  - *Other developments* (`p. 353`): no underlying subtyping or conjunction/disjunction types (`[19, 20, 81,
    82]`); Chapter 5 expresses *safety* properties, whereas `[121]` adds totality/*liveness* annotations;
    complete-lattice annotations (`Mini Project 5.4`: BTA `[75, 114, 123]` and security `[74, 1]`) and Abstract
    Interpretation formulations of Type and Effect Systems (`[108, 36]`) link directly to Chapter 4; `Mini
    Project 5.5` (units and Y2K) draws on `[95, 46, 141]`.
- Citation: [PPA Chapter 5 Concluding Remarks, p. 352] (book p. 352; PDF p. 369); [PPA Chapter 5 Concluding Remarks, p. 353] (book p. 353; PDF p. 370)

### Findings (Concluding Remarks)
- F-U5b-11 (`[Source Erratum — Mis-Cited Section 5.1 on p. 350 & Editorial Typos]`): On p. 350 line 15,
  *Concluding Remarks* prints `"Indeed, the formulation of Section 5.1 allows only shape conformant subtyping"`,
  directly contradicting lines 2–3 of p. 350 (`"there is no additional effect component nor is there any
  coverage of polymorphism or subtyping"`) — shape-conformant subtyping is introduced in **Section 5.4**
  (§5.4.1, p. 324). Also p. 351 prints `"selection of components are"`, and p. 353 prints `"; s this mini
  project"` (stray `"s"`) and `"(inpired by [75, 114, 123])"`.
  [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341);
  [PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367);
  [PPA Chapter 5 Concluding Remarks, p. 351] (book p. 351; PDF p. 368);
  [PPA Chapter 5 Concluding Remarks, p. 353] (book p. 353; PDF p. 370)

### Projections (Concluding Remarks)
- cs_theory: **Exact `U8` unification (`Chapter 3 0-CFA` ↔ `Chapter 5` subtyped CFA, Heintze /
  `[external: Palsberg–O'Keefe 1995]`)**: §5.1 without subtyping forces symmetric equality on arrow annotations
  (`Example 5.5` smearing); equipping `Table 5.2` with contravariant arrow subtyping (`Exercise 5.9`) and
  instrumenting derivations via `Exercise 5.4` `(5.2)` (`ρ̃, C̃; Γ̂ ⊢_CFA e : τ̂`) turns equalities into directed
  inclusion constraints identical to `Table 3.6` `0-CFA` on all simply-typable `FUN` programs (and on all
  untyped `FUN` programs once `[external: equi-recursive types]` drop the occurs check).
- swe_architecture: The **Restricted vs General Effects** split is a primary architecture gate when designing
  custom type/effect passes: keep effects free of type variables whenever a fast two-stage architecture
  (off-the-shelf Hindley/Milner typechecker → standalone `[external: Datalog]`/worklist effect solver) is
  desired; the moment effect tokens embed type variables (`'a chan r`, polymorphic mutable refs), type
  generalisation and effect constraint closure must be coupled in a single pass.
- practical_debugging: Whenever implementing `Algorithm R`-style fixed-point iteration for effect/region
  polymorphic recursion, enforce an explicit region-arity / `[external: Kleene]` widening cap: because syntactic
  completeness fails, naive fixed-point unfolding without arity bounding can oscillate or split fresh region
  parameters indefinitely `[derived]`.
- cyber: Concluding Remarks explicitly flags the **safety vs liveness** boundary: every Type and Effect System
  in §§5.1–5.5 proves *partial-correctness safety* ("if evaluation reaches a point / returns, its actions lie in
  `φ`"), so diverging loops silently satisfy empty return types (`Exercise* 5.10`); auditing availability /
  non-starvation (`[external: CWE-400]` / `[external: CWE-833]`) requires pairing effect types with totality or
  termination certificates.

---

## Mini Projects (5.1–5.5)

Context: Five mini projects extending Chapter 5 with Call-Tracking Effect Analysis (`5.1`), allocation-tracked
Pairs and Lists (`5.2`), an SML/Haskell `𝒲_CFA` prototype (`5.3`), Monotone Type Systems for BTA and Security
Clearance (`5.4`), and Units of Measure and Y2K (`5.5`)
[PPA Mini Project 5.1, p. 353] (book p. 353; PDF p. 370); [PPA Mini Project 5.5, p. 359] (book p. 359; PDF p. 376).

### Mini Project 5.1 — A Call-Tracking Analysis
- Statement: Consider a Type and Effect System `Γ̂ ⊢_CT e : τ̂ & φ` (based on `[169]`) where `φ` denotes the set
  of functions that may be called during evaluation of `e` (and similarly on function arrows):
  1. Formulate an inference system with subeffecting, next add subtyping, and finally add polymorphism.
  2. For the subeffecting-only system, modify `Table 5.4` Natural Semantics so semantic correctness can be
     stated and prove the result holds.
  3. Devise a syntactically sound (and complete) inference algorithm for the subeffecting-only system
     (*ambitious*: extend to subtyping and/or polymorphism). `■`
- Citation: [PPA Mini Project 5.1, p. 353] (book p. 353; PDF p. 370); [PPA Mini Project 5.1, p. 354] (book p. 354; PDF p. 371)

### Mini Project 5.2 — Data Structures
- Statement: As in `Mini Project 3.2` ([PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221)), extend `Table
  5.2` CFA ([PPA Table 5.2, p. 288] (book p. 288; PDF p. 305)) to track data-structure creation points:
  - *Pairs*:
    ```text
    τ̂ ::= ··· | τ̂₁ ×^φ τ̂₂
    e ::= ··· | Pair_π(e₁, e₂) | (case e₀ of Pair(x₁, x₂) => e₁)
    ```
    Illustrated on pair-sorting `srt`:
    ```text
    let srt = fn_X x => case x of Pair(y,z) =>
                          if y<z then x else Pair_B(z,y)
    in srt(Pair_A(n,m))
    ```
    yielding overall annotated type `int ×^{A, B} int` (constructed at `A` if `n < m` and at `B` otherwise;
    finding F-U5b-12). Tasks: (1) modify `Table 5.2`, (2) extend `Table 5.4` and `Theorem 5.9`
    ([PPA Theorem 5.9, p. 295] (book p. 295; PDF p. 312)), (3) extend `𝒲_CFA` and `𝒰_CFA` (`Tables 5.7–5.8`)
    and `Theorems 5.20–5.21` ([PPA Theorem 5.20, p. 312] (book p. 312; PDF p. 329);
    [PPA Theorem 5.21, p. 314] (book p. 314; PDF p. 331)).
  - *Lists*: perform the analogous development for:
    ```text
    τ̂ ::= ··· | τ̂ list^φ
    e ::= ··· | Cons_π(e₁, e₂) | Nil_π | (case e₀ of Cons(x₁, x₂) => e₁ or e₂)
    ```
    (*Ambitious*: generalise to algebraic datatypes as in `Mini Project 3.2`.) `■`
- Citation: [PPA Mini Project 5.2, p. 354] (book p. 354; PDF p. 371); [PPA Mini Project 5.2, p. 355] (book p. 355; PDF p. 372)

### Mini Project 5.3 — A Prototype Implementation
- Statement: Implement §§5.1 and 5.3 CFA in Standard ML or Haskell over:
  ```sml
  type var       = string
  type point     = int
  datatype const = Num of int | True | False
  datatype exp   = Const of const | Var of var | Fn of point * var * exp
                 | Fun of point * var * var * exp | App of exp * exp
                 | If of exp * exp * exp | Let of var * exp * exp
                 | Op of string * exp * exp
  ```
  (1) Define simple types and simple substitutions and implement `𝒰_CFA` (`Table 5.7`, [PPA Table 5.7, p. 307]
  (book p. 307; PDF p. 324)); (2) define simple type environments and constraint sets and implement `𝒲_CFA`
  (`Table 5.8`, [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327)); (3) pretty-print results per §5.3.4 by
  instantiating remaining type variables to `int` and annotation variables to the least constraint solution, and
  test on selected examples. `■`
- Citation: [PPA Mini Project 5.3, p. 355] (book p. 355; PDF p. 372)

### Mini Project 5.4 — Monotone Type Systems
- Statement: Given a *monotone structure* as in §3.5.2 (e.g. Constant Propagation in `Example 3.29`,
  [PPA Example 3.29, p. 187] (book p. 187; PDF p. 205)), define an Annotated Type System with subeffecting (and
  possibly subtyping) over annotated base types in the style of `Table 1.2`
  ([PPA Table 1.2, p. 19] (book p. 19; PDF p. 39)) capable of specifying:
  - *Binding-time analysis*: static (`S`, compile-time) vs dynamic (`D`, run-time) data ordered by `S ⊑ D`
    (static data may be used where dynamic data is expected).
  - *Security analysis*: clearance levels `C₁, ···, C_k` ordered by `C₁ ⊑ ··· ⊑ C_k` (low-clearance data may be
    used at high clearance levels).
  Investigate how much of §§5.2–5.3 transfers (imposing e.g. the Ascending Chain Condition if needed;
  *ambitious*: combine subtyping and polymorphism). `■`
- Citation: [PPA Mini Project 5.4, p. 355] (book p. 355; PDF p. 372); [PPA Mini Project 5.4, p. 356] (book p. 356; PDF p. 373)

### Mini Project 5.5 — Units of Measure (and Y2K)
- Statement: Record both *scaling factor* (e.g. `x FT = (x * 0.3048) M`; `x USD = (x * rate) EURO`) and *base
  of origin* (e.g. `x YY = (1900 + x) AD`, where two-digit `x` causes the Y2K problem outside the 20th century;
  `x F = ((x - 32) * 5)/9 C` combining scale and base) via a 5-step workflow (extend types → identify unit type
  errors → insert explicit conversions → re-verify → optionally migrate data formats). Over underlying types
  `τ ::= num | τ → τ`, define:
  ```text
  τ̂     ::= num^φ | τ̂ → τ̂
  φ     ::= scale BASE base
  scale ::= σ | unit | scale.scale | scale^{-1} | feet | meter | usd | euro | year | kelvin | ···
  base  ::= β | none | ad | 20th | freezing | ···
  ```
  (e.g. `M = meter BASE none`, `USD = usd BASE none`, `AD = year BASE ad`, `YY = year BASE 20th`,
  `C = kelvin BASE freezing`, ordinary dimensionless numbers `unit BASE none`, converter
  `asC : num^{unit BASE none} → num^{kelvin BASE freezing}`). Constrained polymorphic operator schemes (`p. 358`):
  ```text
  * : ∀σ₁, σ₂, σ [with σ = σ₁.σ₂] :
        num^{σ₁ BASE none} → num^{σ₂ BASE none} → num^{σ BASE none}

  / : ∀σ₁, σ₂, σ [with σ = σ₁.(σ₂^{-1})] :
        num^{σ₁ BASE none} → num^{σ₂ BASE none} → num^{σ BASE none}

  + : ∀σ, β₁, β₂, β [with β = { β₁  if β₂ = none ;  β₂  if β₁ = none }] :
        num^{σ BASE β₁} → num^{σ BASE β₂} → num^{σ BASE β}

  - : ∀σ, β₁, β₂, β [with β = { β₁  if β₂ = none ;  none  if β₁ = β₂ ;  undefined  otherwise }] :
        num^{σ BASE β₁} → num^{σ BASE β₂} → num^{σ BASE β}
  ```
  `scale` requires Physics laws (`[external: abelian-group]` laws: `meter.feet = feet.meter`,
  `scale.unit = scale`, `scale.(scale^{-1}) = unit`), strictly more refined than `UCAI`. Formulate the annotated
  type system (allowing polymorphism over `σ` and `β`), establish semantic correctness, develop a syntactically
  sound inference algorithm, and investigate syntactic completeness. `■`
- Citation: [PPA Mini Project 5.5, p. 356] (book p. 356; PDF p. 373); [PPA Mini Project 5.5, p. 357] (book p. 357; PDF p. 374); [PPA Mini Project 5.5, p. 358] (book p. 358; PDF p. 375); [PPA Mini Project 5.5, p. 359] (book p. 359; PDF p. 376)

### Findings (Mini Projects)
- F-U5b-12 (`[Implicit Undefined Guard on Base Addition & Prose Typos in Mini Projects 5.2 and 5.5]`): On p. 358,
  `+`'s `[with β = ...]` side condition prints only `β₁ if β₂ = none` and `β₂ if β₁ = none` without explicitly
  writing `undefined otherwise` when both `β₁, β₂` are non-`none` bases (unlike `-` immediately below it, which
  prints `undefined otherwise`); p. 354 (`Mini Project 5.2`) prints `"returned with be constructed"` (`"with"`
  for `"will"`), and p. 358 (`Mini Project 5.5`) prints `"multiplication and division works"`, `"the the laws"`,
  and `"substraction"`. [PPA Mini Project 5.2, p. 354] (book p. 354; PDF p. 371);
  [PPA Mini Project 5.5, p. 358] (book p. 358; PDF p. 375)

### Projections (Mini Projects)
- cs_theory: `Mini Project 5.5` combines `[external: free abelian-group unification]` (`scale`, decidable via
  `[external: integer Gaussian / Hermite normal form; Kennedy 1994/1997 / F# units of measure]`) with
  `[external: affine-space (torsor) typing]` (`base`: `point - point = vector (none)`, `point + vector = point`,
  `point + point = undefined`, matching `[external: C++ std::chrono::time_point vs duration]`), showing why
  domain-specific effect algebras transcend idempotent `UCAI` sets.
- swe_architecture: `Mini Project 5.4` (`S ⊑ D`, `C₁ ⊑ ··· ⊑ C_k`) bridges Chapter 2/4 complete-lattice
  Monotone Frameworks directly into modular Hindley/Milner library signatures, letting multi-stage compilers
  (partial evaluators) and `[external: taint-tracking]` linters check open modules per-function without
  whole-program CFA.
- practical_debugging: When implementing `Mini Project 5.3` (`𝒲_CFA` + `§5.3.4`), remember F-U5b-01:
  unconstrained `AVar`s `β ∉ AV(C)` in `(θ Γ̂)` or `τ̂` must be defaulted to `∅` alongside `θ_A`, and `𝒰_CFA`
  occurs checks must test `α ∈ FV(ST)` on underlying `SType`s (`Table 5.7`) `[derived]`.
- cyber:
  1. **Information-flow confidentiality (`Mini Project 5.4`, `C₁ ⊑ ··· ⊑ C_k`)**: enforces
     `[external: Denning / Volpano–Smith–Irvine noninterference]` on pure functional flows (`if high then e₁ else e₂`
     `[external: taints]` the branch result to `≥ high`); note that if combined with §5.4.1 mutable references
     `x := e`, a pure value-level clearance system MUST add a `[external: program-counter (pc)]` lower bound on
     write effects (`pc ⊑ level(x)`) to block `[external: implicit-flow]` side-channel leaks.
  2. **Epoch, currency, and physical-unit confusion (`Mini Project 5.5`, `[external: CWE-682]`)**: statically
     rejects adding incompatible currencies (`USD + EURO`), multiplying absolute dates, or subtracting `20th`
     (`YY`) from `ad` (`AD`) timestamps without explicit epoch conversion.

---

## Exercises (5.1–5.15)

Context: Fifteen exercises (`5.4*` and `5.10*` starred in the printed book) spanning `⊢_UL` / `⊢_CFA`
derivations, `[external: Church-style]` determinacy, `UCAI` set-inclusion axiomatisation, the `(5.2)` instrumented
`0-CFA` bridge, dead-call `⊥_{τ̂₀}`, call-site label tracking `LAnn`, CBV vs CBN invariance, Robinson unification,
contravariant `(Typê[τ], ≤)` Moore-family failure, parametric divergence, Side Effect semantic soundness and
CBN adaptation, proof normalisation, `AV(φ₂) = ∅` handler pruning, and scheme-conclusion `Table 5.10`
[PPA Exercise 5.1, p. 359] (book p. 359; PDF p. 376); [PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380).

### Exercise 5.1 — Typing `(f g) + (f h)` in Table 5.1 and Table 5.2
- Statement: Consider:
  ```text
  let f = fn_X x => x 1;
      g = fn_Y y => y+2;
      h = fn_Z z => z+3
  in (f g) + (f h)
  ```
  Use `Table 5.1` ([PPA Table 5.1, p. 285] (book p. 285; PDF p. 302)) to type the expression and identify the
  types of `f`, `g`, and `h`; next use `Table 5.2` ([PPA Table 5.2, p. 288] (book p. 288; PDF p. 305)) to obtain
  its annotated type and the annotated types of `f`, `g`, and `h` (`[derived]`: without subtyping or
  polymorphism, `f` forces `g` and `h` to share `(int →^{Y, Z} int)`). `■`
- Citation: [PPA Exercise 5.1, p. 359] (book p. 359; PDF p. 376)

### Exercise 5.2 — Explicitly typed (`[external: Church-style]`) abstractions and typing determinism
- Statement: Modify `Table 5.1` for explicitly typed function definitions `fn_π x : τ_x => e₀` and
  `fun_π f : (τ_x → τ₀) x => e₀`, and prove determinism: `Γ ⊢_UL e : τ₁ ∧ Γ ⊢_UL e : τ₂ ⇒ τ₁ = τ₂`. `■`
- Citation: [PPA Exercise 5.2, p. 359] (book p. 359; PDF p. 376)

### Exercise 5.3 — Axiomatising set inclusion `φ₁ ⊆ φ₂` modulo `UCAI`
- Statement: Give an axiomatisation of `φ₁ ⊆ φ₂` (§§5.4.1 and 5.2.3) such that `φ₁ ⊆ φ₂` holds iff the set of
  elements mentioned in `φ₁` is a subset of the set of elements mentioned in `φ₂`. `■`
- Citation: [PPA Exercise 5.3, p. 359] (book p. 359; PDF p. 376)

### Exercise 5.4 — (Starred `Exercise* 5.4` in book) Instrumented `0-CFA` bridge `ρ̃, C̃; Γ̂ ⊢_CFA e : τ̂` `(5.2)`
- Statement: To formalise `Example 5.4` ([PPA Example 5.4, p. 288] (book p. 288; PDF p. 305)), simultaneously
  label `FUN` expressions as in Chapters 3 and 5:
  ```text
  e ::= t^ℓ
  t ::= c | x | fn_π x => e₀ | fun_π f x => e₀ | e₁ e₂
      | if e₀ then e₁ else e₂ | let x = e₁ in e₂ | e₁ op e₂
  ```
  Modify `Table 5.2` to define a judgement (formula erased in PDF OCR, restored from rendered p. 359):
  ```text
  ρ̃, C̃; Γ̂ ⊢_CFA e : τ̂                                                 (5.2)
  ```
  such that `C̃(ℓ) = τ̂_ℓ` forces every judgement `ρ̃, C̃; Γ̂' ⊢_CFA t^ℓ : τ̂'` in `(5.2)` to have `τ̂' = τ̂_ℓ`, and
  `ρ̃(x) = τ̂_x` forces every judgement `ρ̃, C̃; Γ̂' ⊢_CFA x^ℓ : τ̂'` in `(5.2)` to have `τ̂' = τ̂_x`. Verify `(5.2)`
  on `Example 5.4` with `C̃(1) = τ̂_Y`, `C̃(2) = τ̂_Y →^{X} τ̂_Y`, `C̃(3) = int`, `C̃(4) = τ̂_Y`, `C̃(5) = τ̂_Y`,
  `ρ̃(x) = τ̂_Y`, and `ρ̃(y) = int` (where `{X}` is written above the arrow in `C̃(2)`). `■`
- Citation: [PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376); [PPA Exercise 5.4, p. 360] (book p. 360; PDF p. 377)

### Exercise 5.5 — Dead-call `[app]` rule returning `⊥_{τ̂₀}` when `φ = ∅`
- Statement: Consider adding to `Table 5.2`:
  ```text
  Γ̂ ⊢_CFA e₁ : τ̂₂ →^φ τ̂₀    Γ̂ ⊢_CFA e₂ : τ̂₂
  ─────────────────────────────────────────    if φ = ∅
              Γ̂ ⊢_CFA e₁ e₂ : ⊥_{τ̂₀}
  ```
  where `⊥_{τ̂₀}` is the least element of `Typê[τ₀]` and `τ₀ = ⌊τ̂₀⌋`. Explain what this rule does and determine
  whether `Theorem 5.9` ([PPA Theorem 5.9, p. 295] (book p. 295; PDF p. 312)) continues to hold (`[derived]`:
  yes — under `Table 5.4` big-step semantics, if `e₁` evaluates to `fn_π x => e₀`, Subject Reduction forces
  `π ∈ φ`, contradicting `φ = ∅`; thus `e₁ e₂` cannot terminate with a value when `φ = ∅`, so assigning least
  element `⊥_{τ̂₀}` is vacuously sound!). `■`
- Citation: [PPA Exercise 5.5, p. 360] (book p. 360; PDF p. 377)

### Exercise 5.6 — Dual arrow annotations `τ̂₁ →^φ_ψ τ̂₂` tracking call-site labels `ψ ∈ LAnn`
- Statement: Extend §5.1 CFA to record *where* functions are called by adding application labels
  `e ::= ··· | (e₁ e₂)^ℓ`, label annotations `ψ ∈ LAnn` (`ψ ::= ℓ | ψ₁ ∪ ψ₂ | ∅` modulo `UCAI`; finding
  F-U5b-13), and dual-annotated arrows `τ̂ ::= ··· | τ̂₁ →^φ_ψ τ̂₂` (`φ` above, `ψ` below the arrow). Modify
  `Table 5.2` so that in `((fn_X x => x) (fn_Y y => y))^1` (`Example 5.4`), `fn_X x => x` gets
  `(int →^{\{Y\}}_∅ int) →^{\{X\}}_{\{1\}} (int →^{\{Y\}}_∅ int)` and more generally
  `(τ̂ →^{\{Y\} ∪ φ_Y}_{ψ_Y} τ̂) →^{\{X\} ∪ φ_X}_{\{1\} ∪ ψ_X} (τ̂ →^{\{Y\} ∪ φ_Y}_{ψ_Y} τ̂)` for all
  `φ_X, φ_Y ∈ Ann`, `ψ_X, ψ_Y ∈ LAnn`, and `τ̂ ∈ Typê`. `■`
- Citation: [PPA Exercise 5.6, p. 360] (book p. 360; PDF p. 377)

### Exercise 5.7 — Call-by-name Table 5.4 vs Table 5.2 soundness and precision
- Statement: Modify `[app]` and `[let]` in `Table 5.4` ([PPA Table 5.4, p. 292] (book p. 292; PDF p. 309)) to
  call-by-name (substituting unevaluated arguments), show `Theorem 5.9` still holds for `Table 5.2` unchanged,
  and explain what this reveals about precision (`[derived]`: `Table 5.2` is evaluation-order-insensitive,
  soundly over-approximating both CBV and CBN). `■`
- Citation: [PPA Exercise 5.7, p. 361] (book p. 361; PDF p. 378)

### Exercise 5.8 — Syntactic soundness and completeness of Robinson unification (`Fact 5.17`)
- Statement: Prove `Fact 5.17` ([PPA Fact 5.17, p. 308] (book p. 308; PDF p. 325)), syntactic soundness and
  completeness of Robinson unification (`Table 5.7`, [PPA Table 5.7, p. 307] (book p. 307; PDF p. 324)). `■`
- Citation: [PPA Exercise 5.8, p. 361] (book p. 361; PDF p. 378)

### Exercise 5.9 — Contravariant subtype lattice `(Typê[τ], ≤)` vs Proposition 5.12 and `θ''_T(α)`
- Statement: On §5.1 annotated types, define contravariant-domain / covariant-codomain-and-arrow ordering `≤`:
  ```text
  τ̂ ≤ τ̂        (τ̂'₁ ≤ τ̂₁ ∧ τ̂₂ ≤ τ̂'₂ ∧ φ ⊆ φ') ⇒ (τ̂₁ →^φ τ̂₂) ≤ (τ̂'₁ →^{φ'} τ̂'₂)
  ```
  (1) Show `(Typê[τ], ≤)` is a complete lattice for every `τ ∈ Type` (flipping joins/meets in contravariant
  positions); (2) investigate whether `Proposition 5.12`
  ([PPA Proposition 5.12, p. 299] (book p. 299; PDF p. 316), Moore family of typings) holds for `≤`
  (`[derived]`: **false!** For `fn_X x => x` at
  `τ = (int → int) → (int → int)`, valid typings `(int →^φ int) →^{\{X\}} (int →^φ int)` over all `φ` have
  `≤`-meet `(int →^⊤ int) →^{\{X\}} (int →^∅ int)`, which is *not* a valid typing and is semantically unsound!);
  (3) reconsider choosing `θ''_T(α)` in §5.3.4 as least in `(Typê[τ], ⊑)` vs `(Typê[τ], ≤)` vs `(Typê[τ], ≥)`
  (finding F-U5b-13). `■`
- Citation: [PPA Exercise 5.9, p. 361] (book p. 361; PDF p. 378)

### Exercise 5.10 — (Starred `Exercise* 5.10` in book) Non-termination proof from `𝒲_UL([], fun_F f x => e₀) = (α_x → α₀, θ)`
- Statement: Suppose `𝒲_UL([], fun_F f x => e₀) = (α_x → α₀, θ)` with **distinct** type variables `α_x ≠ α₀`.
  Let `e` be any closed expression with `[] ⊢_UL e : τ`; prove `(fun_F f x => e₀) e` cannot terminate (Hint: use
  `Fact 5.6` [PPA Fact 5.6, p. 291] (book p. 291; PDF p. 308), `Theorems 5.9, 5.20, 5.21`, and syntactic
  soundness of `𝒲_UL`; `[derived]`: instantiating `α_x ↦ τ` and `α₀` separately to `int` and `bool` gives both
  `[] ⊢_UL (fun_F f x => e₀) e : int` and `: bool`, whereas any terminating value `v` has a unique base/arrow
  kind, forcing divergence!). `■`
- Citation: [PPA Exercise 5.10, p. 361] (book p. 361; PDF p. 378)

### Exercise 5.11 — Semantic correctness formulation for Side Effect Analysis (Table 5.9)
- Statement: Formulate semantic correctness for `Table 5.9` (`§5.4.1`) by modifying the store-passing Natural
  Semantics (`Table 5.4` + `p. 320`) to record actual runtime side effects (`new π`, `!π`, `π:=`) alongside
  location-to-point provenance (`Σ(ξ) = π` `[derived]`). `■`
- Citation: [PPA Exercise 5.11, p. 361] (book p. 361; PDF p. 378)

### Exercise 5.12 — Call-by-name Side Effect Analysis
- Statement: Modify `Table 5.9` (`§5.4.1`) assuming call-by-name rather than call-by-value semantics
  (`[derived]`: variable/argument bindings carry latent thunk effects `(τ̂, φ)` discharged at variable use sites
  rather than eagerly at `[app]`/`[let]`). `■`
- Citation: [PPA Exercise 5.12, p. 362] (book p. 362; PDF p. 379)

### Exercise 5.13 — Two-step proof normalisation eliminating standalone subeffecting
- Statement: Assuming `Table 5.9` includes *only* subeffecting (no subtyping):
  1. Dispense with explicit `[sub]` by adding `"∪ φ'"` to all effects in the conclusions of *all* axioms and
     rules, and prove the exact same judgements are derivable.
  2. Restrict `"∪ φ'"` *only* to axioms (`[con]`, `[var]`, `[deref]`) and function abstractions (`[fn]`, `[fun]`),
     and prove equivalence again — illustrating *proof normalisation* so inference trees match syntax trees for
     soundness proofs and inference-algorithm design. `■`
- Citation: [PPA Exercise 5.13, p. 362] (book p. 362; PDF p. 379)

### Exercise 5.14 — Precision refinement of `[handle]` in Table 5.10 via `AV(φ₂) = ∅`
- Statement: Determine whether `Table 5.10` (`§5.4.2`) remains semantically sound if `[handle]` is replaced by:
  ```text
  Γ̂ ⊢_ES e₁ : τ̂ & φ₁    Γ̂ ⊢_ES e₂ : τ̂ & φ₂
  ─────────────────────────────────────────────    if s ∉ φ₂ and AV(φ₂) = ∅
        Γ̂ ⊢_ES handle s as e₁ in e₂ : τ̂ & φ₂

  Γ̂ ⊢_ES e₁ : τ̂ & φ₁    Γ̂ ⊢_ES e₂ : τ̂ & φ₂
  ─────────────────────────────────────────────────────    if s ∈ φ₂ or AV(φ₂) ≠ ∅
        Γ̂ ⊢_ES handle s as e₁ in e₂ : τ̂ & φ₁ ∪ (φ₂ \ {s})
  ```
  where `s ∈ φ₂` means `{s} ⊆ φ₂` and `AV(φ₂)` is the set of annotation variables in `φ₂` (`[derived]`: sound,
  because when `AV(φ₂) = ∅` and `s ∉ φ₂`, `φ₂` is invariant under `[ins]` substitutions so `e₂` can never raise
  `s` and dead handler `e₁` is never evaluated!). `■`
- Citation: [PPA Exercise 5.14, p. 362] (book p. 362; PDF p. 379)

### Exercise 5.15 — Generalising Table 5.10 rules to type-scheme conclusions `σ̂`
- Statement: Change `[let]` in `Table 5.10` to:
  ```text
  Γ̂ ⊢_ES e₁ : σ̂₁ & φ₁    Γ̂[x ↦ σ̂₁] ⊢_ES e₂ : σ̂₂ & φ₂
  ──────────────────────────────────────────────────────
          Γ̂ ⊢_ES let x = e₁ in e₂ : σ̂₂ & φ₁ ∪ φ₂
  ```
  perform analogous changes in `[if]`, `[raise]`, `[handle]`, and `[sub]` (defining scheme ordering `σ̂ ≤ σ̂'`;
  printed `τ̂ ≤ τ̂'` on p. 363, finding F-U5b-13), and determine whether the new system is strictly more powerful
  than `Table 5.10` (Hint: consider where `[gen]` and `[ins]` can be applied in `Table 5.10`; `[derived]`: for
  prenex schemes `∀ζ⃗. τ̂` without higher-rank arrows, `[ins]` before `[if]`/`[let]`/`[handle]` followed by a
  final `[gen]` over fresh non-escaping variables derives the same prenex schemes!). `■`
- Citation: [PPA Exercise 5.15, p. 362] (book p. 362; PDF p. 379); [PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380)

### [U5b:EX-ocr] OCR Erasure Audit Summary (PDF pp. 336–380)
- Statement: Eleven formal displays and table fragments in Unit 5b are erased or severely corrupted in the
  `pdftotext` OCR layer of `ppa.pdf` and are restored verbatim in this shard from rendered page images:
  1. `§5.4.1` (`p. 320`): all 3 store SOS rules for `!ξ`, `ξ := e`, and `e₁ ; e₂` completely erased
     [PPA §5.4.1, p. 320] (book p. 320; PDF p. 337).
  2. `Table 5.9` (`p. 322`): `[fn]` rule and `[deref]` side condition `if Γ̂(x) = ref_{π₁, ···, π_n} τ̂` erased
     [PPA Table 5.9, p. 322] (book p. 322; PDF p. 339).
  3. `§5.4.1` (`p. 324`): reflexivity `τ̂ ≤ τ̂` and arrow subtyping rule erased
     [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341).
  4. `Table 5.10` (`p. 328`) & `p. 329`: `[fn]` in Table 5.10 and `τ̂ ≤ τ̂'` rules on p. 329 erased
     [PPA Table 5.10, p. 328] (book p. 328; PDF p. 345); [PPA §5.4.2, p. 329] (book p. 329; PDF p. 346).
  5. `§5.4.3` (`p. 332`, `p. 336`): transition `ρ ⊢ ⟨ee, ς⟩ → ⟨v, ς'⟩` mangled and `Example 5.32` arrow display
     erased [PPA §5.4.3, p. 332] (book p. 332; PDF p. 349); [PPA Example 5.32, p. 336] (book p. 336; PDF p. 353).
  6. `Table 5.12` (`p. 337`): `[fn]` premise, `[app]` conclusion, `[let]` conclusion, and `[op]` premises erased
     [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354).
  7. `Table 5.13` (`p. 338`): rule labels `[gen₁]`, `[gen₂]`, `[ins₁]`, `[ins₂]` erased
     [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355).
  8. `Table 5.14` (`p. 341`) & `p. 342`: `v₁ op v₂ → v if v₁ op v₂ = v`, `e₁ → e₂`, and `(e₁₀ → e₂₀)` rule erased
     [PPA Table 5.14, p. 341] (book p. 341; PDF p. 358); [PPA §5.5.1, p. 342] (book p. 342; PDF p. 359).
  9. `Table 5.16` (`p. 346`): `[fn]` rule erased [PPA Table 5.16, p. 346] (book p. 346; PDF p. 363).
  10. `Table 5.18` (`p. 348`): **9 of the 22** behaviour ordering rules/axioms (`φ ⊑ φ`, `rec` congruence, both
      `;`-associativity axioms, both right-distributivity axioms, and all 3 `+` upper-bound/idempotence axioms)
      completely erased [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365).
  11. `Exercise* 5.4` (`p. 359`): formula body `ρ̃, C̃; Γ̂ ⊢_CFA e : τ̂` of display `(5.2)` completely erased
      [PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376).
- Citation: [PPA §5.4.1, p. 320] (book p. 320; PDF p. 337); [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365); [PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376)

### Findings (Exercises)
- F-U5b-13 (`[Source Erratum — Monotype vs Scheme Subtyping in Exercise 5.15, Unbraced LAnn & Subscript Details]`):
  `Exercise 5.15` (`pp. 362–363`) lifts `Table 5.10` conclusions (including `[sub]`) from `τ̂` to type schemes
  `σ̂`, then writes `"do not forget to define the meaning of τ̂ ≤ τ̂'"` on p. 363 instead of `σ̂ ≤ σ̂'` (`τ̂ ≤ τ̂'`
  was already defined on p. 329); `Exercise 5.5` (`p. 360`) writes subscript `⊥_{τ̂₀}` while defining it as the
  least element of `Typê[τ₀]` (`τ₀ = ⌊τ̂₀⌋`, independent of annotations in `τ̂₀`); `Exercise 5.6` (`p. 360`)
  writes `ψ ::= ℓ | ψ₁ ∪ ψ₂ | ∅` without braces around `ℓ` while writing `{1}` on the arrow below; and
  `Exercise 5.9` (`p. 361`) prints `"differs form"` (`"form"` for `"from"`).
  [PPA Exercise 5.5, p. 360] (book p. 360; PDF p. 377); [PPA Exercise 5.6, p. 360] (book p. 360; PDF p. 377);
  [PPA Exercise 5.9, p. 361] (book p. 361; PDF p. 378); [PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380)
- F-U5b-14 (`[PDF OCR Text-Layer Rule & Axiom Erasures]`): Across PDF pp. 336–380, `ppa.pdf`'s OCR layer drops
  21 inference rules/axioms and numbered formula `(5.2)` catalogued in `[U5b:EX-ocr]`, plus corrupts `ς` to
  `c;`/`<;`, `ϱ` to `e`/`[!`, `''1` to `"1`, and `∅` to `0`.
  [PPA §5.4.1, p. 320] (book p. 320; PDF p. 337); [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354);
  [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365)

### Projections (Exercises)
- cs_theory:
  1. **Why contravariant subtyping breaks unconstrained Moore-family principal types (`Exercise 5.9`)**:
     flipping arrow domains from §5.2's covariant `⊑` to §5.4's contravariant `≤` preserves complete-lattice
     structure on `Typê[τ]` while destroying `Proposition 5.12` (`⨅` of valid typings of `fn_X x => x` is
     unsound `(int →^⊤ int) →^{\{X\}} (int →^∅ int)`), proving from first principles why principal subtyped
     polymorphism requires *constrained type schemes* `∀ζ⃗ [C]. τ̂` `[derived]`.
  2. **`[external: Reynolds/Wadler parametricity]` non-termination (`Exercise* 5.10`)**: `α_x → α₀` (`α_x ≠ α₀`)
     has zero total inhabitants in pure `FUN`, turning `𝒲_UL` into a lightweight sound divergence detector.
- swe_architecture: `Exercise 5.13`'s **two-step proof normalisation** (folding standalone `[sub]` into axioms
  and `[fn]`/`[fun]` arrows) is the universal recipe for converting declarative type-and-effect specifications
  into backtrack-free syntax-directed constraint generators (`Theorem 5.21` pattern).
- practical_debugging: `Exercise 5.14` (`s ∉ φ₂ ∧ AV(φ₂) = ∅`) isolates the exact bug in dead-catch-block
  linters: warning that `handle s as e₁ in e₂` is unreachable whenever `s ∉ φ₂` is **unsound** on generic
  functions if `AV(φ₂) ≠ ∅` (since a polymorphic callback variable `'1 ∈ AV(φ₂)` can instantiate to `{s}` at
  call sites!).
- cyber: `Exercise 5.5` (`φ = ∅ ⇒ ⊥_{τ̂₀}`) and `Exercise 5.6` (`ψ ∈ LAnn` call-site tracking) tighten
  post-call dead-code pruning and bidirectional caller/callee provenance graphs for reachability-gated
  vulnerability triage, reducing false-positive `[external: taint]` alerts across unreachable dispatch sites.

---

## Gotcha Ledger

- G-U5b-01: Top 4 lines of book p. 319 complete §5.3.4 (`Corollary 5.23`: `dom(θ_A) = AV(C)` and `θ ⊒ θ_A`, counted in Unit 5a) immediately above §5.4 *Effects*, and Chapter 5 ends on book p. 363 (`PDF p. 380`, constant offset `+17`; book p. 364 is an absent blank verso, with `5` Mini Projects `5.1–5.5` and `15` Exercises `5.1–5.15`). [PPA §5.3.4, p. 319] (book p. 319; PDF p. 336); [PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380)
- G-U5b-02: In effect systems (`Tables 5.9, 5.10, 5.16`), `[fn]` and `[fun]` emit empty immediate effect (`∅` or `Λ`) and place the body's latent effect `φ₀` onto the arrow `τ̂_x →^{φ₀} τ̂₀` until `[app]` discharges `φ₀` (`Remark.` p. 325 contrasts Effect Systems in §5.4 against Annotated Type Systems in §5.1). [PPA Table 5.9, p. 322] (book p. 322; PDF p. 339); [PPA §5.4.1, p. 325] (book p. 325; PDF p. 342)
- G-U5b-03: In `Table 5.9` `[new]`, allocation effect `{new π}` is **not** masked upon exiting the lexical scope `e₂` of `new_π x := e₁ in e₂` (`(φ₁ ∪ φ₂ ∪ {new π})`), intentionally exposing heap/memory allocation inside functions (unlike `Table 5.13` `[region]`, which masks local `{put ϱ}`/`{get ϱ}` via `Observe`). [PPA §5.4.1, p. 319] (book p. 319; PDF p. 336); [PPA Table 5.9, p. 322] (book p. 322; PDF p. 339); [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355)
- G-U5b-04: In §5.4.1's store-passing Natural Semantics (`p. 320`), `new_π` allocates `ξ ∉ dom(ς₂)` and substitutes `e₂[x ↦ ξ]` (producing runtime `!ξ` and `ξ := e` outside p. 319's surface `Var`-only syntax), while assignment `ξ := e` returns the *assigned* value `v` (not `()`). [PPA §5.4.1, p. 320] (book p. 320; PDF p. 337); [PPA §5.4.1, p. 321] (book p. 321; PDF p. 338)
- G-U5b-05: Shape-conformant subtyping `τ̂ ≤ τ̂'` (`⌊τ̂₁⌋ = ⌊τ̂₂⌋`) is **contravariant** in arrow domains (`τ̂'₁ ≤ τ̂₁`), **covariant** in arrow effects/codomains and point sets (`ϖ ⊆ ϖ'`, `r ⊆ r'`), and **strictly invariant** (`τ̂ ≤ τ̂' ∧ τ̂' ≤ τ̂`) in mutable reference payloads `ref_ϖ τ̂` (`p. 324`) and channel payloads `τ̂ chan r` (`p. 347`). [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341); [PPA §5.5.1, p. 347] (book p. 347; PDF p. 364)
- G-U5b-06: Omitting *both* subeffecting and subtyping from `Table 5.9` breaks conservative extension over `Table 5.1`, whereas retaining *either* subeffecting or subtyping (or `[sub]` combining both) preserves conservative extension. [PPA §5.4.1, p. 325] (book p. 325; PDF p. 342)
- G-U5b-07: Equipping §5.1 `Typê[τ]` with contravariant arrow ordering `≤` (`Exercise 5.9`) yields a complete lattice **yet breaks `Proposition 5.12`'s Moore-family property**: meeting all valid ground typings `(int →^φ int) →^{\{X\}} (int →^φ int)` of `fn_X x => x` under `≤` produces the unsound non-typing `(int →^⊤ int) →^{\{X\}} (int →^∅ int)` `[derived]`. [PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367); [PPA Exercise 5.9, p. 361] (book p. 361; PDF p. 378)
- G-U5b-08: In §5.4.2 Natural Semantics, `raise s` belongs to `Val`, so `handle s as e₁ in e₂`'s rule `v₂ ≠ raise s` automatically propagates distinct exceptions `raise s'` (`s' ≠ s`) outward while the third rule propagates any exception raised by handler `e₁`. [PPA §5.4.2, p. 326] (book p. 326; PDF p. 343); [PPA §5.4.2, p. 327] (book p. 327; PDF p. 344)
- G-U5b-09: In `Table 5.10` (`§5.4.2`), syntactic subtraction `φ \ {s}` MUST set **`β \ {s} = β`** (`pp. 329–330`) on uninstantiated effect variables `β`: simplifying `β \ {s}` to `∅` unsoundly erases untrapped exceptions `s' ≠ s` when `[ins]` later substitutes `β ↦ {s, s'}`. [PPA §5.4.2, p. 329] (book p. 329; PDF p. 346); [PPA §5.4.2, p. 330] (book p. 330; PDF p. 347)
- G-U5b-10: `Table 5.10` `[handle]` unions handler effect `φ₁` unconditionally (`φ₁ ∪ (φ₂ \ {s})`); `Exercise 5.14` (`p. 362`) can safely drop `φ₁` **only** when *both* `s ∉ φ₂` *and* `AV(φ₂) = ∅` (if `AV(φ₂) ≠ ∅`, a variable in `φ₂` may still instantiate to `{s}`). [PPA Table 5.10, p. 328] (book p. 328; PDF p. 345); [PPA Exercise 5.14, p. 362] (book p. 362; PDF p. 379)
- G-U5b-11: Polymorphic `[gen]` (`Tables 5.10, 5.13, 5.17`) MUST forbid quantifying variables free in **either `Γ̂` OR `φ`**; `Example 5.36` proves checking only `ζ_i ∉ FV(Γ̂)` generalises `'a` in `channel_A : 'a chan {A} & 'a chan {A}` and unsafely types mixed `int`/`bool` sends on one channel. [PPA Table 5.10, p. 328] (book p. 328; PDF p. 345); [PPA Example 5.36, p. 346] (book p. 346; PDF p. 363); [PPA Example 5.36, p. 347] (book p. 347; PDF p. 364)
- G-U5b-12: When effects contain types (*general effects*, `p. 352`, §5.5), two-stage type-then-effect inference fails and syntactic `FV(Γ̂) ∪ FV(φ)` is insufficient during constraint solving: `[gen]` must exclude the entire **downwards closure** of `FV(Γ̂) ∪ FV(φ)` wrt the constraint set. [PPA Chapter 5 Concluding Remarks, p. 352] (book p. 352; PDF p. 369)
- G-U5b-13: In §5.4.3 Region Inference (`p. 333`, `Tables 5.11–5.12`), **all** ordinary runtime values (including `int` and `bool` constants!) are boxed `(rn, o) ∈ RName × Offset`: `[con]` and `[fn]` emit `{put r}`, `[if]` emits `{get r₀}`, `[op]` emits `{get r₁, get r₂, put r}`, and `[app]` emits `{get r₁}` to read the closure at `r₁` in addition to `φ₀ ∪ β₀`. [PPA §5.4.3, p. 333] (book p. 333; PDF p. 350); [PPA Table 5.11, p. 334] (book p. 334; PDF p. 351); [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354)
- G-U5b-14: `Scheme_RI` (`p. 335`) strictly separates *ordinary* schemes `∀α⃗, β⃗. τ̂` (`[ins₁]`: invisible in `ee`) from *compound* schemes `∀α⃗, β⃗, [ϱ⃗]. τ̂` (`[ins₂]`: emits `ee[θ ϱ⃗] at r'` with `{get r, put r'}` because `Table 5.11` `[app]` cannot invoke `⟨ϱ⃗, x, ee₀, ρ⟩` before `[place]`); hence `∀(), (), []. τ̂` MUST be written `∀[]. τ̂` rather than `τ̂`. [PPA Table 5.11, p. 334] (book p. 334; PDF p. 351); [PPA §5.4.3, p. 335] (book p. 335; PDF p. 352); [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355)
- G-U5b-15: `Table 5.12` `[fun]` restricts polymorphic recursion to effects and regions `(∀β⃗, [ϱ⃗]. τ̂) @ r` (**excluding type variables `α⃗`**, generalised only afterward by `[gen₂]`), because type-polymorphic recursion is undecidable (`p. 336`), and even on `β⃗, ϱ⃗`, `Algorithm R` (`[174]`, `[external: Tofte–Birkedal]`) is syntactically sound **not** syntactically complete (`p. 352`). [PPA §5.4.3, p. 336] (book p. 336; PDF p. 353); [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354); [PPA Chapter 5 Concluding Remarks, p. 352] (book p. 352; PDF p. 369)
- G-U5b-16: Both conjuncts in `Table 5.13` `[region]` (`φ' = Observe(Γ̂, τ̂, r)(φ)` **and** `ϱ⃗ occurs in φ but not in φ'`) are required: `Observe` (`pp. 338–339`) filters only atoms present in `φ`, so omitting "`ϱ⃗` occurs in `φ`" would let `x : int @ ϱ₁ & ∅` (`φ = φ' = ∅`) wrap `letregion ϱ₁ in x` around an escaping region `[derived]`. [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355); [PPA §5.4.3, p. 339] (book p. 339; PDF p. 356)
- G-U5b-17: Section 5.4.3 invokes `τ̂ ≤ τ̂'` in `Table 5.13` `[sub]` (`p. 338`) without stating the arrow rule on `Type_RI` (where `r₁, r₂` in `(τ̂₁ @ r₁) →^{β.φ} (τ̂₂ @ r₂)` must stay invariant `r₁ = r'₁, r₂ = r'₂`), writes `σ̂` for `σ̂ @ r` in `Table 5.12` `[var]` (`p. 337`), and prints `dom(ς)` for `dom(ς₁)` in `Table 5.11` `[region]` (`p. 334`). [PPA Table 5.11, p. 334] (book p. 334; PDF p. 351); [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354); [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355)
- G-U5b-18: Section 5.5.1 replaces big-step semantics with small-step capture-free evaluation-context SOS (`Tables 5.14–5.15`), enforces **synchronous rendezvous** between distinct processes `p₁ ≠ p₂` in `[comm]`, and deliberately omits `Observe`-style masking so all concurrent communications remain globally visible (`p. 349`). [PPA Table 5.14, p. 341] (book p. 341; PDF p. 358); [PPA Table 5.15, p. 343] (book p. 343; PDF p. 360); [PPA §5.5.1, p. 349] (book p. 349; PDF p. 366)
- G-U5b-19: In `Table 5.18` (`p. 348`, 22 rules/axioms), send `r!τ̂` is **covariant** in `τ̂` (`τ̂₁ ≤ τ̂₂`), receive `r?τ̂` is **contravariant** in `τ̂` (`τ̂₂ ≤ τ̂₁`), `τ̂ chan r` is **invariant** in `τ̂`, and `rec β.φ` requires positive `β` occurrences (outside contravariant `r?τ̂` / invariant `chan`) for monotone fixed points `[derived]`. [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365)
- G-U5b-20: Behaviour sequencing `;` in `Table 5.18` (`p. 348`) is associative with identity `Λ`, non-commutative, non-idempotent, and distributes over `+` **only from the right** (`(φ₁ + φ₂); φ₃ ≡ (φ₁; φ₃) + (φ₂; φ₃)`); left-distributivity `φ₁; (φ₂ + φ₃)` is omitted to preserve `[external: branching-time deadlock]` distinctions `[derived]`. [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365)
- G-U5b-21: `Examples 5.35` (`p. 345`) and `5.37` (`p. 349`) print bare `C` instead of singleton `{C}` in `'a chan C` and `C!'a` (violating `r ::= {π} | ϱ | r₁ ∪ r₂ | ∅` on `p. 344` and `Table 5.17` `[chan]`), and `Example 5.35` (`p. 345`) has an unmatched `(` in `pipe`'s type scheme. [PPA §5.5.1, p. 344] (book p. 344; PDF p. 361); [PPA Example 5.35, p. 345] (book p. 345; PDF p. 362); [PPA Example 5.37, p. 349] (book p. 349; PDF p. 366)
- G-U5b-22: `Concluding Remarks` (`p. 350` line 15) mis-cites `"Section 5.1"` instead of `"Section 5.4"` for shape-conformant subtyping; adding contravariant arrow subtyping (`Exercise 5.9`) + `(5.2)` (`Exercise* 5.4`) equates Chapter 5 CFA with Chapter 3 `0-CFA` on typed programs (`U8`). [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341); [PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367); [PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376)
- G-U5b-23: `Exercise 5.13` (`p. 362`) proves two-pass *proof normalisation* absorbing subeffecting `[sub]` solely into axioms and `[fn]`/`[fun]` abstractions, explaining why §5.1 needed no standalone `[sub]` rule. [PPA Exercise 5.13, p. 362] (book p. 362; PDF p. 379)
- G-U5b-24: `Mini Project 5.4` (`pp. 355–356`) embeds §3.5.2 monotone structures into `Table 1.2`-style subeffecting base types (`S ⊑ D` BTA and `C₁ ⊑ ··· ⊑ C_k` security clearance), requiring `ACC` for termination without widening. [PPA Mini Project 5.4, p. 355] (book p. 355; PDF p. 372); [PPA Mini Project 5.4, p. 356] (book p. 356; PDF p. 373)
- G-U5b-25: `Mini Project 5.5` (`pp. 357–358`) requires `[external: abelian-group]` equational laws on `scale` (`meter.feet = feet.meter`, `scale.scale^{-1} = unit`) stronger than `UCAI`, forbids `*` and `/` unless both operands have `BASE none`, and forbids `+` on two non-`none` `[external: affine]` bases (leaving `undefined otherwise` implicit on `+` while printing it on `-`). [PPA Mini Project 5.5, p. 357] (book p. 357; PDF p. 374); [PPA Mini Project 5.5, p. 358] (book p. 358; PDF p. 375)
- G-U5b-26: `Exercise 5.15` (`p. 363`) misprints `τ̂ ≤ τ̂'` where scheme subtyping `σ̂ ≤ σ̂'` is needed, and `ppa.pdf`'s OCR erases 3 store rules on p. 320, `[fn]` in `Tables 5.9, 5.10, 5.16`, half of `Table 5.12`, `v₁ op v₂ → v` in `Table 5.14`, 9 of 22 rules in `Table 5.18`, subtyping displays on pp. 324 and 329, and display `(5.2)` on p. 359. [PPA §5.4.1, p. 320] (book p. 320; PDF p. 337); [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365); [PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376); [PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380)
