<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Chapter 5 L1 reference for annotated type systems, CFA subeffecting, Natural Semantics subject reduction, and covariant fibre Moore families (Sections 5.1-5.2). -->

# Annotated Type Systems, CFA Subeffecting, and Natural-Semantics Soundness

Scope: Chapter 5 opening, Section 5.1 (`§§5.1.1–5.1.2`), Section 5.2 (`§§5.2.1–5.2.3`), and Exercises `5.1–5.3`,
`5.5–5.7`, `5.10*` — [PPA Chapter 5, p. 283] (book p. 283; PDF p. 300) through
[PPA Example 5.13, p. 300] (book p. 300; PDF p. 317), plus [PPA Exercise 5.1, p. 359] (book p. 359; PDF p. 376)
through [PPA Exercise 5.10, p. 361] (book p. 361; PDF p. 378).
Ground truth: `corpus/shards/RAW_SHARD_05a_annotated_types_inference.md` and
`corpus/shards/RAW_SHARD_05b_effects_regions_behaviours.md`.
Type/effect inference (`§5.3`) and polarised subtyping (`§5.4`) live in
[inference-unification-and-subtyping.md](./inference-unification-and-subtyping.md); side effects, exceptions,
regions, and concurrent behaviours (`§§5.4.1–5.5`) live in
[effects-exceptions-regions-and-behaviours.md](./effects-exceptions-regions-and-behaviours.md); lattice/Moore-family
and structural-induction foundations live in
[appendix-a-posets-lattices-fixed-points.md](../../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md)
and [appendix-b-induction-and-coinduction.md](../../ppa-program-analysis/references/appendix-b-induction-and-coinduction.md).

## 1. Typed-Language Prerequisite and Underlying FUN System (Section 5.1.1, Table 5.1)

Unlike Data Flow Analysis, Constraint-Based Analysis, and Abstract Interpretation, Type and Effect Systems
**demand** an underlying well-typed program because the syntax of types serves as the skeleton carrying analysis
properties (`G-U5a-01`) [PPA Chapter 5, p. 283] (book p. 283; PDF p. 300).

### 1.1 FUN Syntax with Abstraction-Site Points (Exp and Pnt)

Chapter 5 adapts `FUN` from [PPA §3.1, p. 142] (book p. 142; PDF p. 160), dropping universal expression labels
`ℓ ∈ Lab` and the separate category `Term`: because annotated types carry subexpression flow facts, program points
`π ∈ Pnt` attach **only** to function definitions (`G-U5a-02`) [PPA §5.1, p. 283] (book p. 283; PDF p. 300)
[PPA §5.1, p. 284] (book p. 284; PDF p. 301):

```text
e ::= c | x | fn_π x => e₀ | fun_π f x => e₀ | e₁ e₂
    | if e₀ then e₁ else e₂ | let x = e₁ in e₂ | e₁ op e₂
```

- **Distinct recursive binders (`G-U5a-09`)**: Every `fun_π f x => e₀` assumes `f ≠ x`
  [PPA §5.2.1, p. 293] (book p. 293; PDF p. 310).
- **Canonical witnesses**: Identity application `(fn_X x => x) (fn_Y y => y)` (`Example 5.1`) and diverging
  `loop` = `let g = (fun_F f x => f (fn_Y y => y)) in g (fn_Z z => z)` (`Example 5.2`)
  [PPA Example 5.1, p. 284] (book p. 284; PDF p. 301) [PPA Example 5.2, p. 284] (book p. 284; PDF p. 301).

### 1.2 Underlying Types (Type), List Environments (TEnv), and Table 5.1

```text
τ ∈ Type ::= int | bool | τ₁ → τ₂          Γ ∈ TEnv ::= [] | Γ[x ↦ τ]
```

- **Base-only constants and operators (`G-U5a-03`)**: Each `c ∈ Const` has `τ_c ∈ {int, bool}` and each binary
  `op ∈ Op` has `τ¹_op, τ²_op, τ_op ∈ {int, bool}` (zero arrow components)
  [PPA §5.1.1, p. 285] (book p. 285; PDF p. 302).
- **Rightmost-wins environment lookup**: `dom(Γ) = {x | Γ contains [x ↦ ···]}`; `Γ(x) = τ` iff `x ∈ dom(Γ)` and
  the *rightmost* entry for `x` in `Γ` is `[x ↦ τ]`; `Γ | X` deletes entries with `x ∉ X`
  [PPA §5.1.1, p. 285] (book p. 285; PDF p. 302) [PPA §5.1.1, p. 286] (book p. 286; PDF p. 303).
- **Complete `Table 5.1` (`Γ ⊢_UL e : τ`)** [PPA Table 5.1, p. 285] (book p. 285; PDF p. 302):

```text
[con]  Γ ⊢_UL c : τ_c                                  [var]  Γ ⊢_UL x : τ     (if Γ(x) = τ)

       Γ[x ↦ τ_x] ⊢_UL e₀ : τ₀                                Γ[f ↦ τ_x → τ₀][x ↦ τ_x] ⊢_UL e₀ : τ₀
[fn]   ---------------------------------               [fun]  -----------------------------------------
       Γ ⊢_UL fn_π x => e₀ : τ_x → τ₀                         Γ ⊢_UL fun_π f x => e₀ : τ_x → τ₀

       Γ ⊢_UL e₁ : τ₂ → τ₀    Γ ⊢_UL e₂ : τ₂                  Γ ⊢_UL e₀ : bool   Γ ⊢_UL e₁ : τ   Γ ⊢_UL e₂ : τ
[app]  ----------------------------------------        [if]   -------------------------------------------------
       Γ ⊢_UL e₁ e₂ : τ₀                                      Γ ⊢_UL if e₀ then e₁ else e₂ : τ

       Γ ⊢_UL e₁ : τ₁    Γ[x ↦ τ₁] ⊢_UL e₂ : τ₂               Γ ⊢_UL e₁ : τ¹_op    Γ ⊢_UL e₂ : τ²_op
[let]  ------------------------------------------      [op]   ----------------------------------------
       Γ ⊢_UL let x = e₁ in e₂ : τ₂                           Γ ⊢_UL e₁ op e₂ : τ_op
```

- **Nondeterminism vs `[external: Church-style]` (`Exercise 5.2`) & Monomorphic `let` (`G-U5a-04`)**:
  - `Table 5.1` guesses `τ_x` in `[fn]`/`[fun]` (`[] ⊢_UL loop : τ → τ` for every `τ ∈ Type`, `Example 5.3`
    [PPA Example 5.3, p. 286] (book p. 286; PDF p. 303)); explicit parameter types `fn_π x : τ_x => e₀` and
    `fun_π f : (τ_x → τ₀) x => e₀` make `⊢_UL` deterministic (`τ₁ = τ₂`)
    [PPA Exercise 5.2, p. 359] (book p. 359; PDF p. 376).
  - `[let]` in `§§5.1–5.3` is **strictly monomorphic**: `let x = e₁ in e₂` admits the exact same typings as
    `(fn_π x => e₂) e₁` regardless of `π` (`let`-polymorphism is deferred to `§§5.4–5.5`)
    [PPA §5.1.1, p. 286] (book p. 286; PDF p. 303).
  - Untypable terms such as `fn_X x => x x` have no `⊢_UL` derivation (`G-U5a-01`), whereas Chapter 3 `0-CFA`
    analyses them cleanly in [cfa-core-and-coinduction.md](../../ppa-control-flow-and-constraints/references/cfa-core-and-coinduction.md)
    and [constraint-generation-and-cubic-solver.md](../../ppa-control-flow-and-constraints/references/constraint-generation-and-cubic-solver.md) (canonical **`U8`**).

## 2. Annotated Types, Subeffecting CFA, and UCAI Equality (Section 5.1.2, Tables 5.2-5.3)

Each function arrow is decorated with an annotation `φ ∈ Ann` naming the abstractions `π ∈ Pnt` that may flow to
that arrow [PPA §5.1.2, p. 287] (book p. 287; PDF p. 304):

```text
φ ∈ Ann   ::= {π} | φ₁ ∪ φ₂ | ∅                 τ̂ ∈ Typê ::= int | bool | τ̂₁ --φ--> τ̂₂
Γ̂ ∈ TEnv̂  ::= [] | Γ̂[x ↦ τ̂]                     ⌊int⌋ = int,  ⌊bool⌋ = bool,  ⌊τ̂₁ --φ--> τ̂₂⌋ = ⌊τ̂₁⌋ → ⌊τ̂₂⌋
```

### 2.1 Table 5.2 (CFA Typing) and Table 5.3 (UCAI Equality)

`Table 5.2` lifts `Table 5.1` to `Typê` and `TEnv̂` (`F-U5a-01` notes unhatted `τ₁, τ₂` on p. 290)
[PPA Table 5.2, p. 288] (book p. 288; PDF p. 305):

```text
[con]  Γ̂ ⊢_CFA c : τ_c                                 [var]  Γ̂ ⊢_CFA x : τ̂     (if Γ̂(x) = τ̂)

       Γ̂[x ↦ τ̂_x] ⊢_CFA e₀ : τ̂₀                               Γ̂[f ↦ τ̂_x --{π}∪φ--> τ̂₀][x ↦ τ̂_x] ⊢_CFA e₀ : τ̂₀
[fn]   -----------------------------------------       [fun]  ------------------------------------------------------
       Γ̂ ⊢_CFA fn_π x => e₀ : τ̂_x --{π}∪φ--> τ̂₀               Γ̂ ⊢_CFA fun_π f x => e₀ : τ̂_x --{π}∪φ--> τ̂₀

       Γ̂ ⊢_CFA e₁ : τ̂₂ --φ--> τ̂₀    Γ̂ ⊢_CFA e₂ : τ̂₂           Γ̂ ⊢_CFA e₀ : bool   Γ̂ ⊢_CFA e₁ : τ̂   Γ̂ ⊢_CFA e₂ : τ̂
[app]  -------------------------------------------------- [if] ------------------------------------------------------
       Γ̂ ⊢_CFA e₁ e₂ : τ̂₀                                     Γ̂ ⊢_CFA if e₀ then e₁ else e₂ : τ̂

       Γ̂ ⊢_CFA e₁ : τ̂₁    Γ̂[x ↦ τ̂₁] ⊢_CFA e₂ : τ̂₂            Γ̂ ⊢_CFA e₁ : τ¹_op    Γ̂ ⊢_CFA e₂ : τ²_op
[let]  ----------------------------------------------  [op]   ------------------------------------------
       Γ̂ ⊢_CFA let x = e₁ in e₂ : τ̂₂                          Γ̂ ⊢_CFA e₁ op e₂ : τ_op
```

`Table 5.3` axiomatises set equality `UCAI` (*unit, commutativity, associativity, idempotence*) on `Ann`
[PPA Table 5.3, p. 290] (book p. 290; PDF p. 307):

```text
[unit] φ = φ ∪ ∅       [idem] φ = φ ∪ φ       [com] φ₁ ∪ φ₂ = φ₂ ∪ φ₁       [ass] φ₁ ∪ (φ₂ ∪ φ₃) = (φ₁ ∪ φ₂) ∪ φ₃
[ref]  φ = φ           [trans] φ₁ = φ₂ ∧ φ₂ = φ₃ ⟹ φ₁ = φ₃                  [cong] φ₁ = φ'₁ ∧ φ₂ = φ'₂ ⟹ φ₁ ∪ φ₂ = φ'₁ ∪ φ'₂
```

Lifted structurally to `Typê` by `(τ̂₁ = τ̂'₁ ∧ τ̂₂ = τ̂'₂ ∧ φ = φ') ⟹ (τ̂₁ --φ--> τ̂₂) = (τ̂'₁ --φ'--> τ̂'₂)` (subset
inclusion `φ₁ ⊆ φ₂` modulo `UCAI` is axiomatised directly in [PPA Exercise 5.3, p. 359] (book p. 359; PDF p. 376)).

### 2.2 Whole-Tree Recovery, Bidirectional Smearing, and Conservative Extension (Fact 5.6)

1. **Whole-tree `Ĉ(ℓ)` recovery (`Example 5.4`, `G-U5a-02`)**: On `((fn_X x => x¹)² (fn_Y y => y³)⁴)⁵` with
   `τ̂_Y = int --{Y}--> int`, the root judgement `[] ⊢_CFA e : τ̂_Y` drops `{X}`! Recovering full control-flow
   cache `Ĉ(ℓ)` requires the **entire inference tree** (restored from rendered PDF page 306 where OCR drops it,
   `G-U5a-22`) [PPA Example 5.4, p. 288] (book p. 288; PDF p. 305)
   [PPA Example 5.4, p. 289] (book p. 289; PDF p. 306):

   | Subexpression `ℓ` | `1` (`x¹`) | `2` (`fn_X x => x¹`) | `3` (`y³`) | `4` (`fn_Y y => y³`) | `5` (whole application) |
   | :--- | :--- | :--- | :--- | :--- | :--- |
   | Resolved `Ĉ(ℓ)` | `τ̂_Y` | `τ̂_Y --{X}--> τ̂_Y` | `int` | `τ̂_Y` | `τ̂_Y` |

2. **Mandatory subeffecting & bidirectional smearing (`Example 5.5`, `Exercise 5.1`, `G-U5a-05`, `G-U5a-06`)**:
   Because `[app]` demands exact equality `τ̂₂` without subtyping, passing `fn_Y` and `fn_Z` into `loop`'s `g`
   (or `g` and `h` into `f` in [PPA Exercise 5.1, p. 359] (book p. 359; PDF p. 376)) forces **both** closures to
   widen via `{π} ∪ φ` to `τ̂ --{Y, Z}--> τ̂` (`bidirectional smearing`), whereas `loop`'s return arrow types as
   `[] ⊢_CFA loop : τ̂ --∅--> τ̂` (`G-U5a-08`) [PPA Example 5.5, p. 289] (book p. 289; PDF p. 306)
   [PPA Example 5.5, p. 290] (book p. 290; PDF p. 307).
3. **Conservative extension (`Fact 5.6`, `G-U5a-05`, `G-U5a-07`)**:
   - `(i)` `Γ̂ ⊢_CFA e : τ̂ ⟹ ⌊Γ̂⌋ ⊢_UL e : ⌊τ̂⌋` (erasure).
   - `(ii)` `Γ ⊢_UL e : τ ⟹ ∃Γ̂, τ̂ : Γ̂ ⊢_CFA e : τ̂ ∧ ⌊Γ̂⌋ = Γ ∧ ⌊τ̂⌋ = τ` (proved by annotating every arrow with
     `Pnt_e` using `{π} ∪ Pnt_e = Pnt_e`; without `∪ φ` in `[fn]`/`[fun]`, `Example 5.5` has **no** `⊢_CFA`
     typing!) [PPA Fact 5.6, p. 291] (book p. 291; PDF p. 308).
   - Syntax-directed `⊢_CFA` must type unreachable `if` branches and dead functions (`G-U5a-07`).

## 3. Environment-Free Natural Semantics and Subject Reduction (Sections 5.2.1-5.2.2, Table 5.4)

### 3.1 Closed Big-Step Evaluation (Table 5.4 and Display 5.1)

Because subexpression labels `ℓ` are absent, Section 5.2.1 evaluates **closed** expressions (`FV(e) = ∅`) to
closed values `v ∈ Val ::= c | fn_π x => e₀` (`FV(fn_π x => e₀) = ∅`) via `⊢ e ⟶ v` (`[con]` and `[if₁]`/`[if₂]`
restored from rendered PDF page 309, `G-U5a-22`) [PPA Table 5.4, p. 292] (book p. 292; PDF p. 309):

```text
[con]  ⊢ c ⟶ c                                  [fn]   ⊢ (fn_π x => e₀) ⟶ (fn_π x => e₀)
[fun]  ⊢ (fun_π f x => e₀) ⟶ fn_π x => (e₀[f ↦ fun_π f x => e₀])
[app]  ⊢ e₁ ⟶ (fn_π x => e₀) ∧ ⊢ e₂ ⟶ v₂ ∧ ⊢ e₀[x ↦ v₂] ⟶ v₀  ⟹  ⊢ e₁ e₂ ⟶ v₀
[if₁]  ⊢ e₀ ⟶ true  ∧ ⊢ e₁ ⟶ v₁  ⟹  ⊢ if e₀ then e₁ else e₂ ⟶ v₁
[if₂]  ⊢ e₀ ⟶ false ∧ ⊢ e₂ ⟶ v₂  ⟹  ⊢ if e₀ then e₁ else e₂ ⟶ v₂
[let]  ⊢ e₁ ⟶ v₁ ∧ ⊢ e₂[x ↦ v₁] ⟶ v₂  ⟹  ⊢ let x = e₁ in e₂ ⟶ v₂
[op]   ⊢ e₁ ⟶ v₁ ∧ ⊢ e₂ ⟶ v₂  ⟹  ⊢ e₁ op e₂ ⟶ v                     (if v₁ op v₂ = v)
```

- **Key structural preconditions (`G-U5a-09`, `G-U5a-10`, `G-U5a-11`, `BKL-004`)**:
  1. `fun_π f x => e₀` is **not** in `Val`; `[fun]` unfolds it one step into an ordinary `fn_π` **inheriting the
     exact same point `π`**, so `[app]` needs only one rule (`Example 5.7`
     [PPA Example 5.7, p. 293] (book p. 293; PDF p. 310)).
  2. Substitution `e₁[x ↦ e₂]` avoids `α`-renaming **solely** because `Table 5.4` evaluates closed terms, keeping
     every substituted `e₂` closed (`FV(e₂) = ∅`) [PPA §5.2.1, p. 293] (book p. 293; PDF p. 310).
  3. **Divergence vacuity (`Example 5.8`, `(5.1)`, `BKL-004`)**: Evaluating `loop` requires finite sub-derivation
     `⊢ (fun_F f x => f (fn_Y y => y)) (fn_Y y => y) ⟶ v` `(5.1)` containing `(5.1)` strictly inside itself;
     non-termination equals *absence of any finite derivation tree*
     [PPA Example 5.8, p. 294] (book p. 294; PDF p. 311).

### 3.2 Subject Reduction (Theorem 5.9), Fact 5.10, and Lemma 5.11

Assuming operator compatibility (`[] ⊢_CFA v₁ : τ¹_op ∧ [] ⊢_CFA v₂ : τ²_op ⟹ [] ⊢_CFA v₁ op v₂ : τ_op`)
[PPA §5.2.2, p. 294] (book p. 294; PDF p. 311):

- **`Theorem 5.9` (Subject Reduction)**: `If [] ⊢_CFA e : τ̂ and ⊢ e ⟶ v then [] ⊢_CFA v : τ̂`
  [PPA Theorem 5.9, p. 295] (book p. 295; PDF p. 312) (printed corollaries on p. 295 omit `CFA` subscript on `⊢`,
  `F-U5a-02`, `G-U5a-22`):
  - **Call/return safety**: `[] ⊢_CFA e : τ̂₁ --φ₀--> τ̂₂ ∧ ⊢ e ⟶ fn_π x => e₀ ⟹ π ∈ φ₀`.
  - **Static non-termination certificate (`G-U5a-08`)**: `[] ⊢_CFA e : τ̂₁ --∅--> τ̂₂` proves `e` **cannot
    terminate** (`π ∈ ∅` is impossible).
  - **Reactive/daemon caveat (`G-U5a-11`, `BKL-004`)**: Because `⊢ e ⟶ v` is empty when `e` diverges, `Theorem 5.9`
    says **nothing** about intermediate calls or side channels inside non-terminating loops!
- **Proof machinery (`Fact 5.10`, `Lemma 5.11`)**:
  - `Fact 5.10` (free-variable invariance): `Γ̂₁ ⊢_CFA e : τ̂ ∧ (∀x ∈ FV(e) : Γ̂₁(x) = Γ̂₂(x)) ⟹ Γ̂₂ ⊢_CFA e : τ̂`
    [PPA Fact 5.10, p. 295] (book p. 295; PDF p. 312).
  - `Lemma 5.11` (closed substitution): `[] ⊢_CFA e₀ : τ̂₀ ∧ Γ̂[x ↦ τ̂₀] ⊢_CFA e : τ̂ ⟹ Γ̂ ⊢_CFA e[x ↦ e₀] : τ̂`
    (induction on `e`; `Theorem 5.9`'s `[fun]` case relies on `f ≠ x` to commute `[f ↦ ···][x ↦ τ̂_x]`)
    [PPA Lemma 5.11, p. 295] (book p. 295; PDF p. 312) [PPA §5.2.2, p. 296] (book p. 296; PDF p. 313).

## 4. Covariant Fibre Lattice and Moore-Family Solutions (Section 5.2.3)

To define a "best" (least) annotated typing over a fixed underlying derivation `Γ ⊢_UL e : τ`:

- **Complete annotation lattice (`G-U5a-13`)**: Order `φ₁ ⊑ φ₂` (or `φ₁ ⊆ φ₂`) iff `∃φ' : φ₁ ∪ φ' = φ₂` modulo
  `UCAI`. Because syntactic `Ann` denotes only *finite* sets, `(Ann, ⊑)` is a complete lattice (`⊓ ∅ = Pnt`)
  only after restricting `Pnt` to finite `Pnt_⋆` or enlarging `Ann` to `(𝒫(Pnt), ⊆)`
  [PPA §5.2.3, p. 298] (book p. 298; PDF p. 315).
- **Covariant fibre order `⊑` on `Typê[τ] = {τ̂ ∈ Typê | ⌊τ̂⌋ = τ}` (`G-U5a-12`)**:
  ```text
                 τ̂₁ ⊑ τ̂'₁    φ ⊆ φ'    τ̂₂ ⊑ τ̂'₂
  τ̂ ⊑ τ̂          -----------------------------------       (τ̂₁ --φ--> τ̂₂) ⊓ (τ̂'₁ --φ'--> τ̂'₂) = (τ̂₁ ⊓ τ̂'₁) --(φ ∩ φ')--> (τ̂₂ ⊓ τ̂'₂)
                 (τ̂₁ --φ--> τ̂₂) ⊑ (τ̂'₁ --φ'--> τ̂'₂)
  ```
  Least and greatest fibre elements per underlying `τ` [PPA §5.2.3, p. 298] (book p. 298; PDF p. 315)
  [PPA §5.2.3, p. 299] (book p. 299; PDF p. 316):
  ```text
  ⊥_int = int,   ⊥_bool = bool,   ⊥_{τ₁→τ₂} = ⊥_{τ₁} --∅--> ⊥_{τ₂}
  ⊤_int = int,   ⊤_bool = bool,   ⊤_{τ₁→τ₂} = ⊤_{τ₁} --Pnt--> ⊤_{τ₂}
  ```
  **Critical variance distinction**: `⊑` is **covariant in BOTH argument `τ̂₁` and result `τ̂₂`**, measuring
  precision across equational derivations — **never** confuse `⊑` with Section 5.4's **contravariant** subtyping
  order `≤` (`τ̂'₁ ≤ τ̂₁`), which would cause `[external: CWE-843 higher-order type/taint confusion]` if inverted!
- **`Proposition 5.12` (Moore family)**: For every `Γ ⊢_UL e : τ`, define the judgement fibre
  `JUDG_CFA[Γ ⊢_UL e : τ] = {(Γ̂ ⊢_CFA e : τ̂) | Γ̂ ⊢_CFA e : τ̂ ∧ ⌊Γ̂⌋ = Γ ∧ ⌊τ̂⌋ = τ}` ordered componentwise by
  `(Γ̂₁ ⊢_CFA e : τ̂₁) ⊑ (Γ̂₂ ⊢_CFA e : τ̂₂) ⟺ (∀x ∈ dom(Γ) : Γ̂₁(x) ⊑ Γ̂₂(x)) ∧ (τ̂₁ ⊑ τ̂₂)`.
  `Proposition 5.12` proves `JUDG_CFA[Γ ⊢_UL e : τ]` is a **Moore family** (`∀Y ⊆ JUDG_CFA[···] : ⨅ Y ∈ JUDG_CFA[···]`):
  - When `Y = ∅`, `⨅ ∅` annotates every arrow in `Γ` and `τ` with `Pnt`, which is derivable by `Fact 5.6(ii)`'s
    coarse construction (`{π} ∪ Pnt = Pnt`);
  - When `Y ≠ ∅`, structural induction on `Γ ⊢_UL e : τ` intersects derivations pointwise (`F-U5a-02` notes missing
    `CFA` subscripts in `[app]` on p. 300), relying on `{π} ∪ (⋂_i φ^i) = ⋂_i ({π} ∪ φ^i)` in `[fn]` and `[fun]`
    [PPA Proposition 5.12, p. 299] (book p. 299; PDF p. 316) [PPA Proposition 5.12, p. 300] (book p. 300; PDF p. 317).
- **Open-expression precision (`Example 5.13`)**: On `e = f (fn_X x => x+1) + f (fn_Y y => y+2) + (fn_Z z => z+3)(4)`
  over `[f ↦ (int → int) → int] ⊢_UL e : int`:
  ```text
  Valid judgements : [f ↦ (int --φ₁--> int) --φ₂--> int] ⊢_CFA e : int     iff {X, Y} ⊆ φ₁
  Least judgement  : [f ↦ (int --{X,Y}--> int) --∅--> int] ⊢_CFA e : int   (certifies f never receives fn_Z)
  ```
  [PPA Example 5.13, p. 300] (book p. 300; PDF p. 317).

### Proof Architecture Summary (`Section 5.2.2`, `Lemma 5.11` -> `Theorem 5.9`)

| Step | Statement & Induction Measure | Critical Side Condition |
| :--- | :--- | :--- |
| `Fact 5.10` | `Γ̂₁ ⊢_CFA e : τ̂ ∧ (∀x ∈ FV(e) : Γ̂₁(x) = Γ̂₂(x)) ⟹ Γ̂₂ ⊢_CFA e : τ̂` (structural on `e`) | Rightmost-wins lookup in `Γ̂[x ↦ τ̂_x]` shadows outer `x` [PPA Fact 5.10, p. 295] (book p. 295; PDF p. 312) |
| `Lemma 5.11` | `[] ⊢_CFA e₀ : τ̂₀ ∧ Γ̂[x ↦ τ̂₀] ⊢_CFA e : τ̂ ⟹ Γ̂ ⊢_CFA e[x ↦ e₀] : τ̂` (structural on `e`) | `[] ⊢_CFA e₀ : τ̂₀` forces `FV(e₀) = ∅`, preventing variable capture [PPA Lemma 5.11, p. 296] (book p. 296; PDF p. 313) |
| `Theorem 5.9` | `[] ⊢_CFA e : τ̂ ∧ ⊢ e ⟶ v ⟹ [] ⊢_CFA v : τ̂` (shape of `⊢ e ⟶ v` tree) | `f ≠ x` in `[fun]`; `op` compatibility; vacuous when `⊢ e ⟶ v` absent (`BKL-004`) [PPA Theorem 5.9, p. 295] (book p. 295; PDF p. 312) |

## 5. End-Matter Refinements and Non-Blocking Backlog Pointers (Exercises 5.1-5.7, 5.10)

| Exercise | Refinement & Soundness Mechanism | Source Coordinate |
| :--- | :--- | :--- |
| `Exercise 5.1` | `(f g) + (f h)` forces monomorphic smearing `g, h : int →^{Y,Z} int` in `Table 5.2` | [PPA Exercise 5.1, p. 359] (book p. 359; PDF p. 376) |
| `Exercise 5.2` | `[external: Church-style]` `fn_π x : τ_x => e₀` restores `⊢_UL` determinism `τ₁ = τ₂` | [PPA Exercise 5.2, p. 359] (book p. 359; PDF p. 376) |
| `Exercise 5.3` | Direct `[external: Horn]` axiomatisation of subset inclusion `φ₁ ⊆ φ₂` modulo `UCAI` | [PPA Exercise 5.3, p. 359] (book p. 359; PDF p. 376) |
| `Exercise 5.5` | Dead-call `[app]` returning `⊥_{τ̂₀}` when `φ = ∅` preserves `Theorem 5.9` vacuously | [PPA Exercise 5.5, p. 360] (book p. 360; PDF p. 377) |
| `Exercise 5.6` | Dual arrows `τ̂₁ →^φ_ψ τ̂₂` (`ψ ∈ LAnn`) track call-site labels `(e₁ e₂)^ℓ` (`F-U5b-13`) | [PPA Exercise 5.6, p. 360] (book p. 360; PDF p. 377) |
| `Exercise 5.7` | `Table 5.2` stays sound unchanged under call-by-name `Table 5.4` (`[app]`, `[let]`) | [PPA Exercise 5.7, p. 361] (book p. 361; PDF p. 378) |
| `Exercise* 5.10` | `𝒲_UL([], fun_F f x => e₀) = (α_x → α₀, θ)` (`α_x ≠ α₀`) proves `(fun_F ···) e` diverges | [PPA Exercise 5.10, p. 361] (book p. 361; PDF p. 378) |

- **Backlog pointers**: `BKL-004` (`Table 5.4` big-step Natural Semantics divergence vacuity, `G-U5a-11`);
  `BKL-011` (`PDF` OCR erasures in `Example 5.4` p. 289 and `Table 5.4` p. 292, plus printed subscript omissions
  `F-U5a-01`, `F-U5a-02` catalogued in `G-U5a-22`); `BKL-075` (typed-substrate `⊢_UL` gate, monomorphic `let`,
  whole-tree `(5.2)`, smearing, and divergence vacuity); `BKL-076` (finite `Pnt_⋆` / covariant `⊑` in `Prop 5.12`
  vs contravariant `≤` breakdown in `Exercise 5.9`); and `BKL-077` (`F-U5a-01..02` subscript omissions).

## 6. Worked Derivation Witnesses (`Examples 5.1-5.5`, `5.8`, `5.13`)

| Witness | Expression & Underlying Skeleton | Annotated `⊢_CFA` / Semantic Outcome | Key Soundness or Precision Lesson |
| :--- | :--- | :--- | :--- |
| `Example 5.1` | `(fn_X x => x) (fn_Y y => y)` (`τ = int → int`) | `τ̂_Y = int --{Y}--> int`; `τ̂_X = τ̂_Y --{X}--> τ̂_Y` | Demonstrates abstraction-only program points `π ∈ {X, Y}` vs universal labels `ℓ` [PPA Example 5.1, p. 284] (book p. 284; PDF p. 301) |
| `Example 5.2` | `loop = let g = (fun_F f x => f (fn_Y y => y)) in g (fn_Z z => z)` | `g : (int → int) → (int → int)` (`⊢_UL`); non-terminating | Canonical recursion & divergence benchmark reused across `Examples 5.5, 5.8, 5.19` [PPA Example 5.2, p. 284] (book p. 284; PDF p. 301) |
| `Example 5.3` | Underlying derivation `[] ⊢_UL loop : τ → τ` (`Example 5.2` `loop`) | Holds for every `τ ∈ Type` via `g : (τ → τ) → (τ → τ)` | Proves `⊢_UL` is nondeterministic (`Exercise 5.2` restores uniqueness) [PPA Example 5.3, p. 286] (book p. 286; PDF p. 303) [PPA Example 5.3, p. 287] (book p. 287; PDF p. 304) |
| `Example 5.4` | Annotated tree for `Example 5.1` (`τ̂_Y = int --{Y}--> int`) | Root yields `τ̂_Y`, while `[app]` sub-premise exposes `{X}` | Root type drops inner call arrows; full tree (`(5.2)`) is required (`G-U5a-02`) [PPA Example 5.4, p. 289] (book p. 289; PDF p. 306) |
| `Example 5.5` | Annotated tree for `loop` (`Example 5.2`) | Parameter arrow forces `{Y, Z}`; return arrow admits `--∅-->` | Shows `{π} ∪ φ` necessity (`G-U5a-05`), smearing (`G-U5a-06`), and `--∅-->` divergence (`G-U5a-08`) [PPA Example 5.5, p. 289] (book p. 289; PDF p. 306) |
| `Example 5.8` | Big-step evaluation of `Example 5.1` vs `loop` | `⊢ e_1 ⟶ fn_Y y => y`; `loop` has no `⊢ loop ⟶ v` tree | Illustrates closed substitution without alpha-renaming and divergence vacuity (`(5.1)`) [PPA Example 5.8, p. 294] (book p. 294; PDF p. 311) |
| `Example 5.13` | `f (fn_X x => x+1) + f (fn_Y y => y+2) + (fn_Z z => z+3)(4)` | Least judgement `[f ↦ (int --{X,Y}--> int) --∅--> int] ⊢_CFA e : int` | Least element of covariant Moore family separates `{X, Y}` from `fn_Z` [PPA Example 5.13, p. 300] (book p. 300; PDF p. 317) |

### Checklist for Auditing Custom Annotated Type Systems (`§§5.1-5.2`)

1. **Conservative extension check (`Fact 5.6`)**: Test whether replacing every annotation by `Pnt` (or `⊤`) makes every
   `⊢_UL` derivation lift mechanically into `⊢_CFA`; if a recursive function (`Example 5.5`) fails to lift, embedded
   subeffecting (`{π} ∪ φ`) or `[sub]` is missing (`G-U5a-05`).
2. **Substitution-lemma hygiene (`Lemma 5.11`)**: Confirm `[] ⊢ e₀ : τ̂₀` enforces closed `e₀`, confirm `Γ̂[x ↦ τ̂_x]`
   shadows rightmost-wins, and confirm `fun_π f x => e₀` enforces `f ≠ x` (`G-U5a-04`, `G-U5a-10`).
3. **Moore-family meet check (`Proposition 5.12`)**: Verify every annotation constructor in rules distributes over
   arbitrary intersections (`{π} ∪ ⋂_i φ^i = ⋂_i ({π} ∪ φ^i)`) and that domain positions remain **covariant** in the
   precision order `⊑` (`G-U5a-12`, `G-U5a-13`).
