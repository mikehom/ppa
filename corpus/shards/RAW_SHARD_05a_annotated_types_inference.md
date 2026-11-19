<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 5a (Chapter 5 §§5.1-5.3). -->

# RAW_SHARD_05a — Chapter 5 Annotated Type Systems, Soundness, and Inference for CFA (Unit 5a)

Source: *Principles of Program Analysis* (Nielson, Nielson, Hankin), corrected 2nd printing, 2005.
Scope: Chapter 5 opening, §5.1 Control Flow Analysis (§5.1.1–§5.1.2), §5.2 Theoretical Properties
(§5.2.1–§5.2.3), and §5.3 Inference Algorithms (§5.3.1–§5.3.4), spanning book pages 283–319 / PDF pages
300–336 and ending after the 4-line carryover of §5.3.4 at the top of book p. 319 immediately above the
§5.4 Effects heading. Effects (§5.4: Side Effect Analysis, Exception Analysis, Region Inference),
Behaviours (§5.5: Communication Analysis), Concluding Remarks, Mini Projects 5.1–5.5, Figures 5.1–5.2,
Tables 5.9–5.18, and Exercises 5.1–5.15 belong to Unit 5b.

Coordinates: PDF page = book page + 17 throughout Chapter 5 (no blank verso precedes p. 283 after p. 282 of
Chapter 4). Section starts in Unit 5a: Chapter 5 opening and §5.1 on p. 283 (§5.1.1 on p. 284, §5.1.2 on
p. 287), §5.2 on p. 291 (§5.2.1 on p. 292, §5.2.2 on p. 294, §5.2.3 on p. 297), and §5.3 and §5.3.1 on
p. 300 (§5.3.2 on p. 306, §5.3.3 on p. 312, §5.3.4 on p. 317, concluding at the top of p. 319 before §5.4)
[PPA §5.1, p. 283] (book p. 283; PDF p. 300).

Conventions:

- Every source reference pairs a strict inline locator token with its book/PDF coordinate companion, for
  example [PPA §5.1, p. 283] (book p. 283; PDF p. 300), [PPA Table 5.1, p. 285] (book p. 285; PDF p. 302),
  or [PPA Preface, p. VI] (book p. VI; PDF p. 6).
- Book-numbered items preserve their exact printed kind word and number (`5.1`–`5.23` in one shared
  per-chapter sequence of 13 Examples, 3 Facts, 3 Theorems, 2 Lemmas, 1 Proposition, and 1 Corollary,
  plus Tables `5.1`–`5.8` and equation display `(5.1)`; there are `0` numbered Figures and `0` numbered
  Definitions in §§5.1–5.3). Unnumbered definitions, syntactic grammars, proof blocks, and the printed
  `Analogy.` block (pp. 304–305) carry non-book identifiers `[U5a:<section>-<letter>]`.
- Every formula, rule, algorithm, table, and example derivation is transcribed directly from rendered page
  images (PDF pages 300–336) rather than the OCR text layer, which drops the labelled expression and 5-column
  `Ĉ(ℓ)` comparison table in Example 5.4 (p. 289), the `[con]` axiom and `[if₁]`/`[if₂]` labels in Table 5.4
  (p. 292), the arrow clause in Table 5.6 (p. 305), the `φ ∈ SAnn` BNF line below Table 5.7 (p. 307), the
  intersection displays in Lemma 5.22 (p. 318), and wide hats across `τ̂`, `Γ̂`, `Typê`, and `TEnv̂`.
- Terms absent from the book carry `[external]`. Deductions, worked counterexamples, and complexity
  refinements not printed in the text carry `[derived]`. Source misprints and internal tensions are
  transcribed verbatim as printed and logged under `Findings` (`F-U5a-NN`).
- Notation: `e ∈ Exp` expressions (unlabelled except for abstraction-site program points `π ∈ Pnt` on
  `fn_π` and `fun_π`); `c ∈ Const` constants; `op ∈ Op` syntactic binary operators and bold `**op**`
  semantic binary operations; `f, x ∈ Var` variables; `τ ∈ Type` underlying types (`int`, `bool`, `τ₁ → τ₂`)
  with constant types `τ_c` and operator types `(τ¹_op, τ²_op) → τ_op`; `Γ ∈ TEnv` list-structured type
  environments (`[]` or `Γ[x ↦ τ]`) with `dom(Γ)`, rightmost lookup `Γ(x)`, and restriction `Γ | X`;
  `Γ ⊢_UL e : τ` underlying typing judgement (Table 5.1); `φ ∈ Ann` concrete annotations (`{π}`, `φ₁ ∪ φ₂`,
  `∅`) modulo `UCAI` set equality (Table 5.3); `τ̂ ∈ Typê` annotated types (`int`, `bool`, `τ̂₁ --φ--> τ̂₂`)
  and `Γ̂ ∈ TEnv̂` annotated environments; `⌊τ̂⌋` and `⌊Γ̂⌋` underlying-type erasure; `Γ̂ ⊢_CFA e : τ̂` CFA
  typing judgement with built-in subeffecting `{π} ∪ φ` (Table 5.2); `v ∈ Val` closed values (`c` or closed
  `fn_π x => e₀`); `e₁[x ↦ e₂]` capture-free closed substitution; `⊢ e ⟶ v` environment-free Natural
  Semantics (Table 5.4); `⊑` / `⊆` covariant fibre ordering on `Typê[τ]` and `JUDG_CFA[Γ ⊢_UL e : τ]` with
  meet `⊓` / `⋂`; `α ∈ TVar` (`'a, 'b, ...`) type variables; `τ ∈ AType` augmented underlying types;
  `θ : TVar →_fin AType` finite substitutions (`id`, `θ₁ ∘ θ₂`); `𝒲_UL` and `𝒰_UL` underlying inference
  and unification (Tables 5.5–5.6); `β ∈ AVar` (`'1, '2, ...`) annotation variables; `τ̂ ∈ SType` simple
  types (`τ̂₁ --β--> τ̂₂`) and `φ ∈ SAnn` simple annotations; `𝒰_CFA` and `𝒲_CFA` simple-type unification
  and CFA inference (Tables 5.7–5.8); `C` finite constraint sets of inclusions `β ⊇ φ` (`AV(C)` annotation
  variables); `θ_T`, `θ_A` (`θ_A ⊨ C`), and `θ_G = θ_A ∘ θ_T` ground validations; `■` and `□` as printed.

## Chapter 5 Opening

Context: Chapter 5 (*Type and Effect Systems*) opens on p. 283 above the §5.1 heading with the typed-language
prerequisite and the three-stage progression from annotated types to effect systems and concurrent
behaviours [PPA Chapter 5, p. 283] (book p. 283; PDF p. 300).

### [U5a:5.0-a] Typed-language prerequisite and plan of Chapter 5 (unnumbered remark)
- Statement: Whereas the Data Flow, Control Flow, and Abstract Interpretation frameworks of Chapters 2–4
  apply equally to typed and untyped languages, *Type and Effect Systems* **demand** that the target
  language is typed, because the syntax of types itself serves as the carrier for program-analysis
  properties (continuing the overview in §1.6 [PPA §1.6, p. 20] (book p. 20; PDF p. 40)):
  1. Present an *Annotated Type System* for Control Flow Analysis (§5.1), establish its semantic soundness
     and Moore-family properties (§5.2), and construct a sound and complete inference algorithm (§5.3).
  2. Generalise in §5.4 (Unit 5b [PPA §5.4, p. 319] (book p. 319; PDF p. 336)) to Type and Effect Systems
     with explicit subtyping, `let`-polymorphism, and polymorphic recursion across *Side Effect Analysis*,
     *Exception Analysis*, and *Region Inference*.
  3. Generalise in §5.5 (Unit 5b [PPA §5.5, p. 339] (book p. 339; PDF p. 356)) to structured causal
     annotations (*behaviours*) for *Communication Analysis* of concurrent programs.
- Citation: [PPA Chapter 5, p. 283] (book p. 283; PDF p. 300)

### Projections (Chapter 5 Opening)
- cs_theory: Type and Effect Systems internalise static analysis inside `[external: Curry–Howard]` type structure,
  trading untyped universality (Chapters 2–4) for syntax-directed modularity over
  open higher-order terms.
- swe_architecture: Piggybacking flow/effect metadata onto existing compiler typecheckers (`Typê` erasing to
  `Type` via `⌊·⌋`) avoids maintaining a separate AST/CFG front-end and naturally produces modular function
  summaries at interface boundaries `[external]`.
- practical_debugging: Any untyped idiom, dynamic cast, or `[external: FFI]` boundary violating the underlying
  type system `⊢_UL` falls outside Chapter 5's analysis domain (`𝒰_UL` / `𝒰_CFA` rejects `fn_X x => x x` via the
  occurs check), so type errors must be triaged before inspecting flow annotations.
- cyber: Attaching security/`[external: taint]`/`[external: capability]` qualifiers to underlying types
  (`[external: Volpano–Smith–Irvine security type systems, Jif, FlowCaml]`) inherits compositional verification
  on well-typed code, provided unsafe casts/`[external: FFI]` boundaries do not violate underlying type soundness.

## 5.1 Control Flow Analysis

Context: Section 5.1 adapts `FUN` so only function abstractions carry program points `π ∈ Pnt`, defines the
monomorphic underlying type system `Γ ⊢_UL e : τ` (Table 5.1), enriches function arrows with set annotations
`τ̂₁ --φ--> τ̂₂` and built-in subeffecting `{π} ∪ φ` in `Γ̂ ⊢_CFA e : τ̂` (Table 5.2), axiomatises `UCAI`
annotation equality (Table 5.3), and proves conservative extension over `⊢_UL` (Fact 5.6)
[PPA §5.1, p. 283] (book p. 283; PDF p. 300).

### [U5a:5.1-a] Syntax of `FUN` with abstraction-site program points (`Exp`, `Pnt`)
- Statement: Chapter 5 reuses the functional language `FUN` of Chapter 3
  [PPA §3.1, p. 142] (book p. 142; PDF p. 160) (noting imperative `WHILE` can also be treated via Type and
  Effect Systems as in §1.6 [PPA §1.6, p. 20] (book p. 20; PDF p. 40)), but drops universal subexpression
  labels `ℓ ∈ Lab` and the separate category `Term`: because annotated types now carry subexpression flow
  information, only `fn_π` and `fun_π` carry *program points* `π ∈ Pnt` naming function definitions:
  ```text
  e    ∈ Exp     expressions
  c    ∈ Const   constants (unspecified; includes truth values true, false)
  op   ∈ Op      binary operators (unspecified; includes arithmetic, boolean, relational operators)
  f, x ∈ Var     variables (countable set assumed given)
  π    ∈ Pnt     program points (unspecified; name function abstractions)

  e ::= c
      | x
      | fn_π x => e₀
      | fun_π f x => e₀
      | e₁ e₂
      | if e₀ then e₁ else e₂
      | let x = e₁ in e₂
      | e₁ op e₂
  ```
- Side conditions: Throughout Chapter 5 (§5.2.1, p. 293), `fun_π f x => e₀` is assumed to use distinct bound
  variables `f ≠ x`.
- Citation: [PPA §5.1, p. 283] (book p. 283; PDF p. 300); [PPA §5.1, p. 284] (book p. 284; PDF p. 301)

### Example 5.1 — Identity self-application with abstraction points
- Statement: The expression `(fn x => x) (fn y => y)` of Chapters 1 and 3 (matching Example 1.5
  [PPA Example 1.5, p. 23] (book p. 23; PDF p. 43)) is written:
  ```text
  (fn_X x => x) (fn_Y y => y)
  ```
  `■`
- Citation: [PPA Example 5.1, p. 284] (book p. 284; PDF p. 301)

### Example 5.2 — Diverging recursive program `loop`
- Statement: The program `loop` of Example 3.2 [PPA Example 3.2, p. 143] (book p. 143; PDF p. 161) is written:
  ```text
  let g = (fun_F f x => f (fn_Y y => y))
  in g (fn_Z z => z)
  ```
  `g` is first applied to `fn_Z z => z`, ignores its formal parameter `x`, and calls itself recursively via
  `f` on `fn_Y y => y` forever. `■`
- Citation: [PPA Example 5.2, p. 284] (book p. 284; PDF p. 301)

### 5.1.1 The Underlying Type System

### [U5a:5.1.1-a] Underlying types (`Type`), base-type operator assumption, and list environments (`TEnv`)
- Statement:
  ```text
  τ ∈ Type   types               τ ::= int | bool | τ₁ → τ₂
  Γ ∈ TEnv   type environments   Γ ::= [] | Γ[x ↦ τ]
  ```
  - **Constants and binary operators**: `int` and `bool` are the only base types. Each `c ∈ Const` has a
    predefined base type `τ_c ∈ {int, bool}` (e.g. `τ_true = bool`, `τ_7 = int`), and each `op ∈ Op` has
    base-type operand and result types `τ¹_op, τ²_op, τ_op ∈ {int, bool}` (e.g. `≤` has `τ¹_≤ = int`,
    `τ²_≤ = int`, `τ_≤ = bool`).
  - **List environments with rightmost-wins lookup**: `dom(Γ) = {x | Γ contains [x ↦ ⋯]}`; `Γ(x) = τ` iff
    `x ∈ dom(Γ)` and the *rightmost* binding for `x` in `Γ` is `[x ↦ τ]`; `Γ | X` deletes entries `[x ↦ ⋯]`
    with `x ∉ X`; `[x ↦ τ]` abbreviates `[][x ↦ τ]`.
- Citation: [PPA §5.1.1, p. 284] (book p. 284; PDF p. 301); [PPA §5.1.1, p. 285] (book p. 285; PDF p. 302); [PPA §5.1.1, p. 286] (book p. 286; PDF p. 303)

### Table 5.1 — The Underlying Type System
- Statement: Syntax-directed underlying typing judgement `Γ ⊢_UL e : τ`:
  ```text
  [con]  Γ ⊢_UL c : τ_c

  [var]  Γ ⊢_UL x : τ                                   if Γ(x) = τ

         Γ[x ↦ τ_x] ⊢_UL e₀ : τ₀
  [fn]   ---------------------------------
         Γ ⊢_UL fn_π x => e₀ : τ_x → τ₀

         Γ[f ↦ τ_x → τ₀][x ↦ τ_x] ⊢_UL e₀ : τ₀
  [fun]  -----------------------------------------
         Γ ⊢_UL fun_π f x => e₀ : τ_x → τ₀

         Γ ⊢_UL e₁ : τ₂ → τ₀    Γ ⊢_UL e₂ : τ₂
  [app]  ----------------------------------------
         Γ ⊢_UL e₁ e₂ : τ₀

         Γ ⊢_UL e₀ : bool    Γ ⊢_UL e₁ : τ    Γ ⊢_UL e₂ : τ
  [if]   ----------------------------------------------------
         Γ ⊢_UL if e₀ then e₁ else e₂ : τ

         Γ ⊢_UL e₁ : τ₁    Γ[x ↦ τ₁] ⊢_UL e₂ : τ₂
  [let]  ------------------------------------------
         Γ ⊢_UL let x = e₁ in e₂ : τ₂

         Γ ⊢_UL e₁ : τ¹_op    Γ ⊢_UL e₂ : τ²_op
  [op]   ----------------------------------------
         Γ ⊢_UL e₁ op e₂ : τ_op
  ```
- Side conditions:
  - `⊢_UL` is *nondeterministic* (`[fn]` and `[fun]` guess bound-variable types; e.g. `[] ⊢_UL fn_X x => x : τ → τ`
    for every `τ ∈ Type`).
  - `[let]` is **monomorphic**: `let x = e₁ in e₂` admits the *exact* same underlying typings as
    `(fn_π x => e₂) e₁` regardless of `π` (polymorphic `let` is deferred to §§5.4–5.5).
- Citation: [PPA Table 5.1, p. 285] (book p. 285; PDF p. 302); [PPA §5.1.1, p. 286] (book p. 286; PDF p. 303)

### Example 5.3 — Underlying typing `[] ⊢_UL loop : τ → τ`
- Statement: For any `τ ∈ Type`, taking `Γ_{fx} = [f ↦ (τ → τ) → (τ → τ)][x ↦ τ → τ]` gives
  `Γ_{fx} ⊢_UL f : (τ → τ) → (τ → τ)` and `Γ_{fx} ⊢_UL fn_Y y => y : τ → τ`, hence
  `[] ⊢_UL fun_F f x => f (fn_Y y => y) : (τ → τ) → (τ → τ)` by `[app]` and `[fun]`; binding `g` via `[let]`
  and applying to `fn_Z z => z : τ → τ` yields `[] ⊢_UL loop : τ → τ`. `■`
- Citation: [PPA Example 5.3, p. 286] (book p. 286; PDF p. 303); [PPA Example 5.3, p. 287] (book p. 287; PDF p. 304)

### 5.1.2 The Analysis

### [U5a:5.1.2-a] Annotations (`Ann`), annotated types (`Typê`, `TEnv̂`), and erasure `⌊·⌋`
- Statement: Annotate each function arrow with `φ ∈ Ann` recording the set of function abstractions `π ∈ Pnt`
  that may reach that arrow:
  ```text
  φ ∈ Ann     annotations                   φ ::= {π} | φ₁ ∪ φ₂ | ∅
  τ̂ ∈ Typê    annotated types               τ̂ ::= int | bool | τ̂₁ --φ--> τ̂₂
  Γ̂ ∈ TEnv̂    annotated type environments   Γ̂ ::= [] | Γ̂[x ↦ τ̂]
  ```
  Finite-set shorthand `{π₁, ..., π_n}` stands formally for `((∅ ∪ {π₁}) ∪ ⋯) ∪ {π_n}`. Underlying-type
  erasure `⌊·⌋` strips all arrow annotations:
  ```text
  ⌊int⌋ = int,    ⌊bool⌋ = bool,    ⌊τ̂₁ --φ--> τ̂₂⌋ = ⌊τ̂₁⌋ → ⌊τ̂₂⌋,    ⌊Γ̂⌋(x) = ⌊Γ̂(x)⌋
  ```
- Citation: [PPA §5.1.2, p. 287] (book p. 287; PDF p. 304)

### Table 5.2 — Control Flow Analysis
- Statement: Syntax-directed CFA typing judgement `Γ̂ ⊢_CFA e : τ̂` with built-in subeffecting `{π} ∪ φ` on
  `[fn]` and `[fun]`:
  ```text
  [con]  Γ̂ ⊢_CFA c : τ_c

  [var]  Γ̂ ⊢_CFA x : τ̂                                         if Γ̂(x) = τ̂

         Γ̂[x ↦ τ̂_x] ⊢_CFA e₀ : τ̂₀
  [fn]   -----------------------------------------
         Γ̂ ⊢_CFA fn_π x => e₀ : τ̂_x --{π}∪φ--> τ̂₀

         Γ̂[f ↦ τ̂_x --{π}∪φ--> τ̂₀][x ↦ τ̂_x] ⊢_CFA e₀ : τ̂₀
  [fun]  ------------------------------------------------------
         Γ̂ ⊢_CFA fun_π f x => e₀ : τ̂_x --{π}∪φ--> τ̂₀

         Γ̂ ⊢_CFA e₁ : τ̂₂ --φ--> τ̂₀    Γ̂ ⊢_CFA e₂ : τ̂₂
  [app]  --------------------------------------------------
         Γ̂ ⊢_CFA e₁ e₂ : τ̂₀

         Γ̂ ⊢_CFA e₀ : bool    Γ̂ ⊢_CFA e₁ : τ̂    Γ̂ ⊢_CFA e₂ : τ̂
  [if]   ----------------------------------------------------------
         Γ̂ ⊢_CFA if e₀ then e₁ else e₂ : τ̂

         Γ̂ ⊢_CFA e₁ : τ̂₁    Γ̂[x ↦ τ̂₁] ⊢_CFA e₂ : τ̂₂
  [let]  ----------------------------------------------
         Γ̂ ⊢_CFA let x = e₁ in e₂ : τ̂₂

         Γ̂ ⊢_CFA e₁ : τ¹_op    Γ̂ ⊢_CFA e₂ : τ²_op
  [op]   ------------------------------------------
         Γ̂ ⊢_CFA e₁ op e₂ : τ_op
  ```
- Citation: [PPA Table 5.2, p. 288] (book p. 288; PDF p. 305)

### Example 5.4 — CFA inference tree and `Ĉ(ℓ)` subexpression table on `(fn_X x => x) (fn_Y y => y)`
- Statement: Writing `τ̂_Y = int --{Y}--> int`, Table 5.2 derives:
  ```text
  [x ↦ τ̂_Y] ⊢_CFA x : τ̂_Y                       [y ↦ int] ⊢_CFA y : int
  -----------------------------------------      ----------------------------
  [] ⊢_CFA fn_X x => x : τ̂_Y --{X}--> τ̂_Y       [] ⊢_CFA fn_Y y => y : τ̂_Y
  ---------------------------------------------------------------------------
                 [] ⊢_CFA (fn_X x => x) (fn_Y y => y) : τ̂_Y
  ```
  The *whole inference tree* is needed to recover full control-flow information (since the root type `τ̂_Y`
  omits `{X}`). Labelling all five subexpressions `((fn_X x => x^1)^2 (fn_Y y => y^3)^4)^5` as in Example
  3.1 [PPA Example 3.1, p. 143] (book p. 143; PDF p. 161) yields the subexpression table (erased in the PDF
  OCR layer and restored from `PDF p. 306`):

  | `ℓ` | `1` | `2` | `3` | `4` | `5` |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | `Ĉ(ℓ)` | `τ̂_Y` | `τ̂_Y --{X}--> τ̂_Y` | `int` | `τ̂_Y` | `τ̂_Y` |

  matching `Ĉ_e` of Example 3.3 [PPA Example 3.3, p. 144] (book p. 144; PDF p. 162), while `ρ̂` is obtained
  by merging the `Γ̂` environments across the inference tree (Exercise 5.4
  [PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376)). `■`
- Citation: [PPA Example 5.4, p. 288] (book p. 288; PDF p. 305); [PPA Example 5.4, p. 289] (book p. 289; PDF p. 306)

### Example 5.5 — Mandatory subeffecting and `--∅-->` non-termination witness on `loop`
- Statement: On `loop` (Example 5.2), setting `Γ̂_{fx} = [f ↦ (τ̂ --{Y,Z}--> τ̂) --{F}--> (τ̂ --∅--> τ̂)][x ↦ τ̂ --{Y,Z}--> τ̂]`
  requires subeffecting in `[fn]` to enlarge `{Y}` on `fn_Y y => y` to `{Y, Z}` and `{Z}` on `fn_Z z => z`
  to `{Z, Y}` (`= {Y, Z}`), deriving `[] ⊢_CFA loop : τ̂ --φ--> τ̂` for *every* `φ ∈ Ann`, with `φ = ∅`
  (`[] ⊢_CFA loop : τ̂ --∅--> τ̂`) strictly most informative and witnessing that `loop` never returns any
  function abstraction (hence does not terminate). `■`
- Citation: [PPA Example 5.5, p. 289] (book p. 289; PDF p. 306); [PPA Example 5.5, p. 290] (book p. 290; PDF p. 307)

### Table 5.3 — Equality of Annotations (`UCAI`) and structural equality on `Typê`
- Statement: Set-equality axioms and congruence rules `UCAI` (*unit, commutativity, associativity,
  idempotence*) on `Ann`:
  ```text
  [unit]   φ = φ ∪ ∅                 [idem]  φ = φ ∪ φ
  [com]    φ₁ ∪ φ₂ = φ₂ ∪ φ₁        [ass]   φ₁ ∪ (φ₂ ∪ φ₃) = (φ₁ ∪ φ₂) ∪ φ₃
  [ref]    φ = φ

           φ₁ = φ₂    φ₂ = φ₃                φ₁ = φ'₁    φ₂ = φ'₂
  [trans]  ------------------        [cong]  --------------------
                φ₁ = φ₃                      φ₁ ∪ φ₂ = φ'₁ ∪ φ'₂
  ```
  lifted structurally to `Typê` by `τ̂ = τ̂` and `(τ̂₁ = τ̂'₁ ∧ τ̂₂ = τ̂'₂ ∧ φ = φ') ⇒ (τ̂₁ --φ--> τ̂₂) = (τ̂'₁ --φ'--> τ̂'₂)`.
- Citation: [PPA Table 5.3, p. 290] (book p. 290; PDF p. 307)

### Fact 5.6 — Conservative extension of `⊢_CFA` over `⊢_UL`
- Statement:
  - `(i)` `If Γ̂ ⊢_CFA e : τ̂ then ⌊Γ̂⌋ ⊢_UL e : ⌊τ̂⌋.`
  - `(ii)` `If Γ ⊢_UL e : τ then there exists Γ̂ and τ̂ such that Γ̂ ⊢_CFA e : τ̂, ⌊Γ̂⌋ = Γ and ⌊τ̂⌋ = τ.` `■`
  (Proof: `(i)` erases annotations on the derivation tree; `(ii)` annotates every arrow in `Γ`, `τ`, and the
  `⊢_UL` tree with the set of all program points `π` occurring in `e`, relying on `{π} ∪ φ` subeffecting so
  `{π} ∪ Pnt_e = Pnt_e`; without subeffecting, Example 5.5 would have *no* `⊢_CFA` typing!)
- Citation: [PPA Fact 5.6, p. 291] (book p. 291; PDF p. 308)

### Findings (5.1)
- F-U5a-01: On p. 290 (*Equivalence of annotations*, paragraph 3), the book writes unhatted
  `τ₁ --φ₁--> τ₂` and `τ₁ --φ₂--> τ₂` before switching to hatted `τ̂₁, τ̂₂` in paragraph 4; on p. 291, Fact
  5.6(ii) prints `"there exists Γ̂ and τ̂"` (singular verb with plural subject). Recorded as printed.
  [PPA §5.1.2, p. 290] (book p. 290; PDF p. 307); [PPA Fact 5.6, p. 291] (book p. 291; PDF p. 308)

### Projections (5.1)
- cs_theory: `Fact 5.6` exhibits `⌊·⌋` as a split-surjective forgetful functor
  `[external: refinement-type fibration]` from `⊢_CFA` derivations to `⊢_UL` derivations, where built-in
  `{π} ∪ φ` subeffecting supplies the coarse top section annotating every arrow with `Pnt_e`.
- swe_architecture: As Example 5.4 demonstrates, the root type returned at the top of an AST (`int` when
  `main : int`) discards internal call-site arrow annotations! Any compiler `[external: devirtualiser]` or
  call-graph builder built on `⊢_CFA` must maintain an AST-node side table recording the resolved annotated
  type of every operator subexpression `e₁` at `e₁ e₂` `[derived]`.
- practical_debugging: Because Table 5.2 `[app]` demands exact argument-type equality `τ̂₂` without
  directional subtyping, passing `fn_Y` and `fn_Z` to the same monomorphic higher-order parameter forces
  **bidirectional smearing** (`{Y, Z}` on *both* `fn_Y` and `fn_Z` in Example 5.5, unlike Chapter 3's
  directional 0-CFA in Example 3.4 where `Ĉ_lp(3) = {id_y}` and `Ĉ_lp(8) = {id_z}` stayed separate!).
- cyber: Replacing `Ann = 𝒫(Pnt)` with a security/`[external: taint]` lattice `(Low ⊑ High)`
  `[external: Volpano–Smith–Irvine]` turns Table 5.2 into a higher-order `[external: taint]`/integrity type
  system; without directional subtyping (§5.4), passing one `Untrusted` callback into a shared helper
  bi-directionally `[external: taints]` every `Trusted` callback passed to the same helper.

## 5.2 Theoretical Properties

Context: Section 5.2 defines an environment-free big-step Natural Semantics `⊢ e ⟶ v` over closed terms
(Table 5.4), proves semantic correctness via Subject Reduction (Theorem 5.9) using closed substitution
(Lemma 5.11), defines the **covariant** fibre lattice `(Typê[τ], ⊑)`, and proves that valid CFA typings over
any underlying typing `Γ ⊢_UL e : τ` form a Moore family (Proposition 5.12)
[PPA §5.2, p. 291] (book p. 291; PDF p. 308).

### 5.2.1 Natural Semantics

### [U5a:5.2.1-a] Environment-free closed Natural Semantics (`Val`, `e₁[x ↦ e₂]`, `⊢ e ⟶ v`)
- Statement: Because Chapter 5 has no subexpression labels `ℓ` to preserve (unlike §3.2.1
  [PPA §3.2.1, p. 153] (book p. 153; PDF p. 171)), §5.2.1 adopts an environment-free *Natural Semantics*
  (big-step operational semantics) over **closed** expressions `e ∈ Exp` (`FV(e) = ∅`):
  ```text
  v ∈ Val   values         v ::= c | fn_π x => e₀    (provided FV(fn_π x => e₀) = ∅)
  ```
  - Substitution `e₁[x ↦ e₂]` replaces free occurrences of `x` in `e₁` by `e₂`; since `e₂` is always closed
    whenever `e₁[x ↦ e₂]` is formed in Table 5.4, variable capture cannot occur and bound-variable
    `α`-renaming is never required.
  - Standing assumption: `f ≠ x` in every `fun_π f x => e₀`.
  - Trade-off: avoids `close`, `bind`, and recursive `ℛ` from §3.2, at the price that subject reduction
    becomes vacuous on looping programs (cf. Chapter 3 Concluding Remarks
    [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219)).
- Citation: [PPA §5.2.1, p. 292] (book p. 292; PDF p. 309); [PPA §5.2.1, p. 293] (book p. 293; PDF p. 310); [PPA §5.2.1, p. 294] (book p. 294; PDF p. 311)

### Table 5.4 — Natural Semantics for `FUN`
- Statement: Big-step evaluation judgement `⊢ e ⟶ v` (with `[con]` and `[if₁]`/`[if₂]` restored from
  `PDF p. 309` where OCR drops them):
  ```text
  [con]   ⊢ c ⟶ c

  [fn]    ⊢ (fn_π x => e₀) ⟶ (fn_π x => e₀)

  [fun]   ⊢ (fun_π f x => e₀) ⟶ fn_π x => (e₀[f ↦ fun_π f x => e₀])

          ⊢ e₁ ⟶ (fn_π x => e₀)    ⊢ e₂ ⟶ v₂    ⊢ e₀[x ↦ v₂] ⟶ v₀
  [app]   --------------------------------------------------------------
          ⊢ e₁ e₂ ⟶ v₀

          ⊢ e₀ ⟶ true    ⊢ e₁ ⟶ v₁
  [if₁]   -----------------------------------
          ⊢ if e₀ then e₁ else e₂ ⟶ v₁

          ⊢ e₀ ⟶ false    ⊢ e₂ ⟶ v₂
  [if₂]   -----------------------------------
          ⊢ if e₀ then e₁ else e₂ ⟶ v₂

          ⊢ e₁ ⟶ v₁    ⊢ e₂[x ↦ v₁] ⟶ v₂
  [let]   -----------------------------------
          ⊢ let x = e₁ in e₂ ⟶ v₂

          ⊢ e₁ ⟶ v₁    ⊢ e₂ ⟶ v₂
  [op]    -------------------------    if v₁ **op** v₂ = v
          ⊢ e₁ op e₂ ⟶ v
  ```
- Side conditions: Notice `[fun]` unfolds `fun_π f x => e₀` one step into an ordinary `fn_π` abstraction
  **inheriting the exact same program point `π`**, so `[app]` needs only one rule!
- Citation: [PPA Table 5.4, p. 292] (book p. 292; PDF p. 309)

### Example 5.7 — Big-step evaluation of `(fn_X x => x) (fn_Y y => y)`
- Statement: `[fn]` gives `⊢ fn_X x => x ⟶ fn_X x => x`, `⊢ fn_Y y => y ⟶ fn_Y y => y`, and
  `⊢ x[x ↦ fn_Y y => y] ⟶ fn_Y y => y`, so `[app]` yields `⊢ (fn_X x => x) (fn_Y y => y) ⟶ fn_Y y => y`. `■`
- Citation: [PPA Example 5.7, p. 293] (book p. 293; PDF p. 310)

### Example 5.8 — Divergence of `loop` via circular subgoal `(5.1)`
- Statement: Evaluating `loop` unfolds `fun_F` to `fn_F x => ((fun_F f x => f (fn_Y y => y)) (fn_Y y => y))`
  and requires a finite derivation tree for `(5.1)`:
  ```text
  ⊢ (fun_F f x => f (fn_Y y => y)) (fn_Y y => y) ⟶ v                     (5.1)
  ```
  which immediately demands `(5.1)` again as a strict sub-derivation; thus *non-termination is modelled by
  the absence of any finite derivation tree `⊢ loop ⟶ v`*. `■`
- Citation: [PPA Example 5.8, p. 294] (book p. 294; PDF p. 311)

### 5.2.2 Semantic Correctness

### [U5a:5.2.2-a] Operator typing compatibility assumption
- Statement: Assumes `[] ⊢_CFA v₁ : τ¹_op` and `[] ⊢_CFA v₂ : τ²_op` imply `[] ⊢_CFA v : τ_op` whenever
  `v = v₁ **op** v₂`.
- Citation: [PPA §5.2.2, p. 294] (book p. 294; PDF p. 311); [PPA §5.2.2, p. 295] (book p. 295; PDF p. 312)

### Theorem 5.9 — Subject reduction for `⊢_CFA`
- Statement:
  `If [] ⊢_CFA e : τ̂, and ⊢ e ⟶ v then [] ⊢_CFA v : τ̂.`
  Immediate corollaries (p. 295):
  1. If `[] ⊢_CFA e : τ̂₁ --φ₀--> τ̂₂` and `⊢ e ⟶ fn_π x => e₀`, then `π ∈ φ₀` (`φ₀ = {π} ∪ φ` by `[fn]`).
  2. If `[] ⊢_CFA e : τ̂₁ --∅--> τ̂₂` (as for `loop` in Example 5.5), then `e` **cannot terminate** (`π ∈ ∅`
     is impossible).
- Citation: [PPA Theorem 5.9, p. 295] (book p. 295; PDF p. 312)

### Fact 5.10 — Free-variable environment invariance
- Statement:
  `If Γ̂₁ ⊢_CFA e : τ̂ and Γ̂₁(x) = Γ̂₂(x) for all x ∈ FV(e) then Γ̂₂ ⊢_CFA e : τ̂.` `■`
- Citation: [PPA Fact 5.10, p. 295] (book p. 295; PDF p. 312)

### Lemma 5.11 — Closed-expression Substitution Lemma
- Statement:
  `Assume [] ⊢_CFA e₀ : τ̂₀ and Γ̂[x ↦ τ̂₀] ⊢_CFA e : τ̂. Then Γ̂ ⊢_CFA e[x ↦ e₀] : τ̂.` `■`
  (Proved by structural induction on `e` using `Fact 5.10`, noting `[] ⊢_CFA e₀ : τ̂₀` forces `FV(e₀) = ∅`;
  Theorem 5.9 then follows by induction on `⊢ e ⟶ v`, using `f ≠ x` in `[fun]` to commute `[f ↦ ...][x ↦ τ̂_x]`
  before applying Lemma 5.11.)
- Citation: [PPA Lemma 5.11, p. 295] (book p. 295; PDF p. 312); [PPA Lemma 5.11, p. 296] (book p. 296; PDF p. 313); [PPA §5.2.2, p. 297] (book p. 297; PDF p. 314)

### 5.2.3 Existence of Solutions

### [U5a:5.2.3-a] Annotation lattice `(Ann, ⊑)` and **covariant** fibre lattice `(Typê[τ], ⊑)`
- Statement:
  - Order `Ann` by `φ₁ ⊑ φ₂` (or `φ₁ ⊆ φ₂`) iff `∃φ' : φ₁ ∪ φ' = φ₂` modulo `UCAI`; assuming `Pnt` is
    restricted to finite `Pnt_⋆` (or `Ann` enlarged to arbitrary subsets), `(Ann, ⊑)` is a complete lattice
    isomorphic to `(𝒫(Pnt), ⊆)`.
  - For each underlying `τ ∈ Type`, define its annotated fibre `Typê[τ] = {τ̂ ∈ Typê | ⌊τ̂⌋ = τ}` ordered
    **covariantly in both domain and codomain**:
    ```text
                   τ̂₁ ⊑ τ̂'₁    φ ⊆ φ'    τ̂₂ ⊑ τ̂'₂
    τ̂ ⊑ τ̂          -----------------------------------
                   (τ̂₁ --φ--> τ̂₂) ⊑ (τ̂'₁ --φ'--> τ̂'₂)
    ```
    Notice p. 298's explicit warning: `⊑` on `Typê[τ]` is **covariant** on argument types (`τ̂₁ ⊑ τ̂'₁`),
    measuring annotation precision across derivations, **not** contravariant like behavioral subtyping `≤` in
    §5.4! `(Typê[τ], ⊑)` is a complete lattice with `⊥_τ` (`∅` on all arrows) and `⊤_τ` (`Pnt` on all arrows).
- Citation: [PPA §5.2.3, p. 297] (book p. 297; PDF p. 314); [PPA §5.2.3, p. 298] (book p. 298; PDF p. 315); [PPA §5.2.3, p. 299] (book p. 299; PDF p. 316)

### Proposition 5.12 — Moore family property of `JUDG_CFA[Γ ⊢_UL e : τ]`
- Statement: Defining `JUDG_CFA[Γ ⊢_UL e : τ] = {(Γ̂ ⊢_CFA e : τ̂) | Γ̂ ⊢_CFA e : τ̂ ∧ ⌊Γ̂⌋ = Γ ∧ ⌊τ̂⌋ = τ}`:
  `JUDG_CFA[Γ ⊢_UL e : τ] is a Moore family whenever Γ ⊢_UL e : τ.`
  (Proved by structural induction on the `Γ ⊢_UL e : τ` tree via pointwise meets `⊓_i` in `Typê[·]`, where
  `⊓ ∅` puts `Pnt` on every arrow and `{π} ∪ ⋂_i φ^i = ⋂_i ({π} ∪ φ^i)` in `[fn]`/`[fun]`.) `■`
- Citation: [PPA Proposition 5.12, p. 299] (book p. 299; PDF p. 316); [PPA Proposition 5.12, p. 300] (book p. 300; PDF p. 317)

### Example 5.13 — Least CFA typing on an open higher-order expression
- Statement: On `e = f (fn_X x => x+1) + f (fn_Y y => y+2) + (fn_Z z => z+3)(4)` over
  `[f ↦ (int → int) → int] ⊢_UL e : int`, valid CFA typings `[f ↦ (int --φ₁--> int) --φ₂--> int] ⊢_CFA e : int`
  hold iff `{X, Y} ⊆ φ₁` (for arbitrary `φ₂`); the **least** typing sets `φ₁ = {X, Y}` and `φ₂ = ∅`,
  certifying `f` is never applied to `fn_Z`. `■`
- Citation: [PPA Example 5.13, p. 300] (book p. 300; PDF p. 317)

### Findings (5.2)
- F-U5a-02: Seven turnstiles omit their system subscript across pp. 295 and 300: twice below Theorem 5.9 on
  p. 295 (`[] ⊢ e : τ̂₁ --φ₀--> τ̂₂` and `[] ⊢ e : τ̂₁ --∅--> τ̂₂`, missing `CFA`), three times in Proposition
  5.12's `[app]` proof on p. 300 (missing `CFA`), and twice in Example 5.13 on p. 300 (missing `UL` and
  `CFA`, plus math-italic `f`). [PPA §5.2.2, p. 295] (book p. 295; PDF p. 312); [PPA Proposition 5.12, p. 300] (book p. 300; PDF p. 317); [PPA Example 5.13, p. 300] (book p. 300; PDF p. 317)

### Projections (5.2)
- cs_theory: Separating the **covariant** precision order `⊑` on fibres `Typê[τ]` (`Proposition 5.12`) from
  the **contravariant** behavioral subtyping order `≤` (`§5.4`) resolves a classic confusion: `⊑` shrinks
  sets uniformly across all syntactic slots so pointwise `⊓` preserves equational typing rules, whereas `≤`
  directs value flow from producers to consumers.
- swe_architecture: `[] ⊢_CFA e : τ̂₁ --∅--> τ̂₂` is the exact type-and-effect precursor of uninhabited return
  types (`[external: ! in Rust, Never in Swift/TypeScript, NoReturn in Python]`): because closed arrow values
  must carry `{π} ≠ ∅`, an empty arrow annotation statically proves non-returning control flow.
- practical_debugging: Never rely solely on big-step evaluation tests (`if eval(e) == v: check(v)`) when
  validating an effect/flow analyser on event loops or servers: Theorem 5.9 holds *vacuously* whenever `e`
  diverges (`(5.1)`), masking faulty call/effect tracking prior to divergence unless small-step or
  fuel-bounded interpreters are tested `[derived]`.
- cyber: Two high-severity security pitfalls arise here:
  1. **Variance inversion (`[external: CWE-843]` type confusion)**: confusing covariant precision order `⊑`
     with subtyping `≤` and allowing covariant function-parameter subtyping lets an attacker pass an
     `Untrusted` input handler where a `Trusted`-only handler is expected.
  2. **Non-terminating daemon blind spot**: big-step `Table 5.4` proves nothing about privilege escalations
     or side channels inside infinite request-handling loops.

## 5.3 Inference Algorithms

Context: Section 5.3 replaces clairvoyant guessing in Tables 5.1–5.2 with deterministic reconstruction: first
`𝒲_UL` and Robinson unification `𝒰_UL` over augmented underlying types `AType` (§5.3.1, Tables 5.5–5.6),
next `𝒲_CFA` and `𝒰_CFA` over free-algebra **simple types** `SType` (`τ̂₁ --β--> τ̂₂`) paired with atomic
inclusion constraints `β ⊇ {π}` (§5.3.2, Tables 5.7–5.8), then syntactic soundness and completeness
(§5.3.3, Theorems 5.20–5.21), and finally Moore-family solvability and the closed-form least annotation
substitution `θ_A` (§5.3.4, Lemma 5.22, Corollary 5.23, concluding at the top of p. 319)
[PPA §5.3, p. 300] (book p. 300; PDF p. 317).

### 5.3.1 An Algorithm for the Underlying Type System

### [U5a:5.3.1-a] Augmented types (`AType`, `TVar`) and finite type substitutions (`θ`)
- Statement:
  ```text
  τ ∈ AType   augmented types   τ ::= int | bool | τ₁ → τ₂ | α
  α ∈ TVar    type variables    α ::= 'a | 'b | 'c | ⋯
  ```
  - Substitution `θ : TVar →_fin AType` (`dom(θ)` finite, `θ α = α` outside `dom(θ)`) lifts homomorphically
    to `AType` (`θ int = int`, `θ bool = bool`, `θ(τ₁ → τ₂) = (θ τ₁) → (θ τ₂)`) and pointwise to `Γ`.
  - `θ` is *ground* iff `∀α ∈ dom(θ) : θ α ∈ Type`; `θ` *covers* `Γ` (resp. `τ`) iff `dom(θ)` contains all
    type variables in `Γ` (resp. `τ`); composition `(θ₁ ∘ θ₂) τ = θ₁(θ₂ τ)` with identity `id`.
  - Intended soundness contract for `𝒲_UL(Γ, e) = (τ, θ)`: `θ_G(θ Γ) ⊢_UL e : θ_G τ` for every ground `θ_G`
    covering `θ Γ` and `τ`. Fresh variables allocated during `𝒲_UL` are disjoint from inputs and prior
    allocations.
- Citation: [PPA §5.3.1, p. 300] (book p. 300; PDF p. 317); [PPA §5.3.1, p. 301] (book p. 301; PDF p. 318); [PPA §5.3.1, p. 302] (book p. 302; PDF p. 319)

### Table 5.5 — Algorithm `𝒲_UL` for the underlying type system
- Statement: Bottom-up underlying type reconstruction `𝒲_UL(Γ, e) = (τ, θ)` (transcribed verbatim as printed
  on p. 303, including the `if`-clause omission of `∘ θ₀`; see `F-U5a-04`):
  ```text
  𝒲_UL(Γ, c) = (τ_c, id)

  𝒲_UL(Γ, x) = (Γ(x), id)

  𝒲_UL(Γ, fn_π x => e₀) =
      let α_x be fresh
          (τ₀, θ₀) = 𝒲_UL(Γ[x ↦ α_x], e₀)
      in  ((θ₀ α_x) → τ₀,  θ₀)

  𝒲_UL(Γ, fun_π f x => e₀) =
      let α_x, α₀ be fresh
          (τ₀, θ₀) = 𝒲_UL(Γ[f ↦ α_x → α₀][x ↦ α_x], e₀)
          θ₁ = 𝒰_UL(τ₀, θ₀ α₀)
      in  (θ₁(θ₀ α_x) → θ₁ τ₀,  θ₁ ∘ θ₀)

  𝒲_UL(Γ, e₁ e₂) =
      let (τ₁, θ₁) = 𝒲_UL(Γ, e₁)
          (τ₂, θ₂) = 𝒲_UL(θ₁ Γ, e₂)
          α be fresh
          θ₃ = 𝒰_UL(θ₂ τ₁, τ₂ → α)
      in  (θ₃ α,  θ₃ ∘ θ₂ ∘ θ₁)

  𝒲_UL(Γ, if e₀ then e₁ else e₂) =
      let (τ₀, θ₀) = 𝒲_UL(Γ, e₀)
          (τ₁, θ₁) = 𝒲_UL(θ₀ Γ, e₁)
          (τ₂, θ₂) = 𝒲_UL(θ₁(θ₀ Γ), e₂)
          θ₃ = 𝒰_UL(θ₂(θ₁ τ₀), bool)
          θ₄ = 𝒰_UL(θ₃ τ₂, θ₃(θ₂ τ₁))
      in  (θ₄(θ₃ τ₂),  θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁)

  𝒲_UL(Γ, let x = e₁ in e₂) =
      let (τ₁, θ₁) = 𝒲_UL(Γ, e₁)
          (τ₂, θ₂) = 𝒲_UL((θ₁ Γ)[x ↦ τ₁], e₂)
      in  (τ₂,  θ₂ ∘ θ₁)

  𝒲_UL(Γ, e₁ op e₂) =
      let (τ₁, θ₁) = 𝒲_UL(Γ, e₁)
          (τ₂, θ₂) = 𝒲_UL(θ₁ Γ, e₂)
          θ₃ = 𝒰_UL(θ₂ τ₁, τ¹_op)
          θ₄ = 𝒰_UL(θ₃ τ₂, τ²_op)
      in  (τ_op,  θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁)
  ```
- Citation: [PPA Table 5.5, p. 303] (book p. 303; PDF p. 320)

### Example 5.14 — `𝒲_UL` trace on `(fn_X x => x) (fn_Y y => y)`
- Statement: `𝒲_UL([], fn_X x => x) = ('a → 'a, id)`, `𝒲_UL([], fn_Y y => y) = ('b → 'b, id)`, and fresh `'c`
  triggers `𝒰_UL('a → 'a, ('b → 'b) → 'c) = ['a ↦ 'b → 'b]['c ↦ 'b → 'b]`, returning
  `('b → 'b, ['a ↦ 'b → 'b]['c ↦ 'b → 'b])`. `■`
- Citation: [PPA Example 5.14, p. 304] (book p. 304; PDF p. 321)

### [U5a:5.3.1-b] `Analogy.` — Substitutions as retroactive laws (unnumbered remark)
- Statement: Just as a computer seller pricing PCs must retroactively update all prior pricing calculations
  whenever parliament passes a new 10% software-disk transfer-fee law, each unification substitution `θ_i`
  ("new law") returned by `𝒰_UL` must be applied retroactively to all previously inferred types and
  environment assumptions ("considerations") in Table 5.5 (`θ₁ Γ`, `θ₂ τ₁`, `θ₂(θ₁ τ₀)`, `θ₃(θ₂ τ₁)`) so they
  remain valid. `□`
- Citation: [PPA §5.3.1, p. 304] (book p. 304; PDF p. 321); [PPA §5.3.1, p. 305] (book p. 305; PDF p. 322)

### Table 5.6 — Unification of underlying types (`𝒰_UL`)
- Statement: Syntactic Robinson unification `𝒰_UL(τ₁, τ₂) = θ` (restoring the arrow clause erased in OCR on
  `PDF p. 322`):
  ```text
  𝒰_UL(int, int)           = id
  𝒰_UL(bool, bool)         = id
  𝒰_UL(τ₁ → τ₂, τ'₁ → τ'₂) = let θ₁ = 𝒰_UL(τ₁, τ'₁)
                                 θ₂ = 𝒰_UL(θ₁ τ₂, θ₁ τ'₂)
                             in  θ₂ ∘ θ₁
  𝒰_UL(τ, α)               = [α ↦ τ]   if α does not occur in τ or if α equals τ
                           = fail      otherwise
  𝒰_UL(α, τ)               = [α ↦ τ]   if α does not occur in τ or if α equals τ
                           = fail      otherwise
  𝒰_UL(τ₁, τ₂)             = fail      in all other cases
  ```
  Top-level failure occurs **iff** either two distinct top-level constructors (`int`, `bool`, `→`) clash, or
  the **occurs check** rejects unifying `α` with a function type properly containing `α` (e.g. self-application
  `fn_X x => x x`).
- Citation: [PPA Table 5.6, p. 305] (book p. 305; PDF p. 322)

### Example 5.15 — `𝒰_UL` trace
- Statement: `𝒰_UL('a → 'a, ('b → 'b) → 'c)` computes `θ₁ = 𝒰_UL('a, 'b → 'b) = ['a ↦ 'b → 'b]` and
  `θ₂ = 𝒰_UL('b → 'b, 'c) = ['c ↦ 'b → 'b]`, returning `['a ↦ 'b → 'b]['c ↦ 'b → 'b]`. `■`
- Citation: [PPA Example 5.15, p. 305] (book p. 305; PDF p. 322); [PPA Example 5.15, p. 306] (book p. 306; PDF p. 323)

### 5.3.2 An Algorithm for Control Flow Analysis

### [U5a:5.3.2-a] Non-free `Typê` modulo `UCAI` vs free-algebra simple types (`SType`, `AVar`, `SAnn`)
- Statement: Because `UCAI` (`Table 5.3`) identifies syntactically distinct types such as
  `int --{π₁}∪{π₂}--> int` and `int --{π₂}∪{π₁}--> int`, `Typê` is a **non-free algebra** lacking unitary
  syntactic MGUs. To recover a **free algebra**, §5.3.2 restricts arrow annotations inside types to single
  *annotation variables* `β ∈ AVar` (*simple types* `SType`) while deferring concrete set unions to an
  auxiliary inclusion constraint set `C` (restoring the `φ ∈ SAnn` BNF line below Table 5.7 dropped by OCR on
  `PDF p. 324`):
  ```text
  τ̂ ∈ SType   simple types           τ̂ ::= int | bool | τ̂₁ --β--> τ̂₂ | α
  α ∈ TVar    type variables         α ::= 'a | 'b | 'c | ⋯
  β ∈ AVar    annotation variables   β ::= '1 | '2 | '3 | ⋯
  φ ∈ SAnn    simple annotations     φ ::= {π} | φ₁ ∪ φ₂ | ∅ | β
  ```
  A *simple substitution* `θ` maps `TVar → SType` and **`AVar → AVar` only**, ensuring `SType` is closed
  under `θ`.
- Citation: [PPA §5.3.2, p. 306] (book p. 306; PDF p. 323); [PPA §5.3.2, p. 307] (book p. 307; PDF p. 324)

### Table 5.7 — Unification of simple types (`𝒰_CFA`)
- Statement: Structural unification `𝒰_CFA(τ̂₁, τ̂₂) = θ` on free `SType`:
  ```text
  𝒰_CFA(int, int)                  = id
  𝒰_CFA(bool, bool)                = id
  𝒰_CFA(τ̂₁ --β--> τ̂₂, τ̂'₁ --β'--> τ̂'₂) =
      let θ₀ = [β' ↦ β]
          θ₁ = 𝒰_CFA(θ₀ τ̂₁, θ₀ τ̂'₁)
          θ₂ = 𝒰_CFA(θ₁(θ₀ τ̂₂), θ₁(θ₀ τ̂'₂))
      in  θ₂ ∘ θ₁ ∘ θ₀
  𝒰_CFA(τ̂, α)                      = [α ↦ τ̂]   if α does not occur in τ̂ or if α equals τ̂
                                   = fail       otherwise
  𝒰_CFA(α, τ̂)                      = [α ↦ τ̂]   if α does not occur in τ̂ or if α equals τ̂
                                   = fail       otherwise
  𝒰_CFA(τ̂₁, τ̂₂)                    = fail       in all other cases
  ```
  Crucial property (p. 307): **`𝒰_CFA(τ̂₁, τ̂₂)` fails if and only if `𝒰_UL(⌊τ̂₁⌋, ⌊τ̂₂⌋)` fails**!
- Citation: [PPA Table 5.7, p. 307] (book p. 307; PDF p. 324)

### Example 5.16 — `𝒰_CFA` trace
- Statement: `𝒰_CFA('a --'1--> 'a, ('b --'2--> 'b) --'3--> 'c)` forms `θ₀ = ['3 ↦ '1]`, `θ₁ = ['a ↦ 'b --'2--> 'b]`,
  and `θ₂ = ['c ↦ 'b --'2--> 'b]`, returning `['3 ↦ '1]['a ↦ 'b --'2--> 'b]['c ↦ 'b --'2--> 'b]`. `■`
- Citation: [PPA Example 5.16, p. 308] (book p. 308; PDF p. 325)

### Fact 5.17 — Soundness and MGU completeness of `𝒰_CFA`
- Statement: Let `τ̂₁` and `τ̂₂` be two simple types (Exercise 5.8
  [PPA Exercise 5.8, p. 361] (book p. 361; PDF p. 378)):
  1. `If 𝒰_CFA(τ̂₁, τ̂₂) = θ then θ is a simple substitution such that θ τ̂₁ = θ τ̂₂.`
  2. `If there exists a substitution θ'' such that θ'' τ̂₁ = θ'' τ̂₂ then there exists substitutions θ and θ' such that 𝒰_CFA(τ̂₁, τ̂₂) = θ and θ'' = θ' ∘ θ.` `■`
- Citation: [PPA Fact 5.17, p. 308] (book p. 308; PDF p. 325)

### [U5a:5.3.2-b] Constraints `C`, substitution classes (`θ_T`, `θ_A`, `θ_G`), and ground validations
- Statement:
  - A *constraint* is an inclusion `β ⊇ φ` (`β ∈ AVar`, `φ ∈ SAnn`); for simple substitution `θ`,
    `θ C = {θ β ⊇ θ φ | (β ⊇ φ) ∈ C}`.
  - *Type substitution* `θ_T` maps `TVar → Typê` (ground); *annotation substitution* `θ_A` maps `AVar → Ann`
    (ground), satisfying `θ_A ⊨ C` iff `θ_A` covers `C` and `∀(β ⊇ φ) ∈ C : θ_A β ⊇ θ_A φ`.
  - A *ground substitution* factors as `θ_G = θ_A ∘ θ_T = θ_T ∘ θ_A`, and is a **ground validation** of
    `(Γ̂, τ̂, C)` iff it covers `Γ̂`, `τ̂`, and `C` and satisfies `θ_A ⊨ C`.
- Citation: [PPA §5.3.2, p. 308] (book p. 308; PDF p. 325); [PPA §5.3.2, p. 309] (book p. 309; PDF p. 326)

### Table 5.8 — Algorithm `𝒲_CFA` for Control Flow Analysis
- Statement: Constraint-generating CFA reconstruction `𝒲_CFA(Γ̂, e) = (τ̂, θ, C)` emitting *only* atomic
  constraints `β ⊇ {π}` (note: line 6 of `if` prints unhatted `τ₁` in `θ₃(θ₂ τ₁)` while restoring `∘ θ₀`
  omitted in Table 5.5; see `F-U5a-04` and `F-U5a-05`):
  ```text
  𝒲_CFA(Γ̂, c) = (τ_c, id, ∅)

  𝒲_CFA(Γ̂, x) = (Γ̂(x), id, ∅)

  𝒲_CFA(Γ̂, fn_π x => e₀) =
      let α_x be fresh
          (τ̂₀, θ₀, C₀) = 𝒲_CFA(Γ̂[x ↦ α_x], e₀)
          β₀ be fresh
      in  ((θ₀ α_x) --β₀--> τ̂₀,  θ₀,  C₀ ∪ {β₀ ⊇ {π}})

  𝒲_CFA(Γ̂, fun_π f x => e₀) =
      let α_x, α₀, β₀ be fresh
          (τ̂₀, θ₀, C₀) = 𝒲_CFA(Γ̂[f ↦ α_x --β₀--> α₀][x ↦ α_x], e₀)
          θ₁ = 𝒰_CFA(τ̂₀, θ₀ α₀)
      in  (θ₁(θ₀ α_x) --θ₁(θ₀ β₀)--> θ₁ τ̂₀,  θ₁ ∘ θ₀,
           (θ₁ C₀) ∪ {θ₁(θ₀ β₀) ⊇ {π}})

  𝒲_CFA(Γ̂, e₁ e₂) =
      let (τ̂₁, θ₁, C₁) = 𝒲_CFA(Γ̂, e₁)
          (τ̂₂, θ₂, C₂) = 𝒲_CFA(θ₁ Γ̂, e₂)
          α, β be fresh
          θ₃ = 𝒰_CFA(θ₂ τ̂₁, τ̂₂ --β--> α)
      in  (θ₃ α,  θ₃ ∘ θ₂ ∘ θ₁,  θ₃(θ₂ C₁) ∪ θ₃ C₂)

  𝒲_CFA(Γ̂, if e₀ then e₁ else e₂) =
      let (τ̂₀, θ₀, C₀) = 𝒲_CFA(Γ̂, e₀)
          (τ̂₁, θ₁, C₁) = 𝒲_CFA(θ₀ Γ̂, e₁)
          (τ̂₂, θ₂, C₂) = 𝒲_CFA(θ₁(θ₀ Γ̂), e₂)
          θ₃ = 𝒰_CFA(θ₂(θ₁ τ̂₀), bool)
          θ₄ = 𝒰_CFA(θ₃ τ̂₂, θ₃(θ₂ τ₁))
      in  (θ₄(θ₃ τ̂₂),  θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁ ∘ θ₀,
           θ₄(θ₃(θ₂(θ₁ C₀))) ∪ θ₄(θ₃(θ₂ C₁)) ∪ θ₄(θ₃ C₂))

  𝒲_CFA(Γ̂, let x = e₁ in e₂) =
      let (τ̂₁, θ₁, C₁) = 𝒲_CFA(Γ̂, e₁)
          (τ̂₂, θ₂, C₂) = 𝒲_CFA((θ₁ Γ̂)[x ↦ τ̂₁], e₂)
      in  (τ̂₂,  θ₂ ∘ θ₁,  (θ₂ C₁) ∪ C₂)

  𝒲_CFA(Γ̂, e₁ op e₂) =
      let (τ̂₁, θ₁, C₁) = 𝒲_CFA(Γ̂, e₁)
          (τ̂₂, θ₂, C₂) = 𝒲_CFA(θ₁ Γ̂, e₂)
          θ₃ = 𝒰_CFA(θ₂ τ̂₁, τ¹_op)
          θ₄ = 𝒰_CFA(θ₃ τ̂₂, τ²_op)
      in  (τ_op,  θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁,
           θ₄(θ₃(θ₂ C₁)) ∪ θ₄(θ₃ C₂))
  ```
- Citation: [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327)

### Example 5.18 — `𝒲_CFA` trace on `(fn_X x => x) (fn_Y y => y)`
- Statement: `𝒲_CFA([], fn_X x => x) = ('a --'1--> 'a, id, {'1 ⊇ {X}})`,
  `𝒲_CFA([], fn_Y y => y) = ('b --'2--> 'b, id, {'2 ⊇ {Y}})`, and Example 5.16's unifier `θ₃` yields
  `('b --'2--> 'b, ['3 ↦ '1]['a ↦ 'b --'2--> 'b]['c ↦ 'b --'2--> 'b], {'1 ⊇ {X}, '2 ⊇ {Y}})`. `■`
- Citation: [PPA Example 5.18, p. 311] (book p. 311; PDF p. 328)

### Example 5.19 — `𝒲_CFA` trace on `loop`
- Statement: `𝒲_CFA([], fun_F f x => f (fn_Y y => y))` produces `('a --'2--> 'a) --'1--> 'b` and
  `{'1 ⊇ {F}, '2 ⊇ {Y}}`; unifying `g` with `('c --'3--> 'c) --'4--> 'd` merges `'2` and `'3` so one
  annotation variable accumulates `{Y}` and `{Z}` (`Example 5.19` writes `['1 ↦ '4, '2 ↦ '3, 'a ↦ 'c, 'b ↦ 'd]`,
  type `'d`, and `{'4 ⊇ {F}, '3 ⊇ {Y}, '3 ⊇ {Z}}`, reversing Table 5.7's `[β' ↦ β]` binding orientation; see
  `F-U5a-06`). `■`
- Citation: [PPA Example 5.19, p. 311] (book p. 311; PDF p. 328)

### 5.3.3 Syntactic Soundness and Completeness

### Theorem 5.20 — Syntactic Soundness of `𝒲_CFA`
- Statement:
  `If 𝒲_CFA(Γ̂, e) = (τ̂, θ, C) and θ_G is a ground validation of θ Γ̂, τ̂ and C then θ_G(θ Γ̂) ⊢_CFA e : θ_G τ̂.`
  (Proved by structural induction on `e` across pp. 312–314, extending `θ_G` to a ground extension `θ'_G` at
  `e₁ e₂` to cover eliminated intermediate variables in `θ₃(θ₂ τ̂₁)` and `θ₃ τ̂₂`.) `■`
- Citation: [PPA Theorem 5.20, p. 312] (book p. 312; PDF p. 329); [PPA Theorem 5.20, p. 313] (book p. 313; PDF p. 330); [PPA Theorem 5.20, p. 314] (book p. 314; PDF p. 331)

### Theorem 5.21 — Syntactic Completeness of `𝒲_CFA`
- Statement:
  `Assume that Γ̂ is a simple type environment and θ' Γ̂ ⊢_CFA e : τ̂' holds for some ground substitution θ' that covers Γ̂. Then there exists τ̂, θ, C and θ_G such that`
  - `𝒲_CFA(Γ̂, e) = (τ̂, θ, C),`
  - `θ_G is a ground validation of θ Γ̂, τ̂ and C,`
  - `θ_G ∘ θ = θ' except on fresh type and annotation variables (as created by 𝒲_CFA(Γ̂, e)), and`
  - `θ_G τ̂ = τ̂'.`
  (Proved directly by structural induction on `θ' Γ̂ ⊢_CFA e : τ̂'` using `Fact 5.17(2)` without proof
  normalisation because Table 5.2 inlined `{π} ∪ φ` into `[fn]`/`[fun]`, unlike standalone subeffecting in
  Exercise 5.13 [PPA Exercise 5.13, p. 362] (book p. 362; PDF p. 379).) `■`
- Citation: [PPA Theorem 5.21, p. 314] (book p. 314; PDF p. 331); [PPA Theorem 5.21, p. 315] (book p. 315; PDF p. 332); [PPA Theorem 5.21, p. 316] (book p. 316; PDF p. 333); [PPA Theorem 5.21, p. 317] (book p. 317; PDF p. 334)

### 5.3.4 Existence of Solutions

### Lemma 5.22 — Moore family of constraint-solving annotation substitutions
- Statement:
  `If 𝒲_CFA(Γ̂, e) = (τ̂, θ, C) and X is a finite set of annotation variables such that X ⊇ AV(C), then {θ_A | θ_A ⊨ C ∧ dom(θ_A) = X ∧ θ_A is an annotation substitution} is a Moore family.` `■`
  (Proof on p. 318 — restored from `PDF p. 335` where OCR drops the intersection equations — sets
  `θ β = ⋂_{θ_A ∈ Y} (θ_A β)` for `β ∈ X`; monotonicity of `φ ∈ SAnn` in free annotation variables gives
  `θ β = ⋂_{θ_A ∈ Y} θ_A β ⊇ ⋂_{θ_A ∈ Y} θ φ ⊇ θ φ` for every `(β ⊇ φ) ∈ C`, holding for *general* `φ ∈ SAnn`
  beyond `𝒲_CFA`!) `■`
- Citation: [PPA Lemma 5.22, p. 317] (book p. 317; PDF p. 334); [PPA Lemma 5.22, p. 318] (book p. 318; PDF p. 335)

### Corollary 5.23 — Existence of ground validations for `𝒲_CFA`
- Statement:
  `If 𝒲_CFA(Γ̂, e) = (τ̂, θ, C) then there exists a ground validation θ_G of θ Γ̂, τ̂ and C.` `■`
- Citation: [PPA Corollary 5.23, p. 318] (book p. 318; PDF p. 335)

### [U5a:5.3.4-a] Choice of `θ_T` and closed-form least solution `θ_A` (concluding atop p. 319)
- Statement:
  1. Unconstrained `α ∈ TVar` in `θ Γ̂` or `τ̂` may be mapped by `θ_T` to `int`, `bool`, or any `θ''_T α ∈ Typê[τ_α]`
     (preferring the `∅`-annotated least element of `Typê[τ_α]`; cf. Exercise 5.9
     [PPA Exercise 5.9, p. 361] (book p. 361; PDF p. 378)).
  2. Because `𝒲_CFA` generates *only* atomic constraints `β ⊇ {π}`, the least annotation substitution on
     `AV(C)` requires *no fixed-point iteration* (bottom of p. 318 and top 4 lines of p. 319 above `§5.4`):
     ```text
     θ_A β = {π | β ⊇ {π} is in C}     if β ∈ AV(C)
           = undefined                  otherwise
     ```
     Then `dom(θ_A) = AV(C)`, `θ_A ⊨ C`, and for any `θ` with `dom(θ) = AV(C)` and `θ ⊨ C`,
     `∀β : θ β ⊇ θ_A β` (`θ ⊒ θ_A`), showing `θ_A` is the least element of Lemma 5.22's Moore family at
     `X = AV(C)`. (Note: when `(AV(θ Γ̂) ∪ AV(τ̂)) \ AV(C) ≠ ∅`, `θ_A` must additionally set `θ_A β = ∅` on
     those unconstrained variables to cover `θ Γ̂` and `τ̂`; see `F-U5a-08`.)
- Citation: [PPA §5.3.4, p. 318] (book p. 318; PDF p. 335); [PPA §5.3.4, p. 319] (book p. 319; PDF p. 336)

### Findings (5.3)
- F-U5a-03: On p. 302 (last paragraph), the recursive `fun_π` explanation cites `"rule [fn] of Table 5.1"`
  instead of `[fun]`. [PPA §5.3.1, p. 302] (book p. 302; PDF p. 319)
- F-U5a-04 (`[Source Erratum — Genuine Soundness Bug in Table 5.5]`): In Table 5.5 (p. 303), the `if` clause
  of `𝒲_UL(Γ, if e₀ then e₁ else e₂)` returns `(θ₄(θ₃ τ₂), θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁)`, **omitting `∘ θ₀`**! On
  `Γ = [b ↦ 'a]` and `e = if (b < 5) then 1 else 2`, `θ₀ = ['a ↦ int]` and `θ₁ = θ₂ = θ₃ = θ₄ = id`, so
  Table 5.5 returns `(int, id)` and allows `θ_G = ['a ↦ bool]` where `[b ↦ bool] ⊬_UL e : int` `[derived]`.
  Corrected to `θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁ ∘ θ₀` in Table 5.8 (p. 310).
  [PPA Table 5.5, p. 303] (book p. 303; PDF p. 320); [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327)
- F-U5a-05: On p. 307 (last paragraph), prose omits the prime on `τ̂'₂` in `τ̂'₁ --β'--> τ̂₂`; on p. 309 (last
  paragraph), prose writes `β` for `β₀`; in Table 5.8 (p. 310, `if` line 6), `θ₄ = 𝒰_CFA(θ₃ τ̂₂, θ₃(θ₂ τ₁))`
  omits the hat on `τ̂₁`; on p. 312, prose prints `"the the Concluding Remarks"`, `"respect the the inference
  system"`, and `"substition"`; on p. 313 (`Theorem 5.20` case `c`), `θ_G(Γ)` omits the hat on `Γ̂`.
  [PPA §5.3.2, p. 307] (book p. 307; PDF p. 324); [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327); [PPA §5.3.3, p. 312] (book p. 312; PDF p. 329); [PPA Theorem 5.20, p. 313] (book p. 313; PDF p. 330)
- F-U5a-06: Example 5.19 (p. 311) states `𝒰_CFA(('a --'2--> 'a) --'1--> 'b, ('c --'3--> 'c) --'4--> 'd)`
  returns `['1 ↦ '4, '2 ↦ '3, 'a ↦ 'c, 'b ↦ 'd]`, reversing Table 5.7's deterministic binding direction
  `θ₀ = [β' ↦ β]` and `𝒰_CFA(τ̂, α)`-first rule (which actually returns `['4 ↦ '1, '3 ↦ '2, 'c ↦ 'a, 'd ↦ 'b]`,
  `α`-equivalent up to renaming `[derived]`). [PPA Table 5.7, p. 307] (book p. 307; PDF p. 324); [PPA Example 5.19, p. 311] (book p. 311; PDF p. 328)
- F-U5a-07: In Theorem 5.21's proof (pp. 315–316): case `fn_π` (p. 315) writes `{β ⊇ {π}}` for `{β₀ ⊇ {π}}`;
  case `fun_π` (p. 315) writes unhatted `τ'₀` for `τ̂'₀`; case `fun_π` (p. 316) applies Fact 5.17 to reversed
  `𝒰_CFA(θ₀ α₀, τ̂₀)` (where Table 5.8 calls `𝒰_CFA(τ̂₀, θ₀ α₀)`); and case `e₁ e₂` (p. 316) writes
  `𝒲_CFA(θ' Γ̂, e₁)` instead of `𝒲_CFA(Γ̂, e₁)`.
  [PPA Theorem 5.21, p. 315] (book p. 315; PDF p. 332); [PPA Theorem 5.21, p. 316] (book p. 316; PDF p. 333)
- F-U5a-08 (`[Domain Coverage Subtlety on θ_A]`): On pp. 318–319, `θ_A` has `dom(θ_A) = AV(C)` (`undefined`
  outside `AV(C)`), which fails to cover unconstrained arrow variables `β ∈ (AV(θ Γ̂) ∪ AV(τ̂)) \ AV(C)` (e.g.
  `'1` in `𝒲_CFA([], fn_X x => x 1) = ((int --'1--> 'b) --'2--> 'b, ..., {'2 ⊇ {X}})` `[derived]`) unless
  defaulted to `∅` on `X \ AV(C)` as in Corollary 5.23's proof!
  [PPA Corollary 5.23, p. 318] (book p. 318; PDF p. 335); [PPA §5.3.4, p. 319] (book p. 319; PDF p. 336)

### Projections (5.3)
- cs_theory: `UCAI` is the `[external: ACUI (Associative-Commutative-Idempotent with Unit); Baader–Snyder 2001]`
  equational theory, whose general unification problem is NP-complete and non-unitary; restricting `SType`
  arrows to `AVar`s factors inference into **unitary first-order syntactic unification** (`𝒰_CFA`, `Fact 5.17`)
  plus **monotone join-semilattice constraints** (`Lemma 5.22`), achieving `[external: union-find unification]` near-linear `O(n α(n))`
  complexity on monomorphic `FUN` (no Ch 5 complexity claim) vs `O(n³)` for untyped Chapter 3 `0-CFA` (`U8` comparison).
- swe_architecture: Rather than threading explicit immutable substitution maps `θ₄(θ₃(θ₂(θ₁ C₀)))` (which
  costs `O(n²)` rewrites and invites dropped-`θ_i` bugs like Table 5.5's `if` bug), production compilers
  (`[external: rustc, GHC, OCaml]`) represent `TVar` and `AVar` as `[external: Tarjan Union-Find]` nodes where
  `[β' ↦ β]` unions their `{π}` `[external: bitsets]` in `O(α(n))` amortised time and post-pass
  `[external: zonking]` reads call graphs from an AST side table `[derived]`.
- practical_debugging: Three concrete implementation traps in Tables 5.6–5.8 must be guarded by unit tests:
  1. **Self-binding loops**: Tables 5.6–5.7 specify `[α ↦ α]` when `α = τ` and `θ₀ = [β ↦ β]` when `β = β'`,
     causing infinite loops in naive map/`[external: union-find]` chasers unless short-circuited to `id` `[derived]`;
  2. **Dropped `θ_i` on `Γ` or `C_j`**: test `𝒲_UL([b ↦ 'a], if (b < 5) then 1 else 2)` (`Table 5.5` bug!)
     and cross-check `θ_G(θ Γ̂) ⊢_CFA e : θ_G τ̂` via a 40-line Table 5.2 checker;
  3. **`undefined` `θ_A` crash**: test `𝒲_CFA([], fn_X x => x 1)` where `'1 ∉ AV(C)` and default `θ_A β = ∅`
     for all `β ∈ (AV(θ Γ̂) ∪ AV(τ̂)) \ AV(C)` `[derived]`.
- cyber: Reusing a shared default annotation variable `β_def` across library signatures instead of allocating
  fresh `β` per site causes `𝒰_CFA` (`[β' ↦ β]`) to merge unrelated callers into one global equivalence class
  (`[external: Steensgaard collapse]`), flooding security/`[external: taint]` call graphs with false-positive
  edges; conversely, forgetting to apply `θ₃ ∘ θ₂` to `C₁` in `[app]` orphans `{π}` inside dead
  pre-unification variables and causes **silent false negatives** (missed `[external: taint]`/callee edges!)
  `[derived]`.

## Gotcha Ledger

- G-U5a-01: Unlike Chapters 2–4 (which apply to untyped languages), Chapter 5 Type and Effect Systems require an underlying well-typed program (`Fact 5.6(i)`): untypable expressions such as self-application `fn_X x => x x` fail the occurs check in `𝒰_UL` / `𝒰_CFA` (`Tables 5.6–5.7`) even though Chapter 3 `0-CFA` analyses them. [PPA Chapter 5, p. 283] (book p. 283; PDF p. 300)
- G-U5a-02: Chapter 5 dispenses with Chapter 3's `Term` category and subexpression labels `ℓ ∈ Lab`, attaching program points `π ∈ Pnt` *only* to `fn_π` and `fun_π`; recovering per-subexpression `Ĉ(ℓ)` and `ρ̂` requires inspecting the *entire* `⊢_CFA` inference tree (`Example 5.4`, `Exercise 5.4`), never the root type alone. [PPA Example 5.4, p. 289] (book p. 289; PDF p. 306)
- G-U5a-03: Every constant `c ∈ Const` and binary operator `op ∈ Op` in `§5.1.1` has base-only types (`τ_c, τ¹_op, τ²_op, τ_op ∈ {int, bool}`) carrying zero arrows or annotations, which is why `[op]` in `Tables 5.5` and `5.8` returns `τ_op` without applying `θ₄`. [PPA §5.1.1, p. 285] (book p. 285; PDF p. 302)
- G-U5a-04: In `§§5.1–5.3`, `let x = e₁ in e₂` is strictly *monomorphic* and admits the exact same typings as `(fn_π x => e₂) e₁` regardless of `π`; `let`-polymorphism is deferred to `§§5.4–5.5`. [PPA §5.1.1, p. 286] (book p. 286; PDF p. 303)
- G-U5a-05: Built-in *subeffecting* (`{π} ∪ φ` rather than `{π}` in `Table 5.2` `[fn]` and `[fun]`) is essential for conservative extension (`Fact 5.6(ii)`): without `∪ φ`, well-typed programs such as `loop` (`Example 5.5`) have *no* `⊢_CFA` typing at all. [PPA Fact 5.6, p. 291] (book p. 291; PDF p. 308)
- G-U5a-06: Because `Table 5.2` `[app]` demands exact argument-type equality modulo `UCAI` (`Table 5.3`) without subtyping, closures passed to the same monomorphic higher-order parameter suffer *bidirectional smearing* (`fn_Y` and `fn_Z` in `Examples 5.5, 5.19` both acquire `{Y, Z}`). [PPA Example 5.5, p. 289] (book p. 289; PDF p. 306)
- G-U5a-07: Syntax-directed `⊢_CFA` (`Table 5.2`) and `𝒲_CFA` (`Table 5.8`) must type *every* subexpression including unreachable `if` branches and uncalled functions (matching Chapter 3's `⊨_s` rather than coinductive `⊨`), so an ill-typed dead branch causes `𝒲_CFA` to `fail`. [PPA Table 5.2, p. 288] (book p. 288; PDF p. 305)
- G-U5a-08: Deriving an empty arrow annotation `[] ⊢_CFA e : τ̂₁ --∅--> τ̂₂` (`Example 5.5`) is a sound static *non-termination certificate*: every closed arrow value in `Val` has syntax `fn_π x => e₀`, which would force `π ∈ ∅` by `Theorem 5.9`. [PPA §5.2.2, p. 295] (book p. 295; PDF p. 312)
- G-U5a-09: In `Table 5.4` Natural Semantics, `fun_π f x => e₀` is *not* in `Val`; `[fun]` unfolds it one step to `fn_π x => (e₀[f ↦ fun_π f x => e₀])` *inheriting the same program point `π`*, and `f ≠ x` is assumed so `[f ↦ ...][x ↦ τ̂_x]` commutes in `Theorem 5.9`'s proof. [PPA Table 5.4, p. 292] (book p. 292; PDF p. 309)
- G-U5a-10: Capture-free substitution `e₁[x ↦ e₂]` in `Table 5.4` avoids `α`-renaming *only* because `Table 5.4` restricts evaluation to closed expressions (`FV(e) = ∅`), ensuring `FV(e₂) = ∅` at `[fun]`, `[app]`, and `[let]`. [PPA §5.2.1, p. 293] (book p. 293; PDF p. 310)
- G-U5a-11: Big-step Natural Semantics (`Table 5.4`) models non-termination by the *absence* of any finite derivation tree (`Example 5.8`, display `(5.1)`), making `Theorem 5.9` (`[] ⊢_CFA e : τ̂ ∧ ⊢ e ⟶ v ⇒ [] ⊢_CFA v : τ̂`) *vacuously true* on diverging or reactive loops. [PPA Example 5.8, p. 294] (book p. 294; PDF p. 311)
- G-U5a-12: The fibre partial order `⊑` on `Typê[τ]` (`§5.2.3`, p. 298) is **covariant** in *both* domain and codomain (`τ̂₁ ⊑ τ̂'₁ ∧ φ ⊆ φ' ∧ τ̂₂ ⊑ τ̂'₂`) so `JUDG_CFA[Γ ⊢_UL e : τ]` forms a Moore family (`Proposition 5.12`), **unlike** `§5.4`'s **contravariant** subtyping order `≤` (`τ̂'₁ ≤ τ̂₁`). [PPA §5.2.3, p. 298] (book p. 298; PDF p. 315)
- G-U5a-13: Syntactic `Ann` (`{π} | φ₁ ∪ φ₂ | ∅`) expresses only *finite* subsets of `Pnt`, so making `(Ann, ⊑)` a *complete* lattice (`⊓ ∅ = Pnt` in `Proposition 5.12` and `Lemma 5.22`) requires restricting `Pnt` to finite `Pnt_⋆` or enlarging `Ann` to `(𝒫(Pnt), ⊆)`. [PPA §5.2.3, p. 298] (book p. 298; PDF p. 315)
- G-U5a-14: In `Table 5.5` (p. 303), `𝒲_UL(Γ, if e₀ then e₁ else e₂)` prints `θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁` **omitting `∘ θ₀`** — a genuine soundness bug (dropping `['a ↦ int]` on `Γ = [b ↦ 'a]`, `if (b < 5) then 1 else 2`) that is corrected to `θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁ ∘ θ₀` in `Table 5.8` (p. 310). [PPA Table 5.5, p. 303] (book p. 303; PDF p. 320)
- G-U5a-15: Annotated types `Typê` modulo `UCAI` form a *non-free algebra*; `§5.3.2` restores a *free algebra* by restricting `SType` arrows to single annotation variables `β ∈ AVar` (`τ̂₁ --β--> τ̂₂`) and restricting simple substitutions to map `AVar → AVar` only. [PPA §5.3.2, p. 306] (book p. 306; PDF p. 323)
- G-U5a-16: `𝒰_CFA(τ̂₁, τ̂₂)` (`Table 5.7`) fails *iff* `𝒰_UL(⌊τ̂₁⌋, ⌊τ̂₂⌋)` (`Table 5.6`) fails; annotation variables never fail occurs checks, and repeated occurrences of `β` such as `'a --'1--> ('b --'1--> 'c)` are valid. [PPA Table 5.7, p. 307] (book p. 307; PDF p. 324)
- G-U5a-17: `Tables 5.6` and `5.7` return `[α ↦ α]` when `α = τ` and set `θ₀ = [β ↦ β]` when `β = β'`; imperative substitution maps or `[external: union-find]` tables must short-circuit trivial self-bindings to `id` to avoid infinite lookup loops. [PPA Table 5.6, p. 305] (book p. 305; PDF p. 322)
- G-U5a-18: In `Table 5.8`, every substitution `θ_i` computed *after* a recursive `𝒲_CFA` call must be applied to that call's constraint set `C_j` (`θ₄(θ₃(θ₂(θ₁ C₀)))` in `if`, `θ₃(θ₂ C₁)` in `app`), whereas `C_j` already incorporates its own `θ_j`. [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327)
- G-U5a-19: Proving `Theorem 5.20` (`[app]`, p. 313) requires extending `θ_G` to a *ground extension* `θ'_G` covering eliminated intermediate types `θ₃(θ₂ τ̂₁)` and `θ₃ τ̂₂` whose dead variables need not appear in `(θ Γ̂, τ̂, C)`. [PPA Theorem 5.20, p. 313] (book p. 313; PDF p. 330)
- G-U5a-20: Syntactic completeness (`Theorem 5.21`) holds without *proof normalisation* solely because `Table 5.2` inlined `{π} ∪ φ` into `[fn]`/`[fun]`; standalone subeffecting or subtyping rules (`§5.4`, `Exercise 5.13`) require normalising derivations before proving completeness. [PPA §5.3.3, p. 312] (book p. 312; PDF p. 329)
- G-U5a-21: While `θ_A β = {π | β ⊇ {π} is in C}` (pp. 318–319, concluding in the top 4 lines of p. 319 above `§5.4`) gives the closed-form least solution on `dom(θ_A) = AV(C)` without fixed-point iteration, forming a covering ground validation (`Corollary 5.23`) additionally requires setting `θ_A β = ∅` on unconstrained `β ∈ (AV(θ Γ̂) ∪ AV(τ̂)) \ AV(C)` (such as `'1` in `fn_X x => x 1`). [PPA Corollary 5.23, p. 318] (book p. 318; PDF p. 335)
- G-U5a-22: Verified source misprints and OCR drops across `§§5.1–5.3`: OCR drops `Example 5.4`'s `Ĉ(ℓ)` table (p. 289), `Table 5.4` `[con]` (p. 292), `Table 5.6` arrow clause (p. 305), `SAnn` BNF (p. 307), and `Lemma 5.22` intersections (p. 318); print has unhatted `τ₁, τ₂` (p. 290), bare `⊢` (pp. 295, 300), `[fn]` for `[fun]` (p. 302), unhatted `τ₁` in `Table 5.8` `if` (p. 310), reversed unifier orientation in `Example 5.19` (p. 311), `{β ⊇ {π}}` for `{β₀ ⊇ {π}}` (p. 315), and reversed `𝒰_CFA(θ₀ α₀, τ̂₀)` plus `𝒲_CFA(θ' Γ̂, e₁)` (p. 316). [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327)
