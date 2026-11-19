---
name: ppa-types-effects-and-regions
description: Construct, verify, and debug annotated type systems, type and effect reconstruction algorithms, polarised subtyping rules, stack-based region inference translators, and Concurrent ML communication behaviours. Use when attaching flow annotations or latent effects onto typed functional IRs, implementing free-algebra unification W_CFA with inclusion constraints, checking reference or channel payload invariance, tracking uncaught exceptions under let-polymorphism, inferring lexical letregion placement via Observe masking, or ordering causal spawn/send/receive behaviours. Do not use for untyped closure call graphs (ppa-control-flow-and-constraints), imperative CFG equations or mutable pointer shape graphs (ppa-dataflow-and-slicing), infinite numeric domains with Galois widenings (ppa-abstract-interpretation), RPO/SCC solver queues (ppa-fixedpoint-solvers), exploitability threat audits (ppa-cyber-vulnerability-analysis), or Chapter 1 paradigm routing (ppa-program-analysis).
---

<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L2 procedural skill for Chapter 5 annotated types, effect reconstruction, subtyping, region inference, and communication behaviours. -->

# Annotated Types, Effect Reconstruction, Region Inference, and Behaviours

Actionable engineering workflows for designing, implementing, verifying, and debugging Chapter 5 Type and Effect
Systems ([PPA Chapter 5, p. 283] (book p. 283; PDF p. 300) through
[PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380)). Complete rule tables, side conditions, and proof
machinery live in the self-contained `L1` references:

- Annotated `⊢_UL`/`⊢_CFA`, `UCAI` equality, Natural Semantics `Theorem 5.9`, covariant `Typê[τ]` Moore families:
  [annotated-types-and-cfa-soundness.md](./references/annotated-types-and-cfa-soundness.md)
- Algorithms `𝒲_UL`/`𝒰_UL` & `𝒲_CFA`/`𝒰_CFA`, `SType`, closed-form `θ_A`, polarised subtyping `≤`, canonical `U8`:
  [inference-unification-and-subtyping.md](./references/inference-unification-and-subtyping.md)
- Side effects (`ref_ϖ`), exceptions (`β \ {s} = β`), stack-based regions (`[175, 176]`, `[external: Tofte–Talpin]`, `Observe`), CML behaviours (`Table 5.18`):
  [effects-exceptions-regions-and-behaviours.md](./references/effects-exceptions-regions-and-behaviours.md)
- Shared cross-chapter foundations and comparison anchors:
  [chapter-1-five-formulations.md](../ppa-program-analysis/references/chapter-1-five-formulations.md),
  [appendix-a-posets-lattices-fixed-points.md](../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md),
  [appendix-b-induction-and-coinduction.md](../ppa-program-analysis/references/appendix-b-induction-and-coinduction.md),
  [cfa-core-and-coinduction.md](../ppa-control-flow-and-constraints/references/cfa-core-and-coinduction.md),
  [constraint-generation-and-cubic-solver.md](../ppa-control-flow-and-constraints/references/constraint-generation-and-cubic-solver.md),
  [interprocedural-and-correctness.md](../ppa-dataflow-and-slicing/references/interprocedural-and-correctness.md), and
  [shape-analysis.md](../ppa-dataflow-and-slicing/references/shape-analysis.md).

## 1. Boundary Dispatch and Five-Axis Architecture Selection

Confirm that the target program has a static underlying type discipline (`TYPED_SUBSTRATE_GATE`) before choosing
Chapter 5 over untyped constraint or flow-graph frameworks:

| Task Signature | Target Skill | Reason |
| :--- | :--- | :--- |
| Paradigm selection (`DFA` vs `CFA` vs `AI` vs `Types`) or App A-C lattice/coinduction lemmas | `ppa-program-analysis` (router) | Master router arbitrates across Chapters 1-6 |
| Annotated types (`⊢_CFA`), `𝒲_CFA`/`SType`, `ref_ϖ` effects, `handle` masking, `letregion`/`Observe`, CML behaviours, units/BTA | **This skill (`ppa-types-effects-and-regions`)** | Core Chapter 5 type-and-effect domain (`§§5.1–5.5`) |
| Untyped higher-order closures (`fn x => x x`), `k`-CFA contours, `[2]` `[external: Agesen]` `CPA`, `Table 3.7` cubic solver | `ppa-control-flow-and-constraints` | `⊢_UL` occurs check rejects untyped idioms (`G-U5a-01`, `U8`) |
| Imperative `WHILE` `AE`/`RD`/`VB`/`LV`, `ud`/`du` slicing, or flow-sensitive mutable `SG = (S, H, is)` destructive updates | `ppa-dataflow-and-slicing` | `§5.4.3` regions use lexical bulk pop rather than per-cell `kill_{x.sel}` |
| Infinite-height numeric domains (`Interval`, relational `⊗`), Galois connections `(α, γ)`, widening `∇` / narrowing `Δ` | `ppa-abstract-interpretation` | Unbounded chains without `ACC` (`Mini Project 5.4`, `G-U5b-24`) need Ch 4 |
| Worklist priority queues, reverse postorder (`RPO`), strong components (`SCC`), `d(G_S, T) + 3` pass bounds | `ppa-fixedpoint-solvers` | Chapter 6 optimises general constraint iteration schedules |
| End-to-end exploitability triage, `[external: HTTP-to-SQL taint policies, sanitizer bypass auditing]` | `ppa-cyber-vulnerability-analysis` | Security threat modelling consuming effect/capability summaries |

### Five-Axis Design Decision Matrix (Concluding Remarks, pp. 350-352)

Select the minimum mechanism tier needed for precision (`[PPA Chapter 5 Concluding Remarks, p. 351] (book p. 351; PDF p. 368)`):

| Design Axis | Precision Gain | Solver Cost & Decidability Impact |
| :--- | :--- | :--- |
| **1. Subeffecting only (`§5.1`, `Table 5.2`)** | Mandatory for `Fact 5.6(ii)` conservative extension; suffers monomorphic argument smearing (`Example 5.5`) | Near-linear Robinson unification `𝒰_CFA` + `O(\|C\|)` bucket `θ_A` (zero fixed-point iteration) |
| **2. Shape-conformant subtyping `≤` (`§5.4.1`)** | Eliminates caller-to-argument smearing (`Example 5.27`), matching `0-CFA` (`U8`); breaks unconstrained Moore families (`Exercise 5.9`) | Two-stage `[external: HM]` + `O(n³)` directed `[external: Horn]` set-inclusion closure; requires `ref_ϖ`/`chan` payload invariance |
| **3. `let`-polymorphism `∀ζ⃗. τ̂` (`§5.4.2`)** | Isolates higher-order combinator call sites (`Example 5.30` `map`/`apply`) without monomorphic merging | Two-stage when effects are *restricted* (no types in `φ`); coupled `[gen]` downwards closure when `φ` embeds types (`§5.5`) |
| **4. Effect/region polymorphic recursion `∀β⃗,[ϱ⃗]` (`§5.4.3`)** | Separates per-invocation recursive allocations (`letregion` inside loops) | Decidable **only** by excluding `α⃗` in `[fun]`; `Algorithm R` is syntactically sound, **not** complete (`p. 352`) |
| **5. Causal behaviours `φ₁; φ₂`, `rec β.φ` (`§5.5`)** | Preserves temporal send/receive/spawn order and synchronous `[external: deadlocks]` (`Table 5.18`) | Requires positive `β` polarity, coinductive `[external: (φ₁, φ₂) pair memoisation]`, and right-only `;` over `+` distributivity |

### Variance Polarity Audit Matrix (`Section 5.2.3`, `Section 5.4.1`, `Table 5.18`)

Verify every type/effect constructor's slot variance before writing unification or subtyping constraints
([PPA §5.2.3, p. 298] (book p. 298; PDF p. 315) [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341)
[PPA Table 5.18, p. 348] (book p. 348; PDF p. 365)):

| Construct / Judgement Relation | Domain / Payload Slot | Effect / Region Slot | Codomain Slot | Violation Consequence |
| :--- | :--- | :--- | :--- | :--- |
| Fibre precision `(τ̂₁ --φ--> τ̂₂) ⊑ (τ̂'₁ --φ'--> τ̂'₂)` | **Covariant** (`τ̂₁ ⊑ τ̂'₁`) | Covariant (`φ ⊆ φ'`) | **Covariant** (`τ̂₂ ⊑ τ̂'₂`) | Needed for `Proposition 5.12` Moore family; unsound as `[sub]` |
| Arrow subtype `(τ̂₁ →^φ τ̂₂) ≤ (τ̂'₁ →^{φ'} τ̂'₂)` | **Contravariant** (`τ̂'₁ ≤ τ̂₁`) | Covariant (`φ ⊆ φ'`) | **Covariant** (`τ̂₂ ≤ τ̂'₂`) | Covariant domain causes `[external: CWE-843]` callback confusion |
| Region arrow `(τ̂₁@r₁ →^{β.φ} τ̂₂@r₂) ≤ ···` | **Contravariant** (`τ̂'₁ ≤ τ̂₁`) | `r₁=r'₁, r₂=r'₂` **invariant**; `β∪φ ⊆ β'∪φ'` | **Covariant** (`τ̂₂ ≤ τ̂'₂`) | `Reg_RI` has no subset order (`F-U5b-06`, `G-U5b-17`) |
| Mutable cell `ref_ϖ τ̂ ≤ ref_{ϖ'} τ̂'` | **Invariant** (`τ̂ ≤ τ̂' ∧ τ̂' ≤ τ̂`) | Covariant (`ϖ ⊆ ϖ'`) | *(n/a)* | Write-side alias corruption (`!x` cov + `x:=e` contrav) |
| CML channel `τ̂ chan r ≤ τ̂' chan r'` | **Invariant** (`τ̂ ≤ τ̂' ∧ τ̂' ≤ τ̂`) | Covariant (`r ⊆ r'`) | *(n/a)* | Cross-process `[external: CWE-843]` payload mismatch |
| CML output `r₁!τ̂₁ ⊑ r₂!τ̂₂` vs input `r₁?τ̂₁ ⊑ r₂?τ̂₂` | `!`: **Covariant** (`τ̂₁ ≤ τ̂₂`); `?`: **Contravariant** (`τ̂₂ ≤ τ̂₁`) | Covariant (`r₁ ⊆ r₂`) | *(n/a)* | Dual producer/consumer safety (`[external: Session Types]`) |
| Recursive behaviour `rec β.φ` (`Table 5.18`) | `β` **strictly positive** only | Covariant (`φ₁ ⊑ φ₂`) | *(n/a)* | Negative `β` inside `r?τ̂`/`chan` breaks monotonicity (`F-U5b-09`) |

### Two-Stage vs Coupled Solver Architecture Checklist (`pp. 351-352`)

1. **Test `RESTRICTED_EFFECT_GATE` (`p. 351`)**: Does `Ann_*` mention any type `τ̂` or type variable `α`?
   - **No (`⊢_CFA`, `⊢_SE`, `⊢_ES`, `⊢_RI`)**: Run **Stage 1** off-the-shelf Hindley/Milner type
     inference first; decorate the typed AST with fresh `AVar`/`RVar` nodes; run **Stage 2** set/region solver.
   - **Yes (`⊢_CA` `'a chan r`, polymorphic `ref` creation)**: Couple unification with constraint closure in one
     pass and block `[gen]` on the **downwards closure** of `FV(Γ̂) ∪ FV(φ)` (`Example 5.36`, `G-U5b-12`).
2. **Differential-check inference outputs (`Mini Project 5.3`)**: Implement a small declarative checker for
   `θ_G(θ Γ̂) ⊢_* e : θ_G τ̂ & θ_G φ` and assert it passes on every `𝒲_*` test case (`Theorem 5.20`).

## 2. Procedure 1: Design an Annotated Type System and Prove Soundness (Sections 5.1-5.2)

Follow these steps when attaching value-flow or qualifier annotations (`⊢_CFA`, `Mini Project 5.2`) onto an
underlying type system [PPA §5.1, p. 283] (book p. 283; PDF p. 300) [PPA §5.2, p. 291] (book p. 291; PDF p. 308):

1. **Enforce `TYPED_SUBSTRATE_GATE` (`§5.1.1`, `Table 5.1`, `G-U5a-01..04`)**:
   - Verify target expressions type-check under `Γ ⊢_UL e : τ` (`Table 5.1`) with rightmost-wins lookup `Γ(x)` and
     distinct recursive binders `f ≠ x` in `fun_π f x => e₀` (`G-U5a-09`). If untyped self-application
     (`fn_X x => x x`) or dynamic casts must be analysed, route to `ppa-control-flow-and-constraints`.
   - Attach program points `π ∈ Pnt` to abstraction/constructor sites rather than labelling every subexpression,
     and verify constants/operators have base-only signatures `τ_c, τ¹_op, τ²_op, τ_op ∈ {int, bool}` (`G-U5a-03`).
   - Record whether `let x = e₁ in e₂` is monomorphic (`§§5.1–5.3`, identical to `(fn_π x => e₂) e₁`, `G-U5a-04`;
     `[external: Church-style]` determinism in `Exercise 5.2`) or polymorphic (`§§5.4.2–5.5`).
2. **Embed subeffecting and quotient by `UCAI` (`Table 5.2`, `Table 5.3`, `Fact 5.6`, `G-U5a-05..07`)**:
   - Define erasure `⌊·⌋ : Typê → Type` and axiomatise set annotations `φ ∈ Ann` modulo `UCAI` (`Table 5.3`;
     direct inclusion axioms in `Exercise 5.3`).
   - **Never emit exact `{π}` alone on `[fn]`/`[fun]`**: write `τ̂_x --{π}∪φ--> τ̂₀` (or include `[sub]`) so
     `Fact 5.6(ii)` conservative extension holds (`Example 5.5` `loop` is untypable without `∪ φ`, `G-U5a-05`).
   - Persist an **AST-node side table** of resolved subexpression types (`Example 5.4`, `Exercise* 5.4` `(5.2)`,
     `G-U5a-02`): the root type of `main : int` discards internal call-site arrow sets! Add lower arrow labels
     `τ̂₁ →^φ_ψ τ̂₂` (`ψ ∈ LAnn`, `Exercise 5.6`) when call-site provenance `(e₁ e₂)^ℓ` is also required.
   - Remember equational `[app]` without subtyping causes **bidirectional smearing** (`fn_Y` and `fn_Z` both
     receive `{Y, Z}` in `Example 5.5` and `Exercise 5.1`, `G-U5a-06`) and forces dead `if` branches to type-check (`G-U5a-07`).
3. **Orient the fibre lattice covariantly (`SUBEFFECTING_VARIANCE_GATE`, `§5.2.3`, `Proposition 5.12`)**:
   - Finitise `Pnt` to `Pnt_⋆` (or enlarge `Ann` to `𝒫(Pnt)`, `G-U5a-13`) so `⊓ ∅ = Pnt` exists.
   - Order `Typê[τ] = {τ̂ | ⌊τ̂⌋ = τ}` **covariantly in BOTH domain and codomain** (`τ̂₁ ⊑ τ̂'₁ ∧ φ ⊆ φ' ∧ τ̂₂ ⊑ τ̂'₂`,
     `G-U5a-12`) to make `JUDG_CFA[Γ ⊢_UL e : τ]` a **Moore family** (`Proposition 5.12`) [PPA Proposition 5.12, p. 299] (book p. 299; PDF p. 316).
   - **Do NOT substitute contravariant `≤` into `Proposition 5.12` (`G-U5b-07`, `Exercise 5.9`)**: meeting valid
     typings of `fn_X x => x` under contravariant `≤` yields unsound `(int →^⊤ int) →^{\{X\}} (int →^∅ int)`!
4. **Audit big-step vs small-step soundness (`Table 5.4`, `Theorem 5.9`, `BKL-004`, `G-U5a-08..11`)**:
   - In `Table 5.4` closed Natural Semantics (`FV(e) = ∅` avoids capture-avoiding `α`-renaming, `G-U5a-10`; `[fun]`
     unfolds one step inheriting `π`, `G-U5a-09`), prove `Lemma 5.11` via `Fact 5.10`, then `Theorem 5.9` (noting
     `Table 5.2` remains sound under call-by-name `Exercise 5.7`).
   - Use `[] ⊢_CFA e : τ̂₁ --∅--> τ̂₂` (`G-U5a-08`) or `𝒲_UL = (α_x → α₀, θ)` with `α_x ≠ α₀` (`Exercise* 5.10`) as
     sound static **non-termination certificates** (justifying dead-call `⊥_{τ̂₀}` in `Exercise 5.5`).
   - **Divergence firewall (`BKL-004`, `G-U5a-11`)**: Because diverging loops lack finite `⊢ e ⟶ v` trees (`(5.1)`
     on p. 294), `Theorem 5.9` is **vacuous** on event loops and daemons — switch to small-step SOS (`Tables 5.14–5.15`
     or Chapter 3 `Theorem 3.10`) whenever auditing non-terminating reactive code!

## 3. Procedure 2: Implement W_CFA Reconstruction and Two-Stage Subtyping (Sections 5.3-5.4)

Execute this workflow when building an automated type-and-effect inference engine (`Mini Project 5.3`)
[PPA §5.3.2, p. 306] (book p. 306; PDF p. 323) [PPA Chapter 5 Concluding Remarks, p. 351] (book p. 351; PDF p. 368):

1. **Factor non-free `Typê` into free-algebra `SType` + constraints `C` (`UNIFICATION_CONSTRAINT_GATE`, `G-U5a-15..17`)**:
   - Never run syntactic unification directly on `UCAI` set unions (`int --{π₁}∪{π₂}--> int`).
   - Restrict arrows in `SType` to single annotation variables `τ̂₁ --β--> τ̂₂` (`β ∈ AVar`), restrict simple
     substitutions `θ` to map `TVar → SType` and **`AVar → AVar` only**, and unify via `𝒰_CFA` (`Table 5.7`,
     `Fact 5.17`, `Exercise 5.8`), which fails **iff** `𝒰_UL(⌊τ̂₁⌋, ⌊τ̂₂⌋)` (`Table 5.6`) fails (`G-U5a-16`).
   - **Short-circuit trivial self-bindings (`G-U5a-17`)**: Return `id` whenever `α = τ̂` in `𝒰_UL`/`𝒰_CFA` or
     `β = β'` in `θ₀ = [β' ↦ β]` so imperative map/`[external: union-find]` chasers never loop.
2. **Thread retroactive substitutions across `Γ̂` and `C` (`Tables 5.5, 5.8`, `G-U5a-14, G-U5a-18..20, G-U5a-22`)**:
   - **Fix `Table 5.5`'s `if` bug (`F-U5a-04`, `G-U5a-14`)**: Always return `θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁ ∘ θ₀` (never omit
     `∘ θ₀`!), and keep hatted `τ̂₁` in `Table 5.8` `if` (`F-U5a-05`, `G-U5a-22`).
   - Apply every post-call `θ_i` to earlier constraint sets (`θ₃(θ₂ C₁) ∪ θ₃ C₂` in `[app]`;
     `θ₄(θ₃(θ₂(θ₁ C₀))) ∪ θ₄(θ₃(θ₂ C₁)) ∪ θ₄(θ₃ C₂)` in `[if]`), or coalesce `AVar` `[external: bitsets]` directly inside
     `[external: Tarjan union-find]` equivalence classes (`G-U5a-18`).
   - If standalone `[sub]` rules exist (`§5.4`), apply `Exercise 5.13` two-step **proof normalisation** (pushing
     subeffecting into axioms and `[fn]`/`[fun]`) before claiming `Theorem 5.21` syntactic completeness (`G-U5a-20`,
     `G-U5b-23`; remember `Theorem 5.20` needs intermediate ground extension `θ'_G`, `G-U5a-19`).
3. **Materialise ground validations `θ_G = θ_A ∘ θ_T` safely (`§5.3.4`, `Lemma 5.22`, `Corollary 5.23`, `G-U5a-21`)**:
   - For monomorphic `𝒲_CFA` (atomic `β ⊇ {π}` only), compute the exact least reductive solution in `Red`
     ([PPA §A.4, p. 402] (book p. 402; PDF p. 418)) in `O(|C|)` without fixed-point iteration:
     `θ_A β = {π | (β ⊇ {π}) ∈ C}` for `β ∈ AV(C)`, **AND default `θ_A β = ∅` for all unconstrained
     `β ∈ (AV(θ Γ̂) ∪ AV(τ̂)) \ AV(C)`** (`F-U5a-08`, `F-U5b-01`, `G-U5a-21`, `G-U5b-01`).
   - Instantiate leftover `α ∈ TVar` to `int` (or `∅`-annotated `⊥_{τ_α}`) per `Mini Project 5.3`.
4. **Upgrade to polarised subtyping (`§5.4.1`, `Concluding Remarks` `pp. 350–352`, `U8`)**:
   - Check **restricted-effects gate (`p. 351`, `G-U5b-12`)**: If effects carry **no types**, run Two-Stage
     Inference — Stage 1 solves Hindley/Milner underlying shapes; Stage 2 decomposes each
     `τ̂₁ ≤ τ̂₂` (`⌊τ̂₁⌋ = ⌊τ̂₂⌋`) into **contravariant** domain `τ̂'₁ ≤ τ̂₁`, **covariant** codomain/effect
     `τ̂₂ ≤ τ̂'₂ ∧ φ ⊆ φ'`, and **bidirectional invariant** mutable payloads (`G-U5b-05`, `G-U5b-22`), matching
     Chapter 3 `0-CFA` directional precision on well-typed `FUN` (`U8`, `Exercise* 5.4` `(5.2)`).

## 4. Procedure 3: Side Effects, Exception Masking, and Effect Polymorphism (Sections 5.4.1-5.4.2)

Apply this checklist when building stateful, exception-aware, or polymorphic effect passes
[PPA Table 5.9, p. 322] (book p. 322; PDF p. 339) [PPA Table 5.10, p. 328] (book p. 328; PDF p. 345):

1. **Audit evaluation strategy and latent arrow deferral (cf. `BKL-026`, `BKL-031`, `G-U5b-02..04`)**:
   - Confirm call-by-value semantics (`[con]`, `[var]`, `[fn]`, `[fun]` emit immediate `& ∅`, parking body effect
     `φ₀` on `τ̂_x →^{φ₀} τ̂₀` until operator `e₁` at `[app]` discharges `φ₁ ∪ φ₂ ∪ φ₀`; for CBN use `Exercise 5.12`;
     for store soundness use `Exercise 5.11`).
   - In `§5.4.1` (`Table 5.9`), keep `{new π}` **unmasked** on `new_π x := e₁ in e₂` exit (`G-U5b-03`), remember
     `ξ := e` returns `v` (`G-U5b-04`), and promote `new_π` to stack `let` whenever `π:= ∉ φ` (`Example 5.26`).
2. **Enforce mutable payload invariance (`SUBEFFECTING_VARIANCE_GATE`, `G-U5b-05`, `G-U5b-06`)**:
   - Require **both** `τ̂ ≤ τ̂'` **and** `τ̂' ≤ τ̂` alongside `ϖ ⊆ ϖ'` on `ref_ϖ τ̂ ≤ ref_{ϖ'} τ̂'` (and on
     `τ̂ chan r ≤ τ̂' chan r'` in `§5.5.1`). Never make mutable cells covariant (`[external: CWE-843]`).
   - Retain at least subeffecting or subtyping so conservative extension over `Table 5.1` holds (`G-U5b-06`).
3. **Enforce `β \ {s} = β` and `AV(φ₂) = ∅` in Exception Analysis (`Table 5.10`, `BKL-009`, `G-U5b-08..10`)**:
   - Model `raise s ∈ Val` short-circuiting (`G-U5b-08`), typing `[handle]` as `φ₁ ∪ (φ₂ \ {s})`.
   - **Never simplify `β \ {s}` to `∅` (`G-U5b-09`, `BKL-009`)**: keep **`β \ {s} = β`** (or add symbolic
     difference terms `φ \ {s}` to `Ann_ES`) so instantiating `β ↦ {s, s'}` at `[ins]` never drops `s'`!
   - Prune dead handler effect `φ₁` (`Exercise 5.14`, `G-U5b-10`) **iff BOTH `s ∉ φ₂` AND `AV(φ₂) = ∅`**.
4. **Enforce `GENERALISATION_CLOSURE_GATE` at `[gen]` (`BKL-009`, `Example 5.36`, `G-U5b-11`, `G-U5b-12`, `G-U5b-26`)**:
   - At `[gen]`, forbid quantifying any `ζ_i` free in **`Γ̂` OR `φ`** (`Example 5.36`: generalising `'a` across
     `channel_A : 'a chan {A} & 'a chan {A}` permits sending both `1` and `true`!).
   - Whenever effects embed types (*general effects*, `§5.5`, `p. 352`), compute forbidden variables across the
     **downwards closure** of `FV(Γ̂) ∪ FV(φ)` wrt the active constraint set (`G-U5b-12`), and define `σ̂ ≤ σ̂'` if
     lifting conclusions to schemes (`Exercise 5.15`, `F-U5b-13`, `G-U5b-26`).

## 5. Procedure 4: Region Inference (Section 5.4.3) and CML Behaviours (Section 5.5)

1. **Translate `FUN` to stack regions safely (`LEXICAL_REGION_ESCAPE_GATE`, `Figure 5.1`, `Tables 5.11–5.13`)**:
   - Box **all** runtime values (`int`, `bool`, closures) in `(rn, o)` (`G-U5b-13`): emit `{put r}` on `[con]`/`[fn]`,
     `{get r₀}` on `[if]`, `{get r₁, get r₂, put r}` on `[op]`, and **`{get r₁}`** (closure container!) on `[app]`.
   - Keep `r₁, r₂` invariant in `(τ̂₁ @ r₁) →^{β.φ} (τ̂₂ @ r₂)` subtyping and check `{rn⃗} ∩ dom(ς₁) = ∅` (`G-U5b-17`).
   - Keep `∀[]. τ̂` distinct from `τ̂` (`G-U5b-14`) so compound recursive closures emit `[place]` (`ee[θ ϱ⃗] at r'`
     + `{get r, put r'}`) via `[ins₂]`, and restrict `[fun]` polymorphic recursion to **`∀β⃗, [ϱ⃗]` excluding `α⃗`**
     for decidability (with an iteration/arity bound on `Algorithm R` since completeness fails, `G-U5b-15`).
   - Wrap `letregion ϱ⃗ in ee` (`Table 5.13` `[region]`, `G-U5b-16`) **iff** `φ' = Observe(Γ̂, τ̂, r)(φ)` **AND `ϱ⃗`
     occurs in `φ` AND `ϱ⃗ ∉ φ'`** (blocking `[external: CWE-416 arena UAF]`). If a recursive accumulator forces
     `r_in = r_out` (`[external: CWE-400]` leak), refactor to `[external: destination-passing]` regions or switch to `§2.6`
     flow-sensitive Shape Analysis (`ppa-dataflow-and-slicing`) when in-place cell mutation is required.
2. **Analyse Concurrent ML causal behaviours (`BEHAVIOUR_CAUSALITY_GATE`, `Figure 5.2`, `Tables 5.14–5.18`)**:
   - Use small-step contextual SOS (`Tables 5.14–5.15`, `p₁ ≠ p₂` synchronous `[comm]`), **omit `Observe` masking**
     so all channel actions stay globally visible (`G-U5b-18`), and brace singleton regions `{C}` (`G-U5b-21`).
   - Enforce `Table 5.18` variance & algebra (`G-U5b-19`, `G-U5b-20`): invariant `τ̂ chan r`, covariant `r!τ̂`,
     contravariant `r?τ̂`, **positive-only `β` in `rec β.φ`** (checked with coinductive `[external: pair memoisation]`), and
     **right-only distributivity** `(φ₁ + φ₂); φ₃ ≡ (φ₁; φ₃) + (φ₂; φ₃)` — **never** rewrite `φ₁; (φ₂ + φ₃)` to
     `(φ₁; φ₂) + (φ₁; φ₃)` or `[external: branching-time CWE-833 deadlocks]` disappear!

## 6. Procedure 5: Monotone Qualifier Lattices and Units of Measure (Mini Projects 5.1-5.5)

Execute this workflow when building domain-specific annotated type checkers (`pp. 353–359`)
[PPA Mini Project 5.4, p. 355] (book p. 355; PDF p. 372) [PPA Mini Project 5.5, p. 358] (book p. 358; PDF p. 375):

1. **Call-tracking & algebraic constructors (`Mini Projects 5.1–5.2`)**:
   - For call-tracking `Γ̂ ⊢_CT e : τ̂ & φ` (`5.1`), emit `{π}` on `[app]` / arrow discharge rather than `[fn]`
     creation; for pairs `τ̂₁ ×^φ τ̂₂` and lists `τ̂ list^φ` (`5.2`), attach `{π}` on `Pair_π`/`Cons_π`/`Nil_π` with
     built-in `∪ φ` subeffecting (`srt(Pair_A(n,m)) : int ×^{A,B} int`).
2. **Binding-time & security clearance lattices (`Mini Project 5.4`, `G-U5b-24`, cf. `BKL-030`)**:
   - Embed finite/ACC complete lattices (`S ⊑ D` or `C₁ ⊑ ··· ⊑ C_k`) onto base types (`int^l`, `bool^l`) with
     subeffecting/subtyping `l₁ ⊑ l₂`; join guard level `l₀` into conditional branches `l₀ ⊔ l₁ ⊔ l₂`, and add an
     explicit `[external: implicit-flow pc]` write guard (`pc ⊑ level(x)`) whenever mutable references (`§5.4.1`) are present.
3. **`[external: Abelian-group]` scales & `[external: affine-torsor]` origins (`Mini Project 5.5`, `G-U5b-25`)**:
   - Represent `num^{scale BASE base}` with **`[external: abelian-group]` unification** on `scale` (`meter.feet = feet.meter`,
     `scale.unit = scale`, `scale.scale^{-1} = unit`, solved via `[external: integer Gaussian/Hermite normal form]`,
     strictly stronger than idempotent `UCAI`) and **`[external: affine-torsor]` rules** on `base`:
     - Require `BASE none` on both operands of `*` (`σ = σ₁.σ₂`) and `/` (`σ = σ₁.(σ₂^{-1})`);
     - On `-`, map `β₁ = β₂` to `BASE none` (duration/offset), `β₂ = none` to `β₁`, else **`undefined`**;
     - On `+`, allow `β₁` if `β₂ = none` or `β₂` if `β₁ = none`, and **explicitly reject (`undefined`) when both
       `β₁ ≠ none` and `β₂ ≠ none`** (fixing `F-U5b-12`, preventing `[external: CWE-682]` Y2K/currency/unit errors).

## 7. Symptom-to-Mechanism Debugging Playbook

| Observed Symptom | Root Mechanism (`PPA` Reference) | Required Fix |
| :--- | :--- | :--- |
| Call-graph query on `main : int` returns empty callee sets | Only root type inspected; internal arrows discarded (`Example 5.4`, `G-U5a-02`) | Record resolved operator `τ̂₁` at every `[app]` node (`Exercise* 5.4` `(5.2)`) |
| `𝒲_UL` accepts ill-typed `if (b < 5) then 1 else 2` under `[b ↦ 'a]` | Printed `Table 5.5` `if` omits `∘ θ₀` (`F-U5a-04`, `G-U5a-14`) | Return `θ₄ ∘ θ₃ ∘ θ₂ ∘ θ₁ ∘ θ₀` as in `Table 5.8` |
| `𝒰_UL` / `𝒰_CFA` hangs on `α = τ` or `β = β'` | Self-binding `[α ↦ α]` / `[β ↦ β]` inserted into map (`G-U5a-17`) | Short-circuit identical variable bindings to `id` |
| Pretty-printer crashes on `fn_X x => x 1` after `𝒲_CFA` | Unconstrained `'1 ∉ AV(C)` is `undefined` in `θ_A` (`F-U5a-08`, `G-U5a-21`) | Default `θ_A β = ∅` on `(AV(θ Γ̂) ∪ AV(τ̂)) \ AV(C)` |
| Wrapper `(fn g => handle s as 0 in g 1)` hides uncaught `s'` | Symbolic `β \ {s}` simplified to `∅` before `[ins]` (`G-U5b-09`, `BKL-009`) | Enforce `β \ {s} = β` (or retain symbolic `φ \ {s}`) and guard `Exercise 5.14` with `AV(φ₂) = ∅` (`G-U5b-10`) |
| Polymorphic channel/ref allows mixed `int` and `bool` writes | `[gen]` checked `FV(Γ̂)` without `FV(φ)` or downwards closure (`Example 5.36`, `G-U5b-11..12`) | Forbid `ζ_i` in downwards closure of `FV(Γ̂) ∪ FV(φ)` (`BKL-009`) |
| `[external: Segfault]` / stuck `(rn, o)` read after `letregion` exit | Missing `{get r₁}` on `[app]` or `ϱ⃗ ∈ φ` guard in `[region]` (`G-U5b-13, G-U5b-16`) | Emit `{get r₁}` on closure call; check both `Observe` and `ϱ⃗ ∈ φ` |
| Behaviour checker loops or misses synchronous `[external: deadlock]` | Eager `rec β.φ` unfolding or illegal left-distributivity (`G-U5b-19, G-U5b-20`) | Use coinductive `[external: (φ₁, φ₂) pair memoisation]`; distribute `;` over `+` from right only |

## 8. Golden Regression Oracles and Anti-Degradation Sign-Off

Validate every Chapter 5 analyser or type/effect solver against these five canonical book witnesses:

1. **Oracle A — Whole-Tree `Ĉ(ℓ)` vs Bidirectional Smearing (`Examples 5.4, 5.5, 5.18, 5.19`)**:
   - On `((fn_X x => x¹)² (fn_Y y => y³)⁴)⁵`, assert `Ĉ(2) = (int --{Y}--> int) --{X}--> (int --{Y}--> int)` and
     `Ĉ(5) = int --{Y}--> int` (`G-U5a-02`).
   - On `loop` (`Examples 5.2, 5.19`), assert `𝒲_CFA` returns unconstrained `TVar` `'d` with
     `{'4 ⊇ {F}, '3 ⊇ {Y}, '3 ⊇ {Z}}` (merging `{Y, Z}` on the formal parameter arrow), so choosing
     `θ_T('d) = int --∅--> int` recovers `[] ⊢_CFA loop : int --∅--> int` (`G-U5a-06`, `G-U5a-08`).
2. **Oracle B — `Table 5.5` `∘ θ₀` Bug & Unconstrained `AVar` Default (`F-U5a-04, F-U5a-08`)**:
   - On `Γ = [b ↦ 'a]`, `e = if (b < 5) then 1 else 2`, assert `𝒲_UL` returns `θ('a) = int` (`G-U5a-14`).
   - On `[]`, `fn_X x => x 1`, assert `θ_G τ̂ = (int --∅--> int) --{X}--> int` with zero `undefined` lookups (`G-U5a-21`).
3. **Oracle C — Contravariant Subtyping vs Effect Polymorphism (`Examples 5.27, 5.30`, `Exercise 5.9`)**:
   - Verify `Example 5.27` keeps reader `int →^{!A} int` and writer `int →^{A:=} int` distinct under `≤` while
     rejecting `ref_{A} (int →^∅ int) ≤ ref_{A} (int →^{A:=} int)` (`G-U5b-05`).
   - Verify `Example 5.30` types `f (fn y => if y < 0 then raise neg else y) (3-2)` as `int & {neg}` and
     `f (fn z => if z > 0 then raise pos else 0-z) (2-3)` as `int & {pos}` (`∀'a,'b,'0`), and verify
     `Exercise 5.9` rejects `(int →^⊤ int) →^{\{X\}} (int →^∅ int)` (`G-U5b-07`).
4. **Oracle D — Lexical `Observe` Masking & Compound `∀[]. τ̂` (`Examples 5.31–5.33`, `Tables 5.11–5.13`)**:
   - On `(let x = 7 in fn_Y y => y+x) 9`, assert `Observe([], int, ϱ₂)` masks `ϱ₁, ϱ₃, ϱ₄` and `β` inside
     `letregion ϱ₁, ϱ₃, ϱ₄`, leaving root `(int @ ϱ₂) & {put ϱ₂}` (`G-U5b-16`), while `x : int @ ϱ₁ & ∅` refuses
     `letregion ϱ₁ in x` because `ϱ₁ ∉ φ`.
5. **Oracle E — `[gen]` `FV(φ)` Value Barrier & `pipe` Behaviours (`Examples 5.34–5.37`, `Table 5.18`)**:
   - Assert `let ch = channel_A in (send 1 on ch; send true on ch)` is **rejected** because `'a ∈ FV('a chan {A})`
     blocks `[gen]` (`Example 5.36`, `G-U5b-11`).
   - Assert `node` in `Example 5.35` checks against `spawn(rec '2. (''1?'a; '1; ''2!'b; '2))` via `φ[β ↦ rec β.φ] ⊑ rec β.φ`
     with braced `{C}` in `pipe` (`G-U5b-21`).

```text
W_CFA θ_A(β)        = {π | (β ⊇ {π}) ∈ C} if β ∈ AV(C) else ∅     (defaulting X \ AV(C) to ∅)
Arrow / ref ≤       : (τ̂₁→^φ τ̂₂) ≤ (τ̂'₁→^{φ'} τ̂'₂) iff τ̂'₁≤τ̂₁ ∧ τ̂₂≤τ̂'₂ ∧ φ⊆φ';  ref_ϖ τ̂ ≤ ref_{ϖ'} τ̂' iff τ̂≤τ̂' ∧ τ̂'≤τ̂ ∧ ϖ⊆ϖ'
[handle] & [gen]    : φ₁ ∪ (φ₂ \ {s}) with β \ {s} = β;  [gen] requires ζ_i ∉ downwards_closure_C(FV(Γ̂) ∪ FV(φ))
[region] Observe    : letregion ϱ⃗ in ee valid iff φ' = Observe(Γ̂, τ̂, r)(φ) ∧ ϱ⃗ ∈ φ ∧ ϱ⃗ ∉ φ'
Behaviour Table 5.18: (φ₁ + φ₂); φ₃ ≡ (φ₁; φ₃) + (φ₂; φ₃) [right-only!];  r₁!τ̂₁ cov τ̂₁,  r₁?τ̂₁ contrav τ̂₁,  τ̂ chan r inv τ̂
```

### Five Anti-Degradation Sign-Off Checks

- **No smoothing (`SMOOTHING_TRAP`)**: Keep `⊢_UL` typability (`G-U5a-01`), `{π} ∪ φ` subeffecting (`G-U5a-05`),
  big-step divergence vacuity (`BKL-004`, `G-U5a-11`), `AV(φ₂) = ∅` (`G-U5b-10`), and `ϱ⃗ ∈ φ` in `[region]` (`G-U5b-16`).
- **No signature distortion (`SIGNATURE_DISTORTION`)**: Preserve covariant `⊑` (`§5.2.3`) vs contravariant `≤`
  (`§5.4`, `G-U5a-12`), `∘ θ₀` in `if` (`G-U5a-14`), invariant `ref_ϖ`/`chan` (`G-U5b-05`), and right-only `;`
  distributivity (`G-U5b-20`).
- **No silent gotcha truncation (`SILENT_GOTCHA_TRUNCATION`)**: Retain `θ_A` `X \ AV(C)` `∅`-defaulting (`G-U5a-21`),
  `β \ {s} = β` (`BKL-009`, `G-U5b-09`), `[gen]` downwards closure (`G-U5b-11..12`), and `Algorithm R` incompleteness (`G-U5b-15`).
- **Zero hallucinated symbols (`HALLUCINATED_SYMBOL`)**: Every rule and numbered item traces to
  `corpus/shards/RAW_SHARD_05a_annotated_types_inference.md` or `corpus/shards/RAW_SHARD_05b_effects_regions_behaviours.md`,
  with post-book extensions explicitly tagged `[external: ...]`.
- **Provenance intact (`PROVENANCE_DISCONNECTION`)**: Every claim carries exact single-page citations (such as
  [PPA §5.1, p. 283] (book p. 283; PDF p. 300)), `G-U5a-*`/`G-U5b-*` gotcha IDs, and `BKL-*` pointers:
  `BKL-073` (`Table 5.5` `if` `∘ θ₀`), `BKL-074` (`θ_A` `X \ AV(C)` `∅`-default), `BKL-075` (`§§5.1–5.3` typed-substrate,
  whole-tree `(5.2)`, smearing, big-step vacuity with `BKL-004`), `BKL-076` (covariant `⊑` vs contravariant `≤` `Exercise 5.9`),
  `BKL-077` (turnstile subscripts, `Table 5.8` `τ₁`, `Example 5.19` `[β' ↦ β]`, self-bindings), `BKL-078` (`§5.4.1` `ξ ∈ Loc`,
  unbraced `ϖ`, `p. 323` slip with `BKL-026`/`BKL-031`), `BKL-079` (`β \ {s} = β` with `BKL-009`, `AV(φ₂) = ∅`, `Exercise 5.15` `σ̂ ≤ σ̂'`),
  `BKL-080` (`Table 5.11` `dom(ς₁)`, `Table 5.12` `σ̂ @ r`, `Type_RI` invariance, `Observe` + `ϱ⃗ ∈ φ`), `BKL-081` (unbraced `{C}`,
  positive `rec β.φ`, right-only `;`), and `BKL-082` (`p. 350` `§5.1` mis-citation, `+` guard, OCR drops with `BKL-011`, `BKL-030`).

## 9. Complete Chapter 5 Tables and Figures Lookup Index

| Formal Artifact | Role & Primary Invariant | Book / PDF Coordinate |
| :--- | :--- | :--- |
| `Table 5.1` | Underlying monomorphic type system `Γ ⊢_UL e : τ` (rightmost-wins `Γ`, base `Const`/`Op`) | [PPA Table 5.1, p. 285] (book p. 285; PDF p. 302) |
| `Table 5.2` | Annotated CFA `Γ̂ ⊢_CFA e : τ̂` with embedded `{π} ∪ φ` subeffecting (`Fact 5.6`) | [PPA Table 5.2, p. 288] (book p. 288; PDF p. 305) |
| `Table 5.3` | `UCAI` set axioms (`∅, ∪`) and structural equality `τ̂₁ = τ̂₂` on `Typê` | [PPA Table 5.3, p. 290] (book p. 290; PDF p. 307) |
| `Table 5.4` | Closed big-step Natural Semantics `⊢ e ⟶ v` (vacuous on divergence, `BKL-004`) | [PPA Table 5.4, p. 292] (book p. 292; PDF p. 309) |
| `Table 5.5` | Underlying reconstruction `𝒲_UL(Γ, e) = (τ, θ)` (`if` omits `∘ θ₀`, `F-U5a-04`) | [PPA Table 5.5, p. 303] (book p. 303; PDF p. 320) |
| `Table 5.6` | Syntactic unification `𝒰_UL(τ₁, τ₂)` with occurs check (`[α ↦ α]` guard) | [PPA Table 5.6, p. 305] (book p. 305; PDF p. 322) |
| `Table 5.7` | Simple-type unification `𝒰_CFA(τ̂₁, τ̂₂)` (`Fact 5.17`, `β` never occurs-checked) | [PPA Table 5.7, p. 307] (book p. 307; PDF p. 324) |
| `Table 5.8` | CFA reconstruction `𝒲_CFA(Γ̂, e) = (τ̂, θ, C)` (fixes `∘ θ₀`, emits `β ⊇ {π}`) | [PPA Table 5.8, p. 310] (book p. 310; PDF p. 327) |
| `Table 5.9` | Side-effect analysis `Γ̂ ⊢_SE e : τ̂ & φ` (unmasked `new π`, invariant `ref_ϖ`) | [PPA Table 5.9, p. 322] (book p. 322; PDF p. 339) |
| `Table 5.10` | Polymorphic exception analysis `Γ̂ ⊢_ES e : σ̂ & φ` (`β \ {s} = β`, `BKL-009`) | [PPA Table 5.10, p. 328] (book p. 328; PDF p. 345) |
| `Figure 5.1` | Stack-of-regions memory model (`RName` stack, boxed `(rn, o) ∈ EVal`) | [PPA Figure 5.1, p. 331] (book p. 331; PDF p. 348) |
| `Table 5.11` | Extended-expression region semantics `ρ ⊢ ⟨ee, ς₁⟩ ⟶ ⟨v, ς₂⟩` (`dom(ς₁)` fix) | [PPA Table 5.11, p. 334] (book p. 334; PDF p. 351) |
| `Tables 5.12–5.13` | Stack-based region translation (`[175, 176]`, `[external: Tofte–Talpin]`) `Γ̂ ⊢_RI e ↝ ee : (τ̂ @ r) & φ` + `Observe` + `[place]` | [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354) [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355) |
| `Figure 5.2` | Concurrent ML pipeline produced by `pipe [f₁, f₂] inp out` (`Example 5.34`) | [PPA Figure 5.2, p. 340] (book p. 340; PDF p. 357) |
| `Tables 5.14–5.15` | CML sequential evaluation-context SOS & synchronous rendezvous process pool | [PPA Table 5.14, p. 341] (book p. 341; PDF p. 358) [PPA Table 5.15, p. 343] (book p. 343; PDF p. 360) |
| `Tables 5.16–5.17` | CML communication behaviour typing `Γ̂ ⊢_CA e : σ̂ & φ` (`Example 5.36` `[gen]`) | [PPA Table 5.16, p. 346] (book p. 346; PDF p. 363) [PPA Table 5.17, p. 347] (book p. 347; PDF p. 364) |
| `Table 5.18` | 22-rule causal behaviour preorder `φ₁ ⊑ φ₂` (right-only `;` over `+`, `!/?/chan`) | [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365) |
