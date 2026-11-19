<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Chapter 2 L1 reference for heap pointer semantics, Shape Graphs, Invariants 1–5, and Shape transfer functions (§2.6). -->

# Shape Analysis: Pointer Semantics, Shape Graphs, and Strong Updates

Scope: Chapter 2, §2.6 (`§§2.6.1–2.6.3`), Concluding Remarks (`[U2b:CR-c]`), and Exercises `2.21*–2.25*` —
[PPA §2.6, p. 104] (book p. 104; PDF p. 123) through [PPA §2.6.3, p. 128] (book p. 128; PDF p. 147), plus
[PPA Chapter 2 Concluding Remarks, p. 129] (book p. 129; PDF p. 148),
[PPA Chapter 2 Concluding Remarks, p. 130] (book p. 130; PDF p. 149), and
[PPA Exercise 2.21, p. 139] (book p. 139; PDF p. 158) through [PPA Exercise 2.25, p. 139] (book p. 139; PDF p. 158).
Ground truth: `corpus/shards/RAW_SHARD_02b_interproc_shape.md`. Intraprocedural/interprocedural data flow
live in [intraprocedural-analyses-and-frameworks.md](./intraprocedural-analyses-and-frameworks.md) and
[interprocedural-and-correctness.md](./interprocedural-and-correctness.md); finite-height powerset/ACC lattice foundations live in
[appendix-a-posets-lattices-fixed-points.md](../../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md);
and two-tier `§4.5.2` Galois shape soundness (`Mini Project 4.2`, `SH → 𝒫(SG)`) lives in
[combinators-and-induced-operations.md](../../ppa-abstract-interpretation/references/combinators-and-induced-operations.md);
the functional stack-of-regions alternative (`§5.4.3`, `letregion` + `Observe`, canonical `X1`) is contrasted in
[effects-exceptions-regions-and-behaviours.md](../../ppa-types-effects-and-regions/references/effects-exceptions-regions-and-behaviours.md).

## 1. Pointer Language & Concrete Heap SOS (`§§2.6–2.6.1`)

Section 2.6 constructs an **intraprocedural** shape analysis verifying heap invariants (such as in-situ list
reversal preserving non-cyclicity, `Example 2.43`, `Figure 2.12`) and detecting guaranteed `nil` dereferences
[PPA §2.6, p. 104] (book p. 104; PDF p. 123) [PPA Example 2.43, p. 105] (book p. 105; PDF p. 124).

- **Restricted Syntax (`G-U2b-16`, `BKL-005`)**: Over finite non-empty selector names `sel ∈ Sel`, pointer
  expressions `p ::= x | x.sel` allow only **one** selector level; `op_a` forbids pointer arithmetic; `op_r`
  adds pointer equality; unary `op_p` includes `is-nil` and `has-sel`; expressions only read heap cells (`[p := a]^ℓ`,
  `[malloc p]^ℓ` mutate/allocate). No interior struct pointers, unions, or concurrency (`BKL-005`)
  [PPA §2.6, p. 105] (book p. 105; PDF p. 124).
- **Concrete Domains & Valuations (`G-U2b-16`, `Example 2.44`, `Figure 2.12`)**:
  - `σ ∈ State = Var⋆ → (Z + Loc + {◇})` (`◇` = `nil`);
  - `ℋ ∈ Heap = (Loc × Sel) →_fin (Z + Loc + {◇})` (newly allocated cells leave all selectors undefined);
  - `℘⟦x.sel⟧(σ, ℋ) = ℋ(σ(x), sel)` if `σ(x) ∈ Loc ∧ (σ(x), sel) ∈ dom(ℋ)` else `undef` (printed signatures of `℘, 𝒜, ℬ`
    on pp. 107–108 errantly write `→_fin` over infinite `State × Heap` instead of partial `⇀`, `F-U2b-08`);
  - `op_a` requires integers; `op_r` requires two integers or two pointers; `is-nil(◇) = tt`, `ff` otherwise
    [PPA §2.6.1, p. 106] (book p. 106; PDF p. 125) [PPA §2.6.1, p. 107] (book p. 107; PDF p. 126)
    [PPA §2.6.1, p. 108] (book p. 108; PDF p. 127).
- **Stuck Faults & Limited Garbage Reuse (`G-U2b-17`)**: Selector assignment `[x.sel := a]^ℓ` and `[malloc (x.sel)]^ℓ`
  require `σ(x) ∈ Loc` (and `𝒜⟦a⟧` defined), otherwise configurations get stuck (`undef`). `[malloc p]^ℓ` picks
  `ξ` occurring in *neither* `σ` nor `ℋ`: after `[malloc x]¹; [x.cdr:=nil]²; [x:=nil]³`, `ξ` remains in
  `dom(ℋ)` and cannot be reused by `[malloc y]⁴` despite being unreachable garbage (`Remark.`, p. 109)
  [PPA §2.6.1, p. 109] (book p. 109; PDF p. 128).

## 2. Shape Graphs `(S, H, is)` and the Five Compatibility Invariants (`§2.6.2`)

To abstract unbounded concrete heaps into a finite lattice, concrete cells pointed to by the exact variable set
`X = {x ∈ Var⋆ | σ(x) = ξ}` map to `n_X ∈ ALoc = {n_Z | Z ⊆ Var⋆}`; all cells unreachable directly from
variables collapse into **abstract summary location `n_∅`** (`Examples 2.45–2.46`, `Figure 2.13`)
[PPA §2.6.2, p. 110] (book p. 110; PDF p. 129) [PPA Figure 2.13, p. 112] (book p. 112; PDF p. 131).

- **Dynamic Membership & Absent Values (`G-U2b-18`)**: Concrete cells are *not* pinned to fixed `ALoc`s across
  execution (cells enter/leave `n_∅` as stack pointers move, `Example 2.46`), and `S ∈ 𝒫(Var⋆ × ALoc)`,
  `H ∈ 𝒫(ALoc × Sel × ALoc)` **omit integers, `◇`, and uninitialised fields** — absent bindings represent
  any non-pointer value or `nil`/`undef` [PPA Example 2.46, p. 111] (book p. 111; PDF p. 130).
- **Heap Sharing `is` (`G-U2b-19`, `Figure 2.14`)**: `n_X ∈ is` (double box) means `n_X` *may* represent a
  cell targeted by `≥ 2` pointers **from within the heap** — *never* stack-variable aliasing (`x, y → ξ` gives
  `n_{x,y} ∉ is` unless `≥ 2` heap pointers also target `ξ`, `Figure 2.14`)
  [PPA Figure 2.14, p. 113] (book p. 113; PDF p. 132).

Every `(S, H, is) ∈ SG` satisfies all **five compatibility invariants** (`p. 114`) [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133):

1. **Invariant 1 (Disjoint naming)**: `∀n_V, n_W ∈ ALoc(S) ∪ ALoc(H) ∪ is : (V = W) ∨ (V ∩ W = ∅)`.
2. **Invariant 2 (State naming)**: `∀(x, n_X) ∈ S : x ∈ X` (combined with 1, unique target per variable;
   transfer functions also preserve the converse `x ∈ X ⇒ (x, n_X) ∈ S` `[derived]`).
3. **Invariant 3 (Deterministic selectors off named nodes, `G-U2b-20`)**:
   `∀(n_V, sel, n_W), (n_V, sel, n_{W'}) ∈ H : (V = ∅) ∨ (W = W')`. Only summary node `n_∅` may carry
   multiple outgoing edges with the same selector (including self-loops).
4. **Invariant 4 (`is` must be witnessed)**:
   `∀n_X ∈ is : (∃sel : (n_∅, sel, n_X) ∈ H) ∨ (∃(n_V, sel₁, n_X), (n_W, sel₂, n_X) ∈ H : sel₁ ≠ sel₂ ∨ V ≠ W)`.
5. **Invariant 5 (Forced `is` on distinct edges, `G-U2b-21`)**:
   `∀(n_V, sel₁, n_X), (n_W, sel₂, n_X) ∈ H : ((sel₁ ≠ sel₂ ∨ V ≠ W) ∧ X ≠ ∅) ⇒ n_X ∈ is`.
   Invariant 5 inverts 4(b) for `X ≠ ∅`, whereas **4(a) has no inverse**: an edge `(n_∅, sel, n_X)` is
   compatible with both `n_X ∉ is` (`Figure 2.14` top row) and `n_X ∈ is` (middle row), while `n_∅ ∉ is`
   certifies every cell in `n_∅` has `≤ 1` incoming heap pointer (`p. 114`).

Lattice `L = (𝒫(SG), ⊆, ∪)` is finite because `|ALoc| = 2^{|Var⋆|}` (`Figure 2.15` gives singleton `ι` for
unshared `≥ 2`-node list in `x`) [PPA Figure 2.15, p. 115] (book p. 115; PDF p. 134).

## 3. `Shape` Transfer Functions & Materialisation Mechanics (`§2.6.3`)

For each label-consistent program `S⋆` with isolated entries (or using `§2.3`'s unconditional
`⋃{Shape•(ℓ') | (ℓ', ℓ) ∈ flow(S⋆)} ∪ ι^ℓ_E` join when `init(S⋆)` has incoming back-edges)
[PPA §2.6.3, p. 115] (book p. 115; PDF p. 134):

```
Shape∘(ℓ) = ι if ℓ=init(S⋆);  ⋃{Shape•(ℓ') | (ℓ',ℓ)∈flow(S⋆)} else       f_ℓ^SA(SG) = ⋃{φ_ℓ^SA((S,H,is)) | (S,H,is) ∈ SG}
```

- **Outer-May / Inner-Must Soundness (`G-U2b-22`, `F-U2b-10`)**: Here `f_ℓ^SA(SG)` uses `SG` (`p. 116`) as a
  meta-variable ranging over subsets `X ∈ 𝒫(SG)`. The book only calls `Shape` "an instance of a Monotone
  Framework" (`p. 115`). `[derived]`: `f_ℓ^SA` is a pointwise union lift, so it distributes over binary `⋃` on a
  finite lattice (and is strict, `f_ℓ^SA(∅) = ∅`), making `Shape` a finite **Distributive Framework**; then
  `Lemma 2.32` yields `MFP = MOP` provided `path∘(ℓ) ≠ ∅` for all `ℓ` in `E` and `F`
  (`[PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99)`; strictness handles empty paths per `Exercise 2.13` `[derived]`). Externally it is a *may* union,
  while internally each `(S, H, is)` carries *must* absence of extra aliases/edges (Invariants 1–3 ensure every
  non-empty `n_X` represents at most one concrete cell), enabling **strong update** and **strong nullification**
  [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134) [PPA §2.6.3, p. 116] (book p. 116; PDF p. 135).
- **Boolean Tests & `skip` (`G-U2b-23`, `Example 2.48`)**: `φ_ℓ^SA((S, H, is)) = {(S, H, is)}`. Even
  `[not is-nil(x)]^2` is the identity — boolean guards do not prune `Shape` branches unless combined with
  two-label `[b]^{ℓ₁,ℓ₂}` splitting (`Exercise 2.11`) [PPA §2.6.3, p. 116] (book p. 116; PDF p. 135).
- **Primitive Nullification `kill_x` (`[x:=a]^ℓ` with `a ∈ {n, a₁ op_a a₂, nil}`, `Figure 2.16`, `G-U2b-24`)**:
  With `k_x(n_Z) = n_{Z \ {x}}`, strip `x` from `S`, rename all `ALoc`s in `S, H, is` via `k_x`, merging `n_{x}`
  into `n_∅` (`n_∅ ∉ is'` iff both `n_∅ ∉ is` and `n_{x} ∉ is`, `Examples 2.49–2.50`). Because **no GC**
  runs (`Remark.`, `p. 117`), unreachable `n_{x}` edges pollute `n_∅`
  [PPA Figure 2.16, p. 116] (book p. 116; PDF p. 135) [PPA §2.6.3, p. 117] (book p. 117; PDF p. 136).
- **Variable Copy `[x:=y]^ℓ` (`Figure 2.17`, `Example 2.51`, `G-U2b-19`)**: Identity if `x = y`; otherwise run
  `kill_x` then apply `g_x^y(n_Z) = n_{Z∪{x}}` (`y ∈ Z`) else `n_Z` and add `(x, n_{Y∪{x}})` — inheriting
  `n_Y`'s `is'` bit directly (`is` ignores stack aliases) [PPA §2.6.3, p. 118] (book p. 118; PDF p. 137).
- **Desugaring Self/Compound Heap Ops (`G-U2b-25`)**: Self-referential and double-deref statements have no
  direct `x = y` rule (`§2.6.3`; direct versions are `Exercise 2.22`); rewrite with fresh `t ∉ Var⋆` and
  trailing `[t := nil]^{ℓ₃}`:
  - `[x := x.sel]^ℓ` (`Example 2.52`) `⇝ [t := x.sel]^{ℓ₁}; [x := t]^{ℓ₂}; [t := nil]^{ℓ₃}` (`p. 119`);
  - `[x.sel := x]^ℓ ⇝ [t := x]^{ℓ₁}; [x.sel := t]^{ℓ₂}; [t := nil]^{ℓ₃}` (`p. 126`);
  - `[x.sel := y.sel']^ℓ ⇝ [t := y.sel']^{ℓ₁}; [x.sel := t]^{ℓ₂}; [t := nil]^{ℓ₃}` (`p. 127`);
  - `[malloc (x.sel)]^ℓ ⇝ [malloc t]^{ℓ₁}; [x.sel := t]^{ℓ₂}; [t := nil]^{ℓ₃}` (`p. 128`).
- **Selector Dereference `[x := y.sel]^ℓ` (`x ≠ y`, `pp. 119–125`)**: First set `(S', H', is') = kill_x((S, H, is))`:
  1. **Case 1 (`p. 120`, `G-U2b-23`)**: `¬∃n_Y : (y, n_Y) ∈ S'` OR `(y, n_Y) ∈ S' ∧ ¬∃n_Z : (n_Y, sel, n_Z) ∈ H'`.
     Returns `{kill_x((S, H, is))}` — silently over-approximates a `nil`/`undef` dereference fault (since SOS
     gets stuck) rather than flagging an error unless a client checks `Shape∘(ℓ)` before transfer!
  2. **Case 2 (`pp. 120–121`, `Figure 2.18`)**: `(n_Y, sel, n_U) ∈ H'` with `n_U ≠ n_∅` (unique `n_Y, n_U` by
     Invariants 1–3, possibly `n_Y = n_U`). Rename `n_U ↦ n_{U∪{x}}` (`h_x^U`), preserving `n_U ∈ is'`
     [PPA Figure 2.18, p. 120] (book p. 120; PDF p. 139).
  3. **Case 3 — Materialisation (`pp. 121–125`, `Figures 2.19–2.20`, `Example 2.53`, `G-U2b-26`)**:
     `(y, n_Y) ∈ S'` and `(n_Y, sel, n_∅) ∈ H'`. Defined declarative-inverse via `[x:=nil]; [x:=y.sel]; [x:=nil]`:
     `φ_ℓ^SA = {(S'', H'', is'') compatible | kill_x((S'', H'', is'')) = (S', H', is') ∧ (x, n_{x}) ∈ S'' ∧ (n_Y, sel, n_{x}) ∈ H''}`.
     Properties proven (`pp. 122–124`):
     - `S'' = S' ∪ {(x, n_{x})}` uniquely;
     - `is'' \ {n_∅, n_{x}} = is' \ {n_∅}` and **`n_∅ ∈ is' ⇔ (n_∅ ∈ is'' ∨ n_{x} ∈ is'')`**;
     - Partition edges under `k_x`-relatedness (`external`, `internal`, `going-out`, `going-in`):
       `(n_Y, sel, n_∅)` becomes `(n_Y, sel, n_{x})` (Invariant 3 forbids retaining `(n_Y, sel, n_∅)`).
     - `Figures 2.19–2.20` (`n_∅, n_W ∉ is`): `(n_V, sel₁, n_∅)` cannot redirect to `n_{x}` (else Invariant 5
       would force `n_{x} ∈ is''`, contradicting `n_∅ ∉ is'`); `sel₂ → n_W` splits 2 ways (`n_∅` xor `n_{x}`
       since `n_W ∉ is`); `sel₃ → n_∅` splits 3 ways (`n_{x}`, `n_∅`, or both), yielding **6** graphs
       `(S''_{1..6}, H''_{1..6}, is''_{1..6})` [PPA Figure 2.20, p. 124] (book p. 124; PDF p. 143).
- **Strong Edge Kill `kill_{x.sel}` (`[x.sel := a]^ℓ`, `p. 125`, `Figure 2.21`, `G-U2b-27`)**:
  Identity unless `(x, n_X) ∈ S` and `(n_X, sel, n_U) ∈ H`. Otherwise drop `(n_X, sel, n_U)` from `H` and
  clear `n_U` from `is` **iff all three hold**:
  `n_U ∈ is  ∧  #into(n_U, H') ≤ 1  ∧  ¬∃sel' : (n_∅, sel', n_U) ∈ H'`.
  Omitting the third conjunct unsoundly unshares `n_U` when multiple summary cells in `n_∅` target it
  (`Figure 2.14` middle row, `Figure 2.21` slashed arrow) (`Remark.`, p. 126: no GC on detached `n_U`)
  [PPA §2.6.3, p. 125] (book p. 125; PDF p. 144) [PPA Figure 2.21, p. 126] (book p. 126; PDF p. 145).
- **Destructive Heap Update `[x.sel := y]^ℓ` (`x ≠ y`, `pp. 126–127`, `Figure 2.22`, `Example 2.54`)**:
  Identity if `x ∉ dom(S)`; `{kill_{x.sel}(...)}` if `x ∈ dom(S) ∧ y ∉ dom(S)`; when `x, y ∈ dom(S)`, run `(S', H', is') = kill_{x.sel}(...)`,
  set `H'' = H' ∪ {(n_X, sel, n_Y)}`, and set `is'' = is' ∪ {n_Y}` if `#into(n_Y, H') ≥ 1` else `is'` (`Figure 2.22` illustrates
  `< 1` while captioning `(S', H'', is'')`, `F-U2b-10`) [PPA §2.6.3, p. 127] (book p. 127; PDF p. 146) [PPA Figure 2.22, p. 127] (book p. 127; PDF p. 146).
- **`[malloc x]^ℓ` (`p. 127`)**: `{(S' ∪ {(x, n_{x})}, H', is')}` from `kill_x((S, H, is))` (fresh `n_{x}` unshared).

## 4. Cost Controls & Pointer Analysis Taxonomy (`[U2b:CR-c]`, `Exercises 2.21*–2.25*`)

| Refinement / Alternative | Mechanism & Cost Impact | Source Anchor |
| :--- | :--- | :--- |
| **`𝒫(SG)` blowup (`G-U2b-28`)** | 7-block list reversal (`Example 2.47`) generates `> 50` graphs across points | [PPA Exercise 2.21, p. 139] (book p. 139; PDF p. 158) |
| **Single summary graph (`[148, 149]`, `G-U2b-28`)** | Merge compatible `𝒫(SG)` elements into one summary graph per label to avoid exponential factor | [PPA Chapter 2 Concluding Remarks, p. 130] (book p. 130; PDF p. 149) |
| **Tightening Case 3 & GC (`Exercises 2.23*, 2.24*`)** | Prune unreachable graphs in `H''` (`2.23*`); add reachability-based GC to SOS & `Shape` (`2.24*`) | [PPA Exercise 2.23, p. 139] (book p. 139; PDF p. 158) |
| **Allocation-site naming (`Exercise 2.25*`)** | Partition `n_∅` into per-`malloc` summaries `n_{ℓ,X}` (isolates disjoint containers) | [PPA Exercise 2.25, p. 139] (book p. 139; PDF p. 158) |
| **Stack points-to vs heap shape (`[U2b:CR-c]`)** | Stack-only `(p, x)` (`[162, 153]`, Steensgaard) vs bounded paths (`[84]`), access paths (`[101]`), general instrumentation (`[150]`) | [PPA Chapter 2 Concluding Remarks, p. 129] (book p. 129; PDF p. 148) |

## 5. Non-blocking Shape Analysis Backlog (`ARCHITECTURE.md` §6.4)

- `BKL-005` (`§2.6` no pointer arithmetic, interior pointers, or type punning);
- `BKL-046` (`§2.6.1 pp. 107–108` prints `→_fin` for partial functions `℘, 𝒜, ℬ` over infinite `State × Heap`);
- `BKL-047` (`Figures 2.21–2.22` slashed-arrow/label typos, Invariant 4 row citation, and fresh temporary `t ∉ Var⋆` expansion);
- `BKL-048` (`§2.6.3` nil-deref absorption in Case 1, branch insensitivity, and ungarbage-collected `𝒫(SG)` explosion).
