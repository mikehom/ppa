<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 0. -->

# RAW_SHARD_00 — Appendices A, B, C (Unit 0)

Source: *Principles of Program Analysis* (Nielson, Nielson, Hankin), corrected 2nd printing, 2005.
Scope: Appendix A (§A.1–§A.4), Appendix B (§B.1–§B.3), Appendix C (§C.1–§C.3) and the three
Concluding Remarks sections, book pages 393–427. The Index of Notation on book pages 429–432
(PDF pages 443–446) is out of scope for this shard.

Coordinates: book pp. 393–415 are PDF pp. 409–431 (offset +16); book pp. 417–427 are PDF pp. 432–442
(offset +15). Book pp. 416 and 428 are blank pages absent from the PDF.

Conventions:

- Each item is cited twice: an inline `N8` citation and its book/PDF companion coordinate pair, e.g.
  [PPA §A.1, p. 393] (book p. 393; PDF p. 409).
- Items with a book number keep that number exactly. Unnumbered items carry non-book ids
  `[U0:<section>-<letter>]`; these ids are not book numbering.
- Math is transcribed from page images, not from the text layer. Proofs are summarised.
- Terms the book does not use carry the tag `[external]`. Statements derived by the shard author
  rather than printed in the book are tagged `[derived]`.
- Typeface: in Appendix B, sans-serif `Q` is the defined predicate, calligraphic `𝒬` the functional,
  italic `Q′` a candidate predicate. In Appendix C, `rPostorder` and `DFS` are sans-serif program
  names and `T` in Table C.1 is sans-serif.
- No appendix has an Exercises or Mini Projects section (see the Concluding Remarks sections).

## A.1 Basic Definitions

Context: Appendix A summarises properties of partially ordered sets and complete lattices,
constructions of complete lattices, the Ascending and Descending Chain Conditions, and the classical
results on least and greatest fixed points [PPA Appendix A, p. 393] (book p. 393; PDF p. 409).

### [U0:A.1-a] Partial ordering; partially ordered set (unnumbered definition)
- Statement: a *partial ordering* is a relation ⊑ : L × L → {true, false} that is
  reflexive (∀l : l ⊑ l), transitive (∀l₁, l₂, l₃ : l₁ ⊑ l₂ ∧ l₂ ⊑ l₃ ⇒ l₁ ⊑ l₃) and anti-symmetric
  (∀l₁, l₂ : l₁ ⊑ l₂ ∧ l₂ ⊑ l₁ ⇒ l₁ = l₂). A *partially ordered set* (L, ⊑) is a set L with a partial
  ordering ⊑ (sometimes written ⊑_L).
- Notation: l₂ ⊒ l₁ for l₁ ⊑ l₂; l₁ ⊏ l₂ for l₁ ⊑ l₂ ∧ l₁ ≠ l₂.
- Citation: [PPA §A.1, p. 393] (book p. 393; PDF p. 409)

### [U0:A.1-b] Upper and lower bounds; least upper bound; greatest lower bound; join; meet (unnumbered definition)
- Statement: for Y ⊆ L, l ∈ L is an *upper bound* of Y if ∀l′ ∈ Y : l′ ⊑ l and a *lower bound* if
  ∀l′ ∈ Y : l′ ⊒ l. A *least upper bound* l of Y is an upper bound with l ⊑ l₀ for every upper bound
  l₀ of Y; a *greatest lower bound* l of Y is a lower bound with l₀ ⊑ l for every lower bound l₀.
  Written ⨆Y and ⨅Y; ⨆ is the *join* operator, ⨅ the *meet* operator;
  l₁ ⊔ l₂ = ⨆{l₁, l₂}, l₁ ⊓ l₂ = ⨅{l₁, l₂}.
- Side conditions: subsets of a partially ordered set need not have least upper bounds or greatest
  lower bounds; when they exist they are unique (anti-symmetry).
- Citation: [PPA §A.1, p. 393] (book p. 393; PDF p. 409)

### [U0:A.1-c] Complete lattice; least and greatest element (unnumbered definition)
- Statement: a *complete lattice* L = (L, ⊑) = (L, ⊑, ⨆, ⨅, ⊥, ⊤) is a partially ordered set in which
  all subsets have least upper bounds as well as greatest lower bounds. ⊥ = ⨆∅ = ⨅L is the *least
  element*; ⊤ = ⨅∅ = ⨆L is the *greatest element*.
- Citation: [PPA §A.1, p. 393] (book p. 393; PDF p. 409); the definition of ⊥ and ⊤ is on [PPA §A.1, p. 394] (book p. 394; PDF p. 410)

### Figure A.1 — Two complete lattices
- Content: Hasse diagrams for S = {1, 2, 3}. (a) (𝒫(S), ⊆): ∅ at the bottom; {1}, {2}, {3}; then
  {1,2}, {1,3}, {2,3}; {1,2,3} at the top. (b) (𝒫(S), ⊇): the same cube inverted, ∅ at the top and
  {1,2,3} at the bottom.
- Citation: [PPA §A.1, p. 394] (book p. 394; PDF p. 410)

### Example A.1 — Powerset lattices
- Statement: if L = (𝒫(S), ⊆) then ⊑ is ⊆, ⨆Y = ⋃Y, ⨅Y = ⋂Y, ⊥ = ∅, ⊤ = S. If L = (𝒫(S), ⊇) then ⊑ is
  ⊇, ⨆Y = ⋂Y, ⨅Y = ⋃Y, ⊥ = S, ⊤ = ∅. Both are complete lattices (drawn in Figure A.1 for S = {1,2,3}).
- Side conditions: the drawings are Hasse diagrams; a line "going upwards" from l₁ to l₂ means
  l₁ ⊑ l₂; lines that follow from reflexivity or transitivity are not drawn.
- Citation: [PPA §A.1, p. 394] (book p. 394; PDF p. 410)

### Lemma A.2 — Complete lattice from one-sided bounds
- Statement: for a partially ordered set L = (L, ⊑) the claims (i) L is a complete lattice, (ii) every
  subset of L has a least upper bound, (iii) every subset of L has a greatest lower bound, are
  equivalent.
- Proof (summary): (i) implies (ii) and (iii). (ii) ⇒ (i) by Display (A.1). (iii) ⇒ (i) by
  ⨆Y = ⨅{l ∈ L | ∀l′ ∈ Y : l′ ⊑ l} and analogous arguments.
- Citation: [PPA §A.1, p. 394] (book p. 394; PDF p. 410); the (iii) ⇒ (i) step is on [PPA §A.1, p. 395] (book p. 395; PDF p. 411)

### Display (A.1) — Greatest lower bound from least upper bounds
- Statement: ⨅Y = ⨆{l ∈ L | ∀l′ ∈ Y : l ⊑ l′}.
- Side conditions: used in the proof of Lemma A.2, (ii) ⇒ (i); every element of the right-hand set is
  a lower bound of Y and every lower bound of Y is in the set.
- Citation: [PPA §A.1, p. 394] (book p. 394; PDF p. 410)

### [U0:A.1-d] Moore family (unnumbered definition)
- Statement: a *Moore family* is a subset Y of a complete lattice L = (L, ⊑) that is closed under
  greatest lower bounds: ∀Y′ ⊆ Y : ⨅Y′ ∈ Y.
- Consequences stated: a Moore family always contains a least element ⨅Y and a greatest element ⨅∅,
  which equals ⊤ of L; in particular a Moore family is never empty.
- Citation: [PPA §A.1, p. 395] (book p. 395; PDF p. 411)

### Example A.3 — Moore families in (𝒫({1,2,3}), ⊆)
- Statement: in the complete lattice of Figure A.1 (a), {{2}, {1,2}, {2,3}, {1,2,3}} and {∅, {1,2,3}}
  are Moore families; {{1}, {2}} and {∅, {1}, {2}, {1,2}} are not.
- Side conditions: the book gives no reasons. [derived] {{1}, {2}} lacks {1} ∩ {2} = ∅ and lacks
  ⨅∅ = {1,2,3}; {∅, {1}, {2}, {1,2}} lacks ⨅∅ = {1,2,3}.
- Citation: [PPA §A.1, p. 395] (book p. 395; PDF p. 411)

### [U0:A.1-e] Properties of functions (unnumbered definition)
- Statement: for f : L₁ → L₂ between partially ordered sets L₁ = (L₁, ⊑₁), L₂ = (L₂, ⊑₂):
  - *surjective* (onto, epic): ∀l₂ ∈ L₂ : ∃l₁ ∈ L₁ : f(l₁) = l₂;
  - *injective* (1–1, monic): ∀l, l′ ∈ L₁ : f(l) = f(l′) ⇒ l = l′;
  - *monotone* (isotone, order-preserving): ∀l, l′ ∈ L₁ : l ⊑₁ l′ ⇒ f(l) ⊑₂ f(l′);
  - *additive* (join morphism; sometimes called *distributive*): ∀l₁, l₂ ∈ L₁ : f(l₁ ⊔ l₂) = f(l₁) ⊔ f(l₂);
  - *multiplicative* (meet morphism): ∀l₁, l₂ ∈ L₁ : f(l₁ ⊓ l₂) = f(l₁) ⊓ f(l₂);
  - *completely additive* (complete join morphism): ∀Y ⊆ L₁ : f(⨆₁Y) = ⨆₂{f(l′) | l′ ∈ Y} whenever
    ⨆₁Y exists;
  - *completely multiplicative* (complete meet morphism): ∀Y ⊆ L₁ : f(⨅₁Y) = ⨅₂{f(l′) | l′ ∈ Y}
    whenever ⨅₁Y exists;
  - *affine*: for all non-empty Y ⊆ L₁ : f(⨆₁Y) = ⨆₂{f(l′) | l′ ∈ Y} whenever ⨆₁Y exists (and Y ≠ ∅);
  - *strict*: f(⊥₁) = ⊥₂.
- Stated fact: a function is completely additive if and only if it is both affine and strict.
- Side conditions: when L₂ is not a complete lattice, the statements additionally require the
  relevant least upper bounds and greatest lower bounds to exist in L₂.
- Citation: [PPA §A.1, p. 395] (book p. 395; PDF p. 411); completely multiplicative, affine and strict are on [PPA §A.1, p. 396] (book p. 396; PDF p. 412)

### Lemma A.4 — Complete multiplicativity on a finite domain
- Statement: let L = (L, ⊑, ⊔, ⊓, ⊥, ⊤) and M = (M, ⊑, ⊔, ⊓, ⊥, ⊤) be complete lattices with M finite.
  Then the three conditions (i) γ : M → L is monotone, (ii) γ(⊤) = ⊤, (iii) γ(m₁ ⊓ m₂) = γ(m₁) ⊓ γ(m₂)
  whenever m₁ ⋢ m₂ ∧ m₂ ⋢ m₁, are jointly equivalent to γ : M → L being completely multiplicative.
- Side conditions: M must be finite; (iii) is required only for incomparable pairs.
- Proof (summary): induction on the cardinality of M′ ⊆ M proving Display (A.2); base case from (ii);
  step M′ = M″ ∪ {m″} with m″ ∉ M″; comparable pairs are covered by monotonicity.
- Citation: [PPA §A.1, p. 396] (book p. 396; PDF p. 412)

### Display (A.2) — Meet preservation on finite subsets
- Statement: γ(⨅M′) = ⨅{γ(m) | m ∈ M′}.
- Side conditions: the claim proved by induction on the finite cardinality of M′ ⊆ M in Lemma A.4.
- Citation: [PPA §A.1, p. 396] (book p. 396; PDF p. 412)

### Lemma A.5 — Affine maps between powersets
- Statement: f : (𝒫(D), ⊆) → (𝒫(E), ⊆) is affine if and only if there exist φ : D → 𝒫(E) and
  φ_∅ ∈ 𝒫(E) such that f(Y) = ⋃{φ(d) | d ∈ Y} ∪ φ_∅. Furthermore f is completely additive if and only if
  additionally φ_∅ = ∅.
- Proof (summary): witnesses φ(d) = f({d}) and φ_∅ = f(∅); write Y as the union of the non-empty family
  {{d} | d ∈ Y} ∪ {∅} and apply affinity.
- Citation: [PPA §A.1, p. 396] (book p. 396; PDF p. 412); the proof is completed on [PPA §A.1, p. 397] (book p. 397; PDF p. 413)

### [U0:A.1-f] Isomorphism (unnumbered definition)
- Statement: an isomorphism from (L₁, ⊑₁) to (L₂, ⊑₂) is a monotone θ : L₁ → L₂ for which there is a
  (necessarily unique) monotone θ⁻¹ : L₂ → L₁ with θ ∘ θ⁻¹ = id₂ and θ⁻¹ ∘ θ = id₁.
- Citation: [PPA §A.1, p. 397] (book p. 397; PDF p. 413)

### Projections (A.1)
- cs_theory: lattice vocabulary for every analysis domain; Moore families give a least element of any
  meet-closed (Moore family) subset of acceptable solutions; Lemma A.5 characterises affine powerset
  maps as per-element images plus a constant; Lemma A.4 is a finite test for complete multiplicativity
  of a map named γ.
- swe_architecture: a domain interface exposes bottom, order test and join (top and meet when needed);
  the order direction is a parameter, since (𝒫(S), ⊇) reuses the powerset code with ⋂ as join;
  Lemma A.5 justifies storing an affine powerset transfer function as a table of per-element images
  plus a constant (gen/kill [external] shape).
- practical_debugging: unit-test reflexivity, transitivity, anti-symmetry and least-upper-bound laws;
  a node with no predecessors receives the fold identity ⨆∅ = ⊥, so an intersection-based analysis
  initialised with ∅ instead of S is wrong; imprecision appearing only at merge points suggests a
  non-additive transfer function.
- cyber: a may-taint [external] analysis uses (𝒫(Sources), ⊆) with join ⋃; a must-sanitised
  [external] analysis uses the dual order with join ⋂; swapping the two at a control-flow merge turns
  one checked branch into a sanitiser bypass.

## A.2 Construction of Complete Lattices

Context: the section treats products and then two kinds of function spaces [PPA §A.2, p. 397] (book p. 397; PDF p. 413).

### [U0:A.2-a] Cartesian product (unnumbered definition)
- Statement: for partially ordered sets L₁ = (L₁, ⊑₁), L₂ = (L₂, ⊑₂), L = {(l₁, l₂) | l₁ ∈ L₁ ∧ l₂ ∈ L₂}
  with (l₁₁, l₂₁) ⊑ (l₁₂, l₂₂) iff l₁₁ ⊑₁ l₁₂ ∧ l₂₁ ⊑₂ l₂₂. L is a partially ordered set. If each
  Lᵢ = (Lᵢ, ⊑ᵢ, ⨆ᵢ, ⨅ᵢ, ⊥ᵢ, ⊤ᵢ) is a complete lattice then so is L, with
  ⨆Y = (⨆₁{l₁ | ∃l₂ : (l₁, l₂) ∈ Y}, ⨆₂{l₂ | ∃l₁ : (l₁, l₂) ∈ Y}) and ⊥ = (⊥₁, ⊥₂), and similarly for ⨅Y
  and ⊤. Written L₁ × L₂.
- Citation: [PPA §A.2, p. 397] (book p. 397; PDF p. 413); the complete-lattice clauses are on [PPA §A.2, p. 398] (book p. 398; PDF p. 414)

### [U0:A.2-b] Smash product (unnumbered definition)
- Statement: a variant of the cartesian product in which all pairs (l₁, l₂) satisfy l₁ = ⊥₁ ⇔ l₂ = ⊥₂.
- Citation: [PPA §A.2, p. 398] (book p. 398; PDF p. 414)

### [U0:A.2-c] Total function space (unnumbered definition)
- Statement: for a partially ordered set L₁ = (L₁, ⊑₁) and a set S, L = {f : S → L₁ | f is a total
  function} with f ⊑ f′ iff ∀s ∈ S : f(s) ⊑₁ f′(s). If L₁ is a complete lattice then so is L, with
  ⨆Y = λs.⨆₁{f(s) | f ∈ Y} and ⊥ = λs.⊥₁ (similarly ⨅Y and ⊤). Written S → L₁.
- Citation: [PPA §A.2, p. 398] (book p. 398; PDF p. 414)

### [U0:A.2-d] Monotone function space (unnumbered definition)
- Statement: for partially ordered sets L₁, L₂, L = {f : L₁ → L₂ | f is a monotone function} with
  f ⊑ f′ iff ∀l₁ ∈ L₁ : f(l₁) ⊑₂ f′(l₁). If each Lᵢ is a complete lattice then so is L, with
  ⨆Y = λl₁.⨆₂{f(l₁) | f ∈ Y} and ⊥ = λl₁.⊥₂ (similarly ⨅Y and ⊤). Written L₁ → L₂.
- Side conditions: the same arrow → is used for the total and the monotone function space; whether the
  source is a plain set or a partially ordered set disambiguates.
- Citation: [PPA §A.2, p. 398] (book p. 398; PDF p. 414)

### Projections (A.2)
- cs_theory: product and function-space constructions lift complete lattices; the chain-condition
  preservation results for them are in §A.3 ([U0:A.3-d]).
- swe_architecture: a product is a record of independent analysis components; a total function space
  is an abstract environment keyed by variables or labels; a monotone function space is the type of
  transfer functions and summaries as values.
- practical_debugging: the componentwise order of a product cannot express facts relating two
  components; termination of an environment-shaped domain depends on its key set being finite (§A.3).
- cyber: a confidentiality × integrity product [external] keeps the two components independent; maps
  keyed by attacker-controlled strings form a total function space with an unbounded key set.

## A.3 Chains

Context: the ordering of a complete lattice expresses when one property is better (more precise) than
another; an analysis constructs a sequence of elements, and this section studies such sequences
[PPA §A.3, p. 398] (book p. 398; PDF p. 414).

### [U0:A.3-a] Chain; finite chain (unnumbered definition)
- Statement: Y ⊆ L of a partially ordered set L = (L, ⊑) is a *chain* if
  ∀l₁, l₂ ∈ Y : (l₁ ⊑ l₂) ∨ (l₂ ⊑ l₁): a (possibly empty) totally ordered subset. A *finite chain* is a
  chain that is a finite subset of L.
- Citation: [PPA §A.3, p. 399] (book p. 399; PDF p. 415)

### [U0:A.3-b] Ascending chain; descending chain; eventual stabilisation (unnumbered definition)
- Statement: a sequence (lₙ)ₙ = (lₙ)_{n∈ℕ} is an *ascending chain* if n ≤ m ⇒ lₙ ⊑ lₘ and a
  *descending chain* if n ≤ m ⇒ lₙ ⊒ lₘ; both are chains (writing (lₙ)ₙ also for {lₙ | n ∈ ℕ}).
  (lₙ)ₙ *eventually stabilises* iff ∃n₀ ∈ ℕ : ∀n ∈ ℕ : n ≥ n₀ ⇒ lₙ = l_{n₀}.
- Notation: ⨆ₙ lₙ for ⨆{lₙ | n ∈ ℕ}; ⨅ₙ lₙ for ⨅{lₙ | n ∈ ℕ}.
- Citation: [PPA §A.3, p. 399] (book p. 399; PDF p. 415)

### [U0:A.3-c] Finite height; Ascending Chain Condition; Descending Chain Condition (unnumbered definition)
- Statement: L has *finite height* iff all chains are finite; finite height *at most h* if all chains
  contain at most h + 1 elements; finite height *h* if additionally some chain has h + 1 elements. L
  satisfies the *Ascending Chain Condition* iff all ascending chains eventually stabilise, and the
  *Descending Chain Condition* iff all descending chains eventually stabilise.
- Citation: [PPA §A.3, p. 399] (book p. 399; PDF p. 415)

### Lemma A.6 — Finite height iff both chain conditions
- Statement: a partially ordered set L = (L, ⊑) has finite height if and only if it satisfies both the
  Ascending and the Descending Chain Conditions.
- Proof (summary): (⇒) every ascending or descending chain is finite, hence stabilises. (⇐) for a
  non-empty chain Y, Display (A.3) is proved by a descending chain in Y′ that stabilises by the
  Descending Chain Condition; then elements of Y are enumerated in increasing order as an ascending
  chain, which stabilises by the Ascending Chain Condition, so Y is finite.
- Citation: [PPA §A.3, p. 399] (book p. 399; PDF p. 415); the proof is completed on [PPA §A.3, p. 400] (book p. 400; PDF p. 416)

### Display (A.3) — Least elements in a chain
- Statement: each non-empty subset Y′ of Y contains a least element.
- Side conditions: auxiliary result inside the proof of Lemma A.6, for a non-empty chain Y in a
  partially ordered set satisfying both chain conditions; its proof uses the Descending Chain
  Condition. §B.1 cites this proof for well-founded induction ([U0:B.1-g]).
- Citation: [PPA §A.3, p. 399] (book p. 399; PDF p. 415); the proof is on [PPA §A.3, p. 400] (book p. 400; PDF p. 416)

### Figure A.2 — Two partially ordered sets
- Content: (a) a vertical chain with 0 at the top, then −1, −2, …, and −∞ at the bottom; (b) a
  vertical chain with 0 at the bottom, then 1, 2, …, and ∞ at the top.
- Citation: [PPA §A.3, p. 400] (book p. 400; PDF p. 416)

### Example A.7 — Chain conditions without finite height
- Statement: the partially ordered set of Figure A.2 (a) satisfies the Ascending Chain Condition but
  does not have finite height; that of Figure A.2 (b) satisfies the Descending Chain Condition but does
  not have finite height.
- Citation: [PPA §A.3, p. 400] (book p. 400; PDF p. 416)

### [U0:A.3-d] Preservation of chain conditions (unnumbered fact)
- Statement: each of the three conditions finite height, Ascending Chain Condition and Descending Chain
  Condition is preserved under cartesian product: if L₁ and L₂ satisfy it then so does L₁ × L₂. The
  total function space S → L preserves the conditions of L only if S is finite. The monotone function
  space L₁ → L₂ does not in general preserve the conditions.
- Side conditions: stated as "one can show"; no proof is given.
- Citation: [PPA §A.3, p. 400] (book p. 400; PDF p. 416)

### Lemma A.8 — Complete lattices satisfying the Ascending Chain Condition
- Statement: for a partially ordered set L = (L, ⊑) the conditions (i) L is a complete lattice
  satisfying the Ascending Chain Condition, and (ii) L has a least element ⊥, binary least upper bounds
  and satisfies the Ascending Chain Condition, are equivalent.
- Proof (summary): ⨆∅ = ⊥; finite Y by iterated binary joins; infinite Y by an ascending chain
  l₀ = y₀, l_{n+1} = lₙ if every y ∈ Y satisfies y ⊑ lₙ, otherwise l_{n+1} = lₙ ⊔ y_{n+1} for some
  y_{n+1} ⋢ lₙ; the chain stabilises at the least upper bound of Y. Lemma A.2 completes the argument.
- Citation: [PPA §A.3, p. 401] (book p. 401; PDF p. 417)

### Lemma A.9 — Additive iff affine under the Ascending Chain Condition
- Statement: for a complete lattice L = (L, ⊑) satisfying the Ascending Chain Condition and a total
  f : L → L, the conditions (i) f is additive, ∀l₁, l₂ : f(l₁ ⊔ l₂) = f(l₁) ⊔ f(l₂), and (ii) f is
  affine, ∀Y ⊆ L, Y ≠ ∅ : f(⨆Y) = ⨆{f(l) | l ∈ Y}, are equivalent, and in both cases f is monotone.
- Side conditions: the Ascending Chain Condition is required for (i) ⇒ (ii).
- Citation: [PPA §A.3, p. 401] (book p. 401; PDF p. 417)

### Projections (A.3)
- cs_theory: the Ascending Chain Condition is the termination precondition for iteration from ⊥;
  finite height needs both chain conditions; Lemma A.8 lets a lattice be specified by ⊥ and binary
  join alone when the Ascending Chain Condition holds.
- swe_architecture: height h bounds how many times one component can change; environments keyed by an
  unbounded set lose the chain conditions, so the key set must be bounded by program syntax or the
  domain needs widening (§4.2, outside this unit).
- practical_debugging: a solver that never stabilises points to a domain without the Ascending Chain
  Condition (Figure A.2 (b) climbs forever) or to an environment keyed by an infinite set; compare
  observed update counts with the declared height.
- cyber: an analyser keyed by attacker-controlled strings, unbounded call strings or symbolic addresses
  has an infinite key set and can be driven into very long ascending chains (resource exhaustion
  [external]).

## A.4 Fixed Points

### [U0:A.4-a] Fixed points; reductive; extensive; least and greatest fixed point (unnumbered definition)
- Statement: for a monotone f : L → L on a complete lattice L = (L, ⊑, ⨆, ⨅, ⊥, ⊤): l is a fixed point
  iff f(l) = l, and Fix(f) = {l | f(l) = l}; f is *reductive* at l iff f(l) ⊑ l, Red(f) = {l | f(l) ⊑ l},
  and f is reductive if Red(f) = L; f is *extensive* at l iff f(l) ⊒ l, Ext(f) = {l | f(l) ⊒ l}, and f is
  extensive if Ext(f) = L. lfp(f) = ⨅Fix(f) and gfp(f) = ⨆Fix(f).
- Side conditions: these bounds exist because L is a complete lattice. Red(f) and Ext(f) correspond to
  pre-fixed and post-fixed points [external]; the book uses only Red and Ext.
- Citation: [PPA §A.4, p. 402] (book p. 402; PDF p. 418)

### Proposition A.10 — Tarski's Fixed Point Theorem
- Statement: let L = (L, ⊑, ⨆, ⨅, ⊥, ⊤) be a complete lattice. If f : L → L is a monotone function then
  lfp(f) = ⨅Red(f) ∈ Fix(f) and gfp(f) = ⨆Ext(f) ∈ Fix(f). Hence lfp(f) is the least and gfp(f) the
  greatest fixed point of f.
- Side conditions: f monotone; L complete.
- Proof (summary): for l₀ = ⨅Red(f), f(l₀) ⊑ f(l) ⊑ l for every l ∈ Red(f), so f(l₀) ⊑ l₀; then
  f(f(l₀)) ⊑ f(l₀) puts f(l₀) in Red(f), giving l₀ ⊑ f(l₀); leastness from Fix(f) ⊆ Red(f); gfp
  similarly.
- Citation: [PPA §A.4, p. 402] (book p. 402; PDF p. 418); the proof is completed on [PPA §A.4, p. 403] (book p. 403; PDF p. 419)

### Figure A.3 — Fixed points of f
- Content: L drawn vertically with, from bottom to top, ⊥, fⁿ(⊥), ⨆ₙ fⁿ(⊥), lfp(f), gfp(f),
  ⨅ₙ fⁿ(⊤), fⁿ(⊤), ⊤. An outer ellipse spans L; two overlapping inner ellipses are labelled Red(f)
  (upper, from lfp(f) to ⊤) and Ext(f) (lower, from ⊥ to gfp(f)); their overlap is labelled Fix(f).
- Citation: [PPA §A.4, p. 403] (book p. 403; PDF p. 419)

### [U0:A.4-b] Iteration bounds for fⁿ(⊥) and fⁿ(⊤) (unnumbered fact)
- Statement: no continuity requirement (e.g. f(⨆ₙ lₙ) = ⨆ₙ(f(lₙ)) for all ascending chains (lₙ)ₙ) is
  imposed on f, so iterating from ⊥ is not guaranteed to reach the fixed point. One can show
  ⊥ ⊑ fⁿ(⊥) ⊑ ⨆ₙ fⁿ(⊥) ⊑ lfp(f) ⊑ gfp(f) ⊑ ⨅ₙ fⁿ(⊤) ⊑ fⁿ(⊤) ⊑ ⊤, and all inequalities can be strict (⊏).
  If L satisfies the Ascending Chain Condition there exists n with fⁿ(⊥) = fⁿ⁺¹(⊥) and hence
  lfp(f) = fⁿ(⊥); any monotone f over a partially ordered set satisfying the Ascending Chain Condition is
  also continuous. If L satisfies the Descending Chain Condition there exists n with fⁿ(⊤) = fⁿ⁺¹(⊤)
  and hence gfp(f) = fⁿ(⊤).
- Side conditions: the iteration is called Kleene iteration [external] elsewhere; the book does not
  name it.
- Citation: [PPA §A.4, p. 403] (book p. 403; PDF p. 419)

### [U0:A.4-c] Transfinite iteration (unnumbered remark)
- Statement: Remark "for readers familiar with ordinal numbers": lfp(f) can always be obtained as the
  limit of an ascending (transfinite) sequence. Define f^{↑κ} ∈ L for an ordinal κ by
  f^{↑κ} = f(⨆_{κ′<κ} f^{↑κ′}); for a natural number n, f^{↑n} = fⁿ⁺¹(⊥). Then lfp(f) = f^{↑κ} whenever κ
  is a cardinal number strictly greater than the cardinality of L (e.g. the cardinality of 𝒫(L)). A
  similar construction obtains gfp(f) as the limit of a descending (transfinite) chain.
- Side conditions: the index of f^{↑n} is offset by one from the fⁿ(⊥) of [U0:A.4-b] (finding F-U0-04).
- Citation: [PPA §A.4, p. 404] (book p. 404; PDF p. 420)

### Findings (A.4)
- F-U0-04: on p. 404 the remark writes f^{↑n} = fⁿ⁺¹(⊥), while p. 403 indexes iterates as fⁿ(⊥) with
  f⁰(⊥) = ⊥; the two indexings differ by one. Recorded, not corrected. [PPA §A.4, p. 404] (book p. 404; PDF p. 420)

### Projections (A.4)
- cs_theory: Proposition A.10 gives existence and characterisation of lfp and gfp for monotone maps on
  complete lattices; the Kleene [external] chain `⨆ₙ fⁿ(⊥)` equals `lfp(f)` when `f` is continuous,
  and stabilises in finitely many steps (`∃n : fⁿ(⊥) = lfp(f)`) when `L` satisfies the Ascending Chain
  Condition (both sufficient conditions); transfinite iteration needs neither.
- swe_architecture: a checker can validate a claimed result l with one application of f: f(l) ⊑ l
  places l in Red(f), so lfp(f) ⊑ l; results can therefore be shipped as re-checkable certificates.
- practical_debugging: stopping an iteration early yields fⁿ(⊥), which is below lfp(f) and unsound for
  an over-approximating analysis; a fixed point that is not least suggests iteration did not start from
  ⊥ or reused state.
- cyber: an analyser with an iteration cap reports a state below lfp(f) and can miss flows; a safe
  cap must be followed by a jump to an element of Red(f) (widening, §4.2, outside this unit).

## Concluding Remarks (Appendix A)

### Concluding Remarks (Appendix A) — summary
- Statement: for more information on partially ordered sets consult a text book (e.g. [43]).
- Side conditions: Appendix A has no Exercises section and no Mini Projects (finding F-U0-05).
- Citation: [PPA Appendix A, p. 404] (book p. 404; PDF p. 420)

## B.1 Proof by Induction

Context: Appendix B reviews inductive proof techniques, motivates coinduction and formulates a general
coinductive proof principle; it makes heavy use of Tarski's Fixed Point Theorem (Proposition A.10)
[PPA Appendix B, p. 405] (book p. 405; PDF p. 421).

### [U0:B.1-a] Mathematical induction (unnumbered principle)
- Statement: establish Q(0) and ∀n : Q(n) ⇒ Q(n+1); conclude ∀n : Q(n).
- Side conditions: justified because every natural number is 0 or a successor n+1; the principle
  reflects the way the natural numbers are constructed.
- Citation: [PPA §B.1, p. 405] (book p. 405; PDF p. 421)

### [U0:B.1-b] Algebraic data type D and size measure (unnumbered definition)
- Statement: d ∈ **D**, d ::= Base | Con₁(d) | Con₂(d, d) (base case, unary and binary constructor).
  size(Base) = 0; size(Con₁(d)) = 1 + size(d); size(Con₂(d₁, d₂)) = 1 + size(d₁) + size(d₂). Q(d) for all
  d follows by mathematical induction on size(d).
- Citation: [PPA §B.1, p. 405] (book p. 405; PDF p. 421); the size measure is on [PPA §B.1, p. 406] (book p. 406; PDF p. 422)

### [U0:B.1-c] Structural induction (unnumbered principle)
- Statement: show Q(Base); ∀d : Q(d) ⇒ Q(Con₁(d)); ∀d₁, d₂ : Q(d₁) ∧ Q(d₂) ⇒ Q(Con₂(d₁, d₂)); conclude
  ∀d : Q(d). The proof principle reflects the way the data are constructed.
- Citation: [PPA §B.1, p. 406] (book p. 406; PDF p. 422)

### [U0:B.1-d] Natural Semantics d → n; evaluation trees (unnumbered definition)
- Statement: reading Base as 0, Con₁(d) as d + 1 and Con₂(d₁, d₂) as d₁ + d₂:
  [base] Base → 0; [con₁] from d → n infer Con₁(d) → n + 1; [con₂] from d₁ → n₁ and d₂ → n₂ infer
  Con₂(d₁, d₂) → n₁ + n₂. Evaluation trees are written d →^▽ n (arrow with a ▽ above it); one base
  case ([base]) and two constructors ([con₁], [con₂]).
- Citation: [PPA §B.1, p. 406] (book p. 406; PDF p. 422)

### [U0:B.1-e] Induction on the shape of inference trees (unnumbered principle)
- Statement: show Q(Base → 0);
  ∀(d →^▽ n) : Q(d →^▽ n) ⇒ Q(tree with premise d →^▽ n and conclusion Con₁(d) → n+1);
  ∀(d₁ →^▽ n₁), (d₂ →^▽ n₂) : Q(d₁ →^▽ n₁) ∧ Q(d₂ →^▽ n₂) ⇒ Q(tree with premises d₁ →^▽ n₁, d₂ →^▽ n₂
  and conclusion Con₂(d₁, d₂) → n₁ + n₂); conclude ∀(d →^▽ n) : Q(d →^▽ n).
- Side conditions: conceals a mathematical induction on the size of evaluation trees.
- Citation: [PPA §B.1, p. 406] (book p. 406; PDF p. 422); the principle is completed on [PPA §B.1, p. 407] (book p. 407; PDF p. 423)

### [U0:B.1-f] Course of values induction (unnumbered principle)
- Statement: prove ∀n : (∀m < n : Q(m)) ⇒ Q(n); conclude ∀n : Q(n). The base case is handled in the same
  way as the induction step.
- Citation: [PPA §B.1, p. 407] (book p. 407; PDF p. 423)

### [U0:B.1-g] Well-founded ordering; well-founded induction (unnumbered definition and principle)
- Statement: a partial ordering ⪯ on D is *well-founded* if there is no infinite decreasing sequence
  d₁ ≻ d₂ ≻ d₃ ≻ ⋯, where d ≻ d′ means d′ ⪯ d ∧ d ≠ d′; the book says this amounts to the Descending Chain
  Condition of Appendix A. Principle: from ∀d : (∀d′ ≺ d : Q(d′)) ⇒ Q(d) conclude ∀d : Q(d).
- Side conditions: correctness is proved along the lines of the proof of Display (A.3) in Lemma A.6.
  Course of values induction is the instance (ℕ, ≤).
- Citation: [PPA §B.1, p. 407] (book p. 407; PDF p. 423)

### Projections (B.1)
- cs_theory: five induction principles of increasing generality; well-founded induction rests on the
  Descending Chain Condition, not the ascending one.
- swe_architecture: structural induction is the correctness argument for a fold or visitor with one
  case per constructor; induction on inference trees matches evaluators and checkers written with one
  case per rule.
- practical_debugging: a missing constructor case is a missing proof case; unbounded recursion means
  some argument fails to decrease in a well-founded order (ranking function [external]).
- cyber: termination arguments for parsers of untrusted input need a well-founded measure that every
  recursive call decreases; without one, crafted input can force unbounded recursion.

## B.2 Introducing Coinduction

### [U0:B.2-a] Motivating program (unnumbered example)
- Statement: program `if f(27, m) then "something good" else "something bad"`, with f from pairs of
  natural numbers to truth values and m unknown. Goal: the program never does "something bad".
  Predicate: Q_f(n) iff ∀m : f(n, m) ≠ false (n, m ≥ 0). Inductive approach: Q_f(0) and
  ∀n : Q_f(n) ⇒ Q_f(n+1) give ∀n : Q_f(n), hence Q_f(27); equivalently the axiom Q_f(0) and the rule
  from Q_f(n) infer Q_f(n+1) form an *inductive definition* of Q_f.
- Citation: [PPA §B.2, p. 407] (book p. 407; PDF p. 423); the predicate and rule are on [PPA §B.2, p. 408] (book p. 408; PDF p. 424)

### [U0:B.2-b] Functions f₀–f₃ (unnumbered definition)
- Statement: f₀(0, m) = true, f₀(n+1, m) = f₀(n, m); f₁(0, m) = f₁(0, m), f₁(n+1, m) = f₁(n, m);
  f₂(0, m) = true, f₂(n+1, m) = f₂(n+1, m); f₃(0, m) = f₃(0, m), f₃(n+1, m) = f₃(n+1, m). For i = 1, 2, 3,
  fᵢ(27, m) never terminates.
- Side conditions: induction cannot establish the base case (f₁, f₃) and/or the inductive step (f₂, f₃).
  The intuitive argument (assume all right-hand occurrences of fᵢ satisfy Qᵢ, conclude the left-hand
  side does) "sounds very dangerous" but, with due care and the proper definition of Qᵢ, is a valid
  coinductive proof.
- Citation: [PPA §B.2, p. 408] (book p. 408; PDF p. 424); the non-termination remark and the coinductive intuition are on [PPA §B.2, p. 409] (book p. 409; PDF p. 425)

### Display (B.1) — Clauses for Qᵢ
- Statement: Q₀(0) iff true; Q₀(n+1) iff Q₀(n). Q₁(0) iff Q₁(0); Q₁(n+1) iff Q₁(n). Q₂(0) iff true;
  Q₂(n+1) iff Q₂(n+1). Q₃(0) iff Q₃(0); Q₃(n+1) iff Q₃(n+1).
- Side conditions: the clauses for Q₀ look like the principle of mathematical induction; the others
  involve circularity.
- Citation: [PPA §B.2, p. 409] (book p. 409; PDF p. 425)

### Display (B.2) — Fixed-point form
- Statement: Qᵢ = 𝒬ᵢ(Qᵢ).
- Citation: [PPA §B.2, p. 409] (book p. 409; PDF p. 425)

### Display (B.3) — The functionals 𝒬ᵢ
- Statement: 𝒬₀(Q′)(0) = true, 𝒬₀(Q′)(n+1) = Q′(n); 𝒬₁(Q′)(0) = Q′(0), 𝒬₁(Q′)(n+1) = Q′(n);
  𝒬₂(Q′)(0) = true, 𝒬₂(Q′)(n+1) = Q′(n+1); 𝒬₃(Q′)(0) = Q′(0), 𝒬₃(Q′)(n+1) = Q′(n+1).
- Side conditions: Qᵢ satisfies (B.1) iff it satisfies (B.2) with 𝒬ᵢ as in (B.3). Each 𝒬ᵢ is monotone
  on the complete lattice (ℕ → {true, false}, ⊑) with Q₁ ⊑ Q₂ iff ∀n : Q₁(n) ⇒ Q₂(n), ⊥(n) = false and
  ⊤(n) = true; by Proposition A.10 each 𝒬ᵢ has lfp(𝒬ᵢ) and gfp(𝒬ᵢ), possibly different predicates. A
  *functional* is a function whose argument and result are themselves functions (or more elaborate
  structures containing functions).
- Citation: [PPA §B.2, p. 409] (book p. 409; PDF p. 425)

### [U0:B.2-c] Least fixed points of 𝒬₀ and 𝒬₃ (unnumbered fact)
- Statement: ⨆ₖ 𝒬₀ᵏ(⊥) ⊑ lfp(𝒬₀) by Appendix A; since the clauses for 𝒬₀(Q) use only a finite number
  of Q's on the right-hand sides (zero or one), 𝒬₀ satisfies a continuity property ensuring
  ⨆ₖ 𝒬₀ᵏ(⊥) = lfp(𝒬₀). 𝒬₀ᵏ(⊥)(n) holds iff at most k axioms and rules suffice to prove Q₀(n); a proof by
  induction "corresponds" to taking the least fixed point. lfp(𝒬₃) = ⊥ because 𝒬₃(⊥) = ⊥; hence
  lfp(𝒬₃)(27) = false and an inductive proof cannot establish Q₃(27).
- Side conditions: for 𝒬₁ and 𝒬₂ the book says only "somewhat similar arguments can be given"; it
  does not state their least fixed points.
- Citation: [PPA §B.2, p. 410] (book p. 410; PDF p. 426)

### [U0:B.2-d] Greatest fixed points; agreement for 𝒬₀ (unnumbered fact)
- Statement: gfp(𝒬₃) = ⊤ because 𝒬₃(⊤) = ⊤; hence gfp(𝒬₃)(27) = true, the formal underpinning for the
  belief that f₃ causes no harm (similar arguments for 𝒬₁, 𝒬₂). gfp(𝒬₀)(27) = true since
  lfp(𝒬₀)(27) = true and lfp(𝒬₀) ⊑ gfp(𝒬₀). Moreover lfp(𝒬₀) = gfp(𝒬₀), because mathematical induction
  on n proves lfp(𝒬₀)(n) = gfp(𝒬₀)(n); this is unlike 𝒬₁, 𝒬₂ and 𝒬₃.
- Citation: [PPA §B.2, p. 410] (book p. 410; PDF p. 426)

### [U0:B.2-e] Banach remark (unnumbered remark)
- Statement: lfp(𝒬₀) = gfp(𝒬₀) is related to Banach's Fixed Point Theorem: a contractive operator on a
  complete metric space has a unique fixed point. 𝒬₀ is contractive (unlike 𝒬₁, 𝒬₂, 𝒬₃) because the
  clause for 𝒬₀(Q)(n) only calls Q on arguments smaller than n.
- Citation: [PPA §B.2, p. 410] (book p. 410; PDF p. 426)

### Findings (B.2)
- F-U0-01: p. 409 prints "a greatest fixed fixed point gfp(𝒬ᵢ)" (duplicated word). Recorded, not
  corrected. [PPA §B.2, p. 409] (book p. 409; PDF p. 425)

### Projections (B.2)
- cs_theory: induction corresponds to lfp and coinduction to gfp of the same monotone functional; the
  two coincide for contractive functionals such as 𝒬₀ (guarded recursion [external]).
- swe_architecture: when every recursive use is on a strictly smaller argument, the inductive and the
  coinductive reading agree and the implementation choice is free; otherwise a specification must say
  which reading it means.
- practical_debugging: a recursive predicate that is unexpectedly false everywhere was computed as an
  lfp where a gfp was intended (lfp(𝒬₃) = ⊥ but gfp(𝒬₃) = ⊤).
- cyber: safety of a non-terminating service ("something bad" never happens) cannot be shown by finite
  induction over traces; it needs a gfp-style invariant argument.

## B.3 Proof by Coinduction

### [U0:B.3-a] Clause-defined predicate and its functional (unnumbered definition)
- Statement: for Q : **D** → {true, false} defined by clauses Q(Base) iff ⋯; Q(Con₁(d)) iff ⋯Q(d′)⋯;
  Q(Con₂(d₁, d₂)) iff ⋯Q(d₁′)⋯Q(d₂′)⋯, the functional 𝒬 is defined by cases: 𝒬(Q′)(Base) = ⋯;
  𝒬(Q′)(Con₁(d)) = ⋯Q′(d′)⋯; 𝒬(Q′)(Con₂(d₁, d₂)) = ⋯Q′(d₁′)⋯Q′(d₂′)⋯. (**D** → {true, false}, ⊑) is a
  complete lattice with Q₁ ⊑ Q₂ iff ∀d : Q₁(d) ⇒ Q₂(d).
- Side conditions: 𝒬 is assumed monotone, so a clause like "Q(Con₁(d)) iff ¬Q(d)" is not acceptable.
  By Proposition A.10, 𝒬 then has a least and a greatest fixed point.
- Citation: [PPA §B.3, p. 411] (book p. 411; PDF p. 427)

### Display (B.4) — Inductive definition
- Statement: Q = lfp(𝒬).
- Citation: [PPA §B.3, p. 411] (book p. 411; PDF p. 427)

### Display (B.5) — Inductive definition as rules
- Statement: three rules: premise ⋯, conclusion Q(Base); premise ⋯Q(d′)⋯, conclusion Q(Con₁(d));
  premise ⋯Q(d₁′)⋯Q(d₂′)⋯, conclusion Q(Con₂(d₁, d₂)).
- Side conditions: when each rule has only a finite number of calls to Q, (B.5) and (B.4) are
  equivalent: (B.5) amounts to ⨆ₖ 𝒬ᵏ(⊥), which by continuity equals the predicate of (B.4).
- Citation: [PPA §B.3, p. 411] (book p. 411; PDF p. 427); the equivalence is completed on [PPA §B.3, p. 412] (book p. 412; PDF p. 428)

### [U0:B.3-b] Proof by induction (unnumbered definition)
- Statement: a *proof by induction* establishes the validity of the axioms and rules in (B.5). It has a
  constructive flavour: take nothing for granted and believe only what can be demonstrated. It is
  often used to reason about semantics, since a semantics should not allow spurious behaviour not
  forced by the semantics.
- Citation: [PPA §B.3, p. 412] (book p. 412; PDF p. 428)

### [U0:B.3-c] Coinductive definition; proof by coinduction (unnumbered definition and principle)
- Statement: coinductive definition Q = gfp(𝒬). A *proof by coinduction* uses the rule: from
  Q′ ⊑ 𝒬(Q′) infer Q′ ⊑ Q (i.e. from Q′ ⊑ 𝒬(Q′) infer Q′ ⊑ gfp(𝒬)), which follows from the formula for
  gfp in Proposition A.10. To prove Q(d), find some Q′ with Q′(d) and ∀d′ : Q′(d′) ⇒ 𝒬(Q′)(d′).
- Side conditions: optimistic flavour: assume everything as long as no fact is demonstrably violated.
  Commonly used for checking that a specification holds, since a specification should not forbid
  behaviour unless explicitly called for. The rule is called Park's principle [external] elsewhere.
- Citation: [PPA §B.3, p. 412] (book p. 412; PDF p. 428)

### [U0:B.3-d] Derived coinduction rule (unnumbered derived rule)
- Statement: from Q′ ⊑ 𝒬(Q ⊔ Q′) infer Q′ ⊑ Q.
- Proof (summary): Q ⊑ 𝒬(Q) and monotonicity give Q ⊑ 𝒬(Q ⊔ Q′); hence Q ⊔ Q′ ⊑ 𝒬(Q ⊔ Q′), so
  Q ⊔ Q′ ⊑ Q by definition of Q, and Q′ ⊑ Q.
- Side conditions: the explanation generalises to algebraic data types with more base cases and
  constructors, and from predicates to relations.
- Citation: [PPA §B.3, p. 412] (book p. 412; PDF p. 428)

### Example B.1 — Coinduction for mutually defined relations
- Statement: relations R₁ : D₁₁ × D₁₂ → {true, false} and R₂ : D₂₁ × D₂₂ → {true, false} with
  R₁ = ℛ₁(R₁, R₂), R₂ = ℛ₂(R₁, R₂), intended as (R₁, R₂) = gfp(ℛ) where
  ℛ(R₁′, R₂′) = (ℛ₁(R₁′, R₂′), ℛ₂(R₁′, R₂′)) is assumed monotone. d₁ (R′ ⊔ R″) d₂ iff
  (d₁ R′ d₂) ∨ (d₁ R″ d₂); R′ ⊑ R″ iff ∀d₁, d₂ : d₁ R′ d₂ ⇒ d₁ R″ d₂. Principle: from R₁′ ⊑ ℛ₁(R₁′, R₂′) and
  R₂′ ⊑ ℛ₂(R₁′, R₂′) conclude R₁′ ⊑ R₁ and R₂′ ⊑ R₂. It suffices to show R₁′ ⊑ ℛ₁(R₁ ⊔ R₁′, R₂ ⊔ R₂′) and
  R₂′ ⊑ ℛ₂(R₁ ⊔ R₁′, R₂ ⊔ R₂′), because Rᵢ ⊑ ℛᵢ(R₁, R₂) ⊑ ℛᵢ(R₁ ⊔ R₁′, R₂ ⊔ R₂′).
- Citation: [PPA §B.3, p. 413] (book p. 413; PDF p. 429)

### Example B.2 — Inductive and coinductive reading of a grammar
- Statement: universe {0,1,2}^∞ = {0,1,2}* ∪ {0,1,2}^ω of finite strings (aᵢ)ᵢ₌₁ⁿ = a₁⋯aₙ and infinite
  strings (aᵢ)ᵢ₌₁^∞ = a₁⋯aₙ⋯ over {0,1,2}. Concatenation: (aᵢ)ᵢ₌₁ⁿ (bⱼ)ⱼ₌₁ᵐ = (cₖ)ₖ₌₁ⁿ⁺ᵐ and
  (aᵢ)ᵢ₌₁ⁿ (bⱼ)ⱼ₌₁^∞ = (cₖ)ₖ₌₁^∞ with cₖ = aₖ if k ≤ n and cₖ = b_{k−n} if k > n; (aᵢ)ᵢ₌₁^∞ (bⱼ)ⱼ₌₁^⋯ =
  (cₖ)ₖ₌₁^∞ with cₖ = aₖ, where ⋯ denotes m or ∞. Grammar S → 0 | 1 | 0S | 1S, rephrased as 0 ∈ S;
  1 ∈ S; from x ∈ S infer 0x ∈ S; from x ∈ S infer 1x ∈ S.
  - Inductive interpretation (as usual for context free grammars): S = {0,1}⁺, the finite non-empty
    strings (n > 0) without 2.
  - Coinductive interpretation: S = {0,1}⁺ ∪ {0,1}^ω. The empty string is excluded (not of the form 0,
    1, 0x or 1x); strings containing 2 are excluded by induction on n for a string a₁⋯aₙ2x with
    aᵢ ∈ {0,1}; infinite strings of 0's and 1's cannot be excluded since each has the form 0x or 1x with
    x ∈ {0,1}^ω.
  - Adding S → S (rule from x ∈ S infer x ∈ S): inductively S is still {0,1}⁺; coinductively S changes
    dramatically to {0,1,2}^∞, including the empty string and strings containing 2, because any x can
    be written x = x.
- Citation: [PPA §B.3, p. 414] (book p. 414; PDF p. 430); the S → S case is completed on [PPA §B.3, p. 415] (book p. 415; PDF p. 431)

### Projections (B.3)
- cs_theory: inductive definitions are lfp and coinductive ones gfp of a monotone functional; the
  coinduction rule is the gfp formula of Proposition A.10; the derived rule corresponds to
  coinduction up to [external] union with the fixed point; strong bisimulation is the
  suggested further reading.
- swe_architecture: lfp fits semantics and reachability ("only what is forced"); gfp fits
  specification checking ("everything not refuted"), implemented as assume-then-check with a visited
  set playing the role of Q′; memoising facts already in Q is sound by the derived rule.
- practical_debugging: a rule engine with negation through recursion has no guaranteed fixed point
  (stratification [external]); a checker that accepts everything usually contains a self-justifying
  rule such as x ∈ S / x ∈ S; divergence on cyclic input suggests an inductive algorithm for a
  coinductive property.
- cyber: recursive trust or delegation rules must be read inductively; an optimistic (coinductive)
  checker with a cycle A → B → A self-certifies, exactly like S → S in Example B.2; conversely,
  non-interference [external] of a reactive service needs a coinductive invariant as in Example B.1.

## Concluding Remarks (Appendix B)

### Concluding Remarks (Appendix B) — summary
- Statement: for induction principles consult a text book (e.g. [16]). Good introductory material on
  coinduction is harder to find; one possibility is the work on strong bisimulation in CCS (e.g.
  Chapter 4 of [106]).
- Side conditions: Appendix B has no Exercises section; it has two numbered examples (Examples
  B.1 and B.2) plus five numbered displays `(B.1)`–`(B.5)` (finding F-U0-05). Book p. 416 is blank and absent from the PDF.
- Citation: [PPA Appendix B, p. 415] (book p. 415; PDF p. 431)

## C.1 Graphs and Forests

### [U0:C.1-a] Directed graph; edge; self-loop (unnumbered definition)
- Statement: a *directed graph* (digraph, or graph) G = (N, A) has a finite set N of nodes (vertices)
  and a set A ⊆ N × N of edges (arcs). Edge (n₁, n₂) has source n₁ and target n₂ and goes from n₁ to n₂;
  it is a *self-loop* if n₁ = n₂.
- Side conditions: N is finite; A is a set, so there are no parallel edges.
- Citation: [PPA §C.1, p. 417] (book p. 417; PDF p. 432)

### [U0:C.1-b] Directed path; trivial path; concatenation; reachability (unnumbered definition)
- Statement: a path from n₀ to nₘ is a sequence of edges (n₀, n₁), (n₁, n₂), …, (n_{m−1}, nₘ) in which the
  target of each edge is the source of the next; source n₀, target nₘ, length m ≥ 0; the path is
  *trivial* if m = 0 (empty edge sequence). Concatenation joins a path ending at nₘ with one starting at
  nₘ. n′ is *reachable* from n if there is a (possibly trivial) path from n to n′.
- Citation: [PPA §C.1, p. 417] (book p. 417; PDF p. 432)

### Example C.1 — Flow graphs are directed graphs
- Statement: for a statement S of WHILE (Chapter 2), the forward flow graph (labels(S), flow(S)) and
  the backward flow graph (labels(S), flow^R(S)) are directed graphs; for a finite set **Lab** of labels
  and a flow relation F ⊆ **Lab** × **Lab** (Section 2.3), G = (**Lab**, F) is a directed graph.
- Citation: [PPA §C.1, p. 417] (book p. 417; PDF p. 432)

### Example C.2 — Constraint graph for FUN
- Statement: for a FUN program e⋆ (Chapter 3), N⋆ is the finite set of nodes p of the form C(ℓ) or
  r(x) with ℓ ∈ **Lab**⋆ and x ∈ **Var**⋆. For a set C of constraints of the form of Section 3.4, A⋆
  contains (p₁, p₂) for each p₁ ⊆ p₂ in C, and the edges (p, p₂) and (p₁, p₂) for each constraint
  {t} ⊆ p ⇒ p₁ ⊆ p₂ in C. Then G = (N⋆, A⋆) is a directed graph.
- Citation: [PPA §C.1, p. 417] (book p. 417; PDF p. 432); continued on [PPA §C.1, p. 418] (book p. 418; PDF p. 433)

### [U0:C.1-c] Node-sequence notation; paths•; cycles (unnumbered definition)
- Statement: following Chapter 2, a path is written as the node sequence p = [n₀, n₁, …, nₘ]; the
  sequence is never empty; the trivial path from n₀ to n₀ is [n₀], a self-loop is [n₀, n₀];
  [n₀, …, nₘ][nₘ, …, nₖ] = [n₀, …, nₖ] (nₘ does not occur twice).
  paths•(n, n′) = {[n₀, …, nₘ] | m ≥ 0 ∧ n₀ = n ∧ nₘ = n′ ∧ ∀i < m : (nᵢ, n_{i+1}) ∈ A}.
  A *cycle* is a non-trivial path from a node to itself (possibly a self-loop):
  cycles(n) = {[n₀, …, nₘ] | m ≥ 1 ∧ n₀ = n ∧ nₘ = n ∧ ∀i < m : (nᵢ, n_{i+1}) ∈ A}, and
  cycles(n) = {p ∈ paths•(n, n) | p ≠ [n]}.
- Citation: [PPA §C.1, p. 418] (book p. 418; PDF p. 433)

### [U0:C.1-d] Multiple-entry cycle; acyclic; DAG; topological sort (unnumbered definition)
- Statement: a cycle [n₀, …, nₘ] is *multiple entry* if it contains two distinct nodes (not merely
  distinct indices) nᵢ ≠ nⱼ such that there are (not necessarily distinct) nodes nᵢ′ and nⱼ′ external to
  the cycle with (nᵢ′, nᵢ), (nⱼ′, nⱼ) ∈ A. A graph with no cycles (∀n ∈ N : cycles(n) = ∅) is *acyclic*;
  a directed acyclic graph is a *DAG*. A *topological sort* is a total ordering of the nodes such that n
  is strictly before n′ for every edge (n, n′). A directed graph has a topological sort iff it is
  acyclic.
- Citation: [PPA §C.1, p. 418] (book p. 418; PDF p. 433)

### [U0:C.1-e] Strongly connected nodes; the relation 𝒮𝒞 (unnumbered definition)
- Statement: n and n′ are *strongly connected* when there is a (possibly trivial) directed path from n
  to n′ and one from n′ to n. 𝒮𝒞 = {(n, n′) | n and n′ are strongly connected} ⊆ N × N.
- Citation: [PPA §C.1, p. 418] (book p. 418; PDF p. 433)

### Fact C.3 — 𝒮𝒞 is an equivalence relation
- Statement: 𝒮𝒞 is an equivalence relation.
- Proof (summary): reflexive by trivial paths; symmetric by definition; transitive by concatenating a
  path p₁₂ from n₁ to n₂ with p₂₃ from n₂ to n₃.
- Citation: [PPA §C.1, p. 418] (book p. 418; PDF p. 433); the proof is completed on [PPA §C.1, p. 419] (book p. 419; PDF p. 434)

### [U0:C.1-f] Strong components; strongly connected graph; reduced graph (unnumbered definition)
- Statement: the equivalence classes of 𝒮𝒞 are the *strong components* (strongly connected
  components); a graph is *strongly connected* when it has exactly one. The *reduced graph* has one node
  per strongly connected component and an edge from one node to another distinct node iff some edge of
  the original graph goes from a node of the first component to a node of the second; hence the
  reduced graph contains no self-loops.
- Citation: [PPA §C.1, p. 419] (book p. 419; PDF p. 434)

### Example C.4 — Loops as strongly connected components
- Statement: in uniquely labelled statements of WHILE, the nodes corresponding to the outermost loop in
  any nested sequence of loops constitute a strongly connected component, for both forward and
  backward flow graphs.
- Citation: [PPA §C.1, p. 419] (book p. 419; PDF p. 434)

### Lemma C.5 — The reduced graph is a DAG
- Statement: for any graph G the reduced graph is a DAG.
- Proof (summary): a cycle [𝒮𝒞₀, …, 𝒮𝒞ₘ] in the reduced graph contains distinct 𝒮𝒞ᵢ, 𝒮𝒞ⱼ (no
  self-loops); original edges and intra-component paths give paths nᵢ → nⱼ and nⱼ → nᵢ, so nᵢ and nⱼ
  would share a class, a contradiction.
- Citation: [PPA §C.1, p. 419] (book p. 419; PDF p. 434)

### [U0:C.1-g] Handle; root; dummy root (unnumbered definition)
- Statement: a *handle* for G = (N, A) is H ⊆ N such that every n ∈ N is reachable by a (possibly
  trivial) path from some h ∈ H. A *root* is r ∈ N from which every node is reachable. If r is a root
  then {r} is a handle; {n} is a handle iff n is a root. If H is a handle and r ∉ N, then r is a root of
  (N ∪ {r}, A ∪ {(r, h) | h ∈ H}); r is a *dummy root* and each (r, h) a *dummy edge*.
- Citation: [PPA §C.1, p. 419] (book p. 419; PDF p. 434)

### [U0:C.1-h] Minimal handle; rooted graph (unnumbered definition)
- Statement: G = (N, A) always has the handle H = N. H is *minimal* if no proper subset is a handle
  (H′ ⊂ H implies H′ is not a handle); minimal handles always exist since N is finite. The minimal
  handle is a singleton iff the graph has a root; the graph is then *rooted*.
- Citation: [PPA §C.1, p. 420] (book p. 420; PDF p. 435)

### Example C.6 — Roots and handles of flow graphs
- Statement: for a WHILE statement S, init(S) is a root for (labels(S), flow(S)) and {init(S)} is a
  minimal handle; final(S) is a handle for the backward flow graph (labels(S), flow^R(S)).
- Citation: [PPA §C.1, p. 420] (book p. 420; PDF p. 435)

### [U0:C.1-i] Paths from a handle (unnumbered definition)
- Statement: a path from H to n is a path from some h ∈ H to n (for a root r, H = {r}).
  path•^H(n) = ⋃{paths•(h, n) | h ∈ H}; when H is implicit, path•(n) stands for path•^H(n).
- Citation: [PPA §C.1, p. 420] (book p. 420; PDF p. 435)

### [U0:C.1-j] In-degree; forest; parent and child; ancestor and descendant; tree; ordered forest (unnumbered definition)
- Statement: n has *in-degree* m if {n′ | (n′, n) ∈ A} has cardinality m (out-degree similarly). A
  *forest* (unordered, directed forest) is a directed acyclic graph whose nodes have in-degree at most
  1; its nodes of in-degree 0 constitute a minimal handle. If (n, n′) ∈ A then n is the *parent* of n′
  and n′ a *child* of n; *ancestor* and *descendant* are the reflexive, transitive closures of the
  parent and child relations; n is a *proper* ancestor of n′ if it is an ancestor and n ≠ n′ (similarly
  for proper descendants). A *tree* (unordered, directed tree) is a forest with a root, i.e. exactly
  one node of in-degree 0. For a forest with minimal handle H, each h ∈ H is the root of the tree of
  nodes reachable from h, so a forest is a set of trees. *Ordered* forests and trees additionally order
  the children of each node linearly.
- Side conditions: the book writes "all the edges (n₁, n₂) ∈ E" in this paragraph (finding F-U0-02).
- Citation: [PPA §C.1, p. 420] (book p. 420; PDF p. 435)

### [U0:C.1-k] Dominators; Dom equation; proper and direct dominance (unnumbered definition)
- Statement: for G = (N, A) with handle H (possibly H = {r} for a root r), n′ is a *dominator* of n
  (n′ *dominates* n) whenever every (possibly trivial) path from H to n contains n′. Consequently the
  only dominator of an element of a minimal handle (such as a root) is the element itself. Dom(n) is
  the greatest solution of
  Dom(n) = {n} if n ∈ H; Dom(n) = {n} ∪ ⋂{Dom(n′) | (n′, n) ∈ A} otherwise.
  n′ *properly dominates* n if n′ ≠ n and n′ dominates n. n′ *directly dominates* n if it is the
  "closest" proper dominator: n′ ∈ Dom(n) \ {n} and for all n″ ∈ Dom(n) \ {n}, n″ ∈ Dom(n′).
- Side conditions: greatest, not least, solution. "Directly dominates" is called the immediate
  dominator [external] elsewhere.
- Citation: [PPA §C.1, p. 420] (book p. 420; PDF p. 435); the Dom equation is on [PPA §C.1, p. 421] (book p. 421; PDF p. 436)

### Findings (C.1)
- F-U0-02: on p. 420 the forest paragraph writes "all the edges (n₁, n₂) ∈ E" where the edge set is A
  everywhere else and E is not defined in Appendix C; the same paragraph prints "n′ is a said to be a
  child". Recorded, not corrected. [PPA §C.1, p. 420] (book p. 420; PDF p. 435)
- F-U0-06: on p. 419 the text prints "then {r} is handle for G" (missing article). Recorded, not
  corrected. [PPA §C.1, p. 419] (book p. 419; PDF p. 434)

### Projections (C.1)
- cs_theory: graphs, paths, cycles, strong components and the reduced DAG; dominators as the greatest
  solution of an intersection equation.
- swe_architecture: dependency graphs collapse to a reduced DAG of strong components for scheduling;
  multiple entry points become a handle, normalised by a dummy root so single-root algorithms apply;
  strong components can be computed by Tarjan's algorithm [external] (the appendix gives none).
- practical_debugging: computing Dom from the empty set or by upward iteration yields sets that are too
  small on graphs with cycles; initialise non-handle nodes to N; unreachable-node reports depend on the
  handle chosen.
- cyber: a privileged sink whose Dom set lacks the required check node has an unguarded path from the
  entry; dominators on flow^R(S) from the handle final(S) give post-dominators [external], which are
  only meaningful if every exit, including abnormal ones, is in the handle.

## C.2 Reverse Postorder

### Table C.1 — The DFSF Algorithm
- Content (verbatim from the page image; `T` is sans-serif):

```
INPUT:   A directed graph (N, A) with k nodes and handle H
OUTPUT:  (1) A DFSF T = (N, A_T), and
         (2) a numbering rPostorder of the nodes indicating the
             reverse order in which each node was last visited
             and represented as an element of array [N] of int
METHOD:  i := k;
         mark all nodes of N as unvisited;
         let A_T be empty;
         while unvisited nodes in H exists do
             choose a node h in H;
             DFS(h);
USING:   procedure DFS(n) is
             mark n as visited;
             while (n, n') ∈ A and n' has not been visited do
                 add the edge (n, n') to A_T;
                 DFS(n');
             rPostorder[n] := i;
             i := i - 1;
```

- Side conditions: the input requires H to be a handle of (N, A). The choice of h is printed without
  "unvisited" (finding F-U0-03).
- Citation: [PPA §C.2, p. 421] (book p. 421; PDF p. 436)

### [U0:C.2-a] Spanning forest; DFSF; reverse postorder; DFST (unnumbered definition)
- Statement: a *spanning forest* for a graph is a forest with the same nodes as the graph and a subset
  of its edges. Table C.1 non-deterministically constructs a *depth-first spanning forest* (DFSF) and
  numbers the nodes in the reverse of the order in which they are last visited (*reverse postorder*),
  stored in an array indexed by nodes. A DFSF that is a tree is a *depth-first spanning tree* (DFST).
- Side conditions: the algorithm does not specify which unvisited node to select, so the depth-first
  spanning forest for a graph is not unique.
- Citation: [PPA §C.2, p. 421] (book p. 421; PDF p. 436); continued on [PPA §C.2, p. 422] (book p. 422; PDF p. 437)

### [U0:C.2-b] Tree, forward, back and cross edges (unnumbered definition)
- Statement: relative to a spanning forest: *tree edges* are in the forest; *forward edges* are non-tree
  edges from a node to a proper descendant; *back edges* go from descendants to ancestors (including
  self-loops); *cross edges* go between nodes unrelated by the ancestor and descendant relations. Table
  C.1 ensures that cross edges go from nodes visited later (lower rPostorder numbers) to nodes visited
  earlier (higher numbers).
- Citation: [PPA §C.2, p. 422] (book p. 422; PDF p. 437)

### Figure C.1 — A flow graph
- Content: nodes b₁, b₂, b₃, S₁, S₂, S₃; entry arrow into b₁; edges b₁ → b₂, b₁ → b₃, b₂ → S₂,
  b₂ → S₁, b₃ → S₁, b₃ → S₃, S₂ → b₂, S₃ → b₃; exit arrow out of S₁.
- Citation: [PPA §C.2, p. 422] (book p. 422; PDF p. 437)

### Example C.7 — Running the DFSF algorithm
- Statement: for Figure C.1 with root b₁, the algorithm may construct the tree of Figure C.2. The
  reverse postorder is b₁, b₃, S₃, b₂, S₁, S₂, reflected by the second number on each node of Figure
  C.2. The edges S₂ → b₂ and S₃ → b₃ are back edges; b₃ → S₁ is a cross edge.
- Citation: [PPA §C.2, p. 422] (book p. 422; PDF p. 437); continued on [PPA §C.2, p. 423] (book p. 423; PDF p. 438)

### Figure C.2 — A DFSF for the graph in Figure C.1
- Content: tree edges b₁:1 → b₂:4, b₁:1 → b₃:2, b₂:4 → S₂:6, b₂:4 → S₁:5, b₃:2 → S₃:3 (node:rPostorder).
- Citation: [PPA §C.2, p. 423] (book p. 423; PDF p. 438)

### Example C.8 — Edge kinds in WHILE flow graphs
- Statement: for a uniquely labelled WHILE statement S with forward flow graph (labels(S), flow(S)) and
  root init(S): a loop `while b′ do S′` in S gives one tree edge and as many back edges as there are
  elements in final(S′). A conditional `if b′ then S₁′ else S₂′` in S that is not the last statement of
  S and not the last statement of the body of a while loop in S gives three tree edges and one fewer
  cross edges than there are elements in final(S₁′) ∪ final(S₂′). No forward edges arise for WHILE; an
  extension with a one-branch conditional `if b then S` can give forward edges.
- Citation: [PPA §C.2, p. 423] (book p. 423; PDF p. 438)

### Lemma C.9 — Back edges via rPostorder
- Statement: let G = (N, A) be a directed graph, T a depth-first spanning forest of G and rPostorder the
  associated ordering computed by Table C.1. An edge (n, n′) ∈ A is a back edge iff
  rPostorder[n] ≥ rPostorder[n′], and is a self-loop iff rPostorder[n] = rPostorder[n′].
- Proof (summary): (⇒) n is a descendant of n′, so DFS(n′) is pending during DFS(n). (⇐) either n is a
  descendant of n′, or n′ lies in a later subtree, which would make (n, n′) a cross edge from a high to
  a low number, which the algorithm does not admit.
- Citation: [PPA §C.2, p. 423] (book p. 423; PDF p. 438); the proof is completed on [PPA §C.2, p. 424] (book p. 424; PDF p. 439)

### Corollary C.10 — Every cycle contains a back edge
- Statement: with G, T and rPostorder as in Lemma C.9, any cycle of G contains at least one back edge.
- Proof (summary): for a cycle [n₀, …, nₘ] with n₀ = nₘ and m ≥ 1, rPostorder[nᵢ] ≥ rPostorder[n_{i+1}] for
  some 0 ≤ i < m; apply Lemma C.9.
- Citation: [PPA §C.2, p. 424] (book p. 424; PDF p. 439)

### Corollary C.11 — rPostorder topologically sorts the non-back edges
- Statement: with G, T and rPostorder as in Lemma C.9, rPostorder topologically sorts T as well as the
  forward and cross edges.
- Proof (summary): by Lemma C.9, rPostorder[n] < rPostorder[n′] iff (n, n′) is not a back edge, i.e. a
  tree, forward or cross edge.
- Citation: [PPA §C.2, p. 424] (book p. 424; PDF p. 439)

### [U0:C.2-c] Loop connectedness d(G, T) (unnumbered definition)
- Statement: for G = (N, A) with handle H and a depth-first spanning forest T constructed by Table C.1,
  the *loop connectedness* parameter is the largest number of back edges found in any cycle-free path
  of G, written d(G, T), or d(G) when T is clear from the context. For the graph of Figure C.1,
  d(G) = 1.
- Citation: [PPA §C.2, p. 424] (book p. 424; PDF p. 439)

### [U0:C.2-d] Dominator-back edge; reducible graph (unnumbered definition)
- Statement: a *dominator-back edge* is an edge (n₁, n₂) whose target n₂ dominates its source n₁; it is
  a back edge regardless of the choice of T, because the path from H to n₁ in T must contain n₂. The
  literature contains many definitions of reducible graph; here G = (N, A) with handle H is *reducible*
  iff the graph (N, A \ A_db), obtained by removing the set A_db of dominator-back edges, is acyclic and
  still has H as handle.
- Side conditions: Figure C.3 shows there may be more back edges than dominator-back edges.
- Citation: [PPA §C.2, p. 424] (book p. 424; PDF p. 439); the reducibility conditions are on [PPA §C.2, p. 425] (book p. 425; PDF p. 440)

### Figure C.3 — An irreducible graph
- Content: root r with an entry arrow; edges r → n₁, r → n₂, n₁ → n₂, n₂ → n₁. It has no dominator-back
  edges, yet any spanning forest classifies one of the edges between n₁ and n₂ as a back edge; it is
  the simplest example of an irreducible graph.
- Citation: [PPA §C.2, p. 425] (book p. 425; PDF p. 440); the discussion is on [PPA §C.2, p. 424] (book p. 424; PDF p. 439)

### Lemma C.12 — Reducible graphs: back edges are dominator-back edges
- Statement: let G = (N, A) be a reducible graph with handle H, T a depth-first spanning forest for G and
  H, and rPostorder the associated ordering computed by Table C.1. Then an edge is a back edge iff it is
  a dominator-back edge.
- Side conditions: consequently the loop connectedness parameter is independent of the choice of
  depth-first spanning forest for reducible graphs.
- Proof (summary): a back edge (n_s, n_t) that is not a dominator-back edge, added to T, closes a cycle
  in (N, A \ A_db), contradicting reducibility.
- Citation: [PPA §C.2, p. 425] (book p. 425; PDF p. 440)

### Example C.13 — WHILE flow graphs are reducible
- Statement: for a uniquely labelled WHILE statement S, (labels(S), flow(S)) with root init(S) is
  reducible: each while loop can be entered only at its test node, which dominates the loop body, so
  the back edges of the loop are dominator-back edges; tree, forward and cross edges form an acyclic
  graph. The loop connectedness parameter equals the maximum number of back edges (hence
  dominator-back edges) on a cycle-free path, which equals the maximum number of nested while loops in
  the program.
- Citation: [PPA §C.2, p. 425] (book p. 425; PDF p. 440); continued on [PPA §C.2, p. 426] (book p. 426; PDF p. 441)

### Corollary C.14 — Monotone rPostorder along cycle-free paths
- Statement: let G = (N, A) be a reducible graph with handle H. Any cycle-free path in G beginning with a
  node in the handle is monotonically increasing by the ordering rPostorder computed by Table C.1.
- Proof (summary): such a path has no dominator-back edges, so by Lemma C.12 it consists of forest paths
  joined by forward or cross edges; apply Corollary C.11.
- Citation: [PPA §C.2, p. 426] (book p. 426; PDF p. 441)

### [U0:C.2-e] Other orders (unnumbered remark)
- Statement: for the tree of Figure C.2, preorder is b₁, b₂, S₂, S₁, b₃, S₃ and breadth-first order is
  b₁, b₂, b₃, S₂, S₁, S₃. Like reverse postorder, both topologically sort the depth-first spanning forest
  and forward edges, but they do not necessarily topologically sort cross edges (for preorder, the edge
  b₃ → S₁; for breadth-first order, add a node between b₁ and b₃). This makes reverse postorder the
  better choice for a number of iterative algorithms.
- Citation: [PPA §C.2, p. 426] (book p. 426; PDF p. 441)

### Findings (C.2)
- F-U0-03: Table C.1 prints "choose a node h in H" without "unvisited"; read literally, calling DFS on
  an already visited h would reassign rPostorder[h] and decrement i again. The guard "while unvisited
  nodes in H exists" implies the unvisited choice. Recorded, not corrected. [PPA §C.2, p. 421] (book p. 421; PDF p. 436)

### Projections (C.2)
- cs_theory: depth-first numbering classifies edges; back edges cut every cycle (Corollary C.10);
  reverse postorder sorts all other edges; for reducible graphs back edges are exactly dominator-back
  edges and d(G) is traversal-independent. The bound of d(G) + 2 passes for round-robin iteration is
  external literature (Kam and Ullman [external]), not stated here.
- swe_architecture: visit nodes in reverse postorder in forward solvers; fix the successor order when
  reproducible results are needed, since the DFSF is not unique; a recursive DFS on deep graphs needs
  an explicit stack that still numbers nodes at last visit.
- practical_debugging: tests should assert invariants (Lemma C.9, Corollary C.11), not exact numberings;
  slow convergence calls for checking the visiting order and d(G); on irreducible graphs (Figure C.3
  pattern) iteration counts depend on the traversal.
- cyber: irreducible control flow arises from control-flow flattening [external] and hand-written jump
  tables in binaries; loop detection by dominator-back edges alone misses the loop of Figure C.3,
  whereas placing widening or cut points on all DFSF back edges cuts every cycle (Corollary C.10).

## C.3 Regular Expressions

### [U0:C.3-a] Alphabet; regular expression (unnumbered definition)
- Statement: an *alphabet* is a finite and non-empty set Σ of symbols, assumed disjoint from the set
  {Λ, ∅, (, ), +, ·, ∗} of special symbols. A *regular expression* over Σ is constructed inductively:
  (1) Λ and ∅ are (atomic) regular expressions, and each a ∈ Σ is an (atomic) regular expression;
  (2) if R₁ and R₂ are regular expressions then (R₁ + R₂), (R₁ · R₂) and (R₁)* are (compound) regular
  expressions. Precedence: ∗ binds more tightly than ·, and · more tightly than +, so most parentheses
  can be omitted.
- Citation: [PPA §C.3, p. 426] (book p. 426; PDF p. 441)

### [U0:C.3-b] Strings; languages; ℒ⟦R⟧; equivalence (unnumbered definition)
- Statement: a string w ∈ Σ* is a sequence of symbols from Σ; a language L over Σ is a set of strings,
  L ⊆ Σ*. ℒ⟦Λ⟧ = {Λ}; ℒ⟦∅⟧ = ∅; ℒ⟦a⟧ = {a} for all a ∈ Σ; ℒ⟦R₁ + R₂⟧ = ℒ⟦R₁⟧ ∪ ℒ⟦R₂⟧;
  ℒ⟦R₁ · R₂⟧ = ℒ⟦R₁⟧ · ℒ⟦R₂⟧; ℒ⟦R₁*⟧ = ⋃_{k=0}^{∞} (ℒ⟦R₁⟧)ᵏ, where L₁ · L₂ = {w₁w₂ | w₁ ∈ L₁ and w₂ ∈ L₂},
  L⁰ = {Λ} and L^{i+1} = Lⁱ · L. R₁ and R₂ are *equivalent*, written R₁ = R₂, if ℒ⟦R₁⟧ = ℒ⟦R₂⟧.
- Citation: [PPA §C.3, p. 427] (book p. 427; PDF p. 442)

### [U0:C.3-c] Homomorphism (unnumbered definition)
- Statement: a homomorphism from Σ₁* to Σ₂* is a function h : Σ₁ → Σ₂*, extended to words
  h(a₁⋯aₘ) = h(a₁)⋯h(aₘ) and to languages h(L) = {h(w) | w ∈ L}, and to regular expressions: h(∅) = ∅;
  h(Λ) = Λ; h(a) = b₁ · … · bₘ if h(a) = b₁⋯bₘ ∧ m > 0, and h(a) = Λ if h(a) = Λ; h(R₁ + R₂) = h(R₁) + h(R₂);
  h(R₁ · R₂) = h(R₁) · h(R₂); h(R*) = h(R)*. If R is a regular expression over Σ₁ then h(R) is a regular
  expression over Σ₂ and ℒ(h(R)) = h(ℒ(R)).
- Side conditions: h may map a symbol to Λ (erasure). The final identity writes ℒ with parentheses
  rather than ⟦·⟧.
- Citation: [PPA §C.3, p. 427] (book p. 427; PDF p. 442)

### Findings (C.3)
- F-U0-07: notation reuse inside this unit: Σ denotes an alphabet here and a state space elsewhere in
  the book; Λ is the empty string here; L is a lattice in Appendix A and a language here; "R₁ = R₂"
  overloads = for language equivalence; ℒ(h(R)) switches from ℒ⟦·⟧ to parentheses. Recorded, not
  corrected. [PPA §C.3, p. 427] (book p. 427; PDF p. 442)

### Projections (C.3)
- cs_theory: regular expressions with a compositional language semantics; regular languages are closed
  under homomorphism (ℒ(h(R)) = h(ℒ(R))); path expressions over flow graphs (algebraic path problem
  [external]) are not covered in this section.
- swe_architecture: a homomorphism is a projection that renames or erases events, e.g. reducing a trace
  alphabet to the events relevant to one resource.
- practical_debugging: an erasing homomorphism (h(a) = Λ) can make distinct traces identical; check
  that the erased symbols are irrelevant to the property under test.
- cyber: projecting a procedure's path expression onto alloc/free/use events of one pointer and
  intersecting with a bad-pattern expression flags double free or use after free [external] candidates.

## Concluding Remarks (Appendix C)

### Concluding Remarks (Appendix C) — summary
- Statement: there are a number of good books on graph theoretic concepts; the presentation is based on
  [48], Chapter 5 of [4], Chapters 3 and 4 of [69], Chapter 10 of [5] and Chapter 7 of [110]. For
  regular languages consult a text book such as [76].
- Side conditions: Appendix C has no Exercises section (finding F-U0-05). Book p. 428 is blank and
  absent from the PDF.
- Citation: [PPA Appendix C, p. 427] (book p. 427; PDF p. 442)

### Findings (all appendices)
- F-U0-05: none of Appendices A, B, C has an Exercises or Mini Projects section; each ends with a
  one-paragraph Concluding Remarks section. Exercises that use appendix material live in the chapters.
  [PPA Appendix A, p. 404] (book p. 404; PDF p. 420) [PPA Appendix B, p. 415] (book p. 415; PDF p. 431) [PPA Appendix C, p. 427] (book p. 427; PDF p. 442)

## Gotcha Ledger

- G-U0-01: Subsets of a partially ordered set need not have least upper bounds or greatest lower bounds; uniqueness holds only when they exist. [PPA §A.1, p. 393]
- G-U0-02: Bounds of the empty set are the extremes: ⨆∅ = ⊥ and ⨅∅ = ⊤. [PPA §A.1, p. 394]
- G-U0-03: Reversing the order swaps the operations: in (𝒫(S), ⊇) the join is ⋂, ⊥ = S and ⊤ = ∅. [PPA §A.1, p. 394]
- G-U0-04: A Moore family is never empty and always contains ⊤ = ⨅∅ of the enclosing lattice; {∅, {1}, {2}, {1,2}} is not a Moore family in (𝒫({1,2,3}), ⊆). [PPA §A.1, p. 395]
- G-U0-05: "Distributive" is only an alternative name for additive (binary joins); completely additive needs arbitrary joins and is equivalent to affine plus strict. [PPA §A.1, p. 395]
- G-U0-06: When L₂ is not a complete lattice, the function properties additionally require the relevant bounds to exist in L₂. [PPA §A.1, p. 396]
- G-U0-07: An affine powerset map with φ_∅ ≠ ∅ is not completely additive (Lemma A.5). [PPA §A.1, p. 396]
- G-U0-08: Lemma A.4 requires M finite and checks meet preservation only for incomparable pairs. [PPA §A.1, p. 396]
- G-U0-09: Height h means chains have at most h + 1 elements, not h. [PPA §A.3, p. 399]
- G-U0-10: The Ascending Chain Condition alone does not give finite height (Example A.7, Figure A.2 (a)); finite height needs both chain conditions (Lemma A.6). [PPA §A.3, p. 400]
- G-U0-11: The total function space S → L keeps the chain conditions only for finite S; the monotone function space L₁ → L₂ does not keep them in general. [PPA §A.3, p. 400]
- G-U0-12: For a complete lattice satisfying the Ascending Chain Condition and a total function f : L → L, additive and affine coincide (Lemma A.9); without ACC they need not coincide [derived]. [PPA §A.3, p. 401]
- G-U0-13: lfp(f) is defined as ⨅Fix(f); that it equals ⨅Red(f) and is a fixed point is the content of Proposition A.10, which assumes f monotone and says nothing about non-monotone f. [PPA §A.4, p. 402]
- G-U0-14: Iterating from ⊥ yields only a lower bound of lfp(f) in general; every inequality in the chain ⊥ ⊑ fⁿ(⊥) ⊑ ⋯ ⊑ fⁿ(⊤) ⊑ ⊤ can be strict; limit equality `⨆ₙ fⁿ(⊥) = lfp(f)` holds when f is continuous, and finite stabilisation `∃n : fⁿ(⊥) = fⁿ⁺¹(⊥) = lfp(f)` holds when L satisfies the Ascending Chain Condition (dually DCC for gfp). [PPA §A.4, p. 403]
- G-U0-15: Transfinite iteration f^{↑κ} reaches lfp(f) for a cardinal κ strictly greater than the cardinality of L, and its index is offset by one: f^{↑n} = fⁿ⁺¹(⊥). [PPA §A.4, p. 404]
- G-U0-16: Well-founded induction corresponds to the Descending Chain Condition, not the ascending one; B.1 phrases it with strict ≻ while A.3 phrases chains with ⊒ that eventually stabilise. [PPA §B.1, p. 407]
- G-U0-17: A coinductive proof assumes its conclusion; it is valid only with due care and the proper definition of the predicate as a greatest fixed point. [PPA §B.2, p. 409]
- G-U0-18: Induction fails for f₁, f₂, f₃: no base case for f₁ and f₃, no inductive step for f₂ and f₃. [PPA §B.2, p. 409]
- G-U0-19: Inductive and coinductive readings agree for 𝒬₀ but differ for 𝒬₁, 𝒬₂, 𝒬₃ (lfp(𝒬₃) = ⊥, gfp(𝒬₃) = ⊤); agreement is a property of the functional, not a default. [PPA §B.2, p. 410]
- G-U0-20: The book states lfp and gfp only for 𝒬₀ and 𝒬₃; for 𝒬₁ and 𝒬₂ it says only that similar arguments can be given. [PPA §B.2, p. 410]
- G-U0-21: The functional 𝒬 must be monotone; a clause such as Q(Con₁(d)) iff ¬Q(d) is not acceptable. [PPA §B.3, p. 411]
- G-U0-22: When each rule only has a finite number of calls to Q (making 𝒬 continuous), the rule notation (B.5) is equivalent to `Q = lfp(𝒬)` (B.4). [PPA §B.3, p. 411]
- G-U0-23: A proof by coinduction needs a Q′ that both contains the goal (Q′(d)) and is closed under one step (∀d′ : Q′(d′) ⇒ 𝒬(Q′)(d′)); checking only the goal proves nothing. [PPA §B.3, p. 412]
- G-U0-24: Proofs about a coinductively defined set can still need induction: Example B.2 excludes strings containing 2 by induction on the position of the first 2. [PPA §B.3, p. 414]
- G-U0-25: Adding S → S leaves the inductive reading {0,1}⁺ unchanged but makes the coinductive reading all of {0,1,2}^∞, including the empty string and strings with 2. [PPA §B.3, p. 415]
- G-U0-26: Graphs have a finite node set and an edge set A ⊆ N × N, so there are no parallel edges. [PPA §C.1, p. 417]
- G-U0-27: Paths may be trivial ([n₀], length 0) but cycles may not (m ≥ 1); a self-loop [n₀, n₀] is a cycle. [PPA §C.1, p. 418]
- G-U0-28: A multiple-entry cycle needs two distinct nodes entered from outside the cycle, not merely two distinct indices. [PPA §C.1, p. 418]
- G-U0-29: The reduced graph has edges only between distinct strongly connected components, so it has no self-loops. [PPA §C.1, p. 419]
- G-U0-30: Handles, dominators and DFSF numbering are relative to a handle (a set of entry nodes), not necessarily a single root. [PPA §C.1, p. 419]
- G-U0-31: Ancestor and descendant are reflexive; "proper" excludes equality. [PPA §C.1, p. 420]
- G-U0-32: Dom is the greatest solution of its equation, not the least. [PPA §C.1, p. 421]
- G-U0-33: The claim that an element is its own only dominator holds for elements of a minimal handle. [PPA §C.1, p. 421]
- G-U0-34: Table C.1 requires H to be a handle; i counts down from k, so a node finished earlier gets a higher number. [PPA §C.2, p. 421]
- G-U0-35: The DFSF and its rPostorder are not unique; the edge classification depends on the forest chosen. [PPA §C.2, p. 422]
- G-U0-36: Back edges include self-loops. [PPA §C.2, p. 422]
- G-U0-37: The cross-edge count of Example C.8 applies only to a conditional that is not the last statement of S or of a while body; forward edges never arise in WHILE but do with a one-branch conditional. [PPA §C.2, p. 423]
- G-U0-38: Back edge iff rPostorder[source] ≥ rPostorder[target]; the inequality is not strict, because of self-loops. [PPA §C.2, p. 423]
- G-U0-39: Reducible has many definitions in the literature; the one used here needs (N, A \ A_db) to be acyclic and to still have H as handle. [PPA §C.2, p. 424]
- G-U0-40: For reducible graphs, back edges and dominator-back edges coincide (Lemma C.12); in Figure C.3 (not reducible) there are back edges but no dominator-back edges, and d(G, T) may depend on T in general. [PPA §C.2, p. 425]
- G-U0-41: Corollary C.14 proves monotone increase of rPostorder along cycle-free paths starting in the handle under the hypothesis that G is reducible. [PPA §C.2, p. 426]
- G-U0-42: d(G) equals the maximum nesting of while loops for uniquely labelled WHILE flow graphs (Example C.13), not for arbitrary graphs; [derived] sibling loops do not add up (Figure C.1 has two loops and d(G) = 1). [PPA Example C.13, p. 425]
- G-U0-43: Preorder and breadth-first order do not necessarily topologically sort cross edges. [PPA §C.2, p. 426]
- G-U0-44: The alphabet must be disjoint from the special symbols {Λ, ∅, (, ), +, ·, ∗}. [PPA §C.3, p. 426]
- G-U0-45: A homomorphism may erase symbols (h(a) = Λ). [PPA §C.3, p. 427]
