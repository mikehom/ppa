<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L1 formal reference for Chapter 4 §4.3 Galois connections, adjoint extraction, Galois insertions, reduction operators, upper closure operators, and duality laws. -->

# Galois Connections, Adjoint Extraction, Galois Insertions, and Closure Operators

Self-contained formal reference for Chapter 4 §4.3 (*Galois Connections*: §§4.3.1–4.3.2), `Concluding Remarks` on upper
closure operators and lattice/guard duality, `Figure 4.10` (`Sign'`), and `Exercises 4.13–4.14` of *Principles of
Program Analysis* ([PPA §4.3, p. 233] (book p. 233; PDF p. 250) through [PPA Example 4.32, p. 246] (book p. 246; PDF p. 263),
[PPA Chapter 4 Concluding Remarks, p. 270] (book p. 270; PDF p. 287) through
[PPA Chapter 4 Concluding Remarks, p. 273] (book p. 273; PDF p. 290), and
[PPA Exercise 4.13, p. 279] (book p. 279; PDF p. 296) through [PPA Exercise 4.14, p. 279] (book p. 279; PDF p. 296)).
Correctness relations and widening/narrowing live in
[correctness-and-fixed-points.md](./correctness-and-fixed-points.md); systematic combinators and induced operations
live in [combinators-and-induced-operations.md](./combinators-and-induced-operations.md).

## 1. Galois Connections and the Adjunction Law (Section 4.3)

Let `(L, ⊑_L)` (concrete or fine-grained space) and `(M, ⊑_M)` (abstract or coarser space) be complete lattices. A
quadruple `(L, α, γ, M)` (`Figure 4.6`) is a **Galois connection** iff **abstraction function** `α : L → M` and
**concretisation function** `γ : M → L` are **monotone** and satisfy Displays `(4.8)` and `(4.9)`
[PPA §4.3, p. 234] (book p. 234; PDF p. 251); [PPA Figure 4.6, p. 235] (book p. 235; PDF p. 252):
```text
γ ∘ α  ⊒  λl. l         (∀l ∈ L : l ⊑ γ(α(l))  — γ ∘ α is extensive)                               (4.8)
α ∘ γ  ⊑  λm. m         (∀m ∈ M : α(γ(m)) ⊑ m  — α ∘ γ is reductive)                               (4.9)
```

- **`Proposition 4.20` (Equivalence with Adjunction `(4.10)`, `G-U4a-17`)**: `(L, α, γ, M)` is a Galois connection
  (monotone `α, γ` satisfying `(4.8)` and `(4.9)`) **iff** `(L, α, γ, M)` is an **adjunction** satisfying Display `(4.10)`
  [PPA Proposition 4.20, p. 236] (book p. 236; PDF p. 253):
  ```text
  ∀l ∈ L, ∀m ∈ M :   α(l) ⊑ m    ⇔    l ⊑ γ(m)                                                     (4.10)
  ```
  *Crucial asymmetric precondition*: `(4.8)` and `(4.9)` **do not** imply monotonicity on their own (`α, γ` monotonicity
  must be checked explicitly), whereas `(4.10)` **automatically implies** monotonicity of both `α` and `γ`!
- **Canonical numerical instance (`Example 4.19`, `G-U4a-17`)**: `(𝒫(Z), α_{ZI}, γ_{ZI}, Interval)` sets
  `γ_{ZI}(int) = {z ∈ Z | inf(int) ≤ z ≤ sup(int)}` (`γ_{ZI}(⊥) = ∅`) and **case-splits `α_{ZI}(∅) = ⊥`** separately from
  `α_{ZI}(Z) = [inf'(Z), sup'(Z)]` (`Z ≠ ∅`, where `inf'(∅) = ∞` and `sup'(∅) = -∞` cannot form `[∞, -∞]` because
  `[z_1, z_2]` requires `z_1 ≤ z_2`) [PPA Example 4.19, p. 235] (book p. 235; PDF p. 252).

## 2. Representation and Extraction Galois Connections (Section 4.3)

Every single-element description lifts systematically to powersets (`G-U4a-18`)
[PPA §4.3, p. 237] (book p. 237; PDF p. 254); [PPA §4.3, p. 238] (book p. 238; PDF p. 255):

1. **From a representation function `β : V → L`**: For complete lattice `L`, define `(𝒫(V), α, γ, L)` by
   ```text
   α(V') = ⨆{ β(v) | v ∈ V' }        and        γ(l) = { v ∈ V | β(v) ⊑ l }.
   ```
   Adjunction `(4.10)` holds directly: `⨆{β(v) | v ∈ V'} ⊑ l ⇔ ∀v ∈ V' : β(v) ⊑ l ⇔ V' ⊆ γ(l)` (linking `§1.5` collecting
   semantics, `BKL-029`, `BKL-033`) [PPA §1.5, p. 15] (book p. 15; PDF p. 35);
   [PPA §4.3, p. 237] (book p. 237; PDF p. 254).
2. **From an extraction function `η : V → D` (`Example 4.21`, `Figure 4.7`)**: Specialising `L = (𝒫(D), ⊆)` and
   `β(v) = {η(v)}` yields `(𝒫(V), α_η, γ_η, 𝒫(D))`:
   ```text
   α_η(V') = { η(v) | v ∈ V' }       and        γ_η(D') = { v ∈ V | η(v) ∈ D' }.
   ```
   `Example 4.21` and `Figure 4.7` instantiate `sign : Z → Sign` (`Sign = {-, 0, +}`) over the 8-element Boolean cube
   `(𝒫(Sign), ⊆)` [PPA Figure 4.7, p. 238] (book p. 238; PDF p. 255);
   [PPA Example 4.21, p. 238] (book p. 238; PDF p. 255).

## 3. Adjoint Uniqueness, Complete Preservation, and Non-Existence Obstructions (Section 4.3.1)

### 3.1 `Lemma 4.22`, `Lemma 4.23`, and `Fact 4.24` (`G-U4a-19`)

In `(L, α, γ, M)`, `α` is the **lower (or left) adjoint** and `γ` is the **upper (or right) adjoint** [PPA §4.3.1, p. 239] (book p. 239; PDF p. 256):

- **`Lemma 4.22`**:
  1. *Mutual uniqueness*: `γ(m) = ⨆{l ∈ L | α(l) ⊑ m}` and `α(l) = ⨅{m ∈ M | l ⊑ γ(m)}`.
  2. *Join/meet preservation*: `α` is **completely additive** (`α(⨆ L') = ⨆{α(l) | l ∈ L'}`, hence **`α(⊥_L) = ⊥_M`**),
     and `γ` is **completely multiplicative** (`γ(⨅ M') = ⨅{γ(m) | m ∈ M'}`, hence **`γ(⊤_M) = ⊤_L`**). *(Neither
     `α(⊤_L) = ⊤_M` nor `γ(⊥_M) = ⊥_L` holds in general — e.g. `BKL-033` where `γ(∅)` contains the empty trace!)*
     [PPA Lemma 4.22, p. 239] (book p. 239; PDF p. 256).
- **`Lemma 4.23` (One-sided synthesis)**: Any completely additive `α : L → M` uniquely determines `γ` making `(L, α, γ, M)`
  a Galois connection; dually, any completely multiplicative `γ : M → L` uniquely determines `α`
  [PPA Lemma 4.23, p. 239] (book p. 239; PDF p. 256).
- **`Fact 4.24` (Zig-zag identities)**: `α ∘ γ ∘ α = α` and `γ ∘ α ∘ γ = γ`
  [PPA Fact 4.24, p. 240] (book p. 240; PDF p. 257).
- **Transporting correctness relations (`G-U4a-21`)**: Given `R` on `V × L` satisfying `(4.4)` and `(4.5)` (generated by
  `β : V → L`), `v S m iff v R (γ(m))` satisfies `(4.4)` and `(4.5)` on `V × M` (specifically by complete multiplicativity
  of `γ`!) and is generated by **`α ∘ β : V → M`** [PPA §4.3.1, p. 241] (book p. 241; PDF p. 258).

### 3.2 Non-Existence on `𝒫(Sign)` (`Example 4.25`) vs Repair via `Sign'` (`Figure 4.10`, `Exercise 4.13`)

- **Failure (`Example 4.25`, `G-U4a-20`)**: Defining monotone `γ_{IS} : 𝒫(Sign) → Interval` with `γ_{IS}({-, +}) = [-∞, ∞]`
  and `γ_{IS}({-, 0}) = [-∞, 0]` violates binary meet preservation (`Appendix A Lemma A.4` `(iii)`):
  ```text
  γ_{IS}({-, 0} ∩ {-, +}) = γ_{IS}({-}) = [-∞, -1]   ≠   [-∞, 0] = [-∞, 0] ⊓ [-∞, ∞] = γ_{IS}({-, 0}) ⊓ γ_{IS}({-, +})
  ```
  so **no lower adjoint `α_{IS} : Interval → 𝒫(Sign)` exists** [PPA Example 4.25, p. 240] (book p. 240; PDF p. 257).
- **Repair (`Figure 4.10`, `Exercise 4.13`, `G-U4b-23`)**: Deleting `{-, +}` yields the 7-element complete lattice
  `Sign' = {⊥, -, 0, +, -0, 0+, ⊤}` (`Figure 4.10`, where `- ⊔ + = ⊤` and `{⊥, -, -0, +, ⊤}` forms the non-distributive
  pentagon `N_5` [external]). On `Sign'`, `γ_{IS'}` preserves `⊤` and all incomparable meets (`γ_{IS'}(-0) ⊓ γ_{IS'}(0+) = [0, 0] = γ_{IS'}(0)`,
  `γ_{IS'}(-0) ⊓ γ_{IS'}(+) = [-∞, 0] ⊓ [1, ∞] = ⊥` over discrete `Z`), yielding a Galois insertion `(Interval, α_{IS'}, γ_{IS'}, Sign')`
  [PPA Figure 4.10, p. 276] (book p. 276; PDF p. 293); [PPA Exercise 4.13, p. 279] (book p. 279; PDF p. 296).

## 4. Galois Insertions and Four Equivalent Characterisations (Section 4.3.2)

`(L, α, γ, M)` (`Figure 4.8`) is a **Galois insertion** iff `α, γ` are monotone, `γ ∘ α ⊒ λl.l`, and **`α ∘ γ = λm.m`**
(eliminating redundant abstract elements that share identical `γ`-meaning, as in `Example 4.26` `(𝒫(Z), α_{ZI}, γ_{ZI}, Interval)`)
[PPA §4.3.2, p. 242] (book p. 242; PDF p. 259); [PPA Figure 4.8, p. 243] (book p. 243; PDF p. 260);
[PPA Example 4.26, p. 243] (book p. 243; PDF p. 260).

- **`Lemma 4.27` (`G-U4a-22`)**: For any Galois connection `(L, α, γ, M)`, the following four conditions are equivalent
  [PPA Lemma 4.27, p. 243] (book p. 243; PDF p. 260):
  1. `(i)` `(L, α, γ, M)` is a Galois insertion (`α ∘ γ = λm.m`);
  2. `(ii)` `α` is surjective (`∀m ∈ M : ∃l ∈ L : α(l) = m`);
  3. `(iii)` `γ` is injective (`∀m_1, m_2 ∈ M : γ(m_1) = γ(m_2) ⇒ m_1 = m_2`);
  4. `(iv)` `γ` is an order-similarity (`∀m_1, m_2 ∈ M : γ(m_1) ⊑ γ(m_2) ⇔ m_1 ⊑ m_2`).
- **Extraction corollary (`Exercise 4.14`, `Example 4.28`)**: `(𝒫(V), α_η, γ_η, 𝒫(D))` is a Galois insertion **iff `η : V → D`
  is surjective**; in `Example 4.28`, `signparity : Z → Sign × Parity` fails surjectivity at uninhabited `(0, odd)`
  (`γ_{signparity}({(0, odd)}) = ∅ = γ_{signparity}(∅)`) [PPA Example 4.28, p. 244] (book p. 244; PDF p. 261);
  [PPA Exercise 4.14, p. 279] (book p. 279; PDF p. 296).

## 5. Reduction Operator, Image Quotient, and Isomorphism (Section 4.3.2)

- **`Proposition 4.29`, `Figure 4.9`, and `Facts 4.30–4.31` (`G-U4a-23`, `G-U4b-01`, `BKL-024`)**: For any Galois connection
  `(L, α, γ, M)`, define the **reduction operator** `ς : M → M` (`Figure 4.9`; overloaded with `§2.5 p. 86` store
  `ς` — see `BKL-024`, alongside `ϕ` `p. 225` and `Δ` `p. 230`) by
  [PPA Proposition 4.29, p. 244] (book p. 244; PDF p. 261); [PPA Figure 4.9, p. 245] (book p. 245; PDF p. 262);
  [PPA Fact 4.30, p. 245] (book p. 245; PDF p. 262); [PPA Fact 4.31, p. 245] (book p. 245; PDF p. 262):
  ```text
  ς(m) = ⨅{ m' ∈ M | γ(m) = γ(m') } = α(γ(m))        with        ς[M] = α[L].
  ```
  Then `(ς[M], ⊑_M)` is a complete lattice — where **joins coincide with `M`** (`⨆_{ς[M]} M' = ⨆_M M'`, `Fact 4.30`)
  while **meets apply `ς`** (`⨅_{ς[M]} M' = ς(⨅_M M') = α(⨅_L γ[M'])`, which can be strictly below `⨅_M M'`) — and
  `(L, α, γ, ς[M])` (corestricting `α`, restricting `γ`) is a **Galois insertion**.
- **Extraction reduction & Galois connection isomorphism (`p. 246`, `Example 4.32`, `Exercise 4.14`)**:
  - For `η : V → D`, `ς_η(D') = D' ∩ η[V]`, making `ς_η[𝒫(D)] = 𝒫(η[V])` (yielding the 5-atom / 32-element insertion
    `(𝒫(Z), α_{signparity}, γ_{signparity}, 𝒫(signparity[Z]))` in `Example 4.32`)
    [PPA §4.3.2, p. 246] (book p. 246; PDF p. 263); [PPA Example 4.32, p. 246] (book p. 246; PDF p. 263).
  - `(L_1, α_1, γ_1, M_1)` is **isomorphic** to `(L_2, α_2, γ_2, M_2)` iff lattice isomorphisms `θ_L : L_1 → L_2` and
    `θ_M : M_1 → M_2` satisfy `α_2 = θ_M ∘ α_1 ∘ θ_L^{-1}` and `γ_2 = θ_L ∘ γ_1 ∘ θ_M^{-1}`
    [PPA §4.3.2, p. 246] (book p. 246; PDF p. 263).

## 6. Upper Closure Operators and Duality Laws (Concluding Remarks)

1. **Upper closure operators `ρ : L → L` (`G-U4b-19`)**: Monotone, **extensive** (`ρ ⊒ λl.l`), and **idempotent**
   (`ρ ∘ ρ = ρ`). Every `(L, α, γ, M)` induces upper closure `γ ∘ α : L → L`; conversely `ρ[L] = Fix(ρ) = {l ∈ L | l = ρ(l)}`
   gives Galois insertion `(L, ρ, λl.l, ρ[L])`. Ordered pointwise (`ρ_1 ⊑ ρ_2 ⇔ ∀l : ρ_1(l) ⊑ ρ_2(l) ⇔ ρ_2[L] ⊆ ρ_1[L]`,
   where `ρ_2` is *more approximate*), upper closure operators on `L` (`uco(L)` [external]) form a complete lattice with
   least `λl.l`, greatest `λl.⊤`, and **binary glb `ρ_1 ⊓ ρ_2` equal to the reduced product** (`§4.4.2`)
   [PPA Chapter 4 Concluding Remarks, p. 270] (book p. 270; PDF p. 287);
   [PPA Chapter 4 Concluding Remarks, p. 271] (book p. 271; PDF p. 288).
2. **Lattice duality (`⊑^d` = `⊒`), dual Galois guards, and Denotational Semantics non-duality (`G-U4b-20`, `G-U4b-21`)**:
   - *Classical DFA vs Abstract Interpretation*: Exact lattice duals (`⊥` uninformative / `gfp` vs `⊤` uninformative /
     `lfp`; monotonicity is self-dual) [PPA Chapter 4 Concluding Remarks, p. 273] (book p. 273; PDF p. 290).
   - *Transformation enabling guards `l_ℓ ⊑ l_Ξ`*: Soundness of approximate check `l'_ℓ ⊑ l'_Ξ ⇒ l_ℓ ⊑ l_Ξ` requires
     approximating reachable facts **upward** (`l_ℓ ⊑ l'_ℓ`, Galois connection) and enabling conditions **downward**
     (`l'_Ξ ⊑ l_Ξ`, **dual Galois connection**) [PPA Chapter 4 Concluding Remarks, p. 273] (book p. 273; PDF p. 290).
   - *Denotational Semantics is NOT dual*: Denotational Semantics puts "no information" at `⊥` (growing upward) while
     Abstract Interpretation puts "no information" at `⊤` (precision growing downward), yet **both seek `lfp`**
     [PPA Chapter 4 Concluding Remarks, p. 273] (book p. 273; PDF p. 290).

## 7. Verified Source Errata and Boundary Subtleties (Section 4.3 and Concluding Remarks)

- `Lemma 4.22` proof (`p. 239`) prints `"are Galois connection"`; `Example 4.25` (`p. 241`) says `"all pairs"` while
  listing `9` unordered incomparable pairs; `Fact 4.31` (`p. 245`) prints stray acute `=ˊ∏`; `Concluding Remarks`
  (`p. 271`, `BKL-064`) writes `ρ_2(L)` with round parens and mis-cites `Section 4.3.` instead of `§4.4.2` for the reduced product;
  and `Exercise 4.14` (`p. 279`, `BKL-066`) prints `ς_η(V') = V' ∩ η[V]` instead of `ς_η(D') = D' ∩ η[V]`
  [PPA Fact 4.31, p. 245] (book p. 245; PDF p. 262); [PPA Chapter 4 Concluding Remarks, p. 271] (book p. 271; PDF p. 288);
  [PPA Exercise 4.14, p. 279] (book p. 279; PDF p. 296).
