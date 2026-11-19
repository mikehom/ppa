<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Chapter 2 L1 reference for intraprocedural DFA, def-use chains, Monotone Frameworks, and MFP/MOP solving. -->

# Intraprocedural Data Flow Analysis, Def-Use Chains, and Monotone Frameworks

Scope: Chapter 2, §§2.1–2.1.5, §§2.3–2.4.2, Mini Projects 2.1 & 2.3, and Exercises 2.1–2.13 —
[PPA §2.1, p. 35] (book p. 35; PDF p. 54) through [PPA §2.4.2, p. 82] (book p. 82; PDF p. 101)
and [PPA Mini Project 2.1, p. 132] (book p. 132; PDF p. 151) through [PPA Exercise 2.13, p. 137] (book p. 137; PDF p. 156).
Ground truth: verbatim tables, proofs, examples, and findings live in `corpus/shards/RAW_SHARD_02a_intraproc_dfa.md`
and `corpus/shards/RAW_SHARD_02b_interproc_shape.md`. Shared foundations live in
[chapter-1-five-formulations.md](../../ppa-program-analysis/references/chapter-1-five-formulations.md),
[appendix-a-posets-lattices-fixed-points.md](../../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md),
and [appendix-c-graphs-dfsf-and-rpo.md](../../ppa-program-analysis/references/appendix-c-graphs-dfsf-and-rpo.md);
semantic correctness (`§2.2`, `Mini Project 2.2`) and interprocedural extensions (`§2.5`) live in
[interprocedural-and-correctness.md](./interprocedural-and-correctness.md).
Conventions: `[external]` = non-book term; `[derived]` = direct consequence of printed definitions;
`G-U2a-*` / `G-U2b-*` point to raw-shard gotcha ledgers; `BKL-*` point to `issues/backlog/`.

## 1. Flow Graphs and Structural Preconditions (§2.1)

Data flow analyses in `§2.1` operate over `WHILE` elementary blocks (`[x := a]^ℓ`, `[skip]^ℓ`, and tests
`[b]^ℓ` inside conditionals and loops) using five syntax-directed extractors
[PPA §2.1, p. 35] (book p. 35; PDF p. 54) [PPA §2.1, p. 36] (book p. 36; PDF p. 55):

- **`init : Stmt → Lab`** returns the unique entry label (`init(S₁; S₂) = init(S₁)`, `init(if [b]^ℓ ...) = ℓ`,
  `init(while [b]^ℓ do S) = ℓ`), whereas **`final : Stmt → 𝒫(Lab)`** returns a set of exit labels
  (`final(if [b]^ℓ then S₁ else S₂) = final(S₁) ∪ final(S₂)`, `final(while [b]^ℓ do S) = {ℓ}`) because a
  conditional has multiple exits and a `while`-loop exits immediately after its test `[b]^ℓ` evaluates to
  `false` (`G-U2a-01`, `Example 2.1`, `Figure 2.1`) [PPA §2.1, p. 36] (book p. 36; PDF p. 55)
  [PPA Figure 2.1, p. 38] (book p. 38; PDF p. 57).
- **`blocks(S)`** gathers syntactic elementary blocks, **`labels(S) = {ℓ | [B]^ℓ ∈ blocks(S)}`**, and
  **`flow(S)`** collects control edges `(ℓ₁, ℓ₂)` (`S₁; S₂` links `final(S₁)` to `init(S₂)`; conditionals link
  `ℓ` to `init(S₁)` and `init(S₂)`; `while` links `ℓ` to `init(S)` and `final(S)` back to `ℓ`)
  [PPA §2.1, p. 37] (book p. 37; PDF p. 56). **`flow^R(S) = {(ℓ, ℓ') | (ℓ', ℓ) ∈ flow(S)}`** reverses edges
  for backward analyses (`Example 2.2`, `Figure 2.3`) [PPA §2.1, p. 38] (book p. 38; PDF p. 57).
- **Graph coverage identities (`G-U2a-02`, `G-U2a-03`)**: `labels(S) = {init(S)} ∪ dom(flow(S)) ∪ ran(flow(S))`
  (and dual with `final(S)` and `flow^R(S)`), where removing `{init(S)}` or `final(S)` is valid *only* for
  composite statements, never single elementary blocks `[B]^ℓ` [PPA §2.1, p. 37] (book p. 37; PDF p. 56);
  moreover `(labels(S), flow^R(S))` has a unique entry only when `|final(S)| = 1`
  [PPA §2.1, p. 38] (book p. 38; PDF p. 57).

| Precondition / Set | Exact Requirement | Failure Mode When Violated | Source Anchor |
| :--- | :--- | :--- | :--- |
| **`Lab⋆, Var⋆, AExp⋆`** | `Lab⋆ = labels(S⋆)`, `Var⋆ = FV(S⋆)`, `AExp⋆` keeps *non-trivial* subexpressions (`G-U2a-04`: excludes variables/constants) | Including trivial `x` or `n` bloats `AE`/`VB`; unbounded `Var` or `AExp` breaks ACC (`G-U2a-26`) | [PPA §2.1, p. 38] (book p. 38; PDF p. 57) |
| **Label consistency (`G-U2a-06`)** | `[B₁]^ℓ, [B₂]^ℓ ∈ blocks(S) ⇒ B₁ = B₂` (weaker than Chapter 1 unique labelling, `BKL-028`) | Label-indexed lookup "`[B]^ℓ ∈ blocks(S⋆)`" becomes multi-valued / ambiguous (`G-U2a-16`) | [PPA §2.1, p. 39] (book p. 39; PDF p. 58) |
| **Isolated entries (`G-U2a-05`)** | `∀ℓ ∈ Lab : (ℓ, init(S⋆)) ∉ flow(S⋆)` (holds unless `S⋆` starts with `while`) | Table 2.1/2.2 `if ℓ = init(S⋆)` overwrites back-edges entering loop header `init(S⋆)` (`G-U2a-07`, `Exercise 2.6`) | [PPA Example 2.3, p. 39] (book p. 39; PDF p. 58) |
| **Isolated exits (`G-U2a-05`)** | `∀ℓ₁ ∈ final(S⋆) ∀ℓ₂ ∈ Lab : (ℓ₁, ℓ₂) ∉ flow(S⋆)` (fails whenever `S⋆` ends with `while`, e.g. `power`) | Table 2.3/2.4 `if ℓ ∈ final(S⋆)` overwrites edges leaving loop header (`G-U2a-07`, `F-U2a-09`) | [PPA Example 2.3, p. 39] (book p. 39; PDF p. 58) |
| **Reachability (`G-U2b-34`)** | `∀ℓ ∈ Lab⋆ : path∘(ℓ) ≠ ∅` for `(flow(S⋆), {init(S⋆)})` and `(flow^R(S⋆), final(S⋆))` (`Exercise 2.13`) | Fails if `Lab⋆` contains unused labels or dead uncalled procedures (`F-U2b-12`) | [PPA Exercise 2.13, p. 137] (book p. 137; PDF p. 156) |

Multi-statement basic blocks `[x₁ := a₁; ···; x_n := a_n; B]^ℓ` (`Exercise 2.5`) compose transfer functions
sequentially per block (`Lemma 2.25`) while preserving the identical graph machinery
[PPA Exercise 2.5, p. 136] (book p. 136; PDF p. 155). Low-level IRs without AST flow graphs require
intraprocedural CFG / structural analysis first (`[U2b:CR-f]`)
[PPA Chapter 2 Concluding Remarks, p. 131] (book p. 131; PDF p. 150).

## 2. The Four Classical Bit-Vector Analyses (`§§2.1.1–2.1.4`, `Figure 2.6`)

Every §2.1 analysis computes `Entry(ℓ), Exit(ℓ)` pairs via `(out(ℓ) \ kill(B^ℓ)) ∪ gen(B^ℓ)` under one of four
combinations of direction (`→` = `flow`, `←` = `flow^R`), confluence (`⋂` = must, `⋃` = may), and fixed-point
extremum (`↑` = largest under `⊆`, `↓` = smallest under `⊆`) [PPA Figure 2.6, p. 70] (book p. 70; PDF p. 89):

| Property | Available Expressions (`AE`, Table 2.1) | Reaching Definitions (`RD`, Table 2.2) | Very Busy Expressions (`VB`, Table 2.3) | Live Variables (`LV`, Table 2.4) |
| :--- | :--- | :--- | :--- | :--- |
| **Type (`G-U2a-21`)** | `(⋂, →, ↑)` forward must | `(⋃, →, ↓)` forward may | `(⋂, ←, ↑)` backward must | `(⋃, ←, ↓)` backward may |
| **Carrier `L`** | `𝒫(AExp⋆)`, order `⊇`, join `∩`, `⊥ = AExp⋆` | `𝒫(Var⋆ × Lab⋆^?)`, order `⊆`, join `∪`, `⊥ = ∅` | `𝒫(AExp⋆)`, order `⊇`, join `∩`, `⊥ = AExp⋆` | `𝒫(Var⋆)`, order `⊆`, join `∪`, `⊥ = ∅` |
| **Boundary `(E, ι)`** | `{init(S⋆)}`, `ι = ∅` (`= ⊤_L`) | `{init(S⋆)}`, `ι = {(x, ?) \| x ∈ FV(S⋆)}` (`G-U2a-11`) | `final(S⋆)`, `ι = ∅` (`= ⊤_L`) | `final(S⋆)`, `ι = ∅` (`= ⊥_L`; `G-U2a-12`) |
| **`kill([x:=a]^ℓ)`** | `{a' ∈ AExp⋆ \| x ∈ FV(a')}` | `{(x, ?)} ∪ {(x, ℓ') \| B^{ℓ'} assigns x}` | `{a' ∈ AExp⋆ \| x ∈ FV(a')}` | `{x}` |
| **`gen([x:=a]^ℓ)`** | `{a' ∈ AExp(a) \| x ∉ FV(a')}` (`G-U2a-08`) | `{(x, ℓ)}` | `AExp(a)` (no `x ∉ FV(a')` filter! `G-U2a-08`) | `FV(a)` |
| **`gen([b]^ℓ)`** | `AExp(b)` (`kill = ∅`) | `∅` (`kill = ∅`) | `AExp(b)` (`kill = ∅`) | `FV(b)` (`kill = ∅`) |
| **Primary use** | Common subexpression elimination [external] | Def-use chains (`§2.1.5`), constant folding (`§1.8`) | Code-size expression hoisting (`Example 2.8`) | Dead code elimination (`Example 2.10`) |

Coordinates: [PPA Table 2.1, p. 40] (book p. 40; PDF p. 59), [PPA Table 2.2, p. 44] (book p. 44; PDF p. 63),
[PPA Table 2.3, p. 47] (book p. 47; PDF p. 66), [PPA Table 2.4, p. 50] (book p. 50; PDF p. 69).

Critical side conditions and semantic traps (`BKL-030`, `BKL-035`, `BKL-006`):
1. **Must vs May fixed points (`G-U2a-09`, `G-U2a-10`)**: Self-referential loops such as `AE_entry(ℓ') = {x+y} ∩ AE_entry(ℓ')`
   (`Figure 2.2`) admit spurious small solutions (`∅`), so must-analyses (`⋂`) require the **largest** solution under
   `⊆` (least fixed point under `⊇`, empty intersection `⋂∅ = AExp⋆`); conversely, `LV_exit(ℓ) = LV_exit(ℓ) ∪ {x}`
   admits spurious supersets, so may-analyses (`⋃`) require the **smallest** solution under `⊆` (`⋃∅ = ∅`).
2. **Asymmetry of `gen_AE` vs `gen_VB` (`G-U2a-08`)**: In `[a:=a+1]^4` (`Example 2.5`), evaluation happens *before*
   update, so `a+1` is very busy at entry (`gen_VB([x:=a]^ℓ) = AExp(a)`) yet *not* available after exit
   (`gen_AE([x:=a]^ℓ) = {a' ∈ AExp(a) | x ∉ FV(a')}`).
3. **Uninitialised sentinel `?` (`G-U2a-11`)**: Chapter 2 separates `? ∉ Lab⋆` into `Lab⋆^? = Lab⋆ ∪ {?}` (unlike
   Chapter 1, `BKL-035`). Setting `RD_entry(init(S⋆)) = ∅` instead of `{(x, ?) | x ∈ FV(S⋆)}` is unsound whenever
   a variable can be read before its first assignment (`§2.1.2`).
4. **Live exit boundary & `[external: zeroization]` (`G-U2a-12`, `BKL-006`)**: Table 2.4 assumes all variables are dead at exit
   (`ι = ∅`); when outputs or escaped secrets are observed, final variables must be included in `ι` (`Example 2.11`),
   or dead-store elimination removes trailing secret-`[external: zeroization]` stores (`BKL-006`).
5. **Extensions (`Exercises 2.3–2.4`)**: *Expression `a` available in variable `x`* (`Exercise 2.3`) adds `kill` on
   writes to `x` or `FV(a)` [PPA Exercise 2.3, p. 135] (book p. 135; PDF p. 154). *Faint variables* (`Exercise 2.4`)
   avoid marking `x` live at exit of `[x:=1]^1` before `[x:=x-1]^2; [x:=2]^3` by branching `f_ℓ(l)` on `x ∈ l`
   [PPA Exercise 2.4, p. 136] (book p. 136; PDF p. 155).

## 3. Derived Information: `ud`/`du` Chains and Sound Slicing (`§2.1.5`, `Mini Project 2.1`)

Non-constructive path predicates define definition-clear paths (`clear`) and symmetric chain relations
[PPA §2.1.5, p. 52] (book p. 52; PDF p. 71) [PPA §2.1.5, p. 53] (book p. 53; PDF p. 72):

```
use(x, ℓ)     = (∃B : [B]^ℓ ∈ blocks(S⋆) ∧ x ∈ gen_LV([B]^ℓ))
def(x, ℓ)     = (∃B : [B]^ℓ ∈ blocks(S⋆) ∧ x ∈ kill_LV([B]^ℓ))
clear(x, ℓ, ℓ') = ∃ℓ₁..ℓ_n (n>0): ℓ₁=ℓ ∧ ℓ_n=ℓ' ∧ (∀i<n: (ℓ_i, ℓ_{i+1}) ∈ flow(S⋆) ∧ ¬def(x, ℓ_i)) ∧ use(x, ℓ_n)

ud(x, ℓ') = {ℓ | def(x, ℓ) ∧ ∃ℓ'' : (ℓ, ℓ'') ∈ flow(S⋆) ∧ clear(x, ℓ'', ℓ')} ∪ {? | clear(x, init(S⋆), ℓ')}
du(x, ℓ)  = {ℓ' | ℓ ∈ ud(x, ℓ')}
UD(x, ℓ)  = {ℓ' | (x, ℓ') ∈ RD_entry(ℓ)}   if x ∈ gen_LV(B^ℓ);   ∅  otherwise
```

- **Self-redefinition edge (`G-U2a-13`)**: Although prose on p. 52 says none of `ℓ₁..ℓ_n` assigns `x`, the formal
  quantifier checks `¬def(x, ℓ_i)` only for `i ∈ {1..n-1}`, allowing `[x := x+1]^{ℓ_n}` to both use and redefine `x`.
- **Signature erratum (`G-U2a-14`, `F-U2a-05`)**: Pages 53–54 type `ud, du, UD, DU` with `Lab⋆` instead of `Lab⋆^?`,
  even though `ud(z, 3) = {?}` and `du(z, ?) = {3}` (`Example 2.12`)
  [PPA Example 2.12, p. 53] (book p. 53; PDF p. 72) [PPA §2.1.5, p. 54] (book p. 54; PDF p. 73).
- **Safe chain-based Constant Folding (`G-U2b-29`, `Figure 2.23`)**: Following a `du`-chain from `[x := n]^ℓ` to use
  `ℓ'` is sound **iff** checking `ud(x, ℓ')` confirms *every* other definition of `x` reaching `ℓ'` also assigns
  the exact constant `n` (`Mini Project 2.1`) [PPA Mini Project 2.1, p. 132] (book p. 132; PDF p. 151)
  [PPA Figure 2.23, p. 132] (book p. 132; PDF p. 151). Static Single Assignment (`SSA`, `x := ϕ(x₁, ..., x_n)`,
  `[U2b:CR-d]`) materialises `du`-chains syntactically so every variable has at most one definition
  [PPA Chapter 2 Concluding Remarks, p. 130] (book p. 130; PDF p. 149).

## 4. Monotone & Distributive Frameworks and Constant Propagation (`§§2.3–2.3.3`)

Unifying the four-corner square (`(⋂, →, ↑)`, `(⋃, →, ↓)`, `(⋂, ←, ↑)`, `(⋃, ←, ↓)`) under abstract precision
order `⊑` (so `⊥_L` is unreached information and `⊔` merges paths) replaces the isolated-boundary case split
with an **unconditional** join equation (`G-U2a-22`) [PPA §2.3, p. 66] (book p. 66; PDF p. 85):

```
Analysis∘(ℓ) = ⨆{Analysis•(ℓ') | (ℓ', ℓ) ∈ F} ⊔ ι^ℓ_E      where ι^ℓ_E = ι if ℓ ∈ E; ⊥ if ℓ ∉ E
Analysis•(ℓ) = f_ℓ(Analysis∘(ℓ))
```

1. **Monotone Framework `(L, 𝓕)` (`§2.3.1`, `G-U2a-23`, `G-U2a-24`)**: `L` is a complete lattice (`⨆`)
   satisfying the **Ascending Chain Condition (ACC)** — equivalently a join semi-lattice `(L, ⊔)` with unit
   `⊥` and ACC (`Lemma A.8`), or dual DCC/`⨅` [PPA §2.3.1, p. 68] (book p. 68; PDF p. 87). `𝓕` is a set of
   monotone functions `L → L` containing `id` and closed under composition `∘` (`𝓕` need not itself be a
   lattice) [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88). An **instance** `Analysis = (L, 𝓕, F, E, ι, f_·)` fixes
   finite flow relation `F`, finite extremal labels `E`, extremal value `ι ∈ L` (which obeys no universal
   `⊤_L`/`⊥_L` rule, `G-U2a-26` [PPA §2.3.2, p. 70] (book p. 70; PDF p. 89)), and `f_· : Lab⋆ → 𝓕`, inducing
   equations `Analysis^=` and constraints `Analysis^⊑` (`G-U2a-24`). §2.3 excludes procedures (`§2.5`).
2. **Framework Expressiveness Hierarchy (`Bit Vector ⊂ Distributive ⊂ Monotone`)**:
   - **Distributive Framework (`G-U2a-25`, `BKL-022`)**: Every `f ∈ 𝓕` satisfies `f(l₁ ⊔ l₂) = f(l₁) ⊔ f(l₂)`
     (binary join preservation, called *additive* in Appendix A; strictness `f(⊥) = ⊥` is **not** demanded)
     [PPA §2.3.1, p. 69] (book p. 69; PDF p. 88).
   - **Bit Vector Framework (`Lemma 2.25`, `Exercise 2.9`, `G-U2a-27`, `G-U2b-31`)**: Finite `D`,
     `L = (𝒫(D), ⊑)` with `⊑ ∈ {⊆, ⊇}`, and `f(Y) = (Y ∩ Y_f^1) ∪ Y_f^2` (written `(l \ l_k) ∪ l_g` in
     `Figure 2.6`, composing via `l_k'' = l_k' ∪ l_k` and `l_g'' = (l_g' \ l_k) ∪ l_g` — note `f'` runs *first*
     in `f ∘ f'`!) [PPA Lemma 2.25, p. 71] (book p. 71; PDF p. 90). Every Bit Vector Framework is Distributive,
     whereas **not every Distributive Framework is Bit Vector** (`G-U2b-31`): copy/faint propagation
     (`[x:=y]^ℓ`, `Exercise 2.4`) satisfies `f(∅) = ∅` (forcing `Y_f^2 = ∅` and `f({x}) ⊆ {x}` in any bit vector
     form) yet maps `f({x}) = {y}` (`[derived]`) [PPA Exercise 2.9, p. 137] (book p. 137; PDF p. 156).
3. **Constant Propagation (`§2.3.3`, `Table 2.7`, `Lemma 2.27`, `G-U2a-28`, `BKL-001`)**:
   - Lattice `State^_CP = ((Var⋆ → Z^⊤)_⊥, ⊑, ⊔, ⊓, ⊥, λx.⊤)` where `Z^⊤ = Z ∪ {⊤}` is flat (`z ⊑ ⊤`),
     finite height `2 + |Var⋆|` `[derived]` satisfies ACC despite infinite `Z` (`Exercise 2.8`), `ι_CP = λx.⊤`,
     and `𝒜_CP`, `op^_a`, `f_ℓ^CP` are strict in unreachable `⊥` (`z₁ op^_a z₂ = ⊥` if either is `⊥`, `⊤` if
     non-constant) [PPA §2.3.3, p. 72] (book p. 72; PDF p. 91) [PPA Table 2.7, p. 73] (book p. 73; PDF p. 92).
   - **Non-distributivity (`Lemma 2.27`, `Exercise 2.10`)**: `𝓕_CP` contains all monotone functions;
     `[y := x * x]^ℓ` with `σ̂₁(x)=1, σ̂₂(x)=-1` gives `f_ℓ^CP(σ̂₁ ⊔ σ̂₂)(y) = ⊤ ≠ 1 = (f_ℓ^CP(σ̂₁) ⊔ f_ℓ^CP(σ̂₂))(y)`
     [PPA Lemma 2.27, p. 74] (book p. 74; PDF p. 93), and `(if [···]^1 then [x:=-1]^2; [y:=1]^3 else [x:=1]^4; [y:=-1]^5); [z:=x*y]^6`
     separates `MFP•(6)(z) = ⊤` from `MOP•(6)(z) = -1` (`Exercise 2.10`)
     [PPA Exercise 2.10, p. 137] (book p. 137; PDF p. 156).
   - **Branch splitting (`Exercise 2.11`)**: Replacing `[b]^ℓ` by two-label `[b]^{ℓ₁,ℓ₂}` (`ℓ₁` true, `ℓ₂` false)
     lets forward frameworks propagate guard facts into `S₁, S₂` without changing framework power
     [PPA Exercise 2.11, p. 137] (book p. 137; PDF p. 156).

## 5. Solving Equations (`MFP`) vs Path Specification (`MOP`) (`§§2.4.1–2.4.2`)

Historical naming warning (`G-U2a-29`, `G-U2b-33`): literature using `⊓`/`⊇` calls these **Maximal Fixed Point
(`MFP`)** and **Meet Over all Paths (`MOP`)**; in PPA's `(L, ⊑)` convention, `MFP` computes the **least**
fixed point and `MOP` computes the **join (`⨆`)** over paths [PPA §2.4.1, p. 74] (book p. 74; PDF p. 93)
[PPA Chapter 2 Concluding Remarks, p. 128] (book p. 128; PDF p. 147).

- **Worklist Algorithm (`Table 2.8`, `Example 2.28`, `Table 2.9`, `G-U2a-30`)**:
  1. Push every `(ℓ, ℓ') ∈ F` onto LIFO stack `W`; set `Analysis[ℓ] := ι` for `ℓ ∈ E`, `⊥_L` otherwise.
  2. Pop `(ℓ, ℓ')`; if **`f_ℓ(Analysis[ℓ]) ⋢ Analysis[ℓ']`**, update **`Analysis[ℓ'] := Analysis[ℓ'] ⊔ f_ℓ(Analysis[ℓ])`**
     and `cons` all `(ℓ', ℓ'') ∈ F` onto `W` (no deduplication in Table 2.8; note typo `ℓ' = snd(head(W))` on p. 75).
  3. Output `MFP∘(ℓ) := Analysis[ℓ]`, `MFP•(ℓ) := f_ℓ(Analysis[ℓ])`
     [PPA Table 2.8, p. 75] (book p. 75; PDF p. 94) [PPA Table 2.9, p. 76] (book p. 76; PDF p. 95).
  Never replace `⋢` by `≠` (re-enqueues subsumed edges without progress) or `⊔` by overwrite (breaks loop
  monotonicity) [PPA Lemma 2.29, p. 76] (book p. 76; PDF p. 95).
- **Termination & Complexity (`Lemma 2.29`, `Example 2.30`, `Exercise 2.12`, `G-U2a-31`)**: Termination holds
  under ACC + finite `F, E` (`Lemma 2.29`, printing `MFP∘[ℓ]` in part (iii))
  [PPA Lemma 2.29, p. 77] (book p. 77; PDF p. 96). The **`O(e · h)`** basic-operations bound requires
  *finite height* `h ≥ 1`, `e ≥ b ≥ 1` (`|F| ≤ e`, `|Lab⋆| ≤ b`), and `O(outdeg)` adjacency lists. Notice
  `Example 2.30` writes `h ≤ v · b` (forgetting `v` uninitialised pairs `(x, ?)`) and `O(b²)` (`e ≤ 2b`,
  label consistency giving `h ≤ b + v` `= O(b)` only when `v = O(b)`) [PPA Example 2.30, p. 78] (book p. 78; PDF p. 97).
- **MOP Path Formulation (`§2.4.2`, `G-U2a-32`)**: For `ℓ⃗ = [ℓ₁, ···, ℓ_n]`, `f_ℓ⃗ = f_{ℓ_n} ∘ ··· ∘ f_{ℓ₁} ∘ id`
  (`f_[ ] = id`), `path∘(ℓ)` excludes `ℓ` (`[ ] ∈ path∘(ℓ)` when `ℓ ∈ E`), `path•(ℓ)` includes `ℓ`, and
  `MOP∘(ℓ) = ⨆{f_ℓ⃗(ι) | ℓ⃗ ∈ path∘(ℓ)}` [PPA §2.4.2, p. 79] (book p. 79; PDF p. 98).
- **MPCP Undecidability (`Lemma 2.31`, `G-U2a-33`)**: `MOP` for Constant Propagation is undecidable by
  reduction from the Modified Post Correspondence Problem (`[76]`, `p. 79` misprints `v_{i_n}` for `v_{i_m}`),
  even when arithmetic allows the needed encoding and `MFP` always terminates
  [PPA Lemma 2.31, p. 79] (book p. 79; PDF p. 98) [PPA Lemma 2.31, p. 80] (book p. 80; PDF p. 99).
- **Safe Approximation & Coincidence (`Lemma 2.32`, `G-U2a-34`, `G-U2a-35`)**:
  `MFP∘(ℓ) ⊒ MOP∘(ℓ)` and `MFP•(ℓ) ⊒ MOP•(ℓ)` (`MFP ⊆ MOP` for `⋂`; `MFP ⊇ MOP` for `⋃`). Moreover,
  **`MFP∘ = MOP∘` and `MFP• = MOP•`** whenever **(1) `(L, 𝓕)` is a Distributive Framework AND
  (2) `∀ℓ : path∘(ℓ) ≠ ∅`** (both hypotheses are needed because Lemma A.9 applies to non-empty sets `Y ≠ ∅`;
  note p. 80 misprints `(L, 𝓕, F, B, ι, f_·)` with `B` for `E`)
  [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99). General MOP formulations reduce to MFP over enriched
  powerset lattices such as `𝒫(L)` (`G-U2a-35`) [PPA §2.4.2, p. 82] (book p. 82; PDF p. 101).

## 6. Section 4.5 / Disjunctive Lifting Pointers and Unit 2a Backlog

- **Cross-chapter pointers (`§2.3.3`, `§2.4.2`, `U4`)**: Constant Propagation (`§2.3.3`) defines transfer functions directly on the non-relational lattice `State^_CP` over `Var⋆ → Z` and defers its formal semantic correctness proof via Galois connections to `§4.5` [PPA §2.3.3, p. 74] (book p. 74; PDF p. 93) (foreshadowing canonical `U6` once Chapter 4 `§4.3–§4.5` is integrated). Separately, `§2.4.2` notes that general `MOP` over non-distributive `L` can be reformulated as `MFP` over the lifted powerset space `𝒫(L)`, which preserves ACC whenever `L` is finite [PPA §2.4.2, p. 82] (book p. 82; PDF p. 101) (`[derived]`/`[external: disjunctive completion]` analogy; not a `§1.5` adjunction claim), while `Table 2.8` specialises `Table 1.5` Chaotic Iteration (`U2` deferred to Chapter 6) and its graph-observer cousin `Table 3.7` is detailed in [constraint-generation-and-cubic-solver.md](../../ppa-control-flow-and-constraints/references/constraint-generation-and-cubic-solver.md) [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196). For canonical unification **`U4`**, higher-order coupled `CFA + DFA` (`§3.5.2`) lifts Chapter 2's monotone structure `(L, ℱ, ι., f.)` without static `flow` `F` or `E` in [polyvariant-kcfa-cpa-and-dfa.md](../../ppa-control-flow-and-constraints/references/polyvariant-kcfa-cpa-and-dfa.md) [PPA §3.5.2, p. 186] (book p. 186; PDF p. 204).
- **Non-blocking Unit 2a Backlog (`ARCHITECTURE.md` §6.4)**:
  - `BKL-001` (`CP` `Z^⊤` overflow / bounded integers [external]); `BKL-006` (DCE wiping observable secret zeroization, `§2.1 p. 49`);
  - `BKL-036` (`ud/du/UD/DU` codomain/domain must use `Lab⋆^?`, `§2.1.5 pp. 53–54`);
  - `BKL-039` (`Example 2.30 p. 78` omits `v` uninitialised `(x, ?)` pairs in `h <= v*b`);
  - `BKL-040` (`Lemma 2.32 p. 80` prints `B` for `E` plus Table 2.7/2.8 and `§2.3` typographical bundle).
