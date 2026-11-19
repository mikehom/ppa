<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Standalone L0 ambient context for Chapter 2 Data Flow Analysis, Interprocedural Context, and Shape Analysis. -->
<!-- @description: Orientation for data flow over first-order WHILE programs: reaching definitions, live variables, available and very busy expressions, gen/kill bit vectors, monotone and distributive frameworks, MFP versus MOP, interprocedural call strings and assumption sets over valid paths, and shape graphs with abstract locations, summary nodes and sharing for heap pointers. Use when reasoning about forward/backward direction, may/must merging, kill sets, slicing, or pointer aliasing in imperative statements. -->

# Data Flow Analysis, Interprocedural Context, and Shape Analysis

> Ambient orientation for Chapter 2 of *Principles of Program Analysis* (F. Nielson, H. R. Nielson,
> C. Hankin; corrected second printing, 2005). Grounded in [PPA §2.1, p. 35] (book p. 35; PDF p. 54)
> through [PPA Exercise 2.25, p. 139] (book p. 139; PDF p. 158).

## What Chapter 2 Is About

Chapter 2 builds a single lattice-theoretic machinery — **Monotone Frameworks** — that covers classical
compiler data flow analyses, chains for program slicing and rewriting, constant propagation, context-sensitive
interprocedural calls, and heap shape analysis [PPA §2.1, p. 35] (book p. 35; PDF p. 54)
[PPA §2.3, p. 65] (book p. 65; PDF p. 84) [PPA §2.6, p. 104] (book p. 104; PDF p. 123).

All four classical analyses operate over elementary blocks of an explicitly represented control flow graph:
- **Forward analyses** follow `flow(S⋆)` from `init(S⋆)`: Available Expressions (`AE`, must) and Reaching
  Definitions (`RD`, may) [PPA §2.1.1, p. 39] (book p. 39; PDF p. 58) [PPA §2.1.2, p. 43] (book p. 43; PDF p. 62).
- **Backward analyses** follow `flow^R(S⋆)` from `final(S⋆)`: Very Busy Expressions (`VB`, must) and Live
  Variables (`LV`, may) [PPA §2.1.3, p. 46] (book p. 46; PDF p. 65) [PPA §2.1.4, p. 49] (book p. 49; PDF p. 68).

## The Four-Square Polarity & Solver Guarantees

Because an analysis seeks the **most informative safe answer**, must and may analyses take opposite fixed
points in set inclusion (`⊆`), yet both compute the **least fixed point (`MFP`)** once information order
`⊑` is oriented toward precision growth (`⊑ = ⊇` for must/`⋂`, `⊑ = ⊆` for may/`⋃`)
[PPA §2.3, p. 66] (book p. 66; PDF p. 85) [PPA §2.4.1, p. 74] (book p. 74; PDF p. 93).

- **Every Monotone Framework** pairs a complete lattice `L` obeying the Ascending Chain Condition (ACC)
  with composition-closed monotone transfers `𝓕` [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87). Worklist
  iteration (`MFP`) terminates and safely approximates all-paths `MOP` (`MFP ⊒ MOP`)
  [PPA Lemma 2.29, p. 75] (book p. 75; PDF p. 94) [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99).
- **Exactness (`MFP = MOP`)** holds when transfer functions distribute over binary joins (`f(l₁ ⊔ l₂) = f(l₁) ⊔ f(l₂)`)
  and every label is reachable (`path∘(ℓ) ≠ ∅`) [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99).
- **Hierarchy (`Bit Vector ⊂ Distributive ⊂ Monotone`)**: Classical `gen/kill` bit-vector frameworks are
  strictly narrower than distributive frameworks (copy/faint variable propagation is distributive but not
  bit-vector) [PPA Exercise 2.9, p. 137] (book p. 137; PDF p. 156), while Constant Propagation (`Table 2.7`)
  is monotone yet non-distributive (its `MOP` is undecidable via MPCP)
  [PPA Lemma 2.27, p. 73] (book p. 73; PDF p. 92) [PPA Lemma 2.31, p. 79] (book p. 79; PDF p. 98).

## Interprocedural Context & Flow Sensitivity

Naive interprocedural equations treat call `(ℓ_c; ℓ_n)` and return `(ℓ_x; ℓ_r)` edges like `goto`s,
allowing unrealizable cross-over paths across distinct call sites [PPA §2.5.2, p. 88] (book p. 88; PDF p. 107).

- **Valid Paths (`VP⋆`) and `MVP`** restrict paths to balanced call/return parentheses (`inter-flow⋆`),
  plus open active calls (`MVP ⊑ MOP`, still undecidable in general) [PPA §2.5.2, p. 89] (book p. 89; PDF p. 108)
  [PPA §2.5.3, p. 90] (book p. 90; PDF p. 109).
- **Embellished Frameworks (`L̂ = Δ → L`)** track calling context `δ ∈ Δ` and require a **binary** return
  function `f̂²_{ℓ_c,ℓ_r}(A∘(ℓ_c), A∘(ℓ_r))` to merge callee exit results with caller locals
  [PPA §2.5.3, p. 93] (book p. 93; PDF p. 112). Three context styles trade precision, cost, and monotonicity:
  bounded call strings `Δ = Lab^{\le k}` [PPA §2.5.4, p. 97] (book p. 97; PDF p. 116), small assumption
  sets `Δ = D` (additive pair summaries), and large assumption sets `Δ = 𝒫(D)` (exact grouping makes
  transfers non-monotone!) [PPA §2.5.5, p. 100] (book p. 100; PDF p. 119).
- **Flow-insensitive summaries** (`AV, CP, IAV`) ignore statement order and compute call graphs and global
  side-effect sets at procedure level [PPA §2.5.6, p. 101] (book p. 101; PDF p. 120).

## Heap Shape Graphs & Strong Updates

When pointers target anonymous dynamically allocated heap cells, unbounded concrete heaps map into finite
**compatible shape graphs** `(S, H, is)` over abstract locations `n_X` (`X ⊆ Var⋆`) plus summary node
`n_∅` (`∅`), governed by five structural invariants [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133).

- Every non-empty `n_X` represents at most one concrete cell with deterministic outgoing selectors,
  enabling **strong nullification (`kill_x`)** and **strong updates (`kill_{x.sel}`)** inside each graph
  while joining distinct possibilities via outer powerset union (`𝒫(SG)`) [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134).
- Dereferencing into `n_∅` triggers **materialisation** (`[x:=y.sel]^ℓ` Case 3), splitting candidate
  named cells `n_{x}` out of `n_∅` [PPA §2.6.3, p. 122] (book p. 122; PDF p. 141).

## Core Chapter 2 Invariants & Traps

1. **Preconditions before equations**: §2.1 analyses assume *label consistency*, finite program sets
   (`Lab⋆, Var⋆, AExp⋆`), and isolated boundaries — use `§2.3`'s unconditional `⊔ ι^ℓ_E` equation
   whenever programs start or end with loops (`Example 2.3`) [PPA §2.3, p. 66] (book p. 66; PDF p. 85).
2. **Do not confuse `is` with stack aliasing**: `n_X ∈ is` records `≥ 2` incoming **heap** pointers,
   never two stack variables pointing to the same cell (`n_{x,y}`); unsharing requires both `#into(n_U, H') ≤ 1`
   and no incoming edge from `n_∅` [PPA §2.6.2, p. 113] (book p. 113; PDF p. 132)
   [PPA §2.6.3, p. 125] (book p. 125; PDF p. 144).
3. **Printed errata exist**: §2.2.2 omits isolated exits on `LV^⊆`, §2.5.6 prints `"context-insensitive"` for
   flow-insensitive and omits `\ {y}` in `IAV(p)`, §2.5.5 writes `ι̂ = {({ι}, ι)}` for set `ι`, and
   `Shape` neither filters boolean guards nor performs GC (`Exercises 2.21*, 2.24*`).

## Key Vocabulary

| Term | Meaning in Chapter 2 |
| :--- | :--- |
| Label consistency | Distinct occurrences of any label `ℓ` always label identical elementary blocks [PPA §2.1, p. 39] (book p. 39; PDF p. 58) |
| Non-trivial expression | Any arithmetic subexpression other than a variable or numeral [PPA §2.1, p. 39] (book p. 39; PDF p. 58) |
| Isolated entry / exit | Entry `init(S⋆)` has no predecessors in `flow(S⋆)` / `final(S⋆)` has no successors [PPA §2.1, p. 39] (book p. 39; PDF p. 58) |
| `ud`- / `du`-chain | Definition-clear links from a use back to reaching defs (`ud`) or defs to uses (`du`) [PPA §2.1.5, p. 52] (book p. 52; PDF p. 71) |
| Monotone Framework | ACC complete lattice `(L, ⨆)` plus composition-closed monotone `𝓕 ∋ id` [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87) |
| Bit Vector Framework | Finite `𝒫(D)` framework with `f(Y) = (Y ∩ Y_f^1) ∪ Y_f^2` [PPA Exercise 2.9, p. 137] (book p. 137; PDF p. 156) |
| `MFP` vs `MOP` / `MVP` | Iterative least fixed point vs join over all CFG paths / valid balanced-call paths [PPA §2.4.1, p. 74] (book p. 74; PDF p. 93) [PPA §2.5.2, p. 90] (book p. 90; PDF p. 109) |
| `inter-flow⋆` | Four-tuples `(ℓ_c, ℓ_n, ℓ_x, ℓ_r)` pairing each call with its matching return [PPA §2.5, p. 84] (book p. 84; PDF p. 103) |
| Call string (`Lab^{\le k}`) | Bounded suffix of pending call labels used as context `δ` [PPA §2.5.4, p. 97] (book p. 97; PDF p. 116) |
| Assumption set | Data-based call context (`Δ = 𝒫(D)` large vs `Δ = D` small) [PPA §2.5.5, p. 99] (book p. 99; PDF p. 118) |
| Shape graph `(S, H, is)` | Compatible abstract stack, heap, and heap-sharing summary over `ALoc` [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133) |
| Summary location `n_∅` | Abstract node representing all heap cells unpointed by stack variables [PPA §2.6.2, p. 110] (book p. 110; PDF p. 129) |
| Materialisation | Splitting a concrete target `n_{x}` out of summary `n_∅` on `[x := y.sel]` [PPA §2.6.3, p. 121] (book p. 121; PDF p. 140) |
| Strong update | Replacing an existing `x` or `x.sel` edge cleanly using non-summary uniqueness [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134) |

## Out of Scope Here (Adjacent Skills)

Chapter 2 stops at constant syntactic procedures and one-level pointers without widening: indirect/higher-order
calls belong to `ppa-control-flow-and-constraints`, Galois abstractions/widening to `ppa-abstract-interpretation`,
type/effect/region systems to `ppa-types-effects-and-regions`, RPO/SCC solver internals to `ppa-fixedpoint-solvers`,
and adversarial `[external: taint/sanitizer]` security policies to `ppa-cyber-vulnerability-analysis`.

## Where to Go Next

When the optional `skills/` channel is installed, Chapter 2 procedures and formal specifications live relative to
the knowledge root:

- Actionable design & verification workflows: skills/ppa-dataflow-and-slicing/SKILL.md
- Classical DFA (`AE, RD, VB, LV`), `ud`/`du` chains, Monotone Frameworks, `MFP`/`MOP`:
  skills/ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md
- Operational correctness (`§2.2`, `Mini Project 2.2`) & interprocedural context (`§2.5`):
  skills/ppa-dataflow-and-slicing/references/interprocedural-and-correctness.md
- Heap pointer semantics, compatible shape graphs, materialisation (`§2.6`):
  skills/ppa-dataflow-and-slicing/references/shape-analysis.md
- Cross-approach master router and Chapter 1 / Appendices A–C: skills/ppa-program-analysis/SKILL.md
