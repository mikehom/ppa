<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 lossless corpus shard for Unit 6 (Chapter 6 §§6.1-6.3, Concluding Remarks, Mini Projects, Exercises, Subject Index, and Bibliography [1]-[185]). -->

# RAW_SHARD_06 — Chapter 6 Algorithms, Subject Index, and Bibliography (Unit 6)

Source: *Principles of Program Analysis* (Nielson, Nielson, Hankin), corrected 2nd printing, 2005.
Scope: Unit 6 spans three non-contiguous regions with piecewise-constant PDF-to-book page offsets verified against `corpus/pdf_page_map.json` and 47 rendered page images:
1. **Chapter 6 — Algorithms** (`§§6.1–6.3`, `Concluding Remarks`, `Mini Projects 6.1–6.2`, `Exercises 6.1–6.14`), spanning book pages 365–392 / PDF pages 381–408 (`PDF page = book page + 16`; book p. 364 is an unnumbered blank verso absent from the PDF) [PPA Chapter 6, p. 365] (book p. 365; PDF p. 381).
2. **Subject Index (`Index`)**, spanning book pages 433–437 / PDF pages 447–451 (`PDF page = book page + 14`; book pp. 416 and 428 are absent blank versos in Appendices A–C, and book p. 438 is an absent blank verso after the Index) [PPA Index, p. 433] (book p. 433; PDF p. 447).
3. **Bibliography (`[1]`–`[185]`)**, spanning book pages 439–452 / PDF pages 452–465 (`PDF page = book page + 13`; 185 contiguous entries `[1]`–`[185]` with zero gaps) [PPA Bibliography, p. 439] (book p. 439; PDF p. 452).

Structural note on Chapter 6 divisions: `§6.1` covers Worklist Algorithms (`§6.1.1` *The Structure of Worklist Algorithms*, `Table 6.1`; `§6.1.2` *Iterating in LIFO and FIFO*, `Table 6.2`, `Figure 6.1`), `§6.2` covers Iterating in Reverse Postorder (`Table 6.3`, `Figures 6.2–6.3`) and `§6.2.1` *The Round Robin Algorithm* (`Table 6.4`, `Figure 6.4`), and `§6.3` covers Iterating Through Strong Components (`Tables 6.5–6.6`, `Figures 6.5–6.6`, with zero numbered subsections). Demand-driven *Local solvers* (`[29, 51–54]`), *Elimination methods* (`[146, 154, 144, 11, 170, 171]`), and *Practical systems* (`Spare`, `System Z`, `PAG`, `Sharlit`, `BANE`) reside in Chapter 6 *Concluding Remarks* (`pp. 384–387`) [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401).

Conventions:
- Every source reference pairs a strict single-page inline locator token with its book/PDF coordinate companion, respecting Unit 6's piecewise `+16` / `+14` / `+13` offsets.
- Book-numbered items preserve their exact printed kind word and number: shared per-chapter sequence `6.1`–`6.15` (`12` Examples + `3` Lemmas: `Lemma 6.4`, `Lemma 6.11`, `Lemma 6.12`; `0` Theorems/Propositions/Corollaries/Facts), `Tables 6.1–6.6`, `Figures 6.1–6.6`, `Mini Projects 6.1–6.2`, `Exercises 6.1–6.14` (`0` starred), `0` numbered equation displays, and Bibliography entries `[1]`–`[185]`. Unnumbered formal blocks carry `[U6:<sec>-<letter>]`.
- Terms absent from the book carry `[external]`. Consequences, concrete counterexamples, and complexity refinements worked out from the book's definitions carry `[derived]`. Source misprints and internal tensions are transcribed verbatim at `L3` and catalogued under `## Source Errata and Findings` (`F-U6-01`..`F-U6-12`).
- Notation: `𝒮 = (x_i ⊒ t_i)_{i=1}^N` finite inequation system (`N ≥ 1`); `X = {x_i | 1 ≤ i ≤ N}` finite flow-variable set; `FV(t)` flow variables occurring in RHS term `t`; `(L, ⊑)` complete lattice satisfying ACC with least element `⊥`, join `⊔`, meet `⊓`, reversed order `⊒` (`x ⊒ y ⇔ y ⊑ x`), negated order `⋣` (`x ⋣ y ⇔ ¬(x ⊒ y) ⇔ ¬(y ⊑ x)`), and finite height `h ≥ 1`; `ψ : X → L` valuation; `⟦t⟧ψ ∈ L` monotone term semantics; `F_𝒮 : (X → L) → (X → L)` induced monotone functional with least fixed point `μ_𝒮 = lfp(F_𝒮)`; `W` abstract worklist with `empty`, `insert((x ⊒ t), W)`, `extract(W)`; `Analysis[x]` solution array, `infl[x]` influence set, `eval(t, Analysis)` helper (Table 6.1); `nil`, `cons`, `head`, `tail` list primitives (Table 6.2); `G_𝒮` constraint dependency digraph, minimal handle `H_𝒮`, depth-first spanning forest `T`, reverse postorder `rPostorder`, loop connectedness `d(G_𝒮, T) ≥ 0`; `(W.c, W.p)` current-list / pending-set pair and `sort_rPostorder` (Table 6.3); `change` boolean flag (Table 6.4); `(scc, rp)`, `fst`, `snd`, `srPostorder` strong-component + local-RPO numbering (Table 6.5); `W_scc`, `sort_srPostorder` (Table 6.6), and three-way split `(W.c, W.pc, W.pf)` (`currentQ, pendingQ, futureQ`); `Dom(n)` dominators (Exercise 6.4); `f^⟨n⟩ = (f ⊔ id)^n` and fastness closure `f̄ = f^⟨i_f⟩` (Exercise 6.14); `■` end-of-item marker.

---

## Chapter 6 Opening and 6.1 Worklist Algorithms

**[U6:6-a] Chapter 6 roadmap and flow-variable abstraction** [PPA Chapter 6, p. 365] (book p. 365; PDF p. 381), [PPA §6.1, p. 365] (book p. 365; PDF p. 381)
Chapter 6 unifies the algorithmic solver techniques of earlier chapters by studying general algorithms for equation and inequation systems over *flow variables*:
- **Data Flow Analysis (Chapter 2)**: separate flow variables represent entry and exit values at each program point.
- **Constraint Based Analysis (Chapter 3)**: separate flow variables represent the abstract cache `C(ℓ)` at each label and the abstract environment `r(x)` at each program variable.

### Example 6.1 — Reaching Definitions as a 12-Variable and 6-Variable Equation System

**[PPA Example 6.1, p. 365] (book p. 365; PDF p. 381), [PPA Example 6.1, p. 366] (book p. 366; PDF p. 382)**
Consider the `WHILE` program (leaving arithmetic/boolean expressions `a_i, b_i` unspecified):
```text
if [b₁]^1 then (while [b₂]^2 do [x := a₁]^3)
          else (while [b₃]^4 do [x := a₂]^5);
[x := a₃]^6
```
Writing `X_ℓ = {(x, ℓ)}` and string-subscript shorthand `X_{356?} = {(x, 3), (x, 5), (x, 6), (x, ?)}`, the Reaching Definitions equations of `§2.1.2` [PPA §2.1.2, p. 43] (book p. 43; PDF p. 62) map `RD_{entry}(1..6)` and `RD_{exit}(1..6)` to flow variables `{x₁, ···, x_{12}}`:
```text
x₁ = X_?          x₇  = x₁
x₂ = x₇ ∪ x₉      x₈  = x₂
x₃ = x₈           x₉  = (x₃ \ X_{356?}) ∪ X₃
x₄ = x₇ ∪ x_{11}  x_{10} = x₄
x₅ = x_{10}       x_{11} = (x₅ \ X_{356?}) ∪ X₅
x₆ = x₈ ∪ x_{10}  x_{12} = (x₆ \ X_{356?}) ∪ X₆
```
Eliminating `x₇..x_{12}` (`RD_{exit}`) produces the simplified 6-variable `RD_{entry}` equation system used as Chapter 6's running benchmark across `Figures 6.1–6.6`:
```text
x₁ = X_?
x₂ = x₁ ∪ (x₃ \ X_{356?}) ∪ X₃
x₃ = x₂
x₄ = x₁ ∪ (x₅ \ X_{356?}) ∪ X₅
x₅ = x₄
x₆ = x₂ ∪ x₄
```
■

**[U6:6.1-a] Equations `(x_i = t_i)` versus inequations `(x_i ⊒ t_i)`** [PPA §6.1, p. 366] (book p. 366; PDF p. 382)
Chapter 2 solved equation systems `(x_i = t_i)_{i=1}^N`, whereas Chapter 3 solved inequation systems `(x_i ⊒ t_i)_{i=1}^N`. Recalling `§2.2` [PPA §2.2, p. 55] (book p. 55; PDF p. 74):
- Every solution of `x_i = t_i` is a solution of `x_i ⊒ t_i`.
- Multiple inequations sharing a left-hand side (`x ⊒ t₁  ···  x ⊒ t_n`, omitted by the PDF OCR layer on p. 366) have the **exact same set of solutions** as the single inflationary equation `x = x ⊔ t₁ ⊔ ··· ⊔ t_n`.
- Their **least solution** coincides with the least solution of `x = t₁ ⊔ ··· ⊔ t_n` (`x` omitted on the RHS; general solutions differ whenever `x ⊐ t₁ ⊔ ··· ⊔ t_n`).
Chapter 6 concentrates on constraint systems allowing **multiple inequations for the same LHS**, which `Exercise 6.5` shows improves worst-case solver efficiency from `O(h · M² · N)` to `O(h · M · N)` [PPA Exercise 6.5, p. 389] (book p. 389; PDF p. 405).

**[U6:6.1-b] Five standing assumptions on constraint systems `𝒮`** [PPA §6.1, p. 367] (book p. 367; PDF p. 383)
1. **Finite inequation system**: `𝒮 = (x_i ⊒ t_i)_{i=1}^N` for `N ≥ 1`, where LHS variables `x_i` need not be distinct.
2. **Closed flow-variable universe**: for every `t_i`, `FV(t_i) ⊆ X = {x_i | 1 ≤ i ≤ N}` (every variable referenced on any RHS must appear on at least one LHS; see `F-U6-01`).
3. **ACC complete-lattice codomain**: a solution is a total function `ψ : X → L` into a complete lattice `(L, ⊑)` satisfying the Ascending Chain Condition (`ACC`).
4. **Term valuation**: each RHS `t` is interpreted with respect to `ψ : X → L` as an element `⟦t⟧ψ ∈ L` (the syntactic nature of `t_i` is otherwise left unspecified).
5. **Monotonicity and locality**: `⟦t⟧ψ` is monotone in `ψ` and depends solely on `{ψ(x) | x ∈ FV(t)}`.

### Example 6.2 — Encoding Chapter 3 Conditional Constraints as RHS Terms

**[PPA Example 6.2, p. 367] (book p. 367; PDF p. 383)**
For `((fn x => x^1)^2 (fn y => y^3)^4)^5` (from `Example 3.20` [PPA Example 3.20, p. 175] (book p. 175; PDF p. 193), dropped by the OCR layer on p. 367), mapping `x₁..x₅` to `C(1)..C(5)`, `x₆` to `r(x)`, and `x₇` to `r(y)` encodes the `0-CFA` conditional constraints as 8 unconditional inequations with monotone conditional RHS terms (evaluating implicitly to `⊥ = ∅` when the guard fails; see `F-U6-02`):
```text
x₁ ⊇ x₆                                  x₂ ⊇ {fn x => x^1}
x₃ ⊇ x₇                                  x₄ ⊇ {fn y => y^3}
x₅ ⊇ if {fn x => x^1} ⊆ x₂ then x₁      x₅ ⊇ if {fn y => y^3} ⊆ x₂ then x₃
x₆ ⊇ if {fn x => x^1} ⊆ x₂ then x₄      x₇ ⊇ if {fn y => y^3} ⊆ x₂ then x₄
```
■

---

## 6.1.1 The Structure of Worklist Algorithms

**[U6:6.1.1-a] Abstract worklist ADT (`empty`, `insert`, `extract`) and set-based specification** [PPA §6.1.1, p. 368] (book p. 368; PDF p. 384)
The solver is parameterised over an abstract datatype `W` of worklists of constraints with three operations:
- `empty`: the empty worklist;
- `insert((x ⊒ t), W)`: returns `W` extended with `x ⊒ t` (idiom: `W := insert((x ⊒ t), W)`);
- `extract(W)`: selects and removes one occurrence of a constraint `x ⊒ t` from non-empty `W`, returning `((x ⊒ t), W')` (idiom: `((x ⊒ t), W) := extract(W)`).

Most abstract set-of-constraints specification (`p. 368`; concrete realisations may use lists, multisets, or paired structures):
```text
empty = ∅
function insert((x ⊒ t), W)
  return W ∪ {x ⊒ t}
function extract(W)
  return ((x ⊒ t), W \ {x ⊒ t}) for some x ⊒ t in W
```

### Table 6.1 — The Abstract Worklist Algorithm

**[PPA Table 6.1, p. 369] (book p. 369; PDF p. 385)**
```text
INPUT:   A system 𝒮 of constraints: x₁ ⊒ t₁, ···, x_N ⊒ t_N
OUTPUT:  The least solution: Analysis
METHOD:  Step 1: Initialisation (of W, Analysis and infl)
                 W := empty;
                 for all x ⊒ t in 𝒮 do
                     W := insert((x ⊒ t),W)
                     Analysis[x] := ⊥;
                     infl[x] := ∅;
                 for all x ⊒ t in 𝒮 do
                     for all x' in FV(t) do
                         infl[x'] := infl[x'] ∪ {x ⊒ t};

         Step 2: Iteration (updating W and Analysis)
                 while W ≠ empty do
                     ((x ⊒ t),W) := extract(W);
                     new := eval(t,Analysis);
                     if Analysis[x] ⋣ new then
                         Analysis[x] := Analysis[x] ⊔ new;
                         for all x' ⊒ t' in infl[x] do
                             W := insert((x' ⊒ t'),W);

USING:   function eval(t,Analysis)
         return ⟦t⟧(Analysis)
         value empty
         function insert((x ⊒ t),W)
         return ···
         function extract(W)
         return ···
```
After Step 1, for every `x ∈ X` [PPA §6.1.1, p. 369] (book p. 369; PDF p. 385):
```text
infl[x] = {(x' ⊒ t') in 𝒮 | x ∈ FV(t')}
```
*(Printed quirk: missing semicolon after `W := insert((x ⊒ t),W)`, and `Analysis[x] := ⊥; infl[x] := ∅;` sits inside `for all x ⊒ t in 𝒮` rather than `for all x ∈ X`; see `F-U6-01`.)*

### Example 6.3 — Influence Sets `infl` for Example 6.1

**[PPA Example 6.3, p. 370] (book p. 370; PDF p. 386)**
Identifying each equation of `Example 6.1`'s 6-variable system by its unique LHS variable `x_i`, Step 1 sets `Analysis[x_i] = ∅` for `i = 1..6` and constructs:

| Variable | `x₁` | `x₂` | `x₃` | `x₄` | `x₅` | `x₆` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `infl` | `{x₂, x₄}` | `{x₃, x₆}` | `{x₂}` | `{x₅, x₆}` | `{x₄}` | `∅` |

■

**[U6:6.1.1-b] Induced fixed-point functional `F_𝒮` and `μ_𝒮 = lfp(F_𝒮)`** [PPA §6.1.1, p. 370] (book p. 370; PDF p. 386)
Define `F_𝒮 : (X → L) → (X → L)` by:
```text
F_𝒮(ψ)(x) = ⨆{⟦t⟧ψ | x ⊒ t in 𝒮}
```
Because each `⟦t⟧` is monotone, `F_𝒮` is monotone on the complete lattice `X → L`. By Tarski's Fixed Point Theorem (`Proposition A.10` [PPA Proposition A.10, p. 402] (book p. 402; PDF p. 418)), `F_𝒮` has a unique least fixed point `μ_𝒮` equal to the least solution of `𝒮`. Since `L` satisfies ACC and `X` is finite, `X → L` satisfies ACC, so the ascending chain `(F_𝒮^n(⊥))_n` stabilises in finitely many steps to:
```text
μ_𝒮 = lfp(F_𝒮) = ⨆_{j≥0} F_𝒮^j(⊥)
```

### Lemma 6.4 — Correctness and Complexity of Table 6.1

**[PPA Lemma 6.4, p. 370] (book p. 370; PDF p. 386)**
> Given the assumptions, the algorithm of Table 6.1 computes the least solution of the given constraint system, `𝒮`. ■

**[U6:6.1.1-c] Proof of Lemma 6.4 and `O(h · M² · N)` complexity derivation** [PPA §6.1.1, p. 371] (book p. 371; PDF p. 387), [PPA §6.1.1, p. 372] (book p. 372; PDF p. 388)
Write `Analysis_i[x]` for `Analysis[x]` after the `i`-th Step 2 `while`-iteration:
1. **Termination (`p. 371`)**: Step 1 executes finite `for`-loops. Each Step 2 iteration extracts 1 constraint from `W` and either leaves `W` strictly smaller (`Analysis[x] ⊒ new`) or strictly increases `Analysis[x]` (`Analysis[x] ⊏ Analysis[x] ⊔ new`) while inserting at most `N` constraints (`|infl[x]| ≤ N`). By ACC on `L` and finiteness of `X`, strict increases occur finitely many times, so `W` eventually reaches `empty` (assuming finite-multiset `insert`/`extract`; see `F-U6-03`).
2. **Part (i) — Lower-bound invariant (`∀x ∈ X: Analysis_i[x] ⊑ μ_𝒮(x)`) (`p. 371`)**: Holds at `i = 0` (`⊥ ⊑ μ_𝒮(x)`). Preserved on update by monotonicity of `⟦t⟧` and `(x ⊒ t) ∈ 𝒮`:
   `Analysis_{i+1}[x] = Analysis_i[x] ⊔ ⟦t⟧(Analysis_i) ⊑ μ_𝒮(x) ⊔ ⟦t⟧(μ_𝒮) ⊑ μ_𝒮(x) ⊔ F_𝒮(μ_𝒮)(x) = μ_𝒮(x)`.
3. **Part (ii) — Reductiveness at `W = empty` (`F_𝒮(Analysis) ⊑ Analysis`, hence `μ_𝒮 ⊑ Analysis`) (`pp. 371–372`)**: Suppose for contradiction `Analysis[x] ⋣ F_𝒮(Analysis)(x)`, so some `(x ⊒ t) ∈ 𝒮` violates `Analysis[x] ⊒ ⟦t⟧(Analysis)`. Consider the last time any `y ∈ FV(t)` had `Analysis[y]` assigned (`FV(t) = ∅` reduces directly to the Step 1 branch `[derived]`; see `F-U6-03`):
   - If in Step 1, `(x ⊒ t)` entered `W` in Step 1 and was popped at some Step 2 iteration `i ≥ 1`, establishing `Analysis_i[x] ⊒ ⟦t⟧(Analysis_{i-1}) = ⟦t⟧(Analysis)`, and monotonicity of updates preserves `Analysis[x] ⊒ ⟦t⟧(Analysis)` thereafter — contradiction.
   - If in Step 2 (while processing some `y ⊒ t'`), `(x ⊒ t) ∈ infl[y]` was inserted into `W` and popped at a later `i ≥ 1` after all `z ∈ FV(t)` had reached their final values, again establishing `Analysis[x] ⊒ ⟦t⟧(Analysis)` — contradiction.
   Hence `Analysis ∈ Red(F_𝒮)` (`F_𝒮(Analysis) ⊑ Analysis`), so `μ_𝒮 = lfp(F_𝒮) = ⨅ Red(F_𝒮) ⊑ Analysis` [PPA §A.4, p. 402] (book p. 402; PDF p. 418).
4. **Part (iii) — Antisymmetry (`p. 372`)**: `Analysis ⊑ μ_𝒮` and `μ_𝒮 ⊑ Analysis` yield `Analysis = μ_𝒮`. ■
5. **`O(h · M² · N)` worst-case bound (`p. 372`)**: Let RHS variable count/size be `≤ M` (`M ≥ 1`), `eval(t, Analysis)` cost `O(M)`, lattice comparison/join/assignment cost `O(1)`, and lattice height be `≤ h` (`h ≥ 1`):
   - Writing `N_x = |infl[x]|`, each of the `N` constraints contains `≤ M` RHS variables, so `∑_{x ∈ X} N_x ≤ M · N`, and Step 1 runs in `O(N + N · M)` steps.
   - Each `Analysis[x]` strictly increases at most `h` times, bounding total worklist insertions by `N + h · ∑_{x ∈ X} N_x ≤ N + h · M · N`.
   - Each extracted constraint executes `O(M)` `eval`, giving **`O(N · M + h · M² · N) = O(h · M² · N)`** steps overall (assuming `O(1)`/`O(M)` amortised `insert`/`extract`; see `F-U6-03`).

---

## 6.1.2 Iterating in LIFO and FIFO

### Table 6.2 — Iterating in Last-In First-Out Order (LIFO)

**[PPA Table 6.2, p. 373] (book p. 373; PDF p. 389)**
```text
empty = nil
function insert((x ⊒ t),W)
return cons((x ⊒ t),W)
function extract(W)
return (head(W), tail(W))
```
Combining `Table 6.1` with `Table 6.2` generalises both Chapter 2's `Table 2.8` (`U2`) and Chapter 3's `Table 3.7` (`U3`) [PPA §6.1.2, p. 372] (book p. 372; PDF p. 388):

### Example 6.5 — Specialisation to Chapter 2 `Table 2.8` (`O(h · b)` and `O(b²)` RD)

**[PPA Example 6.5, p. 372] (book p. 372; PDF p. 388), [PPA Example 6.5, p. 373] (book p. 373; PDF p. 389)**
In `Table 2.8` [PPA Table 2.8, p. 75] (book p. 75; PDF p. 94), each constraint `Analysis[ℓ'] ⊒ f_ℓ(Analysis[ℓ])` is represented on `W` by the flow edge `(ℓ, ℓ') ∈ F` (since `ℓ` uniquely determines `f_ℓ`), with `infl[ℓ'] = {(ℓ', ℓ'') ∈ F | ℓ'' ∈ Lab}`. With `b` elementary blocks, `N = O(b)` and `M = 1`, specialising `O(h · M² · N)` to **`O(h · b)`** — and for Reaching Definitions (`h = O(b)`), **`O(b²)`**, matching `Example 2.30` [PPA Example 2.30, p. 78] (book p. 78; PDF p. 97). ■

### Example 6.6 — Specialisation to Chapter 3 `Table 3.7` (`O(n³)` 0-CFA)

**[PPA Example 6.6, p. 373] (book p. 373; PDF p. 389)**
In `Table 3.7` [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196), constraints `{t} ⊆ p`, `p₁ ⊆ p`, and `{t} ⊆ p₂ ⇒ p₁ ⊆ p` use a *segregated* worklist holding flow variables (`p₁` or `p₂`, plus `p` seeded by `{t} ⊆ p` `[derived]`; see `F-U6-06`), `infl[p]` corresponds to `E[p]`, Step 2 of `Table 3.7` builds `E`, Step 3's `for`-loop traverses `E[q]`, and `Analysis[p]` is `D[p]`. For program size `n`, `N = O(n²)`, `h ≤ n`, and `M = 1`, specialising `O(h · M² · N)` to **`O(n³)`**, matching `§3.4.2` [PPA §3.4.2, p. 177] (book p. 177; PDF p. 195). ■

**[U6:6.1.2-a] Duplicate-entry hazard in naive LIFO and FIFO queue alternative** [PPA §6.1.2, p. 373] (book p. 373; PDF p. 389), [PPA §6.1.2, p. 374] (book p. 374; PDF p. 390)
- **Duplicate pushes on naive LIFO**: `Table 6.2` performs `cons` without checking membership, so `W` accumulates duplicate constraint copies and recomputes downstream RHSs prematurely (`Exercise 6.3` adds membership deduplication).
- **FIFO extraction (`p. 374`)**: treats `W` as a first-in first-out queue (also optionally deduplicated).

### Figure 6.1 and Example 6.7 — LIFO Iteration Walkthrough

**[PPA Figure 6.1, p. 374] (book p. 374; PDF p. 390), [PPA Example 6.7, p. 374] (book p. 374; PDF p. 390)**
Running `Tables 6.1 + 6.2` on `Examples 6.1` and `6.3` (`–` denotes unchanged from previous row; `1` Step 1 row + `14` Step 2 `extract` iterations, evaluating `x₆` multiple times and draining stale `[x₂, x₃, x₄, x₅, x₆]` in rows 10–14):

| Step | `W` | `x₁` | `x₂` | `x₃` | `x₄` | `x₅` | `x₆` |
| ---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| init | `[x₁, x₂, x₃, x₄, x₅, x₆]` | `∅` | `∅` | `∅` | `∅` | `∅` | `∅` |
| 1 | `[x₂, x₄, x₂, x₃, x₄, x₅, x₆]` | `X_?` | `–` | `–` | `–` | `–` | `–` |
| 2 | `[x₃, x₆, x₄, x₂, x₃, x₄, x₅, x₆]` | `–` | `X_{3?}` | `–` | `–` | `–` | `–` |
| 3 | `[x₂, x₆, x₄, x₂, x₃, x₄, x₅, x₆]` | `–` | `–` | `X_{3?}` | `–` | `–` | `–` |
| 4 | `[x₆, x₄, x₂, x₃, x₄, x₅, x₆]` | `–` | `–` | `–` | `–` | `–` | `–` |
| 5 | `[x₄, x₂, x₃, x₄, x₅, x₆]` | `–` | `–` | `–` | `–` | `–` | `X_{3?}` |
| 6 | `[x₅, x₆, x₂, x₃, x₄, x₅, x₆]` | `–` | `–` | `–` | `X_{5?}` | `–` | `–` |
| 7 | `[x₄, x₆, x₂, x₃, x₄, x₅, x₆]` | `–` | `–` | `–` | `–` | `X_{5?}` | `–` |
| 8 | `[x₆, x₂, x₃, x₄, x₅, x₆]` | `–` | `–` | `–` | `–` | `–` | `–` |
| 9 | `[x₂, x₃, x₄, x₅, x₆]` | `–` | `–` | `–` | `–` | `–` | `X_{35?}` |
| 10 | `[x₃, x₄, x₅, x₆]` | `–` | `–` | `–` | `–` | `–` | `–` |
| 11 | `[x₄, x₅, x₆]` | `–` | `–` | `–` | `–` | `–` | `–` |
| 12 | `[x₅, x₆]` | `–` | `–` | `–` | `–` | `–` | `–` |
| 13 | `[x₆]` | `–` | `–` | `–` | `–` | `–` | `–` |
| 14 | `[]` | `–` | `–` | `–` | `–` | `–` | `–` |

■

---

## 6.2 Iterating in Reverse Postorder

**[U6:6.2-a] Dependency digraph `G_𝒮`, minimal handles `H_𝒮`, DFSF `T`, and `rPostorder`** [PPA §6.2, p. 375] (book p. 375; PDF p. 391), [PPA §6.2, p. 376] (book p. 376; PDF p. 392)
To propagate information as far forward as possible before cycling back, impose a directed graph `G_𝒮` on `𝒮 = (x_i ⊒ t_i)_{i=1}^N`:
- **Nodes**: one node per constraint `x_i ⊒ t_i`.
- **Directed edges**: `(x_i ⊒ t_i) → (x_j ⊒ t_j)` iff `x_i ∈ FV(t_j)` (equivalently `(x_j ⊒ t_j) ∈ infl[x_i]`).
- **Roots versus minimal handles**: forward `WHILE` analyses typically admit a single *root* `r` (`{r}` is a handle, e.g. `{x₁}` in `Example 6.1`), whereas backward `WHILE` analyses and `0-CFA` systems (`Example 6.2`) generally lack a single root. Rather than adding synthetic dummy roots/edges, select a **minimal handle** `H_𝒮` (a node set from which every node in `G_𝒮` is reachable, minimal wrt `⊂`; e.g. `{x₂, x₄}` in `Example 6.2`, `p. 375`; always exists by Appendix C though not necessarily unique).
- **Reverse postorder (`rPostorder`)**: run `Table C.1` [PPA Table C.1, p. 421] (book p. 421; PDF p. 436) on `(G_𝒮, H_𝒮)` to obtain a depth-first spanning forest `T` and `rPostorder` numbering (`U10`).

### Figure 6.2, Table 6.3, and Example 6.8 — Constraint Graph, DFST, and RPO Worklist

**[PPA Figure 6.2, p. 376] (book p. 376; PDF p. 392), [PPA Example 6.8, p. 376] (book p. 376; PDF p. 392)**
- **`Figure 6.2(a)` Graphical representation `G_𝒮` for `Example 6.1`**: directed edges `x₁ → x₄`, `x₁ → x₂`, `x₄ ↔ x₅` (2-cycle), `x₂ ↔ x₃` (2-cycle), `x₄ → x₆`, and `x₂ → x₆` (vector diagram omitted by OCR).
- **`Figure 6.2(b)` Depth-first spanning tree `T` rooted at `x₁`**: left child `x₄` (with left child `x₆` and right child `x₅`), right child `x₂` (with child `x₃`). Left-to-right postorder finishes `x₆, x₅, x₄, x₃, x₂, x₁`, giving `rPostorder` sequence `x₁, x₂, x₃, x₄, x₅, x₆` (`Example 6.8`). ■

**[PPA Table 6.3, p. 376] (book p. 376; PDF p. 392)**
```text
empty = (nil,∅)
function insert((x ⊒ t),(W.c,W.p))
return (W.c,(W.p ∪ {x ⊒ t}))
function extract((W.c,W.p))
if W.c = nil then
    W.c := sort_rPostorder(W.p);
    W.p := ∅
return ( head(W.c), (tail(W.c),W.p) )
```

**[U6:6.2-b] Double-buffered `(W.c, W.p)` mechanics and data-structure complexity** [PPA §6.2, p. 377] (book p. 377; PDF p. 393), [PPA §6.2, p. 378] (book p. 378; PDF p. 394)
- **Two-phase sweep inside `Table 6.1`**: `W.c` is the *current* inner pass sorted in `rPostorder`; `W.p` is the *pending* set for the next pass (`insert` adds strictly to `W.p`, `extract` pops `W.c`, refilling `W.c := sort_rPostorder(W.p); W.p := ∅` only when `W.c = nil`; `W ≠ empty` tests `(W.c, W.p) ≠ (nil, ∅)`).
- **Data-structure costs for `N` insertions + `N` extractions (`pp. 377–378`)**:
  1. *`2-3` tree priority queue (`[4]`)* keyed by `rPostorder`: `O(log₂ N)` per operation `⇒` `O(N log₂ N)`.
  2. *Linked list + comparison sort on refill*: `O(1)` list ops + `O(N log₂ N)` batch sort `⇒` `O(N log₂ N)` amortised.
  3. *Length-`N` bit vector `W.p` (constraints pre-indexed `1..N` in `rPostorder`)*: `O(1)` bit-set on `insert` + single `O(N)` `1..N` scan on refill `⇒` **`O(N)`** per dense batch of `N` operations (see `F-U6-04` for sparse-refill caveat).
- **Correctness**: immediate from `Lemma 6.4` by viewing abstract worklist contents as `W.c ∪ W.p` (`p. 378`).

### Figure 6.3 and Example 6.9 — Reverse Postorder Iteration Walkthrough

**[PPA Figure 6.3, p. 377] (book p. 377; PDF p. 393), [PPA Example 6.9, p. 378] (book p. 378; PDF p. 394)**
`Table 6.3` on `Example 6.1` with `rPostorder` `x₁, ···, x₆` finishes in **`11` Step 2 iterations** (vs `14` for LIFO in `Figure 6.1`; row 6 displays the refilled `W.c` one step early relative to `Table 6.3` — see `F-U6-05`):

| Step | `W.c` | `W.p` | `x₁` | `x₂` | `x₃` | `x₄` | `x₅` | `x₆` |
| ---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| init | `[]` | `{x₁, ···, x₆}` | `∅` | `∅` | `∅` | `∅` | `∅` | `∅` |
| 1 | `[x₂, x₃, x₄, x₅, x₆]` | `{x₂, x₄}` | `X_?` | `–` | `–` | `–` | `–` | `–` |
| 2 | `[x₃, x₄, x₅, x₆]` | `{x₂, x₃, x₄, x₆}` | `–` | `X_{3?}` | `–` | `–` | `–` | `–` |
| 3 | `[x₄, x₅, x₆]` | `{x₂, x₃, x₄, x₆}` | `–` | `–` | `X_{3?}` | `–` | `–` | `–` |
| 4 | `[x₅, x₆]` | `{x₂, ···, x₆}` | `–` | `–` | `–` | `X_{5?}` | `–` | `–` |
| 5 | `[x₆]` | `{x₂, ···, x₆}` | `–` | `–` | `–` | `–` | `X_{5?}` | `–` |
| 6 | `[x₂, x₃, x₄, x₅, x₆]` | `∅` | `–` | `–` | `–` | `–` | `–` | `X_{35?}` |
| 7 | `[x₃, x₄, x₅, x₆]` | `∅` | `–` | `–` | `–` | `–` | `–` | `–` |
| 8 | `[x₄, x₅, x₆]` | `∅` | `–` | `–` | `–` | `–` | `–` | `–` |
| 9 | `[x₅, x₆]` | `∅` | `–` | `–` | `–` | `–` | `–` | `–` |
| 10 | `[x₆]` | `∅` | `–` | `–` | `–` | `–` | `–` | `–` |
| 11 | `[]` | `∅` | `–` | `–` | `–` | `–` | `–` | `–` |

■

---

## 6.2.1 The Round Robin Algorithm

**[U6:6.2.1-a] Replacing `W.p` and `infl` with `change` and fixed RPO sweeps** [PPA §6.2.1, p. 378] (book p. 378; PDF p. 394)
Replacing `sort_rPostorder(W.p)` by the full static RPO list `[1, ···, N]` collapses `W.p` into a single boolean `change` (`false` iff `W.p = ∅`) and eliminates `infl` altogether, yielding the two-loop *Round Robin Algorithm* (`Table 6.4`).

### Table 6.4, Figure 6.4, Example 6.10, and Lemma 6.11 — Round Robin Algorithm

**[PPA Table 6.4, p. 379] (book p. 379; PDF p. 395)**
```text
INPUT:   A system 𝒮 of constraints: x₁ ⊒ t₁, ···, x_N ⊒ t_N
         ordered 1 to N in reverse postorder
OUTPUT:  The least solution: Analysis
METHOD:  Step 1: Initialisation
                 for all x ∈ X do
                     Analysis[x] := ⊥
                 change := true;

         Step 2: Iteration (updating Analysis)
                 while change do
                     change := false;
                     for i := 1 to N do
                         new := eval(t_i,Analysis);
                         if Analysis[x_i] ⋣ new then
                             change := true;
                             Analysis[x_i] := Analysis[x_i] ⊔ new;

USING:   function eval(t,Analysis)
         return ⟦t⟧(Analysis)
```

**[PPA Example 6.10, p. 378] (book p. 378; PDF p. 394), [PPA Figure 6.4, p. 379] (book p. 379; PDF p. 395)**
On `Example 6.1` ordered `x₁, ···, x₆` (`*` marks `change := false` at the top of each `while`-sweep; `1` Step 1 init + `2` `while`-sweeps = `3` total iterations and `12` `eval` checks, with all `6` updates occurring in Pass 1):

| Pass / Step | `change` | `x₁` | `x₂` | `x₃` | `x₄` | `x₅` | `x₆` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Step 1 (init) | `true` | `∅` | `∅` | `∅` | `∅` | `∅` | `∅` |
| Pass 1 start | `* false` | | | | | | |
| Pass 1 `i = 1..6` | `true` (`×6`) | `X_?` | `X_{3?}` | `X_{3?}` | `X_{5?}` | `X_{5?}` | `X_{35?}` |
| Pass 2 start | `* false` | | | | | | |
| Pass 2 `i = 1..6` | `false` (`×6`) | `–` (`×6`) | `–` (`×6`) | `–` (`×6`) | `–` (`×6`) | `–` (`×6`) | `–` (`×6`) |

■

**[PPA Lemma 6.11, p. 378] (book p. 378; PDF p. 394)**
> Given the assumptions, the algorithm of Table 6.4 computes the least solution of the given constraint system, `𝒮`. ■ *(Proof left as `Exercise 6.9`, `p. 380`.)*

### Lemma 6.12 and Example 6.13 — Bit Vector Loop-Connectedness Bound

**[U6:6.2.1-b] Bit Vector Framework preconditions, `d(G_𝒮, T)`, and iteration-count convention** [PPA §6.2.1, p. 380] (book p. 380; PDF p. 396), [PPA §6.2.1, p. 381] (book p. 381; PDF p. 397)
- **Bit Vector Framework instance (`p. 380`)**: `L = 𝒫(D)` for finite `D` (`⊑ ∈ {⊆, ⊇}` left implicit on `p. 380`, stated explicitly in `Mini Project 6.1` `p. 387`) and every RHS `t_i` has the unary affine form
  ```text
  t_i = (x_{j_i} ∩ Y_i^1) ∪ Y_i^2
  ```
  for subsets `Y_i^1, Y_i^2 ⊆ D` and a single flow variable `x_{j_i} ∈ X` (covering all `§2.1` classical analyses after splitting `x_i ⊒ t_i^1 ⊔ ··· ⊔ t_i^{k_i}` into separate inequations; cf. `Exercise 2.9` [PPA Exercise 2.9, p. 137] (book p. 137; PDF p. 156)).
- **Loop connectedness `d(G_𝒮, T) ≥ 0`** (`Appendix C` [PPA §C.2, p. 424] (book p. 424; PDF p. 439)): maximum number of *back edges* (edges `(u, v)` not topologically ordered by `rPostorder`, i.e. `rPostorder[v] ≤ rPostorder[u]`) on any **cycle-free** path in `G_𝒮`.
- **Iteration count convention (`p. 380`)**: `Table 6.4` is said to iterate `n ≥ 1` times when Step 1 executes `1` time and Step 2's `while`-loop executes `n - 1` times.

**[PPA Lemma 6.12, p. 380] (book p. 380; PDF p. 396)**
> Under the assumptions stated above, the algorithm of Table 6.4 halts after at most `d(G_𝒮, T) + 3` iterations. It therefore performs at most `O((d(G_𝒮, T) + 1) · N)` assignments. ■
>
> *Proof (`p. 380`)*: Along any cycle-free path containing `d ≤ d(G_𝒮, T)` back edges, RPO-increasing segments propagate a datum forward in a single `for`-sweep up to the source of the next back edge, so `d + 1` `while`-sweeps propagate all information across all `d` back edges (`[derived]` reading relying on the Bit Vector form `(x_{j_i} ∩ Y_i^1) ∪ Y_i^2` so cyclic paths collapse to cycle-free paths), `+ 1` final `while`-sweep observes `change = false`, `+ 1` for Step 1 `=` `d + 3 ≤ d(G_𝒮, T) + 3` iterations, each performing `≤ N` evaluations/assignments. ■

- **`WHILE` corollary and Fortran Folk Theorem (`pp. 380–381`)**: For `WHILE` flow graphs, `d(G_𝒮, T)` is independent of DFSF `T` and equals the maximal `while`-loop nesting depth `d`, giving **`O((d + 1) · b)`** vs `O(b²)` (`Example 2.30` — mis-cited as `"Example 2.8"` on `p. 380`; see `F-U6-06`). The empirical Fortran study (`[98]`) found `d ≤ 3` almost everywhere, yielding the *Folk Theorem* that Round Robin runs in linear time in practice.

**[PPA Example 6.13, p. 381] (book p. 381; PDF p. 397)**
`Example 6.1` has `d(G_𝒮, T) = 1`, so `Lemma 6.12` bounds Round Robin by `1 + 3 = 4` iterations (`1` Step 1 + `3` `while`-sweeps); `Example 6.10` / `Figure 6.4` finished in `3` iterations (`1` Step 1 + `2` `while`-sweeps). ■

---

## 6.3 Iterating Through Strong Components

**[U6:6.3-a] Strong components, reduced DAG, and topological order** [PPA §6.3, p. 381] (book p. 381; PDF p. 397)
Partition `G_𝒮` into its maximal strongly connected subgraphs (*strong components*, `Fact C.3` [PPA Fact C.3, p. 418] (book p. 418; PDF p. 433)). Contracting each strong component to a vertex (dropping self-loops between equal components) yields the *reduced graph*, which is always a **DAG** (`Lemma C.5` [PPA Lemma C.5, p. 419] (book p. 419; PDF p. 434)) and admits a *topological order* `SC₁ ≤ SC₂` computed via reverse postorder on the reduced graph (`Corollary C.11` [PPA Corollary C.11, p. 424] (book p. 424; PDF p. 439)) (`U10`).

### Example 6.14, Figure 6.5, and Table 6.5 — Strong Components and `srPostorder`

**[PPA Example 6.14, p. 381] (book p. 381; PDF p. 397), [PPA Example 6.14, p. 382] (book p. 382; PDF p. 398), [PPA Figure 6.5, p. 382] (book p. 382; PDF p. 398)**
- `Figure 6.5(a)`: 4 strong components `{x₁}`, `{x₂, x₃}`, `{x₄, x₅}`, `{x₆}`.
- `Figure 6.5(b)`: diamond reduced DAG `{x₁} → {x₄, x₅} → {x₆}` and `{x₁} → {x₂, x₃} → {x₆}`, admitting two topological orders: `{x₁}, {x₂, x₃}, {x₄, x₅}, {x₆}` and `{x₁}, {x₄, x₅}, {x₂, x₃}, {x₆}`. In `WHILE` programs (both forward and backward), every *non-trivial* strong component is an outermost `while`-loop (the printed sentence omits *"non-trivial"*; see `F-U6-07`). ■

**[PPA Table 6.5, p. 382] (book p. 382; PDF p. 398)**
Assigns each `(x ⊒ t)` a pair `srPostorder[x ⊒ t] = (scc, rp)` (`fst = scc`, `snd = rp`):
```text
INPUT:   A graph partitioned into strong components
OUTPUT:  srPostorder
METHOD:  scc := 1;
         for each scc in topological order do
             rp := 1;
             for each x ⊒ t in the strong component scc
                 in local reverse postorder do
                     srPostorder[x ⊒ t] := (scc,rp);
                     rp := rp + 1
             scc := scc + 1;
```
*(Source bug `F-U6-08`: `scc` is overloaded simultaneously as the integer counter `1, 2, ···` and as the `for each` strong-component set binder!)*

**[U6:6.3-b] Three-level SCC iteration (`Table 6.6`) and `(W.c, W.pc, W.pf)` split** [PPA §6.3, p. 383] (book p. 383; PDF p. 399)
Simulates 3 nested loops inside `Table 6.1` without modifying `Table 6.1`:
1. *Outermost*: visits strong components in topological order (`min fst(srPostorder[·])`; because the reduced graph is a DAG, updating `scc` can schedule constraints in `scc` or later `> scc` components, **never** earlier `< scc` components!).
2. *Intermediate*: repeats passes over the active component `scc` until no constraint of `scc` remains in `W.p`.
3. *Inner*: sweeps active constraints of `scc` in local reverse postorder `rp`.
Pairs `(scc, rp)` may be linearised into integers preserving lexicographic order (`p. 383`), or `W.p` may be split into `W.pc` (current SCC) and `W.pf` (future SCCs) (`Exercise 6.12`, `[77]`). Correctness (`Lemma 6.4`) and `O(h · M² · N)` worst-case complexity carry over unchanged.

### Table 6.6, Figure 6.6, and Example 6.15 — Strong-Component Worklist Walkthrough

**[PPA Table 6.6, p. 384] (book p. 384; PDF p. 400)**
```text
empty = (nil,∅)
function insert((x ⊒ t),(W.c,W.p))
return (W.c,(W.p ∪ {x ⊒ t}))
function extract((W.c,W.p))
local variables: scc, W_scc
if W.c = nil then
    scc := min{fst(srPostorder[x ⊒ t]) | (x ⊒ t) ∈ W.p};
    W_scc := {(x ⊒ t) ∈ W.p | fst(srPostorder[x ⊒ t]) = scc};
    W.c := sort_srPostorder(W_scc);
    W.p := W.p \ W_scc;
return ( head(W.c), (tail(W.c),W.p) )
```

**[PPA Example 6.15, p. 383] (book p. 383; PDF p. 399), [PPA Figure 6.6, p. 384] (book p. 384; PDF p. 400)**
Using topological order `{x₁}, {x₂, x₃}, {x₄, x₅}, {x₆}`, `Table 6.6` finishes in **`10` Step 2 iterations** (vs `14` LIFO, `11` RPO, `12` RR checks), evaluating `x₆` **strictly once** after both upstream loop SCCs settle (and displaying intermediate `W.c = []` rows literally at steps 1, 3, 5, 7, 9):

| Step | `W.c` | `W.p` | `x₁` | `x₂` | `x₃` | `x₄` | `x₅` | `x₆` |
| ---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| init | `[]` | `{x₁, ···, x₆}` | `∅` | `∅` | `∅` | `∅` | `∅` | `∅` |
| 1 | `[]` | `{x₂, ···, x₆}` | `X_?` | `–` | `–` | `–` | `–` | `–` |
| 2 | `[x₃]` | `{x₃, ···, x₆}` | `–` | `X_{3?}` | `–` | `–` | `–` | `–` |
| 3 | `[]` | `{x₂, ···, x₆}` | `–` | `–` | `X_{3?}` | `–` | `–` | `–` |
| 4 | `[x₃]` | `{x₄, x₅, x₆}` | `–` | `–` | `–` | `–` | `–` | `–` |
| 5 | `[]` | `{x₄, x₅, x₆}` | `–` | `–` | `–` | `–` | `–` | `–` |
| 6 | `[x₅]` | `{x₅, x₆}` | `–` | `–` | `–` | `X_{5?}` | `–` | `–` |
| 7 | `[]` | `{x₄, x₅, x₆}` | `–` | `–` | `–` | `–` | `X_{5?}` | `–` |
| 8 | `[x₅]` | `{x₆}` | `–` | `–` | `–` | `–` | `–` | `–` |
| 9 | `[]` | `{x₆}` | `–` | `–` | `–` | `–` | `–` | `–` |
| 10 | `[]` | `∅` | `–` | `–` | `–` | `–` | `–` | `X_{35?}` |

■

---

## Concluding Remarks

**[U6:CR-a] Iterative solvers (`[96, 69, 92, 98, 77, 87, 4]`)** [PPA Chapter 6 Concluding Remarks, p. 384] (book p. 384; PDF p. 400), [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401)
General lattice worklist algorithms (`[96]`); forward RPO vs backward postorder of DFSF, *integrated form* storing constraints `(x ⊒ t)` on `W` vs *segregated form* storing flow variables `x` on `W`, and Round Robin (`[69]`); Round Robin convergence analysis (`[92]`); empirical Fortran loop-connectedness Folk Theorem (`[98]`); strong-component iteration with priority queues `currentQ`, `pendingQ`, `futureQ` matching `W.c, W.pc, W.pf` (`[77, 87]`); `2-3` trees (`[4]`) — see `## Bibliography` below for full author entries.

**[U6:CR-b] Local / demand-driven fixed-point solvers (`[29, 51, 54, 52, 53]`)** [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401)
When only a small subset of flow variables is queried in a massive constraint system, *local solvers* compute a partial least fixed point on demand over the query's dependency cone while dynamically approximating strong components:
1. **Top-down solver** (`[29]`): recursive demand-driven evaluation developed for logic programming languages.
2. **Timestamp max-priority-queue local solver** (`[51, 54]`): orders worklist entries by dynamic discovery timestamps to approximate SCCs at run time.
3. **Differential worklist local solver** (`[52, 53]`): propagates only incremental differences `Δ` between old and new values to affected sub-terms (`Exercise 6.5` captures the static splitting core).

**[U6:CR-c] Elimination methods (`[146, 154, 144, 11, 170, 171]`) and practical systems (`[177, 185, 104, 117, 17, 97, 26, 172, 8, 7]`)** [PPA Chapter 6 Concluding Remarks, p. 386] (book p. 386; PDF p. 402), [PPA Chapter 6 Concluding Remarks, p. 387] (book p. 387; PDF p. 403)
- **Elimination methods** (surveyed by Ryder & Paull `[146]`):
  - *Structural analysis* (`[154]`, akin to high-level Data Flow Analysis `[144]` & `§1.6` [PPA §1.6, p. 20] (book p. 20; PDF p. 40)): postorder DFSF reduction of structured subgraphs into a single-node *control tree* (capable of translating machine code to high-level programs), solved by a bottom-up transfer-synthesis pass followed by a top-down evaluation pass.
  - *Interval analysis* (`[11]`): collapses single-entry cycles + acyclic extensions into a derived sequence of graphs (coarser than structural trees; stalls on irreducible graphs `[external]`), solved by a backward then forward pass.
  - *Path algebras* (`[170, 171]`): reduces intraprocedural Data Flow Analysis to regular path expressions.
- **Practical analyzer toolkits**: `Spare` `[177]`, `System Z` `[185]` (denotational `[117]`), and `PAG` `[104]` (eager functional DSLs supporting complete lattices, widenings `§4.2`/`Exercise 6.13`, and bit-vector / AVL `[4]` / `BDD's` `[26]` binary decision diagram set representations); graph rewriting `[17]` and modal logic `[97]`; `Sharlit` `[172]` (Bit-Vector elimination); and `BANE` `[8]` (Standard ML toolkit solving general set constraints `[7]` for Constraint Based Analysis and Type Systems).

---

## Mini Projects 6.1–6.2 and Exercises 6.1–6.14

**[PPA Mini Project 6.1, p. 387] (book p. 387; PDF p. 403), [PPA Mini Project 6.1, p. 388] (book p. 388; PDF p. 404) — Comparison of Algorithms**
For Bit Vector Frameworks (`L = (𝒫(D), ⊑)` with `D` finite and `⊑` either `⊆` or `⊇`; `ℱ = {f : 𝒫(D) → 𝒫(D) | ∃Y_f^1, Y_f^2 ⊆ D: ∀Y ⊆ D: f(Y) = (Y ∩ Y_f^1) ∪ Y_f^2}`), implement a solver selectable across `(i)` Round Robin (`Table 6.4`), `(ii)` deduplicated LIFO (`Table 6.2` + `Exercise 6.3`), `(iii)` deduplicated RPO (`Table 6.3` + `Exercise 6.6`), and `(iv)` deduplicated SCC + local RPO (`Table 6.6` + `Exercise 6.11`), benchmark worst/average-case behaviour, and (*ambitious*) generalise to Chapters 2 and 3 systems. ■

**[PPA Mini Project 6.2, p. 388] (book p. 388; PDF p. 404) — Algorithms for Conditional Constraints**
Studies constraint systems whose RHS terms follow:
```text
t ::= x | ⊥ | c | t₁ ⊔ t₂ | t₁ ⊓ t₂ | if t₁ ≠ ⊥ then t₂ | if c ⊑ t₁ then t₂
```
(`x` flow variable, `c` primitive constant such as `{fn x => x^1}`). Tasks: `(1)` verify `§6.1` monotonicity (`[derived]`: `t₁ ≠ ⊥` and `c ⊑ t₁` with *constant* `c` are upward-closed in `ψ`, with implicit `else ⊥`); `(2)` simplify `if ... then t₂` online to `t₂` once its monotone guard becomes true under LIFO (`Tables 6.1–6.2`); `(3)` prove correctness & analyse complexity; `(4)` add `Exercise 6.3` deduplication; `(5)` apply to Chapter 3; (*ambitious*) extend to RPO / SCC algorithms, accounting for how dynamic guard activation adds new dependency edges that can merge SCCs and invalidate static `rPostorder`/`srPostorder`! ■

- **[PPA Exercise 6.1, p. 389] (book p. 389; PDF p. 405)**: Re-run `Example 6.7` when Step 1 produces `W = [x₆, ···, x₁]` instead of `[x₁, ···, x₆]` and compare step counts (`[derived]`: **`20` Step 2 pops** — `x₁` is only popped at Step 12 because non-empty constant `gen` sets `X_5` / `X_3` cause `x₄`/`x₅` and `x₂`/`x₃` to cycle earlier, popping `x₆` `5` times total across Step 1's empty `∅` pop and `4` propagation steps). ■
- **[PPA Exercise 6.2, p. 389] (book p. 389; PDF p. 405)**: Walkthrough of `Tables 6.1 + 6.2` (LIFO) on `Example 6.2`'s 8-constraint `0-CFA` system for `((fn x => x) (fn y => y))`. ■
- **[PPA Exercise 6.3, p. 389] (book p. 389; PDF p. 405)**: Modify `Table 6.2` (`insert`) so a constraint already in `W` is not re-inserted; re-run `Example 6.7` (`[derived]`: reduces `14` Step 2 pops to **`8` Step 2 pops** — `9` table rows including Step 1 init; `[x₁, x₂, x₃, x₂, x₄, x₅, x₄, x₆]`, evaluating `x₆` strictly once). ■
- **[PPA Exercise 6.4, p. 389] (book p. 389; PDF p. 405)**: Formulate a worklist solver for node *dominators* `Dom(n)` in `(N, A)` with handle `H` (greatest solution under `⊆`, i.e. least solution on `(𝒫(N), ⊇)` with `⊥ = N`, `⊔ = ∩`):
  `Dom(n) = {n}` if `n ∈ H`, else `{n} ∪ ⋂_{(n', n) ∈ A} Dom(n')`. ■
- **[PPA Exercise 6.5, p. 389] (book p. 389; PDF p. 405) — `O(h · M² · N) → O(h · M · N)` Inequation Splitting**: For `(x_i ⊒ t_i^1 ⊔ ··· ⊔ t_i^M)_{i=1}^N` where each `t_i^j` has `O(1)` size and `O(1)` `eval` cost: direct `Table 6.1` takes `O(h · M² · N)` steps, whereas splitting into the solution-equivalent `M · N` system `((x_i ⊒ t_i^j)_{j=1}^M)_{i=1}^N` (dropped by OCR on `p. 389`) has `N' = M · N` constraints of size `M' = O(1)`, solving in **`O(h · 1² · (M · N)) = O(h · M · N)`** steps! ■
- **[PPA Exercise 6.6, p. 389] (book p. 389; PDF p. 405)**: Deduplicate `Table 6.3` (`insert` skips `x ⊒ t` if already in `W.p ∪ W.c`); re-run `Example 6.9` (`[derived]`: cuts `11` Step 2 pops to **`8` Step 2 pops** — `9` table rows including Step 1 init; `[x₁..x₆, x₂, x₄]`, evaluating `x₆` strictly once). ■
- **[PPA Exercise 6.7, p. 390] (book p. 390; PDF p. 406)**: Using priority queues for `(W.c, W.p)` in RPO, route `x' ⊒ t'` directly into `W.c` whenever `rPostorder[x' ⊒ t'] > rPostorder[x ⊒ t]` (downstream in the *current* RPO sweep) and into `W.p` only on back/self edges (`≤`), keeping `W.c` maximal without breaking RPO order; re-run `Example 6.9`. ■
- **[PPA Exercise 6.8, p. 390] (book p. 390; PDF p. 406)**: Express Chapter 2 `Example 2.5` [PPA Example 2.5, p. 42] (book p. 42; PDF p. 61) Available Expressions over `{x₁, ···, x_{10}}` (`x₁ = ∅`, `x₂ = x₆`, `x₃ = x₇ ∩ x_{10}`, `x₄ = x₈`, `x₅ = x₉`, `x₆ = x₁ ∪ {a+b}`, `x₇ = x₂ ∪ {a*b}`, `x₈ = x₃ ∪ {a+b}`, `x₉ = x₄ \ {a+b, a*b, a+1}`, `x_{10} = x₅ ∪ {a+b}`), construct `G_𝒮`, compute `rPostorder` via Appendix C, and trace `Table 6.4` (with `⊑ = ⊇`, `⊥ = {a+b, a*b, a+1}`, `⊔ = ∩`). ■
- **[PPA Exercise 6.9, p. 390] (book p. 390; PDF p. 406)**: Complete the proof of `Lemma 6.11` (`Table 6.4` correctness). ■
- **[PPA Exercise 6.10, p. 390] (book p. 390; PDF p. 406)**: Compute strong components and `srPostorder` for `Exercise 6.8` and solve via `§6.3`. ■
- **[PPA Exercise 6.11, p. 390] (book p. 390; PDF p. 406)**: Deduplicate `Table 6.6` (`insert` skips `x ⊒ t` if already in `W.p ∪ W.c`); re-run `Example 6.15` (`[derived]`: cuts `10` pops to `8`). ■
- **[PPA Exercise 6.12, p. 391] (book p. 391; PDF p. 407)**: Implement three priority queues `(W.c, W.pc, W.pf)` (`currentQ, pendingQ, futureQ` `[77]`, misprinted `"two priority queues"` in line 1; see `F-U6-09`), routing `x' ⊒ t'` to `W.c` if `scc' = scc ∧ rp' > rp`, to `W.pc` if `scc' = scc ∧ rp' ≤ rp`, and to `W.pf` if `scc' > scc`; re-run `Example 6.15`. ■
- **[PPA Exercise 6.13, p. 391] (book p. 391; PDF p. 407) — Worklist Solver with Widening `∇` (`U7`)**: Modify `Table 6.1` Step 2 (`Analysis[x] := Analysis[x] ∇ new` guarded by `if Analysis[x] ⋣ new`) using widening `∇` (`§4.2` [PPA §4.2, p. 226] (book p. 226; PDF p. 243)); prove `∇` on `L` lifts pointwise to a widening on finite `X → L`, guaranteeing finite termination at a sound upper approximation `μ_𝒮 ⊑ Analysis` without ACC. ■
- **[PPA Exercise 6.14, p. 391] (book p. 391; PDF p. 407), [PPA Exercise 6.14, p. 392] (book p. 392; PDF p. 408) — Fast Functions and Fastness Closure `f̄`**: Monotone `f : L → L` is *fast* iff `f ∘ f ⊑ f ⊔ id` (every idempotent `f ∘ f = f` — hence every Bit Vector transfer `f(Y) = (Y ∩ A) ∪ B` — is fast!). Define `f^⟨n⟩ = (f ⊔ id)^n` (`n ≥ 0`); if `f^⟨i_f⟩ = f^⟨i_f + 1⟩`, define the *fastness closure* `f̄ = f^⟨i_f⟩`. Prove: `(i)` `f^⟨i_f⟩ = f^⟨j⟩` for `j ≥ i_f`; `(ii)` `f̄` is idempotent and fast; `(iii)` `f̄ ⊒ f ⊔ id`, with `f̄ = f ⊔ id` when `f` is fast and distributive (additive); `(iv)` for distributive `f` and simple-loop functional `F(g) = id ⊔ (g ∘ f)`, `F^{n+1}(⊥) = (f ⊔ id)^n = ⨆_{j=0}^n f^j`, hence **`lfp(F) = f̄`** (`= f ⊔ id` when `f` is fast and distributive — closing loops in one non-iterative algebraic step!). ■

---

## Subject Index — Book Pages 433–437, PDF Pages 447–451, Offset `+14`

**[U6:IDX-a] Subject Index boundaries, headword tally, and Chapter 6 ontology anchors** [PPA Index, p. 433] (book p. 433; PDF p. 447), [PPA Index, p. 437] (book p. 437; PDF p. 451)
Two-column alphabetical Subject Index spanning 5 pages (`379` headwords total; `book p. 438` is an absent blank verso):
- **`p. 433` (`PDF p. 447`)**: `abstract 0-CFA, 147` → `complete lattice, 393` (`69` headwords) [PPA Index, p. 433] (book p. 433; PDF p. 447).
- **`p. 434` (`PDF p. 448`)**: `completely additive, 395` → `fast, 391` (`79` headwords) [PPA Index, p. 434] (book p. 434; PDF p. 448).
- **`p. 435` (`PDF p. 449`)**: `fastness closure, 391` → `Meet Over all Paths, 78` (`80` headwords) [PPA Index, p. 435] (book p. 435; PDF p. 449).
- **`p. 436` (`PDF p. 450`)**: `Meet over all Valid Paths, 89` → `set constraints, 201, 387` (`80` headwords) [PPA Index, p. 436] (book p. 436; PDF p. 450).
- **`p. 437` (`PDF p. 451`)**: `sets of states analysis, 265` → `Y2K, 356` (`71` headwords) [PPA Index, p. 437] (book p. 437; PDF p. 451).
- **Chapter 6 indexed headwords**: `abstract worklist algorithm, 369`; `BANE, 387`; `Bit Vector Framework, 137, 380, 387`; `conditional constraint, 12, 173, 367`; `constraint system, 60, 69, 367`; `depth-first spanning forest, 375, 422`; `directed graph, 375, 417`; `equation system, 60, 65, 66, 69, 366`; `fast, 391`; `fastness closure, 391`; `FIFO, 374`; `first-in first-out, 374`; `flow variable, 365`; `graph formulation of the constraints, 177, 375`; `handle, 375, 419`; `inequation system, 366`; `influence set, 369`; `last-in first-out, 372`; `LIFO, 372`; `loop connectedness, 380, 424`; `Monotone Framework, 68, 391`; `PAG, 387`; `reduced graph, 381, 419`; `reverse postorder, 375, 422`; `root, 375, 419`; `Round Robin Algorithm, 378`; `set constraints, 201, 387`; `Sharlit, 387`; `Spare, 387`; `strong component, 381, 419`; `strongly connected, 381, 419`; `System Z, 387`; `widening operator, 226, 267, 391`; `worklist, 74, 179, 368, 369`.
- **Unindexed Chapter 6 concepts (`[derived]`)**: *local solvers* (`top down solver`, `differential worklist`, `time stamps`, `p. 385`), *elimination methods* (`structural analysis`, `control tree`, `interval analysis`, `path algebras`, `p. 386`), *integrated vs segregated form* (`p. 384`), and `rPostorder` / `srPostorder` (`pp. 375, 382`) have no Subject Index entries.

---

## Bibliography — Book Pages 439–452, PDF Pages 452–465, Offset `+13`

**[U6:BIB-a] Closed 185-entry Bibliography directory (`[1]`–`[185]`, zero gaps)** [PPA Bibliography, p. 439] (book p. 439; PDF p. 452), [PPA Bibliography, p. 452] (book p. 452; PDF p. 465)
All `185` numbered entries verified on `PDF pp. 452–465` (`[130]` on `p. 448` prints an external web note omitted below per `C5.4`):
- **`book p. 439` (`PDF p. 452`, `[1]`–`[10]`)** [PPA Bibliography, p. 439] (book p. 439; PDF p. 452): `[1]` Abadi, Banerjee, Heintze, Riecke (POPL '99, dependency calculus); `[2]` Agesen (ECOOP '95, CPA); `[3]` Agesen, Palsberg, Schwartzbach (ECOOP '93, SELF type inference); `[4]` Aho, Hopcroft, Ullman (1974, *Design & Analysis of Computer Algorithms*); `[5]` Aho, Sethi, Ullman (1986, *Compilers*); `[6]` Aiken (CP '94, set constraints); `[7]` Aiken (*SCP* 1999, set-constraint analysis); `[8]` Aiken, Fähndrich, Foster, Su (TIC '98, BANE); `[9]` Aiken, Wimmers (FPCA '93, type inclusion constraints); `[10]` Aiken, Wimmers, Lakshman (POPL '94, soft typing).
- **`book p. 440` (`PDF p. 453`, `[11]`–`[23]`)** [PPA Bibliography, p. 440] (book p. 440; PDF p. 453): `[11]` Allen, Cocke (*CACM* 1976, interval DFA); `[12]` Alpern, Wegman, Zadeck (POPL '88, value numbering); `[13]` Amtoft, Nielson, Nielson (1999, *Type and Effect Systems*); `[14]` Amtoft, Nielson, Nielson (*JFP* 1997, concurrent behaviours); `[15]` Amtoft, Nielson, Nielson, Ammann (LNCS 1192, 1997, polymorphic subtyping dynamic semantics); `[16]` Arnold, Guessarian (1996, *Mathematics for CS*); `[17]` Assmann (CC '96, graph-rewriting DFA); `[18]` Banerjee (ICFP '97, modular polyvariant closure analysis); `[19]` Benton (LFCS '92, strictness logic); `[20]` Benton (WSA '93, lazy datatypes strictness); `[21]` Biswas (POPL '97, demand-driven set-based analysis); `[22]` Bodei, Degano, Nielson, Nielson (CONCUR '98, π-calculus CFA); `[23]` Bodei, Degano, Nielson, Nielson (FOSSACS '99, no read-up/write-down).
- **`book p. 441` (`PDF p. 454`, `[24]`–`[36]`)** [PPA Bibliography, p. 441] (book p. 441; PDF p. 454): `[24]` Bourdoncle (*JFP* 1992 `[sic: vol. 10]`, dynamic partitioning); `[25]` Bourdoncle (FMPA '93, efficient chaotic iteration strategies with widenings); `[26]` Bryant (*CSUR* 1992, OBDDs); `[27]` Burn, Hankin, Abramsky (*SCP* 1986, higher-order strictness); `[28]` Charatonik, Pacholski (FOCS '94, set constraints with projections in `NEXPTIME`); `[29]` Le Charlier, Van Hentenryck (*TOPLAS* 1994, top-down Prolog AI solver); `[30]` Chase, Wegman, Zadeck (PLDI '90, pointer/shape analysis); `[31]` Colby (PEPM '95, communication topology); `[32]` Colby (SAS '95, storage properties); `[33]` Cortesi, Filé, Giacobazzi, Palamidessi, Ranzato (SAS '95, complementation in AI); `[34]` Cortesi et al. (*TOPLAS* 1997, complementation in AI); `[35]` Cousot (1981, semantic foundations of PA); `[36]` Cousot (POPL '97, types as abstract interpretations).
- **`book p. 442` (`PDF p. 455`, `[37]`–`[49]`)** [PPA Bibliography, p. 442] (book p. 442; PDF p. 455): `[37]` Cousot, Cousot (POPL '77, AI unified lattice model); `[38]` Cousot, Cousot (*SIGPLAN* 1977, type unions); `[39]` Cousot, Cousot (POPL '79, systematic design of PA frameworks); `[40]` Cousot, Cousot (PLILP '92, Galois vs widening/narrowing); `[41]` Cousot, Halbwachs (POPL '78, `[external: convex polyhedra]` / linear restraints — glossed as `convex polygons` in [PPA Chapter 4 Concluding Remarks, p. 272] (book p. 272; PDF p. 289)); `[42]` Cytron, Ferrante, Rosen, Wegman, Zadek `[sic]` (*TOPLAS* 1991, SSA & CDG); `[43]` Davey, Priestley (1990, *Lattices and Order*); `[44]` Deutsch (POPL '90, higher-order lifetime/aliasing); `[45]` Deutsch (PLDI '94, beyond `k`-limiting); `[46]` Eidorf, Henglein, Mossin, Niss, Sørensen, Tofte (POPL '99, AnnoDomini Y2K); `[47]` Emami, Ghiya, Hendren (PLDI '94, context-sensitive function pointers); `[48]` Even (1979, *Graph Algorithms*); `[49]` Faxén (SAS '95, lazy functional flow inference).
- **`book p. 443` (`PDF p. 456`, `[50]`–`[62]`)** [PPA Bibliography, p. 443] (book p. 443; PDF p. 456): `[50]` Faxén (LNCS 1192, 1997, polyvariance & polymorphism); `[51]` Fecht, Seidl (SAS '96, timestamp local solver); `[52]` Fecht, Seidl (ESOP '98, propagating differences); `[53]` Fecht, Seidl (*NJC* 1998, propagating differences); `[54]` Fecht, Seidl (*SCP* 1999, faster equation solver); `[55]` Fischer, LeBlanc (1988, *Crafting a Compiler*); `[56]` Flanagan, Felleisen (Rice TR 1994, futures touch); `[57]` Flanagan, Felleisen (POPL '95, futures semantics/optimisation); `[58]` Fuh, Mishra (TAPSOFT '89, polymorphic subtype inference); `[59]` Fuh, Mishra (*TCS* 1990, type inference with subtypes); `[60]` Gasser, Nielson, Nielson (ICFP '97, CML CFA); `[61]` Ghiya, Hendren (LCPC '95, connection analysis); `[62]` Ghiya, Hendren (POPL '96, tree/dag/cycle shape analysis).
- **`book p. 444` (`PDF p. 457`, `[63]`–`[76]`)** [PPA Bibliography, p. 444] (book p. 444; PDF p. 457): `[63]` Giacobazzi, Ranzato (ESOP '96, disjunctive AI); `[64]` Giacobazzi, Ranzato (*SCP* 1998, optimal disjunctive domains); `[65]` Giegerich, Möncke, Wilhelm (GI '81, transformation invariance); `[66]` Granger (*IJCM* 1989, arithmetical congruences); `[67]` Granger (TAPSOFT '91, linear congruence equalities); `[68]` Hansen, Jensen, Nielson, Nielson (SAS '99, mobile ambients); `[69]` Hecht (1977, *Flow Analysis of Computer Programs*); `[70]` Heintze (LFP '94, ML set-based analysis); `[71]` Heintze (SAS '95, CFA and type systems); `[72]` Heintze, Jaffar (LICS '90, Herbrand set constraints); `[73]` Heintze, Jaffar (LICS '92, logic program analysis engine); `[74]` Heintze, Riecke (POPL '98, SLam calculus); `[75]` Henglein, Mossin (ESOP '94, polymorphic binding-time analysis); `[76]` Hopcroft, Ullman (1979, *Automata Theory*).
- **`book p. 445` (`PDF p. 458`, `[77]`–`[90]`)** [PPA Bibliography, p. 445] (book p. 445; PDF p. 458): `[77]` Horwitz, Demers, Teitelbaum (*Acta Inf.* 1987, SCC iterative DFA); `[78]` Jagannathan, Weeks (LFP '94, parallel stores); `[79]` Jagannathan, Weeks (POPL '95, unified higher-order flow / `k`-CFA complexity); `[80]` Jagannathan, Wright (SAS '95, polymorphic splitting); `[81]` Jensen (FPCA '91, logical strictness); `[82]` Jensen (LICS '92, disjunctive strictness); `[83]` Jones (ESOP '92, qualified types); `[84]` Jones, Muchnick (1981, Lisp-like structure flow); `[85]` Jones, Muchnick (POPL '82, interprocedural tokens & recursive structures); `[86]` Jones, Nielson (1995, *Handbook of Logic in CS* AI chapter); `[87]` Jourdan, Parigot (ESOP '90, grammar flow SCC); `[88]` Jouvelot (POPL '87, semantic parallelization); `[89]` Jouvelot, Gifford (PLDI '89, continuation control effects); `[90]` Jouvelot, Gifford (POPL '91 `[printed 1990]`, algebraic type/effect reconstruction).
- **`book p. 446` (`PDF p. 459`, `[91]`–`[105]`)** [PPA Bibliography, p. 446] (book p. 446; PDF p. 459): `[91]` Kahn (STACS '87, Natural Semantics); `[92]` Kam, Ullman (*JACM* 1976, global DFA & Round Robin); `[93]` Kam, Ullman (*Acta Inf.* 1977, Monotone Frameworks / MOP undecidability); `[94]` Karr (*Acta Inf.* 1976, affine relationships); `[95]` Kennedy (ESOP '94, dimension types); `[96]` Kildall (POPL '73, unified global optimization / lattice DFA); `[97]` Klein, Knoop, Koschützki, Steffen (TACAS '96, METAFrame); `[98]` Knuth (*SPE* 1971, empirical study of Fortran programs); `[99]` Landi, Ryder (POPL '91, pointer aliasing classification); `[100]` Landi, Ryder (PLDI '92, interprocedural pointer aliasing); `[101]` Larus, Hilfinger (PLDI '88, structure access conflicts); `[102]` Lucassen, Gifford (POPL '88, polymorphic effect analysis); `[103]` Marlowe, Ryder (*Acta Inf.* 1990, data-flow framework properties); `[104]` Martin (*STTT* 1998, PAG analyzer generator); `[105]` Masdupuy (ICS '91, array data dependencies).
- **`book p. 447` (`PDF p. 460`, `[106]`–`[120]`)** [PPA Bibliography, p. 447] (book p. 447; PDF p. 460): `[106]` Milner (1989, *Communication and Concurrency*); `[107]` Mitchell (*JFP* 1991, simple subtypes); `[108]` Monsuez (WSA '93, polymorphic types & widenings); `[109]` Morgan (1998, *Building an Optimising Compiler*); `[110]` Muchnick (1997, *Advanced Compiler Design & Implementation*); `[111]` F. Nielson (Edinburgh PhD 1984, AI using domain theory); `[112]` F. Nielson (*TOPLAS* 1985, denotational program transformations); `[113]` F. Nielson (1985, tensor products); `[114]` F. Nielson (1988, partial-evaluator type system); `[115]` F. Nielson (*TCS* 1989, two-level semantics & AI); `[116]` F. Nielson (PARLE '89, typed λ-calculus with processes); `[117]` F. Nielson (SAS '96, semantics-directed PA); `[118]` F. Nielson, H. R. Nielson (LFP '92, finiteness conditions); `[119]` F. Nielson, H. R. Nielson (CONCUR '93, CML to process algebras); `[120]` F. Nielson, H. R. Nielson (*TCS* 1996, CML to process algebra).
- **`book p. 448` (`PDF p. 461`, `[121]`–`[133]`)** [PPA Bibliography, p. 448] (book p. 448; PDF p. 461): `[121]` F. Nielson, H. R. Nielson (*NJC* 1996, termination types); `[122]` F. Nielson, H. R. Nielson (POPL '97, infinitary CFA / uniform `k`-CFA / coinductive specs); `[123]` F. Nielson, H. R. Nielson (PEPM '97, multi-level λ-calculi); `[124]` F. Nielson, H. R. Nielson (MFCS '98, flow logic of imperative objects); `[125]` F. Nielson, H. R. Nielson (*ENTCS* 1998, flow logics & SOS); `[126]` F. Nielson, H. R. Nielson (ESOP '99, interprocedural CFA); `[127]` F. Nielson, H. R. Nielson, Amtoft (LNCS 1192, 1997, polymorphic subtyping algorithm); `[128]` H. R. Nielson, Amtoft, F. Nielson (FASE '98, CML behaviour analysis); `[129]` H. R. Nielson, F. Nielson (*JLC* 1992, bounded fixed-point iteration); `[130]` H. R. Nielson, F. Nielson (Wiley 1992, *Semantics with Applications*, electronic edition note omitted per `C5.4`); `[131]` H. R. Nielson, F. Nielson (POPL '94, finite communication topology); `[132]` H. R. Nielson, F. Nielson (1997, CML communication analysis); `[133]` H. R. Nielson, F. Nielson (CC '98, flow logics for constraint-based analysis).
- **`book p. 449` (`PDF p. 462`, `[134]`–`[147]`)** [PPA Bibliography, p. 449] (book p. 449; PDF p. 462): `[134]` H. R. Nielson, F. Nielson, Amtoft (LNCS 1192, 1997, polymorphic subtyping static semantics); `[135]` Pacholski, Podelski (CP '97, set constraints pearl); `[136]` Palsberg (*TOPLAS* 1995, closure analysis in constraint form); `[137]` Palsberg, Schwartzbach (Wiley 1994, *Object-Oriented Type Systems*); `[138]` Pande, Ryder (SAS '96, virtual function resolution); `[139]` Plevyak, Chien (OOPSLA '94, OO concrete type inference); `[140]` Plotkin (Aarhus FN-19, 1981, Structural Operational Semantics); `[141]` Ramalingam, Field, Tip (POPL '99, aggregate structure identification); `[142]` Reif, Smolka (*IJPP* 1990, distributed process DFA); `[143]` Reynolds (IFIP '69, automatic data-set definitions); `[144]` Rosen (*CACM* 1977, high-level DFA); `[145]` Ruf (PLDI '95, context-insensitive alias analysis); `[146]` Ryder, Paull (*CSUR* 1986, elimination algorithms survey); `[147]` Sagiv, Reps, Horwitz (TAPSOFT '95, IDE/IFDS interprocedural constant propagation).
- **`book p. 450` (`PDF p. 463`, `[148]`–`[161]`)** [PPA Bibliography, p. 450] (book p. 450; PDF p. 463): `[148]` Sagiv, Reps, Wilhelm (POPL '96, destructive-update shape analysis); `[149]` Sagiv, Reps, Wilhelm (*TOPLAS* 1998, shape analysis); `[150]` Sagiv, Reps, Wilhelm (POPL '99, TVLA 3-valued shape analysis); `[151]` Schmidt (POPL '98, DFA as model checking of AI); `[152]` Sestoft (Copenhagen MSc 1988, closure analysis / parameter globalising); `[153]` Shapiro, Horwitz (POPL '97, fast flow-insensitive points-to); `[154]` Sharir (*Comp. Lang.* 1980, structural analysis); `[155]` Sharir, Pnueli (1981, call-strings & functional interprocedural DFA); `[156]` Shivers (PLDI '88, CFA in Scheme); `[157]` Shivers (1991, Scheme DFA & type recovery); `[158]` Shivers (PEPM '91, semantics of Scheme CFA); `[159]` Siekmann (*JSC* 1989, unification theory); `[160]` G. S. Smith (TAPSOFT '93, overloading & subtyping); `[161]` G. S. Smith (*SCP* 1994, principal type schemes with overloading & subtyping).
- **`book p. 451` (`PDF p. 464`, `[162]`–`[177]`)** [PPA Bibliography, p. 451] (book p. 451; PDF p. 464): `[162]` Steensgaard (POPL '96, almost-linear points-to); `[163]` Stefanescu, Zhou (LFP '94, equational higher-order flow); `[164]` Steffen (*SCP* 1993, modal DFA generation); `[165]` Stransky (*Inf. Comp.* 1990, Lisp structure lattice); `[166]` Talpin, Jouvelot (*JFP* 1992, polymorphic type/region/effect inference); `[167]` Talpin, Jouvelot (LICS '92, type and effect discipline); `[168]` Talpin, Jouvelot (*Inf. Comp.* 1994, type and effect discipline); `[169]` Tang (ENSMP PhD 1994, CFA via effects & AI); `[170]` Tarjan (*JACM* 1981, fast path-problem algorithms); `[171]` Tarjan (*JACM* 1981, unified path programs); `[172]` Tjiang, Hennessy (PLDI '92, Sharlit); `[173]` Tofte (*Inf. Comp.* 1990, polymorphic references); `[174]` Tofte, Birkedal (*TOPLAS* 1998, region inference algorithm); `[175]` Tofte, Talpin (POPL '94, stack of regions); `[176]` Tofte, Talpin (*Inf. Comp.* 1997, region-based memory management); `[177]` Venkatesh, Fischer (*IEEE TSE* 1992, Spare).
- **`book p. 452` (`PDF p. 465`, `[178]`–`[185]`)** [PPA Bibliography, p. 452] (book p. 452; PDF p. 465): `[178]` Vitek, Horspool, Uhl (CC '92, OO compile-time analysis); `[179]` Webber (PLDI '97, binary-relation PA); `[180]` Wegman, Zadeck (*TOPLAS* 1991, Sparse Conditional Constant Propagation); `[181]` Wilhelm, Maurer (1995, *Compiler Design*); `[182]` Wilson, Lam (PLDI '95, context-sensitive C pointer analysis); `[183]` Wright (ESOP '92, typing references by effects); `[184]` Wright, Felleisen (*Inf. Comp.* 1994, syntactic type soundness); `[185]` Yi, Harrison (POPL '93, System Z).

---

## Multi-Dimensional Projections (`cs_theory`, `swe_architecture`, `practical_debugging`, `cyber`)

- **`cs_theory`**:
  - **Order-Independence of `μ_𝒮 = lfp(F_𝒮)` vs Scheduling Cost**: `Lemma 6.4` proves that *every* fair extraction schedule (`LIFO`, `FIFO`, `RPO`, `SCC`) converges to the identical `μ_𝒮 = lfp(F_𝒮)` via `Analysis ∈ Red(F_𝒮)` (`F_𝒮(Analysis) ⊑ Analysis`) at `W = empty`, provided `(L, ⊑)` satisfies ACC and every `⟦t⟧` is monotone (`p. 367`). When `L` lacks ACC, `Exercise 6.13` (`U7`) lifts widening `∇` pointwise to finite `X → L` to terminate at a reductive upper bound (`[external: post-fixed-point]`).
  - **Scope Boundary of `Lemma 6.12` (`d(G_𝒮, T) + 3`) and Fastness Closure `f̄` (`Exercise 6.14`)**: `Lemma 6.12` is stated only for *Bit Vector Frameworks* (`L = 𝒫(D)`, every RHS `(x_{j_i} ∩ Y_i^1) ∪ Y_i^2`, `p. 380`), *not* for non-Bit-Vector lattices (`Constant Propagation`, `0-CFA`, intervals) where cycles ascend up to lattice height `h`. `Exercise 6.14` defines fast functions and `f̄` but states no Round Robin bound; carrying a similar bound over to fast distributive (`f ∘ f ⊑ f ⊔ id`) frameworks is `[external: Kam–Ullman rapid frameworks]` `[derived]`.
  - **Inequation Splitting & `[external: semi-naive]` Differencing**: Splitting `M`-ary joins (`Exercise 6.5`: `O(h · M² · N) → O(h · M · N)`) and differential worklists (`[52, 53]`) correspond to `[external: semi-naive Datalog evaluation]` and `[external: Paige–Koenig finite differencing]`.
- **`swe_architecture`**:
  - **Template Method + Queue Strategy (`Tables 6.1–6.6`) `[external]`**: `Table 6.1` isolates invariant `eval`/`⊔`/`infl` propagation from the pluggable queue strategy (`Table 6.2` LIFO, `Table 6.3` `(W.c, W.p)` RPO, `Table 6.6` / `Exercise 6.12` 3-queue `(W.c, W.pc, W.pf)` SCC).
  - **Why Single Min-Heaps Starve & Why Flat SCCs Differ from `[external: WTO]` `[derived]`**: Replacing `(W.c, W.p)` with a single RPO min-heap allows a tight inner self-loop (`rPostorder = 2`) to spin and starve downstream nodes in a shared multi-node cycle; `Exercise 6.7` fixes this cleanly by routing forward edges (`rPostorder[y] > rPostorder[x]`) to `W.c` and back/self edges (`≤`) to `W.p`. Flat SCC condensation (`[external: Tarjan SCC]`, `Table 6.6`) prevents premature downstream DAG evaluations (`x₆` evaluated once in `Figure 6.6`) while merging nested loops into one outer SCC; decomposing nested loops requires hierarchical `[external: Bourdoncle WTO]` (`[25]`).
  - **Integrated vs Segregated Worklists & Sparse Sets `[external]`**: Integrated constraint worklists (`Table 6.1`) pair naturally with `Exercise 6.5` `M = 1` splitting, whereas segregated variable worklists (`Table 3.7`, `[69]`) pair with differential `(x, Δ_x)` propagation (`[52, 53]`). Pairing queues with `[external: Briggs–Torczon sparse sets]` gives `O(1)` deduplication (`Exercises 6.3, 6.6, 6.11`) without `O(N)` empty-bit scans on sparse passes (`F-U6-04`).
- **`practical_debugging`**:
  - **Silent Under-Approximation (`Analysis[x] ⋣ ⟦t⟧(Analysis)` after `W = empty`) `[derived]`**: Check `(1)` `Table 6.5` `scc` variable-shadowing bug (`F-U6-08`); `(2)` conditional terms `if c ⊑ x₂ then x₁` missing either guard `x₂` or payload `x₁` from `FV(t)` / `infl` (`Example 6.2`, `Mini Project 6.2`); `(3)` source-only RHS variables missing from `X = LHS(𝒮)` (`F-U6-01`); `(4)` must-analyses (`Dom(n)` `Exercise 6.4`, `AE` `Exercise 6.8`) initialised to `∅` (`⊤`) instead of `⊥_L = U` with `⊔_L = ∩`.
  - **Thrashing, Non-Termination, or Over-Widening `[derived]`**: Check `(1)` forward RPO used on backward DFA (turning DAG edges into back edges so `d(G_𝒮, T) = Θ(b)`); `(2)` un-split `M`-way switch/merge joins (`M²` blowup, `Exercise 6.5`); `(3)` omitting `if Analysis[x] ⋣ new` before `Analysis[x] ∇ new` (diverges since `a ∇ b` need not equal `a` when `b ⊑ a`), or widening split acyclic inequations individually (`[0,0] ∇ [1,1] = [0,∞]`, `Exercise 6.13`); `(4)` dynamic guard activation (`Mini Project 6.2`) invalidating static `srPostorder`.
- **`cyber`**:
  - **Early-Cutoff Vulnerability Evasion Trap (`W ≠ empty` Under-Approximation) `[derived]` `[external]`**: `Lemma 6.4` Part (i) proves only `Analysis_i[x] ⊑ μ_𝒮(x)` for pre-termination states; an intermediate state can already equal `μ_𝒮` while `W ≠ empty` (`Figure 6.1` row 10, `Figure 6.3` rows 7–12), but it is not *certified* reductive until `W = empty`. Aborting `Table 6.1` at a naive step cap (`steps > MAX_STEPS`) and returning `Analysis_i` therefore *may* **silently under-approximate** may-taint, alias sets, and indirect call graphs — letting an adversary pad loop/call complexity ahead of a sink to starve the worklist and evade detection with zero error! Sound timeouts MUST either widen dirty variables (`Exercise 6.13`) until `W = empty` or top (`⊤_L`) the forward cone reachable from `W` in `G_𝒮` and emit a degraded-precision alert.
  - **Algorithmic Complexity DoS (`[external: CWE-400]` / `[external: CWE-407]`) & Sink-Driven Local Triage `[external]`**: Control-flow-flattened / VM-obfuscated binaries create irreducible high-`d(G_𝒮, T)` single-SCC graphs (`d = Θ(|V|)`) that defeat the Fortran Folk Theorem `d ≤ 3` assumption (`[98]`) and drive un-split solvers to `O(h · M² · N)`. Mitigate via `Exercise 6.5` unary splitting, deduplicated 3-queue SCC / `[external: Bourdoncle WTO]` scheduling, and demand-driven local solvers (`[29, 51–54]`) that slice backward solely from the queried security sink `x_sink`.

---

## Source Errata and Findings (`F-U6-01`..`F-U6-12`)

- **`F-U6-01` (`Table 6.1` & `Table 6.4` Semicolons and LHS-Only Step 1 Initialisation)**: `Table 6.1` Step 1 (`p. 369`) omits `;` after `W := insert((x ⊒ t),W)` (`Table 6.4` `p. 379` omits `;` after `Analysis[x] := ⊥`; `Table 6.5` `p. 382` omits `;` after `rp := rp + 1`), and places `Analysis[x] := ⊥; infl[x] := ∅;` inside `for all x ⊒ t in 𝒮` — redundantly re-initialising `x` on multi-inequation LHSs and leaving any unconstrained RHS variable `y ∉ LHS(𝒮)` uninitialised (relying strictly on Assumption 2 `FV(t_i) ⊆ X`, `p. 367`) [PPA §6.1, p. 367] (book p. 367; PDF p. 383), [PPA Table 6.1, p. 369] (book p. 369; PDF p. 385), [PPA Table 6.4, p. 379] (book p. 379; PDF p. 395).
- **`F-U6-02` (Implicit `else ⊥` in One-Armed Conditional RHS Terms)**: `Example 6.2` (`p. 367`) and `Mini Project 6.2` (`p. 388`) write one-armed `if ... then t₂` RHS terms without specifying their value when the guard is false; monotonicity and equivalence to `Table 3.6` [PPA Table 3.6, p. 174] (book p. 174; PDF p. 192) require implicit `else ⊥` (`∅` in `Example 6.2`) [PPA Example 6.2, p. 367] (book p. 367; PDF p. 383), [PPA Mini Project 6.2, p. 388] (book p. 388; PDF p. 404).
- **`F-U6-03` (`FV(t) = ∅` Case & Implicit Multiset / Amortised ADT Premises in `Lemma 6.4`)**: `Lemma 6.4` Part (ii) (`p. 371`) chooses *"the last time that `Analysis[y]` was assigned to, for any variable `y ∈ FV(t)`"*, implicitly assuming `FV(t) ≠ ∅` (constant constraints like `x₁ = X_?` have `FV(t) = ∅` and are discharged directly by Step 1 seeding); termination (`p. 371`) assumes finite-multiset `insert`/`extract`, and `O(h · M² · N)` (`p. 372`) assumes `O(1)` lattice ops and `O(M)`-amortised worklist ops [PPA §6.1.1, p. 371] (book p. 371; PDF p. 387), [PPA §6.1.1, p. 372] (book p. 372; PDF p. 388).
- **`F-U6-04` (Sparse-Refill `O(h · N²)` Scan Gap in `§6.2` Bit-Vector Worklist)**: `§6.2` (`pp. 377–378`) claims scanning a length-`N` bit vector `W.p` with a `1..N` `for`-loop preserves `§6.1.1`'s `O(h · M² · N)` bound; when `M = 1` and `Θ(h · N)` refills each contain `O(1)` set bits, full `1..N` scans cost `Θ(h · N²)` vs `O(h · N)` unless backed by a hierarchical bitset or `[external: sparse set]` [PPA §6.2, p. 377] (book p. 377; PDF p. 393), [PPA §6.2, p. 378] (book p. 378; PDF p. 394).
- **`F-U6-05` (Eager Refill Display in `Figure 6.3` Row 6 vs `Table 6.3`)**: In `Table 6.3` (`p. 376`), `if W.c = nil` executes on entry to `extract` *before* popping `head(W.c)`, so step 6 popping `x₆` from `([x₆], {x₂, ···, x₆})` literally yields `([], {x₂, ···, x₆})` and refills `W.c` only at step 7's `extract`; `Figure 6.3` row 6 (`p. 377`) displays `([x₂, x₃, x₄, x₅, x₆], ∅)` one step early (contrast `Figure 6.6` `p. 384`, which displays intermediate `[]` rows at steps 1, 3, 5, 7, 9) [PPA Table 6.3, p. 376] (book p. 376; PDF p. 392), [PPA Figure 6.3, p. 377] (book p. 377; PDF p. 393), [PPA Figure 6.6, p. 384] (book p. 384; PDF p. 400).
- **`F-U6-06` (Mis-Cited `"Example 2.8"` on `p. 380` & LHS/RHS Orientation Shift in `Example 6.6`)**: Bottom of `p. 380` compares `O((d + 1) · b)` against *"the `O(b²)` obtained in Examples 2.8 and 6.5"* — `Example 2.8` (`p. 46`) is Very Busy Expressions [PPA Example 2.8, p. 46] (book p. 46; PDF p. 65), whereas **`Example 2.30`** (`p. 78`, cited in `Example 6.5` on `p. 373`) proves `O(b²)`! Also `Example 6.6` (`p. 373`) calls `p₁, p₂` in `{t} ⊆ p₂ ⇒ p₁ ⊆ p` *"left hand side"* variables (using Chapter 3's `⊆` orientation rather than Chapter 6's `⊒` orientation) [PPA Example 6.6, p. 373] (book p. 373; PDF p. 389), [PPA §6.2.1, p. 380] (book p. 380; PDF p. 396).
- **`F-U6-07` (Overstated Universal Loop Claim on Trivial SCCs in `Example 6.14`)**: `Example 6.14` (`p. 382`) states *"In this example each strong component was an outermost loop. This holds in general for both forward and backward flow graphs for programs in the WHILE language"* — `{x₁}` and `{x₆}` in `Figure 6.5` are **trivial 1-node acyclic** SCCs, not loops; only *non-trivial* SCCs correspond to outermost `while`-loops [PPA Example 6.14, p. 382] (book p. 382; PDF p. 398), [PPA Figure 6.5, p. 382] (book p. 382; PDF p. 398).
- **`F-U6-08` (`scc` Variable-Shadowing / Type-Clash Bug in `Table 6.5`)**: `Table 6.5` (`p. 382`) uses `scc` simultaneously as the integer rank (`scc := 1; ... srPostorder[x ⊒ t] := (scc,rp); ... scc := scc + 1;`) and as the `for each` strong-component node-set (`for each scc in topological order do ... in the strong component scc`) [PPA Table 6.5, p. 382] (book p. 382; PDF p. 398).
- **`F-U6-09` (`"two priority queues"` for Three Queues in `Exercise 6.12` & `"the the"` in `Exercise 6.14`)**: `Exercise 6.12` (`p. 391`) says *"using **two** priority queues"* while immediately listing **three** (`W.c`, `W.pc`, `W.pf`, matching `currentQ, pendingQ, futureQ` on `p. 385`), and `Exercise 6.14` (`p. 391`) prints *"that the the fastness closure"* (also `"a srPostorder"` in `Exercise 6.10` `p. 390`) [PPA Exercise 6.10, p. 390] (book p. 390; PDF p. 406), [PPA Exercise 6.12, p. 391] (book p. 391; PDF p. 407), [PPA Exercise 6.14, p. 391] (book p. 391; PDF p. 407).
- **`F-U6-10` (Constant RHS Encoding & Unstated Order Polarity in `§6.2.1` Bit Vector Definition)**: `p. 380` defines Bit Vector Frameworks over `L = 𝒫(D)` without explicitly specifying `⊑ ∈ {⊆, ⊇}` (made explicit in `Mini Project 6.1` `p. 387`) and requires a flow variable `x_{j_i}` in every RHS `(x_{j_i} ∩ Y_i^1) ∪ Y_i^2` (encoding constant `x₁ = X_?` requires setting `Y_1^1 = ∅` on dummy `x_{j_1}`) [PPA §6.2.1, p. 380] (book p. 380; PDF p. 396), [PPA Mini Project 6.1, p. 387] (book p. 387; PDF p. 403).
- **`F-U6-11` (Verified Subject Index & Bibliography Errata)**: Subject Index: `p. 433` `"Call-Tracking Analysis, 23"` omits `353` (`Mini Project 5.1`); `p. 435` prints `"lower adjoint , 239"` (space before comma); `p. 437` `"Side Effect Analysis, 320"` starts one page after `§5.4.1` (`p. 319`). Bibliography: `[24]` (`p. 441`) prints *JFP* `10:407–435, 1992` (contradicting `[107]` `JFP 1(3), 1991` & `[166]` `JFP 2(3), 1992`); `[42]` (`p. 442`) misspells `Zadeck` as `"Zadek"`; `[61]` (`p. 443`) prints `"eight workshop"`; `[90]` (`p. 445`) prints `POPL '91 ... 1990`; `[131]` (`p. 448`) lists `Springer` for `POPL '94`; `[156]` (`p. 450`) prints `SIGPLAN Notices` `volume 7 (1)`; `[157]` (`p. 450`) duplicates `"In P.Lee, editor, In Topics"`; `[180]` (`p. 452`) omits *TOPLAS* volume [PPA Index, p. 435] (book p. 435; PDF p. 449), [PPA Bibliography [24], p. 441] (book p. 441; PDF p. 454), [PPA Bibliography [42], p. 442] (book p. 442; PDF p. 455), [PPA Bibliography [90], p. 445] (book p. 445; PDF p. 458), [PPA Bibliography [180], p. 452] (book p. 452; PDF p. 465).
- **`F-U6-12` (PDF OCR Text-Layer Drops & Corruptions)**: `pdftotext` completely drops `x ⊒ t₁ ··· x ⊒ t_n` (`p. 366`), `(x_i ⊒ t_i)_{i=1}^N` & `((fn x => x^1)^2 (fn y => y^3)^4)^5` (`p. 367`), vector diagrams `Figures 6.2 & 6.5` (`pp. 376, 382`), and `((x_i ⊒ t_i^j)_{j=1}^M)_{i=1}^N` (`Exercise 6.5`, `p. 389`), and mangles `⊒`/`⋣`/`⊥`, `du-chain` (`p. 434` → `d'Ur-chain`), and `[63]`–`[75]`, `[172]` brackets (`pp. 444, 451`) [PPA §6.1, p. 366] (book p. 366; PDF p. 382), [PPA Exercise 6.5, p. 389] (book p. 389; PDF p. 405), [PPA Index, p. 434] (book p. 434; PDF p. 448), [PPA Bibliography, p. 444] (book p. 444; PDF p. 457).

---

## Gotcha Ledger

- G-U6-01: Unit 6 spans three distinct PDF-to-book coordinate offsets due to absent blank versos (`pp. 364, 416, 428, 438`): `+16` across Chapter 6, book pages 365–392 / PDF pages 381–408; `+14` across Subject Index, book pages 433–437 / PDF pages 447–451; and `+13` across Bibliography, book pages 439–452 / PDF pages 452–465 [PPA Chapter 6, p. 365] (book p. 365; PDF p. 381), [PPA Index, p. 433] (book p. 433; PDF p. 447), [PPA Bibliography, p. 439] (book p. 439; PDF p. 452).
- G-U6-02: Multiple inequations sharing an LHS (`x ⊒ t₁, ···, x ⊒ t_n`) have the exact same solutions as `x = x ⊔ t₁ ⊔ ··· ⊔ t_n` and the same *least* solution as `x = t₁ ⊔ ··· ⊔ t_n`, **not** the same general solutions (`x = t₁ ⊔ ··· ⊔ t_n` rejects strict reductive points `x ⊐ t₁ ⊔ ··· ⊔ t_n`) [PPA §6.1, p. 366] (book p. 366; PDF p. 382).
- G-U6-03: Keeping `M` join summands grouped in one equation `x_i ⊒ t_i^1 ⊔ ··· ⊔ t_i^M` costs `O(h · M² · N)` in `Table 6.1`, whereas splitting into `M` separate inequations `(x_i ⊒ t_i^j)_{j=1}^M` cuts worst-case solver time by a factor of `M` to **`O(h · M · N)`** (`Exercise 6.5`) [PPA §6.1.1, p. 372] (book p. 372; PDF p. 388), [PPA Exercise 6.5, p. 389] (book p. 389; PDF p. 405).
- G-U6-04: Standing assumption `FV(t_i) ⊆ X = {x_i | 1 ≤ i ≤ N}` (`p. 367`) requires every RHS flow variable to appear on at least one LHS because `Table 6.1` Step 1 (`p. 369`) initialises `Analysis[x]` and `infl[x]` only inside `for all x ⊒ t in 𝒮` (`F-U6-01`) [PPA §6.1, p. 367] (book p. 367; PDF p. 383), [PPA Table 6.1, p. 369] (book p. 369; PDF p. 385).
- G-U6-05: Encoding Chapter 3 conditional constraints `{t} ⊆ p₂ ⇒ p₁ ⊆ p` as RHS terms `p ⊇ if {t} ⊆ p₂ then p₁` (`Example 6.2`, `Mini Project 6.2`) relies on an implicit `else ⊥` (`∅`) branch (`F-U6-02`) and requires `FV(if c ⊑ t₁ then t₂) = FV(t₁) ∪ FV(t₂)` so `infl` registers **both** guard and payload variables [PPA Example 6.2, p. 367] (book p. 367; PDF p. 383), [PPA Example 6.6, p. 373] (book p. 373; PDF p. 389), [PPA Mini Project 6.2, p. 388] (book p. 388; PDF p. 404).
- G-U6-06: Termination and least-solution correctness of `Table 6.1` (`Lemma 6.4`) hold for **every** fair worklist schedule (`LIFO`, `FIFO`, `RPO`, `SCC`), *provided* `(L, ⊑)` satisfies **ACC** and every `⟦t⟧` is **monotone**; infinite-height lattices without ACC require widening (`Exercise 6.13`) [PPA §6.1, p. 367] (book p. 367; PDF p. 383), [PPA Lemma 6.4, p. 370] (book p. 370; PDF p. 386), [PPA Exercise 6.13, p. 391] (book p. 391; PDF p. 407).
- G-U6-07: `Table 6.1` stays below `μ_𝒮` (`Analysis_i[x] ⊑ μ_𝒮(x)`, `Lemma 6.4` Part (i)) and is *certified* reductive (`Analysis ∈ Red(F_𝒮)`, `F_𝒮(Analysis) ⊑ Analysis`) only at `W = empty` (Part (ii)); intermediate states may already equal `μ_𝒮` with `W ≠ empty` (`Figure 6.1` row 10, `Figure 6.3` rows 7–12), so aborting early on `[external: timeout]` (`W ≠ empty`) *may* return an under-approximation (silent `[external: false negatives]` in security/CFA scanners) unless remaining dirty cones are widened or topped `[derived]` [PPA Table 6.1, p. 369] (book p. 369; PDF p. 385), [PPA §6.1.1, p. 371] (book p. 371; PDF p. 387).
- G-U6-08: `Table 6.1`'s `O(h · M² · N)` bound (`p. 372`) assumes `O(1)` lattice join/comparison and `O(1)`/`O(M)`-amortised `insert`/`extract` (`F-U6-03`); non-bitset set unions over `O(n)` universes add an `O(n)` factor, and `2-3` tree priority queues (`O(log₂ N)`, `p. 377`) add a `log N` factor when `M = 1` `[derived]` [PPA §6.1.1, p. 372] (book p. 372; PDF p. 388), [PPA §6.2, p. 377] (book p. 377; PDF p. 393).
- G-U6-09: Naive LIFO (`Table 6.2`) skips membership deduplication on `insert`, pushing duplicate constraints onto `W` (`14` Step 2 pops in `Figure 6.1` vs `20` reversed in `Exercise 6.1` and `8` deduplicated / `9` table rows incl. init in `Exercise 6.3`, `11` in RPO `Figure 6.3` vs `8` deduplicated in `Exercise 6.6`, `12` inner checks across `2` sweeps in Round Robin `Figure 6.4`, and `10` in SCC `Figure 6.6` vs `8` deduplicated in `Exercise 6.11`) [PPA Figure 6.1, p. 374] (book p. 374; PDF p. 390), [PPA Figure 6.3, p. 377] (book p. 377; PDF p. 393), [PPA Figure 6.4, p. 379] (book p. 379; PDF p. 395), [PPA Figure 6.6, p. 384] (book p. 384; PDF p. 400).
- G-U6-10: Backward Data Flow Analyses and `0-CFA` constraint graphs `G_𝒮` (`Example 6.2`) generally lack a single root node; computing `rPostorder` via `Table C.1` requires a **minimal handle `H_𝒮`** (`{x₂, x₄}` in `Example 6.2`, `p. 375`), which always exists though need not be unique [PPA §6.2, p. 375] (book p. 375; PDF p. 391).
- G-U6-11: `Table 6.3` implements RPO iteration via **two** collections `(W.c, W.p)` (draining current pass `W.c` before sorting `W.p`, or routing forward edges `rPostorder[x'] > rPostorder[x]` to `W.c` and back/self edges `≤` to `W.p` in `Exercise 6.7`), preventing an early self-loop with small `rPostorder` from starving downstream nodes in a single min-heap `[derived]` [PPA Table 6.3, p. 376] (book p. 376; PDF p. 392), [PPA Exercise 6.7, p. 390] (book p. 390; PDF p. 406).
- G-U6-12: Representing `W.p` as a length-`N` bit vector scanned `1..N` on refill (`pp. 377–378`) costs `O(N)` per refill even when `1` bit is set (`Θ(h · N²)` across `Θ(h · N)` sparse passes unless backed by a `[external: sparse set]`, `F-U6-04`), and `Figure 6.3` row 6 (`p. 377`) displays the refilled `W.c` one step earlier than `Table 6.3` executes (`F-U6-05`) [PPA Table 6.3, p. 376] (book p. 376; PDF p. 392), [PPA §6.2, p. 377] (book p. 377; PDF p. 393).
- G-U6-13: `Lemma 6.12`'s `d(G_𝒮, T) + 3` Round-Robin iteration bound (`O((d + 1) · N)` assignments) holds **only for Bit Vector Frameworks** (`L = 𝒫(D)`, single-variable RHS `(x_{j_i} ∩ Y_i^1) ∪ Y_i^2`), **never** for general ACC Monotone Frameworks (`Constant Propagation`, `0-CFA`, intervals) where cycles can ascend up to height `h` [PPA Lemma 6.12, p. 380] (book p. 380; PDF p. 396); any fast distributive (`f ∘ f ⊑ f ⊔ id`) extension is `[external: Kam–Ullman rapid frameworks]` `[derived]`.
- G-U6-14: In `Lemma 6.12` and `Example 6.13` (`pp. 380–381`), Chapter 6 counts Step 1 initialisation as `1` iteration plus `n - 1` `while`-sweeps (`d + 3` = `1` init + `≤ d + 1` propagation sweeps + `1` quiescence sweep; `3` iterations = `2` sweeps in `Figure 6.4`), and `p. 380` mis-cites `Example 2.8` instead of `Example 2.30` for the `O(b²)` RD bound (`F-U6-06`) [PPA Figure 6.4, p. 379] (book p. 379; PDF p. 395), [PPA §6.2.1, p. 380] (book p. 380; PDF p. 396).
- G-U6-15: On general (irreducible) constraint graphs `G_𝒮`, loop connectedness `d(G_𝒮, T)` depends on DFSF `T` (and can reach `Θ(|V|)` on `[external: obfuscated/flattened]` CFGs), whereas on `WHILE` flow graphs `d(G_𝒮, T)` is independent of `T` and equals maximal `while`-nesting depth `d` (`d ≤ 3` Fortran Folk Theorem `[98]`) [PPA §6.2.1, p. 380] (book p. 380; PDF p. 396), [PPA §6.2.1, p. 381] (book p. 381; PDF p. 397).
- G-U6-16: `Table 6.5` (`p. 382`) contains a **variable-shadowing / type-clash bug** (`F-U6-08`) reusing `scc` as both the integer rank (`scc := 1; ... scc := scc + 1;`) and the `for each scc` component node-set; implementations must separate `scc_id : int` from `comp : Set` [PPA Table 6.5, p. 382] (book p. 382; PDF p. 398).
- G-U6-17: Flat strong-component iteration (`Table 6.6`, `Figure 6.5`) isolates parallel/sequential loops and evaluates downstream `{x₆}` once (`Figure 6.6`), **but** merges nested inner loops into their outermost loop's SCC (and `Example 6.14` `p. 382` omits *"non-trivial"* when claiming every SCC in `WHILE` is an outermost loop, `F-U6-07`); decomposing nested loops requires `[external: Bourdoncle WTO]` (`[25]`) [PPA Example 6.14, p. 382] (book p. 382; PDF p. 398), [PPA Bibliography [25], p. 441] (book p. 441; PDF p. 454).
- G-U6-18: Splitting `W.p` into `W.pc` (current SCC) and `W.pf` (future SCCs) requires **three** priority queues `(W.c, W.pc, W.pf)` (`currentQ, pendingQ, futureQ` `[77]`, `p. 385`; misprinted `"two priority queues"` in `Exercise 6.12` `p. 391`, `F-U6-09`) and relies on `Lemma C.5` (reduced graph is a DAG) so updates never target `< scc` components [PPA §6.3, p. 383] (book p. 383; PDF p. 399), [PPA Exercise 6.12, p. 391] (book p. 391; PDF p. 407).
- G-U6-19: Demand-driven *local solvers* (`[29]` top-down, `[51, 54]` timestamp PQ, `[52, 53]` differential worklist), *elimination methods* (`[154]` structural, `[11]` interval, `[170, 171]` path algebras), and *integrated vs segregated* worklists (`[69]`) reside in Chapter 6 *Concluding Remarks* (`pp. 384–386`), whereas `Table 6.6` (`p. 384`) is the 3-level SCC worklist solver (and none of those Concluding Remarks solver terms appear in the Subject Index) [PPA Table 6.6, p. 384] (book p. 384; PDF p. 400), [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401), [PPA Chapter 6 Concluding Remarks, p. 386] (book p. 386; PDF p. 402).
- G-U6-20: Online simplification / lazy guard activation for conditional constraints (`Mini Project 6.2`, `p. 388`) preserves monotonicity only for upward-closed guards (`t₁ ≠ ⊥`, `c ⊑ t₁` with constant `c`) and dynamically adds dependency edges during solving, which can merge SCCs and invalidate static `rPostorder`/`srPostorder` numberings `[derived]` [PPA Mini Project 6.2, p. 388] (book p. 388; PDF p. 404).
- G-U6-21: Dualising `Tables 6.1–6.6` for greatest-fixed-point `must` analyses (`Dom(n)` in `Exercise 6.4`, Available Expressions in `Exercise 6.8`) sets `L = (𝒫(U), ⊇)` — so `⊥` in Step 1 is the **full universe `U`** (not `∅`!), `⊔` is **`∩`**, and `Analysis[x] ⋣ new` is **`¬(Analysis[x] ⊆ new)`** [PPA Mini Project 6.1, p. 387] (book p. 387; PDF p. 403), [PPA Exercise 6.4, p. 389] (book p. 389; PDF p. 405), [PPA Exercise 6.8, p. 390] (book p. 390; PDF p. 406).
- G-U6-22: Lifting widening `∇` into `Table 6.1` Step 2 (`Analysis[x] := Analysis[x] ∇ new`, `Exercise 6.13` `p. 391`) **must retain** the `if Analysis[x] ⋣ new` guard for termination (since `∇` need not satisfy `a ∇ b = a` when `b ⊑ a`), relies on `X` being **finite**, and over-widens acyclic joins if split inequations for the same LHS are widened individually rather than joined with `⊔` first `[derived]` [PPA Exercise 6.13, p. 391] (book p. 391; PDF p. 407).
- G-U6-23: For distributive `f`, the loop functional `F(g) = id ⊔ (g ∘ f)` satisfies `F^{n+1}(⊥) = (f ⊔ id)^n = ⨆_{j=0}^n f^j` (`Exercise 6.14`, printing `"the the"` on `p. 391`, `F-U6-09`); when `f` is also *fast* (`f ∘ f ⊑ f ⊔ id`, true of every Bit Vector transfer), `lfp(F) = f̄ = f ⊔ id` closes simple loops non-iteratively [PPA Exercise 6.14, p. 391] (book p. 391; PDF p. 407), [PPA Exercise 6.14, p. 392] (book p. 392; PDF p. 408).
- G-U6-24: Subject Index (`pp. 433–437`) and Bibliography (`[1]`–`[185]`, `pp. 439–452`) contain verified source quirks preserved at `L3` (`F-U6-11`, `F-U6-12`: `lower adjoint , 239` `p. 435`; `[24]` `JFP 10, 1992`; `[42]` `Zadek`; `[90]` `POPL '91 ... 1990`; `[180]` missing volume; `[130]` online URL omitted in core per `C5.4`; OCR `d'Ur-chain` and `[63)` bracket damage) [PPA Index, p. 435] (book p. 435; PDF p. 449), [PPA Bibliography [24], p. 441] (book p. 441; PDF p. 454), [PPA Bibliography [42], p. 442] (book p. 442; PDF p. 455), [PPA Bibliography [90], p. 445] (book p. 445; PDF p. 458).
