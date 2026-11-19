<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 3b (Chapter 3 §§3.5-3.6, Concluding Remarks, Mini Projects 3.1-3.4, and Exercises 3.1-3.17). -->

# RAW_SHARD_03b — Chapter 3 Combined CFA+DFA, Context-Sensitive k-CFA & CPA, and End Matter (Unit 3b)

Source: *Principles of Program Analysis* (Nielson, Nielson, Hankin), corrected 2nd printing, 2005.
Scope: §3.5 Adding Data Flow Analysis (§3.5.1–§3.5.2), §3.6 Adding Context Information (§3.6.1–§3.6.2),
Chapter 3 Concluding Remarks, Mini Projects 3.1–3.4, and Exercises 3.1–3.17, spanning book pages 182–209 /
PDF pages 200–227, beginning at the §3.5 heading mid-page on book p. 182 below Corollary 3.25's open-system
remarks and ending at the black square closing Exercise 3.17 on book p. 209. Chapter 3 opening and §§3.1–3.4
(Tables 3.1–3.7, Figures 3.1–3.5, statements `3.1`–`3.25`, and displays `(3.1)`–`(3.7)`) belong to Unit 3a
(`corpus/shards/RAW_SHARD_03a_0cfa.md`).

Coordinates: PDF page = book page + 18 throughout Chapter 3 (blank versos p. 140 before Chapter 3 and p. 210
after Chapter 3 are absent from the PDF). Division starts in Unit 3b: §3.5 and §3.5.1 on p. 182 (§3.5.2 on
p. 185), §3.6 on p. 189 (§3.6.1 on p. 191, §3.6.2 on p. 196), Concluding Remarks on p. 198, Mini Projects on
p. 202, and Exercises on p. 205 through p. 209 [PPA §3.5, p. 182] (book p. 182; PDF p. 200);
[PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227).

Conventions:

- Every source reference pairs a strict inline locator token with its book/PDF coordinate companion, for
  example [PPA §3.5, p. 182] (book p. 182; PDF p. 200), [PPA Table 3.8, p. 184] (book p. 184; PDF p. 202), or
  [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219).
- Book-numbered items preserve their exact printed kind word and number: shared-sequence statements
  `Example 3.26`–`Example 3.34` (9 Examples; there are no Lemmas, Theorems, Propositions, Corollaries, or
  Facts in Unit 3b, and no `3.35`), Tables `3.8`–`3.10`, Figure `3.6`, `Mini Project 3.1`–`Mini Project 3.4`
  (4 mini projects), `Exercise 3.1`–`Exercise 3.17` (17 exercises, all unstarred; there are no `3.18`–`3.21`
  in the printed book), and numbered equation displays `(3.8)`–`(3.9)`. Unnumbered definitions, specifications,
  and remarks carry non-book identifiers `[U3b:<section>-<letter>]`.
- Every formula, acceptability clause, table, figure, datatype, and exercise was transcribed directly from
  rendered page images (PDF pages 200–227) and cross-checked against `corpus/pdf_page_map.json` rather than
  the OCR text layer, which drops the `[op]` clause body of Table 3.9, both displays in Example 3.28,
  both displays `(3.8)` and `(3.9)` in Exercise 3.4, grammar displays in Mini Projects 3.2 and 3.4, and
  wide hats, primes, ceiling brackets, and subscripts throughout.
- Terms absent from the book carry `[external]`. Deductions, worked counterexamples, and complexity
  refinements not printed in the text carry `[derived]`. Source misprints and internal tensions are
  transcribed verbatim as printed and logged under `Findings` (`F-U3b-NN`).
- Notation: `e ∈ Exp` labelled expressions (`t^ℓ`); `t ∈ Term` unlabelled terms; `f, x ∈ Var` variables;
  `c ∈ Const` constants; `op ∈ Op` binary operators; `ℓ ∈ Lab` labels; `FV` free variables; `Data` abstract
  data properties (`Data_sign = {tt, ff, -, 0, +}`) with `d_c ∈ Data`, `d_op : Data × Data → 𝒫(Data)`,
  `Val̂_d = 𝒫(Term ∪ Data)`, `op̂ : Val̂_d × Val̂_d → Val̂_d`, and `(Ĉ, ρ̂) ⊨_d e` (Table 3.8); `(L, ℱ)` monotone
  structure with instance `(L, ℱ, ι., f.)` (`ι_c ∈ L`, `f_op ∈ ℱ`), `Datâ = L`, `DEnv̂ = Var → Datâ` (`δ̂`),
  `DCachê = Lab → Datâ` (`D̂`), `(Ĉ, D̂, ρ̂, δ̂) ⊨_D e` (Table 3.9), and staged `⊨'_D`; `δ ∈ Δ` context
  information (`Lab^{≤k}` in uniform `k`-CFA, `Term^m` in CPA), empty context `Λ`, left-truncated call string
  `⌈δ, ℓ⌉_k`, `ce ∈ CEnv = Var → Δ` context environments, `ce | X` restriction, `(Ĉ, ρ̂) ⊨_δ^{ce} e` uniform
  `k`-CFA acceptability (Table 3.10); `fn x₁, ···, x_m => e_b` and `e₀(e₁, ···, e_m)` `m`-ary forms with
  `(Ĉ, ρ̂) ⊨_{CPA}^δ e`; `S₁ ⊆ S₂`, `C(S₁, ···, S_n)`, `C^{-i}(S)`, `¬S` general set constraints;
  `R̂ ∈ Reach = Lab → 𝒫({on})` and `(Ĉ, ρ̂, R̂) ⊨'_s e` (Mini Project 3.1); `Constr` algebraic constructors
  (Mini Project 3.2); `π ∈ Pnt`, `me : Var → Pnt`, `Ŝ_∘, Ŝ_• : Lab → (Pnt → Val̂)`, and
  `(Ĉ, ρ̂, Ŝ_∘, Ŝ_•) ⊨_{me} e` (Mini Project 3.4); `𝒞_⋆^=⟦e_⋆⟧` equational constraints (Exercise 3.13);
  `■` end-of-item marker as printed.

## Closed Inventory — Book Pages 182–209 (PDF Pages 200–227)

| Kind | Count | Identifiers |
| :--- | ---: | :--- |
| Sections / Subsections / End-Matter Divisions | 9 | `§3.5` (`§3.5.1`–`§3.5.2`, pp. 182–189), `§3.6` (`§3.6.1`–`§3.6.2`, pp. 189–198), `Concluding Remarks` (pp. 198–202), `Mini Projects` (pp. 202–205), `Exercises` (pp. 205–209) |
| Tables | 3 | `Table 3.8` (p. 184), `Table 3.9` (p. 188), `Table 3.10` (p. 192); continues `Tables 3.1–3.7` (`10` total in Chapter 3) |
| Figures | 1 | `Figure 3.6` (p. 185); continues `Figures 3.1–3.5` (`6` total in Chapter 3) |
| Shared-Sequence Statements (`3.26`–`3.34`) | 9 | `Example 3.26`–`Example 3.34` (`3.26`–`3.31` in `§3.5`, `3.32`–`3.34` in `§3.6`; continues `3.1`–`3.25` for `34` total in Chapter 3) |
| Numbered Displays | 2 | `(3.8)` and `(3.9)` inside `Exercise 3.4` (p. 206); continues `(3.1)`–`(3.7)` (`9` total in Chapter 3) |
| Mini Projects | 4 | `Mini Project 3.1` (p. 202), `Mini Project 3.2` (p. 203), `Mini Project 3.3` (p. 204), `Mini Project 3.4` (pp. 204–205) |
| Exercises | 17 | `Exercise 3.1`–`Exercise 3.17` (pp. 205–209; `0` starred) |
| Unnumbered `[U3b:...]` Units | 21 | `3.5-a` (1), `3.5.1-a..c` (3), `3.5.2-a..d` (4), `3.6-a` (1), `3.6.1-a..d` (4), `3.6.2-a..d` (4), `CR-a..c` (3), `EX-ocr` (1) |

---

## 3.5 Adding Data Flow Analysis

Context: extending Chapter 3's Control Flow Analysis to track non-closure data properties, first as powersets
`𝒫(Data)` (§3.5.1) and then over arbitrary complete lattices `L` (§3.5.2)
[PPA §3.5, p. 182] (book p. 182; PDF p. 200).

### [U3b:3.5-a] Scope and style of Section 3.5 (unnumbered remark)
- Statement: recalling §3.1's remark that `Val̂` can be enlarged beyond function abstractions to incorporate
  Data Flow Analysis, §3.5 develops two abstract acceptability specifications (in the declarative style of
  §3.1, deferring syntax-directed formulations to the exercises, specifically
  [PPA Exercise 3.14, p. 208] (book p. 208; PDF p. 226)):
  1. §3.5.1: when the Data Flow Analysis component is a *powerset*; and
  2. §3.5.2: when the Data Flow Analysis component is generalised to a *complete lattice*.
- Citation: [PPA §3.5, p. 182] (book p. 182; PDF p. 200)

## 3.5.1 Abstract Values as Powersets

Context: adjoining a token set `Data` to `Val̂`, lifting operators pointwise (`Example 3.26`), coupling DFA into
CFA branch selection in `Table 3.8` (`Example 3.27`, `Figure 3.6`), and noting non-projection to `Table 3.1`
[PPA §3.5.1, p. 182] (book p. 182; PDF p. 200).

### [U3b:3.5.1-a] Powerset abstract domain `Val̂_d`, constant properties `d_c`, and lifted operators `op̂`
- Statement: let `Data` be a set of *abstract data values* (abstract properties of booleans and integers) and
  define:
  ```text
  v̂ ∈ Val̂_d = 𝒫(Term ∪ Data)      abstract values
  ```
  (with `ρ̂ : Var → Val̂_d` and `Ĉ : Lab → Val̂_d` updated implicitly here and written explicitly at the opening
  of §3.5.2 on pp. 185–186; finding F-U3b-01).
  - Each constant `c ∈ Const` has an associated abstract property `d_c ∈ Data`.
  - Each binary operator `op ∈ Op` has a total abstract operation `op̂ : Val̂_d × Val̂_d → Val̂_d`, typically
    induced pointwise from a table `d_op : Data × Data → 𝒫(Data)`:
    ```text
    v̂₁ op̂ v̂₂ = ⋃{d_op(d₁, d₂) | d₁ ∈ v̂₁ ∩ Data, d₂ ∈ v̂₂ ∩ Data}
    ```
- Side conditions: `[derived]` intersecting operands with `Data` discards any `Term` elements in `v̂₁` or `v̂₂`
  (contributing `∅` to the union).
- Citation: [PPA §3.5.1, p. 182] (book p. 182; PDF p. 200); [PPA §3.5.1, p. 183] (book p. 183; PDF p. 201)

### Example 3.26 — Detection of Signs domain `Data_sign` and abstract addition `d_+`
- Statement: for *Detection of Signs Analysis*, set `Data_sign = {tt, ff, -, 0, +}` (`tt, ff` for truth values;
  `-, 0, +` for negative integers, zero, and positive integers), with `d_true = tt`, `d_7 = +`, etc., and base
  `+̂` on `d_+`:

| `d_+` | `tt` | `ff` | `-` | `0` | `+` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `tt` | `∅` | `∅` | `∅` | `∅` | `∅` |
| `ff` | `∅` | `∅` | `∅` | `∅` | `∅` |
| `-` | `∅` | `∅` | `{-}` | `{-}` | `{-, 0, +}` |
| `0` | `∅` | `∅` | `{-}` | `{0}` | `{+}` |
| `+` | `∅` | `∅` | `{-, 0, +}` | `{+}` | `{+}` |

  and similarly for the remaining operators. `■`
- Citation: [PPA Example 3.26, p. 183] (book p. 183; PDF p. 201)

### [U3b:3.5.1-b] Coupled acceptability `(Ĉ, ρ̂) ⊨_d e` and DFA-to-CFA branch pruning
- Statement: the acceptability relation `(Ĉ, ρ̂) ⊨_d e` (understood coinductively as `gfp`, matching §3.1.2
  `[derived]`) is specified in Table 3.8:
  - `[con]` records `{d_c} ⊆ Ĉ(ℓ)`, and `[op]` enforces `Ĉ(ℓ₁) op̂ Ĉ(ℓ₂) ⊆ Ĉ(ℓ)`.
  - `[if]` demands acceptability and result flow of the `then`-branch *only* when `d_true ∈ Ĉ(ℓ₀)`, and of the
    `else`-branch *only* when `d_false ∈ Ĉ(ℓ₀)`. Thus **the Data Flow Analysis component directly sharpens the
    Control Flow Analysis component** by suppressing closures inside untaken branches.
  - Following [PPA Exercise 3.3, p. 206] (book p. 206; PDF p. 224), demand/evaluation-order guards can be
    added to other clauses ([PPA Exercise 3.14, p. 208] (book p. 208; PDF p. 226)), increasing flow
    sensitivity.
- Citation: [PPA §3.5.1, p. 183] (book p. 183; PDF p. 201)

### Table 3.8 — Abstract values as powersets
- Content:
  ```text
  [con]  (Ĉ, ρ̂) ⊨_d c^ℓ iff {d_c} ⊆ Ĉ(ℓ)

  [var]  (Ĉ, ρ̂) ⊨_d x^ℓ iff ρ̂(x) ⊆ Ĉ(ℓ)

  [fn]   (Ĉ, ρ̂) ⊨_d (fn x => e₀)^ℓ iff {fn x => e₀} ⊆ Ĉ(ℓ)

  [fun]  (Ĉ, ρ̂) ⊨_d (fun f x => e₀)^ℓ iff {fun f x => e₀} ⊆ Ĉ(ℓ)

  [app]  (Ĉ, ρ̂) ⊨_d (t₁^{ℓ₁} t₂^{ℓ₂})^ℓ
           iff  (Ĉ, ρ̂) ⊨_d t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_d t₂^{ℓ₂}  ∧
                (∀(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) :
                   (Ĉ, ρ̂) ⊨_d t₀^{ℓ₀}  ∧
                   Ĉ(ℓ₂) ⊆ ρ̂(x)  ∧  Ĉ(ℓ₀) ⊆ Ĉ(ℓ))  ∧
                (∀(fun f x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) :
                   (Ĉ, ρ̂) ⊨_d t₀^{ℓ₀}  ∧
                   Ĉ(ℓ₂) ⊆ ρ̂(x)  ∧  Ĉ(ℓ₀) ⊆ Ĉ(ℓ)  ∧
                   {fun f x => t₀^{ℓ₀}} ⊆ ρ̂(f))

  [if]   (Ĉ, ρ̂) ⊨_d (if t₀^{ℓ₀} then t₁^{ℓ₁} else t₂^{ℓ₂})^ℓ
           iff  (Ĉ, ρ̂) ⊨_d t₀^{ℓ₀}  ∧
                (d_true  ∈ Ĉ(ℓ₀) ⇒ ((Ĉ, ρ̂) ⊨_d t₁^{ℓ₁} ∧ Ĉ(ℓ₁) ⊆ Ĉ(ℓ)))  ∧
                (d_false ∈ Ĉ(ℓ₀) ⇒ ((Ĉ, ρ̂) ⊨_d t₂^{ℓ₂} ∧ Ĉ(ℓ₂) ⊆ Ĉ(ℓ)))

  [let]  (Ĉ, ρ̂) ⊨_d (let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ
           iff  (Ĉ, ρ̂) ⊨_d t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_d t₂^{ℓ₂}  ∧
                Ĉ(ℓ₁) ⊆ ρ̂(x)  ∧  Ĉ(ℓ₂) ⊆ Ĉ(ℓ)

  [op]   (Ĉ, ρ̂) ⊨_d (t₁^{ℓ₁} op t₂^{ℓ₂})^ℓ
           iff  (Ĉ, ρ̂) ⊨_d t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_d t₂^{ℓ₂}  ∧
                Ĉ(ℓ₁) op̂ Ĉ(ℓ₂) ⊆ Ĉ(ℓ)
  ```
- Citation: [PPA Table 3.8, p. 184] (book p. 184; PDF p. 202)

### Example 3.27 — Dead-branch closure pruning via Detection of Signs
- Statement: consider:
  ```text
  (let f = (fn x => (if (x^1 > 0^2)^3 then (fn y => y^4)^5
                                       else (fn z => 25^6)^7)^8)^9
   in ((f^{10} 3^{11})^{12} 0^{13})^{14})^{15}
  ```
  - Pure 0-CFA (§3.1, column 1 of Figure 3.6) cannot see that `x` is bound to `3 > 0`, concluding that call
    result `12` may be either `fn y => y^4` or `fn z => 25^6`.
  - Combined `⊨_d` with Detection of Signs (§3.5.1, column 2 of Figure 3.6) computes `Ĉ(1) = {+}`,
    `Ĉ(2) = {0}`, `Ĉ(3) = {tt}`; since `ff ∉ Ĉ(3)`, `(fn z => 25^6)^7` is never analysed, `Ĉ(8) = Ĉ(12) = {fn y => y^4}`,
    and the overall expression (`14`, `15`) evaluates to `{0}`. `■`
- Citation: [PPA Example 3.27, p. 183] (book p. 183; PDF p. 201); [PPA Example 3.27, p. 184] (book p. 184; PDF p. 202)

### Figure 3.6 — Control Flow and Data Flow Analysis for example program
- Content (with `fn x => (···)^8` abbreviating `fn x => (if (x^1 > 0^2)^3 then (fn y => y^4)^5 else (fn z => 25^6)^7)^8`):

| Label / Var | Section 3.1 `(Ĉ, ρ̂)` | Subsection 3.5.1 `(Ĉ, ρ̂)` | Subsection 3.5.2 `(Ĉ, ρ̂)` | Subsection 3.5.2 `(D̂, δ̂)` |
| :--- | :--- | :--- | :--- | :--- |
| `1` | `∅` | `{+}` | `∅` | `{+}` |
| `2` | `∅` | `{0}` | `∅` | `{0}` |
| `3` | `∅` | `{tt}` | `∅` | `{tt}` |
| `4` | `∅` | `{0}` | `∅` | `{0}` |
| `5` | `{fn y => y^4}` | `{fn y => y^4}` | `{fn y => y^4}` | `∅` |
| `6` | `∅` | `∅` | `∅` | `∅` |
| `7` | `{fn z => 25^6}` | `∅` | `∅` | `∅` |
| `8` | `{fn y => y^4, fn z => 25^6}` | `{fn y => y^4}` | `{fn y => y^4}` | `∅` |
| `9` | `{fn x => (···)^8}` | `{fn x => (···)^8}` | `{fn x => (···)^8}` | `∅` |
| `10` | `{fn x => (···)^8}` | `{fn x => (···)^8}` | `{fn x => (···)^8}` | `∅` |
| `11` | `∅` | `{+}` | `∅` | `{+}` |
| `12` | `{fn y => y^4, fn z => 25^6}` | `{fn y => y^4}` | `{fn y => y^4}` | `∅` |
| `13` | `∅` | `{0}` | `∅` | `{0}` |
| `14` | `∅` | `{0}` | `∅` | `{0}` |
| `15` | `∅` | `{0}` | `∅` | `{0}` |
| `f` | `{fn x => (···)^8}` | `{fn x => (···)^8}` | `{fn x => (···)^8}` | `∅` |
| `x` | `∅` | `{+}` | `∅` | `{+}` |
| `y` | `∅` | `{0}` | `∅` | `{0}` |
| `z` | `∅` | `∅` | `∅` | `∅` |

- Citation: [PPA Figure 3.6, p. 185] (book p. 185; PDF p. 203)

### [U3b:3.5.1-c] Soundness, finite-`Data` solvability, and non-projection to Table 3.1 (`⊨_d` vs `⊨`)
- Statement:
  - *Semantic correctness & solver*: §3.2's SOS techniques establish soundness; a slight extension of
    §§3.3–3.4 and [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220) yields an algorithmic
    implementation **provided `Data` is finite**.
  - *Non-projection warning*: `(Ĉ, ρ̂) ⊨_d e` does **not** guarantee `(Ĉ', ρ̂') ⊨ e` ([PPA Table 3.1, p. 146]
    (book p. 146; PDF p. 164)) for `∀ℓ : Ĉ'(ℓ) = Ĉ(ℓ) ∩ Term` and `∀x : ρ̂'(x) = ρ̂(x) ∩ Term`, because
    Table 3.8 `[if]` skips branches whose guard token (`d_true` or `d_false`) is absent (`[derived]`: in
    Figure 3.6 column 2, `Ĉ'(7) = ∅`, violating Table 3.1 `[if]`/`[fn]` on `(fn z => 25^6)^7`).
- Citation: [PPA §3.5.1, p. 184] (book p. 184; PDF p. 202); [PPA §3.5.1, p. 185] (book p. 185; PDF p. 203)

### Findings (3.5.1)
- F-U3b-01: on pp. 182–184, §3.5.1 defines `Val̂_d = 𝒫(Term ∪ Data)` and writes `(Ĉ, ρ̂) ⊨_d e` without
  explicitly redefining `Env̂_d = Var → Val̂_d` and `Cachê_d = Lab → Val̂_d`; the updated signatures
  `Ĉ : Lab → Val̂_d` and `ρ̂ : Var → Val̂_d` are stated retrospectively at the start of §3.5.2 (pp. 185–186).
  [PPA §3.5.1, p. 182] (book p. 182; PDF p. 200); [PPA §3.5.1, p. 184] (book p. 184; PDF p. 202); [PPA §3.5.2, p. 185] (book p. 185; PDF p. 203); [PPA §3.5.2, p. 186] (book p. 186; PDF p. 204)

### Projections (3.5–3.5.1)
- cs_theory: Guarding `[if]` branches on `d_true ∈ Ĉ(ℓ₀)` and `d_false ∈ Ĉ(ℓ₀)` remains monotone on
  `𝒫(Term ∪ Data)` because singleton membership `d ∈ X` is positive/Scott-continuous (`U3a` singleton-guard
  principle), preserving the Moore-family / least-solution structure while strictly refining `Table 3.1`
  [derived] [PPA Table 3.8, p. 184] (book p. 184; PDF p. 202).
- swe_architecture: Online feedback between data values and indirect-call resolution (`Table 3.8`) is the
  higher-order generalisation of Wegman–Zadeck Sparse Conditional Constant Propagation (`SCCP` [external])
  and compiler devirtualisation passes [external] [PPA Example 3.27, p. 183] (book p. 183; PDF p. 201); [PPA Example 3.27, p. 184] (book p. 184; PDF p. 202).
- practical_debugging: Never run a pure `Table 3.1` post-check oracle on the `∩ Term` projection of a
  `Table 3.8` solver output — pruned dead branches legitimately leave `Ĉ(ℓ) ∩ Term = ∅` inside untaken arms
  [PPA §3.5.1, p. 185] (book p. 185; PDF p. 203).
- cyber: Dead-branch pruning eliminates false-positive deserialization gadgets (`CWE-502` [external]) and
  unreachable debug/platform callbacks from security call graphs; however, in *open systems* where attacker
  or FFI inputs `[external]` can invalidate static constant assumptions at `ℓ₀`, skipped branches have **zero** CFA
  coverage (`Ĉ(7) = ∅`), requiring conservative `⊤` seeding on external inputs [derived]
  [PPA §3.5.1, p. 185] (book p. 185; PDF p. 203).

---

## 3.5.2 Abstract Values as Complete Lattices

Context: factoring `𝒫(Term ∪ Data) ≅ 𝒫(Term) × 𝒫(Data)` to replace `𝒫(Data)` with an arbitrary complete
lattice `L` via *monotone structures* `(L, ℱ, ι., f.)`, specifying `(Ĉ, D̂, ρ̂, δ̂) ⊨_D e` in `Table 3.9`, and
contrasting coupled `⊨_D` with two-phase staged `⊨'_D` (`Examples 3.28–3.31`)
[PPA §3.5.2, p. 185] (book p. 185; PDF p. 203); [PPA §3.5.2, p. 189] (book p. 189; PDF p. 207).

### [U3b:3.5.2-a] Product isomorphism, monotone structures `(L, ℱ)`, and instances `(L, ℱ, ι., f.)`
- Statement: using `Val̂_d = 𝒫(Term ∪ Data) ≅ 𝒫(Term) × 𝒫(Data)`, split `Ĉ` and `ρ̂` into closure and data
  components and generalise `𝒫(Data)` to a complete lattice:
  - A *monotone structure* `(L, ℱ)` consists of a complete lattice `L` and a set `ℱ` of monotone binary
    functions `L × L → L`.
  - An *instance* `(L, ℱ, ι., f.)` adds a constant map `ι.` (`c ↦ ι_c ∈ L` for `c ∈ Const`) and an operator
    map `f.` (`op ↦ f_op ∈ ℱ` for `op ∈ Op`).
  - *Relation to §2.3 Monotone Frameworks* ([PPA §2.3.1, p. 68] (book p. 68; PDF p. 87); [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88)): omits
    the `flow` graph `F` because CFA discovers control flow dynamically; replaces single extremal `ι` by `ι.`
    on constants; and replaces block-indexed transfers `f_ℓ` by operator interpretations `f_op`.
- Citation: [PPA §3.5.2, p. 185] (book p. 185; PDF p. 203); [PPA §3.5.2, p. 186] (book p. 186; PDF p. 204)

### Example 3.28 — Powerset `§3.5.1` as a monotone structure instance
- Statement: take `L = 𝒫(Data)` and `ℱ` = all monotone functions `𝒫(Data) × 𝒫(Data) → 𝒫(Data)`, with:
  ```text
  ι_c          = {d_c}                                      for all c ∈ Const
  f_op(l₁, l₂) = ⋃{d_op(d₁, d₂) | d₁ ∈ l₁, d₂ ∈ l₂}         for all op ∈ Op
  ```
  `■`
- Citation: [PPA Example 3.28, p. 186] (book p. 186; PDF p. 204)

### Example 3.29 — Constant Propagation monotone structure (`Z_⊥^⊤ × 𝒫({tt, ff})`)
- Statement: take `L = Z_⊥^⊤ × 𝒫({tt, ff})` and `ℱ` = monotone functions `L × L → L`, with e.g. `ι_7 = (7, ∅)`,
  `ι_true = (⊥, {tt})`, and for `+`:
  ```text
  f_+(l₁, l₂) = (z₁ + z₂, ∅)   if l₁ = (z₁, ···), l₂ = (z₂, ···), and z₁, z₂ ∈ Z
                (⊥, ∅)         if l₁ = (z₁, ···), l₂ = (z₂, ···), and z₁ = ⊥ or z₂ = ⊥
                (⊤, ∅)         otherwise
  ```
  `■`
- Side conditions: `[derived]` testing `z₁ = ⊥ or z₂ = ⊥` *before* `otherwise` makes `f_+` strict in `⊥_Z`
  (`f_+((⊥, {tt}), (⊤, ∅)) = (⊥, ∅)`), which is mandatory for monotonicity on `(Z_⊥^⊤, ⊑)`.
- Citation: [PPA Example 3.29, p. 186] (book p. 186; PDF p. 204); [PPA Example 3.29, p. 187] (book p. 187; PDF p. 205)

### [U3b:3.5.2-b] Split CFA/DFA domains, `(Ĉ, D̂, ρ̂, δ̂) ⊨_D e`, and Ascending Chain Condition (`ACC`)
- Statement: pair §3.1.1's CFA domains (`v̂ ∈ Val̂ = 𝒫(Term)`, `ρ̂ ∈ Env̂ = Var → Val̂`, `Ĉ ∈ Cachê = Lab → Val̂`)
  with data-flow domains:
  ```text
  d̂ ∈ Datâ   = L               abstract data values
  δ̂ ∈ DEnv̂   = Var → Datâ      abstract data environments
  D̂ ∈ DCachê = Lab → Datâ      abstract data caches
  ```
  Acceptability `(Ĉ, D̂, ρ̂, δ̂) ⊨_D e` is defined in Table 3.9. Section 3.2's proof methods establish semantic
  correctness, and §§3.3–3.4 (with [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220)) yield a
  terminating implementation **provided `L` satisfies the Ascending Chain Condition (`ACC`)**.
- Citation: [PPA §3.5.2, p. 187] (book p. 187; PDF p. 205)

### Table 3.9 — Abstract values as complete lattices
- Content (transcribed verbatim from `p-206.png`, restoring `[op]` erased in OCR and preserving the printed
  parenthesisation and tight `Ĉ(ℓ)∧` spacing in `[if]`; finding F-U3b-02):
  ```text
  [con]  (Ĉ, D̂, ρ̂, δ̂) ⊨_D c^ℓ iff ι_c ⊑ D̂(ℓ)

  [var]  (Ĉ, D̂, ρ̂, δ̂) ⊨_D x^ℓ iff ρ̂(x) ⊆ Ĉ(ℓ) ∧ δ̂(x) ⊑ D̂(ℓ)

  [fn]   (Ĉ, D̂, ρ̂, δ̂) ⊨_D (fn x => e₀)^ℓ iff {fn x => e₀} ⊆ Ĉ(ℓ)

  [fun]  (Ĉ, D̂, ρ̂, δ̂) ⊨_D (fun f x => e₀)^ℓ iff {fun f x => e₀} ⊆ Ĉ(ℓ)

  [app]  (Ĉ, D̂, ρ̂, δ̂) ⊨_D (t₁^{ℓ₁} t₂^{ℓ₂})^ℓ
           iff  (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₁^{ℓ₁}  ∧  (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₂^{ℓ₂}  ∧
                (∀(fn x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) :
                   (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₀^{ℓ₀}  ∧
                   Ĉ(ℓ₂) ⊆ ρ̂(x)  ∧  D̂(ℓ₂) ⊑ δ̂(x)  ∧
                   Ĉ(ℓ₀) ⊆ Ĉ(ℓ)  ∧  D̂(ℓ₀) ⊑ D̂(ℓ))  ∧
                (∀(fun f x => t₀^{ℓ₀}) ∈ Ĉ(ℓ₁) :
                   (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₀^{ℓ₀}  ∧
                   Ĉ(ℓ₂) ⊆ ρ̂(x)  ∧  D̂(ℓ₂) ⊑ δ̂(x)  ∧
                   Ĉ(ℓ₀) ⊆ Ĉ(ℓ)  ∧  D̂(ℓ₀) ⊑ D̂(ℓ)  ∧
                   {fun f x => t₀^{ℓ₀}} ⊆ ρ̂(f))

  [if]   (Ĉ, D̂, ρ̂, δ̂) ⊨_D (if t₀^{ℓ₀} then t₁^{ℓ₁} else t₂^{ℓ₂})^ℓ
           iff  (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₀^{ℓ₀}  ∧
                (ι_true  ⊑ D̂(ℓ₀) ⇒ (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₁^{ℓ₁} ∧
                                    Ĉ(ℓ₁) ⊆ Ĉ(ℓ)∧
                                    D̂(ℓ₁) ⊑ D̂(ℓ))  ∧
                (ι_false ⊑ D̂(ℓ₀) ⇒ (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₂^{ℓ₂} ∧
                                    Ĉ(ℓ₂) ⊆ Ĉ(ℓ)∧
                                    D̂(ℓ₂) ⊑ D̂(ℓ))

  [let]  (Ĉ, D̂, ρ̂, δ̂) ⊨_D (let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ
           iff  (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₁^{ℓ₁}  ∧  (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₂^{ℓ₂}  ∧
                Ĉ(ℓ₁) ⊆ ρ̂(x)  ∧  D̂(ℓ₁) ⊑ δ̂(x)  ∧
                Ĉ(ℓ₂) ⊆ Ĉ(ℓ)  ∧  D̂(ℓ₂) ⊑ D̂(ℓ)

  [op]   (Ĉ, D̂, ρ̂, δ̂) ⊨_D (t₁^{ℓ₁} op t₂^{ℓ₂})^ℓ
           iff  (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₁^{ℓ₁}  ∧  (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₂^{ℓ₂}  ∧
                f_op(D̂(ℓ₁), D̂(ℓ₂)) ⊑ D̂(ℓ)
  ```
- Citation: [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206)

### Example 3.30 — Complete-lattice Signs on Example 3.27
- Statement: applying Table 3.9 with Example 3.28's Detection of Signs monotone structure to Example 3.27
  produces the two rightmost columns `(Ĉ, ρ̂)` and `(D̂, δ̂)` of Figure 3.6, matching §3.5.1 (`D̂(15) = {0}`,
  `Ĉ(12) = {fn y => y^4}`). `■`
- Citation: [PPA Example 3.30, p. 187] (book p. 187; PDF p. 205)

### [U3b:3.5.2-c] Staging the specification (`⊨'_D`) — two-phase CFA-then-DFA solving
- Statement: replacing `[if]` in Table 3.9 with unconditional branch obligations defines `(Ĉ, D̂, ρ̂, δ̂) ⊨'_D e`:
  ```text
  (Ĉ, D̂, ρ̂, δ̂) ⊨'_D (if t₀^{ℓ₀} then t₁^{ℓ₁} else t₂^{ℓ₂})^ℓ
    iff  (Ĉ, D̂, ρ̂, δ̂) ⊨'_D t₀^{ℓ₀}  ∧
         (Ĉ, D̂, ρ̂, δ̂) ⊨'_D t₁^{ℓ₁}  ∧  Ĉ(ℓ₁) ⊆ Ĉ(ℓ)  ∧  D̂(ℓ₁) ⊑ D̂(ℓ)  ∧
         (Ĉ, D̂, ρ̂, δ̂) ⊨'_D t₂^{ℓ₂}  ∧  Ĉ(ℓ₂) ⊆ Ĉ(ℓ)  ∧  D̂(ℓ₂) ⊑ D̂(ℓ)
  ```
  - Unlike `⊨_d` and `⊨_D`, `(Ĉ, D̂, ρ̂, δ̂) ⊨'_D e` **does** guarantee `(Ĉ, ρ̂) ⊨ e` (Table 3.1).
  - *Staged least-fixed-point property*: because `(Ĉ, ρ̂)` constraints no longer mention `D̂` or `δ̂`, solving
    for the least `(Ĉ, ρ̂)` *first* and solving for the least `(D̂, δ̂)` *second* (using that `(Ĉ, ρ̂)`) produces
    the **exact least solution** of the combined `⊨'_D` system.
- Citation: [PPA §3.5.2, p. 189] (book p. 189; PDF p. 207)

### Example 3.31 — Precision loss under staged `⊨'_D`
- Statement: re-analysing Example 3.27 / 3.30 under `⊨'_D` degrades `(Ĉ, ρ̂)` back to the pure §3.1 column of
  Figure 3.6 (`fn z => 25^6` enters `Ĉ(7), Ĉ(8), Ĉ(12)`) and enlarges `(D̂, δ̂)` at four entries relative to
  Figure 3.6: `D̂(6) = {+}`, `D̂(14) = {0, +}`, `D̂(15) = {0, +}`, and `δ̂(z) = {0}` (reporting `{0, +}` instead
  of `{0}`). `■`
- Citation: [PPA Example 3.31, p. 189] (book p. 189; PDF p. 207)

### [U3b:3.5.2-d] Pointers to data structures and imperative constructs (unnumbered remark)
- Statement: [PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221) extends CFA to track creation points of
  data structures; [PPA Mini Project 3.4, p. 204] (book p. 204; PDF p. 222); [PPA Mini Project 3.4, p. 205] (book p. 205; PDF p. 223) incorporates
  imperative reference constructs in the manner of Chapter 2's `WHILE`.
- Citation: [PPA §3.5.2, p. 189] (book p. 189; PDF p. 207)

### Findings (3.5.2)
- F-U3b-02: in Table 3.9 `[if]` (p. 188), `(ι_true ⊑ D̂(ℓ₀) ⇒ (Ĉ, D̂, ρ̂, δ̂) ⊨_D t₁^{ℓ₁} ∧ Ĉ(ℓ₁) ⊆ Ĉ(ℓ)∧ D̂(ℓ₁) ⊑ D̂(ℓ))`
  omits inner parentheses around the 3-way RHS conjunction after `⇒` (unlike Table 3.8 `[if]` on p. 184) and
  drops whitespace before `∧` in `Ĉ(ℓ)∧`; semantically, testing `ι_true ⊑ D̂(ℓ₀)` on a general lattice `L`
  requires `true ∈ γ(d̂) ⇒ ι_true ⊑ d̂` (automatic when `ι_c = α({c})` under a Chapter 4 Galois connection
  `[derived]`). Also §3.5.2 uses hatted `δ̂ ∈ DEnv̂`, whereas §3.6 uses unhatted `δ ∈ Δ` for contexts.
  [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206)

### Projections (3.5.2)
- cs_theory: `Table 3.9` realises a *mutually communicating / co-fibered product* (`U4`: Chapter 2 Monotone
  Frameworks lifted into dynamic higher-order CFA, foreshadowing Chapter 4 §4.4 product domains) that is
  strictly tighter than the staged Cartesian product `⊨'_D` (`Example 3.31`) whenever branch predicates gate
  closure creation [derived] [PPA §3.5.2, p. 186] (book p. 186; PDF p. 204); [PPA §3.5.2, p. 189] (book p. 189; PDF p. 207).
- swe_architecture: Factoring `(L, ℱ, ι., f.)` into a pluggable Product-Domain Bridge [external] decouples
  closure propagation from value domains (Signs, Constant Propagation, taint bitsets [external]); pairing `Table 3.9`
  with `Mini Project 3.1` reachability `R̂` in one worklist implements interprocedural `IPSCCP` [external],
  whereas `⊨'_D` suits modular pipelines [external] that reuse an existing `0-CFA` call graph
  [PPA §3.5.2, p. 186] (book p. 186; PDF p. 204); [PPA §3.5.2, p. 189] (book p. 189; PDF p. 207).
- practical_debugging: Two subtle soundness bugs afflict custom `Table 3.9` solvers [derived]: (1) on
  product lattices like `Example 3.29` (`Z_⊥^⊤ × 𝒫({tt, ff})`), relational operators (`>`) on unknown `(⊤, ∅)`
  integers **must** return `(⊥, {tt, ff})` rather than `f_+`'s `(⊤, ∅)`, otherwise neither `ι_true` nor
  `ι_false` is `⊑ D̂(ℓ₀)` and **both** `if`-branches are silently dropped; (2) never prune `else` just because
  `ι_true ⊑ D̂(ℓ₀)` mid-iteration — `D̂(ℓ₀)` grows monotonically and may later reach `ι_true ⊔ ι_false`!
  [PPA Example 3.29, p. 187] (book p. 187; PDF p. 205); [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206).
- cyber: If `L` lacks `ACC` (e.g. unbounded integer intervals `Interval` for buffer-bounds checking
  `CWE-119` [external]), `Table 3.9` fixed-point iteration diverges unless equipped with Chapter 4 widening
  (`§4.1.2`) [PPA §3.5.2, p. 187] (book p. 187; PDF p. 205).

---

## 3.6 Adding Context Information

Context: lifting monovariant 0-CFA to polyvariant context-sensitive analyses via bounded call strings
(*uniform `k`-CFA*, `k`-CFA, *polynomial `k`-CFA* in §3.6.1) and abstract argument tuples (*Cartesian Product
Algorithm*, `CPA` in §3.6.2), establishing exact curried correspondences (`U5`) with §2.5.4 and §2.5.5
[PPA §3.6, p. 189] (book p. 189; PDF p. 207); [PPA §3.6, p. 198] (book p. 198; PDF p. 216).

### [U3b:3.6-a] Monovariant vs polyvariant CFA and taxonomy of context mechanisms
- Statement: pure 0-CFA cannot distinguish different dynamic instances of variables and program points — it
  is *context-insensitive* (§2.5 terminology) or *monovariant* (CFA terminology). Adding context yields a
  *context-sensitive* or *polyvariant* analysis; principal designs are *`k`-CFA*, *uniform `k`-CFA* (§3.6.1),
  *polynomial `k`-CFA* (mainly of interest for `k > 0`, pp. 191, 195), and the *Cartesian Product Algorithm*
  (`CPA`, §3.6.2).
- Citation: [PPA §3.6, p. 189] (book p. 189; PDF p. 207); [PPA §3.6, p. 191] (book p. 191; PDF p. 209)

### Example 3.32 — Monovariant poisoning on polymorphic identity `(f f)(fn y => y)`
- Statement: on `(let f = (fn x => x^1)^2 in ((f^3 f^4)^5 (fn y => y^6)^7)^8)^9`, the least 0-CFA solution
  `(Ĉ_id, ρ̂_id)` is:
  ```text
  Ĉ_id(1) = {fn x => x^1, fn y => y^6}     ρ̂_id(f) = {fn x => x^1}
  Ĉ_id(2) = {fn x => x^1}                  ρ̂_id(x) = {fn x => x^1, fn y => y^6}
  Ĉ_id(3) = {fn x => x^1}                  ρ̂_id(y) = {fn y => y^6}
  Ĉ_id(4) = {fn x => x^1}
  Ĉ_id(5) = {fn x => x^1, fn y => y^6}
  Ĉ_id(6) = {fn y => y^6}
  Ĉ_id(7) = {fn y => y^6}
  Ĉ_id(8) = {fn x => x^1, fn y => y^6}
  Ĉ_id(9) = {fn x => x^1, fn y => y^6}
  ```
  Merging both calls to `f` (`5` and `8`) into `ρ̂_id(x)` pollutes `Ĉ_id(9)` with `fn x => x^1` (`[derived]`:
  and leaking `fn y => y^6` into operator cache `Ĉ_id(5)` forces a bogus self-call `ρ̂_id(y) = {fn y => y^6}`
  even though `fn y => y^6` is never applied at run time!). `■`
- Citation: [PPA Example 3.32, p. 190] (book p. 190; PDF p. 208)

### Example 3.33 — Syntactic let-cloning workaround
- Statement: duplicating `f` into `let f1 = (fn x1 => x1) in let f2 = (fn x2 => x2) in (f1 f2) (fn y => y)`
  lets 0-CFA bind `x1` to `{fn x2 => x2}` and `x2` to `{fn y => y}`, recovering `{fn y => y}` at the cost of
  program expansion. `■`
- Citation: [PPA Example 3.33, p. 190] (book p. 190; PDF p. 208); [PPA Example 3.33, p. 191] (book p. 191; PDF p. 209)

## 3.6.1 Uniform `k`-CFA Analysis

Context: call-string contexts `Δ = Lab^{≤k}`, lexical context environments `ce ∈ CEnv`, `Table 3.10`,
`Example 3.34`, `O(n · n^p)` exponential height vs `O(n⁶)` polynomial `1-CFA`, and `U5` correspondence with
§2.5.4 [PPA §3.6.1, p. 191] (book p. 191; PDF p. 209); [PPA §3.6.1, p. 196] (book p. 196; PDF p. 214).

### [U3b:3.6.1-a] Uniform `k`-CFA vs standard `k`-CFA abstract domains
- Statement: for integer `k ≥ 0`, contexts record the last `≤ k` dynamic application labels:
  ```text
  δ  ∈ Δ     = Lab^{≤k}                context information
  ce ∈ CEnv  = Var → Δ                 context environments
  v̂  ∈ Val̂   = 𝒫(Term × CEnv)          abstract values (abstract closures)
  ρ̂  ∈ Env̂   = (Var × Δ) → Val̂         abstract environments
  Ĉ  ∈ Cachê = (Lab × Δ) → Val̂         abstract caches (uniform k-CFA)
  ```
  - Each abstract closure `(t, ce₀) ∈ Val̂` pairs `t` with its definition-time `ce₀` restricted to `FV(t)`
    (mirroring concrete closures `close t in ρ` of §3.2.1), so `[var]` looks up `ρ̂(x, ce(x))` — simulating
    per-closure local environments inside a single global `ρ̂`.
  - *Contrast with standard `k`-CFA* (p. 193): uniform `k`-CFA uses `Cachê = (Lab × Δ) → Val̂`, whereas
    Shivers' `[156, 157, 158]` (`p. 198`) standard `k`-CFA uses `Cachê = (Lab × CEnv) → Val̂`.
- Citation: [PPA §3.6.1, p. 191] (book p. 191; PDF p. 209); [PPA §3.6.1, p. 193] (book p. 193; PDF p. 211)

### Table 3.10 — Uniform `k`-CFA analysis
- Content:
  ```text
  [con]  (Ĉ, ρ̂) ⊨_δ^{ce} c^ℓ always

  [var]  (Ĉ, ρ̂) ⊨_δ^{ce} x^ℓ iff ρ̂(x, ce(x)) ⊆ Ĉ(ℓ, δ)

  [fn]   (Ĉ, ρ̂) ⊨_δ^{ce} (fn x => e₀)^ℓ iff {(fn x => e₀, ce₀)} ⊆ Ĉ(ℓ, δ)
           where ce₀ = ce | FV(fn x => e₀)

  [fun]  (Ĉ, ρ̂) ⊨_δ^{ce} (fun f x => e₀)^ℓ iff {(fun f x => e₀, ce₀)} ⊆ Ĉ(ℓ, δ)
           where ce₀ = ce | FV(fun f x => e₀)

  [app]  (Ĉ, ρ̂) ⊨_δ^{ce} (t₁^{ℓ₁} t₂^{ℓ₂})^ℓ
           iff  (Ĉ, ρ̂) ⊨_δ^{ce} t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_δ^{ce} t₂^{ℓ₂}  ∧
                (∀(fn x => t₀^{ℓ₀}, ce₀) ∈ Ĉ(ℓ₁, δ) :
                   (Ĉ, ρ̂) ⊨_{δ₀}^{ce'_0} t₀^{ℓ₀}  ∧
                   Ĉ(ℓ₂, δ) ⊆ ρ̂(x, δ₀)  ∧  Ĉ(ℓ₀, δ₀) ⊆ Ĉ(ℓ, δ)
                   where δ₀ = ⌈δ, ℓ⌉_k
                   and ce'_0 = ce₀[x ↦ δ₀])  ∧
                (∀(fun f x => t₀^{ℓ₀}, ce₀) ∈ Ĉ(ℓ₁, δ) :
                   (Ĉ, ρ̂) ⊨_{δ₀}^{ce'_0} t₀^{ℓ₀}  ∧
                   Ĉ(ℓ₂, δ) ⊆ ρ̂(x, δ₀)  ∧  Ĉ(ℓ₀, δ₀) ⊆ Ĉ(ℓ, δ)  ∧
                   {(fun f x => t₀^{ℓ₀}, ce₀)} ⊆ ρ̂(f, δ₀)
                   where δ₀ = ⌈δ, ℓ⌉_k
                   and ce'_0 = ce₀[f ↦ δ₀, x ↦ δ₀])

  [if]   (Ĉ, ρ̂) ⊨_δ^{ce} (if t₀^{ℓ₀} then t₁^{ℓ₁} else t₂^{ℓ₂})^ℓ
           iff  (Ĉ, ρ̂) ⊨_δ^{ce} t₀^{ℓ₀}  ∧  (Ĉ, ρ̂) ⊨_δ^{ce} t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_δ^{ce} t₂^{ℓ₂}  ∧
                Ĉ(ℓ₁, δ) ⊆ Ĉ(ℓ, δ)  ∧  Ĉ(ℓ₂, δ) ⊆ Ĉ(ℓ, δ)

  [let]  (Ĉ, ρ̂) ⊨_δ^{ce} (let x = t₁^{ℓ₁} in t₂^{ℓ₂})^ℓ
           iff  (Ĉ, ρ̂) ⊨_δ^{ce} t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_δ^{ce} t₂^{ℓ₂}  ∧
                Ĉ(ℓ₁, δ) ⊆ ρ̂(x, δ)  ∧  Ĉ(ℓ₂, δ) ⊆ Ĉ(ℓ, δ)
           where ce' = ce[x ↦ δ]

  [op]   (Ĉ, ρ̂) ⊨_δ^{ce} (t₁^{ℓ₁} op t₂^{ℓ₂})^ℓ
           iff  (Ĉ, ρ̂) ⊨_δ^{ce} t₁^{ℓ₁}  ∧  (Ĉ, ρ̂) ⊨_δ^{ce} t₂^{ℓ₂}
  ```
- Citation: [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210)

### [U3b:3.6.1-b] Context-update rules (`⌈δ, ℓ⌉_k` in `[app]` vs unchanged `δ` in `[let]`) and omitted proofs
- Statement:
  - In `[app]` on `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ`, crossing application point `ℓ` updates `δ` to `δ₀ = ⌈δ, ℓ⌉_k`
    (left-truncating `[δ, ℓ]` to length `≤ k`, as in §2.5.4) and extends captured `ce₀` (`ce'_0 = ce₀[x ↦ δ₀]`,
    or `[f ↦ δ₀, x ↦ δ₀]`).
  - In `[let]`, **no application point is passed**, so `x` is bound to the unchanged current context `δ`
    (`ce' = ce[x ↦ δ]`, `Ĉ(ℓ₁, δ) ⊆ ρ̂(x, δ)`).
  - Semantic correctness proofs and solver implementations for Table 3.10 are omitted by the authors (p. 194).
- Citation: [PPA §3.6.1, p. 193] (book p. 193; PDF p. 211); [PPA §3.6.1, p. 194] (book p. 194; PDF p. 212)

### Example 3.34 — Uniform `1-CFA` on `(let f = (fn x => x^1)^2 in ((f^3 f^4)^5 (fn y => y^6)^7)^8)^9`
- Statement: for `k = 1` on Example 3.32's expression (misprinted `"Example 3.33"` on p. 194; finding
  F-U3b-04), reachable call strings are `Δ_⋆ = {Λ, 5, 8}` with `ce₀ = []`, `ce₁ = ce₀[f ↦ Λ]`,
  `ce₂ = ce₀[x ↦ 5]`, `ce₃ = ce₀[x ↦ 8]`. Non-empty entries of `(Ĉ'_id, ρ̂'_id)`:
  ```text
  Ĉ'_id(1, 5) = {(fn x => x^1, ce₀)}      Ĉ'_id(1, 8) = {(fn y => y^6, ce₀)}
  Ĉ'_id(2, Λ) = {(fn x => x^1, ce₀)}      Ĉ'_id(3, Λ) = {(fn x => x^1, ce₀)}
  Ĉ'_id(4, Λ) = {(fn x => x^1, ce₀)}      Ĉ'_id(5, Λ) = {(fn x => x^1, ce₀)}
  Ĉ'_id(7, Λ) = {(fn y => y^6, ce₀)}      Ĉ'_id(8, Λ) = {(fn y => y^6, ce₀)}
  Ĉ'_id(9, Λ) = {(fn y => y^6, ce₀)}      ρ̂'_id(f, Λ) = {(fn x => x^1, ce₀)}
  ρ̂'_id(x, 5) = {(fn x => x^1, ce₀)}      ρ̂'_id(x, 8) = {(fn y => y^6, ce₀)}
  ```
  (all other entries `∅`, notably `Ĉ'_id(6, δ) = ρ̂'_id(y, δ) = ∅` for all `δ ∈ {Λ, 5, 8}`). Checking
  `(Ĉ'_id, ρ̂'_id) ⊨_Λ^{ce₀} e` via `[let]`, `[app]` at `8` (`⌈Λ, 8⌉₁ = 8`), `[app]` at `5` (`⌈Λ, 5⌉₁ = 5`),
  `[fn]`, and `[var]` confirms exact singleton `Ĉ'_id(9, Λ) = {(fn y => y^6, ce₀)}`. `■`
- Citation: [PPA Example 3.34, p. 194] (book p. 194; PDF p. 212); [PPA Example 3.34, p. 195] (book p. 195; PDF p. 213)

### [U3b:3.6.1-c] Exponential worst-case complexity for `k = 1` vs `O(n⁶)` polynomial `1-CFA`
- Statement: for an expression of size `n` with `p = O(n)` distinct variables:
  - *Uniform `1-CFA`*: `|Δ| = O(n)` yields `O(p · n)` pairs `(x, δ)` and `O(n²)` pairs `(ℓ, δ)`, so `(Ĉ, ρ̂)`
    is an `O(n²)`-tuple over `Val̂ = 𝒫(Term × CEnv)`. Because `|CEnv| = O(n^p)`, there are `O(n · n^p)` pairs
    `(t, ce)`, giving `Val̂` height **`O(n · n^p)`** — **exponential worst-case complexity even at `k = 1`**
    (and likewise for standard `k`-CFA).
  - *Contrast with `0-CFA`*: `|Δ| = 1`, `O(p + n)` entries, `Val̂` height `O(n)` (`O(n³)` solver in §3.4.2).
  - *Remedies*: (1) Chapter 4 Abstract Interpretation to shrink `Val̂` height; (2) replace `CEnv` in `Val̂` by
    single contexts `Val̂ = 𝒫(Term × Δ)` (equivalent to **polynomial `k`-CFA**, where context environments are
    constant functions; **polynomial `1-CFA` has worst-case complexity `O(n⁶)`**).
- Citation: [PPA §3.6.1, p. 195] (book p. 195; PDF p. 213)

### [U3b:3.6.1-d] Interprocedural analysis revisited (`U5`): §2.5.4 Call Strings ↔ §3.6.1 Uniform `k`-CFA
- Statement: in §2.5 ([PPA §2.5.3, p. 91] (book p. 91; PDF p. 110); [PPA §2.5.4, p. 98] (book p. 98; PDF p. 117)),
  embellished Monotone Frameworks use `A_∘, A_• : Lab → (Δ → L)` over `Δ = Lab^{≤k}`. Currying uniform `k`-CFA
  with `L = 𝒫(Term × CEnv)` gives:
  ```text
  Ĉ : Lab → Δ → 𝒫(Term × CEnv)
  ρ̂ : Var → Δ → 𝒫(Term × CEnv)
  ```
  Section 2.5 required neither `ρ̂` nor `CEnv` because its imperative procedures lacked lexical closures — all
  free variables inside procedures were global variables (cf. [PPA Exercise 3.16, p. 208]
  (book p. 208; PDF p. 226); [PPA Exercise 3.16, p. 209] (book p. 209; PDF p. 227)).
- Citation: [PPA §3.6.1, p. 196] (book p. 196; PDF p. 214)

### Findings (3.6–3.6.1)
- F-U3b-03: §3.6.1 (p. 191) defines `CEnv = Var → Δ` as total functions, whereas Table 3.10 `[fn]`/`[fun]`
  (p. 192) restricts `ce₀ = ce | FV(...)` to finite subsets and Example 3.34 (p. 194) writes `ce₀ = []`
  (partial finite maps `Var ⇀_fin Δ`). [PPA §3.6.1, p. 191] (book p. 191; PDF p. 209);
  [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210); [PPA Example 3.34, p. 194] (book p. 194; PDF p. 212)
- F-U3b-04 (`[Source Erratum]`): Example 3.34 (p. 194) states `"for the expression of Example 3.33"` while
  displaying and analysing the unexpanded expression of **Example 3.32** (p. 190), and prints `"since we only
  records call strings"` (`records` for `record`). [PPA Example 3.34, p. 194] (book p. 194; PDF p. 212)

### Projections (3.6–3.6.1)
- cs_theory: Exact `k`-CFA (`k ≥ 1`) jumps from `0-CFA`'s polynomial time (`[external: PTIME-complete]`) to exponential worst case (`[external: DEXPTIME-complete]`)
  [external: Van Horn & Mairson 2008] because per-variable `ce ∈ Var → Δ` encodes `n`-variable truth
  assignments across nested closures; collapsing `Val̂` to `𝒫(Term × Δ)` (polynomial `k`-CFA / flat-contour
  `m`-CFA [external: Might, Smaragdakis & Van Horn 2010]) restores polynomial complexity (`O(n⁶)` at `k = 1`),
  and currying `(Lab × Δ) → Val̂` realizes the `U5` call-string isomorphism with §2.5.4
  [PPA §3.6.1, p. 195] (book p. 195; PDF p. 213); [PPA §3.6.1, p. 196] (book p. 196; PDF p. 214).
- swe_architecture: Keep `let` primitive in `k`-CFA IRs rather than desugaring `let x = e₁ in e₂` into
  `((fn x => e₂) e₁)^ℓ`: `[let]` preserves all `k` call-string slots (`ce[x ↦ δ]`), whereas `[app]` consumes
  one slot via `⌈δ, ℓ⌉_k` [derived]; always canonicalise `ce₀ = ce | FV(t)` (Flyweight interning [external])
  so unreachable outer bindings never split identical closures
  [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210).
- practical_debugging: Three high-frequency `k`-CFA implementation bugs are (1) reading `ρ̂(x, δ)` instead of
  `ρ̂(x, ce(x))` in `[var]` (implements dynamic scoping!), (2) extending the caller's `ce` instead of the
  closure's `ce₀` in `[app]`, and (3) pushing callee body label `ℓ₀` instead of application label `ℓ` in
  `δ₀ = ⌈δ, ℓ⌉_k` [derived] [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210).
- cyber: `1-CFA` eliminates monovariant callback/vtable cross-pollution (`Example 3.32` → `3.34`), tightening
  Control-Flow Integrity (`CFI` [external]) target sets, while curried closure chains risk algorithmic
  complexity DoS (`CWE-400` [external]) unless `ce₀` is restricted to `FV(t)` or flattened to `𝒫(Term × Δ)`
  [PPA §3.6.1, p. 195] (book p. 195; PDF p. 213).

---

## 3.6.2 The Cartesian Product Algorithm

Context: Argument-tuple polyvariance (`[2]`, `[external: Agesen]`, `Δ = Term^m`) on closed `m`-ary `FUN` abstractions, memoised
templates, lazy product growth, and `U5` correspondence with §2.5.5 small assumption sets
[PPA §3.6.2, p. 196] (book p. 196; PDF p. 214); [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216).

### [U3b:3.6.2-a] Multi-argument `FUN` syntax and closed-abstraction restriction
- Statement: originally designed for object-oriented languages (`[2]` in [PPA Bibliography, p. 439]
  (book p. 439; PDF p. 452)), CPA is formulated on non-recursive `m`-argument (`m > 0`) `FUN` terms:
  ```text
  t ::= ··· | fn x₁, ···, x_m => e_b | e₀(e₁, ···, e_m)
  ```
  subject to the closed-function requirement `FV(fn x₁, ···, x_m => e_b) = ∅` (generalised to open and
  recursive functions in [PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227)).
- Citation: [PPA §3.6.2, p. 196] (book p. 196; PDF p. 214)

### [U3b:3.6.2-b] Rephrased `m`-ary `0-CFA` specification on Table 3.1
- Statement: adapting abstract `Table 3.1` (explicitly *not* syntax-directed `Table 3.5`):
  ```text
  (Ĉ, ρ̂) ⊨ (fn x₁, ···, x_m => e_b)^ℓ iff {fn x₁, ···, x_m => e_b} ⊆ Ĉ(ℓ)

  (Ĉ, ρ̂) ⊨ (t₀^{ℓ₀}(t₁^{ℓ₁}, ···, t_m^{ℓ_m}))^ℓ
    iff  (Ĉ, ρ̂) ⊨ t₀^{ℓ₀} ∧ (Ĉ, ρ̂) ⊨ t₁^{ℓ₁} ∧ ··· ∧ (Ĉ, ρ̂) ⊨ t_m^{ℓ_m} ∧
         ∀(fn x₁, ···, x_m => t_b^{ℓ_b}) ∈ Ĉ(ℓ₀) :
           Ĉ(ℓ₁) × ··· × Ĉ(ℓ_m) ⊆ ρ̂(x₁) × ··· × ρ̂(x_m) ∧
           (Ĉ, ρ̂) ⊨ t_b^{ℓ_b} ∧
           Ĉ(ℓ_b) ⊆ Ĉ(ℓ)
  ```
  In the case where **no `Ĉ(ℓ_i)` is empty**, `Ĉ(ℓ₁) × ··· × Ĉ(ℓ_m) ⊆ ρ̂(x₁) × ··· × ρ̂(x_m)` is equivalent to
  `Ĉ(ℓ₁) ⊆ ρ̂(x₁) ∧ ··· ∧ Ĉ(ℓ_m) ⊆ ρ̂(x_m)` (finding F-U3b-06).
- Citation: [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215)

### [U3b:3.6.2-c] CPA domains, `(Ĉ, ρ̂) ⊨_{CPA}^δ e` clauses, template pool, and lazy product expansion
- Statement: with `Val̂ = 𝒫(Term)` (no `CEnv` needed since abstractions are closed):
  ```text
  δ ∈ Δ     = Term^m = Term × ··· × Term      (m times)
  ρ̂ ∈ Env̂   = (Var × Δ) → Val̂
  Ĉ ∈ Cachê = (Lab × Δ) → Val̂
  ```
  Key CPA clauses (transcribed verbatim from `p-215.png`, preserving both the missing `)` before `^ℓ` on the
  `[app]` LHS and the omitted `, δ_b` arguments on `ρ̂(x₁) × ··· × ρ̂(x_m)`; finding F-U3b-05):
  ```text
  (Ĉ, ρ̂) ⊨_{CPA}^δ x^ℓ iff ρ̂(x, δ) ⊆ Ĉ(ℓ, δ)

  (Ĉ, ρ̂) ⊨_{CPA}^δ (fn x₁, ···, x_m => e_b)^ℓ iff {fn x₁, ···, x_m => e_b} ⊆ Ĉ(ℓ, δ)

  (Ĉ, ρ̂) ⊨_{CPA}^δ (t₀^{ℓ₀}(t₁^{ℓ₁}, ···, t_m^{ℓ_m})^ℓ
    iff  (Ĉ, ρ̂) ⊨_{CPA}^δ t₀^{ℓ₀} ∧ (Ĉ, ρ̂) ⊨_{CPA}^δ t₁^{ℓ₁} ∧ ··· ∧ (Ĉ, ρ̂) ⊨_{CPA}^δ t_m^{ℓ_m} ∧
         ∀(fn x₁, ···, x_m => t_b^{ℓ_b}) ∈ Ĉ(ℓ₀, δ) :
           ∀δ_b ∈ Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ) :
             {δ_b} ⊆ ρ̂(x₁) × ··· × ρ̂(x_m) ∧
             (Ĉ, ρ̂) ⊨_{CPA}^{δ_b} t_b^{ℓ_b} ∧
             Ĉ(ℓ_b, δ_b) ⊆ Ĉ(ℓ, δ)
  ```
  - *Templates & memoisation* (p. 198): each `(Ĉ, ρ̂) ⊨_{CPA}^{δ_b} t_b^{ℓ_b}` obligation is stored as a
    **template** in a global pool (added only if absent), ensuring each `(callee, argument-tuple)` pair is
    analysed at most once across all call sites.
  - *Lazy monotone expansion* (p. 198): `Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ)` grows monotonically as each `Ĉ(ℓ_i, δ)`
    grows, enabling lazy demand-driven template instantiation.
- Citation: [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215); [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216)

### [U3b:3.6.2-d] Interprocedural analysis revisited (`U5`): §2.5.5 Small Assumption Sets ↔ §3.6.2 CPA
- Statement: in §2.5.5 ([PPA §2.5.5, p. 100] (book p. 100; PDF p. 119); [PPA §2.5.5, p. 101] (book p. 101; PDF p. 120)), *small assumption sets*
  use `A_∘, A_• : Lab → (Δ → L)` with `L = 𝒫(D)` and `Δ = D`. Currying unary (`m = 1`) CPA gives
  `Ĉ : Lab → Δ → Val̂` and `ρ̂ : Var → Δ → Val̂` with `Val̂ = 𝒫(Term)` and `Δ = Term = D`, showing that §2.5.5
  small assumption sets and CPA are variations over the same theme.
- Citation: [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216)

### Findings (3.6.2)
- F-U3b-05 (`[Source Erratum — Missing Context Argument & Missing Parenthesis]`): on p. 197 (`p-215.png`),
  although `Env̂ = (Var × Δ) → Val̂` and `[var]` writes `ρ̂(x, δ)`, the CPA `[app]` clause prints
  `{δ_b} ⊆ ρ̂(x₁) × ··· × ρ̂(x_m)` omitting `, δ_b` (must read `{δ_b} ⊆ ρ̂(x₁, δ_b) × ··· × ρ̂(x_m, δ_b)`), and
  prints `(t₀^{ℓ₀}(t₁^{ℓ₁}, ···, t_m^{ℓ_m})^ℓ` missing the second closing `)` before `^ℓ`; p. 198 also writes
  `Δ = Term` (implicitly specialising `Δ = Term^m` to `m = 1`).
  [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215); [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216)
- F-U3b-06 (`[Empty-Factor Product Trap]`): in both `m`-ary `0-CFA` and CPA (p. 197), if *any* argument `i`
  has `Ĉ(ℓ_i, δ) = ∅` — which occurs for every primitive constant `c^{ℓ_i}` in pure `Term`-only CFA! — the
  Cartesian product `Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ)` collapses to `∅`, vacuously skipping parameter binding and
  body analysis `[derived]`; practical CPA engines must populate non-empty abstract tokens/types (`Data` from
  §3.5.1 or class tags `[2]`) for primitive arguments.
  [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215)

### Projections (3.6.2)
- cs_theory: Quantifying elementwise over tuples `∀δ_b ∈ Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ)` is the exact functional
  mechanism (`U5`) that rescues §2.5.5 *large assumption sets* (`Δ = 𝒫(D)`, non-monotone `BKL-003`) via
  *small assumption sets* (`Δ = D = Term^m`), exploiting complete additivity of `𝒫(Term)^m` [derived]
  [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215); [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216).
- swe_architecture: Unlike `k`-CFA (which loses caller separation after `k + 1` shared wrapper calls), CPA
  is **call-depth invariant** — `id(a)` and `id(b)` stay separate through arbitrarily deep helper chains —
  closely related to OO receiver/type sensitivity (`m`-obj [external: Milanova et al. 2005; Smaragdakis et al.
  2011]) and modern SAST value-specialised dataflow (`CodeQL` / `WALA` / `Doop` [external])
  [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215); [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216).
- practical_debugging: If a CPA solver silently drops calls to mixed `(int, closure)` functions like
  `apply_n(3, fn x => x)`, check F-U3b-06 first (`Ĉ(ℓ₁, δ) = ∅` on `3` annihilates `∅ × {fn x => x} = ∅`!),
  and verify `[app]` binds `ρ̂(x_i, δ_b)` rather than `ρ̂(x_i, δ)` [derived]
  [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215).
- cyber: CPA cleanly separates `sanitize_or_forward(clean)` from `sanitize_or_forward(tainted)` across shared
  middleware wrappers without false-positive taint smearing `[external: taint]`; however, an `m`-ary sink receiving `K` distinct
  abstractions per slot spawns **`K^m` templates** (`CWE-400` megamorphic blowup [external]), requiring
  per-call-site cardinality caps that widen megamorphic parameters back to summary tokens [derived]
  [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216).

---

## Chapter 3 Concluding Remarks

Context: historical origins of `k`-CFA and Closure Analysis, dynamic vs static scoping/contours, OO/concurrent/logic
paradigms, Set-Constraint Based Analysis (`C^{-i}(S)`, `¬S`, Banach's Theorem), empirical `1-CFA` vs `0-CFA`
speedups, and lazy conditional-constraint solving
[PPA Chapter 3 Concluding Remarks, p. 198] (book p. 198; PDF p. 216); [PPA Chapter 3 Concluding Remarks, p. 202] (book p. 202; PDF p. 220).

### [U3b:CR-a] Functional Control Flow Analysis, contours, open systems, and SOS rationale
- Statement:
  - *Origins & complexity*: `k`-CFA originates with Shivers `[156, 157, 158]` [PPA Chapter 3 Concluding Remarks, p. 198] (book p. 198; PDF p. 216), with `0-CFA`-like precursors
    `[163, 136, 57, 56]` and Sestoft's *Closure Analysis* `[152]`. Jagannathan & Weeks `[79]` clarified
    `k`-CFA and polynomial `k`-CFA, established **exponential complexity of `k`-CFA for `k > 0`**, and linked
    Heintze's *Set Based Analysis* `[70]` to `0-CFA`. Nielson & Nielson `[122]` introduced *uniform `k`-CFA*
    (and distinct-call compression, [PPA Exercise 3.15, p. 208] (book p. 208; PDF p. 226)).
  - *Scoping & contours*: `Table 3.1` coalesces distinct lexical bindings sharing a variable name, behaving
    like dynamic scoping unless variables are α-distinct ([PPA Exercise 3.7, p. 207] (book p. 207; PDF p. 225)).
    Context tokens (*mementoes*, *tokens*, *contours*) capture either the *dynamic* call chain (§2.5.4 call
    strings; `CPA` `[2]`, `[external: Agesen]`, = §2.5.5 small assumption sets) or the *static* chain (Jagannathan & Wright's
    *polymorphic splitting* `[80]`, given coinductive abstract specifications in `[122]`).
  - *CFA+DFA, open systems, & SOS choice*: §3.5's CFA+DFA extends to imperative references in `Mini Project 3.4`
    (`[126]`; some authors reserve `0-CFA` for analyses tracking data-flow and evaluation order as in
    `Exercises 3.3, 3.14`). Starting from abstract specifications (`⊨`) rather than directly from
    syntax-directed ones (`[80, 122]`) cleanly supports *open systems* (interfacing with library routines),
    reachability (`[21, 60]`, `Mini Project 3.1`), and Chapter 4 Abstract Interpretation. Small-step
    environment-closure SOS (`[125]`) was chosen over big-step semantics (to cover looping programs) and over
    β-substitution (so function bodies in `Term` stay unmutated), confining `close`/`bind` to §3.2.
- Citation: [PPA Chapter 3 Concluding Remarks, p. 198] (book p. 198; PDF p. 216); [PPA Chapter 3 Concluding Remarks, p. 200] (book p. 200; PDF p. 218)

### [U3b:CR-b] Object-oriented, concurrent, and logic programming paradigms
- Statement:
  - *Object-oriented languages*: track *objects* (classes/allocations) instead of functions (`[3, 124, 137]`,
    or Chapter 2-style data-flow `[178, 139]`). Advanced OO analyses combine `k`-CFA-like context with an
    *abstract store* (`[133]`): achieving precision requires **per-program-point local abstract stores** plus
    **abstract reference counts** to enable strong updates (`"kill"` components as in Chapter 2, [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134)).
  - *Concurrent & logic languages*: concurrent functional languages with dynamic processes and shared
    locations/channels appear in `[78, 57, 60, 22, 23]`; set-based analysis originated in logic programming
    `[72, 73]`.
- Citation: [PPA Chapter 3 Concluding Remarks, p. 200] (book p. 200; PDF p. 218)

### [U3b:CR-c] Set-Constraint Based Analysis, Banach's Theorem, empirical `1-CFA` vs `0-CFA`, and lazy solving
- Statement:
  - *Three-step decoupling*: separating (i) abstract acceptability, (ii) constraint generation, and (iii)
    least-solution solving makes the solver independent of constraint origin and supports forward, backward,
    and mixed-direction analyses uniformly.
  - *Set-constraint syntax* (`[72, 7]`, history `[143, 84]`): general inclusions `S₁ ⊆ S₂` over set
    expressions `S`, set variables `V`, and constructors `C`:
    ```text
    S ::= V | ∅ | S₁ ∪ S₂ | S₁ ∩ S₂ | C(S₁, ···, S_n)
        | (S₁ ⊆ S₂) ⇒ S₃ | (S₁ ≠ ∅) ⇒ S₂ | C^{-i}(S) | ¬S | ···
    V ::= X | Y | ···
    C ::= true | false | 0 | ··· | cons | nil | ···
    ```
    Non-nullary constructors record data-structure shapes (`cons(S₁, S₂) ∪ nil`); **projection** `C^{-i}(S)`
    selects `i`-th components of `C`-terms (e.g. `cons^{-1}(S)` selects list heads) and is expressive enough
    to encode conditional constraints; **complement** `¬S` invalidates monotonicity so **Tarski's Fixed Point
    Theorem no longer applies** and **Banach's Fixed Point Theorem** may be needed instead.
  - *Complexity vs empirical speed*: worst-case bounds vary by operator fragment (`[6, 135, 28]`; cubic
    fragments `[70, 10]`), yet Jagannathan & Wright `[80]` demonstrated empirically that **`1-CFA` can run
    faster than `0-CFA` in practice** despite exponential vs polynomial worst-case complexity, because
    `0-CFA` explores most of its polynomial state space while `1-CFA`'s precision restricts exploration to a
    small fraction of its exponential space.
  - *Two-step lazy solver* (`[9]`, pp. 201–202): (1) dynamically expand conditional constraints as their
    guards become satisfied until no further expansion is possible; (2) remove all conditional constraints and
    solve the remaining unconditional constraints for their least solution. In practice this *lazy* strategy
    is likely much faster than `Tables 3.6–3.7`'s *eager* pre-instantiation over a guessed universe `Term_⋆`.
- Citation: [PPA Chapter 3 Concluding Remarks, p. 200] (book p. 200; PDF p. 218); [PPA Chapter 3 Concluding Remarks, p. 202] (book p. 202; PDF p. 220)

### Findings (Concluding Remarks)
- F-U3b-07: p. 199 prints `"based in [126]"` (`in` for `on`) and `"allow to interface"`; p. 200 bottom prints
  `"we have have taken"` (duplicated `have`); p. 201 prints `"benchmark results of Jaganathan and Wright [80]
  shows"` (single-`n` `"Jaganathan"` for `"Jagannathan"` and singular `"shows"`).
  [PPA Chapter 3 Concluding Remarks, p. 199] (book p. 199; PDF p. 217); [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219)

### Projections (Concluding Remarks)
- cs_theory: Positive set constraints with `C(...)` and `C^{-i}(S)` correspond to regular tree grammars /
  monadic Ackermannian logic (`NEXPTIME`-complete in full generality `[28]` [external], `O(n³)` on
  Heintze–McAllester / CFL-reachability fragments `[70, 10]`), whereas `¬S` exits order-theoretic Tarski
  fixpoints for ultrametric contraction mappings (`Banach's Theorem` [external: MacQueen–Plotkin–Sethi])
  [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219).
- swe_architecture: Production whole-program pointer/call-graph engines (`WALA`, `Doop`/`Soufflé`, `SVF` [external])
  universally adopt `[9]`'s (`[external: Aiken et al.]`) lazy on-the-fly conditional expansion rather than `Table 3.6`'s eager
  `|Apps| × |Term_⋆|` cross-product materialisation [PPA Chapter 3 Concluding Remarks, p. 201]
  (book p. 201; PDF p. 219); [PPA Chapter 3 Concluding Remarks, p. 202] (book p. 202; PDF p. 220).
- practical_debugging: Before escalating from `0-CFA` to `1-CFA` when triaging call-graph supernodes, always
  α-uniquify bound variable IDs first (`p. 199`, `Exercise 3.7`); if a polymorphic hub (`id`, `map`, event
  bus) still causes `O(M²)` cross-edge saturation, upgrading to `1-CFA` or `CPA` often *reduces* wall-clock
  runtime (`[80]`) [PPA Chapter 3 Concluding Remarks, p. 199] (book p. 199; PDF p. 217); [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219).
- cyber: Sound heap taint / capability revocation (`"strong kill"` [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134) on `x.f := clean`, `p. 200` `[133]`, `[external: taint / capability]`)
  requires **both** per-point local abstract stores and singleton reference-count / must-not-alias proofs;
  performing strong kills on a summary allocation site `π` unsoundly erases taint `[external]` on aliased heap objects
  [PPA Chapter 3 Concluding Remarks, p. 200] (book p. 200; PDF p. 218).

---

## Mini Projects (`3.1`–`3.4`)

Context: four mini projects extending Chapter 3 with reachability-guarded syntax-directed CFA (`3.1`),
algebraic data structures (`3.2`), an SML/Haskell prototype (`3.3`), and flow-sensitive imperative references
(`3.4`) [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220).

### Mini Project 3.1 — Reachability Analysis
- Statement: `Table 3.5` analyses every subexpression of `e_⋆` "exactly once" rather than "at most once".
  Introduce an *abstract reachability component*:
  ```text
  R̂ ∈ Reach = Lab → 𝒫({on})
  (Ĉ, ρ̂, R̂) ⊨'_s e
  ```
  so `fn x => t₀^{ℓ₀}` has `{on} ⊆ R̂(ℓ₀)` iff applied somewhere, and the recursive body check
  `(Ĉ, ρ̂, R̂) ⊨'_s t₀^{ℓ₀}` (misprinted `⊨_s` without prime on line 10; finding F-U3b-08) is performed iff
  `{on} ⊆ R̂(ℓ₀)` (based on `[60]`):
  1. Modify `Table 3.5` to incorporate `R̂`.
  2. Prove the analogue of Proposition 3.18: if `(Ĉ, ρ̂, R̂) ⊨'_s t_⋆^{ℓ_⋆}`, `{on} ⊆ R̂(ℓ_⋆)`, and
     `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` then `(Ĉ, ρ̂) ⊨ t_⋆^{ℓ_⋆}`.
  3. Determine whether `((Ĉ, ρ̂) ⊨ e_⋆ ⇒ ∃R̂ : (Ĉ, ρ̂, R̂) ⊨'_s e_⋆)` and
     `((Ĉ, ρ̂) ⊨ e_⋆ ∧ (Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤) ⇒ ∃R̂ : (Ĉ, ρ̂, R̂) ⊨'_s e_⋆)` hold in general. `■`
- Side conditions: `[derived]` in Task 3, **both implications fail in general when `e_⋆` has shared labels**
  (because `Reach = Lab → 𝒫({on})` keys on `ℓ₀ ∈ Lab`: if a called `(fn x => x^1)^2` and a dead
  `(fn y => y^1)^3` share body label `1`, `{on} ⊆ R̂(1)` forces `⊨'_s` to constrain dead `y^1`), whereas on
  **uniquely labelled** `e_⋆` setting `R̂(ℓ) = {on}` iff `(Ĉ, ρ̂) ⊨ t^ℓ` validates `(Ĉ, ρ̂, R̂) ⊨'_s e_⋆`.
- Citation: [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220)

### Mini Project 3.2 — Data Structures
- Statement: extend `FUN` with `n`-ary data constructors `C ∈ Constr` (grammar erased in OCR, verified on
  `p-221.png`):
  ```text
  e ::= ··· | C(e₁, ···, e_n)^ℓ | (case e₀ of C(x₁, ···, x_n) => e₁ or x => e₂)^ℓ
  ```
  illustrated with `Constr = {cons, nil}` (`nil()` `0`-ary) on list `append` and `rev`:
  ```text
  let append = fun app xs => fn ys =>
                 case xs of cons(z,zs) => cons(z,app zs ys)
                         or xs => ys
  in fun rev xs => case xs of cons(y,ys) =>
                          append (rev ys) (cons(y,nil()))
                        or xs => nil()
  ```
  Track field creation points via `Val̂ = 𝒫(Term ∪ {C(ℓ₁, ···, ℓ_n) | C ∈ Constr, ℓ₁, ···, ℓ_n ∈ Lab})`:
  1. Develop a syntax-directed `Table 3.5` analogue.
  2. Modify `Tables 3.6–3.7` (constraint generation & graph solver).
  3. *For the more ambitious*: identify difficulties in developing a `Table 3.1` abstract specification
     (`[derived]`: small-step SOS erases/rewrites outer labels during evaluation, breaking `Fact 3.11` once
     labels `ℓ_i` are embedded inside `Val̂` via `C(ℓ₁, ···, ℓ_n)`, cf. `Exercise 3.6`). `■`
- Citation: [PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221)

### Mini Project 3.3 — A Prototype Implementation
- Statement: implement pure `0-CFA` (§§3.3–3.4) in Standard ML or Haskell over:
  ```sml
  type var       = string
  type label     = int
  datatype const = Num of int | True | False
  datatype exp   = Label of term * label
  and term       = Const of const | Var of var
                 | Fn of var * exp | Fun of var * var * exp
                 | App of exp * exp | If of exp * exp * exp
                 | Let of var * exp * exp | Op of string * exp * exp
  ```
  (1) Define `constraints` for conditional constraints and implement §3.4 constraint generation; (2) choose
  data structures for worklist `W` and arrays `D`, `E` and implement §3.4's graph solver; (*ambitious*) add
  §3.5 data flow or §3.6 context sensitivity. `■`
- Citation: [PPA Mini Project 3.3, p. 204] (book p. 204; PDF p. 222)

### Mini Project 3.4 — Imperative Constructs
- Statement: extend `FUN` with ML-style heap references created at program points `π ∈ Pnt` (based on `[126]`,
  grammar and judgement erased in OCR, verified on `p-222.png`–`p-223.png`):
  ```text
  e ::= ··· | (new_π x := e₁ in e₂)^ℓ | (! x)^ℓ | (x := e₀)^ℓ | (e₁ ; e₂)^ℓ
  ```
  (`e₁ ; e₂` equivalent to `let x = e₁ in e₂` for `x ∉ FV(e₂)`). Formulate flow-sensitive acceptability:
  ```text
  (Ĉ, ρ̂, Ŝ_∘, Ŝ_•) ⊨_{me} e
  ```
  with `Ĉ : Lab → Val̂`, `ρ̂ : Var → Val̂` (non-reference variables), pre/post abstract heap stores
  `Ŝ_∘, Ŝ_• : Lab → (Pnt → Val̂)`, and reference creation-point map `me : Var → Pnt` over e.g.
  `Val̂ = 𝒫(Term) × L`, guided by an extended SOS and optionally §3.6 contexts. `■`
- Citation: [PPA Mini Project 3.4, p. 204] (book p. 204; PDF p. 222); [PPA Mini Project 3.4, p. 205] (book p. 205; PDF p. 223)

### Findings (Mini Projects)
- F-U3b-08: on p. 202, `Mini Project 3.1` introduces `(Ĉ, ρ̂, R̂) ⊨'_s e` (with prime `'`) yet writes
  `(Ĉ, ρ̂, R̂) ⊨_s t₀^{ℓ₀}` without prime two lines below, and alternates `t_⋆^{ℓ_⋆}` (Task 2) with `e_⋆`
  (Task 3). [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220)
- F-U3b-09: `Mini Project 3.2` (p. 203) and `Mini Project 3.4` (p. 204) extend `e ::= ··· | (...)^ℓ` directly
  rather than `t ::= ···` (unlike §3.1 `e ::= t^ℓ` and §3.6.2 `t ::= ···`), and `Mini Project 3.2` uses `0`-ary
  `nil()` under `"n-ary data constructor"` (`n ≥ 0`).
  [PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221); [PPA Mini Project 3.4, p. 204] (book p. 204; PDF p. 222)

### Projections (Mini Projects)
- cs_theory: `Mini Project 3.2` bounds unbounded recursive heap trees (`rev` on lists) into finite domain
  `Constr_⋆ × Lab_⋆^{arity}` (a finite tree-automaton abstraction [external]), while `Mini Project 3.4`
  combines flow-insensitive functional `(Ĉ, ρ̂)` with flow-sensitive store transformers `Ŝ_∘ → Ŝ_•` (`U4`
  bridge to Chapter 2 `WHILE` and Chapter 5 §5.4 Side Effect Analysis)
  [PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221); [PPA Mini Project 3.4, p. 204] (book p. 204; PDF p. 222); [PPA Mini Project 3.4, p. 205] (book p. 205; PDF p. 223).
- swe_architecture: `Mini Project 3.1`'s `R̂(ℓ) ∈ 𝒫({on})` turns whole-AST constraint generation into
  root-seeded on-the-fly reachability, eliminating dead-library noise at `O(1)` extra bit per label
  [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220).
- practical_debugging: If first-class references (`ref` cells passed as function arguments or stored inside
  other refs) are added to `Mini Project 3.4`, `me : Var → Pnt` is too narrow — lift reference locations into
  `Val̂ = 𝒫(Term ∪ Pnt) × L` so aliases flow through `(Ĉ, ρ̂)` [derived]
  [PPA Mini Project 3.4, p. 205] (book p. 205; PDF p. 223).
- cyber: Constructor-origin tuples `C(ℓ₁, ···, ℓ_n)` (`Mini Project 3.2`) track field-sensitive provenance of
  nested deserialized payloads (`CWE-502` [external]), while `Ŝ_∘, Ŝ_• : Lab → (Pnt → Val̂)` (`Mini Project 3.4`)
  tracks flow-sensitive heap mutation across closures (defaulting to weak updates `⊔` `[external]` unless singleton
  reference counts justify strong kills [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134)) [PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221);
  [PPA Mini Project 3.4, p. 205] (book p. 205; PDF p. 223).

---

## Exercises (`3.1`–`3.17`)

Context: 17 unstarred exercises covering finite domain restriction, CBV vs CBN order, non-upward-closure of
`⊨` (`(3.8)` vs `(3.9)`), `Val̂ = 𝒫(Exp)` failure, lexical vs α-renamed scoping, `⊨_s` uniqueness and
incompleteness, equational constraints `𝒞_⋆^=⟦e_⋆⟧`, stuttering call-string compression, first-order recursion
schemes, and open/recursive `CPA` [PPA Exercise 3.1, p. 205] (book p. 205; PDF p. 223).

### Exercise 3.1 — Labelling and verifying 0-CFA on higher-order dispatch
- Statement: Add labels to `let f = fn x => x 1 in let g = fn y => y+2 in let h = fn z => z+3 in (f g) + (f h)`,
  guess `(Ĉ, ρ̂)`, and verify `(Ĉ, ρ̂) ⊨ e` via `Table 3.1`. `■`
- Citation: [PPA Exercise 3.1, p. 205] (book p. 205; PDF p. 223)

### Exercise 3.2 — Restricting Table 3.1 to finite `Cachê_⋆ × Env̂_⋆`
- Statement: Restrict `Table 3.1` to finite `Val̂_⋆ = 𝒫(Term_⋆)`, `Env̂_⋆ = Var_⋆ → Val̂_⋆`,
  `Cachê_⋆ = Lab_⋆ → Val̂_⋆` for `e_⋆`, and show `Table 3.1` remains well-defined on `Cachê_⋆ × Env̂_⋆`
  (`[derived]`: every abstraction in `Ĉ(ℓ₁) ⊆ Term_⋆` is a subterm of `e_⋆`, keeping all body labels and
  variables inside `Lab_⋆` and `Var_⋆`). `■`
- Citation: [PPA Exercise 3.2, p. 206] (book p. 206; PDF p. 224)

### Exercise 3.3 — Left-to-right call-by-value demand guard in `[app]`
- Statement: Modify `Table 3.1` `[app]` for left-to-right CBV order so operand `t₂^{ℓ₂}` is skipped when
  `t₁^{ℓ₁}` produces no closures (misprinted `"cannot produced"`; finding F-U3b-10), and find a program where
  modified `⊨` accepts results rejected by `Table 3.1` (`[derived]`: e.g. `(loop^1 (fn x => x^2)^3)^4` with
  `Ĉ(1) = Ĉ(3) = ∅`). `■`
- Citation: [PPA Exercise 3.3, p. 206] (book p. 206; PDF p. 224)

### Exercise 3.4 — Exact `(3.8)` vs upward-closed `(3.9)` acceptability
- Statement (both displayed formulas erased in OCR, verified on `p-224.png`):
  ```text
  (Ĉ, ρ̂) ⊨ e                                            (3.8)
  ∃(Ĉ', ρ̂') : (Ĉ', ρ̂') ⊨ e  ∧  (Ĉ', ρ̂') ⊑ (Ĉ, ρ̂)      (3.9)
  ```
  Show `(3.8) ⇒ (3.9)` **but not vice versa**, and discuss which is preferable (`[derived]`: `⊨` is *not
  upward-closed* because adding spurious `fn x => (fn y => y^4)^5` to `Ĉ(1)` on `(7^1 8^2)^3` while keeping
  `Ĉ(3) = ∅` satisfies `(3.9)` via `(∅, ∅)` yet violates `(3.8)` `[app]`; `(3.8)` is preferable because every
  recorded target is internally self-consistent for `Theorem 3.10` and open-system checks). `■`
- Citation: [PPA Exercise 3.4, p. 206] (book p. 206; PDF p. 224)

### Exercise 3.5 — Coarse recursive-binding inclusion `Ĉ(ℓ₁) ⊆ ρ̂(f)` in `[app]`
- Statement: Replace `(fun f x => t₀^{ℓ₀}) ∈ ρ̂(f)` in `Table 3.1` `[app]` with `Ĉ(ℓ₁) ⊆ ρ̂(f)`; adapt
  `Theorem 3.10` and compare precision (`[derived]`: strictly coarser whenever `Ĉ(ℓ₁)` holds multiple
  closures). `■`
- Citation: [PPA Exercise 3.5, p. 206] (book p. 206; PDF p. 224)

### Exercise 3.6 — Failure of Fact 3.11 and Theorem 3.10 under `Val̂ = 𝒫(Exp)`
- Statement: Replace `Val̂ = 𝒫(Term)` by `Val̂ = 𝒫(Exp)` (retaining outer labels on functions) and show
  `Fact 3.11` (and `Theorem 3.10`) fails (`[derived]`: SOS `[bind₂]`/`[if₂]`/`[var]` relabels `it^{ℓ₁} → it^{ℓ₂}`,
  whereas `Ĉ(ℓ₁) ⊆ Ĉ(ℓ₂)` carries `(fn x => e₀)^{ℓ₁}` rather than `(fn x => e₀)^{ℓ₂}`). `■`
- Citation: [PPA Exercise 3.6, p. 206] (book p. 206; PDF p. 224); [PPA Exercise 3.6, p. 207] (book p. 207; PDF p. 225)

### Exercise 3.7 — Alpha-renaming sensitivity and static-scoping faithful 0-CFA
- Statement: Observe `((fn x => x^1)^2 (fn y => y^3)^4)^5 =_α ((fn x => x^1)^2 (fn x => x^3)^4)^5` preserves
  SOS semantics yet degrades `Table 3.1` precision when `x` is bound twice; design a lexically faithful
  `0-CFA` coinciding with `Table 3.1` on uniquely bound programs. `■`
- Citation: [PPA Exercise 3.7, p. 207] (book p. 207; PDF p. 225)

### Exercise 3.8 — Call-by-name / lazy SOS soundness invariance of Table 3.1
- Statement: Modify `Tables 3.2–3.3` to *call-by-name* / *lazy* SOS (`ρ : Var → ITerm`, drop `[app₂]` and
  `[let₁]`, `[var]` `ρ ⊢ x^ℓ → it^ℓ if x ∈ dom(ρ) and it = ρ(x)`), prove `Theorem 3.10` still holds for
  `Table 3.1`, and deduce that `Table 3.1` cannot exploit CBV-only strictness properties. `■`
- Citation: [PPA Exercise 3.8, p. 207] (book p. 207; PDF p. 225)

### Exercise 3.9 — Fixed-point uniqueness of syntax-directed `Table 3.5`
- Statement: Prove any two relations `⊨'_s` and `⊨''_s` satisfying `Table 3.5` coincide by structural
  induction on `e` (`lfp(𝒬_s) = gfp(𝒬_s)`). `■`
- Citation: [PPA Exercise 3.9, p. 207] (book p. 207; PDF p. 225)

### Exercise 3.10 — Necessity of `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` in Proposition 3.18
- Statement: Determine whether `(Ĉ, ρ̂) ⊨_s e_⋆ ⇒ (Ĉ, ρ̂) ⊨ e_⋆` holds without Proposition 3.18's bound
  `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` (`[derived]`: **false** — an alien `fn x => t₀^{ℓ₀} ∉ Term_⋆` in `Ĉ(ℓ₁)` is
  unchecked by `⊨_s e_⋆` yet required to satisfy `⊨ t₀^{ℓ₀}` by `⊨ e_⋆`). `■`
- Citation: [PPA Exercise 3.10, p. 207] (book p. 207; PDF p. 225)

### Exercise 3.11 — Counterexamples to completeness `⊨ e_⋆ ⇒ ⊨_s e_⋆`
- Statement: Give counterexamples disproving `(Ĉ, ρ̂) ⊨ e_⋆ ⇒ (Ĉ, ρ̂) ⊨_s e_⋆` both with and without
  `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` (`[derived]`: any uncalled abstraction `(fn x => ((fn y => y^1)^2 (fn z => z^3)^4)^5)^6`
  with `Ĉ(2) = ∅`). `■`
- Citation: [PPA Exercise 3.11, p. 207] (book p. 207; PDF p. 225)

### Exercise 3.12 — Direct subject-reduction proof for `Table 3.5` (`⊨_s`)
- Statement: Extend `Table 3.5` (`⊨_s`) to `bind` and `close` and prove subject reduction
  `ρ ℛ ρ̂ ∧ ρ ⊢ ie → ie' ∧ (Ĉ, ρ̂) ⊨_s ie ⇒ (Ĉ, ρ̂) ⊨_s ie'` directly (`[derived]`: `[close]` must carry
  `(Ĉ, ρ̂) ⊨_s e₀` — and `{fun f x => e₀} ⊆ ρ̂(f)` — so `[app_fn]`/`[app_fun]` unpack validated bodies without
  `Term_⋆` bounds). `■`
- Citation: [PPA Exercise 3.12, p. 208] (book p. 208; PDF p. 226)

### Exercise 3.13 — Grouped equational constraints `𝒞_⋆^=⟦e_⋆⟧` vs inclusions `𝒞_⋆⟦e_⋆⟧`
- Statement: Collapse all `n ≥ 1` inclusions `ls_i ⊆ rhs` in `𝒞_⋆⟦e_⋆⟧` sharing `rhs` into
  `ls₁ ∪ ··· ∪ ls_n = rhs` in `𝒞_⋆^=⟦e_⋆⟧`; prove `⊨_c 𝒞_⋆^=⟦e_⋆⟧ ⇒ ⊨_c 𝒞_⋆⟦e_⋆⟧`, and prove the converse
  holds when `(Ĉ, ρ̂)` is the **least** solution of `𝒞_⋆⟦e_⋆⟧` (finding F-U3b-11). `■`
- Citation: [PPA Exercise 3.13, p. 208] (book p. 208; PDF p. 226)

### Exercise 3.14 — Demand-driven powerset CFA+DFA and syntax-directed counterpart
- Statement: Combine `Exercise 3.3` demand-gating with `Table 3.8` (§3.5.1), construct a syntax-directed
  counterpart, and compare with `Exercises 3.10–3.11`. `■`
- Citation: [PPA Exercise 3.14, p. 208] (book p. 208; PDF p. 226)

### Exercise 3.15 — Stuttering-compressed call strings (`[1, 2, 2, 1, 1] ↦ [2, 1]`)
- Statement: Modify `Table 3.10` so contexts record the last `k` calls differing from the immediately
  preceding call (`[1, 2, 2, 1, 1]` becomes `[1, 1]` in `2-CFA` vs `[2, 1]` here), preserving outer caller `2`
  across arbitrary self-recursion depth at `k = 2`. `■`
- Citation: [PPA Exercise 3.15, p. 208] (book p. 208; PDF p. 226)

### Exercise 3.16 — Uniform `k`-CFA on first-order recursion equation schemes
- Statement: For first-order CBV recursion schemes `define D_⋆ in e_⋆` (`f(x) = e`, `e ::= t^ℓ`,
  `t ::= c | x | f e | if e₀ then e₁ else e₂ | e₁ op e₂`, `fib(z)` example), formulate uniform `k`-CFA
  (`k = 0, 1`) and compare with §2.5 (`[derived]`: without closures or non-local free variables, `CEnv`
  vanishes and uniform `0-CFA`/`1-CFA` coincide with §2.5.4 call strings). `■`
- Citation: [PPA Exercise 3.16, p. 208] (book p. 208; PDF p. 226); [PPA Exercise 3.16, p. 209] (book p. 209; PDF p. 227)

### Exercise 3.17 — Extending CPA to open (`FV ≠ ∅`) and recursive `m`-ary functions
- Statement: Extend CPA (§3.6.2, misprinted `"Cartesian Production Algorithm"`, finding F-U3b-11) to open
  (`FV ≠ ∅`) and recursive `m`-ary functions via `(Ĉ, ρ̂) ⊨_δ^{ce} e` with `δ ∈ Δ = Term^m` and
  `ce ∈ CEnv = Var → Δ` (modifying `Table 3.10` `[app]`). `■`
- Citation: [PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227)

### [U3b:EX-ocr] OCR Erasure Audit Summary (PDF pp. 200–227)
- Statement: Six critical formal items in Unit 3b are erased or mangled in the `pdftotext` OCR layer of
  `ppa.pdf` and must always be read from visual page renders (or this shard):
  1. `Table 3.9` (`[op]`): entire right-hand side body after `[op]` completely erased in OCR
     [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206).
  2. `Example 3.28`: both displayed equations `ι_c = {d_c}` and `f_op(l₁, l₂) = ⋃{...}` completely erased
     [PPA Example 3.28, p. 186] (book p. 186; PDF p. 204).
  3. `Example 3.34`: expression display, `ρ̂'_id(x, 8) = {(fn y => y^6, ce₀)}`, and all three `⊨` obligations
     for `(f^3 f^4)^5` on p. 195 erased [PPA Example 3.34, p. 194] (book p. 194; PDF p. 212); [PPA Example 3.34, p. 195] (book p. 195; PDF p. 213).
  4. `Mini Projects 3.2 & 3.4`: syntax BNF displays (`p. 203`, `p. 204`) and `(Ĉ, ρ̂, Ŝ_∘, Ŝ_•) ⊨_{me} e`
     (`p. 205`) completely erased [PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221);
     [PPA Mini Project 3.4, p. 204] (book p. 204; PDF p. 222); [PPA Mini Project 3.4, p. 205] (book p. 205; PDF p. 223).
  5. `Exercises 3.4, 3.7, 3.10, 3.13, 3.16, 3.17`: **both** numbered displays `(3.8)` and `(3.9)` (`p. 206`,
     leaving only the equation numbers!) plus displayed formulas across `3.7, 3.10, 3.13, 3.16, 3.17` erased
     [PPA Exercise 3.4, p. 206] (book p. 206; PDF p. 224).
  6. Section 3.6 header (`p. 189`): OCR corrupts `"Adding Context Information"` to `"Adding Context
     lnformation"`, and strips hats, primes, and `⌈δ, ℓ⌉_k` ceilings across `Tables 3.8–3.10`
     [PPA §3.6, p. 189] (book p. 189; PDF p. 207); [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210).
- Citation: [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206); [PPA Exercise 3.4, p. 206] (book p. 206; PDF p. 224)

### Findings (Exercises)
- F-U3b-10: `Exercise 3.3` (p. 206) prints `"cannot produced"` (`produced` for `produce`); `Exercise 3.5`
  (p. 206) writes `(fun f x => t₀^{ℓ₀}) ∈ ρ̂(f)` where `Table 3.1` wrote `{fun f x => t₀^{ℓ₀}} ⊆ ρ̂(f)`;
  `Exercise 3.7` (p. 207) prints `"The operational semantics allow"` (`allow` for `allows`).
  [PPA Exercise 3.3, p. 206] (book p. 206; PDF p. 224); [PPA Exercise 3.5, p. 206] (book p. 206; PDF p. 224);
  [PPA Exercise 3.7, p. 207] (book p. 207; PDF p. 225)
- F-U3b-11: `Exercise 3.13` (p. 208) writes `ls_i ⊆ rhs` assuming guarded/expanded LHSs for conditional
  constraints in `𝒞_⋆⟦e_⋆⟧`; `Exercise 3.16` prints unspaced `f(x)= e` (p. 208) and `"defined in D"` omitting
  `⋆` from `D_⋆` (p. 209); `Exercise 3.17` (p. 209) prints **`"Cartesian Production Algorithm"`** for
  `"Cartesian Product Algorithm"`. [PPA Exercise 3.13, p. 208] (book p. 208; PDF p. 226);
  [PPA Exercise 3.16, p. 208] (book p. 208; PDF p. 226); [PPA Exercise 3.16, p. 209] (book p. 209; PDF p. 227);
  [PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227)

### Projections (Exercises)
- cs_theory: `Exercise 3.4` (`(3.8)` vs `(3.9)`), `Exercise 3.6` (`𝒫(Exp)`), `Exercise 3.8` (CBN invariance),
  and `Exercises 3.9–3.11` isolate why `Table 3.1` stores *unlabelled* `Term`s, why `⊨` is not upward-closed,
  and why `⊨_s ⇔ ⊨` fails on dead abstractions [PPA Exercise 3.4, p. 206] (book p. 206; PDF p. 224);
  [PPA Exercise 3.6, p. 206] (book p. 206; PDF p. 224).
- swe_architecture: `Exercise 3.15` (run-length call-string deduplication `[1, 2, 2, 1, 1] ↦ [2, 1]`, dual to
  [PPA Exercise 2.16, p. 138] (book p. 138; PDF p. 157)) and `Exercise 3.17` (`CPA` + `CEnv`) give practical
  hybrid contours for recursive functional/OO codebases [PPA Exercise 3.15, p. 208] (book p. 208; PDF p. 226);
  [PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227).
- practical_debugging: In Datalog/set-based `0-CFA` front-ends `[external: Datalog]`, keying `r(x)` by raw identifier string rather
  than unique AST binder ID (`Exercise 3.7`) silently merges every `fn x => ...` parameter in the program into
  one global bucket [PPA Exercise 3.7, p. 207] (book p. 207; PDF p. 225).
- cyber: `Exercise 3.10` demonstrates why unvalidated external/deserialized closures `[external]` `∉ Term_⋆` invalidate
  `⊨_s ⇒ ⊨`: any reflection, `eval`, or dynamic plugin loader `[external]` injecting code outside `Term_⋆` breaks closed-world
  call-graph soundness unless modelled via open-system stubs (§3.4.2, p. 182)
  [PPA Exercise 3.10, p. 207] (book p. 207; PDF p. 225).

---

## Gotcha Ledger

- G-U3b-01: Section 3.5 starts mid-page on book p. 182 (PDF p. 200) below Corollary 3.25's open-system remarks, and Chapter 3 ends at Exercise 3.17 on book p. 209 (PDF p. 227; book p. 210 is an absent blank verso, with `4` Mini Projects `3.1–3.4` and `17` Exercises `3.1–3.17`). [PPA §3.5, p. 182] (book p. 182; PDF p. 200); [PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227)
- G-U3b-02: Section 3.5 gives only declarative acceptability specifications (`⊨_d` in Table 3.8 and `⊨_D` in Table 3.9); syntax-directed and constraint-based counterparts require reachability tokens (`Mini Project 3.1`, `Exercise 3.14`). [PPA §3.5, p. 182] (book p. 182; PDF p. 200); [PPA Exercise 3.14, p. 208] (book p. 208; PDF p. 226)
- G-U3b-03: In `Table 3.8` (`Val̂_d = 𝒫(Term ∪ Data)`), `v̂₁ op̂ v̂₂` filters out `Term` elements via `∩ Data` (and `d_+` returns `∅` on booleans `tt`/`ff` in `Example 3.26`), while `[if]` gates `t₁^{ℓ₁}` on `d_true ∈ Ĉ(ℓ₀)` and `t₂^{ℓ₂}` on `d_false ∈ Ĉ(ℓ₀)` so DFA prunes dead CFA closures (`Example 3.27`). [PPA Example 3.26, p. 183] (book p. 183; PDF p. 201); [PPA Table 3.8, p. 184] (book p. 184; PDF p. 202)
- G-U3b-04: A valid solution `(Ĉ, ρ̂) ⊨_d e` of `Table 3.8` (or `(Ĉ, D̂, ρ̂, δ̂) ⊨_D e` of `Table 3.9`) does **not** project via `∩ Term` to a valid pure `0-CFA` solution `(Ĉ', ρ̂') ⊨ e` (`Table 3.1`), because `[if]` leaves untaken branch bodies unanalysed (`Ĉ(7) = ∅` in `Figure 3.6`). [PPA §3.5.1, p. 185] (book p. 185; PDF p. 203); [PPA Figure 3.6, p. 185] (book p. 185; PDF p. 203)
- G-U3b-05: Algorithmic termination for `§3.5.1` (`Table 3.8`) requires `Data` to be **finite**, and termination for `§3.5.2` (`Table 3.9`) requires the complete lattice `L` to satisfy the **Ascending Chain Condition (`ACC`)** (otherwise Chapter 4 widening is required). [PPA §3.5.1, p. 184] (book p. 184; PDF p. 202); [PPA §3.5.2, p. 187] (book p. 187; PDF p. 205)
- G-U3b-06: A monotone structure instance `(L, ℱ, ι., f.)` (§3.5.2) omits §2.3's static `flow` graph `F` (CFA computes flow dynamically) and replaces extremal `ι` and block transfer `f_ℓ` with constant map `ι_c` and binary operator map `f_op`. [PPA §3.5.2, p. 186] (book p. 186; PDF p. 204)
- G-U3b-07: In `Example 3.29` (`L = Z_⊥^⊤ × 𝒫({tt, ff})`), `f_+` must test strict bottom (`z₁ = ⊥ or z₂ = ⊥` returning `(⊥, ∅)`) *before* `otherwise` (`(⊤, ∅)`) to preserve monotonicity, and relational operators on `(⊤, ∅)` must yield `(⊥, {tt, ff})` rather than `(⊤, ∅)` so `Table 3.9` `[if]` (`ι_true ⊑ D̂(ℓ₀)`) does not drop both branches `[derived]`. [PPA Example 3.29, p. 187] (book p. 187; PDF p. 205); [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206)
- G-U3b-08: Testing branch reachability via `ι_true ⊑ D̂(ℓ₀)` and `ι_false ⊑ D̂(ℓ₀)` in `Table 3.9` `[if]` is sound on a general lattice `L` only when `true ∈ γ(d̂) ⇒ ι_true ⊑ d̂` (and likewise for `false`), and `else` must never be pruned before fixed-point convergence `[derived]`. [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206)
- G-U3b-09: Staged acceptability `⊨'_D` (`p. 189`, unconditional `[if]`) restores `(Ĉ, D̂, ρ̂, δ̂) ⊨'_D e ⇒ (Ĉ, ρ̂) ⊨ e` and lets least `(Ĉ, ρ̂)` be solved completely *before* least `(D̂, δ̂)` to obtain the exact combined least solution of `⊨'_D`, at the cost of dead-branch pollution (`{0, +}` vs `{0}` in `Example 3.31`). [PPA §3.5.2, p. 189] (book p. 189; PDF p. 207); [PPA Example 3.31, p. 189] (book p. 189; PDF p. 207)
- G-U3b-10: Monovariant `0-CFA` on polymorphic identity `(f f)(fn y => y)` (`Example 3.32`) not only smears `Ĉ_id(9) = {fn x => x^1, fn y => y^6}`, but also leaks `fn y => y^6` into operator cache `Ĉ_id(5)`, triggering a phantom self-call `ρ̂_id(y) = {fn y => y^6}` `[derived]`; syntactic let-cloning (`Example 3.33`) avoids this only by duplicating code. [PPA Example 3.32, p. 190] (book p. 190; PDF p. 208); [PPA Example 3.33, p. 190] (book p. 190; PDF p. 208); [PPA Example 3.33, p. 191] (book p. 191; PDF p. 209)
- G-U3b-11: Do not confuse **uniform `k`-CFA** (`Cachê = (Lab × Δ) → Val̂`, `Δ = Lab^{≤k}`) with **standard `k`-CFA** (Shivers `[156, 157, 158]`, `Cachê = (Lab × CEnv) → Val̂`); both embed per-variable lexical context environments `CEnv = Var → Δ` inside `Val̂ = 𝒫(Term × CEnv)`. [PPA §3.6.1, p. 191] (book p. 191; PDF p. 209); [PPA §3.6.1, p. 193] (book p. 193; PDF p. 211)
- G-U3b-12: In `Table 3.10` (`§3.6.1`), `[var]` looks up `ρ̂(x, ce(x))` using the **lexical birth contour `ce(x)`**, *never* `ρ̂(x, δ)` with the current call context `δ` (which would implement dynamic scoping), and `[fn]`/`[fun]` must restrict `ce₀ = ce | FV(...)` to avoid exponential state splitting over dead outer variables `[derived]`. [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210); [PPA §3.6.1, p. 193] (book p. 193; PDF p. 211)
- G-U3b-13: In `Table 3.10`, `[app]` pushes the **application's outer label `ℓ`** (`δ₀ = ⌈δ, ℓ⌉_k`) and extends the **closure's `ce₀`** (`ce'_0 = ce₀[x ↦ δ₀]`), whereas `[let]` **leaves `δ` unchanged** (`ce' = ce[x ↦ δ]`); desugaring `let x = e₁ in e₂` to `((fn x => e₂) e₁)^ℓ` therefore loses one level of call-string precision for `k ≥ 1` `[derived]`. [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210); [PPA §3.6.1, p. 193] (book p. 193; PDF p. 211)
- G-U3b-14: `Example 3.34` (`p. 194`) mis-cites `"Example 3.33"` while displaying and analysing `Example 3.32`'s unexpanded program (and prints `"only records"`), and §3.6.1 (`p. 194`) explicitly omits soundness proofs and solver algorithms for `Table 3.10`. [PPA §3.6.1, p. 194] (book p. 194; PDF p. 212); [PPA Example 3.34, p. 194] (book p. 194; PDF p. 212)
- G-U3b-15: Even at `k = 1`, both `1-CFA` and uniform `1-CFA` have **exponential worst-case complexity** because `Val̂ = 𝒫(Term × CEnv)` has height `O(n · n^p)` (`p = O(n)` variables); replacing `CEnv` with single contours (`Val̂ = 𝒫(Term × Δ)` / *polynomial `k`-CFA*, `[external: m-CFA]`) reduces `1-CFA` worst-case complexity to `O(n⁶)`. [PPA §3.6.1, p. 195] (book p. 195; PDF p. 213)
- G-U3b-16: Empirical runtime can invert worst-case complexity: `1-CFA` (exponential worst-case) can run **faster** than `0-CFA` (`O(n³)` worst-case) in practice (`[80]`) because higher precision prevents spurious closures from flooding the state space. [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219)
- G-U3b-17: Base `CPA` (`[2]`, `[external: Agesen]`, §3.6.2) adapts `Table 3.1` (not `Table 3.5`) for **closed, non-recursive** `m`-ary abstractions (`FV = ∅`), using `Δ = Term^m` without `CEnv`; supporting open closures or recursion requires re-introducing `ce ∈ CEnv = Var → Δ` (`Exercise 3.17`, misprinted `"Cartesian Production Algorithm"`). [PPA §3.6.2, p. 196] (book p. 196; PDF p. 214); [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215); [PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227)
- G-U3b-18: **Source errata on `p. 197` (`F-U3b-05`)**: the printed `CPA` `[app]` clause `(Ĉ, ρ̂) ⊨_{CPA}^δ (t₀^{ℓ₀}(t₁^{ℓ₁}, ···, t_m^{ℓ_m})^ℓ` drops a closing `)` before `^ℓ` and writes `{δ_b} ⊆ ρ̂(x₁) × ··· × ρ̂(x_m)` **omitting `, δ_b`**, which must read `{δ_b} ⊆ ρ̂(x₁, δ_b) × ··· × ρ̂(x_m, δ_b)` to match `Env̂ = (Var × Δ) → Val̂`. [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215)
- G-U3b-19: In both `m`-ary `0-CFA` and `CPA` (`p. 197`), quantifying over `Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ)` collapses to `∅` — **silently skipping the call** — whenever *any* argument `i` has `Ĉ(ℓ_i, δ) = ∅` (as happens on every constant `c^{ℓ_i}` in pure `Term`-only CFA!); `CPA` must populate non-empty abstract tokens for primitive arguments `[derived]`. [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215)
- G-U3b-20: `CPA` memoises `(Ĉ, ρ̂) ⊨_{CPA}^{δ_b} t_b^{ℓ_b}` into a global pool of **templates** and expands products lazily (`p. 198`), staying precise across arbitrary wrapper depth while risking `K^m` blowup on `m`-argument megamorphic call sites `[derived]`. [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216)
- G-U3b-21: Chapter 2's interprocedural frameworks (`§2.5`) and Chapter 3's polyvariant CFAs (`§3.6`) are curried `U5` isomorphs: `§2.5.4` call strings `A_∘, A_• : Lab → (Lab^{≤k} → L)` correspond to uniform `k`-CFA `Ĉ : Lab → Lab^{≤k} → 𝒫(Term × CEnv)` (`§2.5` lacks `ρ̂`/`CEnv` because non-parameter variables are global, cf. `Exercise 3.16`), and `§2.5.5` *small assumption sets* (`Δ = D`) correspond to unary `CPA` (`Δ = Term = D`). [PPA §3.6.1, p. 196] (book p. 196; PDF p. 214); [PPA §3.6.2, p. 198] (book p. 198; PDF p. 216)
- G-U3b-22: Pure `Table 3.1` `0-CFA` behaves like dynamic scoping when distinct bindings share a variable name (`p. 199`, `Exercise 3.7`), and is sound under *both* call-by-value and call-by-name SOS (`Exercise 3.8`), so α-renaming and CBV demand guards (`Exercise 3.3`) strictly sharpen precision. [PPA Chapter 3 Concluding Remarks, p. 199] (book p. 199; PDF p. 217); [PPA Exercise 3.7, p. 207] (book p. 207; PDF p. 225); [PPA Exercise 3.8, p. 207] (book p. 207; PDF p. 225)
- G-U3b-23: In Set-Constraint Based Analysis (`S₁ ⊆ S₂`, `p. 201`), constructor projection `C^{-i}(S)` preserves monotonicity and encodes conditional constraints, whereas explicit **complement `¬S`** destroys monotonicity so **Tarski's Theorem fails** and Banach's Contraction Theorem is needed. [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219)
- G-U3b-24: `[9]`'s (`[external: Aiken et al.]`) two-step **lazy** conditional-constraint solver (`pp. 201–202`, expanding conditional rules dynamically as guards become non-empty) avoids `Tables 3.6–3.7`'s eager `Term_⋆` pre-instantiation overhead in practice. [PPA Chapter 3 Concluding Remarks, p. 201] (book p. 201; PDF p. 219); [PPA Chapter 3 Concluding Remarks, p. 202] (book p. 202; PDF p. 220)
- G-U3b-25: In `Mini Project 3.1` (`Reach = Lab → 𝒫({on})`, `(Ĉ, ρ̂, R̂) ⊨'_s e`, misprinted `⊨_s` on line 10), `⊨ e_⋆` implies `∃R̂ : ⊨'_s e_⋆` *only* when labels are unique: sharing body label `ℓ₀` between a called and an uncalled abstraction forces `{on} ⊆ R̂(ℓ₀)` to constrain the dead body `[derived]`. [PPA Mini Project 3.1, p. 202] (book p. 202; PDF p. 220)
- G-U3b-26: Embedding labels inside `Val̂` — either via `Val̂ = 𝒫(Exp)` (`Exercise 3.6`) or via constructor field labels `C(ℓ₁, ···, ℓ_n)` (`Mini Project 3.2`) — breaks `Fact 3.11` and `Table 3.1` subject reduction because small-step SOS rewrites outer expression labels during evaluation. [PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221); [PPA Exercise 3.6, p. 206] (book p. 206; PDF p. 224); [PPA Exercise 3.6, p. 207] (book p. 207; PDF p. 225)
- G-U3b-27: Flow-sensitive imperative heap stores `Ŝ_∘, Ŝ_• : Lab → (Pnt → Val̂)` (`Mini Project 3.4`) perform weak updates by default (`[external: weak update]`); sound **strong updates (`"kill"`, [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134))** on heap/object fields require both per-point local stores and abstract reference counts proving singleton allocation (`p. 200` `[133]`). [PPA Chapter 3 Concluding Remarks, p. 200] (book p. 200; PDF p. 218); [PPA Mini Project 3.4, p. 204] (book p. 204; PDF p. 222); [PPA Mini Project 3.4, p. 205] (book p. 205; PDF p. 223)
- G-U3b-28: Declarative acceptability `(Ĉ, ρ̂) ⊨ e` (`(3.8)`) is **not upward-closed** in `⊑` (`(3.8) ⇒ (3.9)` strictly in `Exercise 3.4`, because adding spurious closures to `Ĉ(ℓ₁)` triggers new `[app]` body obligations), and equational constraints `𝒞_⋆^=⟦e_⋆⟧` (`Exercise 3.13`) match `𝒞_⋆⟦e_⋆⟧` on the **least** solution only. [PPA Exercise 3.4, p. 206] (book p. 206; PDF p. 224); [PPA Exercise 3.13, p. 208] (book p. 208; PDF p. 226)
- G-U3b-29: Standard `k`-CFA (`Table 3.10`) flushes outer callers from `⌈δ, ℓ⌉_k` after `k` self-recursive steps (`[1, 2, 2, 1, 1] ↦ [1, 1]`), whereas `Exercise 3.15`'s stuttering compression (`[1, 2, 2, 1, 1] ↦ [2, 1]`) preserves caller context across unbounded direct recursion. [PPA Exercise 3.15, p. 208] (book p. 208; PDF p. 226)
- G-U3b-30: The `pdftotext` OCR layer of `ppa.pdf` erases the entire `[op]` body in `Table 3.9` (`p. 188`), both displays in `Example 3.28` (`p. 186`), both numbered displays `(3.8)` and `(3.9)` in `Exercise 3.4` (`p. 206`), and grammar/judgement displays in `Mini Projects 3.2 & 3.4` (`pp. 203–205`). [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206); [PPA Exercise 3.4, p. 206] (book p. 206; PDF p. 224)
