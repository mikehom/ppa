---
name: ppa-dataflow-and-slicing
description: Design, verify, and debug intraprocedural and interprocedural data flow analyses, def-use slicing, monotone frameworks, and heap shape analyses. Use when building reaching definitions, available expressions, very busy expressions, live or faint variables, ud/du chains, SSA lowering, constant propagation, call-string or assumption-set context sensitivity, flow-insensitive IAV call graphs, or compatible shape graphs with strong updates and materialisation. Do not use for Ch 1 approach comparison or App A-C foundations (ppa-program-analysis), higher-order closures (ppa-control-flow-and-constraints), Galois widenings (ppa-abstract-interpretation), annotated type systems (ppa-types-effects-and-regions), worklist or RPO solver scheduling (ppa-fixedpoint-solvers), or taint threat modelling (ppa-cyber-vulnerability-analysis).
---

<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L2 procedural skill for Chapter 2 DFA, slicing, interprocedural context, and heap shape analysis. -->

# Data Flow Analysis, Def-Use Slicing, and Heap Shape Workflows

Actionable engineering workflows for designing, implementing, verifying, and debugging Chapter 2
analyses ([PPA §2.1, p. 35] (book p. 35; PDF p. 54) through [PPA Exercise 2.25, p. 139] (book p. 139; PDF p. 158)).
Exact definitions, side conditions, and proof sketches live in the self-contained L1 references:

- Classical DFA, `ud`/`du` slicing, Monotone/Distributive Frameworks, `MFP`/`MOP`:
  [intraprocedural-analyses-and-frameworks.md](./references/intraprocedural-analyses-and-frameworks.md)
- Small-step correctness (`§2.2`, `Mini Project 2.2`) & interprocedural context (`§2.5`):
  [interprocedural-and-correctness.md](./references/interprocedural-and-correctness.md)
- Heap pointer SOS, compatible shape graphs, materialisation (`§2.6`):
  [shape-analysis.md](./references/shape-analysis.md)
- Mathematical foundations & formulation comparisons (hosted by router `ppa-program-analysis`):
  [chapter-1-five-formulations.md](../ppa-program-analysis/references/chapter-1-five-formulations.md) and
  [appendix-a-posets-lattices-fixed-points.md](../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md).

## 1. Boundary Dispatch Before Writing Equations

Confirm the problem lies inside Chapter 2 (`WHILE` flow graphs, static procedures, one-level pointers,
ACC complete lattices) before authoring transfer functions:

| Task Signature | Target Skill | Reason |
| :--- | :--- | :--- |
| Paradigm selection (`DFA` vs `CFA` vs `AI` vs `Types`) | `ppa-program-analysis` (router) | Master router arbitrates across Chapters 1–6 |
| Classical `AE`/`RD`/`VB`/`LV`, `ud`/`du` chains, `CP`, Monotone Frameworks, `§2.5` calls, `§2.6` shape | **This skill (`ppa-dataflow-and-slicing`)** | Core Chapter 2 construction, debugging, and correctness domain |
| Function values, closures, indirect call targets, dynamic dispatch (`[U2b:2.5-e]`) | `ppa-control-flow-and-constraints` | `§2.5` flow graphs assume syntactic procedure constants |
| Infinite-height lattices lacking ACC (`Interval` bounds), widening/narrowing | `ppa-abstract-interpretation` | Monotone Frameworks require ACC (`§2.3.1`, `G-U2a-24`) |
| Type/effect/region inference or polymorphic effect subtraction (`BKL-009`) | `ppa-types-effects-and-regions` | Chapter 5 annotated type/effect reconstruction |
| RPO node ordering, SCC decomposition, `d(G, T) + 3` round-robin bounds (`BKL-012`) | `ppa-fixedpoint-solvers` | Chapter 6 solver scheduling beyond Table 2.8 |
| Security threat policies, sanitizer semantics, [external: CWE] exploitability triage | `ppa-cyber-vulnerability-analysis` | Security domain modelling beyond formal lattice safety |

## 2. Procedure 1: Construct a Sound Monotone Framework Instance

Follow these steps whenever building a classical or custom intraprocedural data flow pass
[PPA §2.3, p. 66] (book p. 66; PDF p. 85) [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88):

1. **Audit IR preconditions (`§2.1`)**:
   - Enforce **label consistency** (`[B₁]^ℓ, [B₂]^ℓ ∈ blocks(S) ⇒ B₁ = B₂`, `G-U2a-06`); note loop unrolling
     preserves label consistency even when duplicating labels breaks unique labelling (`G-U2a-16`, `BKL-028`).
   - Finitise carriers to the program of interest (`Var⋆, Lab⋆^? = Lab⋆ ∪ {?}`, non-trivial `AExp⋆`,
     `G-U2a-04`, `G-U2a-11`, `G-U2a-26`). Never evaluate over infinite `Var` or `AExp` (`G-U2a-26`).
   - Verify composite `labels(S)` identities vs single-block edge cases (`G-U2a-02`), single `init(S)` vs
     multi-exit `final(S)` (`G-U2a-01`, `G-U2a-03`). If starting from unstructured three-address IR, run
     intraprocedural CFG / structural analysis (`[U2b:CR-f]`) first [PPA Chapter 2 Concluding Remarks, p. 131] (book p. 131; PDF p. 150).
2. **Choose four-square polarity (`POLARITY_GATE`, `G-U2a-21`)**:
   - **Forward must (`⋂, →, ↑`)** (`AE`): `F = flow(S⋆)`, `E = {init(S⋆)}`, `L = (𝒫(AExp⋆), ⊇)`, `⊥_L = AExp⋆`,
     `ι = ∅`; exclude `x ∈ FV(a')` in `gen_AE([x:=a]^ℓ)` (`G-U2a-08`).
   - **Forward may (`⋃, →, ↓`)** (`RD`): `F = flow(S⋆)`, `E = {init(S⋆)}`, `L = (𝒫(Var⋆ × Lab⋆^?), ⊆)`,
     `⊥_L = ∅`, **`ι = {(x, ?) | x ∈ FV(S⋆)}`** (`G-U2a-11`; never `∅` unless definite-init holds).
   - **Backward must (`⋂, ←, ↑`)** (`VB`): `F = flow^R(S⋆)`, `E = final(S⋆)`, `L = (𝒫(AExp⋆), ⊇)`,
     `⊥_L = AExp⋆`, `ι = ∅`; keep *all* `AExp(a)` in `gen_VB([x:=a]^ℓ)` because RHS reads precede write (`G-U2a-08`).
   - **Backward may (`⋃, ←, ↓`)** (`LV`): `F = flow^R(S⋆)`, `E = final(S⋆)`, `L = (𝒫(Var⋆), ⊆)`, `⊥_L = ∅`,
     set **`ι = observed_outputs`** (`∅` only for closed non-observing programs, `G-U2a-12`, `BKL-006`).
3. **Emit unconditional `⊔ ι^ℓ_E` equations (`G-U2a-07`, `G-U2a-22`)**:
   - Write `Analysis∘(ℓ) = ⨆{Analysis•(ℓ') | (ℓ', ℓ) ∈ F} ⊔ ι^ℓ_E` rather than `if ℓ ∈ E then ι else ⨆{...}`.
   - Rationale: Programs starting or ending with `while` loops violate isolated entries or isolated exits
     (`Example 2.3`, `G-U2a-05`, `Exercise 2.6`), and Table 2.1–2.4 case-splits drop loop back-edges or
     exit-loop facts (`F-U2a-09`, `G-U2a-19`).
4. **Verify lattice & transfer axioms (`MONOTONICITY_GATE`, `CONVERGENCE_GATE`, `§2.3.1`, `BKL-014`, `BKL-022`)**:
   - Prove `L` obeys ACC (`Lemma A.8` / finite height `h`, `G-U2a-23`, `G-U2a-24`).
   - Verify `id ∈ 𝓕`, closure under `∘`, and monotonicity `l₁ ⊑ l₂ ⇒ f_ℓ(l₁) ⊑ f_ℓ(l₂)` (`BKL-014`).
   - Check binary distributivity `f(l₁ ⊔ l₂) = f(l₁) ⊔ f(l₂)` (strictness `f(⊥) = ⊥` is *not* required,
     `G-U2a-25`). Note `Bit Vector ⊂ Distributive ⊂ Monotone` (`Exercise 2.9`, `G-U2b-31`).
   - For multi-statement basic blocks (`Exercise 2.5`) in Bit Vector Frameworks, fold sequential steps with
     `l_k'' = l_k' ∪ l_k` and `l_g'' = (l_g' \ l_k) ∪ l_g` (`Lemma 2.25`, `G-U2a-27`; `f'` runs before `f`).
   - For non-distributive lattices (`Table 2.7` Constant Propagation, `G-U2a-28`), keep global unreachable `⊥`
     strict under `op^_a` and test against `Exercise 2.10` (`z:=x*y` `MFP = ⊤` vs `MOP = -1`), adding
     two-label branches `[b]^{ℓ₁,ℓ₂}` (`Exercise 2.11`) when branch correlation matters.
5. **Solve with Table 2.8 invariant checks (`G-U2a-29`, `G-U2a-30`, `G-U2a-31`)**:
   - Initialise non-extremal `Analysis[ℓ]` strictly to `⊥_L` (`AExp⋆` for `AE`/`VB` `G-U2a-09`; `∅` for
     `RD`/`LV` `G-U2a-10`; global `⊥`, *not* `λx.⊤`, for `CP` `G-U2a-28`).
   - Gate updates with **`f_ℓ(Analysis[ℓ]) ⋢ Analysis[ℓ']`** (not `≠`) and merge via **`⊔`** (not overwrite).
   - Bound worst-case worklist steps by finite-height `O(e · h)` (`G-U2a-31`; remember `+v` for `(x, ?)` pairs).
   - Assert `MFP = MOP` (`Lemma 2.32`) *only* when **both** distributivity **and** `∀ℓ : path∘(ℓ) ≠ ∅`
     (`Exercise 2.13`, `G-U2a-34`, `G-U2b-34`) hold; otherwise use `𝒫(L)` (`G-U2a-35`) or expect `MFP ⊒ MOP`.
     Note also that Round Robin bounds of `d(G_S, T) + 3` (`BKL-012`) apply only to Bit Vector Frameworks
     with DFSF `T` and reverse postorder (`CONVERGENCE_GATE` -> delegate RPO scheduling to `ppa-fixedpoint-solvers`).

## 3. Procedure 2: Compute `ud`/`du` Slices, Constant Folding, and Safe DCE

Execute this workflow for program slicing, def-use transformations, and dead-code cleanup
[PPA §2.1.5, p. 53] (book p. 53; PDF p. 72) [PPA Mini Project 2.1, p. 132] (book p. 132; PDF p. 151):

1. **Compute constructive `UD` and `DU` over `Var⋆ × Lab⋆^?`**:
   - Run `RD` first with `(x, ?) ∈ RD_entry(init(S⋆))` (`G-U2a-11`).
   - Evaluate `UD(x, ℓ') = {ℓ | (x, ℓ) ∈ RD_entry(ℓ')} if x ∈ gen_LV(B^{ℓ'}) else ∅`, and invert via
     `DU(x, ℓ) = {ℓ' | ℓ ∈ UD(x, ℓ')}`.
   - Always include `?` in signature types (`Var⋆ × Lab⋆^? ↔ 𝒫(Lab⋆^?)`, fixing `F-U2a-05`, `G-U2a-14`),
     and allow terminal self-redefinitions (`[x := x+1]^{ℓ_n}`, `G-U2a-13`).
2. **Audit uninitialised reads and trace slices (`UD`/`DU` & `SSA`)**:
   - Flag any `(x, ℓ')` with **`? ∈ UD(x, ℓ')`** as a possible read-before-write defect (`Example 2.12`).
   - Walk `UD` edges backward for data slicing; note implicit conditional branches (`if [b]^ℓ`) are absent
     from pure `UD`/`DU` unless control dependence is added `[external]`. Lower to SSA (`x := ϕ(...)`,
     `[U2b:CR-d]`) when downstream passes require explicit single-def chains.
3. **Gate chain-based Constant Folding (`Mini Project 2.1`, `Figure 2.23`, `G-U2b-29`)**:
   - Follow `du(x, ℓ)` from constant assignment `[x := n]^ℓ` to candidate use `ℓ'`.
   - Before rewriting `x ↦ n` at `ℓ'`, inspect `ud(x, ℓ')`: fold **iff** `? ∉ ud(x, ℓ')` AND *every*
     definition `ℓ'' ∈ ud(x, ℓ')` assigns the exact same constant `n` (`G-U2b-29`). Verify against
     `Example 2.12` (`(if [z=3]^3 ...); [y:=3]^6; [x:=3+z]^7`).
4. **Gate Dead Code Elimination & Secret Zeroization (`Exercise 2.4`, `BKL-006`)**:
   - Protect `observed_outputs` (`G-U2a-12`) and security-critical `[external: zeroization]` stores (`[key := 0]^ℓ`, `BKL-006`)
     by placing them in `ι` at `final(S⋆)` before deleting assignments where `x ∉ LV_exit(ℓ)`.
   - To eliminate dead self-updates (`[x:=1]^1; [x:=x-1]^2; [x:=2]^3`), upgrade `LV` to **faint / strongly live
     variables** (`Exercise 2.4`, `G-U2b-31` — remains distributive despite exiting the bit-vector class `[derived]`).

## 4. Procedure 3: Lift to Context-Sensitive Interprocedural Analysis or `IAV`

Apply this procedure when analysing `P⋆ = begin D⋆ S⋆ end` across calls `[call p(a, z)]^{ℓ_c}_{ℓ_r}`
[PPA §2.5, p. 84] (book p. 84; PDF p. 103) [PPA §2.5.3, p. 93] (book p. 93; PDF p. 112):

1. **Check static-call gate (`G-U2b-02`, `BKL-008`)**: Confirm every call names a declared constant `p` in
   `D⋆`. If procedures or closures are passed dynamically, halt and route CFG discovery to
   `ppa-control-flow-and-constraints`.
2. **Build `flow⋆` and explicit 4-tuple `inter-flow⋆` (`G-U2b-01`, `G-U2b-03`)**:
   - Emit `(ℓ_c; ℓ_n)` and `(ℓ_x; ℓ_r)` in `flow⋆` AND matched 4-tuples `(ℓ_c, ℓ_n, ℓ_x, ℓ_r)` in `IF`.
   - Never propagate through `(ℓ_c; ℓ_n)` and `(ℓ_x; ℓ_r)` as plain `goto`s without `IF` (`§2.5.2`): `n` call
     sites yield `n²` invalid cross-over pairs (`G-U2b-01`).
   - For backward interprocedural passes (`G-U2b-03`), orient `flow⋆^R` via `(ℓ_n; ℓ_c)`, `(ℓ_r; ℓ_x)` and
     reverse 4-tuples to `(ℓ_r, ℓ_x, ℓ_n, ℓ_c)` (`[derived]`).
3. **Select context domain `Δ` using precision, monotonicity, and recursion rules**:
   - **Flow-insensitive [external: mod-ref] pre-pass (`IAV`, `§2.5.6`)**: Build `CP(S)` (`Figure 2.11`), compute
     `IAV(p) = (AV(S) \ {formals(p)}) ∪ ⋃{IAV(p') | p' ∈ CP(S)}` — **fixing `F-U2b-07` (`G-U2b-14`) by
     subtracting BOTH `val x` AND `res y`** (plus locals) — and take the **least** fixed point (`G-U2b-15`;
     `gfp` returns useless `Var⋆`). Remember pp. 102–103 print `"context-insensitive"` where flow-insensitive is meant.
   - **Non-recursive shallow call stacks**: Use **bounded call strings `Δ = Lab^{\le k}`** (`§2.5.4`, `G-U2b-10`).
     Set `k` strictly above wrapper depth; remember `k = 0` gives context-insensitive cross-product smearing
     (`Example 2.40`) and `⌈δ, ℓ_c⌉_k` forces `⨆` joins on `f̂¹_{ℓ_c}`. Never deploy unbounded `Δ = Lab^*`
     on recursive cycles (violates ACC), and do not use distinct-site `k` (`Exercise 2.16`, `G-U2b-11`) if
     distinguishing entry calls from direct recursion matters.
   - **Deep recursion over finite `D`**: Choose **Small Assumption Sets `Δ = D`** (`L̂ = 𝒫(D × D)`, `§2.5.5`),
     which stay polynomial (`|D|²`), monotone, and additive (`[external: IFDS]` summary edges).
   - **Disjunctive caller grouping**: Only use **Large Assumption Sets `Δ = 𝒫(D)`** if exact equality
     `δ' = {d'' | (δ, d'') ∈ Z}` is relaxed to `δ' ⊆ ...` or solved by a weakly monotonic engine (`[51, 52]`,
     `BKL-003`, `G-U2b-12`). Fix printed `ι̂` from `{({ι}, ι)}` / `{(ι, ι)}` to `{(ι, d) | d ∈ ι}` or
     `{(d, d) | d ∈ ι}` (`G-U2b-13`).
4. **Enforce binary return & `res`-init contracts (`G-U2b-04`, `G-U2b-08`, `G-U2b-09`, `G-U2b-34`)**:
   - In `f̂¹_{ℓ_c}`, initialise `res y` to unconstrained `⊤` (`{-, 0, +}` in `Example 2.38`), matching `[call]`'s
     arbitrary `v ∈ Z` (`G-U2b-04`).
   - Wire **`f̂²_{ℓ_c,ℓ_r}(A∘(ℓ_c), A∘(ℓ_r))`** (`Figure 2.8`, `G-U2b-08`) with worklist edges from *both* `ℓ_c`
     and `ℓ_r` to restore caller locals intact (`G-U2b-09`; guard `val-res` actual aliasing under `Exercise 2.20`,
     `G-U2b-34`). Factor additive returns via `f̂^{2A}(l̂) ⊔ f̂^{2B}(l̂')` (`Figure 2.10`).
   - Validate completeness against `VP⋆` / `MVP` (`G-U2b-06`, `G-U2b-07`, noting intermediate `bind` rules require
     Chapter 3 treatment `G-U2b-05`).

## 5. Procedure 4: Implement & Audit Heap Shape Analysis (`§2.6`)

Follow this workflow when verifying pointer invariants or aliasing (`SG = (S, H, is)`, `𝒫(SG)`)
[PPA §2.6.2, p. 114] (book p. 114; PDF p. 133) [PPA §2.6.3, p. 122] (book p. 122; PDF p. 141):

1. **Verify language scope (`G-U2b-16`, `BKL-005`)**: Confirm pointers only dereference one selector `x.sel`,
   with zero pointer arithmetic, interior pointers, or type punning. Lower nested chains (`x.a.b` `[external]`)
   via temporaries first, and interpret `℘, 𝒜, ℬ` over infinite `State × Heap` as partial functions `⇀` (`F-U2b-08`).
2. **Desugar compound / self-referential heap statements (`G-U2b-25`)**: Rewrite `[x:=x.sel]^ℓ`, `[x.sel:=x]^ℓ`,
   `[x.sel:=y.sel']^ℓ`, and `[malloc (x.sel)]^ℓ` into 3-step sequences using fresh `t ∉ Var⋆` ending with
   `[t := nil]^{ℓ₃}` (`pp. 119, 126–128`; or use `Exercise 2.22`'s direct rules for same-variable `[x.sel:=x.sel']^ℓ`). Never apply `x ≠ y` heap clauses
   when `x = y`.
3. **Run `is_compatible(S, H, is)` post-condition checks (`G-U2b-18..21`)**:
   - Assert Invariants 1–5 (`p. 114`) plus `x ∈ X ⇒ (x, n_X) ∈ S`: disjoint sets (`1`), `x ∈ X` (`2`),
     unique target per `(n_V, sel)` when `V ≠ ∅` (`3`, allowing multi-edges/self-loops on `n_∅`, `G-U2b-20`),
     heap witnesses for `is` (`4`), and forced `is` on `≥ 2` distinct heap edges into `X ≠ ∅` (`5`, noting
     4(a) has no inverse, `G-U2b-21`).
   - Never set `n_{Y∪{x}} ∈ is` on `[x := y]^ℓ` from variable aliasing alone (`G-U2b-19`); `is` tracks **heap**
     sharing only. Remember absent entries in `S, H` conflate integers, `nil` (`◇`), and `undef` (`G-U2b-18`).
4. **Apply strong nullification, strong update, and Case 3 materialisation (`STRONG_UPDATE_GATE`, `G-U2b-22..27`)**:
   - Rely on outer-may / inner-must structure (`G-U2b-22`): unique `n_X` (`X ≠ ∅`) permits strong `kill_x`
     and `kill_{x.sel}` updates (any fallback "weak update" phrasing on `n_∅` is `[external]`).
   - In `kill_{x.sel}` (`p. 125`, `G-U2b-27`), remove `n_U` from `is` **iff all 3 hold**:
     `n_U ∈ is`, `#into(n_U, H') ≤ 1`, **AND** `¬∃sel' : (n_∅, sel', n_U) ∈ H'`. Never skip the `n_∅` check.
   - In `[x := y.sel]^ℓ` (`x ≠ y`):
     - **Inspect `Case 1` before transfer (`G-U2b-23`)**: Because `Case 1` maps missing `y` or `n_Y.sel` to
       `{kill_x(...)}` and `[b]^ℓ` is identity, raise null-deref warnings directly from `Shape∘(ℓ)` and pair
       with two-label `[b]^{ℓ₁,ℓ₂}` (`Exercise 2.11`) if `nil` pruning is needed.
     - **Implement `Case 3` via `kill_x` round-trip (`G-U2b-26`)**: Demand `S'' = S' ∪ {(x, n_{x})}`, promote
       `(n_Y, sel, n_∅) ↦ (n_Y, sel, n_{x})`, enforce `n_∅ ∈ is' ⇔ (n_∅ ∈ is'' ∨ n_{x} ∈ is'')`, generate
       related `external/internal/going-out/going-in` edges filtered by `is_compatible`, and test against
       `Figures 2.19–2.20`'s exact **6-graph** oracle!
5. **Control state explosion and garbage retention (`G-U2b-17`, `G-U2b-24`, `G-U2b-28`)**:
   - Because neither `malloc` (`G-U2b-17`) nor `kill_x` / `kill_{x.sel}` (`G-U2b-24`) collects garbage, dead
     pointers fold into `n_∅`, pushing 7-block list reversal over **50 shape graphs** (`Exercise* 2.21`).
     Control cost via `Exercise* 2.23` tightening, `Exercise* 2.24` GC, `Exercise* 2.25` allocation-site
     naming `n_{ℓ,X}`, or `[148, 149]` single-summary merging (`G-U2b-28`).

## 6. Correctness Proofs, Debugging Table, and Anti-Degradation Checks

When proving soundness (`§2.2`, `Mini Project 2.2`, `G-U2a-15..20`, `G-U2b-30`, `G-U2b-32`): always use
**small-step SOS** (`§2.2.1`, not big-step, `BKL-004`), prove preservation against **unconditional constraint
systems `Analysis^⊑`** (`Lemma 2.15`, Moore family under `⋂`, `G-U2b-32`; fixing `F-U2a-09`), leverage
`Lemma 2.14` (`G-U2a-16`, `G-U2a-17`), and show lockstep `∼_V` (`Theorem 2.21`, `Corollary 2.22`). For `RD^⊆`
(`Table 2.10`, `Mini Project 2.2`, `G-U2b-30`), fix `Trace = (Var × Lab^?)*` and `Y ⊆ Var⋆ × Lab⋆^?`.

| Observed Symptom | Root Mechanism (`PPA` Reference) | Required Fix |
| :--- | :--- | :--- |
| Loop headers collapse to `∅` in `AE`/`VB`, or dead code propagates `⊤` in `CP` | Non-extremal nodes initialised to `∅` (`AE`/`VB`) or `λx.⊤` (`CP`) instead of `⊥_L` (`G-U2a-09`, `G-U2a-28`) | Initialise `ℓ ∉ E` strictly to `⊥_L`; isolate `ι` to `E` (`Table 2.8`) |
| Loop facts missing at leading/trailing `while` loop (`Example 2.3`) | `Table 2.1–2.4` case-split `if ℓ ∈ E` dropped incoming or outgoing loop edges (`G-U2a-07`, `G-U2a-19`) | Switch to unconditional `⨆{...} ⊔ ι^ℓ_E` (`§2.3`) |
| Dead-store elimination deletes trailing `[key := 0]` wipe | Closed-world `LV_exit(final) = ∅` assumed at boundary (`G-U2a-12`, `BKL-006`) | Add observable/secret buffers to `ι` at `final(S⋆)` |
| Return site `ℓ_r¹` poisoned by unrelated caller `ℓ_c²` or locals overwritten | Missing `inter-flow⋆`, `k = 0`, or unary `f̂²` ignoring `A∘(ℓ_c)` (`G-U2b-01`, `G-U2b-08`, `G-U2b-09`) | Match `(ℓ_c, ℓ_n, ℓ_x, ℓ_r) ∈ IF`, lift `k ≥ 1` or `Δ = D`, wire binary `f̂²` |
| Worklist oscillates or loses facts on `Δ = 𝒫(D)` calls | Exact fiber `δ' = {d'' \| (δ, d'') ∈ Z}` is non-monotone (`G-U2b-12`, `BKL-003`) | Relax `=` to `⊆`, switch to `Δ = D`, or use `[51, 52]` solver |
| `IAV(p)` flags local `res y` writes as global mutations | Printed formula omits `\ {y}` (`F-U2b-07`, `G-U2b-14`) or solved for `gfp` (`G-U2b-15`) | Subtract all formals/locals `{x, y}`; compute `lfp` |
| [external: UAF]/ownership pass clears `n_U ∈ is` with summary aliases left | Omitted `¬∃sel' : (n_∅, sel', n_U) ∈ H'` in `kill_{x.sel}` (`G-U2b-27`) | Check all 3 unsharing conditions (`Figure 2.21`) |

## 7. Golden Regression Oracles & Exact Kernel Signatures

Run these exact Chapter 2 test witnesses against any new solver, transfer implementation, or IR lowering:

1. **Oracle A — `AE` vs `VB` Assignment Asymmetry (`Examples 2.5, 2.9`)**:
   - On `[a := a + 1]^4`, `kill_AE = kill_VB` includes `a + 1`, yet `gen_AE = ∅` (`a ∈ FV(a+1)`) while
     `gen_VB = {a + 1}` (`G-U2a-08`).
   - On `while [y > a + b]^3 do ([a := a + 1]^4; [x := a + b]^5)` (`Example 2.5`), `AE_entry(3) = {a + b}`
     only holds when non-extremal nodes start at `AExp⋆` (`G-U2a-09`).
2. **Oracle B — Constant Propagation Non-Distributivity (`Lemma 2.27`, `Exercise 2.10`)**:
   - Input `(if [···]^1 then [x:=-1]^2; [y:=1]^3 else [x:=1]^4; [y:=-1]^5); [z:=x*y]^6`.
   - Assert solver computes `MFP•(6)(z) = ⊤` while exact path join gives `MOP•(6)(z) = -1` (`G-U2a-28`).
   - Verify `[y := x * x]^ℓ` separates `f_ℓ^CP(σ̂₁ ⊔ σ̂₂)(y) = ⊤` from `(f_ℓ^CP(σ̂₁) ⊔ f_ℓ^CP(σ̂₂))(y) = 1`.
3. **Oracle C — `ud`/`du` Chain Constant Folding & Uninitialised Safety (`Example 2.12`, `Mini Project 2.1`)**:
   - Input `[x:=0]^1; [x:=3]^2; (if [z=x]^3 then [z:=0]^4 else [z:=x]^5); [y:=x]^6; [x:=y+z]^7`.
   - Assert `ud(z, 3) = {?}` (`du(z, ?) = {3}`, flagging uninitialised `z`), `du(x, 1) = ∅` (`1` removable),
     and `du(x, 2) = {3, 5, 6}` folds safely to `if [z=3]^3 ... [y:=3]^6; [x:=3+z]^7` (`G-U2b-29`).
4. **Oracle D — Recursive Interprocedural Context Matrix (`Examples 2.33, 2.38–2.42`)**:
   - Verify Fibonacci `inter-flow⋆ = {(9, 1, 8, 10), (4, 1, 8, 5), (6, 1, 8, 7)}` (`G-U2b-01`).
   - Verify `k = 1` gives 4 call strings `Λ, [9], [4], [6]` and `k = 2` gives 8 strings (`Example 2.39`),
     while `k = 1` resets return context to caller `δ` (`G-U2b-10`).
   - Verify `IAV` least fixed point on `Example 2.42` yields `{y}` rather than `Var⋆` (`G-U2b-15`), and
     under `proc p(val x, res y)` assigns global writes without leaking `y` (`G-U2b-14`).
5. **Oracle E — Shape Case 3 Materialisation & Unsharing Guard (`Figures 2.14, 2.19–2.21`)**:
   - On `Figure 2.19` (`n_∅ ∉ is, n_W ∉ is, sel₂ ≠ sel₃`), Case 3 of `[x := y.sel]^ℓ` must yield **6**
     graphs (`Figure 2.20`): `(n_V, sel₁, n_∅)` fixed, `sel₂` exclusively on `n_{x}` xor `n_∅`, `sel₃` on
     `n_{x}`, `n_∅`, or both (`G-U2b-26`).
   - On `Figure 2.14` middle row (`(n_∅, cdr, n_{y})`, `n_{y} ∈ is`), deleting another incoming edge to `n_{y}`
     must **keep `n_{y} ∈ is`** (`#into ≤ 1` alone is insufficient without `¬∃sel' : (n_∅, sel', n_U) ∈ H'`,
     `Figure 2.21`, `G-U2b-27`).
   - Remember `[not is-nil(x)]^2` leaves non-terminated shapes untouched (`G-U2b-23`) and `[z:=nil]^7` preserves
     `n_{z}`'s outgoing edges inside `n_∅` (`G-U2b-24`).

### Exact Shape Transfer Quick-Reference (`§2.6.3`, `pp. 117–127`)

See [PPA §2.6.3, p. 117] (book p. 117; PDF p. 136) and [PPA §2.6.3, p. 127] (book p. 127; PDF p. 146) for full case rules:

```
kill_x((S,H,is))     = ({(z,k_x(n_Z)) | (z,n_Z)∈S, z≠x}, {(k_x(n_V),sel,k_x(n_W)) | (n_V,sel,n_W)∈H}, {k_x(n_X) | n_X∈is})
[x := y]^ℓ (x ≠ y)   : run kill_x, map y's node n_Y ↦ n_{Y∪{x}}, keep n_{Y∪{x}} ∈ is'' iff n_Y ∈ is'
[x := y.sel] Case 3  : (x≠y, (y,n_Y)∈S', (n_Y,sel,n_∅)∈H'): {G'' compatible | kill_x(G'')=G', (x,n_{x})∈S'', (n_Y,sel,n_{x})∈H''}
kill_{x.sel}(S,H,is) = drop (n_X,sel,n_U); remove n_U from is iff n_U∈is ∧ #into(n_U,H')≤1 ∧ ¬∃sel':(n_∅,sel',n_U)∈H'
[x.sel := y]^ℓ (x≠y) : x,y∈dom(S): run kill_{x.sel}, add (n_X,sel,n_Y), is'' = is' ∪ {n_Y} if #into(n_Y,H')≥1 else is'
[malloc x]^ℓ         : run kill_x, add (x, n_{x}) unshared
```

## 8. Anti-Degradation Sign-Off Checks

Before signing off on any Chapter 2 analysis design or review, verify all five anti-degradation checks:
- **No smoothing (`SMOOTHING_TRAP`)**: Keep `gen_AE` vs `gen_VB` (`G-U2a-08`), `Bit Vector` vs
  `Distributive` (`G-U2b-31`), `LV^=` vs `LV^⊆` (`G-U2a-18`, `G-U2b-32`), and heap `is` vs stack aliasing
  (`G-U2b-19`) strictly separated.
- **No signature distortion (`SIGNATURE_DISTORTION`)**: Finitise `Lab⋆^?` on `ud/du` (`G-U2a-14`), thread
  binary `(A∘(ℓ_c), A∘(ℓ_r))` into `f̂²` (`G-U2b-08`), and read `℘, 𝒜, ℬ` as partial `⇀` (`G-U2b-16`).
- **No silent gotcha truncation (`SILENT_GOTCHA_TRUNCATION`)**: Preserve non-isolated loop guards (`G-U2a-07`,
  `G-U2a-19`), `ι = {(x,?)}` (`G-U2a-11`), non-monotone `Δ = 𝒫(D)` warnings (`G-U2b-12`), and unsharing's
  `n_∅` condition (`G-U2b-27`).
- **Zero hallucinated symbols (`HALLUCINATED_SYMBOL`)**: Every table, figure, and formula traces directly to
  `corpus/shards/RAW_SHARD_02a_intraproc_dfa.md` or `corpus/shards/RAW_SHARD_02b_interproc_shape.md` (with
  non-book names tagged `[external]`).
- **Provenance intact (`PROVENANCE_DISCONNECTION`)**: Every non-obvious claim carries exact inline citations
  (such as [PPA §2.1, p. 35] (book p. 35; PDF p. 54)), `G-U2a-*`/`G-U2b-*`, or `BKL-*` pointers.
