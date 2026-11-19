---
name: ppa-control-flow-and-constraints
description: Specify, build, verify, and debug higher-order Control Flow Analyses (0-CFA, uniform k-CFA, polynomial k-CFA, Cartesian Product Algorithm), conditional subset-constraint generators, cubic graph solvers, and coupled CFA+DFA passes. Use when resolving closures, callbacks, function pointers, or virtual dispatch; lowering coinductive acceptability to syntax-directed subset constraints; building dual-observer constraint-graph worklists; coupling data lattices online to prune dead branches; or choosing polyvariant call-site vs argument-tuple contexts. Do not use for Ch 1 routing or App A-C theory (ppa-program-analysis), first-order WHILE data flow or shape graphs (ppa-dataflow-and-slicing), Galois widenings (ppa-abstract-interpretation), type and effect inference (ppa-types-effects-and-regions), RPO/SCC iteration order (ppa-fixedpoint-solvers), or CWE triage (ppa-cyber-vulnerability-analysis).
---

<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L2 procedural skill for Chapter 3 higher-order Control Flow Analysis, subset-constraint solving, coupled CFA+DFA, and polyvariant k-CFA/CPA. -->

# Higher-Order Control Flow Analysis and Subset-Constraint Workflows

Actionable engineering workflows for specifying, lowering, solving, coupling, and debugging Chapter 3
constraint-based Control Flow Analyses ([PPA §3.1, p. 141] (book p. 141; PDF p. 159) through
[PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227)). Complete rule tables, definitions, side conditions,
and proof structures live in the self-contained `L1` references:

- Abstract `0-CFA` (`Table 3.1`), closure SOS (`Tables 3.2-3.4`), coinduction (`gfp` vs `lfp`), Moore families,
  and syntax-directed `⊨_s` (`Table 3.5`):
  [cfa-core-and-coinduction.md](./references/cfa-core-and-coinduction.md)
- Conditional subset-constraint generation (`Table 3.6`), dual-observer `O(n^3)` graph solver (`Table 3.7`),
  reachability gating (`Mini Project 3.1`), set constraints, and open-system stubs:
  [constraint-generation-and-cubic-solver.md](./references/constraint-generation-and-cubic-solver.md)
- Coupled `CFA + DFA` (`Tables 3.8-3.9`), uniform `k`-CFA (`Table 3.10`), polynomial `k`-CFA / `m`-CFA `[external]`,
  `CPA` (`[2]`, `[external: Agesen]`), imperative stores (`Mini Project 3.4`), and `U4`/`U5` Chapter 2 bridges:
  [polyvariant-kcfa-cpa-and-dfa.md](./references/polyvariant-kcfa-cpa-and-dfa.md)
- Shared mathematical and cross-chapter references:
  [chapter-1-five-formulations.md](../ppa-program-analysis/references/chapter-1-five-formulations.md),
  [appendix-a-posets-lattices-fixed-points.md](../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md),
  [appendix-b-induction-and-coinduction.md](../ppa-program-analysis/references/appendix-b-induction-and-coinduction.md),
  [appendix-c-graphs-dfsf-and-rpo.md](../ppa-program-analysis/references/appendix-c-graphs-dfsf-and-rpo.md),
  [intraprocedural-analyses-and-frameworks.md](../ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md),
  [interprocedural-and-correctness.md](../ppa-dataflow-and-slicing/references/interprocedural-and-correctness.md),
  [annotated-types-and-cfa-soundness.md](../ppa-types-effects-and-regions/references/annotated-types-and-cfa-soundness.md), and
  [inference-unification-and-subtyping.md](../ppa-types-effects-and-regions/references/inference-unification-and-subtyping.md).

## 1. Boundary Dispatch Before Building a Control Flow Analyser

Verify that dynamic call-target resolution or subset-constraint solving is the core task before writing code:

| Task Signature | Target Skill | Reason |
| :--- | :--- | :--- |
| Paradigm selection (`DFA` vs `CFA` vs `AI` vs `Types`) or App A-C fixed-point proofs | `ppa-program-analysis` (router) | Master router owns cross-approach routing and shared appendices |
| Closures, callbacks, function pointers, `0-CFA`, `k`-CFA, `CPA`, `Table 3.7` cubic solver, coupled `CFA+DFA` | **This skill (`ppa-control-flow-and-constraints`)** | Chapter 3 higher-order call-graph & subset-constraint domain |
| First-order `WHILE` `AE`/`RD`/`VB`/`LV`, static `§2.5` call strings/assumption sets, `§2.6` shape graphs | `ppa-dataflow-and-slicing` | `§2.5` assumes static procedure names (`U5` counterpart) |
| Infinite-height numeric domains (`Interval`, polyhedra), widening `∇` and narrowing `Δ` | `ppa-abstract-interpretation` | `§3.5.2` requires `ACC` on `L`; unbounded chains need Chapter 4 |
| Hindley-Milner / Algorithm `W` annotated type, effect, region, or exception inference (`BKL-009`) | `ppa-types-effects-and-regions` | Chapter 5 subeffecting/unification (`U8` counterpart to `0-CFA`) |
| Reverse-postorder scheduling, strong-component (`SCC`) iteration, `d(G_S, T) + 3` round-robin bounds (`BKL-012`) | `ppa-fixedpoint-solvers` | Chapter 6 general solver strategies (`U3` generalisation of `Table 3.7`) |
| `[external: CWE]` exploitability triage, `[external: taint]` sink policy, `[external: sanitizer]` bypass auditing | `ppa-cyber-vulnerability-analysis` | Security policy layer consuming `CFA` call graphs (`BKL-008`) |

## 2. Procedure 1: Specify and Lower 0-CFA into Conditional Subset Constraints (Sections 3.1-3.4.1)

Execute these steps when building an AST-based closure, callback, or function-pointer resolver
[PPA §3.3, p. 168] (book p. 168; PDF p. 186) [PPA §3.4, p. 173] (book p. 173; PDF p. 191):

1. **Normalise AST labels and alpha-rename distinct bindings (`G-U3a-02`, `G-U3a-03`, `G-U3b-22`, `BKL-051`)**:
   - Assign a distinct label `ℓ ∈ Lab_⋆` to every subexpression `e = t^ℓ` (do *not* wrap parentheses in extra
     labels, and desugar multi-binding `let` blocks into nested single-binding `let x = e₁ in e₂`).
   - **Precondition check**: Resolve every bound variable (`fn x`, `fun f x`, `let x`) to a unique symbol ID
     (`α`-renaming [external]).
   - *Violation symptom*: Unrelated local variables named `x` share one `ρ̂(x)`, causing dynamic-scoping
     cross-talk even on non-polymorphic code (`Concluding Remarks`, `p. 199`, `BKL-059`)
     [PPA Chapter 3 Concluding Remarks, p. 199] (book p. 199; PDF p. 217).
2. **Pass `POLARITY_GATE` and separate specification (`gfp`) from solving (`lfp`) (`G-U3a-06`, `G-U3a-07`, `G-U3a-16`)**:
   - Declare may-polarity: `Val̂_⋆ = 𝒫(Term_⋆)` ordered by `⊆` (`⊥ = ∅`, `⊤ = Term_⋆`, join `⋃`, meet `⋂`) over
     product lattice `Cachê_⋆ × Env̂_⋆` (`(Lab_⋆ → Val̂_⋆) × (Var_⋆ → Val̂_⋆)`).
   - **Precondition check**: Never define or verify acceptability on cyclic call graphs via inductive witness
     trees (`lfp(𝒬)`); acceptability is coinductive (`⊨ = gfp(𝒬)`, `§3.1.2`), while the solver
     computes the least solution `lfp(F_⋆)` (`Proposition 3.22`) [PPA §3.1.2, p. 151] (book p. 151; PDF p. 169).
   - *Violation symptom*: Inductive checkers reject valid self-applicable programs: for the `Ω`-style `e_⋆`
     the inductive `⊨'` admits *zero* acceptable models (`∅`, `Proposition 3.16`) [PPA Proposition 3.16, p. 165] (book p. 165; PDF p. 183);
     for recursive `loop` the book only exhibits the circular obligation [PPA Example 3.6, p. 151] (book p. 151; PDF p. 169).
3. **Intern finite `Term_⋆` to enforce `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)` (`G-U3a-19`, `G-U3b-26`)**:
   - Pre-scan `e_⋆` once to index all `fn x => t₀^{ℓ₀}` and `fun f x => t₀^{ℓ₀}` subterms into a dense table
     `0 .. |Term_⋆|-1` (`|Term_⋆| ≤ n`), storing *unlabelled* `Term_⋆` entries (never `Exp` with outer labels!).
   - **Precondition check**: Ensure `Val̂_⋆` stores `Term_⋆` rather than `Exp` (`Exercise 3.6`) and restricts
     all sets to `Term_⋆` (`Propositions 3.18` and `3.21`) [PPA Proposition 3.18, p. 172] (book p. 172; PDF p. 190).
   - *Violation symptom*: Storing labelled `Exp` breaks `[bind₂]` relabelling soundness (`Fact 3.11`, `G-U3b-26`);
     admitting external terms outside `Term_⋆` without stubbing their bodies breaks `⊨_s ⇒ ⊨` (`Exercise 3.10`).
4. **Choose syntax-directed lowering (`Table 3.6`), reachability gating (`Mini Project 3.1`), or lazy expansion (`[9]`)**:
   - **Standard whole-AST emission (`Table 3.6`, `G-U3a-18`, `G-U3a-21`, `G-U3a-22`)**: Traverse `e_⋆` once,
     emitting `O(n)` unconditional constraints (`{t} ⊆ C(ℓ)`, `{fun ...} ⊆ r(f)`, `r(x) ⊆ C(ℓ)`, `C(ℓ₁) ⊆ r(x)`,
     `C(ℓ_i) ⊆ C(ℓ)`) and, at each `[app]` `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ`, `2 · |Term_⋆|` (`O(n²)` total) conditional
     constraints `{t} ⊆ C(ℓ₁) ⇒ C(ℓ₂) ⊆ r(x)` and `{t} ⊆ C(ℓ₁) ⇒ C(ℓ₀) ⊆ C(ℓ)`
     [PPA Table 3.6, p. 174] (book p. 174; PDF p. 192).
   - **Dead-code / large-bundle refinement (`G-U3b-24`, `G-U3b-25`, `BKL-055`)**: Because `Table 3.6` seeds
     `{t} ⊆ C(ℓ)` even inside dead lambdas (`Corollary 3.25` guarantees soundness `⊨ e_⋆`, not minimality on
     dead code!), either gate `[fn]`/`[fun]` by `on ∈ R̂(ℓ)` (`Mini Project 3.1`, seeding `{on} ⊆ R̂(ℓ_⋆)`) or
     use `[9]`'s (`[external: Aiken et al.]`) on-the-fly expansion (`p. 202`: emit `[app]` body/argument edges
     lazily only when a closure `t` actually arrives in `D[C(ℓ₁)]`!).
   - **Pass `MONOTONICITY_GATE` (`G-U3a-21`, `G-U3b-23`)**: Keep guards strictly of singleton form `{t} ⊆ rhs'`
     (or positive constructor projections `C^{-i}(S)`). While `S₁ ∩ S₂` preserves monotonicity, complement `¬S`
     forfeits the Tarski guarantee (`p. 201`, `BKL-059`); variable-LHS guards `(S₁ ⊆ S₂) ⇒ S₃` (a form the book
     lists as allowed) are antitone in `S₁` and so also break monotonicity `[derived]`.

## 3. Procedure 2: Implement the O(n^3) Dual-Observer Worklist Graph Solver (Section 3.4.2, Table 3.7)

Follow [constraint-generation-and-cubic-solver.md](./references/constraint-generation-and-cubic-solver.md) §3
when coding the constraint solver [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196):

1. **Allocate node arrays (`Step 1`)**: Create `Nodes = {C(ℓ) | ℓ ∈ Lab_⋆} ∪ {r(x) | x ∈ Var_⋆}` (`O(n)` nodes),
   bitset array `D[q] := ∅`, adjacency list `E[q] := []`, and worklist `W := []`.
2. **Build constraint graph with mandatory dual registration (`Step 2`, `G-U3a-24`)**:
   - `{t} ⊆ p`: call `add(p, {t})`.
   - `p₁ ⊆ p₂`: append to `E[p₁]`.
   - `{t} ⊆ p ⇒ p₁ ⊆ p₂`: append to **BOTH `E[p₁]` AND `E[p]`** (deduplicating if `p = p₁`).
   - **Precondition check (`DUAL_OBSERVER_CHECK`)**: Verify unit tests cover *both* arrival orders: (a) `t`
     reaches `D[p]` before `D[p₁]` populates, and (b) `D[p₁]` populates *before* `t` reaches `D[p]`!
   - *Violation symptom*: Omitting `E[p]` silently drops call arguments/returns whenever argument node `p₁` is
     popped (and never changes again) *before* the operator closure `t` reaches `D[p]` during `Step 3`.
     `Example 3.23`/`Figure 3.5` **cannot** expose this (Step 2 already seeds `id_x ∈ D[C(2)]`, so the
     `E[p₁]`-only trace is identical); keep it only as the baseline trace [PPA Figure 3.5, p. 180] (book p. 180; PDF p. 198).
     Witness `[derived]`: `(let f = (fn x => x^1)^2 in (f^3 (fn y => y^4)^5)^6)^7`: `id_x` reaches `D[C(3)]` only in
     Step 3 via `C(2) ⊆ r(f) ⊆ C(3)`; with LIFO `W` popping `C(5)` first, an `E[p₁]`-only solver ends with
     `r(x) = C(1) = C(6) = C(7) = ∅` instead of `{id_y}`. Run both seeding orders.
3. **Iterate to fixed point in true `O(n^3)` elementary time (`Step 3`, `CONVERGENCE_GATE`, `G-U3a-25`, `BKL-055`)**:
   - **Precondition check**: Finiteness of `Term_⋆`, `Lab_⋆`, `Var_⋆` guarantees termination (`Proposition 3.24`:
     each `D[q]` grows "a finite number of times") [PPA Proposition 3.24, p. 180] (book p. 180; PDF p. 198); the
     `≤ n` enlargements-per-node bound is the complexity paragraph's [PPA §3.4.2, p. 181] (book p. 181; PDF p. 199).
   - **Avoid the `O(n^4)` scalar-union trap**: `Table 3.7`'s `add(p₂, D[p₁])` executes `O(n^3)` edge traversals
     (`p. 181`), which degrades to `O(n^4)` elementary operations if `D[p₁]` is scanned as a list on every pop!
     Either represent `D[q]` as fixed-width bitsets (`O(n^4 / w)`) or push *differential `(q, t)` pairs* onto `W`
     (installing active edge `p₁ → p₂` once when `(p, t)` pops, and forwarding single `t` in `O(1)` bitset lookup
     when `(p₁, t)` pops) for exact **`O(n^3)`** elementary operations [external].
   - **Audit open-system / external-code boundaries (`p. 182`, `BKL-008`, `G-U3a-26`)**:
     - Book basis: for an open system `e_∘` using an unspecified library `e_⋆`, `(Ĉ, ρ̂) ⊨ e_⋆` lets `e_⋆` be
       replaced by any `e'_⋆` with `(Ĉ, ρ̂) ⊨ e'_⋆` [PPA §3.4.2, p. 182] (book p. 182; PDF p. 200).
     - Engineering recipe `[derived]` `[external]`: for unanalysed host APIs, FFI imports, reflection, or
       deserialization hooks, insert a stub `e_⋆` that invokes every escaping closure with conservative argument
       tokens and returns all externally reachable callbacks.
     - *Violation symptom*: Soundness holds only for replacements `e'_⋆` satisfying `(Ĉ, ρ̂)`'s clauses without
       label/variable clashes; unmodelled callbacks yield silent false negatives in reachability/CFI [external] scans.
4. **Enforce solver resource & call-graph audit budgets (`p. 181`, `Concluding Remarks`, `BKL-008`)**:
   - Guard whole-bundle `0-CFA` / `k`-CFA passes with per-node set-cardinality caps or context-fallback switches
     so adversarial / bundler-generated dynamic dispatch (`|Term_⋆| = Θ(n)`) cannot trigger `Θ(n^3)` or
     `[external: DEXPTIME]` scanner denial-of-service [external: CWE-400] [PPA §3.4.2, p. 181] (book p. 181; PDF p. 199).
   - Emit explicit `UNRESOLVED_OPEN_CALL` diagnostics at every call site whose `Ĉ(ℓ₁)` reaches an external
     deserialization, `eval`, or native FFI placeholder (`[external]`, `BKL-008`) rather than reporting `Ĉ(ℓ₁) = ∅`.

## 4. Procedure 3: Couple Data Flow Domains Online vs Staged (Section 3.5, Mini Projects 3.2 & 3.4)

Use this workflow when combining closure resolution with abstract constants, signs, algebraic constructors, or
mutable references ([polyvariant-kcfa-cpa-and-dfa.md](./references/polyvariant-kcfa-cpa-and-dfa.md) §§1, 5):

1. **Decide online co-iteration (`⊨_d` / `⊨_D`) vs two-phase staging (`⊨'_D`) (`G-U3b-04`, `G-U3b-09`, `BKL-056`)**:
   - Choose **online co-iteration** (`Tables 3.8-3.9`) when branch conditions guard function returns or dispatch
     tables (`Examples 3.27 / 3.30 / 3.31`: pruning `else` keeps `Ĉ(7) = ∅`, `Ĉ(8) = Ĉ(12) = {fn y => y^4}`,
     `D̂(15) = {0}` instead of polluting with dead `fn z => 25^6` and `D̂(15) = {0, +}`)
     [PPA Table 3.8, p. 184] (book p. 184; PDF p. 202)
     [PPA Example 3.31, p. 189] (book p. 189; PDF p. 207). Remember `(Ĉ, ρ̂)` from `⊨_d`/`⊨_D` need **not**
     satisfy pure `Table 3.1` `⊨` on pruned dead branches (`G-U3b-04`).
   - Choose **staged `⊨'_D`** (run `0-CFA` first, then `DFA` over the fixed call graph) only when call targets do
     not depend on data values and modular pass separation outweighs dead-branch precision (`p. 189`).
2. **Verify `CONVERGENCE_GATE` and strictness on the data domain (`G-U3b-03`, `G-U3b-05..08`, `BKL-056`)**:
   - **Precondition check 1 (`ACC`)**: For `Table 3.8` (`Val̂_d = 𝒫(Term ∪ Data)`), `Data` **must be finite**;
     for `Table 3.9` (`D̂ : Lab → L`), `L` **must satisfy `ACC`** (otherwise switch to `ppa-abstract-interpretation`
     and insert widening `∇`) [PPA §3.5.2, p. 187] (book p. 187; PDF p. 205).
   - **Precondition check 2 (Boolean branch guard soundness, `G-U3b-08`)**: Only use `Table 3.9`'s literal test
     `ι_true ⊑ D̂(ℓ₀)` when `ι_true` is an *atom* covering a single truth value (`{tt}` in `Example 3.29`)! If a
     language treats all non-zero integers as truthy (`ι_true = ⊤_Z`), test overlap `D̂(ℓ₀) ⊓ ι_true ≠ ⊥` instead.
     *Violation symptom*: Singleton `D̂(ℓ₀) = 1` fails `⊤_Z ⊑ 1` and unsoundly drops live `then` branches!
   - **Precondition check 3 (`⊥`-strict operators, `G-U3b-07`)**: In product lattices like
     `Z_⊥^⊤ × 𝒫({tt, ff})` (`Example 3.29`), binary `f_+` must check `z₁ = ⊥ or z₂ = ⊥ ↦ (⊥, ∅)` *before* `⊤`,
     and `Table 3.8` `op̂` must intersect operands with `Data` (`v̂_i ∩ Data`) so closures do not crash `d_op`.
3. **Enforce finiteness and `STRONG_UPDATE_GATE` on constructors and heap refs (`G-U3b-26`, `G-U3b-27`, `BKL-060`, `BKL-061`)**:
   - For algebraic constructors `C(e₁, ···, e_n)` (`Mini Project 3.2`), use the book's flat, finite, label-indexed
     domain `Val̂ = 𝒫(Term ∪ {C(ℓ₁, ···, ℓ_n) | C ∈ Constr, ℓᵢ ∈ Lab})` (`ℓᵢ` = creation point of component `i`;
     no nesting, finite over `Lab_⋆`) for the syntax-directed (`Table 3.5`) and constraint (`Tables 3.6/3.7`)
     analogues [PPA Mini Project 3.2, p. 203] (book p. 203; PDF p. 221). `Fact 3.11` bears only on the "more
     ambitious" open question of an abstract (`Table 3.1`) analogue, not on these two analyses.
   - For mutable references (`(new_π x := e₁ in e₂)^ℓ | (! x)^ℓ | (x := e₀)^ℓ | (e₁ ; e₂)^ℓ`, `me : Var → Pnt`,
     `Mini Project 3.4`, `pp. 204-205`), `π ∈ Pnt` abstracts unbounded heap cells per allocation site, so
     `[assign]` **must perform weak update** (`[external: weak update]`) merging new closures into `Ŝ_•(ℓ)(p)`
     while copying unaffected sites `p'`, unless **both** per-program-point local abstract stores and abstract
     reference counts prove singleton allocation (`p. 200` `[133]`, `strong update` [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134), `BKL-061`).

## 5. Procedure 4: Select Polyvariant Context Sensitivity — 0-CFA vs Uniform k-CFA vs Polynomial k-CFA vs CPA (Section 3.6)

When monovariant `0-CFA` smears closures across callers (`Example 3.32`), select the context domain `Δ` from
[polyvariant-kcfa-cpa-and-dfa.md](./references/polyvariant-kcfa-cpa-and-dfa.md) §§2-4 (`BKL-007`):

1. **Match `Δ` and closure representation to language idioms (`G-U3b-10`, `G-U3b-11`, `G-U3b-15..17`, `G-U3b-21`)**:
   - **Stay at `0-CFA` (`O(n^3)`)** when functions are mostly monomorphic or `let`-cloning (`Example 3.33`) /
     type-directed filtering suffices.
   - **Choose contexts-only `Val̂ = 𝒫(Term × Δ)` (`Δ = Lab^{≤k}`; polynomial lattice height, "closely related to"
     polynomial `k`-CFA, which is `O(n^6)` at `k = 1`, `p. 195`) or flat
     `m`-CFA `[external]` (`Val̂ = 𝒫(Term)`)** when worst-case polynomial bounds are mandatory or functions lack
     deep curried free-variable capture (e.g. first-order / flat-closure modules, `Exercise 3.16`).
   - **Choose Uniform `k`-CFA (`Table 3.10`, `Cachê = (Lab × Δ) → Val̂`, `Val̂ = 𝒫(Term × CEnv)`) or standard `k`-CFA
     (Shivers `[156, 157, 158]` [PPA Chapter 3 Concluding Remarks, p. 198] (book p. 198; PDF p. 216), `Cachê = (Lab × CEnv) → Val̂`, `Val̂ = 𝒫(Term × CEnv)`)** when
     higher-order wrappers capture free variables in distinct call chains (`Example 3.34`), *budgeting* solver
     timeouts for exponential **`[external: DEXPTIME]` (`|Val̂|` height `O(n · n^p)`) worst-case** (`BKL-007`), even
     though `1-CFA` often runs faster than `0-CFA` in practice by pruning spurious edges (`[80]`, `G-U3b-16`). For
     direct self-recursion, compress stuttering call strings (`Exercise 3.15`, `G-U3b-29`) so recursive loops do not
     flush callers!
   - **Choose `CPA` (`§3.6.2`, `[2]` `[external: Agesen]`, `Δ = Term^m`) or OO receiver sensitivity [external] (`p. 199`)**
     when polymorphism depends on *argument kinds/classes* rather than call-site stack depth (`U5` counterpart to
     `§2.5.5` small assumption sets) [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215).
2. **Audit the four implementation traps in `Table 3.10` and `CPA` (`G-U3b-12..14`, `G-U3b-18..20`, `BKL-057`, `BKL-058`)**:
   - **`[var]` lexical contour & `ce₀` finiteness (`G-U3b-12`, `BKL-057`)**: Look up `ρ̂(x, ce(x))` using `x`'s
     captured birth contour `ce(x)` (never current `δ`), and implement `CEnv` as finite partial maps `ce | FV(...)`
     (`ce₀ = []` in `Example 3.34`) rather than total functions `Var → Δ` (`p. 191`).
   - **`[app]` vs `[let]` contour push (`G-U3b-13`)**: Push the **application's outer label `ℓ`**
     (`δ₀ = ⌈δ, ℓ⌉_k`, not `ℓ₁`!) and update the **closure's captured `ce₀`**, while keeping `δ` **unchanged**
     across `[let]` (`ce' = ce[x ↦ δ]`) [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210).
   - **Corrected `CPA` `[app]` arg/syntax binding (`G-U3b-18`, `BKL-058`)**: Propagate body return `Ĉ(ℓ_b, δ_b) ⊆ Ĉ(ℓ, δ)`
     under `δ_b = (t'₁, ..., t'_m)`, and bind **`{δ_b} ⊆ ρ̂(x₁, δ_b) × ··· × ρ̂(x_m, δ_b)`** (adding `, δ_b` omitted on
     `p. 197`, plus closing `)` before `^ℓ`)!
   - **`CPA` empty-argument & template memoisation (`G-U3b-19`, `G-U3b-20`)**: Populate base-type tokens in
     `Ĉ(ℓ_j, δ)` (so non-function arguments like `5` do not make `Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ) = ∅`!) and memoise
     `(fn ..., δ_b)` into a shared **template pool** with lazy product expansion (`pp. 197-198`).

## 6. Verification Oracles, Symptom-to-Root-Cause Debugging Table, and Anti-Degradation Gates

### Golden Regression Oracles (Mandatory Unit Tests)

1. **`Examples 3.1 / 3.3 / 3.20 / 3.23` (`((fn x => x^1)^2 (fn y => y^3)^4)^5`)**: `8` constraints (`4`
   unconditional, `4` conditional); `Table 3.7` halts in `6` states (`Figure 3.5`) at `Ĉ(1)=Ĉ(4)=Ĉ(5)=ρ̂(x)={id_y}`,
   `Ĉ(2)={id_x}`, and **`Ĉ(3)=ρ̂(y)=∅`** [PPA Example 3.20, p. 175] (book p. 175; PDF p. 193).
2. **`Examples 3.2 / 3.4 / 3.6 / 3.17` (`loop`)**: Terminates without divergence; `Ĉ(1)=Ĉ(5)=Ĉ(6)=ρ̂(g)=ρ̂(f)={f}`,
   `Ĉ(3)={id_y}`, `Ĉ(8)={id_z}`, `ρ̂(x)={id_y, id_z}`, and **`Ĉ(4)=Ĉ(9)=Ĉ(10)=∅`**
   [PPA Example 3.4, p. 145] (book p. 145; PDF p. 163).
3. **`Examples 3.27 / 3.30 / 3.31` (Coupled `CFA + Signs`)**: Online `⊨_d`/`⊨_D` prunes dead `else` closure (`Ĉ(7)=∅`,
   `Ĉ(8)=Ĉ(12)={fn y => y^4}`, `D̂(15)={0}`), whereas staged `⊨'_D` leaks `fn z => 25^6` (`D̂(6)={+}`,
   `D̂(14)=D̂(15)={0, +}`, `δ̂(z)={0}`) [PPA Example 3.31, p. 189] (book p. 189; PDF p. 207).
4. **`Examples 3.32 / 3.34` (`(let f = (fn x => x^1)^2 in ((f^3 f^4)^5 (fn y => y^6)^7)^8)^9`)**: `0-CFA` smears
   `Ĉ_id(5) = Ĉ_id(8) = {id_x, id_y}`; Uniform `1-CFA` isolates `δ=5` vs `δ=8`, yielding exact
   **`Ĉ'_id(8, Λ) = Ĉ'_id(9, Λ) = {(fn y => y^6, ce₀)}`** (`ce₀ = []`) [PPA Example 3.34, p. 194] (book p. 194; PDF p. 212).

### Symptom-to-Root-Cause Debugging Matrix

| Observed Solver / Precision Symptom | Exact Root Cause & Gotcha Anchor | Fix |
| :--- | :--- | :--- |
| Call site drops argument/return flow depending on AST order | Conditional `{t} ⊆ p ⇒ p₁ ⊆ p₂` added to `E[p₁]` only, omitting `E[p]` (`G-U3a-24`) | Register in **both** `E[p₁]` and `E[p]` (`Table 3.7` Step 2) |
| Two sound passes produce incomparable call sets; unsure which bug | Neither need be buggy — acceptable solutions form a Moore family (`G-U3a-14`, `G-U3a-15`) | Intersect `Ĉ₁ ⊓ Ĉ₂`: if `⊭` fails on intersection, at least one pass is unsound (`Prop 3.13`) |
| `0-CFA` solver scales as `Θ(n^4)` on large bundles | Whole-set `add(p₂, D[p₁])` union + dead-lambda instantiation (`G-U3a-25`, `G-U3b-24`) | Use `(q, t)` delta worklist + bitsets + `Mini Project 3.1` `R̂` / `[9]` (`[external: Aiken et al.]`) lazy edges |
| Shadowed local `x` receives closures from outer `x` | No pre-pass `α`-renaming on `Env̂ = Var → Val̂` (`G-U3a-03`, `G-U3b-22`, `BKL-059`) | Index `Env̂` by unique binding/DefID rather than raw identifier string |
| `1-CFA` loses free-variable bindings inside closures | `[var]` looked up `ρ̂(x, δ)` instead of lexical `ρ̂(x, ce(x))` (`G-U3b-12`, `BKL-057`) | Thread `ce` inside `(Term × CEnv)` and query `ce(x)` in `(Ĉ, ρ̂) ⊨_δ^{ce}` |
| `1-CFA` loses caller precision across self-recursive helper | `⌈δ, ℓ⌉_k` flushes outer caller after `k` self-calls (`G-U3b-29`, `Exercise 3.15`) | Compress adjacent stuttering call labels (`[1, 2, 2, 1, 1] ↦ [2, 1]`) |
| `CPA` skips calls that pass integer/boolean literals | Empty `Ĉ(ℓ_j, δ) = ∅` collapses Cartesian product to `∅` (`G-U3b-19`, `BKL-058`) | Seed base-type tokens (`int`, `bool`) or `§3.5` `Data` in `Ĉ` |
| Coupled `CFA + CP` drops taken `then` branch on `if x` | Non-singleton `ι_true` tested via `ι_true ⊑ D̂(ℓ₀)` (`G-U3b-08`, `BKL-056`) | Replace `ι_true ⊑ D̂(ℓ₀)` with non-disjointness `D̂(ℓ₀) ⊓ ι_true ≠ ⊥` |
| Imperative `new_π` store loses prior pointees after `:=` | Destructive overwrite or missing local-store / reference-count invariant (`p. 200` `[133]`, `G-U3b-27`, `BKL-061`) | Weak-union RHS `e₀` values into target `p` and preserve unaffected `p'` across `Ŝ_∘`→`Ŝ_•` `[derived]` |

## 7. Compact Kernel Quick-Reference Card & Complexity Matrix

| Variant | Cache / Value Signature | Context `Δ` | Worst-Case Cost | Primary Book Anchor |
| :--- | :--- | :--- | :--- | :--- |
| **Abstract `0-CFA` (`⊨`)** | `Cachê = Lab → 𝒫(Term)`, `Env̂ = Var → 𝒫(Term)` | None (`monovariant`) | Spec only (`gfp(𝒬)`) | [PPA Table 3.1, p. 146] (book p. 146; PDF p. 164) |
| **Constraint `0-CFA` (`𝒞_⋆`)** | `Nodes = C(Lab_⋆) ∪ r(Var_⋆)`, `D[q] ⊆ Term_⋆` | None (`monovariant`) | **`O(n^3)`** steps (`O(n^2)` constraints) | [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196) |
| **Coupled `CFA + DFA` (`⊨_D`)** | `Ĉ : Lab → 𝒫(Term)`, `D̂ : Lab → L` (`ACC`) | None (online branch prune) | Finite iff `L` satisfies `ACC` | [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206) |
| **Uniform `k`-CFA** | `Val̂ = 𝒫(Term × CEnv)`, `Cachê = (Lab × Δ) → Val̂` | `Δ = Lab^{≤k}` + `ce ∈ CEnv` | **`[external: DEXPTIME]`** (`O(n · n^p)` height) | [PPA Table 3.10, p. 192] (book p. 192; PDF p. 210) |
| **Standard `k`-CFA (Shivers `[156, 157, 158]`, `p. 198`)** | `Val̂ = 𝒫(Term × CEnv)`, `Cachê = (Lab × CEnv) → Val̂` | `Δ = Lab^{≤k}` per free var | **`[external: DEXPTIME]`** for `k ≥ 1` (`BKL-007`) | [PPA §3.6.1, p. 193] (book p. 193; PDF p. 211) |
| **Contexts-only `𝒫(Term × Δ)` ("closely related to" polynomial `1-CFA`)** | `Val̂ = 𝒫(Term × Δ)`, `Cachê = (Lab × Δ) → Val̂` | `Δ = Lab^{≤1}` (`m`-CFA `[external]`: `𝒫(Term)`) | Polynomial height; polynomial `1-CFA` is **`O(n^6)`** (`p. 195`) | [PPA §3.6.1, p. 195] (book p. 195; PDF p. 213) |
| **`CPA` (`[2]` `[external: Agesen]`)** | `Val̂ = 𝒫(Term)`, `Cachê = (Lab × Δ) → Val̂` | `Δ = Term^m` (arg `m`-tuple) | Not stated by the book (`[external: exponential worst case; template sharing]`) | [PPA §3.6.2, p. 197] (book p. 197; PDF p. 215) |

## 8. Anti-Degradation Gates & Non-Blocking Chapter 3 Backlog (`ARCHITECTURE.md` §§6.4, 7)

### Anti-Degradation Gate Checklist

- **No `SMOOTHING_TRAP`**: Never state `⊨_s ⇔ ⊨` (`Proposition 3.18` gives `⊨_s ⇒ ⊨` only under `(Ĉ, ρ̂) ⊑ (Ĉ_⋆^⊤, ρ̂_⋆^⊤)`,
  `G-U3a-17`, `G-U3a-19`), never claim `(Ĉ, ρ̂)` from `⊨_d`/`⊨_D` satisfies `Table 3.1` `⊨` (`G-U3b-04`), and
  never omit `Data` finiteness / `L` `ACC` (`G-U3b-05`) or `k-CFA` `[external: DEXPTIME]` cost (`BKL-007`).
- **No `SIGNATURE_DISTORTION`**: Keep `gfp(𝒬)` on acceptability vs `lfp(F_⋆)` on constraint solving (`G-U3a-07`),
  sans-serif syntactic `C(ℓ), r(x)` vs semantic `Ĉ(ℓ), ρ̂(x)` (`G-U3a-21`), `[app]` outer-label push `⌈δ, ℓ⌉_k`
  (`G-U3b-13`), and corrected `CPA` binding `{δ_b} ⊆ ρ̂(x₁, δ_b) × ··· × ρ̂(x_m, δ_b)` (`G-U3b-18`, `BKL-058`).
- **No `HALLUCINATED_SYMBOL`**: Verify formulas against rendered PDF pages rather than `ppa.pdf` OCR (`G-U3a-12`,
  `G-U3b-30`, `BKL-011`), and tag external names (`m`-CFA, Andersen, Datalog, CFI, object-sensitivity) `[external]`.

### Non-Blocking Source Errata & Edge-Case Pointers

- `BKL-007`: Uniform `k`-CFA / `1-CFA` exponential worst-case (`p. 195`) vs `O(n^6)` polynomial `1-CFA` and `CPA` templates.
- `BKL-008`: Closed-world `FUN` syntax vs reflection, FFI, dynamic loading, and deserialization `[external]` (`p. 182` open-system stubs required).
- `BKL-011`: `ppa.pdf` OCR erases fraction premises in `Tables 3.2-3.3`, `Fact 3.11` (`p. 160`), `Prop 3.24` (`p. 180`), and `Table 3.9` `[op]` (`p. 188`).
- `BKL-051`: `§3.1` multi-binding `let` sugar (`p. 142`), `Table 3.1`/`3.2` typos, `[let₂]` `FV(e₂)` (`p. 156`), and `[app_fun]` `[x ↦ v₂]` order (`p. 155`).
- `BKL-052`: `Fact 3.11` OCR erasure (`p. 160`), `[if₂,₃]`/`[bind₂]` outermost-label relabelling (`pp. 155-157`), and `Exercise 3.6` `Val̂ = 𝒫(Exp)` failure (`p. 206`).
- `BKL-053`: `Example 3.15` reuses `(Ĉ'_e, ρ̂'_e)` with a new acceptable table (`p. 164`); `Prop 3.16` writes `IExp_e` for `Exp_e` (`p. 165`).
- `BKL-054`: `§3.4.2` cites `Prop 3.18` instead of `3.19` (`p. 176`), writes `Cachê_⋆ × Val̂_⋆` (`p. 177`), and drops `_⋆` on `𝒞⟦e_⋆⟧` (`pp. 181-182`).
- `BKL-055`: `Table 3.7` whole-set `add(p₂, D[p₁])` costs `O(n^4)` without `(q, t)` deltas/bitsets, and `𝒞_⋆⟦e_⋆⟧` analyses dead lambdas.
- `BKL-056`: Coupled `⊨_d`/`⊨_D` (`Tables 3.8-3.9`) does not project to `Table 3.1` `⊨` on pruned branches, and `ι_true ⊑ D̂(ℓ₀)` requires singleton `ι_true`.
- `BKL-057`: `§3.6.1` `p. 191` defines total `CEnv = Var → Δ` vs finite partial `ce | FV(...)` (`ce₀ = []`); `Example 3.34` mis-cites `Example 3.33` (`p. 194`).
- `BKL-058`: `§3.6.2` `p. 197` `CPA` `[app]` omits `)` before `^ℓ` and `, δ_b` in `ρ̂(x_i, δ_b)`, `p. 198` writes `Δ = Term`, and empty args collapse to `∅`.
- `BKL-059`: Pure `0-CFA` collapses shadowed variable names (`p. 199`); set-constraint `¬S` and variable-LHS guards break monotonicity (`p. 201`).
- `BKL-060`: `Mini Project 3.1` (`p. 202`) prose line 10 writes `⊨_s` for `⊨'_s`; `Mini Project 3.2` (`p. 203`) embeds `ℓ_i` in `Val̂` (flat & finite for Tables 3.5–3.7; `Fact 3.11` concerns only the abstract-spec open question).
- `BKL-061`: `Mini Project 3.4` (`pp. 204-205`) leaves `[assign]` acceptability unprinted; singleton strong kill (`strong update` [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134)) needs local stores + ref counts (`p. 200` `[133]`).
- `BKL-062`: `Exercise 3.3` (`"cannot produced"`), `Exercise 3.4` (`(3.8)` non-upward-closure), `Exercise 3.16` (`f(x)= e`, `"defined in D"`), `Exercise 3.17` (`"Cartesian Production"`).
