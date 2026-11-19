<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Standalone L0 ambient orientation for Chapter 6 fixed-point solvers and Unit 6 Index/Bibliography lookup. -->
<!-- @description: Orientation for algorithms that compute least solutions of flow-variable inequation systems: the abstract worklist with influence sets, stack or queue realisations, reverse postorder scheduling, round robin sweeps, strong component ordering, termination via lattice height, iteration cost, and local demand-driven solving, plus lookup in the subject index and bibliography. Use when a specification is correct but runs slowly, fails to terminate, or needs a scheduling strategy. -->

# PPA Fixed-Point Solvers & Iteration Order (`Chapter 6`)

> Ambient orientation for Chapter 6 (*Algorithms*), the Subject Index, and the Bibliography of
> *Principles of Program Analysis* (F. Nielson, H. R. Nielson, C. Hankin; corrected second printing,
> 2005). Grounded in [PPA §6.1, p. 365] (book p. 365; PDF p. 381) through
> [PPA Exercise 6.14, p. 392] (book p. 392; PDF p. 408), [PPA Index, p. 433] (book p. 433; PDF p. 447),
> and [PPA Bibliography, p. 439] (book p. 439; PDF p. 452).

## What Chapter 6 Is About

Chapters 2–5 specify *what* static property an analysis approximates (per-point data flow,
higher-order closure sets, Galois abstract domains, or annotated types and effects); Chapter 6
(*Algorithms*, book pp. 365–392 / PDF pp. 381–408, offset `+16`; `G-U6-01`) answers **how to compute
the least solution `μ_𝒮 = lfp(F_𝒮)` efficiently** [PPA §6.1, p. 365] (book p. 365; PDF p. 381).

Every finite monotone analysis compiles down to a system of flow-variable inequations
`𝒮 = (x_i ⊒ t_i)_{i=1}^N` over a complete lattice `(L, ⊑)` satisfying the Ascending Chain Condition
(`ACC`), unifying Chapter 2's CFG edge worklist (`Table 2.8`, `Example 6.5`, `U2`) and Chapter 3's
cubic `0-CFA` solver (`Table 3.7`, `Examples 6.2, 6.6`, `U3`) under one parameterised engine
(`Table 6.1`) [PPA §6.1, p. 367] (book p. 367; PDF p. 383), [PPA Table 6.1, p. 369] (book p. 369; PDF p. 385).

## Core Mental Model: Correctness Is Order-Free, Performance Is Graph-Driven

1. **Chaotic Correctness Invariant (`Lemma 6.4`)**:
   - `Table 6.1` seeds `W` with all constraints, sets `Analysis[x] := ⊥_L`, builds the inverted
     observer index `infl[x] = {(x' ⊒ t') ∈ 𝒮 | x ∈ FV(t')}`, and pops `(x ⊒ t)` updating
     `Analysis[x] := Analysis[x] ⊔ eval(t, Analysis)` and re-queuing `infl[x]` strictly when
     `Analysis[x] ⋣ new`.
   - Under `ACC`, monotone `⟦t⟧`, and closed flow variables `FV(t_i) ⊆ X = LHS(𝒮)` (`G-U6-04`),
     **every** fair worklist realisation (`LIFO`, `FIFO`, `RPO`, `SCC`) terminates at the exact same
     least fixed point `Analysis = μ_𝒮` (`G-U6-06`) [PPA Lemma 6.4, p. 370] (book p. 370; PDF p. 386).
   - **Never Return Early (`G-U6-07`) `[derived]`**: `Lemma 6.4(i)` guarantees only `Analysis_i ⊑ μ_𝒮` from
     below. An intermediate state may already equal `μ_𝒮`, but it is not *certified* reductive
     (`Analysis ∈ Red(F_𝒮)`, `[external: post-fixed-point]`) until `W = empty`. Cutting off a worklist at a
     step cap *may* under-approximate may-analyses unless dirty cones are widened or topped
     [PPA §6.1.1, p. 371] (book p. 371; PDF p. 387).

2. **Granularity Before Ordering — Split `M`-Ary Joins (`Exercise 6.5`)**:
   - Multi-LHS inequations `x ⊒ t₁, ···, x ⊒ t_M` share all solutions with `x = x ⊔ t₁ ⊔ ··· ⊔ t_M`
     and share the **least** solution with `x = t₁ ⊔ ··· ⊔ t_M` (`G-U6-02`)
     [PPA §6.1, p. 366] (book p. 366; PDF p. 382).
   - Splitting one `O(M)`-sized join equation into `M` unary `O(1)` inequations drops `Table 6.1`'s
     worst-case cost by a factor of `M`, from `O(h · M² · N)` to **`O(h · M · N)`** (`G-U6-03`)
     [PPA §6.1.1, p. 372] (book p. 372; PDF p. 388), [PPA Exercise 6.5, p. 389] (book p. 389; PDF p. 405).

3. **Graph-Ordered Iteration Hierarchy (`§§6.1.2–6.3`, `U10`)**: the schedule changes speed, never the result.
   - Build the constraint dependency digraph `G_𝒮` (`c_i → c_j` iff `LHS(c_i) ∈ FV(RHS(c_j))`). When it
     has no single root (backward DFA, `0-CFA`), start Appendix C's depth-first traversal from a
     **minimal handle `H_𝒮`** [PPA §6.2, p. 375] (book p. 375; PDF p. 391).
   - **LIFO / FIFO (`Table 6.2`)**: the simplest realisations; without membership checks they re-queue
     duplicate constraints [PPA Figure 6.1, p. 374] (book p. 374; PDF p. 390).
   - **Reverse postorder (`Table 6.3`)**: drain the current pass `W.c` in `rPostorder` before refilling it
     from the pending set `W.p`, so producers run before consumers
     [PPA Table 6.3, p. 376] (book p. 376; PDF p. 392).
   - **Round Robin (`Table 6.4`)**: drops `W` and `infl` for repeated `1..N` sweeps until no `change`. The
     `d(G_𝒮, T) + 3` pass bound of `Lemma 6.12` holds **only for Bit Vector Frameworks** (`L = 𝒫(D)`, every
     right-hand side of the form `(x_{j_i} ∩ Y_i^1) ∪ Y_i^2`), never for general lattices such as Constant
     Propagation or `0-CFA` [PPA Lemma 6.12, p. 380] (book p. 380; PDF p. 396).
   - **Strong components (`Tables 6.5–6.6`)**: order the reduced component DAG topologically and settle
     each loop component completely before its downstream consumers
     [PPA Table 6.6, p. 384] (book p. 384; PDF p. 400).

## Beyond Global ACC Worklists (`Concluding Remarks` & `Exercises 6.4, 6.13`)

- **`Must` Lattice Dualisation (`Exercises 6.4, 6.8`, `G-U6-21`)**: Greatest-solution equations
  (`Dom(n)`, `AE`) run on `(𝒫(U), ⊇)` with **`⊥_L = U`** and `⊔_L = ∩`
  [PPA Exercise 6.4, p. 389] (book p. 389; PDF p. 405).
- **Pointwise Worklist Widening (`Exercise 6.13`, `U7`, `G-U6-22`)**: Removes `ACC` on finite `X → L`
  via `Analysis[x] := Analysis[x] ∇ new`, keeping the mandatory `if Analysis[x] ⋣ new` guard so
  non-monotone `∇` cannot diverge [PPA Exercise 6.13, p. 391] (book p. 391; PDF p. 407).
- **Local Demand-Driven & Elimination Solvers (`Concluding Remarks pp. 385–386`, `G-U6-19`)**:
  Top-down (`[29]`), timestamp (`[51, 54]`), and differential (`[52, 53]`) local solvers evaluate
  only the backward dependency cone of queried variables, while structural (`[154]`), interval
  (`[11]`), and path-algebra (`[170, 171]`) elimination solvers reduce structured CFGs algebraically
  [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401),
  [PPA Chapter 6 Concluding Remarks, p. 386] (book p. 386; PDF p. 402).

## Key Vocabulary

| Term | Meaning in Chapter 6 |
| :--- | :--- |
| Flow variable (`x ∈ X`) | Unknown denoting per-point DFA fact or CFA cache/environment entry [PPA §6.1, p. 365] (book p. 365; PDF p. 381) |
| Influence set (`infl[x]`) | Set of constraints `(x' ⊒ t') ∈ 𝒮` mentioning `x ∈ FV(t')` [PPA §6.1.1, p. 369] (book p. 369; PDF p. 385) |
| Integrated vs segregated `W` | Queuing constraints `(x ⊒ t)` vs queuing flow variables `x` (`[69]`) [PPA Chapter 6 Concluding Remarks, p. 384] (book p. 384; PDF p. 400) |
| Minimal handle (`H_𝒮`) | Minimal vertex set reaching every node of `G_𝒮` (`{x₂, x₄}` in `Ex 6.2`) [PPA §6.2, p. 375] (book p. 375; PDF p. 391) |
| `(W.c, W.p)` | Current RPO pass list paired with pending next-pass set (`Table 6.3`) [PPA Table 6.3, p. 376] (book p. 376; PDF p. 392) |
| Loop connectedness `d(G_𝒮, T)` | Maximum back edges on any cycle-free path of `G_𝒮` wrt DFSF `T` [PPA §6.2.1, p. 380] (book p. 380; PDF p. 396) |
| `srPostorder = (scc, rp)` | Lexicographic `(topological SCC id, local RPO)` pair (`Table 6.5`) [PPA Table 6.5, p. 382] (book p. 382; PDF p. 398) |
| `(W.c, W.pc, W.pf)` | Three-queue SCC split: current pass, current SCC pending, future SCCs [PPA Exercise 6.12, p. 391] (book p. 391; PDF p. 407) |
| Fast function & closure `f̄` | `f ∘ f ⊑ f ⊔ id` and `f̄ = (f ⊔ id)^{i_f}` closing distributive loops [PPA Exercise 6.14, p. 391] (book p. 391; PDF p. 407) |
| Local solver | Demand-driven partial fixed-point engine (`[29, 51–54]`) [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401) |

## Out of Scope Here (Adjacent Skills)

Formulating transfer equations or shape graphs belongs to `ppa-dataflow-and-slicing`, generating
higher-order closure constraints to `ppa-control-flow-and-constraints`, designing Galois connections
and domain widenings to `ppa-abstract-interpretation`, building annotated type/effect systems to
`ppa-types-effects-and-regions`, and `[external: security threat/taint]` policies to `ppa-cyber-vulnerability-analysis`.
Unit 6 also indexes the 5-page Subject Index across book pages 433–437 / PDF pages 447–451 (offset `+14`)
and 185-entry Bibliography across book pages 439–452 / PDF pages 452–465 (offset `+13`; `G-U6-24`)
[PPA Index, p. 433] (book p. 433; PDF p. 447), [PPA Bibliography, p. 439] (book p. 439; PDF p. 452).

## Where to Go Next

When the optional `skills/` channel is installed, Chapter 6 procedures and references live at:

- Actionable solver workflows & debugging playbooks: skills/ppa-fixedpoint-solvers/SKILL.md
- Worklist ADTs, RPO `(W.c, W.p)`, Round Robin `Lemma 6.12`:
  skills/ppa-fixedpoint-solvers/references/worklist-and-rpo-algorithms.md
- SCC condensation (`Table 6.6`), widening (`Ex 6.13`), fastness closure (`Ex 6.14`), local &
  elimination solvers:
  skills/ppa-fixedpoint-solvers/references/scc-round-robin-and-advanced-solvers.md
