<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L1 formal reference for Chapter 4 §§4.4-4.5 Galois combinators, 29-atom Array Bound lattice, induced transformers, generalised Monotone Frameworks (U6), gamma-induced widening, and Mini Projects 4.1-4.3. -->

# Galois Combinators, Array Bound Synthesis, and Induced Operations

Self-contained formal reference for Chapter 4 §4.4 (*Systematic Design of Galois Connections*: §§4.4.1–4.4.2), §4.5
(*Induced Operations*: §§4.5.1–4.5.3), `Concluding Remarks` on distributive/tensor/concrete domains, `Mini Projects
4.1–4.3`, and `Exercises 4.15–4.24` of *Principles of Program Analysis* ([PPA §4.4, p. 246] (book p. 246; PDF p. 263)
through [PPA §4.5.3, p. 270] (book p. 270; PDF p. 287), [PPA Chapter 4 Concluding Remarks, p. 271] (book p. 271; PDF p. 288)
through [PPA Chapter 4 Concluding Remarks, p. 272] (book p. 272; PDF p. 289),
[PPA Mini Project 4.1, p. 274] (book p. 274; PDF p. 291) through [PPA Mini Project 4.3, p. 275] (book p. 275; PDF p. 292),
and [PPA Exercise 4.15, p. 279] (book p. 279; PDF p. 296) through [PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299)).
Foundations live in [correctness-and-fixed-points.md](./correctness-and-fixed-points.md) and
[galois-connections-and-insertions.md](./galois-connections-and-insertions.md); Chapter 2 Monotone Frameworks and
Shape Analysis (`Mini Project 4.2`), Chapter 3 coupled `CFA + DFA` (`Mini Project 4.3`, `Table 3.9`), and
Chapter 1 induced Reaching Definitions live in
[intraprocedural-analyses-and-frameworks.md](../../ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md),
[shape-analysis.md](../../ppa-dataflow-and-slicing/references/shape-analysis.md),
[polyvariant-kcfa-cpa-and-dfa.md](../../ppa-control-flow-and-constraints/references/polyvariant-kcfa-cpa-and-dfa.md),
and [chapter-1-five-formulations.md](../../ppa-program-analysis/references/chapter-1-five-formulations.md).

## 1. Sequential Composition and Component-Wise Combinators (Sections 4.4-4.4.1)

1. **Sequential (functional) composition (`§4.4`, `G-U4b-02`, `G-U4b-03`)**:
   - Chaining `(L_0, α_1, γ_1, L_1)` and `(L_1, α_2, γ_2, L_2)` reverses composition order on `γ` relative to `α`:
     **`(L_0, α_2 ∘ α_1, γ_1 ∘ γ_2, L_2)`**, preserving Galois insertions (`Exercise 4.15` proves `α_{η_2} ∘ α_{η_1} = α_{η_2 ∘ η_1}`
     and `γ_{η_1} ∘ γ_{η_2} = γ_{η_2 ∘ η_1}`) [PPA §4.4, p. 247] (book p. 247; PDF p. 264);
     [PPA Exercise 4.15, p. 279] (book p. 279; PDF p. 296).
   - **`Example 4.33`**: Composes `diff : Z × Z → Z` (`diff(z_1, z_2) = |z_1| - |z_2|`, *magnitude* difference!) with
     `range : Z → Range` (`Range = {<-1, -1, 0, +1, >+1}`) into Galois insertion `(𝒫(Z × Z), α_R, γ_R, 𝒫(Range))`
     [PPA Example 4.33, p. 247] (book p. 247; PDF p. 264).
2. **Independent attribute method (`§4.4.1`, `Example 4.34`, `G-U4b-04`, `G-U4b-05`)**:
   - `(L_1 × L_2, α, γ, M_1 × M_2)` sets `α(l_1, l_2) = (α_1(l_1), α_2(l_2))` and `γ(m_1, m_2) = (γ_1(m_1), γ_2(m_2))`,
     preserving Galois insertions (`Exercise 4.17`) [PPA §4.4.1, p. 249] (book p. 249; PDF p. 266);
     [PPA Exercise 4.17, p. 280] (book p. 280; PDF p. 297).
   - Loses cross-component correlations (`Example 4.34`: `{(z, -z) | z ∈ Z}` projects to `(Z, Z) ↦ (Sign, Sign)`), and
     `𝒫(V_1) × 𝒫(V_2)` requires disjoint-union tagging `({1} × V_1) ∪ ({2} × V_2)` (`twosigns(i, z) = (i, sign(z))`,
     `Exercise 4.16`, where disjointness of **both** `V_1, V_2` and `D_1, D_2` is required)
     [PPA Example 4.34, p. 250] (book p. 250; PDF p. 267); [PPA Exercise 4.16, p. 279] (book p. 279; PDF p. 296).
3. **Relational method on powersets (`⊗`, `Example 4.35`, `Exercise 4.18`, `G-U4b-05`, `G-U4b-06`)**:
   - `(𝒫(V_1 × V_2), α, γ, 𝒫(D_1 × D_2))` (`= (𝒫(V_1) ⊗ 𝒫(V_2), α, γ, 𝒫(D_1) ⊗ 𝒫(D_2))`) sets
     `α(VV) = ⋃{α_1({v_1}) × α_2({v_2}) | (v_1, v_2) ∈ VV}` and `γ(DD) = {(v_1, v_2) | α_1({v_1}) × α_2({v_2}) ⊆ DD}`,
     preserving `{(-, +), (0, 0), (+, -)}` on `{(z, -z)}` (`Example 4.35`) and **always preserving Galois insertions on
     powersets** (`Exercise 4.18`, because singletons `{d_i}` are completely join-irreducible in `𝒫(D_i)`)
     [PPA §4.4.1, p. 251] (book p. 251; PDF p. 268); [PPA Example 4.35, p. 251] (book p. 251; PDF p. 268);
     [PPA Exercise 4.18, p. 280] (book p. 280; PDF p. 297).
4. **Total (`S → L`) and monotone (`L_1 → L_2`) function spaces (`§4.4.1`, `G-U4b-10`)**:
   - `(S → L, α', γ', S → M)` lifts pointwise (`α'(f) = α ∘ f`, `γ'(g) = γ ∘ g`; `Example 4.36` abstracts abstract
     states `Var → L` to `Var → M`) and preserves Galois insertions [PPA §4.4.1, p. 252] (book p. 252; PDF p. 269);
     [PPA Example 4.36, p. 253] (book p. 253; PDF p. 270).
   - `(L_1 → L_2, α, γ, M_1 → M_2)` over **monotone** maps sets **`α(f) = α_2 ∘ f ∘ γ_1`** and **`γ(g) = γ_2 ∘ g ∘ α_1`**
     (contravariant input, covariant output; binary `((L_1 × L_2) → L_3, α, γ, (M_1 × M_2) → M_3)` in `Exercise 4.22`),
     preserving Galois insertions (`Exercise 4.17`). By `Exercise 4.20` (`L_1 = L_2`, `M_1 = M_2`), **none** of
     `α(id) = id`, `γ(id) = id`, `α(f_1 ∘ f_2) = α(f_1) ∘ α(f_2)`, `γ(g_1 ∘ g_2) = γ(g_1) ∘ γ(g_2)` hold under a mere
     Galois connection, while under a **Galois insertion** `α(id) = id` and `γ(g_1 ∘ g_2) = γ(g_1) ∘ γ(g_2)` hold yet
     **`γ(id) = id` and `α(f_1 ∘ f_2) = α(f_1) ∘ α(f_2)` still fail** (`α(f_1 ∘ f_2) ⊑ α(f_1) ∘ α(f_2)` can be strict!)
     [PPA §4.4.1, p. 253] (book p. 253; PDF p. 270); [PPA Exercise 4.20, p. 280] (book p. 280; PDF p. 297);
     [PPA Exercise 4.22, p. 281] (book p. 281; PDF p. 298).

## 2. Same-Carrier Products, Reduction, and the 29-Atom Array Bound Domain (Section 4.4.2)

Given two abstractions `(L, α_1, γ_1, M_1)` and `(L, α_2, γ_2, M_2)` of the **same** concrete lattice `L`:

1. **Direct product (`(L, α, γ, M_1 × M_2)`, `Example 4.37`, `Exercise 4.19`, `G-U4b-05`, `G-U4b-06`)**:
   - `α(l) = (α_1(l), α_2(l))` and `γ(m_1, m_2) = γ_1(m_1) ⊓ γ_2(m_2)`. Fails cross-domain correlation (`Example 4.37`:
     `{(z, 3*z)}` abstracts to `({(-, -), (0, 0), (+, +)}, {<-1, 0})`, admitting `(-1, -1)`) and **fails to preserve
     Galois insertions** (`Exercise 4.19`: `γ({0}, {odd}) = ∅ = γ(∅, ∅)`)
     [PPA §4.4.2, p. 254] (book p. 254; PDF p. 271); [PPA Example 4.37, p. 254] (book p. 254; PDF p. 271);
     [PPA Exercise 4.19, p. 280] (book p. 280; PDF p. 297).
2. **Direct tensor product on powersets (`(𝒫(V), α, γ, 𝒫(D_1 × D_2))`, `Example 4.38`, `G-U4b-06`)**:
   - `α(V') = ⋃{α_1({v}) × α_2({v}) | v ∈ V'}` and `γ(DD) = {v ∈ V | α_1({v}) × α_2({v}) ⊆ DD}`. In `Example 4.38`,
     `twosignsrange(z_1, z_2) = (sign(z_1), sign(z_2), range(diff(z_1, z_2)))` keeps `{(z, 3*z)} ↦ {(-, -, <-1), (0, 0, 0), (+, +, <-1)}`,
     yet **still fails Galois insertion** (`γ_{SSR'}({(0, 0, <-1)}) = ∅ = γ_{SSR'}(∅)`)
     [PPA §4.4.2, p. 255] (book p. 255; PDF p. 272); [PPA Example 4.38, p. 255] (book p. 255; PDF p. 272).
3. **Reduced product & reduced tensor product (`AB`, `Example 4.39`, `Exercise 4.21`, `G-U4b-07`, `G-U4b-08`, `G-U4b-09`)**:
   - Applying `Proposition 4.29`'s `ς` yields Galois insertions `(L, α, γ, ς[M_1 × M_2])` (`ς(m_1, m_2) = ⨅{(m'_1, m'_2) | γ_1(m_1) ⊓ γ_2(m_2) = γ_1(m'_1) ⊓ γ_2(m'_2)}`)
     and `(𝒫(V), α, γ, ς[𝒫(D_1 × D_2)])` [PPA §4.4.2, p. 256] (book p. 256; PDF p. 273). *(In practice, `[external: Granger channel reduction]` `ρ_{12}` must never run **after** loop-head widening `(m_1 ∇_1 m'_1, m_2 ∇_2 m'_2)` lest it
     re-finite `∞` bounds and break termination, `G-U4b-09`.)*
   - **`Example 4.39` (`45 → 29` Array Bound lattice `AB`)**: `ς_{SSR'}` maps `16` uninhabited zero-sign singletons
     (`(-, 0, <-1/-1/0)`, `(0, -, 0/+1/>+1)`, `(0, 0, <-1/-1/+1/>+1)`, `(0, +, 0/+1/>+1)`, `(+, 0, <-1/-1/0)`) to `∅`,
     leaving **`29` disjoint atoms `AB`** (`45` bits → `29` bits, `twosignsrange' : Z × Z → AB`). By `Exercise 4.21`,
     `x = y + 3` maps to only `6` atoms (`(+, -)` restricted to `-1, +1` at `(1, -2), (2, -1)`), `x ≥ y` to `16`,
     `x ≥ y + 1` to `13`, while `x^2 + y^2 ≤ 100` collapses to all `29` atoms (`AB`)
     [PPA Example 4.39, p. 257] (book p. 257; PDF p. 274); [PPA Exercise 4.21, p. 281] (book p. 281; PDF p. 298).

## 3. Combinator Comparison Matrix and Disjunctive Completion

| Combinator | Signature | Preserves Insertion? | Relational Coupling | Representation Cost |
| :--- | :--- | :--- | :--- | :--- |
| Sequential composition (`§4.4`) | `(L_0, α_2 ∘ α_1, γ_1 ∘ γ_2, L_2)` | **Yes** (`p. 247`) | Across pipeline stages | That of `L_2` |
| Independent attribute (`§4.4.1`) | `(L_1 × L_2, α, γ, M_1 × M_2)` | **Yes** (`Ex 4.17`) | None (`Ex 4.34`) | Additive (`size(M_1) + size(M_2)`) |
| Relational powerset (`§4.4.1`, `⊗`) | `(𝒫(V_1 × V_2), α, γ, 𝒫(D_1 × D_2))` | **Yes** (`Ex 4.18`) | Full cross-component (`Ex 4.35`) | Multiplicative (`|D_1| · |D_2|` bits) |
| Total / monotone space (`§4.4.1`) | `S → M` / `M_1 → M_2` | **Yes** (`p. 252`, `Ex 4.17`) | Pointwise / input-output | `|S| · size(M)` / transformer table |
| Direct product (`§4.4.2`) | `(L, α, γ, M_1 × M_2)` | **No** (`Ex 4.19`) | Query-time `⊓` only (`Ex 4.37`) | Additive |
| Direct tensor (`§4.4.2`) | `(𝒫(V), α, γ, 𝒫(D_1 × D_2))` | **No** (`Ex 4.38`) | Joint per-element (`Ex 4.38`) | `|D_1| · |D_2|` bits (`45` in `SSR'`) |
| Reduced / reduced tensor (`§4.4.2`) | `ς[M_1 × M_2]` / `ς[𝒫(D_1 × D_2)]` | **Yes** (`Prop 4.29`) | Canonicalised (`AB`) | Pruned (`29` bits in `AB`) |
| Disjunctive completion (`CR`) | Join-closure of `ρ[L]` / quotient of `𝒫(M)` | **Yes** (`[39]`) | Exact abstract joins | Up to `2^{|M|}` |

Distributive lattices with atoms / join-irreducibles lift Bit Vector speed bounds beyond powersets (`[129, 118]`),
non-powerset tensor products require `[111, 113, 115]`, and concrete domains span Karr affine subspaces `[94]`,
Cousot–Halbwachs convex polygons `[41]` (`[external: convex polyhedra]`), Granger congruences `[66, 67]`, Masdupuy
`[105]`, and Deutsch/Colby word-to-vector reductions `[44, 45, 31, 32]`
[PPA Chapter 4 Concluding Remarks, p. 271] (book p. 271; PDF p. 288);
[PPA Chapter 4 Concluding Remarks, p. 272] (book p. 272; PDF p. 289).

## 4. Best Induced Transformers, Optimality, and Fixed-Point Soundness (Section 4.5.1)

- **Induced operation `α_2 ∘ f_p ∘ γ_1` and `Example 4.40` (`G-U4b-11`)**: Lifting `f_p : L_1 → L_2` across
  `(L_i, α_i, γ_i, M_i)` yields **`α(f_p) = α_2 ∘ f_p ∘ γ_1`** (`Example 4.40` induces
  `g_{plus} = α_{sign} ∘ f_{plus} ∘ γ_{SS'} : 𝒫(Sign × Sign) → 𝒫(Sign)` from `Example 4.9` and `Example 4.35`, yielding
  `g_{plus}(SS) = ⋃{s_1 ⊕ s_2 | (s_1, s_2) ∈ SS}` with `+ ⊕ + = {+}` and `+ ⊕ - = {-, 0, +}`)
  [PPA §4.5.1, p. 259] (book p. 259; PDF p. 276); [PPA Example 4.40, p. 259] (book p. 259; PDF p. 276).
- **`Lemma 4.41` & optimality preservation (`G-U4b-11`)**: For representation functions `β_i : V_i → L_i`,
  **`((α_1 ∘ β_1) ↠ (α_2 ∘ β_2))(↝) = α_2 ∘ ((β_1 ↠ β_2)(↝)) ∘ γ_1`**. Consequently: `(1)` if `f_p` is sound and
  **`α_2 ∘ f_p ∘ γ_1 ⊑ g_p`** (upper approximation!), then `g_p` is sound for `S_1 ↠ S_2`; and `(2)` if `f_p` is
  **optimal** (`f_p = (β_1 ↠ β_2)(p ⊢ · ↝ ·)`), then **`α_2 ∘ f_p ∘ γ_1` is also optimal**
  [PPA Lemma 4.41, p. 260] (book p. 260; PDF p. 277); [PPA §4.5.1, p. 261] (book p. 261; PDF p. 278).
- **`Lemma 4.42` (`G-U4b-12`)**: For monotone `f : L → L`, `g : M → M` with `α ∘ f ∘ γ ⊑ g`, complete multiplicativity
  of `γ` gives `g(m) ⊑ m ⇒ f(γ(m)) ⊑ γ(m)` and **`lfp(f) ⊑ γ(lfp(g))`** (`α(lfp(f)) ⊑ lfp(g)` — inequality, **not**
  equality!) [PPA Lemma 4.42, p. 261] (book p. 261; PDF p. 278).

## 5. Cross-Chapter Unification U6: Generalised Monotone Frameworks and Collecting Semantics (Section 4.5.2)

- **Stated correspondence (`U6`)**: Chapter 1 `§1.5` calculated Reaching Definitions from trace collecting semantics via
  `(α, γ)` (`[PPA Preface, p. VII]`, `[PPA §1.5, p. 16]`), and Chapter 4 `§4.5.2` generalises Chapter 2 `§2.3` Monotone
  Frameworks (`A = (L, F, E, ι, f_.)`) by **dropping `ACC` on `L` and allowing all monotone transfers `L → L`**
  [PPA Preface, p. VII] (book p. VII; PDF p. 7); [PPA §1.5, p. 16] (book p. 16; PDF p. 36);
  [PPA §4.5.2, p. 262] (book p. 262; PDF p. 279).
- **Exact conditions (`G-U4b-13`)**:
  1. *Constraint lifting (`p. 263`)*: `g_ℓ ⊒ α ∘ f_ℓ ∘ γ` (`∀ℓ`) and `ȷ ⊒ α(ι)` give `\vec{g} ⊒ α' ∘ \vec{f} ∘ γ'`
     (via `α(⊥_L) = ⊥_M`), whence **`(B_∘, B_•) ⊨ B^⊒ ⇒ (γ ∘ B_∘, γ ∘ B_•) ⊨ A^⊒`** (`Lemma 4.42`).
  2. *Semantic correctness transfer `(4.11) ⇒ (4.12)` (`p. 264`)*: requires strengthened extremal equality **`γ(ȷ) = ι`**
     so `(α ∘ β)(σ_1) ⊑ ȷ ⇒ β(σ_1) ⊑ γ(ȷ) = ι` [PPA §4.5.2, p. 264] (book p. 264; PDF p. 281).
- **Key differences (`SS` `Lemma 4.43`, `Remark.` `p. 266`, `CP` `pp. 266–267`, `G-U4b-14`, `G-U4b-15`)**:
  - Concrete sets-of-states `SS` (`(𝒫(State), ⊆)`, `ι = State`, `Lemma 4.43`) is sound (`(4.11)`) yet **strictly coarser
    than the collecting semantics** (`Remark.` `p. 266`) because node-attached `f_ℓ^{SS}([b]^ℓ) = Σ` ignores branch test
    outcomes unless transfers sit on **CFG edges** (`Exercise 2.11`)
    [PPA Lemma 4.43, p. 265] (book p. 265; PDF p. 282); [PPA §4.5.2, p. 266] (book p. 266; PDF p. 283).
  - Constant Propagation (`Statê_CP = ((Var → Z^⊤)_⊥, ⊑)`, unstarred `Var`) follows immediately via `γ_{CP}(λx.⊤) = State`
    and `α_{CP} ∘ f_ℓ^{SS} ∘ γ_{CP} ⊑ f_ℓ^{CP}` (short-circuiting `σ̂ = ⊥` via `γ_{CP}(⊥) = ∅`)
    [PPA §4.5.2, p. 267] (book p. 267; PDF p. 284).

## 6. Inducing Widening Along Concretisation vs Narrowing Asymmetry (Section 4.5.3 and Exercise 4.24)

1. **`Proposition 4.44` (`(4.13)`, `G-U4b-16`)**: For `(L, α, γ, M)` and upper bound `∇_M : M × M → M`,
   **`l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))`** is always an upper bound operator on `L`, and is a **widening operator** if:
   - `(i)` `M` satisfies `ACC` (for *any* Galois connection; proof takes `n_0 ≥ 1` so `l_n^{∇_L} ∈ γ[M]`), or
   - `(ii)` `(L, α, γ, M)` is a **Galois insertion** and `∇_M` is a widening operator (yielding `(4.13)`:
     `(α(l_n))^{∇_M} = α(l_n^{∇_L})`, instantiated for `𝒫(Z) ↔ Interval` in `Exercise 4.23`)
     [PPA Proposition 4.44, p. 268] (book p. 268; PDF p. 285); [PPA Exercise 4.23, p. 281] (book p. 281; PDF p. 298).
2. **`Lemma 4.45` (`(4.14)`–`(4.15)`, `G-U4b-17`)**: If `(L, α, γ, M)` is a **Galois insertion** **and** **`γ(⊥_M) = ⊥_L`**,
   then **`lfp_{∇_L}(f) = γ(lfp_{∇_M}(α ∘ f ∘ γ))`** (`f_{∇_L}^n = γ(g_{∇_M}^n)` `(4.14)` and
   `f(f_{∇_L}^n) ⊑ f_{∇_L}^n ⇔ g(g_{∇_M}^n) ⊑ g_{∇_M}^n` `(4.15)`). Applying `∇_L` selectively at CFG loop headers while
   keeping `L` elsewhere strictly improves precision over global `α ∘ f ∘ γ`
   [PPA Lemma 4.45, p. 269] (book p. 269; PDF p. 286); [PPA §4.5.3, p. 270] (book p. 270; PDF p. 287).
3. **Failure of `γ`-induced narrowing (`Exercise 4.24`, `G-U4b-18`)**: **`l_1 Δ_L l_2 = γ(α(l_1) Δ_M α(l_2))` is NOT a
   narrowing operator** whenever `γ ∘ α ≠ id_L` (even on a Galois insertion with finite `M`!), because `l_1 ∉ γ[M]` gives
   `l_1 Δ_L l_1 = γ(α(l_1)) ⋢ l_1` [PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299).

## 7. Capstone Applications and Verified Source Errata (Mini Projects 4.1-4.3 and Exercises 4.15-4.24)

- **`Mini Projects 4.1–4.3` (`G-U4b-22`)**: `Mini Project 4.1` builds list-pair Galois insertion `(𝒫(V × V), α, γ, 𝒫(LR))`
  (`LR ⊆ 𝒫({H, S}) × Range`, `16` atoms under formal asymmetric suffix vs `20` under symmetric gloss, `([], []) ↦ ({S}, 0)`);
  `Mini Project 4.2` connects concrete `(State × Heap)` `SH` to `§2.6` Shape Analysis `(𝒫(State × Heap), α_{SA}, γ_{SA}, 𝒫(SG))`
  (non-insertion, `f_ℓ^{SA} ⊐ α_{SA} ∘ f_ℓ^{SH} ∘ γ_{SA}`); `Mini Project 4.3` lifts `(𝒫(Val), α, γ, L)` to `§3.5`
  `γ'(Ĉ, D̂, ρ̂, δ̂) ⊨_{SV} e` [PPA Mini Project 4.1, p. 274] (book p. 274; PDF p. 291);
  [PPA Mini Project 4.2, p. 274] (book p. 274; PDF p. 291); [PPA Mini Project 4.3, p. 275] (book p. 275; PDF p. 292).
- **Source errata & backlog (`BKL-063`, `BKL-065`, `BKL-069`, `BKL-070`, `BKL-071`, `BKL-072`)**: `p. 249` `"a relative small set"` / `"have"`; `p. 266` `"that that"`; `Mini Project 4.1` (`p. 274`, `BKL-070`) formal asymmetric suffix (`16` atoms) vs symmetric gloss (`20` atoms); `§4.5.2` `SS` (`p. 265`, `BKL-071`) node-attached `f_ℓ^{SS}([b]^ℓ) = Σ` vs edge guards; `Proposition 4.44` (`p. 268`, `BKL-069`) `(α(l_n)_n)` and unstated `n_0 ≥ 1` in `(ii)`; `Lemma 4.45` (`p. 269`, `BKL-063`) **`g(g_{∇_L}^n) ⊑ g_{∇_M}^n`** for `g(g_{∇_M}^n)`; `p. 270` `"turn"`; `Mini Project 4.3` (`p. 275`, `BKL-065`) `Example 4.40` for `Example 4.4` plus **`d̂`** for **`δ̂`**; and `Exercise 4.24` (`p. 282`, `BKL-072`) broken `γ`-induced narrowing
  [PPA Lemma 4.45, p. 269] (book p. 269; PDF p. 286); [PPA Mini Project 4.3, p. 275] (book p. 275; PDF p. 292).
