<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Self-contained L1 comparative reference for Chapter 3 sections 3.5-3.6, Concluding Remarks paradigm extensions, Mini Projects 3.2 and 3.4, and Exercises 3.14-3.17. -->

# Combined CFA+DFA, Uniform k-CFA, CPA, and Polyvariant Extensions (Sections 3.5-3.6, End Matter)

Self-contained `L1` formal reference for Sections 3.5-3.6 and Chapter 3 End Matter
([PPA §3.5, p. 182] (book p. 182; PDF p. 200) to [PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227)).
Chapter 2 Monotone Frameworks (`§2.3`) and interprocedural contexts (`§2.5`) unified in Section 4 below live in
[intraprocedural-analyses-and-frameworks.md](../../ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md)
and [interprocedural-and-correctness.md](../../ppa-dataflow-and-slicing/references/interprocedural-and-correctness.md).

## 1. Coupled CFA + Data Flow: Powerset Val_d vs Complete-Lattice D (Section 3.5, Tables 3.8-3.9, Figure 3.6)

- **Scope & style (`G-U3b-01`, `G-U3b-02`)**: Section 3.5 starts mid-page on `p. 182` and gives declarative
  acceptability relations (`⊨_d` in `Table 3.8`, `⊨_D` in `Table 3.9`) without repeating `§§3.2-3.4`'s SOS proofs
  or constraint lowering (`Exercise 3.14` supplies demand-driven and syntax-directed variants)
  [PPA §3.5, p. 182] (book p. 182; PDF p. 200) [PPA Exercise 3.14, p. 208] (book p. 208; PDF p. 226).
- **Powerset integration `Val̂_d = 𝒫(Term ∪ Data)` (`§3.5.1`, `Table 3.8`, `Figure 3.6`, `G-U3b-03..05`)**:
  Given abstract base constants `Data` (including `d_true = tt`, `d_false = ff`; e.g. `Data_sign = {tt, ff, -, 0, +}`),
  `d_c ∈ Data` (`d_7 = +`), and `d_op : Data × Data → 𝒫(Data)` lifted via
  `v̂₁ op̂ v̂₂ = ⋃ {d_op(d₁, d₂) | d₁ ∈ v̂₁ ∩ Data, d₂ ∈ v̂₂ ∩ Data}`
  (`∩ Data` strips closures; `Example 3.26` Detection of Signs sets `d_+(+, -) = {-, 0, +}` and returns
  `∅` on type mismatches like `+` + `tt`), `Table 3.8` defines `(Ĉ, ρ̂) ⊨_d e`
  [PPA Example 3.26, p. 183] (book p. 183; PDF p. 201) [PPA Table 3.8, p. 184] (book p. 184; PDF p. 202):
  - `[con]`: `{d_c} ⊆ Ĉ(ℓ)`; `[op]`: `(Ĉ, ρ̂) ⊨_d t₁^{ℓ₁} ∧ (Ĉ, ρ̂) ⊨_d t₂^{ℓ₂} ∧ Ĉ(ℓ₁) op̂ Ĉ(ℓ₂) ⊆ Ĉ(ℓ)`;
  - `[if]`: `(Ĉ, ρ̂) ⊨_d t₀^{ℓ₀}` plus **`(d_true ∈ Ĉ(ℓ₀) ⇒ ((Ĉ, ρ̂) ⊨_d t₁^{ℓ₁} ∧ Ĉ(ℓ₁) ⊆ Ĉ(ℓ)))`** and
    **`(d_false ∈ Ĉ(ℓ₀) ⇒ ((Ĉ, ρ̂) ⊨_d t₂^{ℓ₂} ∧ Ĉ(ℓ₂) ⊆ Ĉ(ℓ)))`** (`[var], [fn], [fun], [app], [let]` as in `Table 3.1`).
  - **Mutual precision (`Example 3.27`, `Figure 3.6`) & non-projection (`G-U3b-04`, `BKL-056`)**: On
    `(let f = (fn x => (if (x^1 > 0^2)^3 then (fn y => y^4)^5 else (fn z => 25^6)^7)^8)^9 in ((f^{10} 3^{11})^{12} 0^{13})^{14})^{15}`,
    `Ĉ(3) = {tt}` prunes the `else` branch (`Ĉ(7) = ∅`, `Ĉ(8) = Ĉ(12) = {fn y => y^4}`,
    `Ĉ(13) = Ĉ(14) = Ĉ(15) = {0}`) [PPA Example 3.27, p. 184] (book p. 184; PDF p. 202)
    [PPA Figure 3.6, p. 185] (book p. 185; PDF p. 203). Consequently `(Ĉ, ρ̂) ⊨_d e` does **not** project to
    `Table 3.1` (`⊨_d ⇏ ⊨` on pruned dead branches, `G-U3b-04`). Termination requires **finite `Data`** (`G-U3b-05`).
- **Complete-lattice integration `(Ĉ, D̂, ρ̂, δ̂) ⊨_D e` (`§3.5.2`, `Table 3.9`, `G-U3b-05..09`, `BKL-056`)**:
  Splitting `𝒫(Term ∪ Data) ≅ 𝒫(Term) × 𝒫(Data)` replaces `(𝒫(Data), ⊆)` with any **ACC** complete lattice
  `L` (`G-U3b-05`) inside a *monotone structure instance* `(L, ℱ, ι., f.)` (`ι_c ∈ L`, `f_op ∈ ℱ₂ : L × L → L`;
  `Example 3.28` embeds `§3.5.1`; `Example 3.29` defines Constant Propagation on `Z_⊥^⊤ × 𝒫({tt, ff})` where
  `f_+` must check strict `z₁ = ⊥ or z₂ = ⊥ ↦ (⊥, ∅)` before `⊤`, `G-U3b-07`)
  [PPA Example 3.28, p. 186] (book p. 186; PDF p. 204) [PPA Example 3.29, p. 186] (book p. 186; PDF p. 204).
  Over `D̂ ∈ Lab → L` and `δ̂ ∈ Var → L`, `Table 3.9` pairs every `Ĉ`/`ρ̂` inclusion with `D̂`/`δ̂` (`⊑`) (`[op]`
  erased in OCR on `p. 188`, `G-U3b-30`, `BKL-011`) and gates `[if]` by `ι_true ⊑ D̂(ℓ₀)` and `ι_false ⊑ D̂(ℓ₀)`
  (`Example 3.30`) [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206) [PPA Example 3.30, p. 187] (book p. 187; PDF p. 205).
  - **Non-singleton guard flaw (`G-U3b-08`, `BKL-056`)**: If `ι_true` abstracts >1 concrete truth value (e.g. C
    non-zero integers where `ι_true = ⊤_Z`), a singleton constant `D̂(ℓ₀) = 1` fails `ι_true ⊑ D̂(ℓ₀)` and
    unsoundly skips `then`! Always enforce `D̂(ℓ₀) ⊓ ι_true ≠ ⊥` or singleton `{tt}`/`{ff}` booleans (`Example 3.29`).
  - **Online `⊨_D` vs two-phase staged `⊨'_D` (`Example 3.31`, `G-U3b-09`)**: Dropping `[if]` guards yields
    staged `⊨'_D` (`0-CFA` first, then `DFA` over the fixed call graph), restoring `⊨'_D ⇒ ⊨` (`G-U3b-09`) at
    precision loss (`fn z => 25^6` enters `Ĉ(7), Ĉ(8), Ĉ(12)` in `Example 3.31`, polluting `D̂(6) = {+}`,
    `δ̂(z) = {0}`, and `D̂(14) = D̂(15) = {0, +}` vs Figure 3.6's `{0}`)
    [PPA §3.5.2, p. 189] (book p. 189; PDF p. 207) [PPA Example 3.31, p. 189] (book p. 189; PDF p. 207).

## 2. Monovariant Poisoning and Uniform k-CFA (Sections 3.6-3.6.1, Table 3.10)

- **Monovariant poisoning (`Examples 3.32-3.33`, `G-U3b-10`)**: On `(let f = (fn x => x^1)^2 in ((f^3 f^4)^5 (fn y => y^6)^7)^8)^9`,
  monovariant `0-CFA` merges both calls to `f` into `ρ̂_id(x) = {fn x => x^1, fn y => y^6}`, smearing the final
  result `Ĉ_id(8) = Ĉ_id(9)` **and** poisoning the intermediate operator `Ĉ_id(5)` so the second call falsely
  dispatches to `fn y => y^6` as well as `fn x => x^1` (`Example 3.33` clones `f₁, f₂` syntactically, failing on
  recursion) [PPA Example 3.32, p. 190] (book p. 190; PDF p. 208) [PPA Example 3.33, p. 191] (book p. 191; PDF p. 209).
- **Uniform `k`-CFA vs standard & polynomial `k`-CFA (`§3.6.1`, `Table 3.10`, `G-U3b-11..16`, `G-U3b-29`, `BKL-007`, `BKL-057`)**:
  With `Δ = Lab^{≤k}` (sequences of `≤ k` call-site labels; `k = 0 ⇒ Δ = {Λ}` recovers `0-CFA`) and
  `ce ∈ CEnv = Var → Δ` (`ce | FV(...)` at definitions; see `BKL-057` on total `Var → Δ` vs `ce₀ = []`):
  - **Standard `k`-CFA (`[156, 157, 158]`, `[external: Shivers]`, `pp. 191, 193`)**:
    `Val̂ = 𝒫(Term × CEnv)`, `Env̂ = (Var × Δ) → Val̂`, **`Cachê = (Lab × CEnv) → Val̂`**.
  - **Uniform `k`-CFA (`Table 3.10`, `pp. 191–192`)**: retains **`Val̂ = 𝒫(Term × CEnv)`** and
    `Env̂ = (Var × Δ) → Val̂`, simplifying caches to **`Cachê = (Lab × Δ) → Val̂`** (`G-U3b-11`)
    [PPA §3.6.1, p. 191] (book p. 191; PDF p. 209) [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210):
    - `[var]`: `(Ĉ, ρ̂) ⊨_δ^{ce} x^ℓ iff ρ̂(x, ce(x)) ⊆ Ĉ(ℓ, δ)` — looks up **lexical birth contour `ce(x)`**,
      *never* current `δ` (`p. 193` prose matches `ρ̂(x, ce(x))` cleanly, `G-U3b-12`).
    - `[fn]` / `[fun]`: `{(fn x => e₀, ce₀)} ⊆ Ĉ(ℓ, δ)` capturing `ce₀ = ce | FV(fn x => e₀)`.
    - `[app]`: for `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ` at `(δ, ce)` and `(fn x => t₀^{ℓ₀}, ce₀) ∈ Ĉ(ℓ₁, δ)`, pushes the
      **application's outer label `ℓ`** via `δ₀ = ⌈δ, ℓ⌉_k`, extends `ce'_0 = ce₀[x ↦ δ₀]`, and checks
      `(Ĉ, ρ̂) ⊨_{δ₀}^{ce'_0} t₀^{ℓ₀}`, `Ĉ(ℓ₂, δ) ⊆ ρ̂(x, δ₀)`, and `Ĉ(ℓ₀, δ₀) ⊆ Ĉ(ℓ, δ)`
      (plus `{(fun f x => t₀^{ℓ₀}, ce₀)} ⊆ ρ̂(f, δ₀)` and `ce'_0 = ce₀[f ↦ δ₀, x ↦ δ₀]` for `fun`, `G-U3b-13`).
    - `[let]`: keeps `δ` **unchanged** (`ce' = ce[x ↦ δ]`), because `let` is local binding, not dynamic dispatch
      [PPA §3.6.1, p. 193] (book p. 193; PDF p. 211).
  - **Precision & complexity (`Example 3.34`, `pp. 194-195`, `BKL-007`)**: Uniform `1-CFA` (`Example 3.34`,
    which mis-cites `Example 3.33` for `Example 3.32`, `G-U3b-14`, `BKL-057`) isolates contexts `5` and `8`,
    yielding exact **`Ĉ'_id(8, Λ) = Ĉ'_id(9, Λ) = {(fn y => y^6, ce₀)}`** (`ce₀ = []`)
    [PPA Example 3.34, p. 194] (book p. 194; PDF p. 212).
    However, for `k ≥ 1`, **`|Val̂|`** lattice height `O(n · n^p)` (`p = O(n)` variables) makes **both** `1-CFA` and
    uniform `1-CFA` **exponential worst-case (`[external: DEXPTIME]`)** (`G-U3b-15`, `BKL-007`), whereas **Polynomial
    `k`-CFA** (`Val̂ = 𝒫(Term × Δ)`, replacing `CEnv` with single contour `Δ`; distinct from flat `Val̂ = 𝒫(Term)`
    `[external: m-CFA]`) runs in **`O(n⁶)`** at `k = 1` (at the cost of losing per-variable lexical separation on
    curried closures) [PPA §3.6.1, p. 195] (book p. 195; PDF p. 213). Empirically (`[80]`), `1-CFA` can run
    *faster* than `0-CFA` when precision prunes spurious call graphs (`G-U3b-16`)
    [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219). Under self-recursion, `⌈δ, ℓ⌉_k` flushes
    outer callers (`Exercise 3.15` compresses stuttering `[1,2,2,1,1] ↦ [2,1]`, `G-U3b-29`; `Exercise 3.16`
    specialises uniform `k`-CFA to first-order recursion equations, `BKL-062`)
    [PPA Exercise 3.15, p. 208] (book p. 208; PDF p. 226) [PPA Exercise 3.16, p. 209] (book p. 209; PDF p. 227).

## 3. Multi-Argument 0-CFA and Cartesian Product Algorithm (Section 3.6.2)

- **Closed `m`-ary syntax & CPA domains (`[2]`, `[external: Agesen]`, `G-U3b-17`, `Exercise 3.17`)**: Base `CPA` (`[2]`)
  restricts `FUN` to **closed, non-recursive** `m`-ary abstractions `fn x₁ ··· x_m => e₀` (`FV = ∅`, eliminating
  closure environments; `Exercise 3.17` restores `FV ≠ ∅` and `fun f x₁ ··· x_m`) with `Val̂ = 𝒫(Term)`,
  `Δ = ⋃_{m≥1} Term^m` (`p. 198` writes `Δ = Term`), `Env̂ = (Var × Δ) → Val̂`, `Cachê = (Lab × Δ) → Val̂`
  [PPA §3.6.2, p. 196] (book p. 196; PDF p. 214)
  [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215) [PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227).
- **`CPA [app]` clause, errata, empty-product hazard, and template memoisation (`G-U3b-18..20`, `BKL-058`)**:
  At `(t₀^{ℓ₀}(t₁^{ℓ₁}, ..., t_m^{ℓ_m}))^ℓ` in context `δ`, for each `(fn x₁, ···, x_m => t_b^{ℓ_b}) ∈ Ĉ(ℓ₀, δ)` and
  every **concrete argument tuple** `δ_b = (t'₁, ..., t'_m) ∈ Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ)`, `p. 197` requires
  `(Ĉ, ρ̂) ⊨_{CPA}^{δ_b} t_b^{ℓ_b} ∧ {t'₁} ⊆ ρ̂(x₁, δ_b) ∧ ··· ∧ {t'_m} ⊆ ρ̂(x_m, δ_b) ∧ Ĉ(ℓ_b, δ_b) ⊆ Ĉ(ℓ, δ)`
  [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215).
  - **Source errata (`F-U3b-05`, `G-U3b-18`, `BKL-058`)**: Printed `[app]` on `p. 197` drops a closing `)` before
    `^ℓ` on `(t₀^{ℓ₀}(t₁^{ℓ₁}, ···, t_m^{ℓ_m})^ℓ`, and writes `{δ_b} ⊆ ρ̂(x₁) × ··· × ρ̂(x_m)` **omitting `, δ_b`**
    (must read `ρ̂(x₁, δ_b) × ··· × ρ̂(x_m, δ_b)` to match `Env̂ = (Var × Δ) → Val̂`; `t_b^{ℓ_b}` and `Ĉ(ℓ_b, δ_b)`
    are already printed cleanly).
  - **Empty-product vacuity (`G-U3b-19`, `BKL-058`)**: If any `Ĉ(ℓ_j, δ) = ∅` (e.g. an integer constant argument
    `5^{ℓ_j}` in pure `CPA` without `§3.5` data tokens!), `Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ) = ∅` silently skips the
    entire call unless base types/tokens inhabit `Ĉ(ℓ_j, δ)` or empty slots use a fallback token.
  - **Templates & lazy expansion (`G-U3b-20`, `BKL-007`)**: Global memoisation shares one *template* per `(fn ..., δ_b)`
    across all call sites; lazy demand expansion avoids `|Ĉ(ℓ₁)| × ··· × |Ĉ(ℓ_m)|` blowup on unused parameters
    [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215) [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216).

## 4. Cross-Chapter Unifications U4 & U5: Chapter 2 Sections 2.3, 2.5 vs Chapter 3 Sections 3.5, 3.6

| Unification | Chapter 2 Construct | Chapter 3 Construct | Conditions for Correspondence | Key Differences |
| :--- | :--- | :--- | :--- | :--- |
| **`U4`** ([PPA Preface, p. VII] (book p. VII; PDF p. 7), [PPA §3.5.2, p. 186] (book p. 186; PDF p. 204)) | Monotone Framework `(L, ℱ, F, E, ι, f.)` (`§2.3`) | Monotone structure `(L, ℱ, ι., f.)` in `⊨_D` (`§3.5.2`, `Table 3.9`) | `L` complete lattice satisfying `ACC`; monotone operator family `ℱ` | `§3.5.2` omits static `flow` `F` and extremal `E` (`G-U3b-06` — `CFA` discovers flow dynamically) and couples `[if]` reachability to `Ĉ` |
| **`U5` (call strings)** ([PPA Preface, p. VII] (book p. VII; PDF p. 7), [PPA §3.6.1, p. 196] (book p. 196; PDF p. 214)) | Bounded call strings `Lab → (Δ → L)`, `Δ = Lab^{≤k}` (`§2.5.4`) | Uniform `k`-CFA `(Lab × Δ) → Val̂`, `Δ = Lab^{≤k}` (`§3.6.1`, `Table 3.10`) | Same call-site suffix domain `Δ = Lab^{≤k}` under currying `(A × B → C) ≅ (A → (B → C))` (`G-U3b-21`) | `§2.5.4` tracks data states across static procedures; Uniform `1-CFA` embeds `CEnv` inside `Val̂ = 𝒫(Term × CEnv)`, incurring exponential (`[external: DEXPTIME]`) worst case (`BKL-007`) |
| **`U5` (value summaries)** ([PPA Preface, p. VII] (book p. VII; PDF p. 7), [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216)) | Small assumption sets `Δ = D` (`§2.5.5`) | Cartesian Product Algorithm `Δ = Term^m` (`§3.6.2`) | Both index callee analyses by **individual** abstract argument tuples (`G-U3b-21`) | `CPA` avoids large assumption sets' `𝒫(D)` non-monotonicity (`BKL-003`) by distributing pointwise over `Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ)` |

## 5. Data Structures, Imperative Stores, OO/Concurrent Paradigms & Backlog (Mini Projects 3.2 & 3.4)

- **Algebraic data constructors (`Mini Project 3.2`, `G-U3b-26`, `BKL-060`)**: Extending `FUN` with `C(e₁, ···, e_n)`
  (`C ∈ Constr`) and `case e₀ of C(x₁, ···, x_n) => e₁ or x => e₂` uses **flat finite
  `Val̂ = 𝒫(Term ∪ {C(ℓ₁, ···, ℓ_n) | C ∈ Constr, ℓ₁, ···, ℓ_n ∈ Lab})`**; embedding expression labels `ℓ_i` inside
  `Val̂` breaks `Fact 3.11` and `Theorem 3.10` subject reduction because small-step SOS rewrites outer labels (`BKL-060`)
  [PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221).
- **Flow-sensitive imperative stores (`Mini Project 3.4`, `p. 200` `[133]`, `G-U3b-27`, `BKL-061`)**: Adding ML references
  `(new_π x := e₁ in e₂)^ℓ | (! x)^ℓ | (x := e₀)^ℓ | (e₁ ; e₂)^ℓ` with `me : Var → Pnt` extends acceptability to
  `(Ĉ, ρ̂, Ŝ_∘, Ŝ_•) ⊨_{me} e` (`Ŝ_∘, Ŝ_• : Lab → (Pnt → Val̂)`), challenging readers to formulate rules including
  `[assign]`. Because `π ∈ Pnt` abstracts multiple allocations, default `[assign]` performs `[external: weak update]`,
  while sound `[external: strong update]` (`"kill"`) requires both
  per-program-point local stores and abstract reference counts proving singleton allocation (`p. 200` `[133]`, `BKL-061`)
  [PPA Chapter 3 Concluding Remarks, p. 200] (book p. 200; PDF p. 218)
  [PPA Mini Project 3.4, p. 204] (book p. 204; PDF p. 222) [PPA Mini Project 3.4, p. 205] (book p. 205; PDF p. 223).
- **OO, concurrent, and logic paradigms (`Concluding Remarks`, `pp. 199-200`)**: OO dynamic dispatch `e₁.m(e₂)`
  specialises `0-CFA`/`CPA` (object/receiver-type sensitivity `[external]` is `1-ary CPA` on receiver classes);
  concurrent process calculi (`[external: Concurrent ML, π-calculus]`) track dynamic processes/channels similarly to
  closures (`[78, 57, 60, 22, 23]`); logic programming set-based analysis (`[72, 73]`, `[external: Prolog groundness]`)
  mirrors constraint propagation
  [PPA Chapter 3 Concluding Remarks, p. 199] (book p. 199; PDF p. 217)
  [PPA Chapter 3 Concluding Remarks, p. 200] (book p. 200; PDF p. 218).
- **Non-blocking backlog (`ARCHITECTURE.md` §6.4)**: `BKL-007` (`k-CFA` `[external: DEXPTIME]` vs polynomial
  `O(n^6)` `k`-CFA/`CPA` cost); `BKL-011` (`Table 3.9` `[op]` & `Example 3.34` OCR erasures, `G-U3b-30`); `BKL-056`
  (`§3.5` `⊨_d`/`⊨_D` non-projection & `ι_true` guard); `BKL-057` (`§3.6.1` `CEnv` `ce | FV` vs total `Var → Δ`
  & `Example 3.34` `"Example 3.33"`); `BKL-058` (`§3.6.2` `CPA` `[app]` `)`/`, δ_b` errata & empty-product vacuity);
  `BKL-060` (`Mini Project 3.1` `p. 202` `⊨_s` typo & `Mini Project 3.2` `p. 203` `Fact 3.11`); `BKL-061`
  (`Mini Project 3.4` unprinted `[assign]` design challenge & `p. 200` `[133]` strong-update precondition `[external]`).
