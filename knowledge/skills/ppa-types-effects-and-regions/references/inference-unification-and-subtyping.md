<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Chapter 5 L1 reference for W_UL/W_CFA reconstruction, free-algebra SType unification, constraint solving, polarised subtyping, and canonical U8 0-CFA correspondence (Sections 5.3-5.4). -->

# Type and Annotation Inference, Free-Algebra Unification, and Subtyping

Scope: Section 5.3 (`§§5.3.1–5.3.4`), Section 5.4 subtyping core (`§5.4.1`, `pp. 324–325`), Concluding Remarks
(`pp. 349–352`), Mini Project `5.3`, and Exercises `5.4*`, `5.8`, `5.9`, `5.13` —
[PPA §5.3, p. 300] (book p. 300; PDF p. 317) through [PPA §5.3.4, p. 319] (book p. 319; PDF p. 336), plus
[PPA §5.4.1, p. 324] (book p. 324; PDF p. 341), [PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367)
through [PPA Chapter 5 Concluding Remarks, p. 352] (book p. 352; PDF p. 369),
[PPA Mini Project 5.3, p. 355] (book p. 355; PDF p. 372), and [PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376)
through [PPA Exercise 5.13, p. 362] (book p. 362; PDF p. 379).
Ground truth: `corpus/shards/RAW_SHARD_05a_annotated_types_inference.md` and
`corpus/shards/RAW_SHARD_05b_effects_regions_behaviours.md`.
Declarative `⊢_UL`/`⊢_CFA` rules and `Theorem 5.9` live in
[annotated-types-and-cfa-soundness.md](./annotated-types-and-cfa-soundness.md); concrete side-effect, exception,
region (`Figures 5.1–5.2`), and behaviour systems live in
[effects-exceptions-regions-and-behaviours.md](./effects-exceptions-regions-and-behaviours.md); Chapter 1
constraint/type previews live in
[chapter-1-five-formulations.md](../../ppa-program-analysis/references/chapter-1-five-formulations.md).

## 1. Underlying Type Reconstruction W_UL and Unification U_UL (Section 5.3.1, Tables 5.5-5.6)

To eliminate clairvoyant type guessing in `Table 5.1`, Section 5.3.1 introduces augmented types
`τ ∈ AType ::= int | bool | τ₁ → τ₂ | α` over type variables `α ∈ TVar` (`'a, 'b, ...`) and finite substitutions
`θ : TVar →_fin AType` (`(θ₁ ∘ θ₂) τ = θ₁(θ₂ τ)`) [PPA §5.3.1, p. 300] (book p. 300; PDF p. 317)
[PPA §5.3.1, p. 301] (book p. 301; PDF p. 318).

### 1.1 Syntactic Unification U_UL (Table 5.6)

First-order Robinson unification `𝒰_UL(τ₁, τ₂) = θ` (with arrow clause restored from rendered PDF
page 322, `G-U5a-22`) [PPA Table 5.6, p. 305] (book p. 305; PDF p. 322):

```text
𝒰_UL(int, int) = id                        𝒰_UL(bool, bool) = id
𝒰_UL(τ₁ → τ₂, τ'₁ → τ'₂) = let θ₁ = 𝒰_UL(τ₁, τ'₁); θ₂ = 𝒰_UL(θ₁ τ₂, θ₁ τ'₂) in θ₂ ∘ θ₁
𝒰_UL(τ, α) = [α ↦ τ]   if α does not occur in τ or if α equals τ   (else fail)
𝒰_UL(α, τ) = [α ↦ τ]   if α does not occur in τ or if α equals τ   (else fail)
𝒰_UL(τ₁, τ₂) = fail    in all other cases
```

- **Failure criterion (`G-U5a-01`, `G-U5a-17`)**: `𝒰_UL` fails **iff** top-level constructors (`int`, `bool`, `→`)
  clash or the **occurs check** rejects `α` properly inside an arrow type (rejecting `fn_X x => x x`). Note
  `α = τ` returns `[α ↦ α]`, which imperative `[external: union-find]` maps must short-circuit to `id` to avoid self-loops
  (`G-U5a-17`) [PPA Table 5.6, p. 305] (book p. 305; PDF p. 322) (`Example 5.15` traces
  `𝒰_UL('a → 'a, ('b → 'b) → 'c)` [PPA Example 5.15, p. 305] (book p. 305; PDF p. 322)).

### 1.2 Algorithm W_UL (Table 5.5) and the Missing theta_0 Erratum (G-U5a-14)

Monomorphic `[external: Damas–Milner]`-style reconstruction `𝒲_UL(Γ, e) = (τ, θ)` threads each new substitution
("retroactive law", `Analogy.` [PPA §5.3.1, p. 304] (book p. 304; PDF p. 321)) into subsequent recursive calls so
that `θ_G(θ Γ) ⊢_UL e : θ_G τ` holds for every covering ground `θ_G`
[PPA Table 5.5, p. 303] (book p. 303; PDF p. 320):

```text
𝒲_UL(Γ, c) = (τ_c, id)                                𝒲_UL(Γ, x) = (Γ(x), id)
𝒲_UL(Γ, fn_π x => e₀)      = let α_x fresh; (τ₀, θ₀) = 𝒲_UL(Γ[x ↦ α_x], e₀) in ((θ₀ α_x) → τ₀, θ₀)
𝒲_UL(Γ, fun_π f x => e₀)   = let α_x, α₀ fresh; (τ₀, θ₀) = 𝒲_UL(Γ[f ↦ α_x → α₀][x ↦ α_x], e₀);
                                  θ₁ = 𝒰_UL(τ₀, θ₀ α₀) in (θ₁(θ₀ α_x) → θ₁ τ₀, θ₁ ∘ θ₀)
𝒲_UL(Γ, e₁ e₂)             = let (τ₁, θ₁) = 𝒲_UL(Γ, e₁); (τ₂, θ₂) = 𝒲_UL(θ₁ Γ, e₂); α fresh;
                                  θ₃ = 𝒰_UL(θ₂ τ₁, τ₂ → α) in (θ₃ α, θ₃ ∘ θ₂ ∘ θ₁)
𝒲_UL(Γ, if e₀ then e₁ else e₂) =
    let (τ₀, θ₀) = 𝒲_UL(Γ, e₀); (τ₁, θ₁) = 𝒲_UL(θ₀ Γ, e₁); (τ₂, θ₂) = 𝒲_UL(θ₁(θ₀ Γ), e₂);
        θ₃ = 𝒰_UL(θ₂(θ₁ τ₀), bool); θ₄ = 𝒰_UL(θ₃ τ₂, θ₃(θ₂ τ₁))
    in  (θ₄(θ₃ τ₂), θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁)            (* ERRATUM F-U5a-04: omits ∘ θ₀; must be θ₄∘θ₃∘θ₂∘θ₁∘θ₀! *)
𝒲_UL(Γ, let x = e₁ in e₂)  = let (τ₁, θ₁) = 𝒲_UL(Γ, e₁); (τ₂, θ₂) = 𝒲_UL((θ₁ Γ)[x ↦ τ₁], e₂) in (τ₂, θ₂ ∘ θ₁)
𝒲_UL(Γ, e₁ op e₂)          = let (τ₁, θ₁) = 𝒲_UL(Γ, e₁); (τ₂, θ₂) = 𝒲_UL(θ₁ Γ, e₂);
                                  θ₃ = 𝒰_UL(θ₂ τ₁, τ¹_op); θ₄ = 𝒰_UL(θ₃ τ₂, τ²_op) in (τ_op, θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁)
```

- **Base-type operator invariance (`G-U5a-03`)**: `[op]` returns `τ_op` without `θ₄` because `τ_op ∈ {int, bool}`
  (`Example 5.14` traces `(fn_X x => x) (fn_Y y => y)` [PPA Example 5.14, p. 304] (book p. 304; PDF p. 321); p. 302
  mis-cites `[fn]` for `[fun]`, `F-U5a-03`).
- **Minimal counterexample to `Table 5.5` `if` (`F-U5a-04`, `G-U5a-14`)**: On `Γ = [b ↦ 'a]` and
  `e = if (b < 5) then 1 else 2`, `θ₀ = ['a ↦ int]` while `θ₁ = θ₂ = θ₃ = θ₄ = id`. Dropping `∘ θ₀` returns
  `(int, id)`, letting `θ_G = ['a ↦ bool]` violate `[b ↦ bool] ⊢_UL e : int` `[derived]`. Fixed in `Table 5.8`
  [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327).

## 2. Free-Algebra Simple Types SType, U_CFA, and W_CFA (Section 5.3.2, Tables 5.7-5.8)

### 2.1 Why Annotated Types Require Simple Types (G-U5a-15, G-U5a-16)

Because `UCAI` (`Table 5.3`) equates `int --{π₁}∪{π₂}--> int` with `int --{π₂}∪{π₁}--> int`, `Typê` is a
**non-free algebra** (`[external: ACUI unification]` is NP-complete and non-unitary). Section 5.3.2 recovers a
**free algebra** by restricting arrow slots inside types to single *annotation variables* `β ∈ AVar` (`'1, '2, ...`)
while deferring unions to inclusion constraints `C` (`SAnn` BNF restored from rendered p. 307, `G-U5a-22`)
[PPA §5.3.2, p. 306] (book p. 306; PDF p. 323) [PPA §5.3.2, p. 307] (book p. 307; PDF p. 324):

```text
τ̂ ∈ SType ::= int | bool | τ̂₁ --β--> τ̂₂ | α        φ ∈ SAnn ::= {π} | φ₁ ∪ φ₂ | ∅ | β
```

- **Simple substitutions (`G-U5a-15`)**: `θ` maps `TVar → SType` and **`AVar → AVar` only**, keeping `SType` closed.
- **`Table 5.7` (`𝒰_CFA`) and `Fact 5.17` (`G-U5a-16`, `Exercise 5.8`)**:
  ```text
  𝒰_CFA(int, int) = id                        𝒰_CFA(bool, bool) = id
  𝒰_CFA(τ̂₁ --β--> τ̂₂, τ̂'₁ --β'--> τ̂'₂) =
      let θ₀ = [β' ↦ β];  θ₁ = 𝒰_CFA(θ₀ τ̂₁, θ₀ τ̂'₁);  θ₂ = 𝒰_CFA(θ₁(θ₀ τ̂₂), θ₁(θ₀ τ̂'₂))
      in  θ₂ ∘ θ₁ ∘ θ₀
  𝒰_CFA(τ̂, α) = [α ↦ τ̂]   if α does not occur in τ̂ or if α equals τ̂   (else fail; symmetric for 𝒰_CFA(α, τ̂))
  ```
  `𝒰_CFA(τ̂₁, τ̂₂)` fails **iff** `𝒰_UL(⌊τ̂₁⌋, ⌊τ̂₂⌋)` fails (`AVar`s never fail occurs checks; `'a --'1--> ('b --'1--> 'c)`
  is valid). `Fact 5.17` proves soundness (`θ τ̂₁ = θ τ̂₂`) and MGU completeness (`θ'' = θ' ∘ θ`)
  [PPA Table 5.7, p. 307] (book p. 307; PDF p. 324) [PPA Fact 5.17, p. 308] (book p. 308; PDF p. 325)
  [PPA Exercise 5.8, p. 361] (book p. 361; PDF p. 378) (`Example 5.16` traces `𝒰_CFA`
  [PPA Example 5.16, p. 308] (book p. 308; PDF p. 325)).

### 2.2 Constraint Generation W_CFA (Table 5.8, G-U5a-18)

A constraint is `β ⊇ φ` (`β ∈ AVar, φ ∈ SAnn`), rewritten by simple `θ` as `θ C = {θ β ⊇ θ φ | (β ⊇ φ) ∈ C}`.
Ground validations `θ_G = θ_A ∘ θ_T = θ_T ∘ θ_A` combine ground `θ_T : TVar → Typê` and `θ_A : AVar → Ann`
covering `(Γ̂, τ̂, C)` with `θ_A ⊨ C` [PPA §5.3.2, p. 308] (book p. 308; PDF p. 325)
[PPA §5.3.2, p. 309] (book p. 309; PDF p. 326). `Table 5.8` defines `𝒲_CFA(Γ̂, e) = (τ̂, θ, C)` emitting **only
atomic inclusions `β ⊇ {π}`** [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327):

```text
𝒲_CFA(Γ̂, c) = (τ_c, id, ∅)                            𝒲_CFA(Γ̂, x) = (Γ̂(x), id, ∅)
𝒲_CFA(Γ̂, fn_π x => e₀)    = let α_x, β₀ fresh; (τ̂₀, θ₀, C₀) = 𝒲_CFA(Γ̂[x ↦ α_x], e₀)
                            in  ((θ₀ α_x) --β₀--> τ̂₀, θ₀, C₀ ∪ {β₀ ⊇ {π}})
𝒲_CFA(Γ̂, fun_π f x => e₀) = let α_x, α₀, β₀ fresh; (τ̂₀, θ₀, C₀) = 𝒲_CFA(Γ̂[f ↦ α_x --β₀--> α₀][x ↦ α_x], e₀);
                                θ₁ = 𝒰_CFA(τ̂₀, θ₀ α₀)
                            in  (θ₁(θ₀ α_x) --θ₁(θ₀ β₀)--> θ₁ τ̂₀, θ₁ ∘ θ₀, (θ₁ C₀) ∪ {θ₁(θ₀ β₀) ⊇ {π}})
𝒲_CFA(Γ̂, e₁ e₂)           = let (τ̂₁, θ₁, C₁) = 𝒲_CFA(Γ̂, e₁); (τ̂₂, θ₂, C₂) = 𝒲_CFA(θ₁ Γ̂, e₂); α, β fresh;
                                θ₃ = 𝒰_CFA(θ₂ τ̂₁, τ̂₂ --β--> α)
                            in  (θ₃ α, θ₃ ∘ θ₂ ∘ θ₁, θ₃(θ₂ C₁) ∪ θ₃ C₂)
𝒲_CFA(Γ̂, if e₀ then e₁ else e₂) =
    let (τ̂₀, θ₀, C₀) = 𝒲_CFA(Γ̂, e₀); (τ̂₁, θ₁, C₁) = 𝒲_CFA(θ₀ Γ̂, e₁); (τ̂₂, θ₂, C₂) = 𝒲_CFA(θ₁(θ₀ Γ̂), e₂);
        θ₃ = 𝒰_CFA(θ₂(θ₁ τ̂₀), bool); θ₄ = 𝒰_CFA(θ₃ τ̂₂, θ₃(θ₂ τ̂₁))   (* printed τ₁ unhatted, F-U5a-05 *)
    in  (θ₄(θ₃ τ̂₂), θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁ ∘ θ₀, θ₄(θ₃(θ₂(θ₁ C₀))) ∪ θ₄(θ₃(θ₂ C₁)) ∪ θ₄(θ₃ C₂))
𝒲_CFA(Γ̂, let x = e₁ in e₂) = let (τ̂₁, θ₁, C₁) = 𝒲_CFA(Γ̂, e₁); (τ̂₂, θ₂, C₂) = 𝒲_CFA((θ₁ Γ̂)[x ↦ τ̂₁], e₂)
                             in  (τ̂₂, θ₂ ∘ θ₁, (θ₂ C₁) ∪ C₂)
𝒲_CFA(Γ̂, e₁ op e₂)        = let (τ̂₁, θ₁, C₁) = 𝒲_CFA(Γ̂, e₁); (τ̂₂, θ₂, C₂) = 𝒲_CFA(θ₁ Γ̂, e₂);
                                θ₃ = 𝒰_CFA(θ₂ τ̂₁, τ¹_op); θ₄ = 𝒰_CFA(θ₃ τ̂₂, τ²_op)
                            in  (τ_op, θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁, θ₄(θ₃(θ₂ C₁)) ∪ θ₄(θ₃ C₂))
```

Note: in `if` line 2 above, `θ₃ = 𝒰_CFA(θ₂(θ₁ τ̂₀), bool)`; `Examples 5.18–5.19` trace `𝒲_CFA` (`Example 5.19`
reverses `[β' ↦ β]` orientation up to renaming, `F-U5a-06`, `G-U5a-22`)
[PPA Example 5.18, p. 311] (book p. 311; PDF p. 328) [PPA Example 5.19, p. 311] (book p. 311; PDF p. 328).
Every `θ_i` computed *after* a recursive call returning `C_j` MUST be applied to `C_j` (`G-U5a-18`).

## 3. Syntactic Soundness, Completeness, and Closed-Form theta_A (Sections 5.3.3-5.3.4)

- **`Theorem 5.20` (Syntactic Soundness, `G-U5a-19`)**: If `𝒲_CFA(Γ̂, e) = (τ̂, θ, C)` and `θ_G` is a ground
  validation of `(θ Γ̂, τ̂, C)`, then `θ_G(θ Γ̂) ⊢_CFA e : θ_G τ̂` (proved by extending `θ_G` to `θ'_G` covering
  eliminated intermediate types `θ₃(θ₂ τ̂₁)` and `θ₃ τ̂₂` at `[app]`)
  [PPA Theorem 5.20, p. 312] (book p. 312; PDF p. 329) [PPA Theorem 5.20, p. 313] (book p. 313; PDF p. 330).
- **`Theorem 5.21` (Syntactic Completeness, `G-U5a-20`, `Exercise 5.13`)**: If simple `Γ̂` and covering ground `θ'`
  satisfy `θ' Γ̂ ⊢_CFA e : τ̂'`, then there exist `τ̂, θ, C, θ_G` such that:
  1. `𝒲_CFA(Γ̂, e) = (τ̂, θ, C)`,
  2. `θ_G` is a ground validation of `θ Γ̂, τ̂, C`,
  3. `θ_G ∘ θ = θ'` except on fresh variables created by `𝒲_CFA(Γ̂, e)`, and
  4. `θ_G τ̂ = τ̂'` (`F-U5a-07` logs minor proof slips on pp. 315–316)
     [PPA Theorem 5.21, p. 314] (book p. 314; PDF p. 331) [PPA Theorem 5.21, p. 316] (book p. 316; PDF p. 333).
  Completeness avoids *proof normalisation* only because `Table 5.2` inlined `{π} ∪ φ` into `[fn]`/`[fun]`;
  standalone `[sub]` rules require `Exercise 5.13` two-step normalisation (absorbing `"∪ φ'"` into all rules, then
  restricting it solely to axioms `[con]/[var]/[deref]` and abstractions `[fn]/[fun]`, `G-U5b-23`)
  [PPA Exercise 5.13, p. 362] (book p. 362; PDF p. 379).
- **`Lemma 5.22`, `Corollary 5.23`, and Closed-Form `θ_A` (`G-U5a-21`, `G-U5b-01`, `Mini Project 5.3`)**:
  - For finite `X ⊇ AV(C)`, `{θ_A | θ_A ⊨ C ∧ dom(θ_A) = X}` is a **Moore family** under `(θ β) = ⋂_{θ_A ∈ Y} (θ_A β)`
    (intersections restored from rendered p. 318, `G-U5a-22`), holding for general monotone `φ ∈ SAnn` (reductive
    solutions in `Red`, [PPA §A.4, p. 402] (book p. 402; PDF p. 418)) and establishing `Corollary 5.23`
    [PPA Lemma 5.22, p. 317] (book p. 317; PDF p. 334) [PPA Corollary 5.23, p. 318] (book p. 318; PDF p. 335).
  - Because `𝒲_CFA` emits **only atomic `β ⊇ {π}`**, the least solution requires **zero fixed-point iteration**
    (`pp. 318–319`, concluding in the top 4 lines of p. 319 above `§5.4`, `G-U5b-01`):
    ```text
    θ_A β = {π | (β ⊇ {π}) ∈ C}   if β ∈ AV(C);     θ_A β = ∅   if β ∈ (AV(θ Γ̂) ∪ AV(τ̂)) \ AV(C)
    ```
    **Mandatory coverage guard (`F-U5a-08`, `F-U5b-01`, `G-U5a-21`)**: Printed `θ_A` sets `undefined` outside
    `AV(C)`, failing to cover unconstrained `'1` in `𝒲_CFA([], fn_X x => x 1)` unless defaulted to `∅` (with
    leftover `α ∈ TVar` mapped to `int` or `⊥_{τ_α}`, [PPA Mini Project 5.3, p. 355] (book p. 355; PDF p. 372))
    [PPA §5.3.4, p. 318] (book p. 318; PDF p. 335) [PPA §5.3.4, p. 319] (book p. 319; PDF p. 336).

## 4. Polarised Subtyping, Two-Stage Inference, and Canonical U8 (0-CFA Bridge)

### 4.1 Contravariant Subtyping vs Moore-Family Breakdown (G-U5b-05, G-U5b-07, G-U5b-22, Exercise 5.9)

Section 5.4 introduces **shape-conformant subtyping** `τ̂₁ ≤ τ̂₂` (`⌊τ̂₁⌋ = ⌊τ̂₂⌋`, mis-cited as `"Section 5.1"` on
p. 350 line 15, `F-U5b-11`, `G-U5b-22`) with **contravariant** arrow domains and **covariant** codomains/annotations
[PPA §5.4.1, p. 324] (book p. 324; PDF p. 341) [PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367):

```text
τ̂'₁ ≤ τ̂₁    τ̂₂ ≤ τ̂'₂    φ ⊆ φ'
─────────────────────────────────
  (τ̂₁ →^φ τ̂₂) ≤ (τ̂'₁ →^{φ'} τ̂'₂)
```

- **`Exercise 5.9` non-Moore answer (`G-U5b-07`) `[derived]`** (exercise answer, not book text): Although `(Typê[τ], ≤)` is a complete lattice (flipping
  meets/joins in contravariant slots), **`Proposition 5.12` FAILS under `≤`**! On `fn_X x => x` at
  `τ = (int → int) → (int → int)`, valid typings `(int →^φ int) →^{\{X\}} (int →^φ int)` for all `φ` have
  `≤`-meet `(int →^⊤ int) →^{\{X\}} (int →^∅ int)` — an **unsound non-typing**! Principal subtyped polymorphism
  therefore requires *constrained type schemes* `∀ζ⃗ [C]. τ̂` (`p. 350`, `[83, 160, 161]`)
  [PPA Exercise 5.9, p. 361] (book p. 361; PDF p. 378).
- **Two-stage inference for restricted effects (`pp. 351–352`, `G-U5b-12`)**: Whenever effects record **no type
  information** (`§§5.1, 5.4`), inference factors into Stage 1 (Hindley/Milner underlying types,
  keeping region/stack and pipeline topologies in `Figures 5.1–5.2` shape-fixed) followed by Stage 2 (decomposing
  `τ̂₁ ≤ τ̂₂` polarised inequalities into directed `[external: Horn clauses]` `β₁ ⊆ β₂` over `(𝒫(Pnt_⋆), ⊆)`)
  [PPA Chapter 5 Concluding Remarks, p. 351] (book p. 351; PDF p. 368).

### 4.2 Canonical U8 Unification: Chapter 5 Annotated Types and Chapter 3 Constraint 0-CFA

Grounded in [PPA Preface, p. VII] (book p. VII; PDF p. 7), [PPA §1.4, p. 11] (book p. 11; PDF p. 31),
[PPA §1.6, p. 19] (book p. 19; PDF p. 39), [PPA Example 5.4, p. 288] (book p. 288; PDF p. 305),
[PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367), and starred `Exercise* 5.4`
[PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376) [PPA Exercise 5.4, p. 360] (book p. 360; PDF p. 377); compare Chapter 3's
declarative and constraint-based `0-CFA` formulations in
[cfa-core-and-coinduction.md](../../ppa-control-flow-and-constraints/references/cfa-core-and-coinduction.md) and
[constraint-generation-and-cubic-solver.md](../../ppa-control-flow-and-constraints/references/constraint-generation-and-cubic-solver.md):

To bridge Chapter 5's unlabelled expressions directly to Chapter 3's per-label cache `Ĉ(ℓ)` and environment `ρ̂(x)`,
`Exercise* 5.4` simultaneously labels expressions `e ::= t^ℓ` (`t ::= c | x | fn_π x => e₀ | fun_π f x => e₀ | ···`)
and instruments `Table 5.2` with display `(5.2)` (formula restored from rendered p. 359, `G-U5b-26`):

```text
ρ̃, C̃; Γ̂ ⊢_CFA e : τ̂                                                   (5.2)
```

where `C̃(ℓ) = τ̂_ℓ` requires every sub-judgement at `t^ℓ` in `(5.2)` to derive `τ̂' = τ̂_ℓ`, and `ρ̃(x) = τ̂_x`
requires every variable lookup `x^ℓ` in `(5.2)` to derive `τ̂' = τ̂_x` (`Example 5.4` yields `C̃(1) = τ̂_Y`,
`C̃(2) = τ̂_Y →^{X} τ̂_Y`, `C̃(3) = int`, `C̃(4) = τ̂_Y`, `C̃(5) = τ̂_Y`, `ρ̃(x) = τ̂_Y`, `ρ̃(y) = int`).

| Axis | Equational `⊢_CFA` (`§§5.1–5.3`) | Subtyped `⊢_CFA + [sub]` (`§5.4`, `Exercises 5.4*, 5.9`) | Chapter 3 Constraint `0-CFA` (`Tables 3.1, 3.6`) |
| :--- | :--- | :--- | :--- |
| **Program scope** | `⊢_UL`-typable `FUN` (`G-U5a-01`) | `⊢_UL`-typable `FUN` (`[external: equi-recursive]` drops occurs check) | Arbitrary untyped `FUN` (accepts `fn x => x x`) |
| **Flow constraints** | Symmetric unification `[β' ↦ β]` + atomic `β ⊇ {π}` | Contravariant `τ̂'₁ ≤ τ̂₁` emits directed `β₁ ⊆ β₂` + `(5.2)` `ρ̃, C̃` | Conditional subset constraints `{t} ⊆ C(ℓ₁) ⇒ ···` (`Table 3.6`) |
| **Precision** | Bidirectional smearing (`Example 5.5`: `{Y,Z}`) | Exact directional parity with `0-CFA` on well-typed `FUN` (`[71]` Heintze; `[external: Palsberg–O'Keefe 1995]`) | Asymmetric call-site flow (`Example 3.4` separates `{id_y}` / `{id_z}`) |
| **Complexity** | `𝒰_CFA` (`[external]` near-linear only with union-find/DAG sharing) + `O(\|C\|)` bucket `θ_A` `[derived]` | Underlying HM + directed inclusion closure (`[external]` `O(n³)`) | `O(n³)` dynamic constraint-graph worklist (`Table 3.7`) |

### Subtyping Taxonomy and Proof-Normalisation Summary (`Concluding Remarks`, `Exercise 5.13`)

Section 5 Concluding Remarks (`p. 350`) classifies subtyped analysis systems into three expressiveness levels
[PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367):
1. **Shape-conformant subtyping (`§5.4`)**: `τ̂₁ ≤ τ̂₂ ⟹ ⌊τ̂₁⌋ = ⌊τ̂₂⌋` (zero subtyping in `⊢_UL`; solved cleanly
   in two stages whenever effects are restricted);
2. **Atomic subtyping**: partial order imposed on base types (`int ≤ real`), propagating structurally;
3. **General subtyping**: ordering across distinct type constructors, requiring explicit constraint sets in
   judgements (`∀ζ⃗ [C]. τ̂`, `[83, 160, 161]`).

When designing syntax-directed inference for subeffecting systems (`Exercise 5.13`
[PPA Exercise 5.13, p. 362] (book p. 362; PDF p. 379)):
- **Pass 1**: Eliminate standalone `[sub]` by appending `"∪ φ'"` to the effect of *every* axiom and rule conclusion;
- **Pass 2**: Push `"∪ φ'"` upward so slack appears **only** on leaf axioms (`[con]`, `[var]`, `[deref]`) and
  abstractions (`[fn]`, `[fun]`), aligning derivation tree shapes 1-to-1 with AST syntax trees (`G-U5a-20`, `G-U5b-23`).

## 5. Worked Unification and Reconstruction Traces (`Examples 5.14-5.19`)

| Example | Input Expression `e` | Computed Output `(τ̂, θ, C)` & Ground Least Typing | Source Coordinate |
| :--- | :--- | :--- | :--- |
| `Example 5.14` | `(fn_X x => x) (fn_Y y => y)` (`𝒲_UL`) | `('b → 'b, ['a ↦ 'b→'b]['c ↦ 'b→'b])` | [PPA Example 5.14, p. 304] (book p. 304; PDF p. 321) |
| `Example 5.16` | `𝒰_CFA('a --'1--> 'a, ('b --'2--> 'b) --'3--> 'c)` | `['3 ↦ '1]['a ↦ 'b --'2--> 'b]['c ↦ 'b --'2--> 'b]` | [PPA Example 5.16, p. 308] (book p. 308; PDF p. 325) |
| `Example 5.18` | `(fn_X x => x) (fn_Y y => y)` (`𝒲_CFA`) | `('b --'2--> 'b, θ₃, {'1 ⊇ {X}, '2 ⊇ {Y}})` -> `int --{Y}--> int` | [PPA Example 5.18, p. 311] (book p. 311; PDF p. 328) |
| `Example 5.19` | `loop` (`let g = fun_F ··· in g (fn_Z z => z)`) | `('d, θ, {'4 ⊇ {F}, '3 ⊇ {Y}, '3 ⊇ {Z}})`; `θ_T('d) = int --∅--> int` (`F-U5a-06`) | [PPA Example 5.19, p. 311] (book p. 311; PDF p. 328) |

- **Source errata & backlog summary (`BKL-011`, `BKL-073`, `BKL-074`, `BKL-076`, `BKL-077`, `BKL-082`)**:
  `Table 5.5` missing `∘ θ₀` (`p. 303`, `F-U5a-04`, `BKL-073`);
  `Table 5.6` arrow clause & `SAnn` BNF & `Lemma 5.22` intersections dropped in PDF OCR (`pp. 305, 307, 318`, `BKL-011`);
  `Table 5.8` unhatted `τ₁` (`p. 310`), `Example 5.19` reversed `[β' ↦ β]` (`p. 311`), `Theorem 5.21` slips (`pp. 315–316`),
  and `[α ↦ α]`/`[β ↦ β]` self-bindings (`BKL-077`); `θ_A` `AV(C)` domain gap (`pp. 318–319`, `F-U5a-08`, `F-U5b-01`, `BKL-074`);
  `Exercise 5.9` contravariant non-Moore witness (`BKL-076`); and `p. 350` mis-citing `Section 5.1` for `Section 5.4` +
  `Exercise 5.13` proof normalisation (`BKL-082`).

## 6. Proof-Case Audit Matrix (`Theorems 5.20-5.21`) and `Mini Project 5.3` Checklist

| Proof Obligation | Critical Inductive Case | Required Side Condition / Guard | Source Coordinate |
| :--- | :--- | :--- | :--- |
| `Fact 5.17` (`𝒰_CFA` mgu) | Arrow unification `τ̂₁ --β--> τ̂₂` vs `τ̂'₁ --β'--> τ̂'₂` | Emit `[β' ↦ β]` (or `id` when `β = β'`); never occurs-check `β ∈ AV(τ̂)` (`G-U5a-16`, `G-U5a-17`) | [PPA Fact 5.17, p. 308] (book p. 308; PDF p. 325) |
| `Theorem 5.20` (Soundness) | `[app]` case (`e₁ e₂`) | Extend `θ_G` to `θ'_G` covering eliminated fresh variables (`α₀, β₀`) while agreeing on `Γ̂, τ̂, C` (`G-U5a-19`) | [PPA Theorem 5.20, p. 312] (book p. 312; PDF p. 329) |
| `Theorem 5.20` (Soundness) | `[if]` case (`if e₀ then e₁ else e₂`) | Compose full chain `θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁ ∘ θ₀` and propagate `θ_i` across `C₀, C₁, C₂` (`G-U5a-14`, `G-U5a-18`) | [PPA Theorem 5.20, p. 314] (book p. 314; PDF p. 331) |
| `Theorem 5.21` (Completeness) | `[fn]` / `[fun]` cases | Works directly without proof normalisation only because `Table 5.2` embeds `{π} ∪ φ` (`G-U5a-20`) | [PPA Theorem 5.21, p. 314] (book p. 314; PDF p. 331) |
| `Lemma 5.22` & `Corollary 5.23` | Constraint solution lattice & `θ_A` | Intersect pointwise `(⨅_i θ_A^i)(β) = ⋂_i θ_A^i(β)`; totalise `θ_A` with `∅` on `X \ AV(C)` (`G-U5a-21`, `G-U5b-01`) | [PPA Lemma 5.22, p. 318] (book p. 318; PDF p. 335) [PPA Corollary 5.23, p. 318] (book p. 318; PDF p. 335) |

### Prototype Implementation Checklist (`Mini Project 5.3`)

When building `𝒲_CFA` in SML/Haskell/`[external: Rust]` (`[external: Tarjan union-find]`) per
[PPA Mini Project 5.3, p. 355] (book p. 355; PDF p. 372):
1. Represent `SType` with disjoint `TVar` and `AVar` ID namespaces so `𝒰_CFA` runs occurs-check on `TVar` only.
2. Short-circuit `find(a) == find(b)` to a no-op before linking `[external: union-find]` roots (`G-U5a-17`).
3. Maintain a side map `ast_node_id -> SType` during `𝒲_CFA` traversal so every subexpression's annotated arrow
   (`(5.2)`) is recovered after applying final `θ_G = θ_A ∘ θ_T` (`G-U5a-02`).
4. Collect atomic constraints `(find(β), π)` into per-root `[external: bitsets]` and initialise every root without constraints to `∅`
   before querying (`G-U5a-21`, `G-U5b-01`).
5. Run regression tests on `Examples 5.14, 5.16, 5.18, 5.19`, `Γ = [b ↦ 'a], if (b < 5) then 1 else 2` (`F-U5a-04`),
   and `fn_X x => x 1` (`F-U5a-08`).
