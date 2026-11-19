<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 4b (Chapter 4 §§4.4-4.5, Concluding Remarks, Mini Projects 4.1-4.3, Figure 4.10, and Exercises 4.1-4.24). -->

# RAW_SHARD_04b — Chapter 4 Systematic Design of Galois Connections, Induced Operations, and End Matter (Unit 4b)

Source: *Principles of Program Analysis* (Nielson, Nielson, Hankin), corrected 2nd printing, 2005.
Scope: Upper-half boundary carryover of §4.3.2 on book p. 246 (`Fact 4.31` conclusion and proof, `Proposition 4.29`
proof, `ς_η` extraction reduction, Galois connection isomorphism, and `Example 4.32`), §4.4 *Systematic Design of
Galois Connections* (§4.4.1 *Component-wise Combinations*, §4.4.2 *Other Combinations*), §4.5 *Induced Operations*
(§4.5.1 *Inducing along the Abstraction Function*, §4.5.2 *Application to Data Flow Analysis*, §4.5.3 *Inducing along
the Concretisation Function*), Chapter 4 *Concluding Remarks*, *Mini Projects* `4.1`–`4.3`, `Figure 4.10` (`Sign'`),
and *Exercises* `4.1`–`4.24`, spanning book pages 246–282 / PDF pages 263–299. Chapter 4 opening, §4.1 (*A Mundane
Approach to Correctness*), §4.2 (*Approximation of Fixed Points*), and §4.3 (*Galois Connections* through `Example 4.32`
atop book p. 246) belong to Unit 4a (`RAW_SHARD_04a_galois_widening.md`).

Coordinates: `PDF page = book page + 17` uniformly across all 37 pages of Unit 4b (spanning book pages 246–282 /
PDF pages 263–299; blank verso p. 210 after Chapter 3 is absent from the PDF, whereas p. 282 is printed —
Chapter 4 ends on book p. 282 / PDF p. 299 and Chapter 5 opens on book p. 283 / PDF p. 300 with the same `+17`
offset). Section starts in Unit 4b: §4.3.2 tail atop p. 246, §4.4 near bottom of p. 246 (§4.4.1 on p. 249, §4.4.2 near
bottom of p. 253), §4.5 on p. 258 (§4.5.1 near bottom of p. 258, §4.5.2 on p. 262, §4.5.3 on p. 267), Concluding Remarks on p. 270, Mini
Projects on p. 274, Figure 4.10 and Exercises on p. 276, concluding with Exercise 4.24 on p. 282
[PPA §4.4, p. 246] (book p. 246; PDF p. 263); [PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299).

Conventions:

- Every source reference pairs a strict inline locator token with its book/PDF coordinate companion, for example
  [PPA §4.4, p. 246] (book p. 246; PDF p. 263), [PPA Figure 4.10, p. 276] (book p. 276; PDF p. 293), or
  [PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299).
- Book-numbered items preserve their exact printed kind word and number: statements `4.33`–`4.45` (`8` Examples
  `4.33`–`4.40`, `4` Lemmas `4.41`–`4.43` and `4.45`, `1` Proposition `4.44`, plus boundary carryover of `Fact 4.31`,
  `Proposition 4.29` proof, and `Example 4.32` on p. 246; `0` numbered Definitions, Theorems, or Corollaries),
  `0` Tables, `1` Figure (`Figure 4.10`), `5` numbered displays `(4.11)`–`(4.15)`, `3` Mini Projects (`4.1`–`4.3`),
  and `24` Exercises (`4.1`–`4.24`, `0` starred). Unnumbered combinators, definitions, derivations, and the printed
  `Summary.` (p. 258) and `Remark.` (p. 266) paragraphs carry local identifiers `[U4b:<section>-<letter>]`.
- Every formula, commuting diagram, lattice Hasse diagram, and proof step is transcribed directly from rendered
  150-dpi page images (`PDF pp. 263–299`) rather than the embedded PDF OCR text layer, which drops entire displayed
  equations in `§4.4`, `Lemma 4.41`, `§4.5.2`, `§4.5.3`, `Lemma 4.45`, `Exercise 4.11`, and `Exercise 4.24` while
  corrupting `ς`, `⊗`, `∇`, `Δ`, `ȷ`, `Ξ`, `ϒ`, and vector arrows.
- Terms absent from the book carry `[external]`. Mathematical consequences, explicit witnesses, counterexamples, and
  worked resolutions of Mini Projects and Exercises carry `[derived]`. Source misprints and internal tensions are
  transcribed as printed and logged under `Findings` (`F-U4b-NN`).
- Notation: `(L, α, γ, M)` Galois connection (`α` lower/left adjoint, `γ` upper/right adjoint) and Galois insertion
  when `α ∘ γ = λm.m`; `η : V → D` extraction function generating `(𝒫(V), α_η, γ_η, 𝒫(D))`; `ς : M → M` reduction
  operator `ς(m) = ⨅{m' | γ(m) = γ(m')} = α(γ(m))`; `θ_L, θ_M` lattice isomorphisms; `Sign = {-, 0, +}`;
  `Parity = {odd, even}`; `Range = {<-1, -1, 0, +1, >+1}`; `AB ⊆ Sign × Sign × Range` 29-atom Array Bound set;
  `⊗` tensor product; `S → L` total function space; `L_1 → L_2` monotone function space; `β : V → L` representation
  function; `(β_1 ↠ β_2)(↝)` induced monotone transformer; `R_1 ↠ R_2` lifted correctness relation; `⊕` abstract sign
  addition; `A = (L, F, E, ι, f_.)` and `B = (M, F, E, ȷ, g_.)` generalised Monotone Frameworks with constraints
  `A^⊒`, `B^⊒` and associated monotone operators `\vec{f}, \vec{g}`; `SS` sets-of-states analysis; `CP` Constant
  Propagation over `Statê_CP = ((Var → Z^⊤)_⊥, ⊑)`; `∇_L, ∇_M` widening operators; `Δ_L, Δ_M` narrowing operators;
  `ϒ` descending chain truncator; `ρ : L → L` upper closure operator with fixed points `ρ[L] = Fix(ρ)`; `⊑^d` dual
  partial order; `Ξ` program transformation with enabling condition `l_ℓ ⊑ l_Ξ`; `LR ⊆ 𝒫({H, S}) × Range` list-pair
  atoms; `SG` shape graphs; `⊨_{SV}` sets-of-values CFA acceptability; `Sign'` 7-element lattice (`Figure 4.10`).

## Closed-World Inventory (book p. 246; PDF p. 263) (book p. 282; PDF p. 299)

| Kind | Count | Identifiers |
| :--- | ---: | :--- |
| Boundary carryover & Sections | 3 | `§4.3.2` conclusion (`p. 246` top), `§4.4` (`pp. 246–258`), `§4.5` (`pp. 258–270`) |
| Numbered subsections | 5 | `§4.4.1` (`pp. 249–253`), `§4.4.2` (`pp. 253–258`), `§4.5.1` (`pp. 258–262`), `§4.5.2` (`pp. 262–267`), `§4.5.3` (`pp. 267–270`) |
| End-matter divisions | 3 | `Concluding Remarks` (`pp. 270–273`), `Mini Projects` (`pp. 274–275`), `Exercises` (`pp. 276–282`) |
| Tables | 0 | None in Chapter 4 |
| Figures | 1 | `Figure 4.10` (`Sign'`, `p. 276`) |
| Numbered displays | 5 | `(4.11)` (`p. 264`), `(4.12)` (`p. 264`), `(4.13)` (`p. 268`), `(4.14)` (`p. 269`), `(4.15)` (`p. 269`) |
| Examples | 8 (+1 carryover) | `4.33` (`pp. 247–248`), `4.34` (`p. 250`), `4.35` (`pp. 251–252`), `4.36` (`p. 253`), `4.37` (`p. 254`), `4.38` (`pp. 255–256`), `4.39` (`pp. 257–258`), `4.40` (`p. 259`), plus carryover `4.32` (`p. 246`) |
| Lemmas | 4 | `4.41` (`p. 260`), `4.42` (`pp. 261–262`), `4.43` (`pp. 265–266`), `4.45` (`pp. 269–270`) |
| Propositions | 1 (+1 proof carryover) | `4.44` (`p. 268`), plus proof of `4.29` (`p. 246`) |
| Mini Projects | 3 | `Mini Project 4.1` (`p. 274`), `Mini Project 4.2` (`pp. 274–275`), `Mini Project 4.3` (`p. 275`) |
| Exercises | 24 | `Exercise 4.1`–`Exercise 4.24` (`pp. 276–282`; `0` starred) |

## Boundary Carryover on Book Page 246 (§4.3.2 Tail)

Context: Book page 246 (`PDF p. 263`) is shared between the closing paragraphs of `§4.3.2` (*Galois Insertions*,
formally catalogued in Unit 4a through `Example 4.32`) and the opening of `§4.4` (*Systematic Design of Galois
Connections*). The `§4.3.2` results on `p. 246` are recorded here in compact reference form because `§4.4.2`,
`Concluding Remarks`, `Mini Project 4.1`, and `Exercise 4.14` invoke them directly
[PPA §4.3.2, p. 246] (book p. 246; PDF p. 263).

### [U4b:4.3.2-a] Boundary coordinate note: `Fact 4.31`, `Proposition 4.29` proof, `ς_η`, isomorphism, and `Example 4.32`
- Statement: On the upper 75% of book p. 246 (`PDF p. 263`), immediately above the `4.4 Systematic Design of Galois Connections` heading:
  1. **Conclusion and proof of `Fact 4.31`** (opening on p. 245): for `(L, α, γ, M)` and reduction operator
     `ς(m) = ⨅{m' | γ(m) = γ(m')}`,
     ```text
     ς(m) = α(γ(m))        and hence        α[L] = ς[M].
     ```
     *Proof*: `γ(m) = γ(α(γ(m)))` (`Fact 4.24`) yields `ς(m) ⊑ α(γ(m))`; conversely `α(γ(m)) ⊑ ς(m) ⇔ γ(m) ⊑ γ(ς(m))`
     (`Proposition 4.20`), and `γ(ς(m)) = ⨅{γ(m') | γ(m') = γ(m)} = γ(m)` by complete multiplicativity of `γ`
     (`Lemma 4.22`). For `l ∈ L`, `α(l) = α(γ(α(l))) = ς(α(l))` gives `α[L] ⊆ ς[M]`, while `ς(m) = α(γ(m))` gives
     `ς[M] ⊆ α[L]` [PPA Fact 4.31, p. 246] (book p. 246; PDF p. 263).
  2. **Proof of `Proposition 4.29`**: `Facts 4.30` and `4.31` establish that `ς[M] = α[L]` is a complete lattice
     (where `Fact 4.30` on p. 245 proves joins in `α[L]` coincide with joins in `M`, `⨆_{ς[M]} M' = ⨆_M M'`, whereas
     meets in `ς[M]` are `⨅_{ς[M]} M' = ς(⨅_M M') = α(⨅_L γ[M'])` `[derived]`). Restricting the adjunction
     `(L, α, γ, M)` (`Proposition 4.20`) to `α[L]` makes `α` surjective onto `α[L]`, yielding a Galois insertion by
     `Lemma 4.27` [PPA §4.3.2, p. 246] (book p. 246; PDF p. 263).
  3. **Reduction operators defined by extraction functions & Galois connection isomorphism**: For
     `(𝒫(V), α_η, γ_η, 𝒫(D))` generated by `η : V → D`, the reduction operator `ς_η : 𝒫(D) → 𝒫(D)` is
     ```text
     ς_η(D') = D' ∩ η[V]        where        η[V] = {η(v) | v ∈ V},
     ```
     making `ς_η[𝒫(D)]` isomorphic (in fact equal as a set family `[derived]`) to `𝒫(η[V])` (`Exercise 4.14`).
     Formally, `(L_1, α_1, γ_1, M_1)` is *isomorphic* to `(L_2, α_2, γ_2, M_2)` iff there exist complete-lattice
     isomorphisms `θ_L : L_1 → L_2` and `θ_M : M_1 → M_2` (`Appendix A`) such that
     ```text
     α_2 = θ_M ∘ α_1 ∘ θ_L^{-1}        and        γ_2 = θ_L ∘ γ_1 ∘ θ_M^{-1}.
     ```
  4. **`Example 4.32`**: Returning to `Example 4.28` (`signparity : Z → Sign × Parity`),
     `signparity[Z] = {(-, odd), (-, even), (0, even), (+, odd), (+, even)}` eliminates uninhabited `(0, odd)`,
     producing the Galois insertion `(𝒫(Z), α_{signparity}, γ_{signparity}, 𝒫(signparity[Z]))`
     [PPA Example 4.32, p. 246] (book p. 246; PDF p. 263).
- Citation: [PPA Fact 4.31, p. 246] (book p. 246; PDF p. 263); [PPA §4.3.2, p. 246] (book p. 246; PDF p. 263);
  [PPA Example 4.32, p. 246] (book p. 246; PDF p. 263)

## 4.4 Systematic Design of Galois Connections

Context: Section 4.4 develops a compositional combinator calculus for building complex Galois connections and Galois
insertions out of elementary verified building blocks: sequential composition (`§4.4` opening), component-wise product
and function-space liftings (`§4.4.1`), and same-carrier direct, tensor, and `ς`-reduced products culminating in the
29-atom Array Bound lattice `AB` (`§4.4.2`) [PPA §4.4, pp. 246–258] (book p. 246; PDF p. 263) (book p. 258; PDF p. 275).

### [U4b:4.4-a] Sequential (functional) composition of Galois connections and combinator motivation
- Statement: Complex analyses are constructed in stages starting from a complete lattice `(L_0, ⊑)` closely tied to
  concrete semantics (for example `(𝒫(Z), ⊆)`) and chaining Galois connections `(L_i, α_{i+1}, γ_{i+1}, L_{i+1})`
  for `i = 0, …, k - 1`:
  ```text
  L_0  ⇄_{α_1, γ_1}  L_1  ⇄_{α_2, γ_2}  ⋯  ⇄_{α_k, γ_k}  L_k
  ```
  For `k = 2`, given `(L_0, α_1, γ_1, L_1)` and `(L_1, α_2, γ_2, L_2)`, their *sequential* (or *functional*)
  *composition* is
  ```text
  (L_0, α_2 ∘ α_1, γ_1 ∘ γ_2, L_2)
  ```
  where `(α_2 ∘ α_1)(l_0) = α_2(α_1(l_0))` and `(γ_1 ∘ γ_2)(l_2) = γ_1(γ_2(l_2))`.
  - *Proof of Galois connection (`Proposition 4.20`)*: for `l_0 ∈ L_0` and `l_2 ∈ L_2`,
    `(α_2 ∘ α_1)(l_0) = α_2(α_1(l_0)) ⊑ l_2 ⇔ α_1(l_0) ⊑ γ_2(l_2) ⇔ l_0 ⊑ γ_1(γ_2(l_2)) = (γ_1 ∘ γ_2)(l_2)`.
  - *Preservation of Galois insertions (`Lemma 4.27`)*: if `(L_0, α_1, γ_1, L_1)` and `(L_1, α_2, γ_2, L_2)` are
    Galois insertions, `α_1` and `α_2` are surjective, so `α_2 ∘ α_1` is surjective (equivalently
    `(α_2 ∘ α_1) ∘ (γ_1 ∘ γ_2) = α_2 ∘ (α_1 ∘ γ_1) ∘ γ_2 = α_2 ∘ id_{L_1} ∘ γ_2 = id_{L_2}` `[derived]`), making
    `(L_0, α_2 ∘ α_1, γ_1 ∘ γ_2, L_2)` a Galois insertion.
  - *Modularity rationale (`p. 249`)*: just as structured types are built from primitive types via type constructors,
    combinators build intricate abstract domains from a small library of proven-correct atomic Galois connections so
    each new stage supplies only a minimal delta of proof obligations.
- Citation: [PPA §4.4, pp. 246–247] (book p. 246; PDF p. 263) (book p. 247; PDF p. 264); [PPA §4.4, p. 249] (book p. 249; PDF p. 266)

### Example 4.33 — Two-stage magnitude-difference range abstraction `(𝒫(Z × Z), α_R, γ_R, 𝒫(Range))`
- Statement: One of the components in the Array Bound Analysis approximates the difference in magnitude `|z_1| - |z_2|`
  between two numbers `(z_1, z_2) ∈ Z × Z` (typically the bound and the index) by composing two extraction-function
  Galois connections:
  1. **Stage 1 (`diff`)**: define extraction function `diff : Z × Z → Z` by
     ```text
     diff(z_1, z_2) = |z_1| - |z_2|
     ```
     inducing `(𝒫(Z × Z), α_{diff}, γ_{diff}, 𝒫(Z))` where (for `ZZ ⊆ Z × Z` and `Z ⊆ Z`):
     ```text
     α_{diff}(ZZ) = { |z_1| - |z_2| | (z_1, z_2) ∈ ZZ }
     γ_{diff}(Z)  = { (z_1, z_2) | |z_1| - |z_2| ∈ Z }
     ```
  2. **Stage 2 (`range`)**: define extraction function `range : Z → Range` onto the 5-element set
     `Range = {<-1, -1, 0, +1, >+1}` by
     ```text
     range(z) = <-1   if z < -1
     range(z) = -1    if z = -1
     range(z) = 0     if z = 0
     range(z) = +1    if z = 1
     range(z) = >+1   if z > 1
     ```
     inducing `(𝒫(Z), α_{range}, γ_{range}, 𝒫(Range))` with `α_{range}(Z) = {range(z) | z ∈ Z}` and
     `γ_{range}(R) = {z | range(z) ∈ R}` for `Z ⊆ Z` and `R ⊆ Range`.
  3. **Functional composition (`R`)**: composing Stage 1 and Stage 2 yields `(𝒫(Z × Z), α_R, γ_R, 𝒫(Range))` with
     `α_R = α_{range} ∘ α_{diff}` and `γ_R = γ_{diff} ∘ γ_{range}`, explicitly:
     ```text
     α_R(ZZ) = { range(|z_1| - |z_2|) | (z_1, z_2) ∈ ZZ }
     γ_R(R)  = { (z_1, z_2) | range(|z_1| - |z_2|) ∈ R }
     ```
     By `Exercise 4.15`, this equals the Galois connection specified by `range ∘ diff : Z × Z → Range` (`[derived]`:
     since `diff(z, 0) = z` for `z ≥ 0` and `diff(0, -z) = z` for `z < 0`, both `diff` and `range` are surjective, so
     both stages and `(𝒫(Z × Z), α_R, γ_R, 𝒫(Range))` are Galois insertions; e.g. `diff(5, -7) = -2`). `■`
- Citation: [PPA Example 4.33, pp. 247–248] (book p. 247; PDF p. 264) (book p. 248; PDF p. 265)

## 4.4.1 Component-wise Combinations

Context: Subsection 4.4.1 lifts component Galois connections `(L_i, α_i, γ_i, M_i)` across compound data/domain
constructors: Cartesian products (`independent attribute` vs powerset `relational / tensor` method), total function
spaces `S → L`, and monotone function spaces `L_1 → L_2` [PPA §4.4.1, pp. 249–253] (book p. 249; PDF p. 266) (book p. 253; PDF p. 270).

### [U4b:4.4.1-a] Independent attribute method `(L_1 × L_2, α, γ, M_1 × M_2)`
- Statement: Given Galois connections `(L_1, α_1, γ_1, M_1)` and `(L_2, α_2, γ_2, M_2)`, equip `L_1 × L_2` and
  `M_1 × M_2` with component-wise partial orders (`Appendix A §A.2`) and define `α : L_1 × L_2 → M_1 × M_2` and
  `γ : M_1 × M_2 → L_1 × L_2` by:
  ```text
  α(l_1, l_2) = (α_1(l_1), α_2(l_2))
  γ(m_1, m_2) = (γ_1(m_1), γ_2(m_2))
  ```
  - *Proof of Galois connection*: `α(l_1, l_2) ⊑ (m_1, m_2) ⇔ α_1(l_1) ⊑ m_1 ∧ α_2(l_2) ⊑ m_2 ⇔ l_1 ⊑ γ_1(m_1) ∧ l_2 ⊑ γ_2(m_2) ⇔ (l_1, l_2) ⊑ γ(m_1, m_2)`.
  - *Side conditions*: Preserves Galois insertions (`Exercise 4.17`), scales additively in representation width, and
    discards all cross-component dependencies between `L_1` and `L_2`.
- Citation: [PPA §4.4.1, pp. 249–250] (book p. 249; PDF p. 266) (book p. 250; PDF p. 267)

### Example 4.34 — Independent sign pair `(𝒫(Z) × 𝒫(Z), α_{SS}, γ_{SS}, 𝒫(Sign) × 𝒫(Sign))` and correlation loss
- Statement: Combining two copies of `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))` (`Example 4.21`) by the independent
  attribute method produces `(𝒫(Z) × 𝒫(Z), α_{SS}, γ_{SS}, 𝒫(Sign) × 𝒫(Sign))`:
  ```text
  α_{SS}(Z_1, Z_2) = (α_{sign}(Z_1), α_{sign}(Z_2))
  γ_{SS}(S_1, S_2) = (γ_{sign}(S_1), γ_{sign}(S_2))
  ```
  1. *Correlation loss*: A relational set of concrete pairs `{(z, -z) | z ∈ Z} ⊆ Z × Z` must first be projected to
     `(Z, Z) ∈ 𝒫(Z) × 𝒫(Z)`, abstracting to `α_{SS}(Z, Z) = ({-, 0, +}, {-, 0, +}) = (Sign, Sign)`, which loses the
     opposite-sign invariant completely.
  2. *Non-powerset carrier & tagged-union isomorphism*: Because `𝒫(Z) × 𝒫(Z)` and `𝒫(Sign) × 𝒫(Sign)` are products of
     powersets rather than powersets, `(𝒫(Z) × 𝒫(Z), α_{SS}, γ_{SS}, 𝒫(Sign) × 𝒫(Sign))` is *not* literally given by
     an extraction function; however, it is isomorphic (`§4.3.2`) to
     `(𝒫({1, 2} × Z), α_{twosigns}, γ_{twosigns}, 𝒫({1, 2} × Sign))` induced by extraction function
     `twosigns : {1, 2} × Z → {1, 2} × Sign`, `twosigns(i, z) = (i, sign(z))` (`Exercise 4.16`). `■`
- Citation: [PPA Example 4.34, p. 250] (book p. 250; PDF p. 267)

### [U4b:4.4.1-b] Relational method on powersets `(𝒫(V_1 × V_2), α, γ, 𝒫(D_1 × D_2))` and tensor product `⊗`
- Statement: Given powerset Galois connections `(𝒫(V_1), α_1, γ_1, 𝒫(D_1))` and `(𝒫(V_2), α_2, γ_2, 𝒫(D_2))`, the
  *relational method* constructs `(𝒫(V_1 × V_2), α, γ, 𝒫(D_1 × D_2))` by:
  ```text
  α(VV) = ⋃{ α_1({v_1}) × α_2({v_2}) | (v_1, v_2) ∈ VV }
  γ(DD) = { (v_1, v_2) | α_1({v_1}) × α_2({v_2}) ⊆ DD }
  ```
  - *Proof of adjunction*: `α(VV) ⊆ DD ⇔ (∀(v_1, v_2) ∈ VV : α_1({v_1}) × α_2({v_2}) ⊆ DD) ⇔ (∀(v_1, v_2) ∈ VV : (v_1, v_2) ∈ γ(DD)) ⇔ VV ⊆ γ(DD)`.
  - *Extraction specialisation (`p. 251`)*: when `(𝒫(V_i), α_i, γ_i, 𝒫(D_i))` is induced by `η_i : V_i → D_i`,
    `α_i({v_i}) = {η_i(v_i)}`, so `α(VV) = {(η_1(v_1), η_2(v_2)) | (v_1, v_2) ∈ VV}` and
    `γ(DD) = {(v_1, v_2) ∈ V_1 × V_2 | (η_1(v_1), η_2(v_2)) ∈ DD}` — identical to the extraction connection of
    `η : V_1 × V_2 → D_1 × D_2`, `η(v_1, v_2) = (η_1(v_1), η_2(v_2))`.
  - *Galois insertion preservation (`Exercise 4.18`)*: unlike general direct/tensor same-carrier products, on
    **powersets** `(𝒫(V_1 × V_2), α, γ, 𝒫(D_1 × D_2))` **always** preserves Galois insertions (`[derived]`: every
    singleton `{d_i}` in `𝒫(D_i)` is completely join-irreducible; surjectivity + complete additivity of `α_i` force
    some `v_{d_i} ∈ V_i` with `α_i({v_{d_i}}) = {d_i}`, giving `α({(v_{d_1}, v_{d_2})}) = {(d_1, d_2)}` and hence
    surjectivity of `α` on `𝒫(D_1 × D_2)` by complete additivity!).
  - *Tensor product notation (`p. 252`)*: because `𝒫(U_1 × U_2)` is the *tensor product* `𝒫(U_1) ⊗ 𝒫(U_2)` of
    powerset lattices, the relational method writes `(𝒫(V_1) ⊗ 𝒫(V_2), α, γ, 𝒫(D_1) ⊗ 𝒫(D_2))`. Extending
    `(L_1 ⊗ L_2, α, γ, M_1 ⊗ M_2)` to arbitrary non-powerset complete lattices requires subtle lattice-theoretic
    constructions (`Concluding Remarks`, `[111, 113, 115]`).
- Citation: [PPA §4.4.1, pp. 250–252] (book p. 250; PDF p. 267) (book p. 252; PDF p. 269)

### Example 4.35 — Relational sign pair `(𝒫(Z × Z), α_{SS'}, γ_{SS'}, 𝒫(Sign × Sign))`
- Statement: Applying the relational method to two copies of `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))` yields the
  Galois insertion `(𝒫(Z × Z), α_{SS'}, γ_{SS'}, 𝒫(Sign × Sign))` induced by surjective extraction function
  `twosigns' : Z × Z → Sign × Sign`, `twosigns'(z_1, z_2) = (sign(z_1), sign(z_2))`. For `{(z, -z) | z ∈ Z}`:
  ```text
  α_{SS'}({(z, -z) | z ∈ Z}) = {(-, +), (0, 0), (+, -)}
  γ_{SS'}({(-, +), (0, 0), (+, -)}) = {(z_1, z_2) | (z_1 < 0 ∧ z_2 > 0) ∨ (z_1 = 0 ∧ z_2 = 0) ∨ (z_1 > 0 ∧ z_2 < 0)}
  ```
  retaining the exact sign-opposition and simultaneous-zero correlation lost in `Example 4.34`. `■`
- Citation: [PPA Example 4.35, pp. 251–252] (book p. 251; PDF p. 268) (book p. 252; PDF p. 269)

### [U4b:4.4.1-c] Component-wise combination of total function spaces `(S → L, α', γ', S → M)`
- Statement: For any set `S` and Galois connection `(L, α, γ, M)`, equip total function spaces `S → L` and `S → M`
  with pointwise partial orders (`f_1 ⊑ f_2 iff ∀s ∈ S : f_1(s) ⊑ f_2(s)`, `Appendix A §A.2`) and define:
  ```text
  α'(f) = α ∘ f        (i.e. α'(f)(s) = α(f(s)))
  γ'(g) = γ ∘ g        (i.e. γ'(g)(s) = γ(g(s)))
  ```
  - *Proof*: monotonicity of `α'` and `γ'` follows pointwise from monotonicity of `α` and `γ`; `γ'(α'(f)) = γ ∘ α ∘ f ⊒ f`
    and `α'(γ'(g)) = α ∘ γ ∘ g ⊑ g` follow pointwise from `(4.8)` and `(4.9)`. If `(L, α, γ, M)` is a Galois
    insertion (`α ∘ γ = id_M`), then `α'(γ'(g)) = α ∘ γ ∘ g = g`, so `(S → L, α', γ', S → M)` is a Galois insertion.
- Citation: [PPA §4.4.1, p. 252] (book p. 252; PDF p. 269)

### Example 4.36 — Pointwise variable-to-property abstract states `(Var → L, α', γ', Var → M)`
- Statement: Assuming an analysis mapping program variables to properties from complete lattice `L` (i.e. operating on
  abstract states `Var → L`), given any Galois connection `(L, α, γ, M)` the total function space construction
  (`[U4b:4.4.1-c]`) shows how abstract states of `Var → L` are approximated pointwise by abstract states of `Var → M`.
  (`[derived]`: for finite variable set `Var_⋆`, `Var_⋆ → L` is isomorphic to a finite independent-attribute product and
  tracks each variable independently without expressing inter-variable couplings such as `x = -y`.) `■`
- Citation: [PPA Example 4.36, p. 253] (book p. 253; PDF p. 270)

### [U4b:4.4.1-d] Monotone function space combinator `(L_1 → L_2, α, γ, M_1 → M_2)`
- Statement: Let `L_1 → L_2` and `M_1 → M_2` denote the complete lattices of **monotone** functions ordered pointwise
  (`Appendix A §A.2`). Given Galois connections `(L_1, α_1, γ_1, M_1)` and `(L_2, α_2, γ_2, M_2)`, define
  `α : (L_1 → L_2) → (M_1 → M_2)` and `γ : (M_1 → M_2) → (L_1 → L_2)` by routing arguments contravariantly and
  results covariantly (depicted via two commuting-style square diagrams on `p. 253`):
  ```text
  α(f) = α_2 ∘ f ∘ γ_1
  γ(g) = γ_2 ∘ g ∘ α_1
  ```
  - *Well-definedness & monotonicity*: for monotone `f : L_1 → L_2`, `α_2 ∘ f ∘ γ_1` is a composition of three
    monotone functions (`γ_1`, `f`, `α_2`) and hence belongs to `M_1 → M_2` (and similarly `γ(g) ∈ L_1 → L_2`);
    for `f_1 ⊑ f_2` in `L_1 → L_2` and `m_1 ∈ M_1`, `f_1(γ_1(m_1)) ⊑ f_2(γ_1(m_1))`, so monotonicity of `α_2` gives
    `α(f_1)(m_1) ⊑ α(f_2)(m_1)` (and similarly monotonicity of `γ_2` makes `γ` monotone).
  - *Proof of `(4.8)` and `(4.9)` (`p. 253`)*: for `f ∈ L_1 → L_2` and `l_1 ∈ L_1`, `γ_1(α_1(l_1)) ⊒ l_1` and
    monotonicity of `f` and `γ_2` yield
    `γ(α(f))(l_1) = (γ_2 ∘ α_2)(f((γ_1 ∘ α_1)(l_1))) ⊒ (γ_2 ∘ α_2)(f(l_1)) ⊒ f(l_1)`; symmetrically, for
    `g ∈ M_1 → M_2` and `m_1 ∈ M_1`, `α_1(γ_1(m_1)) ⊑ m_1` and monotonicity of `g` and `α_2` yield
    `α(γ(g))(m_1) = (α_2 ∘ γ_2)(g((α_1 ∘ γ_1)(m_1))) ⊑ (α_2 ∘ γ_2)(g(m_1)) ⊑ g(m_1)`.
  - *Side conditions*: Preserves Galois insertions (`Exercise 4.17`), generalises the total function space when `L_1 = M_1 = 𝒫(S)` with `α_1 = γ_1 = id` on singletons `[derived]`, and satisfies `α(f_1 ∘ f_2) ⊑ α(f_1) ∘ α(f_2)` with strict inequality possible even on Galois insertions (`Exercise 4.20`).
- Citation: [PPA §4.4.1, p. 253] (book p. 253; PDF p. 270)

## 4.4.2 Other Combinations

Context: Subsection 4.4.2 combines two abstractions `(L, α_1, γ_1, M_1)` and `(L, α_2, γ_2, M_2)` sharing the **same**
concrete lattice `L` via direct product, powerset direct tensor product, and `Proposition 4.29` reduction (`ς`) into
reduced products and reduced tensor products, culminating in the 29-atom Array Bound lattice `AB`
[PPA §4.4.2, pp. 253–258] (book p. 253; PDF p. 270) (book p. 258; PDF p. 275).

### [U4b:4.4.2-a] Direct product `(L, α, γ, M_1 × M_2)`
- Statement: Given `(L, α_1, γ_1, M_1)` and `(L, α_2, γ_2, M_2)` over a common complete lattice `L`, their *direct
  product* is `(L, α, γ, M_1 × M_2)` where:
  ```text
  α(l)       = (α_1(l), α_2(l))
  γ(m_1, m_2) = γ_1(m_1) ⊓ γ_2(m_2)
  ```
  - *Proof of adjunction*: `α(l) ⊑ (m_1, m_2) ⇔ α_1(l) ⊑ m_1 ∧ α_2(l) ⊑ m_2 ⇔ l ⊑ γ_1(m_1) ∧ l ⊑ γ_2(m_2) ⇔ l ⊑ γ_1(m_1) ⊓ γ_2(m_2) = γ(m_1, m_2)`.
  - *Side conditions*: Does **not** preserve Galois insertions (`Exercise 4.19`), because incompatible pairs `(m_1, m_2)`
    from the two abstractions can have identical intersection `γ_1(m_1) ⊓ γ_2(m_2)` (for example `⊥_L`).
- Citation: [PPA §4.4.2, p. 254] (book p. 254; PDF p. 271)

### Example 4.37 — Direct product `(𝒫(Z × Z), α_{SSR}, γ_{SSR}, 𝒫(Sign × Sign) × 𝒫(Range))`
- Statement: Taking the direct product of `Example 4.35` (`𝒫(Sign × Sign)`) and `Example 4.33` (`𝒫(Range)`) over
  `L = 𝒫(Z × Z)` yields `(𝒫(Z × Z), α_{SSR}, γ_{SSR}, 𝒫(Sign × Sign) × 𝒫(Range))`:
  `α_{SSR}(ZZ) = ({(sign(z_1), sign(z_2)) | (z_1, z_2) ∈ ZZ}, {range(|z_1| - |z_2|) | (z_1, z_2) ∈ ZZ})` and
  `γ_{SSR}(SS, R) = {(z_1, z_2) | (sign(z_1), sign(z_2)) ∈ SS} ∩ {(z_1, z_2) | range(|z_1| - |z_2|) ∈ R}`. For the
  expression `(x, 3*x)` with concrete values in `ZZ = {(z, 3 * z) | z ∈ Z}`:
  ```text
  α_{SSR}({(z, 3 * z) | z ∈ Z}) = ({(-, -), (0, 0), (+, +)}, {0, <-1})
  ```
  Thus the direct product fails to exploit that `(0, 0)` always pairs with `0` whereas `(-, -)` and `(+, +)` always
  pair with `<-1` (`[derived]`: `γ_{SSR}` therefore admits spurious equal-magnitude pairs such as `(-1, -1)` and
  `(+2, +2)` where `z_2 ≠ 3 * z_1`). `■`
- Citation: [PPA Example 4.37, p. 254] (book p. 254; PDF p. 271)

### [U4b:4.4.2-b] Direct tensor product on powersets `(𝒫(V), α, γ, 𝒫(D_1 × D_2))`
- Statement: Given `(𝒫(V), α_1, γ_1, 𝒫(D_1))` and `(𝒫(V), α_2, γ_2, 𝒫(D_2))` over the **same** concrete powerset
  `𝒫(V)`, their *direct tensor product* is `(𝒫(V), α, γ, 𝒫(D_1 × D_2))` (written `(𝒫(V), α, γ, 𝒫(D_1) ⊗ 𝒫(D_2))`)
  defined by:
  ```text
  α(V') = ⋃{ α_1({v}) × α_2({v}) | v ∈ V' }
  γ(DD) = { v ∈ V | α_1({v}) × α_2({v}) ⊆ DD }
  ```
  - *Proof of adjunction*: `α(V') ⊆ DD ⇔ (∀v ∈ V' : α_1({v}) × α_2({v}) ⊆ DD) ⇔ V' ⊆ γ(DD)` (equivalently `[derived]`,
    compose the diagonal map `Δ_V : V → V × V`, `v ↦ (v, v)`, with `§4.4.1`'s relational method). When induced by
    `η_i : V → D_i`, this equals the extraction connection of `v ↦ (η_1(v), η_2(v))`.
  - *Side conditions*: Preserves per-element correlation between `D_1` and `D_2`, but **fails** to preserve Galois
    insertions whenever `(η_1, η_2) : V → D_1 × D_2` is non-surjective (`Example 4.38`).
- Citation: [PPA §4.4.2, p. 255] (book p. 255; PDF p. 272)

### Example 4.38 — Direct tensor product `(𝒫(Z × Z), α_{SSR'}, γ_{SSR'}, 𝒫(Sign × Sign × Range))`
- Statement: Combining `Example 4.35` (`twosigns'`) and `Example 4.33` (`range ∘ diff`) via the direct tensor product
  (up to `(Sign × Sign) × Range ≅ Sign × Sign × Range`) yields `(𝒫(Z × Z), α_{SSR'}, γ_{SSR'}, 𝒫(Sign × Sign × Range))`,
  induced by extraction function `twosignsrange : Z × Z → Sign × Sign × Range`:
  ```text
  twosignsrange(z_1, z_2) = (sign(z_1), sign(z_2), range(diff(z_1, z_2)))
  ```
  1. *Precision gain over `Example 4.37`*: On `{(z, 3 * z) | z ∈ Z}`,
     `α_{SSR'}({(z, 3 * z) | z ∈ Z}) = {(-, -, <-1), (0, 0, 0), (+, +, <-1)}`, excluding `(-1, -1)` because `(-, -, 0)`
     is absent!
  2. *Failure of Galois insertion*: `Sign × Sign × Range` has `3 · 3 · 5 = 45` triples, several of which describe no
     integer pair: for example `γ_{SSR'}(∅) = γ_{SSR'}({(0, 0, <-1)}) = ∅` (since `z_1 = z_2 = 0` forces
     `|z_1| - |z_2| = 0 ≠ <-1`), violating injectivity of `γ_{SSR'}` (`Lemma 4.27`). `■`
- Citation: [PPA Example 4.38, pp. 255–256] (book p. 255; PDF p. 272) (book p. 256; PDF p. 273)

### [U4b:4.4.2-c] Reduced product and reduced tensor product via `ς` (`Proposition 4.29`)
- Statement: Applying `Proposition 4.29`'s reduction operator `ς` (`§4.3.2`) quotienting `γ`-equivalent abstract
  elements turns non-insertions from `§4.4.2` into Galois insertions:
  1. **Reduced product**: From direct product `(L, α, γ, M_1 × M_2)`, define `ς : M_1 × M_2 → M_1 × M_2` by
     ```text
     ς(m_1, m_2) = ⨅{ (m'_1, m'_2) | γ_1(m_1) ⊓ γ_2(m_2) = γ_1(m'_1) ⊓ γ_2(m'_2) }
     ```
     (`= (α_1(γ_1(m_1) ⊓ γ_2(m_2)), α_2(γ_1(m_1) ⊓ γ_2(m_2)))` by `Fact 4.31` `[derived]`), yielding the Galois
     insertion `(L, α, γ, ς[M_1 × M_2])` (`ς` co-restricted on `α` and restricted on `γ`).
  2. **Reduced tensor product**: From direct tensor product `(𝒫(V), α, γ, 𝒫(D_1 × D_2))`, define
     `ς : 𝒫(D_1 × D_2) → 𝒫(D_1 × D_2)` by
     ```text
     ς(DD) = ⋂{ DD' | γ(DD) = γ(DD') }
     ```
     yielding the Galois insertion `(𝒫(V), α, γ, ς[𝒫(D_1 × D_2)])`.
- Citation: [PPA §4.4.2, pp. 256–257] (book p. 256; PDF p. 273) (book p. 257; PDF p. 274)

### Example 4.39 — Array Bound lattice `AB` (`45 → 29` reduction) and six-step combinator `Summary.`
- Statement: Applying `Proposition 4.29` to `Example 4.38` sets `ς_{SSR'}(SSR) = ⋂{SSR' | γ_{SSR'}(SSR) = γ_{SSR'}(SSR')}`
  for `SSR, SSR' ⊆ Sign × Sign × Range` (and since `twosignsrange` is an extraction function, `ς_{SSR'}(SSR) = SSR ∩ AB`
  by `p. 246` `[derived]`):
  - **`16` infeasible triples mapped as singletons by `ς_{SSR'}` to `∅`** (all involving at least one `0` sign):
    ```text
    (-, 0, <-1),  (-, 0, -1),  (-, 0, 0),
    (0, -, 0),    (0, -, +1),  (0, -, >+1),
    (0, 0, <-1),  (0, 0, -1),  (0, 0, +1),  (0, 0, >+1),
    (0, +, 0),    (0, +, +1),  (0, +, >+1),
    (+, 0, <-1),  (+, 0, -1),  (+, 0, 0)
    ```
    (`[derived]` verification: `z_1 ≠ 0 ∧ z_2 = 0 ⇒ |z_1| - |z_2| = |z_1| ≥ 1 ∈ {+1, >+1}`, ruling out `<-1, -1, 0`
    for `(-, 0, ·)` and `(+, 0, ·)` [`3 + 3 = 6`]; `z_1 = 0 ∧ z_2 ≠ 0 ⇒ -|z_2| ≤ -1 ∈ {<-1, -1}`, ruling out
    `0, +1, >+1` for `(0, -, ·)` and `(0, +, ·)` [`3 + 3 = 6`]; `z_1 = z_2 = 0 ⇒ 0`, ruling out `<-1, -1, +1, >+1`
    [`4`]; total `6 + 6 + 4 = 16`).
  - **`29` feasible pairwise-disjoint nonempty atoms forming `AB` (*Array Bound*)**:
    ```text
    (-, -, <-1),  (-, -, -1),  (-, -, 0),   (-, -, +1),  (-, -, >+1),
    (-, 0, +1),   (-, 0, >+1),
    (-, +, <-1),  (-, +, -1),  (-, +, 0),   (-, +, +1),  (-, +, >+1),
    (0, -, <-1),  (0, -, -1),  (0, 0, 0),   (0, +, <-1), (0, +, -1),
    (+, -, <-1),  (+, -, -1),  (+, -, 0),   (+, -, +1),  (+, -, >+1),
    (+, 0, +1),   (+, 0, >+1),
    (+, +, <-1),  (+, +, -1),  (+, +, 0),   (+, +, +1),  (+, +, >+1)
    ```
  - **Resulting Galois insertion & bit-width payoff**: `ς_{SSR'}[𝒫(Sign × Sign × Range)]` is isomorphic (equal) to
    `𝒫(AB)`, giving the Galois insertion `(𝒫(Z × Z), α_{SSR'}, γ_{SSR'}, 𝒫(AB))` (`F-U4b-02`), shrinking bit
    representation width from `45` bits (`Example 4.38`) down to **`29` bits** (`[external: one 32-bit machine word]`).
  - **`[U4b:4.4.2-d]` Unnumbered `Summary.` (`p. 258`)**: The Array Bound domain is built systematically from three
    atomic extraction Galois connections via six steps:
    `(i)` `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))` via `sign : Z → Sign` (`Example 4.21`);
    `(ii)` `(𝒫(Z × Z), α_{diff}, γ_{diff}, 𝒫(Z))` via `diff : Z × Z → Z` (`Example 4.33`);
    `(iii)` `(𝒫(Z), α_{range}, γ_{range}, 𝒫(Range))` via `range : Z → Range` (`Example 4.33`);
    `(iv)` relational product (`§4.4.1`) on two copies of `(i)` yielding `(𝒫(Z × Z), α_{SS'}, γ_{SS'}, 𝒫(Sign × Sign))`
    (`Example 4.35`);
    `(v)` sequential composition of `(ii)` and `(iii)` yielding `(𝒫(Z × Z), α_R, γ_R, 𝒫(Range))` (`Example 4.33`);
    `(vi)` reduced tensor product of `(iv)` and `(v)` yielding `(𝒫(Z × Z), α_{SSR'}, γ_{SSR'}, 𝒫(AB))`, equivalent to
    extraction function `twosignsrange' : Z × Z → AB` matching `twosignsrange` with codomain restricted to `AB`. `■`
- Citation: [PPA Example 4.39, pp. 257–258] (book p. 257; PDF p. 274) (book p. 258; PDF p. 275)

### Findings (4.4)
- F-U4b-01: Book p. 249 prints `"is that a relative small set of 'basic' analyses, whose correctness have been established"` (`"relative"` for `"relatively"` and `"have"` for `"has"`) [PPA §4.4, p. 249] (book p. 249; PDF p. 266).
- F-U4b-02: `Example 4.39` (`p. 257`), `Mini Project 4.1` (`p. 274`), and `Exercise 4.21` (`p. 281`) reuse the exact
  symbols `α_{SSR'}, γ_{SSR'}` in `(𝒫(Z × Z), α_{SSR'}, γ_{SSR'}, 𝒫(AB))` that `Example 4.38` (`p. 255`) typed on
  `𝒫(Sign × Sign × Range)` (`twosignsrange'` is introduced on `p. 258`); `Summary.` `(iv)` (`p. 258`) also refers to
  `§4.4.1`'s relational method as `"the relational product"` [PPA Example 4.38, p. 255] (book p. 255; PDF p. 272);
  [PPA Example 4.39, pp. 257–258] (book p. 257; PDF p. 274) (book p. 258; PDF p. 275).
- F-U4b-03: In the PDF OCR text layer of `§4.4`, `p. 247` (`PDF p. 264`) drops the `L_0 ... L_k` chain diagram,
  `(L_0, α_2 ∘ α_1, γ_1 ∘ γ_2, L_2)`, and `diff(z_1, z_2) = |z_1| - |z_2|`, while `p. 252` (`PDF p. 269`) corrupts
  `⊗` to `®` and drops the RHS of `γ'(α'(f))` [PPA §4.4, p. 247] (book p. 247; PDF p. 264);
  [PPA §4.4.1, p. 252] (book p. 252; PDF p. 269).

### Projections (4.4)
- software_engineering: Implement `[external: AbstractDomain<T>]` as an algebraic combinator library matching `§4.4`:
  `[external: IndependentProduct<D1, D2>]` (`O(|D_1| + |D_2|)` space, `Example 4.34`), `[external: SparseEnvMap<Var, D>]` +
  `[external: BottomLifted<Env>]` (`Var → M` defaulting missing keys to `⊤_D` and smashing any `x ↦ ⊥_D` to global `⊥`,
  `Example 4.36`), `[external: BitsetTensorDomain<AB>]` (`29`-bit `[external: uint32_t bitmask]` with bitwise OR/AND
  joins/meets and precomputed lookup tables, `Example 4.39`), and `[external: ReducedProduct<D1, D2, Channel>]` using
  `[external: Granger-style directional refinement]` `refine_{1↔2}(m_1, m_2) ⊑ (m_1, m_2)` when exact `ς` over infinite
  `L` is uncomputable.
- cybersecurity: Independent per-variable intervals (`Example 4.36` instantiated on `Interval`) lose symbolic `(idx, len)`
  coupling across control joins (`([0, 3], [4, 4]) ⊔ ([0, 7], [8, 8]) = ([0, 7], [4, 8])`, triggering false alarms or
  missing real `[external: CWE-787]` / `[external: CWE-125]` out-of-bounds bugs), whereas `Example 4.39`'s 29-bit `𝒫(AB)`
  maps the `len ∈ {4, 8}` join to the exact 3-atom invariant `{(+, 0, >+1), (+, +, +1), (+, +, >+1)}` and general
  `0 ≤ idx < len` (including `len = 1, idx = 0`) to the 4-atom invariant `{(+, 0, +1), (+, 0, >+1), (+, +, +1), (+, +, >+1)}`
  `[derived]`; similarly, reduced products (`Sign × Interval × Congruence`) detect signed-to-unsigned
  `[external: size_t wraparound]` (`[external: CWE-195]` / `[external: CWE-681]`) and unaligned pointer offsets
  (`[external: CWE-823]`).
- cs_theory: Galois insertion preservation (`α ∘ γ = id`) is closed under sequential composition (`§4.4`),
  independent product (`Exercise 4.17`), total/monotone function spaces (`§4.4.1`, `Exercise 4.17`), and the
  **powerset** relational method (`Exercise 4.18`, via join-irreducible singletons), whereas same-carrier direct
  product (`Exercise 4.19`) and direct tensor product (`Example 4.38`) create non-injective `γ`-fibres over empty
  intersections until quotiented by `ς` (`Proposition 4.29`).
- debugging: When a `[external: ReducedProduct<D1, D2>]` solver fails to terminate on loops despite valid component
  widenings `∇_1, ∇_2`, check whether channel reduction `ρ_{12}` is invoked *after* `(m_1 ∇_1 m'_1, m_2 ∇_2 m'_2)`:
  refining a widened `[0, ∞]` endpoint back down to `[0, k]` via a partner domain invariant re-triggers finite growth
  `[0, k+1], …` and breaks chain stabilisation `[derived]`; apply `ρ_{12}` inside transfer functions before widening,
  never to post-widened loop headers.

## 4.5 Induced Operations

Context: Section 4.5 shifts from constructing *property spaces* (`§4.4`) to transporting *operations, Monotone
Framework specifications, and fixed-point acceleration operators* along a Galois connection `(L, α, γ, M)`: inducing
best/sound abstract transformers along `α` (`§4.5.1`), proving soundness of generalised Monotone Frameworks such as
Constant Propagation from concrete sets-of-states `SS` (`§4.5.2`), and inducing widening operators on `L` along `γ`
from coarser `M` (`§4.5.3`) [PPA §4.5, pp. 258–270] (book p. 258; PDF p. 275) (book p. 270; PDF p. 287).

### [U4b:4.5-a] Overview of inducing operations along `α` vs along `γ`
- Statement: Given `(L, α, γ, M)`, a concrete or fine-grained operation on `L` may be uncomputable or prohibitively
  expensive (`L` too rich or lacking ACC). Two complementary strategies arise:
  1. **Induce along `α` (`§§4.5.1–4.5.2`)**: replace `f : L → L` entirely by `α ∘ f ∘ γ : M → M` (or a tractable
     upper approximation `g ⊒ α ∘ f ∘ γ`) and compute fixed points in `M`.
  2. **Induce along `γ` (`§4.5.3`)**: keep `f : L → L` over `L` for precision, but lift a widening operator `∇_M` from
     coarser `M` back to `L` via `l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))` so fixed-point iteration terminates in `L`.
- Citation: [PPA §4.5, pp. 258–259] (book p. 258; PDF p. 275) (book p. 259; PDF p. 276)

## 4.5.1 Inducing along the Abstraction Function

Context: Subsection 4.5.1 defines the best induced abstract transformer `α_2 ∘ f_p ∘ γ_1`, proves via `Lemma 4.41`
that it coincides with the representation-function transformer `((α_1 ∘ β_1) ↠ (α_2 ∘ β_2))(↝)` and preserves both
mundane correctness and optimality, and lifts soundness to least fixed points in `Lemma 4.42`
[PPA §4.5.1, pp. 258–262] (book p. 258; PDF p. 275) (book p. 262; PDF p. 279).

### [U4b:4.5.1-a] Induced abstract transformer `α_2 ∘ f_p ∘ γ_1` and upper approximations `g_p`
- Statement: Given `(L_1, α_1, γ_1, M_1)`, `(L_2, α_2, γ_2, M_2)`, and monotone `f_p : L_1 → L_2`, applying `§4.4.1`'s
  monotone function space combinator `(L_1 → L_2, α, γ, M_1 → M_2)` yields the *induced operation*
  ```text
  α(f_p) = α_2 ∘ f_p ∘ γ_1 : M_1 → M_2.
  ```
  In practice, evaluating `γ_1(m_1)` directly is often impossible (infinite sets), so an implementation specifies an
  explicit monotone function `g_p : M_1 → M_2` that safely *over-approximates* (or equals) the induced transformer:
  ```text
  α_2 ∘ f_p ∘ γ_1 ⊑ g_p.
  ```
- Citation: [PPA §4.5.1, p. 259] (book p. 259; PDF p. 276)

### Example 4.40 — Inducing abstract sign addition `g_{plus}` and `⊕` from `f_{plus}`
- Statement: Returning to `Example 4.9`'s simple program `plus` with precise analysis `f_{plus} : 𝒫(Z × Z) → 𝒫(Z)`
  ```text
  f_{plus}(ZZ) = { z_1 + z_2 | (z_1, z_2) ∈ ZZ }
  ```
  using `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))` (`Example 4.21`) and the relational Galois connection
  `(𝒫(Z × Z), α_{SS'}, γ_{SS'}, 𝒫(Sign × Sign))` (`Example 4.35`), induce
  `g_{plus} = α_{sign} ∘ f_{plus} ∘ γ_{SS'} : 𝒫(Sign × Sign) → 𝒫(Sign)` by direct calculation for `SS ⊆ Sign × Sign`:
  ```text
  g_{plus}(SS) = α_{sign}(f_{plus}(γ_{SS'}(SS)))
               = α_{sign}(f_{plus}({ (z_1, z_2) ∈ Z × Z | (sign(z_1), sign(z_2)) ∈ SS }))
               = α_{sign}({ z_1 + z_2 | z_1, z_2 ∈ Z, (sign(z_1), sign(z_2)) ∈ SS })
               = { sign(z_1 + z_2) | z_1, z_2 ∈ Z, (sign(z_1), sign(z_2)) ∈ SS }
               = ⋃{ s_1 ⊕ s_2 | (s_1, s_2) ∈ SS }
  ```
  where `⊕ : Sign × Sign → 𝒫(Sign)` is the "addition" operator on signs (book gloss: `e.g. + ⊕ + = {+} and + ⊕ - = {-, 0, +}`).
  (`[derived]` full `⊕` table: `- ⊕ - = {-}`, `- ⊕ 0 = {-}`, `0 ⊕ - = {-}`, `0 ⊕ 0 = {0}`, `0 ⊕ + = {+}`, `+ ⊕ 0 = {+}`,
  `+ ⊕ + = {+}`, `- ⊕ + = + ⊕ - = {-, 0, +}`; since `f_{plus}` on `𝒫(Z × Z)` is optimal in the sense of `p. 261`,
  `g_{plus} = α_{sign} ∘ f_{plus} ∘ γ_{SS'}` is optimal on `𝒫(Sign × Sign)`.) `■`
- Citation: [PPA Example 4.40, p. 259] (book p. 259; PDF p. 276)

### Lemma 4.41 — Commutation of `↠` with Galois connections
- Statement: If `(L_i, α_i, γ_i, M_i)` are Galois connections and `β_i : V_i → L_i` are representation functions
  (`i = 1, 2`), then for every transition relation `↝ ⊆ V_1 × V_2`:
  ```text
  ((α_1 ∘ β_1) ↠ (α_2 ∘ β_2))(↝) = α_2 ∘ ((β_1 ↠ β_2)(↝)) ∘ γ_1.        ■
  ```
- Proof: For every `m_1 ∈ M_1`, calculate using `(4.10)` (`Proposition 4.20`) and complete additivity of `α_2`
  (`Lemma 4.22(ii)`):
  ```text
  ((α_1 ∘ β_1) ↠ (α_2 ∘ β_2))(↝)(m_1)
    = ⨆{ α_2(β_2(v_2)) | α_1(β_1(v_1)) ⊑ m_1 ∧ v_1 ↝ v_2 }
    = α_2( ⨆{ β_2(v_2) | β_1(v_1) ⊑ γ_1(m_1) ∧ v_1 ↝ v_2 } )
    = α_2( ((β_1 ↠ β_2)(↝))(γ_1(m_1)) ).        ■
  ```
- Citation: [PPA Lemma 4.41, p. 260] (book p. 260; PDF p. 277)

### [U4b:4.5.1-b] Preservation of mundane correctness and optimality across `(L_i, α_i, γ_i, M_i)`
- Statement: Let `R_i : V_i × L_i → {true, false}` be generated by `β_i : V_i → L_i`, and let `S_i : V_i × M_i → {true, false}`
  be generated by `α_i ∘ β_i : V_i → M_i` (`v_i S_i m_i ⇔ v_i R_i γ_i(m_i)`, `§4.3.1`), so `R_1 ↠ R_2` is generated by
  `β_1 ↠ β_2` and `S_1 ↠ S_2` by `(α_1 ∘ β_1) ↠ (α_2 ∘ β_2)` (`Lemma 4.8`).
  1. **Soundness preservation (`pp. 260–261`)**:
     ```text
     (p ⊢ · ↝ ·) (R_1 ↠ R_2) f_p  ∧  α_2 ∘ f_p ∘ γ_1 ⊑ g_p   ⇒   (p ⊢ · ↝ ·) (S_1 ↠ S_2) g_p.
     ```
     *Proof (`Lemma 4.41`)*: `(p ⊢ · ↝ ·)(R_1 ↠ R_2) f_p` means `(β_1 ↠ β_2)(p ⊢ · ↝ ·) ⊑ f_p` (`(4.6)`). Monotonicity
     of `α_2` and `γ_1` plus `Lemma 4.41` yield
     `((α_1 ∘ β_1) ↠ (α_2 ∘ β_2))(p ⊢ · ↝ ·) = α_2 ∘ ((β_1 ↠ β_2)(p ⊢ · ↝ ·)) ∘ γ_1 ⊑ α_2 ∘ f_p ∘ γ_1 ⊑ g_p`,
     which is `(p ⊢ · ↝ ·)(S_1 ↠ S_2) g_p`. *(Direct relational proof also given on `pp. 260–261`: `α_2 ∘ f_p ∘ γ_1 ⊑ g_p`
     is equivalent in `(L_1 → L_2, α, γ, M_1 → M_2)` to `f_p ⊑ γ_2 ∘ g_p ∘ α_1`; hence `v_1 S_1 m_1 ∧ (p ⊢ v_1 ↝ v_2) ⇒ v_1 R_1 γ_1(m_1) ∧ (p ⊢ v_1 ↝ v_2) ⇒ v_2 R_2 f_p(γ_1(m_1)) ⇒ v_2 R_2 (γ_2 ∘ g_p ∘ α_1 ∘ γ_1)(m_1) ⇒ v_2 R_2 γ_2(g_p(m_1)) ⇒ v_2 S_2 g_p(m_1)` using `α_1 ∘ γ_1 ⊑ id` and `(4.4)`.)*
  2. **Optimality (`p. 261`)**: Monotone `f_p : L_1 → L_2` is **optimal** for `p` (also called *most precise* or
     *best* `[external]`) iff `(β_1 ↠ β_2)(p ⊢ · ↝ ·) = f_p` — i.e., `f_p` is sound and satisfies `f_p ⊑ f'` for every
     sound `f'` (`Exercise 4.5` shows the collecting semantics is optimal for `β_i(v_i) = {v_i}`). By `Lemma 4.41`,
     **if `f_p` is optimal on `(L_1, L_2)`, then the induced transformer `α_2 ∘ f_p ∘ γ_1` is automatically optimal on
     `(M_1, M_2)`**: `((α_1 ∘ β_1) ↠ (α_2 ∘ β_2))(p ⊢ · ↝ ·) = α_2 ∘ f_p ∘ γ_1` (as in `Example 4.40`).
- Citation: [PPA §4.5.1, pp. 260–261] (book p. 260; PDF p. 277) (book p. 261; PDF p. 278)

### Lemma 4.42 — Fixed-point soundness of induced operations
- Statement: Let `(L, α, γ, M)` be a Galois connection and let `f : L → L` and `g : M → M` be monotone functions such
  that `α ∘ f ∘ γ ⊑ g` (i.e. `g` is an upper approximation to the operation induced by `f`). Then:
  - `g(m) ⊑ m` implies `f(γ(m)) ⊑ γ(m)`, and
  - `lfp(f) ⊑ γ(lfp(g))` as well as `α(lfp(f)) ⊑ lfp(g)`. `■`
- Proof: Assume `g(m) ⊑ m`. Since `α ∘ f ∘ γ ⊑ g`, `(α ∘ f ∘ γ)(m) ⊑ g(m) ⊑ m`, and adjunction (`Proposition 4.20`)
  gives `(f ∘ γ)(m) ⊑ γ(m)`. Using Tarski's Theorem (`Appendix A Proposition A.10`, `lfp(h) = ⨅{x | h(x) ⊑ x}`) and
  complete multiplicativity of `γ` (`Lemma 4.22(ii)`):
  ```text
  lfp(f) = ⨅{ l | f(l) ⊑ l }
        ⊑ ⨅{ γ(m) | f(γ(m)) ⊑ γ(m) }
        ⊑ ⨅{ γ(m) | g(m) ⊑ m }
        = γ( ⨅{ m | g(m) ⊑ m } )
        = γ(lfp(g)).
  ```
  Adjunction (`Proposition 4.20`) immediately yields `α(lfp(f)) ⊑ lfp(g)`. `■`
- Side conditions: Only inequality `α(lfp(f)) ⊑ lfp(g)` holds in general, **not** fixed-point fusion equality
  `α(lfp(f)) = lfp(g)`, even when `g = α ∘ f ∘ γ` and `(L, α, γ, M)` is a Galois insertion (`Exercise 4.20`).
- Citation: [PPA Lemma 4.42, pp. 261–262] (book p. 261; PDF p. 278) (book p. 262; PDF p. 279)

## 4.5.2 Application to Data Flow Analysis

Context: Subsection 4.5.2 drops the Ascending Chain Condition and restricted function-space axioms of Chapter 2 `§2.3`
to define *generalised Monotone Frameworks*, lifts `(L, α, γ, M)` across `Lab → L` to transport constraint solutions
and semantic soundness (`(4.11) ⇒ (4.12)` under `γ(ȷ) = ι`), proves soundness of concrete sets-of-states `SS`
(`Lemma 4.43`), diagnoses node-vs-edge non-optimality (`Remark.` `p. 266`), and discharges the semantic soundness
proof of `WHILE` Constant Propagation `CP` [PPA §4.5.2, pp. 262–267] (book p. 262; PDF p. 279) (book p. 267; PDF p. 284).

### [U4b:4.5.2-a] Generalised Monotone Frameworks `A = (L, F, E, ι, f_.)` and constraints `A^⊒`
- Statement: A *generalised Monotone Framework* drops the `ACC` requirement on `L` and drops the explicit sub-family
  `ℱ` of `§2.3` (allowing *all* monotone functions `L → L`). An *instance* `A = (L, F, E, ι, f_.)` specifies:
  - a complete lattice `(L, ⊑)`;
  - a finite flow relation `F` and finite extremal-label set `E` over label set `Lab`;
  - an extremal value `ι ∈ L`; and
  - a mapping `f_.` assigning a monotone transfer function `f_ℓ : L → L` to each `ℓ ∈ Lab`.
  The constraint system `A^⊒` over `A_∘, A_• : Lab → L` consists of:
  ```text
  A_∘(ℓ) ⊒ ⨆{ A_•(ℓ') | (ℓ', ℓ) ∈ F } ⊔ ι_E^ℓ        where  ι_E^ℓ = ι if ℓ ∈ E,  ⊥ if ℓ ∉ E
  A_•(ℓ) ⊒ f_ℓ(A_∘(ℓ))
  ```
  Write `(A_∘, A_•) ⊨ A^⊒` when `(A_∘, A_•)` satisfies all constraints of `A^⊒`. Defining the monotone operator
  `\vec{f} : (Lab → L) × (Lab → L) → (Lab → L) × (Lab → L)` by
  ```text
  \vec{f}(A_∘, A_•) = ( λℓ. ⨆{ A_•(ℓ') | (ℓ', ℓ) ∈ F } ⊔ ι_E^ℓ ,  λℓ. f_ℓ(A_∘(ℓ)) )
  ```
  gives the equivalence (`p. 263`, `F-U4b-04`):
  ```text
  (A_∘, A_•) ⊒ \vec{f}(A_∘, A_•)    is equivalent to    (A_∘, A_•) ⊨ A^⊒.
  ```
- Citation: [PPA §4.5.2, pp. 262–263] (book p. 262; PDF p. 279) (book p. 263; PDF p. 280)

### [U4b:4.5.2-b] Lifting `(L, α, γ, M)` to Monotone Framework `B` and solution preservation
- Statement: Given Galois connection `(L, α, γ, M)` and instance `A = (L, F, E, ι, f_.)`, let `B = (M, F, E, ȷ, g_.)`
  be an instance over `M` with the same `F` and `E` satisfying:
  1. `g_ℓ ⊒ α ∘ f_ℓ ∘ γ` for all `ℓ ∈ Lab`; and
  2. `ȷ ⊒ α(ι)` (printed with dotless italic `ȷ` on `pp. 263–264`).
  Then every solution of `B^⊒` concretises to a solution of `A^⊒`:
  ```text
  (B_∘, B_•) ⊨ B^⊒    implies    (γ ∘ B_∘, γ ∘ B_•) ⊨ A^⊒.
  ```
  - *Abstract combinator proof (`pp. 263–264`)*: Lift `(L, α, γ, M)` via `§4.4.1`'s total function space and
    independent attribute combinators to `((Lab → L) × (Lab → L), α', γ', (Lab → M) × (Lab → M))` where
    `α'(A_∘, A_•) = (α ∘ A_∘, α ∘ A_•)` and `γ'(B_∘, B_•) = (γ ∘ B_∘, γ ∘ B_•)`. Using complete additivity of `α`
    (specifically `α(⨆ ...) = ⨆ α(...)` and `α(⊥_L) = ⊥_M` when `ℓ ∉ E`, `Lemma 4.22(ii)`), `ȷ ⊒ α(ι)`, and
    `g_ℓ ⊒ α ∘ f_ℓ ∘ γ`:
    ```text
    (α' ∘ \vec{f} ∘ γ')(B_∘, B_•)
      = ( λℓ. ⨆{ α(γ(B_•(ℓ'))) | (ℓ', ℓ) ∈ F } ⊔ α(ι_E^ℓ) ,  λℓ. α(f_ℓ(γ(B_∘(ℓ)))) )
      ⊑ \vec{g}(B_∘, B_•).
    ```
    By `Lemma 4.42`, `\vec{g}(B_∘, B_•) ⊑ (B_∘, B_•)` implies `\vec{f}(γ'(B_∘, B_•)) ⊑ γ'(B_∘, B_•)`, i.e.,
    `(B_∘, B_•) ⊨ B^⊒ ⇒ (γ ∘ B_∘, γ ∘ B_•) ⊨ A^⊒`.
- Citation: [PPA §4.5.2, pp. 263–264] (book p. 263; PDF p. 280) (book p. 264; PDF p. 281)

### [U4b:4.5.2-c] Mundane semantic correctness transfer `(4.11) ⇒ (4.12)` under `γ(ȷ) = ι`
- Statement: For `WHILE` statement `S_⋆` with `F = flow(S_⋆)`, `E = {init(S_⋆)}`, and representation function
  `β : State → L`, semantic correctness of all solutions to `A^⊒` (`§4.1`) is Display `(4.11)`:
  ```text
  Assume that (A_∘, A_•) ⊨ A^⊒ and ⟨S_⋆, σ_1⟩ →^* σ_2;
  then β(σ_1) ⊑ ι implies β(σ_2) ⊑ ⨆{ A_•(ℓ) | ℓ ∈ final(S_⋆) }.                     (4.11)
  ```
  Using induced representation `α ∘ β : State → M` (`§4.3.1`), semantic correctness of all solutions to `B^⊒` is
  Display `(4.12)`:
  ```text
  Assume that (B_∘, B_•) ⊨ B^⊒ and ⟨S_⋆, σ_1⟩ →^* σ_2;
  then (α ∘ β)(σ_1) ⊑ ȷ implies (α ∘ β)(σ_2) ⊑ ⨆{ B_•(ℓ) | ℓ ∈ final(S_⋆) }.         (4.12)
  ```
  - **Strengthened extremal hypothesis**: To deduce `(4.11) ⇒ (4.12)`, strengthen `ȷ ⊒ α(ι)` by assuming
    ```text
    γ(ȷ) = ι
    ```
    (from which `ȷ ⊒ α(γ(ȷ)) = α(ι)` follows immediately by `(4.9)`).
  - *Proof that `(4.11)` implies `(4.12)` (`p. 264`)*: Suppose `(B_∘, B_•) ⊨ B^⊒`, `⟨S_⋆, σ_1⟩ →^* σ_2`, and
    `(α ∘ β)(σ_1) ⊑ ȷ`. By `[U4b:4.5.2-b]`, `(γ ∘ B_∘, γ ∘ B_•) ⊨ A^⊒`; by adjunction and `γ(ȷ) = ι`,
    `β(σ_1) ⊑ γ(ȷ) = ι` (printed `β(σ_1) ⊑ γ(ȷ) ⊑ ι`). Applying `(4.11)` to `(γ ∘ B_∘, γ ∘ B_•)` gives
    `β(σ_2) ⊑ ⨆{(γ ∘ B_•)(ℓ) | ℓ ∈ final(S_⋆)} ⊑ γ(⨆{B_•(ℓ) | ℓ ∈ final(S_⋆)})` (monotonicity of `γ`), whence
    adjunction yields `(α ∘ β)(σ_2) ⊑ ⨆{B_•(ℓ) | ℓ ∈ final(S_⋆)}`.
- Citation: [PPA §4.5.2, p. 264] (book p. 264; PDF p. 281)

### [U4b:4.5.2-d] Sets of States reference analysis `SS` (`WHILE`)
- Statement: Define concrete generalised Monotone Framework instance `SS` for `S_⋆`:
  - complete lattice `(𝒫(State), ⊆)` (which fails `ACC` since `State = Var → Z` is infinite);
  - `F = flow(S_⋆)`, `E = {init(S_⋆)}`, extremal value `ι = State`;
  - representation function `β : State → 𝒫(State)`, `β(σ) = {σ}` `[derived]`;
  - node-indexed transfer functions `f_ℓ^{SS} : 𝒫(State) → 𝒫(State)`:
    ```text
    f_ℓ^{SS}(Σ) = { σ[x ↦ 𝒜⟦a⟧σ] | σ ∈ Σ }    if [x := a]^ℓ is in S_⋆
    f_ℓ^{SS}(Σ) = Σ                             if [skip]^ℓ is in S_⋆
    f_ℓ^{SS}(Σ) = Σ                             if [b]^ℓ is in S_⋆
    ```
- Citation: [PPA §4.5.2, p. 265] (book p. 265; PDF p. 282)

### Lemma 4.43 — Semantic soundness of Sets of States `SS`
- Statement: Assume `(SS_∘, SS_•) ⊨ SS^⊇` and `⟨S_⋆, σ_1⟩ →^* σ_2`; then `σ_1 ∈ State` implies
  `σ_2 ∈ ⋃{SS_•(ℓ) | ℓ ∈ final(S_⋆)}`. `■`
- Proof: Following `§2.2`, `⟨S, σ⟩ → ⟨S', σ'⟩` implies `final(S) ⊇ final(S') ∧ flow(S) ⊇ flow(S')`, and
  `flow(S) ⊇ flow(S') ∧ (SS_∘, SS_•) ⊨ SS^⊇(S)` implies `(SS_∘, SS_•) ⊨ SS^⊇(S')` (`F-U4b-04`). Prove by structural
  induction on the single-step SOS inference tree (`§2.2`) that:
  1. `(SS_∘, SS_•) ⊨ SS^⊇(S) ∧ ⟨S, σ⟩ → σ' ∧ σ ∈ SS_∘(init(S)) ⇒ σ' ∈ ⋃{SS_•(ℓ) | ℓ ∈ final(S)}`; and
  2. `(SS_∘, SS_•) ⊨ SS^⊇(S) ∧ ⟨S, σ⟩ → ⟨S', σ'⟩ ∧ σ ∈ SS_∘(init(S)) ⇒ σ' ∈ SS_∘(init(S'))`,
  then induct on the length of `⟨S_⋆, σ_1⟩ →^* σ_2` starting from `σ_1 ∈ State = ι ⊆ SS_∘(init(S_⋆))`.
  Representative SOS cases (`p. 266`):
  - *Assignment `⟨[x := a]^ℓ, σ⟩ → σ[x ↦ 𝒜⟦a⟧σ]`*: `init([x := a]^ℓ) = ℓ`, `final([x := a]^ℓ) = {ℓ}`, and
    `SS_•(ℓ) ⊇ {σ[x ↦ 𝒜⟦a⟧σ] | σ ∈ SS_∘(ℓ)}` immediately puts `σ[x ↦ 𝒜⟦a⟧σ] ∈ SS_•(ℓ)`.
  - *Sequence step `⟨S_1; S_2, σ⟩ → ⟨S'_1; S_2, σ'⟩` from `⟨S_1, σ⟩ → ⟨S'_1, σ'⟩`*: `init(S_1; S_2) = init(S_1)` and
    `init(S'_1; S_2) = init(S'_1)`, so the induction hypothesis on `S_1` gives `σ' ∈ SS_∘(init(S'_1; S_2))`.
  - *Sequence completion `⟨S_1; S_2, σ⟩ → ⟨S_2, σ'⟩` from `⟨S_1, σ⟩ → σ'`*: the induction hypothesis gives
    `σ' ∈ ⋃{SS_•(ℓ) | ℓ ∈ final(S_1)}`; since `{(ℓ, init(S_2)) | ℓ ∈ final(S_1)} ⊆ flow(S_1; S_2)`, the entry
    constraint at `init(S_2)` gives `SS_∘(init(S_2)) ⊇ ⋃{SS_•(ℓ) | ℓ ∈ final(S_1)} ∋ σ'`.
  - `[skip]^ℓ`, `if [b]^ℓ then S_1 else S_2`, and `while [b]^ℓ do S_0` follow identically (using `f_ℓ^{SS}(Σ) = Σ` on
    tests). `■`
- Citation: [PPA Lemma 4.43, pp. 265–266] (book p. 265; PDF p. 282) (book p. 266; PDF p. 283)

### [U4b:4.5.2-e] Unnumbered `Remark.` — Non-optimality of node-based `SS` vs edge-based collecting semantics
- Statement: The `SS` analysis is **not** optimal (`p. 261`) and does **not** equal the collecting semantics (`§1.5`,
  `Exercise 4.5`): there exist statements `S_⋆` where `⋃{SS_•(ℓ) | ℓ ∈ final(S_⋆)}` is strictly larger than the
  reachable final states `{σ' | ⟨S_⋆, σ⟩ →^* σ' ∧ σ ∈ State}` (`[derived]` witness: for
  `if [x = 0]^1 then [y := x]^2 else [y := 0]^3`, `f_1^{SS}(State) = State` flows concrete states with `x = 1` into
  label `2`, putting `σ[y ↦ 1] ∈ SS_•(2)` even though every concrete execution finishes with `y = 0`!). Specifying the
  true collecting semantics requires attaching transfer functions to **flow edges** `(ℓ_1, ℓ_2)` rather than **nodes**
  `ℓ` so boolean test outcomes (`ℬ⟦b⟧σ = true` vs `false`) are filtered (`Exercise 2.11`) [PPA Exercise 2.11, p. 137] (book p. 137; PDF p. 156). `■`
- Citation: [PPA §4.5.2, p. 266] (book p. 266; PDF p. 283)

### [U4b:4.5.2-f] Semantic soundness proof of Constant Propagation `CP` induced from `SS`
- Statement: Express `§2.3`'s Constant Propagation (`Table 2.7`) [PPA Table 2.7, p. 73] (book p. 73; PDF p. 92) as a
  generalised Monotone Framework over `Statê_CP = ((Var → Z^⊤)_⊥, ⊑)` (`F-U4b-04`) with `F = flow(S_⋆)`,
  `E = {init(S_⋆)}`, extremal value `λx.⊤`, and `f_.^{CP}` from `Table 2.7`. Representation function
  `β_{CP} : State → Statê_CP`, `β_{CP}(σ) = σ` (`Example 4.6`), induces `(𝒫(State), α_{CP}, γ_{CP}, Statê_CP)`:
  ```text
  α_{CP}(Σ)  = ⨆{ β_{CP}(σ) | σ ∈ Σ }
  γ_{CP}(σ̂) = { σ ∈ State | β_{CP}(σ) ⊑ σ̂ }
  ```
  Verify the two proof obligations of `[U4b:4.5.2-b]`–`[U4b:4.5.2-c]`:
  1. *Extremal equality*: `γ_{CP}(λx.⊤) = {σ ∈ State | σ ⊑ λx.⊤} = State` (`γ(ȷ) = ι` holds with equality!).
  2. *Local transfer bound (`[x := a]^ℓ`)*: for `σ̂ ≠ ⊥` (`F-U4b-04`; for `σ̂ = ⊥`, `γ_{CP}(⊥) = ∅` gives
     `α_{CP}(f_ℓ^{SS}(∅)) = α_{CP}(∅) = ⊥ = f_ℓ^{CP}(⊥)` directly `[derived]`):
     ```text
     α_{CP}(f_ℓ^{SS}(γ_{CP}(σ̂)))
       = α_{CP}(f_ℓ^{SS}({σ | σ ⊑ σ̂}))
       = α_{CP}({σ[x ↦ 𝒜⟦a⟧σ] | σ ⊑ σ̂})
       = ⨆{σ[x ↦ 𝒜⟦a⟧σ] | σ ⊑ σ̂}
       ⊑ σ̂[x ↦ ⨆{𝒜⟦a⟧σ | σ ⊑ σ̂}]
       ⊑ f_ℓ^{CP}(σ̂)
     ```
     using structural induction on `a` to verify `⨆{𝒜⟦a⟧σ | σ ⊑ σ̂} ⊑ 𝒜_{CP}⟦a⟧σ̂` (and trivially `α_{CP} ∘ id ∘ γ_{CP} ⊑ id`
     for `[skip]^ℓ` and `[b]^ℓ`). By `Lemma 4.43` and `(4.11) ⇒ (4.12)`, Constant Propagation is semantically sound.
- Citation: [PPA §4.5.2, pp. 266–267] (book p. 266; PDF p. 283) (book p. 267; PDF p. 284)

## 4.5.3 Inducing along the Concretisation Function

Context: Subsection 4.5.3 addresses complete lattices `L` where ascending fixed-point iteration (`[external: Kleene]`,
`(f^n(⊥_L))_n`) diverges or converges too slowly: instead of coarsening every transfer operation to `α ∘ f ∘ γ` on `M`
(`§4.5.1`), it lifts an upper bound or widening operator `∇_M` on `M` back to `L` along `γ` (`Proposition 4.44`) and
proves exact iterate/fixed-point correspondence (`Lemma 4.45`) [PPA §4.5.3, pp. 267–270] (book p. 267; PDF p. 284) (book p. 270; PDF p. 287).

### [U4b:4.5.3-a] Definition and motivation of `γ`-induced widening `∇_L`
- Statement: Given Galois connection `(L, α, γ, M)` and upper bound / widening operator `∇_M : M × M → M`, define
  `∇_L : L × L → L` by:
  ```text
  l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2)).
  ```
  When `∇_L` is a widening operator on `L`, computing `lfp_{∇_L}(f)` keeps `f` and all non-widened operations at the
  full precision of `L`, applying `M`'s coarsening strictly at widening points.
- Citation: [PPA §4.5.3, p. 267] (book p. 267; PDF p. 284)

### Proposition 4.44 — Sufficient criteria for `γ`-induced widening and Display `(4.13)`
- Statement: Let `(L, α, γ, M)` be a Galois connection and let `∇_M : M × M → M` be an upper bound operator. Then the
  formula
  ```text
  l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))
  ```
  defines an upper bound operator `∇_L : L × L → L`. It defines a **widening operator** if one of the following two
  conditions is fulfilled:
  - `(i)` `M` satisfies the Ascending Chain Condition; or
  - `(ii)` `(L, α, γ, M)` is a Galois insertion and `∇_M : M × M → M` is a widening operator. `■`
- Proof:
  - *Upper bound property*: Since `∇_M` is an upper bound operator, `α(l_i) ⊑ α(l_1) ∇_M α(l_2)` for `i ∈ {1, 2}`.
    Adjunction (`Proposition 4.20`) gives `l_i ⊑ γ(α(l_1) ∇_M α(l_2)) = l_1 ∇_L l_2`.
  - *Case `(i)` (`M` satisfies ACC; arbitrary Galois connection)*: Let `(l_n)_n` be an ascending chain in `L`. By
    `Fact 4.11`, `(l_n^{∇_L})_n` is an ascending chain in `L`, and by definition of `∇_L`, **`l_n^{∇_L} ∈ γ[M]` for
    all `n > 0`** (whereas `l_0^{∇_L} = l_0` need not lie in `γ[M]`). Monotonicity of `α` makes `(α(l_n^{∇_L}))_n` an
    ascending chain in `M`; by ACC on `M`, there exists **`n_0 ≥ 1`** with `α(l_n^{∇_L}) = α(l_{n_0}^{∇_L})` for all
    `n ≥ n_0`. Applying `γ` and using `γ ∘ α ∘ γ = γ` (`Fact 4.24`) on `γ[M]` (`n ≥ n_0 ≥ 1`) gives
    `l_n^{∇_L} = γ(α(l_n^{∇_L})) = γ(α(l_{n_0}^{∇_L})) = l_{n_0}^{∇_L}` for all `n ≥ n_0`.
  - *Case `(ii)` (Galois insertion + `∇_M` widening)*: For ascending `(l_n)_n` in `L`, monotonicity of `α` makes
    `(α(l_n))_n` (`F-U4b-05`) an ascending chain in `M`, so there exists `n_0` (take `n_0 ≥ 1` `[derived]`, `F-U4b-05`)
    with `(α(l_n))^{∇_M} = (α(l_{n_0}))^{∇_M}` for all `n ≥ n_0`. Prove by induction on `n ≥ 0` Display `(4.13)`:
    ```text
    (α(l_n))^{∇_M} = α(l_n^{∇_L}).                                                   (4.13)
    ```
    *Base `n = 0`*: `(α(l_0))^{∇_M} = α(l_0) = α(l_0^{∇_L})`.
    *Step*: assuming `(4.13)` for `n`, `(α(l_{n+1}))^{∇_M} = (α(l_n))^{∇_M} ∇_M α(l_{n+1}) = α(l_n^{∇_L}) ∇_M α(l_{n+1})`,
    while `α(l_{n+1}^{∇_L}) = α(l_n^{∇_L} ∇_L l_{n+1}) = α(γ(α(l_n^{∇_L}) ∇_M α(l_{n+1}))) = α(l_n^{∇_L}) ∇_M α(l_{n+1})`
    because `(L, α, γ, M)` is a Galois insertion (`α ∘ γ = id_M`). By `(4.13)`, `α(l_n^{∇_L}) = α(l_{n_0}^{∇_L})` for
    `n ≥ n_0` (with `n_0 ≥ 1`), so `γ ∘ α ∘ γ = γ` yields `l_n^{∇_L} = l_{n_0}^{∇_L}` for all `n ≥ n_0`. `■`
- Citation: [PPA Proposition 4.44, p. 268] (book p. 268; PDF p. 285)

### Lemma 4.45 — Exact precision of `γ`-induced widening and Displays `(4.14)`–`(4.15)`
- Statement: If `(L, α, γ, M)` is a Galois insertion such that `γ(⊥_M) = ⊥_L`, and if `∇_M : M × M → M` is a widening
  operator, then the widening operator `∇_L : L × L → L` defined by `l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))` satisfies
  ```text
  lfp_{∇_L}(f) = γ(lfp_{∇_M}(α ∘ f ∘ γ))
  ```
  for all monotone functions `f : L → L`. `■`
- Proof: By `Proposition 4.44(ii)`, `∇_L` is a widening operator, so there exists `n_f ≥ 0` with
  `lfp_{∇_L}(f) = f_{∇_L}^{n_f} = f_{∇_L}^n` for `n ≥ n_f`. Setting `g = α ∘ f ∘ γ`, there exists `n_g ≥ 0` with
  `lfp_{∇_M}(g) = g_{∇_M}^{n_g} = g_{∇_M}^n` for `n ≥ n_g`. It suffices to prove by induction on `n ≥ 0` Display `(4.14)`:
  ```text
  f_{∇_L}^n = γ(g_{∇_M}^n).                                                           (4.14)
  ```
  - *Base `n = 0`*: `f_{∇_L}^0 = ⊥_L = γ(⊥_M) = γ(g_{∇_M}^0)` by hypothesis `γ(⊥_M) = ⊥_L`.
  - *Auxiliary equivalence `(4.15)`*: Assuming `(4.14)` at `n`, any Galois connection `(L, α, γ, M)` satisfies
    ```text
    f(f_{∇_L}^n) ⊑ f_{∇_L}^n    ⇔    g(g_{∇_M}^n) ⊑ g_{∇_M}^n.                        (4.15)
    ```
    For `"⇒"`: `f(f_{∇_L}^n) ⊑ f_{∇_L}^n ⇒ α(f(f_{∇_L}^n)) ⊑ α(f_{∇_L}^n) ⇒ α(f(γ(g_{∇_M}^n))) ⊑ α(γ(g_{∇_M}^n)) ⇒ g(g_{∇_M}^n) ⊑ α(γ(g_{∇_M}^n)) ⇒ g(g_{∇_M}^n) ⊑ g_{∇_M}^n` (using `α ∘ γ ⊑ id_M`; **note source misprint `g(g_{∇_L}^n) ⊑ g_{∇_M}^n` on the 4th line of `p. 269`**, `F-U4b-06`).
    For `"⇐"`: `g(g_{∇_M}^n) ⊑ g_{∇_M}^n ⇒ γ(g(g_{∇_M}^n)) ⊑ γ(g_{∇_M}^n) ⇒ γ(α(f(γ(g_{∇_M}^n)))) ⊑ γ(g_{∇_M}^n) ⇒ γ(α(f(f_{∇_L}^n))) ⊑ f_{∇_L}^n ⇒ f(f_{∇_L}^n) ⊑ f_{∇_L}^n` (using `id_L ⊑ γ ∘ α`).
  - *Induction step (`n > 0`, `pp. 269–270`)*: Assuming `(4.14)` and hence `(4.15)` for `n - 1`, and using Galois
    insertion `α(γ(g_{∇_M}^{n-1})) = g_{∇_M}^{n-1}` inside the left argument of `∇_M`:
    ```text
    f_{∇_L}^n = { f_{∇_L}^{n-1}                     if f(f_{∇_L}^{n-1}) ⊑ f_{∇_L}^{n-1}
                { f_{∇_L}^{n-1} ∇_L f(f_{∇_L}^{n-1}) otherwise
              = γ( { g_{∇_M}^{n-1}                        if g(g_{∇_M}^{n-1}) ⊑ g_{∇_M}^{n-1}
                   { α(γ(g_{∇_M}^{n-1})) ∇_M g(g_{∇_M}^{n-1}) otherwise )
              = γ( { g_{∇_M}^{n-1}                  if g(g_{∇_M}^{n-1}) ⊑ g_{∇_M}^{n-1}
                   { g_{∇_M}^{n-1} ∇_M g(g_{∇_M}^{n-1}) otherwise )
              = γ(g_{∇_M}^n).
    ```
    Evaluating `(4.14)` at `n = max(n_f, n_g)` yields `lfp_{∇_L}(f) = γ(lfp_{∇_M}(α ∘ f ∘ γ))`. `■`
- Side conditions: **[U4b:4.5.3-b] Finite-height `∇_M = ⊔_M` corollary (`p. 270`)**: When `M` has finite height (so
  `∇_M = ⊔_M` is a widening operator by `Exercise 4.7`), `(L, α, γ, M)` is a Galois insertion, and `γ(⊥_M) = ⊥_L`,
  `Lemma 4.45` yields `lfp_{∇_L}(f) = γ(lfp(α ∘ f ∘ γ))` in the *exact same number of iterations* (`F-U4b-06`);
  however, when `f` represents a whole CFG equation system, applying `∇_L` **selectively at loop cut-points** while
  keeping exact `L`-transfers/joins elsewhere retains strictly greater precision than `§4.5.1`'s global `α ∘ f ∘ γ`
  coarsening `[derived]`.
- Citation: [PPA Lemma 4.45, pp. 269–270] (book p. 269; PDF p. 286) (book p. 270; PDF p. 287); [PPA §4.5.3, p. 270] (book p. 270; PDF p. 287)

### Findings (4.5)
- F-U4b-04: In `§4.5.2`: `(1)` `p. 263` writes `"(in the manner of Section 4.4)"` for `(A_∘, A_•) ⊒ \vec{f}(A_∘, A_•) ⇔ (A_∘, A_•) ⊨ A^⊒`; `(2)` `Lemma 4.43`'s proof (`pp. 265–266`) writes parametrised `SS^⊇(S)` / `SS^⊇(S')` though `SS^⊇` was introduced unparametrised on `p. 265`, and `p. 266` line 4 prints `"contain the equation"` (for `⊇`) followed by duplicated `"we see that that"`; `(3)` `Constant Propagation Analysis` (`p. 266`) defines `Statê_CP = ((Var → Z^⊤)_⊥, ⊑)` over unstarred `Var` (matching `State = Var → Z` so `β_{CP}(σ) = σ`, whereas `Example 4.1` and `Table 2.7` used `Var_⋆`) and writes `ι` for `B`'s extremal value `ȷ`; `(4)` on `p. 267`, `⨆{σ[x ↦ 𝒜⟦a⟧σ] | σ ⊑ σ̂} ⊑ σ̂[x ↦ ⨆{𝒜⟦a⟧σ | σ ⊑ σ̂}]` tacitly assumes `σ̂ ≠ ⊥` (`γ_{CP}(⊥) = ∅` makes `σ̂ = ⊥` trivial, whereas `⊥[x ↦ …]` is undefined on smash-bottom `_⊥`) [PPA §4.5.2, pp. 263–267] (book p. 263; PDF p. 280) (book p. 267; PDF p. 284); [PPA Lemma 4.43, pp. 265–266] (book p. 265; PDF p. 282) (book p. 266; PDF p. 283).
- F-U4b-05: In `Proposition 4.44` (`p. 268`), the box prints `"one of the following two conditions are fulfilled"`, proof case `(ii)` prints `(α(l_n)_n)` instead of `(α(l_n))_n`, and case `(ii)` omits explicitly stating `n_0 ≥ 1` (needed so `l_{n_0}^{∇_L} ∈ γ[M]` when invoking `γ ∘ α ∘ γ = γ`, unlike case `(i)` which explicitly writes `n_0 ≥ 1`) [PPA Proposition 4.44, p. 268] (book p. 268; PDF p. 285).
- F-U4b-06: In `Lemma 4.45`'s proof (`p. 269`), the 4th line of the `"⇒"` derivation for `(4.15)` prints **`g(g_{∇_L}^n) ⊑ g_{∇_M}^n`** — subscript `∇_L` on inner `g^n` is ill-typed (`g : M → M`) and must read **`g(g_{∇_M}^n) ⊑ g_{∇_M}^n`**; on `p. 270`, prose prints `"the number of iterations needed turn out to be the same"` (`"turn"` for `"turns"`) [PPA Lemma 4.45, p. 269] (book p. 269; PDF p. 286); [PPA §4.5.3, p. 270] (book p. 270; PDF p. 287).
- F-U4b-07: In the PDF OCR text layer of `§4.5`, `Lemma 4.41`'s main equation (`p. 260`), `(B_∘, B_•) ⊨ B^⊒ ⇒ (γ ∘ B_∘, γ ∘ B_•) ⊨ A^⊒` (`p. 263`), `l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))` (`p. 267`), and `Lemma 4.45`'s main equation plus `(4.14)`–`(4.15)` (`p. 269`) are completely dropped [PPA Lemma 4.41, p. 260] (book p. 260; PDF p. 277); [PPA Lemma 4.45, p. 269] (book p. 269; PDF p. 286).

### Projections (4.5)
- software_engineering: Decouple transfer-function **specification** (`f^# = α_2 ∘ f_p ∘ γ_1`, `§4.5.1`) from
  production **implementation** (`g_p ⊒ f^#`): use `[external: property-based or SMT testing]` on the pointwise
  adjunction obligation `∀v_1, v_2, m_1 : (α_1(β_1(v_1)) ⊑ m_1 ∧ p ⊢ v_1 ↝ v_2) ⇒ α_2(β_2(v_2)) ⊑ g_p(m_1)` (`Lemma 4.41`
  + `Lemma 4.22`) to catch unsound transfer edge cases (`⊥` smash, `[external: division-by-zero, overflow]`) automatically;
  for rich domains `L` (e.g. bounded-disjunction or `[external: polyhedral]` states), deploy `γ`-induced widening `∇_L`
  (`§4.5.3`) **only at loop headers** rather than coarsening every CFG node via `α ∘ f ∘ γ` (`Lemma 4.45`).
- cybersecurity: Node-attached Monotone Frameworks (`SS` in `§4.5.2`, `f_ℓ^{SS}([b]^ℓ) = Σ`, `Remark.` `p. 266`)
  cannot filter branch conditions `[b]^ℓ` (e.g. non-null or array-bounds guards), flooding `[external: CWE-476]` /
  `[external: CWE-787]` scanners with false positives unless guard refinement is attached to **CFG edges**
  `f_{(ℓ_1, ℓ_2)}` (`Exercise 2.11`); furthermore, end-to-end vulnerability soundness `(4.12)` requires verifying
  `γ(ȷ) = ι` (`§4.5.2`) so entry states cover all attacker-controlled inputs.
- cs_theory: `Lemma 4.41` unifies Chapter 4's two correctness formalisms (`§4.1` representation transformers `↠` and
  `§4.3` Galois adjunctions), proving that best induced transformers `α_2 ∘ f_p ∘ γ_1` preserve optimality (`§4.5.1`)
  even though sequential composition does not (`α(f_1 ∘ f_2) ⊑ α(f_1) ∘ α(f_2)`, `Exercise 4.20`, explaining why
  Constant Propagation on `[x := y - y]` gives `⊤` whereas optimal `α_{CP} ∘ f_ℓ^{SS} ∘ γ_{CP}` gives `0` `[derived]`);
  `§4.5.2` generalises Chapter 2 `§2.3` Monotone Frameworks (`U6`) to arbitrary complete lattices without `ACC`.
- debugging: Before deploying `l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))` (`Proposition 4.44`, `Lemma 4.45`), check three
  failure modes: `(1)` if `M` lacks `ACC` and `(L, α, γ, M)` is *not* a Galois insertion (e.g. an unreduced direct
  product `Exercise 4.19`), `(4.13)` breaks and `∇_L` may fail to stabilise; `(2)` if `γ(⊥_M) ⊐ ⊥_L`, step `0` already
  inflates `f_{∇_L}^1` above `γ(g_{∇_M}^1)`; and `(3)` **never** copy the formula to narrowing
  `l_1 Δ_L l_2 = γ(α(l_1) Δ_M α(l_2))` (`Exercise 4.24`), which violates `(l_1 Δ_L l_2) ⊑ l_1` whenever `l_1 ∉ γ[M]`!

## Concluding Remarks

Context: Chapter 4's *Concluding Remarks* (`pp. 270–273`) record bibliographic provenance (`[37, 39, 35, 40, 179, 126, 68]`)
and develop four foundational extensions: the complete lattice of upper closure operators (`[external: uco(L)]`,
`pp. 270–271`), distributive/atom-based bit-vector bounds and general tensor products (`p. 271`), concrete relational
numerical and regular-word domains (`pp. 271–272`), and lattice duality, dual Galois connections for
program-transformation guards, and non-duality with Denotational Semantics (`pp. 272–273`)
[PPA Chapter 4 Concluding Remarks, pp. 270–273] (book p. 270; PDF p. 287) (book p. 273; PDF p. 290).

### [U4b:CR-a] Primary sources for Chapter 4
- Statement: Chapter 4's core Abstract Interpretation development is based primarily on `[37, 39, 35, 40]` (`P. Cousot` and
  `R. Cousot [37, 39, 40]`; `P. Cousot [35]`); `Mini Project 4.1` and the series of examples leading up to `Example 4.39` (`AB`) are based on `[179]`
  (Webber); `Mini Project 4.3` is inspired by `[126, 68]` (Nielson and Nielson `[126]`; Hansen, Jensen, Nielson, and
  Nielson `[68]`).
- Citation: [PPA Chapter 4 Concluding Remarks, p. 270] (book p. 270; PDF p. 287)

### [U4b:CR-b] Upper closure operators `ρ : L → L`, precision ordering, and domain decompositions
- Statement: An *upper closure operator* `ρ : L → L` is a monotone function that is *extensive* (`ρ ⊒ λl.l`) and
  *idempotent* (`ρ ∘ ρ = ρ`) `[39]`:
  1. **Equivalence to Galois insertions up to isomorphism**: For any Galois connection `(L, α, γ, M)`, `γ ∘ α : L → L`
     is an upper closure operator (`(4.8)`, `Fact 4.24`). Conversely, for any upper closure operator `ρ : L → L`, its
     image `ρ[L] = {ρ(l) | l ∈ L}` equals its fixed-point set `Fix(ρ) = {l ∈ L | l = ρ(l)}`, forms a complete lattice
     under `⊑_L`, and makes `(L, ρ, λl.l, ρ[L])` a Galois insertion. Representing abstract domains inside `L` loses no
     essential structure up to isomorphism.
  2. **Complete lattice of upper closure operators**: Ordering upper closure operators on `L` pointwise (`ρ_1 ⊑ ρ_2`
     iff `∀l ∈ L : ρ_1(l) ⊑ ρ_2(l)`) is equivalent to reverse inclusion of their images (`ρ_2(L) ⊆ ρ_1(L)` as printed on
     `p. 271`, `F-U4b-08`), meaning `ρ_2` is *more approximate* (coarser) than `ρ_1`. Under `⊑`, the set of upper
     closure operators on `L` (`uco(L)` `[external]`) is a complete lattice with least (most precise) element `λl.l`,
     greatest (most approximate) element `λl.⊤`, and binary greatest lower bound `ρ_1 ⊓ ρ_2` giving the **reduced
     product** `[39]` (`p. 271` mis-cites `Section 4.3.` instead of `§4.4.2`, `F-U4b-08`).
  3. **Further combinators and inverse decompositions (`p. 271`)**: Upper closure operators explain *reduced cardinal
     power* `[39]` (refining `M_1 → M_2` conditional invariants `[external]`) and *disjunctive completion* `[39]`
     (closing `ρ[L]` under concrete joins `⨆_L`, equivalently quotienting the powerset `𝒫(M)` under `γ^∨(S) = ⨆_{m ∈ S} γ(m)`
     when `L` is completely distributive `[derived]`, eliminating join-merge precision loss such as `- ⊔ + = ⊤` in
     `Sign'` at up to `2^{|M|}` state cost); "inverting" them yields *pseudo-complementation* for minimal
     reduced-product factors `[33, 34]` and irreducible-property bases for disjunctive completion `[63, 64]`.
- Citation: [PPA Chapter 4 Concluding Remarks, pp. 270–271] (book p. 270; PDF p. 287) (book p. 271; PDF p. 288)

### [U4b:CR-c] Stronger complete-lattice properties and non-powerset tensor products
- Statement: Adding stronger algebraic structure to complete lattices — such as *distributivity* and *atoms* or *join
  irreducible elements* playing the role of powerset singletons — lifts powerset / Bit Vector Framework efficiency
  bounds to non-powerset complete lattices, giving low iteration bounds for `(f^n(⊥))_n` stabilisation `[129, 118]`.
  Constructing the *tensor product* `L_1 ⊗ L_2` for complete lattices that are not powersets is non-trivial and was
  developed for program analysis by Nielson `[111, 113, 115]`.
- Citation: [PPA Chapter 4 Concluding Remarks, p. 271] (book p. 271; PDF p. 288)

### [U4b:CR-d] Concrete applications: logic programming, relational geometry, regular words, and chaotic iteration
- Statement: Major concrete application families built on Abstract Interpretation (`pp. 271–272`):
  1. **Logic programming**: groundness of substitutions at program points, widening-based iteration strategies, and
     closure-operator domain decompositions.
  2. **1D and relational 2D+ numerical vector spaces (over `Z` or `Q`)**:
     - *1D*: `Interval` (and finite/arbitrary unions of intervals) plus modular arithmetic `{x | x mod k_1 = k_2}`,
       combinable via product/reduction.
     - *2D+ relational*: axis-independent geometric domains beyond independent attributes, starting from Karr's affine
       subspaces `{(x, y) | k_1 x + k_2 y = k_3}` `[94]` and Cousot and Halbwachs' convex polygons `[41]`
       (`[external: convex polyhedra]`; inequalities closed under intersection), generalised and combined with
       congruences by Granger `[66, 67]` and Masdupuy `[105]`.
  3. **Regular sets of words via integer vectors**: Deutsch `[44, 45]` and Deutsch and Colby `[31, 32]` reduce regular
     word-set descriptions to integer-vector relations, capturing activation-record shapes in higher-order programs and
     communication patterns in concurrent programs.
  4. **Dynamic domain construction & chaotic iteration**: dynamic property-space construction `[24]` (Bourdoncle) and
     widening/narrowing chaotic-iteration strategies `[25]` (Bourdoncle).
- Citation: [PPA Chapter 4 Concluding Remarks, pp. 271–272] (book p. 271; PDF p. 288) (book p. 272; PDF p. 289)

### [U4b:CR-e] Lattice duality `⊑^d`, dual Galois connections for transformation guards, and non-duality with Denotational Semantics
- Statement: Define the *dual* partial ordering `⊑^d` of `⊑` (`pp. 272–273`) by `l_1 ⊑^d l_2 iff l_2 ⊑ l_1` (`⊑^d` is `⊒`):
  1. **Relating Abstract Interpretation and "classical" Data Flow Analysis**: Dualising replaces least elements with
     greatest elements and `lfp` with `gfp` (while *monotonicity is its own dual*). Thus Abstract Interpretation (`⊤`
     trivially safe/uninformative, seeking `lfp`) and "classical" Data Flow Analysis (`⊥` trivially safe/uninformative,
     seeking `gfp`) are exact lattice duals.
  2. **Dual Galois connections for program-transformation enabling conditions (`p. 273`)**: Suppose program point `ℓ`
     has reachable property `l_ℓ ∈ L` and a program transformation `Ξ` is valid iff `l_ℓ ⊑ l_Ξ`. Under approximation
     `l'_ℓ` of `l_ℓ` and `l'_Ξ` of `l_Ξ`, ensuring the approximate test `l'_ℓ ⊑ l'_Ξ` implies concrete validity
     `l_ℓ ⊑ l_Ξ` demands **opposite approximation directions**:
     ```text
     l_ℓ ⊑ l'_ℓ        (upward over-approximation of point facts via Galois connections)
     l'_Ξ ⊑ l_Ξ        (downward under-approximation of enabling guards via dual Galois connections).
     ```
  3. **Non-duality of Abstract Interpretation and Denotational Semantics (`p. 273`)**: In Denotational Semantics `⊥`
     conveys no information and growing larger (`⊑`) adds information (`⊤` would represent conflict), whereas in
     Abstract Interpretation `⊤` conveys no information and growing smaller (`⊑`) adds information (`⊥` often denotes
     non-reachability); **because both formalisms ask for least fixed points (`lfp`), they are NOT duals of one
     another**, and importing domain-theoretic intuitions blindly into Abstract Interpretation is unsound.
- Citation: [PPA Chapter 4 Concluding Remarks, pp. 272–273] (book p. 272; PDF p. 289) (book p. 273; PDF p. 290)

### Findings (Concluding Remarks)
- F-U4b-08: On book p. 271 (`PDF p. 288`), paragraph 1 switches from `ρ[L]` (`p. 270`) to round parentheses
  `ρ_2(L) ⊆ ρ_1(L)` (and reuses italic `ρ` for closure operators after Chapter 3 used `ρ` for environments), while
  paragraph 2 prints `"the construction of the reduced product [39] (see Section 4.3.)"` — **reduced product** is
  defined in **`§4.4.2` (`p. 256`)**, whereas `§4.3.2` only defines single-lattice reduction `ς`; on `p. 273`, the PDF
  OCR text layer corrupts `Ξ` into `3` [PPA Chapter 4 Concluding Remarks, pp. 270–273] (book p. 270; PDF p. 287) (book p. 273; PDF p. 290).

### Projections (Concluding Remarks)
- software_engineering: In optimising compilers, enforce distinct types `[external: OverApprox<L>]` (`l_ℓ ⊑ l'_ℓ`) for
  reachable program-point invariants vs `[external: UnderApprox<L>]` (`l'_Ξ ⊑ l_Ξ`, dual Galois connection) for
  pass-enabling guards (`Ξ` such as bounds-check elimination, devirtualisation, or dead-branch pruning) so upward
  approximations can never be accidentally consumed as transformation sufficiency witnesses.
- cybersecurity: Unsound direction inversion on `l_ℓ ⊑ l_Ξ` (Concluding Remarks) — over-approximating a security check's
  safety region `l_Ξ` upward instead of downward — causes compilers or `[external: JITs (V8 TurboFan / eBPF verifiers)]`
  to delete mandatory runtime bounds or type checks while out-of-bounds states remain concretely reachable
  (`[external: CWE-787]` / `[external: CWE-843]`).
- cs_theory: `[external: uco(L)]` provides a representation-independent meta-lattice of all abstractions of `L`
  (`ρ_1 ⊓ ρ_2` = reduced product `§4.4.2`; `ρ_1 ⊔ ρ_2` = `Fix(ρ_1) ∩ Fix(ρ_2)` common invariants `[derived]`), while
  Concluding Remarks cleanly separate order-duality (`AI ↔ classical gfp DFA`) from information-order inversion without
  fixed-point inversion (`AI ≇^d Denotational Semantics`).
- debugging: When translating papers or textbook equations between `⊔`/`lfp` (Abstract Interpretation) and `⊓`/`gfp`
  (classical compiler DFA, e.g. `[external: Kildall constant propagation]` or must-analyses in Chapter 2), verify that
  **every** lattice component (`⊥ ↔ ⊤`, `⊑ ↔ ⊒`, `⊔ ↔ ⊓`, `lfp ↔ gfp`, `∇ ↔` dual widening) is flipped simultaneously
  rather than mixing `[external: Scott-domain]` `⊥`-upward `lfp` intuition.

## Mini Projects

Context: Three capstone Mini Projects (`pp. 274–275`) apply `§4.4`'s combinator synthesis and `§4.5.2`'s semantic
soundness lifting to finite-list relations (`Mini Project 4.1`), Chapter 2 Shape Analysis (`Mini Project 4.2`), and
Chapter 3 Control and Data Flow Analysis (`Mini Project 4.3`)
[PPA Chapter 4 Mini Projects, pp. 274–275] (book p. 274; PDF p. 291) (book p. 275; PDF p. 292).

### Mini Project 4.1 — A Galois Connection for Lists `(𝒫(V × V), α, γ, 𝒫(LR))`
- Statement: Let `V` be the domain of finite-length lists `x = [x_1, ⋯, x_n]` (`x = []` when `n = 0`) over a simple
  data type, with `length(x) = n` and `length(y) = m` for `y = [y_1, ⋯, y_m]`. Two lists have the *same head* iff
  `n > 0, m > 0`, and `x_1 = y_1`; list `x` is a *suffix* of `y` iff `∃k ≥ 0 : n + k = m ∧ ∀i ∈ {1, ⋯, n} : x_i = y_{i+k}`.
  Construct a Galois insertion `(𝒫(V × V), α, γ, 𝒫(LR))` where `LR ⊆ 𝒫({H, S}) × Range`, `H` records same head, `S`
  glosses `"one list is a suffix of the other"` (`F-U4b-09`), and `Range` describes `length(x) - length(y)`. `■`
- Worked resolution `[derived]`:
  1. Define extraction functions `hs : V × V → 𝒫({H, S})` and `ldiff : V × V → Z` (`ldiff(x, y) = length(x) - length(y)`),
     compose `range ∘ ldiff` (`Example 4.33` stage 2), take their direct tensor product on `𝒫(V × V)` into
     `𝒫(𝒫({H, S}) × Range)` (`4 · 5 = 20` candidates), and apply `ς` (`Proposition 4.29`).
  2. **Under the formal asymmetric suffix definition (`x` suffix of `y`, requiring `n ≤ m`)**:
     - For `r ∈ {+1, >+1}` (`n > m`): `S` is impossible (`k = m - n < 0`), while `m = 0` (`([], …)`) vs `m > 0` with
       `x_1 = y_1` or `x_1 ≠ y_1` (assuming base type size `≥ 2`) realises `∅` and `{H}` (`2 · 2 = 4` atoms).
     - For `r = 0` (`n = m`): `x = y = []` realises **`({S}, 0)`** (`n = m = 0` makes `H` false and `S` vacuously true
       with `k = 0`!); non-empty `x = y = [a]` realises `({H, S}, 0)`; `[a, b]` vs `[a, c]` realises `({H}, 0)`; `[a]`
       vs `[b]` realises `(∅, 0)` (`4` atoms).
     - For `r ∈ {-1, <-1}` (`n < m`): all 4 subsets `∅, {H}, {S}, {H, S}` are inhabited over any `≥ 2`-element base
       type — e.g. for `-1`: `([b], [a, c]) ↦ ∅`, `([a], [a, b]) ↦ {H}`, `([b], [a, b]) ↦ {S}`, `([a], [a, a]) ↦ {H, S}`;
       analogously padding `y` for `<-1` (`2 · 4 = 8` atoms).
     Total: **`|LR| = 4 + 4 + 8 = 16` atoms** (eliminating the 4 triples `({S}, +1), ({H, S}, +1), ({S}, >+1), ({H, S}, >+1)`).
     *(Under the symmetric prose gloss `"one list is a suffix of the other"`, those 4 triples become inhabited by
     swapping `x, y` from `-1, <-1`, giving `|LR| = 20` over a `≥ 2`-element alphabet; over a 1-element alphabet where
     `x_1 = y_1` always holds for `n, m > 0`, `{S}` only occurs when `min(n, m) = 0`.)*
- Citation: [PPA Mini Project 4.1, p. 274] (book p. 274; PDF p. 291)

### Mini Project 4.2 — Correctness of the Shape Analysis `(𝒫(State × Heap), α_{SA}, γ_{SA}, 𝒫(SG))`
- Statement: Returning to Chapter 2 `§2.6` Shape Analysis [PPA §2.6, p. 104] (book p. 104; PDF p. 123)
  over `(σ, ℋ) ∈ State × Heap` and shape graphs `(S, H, is) ∈ SG`, define `vars(ξ)(σ) = n_X` where `X = {x | σ(x) = ξ}`
  and proceed in three steps:
  1. Define `β_{SA} : State × Heap → 𝒫(SG)` mapping `(σ, ℋ)` to the singleton set containing its compatible shape graph
     (`§2.6`), construct `(𝒫(State × Heap), α_{SA}, γ_{SA}, 𝒫(SG))`, and determine whether it is a Galois insertion.
  2. Specify concrete `(𝒫(State × Heap), ⊆)` generalised Monotone Framework `SH` (`f_ℓ^{SH}`) and prove its soundness
     (`Lemma 4.43` analogue).
  3. Prove `f_ℓ^{SA} ⊒ α_{SA} ∘ f_ℓ^{SH} ∘ γ_{SA}` for all transfer functions (`§4.5.2`), conclude semantic correctness
     of Shape Analysis, and determine whether `f_ℓ^{SA} = α_{SA} ∘ f_ℓ^{SH} ∘ γ_{SA}` holds (`Exercise 2.23`)
     [PPA Exercise 2.23, p. 139] (book p. 139; PDF p. 158). `■`
- Worked resolution `[derived]`:
  1. **Construction & non-insertion**: `β_{SA}(σ, ℋ) = {(S, H, is)}` where `S = {(x, vars(σ(x))(σ)) | x ∈ dom(σ) ∧ σ(x) ∈ Loc}`,
     `H = {(vars(ξ_1)(σ), sel, vars(ξ_2)(σ)) | ℋ(ξ_1, sel) = ξ_2 ∧ vars(ξ_1)(σ) ≠ n_∅ ∨ reachable}`, and `is` marks
     heap-shared summary/abstract locations compatible with `(σ, ℋ)` (`§2.6.1`). Lifting `β_{SA}` (`§4.3`) gives
     `α_{SA}(C) = ⋃{β_{SA}(σ, ℋ) | (σ, ℋ) ∈ C}` and `γ_{SA}(G) = {(σ, ℋ) | β_{SA}(σ, ℋ) ⊆ G}`. **Not a Galois
     insertion**: `SG` contains syntactically valid shape graphs in `SG` that are *not* the exact `β_{SA}` image of any
     concrete `(σ, ℋ)` (e.g. graphs with `n_∅` unreachable garbage nodes or conservative over-approximated sharing bits
     `is` not forced by any concrete heap witness), giving `γ_{SA}({g}) = ∅ = γ_{SA}(∅)`.
  2. **`SH` and soundness**: `SH = (𝒫(State × Heap), flow(S_⋆), {init(S_⋆)}, State × Heap, f_.^{SH})` with
     `f_ℓ^{SH}(C) = {(σ', ℋ') | ∃(σ, ℋ) ∈ C : ⟨[B]^ℓ, σ, ℋ⟩ → (σ', ℋ')}` on elementary pointer/mutation statements and
     identity on `[skip]^ℓ` / `[b]^ℓ`; SOS induction identical to `Lemma 4.43` proves `(4.11)`, and `γ_{SA}(SG) = State × Heap`
     discharges `γ(ȷ) = ι`.
  3. **Transfer inequality & non-optimality**: Case analysis on `[x := y]^ℓ`, `[x := y.sel]^ℓ`, `[x.sel := y]^ℓ`, and
     `[malloc x]^ℓ` shows `β_{SA}(σ', ℋ') ⊆ f_ℓ^{SA}(g)` whenever `β_{SA}(σ, ℋ) = {g}`, giving
     `α_{SA}(f_ℓ^{SH}(γ_{SA}(G))) ⊆ f_ℓ^{SA}(G)`. **Equality fails (`f_ℓ^{SA} ≠ α_{SA} ∘ f_ℓ^{SH} ∘ γ_{SA}`)**: on
     materialisation/destructive update over summary node `n_∅` (e.g. cyclic vs DAG structures sharing the same shape
     graph `g`, cf. `Exercise 2.23`), conservative `is` / `H` edge retention in `f_ℓ^{SA}` produces impossible post-graphs
     not arising from any concrete `(σ, ℋ) ∈ γ_{SA}({g})`.
- Citation: [PPA Mini Project 4.2, pp. 274–275] (book p. 274; PDF p. 291) (book p. 275; PDF p. 292)

### Mini Project 4.3 — Application to Control Flow Analysis (`⊨_{SV}` and `⊨_D`)
- Statement: Perform the `§4.5.2` development for Chapter 3 `§3.5` Control and Data Flow Analysis
  [PPA §3.5, pp. 182–189] (book p. 182; PDF p. 200) (book p. 189; PDF p. 207):
  1. Specify `"sets of values"` analysis `(Ĉ_{SV}, ρ̂_{SV}) ⊨_{SV} e` in the manner of `§3.5.1` taking `Data = Val`
     (`Val` as in `§3.2`), and formulate/prove semantic correctness in the manner of `Example 4.4` (printed
     `Example 4.40`, `F-U4b-10`) and `Theorem 3.10` [PPA Theorem 3.10, p. 159] (book p. 159; PDF p. 177).
  2. Given monotone structure `(L, ℱ)` (`§3.5.2`) and Galois connection `(𝒫(Val), α, γ, L)`, construct a Galois
     connection `({(Ĉ_{SV}, ρ̂_{SV}) | ⋯}, α', γ', {(Ĉ, D̂, ρ̂, d̂) | ⋯})` (`F-U4b-10`: `d̂` printed for `δ̂`), and
     formulate/prove `(Ĉ, D̂, ρ̂, d̂) ⊨_D e ⇒ γ'((Ĉ, D̂, ρ̂, d̂)) ⊨_{SV} e` to conclude semantic correctness of `⊨_D`. `■`
- Worked resolution `[derived]`:
  1. **`⊨_{SV}` specification & soundness**: Set `Val̂_{SV} = 𝒫(Val)` (`c ∈ Const` and closures `close t in ρ`),
     `Ĉ_{SV} : Lab → 𝒫(Val)`, `ρ̂_{SV} : Var → 𝒫(Val)` with clauses mirroring `Table 3.8` (`c ∈ Ĉ_{SV}(ℓ)` on `[con]`,
     `ρ̂_{SV}(x) ⊆ Ĉ_{SV}(ℓ)` on `[var]`, `{close fn x => e_0 in ρ | ρ ℛ_{SV} ρ̂_{SV}} ⊆ Ĉ_{SV}(ℓ)` on `[fn]`/`[fun]`,
     conditional guard filtering `true ∈ Ĉ_{SV}(ℓ_0) ⇒ …`, and operator image `f_{op}` on `[op]`). Coinductive
     preservation (`Theorem 3.10` + `Exercise 4.3`) proves `ρ ⊢ e →^* v^ℓ ∧ ρ ℛ_{SV} ρ̂_{SV} ∧ (Ĉ_{SV}, ρ̂_{SV}) ⊨_{SV} e ⇒ v ∈ Ĉ_{SV}(ℓ)`.
  2. **Pointwise lifting & `(Ĉ, D̂, ρ̂, δ̂) ⊨_D e ⇒ γ'(Ĉ, D̂, ρ̂, δ̂) ⊨_{SV} e`**: Split `𝒫(Val) ≅ 𝒫(Clos) × 𝒫(Const)`
     (`Val = Clos ⊎ Const`); `(𝒫(Const), α, γ, L)` (or `(𝒫(Val), α, γ, L)` combined with closure-term projection to
     `𝒫(Term)`) lifts via `§4.4.1` total function spaces (`Lab → ·`, `Var → ·`) and products to `(α', γ')` where
     `γ'(Ĉ, D̂, ρ̂, δ̂) = (λℓ. γ_{Clos}(Ĉ(ℓ)) ∪ γ(D̂(ℓ)), λx. γ_{Clos}(ρ̂(x)) ∪ γ(δ̂(x)))`. Assuming sound abstract operator
     transfers `f̂_{op} ⊒ α ∘ f_{op} ∘ (γ × γ)` (`Table 3.9`), structural induction on `e` shows every clause of
     `(Ĉ, D̂, ρ̂, δ̂) ⊨_D e` implies the corresponding clause of `γ'(Ĉ, D̂, ρ̂, δ̂) ⊨_{SV} e`, discharging semantic
     correctness of `§3.5.2` modularly from Step 1.
- Citation: [PPA Mini Project 4.3, p. 275] (book p. 275; PDF p. 292)

### Findings (Mini Projects)
- F-U4b-09: `Mini Project 4.1` (`p. 274`) formally defines asymmetric suffix (`x` is a suffix of `y` iff `∃k ≥ 0 : n + k = m ∧ …`, giving `|LR| = 16`), then glosses `S` five lines below as symmetric `"one list is a suffix of the other"` (giving `|LR| = 20`) [PPA Mini Project 4.1, p. 274] (book p. 274; PDF p. 291).
- F-U4b-10: `Mini Project 4.3` (`p. 275`) Part 1 prints `"in the manner of Example 4.40 and Theorem 3.10"` where CFA
  mundane correctness is **`Example 4.4`** (`p. 215`; `Example 4.40` on `p. 259` is `g_{plus}`), and Part 2 prints
  Latin **`d̂`** four times in `(Ĉ, D̂, ρ̂, d̂)` where `§3.5.2` (`Table 3.9`, `p. 188`) uses Greek **`δ̂ ∈ DEnv̂`**
  [PPA Mini Project 4.3, p. 275] (book p. 275; PDF p. 292); [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206).

### Projections (Mini Projects)
- software_engineering: Follow the two-tier verification architecture of `Mini Projects 4.2–4.3` whenever building a
  complex heap or interprocedural analyzer: write a non-computable mathematical reference specification (`SH` or `⊨_{SV}`)
  whose SOS soundness is trivial (`Lemma 4.43` / `Theorem 3.10`), then discharge every abstract domain optimization as a
  local inequality `f^# ⊒ α ∘ f^{ref} ∘ γ`.
- cybersecurity: `Mini Project 4.1`'s `LR` tracks slice/buffer prefix-sharing (`H`) and length delta (`Range`), catching
  off-by-one slice truncations (`[external: CWE-193]`); `Mini Project 4.2` certifies heap alias/sharing summaries
  behind `[external: use-after-free]` and `[external: double-free]` detectors (`[external: CWE-416]` / `[external: CWE-415]`);
  `Mini Project 4.3` certifies higher-order closure + `[external: taint]`/value propagation (`⊨_D`) across dynamic callbacks.
- cs_theory: `Mini Project 4.2` connects Chapter 2 `§2.6` Shape Analysis to `U6` (Galois connections), illustrating
  a natural real-world domain where `(𝒫(State × Heap), α_{SA}, γ_{SA}, 𝒫(SG))` is a sound Galois connection that fails
  both Galois insertion (`γ_{SA}` non-injective) and local transfer optimality (`f_ℓ^{SA} ⊐ α_{SA} ∘ f_ℓ^{SH} ∘ γ_{SA}`);
  `Mini Project 4.3` connects Chapter 3 `§3.5` (`⊨_D`, `U4`) to `U6`.
- debugging: When debugging false positives in Shape Analysis (`Mini Project 4.2`), distinguish *unreachable ghost shape
  graphs* (`γ_{SA}({g}) = ∅`, domain non-insertion) from *summary-node materialisation imprecision*
  (`f_ℓ^{SA}({g}) ⊋ α_{SA}(f_ℓ^{SH}(γ_{SA}({g})))`, transfer over-approximation).

## Exercises

Context: Book p. 276 (`PDF p. 293`) opens with `Figure 4.10` (`(Sign', ⊑)`) followed by `24` unstarred exercises
(`Exercises 4.1–4.24`, `pp. 276–282`) spanning `§4.1` (`4.1`–`4.5`), `§4.2` (`4.6`–`4.12`), `§4.3` (`4.13`–`4.14`),
`§4.4` (`4.15`–`4.21`), and `§4.5` (`4.22`–`4.24`)
[PPA Figure 4.10, p. 276] (book p. 276; PDF p. 293); [PPA Chapter 4 Exercises, pp. 276–282] (book p. 276; PDF p. 293) (book p. 282; PDF p. 299).

### Figure 4.10 — The complete lattice `(Sign', ⊑)`
- Statement: Seven-element Hasse diagram of `(Sign', ⊑)` with carrier `Sign' = {⊥, -, 0, +, -0, 0+, ⊤}` and covering
  edges:
  ```text
            ⊤
          /   \
        -0     0+
        | \   / |
        -   0   +
         \  |  /
            ⊥
  ```
  Specifically: `⊥ ⊏ -`, `⊥ ⊏ 0`, `⊥ ⊏ +`; `- ⊏ -0`, `0 ⊏ -0`, `0 ⊏ 0+`, `+ ⊏ 0+`; `-0 ⊏ ⊤`, `0+ ⊏ ⊤` (omitting a
  `-+` non-zero element, so `- ⊔ + = ⊤` and `-0 ⊓ 0+ = 0`).
- Side conditions `[derived]`: Contains the 5-element pentagon sublattice `{⊥, -, -0, +, ⊤}` (`[external: N_5]`: `- ⊏ -0`, yet
  `- ⊔ + = ⊤ = -0 ⊔ +` and `- ⊓ + = ⊥ = -0 ⊓ +`), so **`Sign'` is neither distributive nor modular** — yet removing
  `{-, +}` restores complete multiplicativity of `γ_{IS'} : Sign' → Interval` (`Exercise 4.13`).
- Citation: [PPA Figure 4.10, p. 276] (book p. 276; PDF p. 293)

### Exercise 4.1 — Correctness relation `R_{ZS'}` and representation `β_{ZS'}` for `Sign'`
- Statement: For `(Sign', ⊑)` of `Figure 4.10`, define correctness relation `R_{ZS'} : Z × Sign' → {true, false}`,
  verify `(4.4)` and `(4.5)`, define `β_{ZS'} : Z → Sign'`, and show `R_{ZS'}` is generated by `β_{ZS'}`. `■`
- Worked resolution `[derived]`: Set `β_{ZS'}(z) = -` (`z < 0`), `0` (`z = 0`), `+` (`z > 0`), and `z R_{ZS'} s' ⇔ β_{ZS'}(z) ⊑ s'`
  (`z R_{ZS'} ⊥ = false`, `z R_{ZS'} -0 ⇔ z ≤ 0`, `z R_{ZS'} 0+ ⇔ z ≥ 0`, `z R_{ZS'} ⊤ = true`). Upward closure `(4.4)`
  follows by transitivity of `⊑`, and `(4.5)` holds because `{s' ∈ Sign' | z R_{ZS'} s'} = ↑β_{ZS'}(z)` has least
  element `β_{ZS'}(z)` (`Lemma 4.5`).
- Citation: [PPA Exercise 4.1, p. 276] (book p. 276; PDF p. 293)

### Exercise 4.2 — Closure of correctness relations under non-empty joins vs failure of `v R ⊥`
- Statement: Show that `(4.4)` and `(4.5)` imply `v R l_1 ∧ v R l_2 ⇒ v R (l_1 ⊔ l_2)` and more generally
  `(∀l ∈ L' ≠ ∅ : v R l) ⇒ v R (⨆L')`. Give an example where `v R ⊥` fails even though `(4.4)` and `(4.5)` hold. `■`
- Worked resolution `[derived]`: Pick any `l_0 ∈ L'` (using `L' ≠ ∅`); since `l_0 ⊑ ⨆L'` and `v R l_0`, `(4.4)` immediately
  yields `v R (⨆L')` (notably without even needing `(4.5)`!). For `L' = ∅`, `⨆∅ = ⊥`, and in `Exercise 4.1` (`R_{ZS'}`)
  or powerset membership `v ∈ X` on `(𝒫(V), ⊆)`, `(4.4)` and `(4.5)` hold while `z R_{ZS'} ⊥` (`v ∈ ∅`) is `false`!
- Citation: [PPA Exercise 4.2, p. 276] (book p. 276; PDF p. 293)

### Exercise 4.3 — Mundane correctness `(4.3)` of 0-CFA (`Example 4.4` via `Theorem 3.10`)
- Statement: Show that Chapter 3's 0-CFA is correct in the sense of `(4.3)` (`Example 4.4`): first show
  `(Ĉ, ρ̂) ⊨ v^ℓ iff v 𝒱 (ρ̂, Ĉ(ℓ))` for values `v` (closures or constants); next deduce
  `[] ⊢ (e_⋆ v_1^{ℓ_1})^ℓ →^* v^ℓ ∧ (Ĉ, ρ̂) ⊨ (e_⋆ v_1^{ℓ_1})^ℓ ⇒ (Ĉ, ρ̂) ⊨ v^ℓ` from `Theorem 3.10`; finally establish `(4.3)`. `■`
- Worked resolution `[derived]`: By `Table 3.4` (`§3.2.2`), if `v = c`, `(Ĉ, ρ̂) ⊨ c^ℓ` is vacuously `true` (`[con]`) and
  `c 𝒱 (ρ̂, Ĉ(ℓ))` is `true`; if `v = close t in ρ_0` (`t = fn x => e_0` or `fun f x => e_0`), `Table 3.4 [close]` gives
  `(Ĉ, ρ̂) ⊨ (close t in ρ_0)^ℓ ⇔ {t} ⊆ Ĉ(ℓ) ∧ ρ_0 ℛ ρ̂` (where `ρ_0 ℛ ρ̂` iff `∀x ∈ dom(ρ_0) : ρ_0(x) 𝒱 (ρ̂, ρ̂(x))`, with
  no `(Ĉ, ρ̂) ⊨ e_0` conjunct) `⇔ v 𝒱 (ρ̂, Ĉ(ℓ))` (`§3.2.2`). Repeated single-step subject reduction (`Theorem 3.10`)
  from `[] ℛ ρ̂` yields `(Ĉ, ρ̂) ⊨ v^ℓ`; finally `v_1 R_{CFA} (ρ̂, v̂_1)` gives `(Ĉ[ℓ_1 ↦ v̂_1], ρ̂) ⊨ v_1^{ℓ_1}`, so `(4.2)`
  for `Example 4.2`/`4.4` yields `v_2 R_{CFA} (ρ̂, Ĉ(ℓ))`.
- Citation: [PPA Exercise 4.3, pp. 276–277] (book p. 276; PDF p. 293) (book p. 277; PDF p. 294)

### Exercise 4.4 — Equivalence `v R_{CFA} (ρ̂, v̂) iff β_{CFA}(v) ⊑_{CFA} (ρ̂, v̂)`
- Statement: Prove `v R_{CFA} (ρ̂, v̂) iff β_{CFA}(v) ⊑_{CFA} (ρ̂, v̂)` (`Examples 4.4, 4.7`) by induction on the size of `v`. `■`
- Worked resolution `[derived]`: Base `v = c`: `β_{CFA}(c) = (λx.∅, ∅) ⊑_{CFA} (ρ̂, v̂)` always, matching `c R_{CFA} (ρ̂, v̂) = true`.
  Step `v = close t in ρ_0`: `v R_{CFA} (ρ̂, v̂) ⇔ {t} ⊆ v̂ ∧ (∀x ∈ dom(ρ_0) : ρ_0(x) R_{CFA} (ρ̂, ρ̂(x)))`. By IH on every
  strictly smaller value `ρ_0(x)` (`x ∈ dom(ρ_0)`, finite non-circular list environment `ρ_0`), writing `β_{CFA}(ρ_0(x)) = (ρ̂_x, v̂_x)`:
  `ρ_0(x) R_{CFA} (ρ̂, ρ̂(x)) ⇔ (ρ̂_x, v̂_x) ⊑_{CFA} (ρ̂, ρ̂(x)) ⇔ (ρ̂_x ⊑ ρ̂ ∧ v̂_x ⊆ ρ̂(x))`. Thus `∀y ∈ dom(ρ_0) : ρ̂_y ⊑ ρ̂` and
  `∀x ∈ dom(ρ_0) : v̂_x ⊆ ρ̂(x)` hold iff `β_{CFA}^E(ρ_0) ⊑ ρ̂` (`Example 4.7`: `β_{CFA}^E(ρ_0)(x) = ⋃{ρ̂_y(x) | y ∈ dom(ρ_0)} ∪ (v̂_x if x ∈ dom(ρ_0); ∅ else)`),
  which together with `{t} ⊆ v̂` equals `β_{CFA}(close t in ρ_0) = (β_{CFA}^E(ρ_0), {t}) ⊑_{CFA} (ρ̂, v̂)`.
- Citation: [PPA Exercise 4.4, p. 277] (book p. 277; PDF p. 294)

### Exercise 4.5 — Optimality of the collecting semantics on `(𝒫(V_i), ⊆)`
- Statement: For `L_i = (𝒫(V_i), ⊆)` (`i = 1, 2`), define `f_p(l_1) = {v_2 ∈ V_2 | ∃v_1 ∈ l_1 : p ⊢ v_1 ↝ v_2}` and
  `v_i R_i l_i iff v_i ∈ l_i`. Show `f_p` is monotone, `(p ⊢ · ↝ ·)(R_1 ↠ R_2) f_p`, `(p ⊢ · ↝ ·)(R_1 ↠ R_2) f' ⇔ f_p ⊑ f'`,
  and `f_p = (β_1 ↠ β_2)(p ⊢ · ↝ ·)` for `β_i(v_i) = {v_i}`. `■`
- Worked resolution `[derived]`: `l_1 ⊆ l'_1 ⇒ f_p(l_1) ⊆ f_p(l'_1)`. For `f' : L_1 → L_2`, `(p ⊢ · ↝ ·)(R_1 ↠ R_2) f'`
  means `∀v_1, v_2, l_1 : (v_1 ∈ l_1 ∧ p ⊢ v_1 ↝ v_2) ⇒ v_2 ∈ f'(l_1)`, which is literally `∀l_1 : f_p(l_1) ⊆ f'(l_1)`,
  i.e. `f_p ⊑ f'` (taking `f' = f_p` gives soundness of `f_p`). Finally `((β_1 ↠ β_2)(p ⊢ · ↝ ·))(l_1) = ⋃{{v_2} | {v_1} ⊆ l_1 ∧ p ⊢ v_1 ↝ v_2} = f_p(l_1)`.
- Citation: [PPA Exercise 4.5, p. 277] (book p. 277; PDF p. 294)

### Exercise 4.6 — Five upper bound operators and widening condition on `↓l'`
- Statement: Show that `(1)` `⊔`, `(2)` `λ(l_1, l_2). ⊤`, `(3)` `λ(l_1, l_2). (l_1 if l_2 ⊑ l_1 else ⊤)`,
  `(4)` `λ(l_1, l_2). (l_2 if l_1 = ⊥; l_1 if l_2 ⊑ l_1 ∧ l_1 ≠ ⊥; ⊤ otherwise)`, and
  `(5)` `λ(l_1, l_2). (l_1 ⊔ l_2 if l_1 ⊑ l' ∨ l_2 ⊑ l_1 else ⊤)` are upper bound operators, determine which are
  widening operators, and give sufficient conditions on `l'` for `(5)` (`F-U4b-11`). `■`
- Worked resolution `[derived]`: Upper bound (`l_1, l_2 ⊑ l_1 ⊔̆ l_2`) holds case-by-case (`l_2 ⊑ l_1 ⇒ l_1 ⊔ l_2 = l_1`;
  `l_1 = ⊥ ⇒ ⊥ ⊑ l_2`; else `⊤` or `l_1 ⊔ l_2`). Widening status on general `L`:
  - `(1)` `⊔` is **not** a widening in general (stabilises iff `L` satisfies `ACC`, `Exercise 4.7`).
  - `(2)`, `(3)`, and `(4)` **are always widening operators** on every complete lattice `L` (`l_n^∇` jumps to `⊤` on the
    first strict step in `(2)`–`(3)` and on at most the second strict step in `(4)`).
  - `(5)` is a widening operator **iff the principal ideal `↓l' = {x ∈ L | x ⊑ l'}` satisfies `ACC`**: if `↓l'` has `ACC`,
    `(l_n^∇)_n` either stays inside `↓l'` and stabilises by `ACC` or leaves `↓l'` once and jumps to `⊤` on the next
    strict increase; conversely, if `↓l'` contains a strictly ascending chain `x_0 ⊏ x_1 ⊏ ⋯ ⊑ l'`, then `x_n^∇ = x_n ⊑ l'`
    never stabilises (matching `Example 4.12`!).
- Citation: [PPA Exercise 4.6, p. 277] (book p. 277; PDF p. 294)

### Exercise 4.7 — Equivalence of widening and upper bound operators under `ACC`
- Statement: Show that if `L` satisfies `ACC` then an operator on `L` is a widening operator iff it is an upper bound
  operator, and conclude that `⊔ : L × L → L` is a widening operator under `ACC`. `■`
- Worked resolution `[derived]`: Every widening operator is an upper bound operator by definition; conversely, for any
  upper bound operator `⊔̆` and chain `(l_n)_n`, `Fact 4.11` makes `(l_n^{⊔̆})_n` an ascending chain in `L`, which must
  stabilise by `ACC`. Since `⊔` is an upper bound operator, `⊔` is a widening operator whenever `L` satisfies `ACC`.
- Citation: [PPA Exercise 4.7, p. 277] (book p. 277; PDF p. 294)

### Exercise 4.8 — Non-bottom initial seeds `f_∇^0 = l_0` for `Fact 4.14` vs `Proposition 4.13`
- Statement: Consider changing `f_∇^0 = ⊥` to `f_∇^0 = l_0` under `(a)` `l_0 = f(⊥)`, `(b)` `l_0 = f^{27}(⊥)`,
  `(c)` `l_0 ∈ Ext(f)` (`l_0 ⊑ f(l_0)`), or `(d)` `l_0` arbitrary. Which suffice for `Fact 4.14` and `Proposition 4.13`? `■`
- Worked resolution `[derived]`:
  - **`Fact 4.14` holds under all four (`(a)`, `(b)`, `(c)`, and `(d)` arbitrary `l_0`)**: `Fact 4.14` only asserts
     monotonicity of `(f_∇^n)_n` (`f_∇^n ⊑ f_∇^m` for `n ≤ m`, true by `l_1 ⊑ l_1 ∇ l_2`) and reductiveness (`f_∇^m ∈ Red(f)`) at
    stabilisation (`f_∇^{m+1} = f_∇^m ⇒ f(f_∇^m) ⊑ f_∇^m` by the `if`-guard, whence `lfp(f) ⊑ f_∇^m` by Tarski!).
  - **`Proposition 4.13` (termination) holds under `(a)`, `(b)`, and `(c)` (`f(⊥), f^{27}(⊥) ∈ Ext(f)`), and FAILS under
    `(d)` arbitrary `l_0`**: `Proposition 4.13`'s proof (`p. 228`) requires `(l_n)_n` (`l_0 = f_∇^0`, `l_{n+1} = f(f_∇^n)`)
    to be an **ascending chain** so `∇` stabilises `(l_n^∇)_n = (f_∇^n)_n`; `l_0 ⊑ l_1 = f(l_0)` holds iff `l_0 ∈ Ext(f)`.
    *Counterexample for `(d)`*: Let `L = (N_0 ∪ {∞}) × {0, 1}` ordered component-wise (`⊥ = (0, 0)`, `⊤ = (∞, 1)`),
    and define `x ∇ y = x` if `y ⊑ x`, `(m, 1)` if `x = (n, 1)` and `y = (m, 0)` with finite `n < m`, and `⊤`
    otherwise. Clearly `∇` is an upper bound operator (`x, y ⊑ x ∇ y`), and on *every* ascending chain `(l_k)_k` the
    middle branch never fires (if `l_0` has bit `0` then `l_{j-1}^∇ = l_0` has bit `0` at the first strict jump; if
    `l_0` has bit `1` then monotonicity forces every `l_k` to have bit `1`), so `(l_k^∇)_k` stabilises in `≤ 1` strict
    step and `∇` is a genuine widening operator. Now take monotone `f(n, b) = (n + 1, 0)` (`∞ + 1 = ∞`) and
    `l_0 = (0, 1) ∉ Ext(f)` (`f(0, 1) = (1, 0)`): at every `k ≥ 0`, `f(k, 1) = (k + 1, 0) ⋢ (k, 1)` bypasses the
    reductive guard and `f_∇^{k+1} = (k, 1) ∇ (k + 1, 0) = (k + 1, 1)`, so `(f_∇^k)_k = ((k, 1))_k` diverges forever!
- Citation: [PPA Exercise 4.8, pp. 277–278] (book p. 277; PDF p. 294) (book p. 278; PDF p. 295)

### Exercise 4.9 — Bounded-box delayed widening `int_1 ∇ int_2` on `Interval`
- Statement: Let `∇_K` be as in `Example 4.15` and for `int' ∈ Interval` with `inf(int') > -∞` and `sup(int') < ∞`,
  define `int_1 ∇ int_2 = int_1 ⊔ int_2` if `int_1 ⊑ int' ∨ int_2 ⊑ int_1`, and `int_1 ∇_K int_2` otherwise. Show
  `∀int_1, int_2 : int_1 ∇ int_2 ⊑ int_1 ∇_K int_2` (possibly strict), show `∇` is an upper bound operator, and
  determine whether `∇` is a widening operator. `■`
- Worked resolution `[derived]`: Since `⊔` is the *least* upper bound and `∇_K` is an upper bound operator,
  `int_1 ⊔ int_2 ⊑ int_1 ∇_K int_2`, giving `int_1 ∇ int_2 ⊑ int_1 ∇_K int_2` everywhere; for `int' = [0, 10]`, `K = ∅`,
  `[0, 1] ∇ [0, 2] = [0, 2] ⊏ [0, ∞] = [0, 1] ∇_∅ [0, 2]`. Upper bound holds since both branches (`⊔` and `∇_K`) bound
  `int_1, int_2`. **Yes, `∇` IS a widening operator**: because `inf(int') = A ∈ Z` and `sup(int') = B ∈ Z` are finite,
  `↓int' = {⊥} ∪ {[a, b] | A ≤ a ≤ b ≤ B}` is **finite** (`1 + (B - A + 1)(B - A + 2)/2` elements)! Hence any ascending
  chain `(int_n^∇)_n` can take only finitely many strict steps while `int_n^∇ ⊑ int'`; once `int_{n_1}^∇ ⋢ int'`, every
  subsequent strict step uses `∇_K`, which stabilises on the shifted tail (`Example 4.15`).
- Citation: [PPA Exercise 4.9, p. 278] (book p. 278; PDF p. 295)

### Exercise 4.10 — Monotonicity and upper-bound property of narrowed chain `(l_n^Δ)_n`
- Statement: Let `(l_n)_n` be a descending chain and `Δ : L × L → L` satisfy `l'_2 ⊑ l'_1 ⇒ l'_2 ⊑ (l'_1 Δ l'_2) ⊑ l'_1`.
  Show `(l_n^Δ)_n` is a descending chain and `l_n^Δ ⊒ l_n` for all `n`. `■`
- Worked resolution `[derived]`: Induct on `n`: at `n = 0`, `l_0^Δ = l_0 ⊒ l_0`. Assuming `l_n^Δ ⊒ l_n`, since `(l_n)_n`
  is descending (`l_n ⊒ l_{n+1}`), transitivity gives `l_{n+1} ⊑ l_n ⊑ l_n^Δ`. Instantiating the `Δ`-axiom at
  `l'_1 = l_n^Δ, l'_2 = l_{n+1}` yields `l_{n+1} ⊑ (l_n^Δ Δ l_{n+1}) = l_{n+1}^Δ ⊑ l_n^Δ`.
- Citation: [PPA Exercise 4.10, p. 278] (book p. 278; PDF p. 295)

### Exercise 4.11 — Descending chain truncators `ϒ` vs narrowing operators `Δ`
- Statement: Given `f_∇^m ∈ Red(f)`, a *descending chain truncator* `ϒ` maps descending chains `(l_n)_n` to `N_0` such
  that `(∀n ≤ ϒ((l_n)_n) : l_n = l'_n) ⇒ ϒ((l_n)_n) = ϒ((l'_n)_n)` (`F-U4b-11`), yielding `lfp_∇^ϒ(f) = f^{m'}(f_∇^m)`
  where `m' = ϒ((f^n(f_∇^m))_n)`. Prove this is a sound alternative to narrowing and relate the two concepts. `■`
- Worked resolution `[derived]`: Because `f(f_∇^m) ⊑ f_∇^m` and `f` is monotone, `(f^n(f_∇^m))_n` is a descending chain
  inside `Red(f)` with `lfp(f) ⊑ f^n(f_∇^m) ⊑ f_∇^m` for every `n ≥ 0`; prefix-determinism means computing `m'` inspects
  only finitely many iterates `f^0(f_∇^m), …, f^{m'}(f_∇^m)` (e.g. constant `k`-step bounded `[external: Kleene]` refinement `ϒ = k`).
  *Relationship to `Δ`*: Every truncator `ϒ` stops at an *exact finite `[external: Kleene]` iterate* `f^{m'}(f_∇^m)` along `(f^n(f_∇^m))_n`
  (and depends on step history/index, whereas binary `Δ : L × L → L` is history-free/`[external: Markovian]` on `(current, next)`),
  while general narrowing `Δ` (`Example 4.18` `Δ_N`) can jump across infinitely many `[external: Kleene]` steps to a reductive element
  `[f]_Δ^k` not equal to any finite `f^n(f_∇^m)`!
- Citation: [PPA Exercise 4.11, p. 278] (book p. 278; PDF p. 295)

### Exercise 4.12 — Greatest lower bound `⊓` is a narrowing operator under `DCC`
- Statement: Show that if `L` satisfies the Descending Chain Condition (`DCC`) then `⊓ : L × L → L` is a narrowing operator. `■`
- Worked resolution `[derived]`: Whenever `l_2 ⊑ l_1`, `l_1 ⊓ l_2 = l_2`, so `l_2 ⊑ (l_1 ⊓ l_2) ⊑ l_1` holds trivially;
  for any descending chain `(l_n)_n`, `Exercise 4.10` makes `(l_n^⊓)_n` (`= (l_n)_n`) a descending chain in `L`, which
  stabilises by `DCC`.
- Citation: [PPA Exercise 4.12, p. 279] (book p. 279; PDF p. 296)

### Exercise 4.13 — Galois connection `(Interval, α_{IS'}, γ_{IS'}, Sign')` via `γ_{IS'}`
- Statement: Define `γ_{IS'} : Sign' → Interval` by `γ_{IS'}(⊤) = [-∞, ∞]`, `γ_{IS'}(-0) = [-∞, 0]`, `γ_{IS'}(0+) = [0, ∞]`,
  `γ_{IS'}(-) = [-∞, -1]`, `γ_{IS'}(0) = [0, 0]`, `γ_{IS'}(+) = [1, ∞]`, `γ_{IS'}(⊥) = ⊥`. Show there exists a Galois
  connection between `Interval` and `Sign'` with `γ_{IS'}` as upper adjoint. `■`
- Worked resolution `[derived]`: Since `Sign'` (`Figure 4.10`) is finite (`7` elements), by `Appendix A Lemma A.4` and
  `Lemma 4.23` it suffices to check `(i)` monotonicity of `γ_{IS'}` (immediate along the `9` covering edges), `(ii)`
  `γ_{IS'}(⊤) = [-∞, ∞] = ⊤_{Interval}`, and `(iii)` binary meet preservation on all `8` unordered incomparable pairs:
  `(-0, 0+) ↦ [-∞, 0] ⊓ [0, ∞] = [0, 0] = γ_{IS'}(0)`; `(-0, +) ↦ [-∞, 0] ⊓ [1, ∞] = ⊥ = γ_{IS'}(⊥)` (by discrete `Z`!);
  `(0+, -) ↦ ⊥`; `(-, 0), (-, +), (0, +) ↦ ⊥`. Thus `α_{IS'}(int) = ⨅{s' | int ⊑ γ_{IS'}(s')}` exists and (since `γ_{IS'}`
  is injective!) `(Interval, α_{IS'}, γ_{IS'}, Sign')` is in fact a **Galois insertion**.
- Citation: [PPA Exercise 4.13, p. 279] (book p. 279; PDF p. 296)

### Exercise 4.14 — Surjectivity of `η`, `ς_η[𝒫(D)] ≅ 𝒫(η[V])`, and `ς_η(D') = D' ∩ η[V]`
- Statement: For `(𝒫(V), α_η, γ_η, 𝒫(D))` induced by `η : V → D`, show `α_η` is surjective iff `η` is surjective,
  conclude Galois insertion iff `η` is surjective, show `ς_η[𝒫(D)] = α_η[𝒫(V)]` is isomorphic to `𝒫(η[V])`, and verify
  `ς_η(V') = V' ∩ η[V]` (`F-U4b-12`: `V'` printed for `D'`). `■`
- Worked resolution `[derived]`: If `η` is surjective, picking `v_d ∈ η^{-1}({d})` gives `α_η({v_d | d ∈ D'}) = D'`;
  conversely, if `α_η(V') = {d}` then `V' ≠ ∅` and every `v ∈ V'` satisfies `η(v) = d`. By `Fact 4.31`, for `D' ⊆ D`:
  `ς_η(D') = α_η(γ_η(D')) = {η(v) | v ∈ V ∧ η(v) ∈ D'} = D' ∩ η[V]`. Thus `ς_η[𝒫(D)] = {D' ∩ η[V] | D' ⊆ D} = 𝒫(η[V])`
  (identity isomorphism `θ_M = id`; note `⨆` is `∪` and `⨅_{𝒫(η[V])} 𝒟 = ς_η(⋂_D 𝒟)` where `⋂ ∅ = η[V] = ς_η(D)`).
- Citation: [PPA Exercise 4.14, p. 279] (book p. 279; PDF p. 296)

### Exercise 4.15 — Sequential composition of extraction Galois connections equals `η_2 ∘ η_1`
- Statement: For `(𝒫(D_i), α_{η_{i+1}}, γ_{η_{i+1}}, 𝒫(D_{i+1}))` (`i = 0, 1`), show `α_{η_2} ∘ α_{η_1} = α_{η_2 ∘ η_1}`
  and `γ_{η_1} ∘ γ_{η_2} = γ_{η_2 ∘ η_1}`. `■`
- Worked resolution `[derived]`: `(α_{η_2} ∘ α_{η_1})(X_0) = {η_2(d_1) | d_1 ∈ {η_1(d_0) | d_0 ∈ X_0}} = {(η_2 ∘ η_1)(d_0) | d_0 ∈ X_0} = α_{η_2 ∘ η_1}(X_0)`,
  and `(γ_{η_1} ∘ γ_{η_2})(X_2) = {d_0 ∈ D_0 | η_1(d_0) ∈ {d_1 ∈ D_1 | η_2(d_1) ∈ X_2}} = {d_0 ∈ D_0 | (η_2 ∘ η_1)(d_0) ∈ X_2} = γ_{η_2 ∘ η_1}(X_2)`.
- Citation: [PPA Exercise 4.15, p. 279] (book p. 279; PDF p. 296)

### Exercise 4.16 — Disjoint-union extraction reformulation of independent attribute powersets
- Statement: Given extraction connections `(𝒫(V_i), α_i, γ_i, 𝒫(D_i))` (`η_i : V_i → D_i`) with `V_1 ∩ V_2 = ∅` and
  `D_1 ∩ D_2 = ∅`, define `η : V_1 ∪ V_2 → D_1 ∪ D_2` piecewise, reformulate `(𝒫(V_1 ∪ V_2), α_η, γ_η, 𝒫(D_1 ∪ D_2))`
  as isomorphic to `(𝒫(V_1) × 𝒫(V_2), α, γ, 𝒫(D_1) × 𝒫(D_2))`, and assess how important both disjointness assumptions are. `■`
- Worked resolution `[derived]`: Define lattice isomorphisms `θ_V : 𝒫(V_1 ∪ V_2) → 𝒫(V_1) × 𝒫(V_2)`, `θ_V(U) = (U ∩ V_1, U ∩ V_2)`
  (`θ_V^{-1}(U_1, U_2) = U_1 ∪ U_2`) and `θ_D(W) = (W ∩ D_1, W ∩ D_2)` (`θ_D^{-1}(W_1, W_2) = W_1 ∪ W_2`). **Both
  disjointness conditions are essential**: `(1)` if `V_1 ∩ V_2 ≠ ∅`, `η` is ill-defined unless `η_1 = η_2` on `V_1 ∩ V_2`,
  and `θ_V^{-1}(U_1, ∅) = U_1` fails `θ_V(U_1) = (U_1, U_1 ∩ V_2) ≠ (U_1, ∅)` (not a bijection!); `(2)` even if
  `V_1 ∩ V_2 = ∅`, if `d ∈ D_1 ∩ D_2` with `η_1(v_1) = d = η_2(v_2)`, then `θ_D` is not a bijection and `(α_η({v_1}))`
  cross-contaminates component 2 via `γ_η({d}) = {v_1, v_2}`! Tagging `({1} × V_1) ∪ ({2} × V_2)` (`Example 4.34`)
  enforces disjointness canonically.
- Citation: [PPA Exercise 4.16, p. 279] (book p. 279; PDF p. 296)

### Exercise 4.17 — Galois insertion preservation for `L_1 × L_2` and `L_1 → L_2`
- Statement: Let `(L_1, α_1, γ_1, M_1)` and `(L_2, α_2, γ_2, M_2)` be Galois insertions. Prove that both the independent
  attribute product `(L_1 × L_2, α, γ, M_1 × M_2)` and the monotone function space `(L_1 → L_2, α, γ, M_1 → M_2)` are
  Galois insertions. `■`
- Worked resolution `[derived]`: Already Galois connections by `§4.4.1`; check `α ∘ γ = id`:
  - *Product*: `α(γ(m_1, m_2)) = (α_1(γ_1(m_1)), α_2(γ_2(m_2))) = (m_1, m_2)`.
  - *Monotone function space*: for `g ∈ M_1 → M_2`, `α(γ(g)) = α_2 ∘ (γ_2 ∘ g ∘ α_1) ∘ γ_1 = (α_2 ∘ γ_2) ∘ g ∘ (α_1 ∘ γ_1) = id_{M_2} ∘ g ∘ id_{M_1} = g`.
- Citation: [PPA Exercise 4.17, p. 280] (book p. 280; PDF p. 297)

### Exercise 4.18 — Relational powerset combinator `(𝒫(V_1 × V_2), α, γ, 𝒫(D_1 × D_2))` preserves Galois insertions
- Statement: Let `(𝒫(V_1), α_1, γ_1, 𝒫(D_1))` and `(𝒫(V_2), α_2, γ_2, 𝒫(D_2))` be Galois insertions. Define
  `α(VV) = ⋃{α_1({v_1}) × α_2({v_2}) | (v_1, v_2) ∈ VV}` and `γ(DD) = {(v_1, v_2) | α_1({v_1}) × α_2({v_2}) ⊆ DD}`,
  and determine whether `(𝒫(V_1 × V_2), α, γ, 𝒫(D_1 × D_2))` is a Galois insertion. `■`
- Worked resolution `[derived]`: **YES — it is ALWAYS a Galois insertion!**
  *Proof*: Fix arbitrary `d_i ∈ D_i` (`i ∈ {1, 2}`). Because `(𝒫(V_i), α_i, γ_i, 𝒫(D_i))` is a Galois insertion, `α_i`
  is **surjective** (`Lemma 4.27`) and **completely additive** (`Lemma 4.22(ii)`). Choose `U_i ⊆ V_i` such that
  `α_i(U_i) = {d_i}`. Since `U_i = ⋃_{v ∈ U_i} {v}`, complete additivity gives `⋃_{v ∈ U_i} α_i({v}) = {d_i}`! In the
  powerset `𝒫(D_i)`, `{d_i} ≠ ∅` cannot be a union of empty sets exclusively, so there MUST exist some `v_{d_i} ∈ U_i`
  with `α_i({v_{d_i}}) ≠ ∅` and `α_i({v_{d_i}}) ⊆ {d_i}`, i.e. **`α_i({v_{d_i}}) = {d_i}`**! Consequently,
  `α({(v_{d_1}, v_{d_2})}) = {d_1} × {d_2} = {(d_1, d_2)}`. For any `DD ⊆ D_1 × D_2`, setting
  `VV = {(v_{d_1}, v_{d_2}) | (d_1, d_2) ∈ DD}` gives `α(VV) = ⋃_{(d_1, d_2) ∈ DD} {(d_1, d_2)} = DD` by complete
  additivity of `α`, proving `α` surjective (`Lemma 4.27`)! *(Note: this relies critically on `𝒫(D_i)` being atomic /
  singletons join-irreducible; on non-powerset lattices it need not hold.)*
- Citation: [PPA Exercise 4.18, p. 280] (book p. 280; PDF p. 297)

### Exercise 4.19 — Direct product `(L, α, γ, M_1 × M_2)` fails to preserve Galois insertions
- Statement: Let `(L, α_1, γ_1, M_1)` and `(L, α_2, γ_2, M_2)` be Galois insertions, define `α(l) = (α_1(l), α_2(l))`
  and `γ(m_1, m_2) = γ_1(m_1) ⊓ γ_2(m_2)`, and determine whether `(L, α, γ, M_1 × M_2)` is a Galois insertion. `■`
- Worked resolution `[derived]`: **NO in general!** Take `L = 𝒫(Z)` with `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))` and
  `(𝒫(Z), α_{parity}, γ_{parity}, 𝒫(Parity))` (both surjective extraction Galois insertions): in the direct product
  `(𝒫(Z), α, γ, 𝒫(Sign) × 𝒫(Parity))`, `γ({0}, {odd}) = {0} ∩ {z | z odd} = ∅ = γ(∅, ∅)`, so `γ` is not injective
  (`α(γ({0}, {odd})) = (∅, ∅) ≠ ({0}, {odd})`). Even taking `M_1 = M_2 = 𝒫(Sign)` with `α_1 = α_2 = α_{sign}` fails:
  `γ({-}, {+}) = Z_{<0} ∩ Z_{>0} = ∅ = γ(∅, ∅)`.
- Citation: [PPA Exercise 4.19, p. 280] (book p. 280; PDF p. 297)

### Exercise 4.20 — Identity and composition laws for `(L_1 → L_1, α, γ, M_1 → M_1)`
- Statement: Let `(L_1, α_1, γ_1, M_1)` be a Galois connection and define `α(f) = α_1 ∘ f ∘ γ_1`, `γ(g) = γ_1 ∘ g ∘ α_1`.
  Determine which of `(1)` `α(λl.l) = λm.m`, `(2)` `γ(λm.m) = λl.l`, `(3)` `α(f_1 ∘ f_2) = α(f_1) ∘ α(f_2)`, and
  `(4)` `γ(g_1 ∘ g_2) = γ(g_1) ∘ γ(g_2)` hold under a Galois connection vs a Galois insertion. `■`
- Worked resolution `[derived]`:
  - **Under an arbitrary Galois connection**: **NONE** of `(1)`–`(4)` necessarily hold! We only have inequalities
    `α(λl.l) = α_1 ∘ γ_1 ⊑ λm.m`, `γ(λm.m) = γ_1 ∘ α_1 ⊒ λl.l`, `α(f_1 ∘ f_2) = α_1 ∘ f_1 ∘ f_2 ∘ γ_1 ⊑ α_1 ∘ f_1 ∘ (γ_1 ∘ α_1) ∘ f_2 ∘ γ_1 = α(f_1) ∘ α(f_2)`, and `γ(g_1 ∘ g_2) = γ_1 ∘ g_1 ∘ g_2 ∘ α_1 ⊒ γ_1 ∘ g_1 ∘ (α_1 ∘ γ_1) ∘ g_2 ∘ α_1 = γ(g_1) ∘ γ(g_2)`.
  - **Under a Galois insertion (`α_1 ∘ γ_1 = id_{M_1}`)**: **`(1)` and `(4)` HOLD**, while **`(2)` and `(3)` STILL FAIL**
    whenever `γ_1 ∘ α_1 ≠ id_{L_1}` (`|L_1| > |M_1|`):
    - `(1)` `α(λl.l) = α_1 ∘ γ_1 = λm.m` (**holds**).
    - `(4)` `γ(g_1) ∘ γ(g_2) = γ_1 ∘ g_1 ∘ (α_1 ∘ γ_1) ∘ g_2 ∘ α_1 = γ_1 ∘ g_1 ∘ g_2 ∘ α_1 = γ(g_1 ∘ g_2)` (**holds**).
    - `(2)` `γ(λm.m) = γ_1 ∘ α_1 ≠ λl.l` on `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))`: `γ_{sign}(α_{sign}({1})) = Z_{>0} ≠ {1}` (**fails**).
    - `(3)` On `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))` with `f_2(X) = {z - 1 | z ∈ X}` and `f_1(X) = {z + 1 | z ∈ X}`,
      `f_1 ∘ f_2 = id`, so `α(f_1 ∘ f_2)({-}) = {-}`, whereas `(α(f_1) ∘ α(f_2))({-}) = α(f_1)({-}) = {-, 0}` (**fails**!).
- Citation: [PPA Exercise 4.20, p. 280] (book p. 280; PDF p. 297)

### Exercise 4.21 — Best descriptions in `𝒫(AB)` (`Example 4.39`) for seven relations on `Z × Z`
- Statement: For `(𝒫(Z × Z), α_{SSR'}, γ_{SSR'}, 𝒫(AB))` (`Example 4.39`), determine `α_{SSR'}` in `𝒫(AB)` for each of:
  `(1)` `{(x, y) | x = y}`, `(2)` `{(x, y) | x = -y}`, `(3)` `{(x, y) | x = y + 1}`, `(4)` `{(x, y) | x = y + 3}`,
  `(5)` `{(x, y) | x ≥ y}`, `(6)` `{(x, y) | x ≥ y + 1}`, `(7)` `{(x, y) | x^2 + y^2 ≤ 100}`. `■`
- Worked resolution `[derived]` (`diff(x, y) = |x| - |y|`):
  1. `x = y`: **`3` atoms** `{(-, -, 0), (0, 0, 0), (+, +, 0)}`.
  2. `x = -y`: **`3` atoms** `{(-, +, 0), (0, 0, 0), (+, -, 0)}`.
  3. `x = y + 1`: **`4` atoms** `{(-, -, -1), (0, -, -1), (+, 0, +1), (+, +, +1)}` (`y ≤ -2 ⇒ (-, -, -1)`; `y = -1 ⇒ (0, -1) ↦ (0, -, -1)`; `y = 0 ⇒ (1, 0) ↦ (+, 0, +1)`; `y ≥ 1 ⇒ (+, +, +1)`; note `x > 0 ∧ y < 0` never occurs since `y + 1 > 0 ⇒ y ≥ 0`!).
  4. `x = y + 3`: **`6` atoms** `{(-, -, <-1), (0, -, <-1), (+, -, -1), (+, -, +1), (+, 0, >+1), (+, +, >+1)}` (`y ≤ -4 ⇒ |y+3| - |y| = -3 ↦ (-, -, <-1)`; `y = -3 ⇒ (0, -3) ↦ (0, -, <-1)`; **`y = -2 ⇒ (1, -2) ↦ (+, -, -1)`**; **`y = -1 ⇒ (2, -1) ↦ (+, -, +1)`** — notice `(+, -, 0)`, `(+, -, <-1)`, and `(+, -, >+1)` NEVER occur!; `y = 0 ⇒ (3, 0) ↦ (+, 0, >+1)`; `y ≥ 1 ⇒ (+, +, >+1)`).
  5. `x ≥ y`: **`16` atoms** `{(-, -, <-1), (-, -, -1), (-, -, 0), (0, -, <-1), (0, -, -1), (0, 0, 0), (+, -, <-1), (+, -, -1), (+, -, 0), (+, -, +1), (+, -, >+1), (+, 0, +1), (+, 0, >+1), (+, +, 0), (+, +, +1), (+, +, >+1)}` (`3 + 2 + 1 + 5 + 2 + 3 = 16` atoms, excluding the `13` atoms where `x < y`).
  6. `x ≥ y + 1` (`x > y`): **`13` atoms** obtained from `(5)` by dropping the `3` equality atoms `(-, -, 0), (0, 0, 0), (+, +, 0)`: `{(-, -, <-1), (-, -, -1), (0, -, <-1), (0, -, -1), (+, -, <-1), (+, -, -1), (+, -, 0), (+, -, +1), (+, -, >+1), (+, 0, +1), (+, 0, >+1), (+, +, +1), (+, +, >+1)}` (`2 + 2 + 5 + 2 + 2 = 13` atoms).
  7. `x^2 + y^2 ≤ 100`: **`29` atoms = all of `AB`**! Every sign/magnitude-difference combination is witnessed inside the radius-10 disk using coordinates `{-3, -2, -1, 0, 1, 2, 3}` (since `3^2 + 3^2 = 18 ≤ 100`), showing `𝒫(AB)` discards pure absolute bounds.
- Citation: [PPA Exercise 4.21, p. 281] (book p. 281; PDF p. 298)

### Exercise 4.22 — Binary monotone-space combinator `((L_1 × L_2) → L_3, α, γ, (M_1 × M_2) → M_3)` and `α(plus)` on `Interval`
- Statement: Given `(L_i, α_i, γ_i, M_i)` (`i = 1, 2, 3`), define `(α, γ)` making `((L_1 × L_2) → L_3, α, γ, (M_1 × M_2) → M_3)`
  a Galois connection, then instantiate all three to `(𝒫(Z), α_{ZI}, γ_{ZI}, Interval)` (`Example 4.19`) to compute
  `α(plus)` for `plus(Z_1, Z_2) = {z_1 + z_2 | z_1 ∈ Z_1 ∧ z_2 ∈ Z_2}`. `■`
- Worked resolution `[derived]`: Combine `§4.4.1` independent attribute (`L_1 × L_2 ↔ M_1 × M_2`) with monotone function
  space:
  ```text
  α(f)(m_1, m_2) = α_3(f(γ_1(m_1), γ_2(m_2)))
  γ(g)(l_1, l_2) = γ_3(g(α_1(l_1), α_2(l_2))).
  ```
  Instantiating on `Interval` with extended endpoint addition (`(-∞) + z = -∞` for `z < ∞`, `∞ + z = ∞` for `z > -∞`,
  `(-∞) + (-∞) = -∞`, `∞ + ∞ = ∞`; note `-∞ + ∞` never occurs between two lower bounds or two upper bounds of non-`⊥`
  intervals because `a_i < ∞` and `b_i > -∞`!):
  ```text
  α(plus)(int_1, int_2) = ⊥                            if int_1 = ⊥ ∨ int_2 = ⊥
  α(plus)([a_1, b_1], [a_2, b_2]) = [a_1 + a_2, b_1 + b_2].
  ```
- Citation: [PPA Exercise 4.22, p. 281] (book p. 281; PDF p. 298)

### Exercise 4.23 — Closed-form `γ`-induced widening `∇_L` on `𝒫(Z)` from `Example 4.15` (`Interval`)
- Statement: Let `L = (𝒫(Z), ⊆)`, `M = Interval` (`Example 4.10`), `(L, α, γ, M)` be the Galois insertion of
  `Example 4.19`, and `∇_M : M × M → M` be `Example 4.15`'s widening `∇_K`. Observe that `l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))`
  defines a widening operator on `L` (`Proposition 4.44(ii)`) and give a direct formula for `∇_L` in the manner of
  `Example 4.15`. `■`
- Worked resolution `[derived]`: Using `inf'(Z')` and `sup'(Z')` (`Example 4.19`, with `inf'(∅) = ∞, sup'(∅) = -∞` matching
  `inf(⊥) = ∞, sup(⊥) = -∞` in `Example 4.15`) and `LB_K, UB_K` from `Example 4.15` (`p. 228`):
  ```text
  Z_1 ∇_L Z_2 = ∅                                                                 if Z_1 = ∅ ∧ Z_2 = ∅
  Z_1 ∇_L Z_2 = { z ∈ Z | LB_K(inf'(Z_1), inf'(Z_2)) ≤ z ≤ UB_K(sup'(Z_1), sup'(Z_2)) }  otherwise
  ```
  (Specifically, for `Z_1 ≠ ∅, Z_2 = ∅`, `LB_K(a_1, ∞) = a_1` and `UB_K(b_1, -∞) = b_1` convex-hulls `Z_1` to
  `{z ∈ Z | inf'(Z_1) ≤ z ≤ sup'(Z_1)}`; for `Z_1 = ∅, Z_2 ≠ ∅`, literal `Example 4.15` gives `{z ∈ Z | LB_K(∞, inf'(Z_2)) ≤ z ≤ UB_K(-∞, sup'(Z_2))}`, or `{z ∈ Z | inf'(Z_2) ≤ z ≤ sup'(Z_2)}` under the `⊥ ∇_K x = x` refinement.)
- Citation: [PPA Exercise 4.23, p. 281] (book p. 281; PDF p. 298)

### Exercise 4.24 — Failure of `γ`-induced narrowing `l_1 Δ_L l_2 = γ(α(l_1) Δ_M α(l_2))`
- Statement: Suppose `(L, α, γ, M)` is a Galois connection or Galois insertion and possibly `M` satisfies `DCC`. Let
  `Δ_M : M × M → M` be a narrowing operator and determine whether `l_1 Δ_L l_2 = γ(α(l_1) Δ_M α(l_2))` defines a
  narrowing operator `Δ_L : L × L → L`. `■`
- Worked resolution `[derived]`: **NO — `Δ_L` fails the narrowing bound `l_2 ⊑ l_1 ⇒ (l_1 Δ_L l_2) ⊑ l_1` whenever
  `γ ∘ α ≠ id_L` (i.e. whenever `∃l_1 ∈ L : l_1 ⊏ γ(α(l_1))`), EVEN IF `(L, α, γ, M)` is a Galois insertion and `M` is
  finite (satisfying `DCC` and `ACC`)!**
  *Proof & counterexample*: Every narrowing operator `Δ_M` satisfies `m Δ_M m = m` (`m ⊑ m Δ_M m ⊑ m`). Pick any
  `l_1 ∈ L \ γ[M]` (so `l_1 ⊏ γ(α(l_1))`) and set `l_2 = l_1` (`l_2 ⊑ l_1`): then
  `l_1 Δ_L l_1 = γ(α(l_1) Δ_M α(l_1)) = γ(α(l_1)) ⋢ l_1`! Concretely, on the Galois insertion
  `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))` (`|𝒫(Sign)| = 8`, finite `DCC`) with `Δ_M = ∩` (`Exercise 4.12`), take
  `l_1 = l_2 = {1, 2}`: `{1, 2} Δ_L {1, 2} = γ_{sign}({+} ∩ {+}) = Z_{>0} ⊈ {1, 2}`! *(Note: clamping with `l_1 ⊓_L ·`
  — `l_1 Δ'_L l_2 = l_1 ⊓_L γ(α(l_1) Δ_M α(l_2))` — restores `l_2 ⊑ (l_1 Δ'_L l_2) ⊑ l_1`, though termination of
  `(l_n^{Δ'_L})_n` is NOT guaranteed unless `L` itself or `↓l_0` has `DCC`!)*
- Citation: [PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299)

### Findings (Exercises)
- F-U4b-11: `Exercise 4.6` (`p. 277`) prints `"Determine which of them that are also widening operators"` (extra `"that"`);
  in the PDF OCR text layer, `Exercise 4.8` (`p. 278`) corrupts `l_0 = f^{27}(⊥)` to `la = P 7 ( .l)`, `Exercise 4.11`
  (`p. 278`) corrupts `ϒ` to `Y` and drops `lfp_∇^ϒ(f) = f^{m'}(f_∇^m)`, and `Exercise 4.24` (`p. 282`) drops
  `l_1 Δ_L l_2 = γ(α(l_1) Δ_M α(l_2))` completely [PPA Exercise 4.6, p. 277] (book p. 277; PDF p. 294);
  [PPA Exercise 4.8, p. 278] (book p. 278; PDF p. 295); [PPA Exercise 4.11, p. 278] (book p. 278; PDF p. 295);
  [PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299).
- F-U4b-12: `Exercise 4.14` (`p. 279`, final line) prints `"verify that ς_η(V') = V' ∩ η[V]"` with concrete-subset
  metavariable `V'` instead of abstract-subset `D' ⊆ D` (`ς_η : 𝒫(D) → 𝒫(D)` satisfies `ς_η(D') = D' ∩ η[V]`, as
  printed on `p. 246`), while `Exercise 4.16` (`p. 279`) reuses `α_η, γ_η` across both `𝒫(V_1 ∪ V_2)` and
  `𝒫(V_1) × 𝒫(V_2)` [PPA §4.3.2, p. 246] (book p. 246; PDF p. 263); [PPA Exercise 4.14, p. 279] (book p. 279; PDF p. 296);
  [PPA Exercise 4.16, p. 279] (book p. 279; PDF p. 296).

### Projections (Exercises)
- software_engineering: Use `Exercise 4.9`'s bounded-box delayed widening (`⊔` inside finite `[A, B]`, `∇_K` outside)
  to unroll small fixed-bound loops without losing precision, and use `Exercise 4.11`'s `k`-step truncator `ϒ` (`k = 1..2`
  exact `f` passes after `f_∇^m`) when domain narrowing `Δ` is unavailable or non-terminating.
- cybersecurity: `Exercise 4.21` exposes the exact boundary of finite relational predicate domains (`𝒫(AB)`): linear
  offset checks `x ≥ y + 1` (`13` atoms) and `x = y + 3` (`6` atoms) stay sharp for relative array-bounds proofs,
  whereas quadratic/norm bounds `x^2 + y^2 ≤ 100` collapse to `⊤ = AB` (`29` atoms), requiring intervals or
  `[external: ellipsoidal domains]`.
- cs_theory: `Figure 4.10` and `Exercise 4.13` prove that distributivity is **not** required for a Galois insertion
  (`Sign'` contains `[external: N_5]` yet embeds into `Interval`), whereas `Exercise 4.20` proves that Galois abstraction
  `α(f) = α_1 ∘ f ∘ γ_1` is a `[external: lax functor]` (`α(f_1 ∘ f_2) ⊑ α(f_1) ∘ α(f_2)`) rather than a strict
  composition homomorphism even on Galois insertions.
- debugging: When warm-starting incremental fixed-point solvers from a cached previous run `l_0` instead of `⊥`
  (`Exercise 4.8`), verify `l_0 ⊑ f(l_0)` (`l_0 ∈ Ext(f)`); arbitrary stale caches `l_0 ∉ Ext(f)` preserve reductive
  (`Red(f)`) soundness *if* iteration stops (`Fact 4.14`) but can break widening termination (`Proposition 4.13`)!

## Gotcha Ledger

- G-U4b-01: Book p. 246 (`PDF p. 263`) carries the closing §4.3.2 results (`Fact 4.31` `ς(m) = α(γ(m))` and `α[L] = ς[M]`, `Proposition 4.29` proof where `⨆_{ς[M]} = ⨆_M` while `⨅_{ς[M]} = ς ∘ ⨅_M`, `ς_η(D') = D' ∩ η[V]`, GC isomorphism `(θ_L, θ_M)`, and `Example 4.32`) above the §4.4 heading [PPA Fact 4.31, p. 246] (book p. 246; PDF p. 263); [PPA §4.4, p. 246] (book p. 246; PDF p. 263).
- G-U4b-02: Sequential composition of `(L_0, α_1, γ_1, L_1)` and `(L_1, α_2, γ_2, L_2)` reverses composition order between `α` and `γ` — `(L_0, α_2 ∘ α_1, γ_1 ∘ γ_2, L_2)` — while preserving Galois insertions (`γ_{η_2 ∘ η_1} = γ_{η_1} ∘ γ_{η_2}`, `Exercise 4.15`) [PPA §4.4, p. 247] (book p. 247; PDF p. 264); [PPA Exercise 4.15, p. 279] (book p. 279; PDF p. 296).
- G-U4b-03: `Example 4.33` defines `diff(z_1, z_2) = |z_1| - |z_2|` on *absolute magnitudes* (`diff(5, -7) = -2`), whereas `Mini Project 4.1` feeds signed length difference `length(x) - length(y)` into the same `Range = {<-1, -1, 0, +1, >+1}` set [PPA Example 4.33, p. 247] (book p. 247; PDF p. 264); [PPA Mini Project 4.1, p. 274] (book p. 274; PDF p. 291).
- G-U4b-04: `𝒫(V_1) × 𝒫(V_2)` is not a powerset and cannot be given directly by an extraction function without disjoint-union tagging `({1} × V_1) ∪ ({2} × V_2)` (`Example 4.34`); omitting disjointness of either `V_1, V_2` or `D_1, D_2` breaks the `Exercise 4.16` isomorphism [PPA Example 4.34, p. 250] (book p. 250; PDF p. 267); [PPA Exercise 4.16, p. 279] (book p. 279; PDF p. 296).
- G-U4b-05: Distinguish §4.4.1's *separate-component* combinators — independent attribute (`L_1 × L_2 ↔ M_1 × M_2`, losing `z_2 = -z_1` in `Example 4.34`) and relational tensor product (`𝒫(V_1 × V_2) ↔ 𝒫(D_1 × D_2)`, keeping `{(-, +), (0, 0), (+, -)}` in `Example 4.35`) — from §4.4.2's *same-carrier* combinators — direct product (`γ(m_1, m_2) = γ_1(m_1) ⊓ γ_2(m_2)`, `Example 4.37`) and direct tensor product (`𝒫(V) ↔ 𝒫(D_1 × D_2)`, `Example 4.38`) [PPA §4.4.1, pp. 249–252] (book p. 249; PDF p. 266) (book p. 252; PDF p. 269); [PPA §4.4.2, pp. 254–256] (book p. 254; PDF p. 271) (book p. 256; PDF p. 273).
- G-U4b-06: Galois insertions are preserved by sequential composition (`p. 247`), independent attribute (`Exercise 4.17`), total/monotone function spaces (`p. 252`, `Exercise 4.17`), and the *powerset relational method* (`Exercise 4.18`, via join-irreducible singletons), but **fail** for direct product (`Exercise 4.19`) and direct tensor product (`Example 4.38`) until reduced by `ς` [PPA Example 4.38, p. 256] (book p. 256; PDF p. 273); [PPA Exercise 4.17, p. 280] (book p. 280; PDF p. 297); [PPA Exercise 4.18, p. 280] (book p. 280; PDF p. 297); [PPA Exercise 4.19, p. 280] (book p. 280; PDF p. 297).
- G-U4b-07: In `Example 4.39`, `ς_{SSR'}` removes the `16` uninhabited zero-sign triples from `Sign × Sign × Range` (`45` triples) to form the `29`-atom Array Bound lattice `AB` (`45` bits → `29` bits), capturing `0 ≤ idx < len` (`[external: CWE-787]`) while still abstracting `x^2 + y^2 ≤ 100` to `AB = ⊤` (`Exercise 4.21`) [PPA Example 4.39, p. 257] (book p. 257; PDF p. 274); [PPA Exercise 4.21, p. 281] (book p. 281; PDF p. 298).
- G-U4b-08: In `Exercise 4.21`, `{(x, y) | x = y + 3}` maps to only **`6` atoms** `{(-, -, <-1), (0, -, <-1), (+, -, -1), (+, -, +1), (+, 0, >+1), (+, +, >+1)}` in `AB` because `x > 0 ∧ y < 0` with `x = y + 3` occurs only at `(1, -2)` and `(2, -1)`, excluding `(+, -, 0)`, `(+, -, <-1)`, and `(+, -, >+1)` `[derived]` [PPA Exercise 4.21, p. 281] (book p. 281; PDF p. 298).
- G-U4b-09: Applying `[external: Granger-style pairwise reduction]` `ρ_{12}` *after* component-wise widening `(m_1 ∇_1 m'_1, m_2 ∇_2 m'_2)` in a reduced product (`§4.4.2`) can pull widened `∞` bounds back to finite constants and cause infinite solver oscillation `[derived]` [PPA §4.4.2, p. 256] (book p. 256; PDF p. 273).
- G-U4b-10: In the monotone function space `(L_1 → L_2, α, γ, M_1 → M_2)`, `α(f) = α_2 ∘ f ∘ γ_1` and `γ(g) = γ_2 ∘ g ∘ α_1` are contravariant in the input slot; even for a Galois insertion (`L_1 = L_2`, `M_1 = M_2`), `α(λl.l) = λm.m` and `γ(g_1 ∘ g_2) = γ(g_1) ∘ γ(g_2)` hold while `γ(λm.m) = λl.l` and `α(f_1 ∘ f_2) = α(f_1) ∘ α(f_2)` fail in general (`Exercise 4.20`) [PPA §4.4.1, p. 253] (book p. 253; PDF p. 270); [PPA Exercise 4.20, p. 280] (book p. 280; PDF p. 297).
- G-U4b-11: By `Lemma 4.41`, `((α_1 ∘ β_1) ↠ (α_2 ∘ β_2))(↝) = α_2 ∘ ((β_1 ↠ β_2)(↝)) ∘ γ_1`, so induced `α_2 ∘ f_p ∘ γ_1` preserves optimality (`p. 261`, `Example 4.40`, `Exercise 4.5`), while soundness of an implementation `g_p` requires *upper* approximation `α_2 ∘ f_p ∘ γ_1 ⊑ g_p` [PPA Lemma 4.41, p. 260] (book p. 260; PDF p. 277); [PPA §4.5.1, p. 261] (book p. 261; PDF p. 278).
- G-U4b-12: `Lemma 4.42` (`α ∘ f ∘ γ ⊑ g`) guarantees `g(m) ⊑ m ⇒ f(γ(m)) ⊑ γ(m)`, `lfp(f) ⊑ γ(lfp(g))`, and `α(lfp(f)) ⊑ lfp(g)` via complete multiplicativity of `γ`, **not** equality `α(lfp(f)) = lfp(g)` [PPA Lemma 4.42, pp. 261–262] (book p. 261; PDF p. 278) (book p. 262; PDF p. 279).
- G-U4b-13: In generalised Monotone Frameworks (`§4.5.2`), `ȷ ⊒ α(ι)` and `g_ℓ ⊒ α ∘ f_ℓ ∘ γ` suffice for `(B_∘, B_•) ⊨ B^⊒ ⇒ (γ ∘ B_∘, γ ∘ B_•) ⊨ A^⊒`, whereas transporting semantic correctness `(4.11) ⇒ (4.12)` requires strengthened extremal equality **`γ(ȷ) = ι`** (`p. 264`) [PPA §4.5.2, pp. 263–264] (book p. 263; PDF p. 280) (book p. 264; PDF p. 281).
- G-U4b-14: Node-attached concrete Sets of States `SS` (`Lemma 4.43`) is sound but **not optimal** (`Remark.` `p. 266`) because `f_ℓ^{SS}([b]^ℓ) = Σ` ignores test outcomes; exact collecting semantics and branch-sensitive guard refinement require *edge-attached* transfers (`Exercise 2.11`, `Exercise 4.5`) [PPA Lemma 4.43, p. 265] (book p. 265; PDF p. 282); [PPA §4.5.2, p. 266] (book p. 266; PDF p. 283).
- G-U4b-15: In `§4.5.2`'s Constant Propagation proof (`pp. 266–267`), `Statê_CP = ((Var → Z^⊤)_⊥, ⊑)` uses unstarred `Var`, and `⨆{σ[x ↦ 𝒜⟦a⟧σ] | σ ⊑ σ̂} ⊑ σ̂[x ↦ ⨆{𝒜⟦a⟧σ | σ ⊑ σ̂}]` assumes `σ̂ ≠ ⊥` (`σ̂ = ⊥` must short-circuit via `γ_{CP}(⊥) = ∅` `[derived]`) [PPA §4.5.2, pp. 266–267] (book p. 266; PDF p. 283) (book p. 267; PDF p. 284).
- G-U4b-16: `Proposition 4.44` makes `l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))` a widening operator under `(i)` `ACC` on `M` for *any* Galois connection (requiring `n_0 ≥ 1` since `l_0^{∇_L} = l_0` may lie outside `γ[M]`), whereas `(ii)` infinite `M` with widening `∇_M` **requires `(L, α, γ, M)` to be a Galois insertion** so `(4.13)` `(α(l_n))^{∇_M} = α(l_n^{∇_L})` holds (`Exercise 4.23`) [PPA Proposition 4.44, p. 268] (book p. 268; PDF p. 285); [PPA Exercise 4.23, p. 281] (book p. 281; PDF p. 298).
- G-U4b-17: `Lemma 4.45`'s lockstep identity `lfp_{∇_L}(f) = γ(lfp_{∇_M}(α ∘ f ∘ γ))` (`(4.14)`–`(4.15)`) requires **both** a Galois insertion **and** `γ(⊥_M) = ⊥_L` (`n = 0` base case); note the printed proof typo `g(g_{∇_L}^n) ⊑ g_{∇_M}^n` on line 4 of `"⇒"` (`p. 269`) for `g(g_{∇_M}^n) ⊑ g_{∇_M}^n` [PPA Lemma 4.45, p. 269] (book p. 269; PDF p. 286).
- G-U4b-18: Unlike `γ`-induced widening, `l_1 Δ_L l_2 = γ(α(l_1) Δ_M α(l_2))` (`Exercise 4.24`) **fails** to define a narrowing operator whenever `γ ∘ α ≠ id_L` (even on a Galois insertion with finite `M`), because `l_1 Δ_L l_1 = γ(α(l_1)) ⋢ l_1` for `l_1 ∉ γ[M]` [PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299).
- G-U4b-19: On upper closure operators `ρ : L → L` (`Concluding Remarks` `pp. 270–271`), `ρ_1 ⊑ ρ_2 ⇔ ρ_2[L] ⊆ ρ_1[L]` (`ρ_2` coarser), and binary **meet** `ρ_1 ⊓ ρ_2` yields the reduced product (`p. 271` mis-cites `Section 4.3.` instead of `§4.4.2` and writes `ρ_2(L)` with round parens) [PPA Chapter 4 Concluding Remarks, pp. 270–271] (book p. 270; PDF p. 287) (book p. 271; PDF p. 288).
- G-U4b-20: Abstract Interpretation (`⊤` uninformative, `lfp`) is lattice-dual (`⊑^d`) to classical Data Flow Analysis (`⊥` uninformative, `gfp`), whereas Abstract Interpretation and Denotational Semantics (`⊥` uninformative, **also `lfp`**) are **NOT duals** (`p. 273`) [PPA Chapter 4 Concluding Remarks, p. 273] (book p. 273; PDF p. 290).
- G-U4b-21: Soundly checking transformation enabling conditions `l_ℓ ⊑ l_Ξ` (`Concluding Remarks` `p. 273`) requires approximating point properties `l_ℓ` **upward** (`l_ℓ ⊑ l'_ℓ`, Galois connection) and transformation guards `l_Ξ` **downward** (`l'_Ξ ⊑ l_Ξ`, dual Galois connection) [PPA Chapter 4 Concluding Remarks, p. 273] (book p. 273; PDF p. 290).
- G-U4b-22: `Mini Project 4.1` (`p. 274`) defines asymmetric list suffix (`|LR| = 16`) before glossing `S` symmetrically (`|LR| = 20`, with `([], []) ↦ ({S}, 0)`); `Mini Project 4.2` (`pp. 274–275`) yields a non-insertion `(𝒫(State × Heap), α_{SA}, γ_{SA}, 𝒫(SG))` with non-optimal `f_ℓ^{SA}`; `Mini Project 4.3` (`p. 275`) misprints `Example 4.40` for `Example 4.4` and `d̂` for `δ̂` [PPA Mini Project 4.1, p. 274] (book p. 274; PDF p. 291); [PPA Mini Project 4.2, p. 275] (book p. 275; PDF p. 292); [PPA Mini Project 4.3, p. 275] (book p. 275; PDF p. 292).
- G-U4b-23: `(4.4)` alone gives `v R (⨆L')` for non-empty `L' ≠ ∅`, while `v R ⊥` (`L' = ∅`) routinely fails (`Exercise 4.2`); `Figure 4.10`'s 7-element `Sign'` omits `{-+}` (`[external: N_5]` non-distributive) to restore `γ_{IS'}` complete multiplicativity (`Exercise 4.13`); and `Exercise 4.14` misprints `ς_η(V')` for `ς_η(D')` [PPA Figure 4.10, p. 276] (book p. 276; PDF p. 293); [PPA Exercise 4.2, p. 276] (book p. 276; PDF p. 293); [PPA Exercise 4.13, p. 279] (book p. 279; PDF p. 296); [PPA Exercise 4.14, p. 279] (book p. 279; PDF p. 296).
- G-U4b-24: Under `ACC` (`Exercise 4.7`) `⊔` is a widening operator and `Exercise 4.6(5)` / `Exercise 4.9` require `ACC` on `↓l'` / finite `int'`; changing `f_∇^0 = l_0` (`Exercise 4.8`) preserves `Fact 4.14` for arbitrary `l_0` but preserves `Proposition 4.13` termination **only for `l_0 ∈ Ext(f)`**; under `DCC` (`Exercise 4.12`) `⊓` is a narrowing operator, while truncators `ϒ` (`Exercise 4.11`) always stop at finite `[external: Kleene]` iterates `f^{m'}(f_∇^m)` [PPA Exercise 4.6, p. 277] (book p. 277; PDF p. 294); [PPA Exercise 4.8, pp. 277–278] (book p. 277; PDF p. 294) (book p. 278; PDF p. 295); [PPA Exercise 4.11, p. 278] (book p. 278; PDF p. 295); [PPA Exercise 4.12, p. 279] (book p. 279; PDF p. 296).
