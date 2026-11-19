<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L1 formal reference for Chapter 6 §6.3, Concluding Remarks, Mini Projects 6.1-6.2, Exercises 6.10-6.14, and Unit 6 Index/Bibliography solver concordance. -->

# Strong-Component, Local, Elimination, and Widened Fixed-Point Solvers (`§6.3` & End Matter)

Scope: `§6.3` *Iterating Through Strong Components* (`Tables 6.5–6.6`, `Figures 6.5–6.6`, `Examples 6.14–6.15`), Chapter 6 *Concluding Remarks* (`pp. 384–387`: iterative, demand-driven local, differential, and elimination solvers + practical toolkits), `Mini Projects 6.1–6.2`, `Exercises 6.10–6.14`, and Unit 6 Subject Index (`pp. 433–437`, offset `+14`) & Bibliography (`[1]`–`[185]`, `pp. 439–452`, offset `+13`) concordance [PPA §6.3, p. 381] (book p. 381; PDF p. 397), [PPA Chapter 6 Concluding Remarks, p. 384] (book p. 384; PDF p. 400). Foundations link to [appendix-c-graphs-dfsf-and-rpo.md](../../ppa-program-analysis/references/appendix-c-graphs-dfsf-and-rpo.md) and [appendix-a-posets-lattices-fixed-points.md](../../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md); core `Table 6.1` and RPO/Round-Robin algorithms live in [worklist-and-rpo-algorithms.md](worklist-and-rpo-algorithms.md).

---

## 1. Strong-Component Condensation and `srPostorder` (`§6.3`, `Tables 6.5–6.6`)

### 1.1 Reduced SCC DAG (`U10`) and `Example 6.14` (`pp. 381–382`)

Partition `G_𝒮` into maximal strongly connected subgraphs (*strong components*, `Fact C.3` [PPA Fact C.3, p. 418] (book p. 418; PDF p. 433)). Contracting each component to a node (omitting self-loops) produces the *reduced graph*, which is guaranteed acyclic (`DAG`, `Lemma C.5` [PPA Lemma C.5, p. 419] (book p. 419; PDF p. 434)) and topologically ordered via reverse postorder on the reduced graph (`Corollary C.11` [PPA Corollary C.11, p. 424] (book p. 424; PDF p. 439)) [PPA §6.3, p. 381] (book p. 381; PDF p. 397).

- **`Example 6.14` & `Figure 6.5`**: Partitioning `Example 6.1` yields `{x₁}`, `{x₂, x₃}`, `{x₄, x₅}`, `{x₆}` forming a diamond DAG (`{x₁} → {x₂, x₃} → {x₆}` and `{x₁} → {x₄, x₅} → {x₆}`) with two topological orders [PPA Example 6.14, p. 381] (book p. 381; PDF p. 397), [PPA Figure 6.5, p. 382] (book p. 382; PDF p. 398).
- **Trivial vs Nested Loop Caveat (`G-U6-17`)**: On `WHILE` graphs, only *non-trivial* strong components (`|SC| > 1` or self-edge) correspond to outermost `while`-loops (`{x₁}`, `{x₆}` are trivial 1-node acyclic SCCs, despite `p. 382`'s broad wording). Moreover, flat `[external: Tarjan SCC]` merges nested inner `while`-loops into their enclosing outer SCC; stabilising inner loops before outer back-edges requires hierarchical `[external: Bourdoncle WTO]` (`[25]`) [PPA Example 6.14, p. 382] (book p. 382; PDF p. 398), [PPA Bibliography [25], p. 441] (book p. 441; PDF p. 454).

### 1.2 `Table 6.5` `srPostorder` Shadowing Bug (`G-U6-16`) and Safe Fix (`p. 382`)

`Table 6.5` assigns each constraint `(x ⊒ t)` a pair `srPostorder[x ⊒ t] = (scc, rp)` (`fst` = topological SCC rank, `snd` = local RPO inside that SCC) [PPA Table 6.5, p. 382] (book p. 382; PDF p. 398):
- **Source Erratum (`G-U6-16`)**: Printed `Table 6.5` writes `scc := 1; for each scc in topological order do ... srPostorder[x ⊒ t] := (scc,rp); ... scc := scc + 1;`, shadowing integer counter `scc` with the component node-set `scc`!
- **Shadow-Free Implementation**:
  ```text
  scc_id := 1;
  for each comp in topological_order(SCCs(G_𝒮)) do
      rp := 1;
      for each (x ⊒ t) in local_rPostorder(comp) do
          srPostorder[x ⊒ t] := (scc_id, rp);
          rp := rp + 1;
      scc_id := scc_id + 1;
  ```

### 1.3 `Table 6.6` Three-Level SCC Worklist and 3-Queue `(W.c, W.pc, W.pf)` (`pp. 383–384, 391`)

`Table 6.6` instantiates `Table 6.1` without altering Step 1 or Step 2 [PPA Table 6.6, p. 384] (book p. 384; PDF p. 400):
```text
empty = (nil, ∅)
insert((x ⊒ t), (W.c, W.p)) = (W.c, (W.p ∪ {x ⊒ t}))
extract((W.c, W.p)):
    local variables: scc, W_scc
    if W.c = nil then
        scc := min{fst(srPostorder[x ⊒ t]) | (x ⊒ t) ∈ W.p};
        W_scc := {(x ⊒ t) ∈ W.p | fst(srPostorder[x ⊒ t]) = scc};
        W.c := sort_srPostorder(W_scc);
        W.p := W.p \ W_scc;
    return (head(W.c), (tail(W.c), W.p))
```
- **DAG Barrier Guarantee (`G-U6-18`)**: Because the reduced graph is a DAG, evaluating `(x ⊒ t)` in component `scc` can push items only into `scc` or downstream `> scc` components — **never** an already-settled `< scc` component [PPA §6.3, p. 383] (book p. 383; PDF p. 399).
- **Three-Queue Priority Routing (`Exercise 6.12`, `[77]`, `G-U6-18`)**: `Exercise 6.12` (misprinted *"two priority queues"* on line 1 while naming three!) replaces `W.p` with **three** queues `(W.c, W.pc, W.pf)` (`currentQ, pendingQ, futureQ` `[77]`), routing newly triggered `(x' ⊒ t')` with `(scc', rp') = srPostorder[x' ⊒ t']` from `(scc, rp)` to:
  1. `W.c` if `scc' = scc ∧ rp' > rp` (downstream in current SCC pass),
  2. `W.pc` if `scc' = scc ∧ rp' ≤ rp` (back/self edge for next pass of current SCC),
  3. `W.pf` if `scc' > scc` (held until `W.c` and `W.pc` both empty!) [PPA Exercise 6.10, p. 390] (book p. 390; PDF p. 406), [PPA Exercise 6.11, p. 390] (book p. 390; PDF p. 406), [PPA Exercise 6.12, p. 391] (book p. 391; PDF p. 407).

### 1.4 Empirical Benchmark Summary on `Example 6.1` (`Figures 6.1, 6.3, 6.4, 6.6`)

| Strategy | Un-deduplicated Trace | With Membership Deduplication | Downstream `x₆` Evaluations | Source Anchor |
| :--- | :--- | :--- | :--- | :--- |
| LIFO (`Table 6.2`) | `14` pops (`Figure 6.1`, `Ex 6.7`; `20` rev. `Ex 6.1`) | `8` Step 2 pops (`Ex 6.3`, `9` rows incl. init) | `3` (`Fig 6.1`: `∅`, `X_{3?}`, `X_{35?}`; `1` in `Ex 6.3`) | [PPA Figure 6.1, p. 374] (book p. 374; PDF p. 390) |
| RPO `(W.c, W.p)` (`Table 6.3`) | `11` pops (`Figure 6.3`, `Ex 6.9`) | `8` Step 2 pops (`Ex 6.6`, `9` rows incl. init) | `2` (`Fig 6.3`: `X_{35?}`, stability check; `1` in `Ex 6.6`) | [PPA Figure 6.3, p. 377] (book p. 377; PDF p. 393) |
| Round Robin (`Table 6.4`) | `12` `eval` checks (`2` sweeps, `Fig 6.4`) | Fixed `[1..N]` sweep (`Mini Project 6.1`) | `2` (`Pass 1`, `Pass 2`) | [PPA Figure 6.4, p. 379] (book p. 379; PDF p. 395) |
| SCC `(W.c, W.p)` (`Table 6.6`) | **`10` pops** (`Figure 6.6`, `Ex 6.15`) | **`8` pops** (`Ex 6.11`) | **`1`** (`X_{35?}` at step 10) | [PPA Figure 6.6, p. 384] (book p. 384; PDF p. 400) |

---

## 2. Dynamic Conditional Constraints, Worklist Widening (`U7`), and Fastness Closure

### 2.1 Online Simplification of Conditional Constraints (`Mini Project 6.2`, `G-U6-20`)

For RHS grammar `t ::= x | ⊥ | c | t₁ ⊔ t₂ | t₁ ⊓ t₂ | if t₁ ≠ ⊥ then t₂ | if c ⊑ t₁ then t₂` [PPA Mini Project 6.2, p. 388] (book p. 388; PDF p. 404):
- **Monotonicity**: Guards `t₁ ≠ ⊥` and `c ⊑ t₁` (with *constant* `c`, implicit `else ⊥`) are upward-closed in `ψ`, so once true during monotone iteration they remain permanently true.
- **Dynamic Graph Hazard (`G-U6-20`) `[derived]`**: Simplifying `x ⊒ if c ⊑ x₂ then x₁` in-place to `x ⊒ x₁` (or lazily activating edge `x₁ → x` only when `c ⊑ Analysis[x₂]` holds) dynamically inserts cross-node edges into `G_𝒮`, which can **merge distinct SCCs** and invalidate static `rPostorder` / `srPostorder` tables unless orderings are dynamically maintained (or run under order-insensitive deduplicated queues).

### 2.2 Worklist Solver with Widening `∇` (`Exercise 6.13`, `U7`, `G-U6-22`)

When `(L, ⊑)` fails ACC (`Chapter 4` `Interval` [PPA Example 4.10, p. 221] (book p. 221; PDF p. 238), `convex polygons` `[41]` [PPA Chapter 4 Concluding Remarks, p. 272] (book p. 272; PDF p. 289), or `[external: convex polyhedra]`), `Exercise 6.13` modifies `Table 6.1` Step 2 [PPA Exercise 6.13, p. 391] (book p. 391; PDF p. 407), [PPA §4.2, p. 226] (book p. 226; PDF p. 243):
```text
if Analysis[x] ⋣ new then
    Analysis[x] := Analysis[x] ∇ new;
    for all x' ⊒ t' in infl[x] do W := insert((x' ⊒ t'), W);
```
- **`U7` Correspondence Basis**: Pointwise `∇` on `X → L` is a valid widening **because `X` is finite** (bridging `§2.3` ACC frameworks to `§4.2` widening `∇` in [correctness-and-fixed-points.md](../../ppa-abstract-interpretation/references/correctness-and-fixed-points.md)); termination holds without ACC and yields a reductive upper bound `μ_𝒮 ⊑ Analysis` (`Analysis ∈ Red(F_𝒮)`, **not** necessarily `μ_𝒮`).
- **Three Mandatory Implementation Guards (`G-U6-22`) `[derived]`**:
  1. *Never drop `if Analysis[x] ⋣ new`*: `∇` is not monotone and need not satisfy `a ∇ b = a` when `b ⊑ a`; unguarded `Analysis[x] ∇ new` can diverge!
  2. *Keep operand order `old ∇ new`*: reversing `new ∇ Analysis[x]` breaks ascending-chain stabilisation.
  3. *Do not split acyclic joins under universal `∇`*: splitting `x = [0,0] ⊔ [1,1]` into `x ⊒ [0,0]` and `x ⊒ [1,1]` and applying `∇` on every variable update widens `[0,0] ∇ [1,1] = [0, +∞]`! Aggregate acyclic `⊔` joins and apply `∇` only at loop-head feedback cutsets.

### 2.3 Fast Functions and Fastness Closure `f̄` (`Exercise 6.14`, `G-U6-23`)

Monotone `f : L → L` is **fast** iff `f ∘ f ⊑ f ⊔ id` (every idempotent `f ∘ f = f`, including every Bit Vector transfer `f(Y) = (Y ∩ A) ∪ B`, is fast) [PPA Exercise 6.14, p. 391] (book p. 391; PDF p. 407), [PPA Exercise 6.14, p. 392] (book p. 392; PDF p. 408):
- Writing `f^⟨n⟩ = (f ⊔ id)^n`, if `f^⟨i_f⟩ = f^⟨i_f + 1⟩`, the **fastness closure** `f̄ = f^⟨i_f⟩` is well-defined (`f^⟨j⟩ = f̄` for all `j ≥ i_f`), idempotent, fast, and satisfies `f̄ ⊒ f ⊔ id` (with **`f̄ = f ⊔ id`** whenever `f` is fast and distributive!).
- For distributive `f` and simple-loop functional `F(g) = id ⊔ (g ∘ f)`, `F^{n+1}(⊥) = (f ⊔ id)^n = ⨆_{j=0}^n f^j`, hence **`lfp(F) = f̄`** — solving simple reducible loops in closed form without fixed-point iteration (`G-U6-23`).

---

## 3. Local Demand-Driven, Elimination, and Practical Solvers (`Concluding Remarks`)

Chapter 6 *Concluding Remarks* (`pp. 384–387`, `G-U6-19`) surveys three solver families beyond global iterative worklists [PPA Chapter 6 Concluding Remarks, p. 384] (book p. 384; PDF p. 400), [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401), [PPA Chapter 6 Concluding Remarks, p. 386] (book p. 386; PDF p. 402), [PPA Chapter 6 Concluding Remarks, p. 387] (book p. 387; PDF p. 403):

| Family | Mechanism & Key Citations | Best Fit & Structural Limits |
| :--- | :--- | :--- |
| **Integrated vs Segregated Iterative (`[69, 96, 77]`)** | *Integrated* queues constraints `(x ⊒ t)` (`Table 6.1`); *segregated* queues flow variables `x` (`Table 3.7`). | Integrated excels with `M = 1` split rules (`Ex 6.5`); segregated pairs cleanly with `(x, Δ_x)` deltas. |
| **Local / Demand-Driven (`[29, 51–54]`)** | `(1)` *Top-down* recursive solver (`[29]`, logic-programming AI); `(2)` *Timestamp max-PQ* (`[51, 54]`); `(3)` *Differential worklist* propagating `Δ` (`[52, 53]`). | Computes `μ_𝒮` only on the backward dependency cone of queried `x_query` (`[external: Salsa/Pluto IDE & sink-taint queries]`), discovering SCCs dynamically. Must keep cyclic in-flight SCCs dirty until quiescence `[derived]`. |
| **Elimination Methods (`[146, 154, 144, 11, 170, 171]`)** | *Structural* postorder control-tree reduction (`[154, 144]`); *Interval* single-entry cycle graphs (`[11]`); *Path algebras* / regular expressions (`[170, 171]`). | Algebraic bottom-up transfer synthesis + top-down pass (`Ex 6.14` `f̄`); structural reduction also translates low-level code to high-level programs. Restricted to reducible/algebraically closed domains (`G-U6-19`). |
| **Generator Toolkits (`[177, 185, 104, 172, 8]`)** | `Spare [177]`, `System Z [185]`, `PAG [104]` (bit vectors, AVL `[4]`, `BDD's [26]`, widenings), graph rewriting `[17]`, modal logic `[97]`, `Sharlit [172]`, `BANE [8]` (set constraints `[7]`). | Declarative specification compilers generating specialised fixed-point engines. |

### 3.1 Repaired Top-Down Local Solver Sketch (`[derived]`, `G-U6-19`)

The book names the top-down (`[29]`) and timestamp (`[51, 54]`) local solvers but prints no pseudo-code; the `solve(x)` block in the `ppa-fixedpoint-solvers` SKILL (Procedure 4, step 3) is a `[derived]` reconstruction, not book pseudo-code [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401). Its invariants:
- **Provisional reads**: a call `solve(y)` with `y` already on the stack returns the current `memo[y]` (a lower bound of `μ_𝒮(y)` under monotone RHS) and `mark_cycle(y)` records the stack segment from `y` upward as one dynamic SCC rooted at its lowest stack entry (`is_scc_root`). A back edge to a node that is already a non-root member does not make it a root: cycles sharing stack entries merge and keep the lowest root.
- **Single-pass members, iterating root**: the exit test `until (not is_scc_root(x)) or (changes = stamp)` lets every non-root member (and every acyclic variable) leave after one pass; only the root repeats. A global counter `changes` is incremented whenever `old ≠ memo[x]`, so `changes = stamp` means no memo entry anywhere in the dynamic SCC changed during the root's last pass, i.e. the SCC is stable.
- **Deferred settling**: members stay unsettled (and are re-evaluated on each root pass) until the root exits; then the root settles itself and exactly the members left unsettled during its own activation (a sibling acyclic node or an unrelated inner root must not settle them). Settling a member earlier freezes a provisional value and under-approximates `μ_𝒮`.
- **Termination**: with ACC each root pass either increases some `memo` entry or ends the loop, and the earlier literal exit (`(root and stabilised) or (not in cycle)`) could never fire for a non-root member. Minimal check: `x ⊒ {1} ⊔ y, y ⊒ x` must stop at `x = y = {1}` after two root passes.

---

## 4. Subject Index (`pp. 433–437`) and Bibliography (`pp. 439–452`) Concordance

Unit 6 closes the book with two global lookup indices under distinct PDF offsets (`G-U6-01`, `G-U6-24`):
- **Subject Index** — book pages 433–437 / PDF pages 447–451 (offset `+14`, `379` headwords: `69 + 79 + 80 + 80 + 71`): Spans `abstract 0-CFA, 147` (`p. 433`) to `Y2K, 356` (`p. 437`) [PPA Index, p. 433] (book p. 433; PDF p. 447), [PPA Index, p. 437] (book p. 437; PDF p. 451). Note that *Concluding Remarks* solver terms (*local solver*, *top-down*, *differential worklist*, *structural/interval/path elimination*, `srPostorder`) are **unindexed** (`G-U6-19`), and `p. 435` prints `lower adjoint , 239` (`G-U6-24`) [PPA Index, p. 435] (book p. 435; PDF p. 449).
- **Bibliography** — book pages 439–452 / PDF pages 452–465 (offset `+13`, `[1]`–`[185]`): Anchor solver citations include Kildall `[96]` (`p. 446`), Hecht `[69]` (`p. 444`), Kam–Ullman `[92, 93]` (`p. 446`), Knuth `[98]` (`p. 446`), Horwitz–Demers–Teitelbaum `[77]` (`p. 445`), Bourdoncle `[24, 25]` (`p. 441`), Le Charlier–Van Hentenryck `[29]` (`p. 441`), Fecht–Seidl `[51–54]` (`p. 443`), Allen–Cocke `[11]` (`p. 440`), Ryder–Paull `[146]` (`p. 449`), Sharir `[154]` (`p. 450`), Tarjan `[170, 171]` (`p. 451`), Martin `PAG [104]` (`p. 446`), and Aiken et al. `BANE [8]` (`p. 439`) (preserving minor source quirks `[24]`, `[42]`, `[90]`, `[180]`, `G-U6-24`) [PPA Bibliography, p. 439] (book p. 439; PDF p. 452), [PPA Bibliography, p. 452] (book p. 452; PDF p. 465).
