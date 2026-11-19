---
name: ppa-abstract-interpretation
description: Construct, compose, and certify abstract domains, Galois connections and insertions, representation functions, widening and narrowing operators, reduced and relational tensor products, and induced transformers over infinite-height lattices. Use when designing Interval, Sign, Parity, or Array Bound AB lattices; proving adjunction laws, Moore-family meet closure, or semantic soundness from collecting semantics; engineering threshold widening and narrowing schedules; or inducing best transfer functions and concretisation widenings. Do not use for Chapter 1 routing or Appendix A-C background (ppa-program-analysis), classical finite-height WHILE data flow or shape graphs (ppa-dataflow-and-slicing), closure call-target constraints (ppa-control-flow-and-constraints), annotated type and effect inference (ppa-types-effects-and-regions), RPO or SCC worklist ordering (ppa-fixedpoint-solvers), or exploit threat triage (ppa-cyber-vulnerability-analysis).
---

<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L2 procedural skill for Chapter 4 Abstract Interpretation, Galois connections, widening/narrowing convergence, domain combinators, and induced operations. -->

# Abstract Interpretation: Domain Synthesis, Widening, and Induced Soundness Workflows

Actionable engineering workflows for designing, combining, accelerating, certifying, and debugging Abstract
Interpretation analyses across Chapter 4 ([PPA Chapter 4, p. 211] (book p. 211; PDF p. 228) through
[PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299)). Complete definitions, side conditions, and proof structures
live in the self-contained L1 references:

- Mundane correctness (`§4.1`), `Interval`, widening `∇`, narrowing `Δ`, and `U7` (`§4.2`, `Exercises 4.1–4.12`):
  [correctness-and-fixed-points.md](./references/correctness-and-fixed-points.md)
- Galois connections `(L, α, γ, M)`, adjoint extraction, Galois insertions, reduction `ς`, upper closure operators (`[external: uco(L)]`), and duality
  (`§4.3`, `Concluding Remarks`, `Figure 4.10`, `Exercises 4.13–4.14`):
  [galois-connections-and-insertions.md](./references/galois-connections-and-insertions.md)
- Domain combinators (`§4.4`), `29`-atom `AB` synthesis, induced operations, generalised Monotone Frameworks (`§4.5`,
  `U6`), `Mini Projects 4.1–4.3`, and `Exercises 4.15–4.24`:
  [combinators-and-induced-operations.md](./references/combinators-and-induced-operations.md)
- Shared foundational and sibling cross-references:
  [chapter-1-five-formulations.md](../ppa-program-analysis/references/chapter-1-five-formulations.md),
  [appendix-a-posets-lattices-fixed-points.md](../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md),
  [intraprocedural-analyses-and-frameworks.md](../ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md),
  [shape-analysis.md](../ppa-dataflow-and-slicing/references/shape-analysis.md), and
  [polyvariant-kcfa-cpa-and-dfa.md](../ppa-control-flow-and-constraints/references/polyvariant-kcfa-cpa-and-dfa.md).

## 1. Boundary Dispatch Before Designing an Abstract Domain

Verify that property-space construction, Galois soundness, or infinite-chain convergence is the core problem before
implementing lattice operations (`G-U4a-01`, `G-U4a-03`):

| Task Signature | Target Skill | Reason |
| :--- | :--- | :--- |
| Choosing between `DFA`, `CFA`, `AI`, and `Types`, or Appendix A–C order/coinduction proofs | `ppa-program-analysis` (router) | Master router owns cross-paradigm arbitration and shared appendices |
| Galois connections/insertions, `β`/`η`/`ς`, `Interval`/`Sign'`/`AB`, `∇`/`Δ`, `α ∘ f ∘ γ`, `γ`-widening | **This skill (`ppa-abstract-interpretation`)** | Core Chapter 4 domain design, convergence, and soundness domain |
| Classical `AE`/`RD`/`VB`/`LV`, `ud`/`du` slicing, `§2.5` call strings, `§2.6` shape graphs on `ACC` lattices | `ppa-dataflow-and-slicing` | Known syntactic CFG with `ACC` (`U6`/`U7` counterpart) |
| Higher-order closures, callbacks, `0-CFA`, `k-CFA`, `CPA`, `Table 3.7` cubic subset solver | `ppa-control-flow-and-constraints` | Dynamic call-graph discovery via subset constraints |
| Annotated types, subeffecting, let-polymorphic effect/region inference, CSP behaviours | `ppa-types-effects-and-regions` | Syntax-directed type/effect inference rules (`Chapter 5`) |
| Worklist data structures, LIFO/FIFO/RPO scheduling, SCC/round-robin `d(G, T) + 3` pass bounds | `ppa-fixedpoint-solvers` | Iteration order and solver complexity once `L` and `∇` are fixed (`U7`) |
| End-to-end `[external: taint/sanitizer]` threat modelling, exploitability triage, `[external: CWE]` policy engineering | `ppa-cyber-vulnerability-analysis` | Security vulnerability policy layer across chapters |

## 2. Procedure 1: Certify Semantic Soundness via Correctness Relations and Adjoints

Execute this workflow when defining a new abstract lattice `M` or auditing whether `M` faithfully abstracts concrete
states/traces `L = (𝒫(V), ⊆)` [PPA §4.1.1, p. 214] (book p. 214; PDF p. 231)
[PPA §4.3.1, p. 239] (book p. 239; PDF p. 256):

1. **Fix information order `⊑` downward toward precision (`ORIENTATION_GATE`, `G-U4a-04`, `G-U4b-20`)**:
   - Orient `m_1 ⊑ m_2` so `m_1` is **more precise** (`⊥` empty/unreachable, `⊤` trivially safe/uninformative).
   - Never import Denotational Semantics intuition (`⊥` uninformative + `lfp`): Denotational Semantics and Abstract
     Interpretation invert `⊑` while both computing `lfp`, so they are **not lattice duals** (`G-U4b-20`)
     [PPA Chapter 4 Concluding Remarks, p. 273] (book p. 273; PDF p. 290).
   - Check whether the target property is **first-order** (sets of values `V`, covered by `§4.1` `R` / `β` and
     `§§4.2–4.5`, `G-U4a-02`, `G-U4a-06`, `G-U4a-07`) or **second-order** (input-output relations or
     `[external: 2-safety hyperproperties]`, which bypass `§4.1` and enter directly at `§4.3` over `L = 𝒫(V × V)`, `G-U4a-03`)
     [PPA §4.1, p. 212] (book p. 212; PDF p. 229).
2. **Verify Moore-family correctness `(4.4)` + `(4.5)` or build `β` / `η` (`MOORE_FAMILY_GATE`, `G-U4a-05`, `G-U4a-18`)**:
   - If starting from `v R m`, verify upward closure `(4.4)` and arbitrary-meet closure `(4.5)` (`{m | v R m}` is a
     Moore family, ensuring `v R ⊤` while allowing `v R ⊥ = false`, `Exercise 4.2`, `G-U4b-23`), then extract canonical
     `β_R(v) = ⨅{m | v R m}` (`Lemma 4.5`) and guard smash-`⊥` carriers (`σ̂ ≠ ⊥` in `Example 4.3`)
     [PPA Lemma 4.5, p. 217] (book p. 217; PDF p. 234).
   - Lift any `β : V → M` directly to `(𝒫(V), α, γ, M)` via `α(V') = ⨆{β(v) | v ∈ V'}` and `γ(m) = {v ∈ V | β(v) ⊑ m}`
     (`§4.3`, `BKL-029`, `BKL-033`), or lift scalar classifier `η : V → D` to `(𝒫(V), α_η, γ_η, 𝒫(D))` (`Example 4.21`)
     [PPA §4.3, p. 237] (book p. 237; PDF p. 254).
3. **Test `γ` complete multiplicativity before coding `α` (`ADJOINT_MULTIPLICATIVITY_GATE`, `G-U4a-17`, `G-U4a-19`, `G-U4a-20`)**:
   - When relating two non-powerset lattices `(L, α, γ, M)` (such as `Interval` and `Sign'`), specify `γ : M → L` first
     and check `γ(⨅ M') = ⨅{γ(m) | m ∈ M'}` (`γ(⊤_M) = ⊤_L`, plus binary meets on all incomparable pairs when `M` is
     finite via `Appendix A Lemma A.4`, `Lemma 4.23`).
   - **Failure witness (`Example 4.25` vs `Exercise 4.13`)**: Monotone `γ_{IS} : 𝒫(Sign) → Interval` **has no lower
     adjoint `α_{IS}`** because `γ_{IS}({-, 0} ∩ {-, +}) = [-∞, -1] ≠ [-∞, 0] = γ_{IS}({-, 0}) ⊓ γ_{IS}({-, +})`!
     Removing `{-, +}` forms the 7-element non-distributive lattice `Sign'` (`Figure 4.10`, `G-U4b-23`), restoring
     `(Interval, α_{IS'}, γ_{IS'}, Sign')` [PPA Example 4.25, p. 240] (book p. 240; PDF p. 257)
     [PPA Exercise 4.13, p. 279] (book p. 279; PDF p. 296).
   - If verifying `(L, α, γ, M)` via `(4.8)` `γ ∘ α ⊒ id_L` and `(4.9)` `α ∘ γ ⊑ id_M`, prove monotonicity of `α` and
     `γ` explicitly; if proving `(4.10)` `α(l) ⊑ m ⇔ l ⊑ γ(m)`, monotonicity follows automatically (`Proposition 4.20`).
     Case-split empty sets explicitly (`α_{ZI}(∅) = ⊥` in `Example 4.19`, `G-U4a-17`), and never assume `γ(⊥_M) = ⊥_L`
     or `α(⊤_L) = ⊤_M` without checking (`G-U4a-19`, `BKL-033`)!
4. **Canonicalise redundant encodings via `ς` (`INSERTION_REDUCTION_GATE`, `G-U4a-22`, `G-U4a-23`, `G-U4b-01`)**:
   - Check Galois insertion (`α ∘ γ = id_M` `⇔` `α` surjective `⇔` `γ` injective `⇔` `η` surjective, `Lemma 4.27`) so
     syntactic equality in solver worklists matches semantic equality (`G-U4a-21`).
   - If ghost elements exist (e.g. `(0, odd)` in `Example 4.28` or multiple empty intervals violating `Example 4.10`'s
     single-`⊥` exclusion `[∞, ∞]` / `[-∞, -∞]`, `G-U4a-08`), quotient `M` by `ς(m) = α(γ(m))` (`Proposition 4.29`,
     `Facts 4.30–4.31`, `ς_η(D') = D' ∩ η[V]` in `Example 4.32`; note `BKL-024` `ς` store `§2.5 p. 86` vs reduction
     operator `§4.3.2 p. 244`), remembering that `⨆_{ς[M]} = ⨆_M` whereas meets must re-reduce via
     `⨅_{ς[M]} M' = ς(⨅_M M')` [PPA Fact 4.31, p. 246] (book p. 246; PDF p. 263).

## 3. Procedure 2: Engineer Widening and Narrowing Convergence Over Infinite Lattices

Follow this two-phase protocol whenever `L` lacks `ACC` (`U7`, `G-U4a-09`, `BKL-013`)
[PPA §4.2.1, p. 226] (book p. 226; PDF p. 243) [PPA §4.2.2, p. 230] (book p. 230; PDF p. 247):

1. **Audit arithmetic semantics before using `Interval` (`MACHINE_INTEGER_WRAP_GATE`, `G-U4a-08`, `BKL-001`)**:
   - `Interval` (`Example 4.10`, `inf(⊥) = ∞, sup(⊥) = -∞`) is sound over mathematical `Z` (`Table 2.5`), **not**
     fixed-width `[external: two's-complement bit-vectors]` (`[external: CWE-190]` signed/unsigned wraparound turns `[0, INT_MAX] + [1, 1]`
     negative at runtime; see `BKL-001`). Require `[external: overflow-trapping semantics]`, arbitrary-precision integers, or
     modular/`[external: wrapped-interval]` domains before eliding bounds checks!
2. **Enforce the five widening invariants (`WIDENING_CUTSET_AND_GUARD_GATE`, `G-U4a-10`–`G-U4a-13`, `BKL-002`)**:
   - **Cutset placement**: Place `∇` strictly at a feedback-vertex loop cutset (e.g. `[external: Bourdoncle WTO]` heads,
     `Chapter 6 Exercise 6.13`), keeping exact `⊔` at acyclic diamond merges.
   - **Strict `old ∇ new` operand order**: Compute `f_∇^{n-1} ∇ f(f_∇^{n-1})`, never `new ∇ old` (`Example 4.12`
     asymmetry causes `new ∇ old` to diverge, `G-U4a-11`).
   - **Explicit reductive guard**: Test **`if f(f_∇^{n-1}) ⊑ f_∇^{n-1}`** before calling `∇` so non-absorptive `∇`
     cannot overshoot `Red(f)` (`Fact 4.14`, `G-U4a-11`, `G-U4a-12`).
   - **Step-1 `⊥` protection & fixed finite `K`**: Explicitly short-circuit **`⊥ ∇_K x = x`** (fixing `Example 4.15`'s
     `⊥ ∇_∅ [0, 0] = [-∞, ∞]` jump, `G-U4a-13`), seed `K ⊆ Z` statically from program integer constants (`[external: AST]` loop constants),
     and **never** grow `K` dynamically during iteration! If delaying widening inside `l'` (`Exercises 4.6, 4.9`),
     verify `↓l'` satisfies `ACC` (`inf(int') > -∞ ∧ sup(int') < ∞`, `G-U4b-24`)
     [PPA Example 4.15, p. 228] (book p. 228; PDF p. 245) [PPA Exercise 4.9, p. 278] (book p. 278; PDF p. 295).
   - **Zero monotonicity assumptions (`BKL-002`)**: Never assume `x_1 ⊑ x_2 ⇒ (x_1 ∇ y) ⊑ (x_2 ∇ y)` in solver caching
     (`[1, 1] ∇_∅ [1, 2] = [1, ∞] ⋢ [0, 2] = [0, 2] ∇_∅ [1, 2]`), and if warm-starting at `f_∇^0 = l_0`, enforce
     **`l_0 ∈ Ext(f)`** (`l_0 ⊑ f(l_0)`, `Exercise 4.8`, `G-U4b-24`) so `Proposition 4.13` termination holds!
3. **Run narrowing strictly inside `Red(f)` (`NARROWING_REDUCTIVE_ENTRY_GATE`, `G-U4a-14`–`G-U4a-16`, `G-U4b-24`)**:
   - Start `[f]_Δ^0 = f_∇^m` **only after** `f(f_∇^m) ⊑ f_∇^m` holds (`Lemma 4.16` `(4.7)`, `Proposition 4.17`);
     starting outside `Red(f)` violates descending chain hypotheses and is unsound!
   - Remember every narrowing operator satisfies `l Δ l = l` (`G-U4a-14`), is **not** dual to widening (`G-U4a-15`), and
     threshold `Δ_N` (`Example 4.18`, `G-U4a-16`) can still take many finite steps on finite shifts — cap refinement
     with a `k`-step descending chain truncator `ϒ` (`k ∈ {1, 2, 3}`, `Exercise 4.11`) when strict budgets apply
     [PPA Lemma 4.16, p. 230] (book p. 230; PDF p. 247) [PPA Exercise 4.11, p. 278] (book p. 278; PDF p. 295).

## 4. Procedure 3: Compose Multi-Attribute and Relational Abstract Domains

Select the leanest `§4.4` combinator capable of expressing the target invariant (`G-U4b-02`–`G-U4b-10`, `G-U4b-19`)
[PPA §4.4.1, p. 249] (book p. 249; PDF p. 266) [PPA §4.4.2, p. 254] (book p. 254; PDF p. 271):

1. **Choose independent vs relational structure (`G-U4b-03`–`G-U4b-05`)**:
   - Use **independent attribute** (`M_1 × M_2`, `Example 4.34`) or **total function space** (`Var → M`, `Example 4.36`;
     optionally wrapped in smash-bottom `_⊥`) when per-variable facts suffice (`O(|Var_⋆|)` memory; tag disjoint unions
     `({1} × V_1) ∪ ({2} × V_2)` if encoding as extraction functions, `Exercise 4.16`).
   - Upgrade to **powerset relational tensor product** (`𝒫(D_1 × D_2)`, `Example 4.35`), **reduced tensor product**
     (`Example 4.39` `AB`, `Mini Project 4.1` `LR`), or relational geometry (`[external: Octagons]`, convex polygons `[41]`
     / `[external: convex polyhedra]`) whenever cross-variable invariants (`y = -x`, `0 ≤ idx < len` for `[external: CWE-787]`) must survive control joins!
2. **Re-establish Galois insertions after same-carrier products (`COMBINATOR_INSERTION_GATE`, `G-U4b-06`–`G-U4b-09`)**:
   - Sequential (`p. 247`, reversing `γ_1 ∘ γ_2`), independent (`Exercise 4.17`), function-space (`Exercise 4.17`), and
     powerset relational (`Exercise 4.18`) combinators **preserve Galois insertions**; **direct product (`Exercise 4.19`)
     and direct tensor product (`Example 4.38`) do NOT**!
   - Apply `ς` reduction (`§4.4.2`, `ρ_1 ⊓ ρ_2` in `[external: uco(L)]`, `G-U4b-19`) to prune uninhabited tuples (`45 → 29` bits in
     `AB`, `Example 4.39`; note `AB` still abstracts bounded disks `x^2 + y^2 ≤ 100` to `⊤` and `x = y + 3` to `6` atoms,
     `Exercise 4.21`, `G-U4b-07`, `G-U4b-08`).
   - **Termination rule (`CHANNEL_REDUCTION_TERMINATION_GATE`, `G-U4b-09`)**: In `[external: ReducedProduct<D1, D2>]`, run
     `[external: Granger channel reduction]` `ρ_{12}` *before* widening inside transfer steps, **never after** loop-header widening!

## 5. Procedure 4: Derive Best Transfer Functions, Lift Monotone Frameworks, and Induce Widening

Execute this workflow when synthesising abstract operations or proving whole-analyser soundness (`§4.5`, `U6`)
[PPA Lemma 4.41, p. 260] (book p. 260; PDF p. 277) [PPA Proposition 4.44, p. 268] (book p. 268; PDF p. 285):

1. **Calculate `f^# = α_2 ∘ f_p ∘ γ_1` and bound `g_p ⊒ f^#` (`G-U4b-10`–`G-U4b-12`)**:
   - Derive closed-form `α_2(f_p(γ_1(m_1)))` symbolically (`Example 4.40` `⊕` on `Sign`, `Exercise 4.22` `[a_1+a_2, b_1+b_2]`
     on `Interval`). By `Lemma 4.41`, optimal `f_p` (`Exercise 4.5`) makes `f^#` optimal, while any monotone **upper**
     approximation `g_p ⊒ f^#` preserves soundness and `lfp(f) ⊑ γ(lfp(g))` (`Lemma 4.42`).
   - Remember composition is sub-multiplicative even on Galois insertions: **`α(f_1 ∘ f_2) ⊑ α(f_1) ∘ α(f_2)`**
     (`Exercise 4.20`, explaining why `CP` yields `⊤` on `[x := y - y]` rather than `0`, `G-U4b-10`).
2. **Lift to Generalised Monotone Frameworks (`EXTREMAL_EQUALITY_GATE` & `EDGE_GUARD_SENSITIVITY_GATE`, `G-U4b-13`–`G-U4b-15`)**:
   - Check `g_ℓ ⊒ α ∘ f_ℓ ∘ γ` (`∀ℓ`, short-circuiting `σ̂ = ⊥` in `CP`, `G-U4b-15`) **and exact extremal equality
     `γ(ȷ) = ι`** (`p. 264`, e.g. `γ_{CP}(λx.⊤) = State`; mere `ȷ ⊒ α(ι)` suffices for `B^⊒ ⇒ A^⊒` but **not** for
     semantic `(4.11) ⇒ (4.12)`!). Use the same two-tier reference pattern (`SS` `Lemma 4.43`, `SH` `Mini Project 4.2`,
     `⊨_{SV}` `Mini Project 4.3`, `G-U4b-22`) for heap and higher-order analyses
     [PPA §4.5.2, p. 264] (book p. 264; PDF p. 281).
   - Attach branch-guard filters `filter_b` to **CFG edges `(ℓ_1, ℓ_2)`** rather than nodes `ℓ` (`Remark.` `p. 266`,
     `Exercise 2.11`, `G-U4b-14`), and approximate compiler transformation guards `l_ℓ ⊑ l_Ξ` **downward** (`l'_Ξ ⊑ l_Ξ`)
     via **dual Galois connections** (`DUAL_GUARD_POLARITY_GATE`, `G-U4b-21`)
     [PPA §4.5.2, p. 266] (book p. 266; PDF p. 283) [PPA Chapter 4 Concluding Remarks, p. 273] (book p. 273; PDF p. 290).
3. **Induce widening along `γ` — NEVER narrowing (`GAMMA_WIDENING_VS_NARROWING_GATE`, `G-U4b-16`–`G-U4b-18`)**:
   - Before deploying `l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))` (`Exercise 4.23`), verify `Proposition 4.44`: either `(i)` `M`
     has `ACC`, or `(ii)` **`(L, α, γ, M)` is a Galois insertion** and `∇_M` is a widening operator (plus **`γ(⊥_M) = ⊥_L`**
     if relying on `Lemma 4.45`'s lockstep identity `lfp_{∇_L}(f) = γ(lfp_{∇_M}(α ∘ f ∘ γ))`, noting `p. 269`'s typo
     `g(g_{∇_L}^n)`).
   - **Hard prohibition (`Exercise 4.24`, `G-U4b-18`)**: **Never** define narrowing as `γ(α(l_1) Δ_M α(l_2))` — for any
     `l_1 ∉ γ[M]`, `l_1 Δ_L l_1 = γ(α(l_1)) ⋢ l_1` breaks contractiveness even on finite Galois insertions!

## 6. Procedure 5: Certify List, Heap Shape, and Higher-Order CFA+DFA Extensions

Apply the two-tier `§4.5.2` verification pattern to structured data, pointer heaps, and higher-order languages
(`Mini Projects 4.1–4.3`, `G-U4b-22`) [PPA Mini Project 4.1, p. 274] (book p. 274; PDF p. 291)
[PPA Mini Project 4.2, p. 274] (book p. 274; PDF p. 291) [PPA Mini Project 4.3, p. 275] (book p. 275; PDF p. 292):

1. **Synthesise relational sequence/slice domains (`Mini Project 4.1`, `LR`)**:
   - Pair structural predicates (`H` = common non-empty head, `S` = suffix) with signed length difference
     `range(length(x) - length(y))` (`Range`, contrasting `Example 4.33`'s absolute-magnitude `|z_1| - |z_2|`,
     `G-U4b-03`).
   - Run `ς` reduction to prune impossible combinations: under the formal asymmetric suffix definition (`x` suffix of
     `y`, `n ≤ m`), `|LR| = 16` (removing `4` triples with `S` and `+1`/`>+1`); under the symmetric gloss, `|LR| = 20`.
     Ensure `([], [])` maps to **`({S}, 0)`** (`n = m = 0` falsifies `H` while satisfying `S`)!
2. **Audit heap shape abstractions (`Mini Project 4.2`, `SH` → `SG`)**:
   - Define `vars(ξ)(σ) = n_X` (`X = {x | σ(x) = ξ}`) and `β_{SA}(σ, ℋ) = {(S, H, is)}` to lift concrete `(State × Heap)`
     transfers `f_ℓ^{SH}` (`Lemma 4.43` analogue) to `(𝒫(State × Heap), α_{SA}, γ_{SA}, 𝒫(SG))`.
   - Do **not** assume Galois insertion (`γ_{SA}` maps unreachable-garbage or over-shared shape graphs to `∅`) or
     transfer optimality (`f_ℓ^{SA} ⊐ α_{SA} ∘ f_ℓ^{SH} ∘ γ_{SA}` on summary-node `n_∅` materialisation, `Exercise 2.23`):
     if `γ`-induced widening (`Proposition 4.44(ii)`) is needed on `𝒫(SG)`, quotient `SG` by `ς_{SA}` first!
3. **Certify coupled higher-order `CFA + DFA` (`Mini Project 4.3`, `⊨_{SV}` → `⊨_D`)**:
   - Specify reference `"sets of values"` acceptability `(Ĉ_{SV}, ρ̂_{SV}) ⊨_{SV} e` (`Data = Val`), prove subject-reduction
     soundness from `Theorem 3.10` and `Example 4.4` (fixing `p. 275`'s misprint `Example 4.40`), then lift
     `(𝒫(Val), α, γ, L)` pointwise (`§4.4.1`) to `(Ĉ, D̂, ρ̂, δ̂) ⊨_D e ⇒ γ'(Ĉ, D̂, ρ̂, δ̂) ⊨_{SV} e` (fixing `p. 275`'s
     Latin `d̂` misprint for `Table 3.9`'s Greek `δ̂`).

## 7. Procedure 6: Soundness Verification Harness (`[external: Property-Based and SMT]`)

Automate verification of custom abstract domains and transfer functions in `[external: CI]` using four algebraic contracts
derived directly from `§§4.1–4.5` [PPA Lemma 4.22, p. 239] (book p. 239; PDF p. 256)
[PPA Lemma 4.41, p. 260] (book p. 260; PDF p. 277):

1. **Contract A — Concretisation Meet-Preservation (`Lemma 4.23` / `Appendix A Lemma A.4`)**:
   - Assert `γ(⊤_M) = ⊤_L`, `m_1 ⊑ m_2 ⇒ γ(m_1) ⊑ γ(m_2)`, and `γ(m_1 ⊓ m_2) = γ(m_1) ⊓ γ(m_2)` across sampled
     incomparable pairs `(m_1, m_2)` before writing `α` (`Example 4.25`).
2. **Contract B — Pointwise Transfer Soundness (`Lemma 4.41` + `Proposition 4.20`)**:
   - Instead of enumerating infinite `γ_1(m_1)`, `[external: fuzz or SMT-check]` the equivalent concrete witness obligation:
     ```text
     ∀v_1 ∈ V_1, ∀v_2 ∈ V_2, ∀m_1 ∈ M_1 :
         (α_1(β_1(v_1)) ⊑ m_1  ∧  (p ⊢ v_1 ↝ v_2))   ⇒   α_2(β_2(v_2)) ⊑ g_p(m_1)
     ```
     including boundary states (`m_1 = ⊥_M`, division by zero, `[external: INT_MIN / INT_MAX]` if modelling machine integers,
     `BKL-001`).
3. **Contract C — Insertion Canonicality (`Lemma 4.27` / `Fact 4.31`)**:
   - On domains claiming Galois insertion (required by `Proposition 4.44(ii)` and `Lemma 4.45`), assert `ς(m) = m` for
     every reachable abstract state `m` (no duplicate empty encodings or unpruned product tuples).
4. **Contract D — Two-Phase Solver Reductive Gate (`Fact 4.14` / `Lemma 4.16`)**:
   - Assert `f(f_∇^m) ⊑ f_∇^m` at the widening-to-narrowing handoff, and assert `f([f]_Δ^n) ⊑ [f]_Δ^n ⊑ [f]_Δ^{n-1}` at
     every narrowing step!

## 8. Diagnostic Symptom-to-Root-Cause Triage Matrix

| Observed Analyser Symptom | Primary Root Cause to Check | Governing Anchor |
| :--- | :--- | :--- |
| Loop counter jumps to `[-∞, ∞]` on iteration 1 | Missing `⊥ ∇_K x = x` short-circuit (`inf(⊥) = ∞` triggers `-∞, ∞`) or `∇` placed at acyclic join | `Example 4.15`, `G-U4a-13` |
| Solver never terminates despite `∇` | Reversed `new ∇ old` order, dynamic `K` growth, non-insertion in `Prop 4.44(ii)`, post-`∇` channel reduction `ρ_{12}`, or `l_0 ∉ Ext(f)` | `G-U4a-11`, `G-U4b-09`, `G-U4b-16`, `G-U4b-24` |
| Concrete reachable state missed (unsound!) | Non-monotone/under-approximating `g_ℓ`, `γ(ȷ) ≠ ι`, narrowing started before `f(x) ⊑ x`, upward guard `l'_Ξ`, or `[external: machine int32 wraparound]` | `BKL-001`, `G-U4a-15`, `G-U4b-13`, `G-U4b-21` |
| Boolean test `[b]^ℓ` fails to refine branch variables | Node-attached `f_ℓ([b]^ℓ) = id` instead of edge-attached guard transfers; or `Sign'` lacks `{-+}` (`- ⊔ + = ⊤`, needs `𝒫(Sign)` / disjunctive completion) | `Remark.` `p. 266`, `Figure 4.10`, `G-U4b-14`, `G-U4b-23` |
| `(idx, len)` bounds lost at `if/else` join | Pointwise `Var → Interval` (`Example 4.36` pattern) instead of relational `𝒫(AB)` (`Ex 4.39`) | `Example 4.36`, `Example 4.39`, `G-U4b-07` |
| Narrowing pass inflates set upward (`⋢ l_1`) | Used broken `γ(α(l_1) Δ_M α(l_2))` (`Exercise 4.24`) on `l_1 ∉ γ[M]` | `Exercise 4.24`, `G-U4b-18` |

## 9. Golden Regression Oracles and Backlog Guardrails

Before certifying any Chapter 4 domain or solver implementation (`G-U4a-24` warns never to copy formulas from unverified
PDF OCR text), run these five deterministic unit-test oracles and verify open backlog guardrails:

1. **Adjoint & Non-Existence Oracle (`Example 4.25` vs `Exercise 4.13`)**: Assert `γ_{IS}({-, 0} ∩ {-, +}) ≠ γ_{IS}({-, 0}) ⊓ γ_{IS}({-, +})`
   on `𝒫(Sign)`, and assert `α_{IS'}(γ_{IS'}(s')) = s'` plus `int ⊑ γ_{IS'}(α_{IS'}(int))` across all `7` elements of `Sign'`.
2. **Widening & Narrowing Trace + Non-Monotonicity Oracle (`Examples 4.15, 4.18`, `BKL-002`)**: With `K = {3, 5}` on
   `[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], ⋯`, verify `∇_K` yields `[0, 1], [0, 3], [0, 3], [0, 5], [0, 5], [0, ∞], [0, ∞], ⋯`;
   with `N = 3` on `[0, ∞], [1, ∞], [2, ∞], [3, ∞], [4, ∞], ⋯`, verify `Δ_N` stabilises at `[3, ∞]`; assert
   `⊥ ∇_∅ [0, 0] = [-∞, ∞]` (requiring `⊥ ∇_K x = x` guard) and `[1, 1] ∇_∅ [1, 2] = [1, ∞] ⋢ [0, 2] = [0, 2] ∇_∅ [1, 2]`.
3. **Array Bound `AB` Reduction Oracle (`Example 4.39`, `Exercise 4.21`)**: Assert `|AB| = 29` (`45 - 16`),
   `α_{SSR'}({(x, y) | x = y + 3})` has cardinality `6`, `α_{SSR'}({(x, y) | x ≥ y + 1})` has cardinality `13`,
   `α_{SSR'}({(x, y) | x^2 + y^2 ≤ 100}) = AB` (`29`), and `[derived]` `α_{SSR'}({(len, idx) | 0 ≤ idx < len})` equals
   the `4`-atom mask `{(+, 0, +1), (+, 0, >+1), (+, +, +1), (+, +, >+1)}`.
4. **Composition Laxness Oracle (`Exercise 4.20`)**: On `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))` with `f_2(X) = {z - 1 | z ∈ X}`
   and `f_1(X) = {z + 1 | z ∈ X}` (`f_1 ∘ f_2 = id`), assert `α(f_1 ∘ f_2)({-}) = {-} ⊂ {-, 0} = (α(f_1) ∘ α(f_2))({-})`.
5. **Broken `γ`-Narrowing Oracle (`Exercise 4.24`)**: On `(𝒫(Z), α_{sign}, γ_{sign}, 𝒫(Sign))`, assert
   `γ_{sign}(α_{sign}({1, 2}) ∩ α_{sign}({1, 2})) = Z_{>0} ⊈ {1, 2}`.
6. **Non-Blocking Backlog & Source-Errata Guardrails**:
   - `BKL-001` (`Interval` over unbounded `Z` vs `[external: wrapping machine arithmetic]`);
   - `BKL-002` (`∇` non-monotonicity, non-commutativity, and `[external: loop-cutset placement]`);
   - `BKL-013` (`S → L` fails `ACC` over infinite index sets `S`);
   - `BKL-024`, `BKL-029`, `BKL-033` (`ς`/`ϕ`/`Δ` scope collisions across `pp. 86, 225, 230, 244`, `Var_⋆` vs `Var`, and non-strict `γ(∅)` in `§1.5`);
   - Printed errata & non-blocking Chapter 4 backlog: `BKL-063` (`Lemma 4.45` `p. 269` `g(g_{∇_L}^n)` for `g(g_{∇_M}^n)`),
     `BKL-064` (`Concluding Remarks` `p. 271` `Section 4.3.` for `§4.4.2` & `ρ_2(L)`), `BKL-065` (`Mini Project 4.3`
     `p. 275` `Example 4.40`/`d̂` for `Example 4.4`/`δ̂`), `BKL-066` (`Exercise 4.14` `p. 279` `ς_η(V')` for `ς_η(D')`),
     `BKL-067` (`§4.2.2` `p. 230` non-absorptive `Δ` vs `l Δ l = l`), `BKL-068` (`Example 4.15` `p. 228` `⊥ ∇_K` blowup),
     `BKL-069` (`Prop 4.13/4.17/4.44(ii)` & `Lemma 4.16` `n` basis), `BKL-070` (`Mini Project 4.1` `p. 274` 16 vs 20 `LR`),
     `BKL-071` (`§4.5.2` `SS` node-attached branch guards), and `BKL-072` (`Exercise 4.24` `p. 282` broken `γ`-narrowing).
