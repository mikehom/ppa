<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-008: Shared Unit 0 L1 reference, hosted with the router skill and linked from it. -->

# Appendix C Reference: Graphs, Depth-First Spanning Forests, Reverse Postorder, Regular Expressions

Scope: Appendix C, sections C.1 to C.3 and the Concluding Remarks [PPA Appendix C, p. 417] (book p. 417; PDF p. 432).
Every item carries a canonical citation such as `[PPA §C.1, p. 417] (book p. 417; PDF p. 432)`. Numbered
items keep the book's numbering; unnumbered items carry `[U0:<section>-<letter>]` ids. Terms tagged
`[external]` are not the book's terminology; `[derived]` marks consequences justified directly from printed
definitions. Book p. 428 is a blank page absent from the PDF and is never cited.

Proofs are not reproduced here. They live in the L3 shard corpus/shards/RAW_SHARD_00_appendices.md
(Appendix C anchors).

Closed inventory of numbered items in Appendix C: Example C.1, Example C.2, Fact C.3, Example C.4,
Lemma C.5, Example C.6, Example C.7, Example C.8, Lemma C.9, Corollary C.10, Corollary C.11, Lemma C.12,
Example C.13, Corollary C.14; Figures C.1 to C.3; Table C.1. Appendix C has no Exercises section
[PPA Appendix C Concluding Remarks, p. 427] (book p. 427; PDF p. 442).

---

## 1. Graphs and forests (C.1)

### [U0:C.1-a] Directed graph
[PPA §C.1, p. 417] (book p. 417; PDF p. 432)

A directed graph (digraph, or graph) `G = (N, A)` has a **finite** set `N` of nodes (vertices) and a set
`A ⊆ N × N` of edges (arcs), excluding parallel multi-edges and infinite node sets (BKL-023, G-U0-26). Edge `(n₁, n₂)` has source `n₁` and target `n₂`; if `n₁ = n₂` it is a
self-loop. Examples: Example C.1 [PPA §C.1, p. 417] (book p. 417; PDF p. 432), forward flow graph
`(labels(S), flow(S))`, backward flow graph `(labels(S), flowᴿ(S))`, and `(Lab, F)` for a finite label set
and flow relation; Example C.2 [PPA §C.1, p. 417] (book p. 417; PDF p. 432), continued
[PPA §C.1, p. 418] (book p. 418; PDF p. 433), the constraint graph `(N⋆, A⋆)` of a FUN program, with edge
`(p₁, p₂)` for each `p₁ ⊆ p₂` and **both** edges `(p, p₂)` and `(p₁, p₂)` for each conditional constraint
`{t} ⊆ p ⇒ p₁ ⊆ p₂` (G-U0-27).

### [U0:C.1-b] and [U0:C.1-c] Paths, reachability, cycles
[PPA §C.1, p. 417] (book p. 417; PDF p. 432); continued [PPA §C.1, p. 418] (book p. 418; PDF p. 433)

- A path from `n₀` to `nₘ` is an edge sequence `(n₀,n₁), …, (n_{m−1},nₘ)` of length `m ≥ 0`; `m = 0` is the
  trivial path. `n′` is reachable from `n` iff there is a (possibly trivial) path from `n` to `n′`.
- Node-sequence notation (as in Chapter 2): `p = [n₀, n₁, …, nₘ]`, **never empty**; the trivial path from
  `n₀` is `[n₀]`, a self-loop is `[n₀, n₀]`. Concatenation: `[n₀,…,nₘ][nₘ,…,nₖ] = [n₀,…,nₖ]` (`nₘ` once).
- `paths•(n, n′) = { [n₀,…,nₘ] | m ≥ 0 ∧ n₀ = n ∧ nₘ = n′ ∧ ∀i < m : (nᵢ, n_{i+1}) ∈ A }`.
- A cycle is a **non-trivial** path from a node to itself (possibly a self-loop):
  `cycles(n) = { [n₀,…,nₘ] | m ≥ 1 ∧ n₀ = n ∧ nₘ = n ∧ ∀i < m : (nᵢ, n_{i+1}) ∈ A }`
  `= { p ∈ paths•(n, n) | p ≠ [n] }`.

### [U0:C.1-d] Multiple-entry cycle, acyclic graph, DAG, topological sort
[PPA §C.1, p. 418] (book p. 418; PDF p. 433)

- A cycle `[n₀,…,nₘ]` is multiple entry iff it contains two **distinct nodes** `nᵢ ≠ nⱼ` (not merely distinct
  indices) such that there are (not necessarily distinct) nodes `nᵢ′`, `nⱼ′` **external to the cycle** with
  `(nᵢ′, nᵢ), (nⱼ′, nⱼ) ∈ A`.
- `G` is acyclic iff `∀n ∈ N : cycles(n) = ∅`; a directed acyclic graph is a DAG.
- A topological sort is a total ordering of the nodes with `n` strictly before `n′` for every edge
  `(n, n′)`. A directed graph has a topological sort **iff** it is acyclic.

### [U0:C.1-e], Fact C.3, [U0:C.1-f] Strong components and the reduced graph
[PPA §C.1, p. 418] (book p. 418; PDF p. 433); continued [PPA §C.1, p. 419] (book p. 419; PDF p. 434)

- `n` and `n′` are strongly connected iff there are (possibly trivial) paths from `n` to `n′` and from
  `n′` to `n`. `𝒮𝒞 = { (n, n′) | n and n′ are strongly connected } ⊆ N × N`.
- **Fact C.3**: `𝒮𝒞` is an equivalence relation [PPA §C.1, p. 418] (book p. 418; PDF p. 433).
- Its equivalence classes are the strong components (strongly connected components). `G` is strongly
  connected iff it has exactly one strongly connected component.
- Example C.4: in uniquely labelled WHILE statements, the nodes of the outermost loop in any nested
  sequence of loops constitute a strongly connected component, in both forward and backward flow graphs
  [PPA §C.1, p. 419] (book p. 419; PDF p. 434).
- Reduced graph: one node per strongly connected component; an edge from one node to **another distinct**
  node iff some original edge goes from a node of the first component to a node of the second. Hence the
  reduced graph has no self-loops.

### Lemma C.5 (reduced graph)
[PPA §C.1, p. 419] (book p. 419; PDF p. 434)

For any graph `G` the reduced graph is a DAG.

### [U0:C.1-g], [U0:C.1-h], and [U0:C.1-i] Handles, roots, and handle paths
[PPA §C.1, p. 419] (book p. 419; PDF p. 434); continued [PPA §C.1, p. 420] (book p. 420; PDF p. 435)

| Notion | Definition |
| :--- | :--- |
| handle `H ⊆ N` | every `n ∈ N` is reachable by a (possibly trivial) path from some `h ∈ H`; `H = N` is always a handle |
| root `r ∈ N` | every `n ∈ N` is reachable from `r` by a (possibly trivial) path; `{n}` is a handle iff `n` is a root |
| dummy root | if `H` is a handle for `(N, A)` and `r ∉ N`, then `r` is a root of `(N ∪ {r}, A ∪ { (r, h) \| h ∈ H })`; each `(r, h)` is a dummy edge |
| minimal handle | no proper subset `H′ ⊂ H` is a handle; minimal handles always exist since `N` is finite |
| rooted graph | the minimal handle is a singleton, which holds iff the graph has a root |
| `path•^H(n)` [U0:C.1-i] | `⋃{ paths•(h, n) \| h ∈ H }`, the paths from `H` to `n`; written `path•(n)` when `H` is implicit |

Example C.6: `init(S)` is a root of `(labels(S), flow(S))` and `{init(S)}` is a minimal handle; `final(S)` is
a handle for the backward flow graph `(labels(S), flowᴿ(S))` (unconditionally for WHILE syntax; general CFGs
with sink-less infinite loops `[external]` require synthetic exit handles — see BKL-017, G-U0-30, G-U0-31)
[PPA §C.1, p. 420] (book p. 420; PDF p. 435).

### [U0:C.1-j] Degrees, forests, trees
[PPA §C.1, p. 420] (book p. 420; PDF p. 435)

- In-degree `m`: the predecessor set `{ n′ | (n′, n) ∈ A }` has cardinality `m`; out-degree similarly.
- A forest (unordered, directed forest) is a DAG whose nodes have **in-degree at most 1**; its in-degree-0
  nodes constitute a minimal handle.
- For `(n, n′) ∈ A`: `n` is the parent of `n′`, `n′` a child of `n`; ancestor and descendant are the
  **reflexive**, transitive closures of parent and child; proper ancestor/descendant additionally `n ≠ n′`.
- A tree is a forest that has a root (exactly one node of in-degree 0). A forest with minimal handle `H`
  is a set of trees, one rooted at each `h ∈ H`.
- Ordered forests and ordered trees additionally order the children of each node linearly.
- Source typo (BKL-020, G-U0-32): the tree paragraph writes `(n₁, n₂) ∈ E` for the edge set `A`.

### [U0:C.1-k] Dominators
[PPA §C.1, p. 420] (book p. 420; PDF p. 435); continued [PPA §C.1, p. 421] (book p. 421; PDF p. 436)

Given `G = (N, A)` with handle `H` (possibly a root `r`, `H = {r}`): `n′` dominates `n` iff **every
(possibly trivial) path from `H` to `n`** contains `n′`. The only dominator of an element of a minimal
handle (such as a root) is the element itself. For any node `n`, the set of dominators is the
**greatest solution** (BKL-016, G-U0-33, G-U0-34) of

```
Dom(n) = {n}                                  if n ∈ H
Dom(n) = {n} ∪ ⋂{ Dom(n′) | (n′, n) ∈ A }     otherwise
```

- `n′` properly dominates `n` iff `n′ ≠ n` and `n′` dominates `n`.
- `n′` directly dominates `n` (the "closest" proper dominator) iff `n′ ∈ Dom(n) \ {n}` and
  `∀n″ ∈ Dom(n) \ {n} : n″ ∈ Dom(n′)`.
- The term immediate dominator `[external]` is not used by the book.

---

## 2. Reverse postorder (C.2)

### Table C.1 (The DFSF Algorithm), verbatim
[PPA Table C.1, p. 421] (book p. 421; PDF p. 436)

```
INPUT:   A directed graph (N, A) with k nodes and handle H
OUTPUT:  (1) A DFSF T = (N, A_T), and
         (2) a numbering rPostorder of the nodes indicating the
             reverse order in which each node was last visited
             and represented as an element of array [N] of int
METHOD:  i := k;
         mark all nodes of N as unvisited;
         let A_T be empty;
         while unvisited nodes in H exists do
             choose a node h in H;
             DFS(h);
USING:   procedure DFS(n) is
             mark n as visited;
             while (n, n') ∈ A and n' has not been visited do
                 add the edge (n, n') to A_T;
                 DFS(n');
             rPostorder[n] := i;
             i := i - 1;
```

Literal-reading gap (BKL-019, G-U0-35): "choose a node h in H" is meant as an **unvisited** `h` (the loop
guard ranges over unvisited nodes in `H`); calling `DFS` again on a visited `h` would renumber it.

### [U0:C.2-a] Spanning forest, DFSF, DFST, reverse postorder
[PPA §C.2, p. 421] (book p. 421; PDF p. 436); continued [PPA §C.2, p. 422] (book p. 422; PDF p. 437)

- A spanning forest for a graph is a forest with the same nodes as the graph and a subset of its edges.
- Table C.1 **non-deterministically** constructs a depth-first spanning forest (DFSF) and numbers the
  nodes in the reverse of the order in which they are last visited: the reverse postorder, an array
  indexed by nodes. A DFSF that is a tree is a depth-first spanning tree (DFST).
- The algorithm does not specify which unvisited node to select at each stage; consequently the DFSF for
  a graph is **not unique** (and neither is rPostorder).

### [U0:C.2-b] The four edge kinds
[PPA §C.2, p. 422] (book p. 422; PDF p. 437)

Relative to a spanning forest; the rPostorder column holds for the forest and numbering of Table C.1.

| Kind | Definition | rPostorder relation for edge `(n, n′)` | Source |
| :--- | :--- | :--- | :--- |
| tree edge | present in the spanning forest | `rPostorder[n] < rPostorder[n′]` | Corollary C.11 |
| forward edge | not a tree edge; from a node to a **proper** descendant | `rPostorder[n] < rPostorder[n′]` | Corollary C.11 |
| back edge | from a descendant to an ancestor, **including self-loops** | `rPostorder[n] ≥ rPostorder[n′]`; `=` iff self-loop | Lemma C.9 |
| cross edge | between nodes unrelated by the ancestor and descendant relations | `rPostorder[n] < rPostorder[n′]`: from later-visited (lower number) to earlier-visited (higher number) | Table C.1 property, Corollary C.11 |

### Figure C.1, Example C.7, and Figure C.2 (running the algorithm)
[PPA Figure C.1, p. 422] (book p. 422; PDF p. 437); [PPA §C.2, p. 422] (book p. 422; PDF p. 437);
[PPA Figure C.2, p. 423] (book p. 423; PDF p. 438) (G-U0-36, G-U0-37)

Figure C.1: nodes `b₁, b₂, b₃, S₁, S₂, S₃`, entry into `b₁`; edges `b₁→b₂`, `b₁→b₃`, `b₂→S₂`, `b₂→S₁`, `b₃→S₁`,
`b₃→S₃`, `S₂→b₂`, `S₃→b₃`; exit from `S₁`. With root `b₁` the algorithm may produce the tree of Figure C.2,
with reverse postorder `b₁, b₃, S₃, b₂, S₁, S₂` (`b₁:1, b₃:2, S₃:3, b₂:4, S₁:5, S₂:6`). `S₂→b₂` and `S₃→b₃` are
back edges; `b₃→S₁` is a cross edge (2 to 5).

### Example C.8 (edge kinds in WHILE flow graphs)
[PPA §C.2, p. 423] (book p. 423; PDF p. 438)

For a uniquely labelled WHILE statement `S` with root `init(S)`, forward flow graph:

| Construct in `S` | Tree edges | Back edges | Cross edges |
| :--- | :--- | :--- | :--- |
| `while b′ do S′` | one | one or more: as many as elements of `final(S′)` | none stated |
| `if b′ then S₁′ else S₂′`, **not** the last statement of `S` and **not** the last statement of a while body | three | none stated | one or more: one fewer than the elements of `final(S₁′) ∪ final(S₂′)` |

No forward edges arise in WHILE; an extension with a one-branch conditional `if b then S` can give rise to
forward edges.

### Lemma C.9 (back edges via rPostorder)
[PPA §C.2, p. 423] (book p. 423; PDF p. 438)

Let `G = (N, A)` be a directed graph, `T` a depth-first spanning forest of `G` and rPostorder the
associated ordering **computed by the algorithm of Table C.1**. An edge `(n, n′) ∈ A` is a back edge **iff**
`rPostorder[n] ≥ rPostorder[n′]`, and is a self-loop iff `rPostorder[n] = rPostorder[n′]`.

### Corollary C.10 (every cycle has a back edge)
[PPA §C.2, p. 424] (book p. 424; PDF p. 439)

Same hypotheses as Lemma C.9. Any cycle of `G` contains at least one back edge.

### Corollary C.11 (rPostorder is a topological sort of the non-back edges)
[PPA §C.2, p. 424] (book p. 424; PDF p. 439)

Same hypotheses as Lemma C.9. rPostorder topologically sorts `T` as well as the forward and cross edges:
`rPostorder[n] < rPostorder[n′]` iff `(n, n′)` is a tree, forward or cross edge.

### [U0:C.2-c] Loop connectedness
[PPA §C.2, p. 424] (book p. 424; PDF p. 439)

Let `G = (N, A)` have handle `H`. The loop connectedness parameter of `G` **with respect to a DFSF `T`
constructed by Table C.1** is the largest number of back edges found in any **cycle-free path** of `G`,
written `d(G, T)`, or `d(G)` when `T` is clear from context. For Figure C.1, `d(G) = 1`.

### [U0:C.2-d] Dominator-back edges and reducibility
[PPA §C.2, p. 424] (book p. 424; PDF p. 439); continued [PPA §C.2, p. 425] (book p. 425; PDF p. 440)

- A dominator-back edge is an edge `(n₁, n₂)` whose **target `n₂` dominates the source `n₁`**. It is a back
  edge regardless of the choice of spanning forest `T` (the path from `H` to `n₁` in `T` must contain `n₂`).
- `G = (N, A)` with handle `H` is reducible **iff** the graph `(N, A \ A_db)`, obtained by removing the set
  `A_db` of dominator-back edges, is **acyclic and still has `H` as handle**.
- The book notes that the literature contains many definitions of reducible graph; this is the book's.

### Figure C.3 (an irreducible graph)
[PPA §C.2, p. 425] (book p. 425; PDF p. 440)

Root `r` (with entry); edges `r→n₁`, `r→n₂`, `n₁→n₂`, `n₂→n₁`. It has no dominator-back edges, yet any spanning
forest `T` characterises one of the edges between `n₁` and `n₂` as a back edge, so there may be more back
edges than dominator-back edges [PPA §C.2, p. 424] (book p. 424; PDF p. 439). It is the simplest example of
an irreducible graph.

### Lemma C.12 (reducible graphs: back edges are dominator-back edges)
[PPA §C.2, p. 425] (book p. 425; PDF p. 440)

Let `G = (N, A)` be a **reducible** graph with handle `H`, `T` a depth-first spanning forest for `G` and `H`,
and rPostorder the associated ordering computed by Table C.1. Then an edge is a back edge **iff** it is a
dominator-back edge. Consequence stated by the book: for reducible graphs the loop connectedness parameter
is independent of the choice of depth-first spanning forest.

### Example C.13 (WHILE flow graphs are reducible)
[PPA §C.2, p. 425] (book p. 425; PDF p. 440); continued [PPA §C.2, p. 426] (book p. 426; PDF p. 441)

For a uniquely labelled WHILE statement `S`, `(labels(S), flow(S))` with root `init(S)` is reducible
(BKL-018, G-U0-42): each while loop is entered only at its test node, which dominates the loop body, so the
loop's back edges are dominator-back edges; tree, forward and cross edges form an acyclic graph. The loop
connectedness parameter equals the maximum number of nested while loops in the program. Scope: stated for
uniquely labelled WHILE, not for arbitrary flow graphs; sibling loops do not add up (Figure C.1 has two loops
and `d(G) = 1`).

### Corollary C.14 (monotone rPostorder on cycle-free paths)
[PPA §C.2, p. 426] (book p. 426; PDF p. 441)

Let `G = (N, A)` be a **reducible** graph with handle `H`. Any **cycle-free** path in `G` **beginning with a
node in the handle** is monotonically increasing by the ordering rPostorder computed by Table C.1 (G-U0-43).
(The book phrases this as "monotonically increasing"; along consecutive distinct steps of such a cycle-free
path every edge is non-back by Lemma C.12, so `rPostorder` increases strictly `<` by Corollary C.11 `[derived]`.)

### Reducible versus irreducible

| Aspect | Reducible (with handle `H`) | Irreducible |
| :--- | :--- | :--- |
| Definition | `(N, A \ A_db)` acyclic and `H` still a handle | that condition fails |
| Back edges vs dominator-back edges | identical sets, for every DFSF `T` (Lemma C.12) | every dominator-back edge is a back edge, but there may be more back edges (Figure C.3) |
| `d(G, T)` | independent of `T` (Lemma C.12) | defined relative to `T`; which edge of a multi-entry cycle becomes the back edge depends on `T` |
| Cycle-free paths from `H` | monotonically increasing in rPostorder (Corollary C.14) | not stated |
| Canonical instance | WHILE flow graphs (Example C.13) | Figure C.3 |

### [U0:C.2-e] Other node orders
[PPA §C.2, p. 426] (book p. 426; PDF p. 441)

| Order | Example for Figure C.2 | Topologically sorts DFSF? | Forward edges? | Cross edges? |
| :--- | :--- | :--- | :--- | :--- |
| reverse postorder | `b₁, b₃, S₃, b₂, S₁, S₂` | yes | yes | yes (Corollary C.11) |
| preorder | `b₁, b₂, S₂, S₁, b₃, S₃` | yes | yes | not necessarily (edge `b₃` to `S₁`) |
| breadth-first order | `b₁, b₂, b₃, S₂, S₁, S₃` | yes | yes | not necessarily (add a node between `b₁` and `b₃`) |

The book concludes that this makes reverse postorder the better choice for a number of iterative
algorithms.

### Complexity bounds and their parameters

Appendix C states **no asymptotic cost** for Table C.1 and no bound on `d(G, T)`. The loop connectedness
parameter enters a bound in Chapter 6:

- **Lemma 6.12** [PPA §6.2, p. 380] (book p. 380; PDF p. 396): under the assumptions stated before it, the
  Round Robin Algorithm of Table 6.4 halts after at most `d(G_S, T) + 3` iterations and therefore performs at
  most `O((d(G_S, T) + 1) · N)` assignments.
- Parameters: `G_S` with handle `H_S` is the graph of the constraint system; `T` is a DFSF and rPostorder a
  reverse postorder constructed for it; `d(G_S, T) ≥ 0` is the loop connectedness parameter above; `N` is the
  number of constraints `(xᵢ ⊒ tᵢ)ᴺᵢ₌₁`. Assumption: the constraint system is an instance of a Bit Vector
  Framework (`L = 𝒫(D)` for finite `D`, each right hand side of the form `(x_{jᵢ} ∩ Yᵢ¹) ∪ Yᵢ²`).
- Iteration count: "iterated `n ≥ 1` times" means step 1 executed once and the while-loop of step 2
  executed `n − 1` times. The `+3` counts the `d + 1` propagation passes, one final pass that detects no
  change, and the step-1 pass.
- For WHILE programs `d` is the maximal nesting depth of while loops (Example C.13), giving `O((d + 1) · b)`
  for `b` elementary blocks.

---

## 3. Regular expressions (C.3)

### [U0:C.3-a] Alphabet and regular expressions
[PPA §C.3, p. 426] (book p. 426; PDF p. 441)

An alphabet `Σ` is a **finite and non-empty** set of symbols, assumed disjoint from `{Λ, ∅, (, ), +, ·, *}`.
Regular expressions over `Σ` (inductive): (1) `Λ`, `∅` and each `a ∈ Σ` are atomic; (2) if `R₁`, `R₂` are
regular expressions then `(R₁ + R₂)`, `(R₁ · R₂)` and `(R₁)*` are compound. Precedence: `*` binds tighter
than `·`, which binds tighter than `+`. Notation clash (BKL-024, G-U0-44): `Σ` here is an alphabet, while
the Index of Notation lists `Σ` only at p. 17 [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443).

### [U0:C.3-b] Languages and equivalence
[PPA §C.3, p. 427] (book p. 427; PDF p. 442)

`ℒ⟦Λ⟧ = {Λ}`; `ℒ⟦∅⟧ = ∅`; `ℒ⟦a⟧ = {a}` for `a ∈ Σ`; `ℒ⟦R₁ + R₂⟧ = ℒ⟦R₁⟧ ∪ ℒ⟦R₂⟧`;
`ℒ⟦R₁ · R₂⟧ = ℒ⟦R₁⟧ · ℒ⟦R₂⟧`; `ℒ⟦R₁*⟧ = ⋃_{k=0}^{∞} (ℒ⟦R₁⟧)ᵏ`, where
`L₁ · L₂ = { w₁w₂ | w₁ ∈ L₁ ∧ w₂ ∈ L₂ }`, `L⁰ = {Λ}`, `L^{i+1} = Lⁱ · L`.
`R₁` and `R₂` are equivalent, written `R₁ = R₂`, iff `ℒ⟦R₁⟧ = ℒ⟦R₂⟧`.

### [U0:C.3-c] Homomorphisms
[PPA §C.3, p. 427] (book p. 427; PDF p. 442)

`h : Σ₁ → Σ₂*` extends to words `h(a₁⋯aₘ) = h(a₁)⋯h(aₘ)`, languages `h(L) = { h(w) | w ∈ L }`, and regular
expressions: `h(∅) = ∅`; `h(Λ) = Λ`; `h(a) = b₁ · … · bₘ` if `h(a) = b₁⋯bₘ` with `m > 0`, and `h(a) = Λ` if
`h(a) = Λ`; `h(R₁ + R₂) = h(R₁) + h(R₂)`; `h(R₁ · R₂) = h(R₁) · h(R₂)`; `h(R*) = h(R)*`.
Fact (parentheses `ℒ(...)` as printed rather than `ℒ⟦...⟧`, BKL-024, G-U0-45): for `R` over `Σ₁`, `h(R)` is a
regular expression over `Σ₂` and `ℒ(h(R)) = h(ℒ(R))`.

---

## 4. Side conditions that are easy to drop (SMOOTHING_TRAP checklist)

| Statement as often smoothed | Condition the book states | Citation |
| :--- | :--- | :--- |
| "graph = nodes and edges" | the node set is finite (minimal handles exist because of it; G-U0-26) | [PPA §C.1, p. 417] (book p. 417; PDF p. 432) |
| "cycle = path back to the start" | non-trivial (`m ≥ 1`); `[n]` is not a cycle, `[n, n]` is; reduced SCC graph drops self-loops (G-U0-28, G-U0-29) | [PPA §C.1, p. 418] (book p. 418; PDF p. 433) |
| "multiple entry = two entry edges" | two distinct nodes of the cycle, each with an edge from outside the cycle (G-U0-28) | [PPA §C.1, p. 418] (book p. 418; PDF p. 433) |
| "Dom solves the equation" | the **greatest** solution; a smaller solution loses dominators on cycles `[derived]` (G-U0-33, G-U0-34) | [PPA §C.1, p. 421] (book p. 421; PDF p. 436) |
| "dominance over all paths" | paths from the handle `H` (possibly trivial; G-U0-30, G-U0-33) | [PPA §C.1, p. 420] (book p. 420; PDF p. 435) |
| "the DFS tree", "the reverse postorder" | the DFSF and numbering are not unique (BKL-019, G-U0-35, G-U0-36) | [PPA §C.2, p. 422] (book p. 422; PDF p. 437) |
| "back edge iff rPostorder decreases" | `≥`, not `>`: self-loops are back edges with equal numbers; numbering must come from Table C.1 (G-U0-37, G-U0-38, G-U0-39) | [PPA §C.2, p. 423] (book p. 423; PDF p. 438) |
| "`d(G)` is a graph property" | `d(G, T)` depends on `T`; independence is proved for reducible graphs only (G-U0-40) | [PPA §C.2, p. 425] (book p. 425; PDF p. 440) |
| "back edges = dominator-back edges" | only for reducible graphs (Lemma C.12); Figure C.3 is a counterexample (G-U0-41) | [PPA §C.2, p. 425] (book p. 425; PDF p. 440) |
| "reducible iff removing back edges leaves a DAG" | remove **dominator-back** edges; the result must be acyclic **and** keep `H` as handle (G-U0-41) | [PPA §C.2, p. 425] (book p. 425; PDF p. 440) |
| "`d(G)` = loop nesting depth" | stated for uniquely labelled WHILE flow graphs (Example C.13; BKL-018, G-U0-42) | [PPA §C.2, p. 425] (book p. 425; PDF p. 440) |
| "paths are strictly increasing in rPostorder" | Corollary C.14 states "monotonically increasing" for reducible cycle-free paths from `H` (strict `<` on each step follows via Lemma C.12 + Corollary C.11 `[derived]`; G-U0-43) | [PPA §C.2, p. 426] (book p. 426; PDF p. 441) |
| "preorder works as well" | preorder and breadth-first order need not sort cross edges (G-U0-43) | [PPA §C.2, p. 426] (book p. 426; PDF p. 441) |
| "Round Robin needs `d + 2` passes" | Lemma 6.12 states `d(G_S, T) + 3` iterations, under its Bit Vector assumptions | [PPA §6.2, p. 380] (book p. 380; PDF p. 396) |

---

## 5. Item index (Appendix C)

| Id | Item | Citation |
| :--- | :--- | :--- |
| [U0:C.1-a], Example C.1 | directed graph; flow graphs as digraphs | [PPA §C.1, p. 417] (book p. 417; PDF p. 432) |
| [U0:C.1-b] | edge-sequence paths, reachability | [PPA §C.1, p. 417] (book p. 417; PDF p. 432) |
| Example C.2 | FUN constraint graph | [PPA §C.1, p. 417] (book p. 417; PDF p. 432) |
| [U0:C.1-c], [U0:C.1-d] | `paths•`, `cycles`, multiple entry, DAG, topological sort | [PPA §C.1, p. 418] (book p. 418; PDF p. 433) |
| [U0:C.1-e], Fact C.3 | strongly connected, `𝒮𝒞` an equivalence | [PPA §C.1, p. 418] (book p. 418; PDF p. 433) |
| [U0:C.1-f], Example C.4, Lemma C.5 | strong components, reduced graph is a DAG | [PPA §C.1, p. 419] (book p. 419; PDF p. 434) |
| [U0:C.1-g] | handle, root, dummy root | [PPA §C.1, p. 419] (book p. 419; PDF p. 434) |
| [U0:C.1-h], Example C.6, [U0:C.1-i] | minimal handle, rooted, `path•^H` | [PPA §C.1, p. 420] (book p. 420; PDF p. 435) |
| [U0:C.1-j] | degrees, forests, trees, ordered forests | [PPA §C.1, p. 420] (book p. 420; PDF p. 435) |
| [U0:C.1-k] | dominators, `Dom` (greatest solution) | [PPA §C.1, p. 421] (book p. 421; PDF p. 436) |
| Table C.1, [U0:C.2-a] | DFSF algorithm, DFSF, DFST, reverse postorder | [PPA Table C.1, p. 421] (book p. 421; PDF p. 436) |
| [U0:C.2-b], Figure C.1, Example C.7 | edge classification, example graph | [PPA §C.2, p. 422] (book p. 422; PDF p. 437) |
| Figure C.2 | DFSF for Figure C.1 | [PPA Figure C.2, p. 423] (book p. 423; PDF p. 438) |
| Example C.8 | WHILE edge kinds | [PPA §C.2, p. 423] (book p. 423; PDF p. 438) |
| Lemma C.9 | back edge iff `rPostorder[n] ≥ rPostorder[n′]` | [PPA §C.2, p. 423] (book p. 423; PDF p. 438) |
| Corollary C.10, Corollary C.11 | cycles have back edges; topological sort | [PPA §C.2, p. 424] (book p. 424; PDF p. 439) |
| [U0:C.2-c] | loop connectedness `d(G, T)` | [PPA §C.2, p. 424] (book p. 424; PDF p. 439) |
| [U0:C.2-d], Figure C.3 | dominator-back edge, reducible graph | [PPA §C.2, p. 425] (book p. 425; PDF p. 440) |
| Lemma C.12, Example C.13 | reducible: back = dominator-back; WHILE reducible | [PPA §C.2, p. 425] (book p. 425; PDF p. 440) |
| Corollary C.14, [U0:C.2-e] | monotone rPostorder; other orders | [PPA §C.2, p. 426] (book p. 426; PDF p. 441) |
| [U0:C.3-a] | alphabet, regular expressions | [PPA §C.3, p. 426] (book p. 426; PDF p. 441) |
| [U0:C.3-b], [U0:C.3-c] | `ℒ⟦R⟧`, equivalence, homomorphisms | [PPA §C.3, p. 427] (book p. 427; PDF p. 442) |
| Concluding Remarks | sources [48], [4], [69], [5], [110]; regular languages [76] | [PPA Appendix C Concluding Remarks, p. 427] (book p. 427; PDF p. 442) |
