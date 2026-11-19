<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L1 formal reference for Chapter 4 §§4.1-4.2 mundane correctness relations, representation functions, Interval lattice, and widening/narrowing fixed-point approximation. -->

# Mundane Correctness Relations, Interval Lattice, and Widening/Narrowing Fixed Points

Self-contained formal reference for Chapter 4 opening, §4.1 (*A Mundane Approach to Correctness*: §§4.1.1–4.1.3),
§4.2 (*Approximation of Fixed Points*: §§4.2.1–4.2.2), and Exercises 4.1–4.12 of *Principles of Program Analysis*
([PPA Chapter 4, p. 211] (book p. 211; PDF p. 228) through [PPA §4.2.2, p. 233] (book p. 233; PDF p. 250), plus
[PPA Figure 4.10, p. 276] (book p. 276; PDF p. 293) and [PPA Exercise 4.1, p. 276] (book p. 276; PDF p. 293) through
[PPA Exercise 4.12, p. 279] (book p. 279; PDF p. 296)). Order-theoretic prerequisites live in
[appendix-a-posets-lattices-fixed-points.md](../../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md);
Galois connections (§4.3) and domain combinators / induced operations (§§4.4–4.5) live in
[galois-connections-and-insertions.md](./galois-connections-and-insertions.md) and
[combinators-and-induced-operations.md](./combinators-and-induced-operations.md).

## 1. Abstracted Semantics, Determinacy, and First-Order Scope (Section 4.1)

Chapter 4 studies Abstract Interpretation in a programming-language-independent setting (`G-U4a-01`), focusing on
property spaces, computations over them, and soundness bridges [PPA Chapter 4, p. 211] (book p. 211; PDF p. 228):

1. **Abstracted operational relation `(4.1)` vs deterministic analysis `(4.2)` (`G-U4a-02`)**:
   - Concrete semantics over value set `V` specifies a transition relation `p ⊢ v_1 ↝ v_2` `(4.1)` **without**
     assuming determinacy (`p ⊢ v_1 ↝ v_2 ∧ p ⊢ v_1 ↝ v_3` need not imply `v_2 = v_3`)
     [PPA §4.1, p. 211] (book p. 211; PDF p. 228).
   - Program analysis over property space `L` specifies `p ⊢ l_1 ⊳ l_2` `(4.2)`, customarily assumed **deterministic
     and total** so it defines a function `f_p : L → L` via `f_p(l_1) = l_2 iff p ⊢ l_1 ⊳ l_2`
     [PPA §4.1, p. 212] (book p. 212; PDF p. 229).
2. **First-order vs second-order scope boundary (`G-U4a-03`)**:
   - `§4.1` is termed *mundane* because its value-to-property relation `R ⊆ V × L` covers only **first-order analyses**
     whose properties describe *sets of values* — instantiated by `WHILE` Constant Propagation (`Example 4.1`:
     `S_⋆ ⊢ σ_1 ↝ σ_2 iff ⟨S_⋆, σ_1⟩ →^* σ_2` and `S_⋆ ⊢ σ̂_1 ⊳ σ̂_2 iff ι = σ̂_1 ∧ σ̂_2 = ⨆{CP_•(ℓ) | ℓ ∈ final(S_⋆)}`),
     `FUN` 0-CFA (`Example 4.2`: `e_⋆ ⊢ v_1 ↝ v_2 iff [] ⊢ (e_⋆ v_1^{ℓ_1})^{ℓ_2} →^* v_2^{ℓ_2}` and
     `e_⋆ ⊢ (ρ̂_1, v̂_1) ⊳ (ρ̂_2, v̂_2)` around fixed `(Ĉ, ρ̂)`, `G-U4a-06`), and Shape Analysis (`§2.6`)
     [PPA Example 4.1, p. 212] (book p. 212; PDF p. 229); [PPA Example 4.2, p. 213] (book p. 213; PDF p. 230).
   - `§4.1` does **not** directly cover **second-order analyses** relating inputs to outputs (such as `§2.1` Live
     Variables or 2-safety relational hyperproperties [external]). By contrast, **`§§4.2–4.5` apply equally to both
     first-order and second-order analyses** [PPA §4.1, p. 212] (book p. 212; PDF p. 229).
3. **Orientation of `⊑` (`G-U4a-04`)**: Throughout Chapter 4, **smaller elements `l_1 ⊑ l_2` are more precise
   (more informative)**: `⊥` is most precise (often unreachable/empty) and `⊤` is trivially safe/uninformative
   [PPA §4.1.1, p. 214] (book p. 214; PDF p. 231).

## 2. Correctness Relations, Moore Families, and Representation Functions (Sections 4.1.1-4.1.3)

### 2.1 Correctness Relations `(4.3)`–`(4.5)` (`§4.1.1`)

A **correctness relation** `R : V × L → {true, false}` (written `v R l`) certifies analysis `⊳` for semantics `↝` via
Display `(4.3)` [PPA §4.1.1, p. 214] (book p. 214; PDF p. 231):
```text
v_1 R l_1  ∧  p ⊢ v_1 ↝ v_2  ∧  p ⊢ l_1 ⊳ l_2   ⇒   v_2 R l_2                                      (4.3)
```
When `(L, ⊑)` is a complete lattice, `R` is required to satisfy two structural axioms (`G-U4a-05`):
```text
v R l_1  ∧  l_1 ⊑ l_2           ⇒   v R l_2                                                         (4.4)
(∀l ∈ L' ⊆ L : v R l)           ⇒   v R (⨅ L')                                                      (4.5)
```
- **Side conditions & consequences (`G-U4a-05`, `G-U4b-23`)**:
  - Axiom `(4.5)` states that `{l ∈ L | v R l}` is a **Moore family** in `L`: setting `L' = ∅` forces **`v R ⊤`** for
    all `v ∈ V`, and `|L'| = 2` gives `v R l_1 ∧ v R l_2 ⇒ v R (l_1 ⊓ l_2)`
    [PPA §4.1.1, p. 215] (book p. 215; PDF p. 232).
  - By `Exercise 4.2`, `(4.4)` alone yields closure under **non-empty** joins `(∀l ∈ L' ≠ ∅ : v R l) ⇒ v R (⨆ L')`,
    whereas **`v R ⊥` (`L' = ∅`) fails in general** (e.g. `z R_{ZS'} ⊥ = false` on `Figure 4.10`'s `Sign'` in
    `Exercise 4.1`) [PPA Exercise 4.1, p. 276] (book p. 276; PDF p. 293);
    [PPA Exercise 4.2, p. 276] (book p. 276; PDF p. 293).
  - **Concrete instances**: `Example 4.3` defines `σ R_{CP} σ̂ iff ∀x ∈ FV(S_⋆) : (σ̂(x) = ⊤ ∨ σ(x) = σ̂(x))` over
    `Statê_{CP} = (Var_⋆ → Z^⊤)_⊥` (requiring an implicit `σ̂ ≠ ⊥` guard because `⊥` is non-functional, `F-U4a-02`)
    [PPA Example 4.3, p. 215] (book p. 215; PDF p. 232); `Example 4.4` defines `v R_{CFA} (ρ̂, v̂)` recursively on closure
    size over `(Env̂ × Val̂, ⊑_{CFA})` and discharges `(4.3)` via `Theorem 3.10` (`Exercise 4.3`)
    [PPA Example 4.4, p. 215] (book p. 215; PDF p. 232); [PPA Exercise 4.3, p. 276] (book p. 276; PDF p. 293).

### 2.2 Representation Functions `β : V → L` and `Lemma 4.5` (`§4.1.2`)

A function `β : V → L` **generates** `R_β : V × L → {true, false}` by `v R_β l iff β(v) ⊑ l` (`Figure 4.1` depicts `V`
on the left mapping `v ↦ β(v) ∈ L` with `v R l` shading the upward cone `↑β(v) = {l ∈ L | β(v) ⊑ l}`)
[PPA §4.1.2, p. 216] (book p. 216; PDF p. 233); [PPA Figure 4.1, p. 218] (book p. 218; PDF p. 235). The correctness
criterion in terms of `β` is Display `(4.6)`:
```text
β(v_1) ⊑ l_1  ∧  p ⊢ v_1 ↝ v_2  ∧  p ⊢ l_1 ⊳ l_2   ⇒   β(v_2) ⊑ l_2                                (4.6)
```
For total deterministic `f_p` (`f_p(l_1) = l_2`), `(4.6)` reads `β(v_1) ⊑ l_1 ∧ p ⊢ v_1 ↝ v_2 ⇒ β(v_2) ⊑ f_p(l_1)` (and
when `f_p` is monotone, equivalently `p ⊢ v_1 ↝ v_2 ⇒ β(v_2) ⊑ f_p(β(v_1))`) [PPA §4.1.2, p. 216] (book p. 216; PDF p. 233).

- **`Lemma 4.5` (Bijection between `(4.4)`+`(4.5)` relations and `β : V → L`)**:
  1. For any `β : V → L`, `R_β` satisfies `(4.4)` and `(4.5)`.
  2. Conversely, if `R` satisfies `(4.4)` and `(4.5)` on complete lattice `L`, then `β_R(v) = ⨅{l ∈ L | v R l}` satisfies
     `R_{β_R} = R`, and furthermore `β_{R_β} = β` [PPA Lemma 4.5, p. 217] (book p. 217; PDF p. 234).
- **Instances**: `Example 4.6` sets `β_{CP}(σ) = λx. σ(x)` generating `R_{CP}`
  [PPA Example 4.6, p. 217] (book p. 217; PDF p. 234); `Example 4.7` constructs `β_{CFA} : Val → Env̂ × Val̂` and
  `β_{CFA}^E : Env → Env̂` by mutual recursion on non-circular closures (`Exercise 4.4`, `G-U4a-06`)
  [PPA Example 4.7, p. 218] (book p. 218; PDF p. 235); [PPA Exercise 4.4, p. 277] (book p. 277; PDF p. 294).

### 2.3 Distinct Input/Output Domains and `Lemma 4.8` (`§4.1.3`)

For `↝ ⊆ V_1 × V_2` and `f_p : L_1 → L_2` (`G-U4a-07`), lift `R_i : V_i × L_i → {true, false}` and `β_i : V_i → L_i` to
the pointwise complete lattice of functions `L_1 → L_2` [PPA §4.1.3, p. 219] (book p. 219; PDF p. 236):
```text
↝ (R_1 ↠ R_2) f               iff   ∀v_1, v_2, l_1 : (v_1 ↝ v_2 ∧ v_1 R_1 l_1) ⇒ v_2 R_2 f(l_1)
((β_1 ↠ β_2)(↝))(l_1)         =     ⨆{ β_2(v_2) | β_1(v_1) ⊑ l_1 ∧ v_1 ↝ v_2 }
```
- **`Lemma 4.8`**: If each `R_i` is generated by `β_i`, then `R_1 ↠ R_2` is a correctness relation on `L_1 → L_2` and is
  generated by `β_1 ↠ β_2`, i.e. `↝ (R_1 ↠ R_2) f ⇔ (β_1 ↠ β_2)(↝) ⊑ f`
  [PPA Lemma 4.8, p. 220] (book p. 220; PDF p. 237).
- **Collecting semantics optimality (`Example 4.9`, `Exercise 4.5`)**: Taking `L_i = (𝒫(V_i), ⊆)` and `β_i(v_i) = {v_i}`
  gives `((β_1 ↠ β_2)(p ⊢ · ↝ ·))(l_1) = {v_2 ∈ V_2 | ∃v_1 ∈ l_1 : p ⊢ v_1 ↝ v_2}`, proving the collecting semantics is
  monotone, sound, and the **least (optimal)** sound transformer `f_p ⊑ f'` (`Example 4.9` instantiates integer `plus`)
  [PPA Example 4.9, p. 220] (book p. 220; PDF p. 237); [PPA Exercise 4.5, p. 277] (book p. 277; PDF p. 294).

## 3. Complete Lattice Interval and Fixed-Point Approximation Chains (Section 4.2)

### 3.1 The `Interval` Lattice (`Example 4.10`, `Figure 4.2`)

Let `Z' = Z ∪ {-∞, ∞}` linearly ordered by `-∞ < z_1 < z_2 < ∞`. The complete lattice `Interval` (`Figure 4.2`) is
[PPA Figure 4.2, p. 221] (book p. 221; PDF p. 238); [PPA Example 4.10, p. 222] (book p. 222; PDF p. 239):
```text
Interval = {⊥} ∪ { [z_1, z_2] | z_1 ≤ z_2, z_1 ∈ Z ∪ {-∞}, z_2 ∈ Z ∪ {∞} }
```
- **Endpoint conventions & exclusions (`G-U4a-08`, `BKL-001`)**:
  - Degenerate intervals `[∞, ∞]` and `[-∞, -∞]` are **excluded**, and empty intervals collapse to the single bottom
    element `⊥`. Endpoint projections invert at `⊥`: **`inf(⊥) = ∞`** and **`sup(⊥) = -∞`** (`inf([z_1, z_2]) = z_1`,
    `sup([z_1, z_2]) = z_2`), so `int_1 ⊑ int_2 ⇔ inf(int_2) ≤ inf(int_1) ∧ sup(int_1) ≤ sup(int_2)` holds uniformly
    including `⊥`!
  - Arbitrary lubs/glbs use `⊓_{Z'}, ⊔_{Z'}` (`⨆ Y = [⨅_{Z'}{inf(int) | int ∈ Y}, ⨆_{Z'}{sup(int) | int ∈ Y}]` for
    `Y ⊈ {⊥}`, `⊤ = [-∞, ∞]`). `Interval` satisfies **neither ACC nor DCC** (`[0, 0] ⊏ [0, 1] ⊏ ⋯` and
    `[-∞, 0] ⊐ [-∞, -1] ⊐ ⋯`). Note `Interval` models unbounded mathematical `Z`, **not** `[external: wrapping machine bit-vectors]`
    (see `BKL-001`) [PPA Example 4.10, p. 222] (book p. 222; PDF p. 239).

### 3.2 Six-Level Fixed-Point Chain (`Figure 4.3`)

For any monotone `f : L → L` on a complete lattice `L` (`G-U4a-09`), Tarski's Theorem guarantees `lfp(f) = ⨅ Red(f)`
(`Red(f) = {l | f(l) ⊑ l}` reductive) and `gfp(f) = ⨆ Ext(f)` (`Ext(f) = {l | l ⊑ f(l)}` extensive) (`Appendix A §A.4`),
sitting inside the six-term chain of `Figure 4.3` [PPA §4.2, p. 223] (book p. 223; PDF p. 240);
[PPA Figure 4.3, p. 224] (book p. 224; PDF p. 241):
```text
∀n ≥ 0 :  f^n(⊥)  ⊑  ⨆_{k≥0} f^k(⊥)  ⊑  lfp(f)  ⊑  gfp(f)  ⊑  ⨅_{k≥0} f^k(⊤)  ⊑  f^n(⊤)
```
Without Scott continuity [external] / ACC, **every `⊑` in this chain can be strict (`⊏`)**, requiring transfinite
ordinals or widening (`§4.2.1`) to reach `Red(f)`.

## 4. Widening Operators, Threshold Extrapolation, and Non-Monotonicity (Section 4.2.1)

### 4.1 Upper Bound (`⊔̆`) and Widening (`∇`) Operators (`Fact 4.11`, `Figure 4.4`)

1. **Upper bound operator (`⊔̆ : L × L → L`)**: satisfies `l_1 ⊑ (l_1 ⊔̆ l_2)` and `l_2 ⊑ (l_1 ⊔̆ l_2)` for all `l_1, l_2 ∈ L`.
   It is **not required to be monotone, commutative, associative, or absorptive (`l ⊔̆ l = l`)** (`G-U4a-10`, `BKL-002`)
   [PPA §4.2.1, p. 225] (book p. 225; PDF p. 242).
2. **Chain transformation `(l_n^{⊔̆})_n` and `Fact 4.11`**: for any sequence `(l_n)_n`, define `l_0^{⊔̆} = l_0` and
   `l_{n+1}^{⊔̆} = l_n^{⊔̆} ⊔̆ l_{n+1}`. **`Fact 4.11`**: `(l_n^{⊔̆})_n` is always an ascending chain (`l_0^{⊔̆} ⊑ l_1^{⊔̆} ⊑ ⋯`)
   dominating `(l_n)_n` (`l_n ⊑ l_n^{⊔̆}` for all `n ≥ 0`) [PPA Fact 4.11, p. 225] (book p. 225; PDF p. 242).
3. **Widening operator (`∇ : L × L → L`)**: an upper bound operator such that for **every ascending chain `(l_n)_n`**,
   the transformed ascending chain `(l_n^∇)_n` **eventually stabilises** (`∃m ≥ 0 : ∀n ≥ m : l_n^∇ = l_m^∇`)
   [PPA §4.2.1, p. 226] (book p. 226; PDF p. 243).
   - *Counterexample (`Example 4.12`)*: `int_1 ⊔̆^{int} int_2 = int_1 ⊔ int_2` if `int_1 ⊑ int ∨ int_2 ⊑ int_1` else
     `[-∞, ∞]` is asymmetric for `int = [0, 2]` (`[1, 2] ⊔̆^{[0,2]} [2, 3] = [1, 3]` vs
     `[2, 3] ⊔̆^{[0,2]} [1, 2] = [-∞, ∞]`), and for `int = [0, ∞]` **fails** to stabilise `[0, 0], [1, 1], [2, 2], ⋯`
     (yielding `[0, 0], [0, 1], [0, 2], ⋯`), whereas `int = [0, 2]` stabilises at `[-∞, ∞]`
     [PPA Example 4.12, p. 225] (book p. 225; PDF p. 242); [PPA Example 4.12, p. 226] (book p. 226; PDF p. 243).

### 4.2 Widened Fixed-Point Sequence `(f_∇^n)_n`, `Proposition 4.13`, and `Fact 4.14`

For monotone `f : L → L`, define `(f_∇^n)_n` (`Figure 4.4` shows `(f_∇^n)_n` climbing through `Ext(f)` and jumping into
`Red(f)` at `lfp_∇(f) ⊒ lfp(f)`) [PPA Figure 4.4, p. 226] (book p. 226; PDF p. 243);
[PPA §4.2.1, p. 227] (book p. 227; PDF p. 244):
```text
f_∇^0 = ⊥
f_∇^n = { f_∇^{n-1}                  if f(f_∇^{n-1}) ⊑ f_∇^{n-1}     (for n > 0)
        { f_∇^{n-1} ∇ f(f_∇^{n-1})   otherwise
```
- **Critical operand & guard invariants (`G-U4a-11`, `G-U4a-12`, `G-U4b-24`)**:
  - **Operand order is strictly `old ∇ new`** (`f_∇^{n-1} ∇ f(f_∇^{n-1})`): swapping to `f(f_∇^{n-1}) ∇ f_∇^{n-1}` lets
    `[0, n] ∇_K [0, n-1] = [0, n]` diverge!
  - **Explicit reductive guard `f(f_∇^{n-1}) ⊑ f_∇^{n-1}` is mandatory**: because `∇` need not satisfy `l ∇ l = l` or
    `l_2 ⊑ l_1 ⇒ l_1 ∇ l_2 = l_1`, omitting the `if`-guard can push an already reductive iterate strictly higher!
  - **`Proposition 4.13` (Termination)**: If `∇` is a widening operator and `f : L → L` is **monotone** (`F-U4a-06`),
    `(f_∇^n)_n` eventually stabilises at some `f_∇^m`, defining **`lfp_∇(f) = f_∇^m`**. *(By `Exercise 4.8`, replacing
    `f_∇^0 = ⊥` with `l_0` preserves `Proposition 4.13` when `l_0 ∈ Ext(f)` — including `f(⊥)` and `f^{27}(⊥)` — but
    can diverge for arbitrary `l_0 ∉ Ext(f)`!)* [PPA Proposition 4.13, p. 227] (book p. 227; PDF p. 244);
    [PPA Exercise 4.8, p. 277] (book p. 277; PDF p. 294).
  - **`Fact 4.14` (Soundness)**: Even if `∇` is merely an upper bound operator (and for **arbitrary** initial `l_0`,
    `Exercise 4.8`), `f_∇^m = f_∇^{m+1}` implies **`f(f_∇^m) ⊑ f_∇^m`** (`f_∇^m ∈ Red(f)`) and hence **`f_∇^m ⊒ lfp(f)`**
    [PPA Fact 4.14, p. 227] (book p. 227; PDF p. 244).

### 4.3 Threshold Widening `∇_K` on `Interval` (`Example 4.15`) and Delayed Widening (`Exercises 4.6, 4.9`)

For **finite, fixed** threshold set `K ⊆ Z` (`G-U4a-13`), `Example 4.15` defines `int_1 ∇_K int_2` (`⊥ ∇_K ⊥ = ⊥`, else
`[LB_K(inf(int_1), inf(int_2)), UB_K(sup(int_1), sup(int_2))]`) where
[PPA Example 4.15, p. 228] (book p. 228; PDF p. 245):
```text
LB_K(z_1, z_3) = z_1                      if z_1 ≤ z_3
               = max{k ∈ K | k ≤ z_3}     if z_3 < z_1 ∧ ∃k ∈ K : k ≤ z_3
               = -∞                       otherwise

UB_K(z_2, z_4) = z_2                      if z_4 ≤ z_2
               = min{k ∈ K | z_4 ≤ k}     if z_2 < z_4 ∧ ∃k ∈ K : z_4 ≤ k
               = ∞                        otherwise
```
- **Step-1 `⊥` blowup & non-monotonicity (`G-U4a-10`, `G-U4a-13`, `BKL-002`)**:
  - As printed, `⊥ ∇_K [z_3, z_4]` evaluates `LB_K(∞, z_3)` and `UB_K(-∞, z_4)` (`⊥ ∇_∅ [0, 0] = [-∞, ∞]`!), losing
    initial bounds unless implementations add `⊥ ∇_K int_2 = int_2` (`cf. Exercise 4.6(4)`).
  - `∇_K` is **non-monotone in its first argument**: `[1, 1] ⊑ [0, 2]`, yet `[1, 1] ∇_∅ [1, 2] = [1, ∞] ⋢ [0, 2] = [0, 2] ∇_∅ [1, 2]`.
  - Delaying widening via `l_1 ⊔ l_2` when `l_1 ⊑ l' ∨ l_2 ⊑ l_1` (`Exercise 4.6(5)`, `Exercise 4.9`) remains a valid
    widening operator **iff `↓l'` satisfies ACC** (true on `Interval` iff `inf(int') > -∞ ∧ sup(int') < ∞`)
    [PPA Exercise 4.6, p. 277] (book p. 277; PDF p. 294); [PPA Exercise 4.9, p. 278] (book p. 278; PDF p. 295).

## 5. Narrowing Operators, Absorptiveness, and Descending Truncators (Section 4.2.2)

Once `f_∇^m ∈ Red(f)` is found (`f(f_∇^m) ⊑ f_∇^m`), descending `[external: Kleene]` steps `f^n(f_∇^m)` stay inside `Red(f)` above
`lfp(f)` (`Figure 4.5`) [PPA §4.2.2, p. 230] (book p. 230; PDF p. 247); [PPA Figure 4.5, p. 231] (book p. 231; PDF p. 248).

1. **Narrowing operator (`Δ : L × L → L`)**: satisfies **(a) Contractiveness**: `l_2 ⊑ l_1 ⇒ l_2 ⊑ (l_1 Δ l_2) ⊑ l_1`,
   and **(b) Stabilisation**: for every descending chain `(l_n)_n` (`l_0 ⊒ l_1 ⊒ ⋯`), `(l_n^Δ)_n` (`l_0^Δ = l_0`,
   `l_{n+1}^Δ = l_n^Δ Δ l_{n+1}`, descending with `l_n^Δ ⊒ l_n` by `Exercise 4.10`) eventually stabilises
   [PPA §4.2.2, p. 230] (book p. 230; PDF p. 247); [PPA Exercise 4.10, p. 278] (book p. 278; PDF p. 295).
   - **Absorptiveness (`G-U4a-14`)**: Although `p. 230` states `Δ` need not be absorptive, setting `l_1 = l_2 = l` in
     `l_2 ⊑ l_1 ⇒ l_2 ⊑ (l_1 Δ l_2) ⊑ l_1` forces **`l Δ l = l` for every narrowing operator**!
2. **Narrowed sequence `([f]_Δ^n)_n`, `Lemma 4.16` `(4.7)`, and `Proposition 4.17` (`G-U4a-15`)**:
   Starting strictly from **`[f]_Δ^0 = f_∇^m ∈ Red(f)`**, set `[f]_Δ^{n+1} = [f]_Δ^n Δ f([f]_Δ^n)` (absorptiveness makes
   an explicit `if`-guard redundant).
   - **`Lemma 4.16`**: For monotone `f` with `f(f_∇^m) ⊑ f_∇^m`, `([f]_Δ^n)_n` is a descending chain in `Red(f)` with
     `[f]_Δ^n ⊒ f^n(f_∇^m) ⊒ lfp(f)` for all `n`, proved by induction via Display `(4.7)`
     [PPA Lemma 4.16, p. 230] (book p. 230; PDF p. 247):
     ```text
     f^{n+1}(f_∇^m)  ⊑  f([f]_Δ^n)  ⊑  [f]_Δ^{n+1}  ⊑  [f]_Δ^n                                       (4.7)
     ```
   - **`Proposition 4.17` & non-duality**: For monotone `f` (`F-U4a-06`) and narrowing `Δ`, `([f]_Δ^n)_n` stabilises at
     **`lfp_∇^Δ(f) = [f]_Δ^{m'}`** with `lfp(f) ⊑ lfp_∇^Δ(f) ⊑ lfp_∇(f)`. **Narrowing is NOT the lattice dual of
     widening** (`p. 232`): `(f_∇^n)_n` may step outside `Ext(f)` to enter `Red(f)`, whereas `([f]_Δ^n)_n` stays inside
     `Red(f)` all the time [PPA Proposition 4.17, p. 232] (book p. 232; PDF p. 249).
3. **Threshold narrowing `Δ_N` (`Example 4.18`) vs `DCC` (`Exercise 4.12`) & Truncators `ϒ` (`Exercise 4.11`)**:
   - `Δ_N` (for a fixed non-negative integer `N ≥ 0`, `G-U4a-16`) sets `int_1 Δ_N int_2 = ⊥` if `int_1 = ⊥ ∨ int_2 = ⊥`,
     else `[z_1, z_2]` where `z_1 = inf(int_1)` if `N < inf(int_2) ∧ sup(int_2) = ∞` (else `inf(int_2)`) and
     `z_2 = sup(int_1)` if `inf(int_2) = -∞ ∧ sup(int_2) < -N` (else `sup(int_2)`). On `[n, ∞]_n` with `N = 3`,
     `([n, ∞]^Δ)_n` stabilises at `[0, ∞], [1, ∞], [2, ∞], [3, ∞], [3, ∞], ⋯`, while bounded changes adopt `int_2`'s
     finite bounds unconditionally (`O(M)` steps on large finite shifts)
     [PPA Example 4.18, p. 232] (book p. 232; PDF p. 249); [PPA Example 4.18, p. 233] (book p. 233; PDF p. 250).
   - Under `DCC`, `⊓` is a narrowing operator (`Exercise 4.12`); prefix-determined *descending chain truncators* `ϒ`
     (`Exercise 4.11`, `G-U4b-24`) stop at finite iterates `lfp_∇^ϒ(f) = f^{m'}(f_∇^m)`, whereas `Δ` can jump past `ω`
     steps in one step [PPA Exercise 4.11, p. 278] (book p. 278; PDF p. 295);
     [PPA Exercise 4.12, p. 279] (book p. 279; PDF p. 296).

## 6. Cross-Chapter Unification U7: Widening vs Ascending Chain Condition

- **Stated correspondence (`U7`)**: Chapter 2 `§2.3` (`Appendix A §A.3`) requires `L` to satisfy `ACC` so least-upper-bound
  iteration stabilises (`BKL-013`), whereas Chapter 4 `§4.2` replaces static `ACC` on `L` with dynamic chain stabilisation
  via widening `∇` [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87); [PPA §4.2, p. 221] (book p. 221; PDF p. 238);
  [PPA §A.3, p. 400] (book p. 400; PDF p. 416).
- **Exact coincidence condition (`Exercise 4.7`)**: When `L` *does* satisfy `ACC`, widening operators coincide with upper
  bound operators and `⊔` itself is a widening operator with `lfp_⊔(f) = ⨆_n f^n(⊥) = lfp(f)` (for `ACC` / affine `f`)
  [PPA Exercise 4.7, p. 277] (book p. 277; PDF p. 294).
- **Key difference**: Without `ACC`, `∇` sacrifices exactness (`lfp(f) ⊑ lfp_∇(f)`) and monotonicity (`BKL-002`), making
  iteration order (`Chapter 6 Exercise 6.13` worklist widening in [scc-round-robin-and-advanced-solvers.md](../../ppa-fixedpoint-solvers/references/scc-round-robin-and-advanced-solvers.md) [PPA Exercise 6.13, p. 391] (book p. 391; PDF p. 407)) and `[external: CFG loop-cutset placement]` affect precision rather than mere runtime.

## 7. Verified Source Errata and Implicit Hypotheses (Sections 4.1-4.2 and Exercises 4.1-4.12)

- **Printed errata & implicit guards (`BKL-067`, `BKL-068`, `BKL-069`)**: `Example 4.2` prints `"as in indeed"` (`p. 213`); `Example 4.3` omits `σ̂ ≠ ⊥`
  (`p. 215`); `Example 4.7` prose prints pair-typed `⋃{β_{CFA}(ρ(x)) | x ∈ Var_⋆}` (`p. 218`); `Example 4.9` switches
  `plus` to `p` (`p. 220`); `Example 4.15` (`p. 228`, `BKL-068`) omits `⊥ ∇_K [z_3, z_4] = [z_3, z_4]`; standalone boxes of `Proposition 4.13` (`p. 227`) and `Proposition 4.17` (`p. 232`) omit
  explicit `f`-monotonicity (inherited from `§4.2` prose `pp. 223, 226`, `BKL-069`); `§4.2.2` (`p. 230`, `BKL-067`) says narrowing need not
  be absorptive despite contractiveness forcing `l Δ l = l`; `Lemma 4.16` basis (`p. 231`, `BKL-069`) leaves `n` symbolic for `0`;
  `Exercise 4.6` (`p. 277`) prints `"which of them that"`; and the PDF OCR text layer drops `(4.1)–(4.3), (4.6)–(4.7)`
  (`G-U4a-24`)
  [PPA Proposition 4.13, p. 227] (book p. 227; PDF p. 244); [PPA Lemma 4.16, p. 231] (book p. 231; PDF p. 248).
