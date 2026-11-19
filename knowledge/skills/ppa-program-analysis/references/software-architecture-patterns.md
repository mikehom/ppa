<!-- @governing: REQ-TECH-PPA-001, REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-001, REQ-PRD-PPA-006 -->
<!-- @decision DEC-PPA-011: Router-hosted L1 software architecture and design-pattern bridge mapping static analyser engineering patterns to PPA formal objects. -->

# Software Architecture Patterns for Static Analysers: A Bridge to PPA Formal Objects

This reference maps the engineering vocabulary used to build static analysers onto the formal objects of
*Principles of Program Analysis*. The book defines no software design patterns: every pattern name, data structure
and implementation technique below is tagged `[external]`, and every pairing of a pattern with a formal object is
an interpretation, not a book result. The formal object on the other side of each pairing is book-native and cited.
When a pattern and a formal contract disagree, the formal contract wins.

## 1. Reading Rules

- **Tagging**: `[external: X]` marks a software engineering term absent from the book; `[derived]` marks a
  consequence argued here rather than stated in the book; untagged formal objects carry a book citation.
- **Direction**: each section states the formal contract first, then the pattern that implements it. A pattern
  that is convenient but breaks the contract is listed under Section 10.
- **Depth**: full definitions, side conditions and errata live in the sibling references listed in Section 11.

## 2. Abstract Domain Interface and the Complete Lattice

An `[external: abstract domain interface]` (`bottom`, `leq`, `join`, `widen`, `narrow`) is the code-level face of
a property space. The book requires a complete lattice `(L, ⊑, ⨆, ⨅, ⊥, ⊤)` in which every subset has a least
upper bound and a greatest lower bound [PPA §A.1, p. 393] (book p. 393; PDF p. 409), and a Monotone Framework
`(L, 𝓕)` whose `L` satisfies the Ascending Chain Condition and whose `𝓕` is a set of monotone functions containing
`id` and closed under composition [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87)
[PPA §2.3.1, p. 69] (book p. 69; PDF p. 88).

| Interface operation `[external]` | PPA formal object | Contract the implementation must honour |
| :--- | :--- | :--- |
| `bottom()` | `⊥ = ⨆∅`, least element [PPA §A.1, p. 394] (book p. 394; PDF p. 410) | Starting value of every flow variable; not the extremal value `ι`, which obeys no universal rule [PPA §2.3.2, p. 70] (book p. 70; PDF p. 89) |
| `leq(a, b)` | Partial order `⊑` [PPA §A.1, p. 393] (book p. 393; PDF p. 409) | Reflexive, transitive, anti-symmetric; read as "at least as precise as" |
| `join(a, b)` | Least upper bound `⊔` [PPA §A.1, p. 393] (book p. 393; PDF p. 409) | Must be the least upper bound, not merely an upper bound, or precision is lost at every merge |
| `height()` / ACC flag | Ascending Chain Condition [PPA §A.3, p. 399] (book p. 399; PDF p. 415) | Decides whether plain `⊔` iteration stabilises or a widening is mandatory |
| `widen(old, new)` | Widening `∇` [PPA §4.2.1, p. 226] (book p. 226; PDF p. 243) | Upper bound operator forcing ascending chains to stabilise; need not be monotone |
| `narrow(old, new)` | Narrowing `Δ` [PPA §4.2.2, p. 230] (book p. 230; PDF p. 247) | Refines a widened result downwards while staying above the least fixed point |

- **Fixed-point target**: for monotone `f` on a complete lattice, `lfp(f) = ⨅Red(f)` exists and is a fixed point
  (`Proposition A.10`, Tarski) [PPA Proposition A.10, p. 402] (book p. 402; PDF p. 418).
- **Widened iteration**: `Proposition 4.13` stabilises at `lfp_∇(f)`, and `Fact 4.14` places it above `lfp(f)`
  [PPA Proposition 4.13, p. 227] (book p. 227; PDF p. 244) [PPA Fact 4.14, p. 227] (book p. 227; PDF p. 244).
  The guard `f(x) ⊑ x` and the operand order `old ∇ new` belong inside the interface, not in each caller `[derived]`.

## 3. Transfer Functions as `[external: Strategy]` and `[external: Visitor]`

- **Flow graph construction as a `[external: Visitor]`**: `init`, `final`, `blocks`, `labels` and `flow` are
  defined by structural recursion over the statements of a program, one clause per syntactic form
  [PPA §2.1, p. 35] (book p. 35; PDF p. 54) [PPA §2.1, p. 36] (book p. 36; PDF p. 55). A visitor over the
  `[external: AST]` that emits a `[external: CFG]` mirrors those clauses.
- **Transfer functions as a `[external: Strategy]`**: an instance `(L, 𝓕, F, E, ι, f_·)` maps each label to a
  transfer function in `𝓕` [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88). Supplying `f_·` as a pluggable strategy keeps
  the equation schema `Analysis∘(ℓ) = ⨆{Analysis•(ℓ') | (ℓ', ℓ) ∈ F} ⊔ ι^ℓ_E` fixed
  [PPA §2.3, p. 66] (book p. 66; PDF p. 85).
- **Constraint generation as a `[external: Visitor]`**: `𝒞_⋆⟦·⟧` is syntax-directed, one clause per expression
  form [PPA §3.4.1, p. 175] (book p. 175; PDF p. 193).
- **Derived transfer functions**: the induced operation `α_2 ∘ f_p ∘ γ_1` computes an abstract transfer function
  from a concrete one [PPA §4.5.1, p. 259] (book p. 259; PDF p. 276); a strategy factory can derive abstract
  transfer functions this way instead of writing them by hand `[derived]`.

## 4. Fixed-Point Engine as `[external: Template Method]`

`Table 6.1` fixes the solver skeleton (initialise, extract, evaluate, compare, join, re-insert dependants) and leaves
the worklist operations `empty`, `insert` and `extract` abstract [PPA §6.1.1, p. 368] (book p. 368; PDF p. 384)
[PPA Table 6.1, p. 369] (book p. 369; PDF p. 385). That is the shape of a `[external: Template Method]` whose hook is a
worklist `[external: Strategy]`.

| Worklist strategy `[external]` | Book realisation | Citation |
| :--- | :--- | :--- |
| `[external: LIFO stack]` / `[external: FIFO queue]` | `Table 6.2` (stack); queue variant in `§6.1.2` | [PPA Table 6.2, p. 373] (book p. 373; PDF p. 389) [PPA §6.1.2, p. 374] (book p. 374; PDF p. 390) |
| Reverse postorder with `(W.c, W.p)` | `Table 6.3` (`§6.2`) | [PPA Table 6.3, p. 376] (book p. 376; PDF p. 392) |
| Round Robin sweeps | `Table 6.4` (`§6.2.1`) | [PPA Table 6.4, p. 379] (book p. 379; PDF p. 395) |
| Strong components in topological order | `Tables 6.5–6.6` (`§6.3`) | [PPA Table 6.5, p. 382] (book p. 382; PDF p. 398) [PPA Table 6.6, p. 384] (book p. 384; PDF p. 400) |
| Chapter 2 and Chapter 3 precursors | `Table 2.8` (MFP worklist), `Table 3.7` (constraint graph) | [PPA Table 2.8, p. 75] (book p. 75; PDF p. 94) [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196) |

- **Dependency graph as `[external: Observer]`**: Step 1 of `Table 6.1` subscribes each constraint `x ⊒ t` to
  `infl[x']` for every `x' ∈ FV(t)`; a change to `Analysis[x]` notifies every subscriber by re-inserting it
  [PPA Table 6.1, p. 369] (book p. 369; PDF p. 385). `Table 3.7` keeps the same subscriber lists as `E[q]`
  [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196).
- **Hook correctness**: `Lemma 6.4` is proved for the abstract worklist operations, so `Table 6.1` terminates with
  `Analysis = μ_𝒮` whatever conforming strategy is plugged in [PPA Lemma 6.4, p. 370] (book p. 370; PDF p. 386);
  strategies differ in cost, bounded by `O(h · M² · N)` for the abstract algorithm
  [PPA §6.1.1, p. 372] (book p. 372; PDF p. 388).
- **Strategy-specific bounds stay scoped**: the Round Robin iteration bound of `Lemma 6.12` is stated for instances
  of a Bit Vector Framework only [PPA Lemma 6.12, p. 380] (book p. 380; PDF p. 396); a generic engine must not
  advertise it for arbitrary domains.

## 5. Galois Connection as `[external: Adapter]`

A Galois connection `(L, α, γ, M)` pairs monotone `α : L → M` and `γ : M → L` with `γ ∘ α ⊒ λl.l` and
`α ∘ γ ⊑ λm.m` [PPA §4.3, p. 234] (book p. 234; PDF p. 251). It adapts a concrete property space to an abstract one
in the role of an `[external: Adapter]`.

- **Soundness law as a `[external: property-based test]`**: `Proposition 4.20` shows that the two laws with
  monotone `α, γ` are equivalent to the adjunction `α(l) ⊑ m` exactly when `l ⊑ γ(m)`, for all `l` and `m`
  [PPA Proposition 4.20, p. 236] (book p. 236; PDF p. 253). Testing the adjunction directly also covers
  monotonicity, which the two laws alone do not imply.
- **One side determines the other**: by `Lemma 4.22` each adjoint determines the other, `α` is completely additive
  (so `α(⊥) = ⊥`) and `γ` is completely multiplicative (so `γ(⊤) = ⊤`)
  [PPA Lemma 4.22, p. 239] (book p. 239; PDF p. 256); by `Lemma 4.23` a completely additive `α` alone fixes `γ`
  [PPA Lemma 4.23, p. 239] (book p. 239; PDF p. 256). An adapter may implement one direction and derive the other.
- **Composing adapters**: correctness relations transport along `γ`, generated by `α ∘ β`
  [PPA §4.3.1, p. 241] (book p. 241; PDF p. 258); a Galois insertion additionally removes redundant abstract
  elements [PPA §4.3.2, p. 242] (book p. 242; PDF p. 259).

## 6. Product Domains as `[external: Composite]` Combinators

Section 4.4 builds new Galois connections from old ones. Each combinator is a `[external: Composite]` that takes
component adapters and returns an adapter, with its own precision trade-off.

| Combinator | Construction | Precision trade-off | Citation |
| :--- | :--- | :--- | :--- |
| Sequential composition | `(L_0, α_2 ∘ α_1, γ_1 ∘ γ_2, L_2)` | Order of `γ` reverses that of `α` | [PPA §4.4, p. 247] (book p. 247; PDF p. 264) |
| Independent attribute | Componentwise `α`, `γ` on `L_1 × L_2` | Loses correlations between components | [PPA §4.4.1, p. 249] (book p. 249; PDF p. 266) |
| Relational (`⊗` on powersets) | `𝒫(V_1 × V_2)` to `𝒫(D_1 × D_2)` | Keeps correlations at higher cost | [PPA §4.4.1, p. 251] (book p. 251; PDF p. 268) |
| Total function space | Pointwise `α ∘ f`, `γ ∘ g` | Lifts per-variable domains to states | [PPA §4.4.1, p. 252] (book p. 252; PDF p. 269) |
| Direct product | `α(l) = (α_1(l), α_2(l))`, `γ = γ_1 ⊓ γ_2` | Same concrete lattice; Galois insertion not preserved | [PPA §4.4.2, p. 254] (book p. 254; PDF p. 271) |
| Direct tensor product | Pairs per element `v` | Keeps more correlation; insertion still not preserved | [PPA §4.4.2, p. 255] (book p. 255; PDF p. 272) |
| Reduced product / reduced tensor product | Apply reduction `ς` | Restores a Galois insertion | [PPA §4.4.2, p. 256] (book p. 256; PDF p. 273) |

- **Composite invariant `[derived]`**: a combinator is correct when its output satisfies Section 5's adjunction law
  whenever its inputs do; test the composite, not only the leaves.
- **Reduction placement**: running a reduction after loop-head widening can re-introduce finite bounds and break
  termination `[derived]`; reduce before widening.

## 7. Type and Effect Systems as `[external: Decorator]` Layers

- **Base component**: the underlying type system `⊢_UL` of `Table 5.1`
  [PPA Table 5.1, p. 285] (book p. 285; PDF p. 302), with Hindley–Milner style inference
  [PPA Chapter 5 Concluding Remarks, p. 353] (book p. 353; PDF p. 370).
- **Decoration**: annotated types attach analysis information to arrows (`Table 5.2`)
  [PPA Table 5.2, p. 288] (book p. 288; PDF p. 305); later layers add side effects (`§5.4.1`), exceptions
  (`§5.4.2`), regions (`§5.4.3`) and communication behaviours (`§5.5`)
  [PPA §5.4, p. 319] (book p. 319; PDF p. 336) [PPA §5.5, p. 339] (book p. 339; PDF p. 356). This layering is the
  shape of a `[external: Decorator]` over the base type checker.
- **Decorator contract**: conservative extension (`Fact 5.6`) says erasing annotations maps every annotated
  typing to an underlying one, and every underlying typing has an annotated counterpart
  [PPA Fact 5.6, p. 291] (book p. 291; PDF p. 308). A decorating layer that rejects a well-typed program breaks it.
- **Layered inference**: `𝒲_UL` with `𝒰_UL` (`Tables 5.5–5.6`) is extended by `𝒲_CFA` with `𝒰_CFA`, which also
  collects annotation constraints (`Tables 5.7–5.8`)
  [PPA Table 5.5, p. 303] (book p. 303; PDF p. 320) [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327).

## 8. Decoupling Constraint Generation from Constraint Solving

- **Generation**: `𝒞_⋆⟦e_⋆⟧` is produced by a syntax-directed pass with no iteration
  [PPA §3.4.1, p. 175] (book p. 175; PDF p. 193); `Proposition 3.21` relates its solutions to the acceptability
  relation, so the generator can be checked separately from any solver
  [PPA Proposition 3.21, p. 176] (book p. 176; PDF p. 194).
- **Solving**: `Table 3.7` solves the generated system with a graph worklist
  [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196), and Chapter 6 treats general systems `x ⊒ t` independently of
  where they came from [PPA §6.1, p. 365] (book p. 365; PDF p. 381).
- **Chapter 5 instance**: `𝒲_CFA` emits constraints `C` during reconstruction and a separate step computes the
  least solution `θ_A` [PPA §5.3.4, p. 318] (book p. 318; PDF p. 335).
- **Engineering consequence `[derived]`**: the generator is a `[external: pure function]` of the syntax tree and
  the solver is reusable across analyses; Chapter 6 notes generator toolkits such as `BANE` for set constraints
  [PPA Chapter 6 Concluding Remarks, p. 387] (book p. 387; PDF p. 403).

## 9. Practical Implementation Patterns (All `[external]`)

| Technique | Where it attaches | Formal anchor | Caveat |
| :--- | :--- | :--- | :--- |
| `[external: hash-consing]` | Immutable lattice elements, shape graphs `(S, H, is)` | Anti-symmetry of `⊑` [PPA §A.1, p. 393] (book p. 393; PDF p. 409); shape graphs [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133) | Needs a canonical encoding, or equal elements get distinct identities |
| `[external: union-find]` | Unification and equivalence classes | `𝒰_UL` (`Table 5.6`) [PPA Table 5.6, p. 305] (book p. 305; PDF p. 322); `𝒰_CFA` (`Table 5.7`) [PPA Table 5.7, p. 307] (book p. 307; PDF p. 324) | The book composes substitutions; near-linear cost comes from the external structure, and binding `α` to `α` must short-circuit |
| `[external: memoisation]` of local queries | Demand-driven solving of one flow variable | Local solvers in Chapter 6 Concluding Remarks [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401) | Cached answers inside an unfinished strong component are provisional `[derived]` |
| `[external: incremental recomputation]` | Re-analysis after program edits | Omitted by the Preface; nearest anchor is the differential worklist propagating `Δ` [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401) | Answer from general knowledge and label it as external |

## 10. Pattern Misuse That Breaks a Formal Contract

- **Merge is an upper bound but not the least**: the result is sound but imprecise at every join; the lattice
  laws of Section 2 are violated.
- **Widening without its guard**: `∇` need not be monotone, so updating with `old ∇ new` when `new ⊑ old`
  can lose stability; keep the `f(x) ⊑ x` guard of `Proposition 4.13`
  [PPA Proposition 4.13, p. 227] (book p. 227; PDF p. 244).
- **Observer that misses a guard variable**: a conditional term `if c ⊑ t₁ then t₂` must subscribe on the free
  variables of both `t₁` and `t₂` [PPA Example 6.2, p. 367] (book p. 367; PDF p. 383); otherwise updates are dropped.
- **Timeout returns an intermediate state**: before the worklist is empty, `Analysis` lies at or below `μ_𝒮` and is
  not yet certified reductive [PPA §6.1.1, p. 371] (book p. 371; PDF p. 387); a may-analysis that returns it can miss
  results `[derived]`.
- **Adapter checked only on its two laws**: `(4.8)` and `(4.9)` without explicit monotonicity do not give a Galois
  connection [PPA Proposition 4.20, p. 236] (book p. 236; PDF p. 253).
- **Decorator that rejects programs**: breaks conservative extension (`Fact 5.6`)
  [PPA Fact 5.6, p. 291] (book p. 291; PDF p. 308).

## 11. Where the Formal Details Live

- Lattices, chains and fixed points: [appendix-a-posets-lattices-fixed-points.md](appendix-a-posets-lattices-fixed-points.md).
- Monotone Frameworks and transfer functions: [intraprocedural-analyses-and-frameworks.md](../../ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md).
- Constraint generation and the graph solver: [constraint-generation-and-cubic-solver.md](../../ppa-control-flow-and-constraints/references/constraint-generation-and-cubic-solver.md).
- Widening and narrowing: [correctness-and-fixed-points.md](../../ppa-abstract-interpretation/references/correctness-and-fixed-points.md).
- Galois connections: [galois-connections-and-insertions.md](../../ppa-abstract-interpretation/references/galois-connections-and-insertions.md).
- Combinators and induced operations: [combinators-and-induced-operations.md](../../ppa-abstract-interpretation/references/combinators-and-induced-operations.md).
- Type inference and unification: [inference-unification-and-subtyping.md](../../ppa-types-effects-and-regions/references/inference-unification-and-subtyping.md).
- Worklist algorithms: [worklist-and-rpo-algorithms.md](../../ppa-fixedpoint-solvers/references/worklist-and-rpo-algorithms.md) and [scc-round-robin-and-advanced-solvers.md](../../ppa-fixedpoint-solvers/references/scc-round-robin-and-advanced-solvers.md).
