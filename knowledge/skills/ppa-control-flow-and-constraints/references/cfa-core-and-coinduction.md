<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Self-contained L1 comparative reference for Chapter 3 sections 3.1-3.3 (abstract 0-CFA, closure SOS, coinductive well-definedness, Moore families, and syntax-directed 0-CFA). -->

# Abstract and Syntax-Directed 0-CFA, Closure SOS, and Coinduction (Sections 3.1-3.3)

Self-contained `L1` formal reference for Chapter 3 opening through Section 3.3
([PPA Chapter 3, p. 141] (book p. 141; PDF p. 159) to [PPA Proposition 3.19, p. 173] (book p. 173; PDF p. 191)),
together with foundational `Exercises 3.1-3.12` ([PPA Exercise 3.1, p. 205] (book p. 205; PDF p. 223) to
[PPA Exercise 3.12, p. 208] (book p. 208; PDF p. 226)). Order-theoretic and coinductive prerequisites live in
[appendix-a-posets-lattices-fixed-points.md](../../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md)
and [appendix-b-induction-and-coinduction.md](../../ppa-program-analysis/references/appendix-b-induction-and-coinduction.md);
the Chapter 1 constraint preview lives in
[chapter-1-five-formulations.md](../../ppa-program-analysis/references/chapter-1-five-formulations.md).

## 1. Dynamic Dispatch, FUN Syntax, and Abstract 0-CFA (Section 3.1, Table 3.1, Figures 3.1-3.2)

- **Dynamic dispatch motivation (`G-U3a-01`, `G-U3a-05`)**: Chapter 2 interprocedural frameworks presuppose a
  statically known call relation `inter-flow_*`, which fails whenever functions or procedures are passed as
  parameters, returned as values, or dispatched dynamically (`let f = fn x => x 1 ... in (f g) + (f h)`)
  [PPA §3.1, p. 141] (book p. 141; PDF p. 159) [PPA §3.1, p. 142] (book p. 142; PDF p. 160). Control Flow
  Analysis (`CFA`) resolves dynamic dispatch by predicting for every subexpression label `ℓ` the set of
  abstractions it may evaluate to; at an application `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ`, `Ĉ(ℓ₁)` recovers the dynamic call
  graph (contrasting `§2.1.5` `ud`-chains, followed immediately by `Remark.` on unifying `(Var ∪ Lab) → Val̂`
  and compiler IRs `[external: CPS, ANF, three-address code]`) [PPA §3.1.1, p. 145] (book p. 145; PDF p. 163). Note Section 3.1 has only two
  subsections (`§3.1.1`, `§3.1.2`) and Chapter 3 has constant offset `PDF = book + 18` (`G-U3a-01`).
- **Labelled `FUN` syntax (`Exp`, `Term`, `G-U3a-02`, `BKL-051`)**: Every expression `e ∈ Exp` carries a
  top-level label (`e ::= t^ℓ`), whereas terms `t ∈ Term` are unlabelled
  [PPA §3.1, p. 142] (book p. 142; PDF p. 160):
  ```text
  e ::= t^ℓ
  t ::= c | x | fn x => e₀ | fun f x => e₀ | e₁ e₂
      | if e₀ then e₁ else e₂ | let x = e₁ in e₂ | e₁ op e₂
  ```
  - **Side conditions**: Labels are syntax pointers and are *not* required to be unique, though distinct
    subexpressions normally receive distinct labels so cache entries stay distinguishable; parentheses carry
    no extra labels (`(t^ℓ)` is `t^ℓ`) [PPA §3.1, p. 143] (book p. 143; PDF p. 161). `fn x => e₀` binds `x`
    in `e₀`; `fun f x => e₀` binds both `f` and `x` in `e₀`; `let x = e₁ in e₂` is **non-recursive** (`x`
    bound in `e₂`, not `e₁`; semicolon multi-bindings on p. 142 are informal sugar, `BKL-051`).
  - **Canonical benchmark programs**: Identity self-application `((fn x => x^1)^2 (fn y => y^3)^4)^5`
    [PPA Example 3.1, p. 143] (book p. 143; PDF p. 161) and non-terminating recursive `loop`:
    `(let g = (fun f x => (f^1 (fn y => y^2)^3)^4)^5 in (g^6 (fn z => z^7)^8)^9)^10`
    [PPA Example 3.2, p. 143] (book p. 143; PDF p. 161) [PPA Example 3.2, p. 144] (book p. 144; PDF p. 162).
- **Abstract domains (`Val̂`, `Env̂`, `Cachê`, `G-U3a-03`, `G-U3b-22`)**:
  `v̂ ∈ Val̂ = 𝒫(Term)`, `ρ̂ ∈ Env̂ = Var → Val̂`, `Ĉ ∈ Cachê = Lab → Val̂`
  [PPA §3.1.1, p. 144] (book p. 144; PDF p. 162). Pure `0-CFA` tracks only function terms (`fn`, `fun`),
  ignores non-function constants and closure environments, and collapses distinct bindings that share variable
  name `x` into one `ρ̂(x)` (behaving like dynamic scoping on shadowed names unless bound variables are
  renamed apart beforehand; see `G-U3a-03`, `G-U3b-22`, `BKL-059` [PPA Chapter 3 Concluding Remarks, p. 199] (book p. 199; PDF p. 217)).
- **Declarative `0-CFA` acceptability `(Ĉ, ρ̂) ⊨ e` (`Table 3.1`, `Figures 3.1-3.2`, `G-U3a-04`, `G-U3a-05`)**:
  `⊨ : (Cachê × Env̂ × Exp) → {true, false}` checks whether a proposed guess `(Ĉ, ρ̂)` is acceptable
  [PPA Table 3.1, p. 146] (book p. 146; PDF p. 164):
  ```text
  [con]  (Ĉ, ρ̂) ⊨ c^ℓ                           always
  [var]  (Ĉ, ρ̂) ⊨ x^ℓ                           iff  ρ̂(x) ⊆ Ĉ(ℓ)
  [fn]   (Ĉ, ρ̂) ⊨ (fn x => e₀)^ℓ                iff  {fn x => e₀} ⊆ Ĉ(ℓ)
  [fun]  (Ĉ, ρ̂) ⊨ (fun f x => e₀)^ℓ             iff  {fun f x => e₀} ⊆ Ĉ(ℓ)
  [app]  (Ĉ, ρ̂) ⊨ (t₁^{ℓ₁} t₂^{ℓ₂})^ℓ          iff  (Ĉ, ρ̂) ⊨ t₁^{ℓ₁} ∧ (Ĉ, ρ̂) ⊨ t₂^{ℓ₂} ∧
         (∀(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) :  (Ĉ, ρ̂) ⊨ t₀^{ℓ₀} ∧ Ĉ(ℓ₂) ⊆ ρ̂(x) ∧ Ĉ(ℓ₀) ⊆ Ĉ(ℓ)) ∧
         (∀(fun f x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) : (Ĉ, ρ̂) ⊨ t₀^{ℓ₀} ∧ Ĉ(ℓ₂) ⊆ ρ̂(x) ∧ Ĉ(ℓ₀) ⊆ Ĉ(ℓ) ∧ {fun f x => t₀^{ℓ₀}} ⊆ ρ̂(f))
  [if]   (Ĉ, ρ̂) ⊨ (if t₀^{ℓ₀} then t₁^{ℓ₁} else t₂^{ℓ₂})^ℓ
         iff  (Ĉ, ρ̂) ⊨ t₀^{ℓ₀} ∧ (Ĉ, ρ̂) ⊨ t₁^{ℓ₁} ∧ (Ĉ, ρ̂) ⊨ t₂^{ℓ₂} ∧ Ĉ(ℓ₁) ⊆ Ĉ(ℓ) ∧ Ĉ(ℓ₂) ⊆ Ĉ(ℓ)
  [let]  (Ĉ, ρ̂) ⊨ (let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ iff (Ĉ, ρ̂) ⊨ t₁^{ℓ₁} ∧ (Ĉ, ρ̂) ⊨ t₂^{ℓ₂} ∧ Ĉ(ℓ₁) ⊆ ρ̂(x) ∧ Ĉ(ℓ₂) ⊆ Ĉ(ℓ)
  [op]   (Ĉ, ρ̂) ⊨ (t₁^{ℓ₁} op t₂^{ℓ₂})^ℓ       iff  (Ĉ, ρ̂) ⊨ t₁^{ℓ₁} ∧ (Ĉ, ρ̂) ⊨ t₂^{ℓ₂}
  ```
  - **Flow diagrams**: `Figure 3.1` depicts `Ĉ(ℓ₁) ⊆ ρ̂(x) ⊆ Ĉ(ℓ')` and `Ĉ(ℓ₂) ⊆ Ĉ(ℓ)` for `[let]`/`[var]`
    [PPA Figure 3.1, p. 148] (book p. 148; PDF p. 166); `Figure 3.2` depicts membership guard
    `(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁)` triggering `Ĉ(ℓ₂) ⊆ ρ̂(x) ⊆ Ĉ(ℓ')` and `Ĉ(ℓ₀) ⊆ Ĉ(ℓ)` for `[app]`/`[fn]`/`[var]`
    [PPA Figure 3.2, p. 149] (book p. 149; PDF p. 167).
  - **Key side conditions**: `[fn]` and `[fun]` omit `(Ĉ, ρ̂) ⊨ e₀` (and `{fun ...} ⊆ ρ̂(f)`), deferring body
    checks to `[app]` only when the abstraction enters `Ĉ(ℓ₁)` (`G-U3a-04`). Thus in `Examples 3.3` and `3.5`,
    `((fn x => x^1)^2 (fn y => y^3)^4)^5` has minimal solution `Ĉ_e(3) = ρ̂_e(y) = ∅` because `fn y => y^3` is
    passed and returned (`Ĉ_e(5) = {fn y => y^3}`) but never called, dropping `fn y => y^3` from
    `ρ̂'_e(x) = ∅` violates `Ĉ'_e(4) ⊆ ρ̂'_e(x)`, and imprecise `(Ĉ''_e, ρ̂''_e)` (`{fn x => x^1, fn y => y^3}`
    everywhere) remains acceptable [PPA Example 3.3, p. 144] (book p. 144; PDF p. 162)
    [PPA Example 3.5, p. 148] (book p. 148; PDF p. 166). On `loop` (`Example 3.4`), `Ĉ_lp(4) = Ĉ_lp(9) = Ĉ_lp(10) = ∅`
    while `ρ̂_lp(x) = {id_y, id_z}` merges both call sites (`G-U3a-05`: context-insensitive and flow-insensitive,
    since `[app]` checks `t₂^{ℓ₂}` even when `Ĉ(ℓ₁) = ∅`) [PPA Example 3.4, p. 145] (book p. 145; PDF p. 163)
    [PPA §3.1.1, p. 150] (book p. 150; PDF p. 168).

## 2. Coinductive Well-Definedness: gfp(Q) vs lfp(Q) (Section 3.1.2, Section 3.2.4)

- **Why structural induction fails (`G-U3a-06`)**: In `[app]`, `(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁)` need not be a
  syntactic subexpression of `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ`. Viewing `Table 3.1` as a positive (hence monotone)
  functional `𝒬` on the complete lattice `((Cachê × Env̂ × Exp) → {true, false}, ⊑)` ordered by implication
  (`Q₁ ⊑ Q₂ iff ∀(Ĉ, ρ̂, e) : Q₁(Ĉ, ρ̂, e) ⇒ Q₂(Ĉ, ρ̂, e)`), Tarski's Theorem (`Proposition A.10`) yields fixed
  points, and acceptability is defined **coinductively** as `⊨ = gfp(𝒬)` (`Unification U9`,
  [PPA Preface, p. VII] (book p. VII; PDF p. 7)) [PPA §3.1.2, p. 150] (book p. 150; PDF p. 168)
  [PPA §3.1.2, p. 151] (book p. 151; PDF p. 169).
- **Dual fixed-point roles (`Analogy.`, `G-U3a-07`)**: On `loop` (`Example 3.6`), verifying
  `(Ĉ_lp, ρ̂_lp) ⊨ (f^1 id_y^3)^4` unfolds to the identical obligation; `gfp(𝒬)` accepts circular witnesses
  (`Q ⊑ 𝒬(Q)`), whereas `lfp(𝒬)` rejects infinite call cycles [PPA Example 3.6, p. 151] (book p. 151; PDF p. 169).
  The procurement analogy (`p. 152`) separates *loose specification* (`⊨ = gfp(𝒬)`, accepting every compliant
  over-approximation unless a clause is violated) from *cheapest compliant bid* (`lfp(F_⋆)` in `§3.4.2`,
  minimising `(Ĉ, ρ̂)` under `⊑`) [PPA §3.1.2, p. 152] (book p. 152; PDF p. 170).
- **Failure of inductive `⊨' = lfp(𝒬)` (`Proposition 3.16`, `G-U3a-16`, `BKL-053`)**:
  `There exists e_⋆ ∈ Exp such that {(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨' e_⋆} is not a Moore family`
  [PPA Proposition 3.16, p. 165] (book p. 165; PDF p. 183). Witness: single-label self-application
  `e_⋆ = ((fn x => (x^ℓ x^ℓ)^ℓ)^ℓ (fn x => (x^ℓ x^ℓ)^ℓ)^ℓ)^ℓ`. On the 2-element domain
  `Val̂_e = 𝒫({fn x => (x^ℓ x^ℓ)^ℓ})`, `gfp(𝒬) = ⊨` gives the singleton Moore family
  `Ĉ(ℓ) = ρ̂(x) = {fn x => (x^ℓ x^ℓ)^ℓ}`, whereas `lfp(𝒬) = ⊨'` requires `Ĉ(ℓ) = ρ̂(x) = ∅` on `(x^ℓ x^ℓ)^ℓ`
  and therefore yields the **empty set `∅`** on `e_⋆` (violating Moore-family non-emptiness `⨅ ∅ = ⊤ ∈ Y`;
  note `p. 165` writes `IExp_e` where `Exp_e` is meant, `BKL-053`)
  [PPA Proposition 3.16, p. 167] (book p. 167; PDF p. 185).

## 3. Closure SOS, Subject Reduction, and Moore Families (Sections 3.2.1-3.2.3, Tables 3.2-3.4, Figure 3.3)

- **Explicit-environment small-step SOS (`Tables 3.2-3.3`, `G-U3a-08..11`, `BKL-011`, `BKL-051`)**:
  Substitution `e₀[x ↦ v₂]` mutates/duplicates subterms and destroys unique syntax labels (`p. 153`, `p. 201`),
  so `FUN` evaluates intermediate syntax `ie ::= it^ℓ` extended with closures `close t in ρ` (`v ∈ Val` is `c`
  or `close t in ρ`) and local frames `bind ρ in ie` under left-to-right call-by-value transitions
  `ρ ⊢ ie₁ → ie₂` (`Examples 3.7-3.8`; OCR erases fraction-bar premises in `Tables 3.2-3.3`, `G-U3a-12`)
  [PPA §3.2.1, p. 153] (book p. 153; PDF p. 171) [PPA Table 3.2, p. 155] (book p. 155; PDF p. 173)
  [PPA Table 3.3, p. 156] (book p. 156; PDF p. 174) [PPA Example 3.7, p. 156] (book p. 156; PDF p. 174)
  [PPA Example 3.8, p. 157] (book p. 157; PDF p. 175):
  - Bodies inside `fn`, `fun`, and `close t in ρ` remain plain source `Exp`/`Term` (`G-U3a-09`); `[fn]` and
    `[fun]` restrict captured environments to `ρ₀ = ρ | FV(...)`, whereas `[let₂]` writes `ρ₀ = ρ | FV(e₂)`
    without subtracting `x`, and `[app_fun]` extends `ρ₂[x ↦ v₂]` where `ρ₂ = ρ₁[f ↦ close (fun f x => e₁) in ρ₁]`
    (`[x ↦ v₂]` rightmost, `G-U3a-11`).
  - `[bind₂]` (`(bind ρ₁ in v₁^{ℓ₁})^ℓ → v₁^ℓ`) and `[if₂]`/`[if₃]` (`(if true^{ℓ₀} then t₁^{ℓ₁} else e₂)^ℓ → t₁^ℓ`,
    `(if false^{ℓ₀} then e₁ else t₂^{ℓ₂})^ℓ → t₂^ℓ`) both **relabel** the selected subterm to outer `ℓ`
    (`p. 157`: outermost labels never change, `G-U3a-10`).
- **Intermediate acceptability (`Table 3.4`), `ℛ`/`𝒱`, and Subject Reduction (`Theorem 3.10`, `Fact 3.11`)**:
  - `Table 3.4` extends `⊨` coinductively to `IExp` with `[bind]` (`(Ĉ, ρ̂) ⊨ (bind ρ in it₀^{ℓ₀})^ℓ iff (Ĉ, ρ̂) ⊨ it₀^{ℓ₀} ∧ Ĉ(ℓ₀) ⊆ Ĉ(ℓ) ∧ ρ ℛ ρ̂`)
    and `[close]` (`(Ĉ, ρ̂) ⊨ (close t₀ in ρ)^ℓ iff {t₀} ⊆ Ĉ(ℓ) ∧ ρ ℛ ρ̂`) [PPA Table 3.4, p. 158] (book p. 158; PDF p. 176).
  - `ρ ℛ ρ̂ iff dom(ρ) ⊆ dom(ρ̂) ∧ ∀x ∈ dom(ρ) : ρ(x) 𝒱 (ρ̂, ρ̂(x))` and
    `v 𝒱 (ρ̂, v̂) iff ∀t ∀ρ : (v = close t in ρ) ⇒ (t ∈ v̂ ∧ ρ ℛ ρ̂)` (`Example 3.9`)
    [PPA §3.2.2, p. 158] (book p. 158; PDF p. 176) [PPA Example 3.9, p. 159] (book p. 159; PDF p. 177).
    `ℛ` is **well-founded** (finite non-cyclic closure trees, `G-U3a-09`), `dom(ρ) ⊆ dom(ρ̂)` is vacuous on
    total `Env̂` (`dom(ρ̂) = Var`) but active on `Env̂_⋆` (`G-U3a-13`), and constants satisfy `c 𝒱 (ρ̂, v̂)` even for `v̂ = ∅`.
  - **`Theorem 3.10` (`Figure 3.3`)**: `If ρ ℛ ρ̂ and ρ ⊢ ie → ie' then (Ĉ, ρ̂) ⊨ ie implies (Ĉ, ρ̂) ⊨ ie'`
    [PPA Figure 3.3, p. 159] (book p. 159; PDF p. 177) [PPA Theorem 3.10, p. 159] (book p. 159; PDF p. 177).
  - **`Fact 3.11` (`G-U3a-10`, `G-U3a-12`, `BKL-052`)**: `If (Ĉ, ρ̂) ⊨ it^{ℓ₁} and Ĉ(ℓ₁) ⊆ Ĉ(ℓ₂) then (Ĉ, ρ̂) ⊨ it^{ℓ₂}`
    (erased in OCR on `p. 160`!) [PPA Fact 3.11, p. 160] (book p. 160; PDF p. 178). Because `[bind₂]`, `[if₂]`, and
    `[if₃]` relabel inner values/branches to outer `ℓ` while keeping top labels invariant under congruence steps
    (`[app₁]`, `[if₁]`, `[let₁]`), `Fact 3.11` discharges all label-change steps directly (no `[app₁]` gap; contrast
    `Exercise 3.6`, where storing `Exp` with outer labels breaks `Fact 3.11`, `BKL-052`).
- **Moore family & least solution (`Proposition 3.13`, `Lemma 3.14`, `(3.1)`, `G-U3a-14`, `G-U3a-15`)**:
  Under pointwise subset order `⊑` on `Cachê × Env̂` (`⊤ = (λℓ.Term, λx.Term)`, `⊥ = (λℓ.∅, λx.∅)`; `p. 162` prose
  gives the `𝒫({1, 2, 3})` Moore-family illustration, while `Example 3.12` checks `Theorem 3.10` on `Example 3.7`
  showing `(Ĉ_e, ρ̂_e) ⊨ (close (fn y => y^3) in [])^5`
  [PPA Example 3.12, p. 162] (book p. 162; PDF p. 180)), `Lemma 3.14` proves `{ρ̂ | ρ ℛ ρ̂}` and
  `{(ρ̂, v̂) | v 𝒱 (ρ̂, v̂)}` are Moore families [PPA Lemma 3.14, p. 163] (book p. 163; PDF p. 181), and
  `Proposition 3.13` proves `∀ie ∈ IExp : {(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨ ie}` is a Moore family (hence always non-empty
  with a unique least acceptable analysis `⨅ {(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨ ie}`, `Example 3.15`; note `Example 3.15`
  reuses `(Ĉ'_e, ρ̂'_e)` with a new acceptable table, `G-U3a-15`, `BKL-053`)
  [PPA Proposition 3.13, p. 163] (book p. 163; PDF p. 181) [PPA Example 3.15, p. 164] (book p. 164; PDF p. 182).
  Key mechanism `(3.1)`: in `[app]`, `t ∈ Ĉ(ℓ₁)` sits contravariantly on the **left** of `⇒`, so intersecting
  `⋂_i Ĉ_i(ℓ₁)` shrinks triggers to terms that fired in *every* `(Ĉ_i, ρ̂_i)` (`G-U3a-14`)
  [PPA §3.2.3, p. 164] (book p. 164; PDF p. 182).

## 4. Syntax-Directed 0-CFA and Finite Subterm Restriction (Section 3.3, Table 3.5)

- **Safe specification refinement (`⊨_A ⇐ ⊨_B`, `G-U3a-17`)**: Enumerating guesses in `Proposition 3.13` is
  not polynomial. Reformulating `⊨` into `⊨_s` (`Table 3.5`) with `(Ĉ, ρ̂) ⊨ e_⋆ ⇐ (Ĉ, ρ̂) ⊨_s e_⋆` guarantees
  every solution of `⊨_s` inherits semantic soundness from `Theorem 3.10` **without** `⊨_s` satisfying subject
  reduction itself (`⊨_s` analyses unreachable bodies; `⊨ ⇒ ⊨_s` fails in general, `Exercise 3.11`)
  [PPA §3.3, p. 168] (book p. 168; PDF p. 186) [PPA §3.3, p. 169] (book p. 169; PDF p. 187).
- **`Table 3.5` (`(Ĉ, ρ̂) ⊨_s e`, `G-U3a-18`)**: Identical to `Table 3.1` on `Exp` except body checks move from
  `[app]` to `[fn]` and `[fun]` [PPA Table 3.5, p. 170] (book p. 170; PDF p. 188):
  - `[fn]`: `{fn x => e₀} ⊆ Ĉ(ℓ) ∧ (Ĉ, ρ̂) ⊨_s e₀`;
  - `[fun]`: `{fun f x => e₀} ⊆ Ĉ(ℓ) ∧ (Ĉ, ρ̂) ⊨_s e₀ ∧ {fun f x => e₀} ⊆ ρ̂(f)`;
  - `[app]`: `(Ĉ, ρ̂) ⊨_s t₁^{ℓ₁} ∧ (Ĉ, ρ̂) ⊨_s t₂^{ℓ₂}` plus `Ĉ(ℓ₂) ⊆ ρ̂(x) ∧ Ĉ(ℓ₀) ⊆ Ĉ(ℓ)` for each
    `fn x => t₀^{ℓ₀}` or `fun f x => t₀^{ℓ₀}` in `Ĉ(ℓ₁)` (each body analysed **once**, structurally inductive:
    `lfp(𝒬_s) = gfp(𝒬_s)`, `Example 3.17` displays `(3.2)-(3.3)` on `loop` without coinduction!)
    [PPA Example 3.17, p. 169] (book p. 169; PDF p. 187) [PPA Example 3.17, p. 170] (book p. 170; PDF p. 188).
- **Finite subterm restriction `(Ĉ_⋆^⊤, ρ̂_⋆^⊤)` & `Propositions 3.18-3.19` (`G-U3a-19`, `G-U3a-20`)**:
  For `e_⋆` with finite subterms `Term_⋆`, labels `Lab_⋆`, variables `Var_⋆`, set `Ĉ_⋆^⊤(ℓ) = Term_⋆` for
  `ℓ ∈ Lab_⋆` (`∅` outside) and `ρ̂_⋆^⊤(x) = Term_⋆` for `x ∈ Var_⋆` (`∅` outside), isomorphic to finite
  lattice `Cachê_⋆ × Env̂_⋆` over `Val̂_⋆ = 𝒫(Term_⋆)` [PPA §3.3.2, p. 171] (book p. 171; PDF p. 189).
  - **`Proposition 3.18` (`(3.4)-(3.5)`)**: `If (Ĉ, ρ̂) ⊨_s e_⋆ and (Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤) then (Ĉ, ρ̂) ⊨ e_⋆`
    [PPA Proposition 3.18, p. 172] (book p. 172; PDF p. 190). Precondition `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` is
    **mandatory** (`Exercise 3.10`, `G-U3a-19`): an alien `fn x => t₀^{ℓ₀} ∉ Term_⋆` inside `Ĉ(ℓ₁)` would never
    have `t₀^{ℓ₀}` checked by `⊨_s e_⋆`!
  - **`Proposition 3.19`**: `{(Ĉ, ρ̂) ∈ Cachê_⋆ × Env̂_⋆ | (Ĉ, ρ̂) ⊨_s e_⋆}` is a Moore family (proved by finite
    induction via `⊤` and binary `⊓`, without coinduction, `G-U3a-20`)
    [PPA Proposition 3.19, p. 172] (book p. 172; PDF p. 190) [PPA Proposition 3.19, p. 173] (book p. 173; PDF p. 191).

## 5. Foundational Exercises & Non-Blocking Backlog (Sections 3.1-3.3, Exercises 3.1-3.12)

- **Key exercises (`G-U3b-26`, `G-U3b-28`, `BKL-062`)**:
  - `Exercise 3.1` (labelling higher-order dispatch) & `Exercise 3.2` (restricting `Table 3.1` directly to
    `Cachê_⋆ × Env̂_⋆`)
    [PPA Exercise 3.1, p. 205] (book p. 205; PDF p. 223) [PPA Exercise 3.2, p. 206] (book p. 206; PDF p. 224);
  - `Exercise 3.3` (guarding `(Ĉ, ρ̂) ⊨ t₂^{ℓ₂}` in `[app]` by `Ĉ(ℓ₁) ≠ ∅` under CBV; `"cannot produced"` typo,
    `BKL-062`) & `Exercise 3.4`
    (declarative `(3.8)` is **not upward-closed** in `⊑` because adding a rogue closure to `Ĉ(ℓ₁)` activates
    new `[app]` obligations, unlike upward-closed `(3.9)`, `G-U3b-28`)
    [PPA Exercise 3.3, p. 206] (book p. 206; PDF p. 224) [PPA Exercise 3.4, p. 206] (book p. 206; PDF p. 224);
  - `Exercise 3.5` (coarse `Ĉ(ℓ₁) ⊆ ρ̂(f)` pollutes `ρ̂(f)` with sibling lambdas) & `Exercise 3.6` (`Val̂ = 𝒫(Exp)`
    breaks `Fact 3.11` and `Theorem 3.10` because `[bind₂]`/`[if₂,₃]` relabel `v^{ℓ₁} → v^ℓ`, `G-U3b-26`, `BKL-052`)
    [PPA Exercise 3.5, p. 206] (book p. 206; PDF p. 224) [PPA Exercise 3.6, p. 206] (book p. 206; PDF p. 224);
  - `Exercise 3.7` (remaining `Theorem 3.10` cases + static-scoping `0-CFA`, `"semantics allow"`, `BKL-062`), `Exercise 3.8` (`Table 3.1`
    remains sound under call-by-name/lazy SOS), and `Exercises 3.9-3.12` (uniqueness of `𝒬_s`, necessity of
    `(Ĉ_⋆^⊤, ρ̂_⋆^⊤)`, counterexamples to `⊨ ⇒ ⊨_s`, direct subject reduction for `⊨_s`)
    [PPA Exercise 3.7, p. 207] (book p. 207; PDF p. 225) [PPA Exercise 3.8, p. 207] (book p. 207; PDF p. 225)
    [PPA Exercise 3.9, p. 207] (book p. 207; PDF p. 225) [PPA Exercise 3.10, p. 207] (book p. 207; PDF p. 225)
    [PPA Exercise 3.11, p. 208] (book p. 208; PDF p. 226) [PPA Exercise 3.12, p. 208] (book p. 208; PDF p. 226).
- **Non-blocking backlog (`ARCHITECTURE.md` §6.4)**: `BKL-011` (`Tables 3.2-3.3` & `Fact 3.11` OCR erasure);
  `BKL-051` (`§3.1` multi-let sugar, `Table 3.1`/`3.2` typos, `[let₂]` `FV(e₂)`, & `[app_fun]` `[x ↦ v₂]` order);
  `BKL-052` (`Fact 3.11` OCR erasure on `p. 160`, `[if₂,₃]`/`[bind₂]` outer-label relabelling invariant, &
  `Exercise 3.6` `Val̂ = 𝒫(Exp)` failure); `BKL-053` (`Example 3.15` `(Ĉ'_e, ρ̂'_e)` reuse & `Proposition 3.16` `IExp_e`);
  `BKL-059` (`0-CFA` shadowed-variable dynamic scoping); `BKL-062` (`Exercises 3.3–3.7, 3.16–3.17` subtleties & non-upward-closure).
