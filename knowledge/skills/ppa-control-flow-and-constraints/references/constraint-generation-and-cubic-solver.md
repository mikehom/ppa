<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Self-contained L1 comparative reference for Chapter 3 section 3.4, Mini Projects 3.1 and 3.3, Exercise 3.13, and Concluding Remarks set-constraint / lazy-solver theory. -->

# Constraint-Based 0-CFA, Cubic Graph Solver, and Open Systems (Section 3.4)

Self-contained `L1` formal reference for Section 3.4
([PPA §3.4, p. 173] (book p. 173; PDF p. 191) to [PPA Corollary 3.25, p. 182] (book p. 182; PDF p. 200)),
`Exercise 3.13` ([PPA Exercise 3.13, p. 208] (book p. 208; PDF p. 226)), `Mini Projects 3.1` and `3.3`
([PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220) to [PPA Mini Project 3.3, p. 204] (book p. 204; PDF p. 222)),
and Set-Constraint / Lazy-Solving remarks ([PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219)
to [PPA Chapter 3 Concluding Remarks, p. 202] (book p. 202; PDF p. 220)). Equational vs inclusion constraint
foundations live in [chapter-1-five-formulations.md](../../ppa-program-analysis/references/chapter-1-five-formulations.md),
graph preliminaries in [appendix-c-graphs-dfsf-and-rpo.md](../../ppa-program-analysis/references/appendix-c-graphs-dfsf-and-rpo.md),
and the Chapter 5 type-based `U8` counterparts (`⊢_CFA`, `𝒲_CFA`, `§5.4.1` shape-conformant subtyping, `(5.2)` `ρ̃, C̃`) in
[annotated-types-and-cfa-soundness.md](../../ppa-types-effects-and-regions/references/annotated-types-and-cfa-soundness.md) and
[inference-unification-and-subtyping.md](../../ppa-types-effects-and-regions/references/inference-unification-and-subtyping.md).

## 1. Syntactic Inclusion Constraints and Equivalence (Sections 3.4-3.4.1, Table 3.6)

- **Syntactic constraint grammar (`(3.6)-(3.7)`, `G-U3a-21`, `G-U3a-22`)**: For a closed or open program of
  interest `e_⋆` of syntactic size `n` (`|Lab_⋆|, |Var_⋆|, |Term_⋆| ≤ n`), `𝒞_⋆⟦e_⋆⟧` emits unconditional
  inclusions `(3.6)` and singleton-guarded conditional inclusions `(3.7)`
  [PPA §3.4, p. 173] (book p. 173; PDF p. 191) [PPA §3.4, p. 174] (book p. 174; PDF p. 192):
  ```text
  lhs ⊆ rhs                         (3.6)
  {t} ⊆ rhs' ⇒ lhs ⊆ rhs            (3.7)
  ```
  - **Syntax vs semantics (`G-U3a-21`)**: Sans-serif `C(ℓ)` and `r(x)` are pure *syntactic* constraint
    variables (`rhs, rhs' ∈ {C(ℓ), r(x)}`, `lhs ∈ {C(ℓ), r(x), {t}}` with `t ∈ Term_⋆` an `fn` or `fun`
    abstraction), distinct from semantic sets `Ĉ(ℓ)` and `ρ̂(x)`. Parsing `(3.7)` as `({t} ⊆ rhs' ⇒ lhs) ⊆ rhs`
    gives every constraint the uniform shape `ls ⊆ rhs`.
  - **Exact constraint count (`G-U3a-22`)**: Although `O(n²)` forms of `(3.6)` and `O(n⁴)` forms of `(3.7)`
    exist syntactically, `Table 3.6` emits **`O(n)` unconditional constraints `(3.6)` and `O(n²)` conditional
    constraints `(3.7)`** (`2` conditional constraints per abstraction `t ∈ Term_⋆` at each `[app]` site)
    [PPA §3.4, p. 175] (book p. 175; PDF p. 193).
- **Constraint generator `𝒞_⋆⟦e⟧` (`Table 3.6`, `Example 3.20`)**
  [PPA Table 3.6, p. 174] (book p. 174; PDF p. 192):
  ```text
  [con]  𝒞_⋆⟦c^ℓ⟧ = ∅
  [var]  𝒞_⋆⟦x^ℓ⟧ = {r(x) ⊆ C(ℓ)}
  [fn]   𝒞_⋆⟦(fn x => e₀)^ℓ⟧ = {{fn x => e₀} ⊆ C(ℓ)} ∪ 𝒞_⋆⟦e₀⟧
  [fun]  𝒞_⋆⟦(fun f x => e₀)^ℓ⟧ = {{fun f x => e₀} ⊆ C(ℓ)} ∪ 𝒞_⋆⟦e₀⟧ ∪ {{fun f x => e₀} ⊆ r(f)}
  [app]  𝒞_⋆⟦(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ⟧ = 𝒞_⋆⟦t₁^{ℓ₁}⟧ ∪ 𝒞_⋆⟦t₂^{ℓ₂}⟧
             ∪ {{t} ⊆ C(ℓ₁) ⇒ C(ℓ₂) ⊆ r(x) | t = (fn x => t₀^{ℓ₀}) ∈ Term_⋆}
             ∪ {{t} ⊆ C(ℓ₁) ⇒ C(ℓ₀) ⊆ C(ℓ) | t = (fn x => t₀^{ℓ₀}) ∈ Term_⋆}
             ∪ {{t} ⊆ C(ℓ₁) ⇒ C(ℓ₂) ⊆ r(x) | t = (fun f x => t₀^{ℓ₀}) ∈ Term_⋆}
             ∪ {{t} ⊆ C(ℓ₁) ⇒ C(ℓ₀) ⊆ C(ℓ) | t = (fun f x => t₀^{ℓ₀}) ∈ Term_⋆}
  [if]   𝒞_⋆⟦(if t₀^{ℓ₀} then t₁^{ℓ₁} else t₂^{ℓ₂})^ℓ⟧ =
             𝒞_⋆⟦t₀^{ℓ₀}⟧ ∪ 𝒞_⋆⟦t₁^{ℓ₁}⟧ ∪ 𝒞_⋆⟦t₂^{ℓ₂}⟧ ∪ {C(ℓ₁) ⊆ C(ℓ)} ∪ {C(ℓ₂) ⊆ C(ℓ)}
  [let]  𝒞_⋆⟦(let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ⟧ = 𝒞_⋆⟦t₁^{ℓ₁}⟧ ∪ 𝒞_⋆⟦t₂^{ℓ₂}⟧ ∪ {C(ℓ₁) ⊆ r(x)} ∪ {C(ℓ₂) ⊆ C(ℓ)}
  [op]   𝒞_⋆⟦(t₁^{ℓ₁} op t₂^{ℓ₂})^ℓ⟧ = 𝒞_⋆⟦t₁^{ℓ₁}⟧ ∪ 𝒞_⋆⟦t₂^{ℓ₂}⟧
  ```
  On `Example 3.20` (`((fn x => x^1)^2 (fn y => y^3)^4)^5`), `Term_⋆` has 2 abstractions (`id_x = fn x => x^1`,
  `id_y = fn y => y^3`), yielding `8` constraints (`4` unconditional + `4` conditional)
  [PPA Example 3.20, p. 175] (book p. 175; PDF p. 193).
- **Valuation `(Ĉ, ρ̂)⟦·⟧`, satisfaction `⊨_c`, and `Proposition 3.21` (`G-U3a-19`)**:
  `(Ĉ, ρ̂)⟦C(ℓ)⟧ = Ĉ(ℓ)`, `(Ĉ, ρ̂)⟦r(x)⟧ = ρ̂(x)`, `(Ĉ, ρ̂)⟦{t}⟧ = {t}`, and
  `(Ĉ, ρ̂)⟦{t} ⊆ rhs' ⇒ lhs⟧ = (Ĉ, ρ̂)⟦lhs⟧` if `{t} ⊆ (Ĉ, ρ̂)⟦rhs'⟧` (`∅` otherwise);
  `(Ĉ, ρ̂) ⊨_c C iff ∀(ls ⊆ rhs) ∈ C : (Ĉ, ρ̂)⟦ls⟧ ⊆ (Ĉ, ρ̂)⟦rhs⟧`
  [PPA §3.4.1, p. 175] (book p. 175; PDF p. 193) [PPA §3.4.1, p. 176] (book p. 176; PDF p. 194).
  - **`Proposition 3.21`**: `If (Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤) then (Ĉ, ρ̂) ⊨_s e_⋆ iff (Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧`
    (so their least solutions in `Cachê_⋆ × Env̂_⋆` coincide; `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` ensures `Ĉ(ℓ₁) ⊆ Term_⋆`)
    [PPA Proposition 3.21, p. 176] (book p. 176; PDF p. 194).
  - **Equational vs inclusion formulation (`Exercise 3.13`, `Unification U1`)**: Grouping `ls ⊆ rhs` per `rhs`
    into equations `rhs = ⋃ ls_i` (`𝒞_⋆^=⟦e_⋆⟧`) yields strictly fewer non-minimal solutions (`Fix(F_⋆) ⊆ Red(F_⋆)`)
    but the **exact same least solution** `lfp(F_⋆)` [PPA Exercise 3.13, p. 208] (book p. 208; PDF p. 226).

## 2. Fixed-Point Operator F_* and Naive O(n^5) Bound (Section 3.4.2, Proposition 3.22)

- **Monotone operator `F_⋆` (`G-U3a-21`, `G-U3a-23`, `BKL-054`)**: On finite complete lattice `Cachê_⋆ × Env̂_⋆`,
  define `F_⋆(Ĉ, ρ̂) = (F₁(Ĉ, ρ̂), F₂(Ĉ, ρ̂))` by `F₁(Ĉ, ρ̂)(ℓ) = ⋃ {(Ĉ, ρ̂)⟦ls⟧ | (ls ⊆ C(ℓ)) ∈ 𝒞_⋆⟦e_⋆⟧}` and
  `F₂(Ĉ, ρ̂)(x) = ⋃ {(Ĉ, ρ̂)⟦ls⟧ | (ls ⊆ r(x)) ∈ 𝒞_⋆⟦e_⋆⟧}`
  [PPA §3.4.2, p. 176] (book p. 176; PDF p. 194) [PPA §3.4.2, p. 177] (book p. 177; PDF p. 195).
  Because every guard `{t} ⊆ rhs'` has a *constant* singleton left-hand side `{t}`, `F_⋆` is monotone (`G-U3a-21`).
  - **`Proposition 3.22`**: `lfp(F_⋆) = ⨅ {(Ĉ, ρ̂) | (Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧}` (since reductive elements `Red(F_⋆)`,
    i.e. `F_⋆(Ĉ, ρ̂) ⊑ (Ĉ, ρ̂)`, are exactly solutions `(Ĉ, ρ̂) ⊨_c 𝒞_⋆⟦e_⋆⟧`)
    [PPA Proposition 3.22, p. 177] (book p. 177; PDF p. 195) [PPA Proposition A.10, p. 402] (book p. 402; PDF p. 418).
  - **Naive ascending-chain bound (`O(n⁵)`) & printed errata (`G-U3a-23`, `BKL-054`)**: `Val̂_⋆` has height `O(n)` across
    `O(n)` nodes in `Cachê_⋆ × Env̂_⋆` (misprinted `Cachê_⋆ × Val̂_⋆` on `p. 177`, and `p. 176` cites
    `Proposition 3.18` instead of `Proposition 3.19` for least-solution existence), giving lattice height `O(n²)`
    and `O(n²)` iterations × `O(n)` components × `O(n²)` constraint evaluations = **`O(n⁵)`** naive work.

## 3. Dual-Observer Worklist Graph Solver and O(n^3) Complexity (Section 3.4.2, Table 3.7, Figures 3.4-3.5)

- **Constraint graph representation (`Nodes`, `W`, `D[q]`, `E[q]`, `G-U3a-24`)**: Over
  `Nodes = {C(ℓ) | ℓ ∈ Lab_⋆} ∪ {r(x) | x ∈ Var_⋆}` (`|Nodes| = O(n)`), `Table 3.7` maintains worklist `W`,
  monotone node value sets `D[q] ∈ Val̂_⋆`, and subscriber edge lists `E[q]`
  [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196):
  - Step 1 initialises `W := nil`, `D[q] := ∅`, `E[q] := nil`.
  - Step 2 scans `cc ∈ 𝒞_⋆⟦e_⋆⟧`: `{t} ⊆ p` calls `add(p, {t})`; `p₁ ⊆ p₂` prepends `cc` to `E[p₁]`;
    conditional `{t} ⊆ p ⇒ p₁ ⊆ p₂` prepends `cc` to **both** `E[p₁]` **and** `E[p]` (`G-U3a-24`!).
  - Step 3 pops `q := head(W)` while `W ≠ nil` and traverses `cc ∈ E[q]`: for `p₁ ⊆ p₂` calls `add(p₂, D[p₁])`;
    for `{t} ⊆ p ⇒ p₁ ⊆ p₂`, `if t ∈ D[p] then add(p₂, D[p₁])` (where `add(q, d)` updates `D[q] := D[q] ∪ d`
    and pushes `W := cons(q, W)` iff `¬(d ⊆ D[q])`). Step 4 copies `D[C(ℓ)]` and `D[r(x)]` to `(Ĉ, ρ̂)`.
  - **Why dual registration (`E[p₁]` and `E[p]`) is mandatory (`G-U3a-24`, `Figures 3.4-3.5`, `Example 3.23`)**:
    In `Example 3.23` (`Figure 3.4` initialisation, `Figure 3.5` 6-step trace), `W = [C(4), C(2)]` pops `C(4)`
    *before* `C(2)` while `id_x ∈ D[C(2)]` already holds; if `{t} ⊆ p ⇒ p₁ ⊆ p₂` were registered only in `E[p₁]`,
    any call where `D[p₁]` populated *before* `t` arrived in `D[p]` would silently drop the call's argument/return
    edges forever [PPA Figure 3.4, p. 179] (book p. 179; PDF p. 197) [PPA Example 3.23, p. 179] (book p. 179; PDF p. 197)
    [PPA Figure 3.5, p. 180] (book p. 180; PDF p. 198).
- **Correctness (`Proposition 3.24`) and `O(n³)` vs `O(n⁴)` complexity (`G-U3a-25`, `BKL-011`, `BKL-055`)**:
  - **`Proposition 3.24`**: `Table 3.7` terminates and outputs `(Ĉ, ρ̂) = ⨅ {(Ĉ', ρ̂') | (Ĉ', ρ̂') ⊨_c 𝒞_⋆⟦e_⋆⟧}`
    (displayed `⨅` equation erased in OCR on `p. 180`, `BKL-011`) [PPA Proposition 3.24, p. 180] (book p. 180; PDF p. 198).
  - **Book's `O(n³)` step bound (`p. 181`, `Unification U3`)**: Step 1 is `O(n)`, Step 2 is `O(n²)`, Step 4 is
    `O(n)`. In Step 3, each `D[q]` grows at most `|Term_⋆| ≤ n` times (`≤ n` pops per node), and
    `∑_q |E[q]| ≤ 2 · |𝒞_⋆⟦e_⋆⟧| = O(n²)`, bounding inner `case` executions by **`O(n³)` edge-traversal steps**
    (generalised by Chapter 6's abstract worklist solver, `U3`) [PPA §3.4.2, p. 181] (book p. 181; PDF p. 199).
  - **Elementary-operation pitfall (`G-U3a-25`, `BKL-055`)**: Treating whole-set `¬(D[p₁] ⊆ D[p₂])` and
    `D[p₂] ∪ D[p₁]` as `O(1)` hides an `O(n)` set-scan factor (`O(n⁴)` scalar operations, or `O(n⁴ / w)` with
    `w`-bit words) [external]. Pushing differential `(q, t)` pairs (`O(n²)` pairs popped once each × `O(n)`
    per-site constraints with `O(1)` bitset test `t ∈ D[p₂]`) achieves true `O(n³)` elementary operations [external].

## 4. End-to-End Soundness, Open Systems, Reachability, and Set Constraints (Corollary 3.25, Mini Projects 3.1 & 3.3)

- **`Corollary 3.25` (`G-U3a-26`, `BKL-055`)**: Extending `Table 3.7`'s output with `∅` outside `Lab_⋆, Var_⋆`
  satisfies `(Ĉ, ρ̂) ⊨ e_⋆` (`Prop 3.24 → Prop 3.21 → Prop 3.18 → Theorem 3.10`), **without** claiming `(Ĉ, ρ̂)`
  is the *least* solution of `⊨ e_⋆` when dead closures exist (`Exercise 3.11`; `p. 181-182` print `𝒞⟦e_⋆⟧` for
  `𝒞_⋆⟦e_⋆⟧`, `BKL-054`) [PPA Corollary 3.25, p. 182] (book p. 182; PDF p. 200).
- **Open systems (`p. 182`, `p. 200`, `BKL-008`, `G-U3a-26`)**: If an open program `e_∘` has its hole filled by
  stub `e_⋆` and `(Ĉ, ρ̂) ⊨ e_⋆` also satisfies all acceptability clauses of a replacement library/host fragment
  in `e'_⋆` (with no label or bound/free variable capture clashes), then `(Ĉ, ρ̂) ⊨ e'_⋆` holds without
  re-analysing `e_∘` [PPA §3.4.2, p. 182] (book p. 182; PDF p. 200)
  [PPA Chapter 3 Concluding Remarks, p. 200] (book p. 200; PDF p. 218). In security/CFI [external] reviews,
  any reflection, FFI callback, or deserialization gadget [external] outside the stubbed clauses breaks closed-world safety (`BKL-008`).
- **Reachability-gated `0-CFA` (`Mini Project 3.1`, `Mini Project 3.3`, `G-U3b-25`, `BKL-060`)**:
  Adding `R̂ ∈ Reach = Lab → 𝒫({on})` with `(Ĉ, ρ̂, R̂) ⊨'_s e` (seeding `{on} ⊆ R̂(ℓ_⋆)`, gating `[fn]`/`[fun]`/`[con]`
  by `on ∈ R̂(ℓ)`, propagating `R̂(ℓ) ⊆ R̂(ℓ_i)`, and `({t} ⊆ Ĉ(ℓ₁) ∧ {on} ⊆ R̂(ℓ)) ⇒ R̂(ℓ) ⊆ R̂(ℓ₀)`; note line 10
  in the project text misprints `⊨_s` for `⊨'_s`, `BKL-060`) avoids analysing dead lambdas in syntax-directed/constraint
  form (though `⊨ e_⋆` remains slightly tighter when `R̂(ℓ) = {on}` holds at an `[app]` with `Ĉ(ℓ₁) = ∅`, `G-U3b-25`)
  [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220).
  `Mini Project 3.3` gives the SML AST (`datatype exp = Label of term * label`) for prototyping `𝒞_⋆` and `Table 3.7`
  [PPA Mini Project 3.3, p. 204] (book p. 204; PDF p. 222).
- **Set Constraints & `[9]` (`[external: Aiken et al.]`) lazy two-step solver (`Concluding Remarks`, `G-U3b-23`, `G-U3b-24`, `BKL-059`)**:
  Set-Constraint Based Analysis (`S₁ ⊆ S₂` over union `∪`, intersection `∩`, constructor expressions `C(S₁, ..., S_a)`,
  and projections `C^{-i}(S)`, `p. 201`) stays monotone (`S₁ ∩ S₂` is monotone!) until complement `¬S` or
  variable-LHS conditional guards `(S₁ ⊆ S₂) ⇒ S₃` break monotonicity (`G-U3b-23`, requiring Banach's
  Contraction Theorem instead of Tarski's Theorem)
  [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219). `[9]`'s (`[external: Aiken et al.]`) two-step solver
  expands conditional constraints `{t} ⊆ p ⇒ ...` *on the fly* only when `t` actually arrives in `D[p]`, avoiding
  upfront `O(n²)` instantiation over unreachable `Term_⋆` (`G-U3b-24`)
  [PPA Chapter 3 Concluding Remarks, p. 202] (book p. 202; PDF p. 220).

## 5. Non-Blocking Constraint & Solver Backlog (Section 3.4)

- `BKL-008` (closed-world syntax vs reflection/FFI/deserialization `[external]`; open-system stub boundary `p. 182`);
- `BKL-011` (`Proposition 3.24` displayed `⨅` equation and `Mini Project 3.1` OCR erasures, `G-U3b-30`);
- `BKL-054` (`§3.4.2` `Prop 3.18` vs `3.19` and `Cachê_⋆ × Val̂_⋆` vs `Env̂_⋆` errata, `F-U3a-09..14`);
- `BKL-055` (`Table 3.7` `O(n³)` vs `O(n⁴)` scalar union gap, dual `E[p₁]`/`E[p]` registration, dead-body over-approx);
- `BKL-059` (set-constraint `¬S`/variable-LHS guard non-monotonicity and `[9]` `[external: Aiken et al.]` lazy expansion vs `Table 3.6`);
- `BKL-060` (`Mini Project 3.1` `p. 202` `⊨_s` prose typo for `⊨'_s`, and `Mini Project 3.2` `p. 203` `Fact 3.11`/label finiteness).
