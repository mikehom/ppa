<!-- @governing: REQ-TECH-PPA-002 @parent: REQ-PRD-PPA-002 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 4a (Chapter 4 Opening & §§4.1-4.3). -->
# Unit 4a Raw Knowledge Shard: Chapter 4 Opening & §§4.1–4.3 (Abstract Interpretation Foundations)

Scope: Chapter 4 (*Abstract Interpretation*) opening, §4.1 (*A Mundane Approach to Correctness*: `§§4.1.1–4.1.3`),
§4.2 (*Approximation of Fixed Points*: `§§4.2.1–4.2.2`), and §4.3 (*Galois Connections*: `§§4.3.1–4.3.2`)
through `Example 4.32` atop book p. 246 immediately above the `4.4 Systematic Design of Galois Connections`
heading — from [PPA Chapter 4, p. 211] (book p. 211; PDF p. 228) through
[PPA Example 4.32, p. 246] (book p. 246; PDF p. 263). Offset across the entire unit:
`PDF page = book page + 17` (`36` rendered pages, `PDF pp. 228–263`; book p. 210 is an omitted blank verso).
Section 4.4 (*Systematic Design of Galois Connections*), starting near the bottom of book p. 246, belongs to
Unit 4b.

Method and conventions: every equation, display, inference diagram, proof step, figure, and source anomaly
was transcribed directly from 150-dpi rendered page images (`PDF pp. 228–263`) and checked against
`corpus/pdf_page_map.json`; PDF OCR corruptions are logged in `Findings` rather than copied. Book labels
(`4.1`–`4.32`, `(4.1)`–`(4.10)`, `Figure 4.1`–`4.9`) are preserved verbatim; unnumbered structural blocks
carry local identifiers `[U4a:<section>-<letter>]`. Terms marked `[external]` lie outside the book;
`[derived]` marks direct logical consequences or witnesses constructed from the printed definitions. Note on
printed structure: there is no `§4.3.3` (`α`/`γ` uniqueness/existence sit in `§4.3.1`, extraction
connections in `§4.3` opening, reduction `ς` in `§4.3.2`, and closure operators in Chapter 4
*Concluding Remarks*).

## Closed Inventory — book pp. 211–246, PDF pp. 228–263

| Kind | Count | Identifiers |
| :--- | ---: | :--- |
| Chapter opening & Sections | 4 | `Chapter 4` opening (`p. 211`), `§4.1` (`pp. 211–221`), `§4.2` (`pp. 221–233`), `§4.3` (`pp. 233–246` top) |
| Numbered subsections | 7 | `§4.1.1` (`pp. 214–216`), `§4.1.2` (`pp. 216–218`), `§4.1.3` (`pp. 219–221`), `§4.2.1` (`pp. 224–229`), `§4.2.2` (`pp. 230–233`), `§4.3.1` (`pp. 239–242`), `§4.3.2` (`pp. 242–246` top) |
| Tables | 0 | None in Chapter 4 |
| Figures | 9 | `Figure 4.1` (`p. 218`), `Figure 4.2` (`p. 221`), `Figure 4.3` (`p. 224`), `Figure 4.4` (`p. 226`), `Figure 4.5` (`p. 231`), `Figure 4.6` (`p. 235`), `Figure 4.7` (`p. 238`), `Figure 4.8` (`p. 243`), `Figure 4.9` (`p. 245`) |
| Numbered displays | 10 | `(4.1)` (`p. 211`), `(4.2)` (`p. 212`), `(4.3)`–`(4.5)` (`p. 214`), `(4.6)` (`p. 216`), `(4.7)` (`p. 230`), `(4.8)`–`(4.9)` (`p. 234`), `(4.10)` (`p. 236`) |
| Examples | 17 | `4.1` (`pp. 212–213`), `4.2` (`p. 213`), `4.3` (`p. 215`), `4.4` (`pp. 215–216`), `4.6` (`p. 217`), `4.7` (`p. 218`), `4.9` (`p. 220`), `4.10` (`pp. 221–222`), `4.12` (`pp. 225–226`), `4.15` (`pp. 228–229`), `4.18` (`pp. 232–233`), `4.19` (`pp. 234–236`), `4.21` (`p. 238`), `4.25` (`pp. 240–241`), `4.26` (`p. 243`), `4.28` (`p. 244`), `4.32` (`p. 246`) |
| Lemmas | 6 | `4.5` (`p. 217`), `4.8` (`p. 220`), `4.16` (`pp. 230–232`), `4.22` (`p. 239`), `4.23` (`pp. 239–240`), `4.27` (`pp. 243–244`) |
| Propositions | 4 | `4.13` (`pp. 227–228`), `4.17` (`p. 232`), `4.20` (`p. 236`), `4.29` (`p. 244`, proof `p. 246`) |
| Facts | 5 | `4.11` (`p. 225`), `4.14` (`p. 227`), `4.24` (`p. 240`), `4.30` (`p. 245`), `4.31` (`pp. 245–246`) |
| Shared statement counter | 32 | Contiguous `4.1`–`4.32` (`0` gaps; `Example 4.33` opens inside `§4.4` on `p. 247` in Unit 4b) |
| Unnumbered `[U4a:...]` blocks | 24 | `4-a` (`1`), `4.1-a` (`1`), `4.1.1-a` (`1`), `4.1.2-a..b` (`2`), `4.1.3-a..b` (`2`), `4.2-a..b` (`2`), `4.2.1-a..c` (`3`), `4.2.2-a..b` (`2`), `4.3-a..c` (`3`), `4.3.1-a..b` (`2`), `4.3.2-a..e` (`5`) |

---

## Chapter 4 Opening & Section 4.1 — A Mundane Approach to Correctness

### [U4a:4-a] Chapter 4 Abstract Interpretation Roadmap

Source: [PPA Chapter 4, p. 211] (book p. 211; PDF p. 228).

Presents *Abstract Interpretation* in a largely programming-language-independent setting, focusing on
property spaces, functions/computations over them, and relationships between property spaces:
1. Formulate semantic correctness for a restricted (*mundane* / first-order) class of analyses (`§4.1`) to
   motivate correctness relations `R` and representation functions `β`.
2. Develop *widening* (`∇`) and *narrowing* (`Δ`) approximations of least fixed points while bounding
   iteration steps (`§4.2`).
3. Develop *Galois connections* and *Galois insertions* (`§4.3`) to replace a costly or uncomputable property
   space `L` with a simpler one `M`, followed (in `§§4.4–4.5`, Unit 4b) by systematic combinators and
   induced operations/specifications.

### [U4a:4.1-a] Abstracted Semantics `(4.1)`, Analysis `(4.2)`, Determinacy of `⊳`, and First-Order vs Second-Order Scope

Source: [PPA §4.1, pp. 211–212] (book p. 211; PDF p. 228) (book p. 212; PDF p. 229).

- **Concrete semantics (`(4.1)`)**: identifies a set `V` of values (states, closures, double-precision reals)
  and specifies how program `p` transforms `v₁ ∈ V` to `v₂ ∈ V`:
  ```text
  p ⊢ v₁ ↝ v₂                                                        (4.1)
  ```
  without fixing semantic style and **without requiring determinacy** (`p ⊢ v₁ ↝ v₂ ∧ p ⊢ v₁ ↝ v₃` need
  not imply `v₂ = v₃`).
- **Program analysis (`(4.2)`)**: identifies a set `L` of properties (shapes of states, abstract closures,
  bounds for reals) and specifies how `p` transforms `l₁ ∈ L` to `l₂ ∈ L`:
  ```text
  p ⊢ l₁ ⊳ l₂                                                        (4.2)
  ```
  Unlike `↝`, `⊳` is customarily assumed **deterministic** (and total) so it defines a function
  `f_p : L → L`:
  ```text
  f_p(l₁) = l₂    iff    p ⊢ l₁ ⊳ l₂
  ```
- **Scope boundary (`first-order` vs `second-order`)**: `§4.1` is called *mundane* because it applies only
  to **first-order analyses** whose properties describe *sets of values* (such as Constant Propagation in
  Chapter 2 `§2.3`, Shape Analysis in Chapter 2 `§2.6`, and Control Flow Analysis in Chapter 3), and **not**
  directly to **second-order analyses** whose properties relate to *relations between values* (such as Live
  Variable Analysis in Chapter 2 `§2.1`). By contrast, **`§§4.2–4.5` apply equally to both first-order and
  second-order analyses**.

### Example 4.1 (`WHILE` Semantics and Constant Propagation in `(4.1)`/`(4.2)` Form)

Source: [PPA Example 4.1, pp. 212–213] (book p. 212; PDF p. 229) (book p. 213; PDF p. 230).

- **Semantics (`V = State = Var → Z`)**: for `WHILE` (Chapter 2) with Structural Operational Semantics
  `⟨S, σ⟩ → ⟨S', σ'⟩` and `⟨S, σ⟩ → σ'` (`S, S' ∈ Stmt`, `σ, σ' ∈ State`) and program of interest `S⋆`,
  define:
  ```text
  S⋆ ⊢ σ₁ ↝ σ₂    iff    ⟨S⋆, σ₁⟩ →* σ₂
  ```
- **Constant Propagation (`L = Statê_CP = (Var⋆ → Z^⊤)_⊥`)**: Chapter 2 `§2.3` yields `CP^=` as a Monotone
  Framework instance with `E = {init(S⋆)}`, `F = flow(S⋆)`, and `ι = λx.⊤`, with solution pair
  `(CP_∘, CP_•)` (`CP_∘, CP_• : Lab⋆ → Statê_CP`). For a solution `(CP_∘, CP_•)` to `CP^=`:
  ```text
  S⋆ ⊢ σ̂₁ ⊳ σ̂₂    iff    ι = σ̂₁  ∧  σ̂₂ = ⨆{CP_•(ℓ) | ℓ ∈ final(S⋆)}
  ```
  For `S⋆` with isolated entries, `σ̂₁` is the abstract entry state and `σ̂₂` joins (`⨆` on `Statê_CP`) exit
  abstract states across `final(S⋆)`. *(Note `ι = σ̂₁` fixes `σ̂₁ = λx.⊤` unless `CP^=` is re-parameterised by
  arbitrary `σ̂₁ ∈ Statê_CP` `[derived]`; see `F-U4a-02`.)* ■

### Example 4.2 (`FUN` Semantics and Pure 0-CFA in `(4.1)`/`(4.2)` Form)

Source: [PPA Example 4.2, p. 213] (book p. 213; PDF p. 230).

- **Semantics (`V = Val`)**: for `FUN` (Chapter 3) with transitions `ρ ⊢ ie → ie'`
  (`ρ ∈ Env = Var →_fin Val`, `ie, ie' ∈ IExp`) and closed program of interest `e⋆`:
  ```text
  e⋆ ⊢ v₁ ↝ v₂    iff    [] ⊢ (e⋆ v₁^{ℓ₁})^{ℓ₂} →* v₂^{ℓ₂}
  ```
  for fresh labels `ℓ₁, ℓ₂`.
- **Pure 0-CFA (`L = Env̂ × Val̂`)**: Chapter 3 `§3.1` (`Table 3.1`) yields `(Ĉ, ρ̂) ⊨ e⋆` with
  `Ĉ ∈ Cachê = Lab⋆ → Val̂`, `ρ̂ ∈ Env̂ = Var⋆ → Val̂`, `Val̂ = 𝒫(Term⋆)`. Taking `L = Env̂ × Val̂` and
  assuming `(Ĉ, ρ̂) ⊨ (e⋆ c^{ℓ₁})^{ℓ₂}` for dummy constant `c` (valid because `[con]` in Chapter 3 `Table 3.1`
  imposes no constraint on `(Ĉ, ρ̂)` — a property that fails in data-flow `0-CFA` `Table 3.8` `[derived]`):
  ```text
  e⋆ ⊢ (ρ̂₁, v̂₁) ⊳ (ρ̂₂, v̂₂)    iff    Ĉ(ℓ₁) = v̂₁  ∧  Ĉ(ℓ₂) = v̂₂  ∧  ρ̂₁ = ρ̂₂ = ρ̂
  ```
  *(Source typo on final line: `"as in indeed the case"` for `"as is indeed the case"`; determinacy of `⊳`
  implicitly assumes a canonical, e.g. least, solution `(Ĉ, ρ̂)`; see `F-U4a-01`, `F-U4a-03`.)* ■

---

### Section 4.1.1 — Correctness Relations

#### [U4a:4.1.1-a] Correctness Relations `R`, Preservation `(4.3)`, Ordering `(4.4)`, and Moore Family `(4.5)`

Source: [PPA §4.1.1, pp. 214–215] (book p. 214; PDF p. 231) (book p. 215; PDF p. 232).

For first-order analyses, correctness relates semantic values directly to abstract properties via a
*correctness relation*:
```text
R : V × L → {true, false}
```
where `v R l` reads "`v` is described by `l`".

- **Preservation under computation (`(4.3)`, logical relation)**:
  ```text
  v₁ R l₁  ∧  p ⊢ v₁ ↝ v₂  ∧  p ⊢ l₁ ⊳ l₂   ⇒   v₂ R l₂            (4.3)
  ```
  visualised as the implication square (`[PPA §4.1.1, p. 214] (book p. 214; PDF p. 231)`):
  ```text
  p ⊢  v₁  ↝  v₂
       ⋮       ⋮
       R   ⇒   R
       ⋮       ⋮
  p ⊢  l₁  ⊳  l₂
  ```
  Such `R` is called a *logical relation*, written `(p ⊢ · ↝ ·) (R ↠ R) (p ⊢ · ⊳ ·)`.
- **Complete-lattice conditions `(4.4)` and `(4.5)`**: for complete lattice `L = (L, ⊑, ⊔, ⊓, ⊥, ⊤)`
  (`Appendix A`):
  ```text
  v R l₁  ∧  l₁ ⊑ l₂          ⇒   v R l₂                            (4.4)
  (∀l ∈ L' ⊆ L : v R l)        ⇒   v R (⨅ L')                        (4.5)
  ```
  - `(4.4)` adopts the convention that **smaller lattice elements (`⊑`) are more precise ("better")** (dual
    by lattice duality to larger-is-better DFA conventions in parts of Chapter 2).
  - `(4.5)` requires `{l | v R l}` to be a **Moore family** for every `v ∈ V` (`Appendix A`), ensuring a
    single *best* description of `v` exists (`⨅{l | v R l}`). Two immediate consequences (`L' = ∅` and
    `L' = {l₁, l₂}`):
    ```text
    v R ⊤
    v R l₁  ∧  v R l₂   ⇒   v R (l₁ ⊓ l₂)
    ```

#### Example 4.3 (`R_CP` for Constant Propagation)

Source: [PPA Example 4.3, p. 215] (book p. 215; PDF p. 232).

```text
R_CP : State × Statê_CP → {true, false}
σ R_CP σ̂    iff    ∀x ∈ FV(S⋆) : (σ̂(x) = ⊤  ∨  σ(x) = σ̂(x))
```
*(Requires implicit guard `σ̂ ≠ ⊥`, since `⊥ ∈ (Var⋆ → Z^⊤)_⊥` is non-functional and describes no concrete
state `[derived]`; see `F-U4a-02`.)* Satisfies `(4.4)` and `(4.5)` on `(Statê_CP, ⊑_CP)` (cf. Chapter 2
`Exercise 2.7`). ■

#### Example 4.4 (`R_CFA` for 0-CFA)

Source: [PPA Example 4.4, pp. 215–216] (book p. 215; PDF p. 232) (book p. 216; PDF p. 233).

Using `𝒱` from Chapter 3 `§3.2`, define `R_CFA : Val × (Env̂ × Val̂) → {true, false}` by `v R_CFA (ρ̂, v̂) iff v 𝒱 (ρ̂, v̂)`:
```text
v 𝒱 (ρ̂, v̂)  iff  true                                         if v = c
                 t ∈ v̂  ∧  ∀x ∈ dom(ρ) : ρ(x) 𝒱 (ρ̂, ρ̂(x))     if v = close t in ρ
```
Condition `(4.3)` specialises (verified from `Theorem 3.10`, `Exercise 4.3`) to:
```text
(v₁ 𝒱 (ρ̂, v̂₁)  ∧  [] ⊢ (e⋆ v₁^{ℓ₁})^{ℓ₂} →* v₂^{ℓ₂}  ∧  (Ĉ, ρ̂) ⊨ (e⋆ c^{ℓ₁})^{ℓ₂}
 ∧  Ĉ(ℓ₁) = v̂₁  ∧  Ĉ(ℓ₂) = v̂₂)   ⇒   v₂ 𝒱 (ρ̂, v̂₂)
```
Under componentwise complete-lattice order:
```text
(ρ̂₁, v̂₁) ⊑_CFA (ρ̂₂, v̂₂)    iff    v̂₁ ⊆ v̂₂  ∧  ∀x : ρ̂₁(x) ⊆ ρ̂₂(x)
```
conditions `(4.4)` and `(4.5)` follow by structural induction on `v ∈ Val` (noting `v ∈ Val` vs `Term⋆`, see
`F-U4a-03`). ■

---

### Section 4.1.2 — Representation Functions

#### [U4a:4.1.2-a] Representation Functions `β : V → L` and Criterion `(4.6)`

Source: [PPA §4.1.2, p. 216] (book p. 216; PDF p. 233).

A *representation function* `β : V → L` maps each concrete value `v` to the best property describing it,
with correctness condition `(4.6)`:
```text
β(v₁) ⊑ l₁  ∧  p ⊢ v₁ ↝ v₂  ∧  p ⊢ l₁ ⊳ l₂   ⇒   β(v₂) ⊑ l₂        (4.6)
```
commuting diagram (`[PPA §4.1.2, p. 216] (book p. 216; PDF p. 233)`):
```text
p ⊢  v₁   ↝   v₂
     │        │
   β │   ⇒    │ β
     ↓        ↓
     ⊑        ⊑
p ⊢  l₁   ⊳   l₂
```

#### [U4a:4.1.2-b] Canonical Conversions `R_β` and `β_R`

Source: [PPA §4.1.2, p. 217] (book p. 217; PDF p. 234).

```text
v R_β l    iff    β(v) ⊑ l
β_R(v)     =      ⨅{l | v R l}
```
Say `R` is *generated by* `β` iff `v R l ⇔ β(v) ⊑ l`.

#### Lemma 4.5 (Equivalence Between Correctness Relations `(4.3)` and Representation Functions `(4.6)`)

Source: [PPA Lemma 4.5, p. 217] (book p. 217; PDF p. 234).

> **(i)** Given `β : V → L`, `R_β : V × L → {true, false}` satisfies `(4.4)` and `(4.5)`, and `β_{R_β} = β`.
> **(ii)** Given `R : V × L → {true, false}` satisfying `(4.4)` and `(4.5)`, `β_R` is well-defined and
> `R_{β_R} = R`.
> Hence `(4.3)` and `(4.6)` are equivalent formulations of semantic correctness. ■

- **Proof** (`[PPA Lemma 4.5, p. 217] (book p. 217; PDF p. 234)`):
  - *(i)*: `(4.4)` follows by transitivity of `⊑`; `(4.5)` follows because `β(v)` is a lower bound of `L'`,
    so `β(v) ⊑ ⨅ L'`; and `β_{R_β}(v) = ⨅{l | β(v) ⊑ l} = β(v)`.
  - *(ii)*: `β_R` is well-defined because `L` is a complete lattice. If `v R l`, then `β_R(v) ⊑ l`, so
    `v R_{β_R} l`. Conversely, if `β_R(v) ⊑ l`, applying `(4.5)` to `L' = {l' | v R l'}` yields
    `v R (β_R(v))`, and `(4.4)` gives `v R l`. ■

#### Example 4.6 (`β_CP` Generating `R_CP`)

Source: [PPA Example 4.6, p. 217] (book p. 217; PDF p. 234).

`β_CP : State → Statê_CP` defined by `β_CP(σ) = λx. σ(x)` satisfies `σ R_CP σ̂ ⇔ β_CP(σ) ⊑_CP σ̂` (aligning
`Var⋆ = FV(S⋆)`, `F-U4a-02`). ■

#### Figure 4.1 (Correctness Relation `R` Generated by Representation Function `β`)

Source: [PPA Figure 4.1, p. 218] (book p. 218; PDF p. 235).

Two-oval diagram: left oval `V` holds `v`; right oval (complete lattice `L`) shows solid arrow `β : v ↦ β(v)`
and dashed fan `R` covering the upward-closed cone `{l ∈ L | β(v) ⊑ l}` anchored at apex `β(v)`.

#### Example 4.7 (`β_CFA` and `β_CFA^E` Generating `R_CFA`)

Source: [PPA Example 4.7, p. 218] (book p. 218; PDF p. 235).

```text
β_CFA(v) = (λx. ∅, ∅)           if v = c
         = (β_CFA^E(ρ), {t})    if v = close t in ρ

β_CFA^E : Env → Env̂
β_CFA^E(ρ)(x) = ⋃{ρ̂_y(x) | β_CFA(ρ(y)) = (ρ̂_y, v̂_y) ∧ y ∈ dom(ρ)}
                ∪ (v̂_x   if x ∈ dom(ρ) ∧ β_CFA(ρ(x)) = (ρ̂_x, v̂_x);
                   ∅     otherwise)
```
Structural induction (`Exercise 4.4`) establishes `v R_CFA (ρ̂, v̂) ⇔ β_CFA(v) ⊑_CFA (ρ̂, v̂)`. *(Prose slip on
p. 218 writes `⋃{β_CFA(ρ(x)) | x ∈ Var⋆}` informally although `β_CFA(ρ(x)) ∈ Env̂ × Val̂` is a pair and `ρ`
is partial, fixed by the displayed `β_CFA^E` formula; see `F-U4a-03`.)* ■

---

### Section 4.1.3 — A Modest Generalisation

#### [U4a:4.1.3-a] Heterogeneous Domains and Higher-Order Logical Relations `R₁ ↠ R₂` / `β₁ ↠ β₂`

Source: [PPA §4.1.3, pp. 219–220] (book p. 219; PDF p. 236) (book p. 220; PDF p. 237).

Relaxing `V₁ = V₂` and `L₁ = L₂` (e.g. distinct input/output types): `p ⊢ v₁ ↝ v₂` (`v₁ ∈ V₁, v₂ ∈ V₂`) and
`p ⊢ l₁ ⊳ l₂` (`l₁ ∈ L₁, l₂ ∈ L₂`, defining `f_p : L₁ → L₂`). Given `R_i` generated by `β_i : V_i → L_i`
(`i = 1, 2`), correctness `(p ⊢ · ↝ ·) (R₁ ↠ R₂) f_p` uses:
```text
↝ (R₁ ↠ R₂) f    iff    ∀v₁ ∈ V₁, v₂ ∈ V₂, l₁ ∈ L₁ : v₁ ↝ v₂  ∧  v₁ R₁ l₁   ⇒   v₂ R₂ f(l₁)
```
with higher-order representation `β₁ ↠ β₂ : 𝒫(V₁ × V₂) → (L₁ → L₂)` (pointwise complete lattice `L₁ → L₂`):
```text
(β₁ ↠ β₂)(↝) = λl₁. ⨆{β₂(v₂) | β₁(v₁) ⊑ l₁  ∧  v₁ ↝ v₂}
```

#### Lemma 4.8 (`R₁ ↠ R₂` Generated by `β₁ ↠ β₂`)

Source: [PPA Lemma 4.8, p. 220] (book p. 220; PDF p. 237).

> If `R_i` is a correctness relation for `V_i` and `L_i` generated by `β_i : V_i → L_i` (`i = 1, 2`), then
> `R₁ ↠ R₂` is a correctness relation and is generated by `β₁ ↠ β₂`. ■

- **Proof** (`[PPA Lemma 4.8, p. 220] (book p. 220; PDF p. 237)`):
  ```text
  (β₁ ↠ β₂)(↝) ⊑ f
    ⇔  ∀l₁ : ⨆{β₂(v₂) | β₁(v₁) ⊑ l₁ ∧ v₁ ↝ v₂} ⊑ f(l₁)
    ⇔  ∀l₁, v₁, v₂ : (β₁(v₁) ⊑ l₁ ∧ v₁ ↝ v₂  ⇒  β₂(v₂) ⊑ f(l₁))
    ⇔  ∀l₁, v₁, v₂ : (v₁ R₁ l₁ ∧ v₁ ↝ v₂  ⇒  v₂ R₂ f(l₁))
    ⇔  ↝ (R₁ ↠ R₂) f
  ```
  By `Lemma 4.5(i)`, `R₁ ↠ R₂` satisfies `(4.4)` and `(4.5)` on `L₁ → L₂`. ■

#### Example 4.9 (`plus` on `𝒫(Z × Z) → 𝒫(Z)`)

Source: [PPA Example 4.9, pp. 220–221] (book p. 220; PDF p. 237) (book p. 221; PDF p. 238).

Concrete `plus ⊢ (z₁, z₂) ↝ z₁ + z₂`; abstract `f_plus(ZZ) = {z₁ + z₂ | (z₁, z₂) ∈ ZZ}` on
`(𝒫(Z × Z), ⊆) → (𝒫(Z), ⊆)`; `β_Z(z) = {z}`, `β_{Z×Z}(z₁, z₂) = {(z₁, z₂)}`. Soundness writes as
`(plus ⊢ · ↝ ·) (R_{Z×Z} ↠ R_Z) f_plus`, equivalently `(β_{Z×Z} ↠ β_Z)(plus ⊢ · ↝ ·) ⊑ f_plus` (exact
equality holds `[derived]`). *(Source metavariable switch on `p. 220`: penultimate display prints generic `p`
in `(β_{Z×Z} ↠ β_Z)(p ⊢ · ↝ ·)` instead of `plus`; see `F-U4a-04`.)* ■

#### [U4a:4.1.3-b] Concrete vs Abstract Equivalence Remark

Source: [PPA §4.1.3, p. 221] (book p. 221; PDF p. 238).

Closing `§4.1` (below `Figure 4.2`): moving freely between correctness relations and representation functions
allows general results to be proved once and reused.

---

## Section 4.2 — Approximation of Fixed Points

#### Figure 4.2 & Example 4.10 (The Complete Lattice `Interval` for Array Bound Analysis)

Source: [PPA Figure 4.2, p. 221] (book p. 221; PDF p. 238), [PPA Example 4.10, pp. 221–222] (book p. 221; PDF p. 238) (book p. 222; PDF p. 239).

- **`[U4a:4.2-a]` Standing assumption**: from `§4.2` through `§4.5`, property spaces such as `L` and `M` are
  tacitly assumed to be complete lattices (`Appendix A`) [PPA §4.2, p. 221] (book p. 221; PDF p. 238).
- **Carrier of `Interval`** (`Z' = Z ∪ {-∞, ∞}` with `-∞ ≤ z ≤ ∞`):
  ```text
  Interval = {⊥} ∪ {[z₁, z₂] | z₁ ≤ z₂, z₁ ∈ Z ∪ {-∞}, z₂ ∈ Z ∪ {∞}}
  ```
  Note `[∞, ∞]` and `[-∞, -∞]` are **excluded**; `⊥` is the dedicated empty interval.
- **Visual Hasse diagram (`Figure 4.2`, `p. 221`)**: bottom `⊥` connects upward to singleton leaves
  `…, [-2,-2], [-1,-1], [0,0], [1,1], [2,2], …`; bounded diamond tiers climb through width-1 (`[-2,-1], [-1,0], [0,1], [1,2]`),
  width-2 (`[-2,0], [-1,1], [0,2]`), width-3 (`[-2,1], [-1,2]`), and width-4 (`[-2,2]`), continuing upward;
  infinite-ray dashed legs rise through left rays `… ⊏ [-∞,-1] ⊏ [-∞,0] ⊏ [-∞,1] ⊏ …` and right rays
  `… ⊏ [1,∞] ⊏ [0,∞] ⊏ [-1,∞] ⊏ …`, meeting at top `[-∞, ∞]`.
- **Endpoint functions, partial order, and arbitrary join**:
  ```text
  inf(int) = ∞     if int = ⊥        sup(int) = -∞    if int = ⊥
           = z₁    if int = [z₁, z₂]           = z₂    if int = [z₁, z₂]

  int₁ ⊑ int₂    iff    inf(int₂) ≤ inf(int₁)  ∧  sup(int₁) ≤ sup(int₂)

  ⨆ Y = ⊥                                                       if Y ⊆ {⊥}
      = [inf'{inf(int) | int ∈ Y}, sup'{sup(int) | int ∈ Y}]    otherwise
  ```
  where on `Z ⊆ Z'` (`F-U4a-04`: `Z` overloads italic set vs bold `Z`): `inf'(∅) = ∞`, `inf'(Z) = z'` if
  `Z` has least element `z'` else `-∞`; `sup'(∅) = -∞`, `sup'(Z) = z'` if `Z` has greatest element `z'` else
  `∞`. By `Appendix A Lemma A.2`, existence of all joins `⨆ Y` makes `(Interval, ⊑)` a complete lattice. ■

#### [U4a:4.2-b] Monotone Fixed Points `Fix`/`Red`/`Ext`, Tarski's Theorem, and Figure 4.3 Chain Inequality

Source: [PPA §4.2, pp. 222–224] (book p. 222; PDF p. 239) (book p. 224; PDF p. 241), [PPA Figure 4.3, p. 224] (book p. 224; PDF p. 241).

For monotone `f : L → L` (`p ⊢ l₁ ⊳ l₂` given by `f(l₁) = l₂`):
```text
Fix(f) = {l | f(l) = l}       (fixed points)
Red(f) = {l | f(l) ⊑ l}       (reductive set; f is reductive iff Red(f) = L)
Ext(f) = {l | f(l) ⊒ l}       (extensive set; f is extensive iff Ext(f) = L)
```
By Tarski's Theorem (`Appendix A Proposition A.10`):
```text
lfp(f) = ⨅ Fix(f) = ⨅ Red(f)  ∈  Fix(f) ⊆ Red(f)
gfp(f) = ⨆ Fix(f) = ⨆ Ext(f)  ∈  Fix(f) ⊆ Ext(f)
```
- **Non-continuous / non-ACC barrier**: `(f^n(⊥))_n` need neither stabilise in finitely many steps nor satisfy
  `⨆_n f^n(⊥) = lfp(f)` unless `f` is continuous (`f(⨆_n l_n) = ⨆_n f(l_n)`); conversely, stopping `(f^n(⊤))_n`
  at any `n` is safe by `(4.4)` **but grossly imprecise in practice**.
- **`Figure 4.3` (`p. 224`)**: nested-oval lattice diagram spanning `⊥` to `⊤` with lower sub-oval `Ext(f)`,
  upper sub-oval `Red(f)`, central overlap lens `Fix(f) = Red(f) ∩ Ext(f)` from `lfp(f)` to `gfp(f)`, and the
  chain of six inequalities — where **every `⊑` can be strict (`≠`)**:
  ```text
  f^n(⊥)  ⊑  ⨆_n f^n(⊥)  ⊑  lfp(f)  ⊑  gfp(f)  ⊑  ⨅_n f^n(⊤)  ⊑  f^n(⊤)
  ```

---

### Section 4.2.1 — Widening Operators

#### [U4a:4.2.1-a] Upper Bound Operators `⊔̆` and Sequence Operator `(l_n^ϕ)_n`

Source: [PPA §4.2.1, pp. 224–225] (book p. 224; PDF p. 241) (book p. 225; PDF p. 242).

- `⊔̆ : L × L → L` (`\breve{\sqcup}`) on complete lattice `(L, ⊑)` is an **upper bound operator** iff:
  ```text
  l₁ ⊑ (l₁ ⊔̆ l₂) ⊒ l₂    for all l₁, l₂ ∈ L
  ```
  **Explicitly NOT required**: monotonicity, commutativity, associativity, or absorptiveness (`l ⊔̆ l = l`).
- Given any sequence `(l_n)_n` in `L` and total `ϕ : L × L → L`:
  ```text
  l_n^ϕ = l_n             if n = 0
        = l_{n-1}^ϕ ϕ l_n if n > 0
  ```

#### Fact 4.11 (Ascending Chain Dominant Property of `(l_n^{⊔̆})_n`)

Source: [PPA Fact 4.11, p. 225] (book p. 225; PDF p. 242).

> If `(l_n)_n` is a sequence and `⊔̆` is an upper bound operator then `(l_n^{⊔̆})_n` is an ascending chain;
> furthermore `l_n^{⊔̆} ⊒ ⨆{l₀, l₁, …, l_n}` for all `n`. ■

- **Proof** (`p. 225`): `l_0^{⊔̆} = l₀ ⊑ l₀ ⊔̆ l₁ = l_1^{⊔̆}` and `l_n^{⊔̆} ⊑ l_n^{⊔̆} ⊔̆ l_{n+1} = l_{n+1}^{⊔̆}`.
  Dominance holds at `n = 0` (`l₀ ⊒ l₀`) and by induction `l_{n+1}^{⊔̆} = l_n^{⊔̆} ⊔̆ l_{n+1} ⊒ ⨆{l₀, …, l_n} ⊔ l_{n+1} = ⨆{l₀, …, l_{n+1}}`. ■

#### Example 4.12 (Asymmetric & Non-Widening Upper Bound Operator `⊔̆^{int}`)

Source: [PPA Example 4.12, pp. 225–226] (book p. 225; PDF p. 242) (book p. 226; PDF p. 243).

For fixed `int ∈ Interval`:
```text
int₁ ⊔̆^{int} int₂ = int₁ ⊔ int₂    if int₁ ⊑ int  ∨  int₂ ⊑ int₁
                   = [-∞, ∞]        otherwise
```
- **Non-symmetry**: for `int = [0, 2]`, `[1, 2] ⊔̆^{[0,2]} [2, 3] = [1, 3]` whereas
  `[2, 3] ⊔̆^{[0,2]} [1, 2] = [-∞, ∞]`.
- On `[0,0], [1,1], [2,2], …`:
  - `int = [0, ∞]` produces the **non-stabilising** chain `[0,0], [0,1], [0,2], [0,3], …`;
  - `int = [0, 2]` stabilises via `[0,0], [0,1], [0,2], [0,3], [-∞, ∞], [-∞, ∞], …`. ■

#### Figure 4.4 & [U4a:4.2.1-b] Widening Operators `∇`, Iterates `(f_∇^n)_n`, and `lfp_∇(f)`

Source: [PPA Figure 4.4, p. 226] (book p. 226; PDF p. 243), [PPA §4.2.1, pp. 226–227] (book p. 226; PDF p. 243) (book p. 227; PDF p. 244).

- `∇ : L × L → L` is a **widening operator** iff:
  1. `∇` is an upper bound operator (`l₁ ⊑ (l₁ ∇ l₂) ⊒ l₂`), and
  2. for **every ascending chain** `(l_n)_n`, `(l_n^∇)_n` eventually stabilises (`∃m : ∀n ≥ m : l_n^∇ = l_m^∇`).
- For monotone `f : L → L`:
  ```text
  f_∇^n = ⊥                          if n = 0
        = f_∇^{n-1}                  if n > 0  ∧  f(f_∇^{n-1}) ⊑ f_∇^{n-1}
        = f_∇^{n-1} ∇ f(f_∇^{n-1})   otherwise
  ```
  When `(f_∇^n)_n` stabilises at `m` with `f(f_∇^m) ⊑ f_∇^m ∈ Red(f)`, set `lfp_∇(f) = f_∇^m ⊒ lfp(f)`.
  Note the explicit reductive guard `f(f_∇^{n-1}) ⊑ f_∇^{n-1}` is mandatory because `∇` need not be
  absorptive (`l ∇ l = l` can fail `[derived]`).
- **`Figure 4.4` (`p. 226`)**: lattice oval `Red(f)` with minimum `lfp(f)` and polyline
  `f_∇^0 = ⊥ → f_∇^1 → f_∇^2 → … → f_∇^{m-1} → f_∇^m = f_∇^{m+1} = …` stepping outside `Red(f)` before landing
  inside `Red(f)` strictly above `lfp(f)` at `m`.

#### Proposition 4.13, Fact 4.14, and `[U4a:4.2.1-c]` Termination & Soundness Proofs

Source: [PPA Proposition 4.13, p. 227] (book p. 227; PDF p. 244), [PPA Fact 4.14, p. 227] (book p. 227; PDF p. 244), [PPA §4.2.1, p. 228] (book p. 228; PDF p. 245).

- **Proposition 4.13**: If `∇` is a widening operator *(and `f` monotone, inherited from `§4.2` prose `pp. 223, 226`
  and used in proof `p. 228`, see `F-U4a-06`)*, then `(f_∇^n)_n` eventually stabilises.
- **Fact 4.14** *(holds even when `∇` is merely an upper bound operator!)*:
  `(i)` `(f_∇^n)_n` is an ascending chain; `(ii)` if `f(f_∇^m) ⊑ f_∇^m` then `∀n > m : f_∇^n = f_∇^m` and
  `⨆_n f_∇^n = f_∇^m`; `(iii)` if `(f_∇^n)_n` stabilises then `∃m : f(f_∇^m) ⊑ f_∇^m`; `(iv)` if `(f_∇^n)_n`
  stabilises then `⨆_n f_∇^n ⊒ lfp(f)`. ■
  - **Proof of `Fact 4.14`** (`p. 227`): `(i)` as in `Fact 4.11`. `(ii)` induction on `n > m` using the guard
    clause. `(iii)` if `∀n > m : f_∇^n = f_∇^m` yet `¬(f(f_∇^m) ⊑ f_∇^m)`, step `m+1` yields
    `f_∇^m = f_∇^{m+1} = f_∇^m ∇ f(f_∇^m) ⊒ f(f_∇^m)`, contradiction. `(iv)` combine `(ii)–(iii)` and
    Tarski's Theorem (`Proposition A.10`). ■
- **`[U4a:4.2.1-c]` Proof of `Proposition 4.13`** (`p. 228`): By contradiction, if `(f_∇^n)_n` never
  stabilises, `Fact 4.14(ii)` forces `f(f_∇^{n-1}) ⊑ f_∇^{n-1}` never to hold (`n > 0`). Define `l₀ = ⊥` and
  `l_n = f(f_∇^{n-1})` (`n > 0`); by `(f_∇^n)_n` ascending (`Fact 4.14(i)`) and monotonicity of `f`, `(l_n)_n`
  is an ascending chain with `∀n : l_n^∇ = f_∇^n`, forcing stabilisation since `∇` is a widening operator,
  contradiction. ■

#### Example 4.15 (Threshold Widening Operator `∇_K` on `Interval`)

Source: [PPA Example 4.15, pp. 228–229] (book p. 228; PDF p. 245) (book p. 229; PDF p. 246).

Let `K ⊆ Z` be a **finite** fixed set of integers (`z_i ∈ Z' = Z ∪ {-∞, ∞}`):
```text
LB_K(z₁, z₃) = z₁    if z₁ ≤ z₃
             = k     if z₃ < z₁  ∧  k = max{k ∈ K | k ≤ z₃}
             = -∞    if z₃ < z₁  ∧  ∀k ∈ K : z₃ < k

UB_K(z₂, z₄) = z₂    if z₄ ≤ z₂
             = k     if z₂ < z₄  ∧  k = min{k ∈ K | z₄ ≤ k}
             = ∞     if z₂ < z₄  ∧  ∀k ∈ K : k < z₄

int₁ ∇_K int₂ = ⊥                                                       if int₁ = int₂ = ⊥
              = [LB_K(inf(int₁), inf(int₂)), UB_K(sup(int₁), sup(int₂))]  otherwise
```
- **Trace (`K = {3, 5}`)**: on `[0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [0,7], …`:
  `[0, 1], [0, 3], [0, 3], [0, 5], [0, 5], [0, ∞], [0, ∞], …`.
- **Verified caveat (`pp. 228–229`)**:
  - **`⊥ ∇_K int₂` step-1 over-widening (`F-U4a-05`)**: because only `int₁ = int₂ = ⊥` returns `⊥`,
    `int₁ = ⊥, int₂ = [z₃, z₄]` (`inf(⊥) = ∞ > z₃`, `sup(⊥) = -∞ < z₄`) jumps on step `f_∇^1 = ⊥ ∇_K f(⊥)`
    to `[LB_K(∞, z₃), UB_K(-∞, z₄)]` (`⊥ ∇_∅ [0, 0] = [-∞, ∞]`) unless `⊥ ∇_K x = x` is special-cased.
  - *Termination proof note (`p. 229`)*: chooses the infinite sequence of strict-jump indices `n₁ < n₂ < ⋯`
    satisfying `∞ > sup(int_{n_i + 1}^∇) > sup(int_{n_i}^∇)` (with consecutive `n_i + 1`), finds `j` above
    `max(K)` (`max(∅) = -∞`), and uses `int_{n_j + 1}^∇ = int_{n_j}^∇ ∇ int_{n_j + 1}` to derive
    `sup(int_{n_j + 1}^∇) = ∞`, contradiction. ■

---

### Section 4.2.2 — Narrowing Operators

#### [U4a:4.2.2-a] Reductive Descent, Narrowing Operators `Δ`, Iterates `([f]_Δ^n)_n`, and `lfp_∇^Δ(f)`

Source: [PPA §4.2.2, p. 230] (book p. 230; PDF p. 247).

*(The opening note states: `"This development can safely be omitted on a first reading."`)* Once widening finds
`f_∇^m ∈ Red(f)` (`f(f_∇^m) ⊑ f_∇^m`), descending `[external: Kleene]` iterates `(f^n(f_∇^m))_n` remain inside `Red(f)` and
above `lfp(f)`, yet need not stabilise. An operator `Δ : L × L → L` is a **narrowing operator** iff:
1. `∀l₁, l₂ ∈ L : l₂ ⊑ l₁ ⇒ l₂ ⊑ (l₁ Δ l₂) ⊑ l₁` *(unconstrained when `l₂ ⋢ l₁`)*, and
2. for **all descending chains** `(l_n)_n`, `(l_n^Δ)_n` eventually stabilises.

- **Important source erratum (`F-U4a-07`)**: prose remarks `"Note that we do not require Δ to be monotone,
  commutative, associative or absorptive"`, overlooking that `l₂ ⊑ l₁ ⇒ l₂ ⊑ (l₁ Δ l₂) ⊑ l₁` at `l₁ = l₂ = l`
  forces `l ⊑ (l Δ l) ⊑ l` and hence **`l Δ l = l`** (absorptiveness holds automatically by antisymmetry
  `[derived]`). Note `(l_n^Δ)_n` is descending whenever `(l_n)_n` is (`Exercise 4.10`).
- Starting from `lfp_∇(f) = f_∇^m` (`f(f_∇^m) ⊑ f_∇^m`), define:
  ```text
  [f]_Δ^n = f_∇^m                         if n = 0
          = [f]_Δ^{n-1} Δ f([f]_Δ^{n-1})  if n > 0
  ```
  and when `[f]_Δ^{m'} = [f]_Δ^{m'+1}`, set `lfp_∇^Δ(f) = [f]_Δ^{m'}`.

#### Lemma 4.16, Display `(4.7)`, and Figure 4.5 (Descending Invariance Inside `Red(f)`)

Source: [PPA Lemma 4.16, pp. 230–232] (book p. 230; PDF p. 247) (book p. 232; PDF p. 249), [PPA Figure 4.5, p. 231] (book p. 231; PDF p. 248).

> If `Δ` is a narrowing operator and `f(f_∇^m) ⊑ f_∇^m` then `([f]_Δ^n)_n` is a descending chain in `Red(f)` and
> `[f]_Δ^n ⊒ f^n(f_∇^m) ⊒ lfp(f)` for all `n`. ■

- **Proof** (`pp. 230–232`): by induction on `n`, establish `(4.7)`:
  ```text
  f^{n+1}(f_∇^m)  ⊑  f([f]_Δ^n)  ⊑  [f]_Δ^{n+1}  ⊑  [f]_Δ^n           (4.7)
  ```
  - *Basis (`n = 0`)*: `f^1(f_∇^m) ⊑ f([f]_Δ^0) ⊑ [f]_Δ^0`, and narrowing gives
    `f([f]_Δ^0) ⊑ [f]_Δ^1 ⊑ [f]_Δ^0`. *(Printed text on `p. 231` leaves `n` uninstantiated instead of `0` in both
    basis displays; see `F-U4a-08`.)*
  - *Step (`n → n+1`)*: monotone `f` applied to `(4.7)` gives `f^{n+2}(f_∇^m) ⊑ f^2([f]_Δ^n) ⊑ f([f]_Δ^{n+1}) ⊑ f([f]_Δ^n)`,
    and since `f([f]_Δ^n) ⊑ [f]_Δ^{n+1}`, chaining yields `f^{n+2}(f_∇^m) ⊑ f([f]_Δ^{n+1}) ⊑ [f]_Δ^{n+1}`,
    where narrowing yields `f([f]_Δ^{n+1}) ⊑ [f]_Δ^{n+2} ⊑ [f]_Δ^{n+1}`.
  - Thus `([f]_Δ^n)_n ⊆ Red(f)` is descending and `f^n(f_∇^m) ⊑ [f]_Δ^n` (`n = 0` trivially; `n > 0` by
    `(4.7)`). Since `f(f_∇^m) ⊑ f_∇^m` implies `f^n(f_∇^m) ∈ Red(f)` by monotonicity, Tarski gives
    `f^n(f_∇^m) ⊒ lfp(f)`. ■
- **`Figure 4.5` (`p. 231`)**: lattice oval diagram of `Red(f)` with minimum `lfp(f)` and descending polyline
  `[f]_Δ^0 = f_∇^m → [f]_Δ^1 → … → [f]_Δ^{m'-1} → [f]_Δ^{m'} = [f]_Δ^{m'+1} = …` staying entirely inside
  `Red(f)` above `lfp(f)`.

#### Proposition 4.17 & `[U4a:4.2.2-b]` Termination of Narrowing and Non-Duality with Widening

Source: [PPA Proposition 4.17, p. 232] (book p. 232; PDF p. 249), [PPA §4.2.2, p. 232] (book p. 232; PDF p. 249).

- **Proposition 4.17**: If `Δ` is a narrowing operator and `f(f_∇^m) ⊑ f_∇^m` then `([f]_Δ^n)_n` eventually
  stabilises. *Proof*: `l₀ = f_∇^m`, `l_n = f([f]_Δ^{n-1})` (`n > 0`) is descending by `Lemma 4.16` and
  monotonicity of `f` (left implicit in text, `F-U4a-06`), with `l_n^Δ = [f]_Δ^n` by induction. ■
- **`[U4a:4.2.2-b]` Non-duality (`p. 232`)**: narrowing is **not** the lattice-theoretic dual of widening —
  `(f_∇^n)_n` may leave `Ext(f)` in order to enter `Red(f)`, whereas `([f]_Δ^n)_n` starts inside `Red(f)` and
  remains inside `Red(f)` at every step (dualising `Fact 4.14(iv)` `lfp_∇(f) ⊒ lfp(f)`, a true dual widening
  yields an **under**-approximation `⊑ gfp(f)`, approaching `gfp(f)` from below `[derived]`).

#### Example 4.18 (Threshold Narrowing Operator `Δ_N` on `Interval`)

Source: [PPA Example 4.18, pp. 232–233] (book p. 232; PDF p. 249) (book p. 233; PDF p. 250).

For fixed integer `N ≥ 0`:
```text
int₁ Δ_N int₂ = ⊥          if int₁ = ⊥  ∨  int₂ = ⊥
              = [z₁, z₂]   otherwise
  where z₁ = inf(int₁)  if N < inf(int₂) ∧ sup(int₂) = ∞,   else inf(int₂)
        z₂ = sup(int₁)  if inf(int₂) = -∞ ∧ sup(int₂) < -N, else sup(int₂)
```
- **Trace (`N = 3`)**: `[0,∞], [1,∞], [2,∞], [3,∞], [4,∞], [5,∞], …` yields `[0,∞], [1,∞], [2,∞], [3,∞], [3,∞], …`.
- **Proof (`p. 233`)**: `int₂ ⊑ int₁ ⇒ int₂ ⊑ int₁ Δ_N int₂ ⊑ int₁` follows by cases on `int₂ = ⊥`. Any
  descending chain `(int_n)_n` yields descending `(int_n^Δ)_n` (`Exercise 4.10`); failure to stabilise would
  eventually avoid `[-∞, ∞]` and `⊥`, leave `sup = ∞` or `inf = -∞` (since bounded `[a, b]` has finitely
  many sub-intervals `[derived]`), and (w.l.o.g. assuming `sup = ∞` and `inf ∈ Z` via chain monotonicity,
  left implicit `F-U4a-06`) force `inf(int_{n₂}^Δ) > N`, freezing `int_n^Δ = int_{n₂}^Δ` for all `n ≥ n₂`,
  contradiction. *(Notice whenever both bounds of `int₂` are finite, `Δ_N` adopts `[inf(int₂), sup(int₂)]`
  regardless of `N`, so shrinking finite bounds may take many finite steps; the book states no bound `[derived]`.)* ■

---

## Section 4.3 — Galois Connections

#### [U4a:4.3-a] Galois Connections `(4.8)`–`(4.9)` and Figure 4.6

Source: [PPA §4.3, pp. 233–235] (book p. 233; PDF p. 250) (book p. 235; PDF p. 252), [PPA Figure 4.6, p. 235] (book p. 235; PDF p. 252).

Between complete lattices `(L, ⊑)` and `(M, ⊑)`, `(L, α, γ, M)` (diagrammed `L ⇄ M` with upper arrow
`γ : M → L` right-to-left and lower arrow `α : L → M` left-to-right) is a **Galois connection** iff:
1. `α : L → M` (*abstraction*) and `γ : M → L` (*concretisation*) are **monotone**, and
2. satisfy `(4.8)` and `(4.9)`:
   ```text
   γ ∘ α  ⊒  λl. l                                                    (4.8)
   α ∘ γ  ⊑  λm. m                                                    (4.9)
   ```
- **`Figure 4.6` (`p. 235`)**: two-oval diagram of `L` (containing inner oval `γ[M]`) and `M` (containing inner
  oval `α[L]`); `l ∈ L` maps via `α` to `α(l) ⊑ m` inside `α[L]`, `m` maps via `γ` to `γ(m)` inside `γ[M]`
  above `γ(α(l)) ⊒ l`.

#### Example 4.19 (`(𝒫(Z), α_ZI, γ_ZI, Interval)`)

Source: [PPA Example 4.19, pp. 234–236] (book p. 234; PDF p. 251) (book p. 236; PDF p. 253).

```text
γ_ZI : Interval → 𝒫(Z),     γ_ZI(int) = {z ∈ Z | inf(int) ≤ z ≤ sup(int)}
α_ZI : 𝒫(Z) → Interval,     α_ZI(Z)   = ⊥                      if Z = ∅
                                      = [inf'(Z), sup'(Z)]     otherwise
```
Examples: `γ_ZI([0, 3]) = {0, 1, 2, 3}`, `γ_ZI([0, ∞]) = {z ∈ Z | z ≥ 0}`, `α_ZI({0, 1, 3}) = [0, 3]`,
`α_ZI({2 * z | z > 0}) = [2, ∞]`. Both `α_ZI` and `γ_ZI` are monotone, `γ_ZI(α_ZI(Z)) ⊇ Z`, and
`α_ZI(γ_ZI(int)) = int` (strict equality, previewing Galois insertions). *(Branch `Z = ∅ ⇒ ⊥` is essential
since `[inf'(∅), sup'(∅)] = [∞, -∞] ∉ Interval` `[derived]`.)* ■

#### [U4a:4.3-b] & Proposition 4.20 (Adjunctions `(4.10)` Equivalence)

Source: [PPA §4.3, p. 236] (book p. 236; PDF p. 253), [PPA Proposition 4.20, p. 236] (book p. 236; PDF p. 253).

`(L, α, γ, M)` is an **adjunction** iff total functions `α : L → M` and `γ : M → L` (monotonicity NOT assumed
a priori) satisfy:
```text
α(l) ⊑ m    ⇔    l ⊑ γ(m)         (∀l ∈ L, m ∈ M)                  (4.10)
```
> **Proposition 4.20**: `(L, α, γ, M)` is an adjunction if and only if `(L, α, γ, M)` is a Galois connection. ■

- **Proof** (`p. 236`):
  - *(GC ⇒ Adj)*: `α(l) ⊑ m ⇒ l ⊑ γ(α(l)) ⊑ γ(m)` by `(4.8)` and monotonicity of `γ`;
    `l ⊑ γ(m) ⇒ α(l) ⊑ α(γ(m)) ⊑ m` by `(4.9)` and monotonicity of `α`.
  - *(Adj ⇒ GC)*: `m = α(l)` in `(4.10)` yields `l ⊑ γ(α(l))` `(4.8)`; `l = γ(m)` yields `α(γ(m)) ⊑ m` `(4.9)`.
    If `l₁ ⊑ l₂`, `(4.8)` gives `l₁ ⊑ l₂ ⊑ γ(α(l₂))`, so `(4.10)` gives `α(l₁) ⊑ α(l₂)`; monotonicity of `γ`
    is dual. ■

#### [U4a:4.3-c] Galois Connections Induced by `β` and Extraction Functions `η` (`Figure 4.7`, `Example 4.21`)

Source: [PPA §4.3, pp. 237–238] (book p. 237; PDF p. 254) (book p. 238; PDF p. 255), [PPA Figure 4.7, p. 238] (book p. 238; PDF p. 255), [PPA Example 4.21, p. 238] (book p. 238; PDF p. 255).

- **From representation `β : V → L`**: defines `(𝒫(V), α, γ, L)` by:
  ```text
  α(V') = ⨆{β(v) | v ∈ V'},        γ(l) = {v ∈ V | β(v) ⊑ l}
  ```
  Adjunction verified (`p. 237`): `α(V') ⊑ l ⇔ (∀v ∈ V' : β(v) ⊑ l) ⇔ V' ⊆ γ(l)`; moreover `α({v}) = β(v)`
  (commuting triangle on `p. 237`).
- **From extraction function `η : V → D`** (special case `L = (𝒫(D), ⊆)`, `β_η(v) = {η(v)}`): defines
  `(𝒫(V), α_η, γ_η, 𝒫(D))` via direct/inverse images (square diagram on `p. 238`):
  ```text
  α_η(V') = {η(v) | v ∈ V'},       γ_η(D') = {v ∈ V | η(v) ∈ D'}
  ```
- **`Figure 4.7` & `Example 4.21` (`p. 238`)**: 8-element Boolean cube Hasse diagram of
  `(𝒫(Sign), ⊆)` for `Sign = {-, 0, +}`, instantiated by `sign : Z → Sign` to
  `(𝒫(Z), α_sign, γ_sign, 𝒫(Sign))`. ■

---

### Section 4.3.1 — Properties of Galois Connections

#### Lemma 4.22 & [U4a:4.3.1-a] Uniqueness, Adjoint Terminology, and Complete Additivity/Multiplicativity

Source: [PPA Lemma 4.22, p. 239] (book p. 239; PDF p. 256), [PPA §4.3.1, p. 239] (book p. 239; PDF p. 256).

> **Lemma 4.22**: If `(L, α, γ, M)` is a Galois connection then:
> **(i)** `α` uniquely determines `γ(m) = ⨆{l | α(l) ⊑ m}` and `γ` uniquely determines `α(l) = ⨅{m | l ⊑ γ(m)}`.
> **(ii)** `α` is *completely additive* (`α(⨆ L') = ⨆{α(l) | l ∈ L'}`) and `γ` is *completely multiplicative*
> (`γ(⨅ M') = ⨅{γ(m) | m ∈ M'}`). In particular `α(⊥) = ⊥` and `γ(⊤) = ⊤`. ■

- **Proof** (`p. 239`): *(i)* `(4.10)` makes `{l | α(l) ⊑ m} = {l | l ⊑ γ(m)}`, whose lub is `γ(m)` (typo
  `"are Galois connection"` on proof line 4, `F-U4a-01`), and dually for `α(l)`. *(ii)*
  `α(⨆ L') ⊑ m ⇔ ⨆ L' ⊑ γ(m) ⇔ (∀l ∈ L' : l ⊑ γ(m)) ⇔ (∀l ∈ L' : α(l) ⊑ m) ⇔ ⨆ α[L'] ⊑ m`; setting `L' = ∅`
  gives `α(⊥) = ⊥`, and dually `γ(⨅ M') = ⨅ γ[M']` gives `γ(⊤) = ⊤`. ■
- **`[U4a:4.3.1-a]`**: `α` is the **lower** (or **left**) **adjoint** of `γ`; `γ` is the **upper** (or **right**)
  **adjoint** of `α`. *(Neither `α(⊤_L) = ⊤_M` nor `γ(⊥_M) = ⊥_L` holds in general `[derived]`.)*

#### Lemma 4.23 (Existence from One-Sided Complete Additivity / Multiplicativity)

Source: [PPA Lemma 4.23, pp. 239–240] (book p. 239; PDF p. 256) (book p. 240; PDF p. 257).

> If `α : L → M` is completely additive then there exists (unique) `γ : M → L` such that `(L, α, γ, M)` is a
> Galois connection. Similarly, if `γ : M → L` is completely multiplicative then there exists (unique)
> `α : L → M` such that `(L, α, γ, M)` is a Galois connection. ■

- **Proof** (`p. 240`): define `γ(m) = ⨆{l' | α(l') ⊑ m}`; then `α(l) ⊑ m ⇒ l ⊑ γ(m)`, and conversely
  `l ⊑ γ(m) ⇒ α(l) ⊑ α(⨆{l' | α(l') ⊑ m}) = ⨆{α(l') | α(l') ⊑ m} ⊑ m` (via monotonicity of completely
  additive `α` and `Proposition 4.20`). Symmetrically for `γ`, set `α(l) = ⨅{m' | l ⊑ γ(m')}`. ■

#### Fact 4.24 (Zig-Zag Idempotence)

Source: [PPA Fact 4.24, p. 240] (book p. 240; PDF p. 257).

> If `(L, α, γ, M)` is a Galois connection then `α ∘ γ ∘ α = α` and `γ ∘ α ∘ γ = γ`. ■

- **Proof** (`p. 240`): `λl.l ⊑ γ ∘ α` gives `α ⊑ α ∘ γ ∘ α` by monotonicity of `α`, while `α ∘ γ ⊑ λm.m` gives
  `α ∘ γ ∘ α ⊑ α`; antisymmetry gives `α ∘ γ ∘ α = α`, and dually `γ ∘ α ∘ γ = γ`. ■

#### Example 4.25 (Non-Existence of Adjoint `α_IS : Interval → 𝒫(Sign)`)

Source: [PPA Example 4.25, pp. 240–241] (book p. 240; PDF p. 257) (book p. 241; PDF p. 258).

Define monotone `γ_IS : 𝒫(Sign) → Interval` by:
```text
γ_IS({-, 0, +}) = [-∞, ∞]       γ_IS({-, 0}) = [-∞, 0]
γ_IS({-, +})    = [-∞, ∞]       γ_IS({0, +}) = [0, ∞]
γ_IS({-})       = [-∞, -1]      γ_IS({0})    = [0, 0]
γ_IS({+})       = [1, ∞]        γ_IS(∅)      = ⊥
```
Using `Appendix A Lemma A.4` on finite `𝒫(Sign)`, `γ_IS` satisfies `(i)` monotonicity and `(ii)`
`γ_IS(⊤) = [-∞, ∞]`, leaving condition `(iii)` `γ_IS(S₁ ∩ S₂) = γ_IS(S₁) ⊓ γ_IS(S₂)` across the `9`
unordered incomparable pairs (`F-U4a-09`): testing `({-, 0}, {-, +})` yields:
```text
γ_IS({-, 0} ∩ {-, +})       = γ_IS({-})         = [-∞, -1]
γ_IS({-, 0}) ⊓ γ_IS({-, +}) = [-∞, 0] ⊓ [-∞, ∞] = [-∞, 0]
```
Since `[-∞, -1] ≠ [-∞, 0]`, `γ_IS` is **not** completely multiplicative, and by `Lemmas 4.22–4.23` **no**
`α_IS` makes `(Interval, α_IS, γ_IS, 𝒫(Sign))` a Galois connection! ■

#### [U4a:4.3.1-b] Transporting Correctness Relations and Representations Along `(L, α, γ, M)`

Source: [PPA §4.3.1, pp. 241–242] (book p. 241; PDF p. 258) (book p. 242; PDF p. 259).

Given `R : V × L → {true, false}` satisfying `(4.4)` and `(4.5)` and Galois connection `(L, α, γ, M)`,
define `S : V × M → {true, false}` by:
```text
v S m    iff    v R (γ(m))
```
- `(4.4)` holds for `S` by monotonicity of `γ` and `(4.4)` for `R`.
- `(4.5)` holds for `S` **specifically by complete multiplicativity of `γ`** (`Lemma 4.22(ii)`):
  `(∀m ∈ M' : v R (γ(m))) ⇒ v R (⨅{γ(m) | m ∈ M'}) = v R (γ(⨅ M')) ⇒ v S (⨅ M')`.
- If `R` is generated by `β : V → L`, then `v S m ⇔ β(v) ⊑ γ(m) ⇔ (α ∘ β)(v) ⊑ m` (`Proposition 4.20`), so
  `S` is generated by **`α ∘ β : V → M`**.

---

### Section 4.3.2 — Galois Insertions

#### [U4a:4.3.2-a], Figure 4.8, and Example 4.26 (Galois Insertions `α ∘ γ = λm.m`)

Source: [PPA §4.3.2, pp. 242–243] (book p. 242; PDF p. 259) (book p. 243; PDF p. 260), [PPA Figure 4.8, p. 243] (book p. 243; PDF p. 260), [PPA Example 4.26, p. 243] (book p. 243; PDF p. 260).

- `(L, α, γ, M)` is a **Galois insertion** iff `α, γ` are monotone, `γ ∘ α ⊒ λl.l`, and:
  ```text
  α ∘ γ = λm. m
  ```
- **`Figure 4.8` (`p. 243`)**: specialisation of `Figure 4.6` where inner oval `α[L]` fills all of `M`; `l ∈ L`
  maps via `α` to `α(l) ∈ M`, `γ` lifts `α(l)` to `γ(α(l))` inside `γ[M]`, and `α(γ(α(l))) = α(l)`.
- **`Example 4.26`**: from `Example 4.19`, `(𝒫(Z), α_ZI, γ_ZI, Interval)` is a Galois insertion. ■

#### Lemma 4.27 (Four Equivalent Characterisations of Galois Insertions)

Source: [PPA Lemma 4.27, pp. 243–244] (book p. 243; PDF p. 260) (book p. 244; PDF p. 261).

> For any Galois connection `(L, α, γ, M)`, the following are equivalent:
> **(i)** `(L, α, γ, M)` is a Galois insertion (`α ∘ γ = λm.m`);
> **(ii)** `α` is surjective (`∀m ∈ M : ∃l ∈ L : α(l) = m`);
> **(iii)** `γ` is injective (`∀m₁, m₂ ∈ M : γ(m₁) = γ(m₂) ⇒ m₁ = m₂`);
> **(iv)** `γ` is an order-similarity (`∀m₁, m₂ ∈ M : γ(m₁) ⊑ γ(m₂) ⇔ m₁ ⊑ m₂`). ■

- **Proof** (`pp. 243–244`): `(i) ⇒ (iii)` via `γ(m₁) = γ(m₂) ⇒ α(γ(m₁)) = α(γ(m₂)) ⇒ m₁ = m₂`; `(iii) ⇒ (ii)`
  via `γ(α(γ(m))) = γ(m)` (`Fact 4.24`) giving `α(γ(m)) = m`; `(ii) ⇒ (iv)` via `γ(α(l₁)) ⊑ γ(α(l₂)) ⇒ α(γ(α(l₁))) ⊑ α(γ(α(l₂)))`; `(iv) ⇒ (i)` via `α(γ(m₁)) ⊑ m₂ ⇔ γ(m₁) ⊑ γ(m₂) ⇔ m₁ ⊑ m₂`.
- **Extraction corollary (`p. 244`)**: `(𝒫(V), α_η, γ_η, 𝒫(D))` is a Galois insertion **iff `η : V → D` is surjective**.

#### Example 4.28 (`signparity` Non-Insertion)

Source: [PPA Example 4.28, p. 244] (book p. 244; PDF p. 261).

`signparity : Z → Sign × Parity` (`Parity = {odd, even}`): `(0, odd)` describes no integer
(`γ_{signparity}({(0, odd)}) = ∅ = γ_{signparity}(∅)`), so `signparity` is non-surjective and
`(𝒫(Z), α_{signparity}, γ_{signparity}, 𝒫(Sign × Parity))` is a Galois connection that is **not** a Galois
insertion. ■

#### [U4a:4.3.2-b], Proposition 4.29, Figure 4.9, Facts 4.30–4.31, and [U4a:4.3.2-c] Reduction Operator `ς`

Source: [PPA Proposition 4.29, p. 244] (book p. 244; PDF p. 261), [PPA Figure 4.9, p. 245] (book p. 245; PDF p. 262), [PPA Fact 4.30, p. 245] (book p. 245; PDF p. 262), [PPA Fact 4.31, pp. 245–246] (book p. 245; PDF p. 262) (book p. 246; PDF p. 263), [PPA §4.3.2, p. 246] (book p. 246; PDF p. 263).

- **`Proposition 4.29`**: For any Galois connection `(L, α, γ, M)`, define the **reduction operator** `ς : M → M`
  (`\varsigma`, `[U4a:4.3.2-b]`):
  ```text
  ς(m) = ⨅{m' | γ(m) = γ(m')}
  ```
  Then `ς[M] = ({ς(m) | m ∈ M}, ⊑_M)` is a complete lattice and `(L, α, γ, ς[M])` is a Galois insertion
  *(corestricting `α` and restricting `γ` to `ς[M]`, `F-U4a-10`)*.
- **`Figure 4.9` (`p. 245`)**: depicts `m ∈ M` outside `α[L]` and `α(l) = α(γ(m)) ∈ α[L]` mapping via dotted
  `γ` arcs to the identical `γ(α(l)) ∈ γ[M] ⊆ L`, while dashed arrow `ς` collapses `m` down onto `α(l)`.
- **`Fact 4.30`**: `α[L] = ({α(l) | l ∈ L}, ⊑_M)` is a complete lattice with `⨆_{α[L]} M' = ⨆_M M'` (proved
  using `l = ⨆_L γ[M']`, `Fact 4.24`, `Lemma 4.22(ii)`, and `Appendix A Lemma A.2`; note meets in `α[L]` are
  `ς(⨅_M M') = α(⨅_L γ[M'])`, which can be strictly smaller than `⨅_M M'` `[derived]`). ■
- **`Fact 4.31`** (`pp. 245–246`; stray prime `=ˊ∏` on `p. 245`, `F-U4a-01`): `ς(m) = α(γ(m))` and hence
  `α[L] = ς[M]`. *Proof (`p. 246`)*: `γ(m) = γ(α(γ(m)))` gives `ς(m) ⊑ α(γ(m))`; conversely
  `α(γ(m)) ⊑ ς(m) ⇔ γ(m) ⊑ γ(ς(m)) = ⨅{γ(m') | γ(m') = γ(m)} = γ(m)` by `Lemma 4.22(ii)`; `α(l) = ς(α(l))`
  and `ς(m) = α(γ(m))` give `α[L] = ς[M]`. ■
- **`[U4a:4.3.2-c]` Proof of `Proposition 4.29`** (`p. 246`): `ς[M] = α[L]` is a complete lattice (`Facts 4.30–4.31`);
  `(L, α, γ, α[L])` inherits `(4.10)` (`Proposition 4.20`) with surjective `α`, hence is a Galois insertion by
  `Lemma 4.27`. ■

#### [U4a:4.3.2-d], Example 4.32, and [U4a:4.3.2-e] Extraction Reduction `ς_η`, Isomorphisms, and Boundary to `§4.4`

Source: [PPA §4.3.2, p. 246] (book p. 246; PDF p. 263), [PPA Example 4.32, p. 246] (book p. 246; PDF p. 263).

- For extraction `(𝒫(V), α_η, γ_η, 𝒫(D))`, the reduction operator `ς_η : 𝒫(D) → 𝒫(D)` is:
  ```text
  ς_η(D') = D' ∩ η[V]      (η[V] = {η(v) | v ∈ V})
  ```
  and `ς_η[𝒫(D)]` is isomorphic (in fact set-equal `[derived]`, `F-U4a-10`) to `𝒫(η[V])` (`Exercise 4.14`).
- **Isomorphism of Galois connections**: `(L₁, α₁, γ₁, M₁)` is *isomorphic* to `(L₂, α₂, γ₂, M₂)` iff there
  exist lattice isomorphisms `θ_L : L₁ → L₂` and `θ_M : M₁ → M₂` (`Appendix A`) satisfying:
  ```text
  α₂ = θ_M ∘ α₁ ∘ θ_L^{-1}      and      γ₂ = θ_L ∘ γ₁ ∘ θ_M^{-1}
  ```
- **`Example 4.32` (`p. 246`)**: `signparity[Z] = {(-, odd), (-, even), (0, even), (+, odd), (+, even)}`
  yields the `32`-element Galois insertion `(𝒫(Z), α_{signparity}, γ_{signparity}, 𝒫(signparity[Z]))`. ■
- **`[U4a:4.3.2-e]` Unit 4a/4b Boundary (book p. 246; PDF p. 263)**: directly below `Example 4.32`, section
  `4.4 Systematic Design of Galois Connections` begins (`Sequential composition.`, continuing to
  `Example 4.33` on `p. 247` in Unit 4b) [PPA §4.4, p. 246] (book p. 246; PDF p. 263).

---

## Projections

### `software_engineering`

- **Specification Oracle vs Canonical Codec vs Bidirectional Adapter `[external]`**: Correctness relation
  `R : V × L → {true, false}` acts as a behavioral conformance predicate (`§4.1.1`), whereas axioms `(4.4)`
  and `(4.5)` turn `R` into a canonical encoder `β_R(v) = ⨅{l | v R l}` (`Lemma 4.5`), and lifting `β` to
  `(𝒫(V), α, γ, L)` yields a lossless/sound bidirectional adapter (`§4.3`, `(4.10)`).
- **Numerical Domain (`Interval`) Engineering Invariants `[external]`**: Enforce disjoint `⊥` (never
  degenerate `[∞, ∞]` / `[-∞, -∞]` structs that violate `γ`-injectivity in `Lemma 4.27`), use `[external: BigInt]` or
  conservative `∓∞` saturation rather than `[external: int64 wraparound]`, implement branch-guard `⊓`, and keep relational
  domains (`[external: Zones/Octagons, Miné]`) unclosed across the left operand of widening (`m₁ ∇ ς(f(m₁))`,
  never `ς(m₁ ∇ m₂)` which breaks chain stabilisation).
- **Two-Stage Fixed-Point Architecture (`∇_K` + `Δ_N`) & Cutset Placement `[external]`**: Separate
  termination acceleration (`∇_K` with fixed loop literals `K` placed strictly at a `[external: CFG loop-cutset]` /
  feedback vertex set `[external: Bourdoncle WTO]`) from post-stabilisation precision recovery (`Δ_N` bounded
  at `k ∈ {1..3}` passes inside `Red(f)`).
- **Concretisation-First Property Testing & Flyweight Product Normalisation (`ς`) `[external]`**: Before
  coding `α`, `[external: property-test]` `γ` for monotonicity, `γ(⊤) = ⊤`, and binary meet preservation (`Lemma A.4`,
  `Example 4.25`); when products contain empty ghost states like `(0, odd)` (`Example 4.28`), canonicalise
  with `ς = α ∘ γ` (`Proposition 4.29`) so syntactic state equality matches semantic equality (`Lemma 4.27`).

### `cybersecurity`

- **First-Order Safety vs 2-Safety Security Hyperproperties (`§4.1`, `p. 212`) `[external]`**: `§4.1`'s mundane
  relation `R ⊆ V × L` covers single-state safety vulnerabilities (`[external: CWE-787]` OOB writes, `[external: CWE-125]` OOB reads,
  `[external: CWE-476]` null dereferences), but **cannot** directly express `[external: 2-safety relational hyperproperties]`
  (`[external: CWE-208]` timing side-channels, `[external: non-interference]`, taint dependency `[external: Clarkson & Schneider]`)
  without switching to relational/product-program semantics (`𝒫(V × V)`) or second-order correctness relations
  governed by `§§4.2–4.5`.
- **Sound Loop Array-Bounds Checking & Integer Wraparound Trap (`[external: CWE-190]` → `[external: CWE-787]`) `[external]`**:
  Because `∇` and valid `Δ` inside `Red(f)` guarantee `[f]_Δ^n ⊒ lfp(f)` (`Fact 4.14`, `Lemma 4.16`),
  interval widening/narrowing never drops reachable array-bounds violations *within mathematical `Z`*;
  however, applying `Interval` (`Z`) directly to fixed-width machine arithmetic (`[external: int32/uint32]`) silently
  misses `[external: CWE-190 two's-complement wraparound]` into negative indices (`[external: wrapped intervals]`).
- **Ghost Attack-Surface Pruning (`ς`) & Coarsening Soundness (`§4.3.1`) `[external]`**: Coarsening heavy
  security lattices `L` along `(L, α, γ, M)` automatically preserves Moore-family correctness `v S m ⇔ v R γ(m)`
  (`Lemma 4.22(ii)`), while reduction `ς` eliminates impossible product states (e.g. `[0, 0] × nonnull`) from
  triage queues.

### `cs_theory`

- **Category-Theoretic Adjunction `α ⊣ γ` (`(4.10)`) `[external]`**: On posets viewed as thin categories,
  `(4.10)` is the `[external: hom-set]` natural isomorphism `Hom_M(α(l), m) ≅ Hom_L(l, γ(m))`, `(4.8)` is unit `id_L ⊑ γ ∘ α`,
  `(4.9)` is counit `α ∘ γ ⊑ id_M`, `Fact 4.24` expresses the triangle identities, `Lemma 4.22(ii)` states
  `[external: LAPL/RAPL]` (`α` preserves all `[external: colimits]` `⨆`; `γ` preserves all limits `⨅`), and `Lemma 4.23` is the `[external: Posetal Adjoint Functor Theorem]`.
- **Cousot–Cousot Closure/Moore-Family Correspondence `[external]`**: For any Galois connection `(L, α, γ, M)`,
  `ρ = γ ∘ α : L → L` is an upper closure operator whose image `γ[M]` is a Moore family in `L` (`(4.5)`),
  while `ς = α ∘ γ : M → M` is a `[external: kernel operator]` whose image `α[L]` is `⨆_M`-closed (`Fact 4.30`); Galois
  insertions correspond 1-to-1 (up to `(θ_L, θ_M)` isomorphism) to Moore families of `L` (`§4.3.2`).
- **Higher-Order `(β₁ ↠ β₂)(↝)` Previewing `U6` (`§4.5`) `[derived]`**: Under `§4.3`'s `β`-induced
  connection `(𝒫(V_i), α_i, γ_i, L_i)`, `(β₁ ↠ β₂)(↝)(l₁)` equals `α₂(post_↝(γ₁(l₁)))`, anticipating Chapter 4
  `§4.5`'s best induced abstract transformer `α₂ ∘ f ∘ γ₁`.
- **`[external: Kleene]` vs Transfinite Ordinals & Non-Duality (`Figure 4.3`, `§4.2.2`)**: Non-continuous monotone `f` may
  need transfinite ordinals (`Appendix A §A.4`) to reach `lfp(f)` above `⨆_{n<ω} f^n(⊥)`; `∇` dynamically
  enforces ACC to hit `Red(f)` in `< ω` steps, whereas `Δ` enforces DCC strictly inside `Red(f)` (NOT the
  `Ext(f)` dual of widening).

### `debugging`

- **Triage Split: Unsoundness (`f`/`⊑`/`⊓`) vs Over-Widening (`[-∞, ∞]`) `[derived]`**: Because valid `∇`
  and `Δ` (from `f(x) ⊑ x`) satisfy `[f]_Δ^n ⊒ lfp(f)` (`Fact 4.14`, `Lemma 4.16`), any missed concrete state
  in an analyser trace comes from transfer `f`, order `⊑`, guard meet `⊓` (`Example 4.10`), `[external: integer wraparound]`,
  or prematurely narrowing before `f(x) ⊑ x` holds — never from widening itself; conversely, `[-∞, ∞]` blowups
  trace to missing `⊥ ∇ x = x` (`F-U4a-05`), unseeded thresholds `K`, or widening at non-loop joins.
- **Non-Termination Despite Widening `[derived]`**: Root causes: `(1)` reversed operands `f(x) ∇ x` instead
  of `x ∇ f(x)` (`Example 4.12` asymmetry freezes `[external: Kleene]` steps `[0,n] ∇ [0,n-1] = [0,n]`), `(2)` mutating
  `K` dynamically during iteration (breaks finiteness in `Example 4.15` proof), `(3)` cycles without a widening
  cutpoint, or `(4)` closing `[external: octagons]` *after* widening.
- **Non-Monotonicity of `∇_K` Breaking Worklist Caching `[derived]`**: `[1, 1] ⊑ [0, 2]` yet
  `[1, 1] ∇_∅ [1, 2] = [1, ∞] ⋢ [0, 2] = [0, 2] ∇_∅ [1, 2]`; solvers must never assume `x ⊑ y ⇒ x ∇ z ⊑ y ∇ z`
  and must stabilise inner SCCs before widening outer loops.

---

## Findings (Source Errata, Implicit Hypotheses, and OCR Corruptions)

### Verified Source Errata & Edge-Case Candidates (`F-U4a-01..10`)

- **`F-U4a-01` (Typographical Print Artifacts, `pp. 213, 239, 245`)**: `Example 4.2` last line prints
  `"as in indeed the case"` (`"in"` for `"is"`); `Lemma 4.22` proof line 4 prints `"are Galois connection"`
  (singular); `Fact 4.31` display (`p. 245`) prints stray acute mark `=ˊ∏` and `γ(m') = γ(m)` instead of
  `γ(m) = γ(m')` (`Proposition 4.29`, `p. 244`) [PPA Example 4.2, p. 213] (book p. 213; PDF p. 230); [PPA Lemma 4.22, p. 239] (book p. 239; PDF p. 256); [PPA Fact 4.31, p. 245] (book p. 245; PDF p. 262).
- **`F-U4a-02` (Missing `σ̂ ≠ ⊥` Guard & `ι = σ̂₁` / `FV(S⋆)` Restriction in `CP`, `Examples 4.1, 4.3, 4.6`)**:
  `Example 4.3` defines `σ R_CP σ̂` without guarding `σ̂ ≠ ⊥` even though `⊥ ∈ (Var⋆ → Z^⊤)_⊥` (`Example 4.1`)
  is non-functional; `Example 4.1` ties `ι = λx.⊤ = σ̂₁`, and `Example 4.3`/`4.6` shift between `FV(S⋆)`,
  `Var`, and `Var⋆` [PPA Example 4.1, pp. 212–213] (book p. 212; PDF p. 229) (book p. 213; PDF p. 230); [PPA Example 4.3, p. 215] (book p. 215; PDF p. 232); [PPA Example 4.6, p. 217] (book p. 217; PDF p. 234).
- **`F-U4a-03` (Ill-Typed Prose Union & Determinacy/Domain Slips in `0-CFA`, `Examples 4.2, 4.4, 4.7`)**:
  `Example 4.7` prose prints `⋃{β_CFA(ρ(x)) | x ∈ Var⋆}` (pair instead of set, omits `dom(ρ)`), whereas the
  displayed `β_CFA^E : Env → Env̂` fixes it; `Example 4.2` assumes an unspecified
  solution `(Ĉ, ρ̂)` for deterministic `⊳` and `[con]` freedom on `Table 3.1`, while `Examples 4.4, 4.7` use
  `Val` without restricting closure subterms to `Term⋆` [PPA Example 4.2, p. 213] (book p. 213; PDF p. 230); [PPA Example 4.4, pp. 215–216] (book p. 215; PDF p. 232) (book p. 216; PDF p. 233); [PPA Example 4.7, p. 218] (book p. 218; PDF p. 235).
- **`F-U4a-04` (Metavariable Slip `Example 4.9` & Overloaded `Z` `Example 4.10`)**: `Example 4.9` (`p. 220`)
  switches to generic `p` in `(β_{Z×Z} ↠ β_Z)(p ⊢ · ↝ ·) = …` two lines above specialising back to `plus`;
  `Example 4.10` (`p. 222`) uses italic `Z` for an arbitrary subset of bold `Z' = Z ∪ {-∞, ∞}` [PPA Example 4.9, p. 220] (book p. 220; PDF p. 237); [PPA Example 4.10, p. 222] (book p. 222; PDF p. 239).
- **`F-U4a-05` (`⊥ ∇_K [z₃, z₄]` Step-1 Over-Widening in `Example 4.15`, `pp. 228–229`)**: `Example 4.15`
  special-cases only `int₁ = int₂ = ⊥`; `⊥ ∇_K [z₃, z₄]` hits `LB_K(∞, z₃)` and `UB_K(-∞, z₄)` (`⊥ ∇_∅ [0, 0] = [-∞, ∞]`), discarding initial bounds on `f_∇^1` unless `⊥ ∇_K x = x` is added [PPA Example 4.15, pp. 228–229] (book p. 228; PDF p. 245) (book p. 229; PDF p. 246).
- **`F-U4a-06` (Implicit Hypotheses in `Prop 4.13`, `Prop 4.17`, and `Ex 4.18`, `pp. 227, 232–233`)**:
  `Proposition 4.13` standalone box omits `"f monotone"` (inherited from `§4.2` prose `pp. 223, 226` and used in proof `p. 228`);
  `Proposition 4.17` (`p. 232`) box and proof omit citing monotonicity of `f` for descending `(l_n)_n`; `Example 4.18`
  (`p. 233`) jumps directly from `∀n ≥ n₁ : sup = ∞ ∨ inf = -∞` to fixed `sup = ∞, inf ∈ Z` via tacit
  chain monotonicity [PPA Proposition 4.13, p. 227] (book p. 227; PDF p. 244); [PPA Proposition 4.17, p. 232] (book p. 232; PDF p. 249); [PPA Example 4.18, p. 233] (book p. 233; PDF p. 250).
- **`F-U4a-07` (Contradicted `"Non-Absorptive"` Remark for Narrowing `Δ`, `p. 230`)**: `§4.2.2` states `Δ` is
  not required to be absorptive (`l Δ l = l`), yet axiom `l₂ ⊑ l₁ ⇒ l₂ ⊑ (l₁ Δ l₂) ⊑ l₁` at `l₁ = l₂ = l`
  forces `l ⊑ (l Δ l) ⊑ l`, i.e. **`l Δ l = l` holds for every narrowing operator `Δ`** `[derived]`
  [PPA §4.2.2, p. 230] (book p. 230; PDF p. 247).
- **`F-U4a-08` (Uninstantiated Variable `n` in `Lemma 4.16` Basis `n = 0`, `p. 231`)**: Both displays under
  `"For the basis (n = 0)"` print symbolic `n` instead of `0` (`f^1(f_∇^m) ⊑ f([f]_Δ^0) ⊑ [f]_Δ^0` and
  `f([f]_Δ^0) ⊑ [f]_Δ^1 ⊑ [f]_Δ^0`) [PPA Lemma 4.16, p. 231] (book p. 231; PDF p. 248).
- **`F-U4a-09` (Ordered vs Unordered Pairs in `Example 4.25`, `p. 241`)**: Prose says `"all pairs (S₁, S₂)"`
  yet lists the `9` unordered incomparable pairs (sufficient by symmetry of `∩`/`⊓`, `p. 241`) [PPA Example 4.25, p. 241] (book p. 241; PDF p. 258).
- **`F-U4a-10` (Domain/Codomain Restriction & Equality vs Isomorphism, `pp. 237, 244, 246`)**: `{v | η(v) ∈ D'}`
  (`p. 237`) omits `∈ V`; `(L, α, γ, ς[M])` (`Proposition 4.29`, `pp. 244, 246`) and `Example 4.32` (`p. 246`)
  reuse `α, γ` without restricting codomain/domain to `ς[M]`; `ς_η[𝒫(D)]` (`p. 246`) is set-theoretically
  equal to `𝒫(η[V])` rather than merely isomorphic [PPA §4.3, p. 237] (book p. 237; PDF p. 254); [PPA Proposition 4.29, p. 244] (book p. 244; PDF p. 261); [PPA §4.3.2, p. 246] (book p. 246; PDF p. 263).

### OCR Text-Layer Damage Logged (`PDF pp. 228–263`)

The embedded PDF text stream drops displayed equations `(4.1)`, `(4.2)`, `(4.3)`, `(4.6)`, `(4.7)`, `(4.8)`,
all four displays of `Example 4.1`, both displays of `⊑_CFA`/`(4.6)`, the `6`-inequality chain above
`Figure 4.3`, and `⨆_{α[L]} M' = ⨆_M M'` (`p. 245`), while mangling `⊳` → `1>`/`[>`, `↝` → `~+`, `⊔̆` → `O`,
`∇` → `\7`/`!!!;`, `Δ` → `~`, `ς` → `c.;`/`~`/`<;`, `∞` → `()()`, `⊑` → `[;;;`, and fragmenting
`Figures 4.1–4.9` — all math above was recovered verbatim from page renders.

---

## Gotcha Ledger

- G-U4a-01: Unit 4a runs book pp. 211–246 top (`PDF pp. 228–263`, constant offset `+17` after absent blank verso p. 210); `§4.3.2` finishes (`Fact 4.31` conclusion & proof, `Proposition 4.29` proof, `ς_η`, isomorphism, `Example 4.32`) on `p. 246` immediately above `§4.4`. [PPA Chapter 4, p. 211] (book p. 211; PDF p. 228); [PPA Example 4.32, p. 246] (book p. 246; PDF p. 263)
- G-U4a-02: Concrete `p ⊢ v₁ ↝ v₂` `(4.1)` allows nondeterminism, whereas abstract `p ⊢ l₁ ⊳ l₂` `(4.2)` is assumed deterministic and total (`f_p(l₁) = l₂`); `Example 4.2` fixes an unspecified `(Ĉ, ρ̂)` to satisfy determinacy. [PPA §4.1, pp. 211–212] (book p. 211; PDF p. 228) (book p. 212; PDF p. 229); [PPA Example 4.2, p. 213] (book p. 213; PDF p. 230)
- G-U4a-03: `§4.1`'s mundane `R` / `β` framework covers only *first-order* value-set analyses (`§2.3`, `§2.6`, Chapter 3 `0-CFA`), NOT *second-order* relational analyses like Live Variables (`§2.1`) or 2-safety security hyperproperties `[external]`, whereas `§§4.2–4.5` apply to both. [PPA §4.1, p. 212] (book p. 212; PDF p. 229)
- G-U4a-04: Chapter 4 fixes `(4.4)` *smaller `⊑` = more precise* (`⊥` exact/empty, `v R ⊤` always), reversing upper-is-more-precise conventions in parts of Chapter 2 (reconciled via lattice duality). [PPA §4.1.1, pp. 214–215] (book p. 214; PDF p. 231) (book p. 215; PDF p. 232)
- G-U4a-05: Equivalence of correctness relations `(4.3)` and representation functions `(4.6)` (`Lemma 4.5`) holds iff `R` satisfies both upward safety `(4.4)` and the Moore-family axiom `(4.5)` (`{l | v R l}` closed under arbitrary meets `⨅ L'`, ensuring `v R ⊤` and binary meets); `Example 4.3` needs an implicit `σ̂ ≠ ⊥` guard in `(Var⋆ → Z^⊤)_⊥`. [PPA §4.1.1, pp. 214–215] (book p. 214; PDF p. 231) (book p. 215; PDF p. 232); [PPA Example 4.3, p. 215] (book p. 215; PDF p. 232); [PPA Lemma 4.5, p. 217] (book p. 217; PDF p. 234)
- G-U4a-06: In `Example 4.2`, encoding `0-CFA` via `(Ĉ, ρ̂) ⊨ (e⋆ c^{ℓ₁})^{ℓ₂}` relies on `Table 3.1`'s `[con]` imposing zero constraints on `Ĉ(ℓ₁)` (breaks under `Table 3.8` `[derived]`); in `Example 4.7`, prose writes `⋃{β_CFA(ρ(x)) | x ∈ Var⋆}` for a pair union over `dom(ρ)`. [PPA Example 4.2, p. 213] (book p. 213; PDF p. 230); [PPA Example 4.7, p. 218] (book p. 218; PDF p. 235)
- G-U4a-07: `§4.1.3` lifts soundness to distinct input/output domains (`V₁ ≠ V₂`, `L₁ ≠ L₂`) via `R₁ ↠ R₂` generated by `(β₁ ↠ β₂)(↝)` (`Lemma 4.8`); `Example 4.9` switches metavariable `plus` to generic `p` in its penultimate display. [PPA Lemma 4.8, p. 220] (book p. 220; PDF p. 237); [PPA Example 4.9, p. 220] (book p. 220; PDF p. 237)
- G-U4a-08: In `Interval` (`Example 4.10`, `Figure 4.2`), `[∞, ∞]` and `[-∞, -∞]` are excluded, and `inf(⊥) = ∞`, `sup(⊥) = -∞` invert endpoints so `int₁ ⊑ int₂` holds uniformly including `⊥` (violated if un-normalised empty intervals coexist, breaking `Lemma 4.27` injectivity `[derived]`). [PPA Figure 4.2, p. 221] (book p. 221; PDF p. 238); [PPA Example 4.10, p. 222] (book p. 222; PDF p. 239)
- G-U4a-09: Without `[external: Scott]` continuity of monotone `f`, every inequality in `f^n(⊥) ⊑ ⨆_n f^n(⊥) ⊑ lfp(f) ⊑ gfp(f) ⊑ ⨅_n f^n(⊤) ⊑ f^n(⊤)` (`Figure 4.3`) can be strict (`≠`). [PPA §4.2, pp. 223–224] (book p. 223; PDF p. 240) (book p. 224; PDF p. 241); [PPA Figure 4.3, p. 224] (book p. 224; PDF p. 241)
- G-U4a-10: Upper bound (`⊔̆`) and widening (`∇`) operators require neither monotonicity, commutativity, associativity, nor absorptiveness: `Example 4.12` shows asymmetry (`[1,2]` vs `[2,3]`) and non-stabilisation (`int = [0, ∞]`), and `∇_K` (`Example 4.15`) violates left-argument monotonicity (`[1, 1] ⊑ [0, 2]` while `[1, 1] ∇_∅ [1, 2] = [1, ∞] ⋢ [0, 2]`) `[derived]`. [PPA §4.2.1, p. 225] (book p. 225; PDF p. 242); [PPA Example 4.12, pp. 225–226] (book p. 225; PDF p. 242) (book p. 226; PDF p. 243)
- G-U4a-11: Reversing widening operand order from `old ∇ new` to `new ∇ old` destroys extrapolation (`[0, n] ∇_K [0, n-1] = [0, n]` diverges `[derived]`), and omitting the `f(f_∇^{n-1}) ⊑ f_∇^{n-1}` guard (`p. 226`) lets non-absorptive `∇` overshoot `Red(f)`. [PPA §4.2.1, pp. 226–227] (book p. 226; PDF p. 243) (book p. 227; PDF p. 244); [PPA Fact 4.14, p. 227] (book p. 227; PDF p. 244)
- G-U4a-12: `Proposition 4.13` standalone box omits `"f monotone"` (inherited from `§4.2` prose `pp. 223, 226` and used on `p. 228`); `Fact 4.14` holds even for mere upper bound operators `⊔̆`. [PPA Proposition 4.13, p. 227] (book p. 227; PDF p. 244); [PPA §4.2.1, p. 228] (book p. 228; PDF p. 245)
- G-U4a-13: In `Example 4.15` (`∇_K`), `int₁ = ⊥, int₂ = [z₃, z₄]` falls into `otherwise` (`inf(⊥) = ∞ > z₃`), blowing up `⊥ ∇_∅ [0, 0] = [-∞, ∞]` on iteration 1 unless `⊥ ∇_K x = x` is enforced; termination requires `K ⊆ Z` to be finite and fixed. [PPA Example 4.15, pp. 228–229] (book p. 228; PDF p. 245) (book p. 229; PDF p. 246)
- G-U4a-14: Although `§4.2.2` says narrowing `Δ` need not be absorptive, `l₂ ⊑ l₁ ⇒ l₂ ⊑ (l₁ Δ l₂) ⊑ l₁` at `l₁ = l₂ = l` forces `l Δ l = l` (`[derived]`). [PPA §4.2.2, p. 230] (book p. 230; PDF p. 247)
- G-U4a-15: Narrowing is **not** the lattice dual of widening: `(f_∇^n)_n` may leave `Ext(f)` to enter `Red(f)`, whereas `([f]_Δ^n)_n` requires `f(f_∇^m) ⊑ f_∇^m` (`n = 0`) and remains inside `Red(f)` above `lfp(f)` throughout (`Lemma 4.16`, `(4.7)`); `Lemma 4.16` basis prints uninstantiated `n` on `p. 231`, and `Proposition 4.17` leaves monotonicity of `f` tacit on `p. 232`. [PPA Lemma 4.16, pp. 230–231] (book p. 230; PDF p. 247) (book p. 231; PDF p. 248); [PPA Proposition 4.17, p. 232] (book p. 232; PDF p. 249)
- G-U4a-16: Threshold narrowing `Δ_N` (`Example 4.18`) checks `±N` only when an endpoint is `±∞`, adopting `int₂`'s finite endpoints unconditionally (possibly many finite steps on large finite ranges, no bound stated in the book `[derived]`), and its proof assumes chain monotonicity implicitly on `p. 233`. [PPA Example 4.18, pp. 232–233] (book p. 232; PDF p. 249) (book p. 233; PDF p. 250)
- G-U4a-17: In `(L, α, γ, M)`, `(4.8)`–`(4.9)` require monotonicity of both `α` and `γ`, whereas the adjunction law `(4.10)` (`α(l) ⊑ m ⇔ l ⊑ γ(m)`) implies monotonicity automatically (`Proposition 4.20`); in `Example 4.19`, `α_ZI(∅) = ⊥` cannot be subsumed into `[inf'(∅), sup'(∅)]`. [PPA Example 4.19, p. 235] (book p. 235; PDF p. 252); [PPA Proposition 4.20, p. 236] (book p. 236; PDF p. 253)
- G-U4a-18: Any `β : V → L` induces `(𝒫(V), α, γ, L)` (`α(V') = ⨆ β[V']`), and any extraction `η : V → D` induces `(𝒫(V), α_η, γ_η, 𝒫(D))` (`Example 4.21`); this is a Galois insertion **iff `η` is surjective** (`p. 244`). [PPA §4.3, pp. 237–238] (book p. 237; PDF p. 254) (book p. 238; PDF p. 255); [PPA Lemma 4.27, p. 244] (book p. 244; PDF p. 261)
- G-U4a-19: `α` (left/lower adjoint) uniquely determines `γ` and preserves all joins `⨆` (`α(⊥) = ⊥`, not `⊓` or `⊤` in general), while `γ` (right/upper adjoint) uniquely determines `α` and preserves all meets `⨅` (`γ(⊤) = ⊤`, not `⊔` or `⊥` in general) (`Lemmas 4.22–4.23`); `Fact 4.24` gives `α ∘ γ ∘ α = α` and `γ ∘ α ∘ γ = γ`. [PPA Lemma 4.22, p. 239] (book p. 239; PDF p. 256); [PPA Lemma 4.23, pp. 239–240] (book p. 239; PDF p. 256) (book p. 240; PDF p. 257); [PPA Fact 4.24, p. 240] (book p. 240; PDF p. 257)
- G-U4a-20: Monotonicity of `γ` alone does NOT guarantee an abstraction `α`: `γ_IS : 𝒫(Sign) → Interval` (`Example 4.25`) breaks binary meet preservation on `({-, 0}, {-, +})` (`[-∞, -1] ≠ [-∞, 0]`, listing `9` unordered pairs), proving no `α_IS` exists (`Lemmas 4.22–4.23`). [PPA Example 4.25, pp. 240–241] (book p. 240; PDF p. 257) (book p. 241; PDF p. 258)
- G-U4a-21: Transporting `R` on `V × L` to `v S m iff v R γ(m)` on `V × M` (`§4.3.1`) preserves Moore-family axiom `(4.5)` specifically because `γ` is completely multiplicative (`Lemma 4.22(ii)`). [PPA §4.3.1, pp. 241–242] (book p. 241; PDF p. 258) (book p. 242; PDF p. 259)
- G-U4a-22: Galois insertions (`α ∘ γ = λm.m`) are characterised equivalently by `α` surjective, `γ` injective, or `γ` an order-similarity (`Lemma 4.27`); `Example 4.28` (`signparity`) fails insertion due to uninhabited `(0, odd)`. [PPA Lemma 4.27, pp. 243–244] (book p. 243; PDF p. 260) (book p. 244; PDF p. 261); [PPA Example 4.28, p. 244] (book p. 244; PDF p. 261)
- G-U4a-23: Reduction `ς(m) = ⨅{m' | γ(m) = γ(m')} = α(γ(m))` (`Proposition 4.29`, `Facts 4.30–4.31`) collapses redundant `γ`-fibers onto `ς[M] = α[L]`, where `⨆_{α[L]} = ⨆_M` while `⨅_{α[L]} M' = ς(⨅_M M')` can lie strictly below `⨅_M M'` (`[derived]`). `Fact 4.31` prints stray `=ˊ∏` on `p. 245`, and `ς_η(D') = D' ∩ η[V]` (`Example 4.32`) equals `𝒫(η[V])` on `p. 246`. [PPA Proposition 4.29, p. 244] (book p. 244; PDF p. 261); [PPA Fact 4.30, p. 245] (book p. 245; PDF p. 262); [PPA Fact 4.31, pp. 245–246] (book p. 245; PDF p. 262) (book p. 246; PDF p. 263); [PPA Example 4.32, p. 246] (book p. 246; PDF p. 263)
- G-U4a-24: `ppa.pdf` OCR strips displays `(4.1)–(4.3), (4.6)–(4.8)`, `Example 4.1`, `⊑_CFA`, and `Figure 4.3`'s chain while corrupting `⊔̆` (`O`), `∇` (`\7`), `Δ` (`~`), and `ς` (`c.;`/`~`); formulas must be read from rendered pages. [PPA §4.1, pp. 211–216] (book p. 211; PDF p. 228) (book p. 216; PDF p. 233); [PPA §4.2.1, pp. 225–226] (book p. 225; PDF p. 242) (book p. 226; PDF p. 243)
