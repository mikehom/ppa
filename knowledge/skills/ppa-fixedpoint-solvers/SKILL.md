---
name: ppa-fixedpoint-solvers
description: >-
  Designs, schedules, optimises, and debugs fixed-point constraint solvers from Chapter 6 of Principles
  of Program Analysis: abstract worklists, unary join splitting, LIFO/FIFO queues, minimal handles,
  reverse postorder double buffering, Round Robin loop-connectedness bounds, three-queue strong
  components, guarded worklist widening, fastness closures, demand-driven local solvers, and elimination
  methods.
  Use when tuning worklist data structures, choosing iteration orderings, diagnosing quadratic or cubic
  solver blowups, preventing unsound early-cutoff timeouts, or building on-demand local solvers.
  Do not use for flow equations or shape graphs (ppa-dataflow-and-slicing), closure constraint
  generation (ppa-control-flow-and-constraints), Galois domains or widenings
  (ppa-abstract-interpretation), annotated types and effects (ppa-types-effects-and-regions), or
  vulnerability policies (ppa-cyber-vulnerability-analysis).
---

<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L2 actionable procedural skill for Chapter 6 fixed-point solvers and scheduling algorithms. -->

# PPA Fixed-Point Solvers & Iteration Scheduling (`Chapter 6`)

Actionable engineering workflows for building, accelerating, and verifying fixed-point engines over
monotone constraint systems `𝒮 = (x_i ⊒ t_i)_{i=1}^N`
([PPA §6.1, p. 367] (book p. 367; PDF p. 383) through [PPA Exercise 6.14, p. 392] (book p. 392; PDF p. 408)).
By `Lemma 6.4`, solver **correctness** (`Analysis = μ_𝒮 = lfp(F_𝒮)`) depends only on lattice `ACC`,
monotone RHS terms `⟦t⟧`, and draining the worklist completely (`W = empty`), whereas **convergence
speed** is governed by constraint granularity (`Exercise 6.5`) and extraction scheduling (`Tables 6.2–6.6`)
[PPA Lemma 6.4, p. 370] (book p. 370; PDF p. 386).

Exact definitions, verbatim algorithm tables, trace figures, and proof sketches live in the
self-contained L1 references:

- Abstract worklists, `O(h · M² · N)` vs `O(h · M · N)` splitting, LIFO/FIFO, minimal handles,
  `(W.c, W.p)` RPO, and Round Robin `d(G_𝒮, T) + 3`:
  [worklist-and-rpo-algorithms.md](./references/worklist-and-rpo-algorithms.md)
- Strong-component condensation (`Tables 6.5–6.6`), 3-queue `(W.c, W.pc, W.pf)`, conditional
  simplification, worklist widening `∇`, fastness closure `f̄`, local demand-driven solvers, and
  elimination methods:
  [scc-round-robin-and-advanced-solvers.md](./references/scc-round-robin-and-advanced-solvers.md)
- Graph & lattice prerequisites (hosted by master router `ppa-program-analysis`):
  [appendix-c-graphs-dfsf-and-rpo.md](../ppa-program-analysis/references/appendix-c-graphs-dfsf-and-rpo.md) and
  [appendix-a-posets-lattices-fixed-points.md](../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md).

---

## 1. Scope & Sibling Routing Boundaries

Confirm that the lattice `(L, ⊑)` and transfer constraints `𝒮` are already formulated before tuning
solver schedules:

| Task Shape | Route | Reason |
| :--- | :--- | :--- |
| Worklist ADTs, `M = 1` join splitting, `rPostorder` `(W.c, W.p)`, Round Robin `d(G_𝒮, T) + 3`, 3-queue SCC `(W.c, W.pc, W.pf)`, guarded worklist `∇`, fastness closure `f̄`, demand-driven local/differential or elimination solvers | **Stay here (`ppa-fixedpoint-solvers`)** | Algorithmic computation and scheduling (`Chapter 6`) |
| Formulating `AE/RD/VB/LV`, `ud`/`du` slicing, `MFP` vs `MOP`, call-strings, or heap shape graphs | `ppa-dataflow-and-slicing` | Domain transfer formulation (`Chapter 2`) |
| Generating `0-CFA`, `k-CFA`, or `CPA` constraints for dynamic dispatch and closures | `ppa-control-flow-and-constraints` | Higher-order control-flow specification (`Chapter 3`) |
| Designing Galois connections `(L, α, γ, M)`, soundness relations, or domain-specific `∇`/`Δ` operators | `ppa-abstract-interpretation` | Domain approximation theory (`Chapter 4`) |
| Annotated types, `𝒲_CFA` constraint generation, region inference, or CML behaviours | `ppa-types-effects-and-regions` | Type-based static analysis (`Chapter 5`) |
| Threat-driven `[external: taint, sanitisation, CWE-400/CWE-407]` policy, or exploitability triage | `ppa-cyber-vulnerability-analysis` | Security-property workflow (cross-book) |
| Comparing paradigms or consulting raw Appendix A/B/C theorems (`Tarski`, `DFSF` proofs) | `ppa-program-analysis` | Master router & foundational appendices |

---

## 2. Solver Architecture Selection Matrix

Choose the simplest solver architecture whose preconditions match your constraint graph `G_𝒮`,
lattice `(L, ⊑)`, and query workload:

| Solver Architecture | Worklist / State | Asymptotic / Empirical Cost | Mandatory Preconditions & When to Choose |
| :--- | :--- | :--- | :--- |
| **3-Queue SCC + Local RPO (`Table 6.6` + `Ex 6.12`)** | `(W.c, W.pc, W.pf)` + membership bitset/`[external: sparse-set]` | `O(h · M · N)` after `M = 1` split (`8–10` pops on `Ex 6.1`; downstream DAGs evaluated **once**) | **Default production global solver** for general ACC lattices, interprocedural CFGs, and static constraint graphs [PPA Table 6.6, p. 384] (book p. 384; PDF p. 400), [PPA Exercise 6.12, p. 391] (book p. 391; PDF p. 407). |
| **Hierarchical `[external: Bourdoncle WTO]` (`[25]`)** | Recursive head-stripped component hierarchy | Stabilises inner loops before outer back-edges; canonical `∇` cutsets | Deeply **nested loops** (`while ... while ...`, merged into one flat SCC by `Table 6.6`, `G-U6-17`) or infinite-height Chapter 4 domains needing loop-head widening [PPA Example 6.14, p. 382] (book p. 382; PDF p. 398), [PPA Bibliography [25], p. 441] (book p. 441; PDF p. 454). |
| **Round Robin in RPO (`Table 6.4`)** | `Analysis[x]` + `change : bool` (`zero` worklist/`infl` memory!) | **`≤ d(G_𝒮, T) + 3` passes** = `O((d + 1) · N)` (`≤ 6` passes for `d ≤ 3`) | **Bit Vector / fast distributive frameworks** (`f ∘ f ⊑ f ⊔ id`) on dense reducible intraprocedural CFGs (`Lemma 6.12`, `G-U6-13`) [PPA Table 6.4, p. 379] (book p. 379; PDF p. 395), [PPA Lemma 6.12, p. 380] (book p. 380; PDF p. 396). |
| **2-Queue Eager RPO (`Table 6.3` + `Ex 6.7`)** | `(W.c, W.p)` routing `rp' > rp` to `W.c`, `≤` to `W.p` | Skips quiescent blocks unlike Round Robin (`9–11` pops on `Ex 6.1`) | Sparse intraprocedural updates where full `[1..N]` sweeps waste checks, or graphs where SCC condensation is skipped [PPA Table 6.3, p. 376] (book p. 376; PDF p. 392), [PPA Exercise 6.7, p. 390] (book p. 390; PDF p. 406). |
| **Segregated / Differential Worklist (`Ex 6.6`, `MP 6.2`, `[52, 53]`)** | Variable queue `(q, Δ_q)` + dynamic edge activation | `O(n³)` on `0-CFA`; avoids re-scanning old set elements | Dynamic conditional constraints (`if c ⊑ x₂ then x₁` in `0-CFA`/points-to) whose graph `G_𝒮` grows online (`G-U6-20`) [PPA Example 6.6, p. 373] (book p. 373; PDF p. 389), [PPA Mini Project 6.2, p. 388] (book p. 388; PDF p. 404). |
| **Local Demand-Driven (`[29, 51, 54]`)** | Recursive `memo[x]` + `on_stack[x]` or timestamp max-PQ | Proportional to backward cone `{y \| y →* x_query}` | `[external: editor IDE]` hover queries, patch-diff checks, or single-sink security audits in multi-million-line codebases (`G-U6-19`) [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401). |
| **Elimination / Fastness Closure (`Ex 6.14`, `[154, 11, 170]`)** | Control-tree or path-expression algebraic reduction | Closed-form `lfp(F) = f̄ = f ⊔ id` on reducible Bit-Vector loops | Structured/reducible CFGs with algebraically composable transfer functions (or decompilation via `[154]` control trees) [PPA Chapter 6 Concluding Remarks, p. 386] (book p. 386; PDF p. 402), [PPA Exercise 6.14, p. 391] (book p. 391; PDF p. 407). |

---

## 3. Procedure 1 — Normalise Constraint Systems & `infl` Before Solving

Before instantiating any worklist, apply four mandatory normalisations
(`§§6.1–6.1.1`, [worklist-and-rpo-algorithms.md](./references/worklist-and-rpo-algorithms.md)):

1. **Split `M`-Way Joins into Unary/Binary Inequations (`Exercise 6.5`, `G-U6-02`, `G-U6-03`)**:
   - Rewrite every `M`-predecessor join equation `x_i = t_i^1 ⊔ ··· ⊔ t_i^M` into `M` separate
     inequations `x_i ⊒ t_i^1, ···, x_i ⊒ t_i^M`.
   - **Equivalence Warning (`G-U6-02`)**: Multi-LHS inequations share *all* solutions with
     `x = x ⊔ t₁ ⊔ ··· ⊔ t_M` and share the **exact least solution `μ_𝒮`** with `x = t₁ ⊔ ··· ⊔ t_M`,
     while admitting strict reductive upper bounds (`x ⊐ t₁ ⊔ ··· ⊔ t_M`) needed when widening
     (`Exercise 6.13`) [PPA §6.1, p. 366] (book p. 366; PDF p. 382).
   - **Asymptotic Gain (`G-U6-03`)**: Cuts `Table 6.1` worst-case complexity from `O(h · M² · N)`
     (`M` summands re-evaluated on each of `h · M · N` pops) to **`O(h · M · N)`** (`N' = M · N`
     constraints of size `M' = 1`), preventing cubic stalls at high fan-in merge/dispatcher blocks
     [PPA Exercise 6.5, p. 389] (book p. 389; PDF p. 405).
   - **Widening Exception (`G-U6-22`)**: When Step 2 applies `∇` (`Exercise 6.13`), keep acyclic `⊔`
     predecessors grouped at non-header joins (or apply `∇` strictly at feedback loop headers) so
     `[0,0]` and `[1,1]` join via `⊔` to `[0,1]` rather than widening via `∇` to `[0, +∞]`.
2. **Close the Flow-Variable Universe `X` (`G-U6-04`)**:
   - Initialise `Analysis[x] := ⊥_L` and `infl[x] := ∅` explicitly over `X = LHS(𝒮) ∪ ⋃_i FV(t_i)`.
   - Never copy `Table 6.1` Step 1's loop indentation literally (`for all x ⊒ t in 𝒮 do ...
     Analysis[x] := ⊥; infl[x] := ∅`), which redundantly resets multi-inequation LHSs and leaves
     unconstrained RHS input variables uninitialised (`F-U6-01`)
     [PPA §6.1, p. 367] (book p. 367; PDF p. 383), [PPA Table 6.1, p. 369] (book p. 369; PDF p. 385).
3. **Register All `FV(t)` Observers on Conditional RHS Terms (`G-U6-05`, `G-U6-20`)**:
   - For `x ⊒ if c ⊑ t₁ then t₂` (`Example 6.2`, `Mini Project 6.2`), ensure `eval` returns `⊥_L`
     (`∅`) when the guard fails (`F-U6-02`), and register `(x ⊒ t)` in `infl[y]` for
     **every `y ∈ FV(t₁) ∪ FV(t₂)`**
     [PPA Example 6.2, p. 367] (book p. 367; PDF p. 383), [PPA Mini Project 6.2, p. 388] (book p. 388; PDF p. 404).
   - **Lazy Edge-Activation Optimization (`Mini Project 6.2`)**: For dynamic call graphs (`0-CFA`),
     attach dormant `if c ⊑ x₂ then x₁` only to `infl[x₂]`; the instant `c ⊑ Analysis[x₂]` turns
     true, simplify the constraint permanently to `x ⊒ x₁`, enqueue `x ⊒ x₁` immediately, and add
     `x ⊒ x₁` to `infl[x₁]` — noting that dynamically added edges can merge SCCs and invalidate
     static `srPostorder` (`G-U6-20`).
4. **Orient Lattice Polarity on `Must` / Greatest-Solution Equations (`G-U6-21`)**:
   - For intersection equations (`Dom(n)` in `Exercise 6.4`, Available Expressions in `Exercise 6.8`),
     instantiate `L = (𝒫(U), ⊇)`: Step 1 **`⊥_L := U`** (full node/expression universe, **never**
     `∅`!), `⊔_L := ∩`, and `Analysis[x] ⋣ new` tests `¬(Analysis[x] ⊆ new)`
     [PPA Exercise 6.4, p. 389] (book p. 389; PDF p. 405), [PPA Exercise 6.8, p. 390] (book p. 390; PDF p. 406).

---

## 4. Procedure 2 — Implement Shadow-Free 3-Queue SCC + Local RPO Solver (`§§6.2–6.3`)

Execute this workflow to build the production `Table 6.6` + `Exercise 6.12` solver
([scc-round-robin-and-advanced-solvers.md](./references/scc-round-robin-and-advanced-solvers.md)):

1. **Construct `G_𝒮`, Strong Components, and Minimal Handle `H_𝒮` (`G-U6-10`, `U10`)**:
   - Add directed edge `c_i → c_j` iff `LHS(c_i) ∈ FV(RHS(c_j))` (`c_j ∈ infl[LHS(c_i)]`).
   - Partition `G_𝒮` into strong components (`[external: Tarjan SCC]` in `O(|V| + |E|)`; `Fact C.3`,
     `Lemma C.5`). Picking one vertex from each source SCC (in-degree `0` in the reduced DAG) yields
     a **minimal handle `H_𝒮`** (`{x₂, x₄}` in `Example 6.2`), covering rootless backward DFA and
     `0-CFA` graphs without dummy nodes
     [PPA §6.2, p. 375] (book p. 375; PDF p. 391), [PPA §6.3, p. 381] (book p. 381; PDF p. 397).
2. **Assign Shadow-Free `srPostorder[c] = (scc_id, rp)` (`Table 6.5` Fix, `G-U6-16`)**:
   - **Never** copy `Table 6.5` (`p. 382`) verbatim (`scc := 1; for each scc ...` overwrites the
     integer counter with the component set!). Separate `scc_id : int` from
     `comp : Sequence[Constraint]` and order each `comp` internally via `Table C.1` local `rPostorder`
     [PPA Table 6.5, p. 382] (book p. 382; PDF p. 398), [PPA Table C.1, p. 421] (book p. 421; PDF p. 436).
3. **Execute Deduplicated 3-Queue `(W.c, W.pc, W.pf)` Loop (`Exercises 6.11–6.12`, `G-U6-11`, `G-U6-18`)**:
   - Pair queues with `queued[0..N-1]` (using `[external: Briggs–Torczon sparse sets]` when `N` is
     large and refills are sparse so refills never pay `O(N)` empty-bit scans, `G-U6-12`)
     [PPA §6.2, p. 377] (book p. 377; PDF p. 393), [PPA Exercise 6.11, p. 390] (book p. 390; PDF p. 406):
   ```text
   seed all c ∈ 𝒮 into W.pf (setting queued[c] := true)
   while W.c ≠ ∅ or W.pc ≠ ∅ or W.pf ≠ ∅ do
       if W.c = ∅ and W.pc ≠ ∅ then
           move all c ∈ W.pc into W.c (ordered by min rp)
       else if W.c = ∅ and W.pc = ∅ then
           active_scc := min { scc_id(c) | c ∈ W.pf }
           move all { c ∈ W.pf | scc_id(c) = active_scc } into W.c (ordered by min rp)
       pop c = (x ⊒ t) with minimal rp(c) from W.c;   queued[c] := false
       new := eval(t, Analysis)
       if Analysis[x] ⋣ new then
           Analysis[x] := Analysis[x] ⊔ new
           for each c' in infl[x] with not queued[c'] do
               queued[c'] := true
               if scc_id(c') = active_scc and rp(c') > rp(c) then push c' to W.c
               else if scc_id(c') = active_scc              then push c' to W.pc
               else (* scc_id(c') > active_scc by DAG *)        push c' to W.pf
   ```

---

## 5. Procedure 3 — Round-Robin Fast Path (`Lemma 6.12`) & Closed-Form Loops (`Ex 6.14`)

1. **Gate Round Robin (`Table 6.4`) Strictly by Bit-Vector / Fastness Preconditions (`G-U6-13..15`)**:
   - Verify `L = 𝒫(D)` (`D` finite) and every RHS is `t_i = (x_{j_i} ∩ Y_i^1) ∪ Y_i^2` (or
     `f ∘ f ⊑ f ⊔ id` distributive, `Exercise 6.14`), with constraints indexed `1..N` in `rPostorder`
     of DFSF `T`.
   - Under these preconditions, `Table 6.4` needs zero queue/`infl` allocations and halts in
     **`≤ d(G_𝒮, T) + 3` total iterations** (`1` Step 1 init + `≤ d + 1` propagation sweeps + `1`
     quiescence sweep = `O((d + 1) · N)` assignments; `d ≤ 3` on structured `WHILE`/Fortran programs
     `[98]`) [PPA Lemma 6.12, p. 380] (book p. 380; PDF p. 396).
   - **Hard Stop**: Reject `d + 3` pass bounds on Constant Propagation, `0-CFA`, or intervals, or on
     `[external: obfuscated]` irreducible state-machine CFGs where `d(G_𝒮, T) = Θ(N)` (`G-U6-13`, `G-U6-15`).
2. **Elimination / Non-Iterative Loop Closure (`Exercise 6.14`, `Concluding Remarks p. 386`, `G-U6-23`)**:
   - On structured/reducible graphs (`[154]` control trees, `[11]` intervals, `[170, 171]` path
     expressions) with fast distributive transfers (`f ∘ f ⊑ f ⊔ id`), replace iterative loop solving
     of `F(g) = id ⊔ (g ∘ f)` by the closed-form fastness closure **`lfp(F) = f̄ = f ⊔ id`**
     [PPA Chapter 6 Concluding Remarks, p. 386] (book p. 386; PDF p. 402), [PPA Exercise 6.14, p. 391] (book p. 391; PDF p. 407).

---

## 6. Procedure 4 — Non-ACC Widening (`U7`), Sound Timeouts, & Demand-Driven Slicing

1. **Guarded Pointwise Widening on Infinite-Height Lattices (`Exercise 6.13`, `G-U6-22`)**:
   - When `(L, ⊑)` lacks ACC, replace `⊔` with `Analysis[x] := Analysis[x] ∇ new` at loop-head
     cutsets **strictly inside `if Analysis[x] ⋣ new`** (omitting `⋣` can diverge because `a ∇ b`
     need not equal `a` when `b ⊑ a`!), keeping operand order `old ∇ new` and confirming `X` is
     finite [PPA Exercise 6.13, p. 391] (book p. 391; PDF p. 407).
2. **Sound Resource-Budget `[external: Timeouts]` (`G-U6-07` — Zero Silent `[external: False Negatives]`)**:
   - Never abort `Table 6.1` via `if steps > MAX_STEPS: return Analysis`! By `Lemma 6.4` Part (i),
     every intermediate `Analysis_i` satisfies `Analysis_i ⊑ μ_𝒮` and `Analysis_i ∉ Red(F_𝒮)`, so
     early cutoff **silently under-approximates** `[external: may-taint]` and call-graph sets (`[external: CWE-407]`
     evasion hazard) [PPA §6.1.1, p. 371] (book p. 371; PDF p. 387).
   - **Mandatory `[external: Timeout]` Protocol**: If step budget expires with `W ≠ empty`, either switch dirty
     variables to widening `∇` until `W = empty` or assign `Analysis[z] := ⊤_L` across the forward
     cone reachable in `G_𝒮` from `{LHS(c) | c ∈ W}` and emit a degraded-precision status flag.
3. **Demand-Driven Local Solver for Single-Sink / `[external: editor IDE]` Queries (`Concluding Remarks p. 385`, `G-U6-19`)**:
   - When only `Analysis[x_query]` is needed, traverse backward edges `{y ∈ FV(t) | (x ⊒ t) ∈ 𝒮}`
     from `x_query` via a top-down memoised solver (`[29]`) or timestamp max-PQ (`[51, 54]`):
   ```text
   solve(x):
       if x ∈ settled then return memo[x]
       if x ∈ on_stack then mark_scc_cyclic(x); return memo[x]   (* provisional lower bound *)
       on_stack.add(x)
       repeat
           old := memo[x]
           for each (x ⊒ t) ∈ 𝒮 do memo[x] := memo[x] ⊔ eval_rec(t, solve)
       until (x is SCC_root and whole dynamic SCC stabilised) or (x not in active cycle)
       on_stack.remove(x); if not in_unfinished_scc(x) then settled.add(x)
       return memo[x]
   ```
   - Never freeze `settled.add(y)` for an inner node `y` of an active cycle `x → y → x` until the
     cycle root `x` reaches quiescence [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401).

---

## 7. Diagnostic Playbook & Golden Regression Oracles

| Observed Symptom | Root Cause (`Chapter 6` Mechanism) | Concrete Fix |
| :--- | :--- | :--- |
| `[external: TypeError]` or scrambled SCC ranks in `srPostorder` | `Table 6.5` `scc` shadowing bug (`G-U6-16`) | Separate `scc_id : int` from `comp : Set` |
| Post-solve check finds `Analysis[x] ⋣ ⟦t⟧(Analysis)` | Missing guard/payload in `FV(t)` (`G-U6-05`), unrooted `rPostorder` (`G-U6-10`), premature cyclic freeze in local solver, or `W ≠ empty` cutoff (`G-U6-07`) | Register `FV(t₁) ∪ FV(t₂)`, seed `Table C.1` from minimal handle `H_𝒮`, and drain `W` to `empty` |
| `Dom(n)` or `AE` collapses to `∅` inside loops | Initialised `Analysis[x] := ∅` (`⊤`) instead of `⊥_L = U` (`G-U6-21`) | Set `⊥_L = U`, `⊔_L = ∩`, and `⋣` to `¬(Analysis[x] ⊆ new)` |
| Round Robin takes `Θ(b)` passes on backward DFA | Forward CFG `rPostorder` used on `flow^R` (`d = Θ(b)`, `G-U6-15`) | Order constraints by `rPostorder` of `G_𝒮` (forward postorder of CFG, `[69]`) |
| Single RPO min-heap spins on inner self-loop | Missing two-phase `(W.c, W.p)` separation (`G-U6-11`) | Route `rp' > rp` to `W.c` and `rp' ≤ rp` to `W.p` (`Ex 6.7`) |
| Solver stalls on `M`-arm `switch` / merge blocks | Un-split `O(M)` join RHS (`O(h · M² · N)`, `G-U6-03`) | Split into `M` unary inequations `x_join ⊒ t_j` (`Ex 6.5`) |
| Widened worklist diverges or jumps to `⊤` on `if-else` | Missing `Analysis[x] ⋣ new` guard, reversed `new ∇ old`, or `∇` on split acyclic inequations (`G-U6-22`) | Guard `∇` with `⋣`, keep `Analysis[x] ∇ new`, and restrict `∇` to loop heads |

### Exact Worklist ADT Quick-Reference (`Tables 6.1–6.6`)

```text
F_𝒮(ψ)(x)        = ⨆ { ⟦t⟧ψ | (x ⊒ t) ∈ 𝒮 },    μ_𝒮 = lfp(F_𝒮) = ⨆_{j≥0} F_𝒮^j(⊥)
infl[x]          = { (x' ⊒ t') ∈ 𝒮 | x ∈ FV(t') },   ∑_{x∈X} |infl[x]| ≤ M · N
LIFO (Table 6.2) : empty = nil, insert(c,W) = cons(c,W), extract(W) = (head(W), tail(W))
RPO  (Table 6.3) : empty = (nil,∅), insert(c,(W.c,W.p)) = (W.c, W.p ∪ {c}), refill W.c := sort_rPostorder(W.p)
SCC  (Table 6.6) : scc := min { fst(srPostorder[c]) | c ∈ W.p }, W.c := sort_srPostorder(W_scc), W.p := W.p \ W_scc
Fast (Ex 6.14)   : f ∘ f ⊑ f ⊔ id  ⇒  lfp(λg. id ⊔ (g ∘ f)) = f̄ = (f ⊔ id)^{i_f} (= f ⊔ id if f distributive)
```

### Golden Regression Oracles (`Examples 6.1–6.15`, `Exercises 6.3, 6.6, 6.8, 6.11`)

1. **`Example 6.1` 6-Variable `RD` System (`x₁..x₆`, `d = 1`)**: Must converge to `x₁ = X_?`,
   `x₂ = x₃ = X_{3?}`, `x₄ = x₅ = X_{5?}`, `x₆ = X_{35?}` across every scheduler, with exact step
   counts: `14` LIFO (`Fig 6.1`) / `20` rev-LIFO (`Ex 6.1`) / `8` dedup-LIFO (`Ex 6.3`; `9` rows incl. init), `11` RPO (`Fig 6.3`) / `8` dedup-RPO
   (`Ex 6.6`; `9` rows incl. init), `12` `eval` checks across `2` sweeps (`3` total iterations) in Round Robin (`Fig 6.4`,
   `Lemma 6.12` bound `≤ 4`), and `10` SCC (`Fig 6.6`) / `8` dedup-SCC (`Ex 6.11`) evaluating `x₆`
   strictly once
   [PPA Figure 6.1, p. 374] (book p. 374; PDF p. 390), [PPA Figure 6.6, p. 384] (book p. 384; PDF p. 400).
2. **`Example 6.2` Rootless `0-CFA` System (`x₁..x₇`)**: `G_𝒮` has minimal handle `H_𝒮 = {x₂, x₄}`
   (`no` single root) and converges to `x₁ = x₄ = x₅ = x₆ = {fn y => y^3}`, `x₂ = {fn x => x^1}`,
   and **`x₃ = x₇ = ∅`** (since `{fn y => y^3} ⊆ x₂` is false!)
   [PPA Example 6.2, p. 367] (book p. 367; PDF p. 383), [PPA §6.2, p. 375] (book p. 375; PDF p. 391).
3. **`Exercise 6.8` 10-Variable `AE` System (`x₁..x_{10}`)**: Dual `must` lattice `(𝒫(AExp_⋆), ⊇)`
   with `⊥_L = {a+b, a*b, a+1}` and `⊔_L = ∩` must converge identically under `Table 6.4` and `Table 6.6`
   [PPA Exercise 6.8, p. 390] (book p. 390; PDF p. 406), [PPA Exercise 6.10, p. 390] (book p. 390; PDF p. 406).

---

## 8. Anti-Degradation Sign-Off Checklist

- [ ] **No `SMOOTHING_TRAP`**: Never claim `≤ d(G_𝒮, T) + 3` passes outside Bit Vector / fast
  distributive frameworks (`G-U6-13`), never drop ACC without `∇` (`G-U6-06`, `G-U6-22`), and never
  conflate `x = t₁ ⊔ ··· ⊔ t_n` general solutions with `x ⊒ t_i` solutions (`G-U6-02`).
- [ ] **Reductiveness (`Red(F_𝒮)`) & `[external: Timeout]` Integrity**: Assert `∀(x ⊒ t) ∈ 𝒮: ⟦t⟧(Analysis) ⊑ Analysis[x]`
  (`Analysis ∈ Red(F_𝒮)`) at termination and forbid silent `W ≠ empty` early returns (`G-U6-07`).
- [ ] **Implementation Hygiene**: Enforce `M = 1` splitting (`G-U6-03`), closed `X` initialisation
  (`G-U6-04`), dual conditional `infl` registration (`G-U6-05`), `⊥_L = U` on `must` lattices
  (`G-U6-21`), and shadow-free `scc_id` vs `comp` (`G-U6-16`).
