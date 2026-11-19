<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Chapter 2 L1 reference for semantic correctness proofs (§2.2, Mini Project 2.2) and interprocedural DFA (§2.5). -->

# Interprocedural Analysis, Context Mechanisms, and Semantic Correctness

Scope: Chapter 2, §§2.2–2.2.2, §2.5 (`§§2.5.1–2.5.6`), Concluding Remarks (`CR-b, d, e, f`),
Mini Project 2.2 (`Table 2.10`), and Exercises `2.7, 2.14–2.20` —
[PPA §2.2, p. 54] (book p. 54; PDF p. 73) to [PPA §2.2.2, p. 65] (book p. 65; PDF p. 84) and
[PPA §2.5, p. 82] (book p. 82; PDF p. 101) to [PPA §2.5.6, p. 103] (book p. 103; PDF p. 122).
Ground truth: `corpus/shards/RAW_SHARD_02a_intraproc_dfa.md` and `corpus/shards/RAW_SHARD_02b_interproc_shape.md`.
Intraprocedural DFA/frameworks live in [intraprocedural-analyses-and-frameworks.md](./intraprocedural-analyses-and-frameworks.md);
heap pointer/shape analysis lives in [shape-analysis.md](./shape-analysis.md); shared order, induction, and Chapter 1 formulations live in
[appendix-a-posets-lattices-fixed-points.md](../../ppa-program-analysis/references/appendix-a-posets-lattices-fixed-points.md),
[appendix-b-induction-and-coinduction.md](../../ppa-program-analysis/references/appendix-b-induction-and-coinduction.md), and
[chapter-1-five-formulations.md](../../ppa-program-analysis/references/chapter-1-five-formulations.md).

## 1. Semantic Correctness Proofs (`§2.2`, `Mini Project 2.2`)

PPA establishes correctness against a **small-step Structural Operational Semantics (SOS)** (`⟨S, σ⟩ → ⟨S', σ'⟩`
or terminal `⟨S, σ⟩ → σ'`) rather than big-step semantics, because small-step SOS exposes intermediate
program states and models diverging loops explicitly as infinite derivation sequences (`Remark.`, `G-U2a-20`,
`BKL-004`) [PPA §2.2.1, p. 54] (book p. 54; PDF p. 73) [PPA §2.2.2, p. 65] (book p. 65; PDF p. 84).

- **Error-free `WHILE` SOS (`Tables 2.5–2.6`, `G-U2a-15`, `BKL-001`, `BKL-037`)**: States `σ ∈ State = Var → Z` are
  total; expressions assume no runtime faults (division by `0` yields an integer; `Table 2.5` omits explicit
  `true`/`false` literal clauses, `F-U2a-06`, `BKL-037`) [PPA Table 2.5, p. 55] (book p. 55; PDF p. 74)
  [PPA Table 2.6, p. 56] (book p. 56; PDF p. 75).
- **Structural Monotonicity (`Lemma 2.14`, `G-U2a-16`, `G-U2a-17`)**: Labels are passive (`Example 2.13`).
  If `⟨S, σ⟩ → σ'` then `final(S) = {init(S)}` (`i`); if `⟨S, σ⟩ → ⟨S', σ'⟩` then `final(S) ⊇ final(S')`
  (`ii`), `flow(S) ⊇ flow(S')` (`iii`, proof heading misprints `[wh₂]` for loop-unrolling `[wh₁]`), and
  `blocks(S) ⊇ blocks(S')` while preserving **label consistency** (`iv`) — whereas unique labelling fails
  under `[wh₁]` unrolling (`BKL-028`) [PPA Lemma 2.14, p. 58] (book p. 58; PDF p. 77)
  [PPA Lemma 2.14, p. 59] (book p. 59; PDF p. 78).
- **Why Constraints `LV^⊆` Replace Equations `LV^=` (`Lemma 2.15`, `Exercise 2.7`, `G-U2a-18`, `G-U2b-32`)**:
  A single solution `live` of `LV^=(S)` fails to solve reduced continuation `S'` after `[if]`/`[seq]`; relaxing
  `=` to reductive constraint inclusions `LV^⊆(S)` (`Red(F) = {x | F(x) ⊑ x}` [PPA §A.4, p. 402] (book p. 402; PDF p. 418)) keeps the identical least solution via Tarski's Theorem
  (`Lemma 2.15`) [PPA Lemma 2.15, p. 60] (book p. 60; PDF p. 79), forms a **Moore family** under `⋂`
  (whereas `{live | live ⊨ LV^=(S)}` fails `⋂∅ = ⊤` when `Var⋆ ≠ ∅`, `Exercise 2.7`, `G-U2b-32`)
  [PPA Exercise 2.7, p. 136] (book p. 136; PDF p. 155), and survives transitions (`Lemmas 2.16, 2.18`,
  `Corollary 2.17`, `Figure 2.4`) [PPA Lemma 2.16, p. 61] (book p. 61; PDF p. 80).
- **Isolated-Exits Soundness Gap (`G-U2a-19`, `F-U2a-09`, `BKL-038`)**: Because p. 60 defines `LV_exit(ℓ) ⊇ ∅` when
  `ℓ ∈ final(S⋆)` (`otherwise` the `flow^R` union), `Lemma 2.18`, `Lemma 2.20`, `Theorem 2.21`, and
  `Corollary 2.22` break on trailing `while` loops (`final(S) = {ℓ}`) and sub-statement `[seq₁]`/`[seq₂]`
  steps unless `§2.3`'s unconditional union `LV_exit(ℓ) ⊇ ⋃{LV_entry(ℓ') | (ℓ', ℓ) ∈ flow^R(S)} ⊔ ι^ℓ_E`
  is used (`BKL-038`; `BKL-017` covers infinite-loop channel limits) [PPA §2.2.2, p. 60] (book p. 60; PDF p. 79)
  [PPA Lemma 2.18, p. 61] (book p. 61; PDF p. 80).
- **2-Run Lockstep Equivalence (`Theorem 2.21`, `Corollary 2.22`, `Figures 2.4–2.5`, `G-U2a-20`)**: With
  `σ₁ ∼_V σ₂ iff ∀x ∈ V : σ₁(x) = σ₂(x)` (`Example 2.19`, `Lemma 2.20`), any step from `σ₁ ∼_{N(init(S))} σ₂`
  reaches matching `S'` (preserving `σ₁' ∼_{N(init(S'))} σ₂'`) or terminal states (`σ₁' ∼_{X(ℓ)} σ₂'` *for some*
  `ℓ ∈ final(S)`) [PPA Theorem 2.21, p. 63] (book p. 63; PDF p. 82)
  [PPA Corollary 2.22, p. 64] (book p. 64; PDF p. 83). Treating `N(ℓ)` as public (`Low`) makes `∼_V`
  termination-and-timing lockstep non-interference (`N(ℓ) ⊇ FV(b)` forbids secret branches) `[external]`.
- **Reaching Definitions Trace Proof (`Table 2.10`, `Mini Project 2.2`, `G-U2b-30`)**: Instrumented SOS
  appends `(x, ℓ)` to trace `tr` on `[ass]` (`tr : (x, ℓ)`), starting from `tr⋆ = ((x₁, ?), ···, (x_n, ?))`,
  and checks `tr ∼ Y iff ∀x ∈ DOM(tr) : (x, SRD(tr)(x)) ∈ Y` (`§1.5`). Requires three repairs over the
  printed text: `Trace = (Var × Lab^?)*` (include `?`), `Y ⊆ Var⋆ × Lab⋆^?`, and unconditional `RD^⊆` without
  needing isolated entries [PPA Table 2.10, p. 133] (book p. 133; PDF p. 152)
  [PPA Mini Project 2.2, p. 134] (book p. 134; PDF p. 153).

## 2. Procedure Syntax, Call/Return Flows, and Operational Semantics (`§2.5`, `§2.5.1`)

`WHILE` extends to `P⋆ = begin D⋆ S⋆ end` with uniquely labelled, statically scoped, mutually recursive
declarations `proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}` and calls `[call p(a, z)]^{ℓ_c}_{ℓ_r}`
(`Example 2.33`, Fibonacci) [PPA §2.5, p. 82] (book p. 82; PDF p. 101)
[PPA Example 2.33, p. 83] (book p. 83; PDF p. 102):

```
init([call p(a,z)]^{ℓ_c}_{ℓ_r}) = ℓ_c,   final(...) = {ℓ_r},   flow(...) = {(ℓ_c; ℓ_n), (ℓ_x; ℓ_r)}
inter-flow⋆ = {(ℓ_c, ℓ_n, ℓ_x, ℓ_r) | P⋆ contains [call p(a,z)]^{ℓ_c}_{ℓ_r} and proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}}
```

- **Matched call/return pairing (`G-U2b-01`, `Example 2.34`, `Figure 2.7`)**: Separate `(ℓ_c^i; ℓ_n)` and
  `(ℓ_x; ℓ_r^i)` pairs in `flow⋆` create spurious cross-over tuples `(ℓ_c^i, ℓ_n, ℓ_x, ℓ_r^j)` (`i ≠ j`);
  only 4-tuple relation `IF = inter-flow⋆` binds each call to its return
  [PPA §2.5, p. 84] (book p. 84; PDF p. 103) [PPA Figure 2.7, p. 85] (book p. 85; PDF p. 104).
- **Static dispatch & backward orientation (`G-U2b-02`, `G-U2b-03`)**: `flow` assumes calls name a fixed
  procedure constant `p` (procedure-valued variables induce dynamic dispatch, deferred to Chapter 3, `BKL-008`);
  backward analysis takes `F = flow⋆^R, E = final⋆, IF = inter-flow⋆^R` without explicitly defining `^R` on
  semicolon flows or 4-tuples (`(ℓ_r, ℓ_x, ℓ_n, ℓ_c)` `[derived]`)
  [PPA §2.5, p. 84] (book p. 84; PDF p. 103) [PPA §2.5, p. 85] (book p. 85; PDF p. 104).
- **Two-Level `Env`/`Store` SOS & `bind` (`§2.5.1`, `G-U2b-04`, `G-U2b-05`, `BKL-024`)**: With `ρ ∈ Var⋆ → Loc`
  and `ς ∈ Loc →_fin Z` (`σ = ς ∘ ρ` total: `ran(ρ) ⊆ dom(ς)`), `[call]` runs callee body `S` under
  top-level `ρ⋆[x ↦ ξ₁, y ↦ ξ₂]` (enforcing static lexical scoping) with `ξ₁ ↦ 𝒜⟦a⟧(ς ∘ ρ)` and `ξ₂`
  holding an **arbitrary `v ∈ Z`** inside `bind ρ⋆[...] in S then z := y`:
  1. Forward call transfers (`Example 2.38`) must set `res y` to unconstrained `⊤` (`{-, 0, +}`), never `0`
     or caller's `y` (`G-U2b-04`), modelling uninitialised out-parameter leaks (`[derived]`).
  2. Intermediate `bind` configurations and unlabelled `z := y` / `x := a` (`p. 86–87`) require bespoke
     correctness handling in Chapter 3 (`Remark.`, `G-U2b-05`) [PPA §2.5.1, p. 86] (book p. 86; PDF p. 105)
     [PPA §2.5.1, p. 87] (book p. 87; PDF p. 106).

## 3. Valid Paths (`MVP`) and Embellished Monotone Frameworks (`§§2.5.2–2.5.3`)

Treating `(ℓ_c; ℓ_n)` and `(ℓ_x; ℓ_r)` as ordinary `goto` edges with identity call/return functions (`§2.5.2`)
is sound yet admits unrealizable paths such as `[9, 1, 2, 4, 1, 2, 3, 8, 10]` in `Figure 2.7`
[PPA §2.5.2, p. 88] (book p. 88; PDF p. 107). Restricting to balanced calls generates two CFG grammars:

```
CP_{ℓ₁,ℓ₂} ⟶ ℓ₁                           whenever ℓ₁ = ℓ₂
CP_{ℓ₁,ℓ₃} ⟶ ℓ₁, CP_{ℓ₂,ℓ₃}                whenever (ℓ₁, ℓ₂) ∈ F
CP_{ℓ_c,ℓ} ⟶ ℓ_c, CP_{ℓ_n,ℓ_x}, CP_{ℓ_r,ℓ} whenever (ℓ_c, ℓ_n, ℓ_x, ℓ_r) ∈ IF

VP⋆        ⟶ VP_{ℓ₁,ℓ₂}                    whenever ℓ₁ ∈ E and ℓ₂ ∈ Lab⋆
VP_{ℓ₁,ℓ₂} ⟶ ℓ₁                            whenever ℓ₁ = ℓ₂
VP_{ℓ₁,ℓ₃} ⟶ ℓ₁, VP_{ℓ₂,ℓ₃}                 whenever (ℓ₁, ℓ₂) ∈ F
VP_{ℓ_c,ℓ} ⟶ ℓ_c, CP_{ℓ_n,ℓ_x}, VP_{ℓ_r,ℓ}  whenever (ℓ_c, ℓ_n, ℓ_x, ℓ_r) ∈ IF
VP_{ℓ_c,ℓ} ⟶ ℓ_c, VP_{ℓ_n,ℓ}                whenever (ℓ_c, ℓ_n, ℓ_x, ℓ_r) ∈ IF
MVP∘(ℓ)    = ⨆{f_ℓ⃗(ι) | ℓ⃗ ∈ vpath∘(ℓ)}
```

- **Pending calls & undecidability (`G-U2b-06`, `G-U2b-07`, `Example 2.35`)**: `VP⋆` includes prefixes with
  entered-and-not-yet-exited calls (`ℓ_c, VP_{ℓ_n,ℓ}`) to cover points inside recursive calls and
  non-terminating executions [PPA Example 2.35, p. 89] (book p. 89; PDF p. 108)
  [PPA §2.5.2, p. 90] (book p. 90; PDF p. 109). Thus `MVP∘(ℓ) ⊑ MOP∘(ℓ)`, yet `MVP` may be undecidable
  even for finite-height `L` (`§2.5.3`) [PPA §2.5.3, p. 90] (book p. 90; PDF p. 109).
- **Embellished Framework `(L̂, 𝓕̂, F, E, ι̂, f̂_·)` (`§2.5.3`, `Example 2.36`, `Figures 2.8–2.10`, `G-U2b-08`, `G-U2b-09`)**:
  Lift property space to `L̂ = Δ → L` (isomorphic to `𝒫(Δ × D)` when `L = 𝒫(D)`), pointwise intraprocedural
  transfers `f̂_ℓ(l̂)(δ) = f_ℓ(l̂(δ))`, identity entry/exit `f̂_{ℓ_n} = f̂_{ℓ_x} = id`, and at each call
  `(ℓ_c, ℓ_n, ℓ_x, ℓ_r) ∈ IF`:
  - `A∘(ℓ) = ⨆{A•(ℓ') | (ℓ', ℓ) ∈ F or (ℓ'; ℓ) ∈ F} ⊔ ι̂^ℓ_E` for *all* labels (`ℓ_c, ℓ_r` included);
  - **`A•(ℓ_c) = f̂¹_{ℓ_c}(A∘(ℓ_c))`** (maps caller context/formals to callee entry);
  - **`A•(ℓ_r) = f̂²_{ℓ_c,ℓ_r}(A∘(ℓ_c), A∘(ℓ_r))`** (*binary* return transfer taking **both** pre-call
    `A∘(ℓ_c)` and callee-exit `A∘(ℓ_r)`! `Figure 2.8`, `G-U2b-08`) [PPA Figure 2.8, p. 93] (book p. 93; PDF p. 112).
  Dropping pre-call `A∘(ℓ_c)` (`Figure 2.9`, misprinting `f̂¹_{ℓ₁}` for `f̂¹_{ℓ_c}` on the top arrow) makes
  restoring caller locals across recursion impossible (`G-U2b-09`). `f̂²` is completely additive on the
  product lattice iff it splits as `f̂^{2A}_{ℓ_c,ℓ_r}(l̂) ⊔ f̂^{2B}_{ℓ_c,ℓ_r}(l̂')` (`Figure 2.10`, local
  caller bypass `2A` + global callee exit `2B`) with both unary factors completely additive (`G-U2b-09`)
  [PPA §2.5.3, p. 94] (book p. 94; PDF p. 113) [PPA Figure 2.10, p. 95] (book p. 95; PDF p. 114).

## 4. Context Representations & Flow-Insensitive Pre-Passes (`§§2.5.4–2.5.6`)

| Context / Strategy | Domain `Δ` & Extremum `ι̂` | Transfer Mechanics & Size | Monotone / ACC | Precision & Pitfalls | Anchor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unbounded call strings** | `Δ = Lab^*`, `ι` at `Λ` (`⊥` else) | `δ ↦ [δ, ℓ_c]` injectively (`Example 2.37–2.38`) | Monotone; **fails ACC** under recursion | Exact `VP` control context, non-terminating on cycles (`[4,4,...]`) | [PPA §2.5.4, p. 96] (book p. 96; PDF p. 115) |
| **Bounded `k` call strings (`G-U2b-10`)** | `Δ = Lab^{\le k}` (`k=0 ⇒ {Λ}` insensitive) | `⌈δ, ℓ_c⌉_k` drops left prefix; `⨆` join on merge (`Examples 2.39–2.40`) | Yes (`O(\|Lab\|^k)`) | Merges callers deeper than `k` and recursive steps at `k=1` | [PPA §2.5.4, p. 98] (book p. 98; PDF p. 117) |
| **Last `k` distinct sites (`G-U2b-11`)** | `≤ k` distinct `Lab` (`Exercise 2.16`) | Drops duplicate calls on push | Yes | Collapses `[ℓ_c, ℓ_c] ↦ [ℓ_c]` — cannot separate 1st call from recursion | [PPA Exercise 2.16, p. 138] (book p. 138; PDF p. 157) |
| **Large assumption sets (`G-U2b-12`, `G-U2b-13`)** | `Δ = 𝒫(D)` (printed `ι̂={(\{ι\},ι)}`) | Exact fiber `δ' = {d'' \| (δ, d'') ∈ Z}` (`2^{\|D\|}·\|D\|`) | **Non-monotone** (`BKL-003`) | Needs `δ' ⊆ ...` relaxation or `[51, 52]` solver; fix `ι̂={(ι,d)\|d∈ι}` | [PPA §2.5.5, p. 100] (book p. 100; PDF p. 119) |
| **Small assumption sets (`G-U2b-13`)** | `Δ = D` (printed `ι̂={(ι,ι)}`) | Relational pairs `𝒫(D × D)` (`\|D\|^2`) | Yes (additive!) | Polynomial `IFDS`-style [external] summaries; cannot group states; fix `{(d,d)\|d∈ι}` | [PPA §2.5.5, p. 101] (book p. 101; PDF p. 120) |
| **Flow-insensitive `IAV` (`G-U2b-14`, `G-U2b-15`)** | Statement/proc sets (`AV, CP, IAV`) | Order-invariant `lfp` over call graph (`Figure 2.11`, `Example 2.42`) | Yes (`lfp` required) | Book prints `"context-insensitive"` (`pp. 102–103`) & omits `\ {y}` (`F-U2b-07`); `gfp = Var⋆` | [PPA §2.5.6, p. 102] (book p. 102; PDF p. 121) |

- **Non-monotonicity mechanism (`BKL-003`, `G-U2b-12`)**: In `§2.5.5` large assumption sets, let `Z₁ = {(δ₀, d₁)}`
  grow to `Z₂ = {(δ₀, d₁), (δ₀, d₂)}`. `f̂¹_{ℓ_c}(Z₁)` tags exit pairs with `δ' = {d₁}`, which disappears from
  `f̂¹_{ℓ_c}(Z₂)` (which tags only with `{d₁, d₂}`), violating `Z₁ ⊆ Z₂ ⇒ f̂¹(Z₁) ⊆ f̂¹(Z₂)` (`Example 2.41`
  also writes 3-var states for 5-var Fibonacci and varies `y` instead of `u`, `F-U2b-06`)
  [PPA Example 2.41, p. 99] (book p. 99; PDF p. 118) [PPA §2.5.5, p. 100] (book p. 100; PDF p. 119).
- **Signs & Multiple Modes (`Exercises 2.14–2.20`, `G-U2b-34`)**: Independent-attribute Detection of Signs
  (`Var⋆ → 𝒫({-,0,+})` ≅ `𝒫(Var⋆ × {-,0,+})`, `Exercise 2.14`) loses variable correlations preserved by
  relational Signs (`𝒫(Var⋆ → {-,0,+})`, `Exercise 2.15`, `Example 2.36`) [PPA Exercise 2.15, p. 138] (book p. 138; PDF p. 157).
  Extending parameters to multiple `val, res, val-res` and locals (`Exercise 2.20`) must handle aliasing when
  two actual `res`/`val-res` arguments share one variable (`G-U2b-34`, `BKL-007` compares Chapter 3 `k`-CFA cost)
  [PPA Exercise 2.20, p. 139] (book p. 139; PDF p. 158).
- **Cross-Chapter Unifications & Architecture (`[U2b:CR-b,d,e,f]`)**: `Small Assumption Sets` + completely
  additive `f̂^{2A} ⊔ f̂^{2B}` are the Chapter 2 blueprint for IFDS/IDE tabulation (`[147, 155]` [external])
  [PPA Chapter 2 Concluding Remarks, p. 129] (book p. 129; PDF p. 148); `IAV(p)` previews Chapter 5's
  statement-level Type & Effect annotations [PPA §2.5.6, p. 103] (book p. 103; PDF p. 122); structural analysis
  (`[154, 110]`) collapses low-level CFGs into AST regions [PPA Chapter 2 Concluding Remarks, p. 131] (book p. 131; PDF p. 150).

## 5. Non-blocking Correctness & Interprocedural Backlog (`ARCHITECTURE.md` §6.4)

- `BKL-003` (large assumption set `Δ = 𝒫(D)` non-monotonicity snag, `§2.5.5`); `BKL-007` (k-CFA vs k-call-string trade-off);
- `BKL-037` (`Table 2.5` omits `true`/`false` boolean literal clauses); `BKL-038` (`§2.2.2` `LV^⊆` omits isolated-exits hypothesis breaking Lemma 2.18 / Theorem 2.21);
- `BKL-041` (`§2.5 p. 85` leaves backward `flow⋆^R` & `inter-flow⋆^R` unstated); `BKL-042` (`§2.5.1` unlabelled `[ass]`/`z:=y` and implicit `ξ₁ ≠ ξ₂`);
- `BKL-043` (`Figure 2.9` `f̂¹_{ℓ₁}` typo & `Example 2.40` `Lab ∪ {Λ}` notation); `BKL-044` (`§2.5.5` ill-typed `ι̂` & `Example 2.41` mismatch);
- `BKL-045` (`§2.5.6` `IAV(p)` omits `\ {y}` & prints `"context-insensitive"`); `BKL-049` (`Mini Project 2.2` `Trace` omits `?` + `Y` powerset + isolated entries);
- `BKL-050` (`§2.5.2` ref & `Exercises 2.7/2.11/2.13` unstated guard/closure preconditions).
