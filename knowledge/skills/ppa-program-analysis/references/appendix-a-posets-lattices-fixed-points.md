<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-008: Shared Unit 0 L1 reference, hosted with the router skill and linked from it. -->

# Appendix A Reference: Partially Ordered Sets, Complete Lattices, Chains, Fixed Points

Scope: Appendix A, sections A.1 to A.4 and the Concluding Remarks [PPA Appendix A, p. 393] (book p. 393; PDF p. 409).
Every item below carries a canonical citation such as `[PPA §A.1, p. 393] (book p. 393; PDF p. 409)`. Items
numbered in the book keep the book's numbering (Lemma A.2, Proposition A.10, ...). Unnumbered items carry
`[U0:<section>-<letter>]` ids. Terms tagged `[external]` are not the book's terminology; `[derived]` marks
consequences justified directly from printed definitions.

Proofs are not reproduced here. They live in the L3 shard corpus/shards/RAW_SHARD_00_appendices.md
(Appendix A anchors).

Closed inventory of numbered items in Appendix A: Example A.1, Lemma A.2, Example A.3, Lemma A.4,
Lemma A.5, Lemma A.6, Example A.7, Lemma A.8, Lemma A.9, Proposition A.10; Figures A.1 to A.3; numbered
displays (A.1) to (A.3). Appendix A has no Exercises section
[PPA Appendix A Concluding Remarks, p. 404] (book p. 404; PDF p. 420).

---

## 1. Basic definitions (A.1)

### [U0:A.1-a] Partial ordering, partially ordered set
[PPA §A.1, p. 393] (book p. 393; PDF p. 409)

A partial ordering is a relation `⊑ : L × L → {true, false}` that is

| Property | Condition |
| :--- | :--- |
| reflexive | `∀l : l ⊑ l` |
| transitive | `∀l₁, l₂, l₃ : l₁ ⊑ l₂ ∧ l₂ ⊑ l₃ ⇒ l₁ ⊑ l₃` |
| anti-symmetric | `∀l₁, l₂ : l₁ ⊑ l₂ ∧ l₂ ⊑ l₁ ⇒ l₁ = l₂` |

A partially ordered set `(L, ⊑)` is a set `L` with a partial ordering `⊑` (sometimes written `⊑_L`).
Notation: `l₂ ⊒ l₁` for `l₁ ⊑ l₂`; `l₁ ⊏ l₂` for `l₁ ⊑ l₂ ∧ l₁ ≠ l₂`.

### [U0:A.1-b] Bounds, least upper bound, greatest lower bound, join, meet
[PPA §A.1, p. 393] (book p. 393; PDF p. 409)

For `Y ⊆ L`:

- `l ∈ L` is an upper bound of `Y` iff `∀l′ ∈ Y : l′ ⊑ l`; a lower bound iff `∀l′ ∈ Y : l′ ⊒ l`.
- A least upper bound `l` of `Y` is an upper bound with `l ⊑ l₀` for every upper bound `l₀` of `Y`.
- A greatest lower bound `l` of `Y` is a lower bound with `l₀ ⊑ l` for every lower bound `l₀` of `Y`.
- Side condition: in a partially ordered set these **need not exist**; when they exist they are unique
  (by anti-symmetry) and are written `⨆Y` and `⨅Y`.
- `⨆` is the join operator, `⨅` the meet operator; `l₁ ⊔ l₂ = ⨆{l₁, l₂}`, `l₁ ⊓ l₂ = ⨅{l₁, l₂}`.

### [U0:A.1-c] Complete lattice
[PPA §A.1, p. 393] (book p. 393; PDF p. 409); continued [PPA §A.1, p. 394] (book p. 394; PDF p. 410)

A complete lattice `L = (L, ⊑) = (L, ⊑, ⨆, ⨅, ⊥, ⊤)` is a partially ordered set in which **all subsets**
(including `∅` and `L` itself) have least upper bounds and greatest lower bounds. Then

- `⊥ = ⨆∅ = ⨅L` is the least element;
- `⊤ = ⨅∅ = ⨆L` is the greatest element.

### Example A.1 and Figure A.1 (powerset lattices)
[PPA §A.1, p. 394] (book p. 394; PDF p. 410)

| Lattice | `⊑` | `⨆Y` | `⨅Y` | `⊥` | `⊤` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `(𝒫(S), ⊆)` | `⊆` | `⋃Y` | `⋂Y` | `∅` | `S` |
| `(𝒫(S), ⊇)` | `⊇` | `⋂Y` | `⋃Y` | `S` | `∅` |

Both are complete lattices. Figure A.1 draws both for `S = {1, 2, 3}` as Hasse diagrams (a line going
upwards from `l₁` to `l₂` means `l₁ ⊑ l₂`). Direction trap: in `(𝒫(S), ⊇)` the join is intersection.

### Lemma A.2 (one-sided completeness suffices)
[PPA §A.1, p. 394] (book p. 394; PDF p. 410)

For a partially ordered set `L = (L, ⊑)` the following are **equivalent**:
(i) `L` is a complete lattice; (ii) every subset of `L` has a least upper bound;
(iii) every subset of `L` has a greatest lower bound.

Display (A.1), the witness for (ii) ⇒ (i): `⨅Y = ⨆{ l ∈ L | ∀l′ ∈ Y : l ⊑ l′ }`
[PPA §A.1, p. 394] (book p. 394; PDF p. 410). Dually, for (iii) ⇒ (i):
`⨆Y = ⨅{ l ∈ L | ∀l′ ∈ Y : l′ ⊑ l }` [PPA §A.1, p. 395] (book p. 395; PDF p. 411).

### [U0:A.1-d] Moore family
[PPA §A.1, p. 395] (book p. 395; PDF p. 411)

A Moore family is a subset `Y` of a **complete lattice** `L = (L, ⊑)` that is closed under greatest lower
bounds: `∀Y′ ⊆ Y : ⨅Y′ ∈ Y`. Consequences stated by the book: it contains a least element `⨅Y` and a
greatest element `⨅∅`, which is `⊤` of `L`; hence a Moore family is **never empty**.

Example A.3 [PPA §A.1, p. 395] (book p. 395; PDF p. 411), in `(𝒫({1,2,3}), ⊆)` (failing glb witnesses `[derived]`, G-U0-05):

| Subset | Moore family? | Failing condition `[derived]` |
| :--- | :--- | :--- |
| `{{2}, {1,2}, {2,3}, {1,2,3}}` | yes | none |
| `{∅, {1,2,3}}` | yes | none |
| `{{1}, {2}}` | no | `⨅∅ = {1,2,3}` missing; `{1} ∩ {2} = ∅` missing |
| `{∅, {1}, {2}, {1,2}}` | no | `⨅∅ = {1,2,3}` missing |

### [U0:A.1-e] Properties of functions
[PPA §A.1, p. 395] (book p. 395; PDF p. 411); continued [PPA §A.1, p. 396] (book p. 396; PDF p. 412)

For `f : L₁ → L₂` between partially ordered sets `L₁ = (L₁, ⊑₁)` and `L₂ = (L₂, ⊑₂)`:

| Name (book's alternatives) | Condition |
| :--- | :--- |
| surjective (onto, epic) | `∀l₂ ∈ L₂ : ∃l₁ ∈ L₁ : f(l₁) = l₂` |
| injective (1-1, monic) | `∀l, l′ ∈ L₁ : f(l) = f(l′) ⇒ l = l′` |
| monotone (isotone, order-preserving) | `∀l, l′ ∈ L₁ : l ⊑₁ l′ ⇒ f(l) ⊑₂ f(l′)` |
| additive (join morphism, sometimes distributive — BKL-022) | `∀l₁, l₂ ∈ L₁ : f(l₁ ⊔ l₂) = f(l₁) ⊔ f(l₂)` |
| multiplicative (meet morphism) | `∀l₁, l₂ ∈ L₁ : f(l₁ ⊓ l₂) = f(l₁) ⊓ f(l₂)` |
| completely additive (complete join morphism) | `∀Y ⊆ L₁ : f(⨆₁Y) = ⨆₂{ f(l′) \| l′ ∈ Y }` whenever `⨆₁Y` exists |
| completely multiplicative (complete meet morphism) | `∀Y ⊆ L₁ : f(⨅₁Y) = ⨅₂{ f(l′) \| l′ ∈ Y }` whenever `⨅₁Y` exists |
| affine | as completely additive but only for **non-empty** `Y ⊆ L₁` (`Y ≠ ∅`) |
| strict | `f(⊥₁) = ⊥₂` |

Side conditions: when `L₂` is not a complete lattice the conditions additionally require the relevant
bounds to exist in `L₂`. Stated fact: `f` is completely additive **iff** it is both affine and strict.

### Lemma A.4 (complete multiplicativity on a finite domain)
[PPA §A.1, p. 396] (book p. 396; PDF p. 412)

Let `L = (L, ⊑, ⊔, ⊓, ⊥, ⊤)` and `M = (M, ⊑, ⊔, ⊓, ⊥, ⊤)` be complete lattices **with `M` finite**. Then the
three conditions

1. `γ : M → L` is monotone,
2. `γ(⊤) = ⊤`,
3. `γ(m₁ ⊓ m₂) = γ(m₁) ⊓ γ(m₂)` whenever `m₁ ⋢ m₂ ∧ m₂ ⋢ m₁` (only **incomparable** pairs),

are jointly equivalent to `γ : M → L` being completely multiplicative. The proof establishes display (A.2),
`γ(⨅M′) = ⨅{ γ(m) | m ∈ M′ }` for `M′ ⊆ M`, by induction on the cardinality of `M′`.

### Lemma A.5 (affine maps between powersets)
[PPA §A.1, p. 396] (book p. 396; PDF p. 412)

`f : (𝒫(D), ⊆) → (𝒫(E), ⊆)` is **affine** iff there exist `φ : D → 𝒫(E)` and `φ_∅ ∈ 𝒫(E)` such that

`f(Y) = ⋃{ φ(d) | d ∈ Y } ∪ φ_∅`.

`f` is **completely additive** iff, additionally, `φ_∅ = ∅`. Witnesses used in the proof: `φ(d) = f({d})`,
`φ_∅ = f(∅)` [PPA §A.1, p. 397] (book p. 397; PDF p. 413).

### [U0:A.1-f] Isomorphism
[PPA §A.1, p. 397] (book p. 397; PDF p. 413)

An isomorphism from `(L₁, ⊑₁)` to `(L₂, ⊑₂)` is a **monotone** `θ : L₁ → L₂` for which there exists a
(necessarily unique) **monotone** `θ⁻¹ : L₂ → L₁` with `θ ∘ θ⁻¹ = id₂` and `θ⁻¹ ∘ θ = id₁`.

---

## 2. Construction of complete lattices (A.2)

[PPA §A.2, p. 397] (book p. 397; PDF p. 413); continued [PPA §A.2, p. 398] (book p. 398; PDF p. 414)

| Construction (id) | Carrier | Ordering | Complete lattice when | `⨆Y` and `⊥` (dually `⨅Y`, `⊤`) |
| :--- | :--- | :--- | :--- | :--- |
| Cartesian product `L₁ × L₂` [U0:A.2-a] | `{ (l₁, l₂) \| l₁ ∈ L₁ ∧ l₂ ∈ L₂ }` | componentwise: `(l₁₁, l₂₁) ⊑ (l₁₂, l₂₂)` iff `l₁₁ ⊑₁ l₁₂ ∧ l₂₁ ⊑₂ l₂₂` | each `Lᵢ` is a complete lattice | `⨆Y = (⨆₁{ l₁ \| ∃l₂ : (l₁, l₂) ∈ Y }, ⨆₂{ l₂ \| ∃l₁ : (l₁, l₂) ∈ Y })`; `⊥ = (⊥₁, ⊥₂)` |
| Smash product [U0:A.2-b] | pairs with `l₁ = ⊥₁ ⇔ l₂ = ⊥₂` | as cartesian product | (variant of cartesian product) | not displayed separately |
| Total function space `S → L₁` [U0:A.2-c] | `{ f : S → L₁ \| f total }`, `S` a set | pointwise: `f ⊑ f′` iff `∀s ∈ S : f(s) ⊑₁ f′(s)` | `L₁` is a complete lattice | `⨆Y = λs. ⨆₁{ f(s) \| f ∈ Y }`; `⊥ = λs. ⊥₁` |
| Monotone function space `L₁ → L₂` [U0:A.2-d] | `{ f : L₁ → L₂ \| f monotone }` | pointwise: `f ⊑ f′` iff `∀l₁ ∈ L₁ : f(l₁) ⊑₂ f′(l₁)` | `L₁` and `L₂` are complete lattices | `⨆Y = λl₁. ⨆₂{ f(l₁) \| f ∈ Y }`; `⊥ = λl₁. ⊥₂` |

Each construction yields a partially ordered set from partially ordered sets; the complete-lattice column is
the extra condition (G-U0-08, G-U0-09). Notation clash (BKL-024): both total and monotone function spaces are
written with `→`; whether the domain is a plain set `S` or a partially ordered set `L₁` disambiguates `[derived]`.

---

## 3. Chains and chain conditions (A.3)

The ordering `⊑` expresses when one property is better (more precise) than another
[PPA §A.3, p. 398] (book p. 398; PDF p. 414).

### [U0:A.3-a] Chain, finite chain
[PPA §A.3, p. 399] (book p. 399; PDF p. 415)

`Y ⊆ L` is a chain iff `∀l₁, l₂ ∈ Y : (l₁ ⊑ l₂) ∨ (l₂ ⊑ l₁)`: a **possibly empty** totally ordered subset.
A finite chain is a chain that is a finite subset.

### [U0:A.3-b] Ascending and descending chains; eventual stabilisation
[PPA §A.3, p. 399] (book p. 399; PDF p. 415)

- A sequence `(lₙ)ₙ = (lₙ)_{n∈ℕ}` is an ascending chain iff `n ≤ m ⇒ lₙ ⊑ lₘ`; a descending chain iff
  `n ≤ m ⇒ lₙ ⊒ lₘ`. Both are chains.
- `(lₙ)ₙ` eventually stabilises iff `∃n₀ ∈ ℕ : ∀n ∈ ℕ : n ≥ n₀ ⇒ lₙ = l_{n₀}`.
- Notation: `⨆ₙ lₙ` for `⨆{ lₙ | n ∈ ℕ }`; `⨅ₙ lₙ` for `⨅{ lₙ | n ∈ ℕ }`.

### [U0:A.3-c] Finite height, Ascending Chain Condition, Descending Chain Condition
[PPA §A.3, p. 399] (book p. 399; PDF p. 415)

| Notion | Definition |
| :--- | :--- |
| finite height | all chains are finite |
| finite height at most `h` | all chains contain at most `h + 1` elements |
| finite height `h` | at most `h`, and additionally some chain has `h + 1` elements |
| Ascending Chain Condition (ACC) | all ascending chains eventually stabilise |
| Descending Chain Condition (DCC) | all descending chains eventually stabilise |

### Lemma A.6 (finite height versus chain conditions)
[PPA §A.3, p. 399] (book p. 399; PDF p. 415)

A partially ordered set `L = (L, ⊑)` has finite height **if and only if** it satisfies **both** the
Ascending and the Descending Chain Conditions (G-U0-10, G-U0-11). Display (A.3), proved **under the
hypothesis that `L` satisfies DCC** (dually, under ACC every non-empty subset of a chain has a greatest
element): each non-empty subset `Y′` of a chain `Y` contains a least element
[PPA §A.3, p. 399] (book p. 399; PDF p. 415).

### Example A.7 and Figure A.2 (one chain condition is not enough)
[PPA §A.3, p. 400] (book p. 400; PDF p. 416)

| Poset (Figure A.2) | Elements | ACC | DCC | Finite height |
| :--- | :--- | :--- | :--- | :--- |
| (a) | `0 ⊒ −1 ⊒ −2 ⊒ ⋯ ⊒ −∞` (top `0`) | yes | no | no |
| (b) | `0 ⊑ 1 ⊑ 2 ⊑ ⋯ ⊑ ∞` (top `∞`) | no | yes | no |

### [U0:A.3-d] Preservation of chain conditions by constructions
[PPA §A.3, p. 400] (book p. 400; PDF p. 416)

| Construction | Finite height / ACC / DCC preserved? |
| :--- | :--- |
| cartesian product `L₁ × L₂` | yes, each of the three |
| total function space `S → L` | **only if `S` is finite** (BKL-013) |
| monotone function space `L₁ → L₂` | **not in general** (BKL-013) |

### Lemma A.8 (ACC complete lattice from a least element and binary joins)
[PPA §A.3, p. 401] (book p. 401; PDF p. 417)

For a partially ordered set `L = (L, ⊑)` the conditions

(i) `L` is a complete lattice satisfying the Ascending Chain Condition, and
(ii) `L` has a least element `⊥`, binary least upper bounds, and satisfies the Ascending Chain Condition

are **equivalent**. ACC appears on both sides; without it, (ii) does not give a complete lattice.

### Lemma A.9 (additive versus affine under ACC)
[PPA §A.3, p. 401] (book p. 401; PDF p. 417)

For a complete lattice `L = (L, ⊑)` **satisfying the Ascending Chain Condition** and a **total** function
`f : L → L`, the conditions

(i) `f` is additive, i.e. `∀l₁, l₂ : f(l₁ ⊔ l₂) = f(l₁) ⊔ f(l₂)`, and
(ii) `f` is affine, i.e. `∀Y ⊆ L, Y ≠ ∅ : f(⨆Y) = ⨆{ f(l) | l ∈ Y }`

are equivalent, and in both cases `f` is a monotone function (BKL-022, G-U0-12).

### ACC / DCC consequences (collected from A.3 and A.4)

| Hypothesis | Consequence | Citation |
| :--- | :--- | :--- |
| finite height | ACC and DCC (Lemma A.6, ⇒) | [PPA §A.3, p. 399] (book p. 399; PDF p. 415) |
| ACC and DCC | finite height (Lemma A.6, ⇐) | [PPA §A.3, p. 399] (book p. 399; PDF p. 415) |
| ACC alone | does **not** give finite height (Example A.7, Figure A.2(a)) | [PPA §A.3, p. 400] (book p. 400; PDF p. 416) |
| `⊥` + binary `⊔` + ACC | complete lattice (Lemma A.8) | [PPA §A.3, p. 401] (book p. 401; PDF p. 417) |
| complete lattice with ACC, `f` total | additive ⇔ affine, and `f` monotone (Lemma A.9) | [PPA §A.3, p. 401] (book p. 401; PDF p. 417) |
| ACC, `f` monotone | `f` is also continuous; `∃n : fⁿ(⊥) = fⁿ⁺¹(⊥)` and `lfp(f) = fⁿ(⊥)` | [PPA §A.4, p. 403] (book p. 403; PDF p. 419) |
| DCC, `f` monotone | `∃n : fⁿ(⊤) = fⁿ⁺¹(⊤)` and `gfp(f) = fⁿ(⊤)` | [PPA §A.4, p. 403] (book p. 403; PDF p. 419) |

---

## 4. Fixed points (A.4)

### [U0:A.4-a] Fix, Red, Ext, reductive, extensive, lfp, gfp
[PPA §A.4, p. 402] (book p. 402; PDF p. 418)

Setting: `f : L → L` **monotone** on a **complete lattice** `L = (L, ⊑, ⨆, ⨅, ⊥, ⊤)`.

| Symbol | Definition | Reading |
| :--- | :--- | :--- |
| `Fix(f)` | `{ l \| f(l) = l }` | the fixed points |
| `Red(f)` | `{ l \| f(l) ⊑ l }` | `f` is reductive at `l`; `f` is reductive iff `Red(f) = L` |
| `Ext(f)` | `{ l \| f(l) ⊒ l }` | `f` is extensive at `l`; `f` is extensive iff `Ext(f) = L` |
| `lfp(f)` | `⨅Fix(f)` | exists because `L` is complete |
| `gfp(f)` | `⨆Fix(f)` | exists because `L` is complete |

Terminology note (G-U0-13): the external terms pre-fixed point and post-fixed point `[external]` are
used with opposite conventions in the literature; this reference uses only the book's `Red(f)` and `Ext(f)`.
Proposition A.10 requires monotone `f` (negated/declassification rules `[external]` break monotonicity; BKL-014).
The Index of Notation lists each of Ext, Fix, gfp, lfp and Red at book pages 223 and 402: Ext
[PPA Index of Notation, p. 430] (book p. 430; PDF p. 444); Fix, gfp, lfp
[PPA Index of Notation, p. 431] (book p. 431; PDF p. 445); Red
[PPA Index of Notation, p. 432] (book p. 432; PDF p. 446).

### Proposition A.10 (Tarski's Fixed Point Theorem)
[PPA §A.4, p. 402] (book p. 402; PDF p. 418)

Let `L = (L, ⊑, ⨆, ⨅, ⊥, ⊤)` be a complete lattice. If `f : L → L` is a monotone function then

`lfp(f) = ⨅Red(f) ∈ Fix(f)` and `gfp(f) = ⨆Ext(f) ∈ Fix(f)`.

So `lfp(f)` is the least and `gfp(f)` the greatest fixed point of `f`. The book labels this item
**Proposition** A.10 (not Theorem, not Fact). The name Knaster-Tarski theorem `[external]` is not used.

### Figure A.3 (fixed points of f)
[PPA §A.4, p. 403] (book p. 403; PDF p. 419)

Points of `L` from bottom to top: `⊥`, `fⁿ(⊥)`, `⨆ₙ fⁿ(⊥)`, `lfp(f)`, `gfp(f)`, `⨅ₙ fⁿ(⊤)`, `fⁿ(⊤)`, `⊤`.
`Red(f)` is the region from `lfp(f)` up to `⊤`; `Ext(f)` the region from `⊥` up to `gfp(f)`; their
intersection is `Fix(f)`, from `lfp(f)` to `gfp(f)`.

### [U0:A.4-b] Iterating from ⊥ and ⊤
[PPA §A.4, p. 403] (book p. 403; PDF p. 419)

- **No continuity requirement** is imposed on `f` in Proposition A.10 (continuity: `f(⨆ₙ lₙ) = ⨆ₙ f(lₙ)` for all
  ascending chains `(lₙ)ₙ`), so without continuity the countable supremum `⨆ₙ fⁿ(⊥)` need not reach `lfp(f)` (G-U0-14, G-U0-15).
- In general:
  `⊥ ⊑ fⁿ(⊥) ⊑ ⨆ₙ fⁿ(⊥) ⊑ lfp(f) ⊑ gfp(f) ⊑ ⨅ₙ fⁿ(⊤) ⊑ fⁿ(⊤) ⊑ ⊤`,
  and **all** of these inequalities can be strict (`⊏`) (G-U0-16).
- If `L` satisfies ACC: there exists `n` with `fⁿ(⊥) = fⁿ⁺¹(⊥)` (finite stabilisation), and hence `lfp(f) = fⁿ(⊥)`. Any
  monotone `f` over a partially ordered set satisfying ACC is also continuous (`⨆ₙ fⁿ(⊥) = lfp(f)` holds whenever `f` is
  continuous, even without ACC finite stabilisation).
- If `L` satisfies DCC: there exists `n` with `fⁿ(⊤) = fⁿ⁺¹(⊤)`, and hence `gfp(f) = fⁿ(⊤)`.
- The book calls none of this Kleene iteration `[external]`.

Bound statement: Appendix A gives the ACC/DCC results **existentially** (`∃n`). It states no numeric
iteration bound in terms of a height `h`; any such bound is `[derived]`, not a cited result.

### [U0:A.4-c] Transfinite iteration (remark for readers familiar with ordinals)
[PPA §A.4, p. 404] (book p. 404; PDF p. 420)

For an ordinal `κ` define `f^{↑κ} = f(⨆_{κ′<κ} f^{↑κ′})`; for a natural number `n`, `f^{↑n} = fⁿ⁺¹(⊥)`.
Then `lfp(f) = f^{↑κ}` whenever `κ` is a cardinal number **strictly greater than the cardinality of `L`**
(for example the cardinality of `𝒫(L)`). A similar construction gives `gfp(f)` as the limit of a
descending transfinite chain. Indexing trap (BKL-021, G-U0-17): `f^{↑n}` is `fⁿ⁺¹(⊥)`, one step ahead of `fⁿ(⊥)`.

### Least versus greatest fixed point

| Aspect | `lfp(f)` | `gfp(f)` |
| :--- | :--- | :--- |
| Definition [U0:A.4-a] | `⨅Fix(f)` | `⨆Fix(f)` |
| Characterisation (Proposition A.10) | `⨅Red(f)` | `⨆Ext(f)` |
| Hypotheses | `L` complete lattice, `f` monotone | same |
| Upper/lower bound obtained from a witness | `f(l) ⊑ l ⇒ lfp(f) ⊑ l` (since `l ∈ Red(f)`) | `l ⊑ f(l) ⇒ l ⊑ gfp(f)` (since `l ∈ Ext(f)`) |
| Finite iteration start | `⊥`: `fⁿ(⊥) ⊑ ⨆ₙ fⁿ(⊥) ⊑ lfp(f)` | `⊤`: `gfp(f) ⊑ ⨅ₙ fⁿ(⊤) ⊑ fⁿ(⊤)` |
| Iteration is exact when | ACC (then `lfp(f) = fⁿ(⊥)` for some `n`) | DCC (then `gfp(f) = fⁿ(⊤)` for some `n`) |
| Transfinite limit [U0:A.4-c] | ascending, `f^{↑κ}` | descending (similar construction) |
| Proof principle (Appendix B) | induction | coinduction |

The witness row restates membership in `Red(f)` / `Ext(f)` combined with Proposition A.10; the book uses
the `gfp` direction as the coinduction proof rule [PPA §B.3, p. 412] (book p. 412; PDF p. 428).

---

## 5. Side conditions that are easy to drop (SMOOTHING_TRAP checklist)

| Statement as often smoothed | Condition the book states | Citation |
| :--- | :--- | :--- |
| "lub/glb of `Y`" in a poset | they need not exist; unique when they exist (G-U0-01, G-U0-02) | [PPA §A.1, p. 393] (book p. 393; PDF p. 409) |
| "complete lattice = has joins" | all subsets, including `∅` (gives `⊥`) and `L` (gives `⊤`); in `(𝒫(S), ⊇)` join is `⋂` (G-U0-03, G-U0-04) | [PPA §A.1, p. 394] (book p. 394; PDF p. 410) |
| "Moore family = closed under binary meets" | closed under `⨅` of **every** subset, so `⊤ = ⨅∅` belongs (G-U0-05) | [PPA §A.1, p. 395] (book p. 395; PDF p. 411) |
| "affine = completely additive" | affine quantifies over non-empty `Y` only; completely additive ⇔ affine ∧ strict (G-U0-06) | [PPA §A.1, p. 396] (book p. 396; PDF p. 412) |
| Lemma A.4 without "finite" | `M` finite; condition (iii) only for incomparable `m₁, m₂` (G-U0-07) | [PPA §A.1, p. 396] (book p. 396; PDF p. 412) |
| "additive ⇔ affine" | sufficient condition: complete lattice satisfying ACC and total `f : L → L` (Lemma A.9; BKL-022, G-U0-12) | [PPA §A.3, p. 401] (book p. 401; PDF p. 417) |
| "ACC ⇒ finite height" | false; finite height needs ACC **and** DCC (Lemma A.6, Example A.7; G-U0-10, G-U0-11) | [PPA §A.3, p. 400] (book p. 400; PDF p. 416) |
| "function spaces preserve ACC" | `S → L` only if `S` finite; `L₁ → L₂` not in general (BKL-013, G-U0-08, G-U0-09) | [PPA §A.3, p. 400] (book p. 400; PDF p. 416) |
| "Tarski: iterate from ⊥ to get lfp" | Proposition A.10 defines `lfp(f) = ⨅Red(f)`; ACC gives finite stabilisation `fⁿ(⊥) = lfp(f)`, whereas continuity gives limit equality `⨆ₙ fⁿ(⊥) = lfp(f)` (G-U0-14, G-U0-15) | [PPA §A.4, p. 403] (book p. 403; PDF p. 419) |
| "`⨆ₙ fⁿ(⊥)` is a fixed point" | without continuity (or ACC, which implies continuity), every inequality in the chain can be strict (G-U0-16) | [PPA §A.4, p. 403] (book p. 403; PDF p. 419) |
| "lfp exists for any `f`" | requires `f` monotone and `L` complete (G-U0-13) | [PPA §A.4, p. 402] (book p. 402; PDF p. 418) |
| "`f^{↑n} = fⁿ(⊥)`" | `f^{↑n} = fⁿ⁺¹(⊥)`; `κ` must be a cardinal strictly greater than `\|L\|` (BKL-021, G-U0-17) | [PPA §A.4, p. 404] (book p. 404; PDF p. 420) |

---

## 6. Item index (Appendix A)

| Id | Item | Citation |
| :--- | :--- | :--- |
| [U0:A.1-a] | partial ordering, partially ordered set | [PPA §A.1, p. 393] (book p. 393; PDF p. 409) |
| [U0:A.1-b] | bounds, `⨆`, `⨅`, `⊔`, `⊓` | [PPA §A.1, p. 393] (book p. 393; PDF p. 409) |
| [U0:A.1-c] | complete lattice, `⊥`, `⊤` | [PPA §A.1, p. 393] (book p. 393; PDF p. 409) |
| Example A.1, Figure A.1 | powerset lattices | [PPA §A.1, p. 394] (book p. 394; PDF p. 410) |
| Lemma A.2, (A.1) | one-sided completeness | [PPA §A.1, p. 394] (book p. 394; PDF p. 410) |
| [U0:A.1-d], Example A.3 | Moore family | [PPA §A.1, p. 395] (book p. 395; PDF p. 411) |
| [U0:A.1-e] | properties of functions | [PPA §A.1, p. 395] (book p. 395; PDF p. 411) |
| Lemma A.4, (A.2) | complete multiplicativity, finite `M` | [PPA §A.1, p. 396] (book p. 396; PDF p. 412) |
| Lemma A.5 | affine powerset maps | [PPA §A.1, p. 396] (book p. 396; PDF p. 412) |
| [U0:A.1-f] | isomorphism | [PPA §A.1, p. 397] (book p. 397; PDF p. 413) |
| [U0:A.2-a] | cartesian product `L₁ × L₂` | [PPA §A.2, p. 397] (book p. 397; PDF p. 413) |
| [U0:A.2-b] to [U0:A.2-d] | smash product, total & monotone function spaces | [PPA §A.2, p. 398] (book p. 398; PDF p. 414) |
| [U0:A.3-a] to [U0:A.3-c] | chains, finite height, ACC, DCC | [PPA §A.3, p. 399] (book p. 399; PDF p. 415) |
| Lemma A.6, (A.3) | finite height ⇔ ACC ∧ DCC | [PPA §A.3, p. 399] (book p. 399; PDF p. 415) |
| Example A.7, Figure A.2 | one chain condition only | [PPA §A.3, p. 400] (book p. 400; PDF p. 416) |
| [U0:A.3-d] | preservation by constructions | [PPA §A.3, p. 400] (book p. 400; PDF p. 416) |
| Lemma A.8 | `⊥` + binary joins + ACC | [PPA §A.3, p. 401] (book p. 401; PDF p. 417) |
| Lemma A.9 | additive ⇔ affine under ACC | [PPA §A.3, p. 401] (book p. 401; PDF p. 417) |
| [U0:A.4-a] | Fix, Red, Ext, lfp, gfp | [PPA §A.4, p. 402] (book p. 402; PDF p. 418) |
| Proposition A.10 | Tarski's Fixed Point Theorem | [PPA §A.4, p. 402] (book p. 402; PDF p. 418) |
| Figure A.3, [U0:A.4-b] | iteration chain, ACC/DCC exactness | [PPA §A.4, p. 403] (book p. 403; PDF p. 419) |
| [U0:A.4-c] | transfinite iteration | [PPA §A.4, p. 404] (book p. 404; PDF p. 420) |
| Concluding Remarks | further reading: reference [43] | [PPA Appendix A Concluding Remarks, p. 404] (book p. 404; PDF p. 420) |
