<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-008: Shared Unit 0 L1 reference, hosted with the router skill and linked from it. -->

# Appendix B Reference: Induction and Coinduction

Scope: Appendix B, sections B.1 to B.3 and the Concluding Remarks [PPA Appendix B, p. 405] (book p. 405; PDF p. 421).
Every item carries a canonical citation such as `[PPA §B.1, p. 405] (book p. 405; PDF p. 421)`. Numbered
items keep the book's numbering; unnumbered items carry `[U0:<section>-<letter>]` ids. Terms tagged
`[external]` are not the book's terminology; `[derived]` marks consequences justified directly from printed
definitions. Book p. 416 is a blank page absent from the PDF and is never cited.

Proofs are not reproduced here. They live in the L3 shard corpus/shards/RAW_SHARD_00_appendices.md
(Appendix B anchors).

Closed inventory of numbered items in Appendix B: Example B.1, Example B.2; numbered displays (B.1) to (B.5).
Example B.2 is the last numbered item; there is no lemma, no figure and no Exercises section
[PPA Appendix B Concluding Remarks, p. 415] (book p. 415; PDF p. 431).

Dependency: Appendix B relies on Tarski's Fixed Point Theorem, Proposition A.10
[PPA §A.4, p. 402] (book p. 402; PDF p. 418): for monotone `f` on a complete lattice,
`lfp(f) = ⨅Red(f)` and `gfp(f) = ⨆Ext(f)`. See the Appendix A reference for its side conditions.

Notation: the book writes the defined predicate in sans-serif (rendered here as `Q`), candidate predicates
in italic (`Q′`), and functionals in calligraphic type (`𝒬`, `𝒬ᵢ`, `ℛ`).

---

## 1. Proof by induction (B.1)

### Induction principles

| Id | Principle | Domain | Premises | Conclusion | Citation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [U0:B.1-a] | mathematical induction | `ℕ` | `Q(0)`; `∀n : Q(n) ⇒ Q(n+1)` | `∀n : Q(n)` | [PPA §B.1, p. 405] (book p. 405; PDF p. 421) |
| [U0:B.1-c] | structural induction | `D` (below) | `Q(Base)`; `∀d : Q(d) ⇒ Q(Con₁(d))`; `∀d₁, d₂ : Q(d₁) ∧ Q(d₂) ⇒ Q(Con₂(d₁, d₂))` | `∀d : Q(d)` | [PPA §B.1, p. 406] (book p. 406; PDF p. 422) |
| [U0:B.1-e] | induction on the shape of inference trees | evaluation trees `d →^▽ n` | one obligation per rule (below) | `∀(d →^▽ n) : Q(d →^▽ n)` | [PPA §B.1, p. 406] (book p. 406; PDF p. 422) |
| [U0:B.1-f] | course of values induction | `ℕ` | `∀n : (∀m < n : Q(m)) ⇒ Q(n)` | `∀n : Q(n)` | [PPA §B.1, p. 407] (book p. 407; PDF p. 423) |
| [U0:B.1-g] | well-founded induction | well-founded `(D, ⪯)` | `∀d : (∀d′ ≺ d : Q(d′)) ⇒ Q(d)` | `∀d : Q(d)` | [PPA §B.1, p. 407] (book p. 407; PDF p. 423) |

Mathematical induction is justified because every natural number is either 0 or the successor `n+1` of
another [PPA §B.1, p. 405] (book p. 405; PDF p. 421). In course of values induction the base case is
handled like the induction step [PPA §B.1, p. 407] (book p. 407; PDF p. 423).

### [U0:B.1-b] Algebraic data type D and its size
[PPA §B.1, p. 405] (book p. 405; PDF p. 421); continued [PPA §B.1, p. 406] (book p. 406; PDF p. 422)

`d ∈ D`, `d ::= Base | Con₁(d) | Con₂(d, d)`: one base case, one unary and one binary constructor.

`size(Base) = 0`; `size(Con₁(d)) = 1 + size(d)`; `size(Con₂(d₁, d₂)) = 1 + size(d₁) + size(d₂)`.

`Q(d)` for all `d` can be proved by mathematical induction on `size(d)`; structural induction
[U0:B.1-c] proves it directly.

### [U0:B.1-d] Natural Semantics for D
[PPA §B.1, p. 406] (book p. 406; PDF p. 422)

Reading `Base` as 0, `Con₁(d)` as `d + 1` and `Con₂(d₁, d₂)` as `d₁ + d₂`:

| Rule | Premises | Conclusion |
| :--- | :--- | :--- |
| `[base]` | none | `Base → 0` |
| `[con₁]` | `d → n` | `Con₁(d) → n + 1` |
| `[con₂]` | `d₁ → n₁`, `d₂ → n₂` | `Con₂(d₁, d₂) → n₁ + n₂` |

An evaluation (inference) tree with conclusion `d → n` is written `d →^▽ n`.

### [U0:B.1-e] Obligations of induction on the shape of inference trees
[PPA §B.1, p. 406] (book p. 406; PDF p. 422); continued [PPA §B.1, p. 407] (book p. 407; PDF p. 423)

Writing `[premises / conclusion]` for the tree built by a rule:

1. `Q(Base → 0)`;
2. `∀(d →^▽ n) : Q(d →^▽ n) ⇒ Q([d →^▽ n / Con₁(d) → n + 1])`;
3. `∀(d₁ →^▽ n₁), (d₂ →^▽ n₂) : Q(d₁ →^▽ n₁) ∧ Q(d₂ →^▽ n₂) ⇒ Q([d₁ →^▽ n₁   d₂ →^▽ n₂ / Con₂(d₁, d₂) → n₁ + n₂])`.

Conclusion: `∀(d →^▽ n) : Q(d →^▽ n)`.

### [U0:B.1-g] Well-founded ordering
[PPA §B.1, p. 407] (book p. 407; PDF p. 423)

For a partially ordered set `(D, ⪯)`, `⪯` is well-founded iff there is **no infinite decreasing sequence**
`d₁ ≻ d₂ ≻ d₃ ≻ ⋯`, where `d ≻ d′` means `d′ ⪯ d ∧ d ≠ d′` (G-U0-18, G-U0-19). The book says this "amounts to"
the Descending Chain Condition of Appendix A: Appendix A phrases DCC as eventual stabilisation of weakly
descending sequences `n ≤ m ⇒ lₙ ⊒ lₘ` [PPA §A.3, p. 399] (book p. 399; PDF p. 415), whereas Appendix B
phrases well-foundedness via strict decrease `≻` (equivalent on any poset `[derived]`). Course of values
induction is well-founded induction on `(ℕ, ≤)`. Its correctness proof follows the proof of (A.3) in Lemma A.6.

---

## 2. Introducing coinduction (B.2)

### [U0:B.2-a] Motivating program and predicate
[PPA §B.2, p. 407] (book p. 407; PDF p. 423); continued [PPA §B.2, p. 408] (book p. 408; PDF p. 424)

Program: `if f(27, m) then "something good" else "something bad"`, with `f : ℕ × ℕ → {true, false}` and
`m` unknown. Predicate: `Q_f(n)` iff `∀m : f(n, m) ≠ false` (for `m, n ≥ 0`). The axiom `Q_f(0)` and the rule
`Q_f(n) / Q_f(n+1)` give an inductive definition of `Q_f`.

### [U0:B.2-b] The four functions
[PPA §B.2, p. 408] (book p. 408; PDF p. 424); continued [PPA §B.2, p. 409] (book p. 409; PDF p. 425)

| Function | Clause for `0` | Clause for `n+1` | Induction lacks | `fᵢ(27, m)` |
| :--- | :--- | :--- | :--- | :--- |
| `f₀` | `f₀(0, m) = true` | `f₀(n+1, m) = f₀(n, m)` | nothing | terminates (`true`) |
| `f₁` | `f₁(0, m) = f₁(0, m)` | `f₁(n+1, m) = f₁(n, m)` | base case | never terminates |
| `f₂` | `f₂(0, m) = true` | `f₂(n+1, m) = f₂(n+1, m)` | inductive step | never terminates |
| `f₃` | `f₃(0, m) = f₃(0, m)` | `f₃(n+1, m) = f₃(n+1, m)` | base case and inductive step | never terminates |

Assuming `Qᵢ` for the right-hand-side occurrences in order to derive it for the left-hand side is a valid
**coinductive** proof, given the proper definition of `Qᵢ` [PPA §B.2, p. 409] (book p. 409; PDF p. 425).

### Displays (B.1) to (B.3): obtaining a functional
[PPA §B.2, p. 409] (book p. 409; PDF p. 425)

- (B.1) `Q₀(0)` iff `true`, `Q₀(n+1)` iff `Q₀(n)`; `Q₁(0)` iff `Q₁(0)`, `Q₁(n+1)` iff `Q₁(n)`;
  `Q₂(0)` iff `true`, `Q₂(n+1)` iff `Q₂(n+1)`; `Q₃(0)` iff `Q₃(0)`, `Q₃(n+1)` iff `Q₃(n+1)`.
- (B.2) `Qᵢ = 𝒬ᵢ(Qᵢ)`.
- (B.3) `𝒬₀(Q′)(0) = true`, `𝒬₀(Q′)(n+1) = Q′(n)`; `𝒬₁(Q′)(0) = Q′(0)`, `𝒬₁(Q′)(n+1) = Q′(n)`;
  `𝒬₂(Q′)(0) = true`, `𝒬₂(Q′)(n+1) = Q′(n+1)`; `𝒬₃(Q′)(0) = Q′(0)`, `𝒬₃(Q′)(n+1) = Q′(n+1)`.

Lattice: `(ℕ → {true, false}, ⊑)` with italic meta-variables `Q₁ ⊑ Q₂` iff `∀n : Q₁(n) ⇒ Q₂(n)` (distinct
from the sans-serif defined predicates `Q₀..Q₃` of (B.1)–(B.2); BKL-024, G-U0-20); `⊥ = λn.false`, `⊤ = λn.true`.
Each `𝒬ᵢ` is monotone, so by Proposition A.10 each has `lfp(𝒬ᵢ)` and `gfp(𝒬ᵢ)`, possibly different
predicates. A functional is a function whose argument and result are themselves functions (or structures
containing functions).

### [U0:B.2-c] and [U0:B.2-d] Least and greatest fixed points of the 𝒬ᵢ
[PPA §B.2, p. 410] (book p. 410; PDF p. 426)

| Functional | Stated by the book | Consequence for `Qᵢ(27)` |
| :--- | :--- | :--- |
| `𝒬₀` | `⨆ₖ 𝒬₀ᵏ(⊥) ⊑ lfp(𝒬₀)`; since the clauses use finitely many (zero or one) `Q`'s, a continuity property gives `⨆ₖ 𝒬₀ᵏ(⊥) = lfp(𝒬₀)`; `𝒬₀ᵏ(⊥)(n)` holds iff at most `k` axioms and rules suffice to prove `Q₀(n)`; `lfp(𝒬₀) = gfp(𝒬₀)` | `lfp(𝒬₀)(27) = true` and `gfp(𝒬₀)(27) = true` |
| `𝒬₃` | `lfp(𝒬₃) = ⊥` because `𝒬₃(⊥) = ⊥`; `gfp(𝒬₃) = ⊤` because `𝒬₃(⊤) = ⊤` | `lfp(𝒬₃)(27) = false`, so induction cannot establish `Q₃(27)`; `gfp(𝒬₃)(27) = true` |
| `𝒬₁`, `𝒬₂` | "somewhat similar arguments" to `𝒬₃`, for both the `lfp` and the `gfp` claims | the book gives no separate formulas |

Reading stated by the book: a proof by induction "corresponds" to taking the least fixed point. The equality
`lfp(𝒬₀) = gfp(𝒬₀)` is proved by mathematical induction on `n`; it does not hold for `𝒬₁`, `𝒬₂`, `𝒬₃`.

### [U0:B.2-e] Remark: Banach's Fixed Point Theorem
[PPA §B.2, p. 410] (book p. 410; PDF p. 426)

`lfp(𝒬₀) = gfp(𝒬₀)` is related to Banach's Fixed Point Theorem: a contractive operator on a complete metric
space has a unique fixed point. `𝒬₀` is contractive (as opposed to `𝒬₁`, `𝒬₂`, `𝒬₃`) because the clause for
`𝒬₀(Q)(n)` only calls `Q` on arguments **smaller than `n`** (BKL-015, G-U0-21).

---

## 3. Proof by coinduction (B.3)

### [U0:B.3-a] Clause-defined predicate and its functional
[PPA §B.3, p. 411] (book p. 411; PDF p. 427)

For sans-serif `Q : D → {true, false}` over bold domain sort `D` (BKL-024; duplicated words on p. 411 noted in BKL-020), defined by clauses `Q(Base)` iff `⋯`;
`Q(Con₁(d))` iff `⋯Q(d′)⋯`; `Q(Con₂(d₁, d₂))` iff `⋯Q(d₁′)⋯Q(d₂′)⋯`, define the functional `𝒬` by cases:
`𝒬(Q′)(Base) = ⋯`; `𝒬(Q′)(Con₁(d)) = ⋯Q′(d′)⋯`; `𝒬(Q′)(Con₂(d₁, d₂)) = ⋯Q′(d₁′)⋯Q′(d₂′)⋯`.

- `(D → {true, false}, ⊑)` is a complete lattice with `Q₁ ⊑ Q₂` iff `∀d : Q₁(d) ⇒ Q₂(d)`.
- **Assumption: `𝒬` is monotone.** A clause such as "`Q(Con₁(d))` iff `¬Q(d)`" is therefore not acceptable.
- From Proposition A.10, `𝒬` has a least and a greatest fixed point.

### [U0:B.3-b] Inductive definition, displays (B.4) and (B.5)
[PPA §B.3, p. 411] (book p. 411; PDF p. 427); continued [PPA §B.3, p. 412] (book p. 412; PDF p. 428)

- (B.4) `Q = lfp(𝒬)`.
- (B.5) the same definition written as axioms and rules:
  `⋯ / Q(Base)`; `⋯Q(d′)⋯ / Q(Con₁(d))`; `⋯Q(d₁′)⋯Q(d₂′)⋯ / Q(Con₂(d₁, d₂))`.
- Equivalence condition: **when each rule has only a finite number of calls to `Q`**, (B.4) and (B.5) are
  equivalent: the predicate in (B.5) amounts to `⨆ₖ 𝒬ᵏ(⊥)`, which by a continuity property agrees with (B.4).
- A proof by induction amounts to establishing the validity of the axioms and rules in (B.5).

### [U0:B.3-c] Coinductive definition and the coinduction proof rule
[PPA §B.3, p. 412] (book p. 412; PDF p. 428)

Coinductive definition: `Q = gfp(𝒬)`. Proof rule, following from `gfp(𝒬) = ⨆Ext(𝒬)` in Proposition A.10:

`Q′ ⊑ 𝒬(Q′)  /  Q′ ⊑ Q`   (i.e. `Q′ ⊑ 𝒬(Q′)  /  Q′ ⊑ gfp(𝒬)`).

To prove `Q(d)`: find some `Q′` such that `Q′(d)` and `∀d′ : Q′(d′) ⇒ 𝒬(Q′)(d′)`.

### [U0:B.3-d] Derived coinduction rule
[PPA §B.3, p. 412] (book p. 412; PDF p. 428)

`Q′ ⊑ 𝒬(Q ⊔ Q′)  /  Q′ ⊑ Q`, valid for `Q = gfp(𝒬)` with `𝒬` monotone. It sometimes saves work because `Q`
itself may be used in the premise. The book notes that the explanation generalises to algebraic data
types with additional base cases and constructors, and from predicates to relations. The name
coinduction up-to `[external]` is not used by the book.

### Induction versus coinduction

| Aspect | Induction (least fixed point) | Coinduction (greatest fixed point) |
| :--- | :--- | :--- |
| Definition | `Q = lfp(𝒬)` (B.4), usually written as rules (B.5) | `Q = gfp(𝒬)` |
| Hypotheses | `𝒬` monotone on `(D → {true, false}, ⊑)` | same |
| Characterisation (Proposition A.10) | `lfp(𝒬) = ⨅Red(𝒬)` | `gfp(𝒬) = ⨆Ext(𝒬)` |
| Proof obligation stated by the book | validity of the axioms and rules in (B.5) | find `Q′` with `Q′(d)` and `Q′ ⊑ 𝒬(Q′)`; or the derived form `Q′ ⊑ 𝒬(Q ⊔ Q′)` |
| Rule-form agreement | (B.5) = (B.4) when each rule has finitely many calls to `Q` (continuity) | no finiteness condition is stated |
| Flavour (book's words) | very constructive: take nothing for granted, only believe what can be demonstrated | very optimistic: assume everything as long as no fact is demonstrably violated |
| Typical use (book's words) | semantics, which should not allow spurious behaviour not forced by the semantics | checking that a specification holds, since it should not forbid behaviour unless explicitly called for |
| Running example `𝒬₃` | `lfp(𝒬₃) = ⊥` | `gfp(𝒬₃) = ⊤` |
| Grammar of Example B.2 | finite strings only | admits infinite strings |

Sources: [PPA §B.3, p. 411] (book p. 411; PDF p. 427) and [PPA §B.3, p. 412] (book p. 412; PDF p. 428).
The dual induction rule `𝒬(Q′) ⊑ Q′ / lfp(𝒬) ⊑ Q′` follows from `lfp(𝒬) = ⨅Red(𝒬)`. Appendix B does
**not** state it; it states induction as rule validity for (B.5).

### Example B.1 (coinduction for mutually defined relations)
[PPA §B.3, p. 413] (book p. 413; PDF p. 429)

- Relations `R₁ : D₁₁ × D₁₂ → {true, false}`, `R₂ : D₂₁ × D₂₂ → {true, false}`, defined by
  `R₁ = ℛ₁(R₁, R₂)` and `R₂ = ℛ₂(R₁, R₂)`, intended as `(R₁, R₂) = gfp(ℛ)` where
  `ℛ(R₁′, R₂′) = (ℛ₁(R₁′, R₂′), ℛ₂(R₁′, R₂′))` **is assumed to be monotone**.
- `d₁ (R′ ⊔ R″) d₂` iff `(d₁ R′ d₂) ∨ (d₁ R″ d₂)`; `R′ ⊑ R″` iff `∀d₁, d₂ : d₁ R′ d₂ ⇒ d₁ R″ d₂`.
- Principle: from `R₁′ ⊑ ℛ₁(R₁′, R₂′)` and `R₂′ ⊑ ℛ₂(R₁′, R₂′)` conclude `R₁′ ⊑ R₁` and `R₂′ ⊑ R₂`.
- Work-saving form: from `R₁′ ⊑ ℛ₁(R₁ ⊔ R₁′, R₂ ⊔ R₂′)` and `R₂′ ⊑ ℛ₂(R₁ ⊔ R₁′, R₂ ⊔ R₂′)` conclude the same,
  because `Rᵢ ⊑ ℛᵢ(R₁, R₂) ⊑ ℛᵢ(R₁ ⊔ R₁′, R₂ ⊔ R₂′)`, using the definition `(R₁, R₂) = gfp(ℛ)`.

### Example B.2 (inductive and coinductive readings of one grammar)
[PPA §B.3, p. 414] (book p. 414; PDF p. 430); continued [PPA §B.3, p. 415] (book p. 415; PDF p. 431)

Universe `{0,1,2}^∞ = {0,1,2}* ∪ {0,1,2}^ω` (finite and infinite strings). Concatenation: finite with finite
gives length `n + m`; finite `(aᵢ)ᵢ₌₁ⁿ` with infinite gives `cₖ = aₖ` for `k ≤ n` and `cₖ = b_{k−n}` for
`k > n`; an infinite left operand absorbs the right operand (`cₖ = aₖ`). Grammar `S → 0 | 1 | 0S | 1S`, as
the rules `0 ∈ S`; `1 ∈ S`; `x ∈ S / 0x ∈ S`; `x ∈ S / 1x ∈ S`.

| Rule set | Inductive reading | Coinductive reading |
| :--- | :--- | :--- |
| `S → 0 \| 1 \| 0S \| 1S` | `S = {0,1}⁺` | `S = {0,1}⁺ ∪ {0,1}^ω` |
| plus `S → S` (rule `x ∈ S / x ∈ S`) | still `{0,1}⁺` | all of `{0,1,2}^∞`, including the empty string and strings containing 2 |

Stated reasons: the coinductive reading excludes the empty string (it is none of `0`, `1`, `0x`, `1x`) and
excludes strings containing 2 (by induction on the position of the first 2), but cannot exclude infinite
0/1 strings (each has the form `0x` or `1x` with `x ∈ {0,1}^ω`). With `S → S`, every `x` can be written
`x = x`, so nothing can be excluded [PPA §B.3, p. 415] (book p. 415; PDF p. 431).

---

## 4. Side conditions that are easy to drop (SMOOTHING_TRAP checklist)

| Statement as often smoothed | Condition the book states | Citation |
| :--- | :--- | :--- |
| "every clause-defined predicate has lfp and gfp" | requires monotone `𝒬` (Proposition A.10 sufficient hypothesis; BKL-014); negated recursive calls like `¬Q(d)` break monotonicity (G-U0-22) | [PPA §B.3, p. 411] (book p. 411; PDF p. 427) |
| "rules (B.5) define `lfp(𝒬)`" | holds when each rule has a finite number of calls to `Q` (sufficient for continuity `⨆ₖ 𝒬ᵏ(⊥) = lfp(𝒬)`; G-U0-22) | [PPA §B.3, p. 411] (book p. 411; PDF p. 427) |
| "coinduction: show `Q′` is preserved" | the rule concludes `Q′ ⊑ gfp(𝒬)` (`Q′ ∈ Ext(𝒬)`) from `Q′ ⊑ 𝒬(Q′)`, and `Q(d)` also needs `Q′(d)` (G-U0-23) | [PPA §B.3, p. 412] (book p. 412; PDF p. 428) |
| "lfp and gfp coincide" | shown for `𝒬₀` (calls on strictly smaller `n` in well-founded `ℕ`); fails on non-decreasing `𝒬₁..𝒬₃` (BKL-015, G-U0-20, G-U0-21) | [PPA §B.2, p. 410] (book p. 410; PDF p. 426) |
| "`⨆ₖ 𝒬ᵏ(⊥)` is the lfp" | in general only `⊑ lfp`; equality uses finitely many calls per clause (G-U0-20) | [PPA §B.2, p. 410] (book p. 410; PDF p. 426) |
| "adding a trivial rule changes nothing" | true inductively; coinductively `S → S` makes `S` the whole universe (BKL-015, G-U0-25) | [PPA §B.3, p. 415] (book p. 415; PDF p. 431) |
| "gfp-defined sets need no induction" | Example B.2 excludes strings with a 2 by induction on the position of the first 2 (BKL-015, G-U0-25) | [PPA §B.3, p. 414] (book p. 414; PDF p. 430) |
| "well-founded = DCC, identical wording" | Appendix B forbids infinite strict-decrease sequences `d₁ ≻ d₂ ≻ ⋯` (`d′ ⪯ d ∧ d ≠ d′`), whereas A.3 states weak-chain stabilisation (G-U0-18, G-U0-19) | [PPA §B.1, p. 407] (book p. 407; PDF p. 423) |
| "Example B.1 needs no assumption" | `ℛ` is assumed to be monotone (G-U0-24) | [PPA §B.3, p. 413] (book p. 413; PDF p. 429) |

---

## 5. Item index (Appendix B)

| Id | Item | Citation |
| :--- | :--- | :--- |
| [U0:B.1-a] | mathematical induction | [PPA §B.1, p. 405] (book p. 405; PDF p. 421) |
| [U0:B.1-b] | data type `D`, `size` | [PPA §B.1, p. 405] (book p. 405; PDF p. 421) |
| [U0:B.1-c] | structural induction | [PPA §B.1, p. 406] (book p. 406; PDF p. 422) |
| [U0:B.1-d] | Natural Semantics `d → n`, trees `d →^▽ n` | [PPA §B.1, p. 406] (book p. 406; PDF p. 422) |
| [U0:B.1-e] | induction on the shape of inference trees | [PPA §B.1, p. 406] (book p. 406; PDF p. 422) |
| [U0:B.1-f] | course of values induction | [PPA §B.1, p. 407] (book p. 407; PDF p. 423) |
| [U0:B.1-g] | well-founded ordering and induction | [PPA §B.1, p. 407] (book p. 407; PDF p. 423) |
| [U0:B.2-a] | motivating program, `Q_f` | [PPA §B.2, p. 407] (book p. 407; PDF p. 423) |
| [U0:B.2-b] | functions `f₀` to `f₃` | [PPA §B.2, p. 408] (book p. 408; PDF p. 424) |
| (B.1) to (B.3) | predicates `Qᵢ`, functionals `𝒬ᵢ` | [PPA §B.2, p. 409] (book p. 409; PDF p. 425) |
| [U0:B.2-c], [U0:B.2-d] | least and greatest fixed points of `𝒬ᵢ` | [PPA §B.2, p. 410] (book p. 410; PDF p. 426) |
| [U0:B.2-e] | Banach remark | [PPA §B.2, p. 410] (book p. 410; PDF p. 426) |
| [U0:B.3-a] | clause-defined predicate, monotone `𝒬` | [PPA §B.3, p. 411] (book p. 411; PDF p. 427) |
| [U0:B.3-b], (B.4), (B.5) | inductive definition | [PPA §B.3, p. 411] (book p. 411; PDF p. 427) |
| [U0:B.3-c] | coinductive definition, proof rule | [PPA §B.3, p. 412] (book p. 412; PDF p. 428) |
| [U0:B.3-d] | derived coinduction rule | [PPA §B.3, p. 412] (book p. 412; PDF p. 428) |
| Example B.1 | mutually defined relations | [PPA §B.3, p. 413] (book p. 413; PDF p. 429) |
| Example B.2 | grammar, inductive versus coinductive | [PPA §B.3, p. 414] (book p. 414; PDF p. 430) |
| Concluding Remarks | further reading: [16]; strong bisimulation in CCS, Chapter 4 of [106] | [PPA Appendix B Concluding Remarks, p. 415] (book p. 415; PDF p. 431) |
