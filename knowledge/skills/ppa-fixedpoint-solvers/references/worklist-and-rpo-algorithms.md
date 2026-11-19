<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L1 formal reference for Chapter 6 §§6.1-6.2 (Abstract Worklist, LIFO/FIFO, Reverse Postorder, and Round Robin algorithms). -->

# Worklist, Reverse-Postorder, and Round-Robin Fixed-Point Solvers (`§§6.1–6.2`)

Scope: Chapter 6 opening, `§6.1` *Worklist Algorithms* (`§6.1.1–§6.1.2`), and `§6.2` *Iterating in Reverse Postorder* (`§6.2.1` *The Round Robin Algorithm*), plus `Mini Project 6.1` and `Exercises 6.1–6.9`, spanning book pages 365–381 and 387–390 (`PDF = book + 16` throughout Chapter 6; `G-U6-01`) [PPA §6.1, p. 365] (book p. 365; PDF p. 381), [PPA §6.2, p. 374] (book p. 374; PDF p. 390). Graph prerequisites (`H_𝒮`, DFSF `T`, `rPostorder`, `d(G_𝒮, T)`) link to [appendix-c-graphs-dfsf-and-rpo.md](../../ppa-program-analysis/references/appendix-c-graphs-dfsf-and-rpo.md); strong-component, local, and elimination solvers live in [scc-round-robin-and-advanced-solvers.md](scc-round-robin-and-advanced-solvers.md).

---

## 1. Flow-Variable Constraint Systems and Equations vs Inequations (`§6.1`)

Chapter 6 unifies Data Flow Analysis (`entry`/`exit` variables at each program point) and Constraint Based Analysis (`C(ℓ)` cache and `r(x)` environment variables) into solving finite systems of inequations over *flow variables* [PPA §6.1, p. 365] (book p. 365; PDF p. 381).

### 1.1 Running Reaching-Definitions Benchmark (`Example 6.1`)

For `if [b₁]^1 then (while [b₂]^2 do [x := a₁]^3) else (while [b₃]^4 do [x := a₂]^5); [x := a₃]^6`, writing `X_ℓ = {(x, ℓ)}` and `X_{356?} = {(x, 3), (x, 5), (x, 6), (x, ?)}`, eliminating the 6 exit variables `x₇..x_{12}` from the 12-variable `RD` system yields the 6-variable `RD_{entry}` benchmark [PPA Example 6.1, p. 365] (book p. 365; PDF p. 381), [PPA Example 6.1, p. 366] (book p. 366; PDF p. 382):
```text
x₁ = X_?                             x₄ = x₁ ∪ (x₅ \ X_{356?}) ∪ X₅
x₂ = x₁ ∪ (x₃ \ X_{356?}) ∪ X₃      x₅ = x₄
x₃ = x₂                              x₆ = x₂ ∪ x₄
```

### 1.2 Equations vs Multi-LHS Inequations (`G-U6-02`, `G-U6-03`)

- Multiple inequations sharing a left-hand side (`x ⊒ t₁, ···, x ⊒ t_n`) have the **exact same set of solutions** as the inflationary equation `x = x ⊔ t₁ ⊔ ··· ⊔ t_n` [PPA §6.1, p. 366] (book p. 366; PDF p. 382).
- Their **least solution** coincides with the least solution of `x = t₁ ⊔ ··· ⊔ t_n` (`x` omitted on the RHS), though `x = t₁ ⊔ ··· ⊔ t_n` rejects strict reductive points `x ⊐ t₁ ⊔ ··· ⊔ t_n` (`G-U6-02`).
- **Asymptotic splitting advantage (`Exercise 6.5`)**: Solving `(x_i ⊒ t_i^1 ⊔ ··· ⊔ t_i^M)_{i=1}^N` directly in `Table 6.1` takes `O(h · M² · N)` steps (re-evaluating all `M` summands whenever one changes). Splitting into the solution-equivalent `N' = M · N` system `((x_i ⊒ t_i^j)_{j=1}^M)_{i=1}^N` with `M' = O(1)` RHS size cuts complexity to **`O(h · M · N)`** (`G-U6-03`) [PPA Exercise 6.5, p. 389] (book p. 389; PDF p. 405).

### 1.3 Five Standing Preconditions and Conditional RHS Encoding (`p. 367`)

Every theorem in `§§6.1–6.3` assumes all five conditions below [PPA §6.1, p. 367] (book p. 367; PDF p. 383):
1. **Finite inequation system**: `𝒮 = (x_i ⊒ t_i)_{i=1}^N` (`N ≥ 1`), where LHS variables `x_i` need not be distinct.
2. **Closed flow-variable universe (`G-U6-04`)**: `FV(t_i) ⊆ X = {x_i | 1 ≤ i ≤ N}` — every RHS flow variable must appear on at least one LHS (otherwise `Table 6.1` Step 1 leaves `Analysis[y]` and `infl[y]` uninitialised; add `y ⊒ ⊥` for unconstrained inputs).
3. **ACC complete lattice**: solutions `ψ : X → L` take values in a complete lattice `(L, ⊑)` satisfying the Ascending Chain Condition (`ACC`).
4. **Term semantics**: each RHS `t` denotes `⟦t⟧ψ ∈ L`.
5. **Monotonicity and locality**: `⟦t⟧ψ` is monotone in `ψ` and depends only on `{ψ(x) | x ∈ FV(t)}`.

**Conditional `0-CFA` encoding (`Example 6.2`, `G-U6-05`)**: For `((fn x => x^1)^2 (fn y => y^3)^4)^5`, `0-CFA` conditional constraints `{fn x => x^1} ⊆ x₂ ⇒ x₁ ⊆ x₅` become unconditional inequations `x₅ ⊇ if {fn x => x^1} ⊆ x₂ then x₁` with implicit `else ⊥` (`∅`) when the guard is false and `FV(t) = {x₂, x₁}` registering **both** guard and payload in `infl` [PPA Example 6.2, p. 367] (book p. 367; PDF p. 383).

---

## 2. The Abstract Worklist Algorithm and `Lemma 6.4` (`§6.1.1`)

### 2.1 Worklist ADT and `Table 6.1` (`pp. 368–370`)

Parameterised by `empty`, `insert((x ⊒ t), W)`, and `extract(W) = ((x ⊒ t), W')` [PPA §6.1.1, p. 368] (book p. 368; PDF p. 384), [PPA Table 6.1, p. 369] (book p. 369; PDF p. 385):
```text
Step 1: W := empty;
        for all x ⊒ t in 𝒮 do
            W := insert((x ⊒ t), W);   Analysis[x] := ⊥;   infl[x] := ∅;
        for all x ⊒ t in 𝒮 do
            for all x' in FV(t) do
                infl[x'] := infl[x'] ∪ {x ⊒ t};

Step 2: while W ≠ empty do
            ((x ⊒ t), W) := extract(W);
            new := eval(t, Analysis);
            if Analysis[x] ⋣ new then
                Analysis[x] := Analysis[x] ⊔ new;
                for all x' ⊒ t' in infl[x] do
                    W := insert((x' ⊒ t'), W);
```
After Step 1, `infl[x] = {(x' ⊒ t') ∈ 𝒮 | x ∈ FV(t')}` (`Example 6.3` on `Example 6.1`: `infl[x₁] = {x₂, x₄}`, `infl[x₂] = {x₃, x₆}`, `infl[x₃] = {x₂}`, `infl[x₄] = {x₅, x₆}`, `infl[x₅] = {x₄}`, `infl[x₆] = ∅`) [PPA Example 6.3, p. 370] (book p. 370; PDF p. 386).

### 2.2 Correctness (`Lemma 6.4`), Complexity, and Early-Cutoff Hazard (`pp. 370–372`)

Define monotone `F_𝒮 : (X → L) → (X → L)` by `F_𝒮(ψ)(x) = ⨆{⟦t⟧ψ | x ⊒ t in 𝒮}`. Under Tarski's Theorem (`Proposition A.10`) and ACC on finite `X → L`, `μ_𝒮 = lfp(F_𝒮) = ⨆_{j≥0} F_𝒮^j(⊥)` [PPA §6.1.1, p. 370] (book p. 370; PDF p. 386), [PPA Proposition A.10, p. 402] (book p. 402; PDF p. 418).

**`Lemma 6.4`** [PPA Lemma 6.4, p. 370] (book p. 370; PDF p. 386): *Under the five standing assumptions (plus finite-multiset `insert`/`extract`), `Table 6.1` terminates and returns `Analysis = μ_𝒮` (`G-U6-06`).*
- **Proof invariants** [PPA §6.1.1, p. 371] (book p. 371; PDF p. 387), [PPA §6.1.1, p. 372] (book p. 372; PDF p. 388):
  1. *Termination*: every update strictly increases `Analysis[x]` in `L` and pushes `≤ N` items; by ACC and finite `X`, updates happen finitely often, and non-updating pops shrink `W`.
  2. *Lower-bound invariant (`Part (i)`) `Analysis_i[x] ⊑ μ_𝒮(x)`*: preserved at every step by monotonicity of `⟦t⟧`.
  3. *Reductiveness at `W = empty` (`Part (ii)`) `F_𝒮(Analysis) ⊑ Analysis`*: after the last update to any `y ∈ FV(t)` (or Step 1 if `FV(t) = ∅`), `(x ⊒ t)` was inserted and extracted, establishing `Analysis[x] ⊒ ⟦t⟧(Analysis)`, so `Analysis ∈ Red(F_𝒮)` (`[external: post-fixed-point]`) and `μ_𝒮 ⊑ Analysis`.
- **Critical Early-Cutoff Trap (`G-U6-07`) `[derived]`**: Because `Analysis_i ⊑ μ_𝒮` approaches `μ_𝒮` strictly from below and is **not** in `Red(F_𝒮)` while `W ≠ empty`, halting `Table 6.1` at an iteration `[external: timeout]` and returning `Analysis_i` silently under-approximates may-analyses (missing reachable call targets or `[external: taint]` flows). Any aborted run must widen (`Exercise 6.13`) or top (`⊤_L`) the forward cone reachable from `W`.
- **`O(h · M² · N)` Complexity (`p. 372`, `G-U6-08`)**: With `|FV(t)| ≤ M`, `eval` in `O(M)`, `O(1)` lattice join/check, `O(1)`/`O(M)` amortised worklist ops, and lattice height `≤ h`: `∑_{x∈X} |infl[x]| ≤ M · N`, total insertions `≤ N + h · M · N`, and total work is **`O(N · M + h · M² · N) = O(h · M² · N)`** (note powerset bitsets/heaps add `O(|D|/w)` or `O(log N)` factors when `O(1)` assumptions do not hold `[derived]`).

---

## 3. LIFO/FIFO Specialisations (`§6.1.2`) and Cross-Chapter Bridges (`U2`, `U3`)

**`Table 6.2` (LIFO stack)** [PPA Table 6.2, p. 373] (book p. 373; PDF p. 389): `empty = nil`, `insert((x ⊒ t), W) = cons((x ⊒ t), W)`, `extract(W) = (head(W), tail(W))`. FIFO replaces the stack with a queue (`p. 374`) [PPA §6.1.2, p. 374] (book p. 374; PDF p. 390).
- **Duplicate-push penalty (`Figure 6.1`, `Example 6.7`, `Exercise 6.3`, `G-U6-09`)**: Unchecked `cons` pushes duplicate constraints (`[x₃, x₆, x₄, x₂, x₃, x₄, x₅, x₆]`), taking **`14` Step 2 pops** on `Example 6.1` (`x₆` evaluated thrice) vs **`8` Step 2 pops** (`9` table rows incl. Step 1 init; `[x₁, x₂, x₃, x₂, x₄, x₅, x₄, x₆]`, `x₆` evaluated once) when `insert` checks membership (`Exercise 6.3`; `Exercise 6.1` shows reversed initial `[x₆..x₁]` takes **`20` Step 2 pops** as non-empty `X_5`/`X_3` cycle both loops before `x₁` pops at Step 12, popping `x₆` `5` times total across Step 1's empty pop and `4` propagation steps; `Exercise 6.2` traces `Example 6.2`) [PPA Figure 6.1, p. 374] (book p. 374; PDF p. 390), [PPA Example 6.7, p. 374] (book p. 374; PDF p. 390), [PPA Exercise 6.1, p. 389] (book p. 389; PDF p. 405), [PPA Exercise 6.2, p. 389] (book p. 389; PDF p. 405), [PPA Exercise 6.3, p. 389] (book p. 389; PDF p. 405).

### 3.1 Cross-Chapter Unification `U2` (`Table 2.8`) and `U3` (`Table 3.7`)

| Bridge | Earlier Solver | Chapter 6 Specialisation & Complexity | Conditions & Key Differences |
| :--- | :--- | :--- | :--- |
| **`U2`** | Chapter 2 MFP worklist (`Table 2.8`, [intraprocedural-analyses-and-frameworks.md](../../ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md)) [PPA Table 2.8, p. 75] (book p. 75; PDF p. 94) | `Tables 6.1 + 6.2` (`Example 6.5`): edge `(ℓ, ℓ') ∈ F` encodes `Analysis[ℓ'] ⊒ f_ℓ(Analysis[ℓ])`; `N = O(b)`, `M = 1` `⇒` **`O(h · b)`** (`O(b²)` for `RD`, `Example 2.30`) [PPA Example 6.5, p. 372] (book p. 372; PDF p. 388), [PPA Example 2.30, p. 78] (book p. 78; PDF p. 97) | **Conditions**: Finite flow `F`, ACC lattice `L`, unary monotone edge transfers (`M = 1`). **Differs**: `Table 2.8` seeds extremal labels `E` to `ι` in Step 1 and stores CFG edges `(ℓ, ℓ')` rather than arbitrary `M`-variable RHS terms. |
| **`U3`** | Chapter 3 `0-CFA` graph solver (`Table 3.7`, [constraint-generation-and-cubic-solver.md](../../ppa-control-flow-and-constraints/references/constraint-generation-and-cubic-solver.md)) [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196) | `Tables 6.1 + 6.2` (`Examples 6.2, 6.6`): `infl[p] = E[p]`, `Analysis[p] = D[p]`; `N = O(n²)`, `h ≤ n`, `M = 1` `⇒` **`O(n³)`** [PPA Example 6.6, p. 373] (book p. 373; PDF p. 389) | **Conditions**: Syntax-directed finite universe `Term_⋆` (`h ≤ n`) and conditional constraints `if {t} ⊆ p₂ then p₁` (`else ∅`). **Differs**: `Table 3.7` uses a *segregated* variable worklist `W ⊆ Node` pushing single tokens rather than re-evaluating whole sets in integrated `(x ⊒ t)` form (`p. 384`). |

---

## 4. Reverse-Postorder Worklists (`§6.2`, `Table 6.3`) and `U10` Graph Ordering

### 4.1 Constraint Graph `G_𝒮`, Minimal Handles `H_𝒮`, and `Table 6.3` (`pp. 375–378`)

- **Dependency digraph `G_𝒮`**: vertices are constraints `(x_i ⊒ t_i)`; directed edge `(x_i ⊒ t_i) → (x_j ⊒ t_j)` iff `x_i ∈ FV(t_j)` (`(x_j ⊒ t_j) ∈ infl[x_i]`) [PPA §6.2, p. 375] (book p. 375; PDF p. 391).
- **Minimal handles vs single roots (`G-U6-10`, `U10`)**: Forward `WHILE` systems usually have one root (`{x₁}` in `Example 6.8` / `Figure 6.2`), whereas backward DFA and `0-CFA` (`Example 6.2`) lack a single root. Choose a **minimal handle `H_𝒮`** (`{x₂, x₄}` in `Example 6.2` — always exists, not necessarily unique) and run `Table C.1` to build DFSF `T` and `rPostorder` [PPA §6.2, p. 375] (book p. 375; PDF p. 391), [PPA Figure 6.2, p. 376] (book p. 376; PDF p. 392), [PPA Example 6.8, p. 376] (book p. 376; PDF p. 392), [PPA Table C.1, p. 421] (book p. 421; PDF p. 436).
- **Double-buffered `(W.c, W.p)` (`Table 6.3`, `G-U6-11`)** [PPA Table 6.3, p. 376] (book p. 376; PDF p. 392):
  ```text
  empty = (nil, ∅)
  insert((x ⊒ t), (W.c, W.p)) = (W.c, (W.p ∪ {x ⊒ t}))
  extract((W.c, W.p)):
      if W.c = nil then W.c := sort_rPostorder(W.p); W.p := ∅
      return (head(W.c), (tail(W.c), W.p))
  ```
  - **Why two structures (`G-U6-11`) `[derived]`**: Draining `W.c` before sorting `W.p` prevents a low-`rPostorder` self-loop from starving downstream nodes in a single min-heap. `Figure 6.3` / `Example 6.9` finishes in **`11` Step 2 pops** (`8` Step 2 pops / `9` table rows incl. Step 1 init when deduplicated against `W.p ∪ W.c` in `Exercise 6.6`, evaluating `x₆` once; note `Figure 6.3` row 6 prints the refilled `W.c` one step early, `G-U6-12`) [PPA Figure 6.3, p. 377] (book p. 377; PDF p. 393), [PPA Example 6.9, p. 378] (book p. 378; PDF p. 394), [PPA Exercise 6.6, p. 389] (book p. 389; PDF p. 405).
  - **Eager current-pass refinement (`Exercise 6.7`)**: With two priority queues, route `x' ⊒ t'` directly to `W.c` when `rPostorder[x' ⊒ t'] > rPostorder[x ⊒ t]` (downstream in the active sweep!) and to `W.p` only when `≤` [PPA Exercise 6.7, p. 390] (book p. 390; PDF p. 406).
  - **Data-structure caveat (`pp. 377–378`, `G-U6-12`)**: `2-3` trees (`[4]`) cost `O(N log₂ N)` per `N` ops; an `N`-bit vector `W.p` gives `O(1)` insert and `O(N)` refill scan on dense passes, though `Θ(h · N)` sparse 1-bit refills scan `Θ(h · N²)` bits unless paired with `[external: Briggs–Torczon sparse sets]` or priority queues [PPA §6.2, p. 377] (book p. 377; PDF p. 393), [PPA §6.2, p. 378] (book p. 378; PDF p. 394).

### 4.2 Dual-Lattice Polarity on `Must` Analyses (`Exercises 6.4, 6.8`, `G-U6-21`)

For greatest-fixed-point intersection equations such as node dominators `Dom(n) = {n}` (`n ∈ H`) else `{n} ∪ ⋂_{(n',n)∈A} Dom(n')` (`Exercise 6.4`) or Available Expressions (`Exercise 6.8`), instantiate `L = (𝒫(U), ⊇)`: Step 1's **`⊥` is the full universe `U`** (`N` or `AExp_⋆`, **never** `∅`!), `⊔` is **`∩`**, and `Analysis[x] ⋣ new` tests `¬(Analysis[x] ⊆ new)` [PPA Exercise 6.4, p. 389] (book p. 389; PDF p. 405), [PPA Exercise 6.8, p. 390] (book p. 390; PDF p. 406).

---

## 5. Round Robin (`§6.2.1`, `Table 6.4`) and `Lemma 6.12`

### 5.1 `Table 6.4` and `Lemma 6.11` (`pp. 378–380`)

Pre-ordering `(x_i ⊒ t_i)_{i=1}^N` in `rPostorder` eliminates `W.p` and `infl` in favour of boolean `change` [PPA Lemma 6.11, p. 378] (book p. 378; PDF p. 394), [PPA Table 6.4, p. 379] (book p. 379; PDF p. 395), [PPA Exercise 6.9, p. 390] (book p. 390; PDF p. 406):
```text
Step 1: for all x ∈ X do Analysis[x] := ⊥;   change := true;
Step 2: while change do
            change := false;
            for i := 1 to N do
                new := eval(t_i, Analysis);
                if Analysis[x_i] ⋣ new then
                    change := true;   Analysis[x_i] := Analysis[x_i] ⊔ new;
```
On `Example 6.1`, `Figure 6.4` / `Example 6.10` converges in Pass 1 and halts after Pass 2 (`1` Step 1 + `2` `while`-passes = `3` iterations, `12` `eval` calls; `Mini Project 6.1` benchmarks Round Robin against deduplicated LIFO, RPO, and SCC) [PPA Example 6.10, p. 378] (book p. 378; PDF p. 394), [PPA Figure 6.4, p. 379] (book p. 379; PDF p. 395), [PPA Mini Project 6.1, p. 387] (book p. 387; PDF p. 403).

### 5.2 Bit-Vector Loop-Connectedness Bound (`Lemma 6.12`, `[92]`) and Scope Preconditions (`G-U6-13..15`)

**`Lemma 6.12`** [PPA Lemma 6.12, p. 380] (book p. 380; PDF p. 396): *Under the preconditions below, `Table 6.4` halts after at most **`d(G_𝒮, T) + 3`** iterations (`1` Step 1 init + `≤ d + 1` propagation sweeps + `1` final quiescence sweep, `G-U6-14`) and performs **`O((d(G_𝒮, T) + 1) · N)`** assignments (`Example 6.13`: `d = 1 ⇒ ≤ 4` vs `3` actual; note `p. 380` mis-cites `Example 2.8` instead of `Example 2.30` for `O(b²)`, `G-U6-14`)* [PPA Example 6.13, p. 381] (book p. 381; PDF p. 397).

**Mandatory Side Conditions (`G-U6-13`, `G-U6-15` — Never Quote Unconditionally)**:
1. **Bit Vector (or Fast Distributive) Transfers**: `L = 𝒫(D)` (`D` finite, `⊑ ∈ {⊆, ⊇}`) and every RHS has single-variable affine form `t_i = (x_{j_i} ∩ Y_i^1) ∪ Y_i^2` (or `f ∘ f ⊑ f ⊔ id` distributive in `Exercise 6.14`). Does **not** hold for Constant Propagation, `0-CFA`, or intervals!
2. **Exact `rPostorder` of DFSF `T`**: constraints `1..N` are ordered by `rPostorder` from `Table C.1` over a valid handle `H_𝒮`, where `d(G_𝒮, T)` counts maximal back edges on any cycle-free path (`U10`).
3. **Reducibility vs Irreducibility (`G-U6-15`)**: on `WHILE` programs `d(G_𝒮, T)` is independent of `T` and equals loop nesting depth `d` (`d ≤ 3` Fortran Folk Theorem `[98]`, `O((d + 1) · b)`), whereas on irreducible/`[external: obfuscated]` graphs `d(G_𝒮, T)` depends on `T` and can reach `Θ(N)` [PPA §6.2.1, p. 380] (book p. 380; PDF p. 396), [PPA §6.2.1, p. 381] (book p. 381; PDF p. 397).
