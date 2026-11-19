<!-- @governing: REQ-TECH-PPA-002 @parent: REQ-PRD-PPA-002 -->
# Unit 2b Raw Knowledge Shard: Chapter 2 (§§2.5–2.6, End Matter)

Scope: Chapter 2 (*Data Flow Analysis*), §§2.5–2.6 (*Interprocedural Analysis* and *Shape Analysis*),
*Concluding Remarks*, *Mini Projects 2.1–2.3*, and *Exercises 2.1–2.25* — from
[PPA §2.5, p. 82] (book p. 82; PDF p. 101) through [PPA Exercise 2.25, p. 139] (book p. 139; PDF p. 158).
Offset across the entire unit: `PDF page = book page + 19`. Book p. 140 is a blank verso absent from the
PDF. The closing paragraph of §2.4.2 above the §2.5 heading on book p. 82 belongs to
`corpus/shards/RAW_SHARD_02a_intraproc_dfa.md`.

Method and conventions: every formula, inference rule, program, table, figure, and numbered statement was
transcribed directly from 150-dpi and 200-dpi rendered page images (`PDF pp. 101–158`) and cross-checked
against `corpus/pdf_page_map.json`; OCR text-layer corruptions are logged in `Findings` rather than copied.
Book numbers are preserved verbatim; unnumbered subsections carry local identifiers `[U2b:<section>-<letter>]`.
Terms marked `[external]` lie outside the book; `[derived]` marks direct logical consequences of printed
definitions.

## Closed Inventory: Book pages 82–139 / PDF pages 101–158

| Kind | Count | Identifiers |
| :--- | ---: | :--- |
| Sections / Subsections | 14 | `§2.5` (`§2.5.1`–`§2.5.6`, pp. 82–103), `§2.6` (`§2.6.1`–`§2.6.3`, pp. 104–128), `Concluding Remarks` (pp. 128–131), `Mini Projects` (pp. 132–135), `Exercises` (pp. 135–139) |
| Tables | 1 | `Table 2.10` (p. 133; continues `Tables 2.1–2.9` from Unit 2a) |
| Figures | 17 | `Figure 2.7`–`2.23` (`2.7` p. 85, `2.8` p. 93, `2.9` p. 94, `2.10` p. 95, `2.11` p. 103, `2.12` p. 106, `2.13` p. 112, `2.14` p. 113, `2.15` p. 115, `2.16` p. 116, `2.17` p. 118, `2.18` p. 120, `2.19` p. 123, `2.20` p. 124, `2.21` p. 126, `2.22` p. 127, `2.23` p. 132) |
| Examples | 22 | `Example 2.33`–`2.54` (`2.33`–`2.42` in `§2.5`, `2.43`–`2.54` in `§2.6`; continues `2.1`–`2.32`) |
| Numbered Theorems / Lemmas | 0 | None in Unit 2b (locally labelled `Invariant 1`–`Invariant 5`, pp. 110–114; inline proofs on pp. 110, 122–123) |
| Unnumbered `Remark.` blocks | 4 | `§2.5.1` (p. 87), `§2.6.1` (p. 109), `§2.6.3` (p. 117), `§2.6.3` (p. 126) |
| Mini Projects | 3 | `Mini Project 2.1` (p. 132), `Mini Project 2.2` (pp. 133–134), `Mini Project 2.3` (pp. 134–135) |
| Exercises | 25 | `Exercise 2.1`–`2.25` (pp. 135–139; starred: `2.21*`, `2.23*`, `2.24*`, `2.25*`) |
| Unnumbered `[U2b:...]` units | 88 | `2.5-a..h` (8), `2.5.1-a..e` (5), `2.5.2-a..f` (6), `2.5.3-a..g` (7), `2.5.4-a..e` (5), `2.5.5-a..e` (5), `2.5.6-a..f` (6), `2.6-a..b` (2), `2.6.1-a..g` (7), `2.6.2-a..j` (10), `2.6.3-a..u` (21), `CR-a..f` (6) |

---

## 2.5 Interprocedural Analysis

Context: extending `WHILE` with mutually recursive top-level procedures, operational store/environment
semantics, context-free call/return path validity (`CP`, `VP`, `MVP`), embellished Monotone Frameworks,
bounded call strings, assumption sets, and flow-insensitive call/`[external: mod-ref]` summaries
[PPA §2.5, p. 82] (book p. 82; PDF p. 101).

### [U2b:2.5-a] Scope and complications of interprocedural analysis (unnumbered remark)
- Statement: §§2.1–2.4 covered *intraprocedural analyses* on languages without functions or procedures.
  *Interprocedural analyses* introduce procedures, bringing three named complications: ensuring calls and returns
  match; parameter-passing mechanisms (and aliasing caused by call-by-reference); and procedures passed as
  parameters. §2.5 extends `WHILE` with top-level declarations of global, mutually recursive procedures having
  one *call-by-value* parameter and one *call-by-result* parameter. Extensions to multiple call-by-value,
  call-by-result, and call-by-value-result parameters plus local variable declarations ([PPA Exercise 2.20, p. 139]
  (book p. 139; PDF p. 158)) are stated to be straightforward and used freely in examples.
- Citation: [PPA §2.5, p. 82] (book p. 82; PDF p. 101)

### [U2b:2.5-b] Procedure-extended `WHILE` syntax (unnumbered definition)
- Statement: a program `P⋆` has the form `begin D⋆ S⋆ end` where `D⋆` is a sequence of procedure declarations:

```
D ::= proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}  |  D D
S ::= ···  |  [call p(a, z)]^{ℓ_c}_{ℓ_r}
```

  Procedure names `p` are syntactically distinct from variables `x, y`. Entry to a body carries label `ℓ_n`
  on `is`; exit carries label `ℓ_x` on `end`. A call carries two labels: `ℓ_c` for calling and `ℓ_r` for
  returning; actual parameters are arithmetic expression `a` and variable `z`.
- Citation: [PPA §2.5, p. 82] (book p. 82; PDF p. 101)

### [U2b:2.5-c] Standing assumptions on procedure programs (unnumbered specification)
- Statement: static scoping; mutually recursive procedures; three standing assumptions:
  1. `P⋆` is uniquely labelled (hence label consistent; cf. BKL-028);
  2. only procedures declared in `D⋆` are ever called; and
  3. `D⋆` contains no duplicate declarations of the same procedure name.
- Citation: [PPA §2.5, p. 83] (book p. 83; PDF p. 102)

### Example 2.33 — Recursive Fibonacci program
- Statement: computes the Fibonacci number of positive integer `x`, returning it in `y` using two `val`
  parameters (`z, u`) and one `res` parameter (`v`):

```
begin proc fib(val z, u, res v) is^1
           if [z<3]^2 then [v:=u+1]^3
           else ([call fib(z-1,u,v)]^4_5; [call fib(z-2,v,v)]^6_7)
      end^8;
      [call fib(x,0,y)]^9_10
end
```

  `x, y` are global variables; formal parameters `z, u, v` are local variables. ■
- Citation: [PPA Example 2.33, p. 83] (book p. 83; PDF p. 102)

### [U2b:2.5-d] Flow-graph equations for `[call p(a, z)]^{ℓ_c}_{ℓ_r}` (unnumbered definition)
- Statement: whenever `proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}` is in `D⋆`:

```
init([call p(a,z)]^{ℓ_c}_{ℓ_r})   = ℓ_c
final([call p(a,z)]^{ℓ_c}_{ℓ_r})  = {ℓ_r}
blocks([call p(a,z)]^{ℓ_c}_{ℓ_r}) = {[call p(a,z)]^{ℓ_c}_{ℓ_r}}
labels([call p(a,z)]^{ℓ_c}_{ℓ_r}) = {ℓ_c, ℓ_r}
flow([call p(a,z)]^{ℓ_c}_{ℓ_r})   = {(ℓ_c; ℓ_n), (ℓ_x; ℓ_r)}
```

  Semicolon pairs `(ℓ_c; ℓ_n)` denote calling flow and `(ℓ_x; ℓ_r)` denote returning flow, distinguishing
  interprocedural transitions from intraprocedural `(ℓ₁, ℓ₂)` edges.
- Citation: [PPA §2.5, p. 83] (book p. 83; PDF p. 102); `flow` explanation on [PPA §2.5, p. 84] (book p. 84; PDF p. 103)

### [U2b:2.5-e] Dynamic dispatch problem (unnumbered remark)
- Statement: defining `flow` on calls relies on calls naming a syntactic procedure constant `p`. Allowing
  variables or parameters to denote procedures makes defining `flow` much harder — the *dynamic dispatch
  problem*, deferred to Chapter 3.
- Citation: [PPA §2.5, p. 84] (book p. 84; PDF p. 103)

### [U2b:2.5-f] Flow-graph equations for procedures and programs (unnumbered definition)
- Statement: for each `proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}` in `D⋆` and whole program `P⋆ = begin D⋆ S⋆ end`:

```
init(p)   = ℓ_n
final(p)  = {ℓ_x}
blocks(p) = {is^{ℓ_n}, end^{ℓ_x}} ∪ blocks(S)
labels(p) = {ℓ_n, ℓ_x} ∪ labels(S)
flow(p)   = {(ℓ_n, init(S))} ∪ flow(S) ∪ {(ℓ, ℓ_x) | ℓ ∈ final(S)}

init⋆     = init(S⋆)
final⋆    = final(S⋆)
blocks⋆   = ⋃{blocks(p) | proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x} is in D⋆} ∪ blocks(S⋆)
labels⋆   = ⋃{labels(p) | proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x} is in D⋆} ∪ labels(S⋆)
flow⋆     = ⋃{flow(p)   | proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x} is in D⋆} ∪ flow(S⋆)
Lab⋆      = labels⋆
```

- Citation: [PPA §2.5, p. 84] (book p. 84; PDF p. 103)

### [U2b:2.5-g] Interprocedural flow relation `inter-flow⋆` (unnumbered definition)
- Statement:

```
inter-flow⋆ = {(ℓ_c, ℓ_n, ℓ_x, ℓ_r) | P⋆ contains [call p(a, z)]^{ℓ_c}_{ℓ_r}
                                     as well as proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}}
```

  If `inter-flow⋆` contains `(ℓ_c^i, ℓ_n, ℓ_x, ℓ_r^i)` for `i = 1, 2`, `flow⋆` contains separate calling
  and returning pairs `(ℓ_c^i; ℓ_n)` and `(ℓ_x; ℓ_r^i)` yielding four tuples `(ℓ_c^i, ℓ_n, ℓ_x, ℓ_r^j)` (`i, j ∈ {1, 2}`);
  only `i = j` matches return to caller, which is precisely what `inter-flow⋆` records.
- Citation: [PPA §2.5, p. 84] (book p. 84; PDF p. 103)

### Figure 2.7 — Flow graph for the Fibonacci program
- Content: procedure box `proc fib(val z, u, res v)` holds `is¹ → [z<3]²`; `[z<3]²` branches `yes → [v:=u+1]³ → end⁸`
  and `no → [call fib(z-1,u,v)]⁴_⁵ → [call fib(z-2,v,v)]⁶_⁷ → end⁸`. Main program box `[call fib(x,0,y)]⁹_{10}`
  has an entry arrow in and an exit arrow out. Curved interprocedural call arcs run `9 → 1`, `4 → 1`, `6 → 1`;
  return arcs run `8 → 10`, `8 → 5`, `8 → 7`.
- Citation: [PPA Figure 2.7, p. 85] (book p. 85; PDF p. 104)

### Example 2.34 — `flow⋆` and `inter-flow⋆` for Fibonacci
- Statement: for Example 2.33 / Figure 2.7:

```
flow⋆       = {(1,2), (2,3), (3,8), (2,4), (4;1), (8;5), (5,6), (6;1), (8;7), (7,8), (9;1), (8;10)}
inter-flow⋆ = {(9,1,8,10), (4,1,8,5), (6,1,8,7)}
init⋆ = 9,   final⋆ = {10}
```

  ■
- Citation: [PPA Example 2.34, p. 85] (book p. 85; PDF p. 104)

### [U2b:2.5-h] Forward and backward interprocedural parameters `F, E, IF` (unnumbered specification)
- Statement: forward analysis takes `F = flow⋆`, `E = {init⋆}`, and `IF = inter-flow⋆`; backward analysis
  takes `F = flow⋆^R`, `E = final⋆`, and `IF = inter-flow⋆^R` (see `F-U2b-01`: reversal on semicolon flows
  and 4-tuples is left implicit).
- Citation: [PPA §2.5, p. 85] (book p. 85; PDF p. 104)

### Findings (2.5 Opening)
- F-U2b-01: on p. 85 backward interprocedural analysis specifies `F = flow⋆^R` and `IF = inter-flow⋆^R`
  without explicitly defining `^R` on semicolon pairs `(ℓ_c; ℓ_n), (ℓ_x; ℓ_r)` or on 4-tuples `(ℓ_c, ℓ_n, ℓ_x, ℓ_r)`
  (`[derived]`: semicolon reversal flips `(ℓ_n; ℓ_c)` and `(ℓ_r; ℓ_x)`, and 4-tuple reversal yields `(ℓ_r, ℓ_x, ℓ_n, ℓ_c)`).
  [PPA §2.5, p. 85] (book p. 85; PDF p. 104)

### Projections (2.5 Opening)
- cs_theory: interprocedural control flow distinguishes call/return edges `(ℓ_c; ℓ_n), (ℓ_x; ℓ_r)` from
  intraprocedural edges and pairs matching sites in 4-tuple relation `inter-flow⋆`, turning regular CFG
  paths into context-free balanced parenthesis constraints.
- swe_architecture: index call and return blocks by explicit `(ℓ_c, ℓ_r)` label pairs and retain an
  explicit `IF` table alongside `F`; collapsing calls into plain CFG edges destroys call-site identity.
- practical_debugging: if a backward interprocedural pass skips procedure bodies or scrambles return
  flows, verify both `(ℓ_x; ℓ_r) ↦ (ℓ_r; ℓ_x)` in `flow⋆^R` and `(ℓ_r, ℓ_x, ℓ_n, ℓ_c)` orientation in `IF`.
- cyber: syntactic call graphs assume closed-world static call targets (`[U2b:2.5-e]`, `BKL-008`); indirect
  calls, function pointers, vtables, and reflection [external] require Chapter 3 dynamic-dispatch recovery
  before interprocedural taint paths are sound.

## 2.5.1 Structural Operational Semantics

Context: splitting state into `Env` and `Store` to model fresh formal-parameter locations, top-level static
scoping `ρ⋆`, and intermediate `bind` statements [PPA §2.5.1, p. 85] (book p. 85; PDF p. 104).

### [U2b:2.5.1-a] Locations, environments, stores, and totality invariant (unnumbered definition)
- Statement: to distinguish incarnations of local procedure variables:

```
ξ ∈ Loc                            (infinite set of locations / addresses)
ρ ∈ Env   = Var⋆ → Loc             (environments)
ς ∈ Store = Loc →_fin Z            (stores: partial finite-domain maps)
```

  State reconstruction is `σ = ς ∘ ρ`, requiring `ς ∘ ρ : Var⋆ → Z` to be total, i.e., `ran(ρ) ⊆ dom(ς)`
  where `ran(ρ) = {ρ(x) | x ∈ Var⋆}` and `dom(ς) = {ξ | ς is defined on ξ}`.
- Citation: [PPA §2.5.1, p. 86] (book p. 86; PDF p. 105)

### [U2b:2.5.1-b] Top-level environment `ρ⋆` and lifted transitions (unnumbered definition)
- Statement: a *top-level environment* `ρ⋆` maps all global variables in `Var⋆` to distinct locations.
  Transition relations `ρ ⊢⋆ ⟨S, ς⟩ → ⟨S', ς'⟩` and `ρ ⊢⋆ ⟨S, ς⟩ → ς'` adapt Table 2.6; for example:

```
[ass]   ρ ⊢⋆ ⟨x:=a, ς⟩ → ς[ρ(x) ↦ 𝒜⟦a⟧(ς ∘ ρ)]     if ς ∘ ρ is total
```

  Expression semantics `𝒜` and `ℬ` (Table 2.5) require no change.
- Citation: [PPA §2.5.1, p. 86] (book p. 86; PDF p. 105)

### [U2b:2.5.1-c] Transition rule `[call]` for `[call p(a, z)]^{ℓ_c}_{ℓ_r}` (unnumbered definition)
- Statement: whenever `proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}` is in `D⋆` (`[U2b:2.5.1-c]` printed on p. 87):

```
ρ ⊢⋆ ⟨[call p(a,z)]^{ℓ_c}_{ℓ_r}, ς⟩ →
     ⟨bind ρ⋆[x ↦ ξ₁, y ↦ ξ₂] in S then z:=y, ς[ξ₁ ↦ 𝒜⟦a⟧(ς ∘ ρ), ξ₂ ↦ v]⟩
     where ξ₁, ξ₂ ∉ dom(ς), v ∈ Z
     and proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x} is in D⋆
```

  Side conditions: fresh locations `ξ₁ ≠ ξ₂` (distinct implicitly because `x ↦ ξ₁, y ↦ ξ₂` bind distinct formals,
  and since `ran(ρ⋆) ⊆ dom(ς)`, `ξ₁, ξ₂` are outside `ran(ρ⋆)` too `[derived]`); body `S` executes under
  `ρ⋆[x ↦ ξ₁, y ↦ ξ₂]` (enforcing static scope rather than dynamic inheritance from caller `ρ`); formal `y`
  starts at an *arbitrary* `v ∈ Z` (uninitialised result parameter).
- Citation: [PPA §2.5.1, p. 87] (book p. 87; PDF p. 106)

### [U2b:2.5.1-d] Semantics of intermediate `bind ρ' in S then z:=y` (unnumbered definition)
- Statement:

```
            ρ' ⊢⋆ ⟨S, ς⟩ → ⟨S', ς'⟩
[bind₁] ────────────────────────────────────────────────────────────────
        ρ ⊢⋆ ⟨bind ρ' in S then z:=y, ς⟩ → ⟨bind ρ' in S' then z:=y, ς'⟩

            ρ' ⊢⋆ ⟨S, ς⟩ → ς'
[bind₂] ───────────────────────────────────────────────────────
        ρ ⊢⋆ ⟨bind ρ' in S then z:=y, ς⟩ → ς'[ρ(z) ↦ ς'(ρ'(y))]
```

  Once `S` terminates in `ς'`, `ς'` writes formal `ρ'(y)` back into caller actual location `ρ(z)` and
  discards `ρ'`, resuming caller execution in `ρ` (allocated stack locations `ξ₁, ξ₂` remain in `dom(ς')`).
- Citation: [PPA §2.5.1, p. 87] (book p. 87; PDF p. 106)

### [U2b:2.5.1-e] Remark — Abstracting `ς ∘ ρ` and analysing `bind` (unnumbered Remark)
- Statement: **Remark.** While the SOS separates environments `ρ` and stores `ς`, analyses frequently abstract
  only states `σ = ς ∘ ρ`; correctness must then relate abstract state to both `ρ` and `ς`. Because `bind`
  occurs only in intermediate configurations, correctness proofs must specify how `bind` is analysed (deferred
  to Chapter 3). ■
- Citation: [PPA §2.5.1, p. 87] (book p. 87; PDF p. 106)

### Findings (2.5.1)
- F-U2b-02: on p. 86 rewritten `[ass]` prints `⟨x:=a, ς⟩` without `[x:=a]^ℓ` brackets/label, and `bind ρ' in S then z:=y`
  on p. 87 embeds unlabelled `z:=y`; `[call]` implicitly forces `ξ₁ ≠ ξ₂` (since if `ξ₁ = ξ₂`, setting `x ↦ ξ₁`
  and `y ↦ ξ₁` would alias `val x` and `res y` and overwrite `𝒜⟦a⟧` with `v`). [PPA §2.5.1, p. 86] (book p. 86; PDF p. 105);
  [PPA §2.5.1, p. 87] (book p. 87; PDF p. 106)

### Projections (2.5.1)
- cs_theory: two-level `Env`/`Store` semantics formalises call-frame allocation and static lexical scoping
  (`ρ⋆[x↦ξ₁, y↦ξ₂]`) while nondeterministic `v ∈ Z` for `res y` makes read-before-write of out-parameters
  observable inside soundness proofs.
- swe_architecture: treat `res`/out-parameters as `⊤`/all-values upon procedure entry (`G-U2b-02`) and
  restore caller-local parameter bindings on return rather than preserving callee-clobbered formals.
- practical_debugging: if a recursive analysis leaks inner-call values into outer `x`/`y` formals or assumes
  unwritten `res` variables hold `0`, check `f̂¹` (must set `res y` to unconstrained `⊤`) and `f̂²` (must restore
  caller formals from `A∘(ℓ_c)`).
- cyber: nondeterministic `v ∈ Z` directly models uninitialised stack/out-parameter memory disclosure (`CWE-908` / `CWE-457` [external])
  when a callee fails to assign `res y` along an error path and `[bind₂]` copies
  uninitialised `ς'(ξ₂)` back into caller `z` (`[derived]`).

## 2.5.2 Intraprocedural versus Interprocedural Analysis

Context: demonstrating naive cross-call poisoning, formalising context-free Complete Paths (`CP`) and
Valid Paths (`VP⋆`), and defining Meet over all Valid Paths (`MVP`) [PPA §2.5.2, p. 88] (book p. 88; PDF p. 107).

### [U2b:2.5.2-a] Four transfer labels per call/declaration (unnumbered definition)
- Statement: calls `[call p(a, z)]^{ℓ_c}_{ℓ_r}` carry `f_{ℓ_c}` (calling) and `f_{ℓ_r}` (returning);
  definitions `proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}` carry `f_{ℓ_n}` (entering) and `f_{ℓ_x}` (exiting).
- Citation: [PPA §2.5.2, p. 88] (book p. 88; PDF p. 107)

### [U2b:2.5.2-b] Naive interprocedural equation system (unnumbered definition)
- Statement: treating `(ℓ_c; ℓ_n)` and `(ℓ_x; ℓ_r)` identically to intraprocedural `(ℓ₁, ℓ₂)` edges and
  taking all four call/return/entry/exit functions as `id`:

```
A•(ℓ) = f_ℓ(A∘(ℓ))
A∘(ℓ) = ⨆{A•(ℓ') | (ℓ', ℓ) ∈ F or (ℓ'; ℓ) ∈ F} ⊔ ι^ℓ_E
ι^ℓ_E = ι   if ℓ ∈ E;   ⊥   if ℓ ∉ E
```

  This is sound ("formally on the safe side") yet grossly imprecise because `IF` is ignored and calls/returns
  act like `goto`s: in Figure 2.7, unrealizable path `[9,1,2,4,1,2,3,8,10]` (entering from `4`, returning to
  `10`) is admitted.
- Citation: [PPA §2.5.2, p. 88] (book p. 88; PDF p. 107)

### [U2b:2.5.2-c] Context-free complete-path grammar `CP_{ℓ₁,ℓ₂}` (unnumbered definition)
- Statement: a *complete path* from `ℓ₁` to `ℓ₂` has balanced call entries and returns matching callers:

```
CP_{ℓ₁,ℓ₂} ⟶ ℓ₁                           whenever ℓ₁ = ℓ₂
CP_{ℓ₁,ℓ₃} ⟶ ℓ₁, CP_{ℓ₂,ℓ₃}                whenever (ℓ₁, ℓ₂) ∈ F
CP_{ℓ_c,ℓ} ⟶ ℓ_c, CP_{ℓ_n,ℓ_x}, CP_{ℓ_r,ℓ} whenever (ℓ_c, ℓ_n, ℓ_x, ℓ_r) ∈ IF
```

  The third rule enforces balanced parentheses pairing `(ℓ_c; ℓ_n)` with `(ℓ_x; ℓ_r)`; terminating runs yield
  complete paths from `init⋆` to `final⋆`. The grammar is finite because `Lab⋆` is finite.
- Citation: [PPA §2.5.2, p. 89] (book p. 89; PDF p. 108)

### Example 2.35 — Complete-path grammar for Fibonacci
- Statement: reachable productions from `CP_{9,10}` in Figure 2.7:

```
CP_{9,10}  ⟶ 9, CP_{1,8}, CP_{10,10}     CP_{3,8} ⟶ 3, CP_{8,8}
CP_{10,10} ⟶ 10                          CP_{8,8} ⟶ 8
CP_{1,8}   ⟶ 1, CP_{2,8}                 CP_{4,8} ⟶ 4, CP_{1,8}, CP_{5,8}
CP_{2,8}   ⟶ 2, CP_{3,8}                 CP_{5,8} ⟶ 5, CP_{6,8}
CP_{2,8}   ⟶ 2, CP_{4,8}                 CP_{6,8} ⟶ 6, CP_{1,8}, CP_{7,8}
                                         CP_{7,8} ⟶ 7, CP_{8,8}
```

  `CP_{9,10}` generates `[9,1,2,4,1,2,3,8,5,6,1,2,3,8,7,8,10]` and rejects `[9,1,2,4,1,2,3,8,10]`. ■
- Citation: [PPA Example 2.35, p. 89] (book p. 89; PDF p. 108)

### [U2b:2.5.2-d] Valid-path grammar `VP⋆` (unnumbered definition)
- Statement: a *valid path* starts at `E`, matches every closed call/return properly, and allows calls
  that have been entered and not yet exited (covering inside-body points and diverging executions):

```
VP⋆        ⟶ VP_{ℓ₁,ℓ₂}                    whenever ℓ₁ ∈ E and ℓ₂ ∈ Lab⋆
VP_{ℓ₁,ℓ₂} ⟶ ℓ₁                            whenever ℓ₁ = ℓ₂
VP_{ℓ₁,ℓ₃} ⟶ ℓ₁, VP_{ℓ₂,ℓ₃}                 whenever (ℓ₁, ℓ₂) ∈ F
VP_{ℓ_c,ℓ} ⟶ ℓ_c, CP_{ℓ_n,ℓ_x}, VP_{ℓ_r,ℓ}  whenever (ℓ_c, ℓ_n, ℓ_x, ℓ_r) ∈ IF
VP_{ℓ_c,ℓ} ⟶ ℓ_c, VP_{ℓ_n,ℓ}                whenever (ℓ_c, ℓ_n, ℓ_x, ℓ_r) ∈ IF
```

- Citation: [PPA §2.5.2, p. 89] (book p. 89; PDF p. 108); productions on [PPA §2.5.2, p. 90] (book p. 90; PDF p. 109)

### [U2b:2.5.2-e] Valid-path sets `vpath∘` and `vpath•` (unnumbered definition)
- Statement:

```
vpath∘(ℓ) = {[ℓ₁, ···, ℓ_{n-1}] | n ≥ 1 ∧ ℓ_n = ℓ ∧ [ℓ₁, ···, ℓ_n] is a valid path}
vpath•(ℓ) = {[ℓ₁, ···, ℓ_n]     | n ≥ 1 ∧ ℓ_n = ℓ ∧ [ℓ₁, ···, ℓ_n] is a valid path}
```

- Citation: [PPA §2.5.2, p. 90] (book p. 90; PDF p. 109)

### [U2b:2.5.2-f] Meet Over all Valid Paths (`MVP`) (unnumbered definition)
- Statement:

```
MVP∘(ℓ) = ⨆{f_ℓ⃗(ι) | ℓ⃗ ∈ vpath∘(ℓ)},     MVP•(ℓ) = ⨆{f_ℓ⃗(ι) | ℓ⃗ ∈ vpath•(ℓ)}
```

  Because `vpath∘(ℓ) ⊆ path∘(ℓ)` and `vpath•(ℓ) ⊆ path•(ℓ)` (against semicolon-collapsed edges),
  `MVP∘(ℓ) ⊑ MOP∘(ℓ)` and `MVP•(ℓ) ⊑ MOP•(ℓ)` for every `ℓ`.
- Citation: [PPA §2.5.2, p. 90] (book p. 90; PDF p. 109)

### Findings (2.5.2)
- F-U2b-03: p. 88 prints `"When inspecting this equation system is should be apparent"` (`"is"` for `"it"`);
  p. 89 prints `"if it is has proper nesting"` (`"is has"`); p. 90 writes `"defined in Section 2.3"` for
  `path∘`/`path•` (actually defined in §2.4.2, p. 79). [PPA §2.5.2, p. 88] (book p. 88; PDF p. 107);
  [PPA §2.5.2, p. 89] (book p. 89; PDF p. 108); [PPA §2.5.2, p. 90] (book p. 90; PDF p. 109)

### Projections (2.5.2)
- cs_theory: `CP` and `VP` form context-free / visibly pushdown Dyck languages [external] whose open-prefix
  production `VP_{ℓ_c,ℓ} ⟶ ℓ_c, VP_{ℓ_n,ℓ}` handles pending calls and non-terminating computations.
- swe_architecture: `MVP` serves as the interprocedural precision gold standard analogous to Chapter 2's
  `MOP`; call-string truncation (`§2.5.4`) and summary tabulation (`§2.5.5`) trade off toward `MVP`.
- practical_debugging: cross-over false positives at `ℓ_r¹` induced by call `ℓ_c²` immediately diagnose
  missing `inter-flow⋆` call/return matching.
- cyber: in interprocedural taint analysis [external], unrealizable paths (`(ℓ_c^{trusted}, ℓ_n, ℓ_x, ℓ_r^{sink})`
  and `(ℓ_c^{tainted}, ℓ_n, ℓ_x, ℓ_r^{ignored})`) inflate triage queues when utilities (`memcpy`, logging,
  parsers) are shared across trusted config loaders and untrusted handlers.

## 2.5.3 Making Context Explicit

Context: lifting a Monotone Framework `(L, 𝓕, F, E, ι, f_·)` to context-indexed space `L̂ = Δ → L` with
binary return transfer functions `f̂²_{ℓ_c,ℓ_r}` [PPA §2.5.3, p. 90] (book p. 90; PDF p. 109).

### [U2b:2.5.3-a] Undecidability of `MVP` and context information `δ ∈ Δ` (unnumbered remark)
- Statement: `MVP` may remain undecidable even when `L` has finite height (`p. 90`, just like `MOP`);
  *context information* `δ ∈ Δ` (`p. 91`) is encoded inside properties to exclude invalid paths in `MFP`.
- Citation: [PPA §2.5.3, p. 90] (book p. 90; PDF p. 109); context `δ ∈ Δ` on [PPA §2.5.3, p. 91] (book p. 91; PDF p. 110)

### [U2b:2.5.3-b] Embellished Monotone Framework `(L̂, 𝓕̂, F, E, ι̂, f̂_·)` (unnumbered definition)
- Statement: for context domain `Δ`, construct lifted framework `(L̂, 𝓕̂, F, E, ι̂, f̂_·)`:
  - property space `L̂ = Δ → L`;
  - transfer functions in `𝓕̂` are monotone; and
  - for all intraprocedural labels (not occurring in 1st or 4th component of `IF`), `f̂_ℓ(l̂)(δ) = f_ℓ(l̂(δ))`:

```
A•(ℓ) = f̂_ℓ(A∘(ℓ))    (ℓ not a first or fourth component in IF)
A∘(ℓ) = ⨆{A•(ℓ') | (ℓ', ℓ) ∈ F or (ℓ'; ℓ) ∈ F} ⊔ ι̂^ℓ_E    (for ALL ℓ)
```

- Citation: [PPA §2.5.3, p. 91] (book p. 91; PDF p. 110)

### Example 2.36 — Detection of Signs, embellished form
- Statement: base framework `L_sign = 𝒫(Var⋆ → Sign)` (`Sign = {-, 0, +}`), `f_ℓ^sign(Y) = ⋃{φ_ℓ^sign(σ^sign) | σ^sign ∈ Y}`
  with `φ_ℓ^sign(σ^sign) = {σ^sign[x ↦ s] | s ∈ 𝒜_sign⟦a⟧(σ^sign)}` (`[x:=a]^ℓ`) and identity for `[skip]^ℓ, [b]^ℓ`.
  Embellished in isomorphic powerset pair form `L̂_sign = 𝒫(Δ × (Var⋆ → Sign))` (`Δ → 𝒫(D) ≅ 𝒫(Δ × D)`):

```
f̂_ℓ^sign(Z) = ⋃{{δ} × φ_ℓ^sign(σ^sign) | (δ, σ^sign) ∈ Z}
```

  ■
- Citation: [PPA Example 2.36, p. 91] (book p. 91; PDF p. 110); isomorphic `𝒫` form on
  [PPA Example 2.36, p. 92] (book p. 92; PDF p. 111)

### [U2b:2.5.3-c] Procedure entry and exit transfer functions (unnumbered definition)
- Statement: for `proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}`, `f̂_{ℓ_n}(l̂) = l̂` and `f̂_{ℓ_x}(l̂) = l̂`; entry/exit
  semantics is instead placed on call/return functions `f̂¹_{ℓ_c}` and `f̂²_{ℓ_c,ℓ_r}`.
- Citation: [PPA §2.5.3, p. 92] (book p. 92; PDF p. 111)

### Figure 2.8 — Analysis of procedure call: the forward case
- Content: box `[call p(a, z)]^{ℓ_c}_{ℓ_r}` accepts `l̂` into its call half, sends `f̂¹_{ℓ_c}(l̂)` to `is^{ℓ_n}`
  of `proc p(val x, res y)` (linked by wavy path to `end^{ℓ_x}`), receives `l̂'` back from `end^{ℓ_x}` into its
  return half alongside an internal vertical edge forwarding pre-call `l̂` to the return half, and outputs
  `f̂²_{ℓ_c,ℓ_r}(l̂, l̂')`.
- Citation: [PPA Figure 2.8, p. 93] (book p. 93; PDF p. 112)

### [U2b:2.5.3-d] Unary call and binary return transfer equations (unnumbered definition)
- Statement: for every `(ℓ_c, ℓ_n, ℓ_x, ℓ_r) ∈ IF` (forward):

```
f̂¹_{ℓ_c}     : (Δ → L) → (Δ → L),           A•(ℓ_c) = f̂¹_{ℓ_c}(A∘(ℓ_c))
f̂²_{ℓ_c,ℓ_r} : (Δ → L) × (Δ → L) → (Δ → L), A•(ℓ_r) = f̂²_{ℓ_c,ℓ_r}(A∘(ℓ_c), A∘(ℓ_r))
```

- Citation: [PPA §2.5.3, p. 93] (book p. 93; PDF p. 112)

### Figure 2.9 — Analysis of procedure call: ignoring calling context
- Content: call box split into `[call p(a, z)]^{ℓ_c}` and `[call p(a, z)]_{ℓ_r}` with no internal edge
  between them; top arrow from call to `is^{ℓ_n}` prints `f̂¹_{ℓ₁}` (erratum for `f̂¹_{ℓ_c}`, `F-U2b-04`),
  wavy path runs `is^{ℓ_n} → end^{ℓ_x}`, bottom arrow carries `f̂²_{ℓ_c,ℓ_r}` from `end^{ℓ_x}` to return box.
- Citation: [PPA Figure 2.9, p. 94] (book p. 94; PDF p. 113)

### [U2b:2.5.3-e] Role of `f̂²`'s first argument (unnumbered remark)
- Statement: pre-call `A∘(ℓ_c)` lets `f̂²_{ℓ_c,ℓ_r}` recover caller-side context and local variables intact
  across the call (essential for Example 2.38).
- Citation: [PPA §2.5.3, p. 94] (book p. 94; PDF p. 113)

### [U2b:2.5.3-f] Variations of `f̂²` and additivity characterisation (unnumbered specification)
- Statement: two standard shapes for `f̂²_{ℓ_c,ℓ_r}(l̂, l̂')`:
  1. `f̂²_{ℓ_c,ℓ_r}(l̂, l̂') = f̂²_{ℓ_r}(l̂')` — ignores pre-call state (Figure 2.9);
  2. `f̂²_{ℓ_c,ℓ_r}(l̂, l̂') = f̂^{2A}_{ℓ_c,ℓ_r}(l̂) ⊔ f̂^{2B}_{ℓ_c,ℓ_r}(l̂')` — joins local bypass with callee exit
     (Figure 2.10). Parenthetical fact: `f̂²_{ℓ_c,ℓ_r}` is completely additive on `(Δ → L) × (Δ → L)` iff it
     decomposes into form 2 with both `f̂^{2A}` and `f̂^{2B}` completely additive.
- Citation: [PPA §2.5.3, p. 94] (book p. 94; PDF p. 113)

### Figure 2.10 — Analysis of procedure call: merging of context
- Content: as Figure 2.9, but with arrow `f̂¹_{ℓ_c}` to `is^{ℓ_n}`, internal vertical bypass arrow
  `f̂^{2A}_{ℓ_c,ℓ_r}` from `[call p(a, z)]^{ℓ_c}` to `[call p(a, z)]_{ℓ_r}`, and return arrow
  `f̂^{2B}_{ℓ_c,ℓ_r}` from `end^{ℓ_x}` to `[call p(a, z)]_{ℓ_r}`.
- Citation: [PPA Figure 2.10, p. 95] (book p. 95; PDF p. 114)

### [U2b:2.5.3-g] Context-insensitive versus context-sensitive analyses (unnumbered definition)
- Statement: conflating all call sites into a single shared procedure summary causes *cross-over* across
  callers and is called *context-insensitive*; distinguishing calls reached under different `δ₁, δ₂` without
  cross-over is *context-sensitive*, balancing higher precision against higher cost.
- Citation: [PPA §2.5.3, p. 94] (book p. 94; PDF p. 113); context-sensitive definition on
  [PPA §2.5.3, p. 95] (book p. 95; PDF p. 114)

### Findings (2.5.3)
- F-U2b-04: Figure 2.9 (`p. 94`) prints `f̂¹_{ℓ₁}` on the call arrow instead of `f̂¹_{ℓ_c}` (compare
  Figures 2.8 and 2.10); note that relational `f̂²` joining identical `δ` across `(A∘(ℓ_c), A∘(ℓ_r))` (Example
  2.38, Small Assumption Sets) is monotone but *not* completely additive in the pair `(l̂, l̂')` `[derived]`.
  [PPA Figure 2.9, p. 94] (book p. 94; PDF p. 113)

### Projections (2.5.3)
- cs_theory: `Δ → 𝒫(D) ≅ 𝒫(Δ × D)` currying makes context-indexed analyses uniformly representable as pair
  relations; additive decomposition `f̂^{2A}(l̂) ⊔ f̂^{2B}(l̂')` isolates call-to-return local frame edges
  (`IFDS`/`IDE` [external]) from relational context filtering.
- swe_architecture: wire binary return transfers `f̂²(A∘(ℓ_c), A∘(ℓ_r))` explicitly in the solver so call
  worklist triggers re-evaluate `ℓ_r` whenever either `A∘(ℓ_c)` *or* `A∘(ℓ_r)` changes (`[derived]`).
- practical_debugging: if a solver omits dependency edge `(ℓ_c → ℓ_r)` in the worklist graph, updates to
  caller locals before a recursive call never propagate past `ℓ_r` until another exit fires.
- cyber: call-to-return bypass (`f̂^{2A}`) without context matching lets secret/tainted caller locals clash
  or smear with unrelated callee returns when local vs global variable scopes are misclassified.

## 2.5.4 Call Strings as Context

Context: unbounded (`Δ = Lab^*`) and length-bounded (`Δ = Lab^{\le k}`) call strings [PPA §2.5.4, p. 95] (book p. 95; PDF p. 114).

### [U2b:2.5.4-a] Design obligations for context choices (unnumbered remark)
- Statement: specifying an embellished instance requires choosing `Δ`, defining extremal `ι̂`, and defining
  `f̂¹_{ℓ_c}` and `f̂²_{ℓ_c,ℓ_r}`.
- Citation: [PPA §2.5.4, p. 95] (book p. 95; PDF p. 114)

### [U2b:2.5.4-b] Unbounded call strings (`Δ = Lab*`) (unnumbered definition)
- Statement:

```
Δ = Lab*     (rightmost entry = most recent call ℓ_c)
ι̂(δ) = ι  if δ = Λ;   ⊥  otherwise
```

- Citation: [PPA §2.5.4, p. 96] (book p. 96; PDF p. 115)

### Example 2.37 — Unbounded call strings for Fibonacci
- Statement: relevant strings for `0, 1, 2, 3, ···` pending calls: `Λ, [9], [9,4], [9,6], [9,4,4], [9,4,6], [9,6,4], [9,6,6], ···`. ■
- Citation: [PPA Example 2.37, p. 96] (book p. 96; PDF p. 115)

### [U2b:2.5.4-c] Unbounded call-string transfer functions (unnumbered definition)
- Statement: with underlying `f¹_{ℓ_c} : L → L` and `f²_{ℓ_c,ℓ_r} : L × L → L`:

```
f̂¹_{ℓ_c}(l̂)(δ')        = f¹_{ℓ_c}(l̂(δ))   when δ' = [δ, ℓ_c];   ⊥  otherwise
f̂²_{ℓ_c,ℓ_r}(l̂, l̂')(δ) = f²_{ℓ_c,ℓ_r}(l̂(δ), l̂'([δ, ℓ_c]))
```

- Citation: [PPA §2.5.4, p. 96] (book p. 96; PDF p. 115)

### Example 2.38 — Detection of Signs with unbounded call strings
- Statement: for `[call p(a, z)]^{ℓ_c}_{ℓ_r}` and `proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}`:

```
f̂^{sign1}_{ℓ_c}(Z)        = ⋃{{δ'} × φ^{sign1}_{ℓ_c}(σ^sign) | (δ, σ^sign) ∈ Z ∧ δ' = [δ, ℓ_c]}
φ^{sign1}_{ℓ_c}(σ^sign)   = {σ^sign[x ↦ s][y ↦ s'] | s ∈ 𝒜_sign⟦a⟧(σ^sign) ∧ s' ∈ {-, 0, +}}

f̂^{sign2}_{ℓ_c,ℓ_r}(Z, Z') = ⋃{{δ} × φ^{sign2}_{ℓ_c,ℓ_r}(σ₁^sign, σ₂^sign) | (δ, σ₁^sign) ∈ Z ∧ (δ', σ₂^sign) ∈ Z' ∧ δ' = [δ, ℓ_c]}
φ^{sign2}_{ℓ_c,ℓ_r}(σ₁^sign, σ₂^sign) = {σ₂^sign[x ↦ σ₁^sign(x); y ↦ σ₁^sign(y); z ↦ σ₂^sign(y)]}
```

  `y` receives `{-, 0, +}` at entry per `[call]` (`§2.5.1`), while `f̂^{sign2}` restores formals `x, y` to
  pre-call `σ₁^sign` and copies callee result `σ₂^sign(y)` into actual `z`. ■
- Citation: [PPA Example 2.38, p. 97] (book p. 97; PDF p. 116)

### [U2b:2.5.4-d] Bounded call strings (`Δ = Lab^{≤k}`) (unnumbered definition)
- Statement: because recursion generates unbounded call chains, call strings are truncated to length `≤ k`
  (`k ≥ 0`): `Δ = Lab^{≤k}` with the same `ι̂`. When `k = 0`, `Δ = {Λ}` (no context information).
- Citation: [PPA §2.5.4, p. 97] (book p. 97; PDF p. 116)

### Example 2.39 — Bounded call strings for Fibonacci (`k = 1, 2`)
- Statement: `k = 1` gives 4 strings `Λ, [9], [4], [6]`; `k = 2` gives 8 strings
  `Λ, [9], [9,4], [9,6], [4,4], [4,6], [6,4], [6,6]`. ■
- Citation: [PPA Example 2.39, p. 97] (book p. 97; PDF p. 116); `k = 2` comparison on
  [PPA Example 2.39, p. 98] (book p. 98; PDF p. 117)

### [U2b:2.5.4-e] Bounded call-string transfer functions (`⌈δ, ℓ_c⌉_k`) (unnumbered definition)
- Statement:

```
f̂¹_{ℓ_c}(l̂)(δ')        = ⨆{f¹_{ℓ_c}(l̂(δ)) | δ' = ⌈δ, ℓ_c⌉_k}
f̂²_{ℓ_c,ℓ_r}(l̂, l̂')(δ) = f²_{ℓ_c,ℓ_r}(l̂(δ), l̂'(⌈δ, ℓ_c⌉_k))
```

  `⌈δ, ℓ_c⌉_k` retains the `≤ k` rightmost call labels of `[δ, ℓ_c]` by dropping older calls on the left.
  Because `δ ↦ ⌈δ, ℓ_c⌉_k` is non-injective, `f̂¹_{ℓ_c}` requires the least upper bound `⨆`.
- Citation: [PPA §2.5.4, p. 98] (book p. 98; PDF p. 117)

### Example 2.40 — Signs with bounded call strings (`k = 0` vs `k = 1`)
- Statement: for `k = 0` (`Δ = {Λ}`), `f̂^{sign2}_{ℓ_c,ℓ_r}(Y, Y') = ⋃{φ^{sign2}_{ℓ_c,ℓ_r}(σ₁^sign, σ₂^sign) | σ₁^sign ∈ Y ∧ σ₂^sign ∈ Y'}`
  (context-insensitive cross-product across callers); for `k = 1` (printed `Δ = Lab ∪ {Λ}`, `F-U2b-05`),
  `f̂^{sign1}_{ℓ_c}(Z)` tags all tuples with `{ℓ_c}` and `f̂^{sign2}_{ℓ_c,ℓ_r}(Z, Z')` matches `(ℓ_c, σ₂^sign) ∈ Z'`
  against `(δ, σ₁^sign) ∈ Z`, resetting context to caller `δ`. ■
- Citation: [PPA Example 2.40, p. 98] (book p. 98; PDF p. 117); `k = 1` equations on
  [PPA Example 2.40, p. 99] (book p. 99; PDF p. 118)

### Findings (2.5.4)
- F-U2b-05: on p. 98 Example 2.40 writes `Δ = Lab ∪ {Λ}` instead of length-`≤ 1` sequences `Lab★^{≤1}`
  and prints `"does not harm"` for `"does no harm"`; note also `Δ = Lab^*` fails ACC whenever `Lab` is
  non-empty, breaking worklist termination unless truncated (`Lab^{\le k}`) or restricted dynamically.
  [PPA Example 2.40, p. 98] (book p. 98; PDF p. 117)

### Projections (2.5.4)
- cs_theory: call strings preserve `[external: Dyck-stack]` suffixes of depth `k`; `Lab^*` violates ACC under recursion,
  while `Lab^{\le k}` restores finiteness of size `O(|Lab|^k)` at the cost of non-injective `⨆` merges.
- swe_architecture: pick `k` to exceed wrapper-nesting depth on non-recursive helpers; inside recursive cycles,
  distinct-call-site `k` (Exercise 2.16) or summary tabulation (`§2.5.5`) beats increasing `k` linearly.
- practical_debugging: if `k = 1` fails to prevent cross-over across two-level wrappers (`handler → helper → sink`)
  or inside recursion (`[4,4]`), trace `⌈δ, ℓ_c⌉_k` truncation on the offending call chain.
- cyber: shallow `k`-CFA (`k = 0, 1`) causes false-positive taint smearing when trusted config paths and
  attacker-controlled paths invoke the same utility at depth `> k` (analogous to Chapter 3's `k`-CFA cost/precision,
  `BKL-007`).

## 2.5.5 Assumption Sets as Context

Context: data-dependent context (`Δ = 𝒫(D)` large assumption sets and `Δ = D` small assumption sets),
and the non-monotonicity snag of exact caller-state fibers [PPA §2.5.5, p. 99] (book p. 99; PDF p. 118).

### [U2b:2.5.5-a] Simplifying assumption `L = 𝒫(D)` (unnumbered convention)
- Statement: assumes `L = 𝒫(D)` and isomorphic `L̂ = 𝒫(Δ × D)` throughout `§2.5.5`, abstracting only the
  last call (`k = 1`-equivalent depth) by call-site data rather than control labels.
- Citation: [PPA §2.5.5, p. 99] (book p. 99; PDF p. 118)

### [U2b:2.5.5-b] Large assumption sets (`Δ = 𝒫(D)`) (unnumbered definition)
- Statement:

```
Δ = 𝒫(D),     ι̂ = {({ι}, ι)}   [printed; see F-U2b-06]
```

  Expresses dependency on *data* (which set of abstract states may hold at the call site).
- Citation: [PPA §2.5.5, p. 99] (book p. 99; PDF p. 118)

### Example 2.41 — Large assumption sets for Fibonacci
- Statement: considers Detection of Signs on Fibonacci (`Example 2.33`) with printed `ι_sign = [x ↦ +, y ↦ -, z ↦ -]`
  and sample call states varying `y ∈ {0, +}` and `z ∈ {-, 0, +}` (see `F-U2b-06`). ■
- Citation: [PPA Example 2.41, p. 99] (book p. 99; PDF p. 118)

### [U2b:2.5.5-c] Large assumption-set transfer functions (unnumbered definition)
- Statement: with `φ¹_{ℓ_c} : D → 𝒫(D)` and `φ²_{ℓ_c,ℓ_r} : D × D → 𝒫(D)`:

```
f̂¹_{ℓ_c}(Z)        = ⋃{{δ'} × φ¹_{ℓ_c}(d)      | (δ, d) ∈ Z ∧ δ' = {d'' | (δ, d'') ∈ Z}}
f̂²_{ℓ_c,ℓ_r}(Z, Z') = ⋃{{δ} × φ²_{ℓ_c,ℓ_r}(d, d') | (δ, d) ∈ Z ∧ (δ', d') ∈ Z' ∧ δ' = {d'' | (δ, d'') ∈ Z}}
```

- Citation: [PPA §2.5.5, p. 100] (book p. 100; PDF p. 119)

### [U2b:2.5.5-d] Non-monotonicity snag and three remedies (unnumbered theorem/remark)
- Statement: `f̂¹_{ℓ_c}` and `f̂²_{ℓ_c,ℓ_r}` above "are in general not monotone!" (adding a new state
  `(δ, d_new)` to `Z` changes `δ'` from `{d₁}` to `{d₁, d_new}`, dropping previously produced `( {d₁}, ... )`
  pairs). Three remedies are named:
  1. generalised solvers for *weakly monotonic* equation systems (`[51, 52]` on p. 129);
  2. monotone relaxation replacing `δ' = {d'' | (δ, d'') ∈ Z}` with `δ' ⊆ {d'' | (δ, d'') ∈ Z}`; or
  3. small assumption sets (`Δ = D`).
- Citation: [PPA §2.5.5, p. 100] (book p. 100; PDF p. 119)

### [U2b:2.5.5-e] Small assumption sets (`Δ = D`) (unnumbered definition)
- Statement:

```
Δ = D,     ι̂ = {(ι, ι)}   [printed; see F-U2b-06]   (L̂ = 𝒫(D × D))
f̂¹_{ℓ_c}(Z)        = ⋃{{d} × φ¹_{ℓ_c}(d)        | (δ, d) ∈ Z}
f̂²_{ℓ_c,ℓ_r}(Z, Z') = ⋃{{δ} × φ²_{ℓ_c,ℓ_r}(d, d') | (δ, d) ∈ Z ∧ (d, d') ∈ Z'}
```

  Reduces property size from `𝒫(𝒫(D) × D)` to `𝒫(D × D)` and is monotone (though unable to group states).
- Citation: [PPA §2.5.5, p. 100] (book p. 100; PDF p. 119); transfer equations on
  [PPA §2.5.5, p. 101] (book p. 101; PDF p. 120)

### Findings (2.5.5)
- F-U2b-06 (`BKL-003` related): on pp. 99–100 `L = 𝒫(D)` makes `ι ⊆ D`, so `ι̂ = {({ι}, ι)}` (p. 99) and
  `ι̂ = {(ι, ι)}` (p. 100) are ill-typed unless `ι` is singleton `{d₀}` (`[derived]`: well-typed forms are
  `{(ι, d) | d ∈ ι}` for large and `{(d, d) | d ∈ ι}` for small assumption sets). Additionally `Example 2.41`
  (p. 99) omits set braces on `ι_sign`, drops formals `u, v` of `Example 2.33`, and varies global `y ∈ {0, +}`
  where `Example 2.33` keeps `y ↦ -` at calls `9, 4, 6` and varies formal `u`!
  [PPA §2.5.5, p. 99] (book p. 99; PDF p. 118); [PPA §2.5.5, p. 100] (book p. 100; PDF p. 119)

### Projections (2.5.5)
- cs_theory: small assumption sets `𝒫(D × D)` tabulate relational transformer summaries (`[155]`, `IFDS`
  [external]) completely additively over `D`, whereas large assumption sets attempt full `𝒫(D) → 𝒫(D)`
  grouping and break monotonicity via exact-fiber comprehension (`BKL-003`, `BKL-014`).
- swe_architecture: implement relational procedure summaries (`Δ = D`) when `D` is compact (e.g. bit-vector
  taint facts) so `O(|E| · |D|^3)` [external] tabulation replaces exponential call strings.
- practical_debugging: if a custom Datalog or worklist engine (`BKL-003`) oscillates or shrinks on growing
  call states, audit every context-key aggregation (`δ' = {d'' | ...}`) and replace equality with `⊆`
  monotone subset closure or per-fact `(d_entry, d_curr)` tabulation.
- cyber: small assumption sets keep taint/sanitizer summaries polynomial in `|D|` across arbitrarily deep
  recursive parsers (`k` would saturate), avoiding exponential timeouts and missed cross-recursion sinks.

## 2.5.6 Flow-Sensitivity versus Flow-Insensitivity

Context: statement-order-invariant abstractions, `AV`, `CP`, procedure call graph, and `IAV(p)`
[PPA §2.5.6, p. 101] (book p. 101; PDF p. 120).

### [U2b:2.5.6-a] Flow-sensitive versus flow-insensitive analysis (unnumbered definition)
- Statement: an analysis is *flow-sensitive* if `S₁; S₂` and `S₂; S₁` can produce different results, and
  *flow-insensitive* if it ignores statement order (motivated by dropping `kill` sets), gaining lower cost
  at the price of lower precision.
- Citation: [PPA §2.5.6, p. 101] (book p. 101; PDF p. 120)

### [U2b:2.5.6-b] `IAV(p)` objective (unnumbered specification)
- Statement: for each `proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}`, compute `IAV(p)`, the set of global
  variables that may be assigned directly or indirectly when `p` is called.
- Citation: [PPA §2.5.6, p. 101] (book p. 101; PDF p. 120)

### [U2b:2.5.6-c] Directly assigned variables `AV(S)` (unnumbered definition)
- Statement (by structural induction on `S`, ignoring callee bodies):

```
AV([skip]^ℓ) = ∅,   AV([x:=a]^ℓ) = {x},   AV([call p(a,z)]^{ℓ_c}_{ℓ_r}) = {z}
AV(S₁; S₂) = AV(S₁) ∪ AV(S₂),   AV(if [b]^ℓ then S₁ else S₂) = AV(S₁) ∪ AV(S₂),   AV(while [b]^ℓ do S) = AV(S)
```

- Citation: [PPA §2.5.6, p. 101] (book p. 101; PDF p. 120); equations on
  [PPA §2.5.6, p. 102] (book p. 102; PDF p. 121)

### [U2b:2.5.6-d] Immediately called procedures `CP(S)` and procedure call graph (unnumbered definition)
- Statement:

```
CP([skip]^ℓ) = CP([x:=a]^ℓ) = ∅,   CP([call p(a,z)]^{ℓ_c}_{ℓ_r}) = {p}
CP(S₁; S₂) = CP(S₁) ∪ CP(S₂),   CP(if [b]^ℓ then S₁ else S₂) = CP(S₁) ∪ CP(S₂),   CP(while [b]^ℓ do S) = CP(S)
```

  The *procedure call graph* has vertices `{p in D⋆} ∪ {main⋆}` and directed edges `p → p'` (`p' ∈ CP(S_p)`)
  and `main⋆ → p'` (`p' ∈ CP(S⋆)`).
- Citation: [PPA §2.5.6, p. 102] (book p. 102; PDF p. 121)

### [U2b:2.5.6-e] Equations for `IAV(p)` (unnumbered definition)
- Statement: for `proc p(val x, res y) is^{ℓ_n} S end^{ℓ_x}` in `D⋆` (seeking the *least* solution):

```
IAV(p) = (AV(S) \ {x}) ∪ ⋃{IAV(p') | p' ∈ CP(S)}     [printed; omits \ {y}, see F-U2b-07]
```

- Citation: [PPA §2.5.6, p. 102] (book p. 102; PDF p. 121)

### Figure 2.11 — Procedure call graph for example program
- Content: vertices `main⋆`, `fib`, `add`; directed edges `main⋆ → fib`, `fib → add`, and self-loop `fib → fib`.
- Citation: [PPA Figure 2.11, p. 103] (book p. 103; PDF p. 122)

### Example 2.42 — `IAV` for Fibonacci variant
- Statement: unlabelled program with `fib(val z)` (calls `add(1)` or recursive `fib`), `add(val u)`
  (`y := y + u; u := 0`), and `main` (`y := 0; call fib(x)`): equations `IAV(fib) = (∅ \ {z}) ∪ IAV(fib) ∪ IAV(add)`
  and `IAV(add) = {y, u} \ {u}`. Least solution `IAV(fib) = IAV(add) = {y}`; greatest solution is
  `Var⋆` ("completely unusable"). ■
- Citation: [PPA Example 2.42, p. 103] (book p. 103; PDF p. 122)

### [U2b:2.5.6-f] Statement-level attachment and link to annotated types (unnumbered remark)
- Statement: `AV`, `CP`, and `IAV` attach one summary per statement/procedure rather than entry/exit pairs
  (linking back to Chapter 1's Type and Effect annotations, Table 1.2 vs Table 1.3).
- Citation: [PPA §2.5.6, p. 103] (book p. 103; PDF p. 122)

### Findings (2.5.6)
- F-U2b-07: `§2.5.6` commits two errors on pp. 102–103: (1) prose on pp. 102 and 103 prints `"context-insensitive"`
  where **flow-insensitive** (statement-order invariance, §2.5.6's own term on p. 101) is meant; (2)
  `IAV(p) = (AV(S) \ {x}) ∪ ...` on p. 102 omits `\ {y}` for formal `res y`, causing local result writes
  in `S` to leak as global side effects (masked in Example 2.42 because `fib` and `add` omit `res`
  parameters!). Also, the `.` periods on p. 102 are corrupted to `o` in the OCR text layer.
  [PPA §2.5.6, p. 102] (book p. 102; PDF p. 121); [PPA §2.5.6, p. 103] (book p. 103; PDF p. 122)

### Projections (2.5.6)
- cs_theory: `IAV` computes transitive graph reachability (`lfp`) over the procedure call graph; greatest
  fixed point (`Var⋆`) fails due to self-cycles (`fib → fib`, Figure 2.11).
- swe_architecture: run cheap flow-insensitive `[external: mod-ref]` (`IAV`) and call-graph (`CP`) summaries as pre-passes
  to skip unaffected globals in downstream flow-sensitive passes (`[external]`).
- practical_debugging: subtracting only `val` formals (`\ {x}`) in `IAV` leaks `res` out-parameter mutations
  into global kill sets across callers; exclude all formal parameters and locals of `p`.
- cyber: call graphs built from syntactic `CP(S)` miss indirect calls (`BKL-008`), while `IAV` serves as
  a fast global-state tamper pre-filter before expensive path/heap checks.

---

## 2.6 Shape Analysis

Context: extending `WHILE` with single-selector heap cells, concrete heap SOS (`§2.6.1`), finite compatible
shape graphs `SG = (S, H, is)` (`§2.6.2`), and the distributive strongly-updating `Shape` framework (`§2.6.3`)
[PPA §2.6, p. 104] (book p. 104; PDF p. 123).

### [U2b:2.6-a] Motivation and guarantees of Shape Analysis (unnumbered remark)
- Statement: intraprocedural analysis computing a finite characterisation of dynamically allocated heap shapes
  to support optimisations, detect guaranteed `nil`-pointer dereferences, and verify shape invariants such as
  in-situ list reversal preserving non-cyclicity.
- Citation: [PPA §2.6, p. 104] (book p. 104; PDF p. 123)

### [U2b:2.6-b] Pointer-language syntax (unnumbered definition)
- Statement: over finite non-empty selector set `sel ∈ Sel` (one selector level only; no pointer arithmetic):

```
p ::= x | x.sel
a ::= p | n | a₁ op_a a₂ | nil
b ::= true | false | not b | b₁ op_b b₂ | a₁ op_r a₂ | op_p p
S ::= [p:=a]^ℓ | [skip]^ℓ | S₁; S₂ | if [b]^ℓ then S₁ else S₂ | while [b]^ℓ do S | [malloc p]^ℓ
```

  `op_r` includes pointer equality; unary pointer predicates `op_p` include `is-nil` and `has-sel`; expressions
  only read the heap and cannot mutate or allocate (`[U2b:2.6-b]`, p. 105; see `BKL-005`).
- Citation: [PPA §2.6, p. 104] (book p. 104; PDF p. 123); pointer-expression restrictions on
  [PPA §2.6, p. 105] (book p. 105; PDF p. 124)

### Example 2.43 — In-situ list reversal
- Statement: reverses list in `x` into `y`:

```
[y:=nil]^1;
while [not is-nil(x)]^2 do
      ([z:=y]^3; [y:=x]^4; [x:=x.cdr]^5; [y.cdr:=z]^6);
[z:=nil]^7
```

  ■
- Citation: [PPA Example 2.43, p. 105] (book p. 105; PDF p. 124)

### Projections (2.6 Opening)
- cs_theory: restricting syntax to one-level field accesses (`x.sel`) without pointer arithmetic isolates
  finite-abstraction heap graph transformations cleanly for relational shape invariants (`BKL-005`).
- swe_architecture: compile multi-level chains (`x.a.b` [external]) to one-level temporaries at IR lowering
  before invoking `Shape`.
- practical_debugging: because pointer arithmetic, interior pointers, and union type punning (`BKL-005`) are
  absent from the source calculus, any C/C++ front-end lowering into `Shape` must conservatively model them.
- cyber: one-level field graphs expose linked-structure invariants (`list`/`tree` non-cyclicity) and
  null-dereference targets directly, but real-world C `offsetof`/container arithmetic falls outside scope
  (`BKL-005`).

## 2.6.1 Structural Operational Semantics (Pointer Language)

Context: concrete domains `State` and `Heap`, partial expression evaluation `℘, 𝒜, ℬ`, statement SOS
rules, and limited garbage reuse [PPA §2.6.1, p. 105] (book p. 105; PDF p. 124).

### [U2b:2.6.1-a] Locations and pointer states (unnumbered definition)
- Statement: infinite set `ξ ∈ Loc`; states `σ ∈ State = Var⋆ → (Z + Loc + {◇})` where `◇` represents `nil`.
- Citation: [PPA §2.6.1, p. 105] (book p. 105; PDF p. 124); `State` formula on
  [PPA §2.6.1, p. 106] (book p. 106; PDF p. 125)

### Figure 2.12 — Reversal of a list of five elements
- Content: six concrete snapshots (rows `0..5`) before entry to loop test `2` (`car` fields omitted; arrows
  are `cdr`, `◇` is `nil`, `z` unmapped in rows `0–1`):
  - Row `0`: `x → ξ₁ → ξ₂ → ξ₃ → ξ₄ → ξ₅ → ◇`, `y → ◇`
  - Row `1`: `x → ξ₂ → ξ₃ → ξ₄ → ξ₅ → ◇`, `y → ξ₁ → ◇`, `z → ◇`
  - Row `2`: `x → ξ₃ → ξ₄ → ξ₅ → ◇`, `y → ξ₂ → ξ₁ → ◇`, `z → ξ₁`
  - Row `3`: `x → ξ₄ → ξ₅ → ◇`, `y → ξ₃ → ξ₂ → ξ₁ → ◇`, `z → ξ₂`
  - Row `4`: `x → ξ₅ → ◇`, `y → ξ₄ → ξ₃ → ξ₂ → ξ₁ → ◇`, `z → ξ₃`
  - Row `5`: `x → ◇`, `y → ξ₅ → ξ₄ → ξ₃ → ξ₂ → ξ₁ → ◇`, `z → ξ₄`
- Citation: [PPA Figure 2.12, p. 106] (book p. 106; PDF p. 125)

### [U2b:2.6.1-b] Concrete heaps `ℋ` (unnumbered definition)
- Statement: `ℋ ∈ Heap = (Loc × Sel) →_fin (Z + Loc + {◇})`, partial finite-domain maps so selector
  fields of newly allocated cells start undefined.
- Citation: [PPA §2.6.1, p. 106] (book p. 106; PDF p. 125); undefined fields note on
  [PPA §2.6.1, p. 107] (book p. 107; PDF p. 126)

### [U2b:2.6.1-c] Pointer expression valuation `℘` (unnumbered definition)
- Statement (`→_fin` printed; see `F-U2b-08`):

```
℘ : PExp⋆ → (State × Heap) →_fin (Z + {◇} + Loc)
℘⟦x⟧(σ, ℋ)     = σ(x)
℘⟦x.sel⟧(σ, ℋ) = ℋ(σ(x), sel)   if σ(x) ∈ Loc and ℋ is defined on (σ(x), sel)
                 undef          if σ(x) ∉ Loc or ℋ is undefined on (σ(x), sel)
```

- Citation: [PPA §2.6.1, p. 107] (book p. 107; PDF p. 126)

### Example 2.44 — Reading Figure 2.12
- Statement: ovals = heap cells `ξ`; unlabelled edges = `σ` (`x → ◇` means `σ(x) = ◇`); labelled edges = `ℋ`
  (`ξ —sel→ ◇` means `ℋ(ξ, sel) = ◇`). In row 0, `℘⟦x.cdr⟧(σ, ℋ) = ξ₂`. ■
- Citation: [PPA Example 2.44, p. 107] (book p. 107; PDF p. 126)

### [U2b:2.6.1-d] Arithmetic and boolean expression semantics `𝒜, ℬ` (unnumbered definition)
- Statement (`→_fin` printed; see `F-U2b-08`):

```
𝒜 : AExp → (State × Heap) →_fin (Z + Loc + {◇}),     ℬ : BExp → (State × Heap) →_fin T
𝒜⟦p⟧(σ, ℋ) = ℘⟦p⟧(σ, ℋ),   𝒜⟦n⟧(σ, ℋ) = 𝒩⟦n⟧,   𝒜⟦a₁ op_a a₂⟧(σ, ℋ) = 𝒜⟦a₁⟧(σ, ℋ) op_a 𝒜⟦a₂⟧(σ, ℋ),   𝒜⟦nil⟧(σ, ℋ) = ◇
ℬ⟦a₁ op_r a₂⟧(σ, ℋ) = 𝒜⟦a₁⟧(σ, ℋ) op_r 𝒜⟦a₂⟧(σ, ℋ),   ℬ⟦op_p p⟧(σ, ℋ) = op_p(℘⟦p⟧(σ, ℋ))
is-nil(v) = tt  if v = ◇;   ff  otherwise
```

  `op_a` is undefined unless both operands are in `Z`; `op_r` is undefined unless both are in `Z` or both
  are pointers (`Loc + {◇}`).
- Citation: [PPA §2.6.1, p. 107] (book p. 107; PDF p. 126); clauses on [PPA §2.6.1, p. 108] (book p. 108; PDF p. 127)

### [U2b:2.6.1-e] SOS rules for pointer assignments (unnumbered definition)
- Statement:

```
⟨[x:=a]^ℓ, σ, ℋ⟩ → ⟨σ[x ↦ 𝒜⟦a⟧(σ, ℋ)], ℋ⟩             if 𝒜⟦a⟧(σ, ℋ) is defined
⟨[x.sel:=a]^ℓ, σ, ℋ⟩ → ⟨σ, ℋ[(σ(x), sel) ↦ 𝒜⟦a⟧(σ, ℋ)]⟩ if σ(x) ∈ Loc and 𝒜⟦a⟧(σ, ℋ) is defined
```

  Note configurations stick (`undef` / type error / `nil` dereference) when side conditions fail.
- Citation: [PPA §2.6.1, p. 108] (book p. 108; PDF p. 127); `σ(x) ∈ Loc` remark on
  [PPA §2.6.1, p. 109] (book p. 109; PDF p. 128)

### [U2b:2.6.1-f] SOS rules for `malloc` (unnumbered definition)
- Statement:

```
⟨[malloc x]^ℓ, σ, ℋ⟩ → ⟨σ[x ↦ ξ], ℋ⟩                    where ξ does not occur in σ or ℋ
⟨[malloc (x.sel)]^ℓ, σ, ℋ⟩ → ⟨σ, ℋ[(σ(x), sel) ↦ ξ]⟩   where ξ does not occur in σ or ℋ and σ(x) ∈ Loc
```

  New `ξ` has all fields `ℋ(ξ, sel)` initially undefined.
- Citation: [PPA §2.6.1, p. 109] (book p. 109; PDF p. 128)

### [U2b:2.6.1-g] Remark — Limited garbage location reuse (unnumbered Remark)
- Statement: **Remark.** In `[malloc x]¹; [x:=nil]²; [malloc y]³`, `ξ` from `1` is absent from `σ` and `ℋ`
  after `2`, so it may be reused at `3`; in `[malloc x]¹; [x.cdr:=nil]²; [x:=nil]³; [malloc y]⁴`, `ξ` still
  occurs in `dom(ℋ)` (mapping `(ξ, cdr) ↦ ◇`) so `[malloc y]⁴` cannot reuse `ξ` even though `ξ` is unreachable
  garbage. ■
- Citation: [PPA §2.6.1, p. 109] (book p. 109; PDF p. 128)

### Findings (2.6.1)
- F-U2b-08: on pp. 107–108, signatures of `℘`, `𝒜`, and `ℬ` use `→_fin` ("partial functions with finite domain")
  over infinite `State × Heap`, whereas `℘⟦x⟧(σ, ℋ) = σ(x)` and `𝒜⟦nil⟧(σ, ℋ) = ◇` are defined on infinitely
  many states/heaps (plain partial function arrow `⇀` is meant `[derived]`). Also `is-nil(v)` prints `ff`
  for integers `v ∈ Z` without clarifying `op_p` vs `op_r`. [PPA §2.6.1, p. 107] (book p. 107; PDF p. 126);
  [PPA §2.6.1, p. 108] (book p. 108; PDF p. 127)

### Projections (2.6.1)
- cs_theory: partial-function `℘, 𝒜, ℬ` turn type mismatches, uninitialised fields, and `nil` dereferences
  into stuck SOS configurations (distinct from §2.2.1's error-free total integer expressions).
- swe_architecture: `malloc` leaves fields undefined until initialised and forbids address reuse while fields
  persist in `ℋ`, cleanly separating allocation from GC (`Exercise 2.24`).
- practical_debugging: uninitialised struct fields behave identically to `nil` under dereference (`stuck`) but
  `is-nil` only matches `◇` (`undef` propagates unless explicitly caught).
- cyber: stuck states in `⟨[x.sel := a]^ℓ, ...⟩` (`σ(x) ∉ Loc`) and `℘⟦x.sel⟧` precisely define `[external: CWE-476]` NULL
  pointer dereference and type-confusion crash conditions; finite-location reuse limits avoid modeling
  use-after-free unless an explicit `free` rule re-exposes `dom(ℋ)` cells [external].

## 2.6.2 Shape Graphs

Context: finite abstract locations `ALoc`, abstract summary node `n_∅`, sharing component `is`, and all five
compatibility invariants defining lattice `(𝒫(SG), ⊆, ∪)` [PPA §2.6.2, p. 109] (book p. 109; PDF p. 128).

### [U2b:2.6.2-a] Shape graph triple `(S, H, is)` (unnumbered definition)
- Statement: finite abstraction of unbounded heaps consisting of abstract state `S`, abstract heap `H`, and
  sharing subset `is`, constrained by five invariants.
- Citation: [PPA §2.6.2, p. 109] (book p. 109; PDF p. 128)

### [U2b:2.6.2-b] Abstract locations `ALoc` and summary location `n_∅` (unnumbered definition)
- Statement:

```
ALoc = {n_X | X ⊆ Var⋆}
```

  If `x ∈ X`, `n_X` represents the single concrete location `σ(x)`; *abstract summary location* `n_∅`
  represents all heap locations not directly reachable from any variable in `Var⋆`. Distinct abstract locations
  in one shape graph always represent disjoint sets of concrete locations.
- Citation: [PPA §2.6.2, p. 110] (book p. 110; PDF p. 129)

### [U2b:2.6.2-c] Invariant 1 — Disjoint variable-set naming (locally numbered invariant)
- Statement: "**Invariant 1.** If two abstract locations `n_X` and `n_Y` occur in the same shape graph then
  either `X = Y` or `X ∩ Y = ∅`." Proved inline by contradiction if `z ∈ X ∩ Y` (`σ(z)` would lie in two
  disjoint sets).
- Citation: [PPA §2.6.2, p. 110] (book p. 110; PDF p. 129)

### Example 2.45 — Abstract locations for row 2 of Figure 2.12
- Statement: `ξ₃, ξ₂, ξ₁` are represented by `n_{x}`, `n_{y}`, `n_{z}`, while unreachable-from-state `ξ₄, ξ₅`
  collapse into `n_∅`. ■
- Citation: [PPA Example 2.45, p. 110] (book p. 110; PDF p. 129)

### [U2b:2.6.2-d] Invariant 2 and `AState` (locally numbered invariant)
- Statement: "**Invariant 2.** If `x` is mapped to `n_X` by the abstract state then `x ∈ X`." States/heaps
  do not distinguish integers, `nil` pointers, or uninitialised fields (none appear in `S` or `H`):

```
S ∈ AState = 𝒫(Var⋆ × ALoc),     ALoc(S) = {n_X | ∃x : (x, n_X) ∈ S}
```

- Citation: [PPA §2.6.2, p. 110] (book p. 110; PDF p. 129); `AState` oversizing remark on
  [PPA §2.6.2, p. 111] (book p. 111; PDF p. 130)

### [U2b:2.6.2-e] `AHeap` and Invariant 3 — Deterministic selectors off non-summary nodes (locally numbered invariant)
- Statement:

```
H ∈ AHeap = 𝒫(ALoc × Sel × ALoc),     ALoc(H) = {n_V, n_W | ∃sel : (n_V, sel, n_W) ∈ H}
```

  "**Invariant 3.** Whenever `(n_V, sel, n_W)` and `(n_V, sel, n_W')` are in the abstract heap then either
  `V = ∅` or `W = W'`." Only summary node `n_∅` may carry multiple outgoing edges sharing a selector `sel`.
- Citation: [PPA §2.6.2, p. 111] (book p. 111; PDF p. 130)

### Example 2.46 — Shape graph for row 2 of Figure 2.12
- Statement: `S₂ = {(x, n_{x}), (y, n_{y}), (z, n_{z})}`, `H₂ = {(n_{x}, cdr, n_∅), (n_∅, cdr, n_∅), (n_{y}, cdr, n_{z})}`
  (`z.cdr = ◇` has no edge in `H₂`). Across rows 0–5, `n_∅` dynamically holds `{ξ₂..ξ₅}`, `{ξ₃..ξ₅}`, `{ξ₄,ξ₅}`,
  `{ξ₁,ξ₅}`, `{ξ₁,ξ₂}`, `{ξ₁,ξ₂,ξ₃}`. ■
- Citation: [PPA Example 2.46, p. 111] (book p. 111; PDF p. 130); dynamic association remark on
  [PPA Example 2.46, p. 112] (book p. 112; PDF p. 131)

### Figure 2.13 — Shape graphs corresponding to Figure 2.12
- Content (all boxes fat, i.e., `is = ∅`):
  - Row `0`: `S = {(x,n_{x})}`, `H = {(n_{x},cdr,n_∅), (n_∅,cdr,n_∅)}`
  - Row `1`: `S = {(x,n_{x}), (y,n_{y})}`, `H = {(n_{x},cdr,n_∅), (n_∅,cdr,n_∅)}`
  - Row `2`: `S = {(x,n_{x}), (y,n_{y}), (z,n_{z})}`, `H = {(n_{x},cdr,n_∅), (n_∅,cdr,n_∅), (n_{y},cdr,n_{z})}`
  - Row `3`: `S = {(x,n_{x}), (y,n_{y}), (z,n_{z})}`, `H = {(n_{x},cdr,n_∅), (n_{y},cdr,n_{z}), (n_{z},cdr,n_∅)}`
  - Row `4`: `S = {(x,n_{x}), (y,n_{y}), (z,n_{z})}`, `H = {(n_∅,cdr,n_∅), (n_{y},cdr,n_{z}), (n_{z},cdr,n_∅)}`
  - Row `5`: `S = {(y,n_{y}), (z,n_{z})}`, `H = {(n_∅,cdr,n_∅), (n_{y},cdr,n_{z}), (n_{z},cdr,n_∅)}`
- Citation: [PPA Figure 2.13, p. 112] (book p. 112; PDF p. 131)

### [U2b:2.6.2-f] Heap-sharing set `is` (unnumbered definition)
- Statement: `n_X ∈ is` (double box in diagrams) indicates `n_X` may represent a location targeted by two
  or more pointers *from within the heap* (`S` and `H` alone cannot distinguish Figure 2.14 top vs middle).
- Citation: [PPA §2.6.2, p. 112] (book p. 112; PDF p. 131)

### Figure 2.14 — Sharing information
- Content: three concrete/abstract pairs (edges `cdr`):
  - Top: `x→ξ₁→ξ₂→ξ₃→ξ₄→ξ₅→◇, y→ξ₅` maps to `S={(x,n_{x}),(y,n_{y})}, H={(n_{x},cdr,n_∅),(n_∅,cdr,n_∅),(n_∅,cdr,n_{y})}` with `is = ∅` (`n_{y}` fat).
  - Middle: `x→ξ₁→ξ₂→ξ₃→ξ₅, ξ₄→ξ₅→◇, y→ξ₅` maps to **identical** `(S, H)` but `is = {n_{y}}` (`n_{y}` double box).
  - Bottom: `ξ₂→ξ₃→ξ₄→ξ₅, x→ξ₁→ξ₅→◇, y→ξ₅` maps to `H={(n_{x},cdr,n_{y}), (n_∅,cdr,n_∅), (n_∅,cdr,n_{y})}`, `is = {n_{y}}` (`n_{y}` double box).
- Citation: [PPA Figure 2.14, p. 113] (book p. 113; PDF p. 132)

### [U2b:2.6.2-g] Invariant 4 — Sharing must be heap-witnessed (locally numbered invariant)
- Statement: "**Invariant 4.** If `n_X ∈ is` then either (a) `(n_∅, sel, n_X)` is in the abstract heap for
  some `sel`, or (b) there exists [sic] two distinct triples `(n_V, sel₁, n_X)` and `(n_W, sel₂, n_X)` in the
  abstract heap (`sel₁ ≠ sel₂` or `V ≠ W`)."
- Citation: [PPA §2.6.2, p. 113] (book p. 113; PDF p. 132)

### [U2b:2.6.2-h] Invariant 5 — Unambiguous multiple heap edges force `is` (locally numbered invariant)
- Statement: "**Invariant 5.** Whenever there are two distinct triples `(n_V, sel₁, n_X)` and `(n_W, sel₂, n_X)`
  in the abstract heap and `n_X ≠ n_∅` then `n_X ∈ is`." Inverse of 4(b) for `X ≠ ∅`; 4(a) has no inverse.
- Citation: [PPA §2.6.2, p. 113] (book p. 113; PDF p. 132); non-inverse of 4(a) on
  [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133)

### [U2b:2.6.2-i] Meaning of `is` on `n_∅` vs `n_X` (unnumbered remark)
- Statement: `n_∅ ∉ is` guarantees every concrete cell in `n_∅` has at most one incoming heap pointer, whereas
  `n_∅ ∈ is` means some cell in `n_∅` *might* have `≥ 2`; `(n_∅, sel, n_X) ∈ H` alone never proves `n_X` shared.
- Citation: [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133)

### [U2b:2.6.2-j] Compatible shape graphs `SG` and lattice `𝒫(SG)` (unnumbered definition)
- Statement: `is ∈ IsShared = 𝒫(ALoc)`. `(S, H, is)` is a *compatible shape graph* iff:

```
1. ∀n_V, n_W ∈ ALoc(S) ∪ ALoc(H) ∪ is : (V = W) ∨ (V ∩ W = ∅)
2. ∀(x, n_X) ∈ S : x ∈ X
3. ∀(n_V, sel, n_W), (n_V, sel, n_W') ∈ H : (V = ∅) ∨ (W = W')
4. ∀n_X ∈ is : (∃sel : (n_∅, sel, n_X) ∈ H) ∨ (∃(n_V, sel₁, n_X), (n_W, sel₂, n_X) ∈ H : sel₁ ≠ sel₂ ∨ V ≠ W)
5. ∀(n_V, sel₁, n_X), (n_W, sel₂, n_X) ∈ H : ((sel₁ ≠ sel₂ ∨ V ≠ W) ∧ X ≠ ∅) ⇒ n_X ∈ is

SG = {(S, H, is) | (S, H, is) is compatible}
```

  `L = (𝒫(SG), ⊆, ∪)` is a finite complete lattice (`2^{|Var⋆|}` abstract locations).
- Citation: [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133)

### Figure 2.15 — Extremal value `ι` for list reversal
- Content: single fat-box graph `ι = {({(x, n_{x})}, {(n_{x}, cdr, n_∅), (n_∅, cdr, n_∅)}, ∅)}` (unshared
  list of at least two elements).
- Citation: [PPA Figure 2.15, p. 115] (book p. 115; PDF p. 134)

### Findings (2.6.2)
- F-U2b-09: on p. 113 Invariant 4 prints `"there exists two distinct triples"`, and commentary on Case 4(a)
  refers to `"second and third rows of Figure 2.14"` even though Figure 2.14's third (bottom) row has two
  distinct edges `(n_{x}, cdr, n_{y})` and `(n_∅, cdr, n_{y})` (Case 4(b)) while only `ξ₄` in `n_∅` targets
  `ξ₅`. Notice also the converse `x ∈ X ⇒ (x, n_X) ∈ S` is not explicitly listed among 1–5 on p. 114,
  though preserved by `ι` and all §2.6.3 transfer functions (`[derived]`).
  [PPA §2.6.2, p. 113] (book p. 113; PDF p. 132); [PPA Figure 2.14, p. 113] (book p. 113; PDF p. 132)

### Projections (2.6.2)
- cs_theory: Invariants 1–5 encode canonical unary abstraction over variable-membership predicates plus the
  heap-sharing instrumentation predicate `is` (foundation of TVLA [external], `[150]`).
- swe_architecture: implement `is_compatible(S, H, is)` checking Invariants 1–5 (plus `x ∈ X ⇒ (x, n_X) ∈ S`)
  as a mandatory property-based test invariant on every shape-graph transfer function.
- practical_debugging: because integers, `nil`, and uninitialised fields have *no* edges in `S` or `H`, an
  absent `x` binding means "non-pointer, `nil`, or undef" rather than "proven non-nil"; conversely, `n_{x,y}`
  without double box means two *stack variables* alias an unshared heap cell.
- cyber: Invariants 1–3 prove unique concrete cell identity for every named node `n_X` (`X ≠ ∅`), which is
  the exact precondition justifying strong nullification and strong capability updates in pointer/ownership checkers [external].

## 2.6.3 The Analysis (`Shape`)

Context: data flow equations for `Shape`, outer-may / inner-must design, `kill_x`, variable copying,
materialisation from `n_∅`, `kill_{x.sel}` unsharing, destructive updates, `malloc`, and temporary-variable
desugarings [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134).

### [U2b:2.6.3-a] Data flow equations for `Shape` (unnumbered definition)
- Statement: for label-consistent `S⋆` with isolated entries and extremal `ι ∈ 𝒫(SG)`:

```
Shape∘(ℓ) = ι                                   if ℓ = init(S⋆)
            ⋃{Shape•(ℓ') | (ℓ', ℓ) ∈ flow(S⋆)}  otherwise
Shape•(ℓ) = f_ℓ^SA(Shape∘(ℓ))
```

  Outer *may* analysis (`⋃`) combined with inner *must* absence-of-superfluous-edges inside each compatible
  shape graph gives *strong update* and *strong nullification*.
- Citation: [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134)

### Example 2.47 — Shape equations for list reversal
- Statement: for Example 2.43 with `ι` from Figure 2.15: `Shape•(1) = f₁^SA(ι)`,
  `Shape•(2) = f₂^SA(Shape•(1) ∪ Shape•(6))`, `Shape•(3) = f₃^SA(Shape•(2))`, ...,
  `Shape•(6) = f₆^SA(Shape•(5))`, `Shape•(7) = f₇^SA(Shape•(2))` (full graph computation deferred to
  `Exercise 2.21`). ■
- Citation: [PPA Example 2.47, p. 115] (book p. 115; PDF p. 134); completion on
  [PPA Example 2.47, p. 116] (book p. 116; PDF p. 135)

### [U2b:2.6.3-b] Elementwise transfer lifting `f_ℓ^SA` (unnumbered definition)
- Statement:

```
f_ℓ^SA(SG) = ⋃{φ_ℓ^SA((S, H, is)) | (S, H, is) ∈ SG}     (φ_ℓ^SA : SG → 𝒫(SG))
```

  Completely additive by construction (`[derived]`: `Shape` is a finite Distributive Framework, yielding `MFP = MOP` when `∀ℓ : path∘(ℓ) ≠ ∅` per `Lemma 2.32`, noting strictness `f_ℓ^SA(∅) = ∅` handles empty paths via `Exercise 2.13` `[derived]`).
- Citation: [PPA §2.6.3, p. 116] (book p. 116; PDF p. 135)

### [U2b:2.6.3-c] Transfer function for `[b]^ℓ` and `[skip]^ℓ` + Example 2.48 (unnumbered definition)
- Statement: `φ_ℓ^SA((S, H, is)) = {(S, H, is)}` (identity; ignores outcomes of pointer predicates like
  `not is-nil(x)`). Illustrated on `[not is-nil(x)]^2` in `Example 2.48`. ■
- Citation: [PPA §2.6.3, p. 116] (book p. 116; PDF p. 135); `Example 2.48` on
  [PPA Example 2.48, p. 116] (book p. 116; PDF p. 135)

### Figure 2.16 — Effect of `[x:=nil]^ℓ`
- Content: `(S, H, is)` has `x → n_{x}` (fat), `n_V —sel₁→ n_{x} —sel₂→ n_W`, and fat `n_∅` with unaffected
  unlabelled arcs; result `(S', H', is')` removes `x` and merges `n_{x}` into `n_∅` (`n_V —sel₁→ n_∅ —sel₂→ n_W`),
  remaining fat. Legend (`p. 117`): fat = unshared, double = possibly shared, thin = unaffected, unlabelled arcs = unaffected edges.
- Citation: [PPA Figure 2.16, p. 116] (book p. 116; PDF p. 135); box/arrow legend on
  [PPA §2.6.3, p. 117] (book p. 117; PDF p. 136)

### [U2b:2.6.3-d] `[x:=a]^ℓ` (`a` in `n, a₁ op_a a₂, nil`), `kill_x` & Examples 2.49–2.50, Remark (unnumbered definition)
- Statement: with `k_x(n_Z) = n_{Z \ {x}}`:

```
φ_ℓ^SA((S, H, is)) = {kill_x((S, H, is))}     where kill_x((S, H, is)) = (S', H', is'):
  S'  = {(z, k_x(n_Z)) | (z, n_Z) ∈ S ∧ z ≠ x}   [printed italic S; see F-U2b-10]
  H'  = {(k_x(n_V), sel, k_x(n_W)) | (n_V, sel, n_W) ∈ H}
  is' = {k_x(n_X) | n_X ∈ is}
```

  Provides *strong nullification* and preserves compatibility (`n_∅ ∉ is'` iff both `n_∅ ∉ is` and `n_{x} ∉ is`).
  `Example 2.49` (`[y:=nil]^1`, `p. 117`): `Shape•(1) = ι` (`y` absent). `Example 2.50` (`[z:=nil]^7`, `p. 117`):
  merges `n_{z}` into `n_∅`. **Remark.** (`p. 117`): no GC — unreachable cells merge into `n_∅` and retain outgoing pointers. ■
- Citation: [PPA §2.6.3, p. 117] (book p. 117; PDF p. 136); `Examples 2.49–2.50` on
  [PPA Example 2.49, p. 117] (book p. 117; PDF p. 136)

### Figure 2.17 — Effect of `[x:=y]^ℓ` (`x ≠ y`)
- Content: `(S, H, is)` has `x → n_X` (thin, unaffected arcs) and `y → n_Y` (fat) with `n_V —sel₁→ n_Y —sel₂→ n_W`;
  `(S'', H'', is'')` strips `x` from `n_X` (`n_{X\{x}}` retains arcs) and renames `n_Y ↦ n_{Y∪{x}}` (fat) with both `x, y → n_{Y∪{x}}`.
- Citation: [PPA Figure 2.17, p. 118] (book p. 118; PDF p. 137)

### [U2b:2.6.3-f] Transfer function for `[x:=y]^ℓ` + Example 2.51 (unnumbered definition)
- Statement: if `x = y`, `f_ℓ^SA = id`. If `x ≠ y`, with `(S', H', is') = kill_x((S, H, is))` and
  `g_x^y(n_Z) = n_{Z∪{x}}` if `y ∈ Z` else `n_Z`:

```
φ_ℓ^SA((S, H, is)) = {(S'', H'', is'')}
  S''  = {(z, g_x^y(n_Z)) | (z, n_Z) ∈ S'} ∪ {(x, g_x^y(n_Y)) | (y', n_Y) ∈ S' ∧ y' = y}
  H''  = {(g_x^y(n_V), sel, g_x^y(n_W)) | (n_V, sel, n_W) ∈ H'}
  is'' = {g_x^y(n_Z) | n_Z ∈ is'}
```

  `n_{Y∪{x}}` inherits `is'` status of `n_Y` (`is` tracks heap sharing, not variable aliasing). Illustrated
  on `[z:=y]^3` and `[y:=x]^4` in `Example 2.51` (`p. 119`). ■
- Citation: [PPA §2.6.3, p. 118] (book p. 118; PDF p. 137); inheritance remark and `Example 2.51` on
  [PPA §2.6.3, p. 119] (book p. 119; PDF p. 138)

### [U2b:2.6.3-g..h] `[x:=y.sel]^ℓ`: self-desugaring & Case 1–3 partition + Example 2.52 (unnumbered definition)
- Statement: if `x = y`, desugar to `[t:=y.sel]^{ℓ₁}; [x:=t]^{ℓ₂}; [t:=nil]^{ℓ₃}` (`t` fresh) with
  `f_ℓ^SA = f_{ℓ₃}^SA ∘ f_{ℓ₂}^SA ∘ f_{ℓ₁}^SA` (`Example 2.52`: `[x:=x.cdr]^5`). For `x ≠ y`, compute
  `(S', H', is') = kill_x((S, H, is))` and split on `(S', H', is')`:
  1. `¬∃n_Y: (y, n_Y) ∈ S'` OR `(y, n_Y) ∈ S' ∧ ¬∃n_Z: (n_Y, sel, n_Z) ∈ H'` (`nil`/int/`undef` or missing `sel`);
  2. `(y, n_Y) ∈ S' ∧ (n_Y, sel, n_U) ∈ H'` with `n_U ≠ n_∅`;
  3. `(y, n_Y) ∈ S' ∧ (n_Y, sel, n_∅) ∈ H'`.
- Citation: [PPA §2.6.3, p. 119] (book p. 119; PDF p. 138); cases on [PPA §2.6.3, p. 120] (book p. 120; PDF p. 139)

### [U2b:2.6.3-i] `[x:=y.sel]^ℓ`, Case 1 (unnumbered definition)
- Statement: `φ_ℓ^SA((S, H, is)) = {kill_x((S, H, is))}` in both subcases (`y` unmapped or `n_Y.sel` absent);
  models error-capturing sound over-approximation without emitting a separate failure state.
- Citation: [PPA §2.6.3, p. 120] (book p. 120; PDF p. 139)

### Figure 2.18 & [U2b:2.6.3-j] `[x:=y.sel]^ℓ`, Case 2 (`n_U ≠ n_∅`) (unnumbered definition)
- Statement: `n_Y, n_U` are unique (`Y ≠ ∅` by Invariant 2; might equal `n_Y`). Rename `n_U` via
  `h_x^U(n_Z) = n_{U∪{x}}` if `Z = U` else `n_Z`:

```
φ_ℓ^SA((S, H, is)) = {(S'', H'', is'')}
  S''  = {(z, h_x^U(n_Z)) | (z, n_Z) ∈ S'} ∪ {(x, h_x^U(n_U))}
  H''  = {(h_x^U(n_V), sel', h_x^U(n_W)) | (n_V, sel', n_W) ∈ H'}
  is'' = {h_x^U(n_Z) | n_Z ∈ is'}
```

  `Figure 2.18` (`p. 120`) shows `x → n_X` (thin) + `y → n_Y —sel→ n_U` (double box, `n_V —sel₁→ n_U —sel₂→ n_W`)
  transforming to `n_{X\{x}}` + `x, y → n_{U∪{x}}` (double box preserving `n_U`'s sharing).
- Citation: [PPA Figure 2.18, p. 120] (book p. 120; PDF p. 139); formula on
  [PPA §2.6.3, p. 121] (book p. 121; PDF p. 140)

### [U2b:2.6.3-k..p] `[x:=y.sel]^ℓ`, Case 3 materialisation + Figures 2.19–2.20, Example 2.53 (unnumbered definition)
- Statement: derived from the round-trip equivalence `[x:=nil]; [x:=y.sel]^ℓ; [x:=nil]` demanding
  `kill_x((S'', H'', is'')) = (S', H', is')`:

```
φ_ℓ^SA((S, H, is)) = {(S'', H'', is'') | (S'', H'', is'') is compatible ∧
                                       kill_x((S'', H'', is'')) = (S', H', is') ∧
                                       (x, n_{x}) ∈ S'' ∧ (n_Y, sel, n_{x}) ∈ H''}
```

  Consequences proved (`pp. 122–124`):
  - State uniqueness (`p. 122`): `S'' = S' ∪ {(x, n_{x})}`;
  - Sharing preservation (`pp. 122–123`): `is' \ {n_∅} = is'' \ {n_∅, n_{x}}` and
    `n_∅ ∈ is' ⇔ (n_∅ ∈ is'' ∨ n_{x} ∈ is'')`;
  - Four-way edge classification under `k_x`-relatedness (`p. 123`): *external* (`∩ {n_∅, n_{x}} = ∅`, unchanged),
    *internal* (`⊆ {n_∅, n_{x}}`), *going-out* (`src ∈ {n_∅, n_{x}}, dst ∉`), and *going-in* (`src ∉, dst ∈`);
    `(n_Y, sel, n_∅)` becomes `(n_Y, sel, n_{x})` (impossible to keep `(n_Y, sel, n_∅)` by Invariant 3).
  - `Figures 2.19–2.20` (`pp. 123–124`) & `Example 2.53` (`p. 125`): with `n_∅, n_W ∉ is`, distinct `n_V, n_W ≠ n_∅`,
    `sel₂ ≠ sel₃`: `n_V —sel₁→ n_∅` (cannot hit unshared `n_{x}`), `sel₂ → n_W` splits 2 ways (from `n_{x}` OR
    `n_∅`, never both since `n_W ∉ is`), `sel₃ → n_∅` splits 3 ways (from `n_{x}`, `n_∅`, or both), giving `2 × 3 = 6`
    graphs `(S''_1..6, H''_1..6, is''_1..6)` (`i=1..6`). ■
- Citation: [PPA §2.6.3, p. 122] (book p. 122; PDF p. 141); `Figures 2.19–2.20` on
  [PPA Figure 2.19, p. 123] (book p. 123; PDF p. 142); [PPA Figure 2.20, p. 124] (book p. 124; PDF p. 143);
  `Example 2.53` on [PPA Example 2.53, p. 125] (book p. 125; PDF p. 144)

### [U2b:2.6.3-q..r] `[x.sel:=a]^ℓ` (`kill_{x.sel}`) + Figure 2.21, Remark (unnumbered definition)
- Statement: identity if `¬∃n_X: (x, n_X) ∈ S` or `¬∃n_U: (n_X, sel, n_U) ∈ H`. Otherwise (`n_X, n_U` unique, `X ≠ ∅`):

```
φ_ℓ^SA((S, H, is)) = {kill_{x.sel}((S, H, is))}   where (S', H', is') = kill_{x.sel}((S, H, is)):
  S'  = S
  H'  = {(n_V, sel', n_W) | (n_V, sel', n_W) ∈ H ∧ ¬(X = V ∧ sel = sel')}
  is' = is \ {n_U}   if n_U ∈ is ∧ #into(n_U, H') ≤ 1 ∧ ¬∃sel' : (n_∅, sel', n_U) ∈ H'
        is           otherwise
```

  Strong unsharing clears `n_U` from `is` iff at most 1 incoming edge remains AND no edge from `n_∅` targets `n_U`
  (`Figure 2.21`, `p. 126`, drawn with a slashed arrow `n_∅ ↛ n_U`). **Remark.** (`p. 126`): no GC — detached
  `n_U` persists in the graph. ■
- Citation: [PPA §2.6.3, p. 125] (book p. 125; PDF p. 144); `Figure 2.21` and `Remark.` on
  [PPA Figure 2.21, p. 126] (book p. 126; PDF p. 145)

### [U2b:2.6.3-s] Destructive pointer update `[x.sel:=y]^ℓ` + Figure 2.22, Example 2.54 (unnumbered definition)
- Statement: if `x = y`, desugar to `[t:=y]^{ℓ₁}; [x.sel:=t]^{ℓ₂}; [t:=nil]^{ℓ₃}`. For `x ≠ y`: identity if
  `¬∃n_X: (x, n_X) ∈ S`; `{kill_{x.sel}((S, H, is))}` if `(x, n_X) ∈ S` and `¬∃n_Y: (y, n_Y) ∈ S`; otherwise
  with `(S', H', is') = kill_{x.sel}((S, H, is))`:

```
φ_ℓ^SA((S, H, is)) = {(S'', H'', is'')}
  S''  = S'  (= S)
  H''  = H' ∪ {(n_X, sel, n_Y)}
  is'' = is' ∪ {n_Y}   if #into(n_Y, H') ≥ 1;   is'  otherwise
```

  `Figure 2.22` (`p. 127`) shows `#into(n_Y, H') = 0 < 1` leaving `n_Y` fat; `Example 2.54` (`p. 127`) transforms
  `Shape•(5)` across `[y.cdr:=z]^6`. ■
- Citation: [PPA §2.6.3, p. 126] (book p. 126; PDF p. 145); formula, `Figure 2.22`, and `Example 2.54` on
  [PPA §2.6.3, p. 127] (book p. 127; PDF p. 146)

### [U2b:2.6.3-t..u] Compound selector copy `[x.sel:=y.sel']^ℓ` and `[malloc p]^ℓ` (unnumbered definition)
- Statement: `[x.sel:=y.sel']^ℓ` desugars to `[t:=y.sel']^{ℓ₁}; [x.sel:=t]^{ℓ₂}; [t:=nil]^{ℓ₃}` (`p. 127`).
  For `[malloc x]^ℓ` (`p. 127`):

```
φ_ℓ^SA((S, H, is)) = {(S' ∪ {(x, n_{x})}, H', is')}   where (S', H', is') = kill_x(S, H, is)   [single parens]
```

  And `[malloc (x.sel)]^ℓ` (`p. 128`) desugars to `[malloc t]^{ℓ₁}; [x.sel:=t]^{ℓ₂}; [t:=nil]^{ℓ₃}`.
- Citation: [PPA §2.6.3, p. 127] (book p. 127; PDF p. 146); `[malloc (x.sel)]^ℓ` on
  [PPA §2.6.3, p. 128] (book p. 128; PDF p. 147)

### Findings (2.6.3)
- F-U2b-10: `p. 117` prints italic `S` in `(z, n_Z) ∈ S`; `p. 120` prints `"dereference a non-existing selector field of pointer"`;
  `p. 125` prints `"the cell pointed to by sel"` (meant: `sel`-field of cell pointed to by `x`); `pp. 126–127`
  Figures 2.21–2.22 use a slashed-arrow negated-edge symbol never added to the legends on `pp. 112, 117`;
  `p. 127` Figure 2.22 labels the right-hand graph `(S', H'', is'')` (`S'' = S'`) and illustrates `< 1` while prose
  mentions `≥ 1`, and text writes `"sequence of statement"` and single-paren `kill_x(S, H, is)`. Moreover,
  all three-step fresh-temporary `t` desugarings (`pp. 119, 126–128`) temporarily expand `Var⋆` to `Var⋆ ∪ {t}`
  until `[t:=nil]^{ℓ₃}` projects back to `Var⋆`.
  [PPA §2.6.3, p. 117] (book p. 117; PDF p. 136); [PPA Figure 2.22, p. 127] (book p. 127; PDF p. 146)

### Projections (2.6.3)
- cs_theory: `Shape` combines outer powerset `⊔ = ∪` with inner canonical compatible graphs, giving a
  completely additive (`MFP = MOP`) framework; Case 3 materialisation (`focus`/`coerce` in TVLA `[150]`)
  computes concrete-free inverse images `k_x^{-1}` filtered by Invariants 1–5.
- swe_architecture: compile `[x:=x.sel]`, `[x.sel:=x]`, `[x.sel:=y.sel']`, `[malloc (x.sel)]` to 3-step `t`
  sequences; consider Exercise 2.24 GC + Exercise 2.25 allocation-site `n_{ℓ,X}` or `[148, 149]` single-summary
  merging to curb `Exercise 2.21`'s `> 50`-graph explosion.
- practical_debugging: validate Case 3 generators directly against Figures 2.19–2.20's 6-graph oracle (`sel₂`
  exclusive split vs `sel₃` inclusive 3-way split); never clear `n_U ∈ is` when `(n_∅, sel', n_U) ∈ H'`.
- cyber: `kill_{x.sel}` and `[x.sel:=y]` demonstrate exact preconditions for sound strong updates (`CWE-416` use-after-free, `CWE-415` double-free, sanitizer clearing `[external]`); ignoring Case 1 silent `kill_x` on
  `nil`/undef (`p. 120`) + branch insensitivity (`[not is-nil(x)]` = `id`, `p. 116`) turns null-dereferences
  into bogus surviving post-crash paths unless client monitors inspect `Shape∘(ℓ)` before transfer.

---

## Concluding Remarks

Context: literature provenance, duality, MPCP undecidability, weakly monotonic solvers, pointer/shape
taxonomy, SSA form, and cross-paradigm DFA extensions [PPA Chapter 2 Concluding Remarks, p. 128] (book p. 128; PDF p. 147).

### [U2b:CR-a] Imperative DFA literature, duality, Monotone Frameworks, MPCP, and modal logic
- Statement: cites compiler texts (entry `[5]` in [PPA Bibliography, p. 439] (book p. 439; PDF p. 452),
  entry `[55]` in [PPA Bibliography, p. 443] (book p. 443; PDF p. 456), entry `[181]` in [PPA Bibliography, p. 452]
  (book p. 452; PDF p. 465)), Hecht (entry `[69]` in [PPA Bibliography, p. 444] (book p. 444; PDF p. 457)),
  Marlowe–Ryder survey (entry `[103]` in [PPA Bibliography, p. 446] (book p. 446; PDF p. 459)), modal-logic DFA
  (Steffen entry `[164]` in [PPA Bibliography, p. 451] (book p. 451; PDF p. 464), Schmidt entry `[151]` in
  [PPA Bibliography, p. 450] (book p. 450; PDF p. 463)), faint variables (`Giegerich–Möncke–Wilhelm` entry `[65]` in
  [PPA Bibliography, p. 444] (book p. 444; PDF p. 457)), SOS LV proofs (`[112, 140, 130]`), Kildall semi-lattices
  (entry `[96]` in [PPA Bibliography, p. 446] (book p. 446; PDF p. 459)), Kam–Ullman Monotone Frameworks and MPCP
  undecidability (`[93, 76]`, noting literature uses *dual* meets/maximal fixed points), and Cousot–Cousot
  Abstract Interpretation (`[37]`, Chapter 4).
- Citation: [PPA Chapter 2 Concluding Remarks, p. 128] (book p. 128; PDF p. 147)

### [U2b:CR-b] Blocks vs flows, Sharir–Pnueli interprocedural contexts, and weakly monotonic systems
- Statement: block-attached vs flow-attached (`[147]`) transfer functions have equal power (flow-to-block
  avoids artificial blocks via `[b]^{ℓ₁,ℓ₂}`, Exercise 2.11). Contrasts Sharir–Pnueli (`[155]`, `p. 129`)
  call strings (`[178]`) vs functional approach (`[99, 138, 145, 44]`). Notes Fecht–Seidl weakly monotonic
  solvers (entries `[51, 52]` in [PPA Bibliography, p. 443] (book p. 443; PDF p. 456)) for non-monotone `§2.5.5`.
- Citation: [PPA Chapter 2 Concluding Remarks, p. 129] (book p. 129; PDF p. 148)

### [U2b:CR-c] Pointer & shape analysis taxonomy and Sagiv–Reps–Wilhelm comparison
- Statement: following Ghiya–Hendren (`[62]`, `p. 129`), separates: (1) statically allocated stack pointers
  (points-to `(p, x)` or alias pairs `(*p, x)`: `[47, 100, 145, 182, 162, 153]`, Steensgaard, Shapiro–Horwitz);
  from (2) anonymous dynamic heap objects: connectivity (`[38, 61]`), path-bounded graphs (`[84, 165]`),
  allocation-site merging (`[85, 30]`, Exercise 2.25), variable-set shape graphs (`[148, 149]`, Sagiv–Reps–Wilhelm
  who merge compatible graphs into **one** summary shape graph to avoid `§2.6`'s exponential `𝒫(SG)` factor;
  generalised properties `[150]`), and access-path abstractions (`[62, 101, 45]`).
- Citation: [PPA Chapter 2 Concluding Remarks, p. 129] (book p. 129; PDF p. 148); access paths & `[148–150]` on
  [PPA Chapter 2 Concluding Remarks, p. 130] (book p. 130; PDF p. 149)

### [U2b:CR-d] Static Single Assignment (SSA) form
- Statement: SSA (`[42]`, `[12, 180, 109, 110]`) gives each variable at most one static definition (explicit
  `du`-chains), inserting `x := ϕ(x₁, ···, x_n)` at control-flow joins via two phases (join-point placement +
  renaming) guided by DFA.
- Citation: [PPA Chapter 2 Concluding Remarks, p. 130] (book p. 130; PDF p. 149)

### [U2b:CR-e] Functional, OOP, and distributed communicating process DFA
- Statement: functional languages need Chapter 3 CFA first; OOP (`[178]`, p. 131) determines receiver classes
  and lifetimes via interprocedural graph DFA; communicating processes (Reif–Smolka `[142]`) link matching
  transmits/receives across process spanning trees.
- Citation: [PPA Chapter 2 Concluding Remarks, p. 130] (book p. 130; PDF p. 149); OOP/distributed on
  [PPA Chapter 2 Concluding Remarks, p. 131] (book p. 131; PDF p. 150)

### [U2b:CR-f] Intraprocedural CFA on low-level IR and structural analysis
- Statement: low-level three-address code requires intraprocedural CFA to recover `flow`/`flow^R`;
  *structural analysis* (Sharir `[154]`, Muchnick `[110]`) iteratively collapses source control patterns
  into abstract nodes, refining natural-loop / interval analysis (`[69, 5, 110]`).
- Citation: [PPA Chapter 2 Concluding Remarks, p. 131] (book p. 131; PDF p. 150)

### Projections (Concluding Remarks)
- cs_theory: connects DFA lattices to modal μ-calculus `[164, 151]`, MPCP pushdown reductions `[93]`,
  Fecht–Seidl non-monotone iteration `[51, 52]`, and single-summary shape compaction `[148, 149]`.
- swe_architecture: clarifies SSA as explicit static def-use IR `[42]` and points-to/allocation-site/shape
  precision tiers (`[162, 153]` vs `[30, 85]` vs `[148, 150]`).
- practical_debugging: explains why literature papers write `⊓`/`GFP` while PPA writes `⊔`/`LFP` (exact duals).
- cyber: structural analysis (`[154, 110]`) underpins binary decompiler AST recovery (`[external]`), while
  points-to vs shape tiering dictates speed vs heap-bug sensitivity.

---

## Mini Projects

Context: three applied capstone projects for Chapter 2 (`du/ud` constant folding, instrumented `RD^⊆`
soundness proof, and ML/Haskell prototype solver) [PPA Mini Project 2.1, p. 132] (book p. 132; PDF p. 151).

### Figure 2.23 — `du`- and `ud`-chains
- Content: top row `[x:=n]^ℓ`, `...`, `[x:=···]^{···}`; bottom row `[···x···]^{···}`, `...`, `[···x···]^{ℓ'}`.
  Downward wavy `du-chain` arrows go from `[x:=n]^ℓ` to `[···x···]^{···}` and `[···x···]^{ℓ'}`; upward
  wavy `ud-chain` arrows go from `[···x···]^{ℓ'}` back to `[x:=n]^ℓ` and `[x:=···]^{···}`.
- Citation: [PPA Figure 2.23, p. 132] (book p. 132; PDF p. 151)

### Mini Project 2.1 — `ud`- and `du`-chains
- Statement: (1) prove declarative `ud` (`clear`) equals equational `UD` (`§2.1.5`); (2) formulate equational
  `DU` from `du` and verify correctness; (3) chain-based Constant Propagation + Constant Folding + Dead Code
  Elimination: replacing `x` at `ℓ'` with `n` from `[x:=n]^ℓ` (`du`) is safe **iff** *all* reaching definitions
  for `x` at `ℓ'` (`ud`, Figure 2.23) also assign constant `n` — transforming `Example 2.12` to
  `(if [z=3]^3 then [z:=0]^4 else [z:=3]^5); [y:=3]^6; [x:=3+z]^7`. ■
- Citation: [PPA Mini Project 2.1, p. 132] (book p. 132; PDF p. 151)

### Table 2.10 — The instrumented semantics of `WHILE`
- Content:

```
[ass]   ⟨[x := a]^ℓ, σ, tr⟩ → ⟨σ[x ↦ 𝒜⟦a⟧σ], tr : (x, ℓ)⟩
[skip]  ⟨[skip]^ℓ, σ, tr⟩ → ⟨σ, tr⟩

                ⟨S₁, σ, tr⟩ → ⟨S₁', σ', tr'⟩
[seq₁]  ─────────────────────────────────────────────
        ⟨S₁; S₂, σ, tr⟩ → ⟨S₁'; S₂, σ', tr'⟩

               ⟨S₁, σ, tr⟩ → ⟨σ', tr'⟩
[seq₂]  ───────────────────────────────────────
        ⟨S₁; S₂, σ, tr⟩ → ⟨S₂, σ', tr'⟩

[if₁]   ⟨if [b]^ℓ then S₁ else S₂, σ, tr⟩ → ⟨S₁, σ, tr⟩            if ℬ⟦b⟧σ = true
[if₂]   ⟨if [b]^ℓ then S₁ else S₂, σ, tr⟩ → ⟨S₂, σ, tr⟩            if ℬ⟦b⟧σ = false
[wh₁]   ⟨while [b]^ℓ do S, σ, tr⟩ → ⟨(S; while [b]^ℓ do S), σ, tr⟩  if ℬ⟦b⟧σ = true
[wh₂]   ⟨while [b]^ℓ do S, σ, tr⟩ → ⟨σ, tr⟩                         if ℬ⟦b⟧σ = false
```

- Citation: [PPA Table 2.10, p. 133] (book p. 133; PDF p. 152)

### Mini Project 2.2 — Correctness of Reaching Definitions
- Statement: proved using Table 2.10 instrumented traces `tr ∈ Trace` starting from `tr⋆ = ((x₁, ?), ···, (x_n, ?))`
  (`Var⋆ = {x₁, ···, x_n}`). Invariant `tr' ∈ TrVar⋆^? = {tr ∈ Trace | ∀x ∈ Var⋆ : ∃ℓ ∈ Lab⋆^? : (x, ℓ) occurs in tr}`;
  study constraint system `RD^⊆(S⋆)` for `reach_entry, reach_exit : Lab⋆ → 𝒫(Var⋆ × Lab⋆^?)`.
  (1) Formulate/prove analogues of Lemmas 2.15, 2.16, 2.18. Correctness relation `tr ∼ Y iff ∀x ∈ DOM(tr) : (x, SRD(tr)(x)) ∈ Y`
  (using `§1.5`'s `SRD`, `[PPA §1.5, p. 13] (book p. 13; PDF p. 33)`).
  (2) Formulate/prove analogues of Lemma 2.20, Theorem 2.21, Corollary 2.22. ■
- Citation: [PPA Mini Project 2.2, p. 133] (book p. 133; PDF p. 152); correctness relation on
  [PPA Mini Project 2.2, p. 134] (book p. 134; PDF p. 153)

### Mini Project 2.3 — A Prototype Implementation
- Statement: functional AST (`var = string`, `label = int`, `aexp`, `bexp`, `stat = Assign | Skip | Seq | If | While`)
  to (1) compute `init, final, flow, flow^R, blocks`, (2) generate `§2.1.4` LV equations, (3) implement
  `§2.4` worklist solver (and optionally parameterise by arbitrary Monotone Framework instance). ■
- Citation: [PPA Mini Project 2.3, p. 134] (book p. 134; PDF p. 153); SML/Haskell datatype on
  [PPA Mini Project 2.3, p. 135] (book p. 135; PDF p. 154)

### Findings (Mini Projects)
- F-U2b-11: Mini Project 2.2 contains three formal errors (`pp. 133–134`): (1) defines `Trace = (Var × Lab)*`
  omitting `?` even though `tr⋆` contains `(x_i, ?)` (`(Var × Lab^?)*` needed); (2) prints `Y ⊆ 𝒫(Var⋆ × Lab⋆^?)`
  where `(x, SRD(tr)(x)) ∈ Y` requires `Y ⊆ Var⋆ × Lab⋆^?`; (3) omits isolated entries needed by Table 2.2's
  `RD^⊆` (dual of `F-U2a-09`). [PPA Mini Project 2.2, p. 133] (book p. 133; PDF p. 152);
  [PPA Mini Project 2.2, p. 134] (book p. 134; PDF p. 153)

### Projections (Mini Projects)
- cs_theory: instrumented trace semantics makes ghost history (`SRD(tr)`) explicit in SOS without altering
  observable state transitions, bridging §1.5's trace `SRD` and §2.2's step preservation.
- swe_architecture: decouples chain consumers (`UD`/`DU`) from equation generation cleanly; SML AST
  patterns show exact pure-functional CFG builder contracts.
- practical_debugging: when chain constant folding breaks a conditional, verify both directions: `du` finds
  uses of `[x:=n]` while `ud` must confirm *every* reaching definition of `x` equals `n`.
- cyber: instrumented traces directly model taint-provenance ghost state (`tr : (x, src_label)`) for certifying
  static taint trackers against concrete runtime executions `[external]`.

---

## Exercises (`2.1`–`2.25`)

Context: 25 exercises spanning classical DFA extensions, faint variables, basic blocks, non-isolated boundaries,
Moore families, Bit Vector vs Distributive Frameworks, `MFP ≠ MOP`, `[b]^{ℓ₁,ℓ₂}` edge-split refinement,
independent-attribute vs relational Signs, distinct-site `k`, parameter modes, and `Shape` scaling/GC/alloc-site
refinements (`2.21*, 2.23*, 2.24*, 2.25*` starred) [PPA Exercise 2.1, p. 135] (book p. 135; PDF p. 154).

- **Exercise 2.1** (`p. 135`): Formulate `RD` equations, `gen`, `kill` for `Example 1.1` factorial. [PPA Exercise 2.1, p. 135] (book p. 135; PDF p. 154)
- **Exercise 2.2** (`p. 135`): Perform `LV` (§2.1.4) on `[x:=1]^1; (while [y>0]^2 do [x:=x-1]^3); [x:=2]^4`. [PPA Exercise 2.2, p. 135] (book p. 135; PDF p. 154)
- **Exercise 2.3** (`p. 135`): Formulate equations for *expression `a` available in a particular variable `x`* at `ℓ` (no redefinition of `x` or `FV(a)`). [PPA Exercise 2.3, p. 135] (book p. 135; PDF p. 154)
- **Exercise 2.4** (`p. 136`): *Faint vs strongly live variables* on `[x:=1]^1; [x:=x-1]^2; [x:=2]^3` (`f_ℓ(l)` splits on `x ∈ l` so `1, 2` do not spuriously mark `x` strongly live). [PPA Exercise 2.4, p. 136] (book p. 136; PDF p. 155)
- **Exercise 2.5** (`p. 136`): Reformulate `§2.1` analyses for multi-statement *basic blocks* `[x₁:=a₁; ···; x_n:=a_n; B]^ℓ` (`n ≥ 0`, `B ∈ {x:=a, skip, b}`). [PPA Exercise 2.5, p. 136] (book p. 136; PDF p. 155)
- **Exercise 2.6** (`p. 136`): Diagnose which `AE`/`RD` equations break without isolated entries and `VB`/`LV` without isolated exits; repair via `§2.3` `ι^ℓ_E`. [PPA Exercise 2.6, p. 136] (book p. 136; PDF p. 155)
- **Exercise 2.7** (`p. 136`): Define compositional `LV^=(S)` / `LV^⊆(S)` and `live ⊨ C`; prove `{live | live ⊨ LV^⊆(S)}` is a *Moore family* (`⋂`), and determine whether `{live | live ⊨ LV^=(S)}` is (it fails `⋂∅ = ⊤` when `Var⋆ ≠ ∅` `[derived]`; unclosed `(` typo, see `F-U2b-12`). [PPA Exercise 2.7, p. 136] (book p. 136; PDF p. 155)
- **Exercise 2.8** (`p. 136`): Show Constant Propagation (`§2.3.3`) with `𝓕_CP` is a Monotone Framework. [PPA Exercise 2.8, p. 136] (book p. 136; PDF p. 155)
- **Exercise 2.9** (`p. 137`): Define *Bit Vector Framework*: finite `D`, `L = (𝒫(D), ⊑)` (`⊑ ∈ {⊆, ⊇}`), `𝓕 = {f | ∃Y_f^1, Y_f^2 ⊆ D : ∀Y ⊆ D : f(Y) = (Y ∩ Y_f^1) ∪ Y_f^2}`; prove all four `§2.1` analyses are Bit Vector Frameworks, every Bit Vector Framework is Distributive, and construct a non-bit-vector Distributive Framework (e.g. copy-variable/faint propagation, `[derived]`). [PPA Exercise 2.9, p. 137] (book p. 137; PDF p. 156)
- **Exercise 2.10** (`p. 137`): Construct `MFP•(6) ≠ MOP•(6)` for Constant Propagation on `(if [···]^1 then [x:=-1]^2; [y:=1]^3 else [x:=1]^4; [y:=-1]^5); [z:=x*y]^6` (`MFP` gives `z = ⊤` vs `MOP` gives `z = -1` `[derived]`). [PPA Exercise 2.10, p. 137] (book p. 137; PDF p. 156)
- **Exercise 2.11** (`p. 137`): Replace `[b]^ℓ` by two-label branch test `[b]^{ℓ₁,ℓ₂}` (`ℓ₁` true, `ℓ₂` false) across `§§2.1, 2.3` to propagate test-filtered facts into `S₁, S₂` (see `F-U2b-12`). [PPA Exercise 2.11, p. 137] (book p. 137; PDF p. 156)
- **Exercise 2.12** (`p. 137`): Complexity bound for `AE`, `VB`, or `LV` following `Example 2.30`. [PPA Exercise 2.12, p. 137] (book p. 137; PDF p. 156)
- **Exercise 2.13** (`p. 137`): Prove `∀ℓ ∈ Lab⋆ : path∘(ℓ) ≠ ∅` for forward `(flow(S⋆), {init(S⋆)})` and backward `(flow^R(S⋆), final(S⋆))` (needed by `Lemma 2.32` coincidence; see `F-U2b-12`). [PPA Exercise 2.13, p. 137] (book p. 137; PDF p. 156)
- **Exercise 2.14** (`p. 138`): *Independent attribute* Detection of Signs comparing `Var⋆ → 𝒫({-, 0, +})` vs `𝒫(Var⋆ × {-, 0, +})` (isomorphic lattices, equal precision `[derived]`). [PPA Exercise 2.14, p. 138] (book p. 138; PDF p. 157)
- **Exercise 2.15** (`p. 138`): *Relational* Detection of Signs over `𝒫(Var⋆ → {-, 0, +})` vs independent attribute (captures correlated signs; Chapter 4 connection). [PPA Exercise 2.15, p. 138] (book p. 138; PDF p. 157)
- **Exercise 2.16** (`p. 138`): Last `k` *distinct* call sites vs `Lab^{\le k}`; examine distinguishing call vs recursion (`[ℓ_c, ℓ_c] ↦ [ℓ_c]` collapses direct recursion `[derived]`). [PPA Exercise 2.16, p. 138] (book p. 138; PDF p. 157)
- **Exercise 2.17** (`p. 138`): Construct large and small assumption-set equations (`§2.5.5`) for Fibonacci (`Example 2.33`) + Signs (`Example 2.36`). [PPA Exercise 2.17, p. 138] (book p. 138; PDF p. 157)
- **Exercise 2.18** (`p. 138`): Lift one `§2.1` classical analysis to call-string interprocedural form. [PPA Exercise 2.18, p. 138] (book p. 138; PDF p. 157)
- **Exercise 2.19** (`pp. 138–139`): Extend to `begin D⋆; input x; S⋆; output y end` (`Z → Z` semantics) with Signs transfer functions for `input`/`output`. [PPA Exercise 2.19, p. 138] (book p. 138; PDF p. 157)
- **Exercise 2.20** (`p. 139`): Multiple `val`, `res`, `val-res` parameters + locals in Signs transfer functions (note `val-res` aliasing `[derived]`). [PPA Exercise 2.20, p. 139] (book p. 139; PDF p. 158)
- **Exercise* 2.21** (`p. 139`, starred): Compute `Shape•(1), ···, Shape•(7)` for `Example 2.47` ("Warning: there will be more than 50 shape graphs."). [PPA Exercise 2.21, p. 139] (book p. 139; PDF p. 158)
- **Exercise 2.22** (`p. 139`): Direct (non-desugared) `Shape` transfers for `[x:=x.sel]^ℓ`, `[x.sel:=x]^ℓ`, `[x.sel:=x.sel']^ℓ`, `[malloc (x.sel)]^ℓ`. [PPA Exercise 2.22, p. 139] (book p. 139; PDF p. 158)
- **Exercise* 2.23** (`p. 139`, starred): Tighten edge conditions on `H''` vs `H'` in Case 3 materialisation (`[x:=y.sel]^ℓ`, `x ≠ y`) to prune spurious graphs. [PPA Exercise 2.23, p. 139] (book p. 139; PDF p. 158)
- **Exercise* 2.24** (`p. 139`, starred): Add garbage collection to both `§2.6.1` heap SOS and `§2.6.3` `Shape`. [PPA Exercise 2.24, p. 139] (book p. 139; PDF p. 158)
- **Exercise* 2.25** (`p. 139`, starred): Allocation-site-indexed abstract locations `n_{ℓ,X}` (`ℓ` a `malloc` label) partitioning `n_∅` into per-site summary nodes `n_{ℓ,∅}`. [PPA Exercise 2.25, p. 139] (book p. 139; PDF p. 158)

### Findings (Exercises)
- F-U2b-12: `Exercise 2.7` (`p. 136`) prints `(with ∏ being ⋂ and determine...` with an unclosed `(` after `⋂`;
  `Exercise 2.11` (`p. 137`) assumes `x ∈ {-, +}` (`0` absent) when concluding `x` is negative on false branch
  of `x > 0` (otherwise `¬(x > 0)` leaves `{-, 0}`); `Exercise 2.13` (`p. 137`) requires `Lab⋆ = labels(S⋆)`
  (no spare unused labels) and intraprocedural `S⋆` without uncalled dead procedures.
  [PPA Exercise 2.7, p. 136] (book p. 136; PDF p. 155); [PPA Exercise 2.11, p. 137] (book p. 137; PDF p. 156);
  [PPA Exercise 2.13, p. 137] (book p. 137; PDF p. 156)

### Projections (Exercises)
- cs_theory: Exercises 2.7, 2.9, 2.10, and 2.13–2.15 sharply separate Bit Vector `⊂` Distributive `⊂` Monotone,
  constraints (`Moore family`) from equations, and independent-attribute from relational lattices.
- swe_architecture: Exercises 2.5, 2.11, 2.19, 2.20, 2.24, and 2.25 capture the practical compiler upgrades
  (`basic blocks`, branch filtering, I/O boundaries, multi-mode params, GC, and allocation-site heap splitting).
- practical_debugging: use `Exercise 2.10` (`z:=x*y`) and `Exercise 2.4` (`x:=x-1`) as regression probes for
  relational vs non-relational joins and strongly live DCE; test `Exercise 2.16` distinct call-sites against
  nested mutual recursion.
- cyber: strongly live variables (`Exercise 2.4`), branch-split `[b]^{ℓ₁,ℓ₂}` (`Exercise 2.11`), and
  allocation-site `n_{ℓ,X}` (`Exercise 2.25`) directly curb dead-taint noise, false-positive guard-bypass alerts,
  and cross-structure summary pollution in real vulnerability scanners `[external]`.

---

## Gotcha Ledger

- G-U2b-01: Interprocedural edges `(ℓ_c; ℓ_n)` and `(ℓ_x; ℓ_r)` in `flow⋆` do not pair matching calls and returns; naive equation solving without `inter-flow⋆` allows unrealizable paths (`(ℓ_c^i, ℓ_n, ℓ_x, ℓ_r^j)` with `i ≠ j`). [PPA §2.5, p. 84] (book p. 84; PDF p. 103)
- G-U2b-02: Defining `flow([call p(a, z)]^{ℓ_c}_{ℓ_r})` assumes statically known procedure constants; procedure variables/parameters cause the dynamic dispatch problem deferred to Chapter 3. [PPA §2.5, p. 84] (book p. 84; PDF p. 103)
- G-U2b-03: Backward `F = flow⋆^R, IF = inter-flow⋆^R` is stated on p. 85 without formally defining reversal on semicolon edges or 4-tuples (`[derived]`: `(ℓ_r, ℓ_x, ℓ_n, ℓ_c)`). [PPA §2.5, p. 85] (book p. 85; PDF p. 104)
- G-U2b-04: In `§2.5.1` `[call]`, body `S` executes under top-level `ρ⋆[x ↦ ξ₁, y ↦ ξ₂]` (static scoping, not caller `ρ`), and formal `res y` location `ξ₂` starts at an *arbitrary* `v ∈ Z`, so sound forward call transfers must set `y` to unconstrained `⊤` (`{-, 0, +}` in Example 2.38). [PPA §2.5.1, p. 87] (book p. 87; PDF p. 106)
- G-U2b-05: Intermediate `bind ρ' in S then z:=y` configurations only appear mid-execution (`Remark.`, p. 87) and require dedicated correctness treatment in Chapter 3; `[ass]` on p. 86 and `z:=y` omit elementary-block labels. [PPA §2.5.1, p. 87] (book p. 87; PDF p. 106)
- G-U2b-06: `VP⋆` includes both balanced complete paths (`CP_{ℓ₁,ℓ₂}`) and prefixes with pending non-returned calls (`VP_{ℓ_c,ℓ} ⟶ ℓ_c, VP_{ℓ_n,ℓ}`), covering points inside procedures and diverging executions. [PPA §2.5.2, p. 90] (book p. 90; PDF p. 109)
- G-U2b-07: `MVP∘(ℓ) ⊑ MOP∘(ℓ)` holds because `vpath∘(ℓ) ⊆ path∘(ℓ)`, yet `MVP` remains undecidable in general even on lattices of finite height (`§2.5.3`, p. 90). [PPA §2.5.3, p. 90] (book p. 90; PDF p. 109)
- G-U2b-08: In an embellished framework `L̂ = Δ → L`, `A∘(ℓ)` uses the predecessor join for *all* labels while `A•(ℓ) = f̂_ℓ(A∘(ℓ))` skips call/return labels, which use `f̂¹_{ℓ_c}` and *binary* `f̂²_{ℓ_c,ℓ_r}(A∘(ℓ_c), A∘(ℓ_r))`. [PPA §2.5.3, p. 93] (book p. 93; PDF p. 112)
- G-U2b-09: Ignoring the first argument `A∘(ℓ_c)` of `f̂²_{ℓ_c,ℓ_r}` (Figure 2.9, whose top arrow misprints `f̂¹_{ℓ₁}` for `f̂¹_{ℓ_c}`) makes restoring caller formals `x, y` impossible; `f̂²` is completely additive on the product lattice iff it splits as `f̂^{2A}(l̂) ⊔ f̂^{2B}(l̂')` with both components completely additive. [PPA §2.5.3, p. 94] (book p. 94; PDF p. 113)
- G-U2b-10: Bounded call-string truncation `δ ↦ ⌈δ, ℓ_c⌉_k` is non-injective, forcing `⨆` joins in `f̂¹_{ℓ_c}` and conflating callers across depth `> k` (or recursive self-calls at `k=1`); `k = 0` collapses to context-insensitive smearing. [PPA §2.5.4, p. 98] (book p. 98; PDF p. 117)
- G-U2b-11: Distinct-site `k` contexts (`Exercise 2.16`) collapse direct self-recursion `[ℓ_c, ℓ_c] ↦ [ℓ_c]`, failing to separate the outer call from subsequent recursive calls. [PPA Exercise 2.16, p. 138] (book p. 138; PDF p. 157)
- G-U2b-12: Large assumption sets (`Δ = 𝒫(D)`) use exact fiber `δ' = {d'' | (δ, d'') ∈ Z}`, making `f̂¹_{ℓ_c}` and `f̂²_{ℓ_c,ℓ_r}` *non-monotone* (`BKL-003`) unless relaxed to `⊆`, solved via weakly monotonic solvers `[51, 52]`, or replaced by small assumption sets (`Δ = D`). [PPA §2.5.5, p. 100] (book p. 100; PDF p. 119)
- G-U2b-13: Printed `ι̂ = {({ι}, ι)}` (p. 99) and `ι̂ = {(ι, ι)}` (p. 100) treat `ι ∈ 𝒫(D)` as a single element of `D`; general `ι ⊆ D` requires `{(ι, d) | d ∈ ι}` or `{(d, d) | d ∈ ι}` (`[derived]`). Also Example 2.41 (`p. 99`) mixes `y` and `u`. [PPA §2.5.5, p. 99] (book p. 99; PDF p. 118)
- G-U2b-14: `§2.5.6` prints `"context-insensitive"` on pp. 102–103 where *flow-insensitive* is meant, and omits `\ {y}` for formal `res y` in `IAV(p) = (AV(S) \ {x}) ∪ ...`, leaking local `res` assignments as global writes if copied verbatim. [PPA §2.5.6, p. 102] (book p. 102; PDF p. 121)
- G-U2b-15: Recursive `IAV(p)` equations over cyclic call graphs (`Figure 2.11`) require the *least* fixed point (`{y}`); the greatest fixed point returns useless `Var⋆`. [PPA Example 2.42, p. 103] (book p. 103; PDF p. 122)
- G-U2b-16: `§2.6` restricts pointers to single-level selectors `x.sel`, forbids pointer arithmetic, interior pointers, and type punning (`BKL-005`), and types `℘, 𝒜, ℬ` with `→_fin` over infinite `State × Heap` (`⇀` meant). [PPA §2.6, p. 105] (book p. 105; PDF p. 124); [PPA §2.6.1, p. 107] (book p. 107; PDF p. 126)
- G-U2b-17: In `§2.6.1`, `[malloc p]^ℓ` chooses `ξ` absent from both `σ` and `ℋ`, leaving `ℋ(ξ, sel)` undefined; unreachable cells still present in `dom(ℋ)` cannot be reused without explicit GC (`Remark.`, p. 109). [PPA §2.6.1, p. 109] (book p. 109; PDF p. 128)
- G-U2b-18: Abstract states `S` and heaps `H` omit integers, `nil` (`◇`), and uninitialised fields altogether, so absent bindings represent any of those three (`◇`/`Z`/`undef`); moreover concrete locations migrate dynamically into and out of `n_∅`. [PPA §2.6.2, p. 110] (book p. 110; PDF p. 129); [PPA Example 2.46, p. 112] (book p. 112; PDF p. 131)
- G-U2b-19: `is` records *heap*-pointer sharing (`≥ 2` heap pointers) only, never stack-variable aliasing via `S`: `[x:=y]^ℓ` merges `x, y` into `n_{Y∪{x}}` while preserving `n_Y`'s `is` membership unchanged. [PPA §2.6.3, p. 119] (book p. 119; PDF p. 138)
- G-U2b-20: `Invariant 3` enforces deterministic selector targets (`W = W'`) only when `V ≠ ∅`; summary node `n_∅` may have multiple outgoing edges for the same `sel` (including self-loops). [PPA §2.6.2, p. 111] (book p. 111; PDF p. 130)
- G-U2b-21: `Invariant 5` is the converse of `Invariant 4(b)` for `X ≠ ∅`, whereas `Invariant 4(a)` (`(n_∅, sel, n_X) ∈ H`) has *no* converse: both `n_X ∉ is` and `n_X ∈ is` are compatible with a single `n_∅ → n_X` edge (`Figure 2.14` rows 1–2); `n_∅ ∉ is` guarantees every `n_∅`-cell has `≤ 1` heap incoming pointer. [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133)
- G-U2b-22: `Shape` over `𝒫(SG)` is outer *may* (`⊔ = ∪`) yet inner *must* (no superfluous edges inside each compatible graph), enabling sound strong nullification (`kill_x`) and strong updates (`kill_{x.sel}` / `[x.sel:=y]`) on unique non-summary `n_X` (`X ≠ ∅`). [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134)
- G-U2b-23: `Shape` treats boolean guards `[b]^ℓ` (even `[not is-nil(x)]^2`) as identity (`p. 116`) and sends `Case 1` `nil`/missing-field dereferences in `[x:=y.sel]^ℓ` to `{kill_x(...)}` rather than `∅` or a raised fault (`p. 120`), retaining infeasible post-crash states unless branch splitting (`Exercise 2.11`) and pre-transfer alarms are added. [PPA §2.6.3, p. 116] (book p. 116; PDF p. 135); [PPA §2.6.3, p. 120] (book p. 120; PDF p. 139)
- G-U2b-24: Neither `kill_x` (`p. 117`) nor `kill_{x.sel}` (`p. 126`) performs garbage collection: `[x:=nil]^ℓ` folds unreachable `n_{x}` (with its outgoing pointers!) into `n_∅`, and `[x.sel:=nil]^ℓ` leaves detached `n_U` in the graph unless Exercise 2.24 GC is added. [PPA §2.6.3, p. 117] (book p. 117; PDF p. 136); [PPA §2.6.3, p. 126] (book p. 126; PDF p. 145)
- G-U2b-25: Self-assigning and two-dereference pointer statements (`[x:=x.sel]`, `[x.sel:=x]`, `[x.sel:=y.sel']`, `[malloc (x.sel)]`) cannot directly apply the `x ≠ y` clauses and must either desugar via fresh temporary `t` (`Var⋆ ∪ {t}`) plus trailing `[t:=nil]^{ℓ₃}` or use Exercise 2.22's direct rules. [PPA §2.6.3, p. 119] (book p. 119; PDF p. 138); [PPA §2.6.3, p. 127] (book p. 127; PDF p. 146)
- G-U2b-26: In `[x:=y.sel]^ℓ` `Case 3` materialisation, `(n_Y, sel, n_∅) ∈ H'` must become `(n_Y, sel, n_{x}) ∈ H''`, `S'' = S' ∪ {(x, n_{x})}`, and `n_∅ ∈ is' ⇔ (n_∅ ∈ is'' ∨ n_{x} ∈ is'')`; when `n_∅ ∉ is'`, `n_{x}` cannot share `is''`, pruning target edges into `n_{x}` while source edges out of `{n_∅, n_{x}}` still branch combinatorially (`Figures 2.19–2.20`, `Exercise 2.23`). [PPA §2.6.3, p. 122] (book p. 122; PDF p. 141); [PPA Figure 2.20, p. 124] (book p. 124; PDF p. 143)
- G-U2b-27: In `kill_{x.sel}`, clearing `n_U` from `is` requires all three conditions: `n_U ∈ is`, `#into(n_U, H') ≤ 1`, AND `¬∃sel' : (n_∅, sel', n_U) ∈ H'`; dropping the `n_∅` check unsoundly unshares cells targeted by multiple concrete summary cells in `n_∅`. [PPA §2.6.3, p. 125] (book p. 125; PDF p. 144)
- G-U2b-28: Operating over powersets `𝒫(SG)` triggers combinatorial explosion (`> 50` shape graphs on 7-block list reversal in `Exercise* 2.21`), whereas Sagiv–Reps–Wilhelm `[148, 149]` merge graphs into one summary shape graph per point and `Exercise* 2.25` splits `n_∅` by allocation site `n_{ℓ,X}`. [PPA Chapter 2 Concluding Remarks, p. 130] (book p. 130; PDF p. 149); [PPA Exercise 2.21, p. 139] (book p. 139; PDF p. 158)
- G-U2b-29: Sound chain-based Constant Folding (`Mini Project 2.1`) requires following `du`-chains from `[x:=n]^ℓ` AND confirming via `ud`-chains at use `ℓ'` that *every* reaching definition of `x` assigns the identical constant `n`. [PPA Mini Project 2.1, p. 132] (book p. 132; PDF p. 151)
- G-U2b-30: `Mini Project 2.2` defines `Trace = (Var × Lab)*` (omitting `?` required by `tr⋆`), writes `Y ⊆ 𝒫(Var⋆ × Lab⋆^?)` instead of `Y ⊆ Var⋆ × Lab⋆^?`, and uses Table 2.2's `RD^⊆` needing isolated entries unless reformulated unconditionally (`§2.3`). [PPA Mini Project 2.2, p. 133] (book p. 133; PDF p. 152); [PPA Mini Project 2.2, p. 134] (book p. 134; PDF p. 153)
- G-U2b-31: Bit Vector Frameworks (`f(Y) = (Y ∩ Y_f^1) ∪ Y_f^2` over finite `𝒫(D)`, `⊑ ∈ {⊆, ⊇}`) strictly refine Distributive Frameworks (`Bit Vector ⊂ Distributive ⊂ Monotone`): copy/faint propagation (`Exercise 2.4`) is distributive (`f({x}) = {y}`) yet not bit-vector because `f(∅) = ∅` would force `f({x}) ⊆ {x}` (`[derived]`). [PPA Exercise 2.4, p. 136] (book p. 136; PDF p. 155); [PPA Exercise 2.9, p. 137] (book p. 137; PDF p. 156)
- G-U2b-32: Constraint solutions `{live | live ⊨ LV^⊆(S)}` form a Moore family under `⋂`, whereas equation solutions `{live | live ⊨ LV^=(S)}` in general fail `⋂∅ = ⊤` when `Var⋆ ≠ ∅` (`[derived]`). [PPA Exercise 2.7, p. 136] (book p. 136; PDF p. 155)
- G-U2b-33: Early DFA literature (`[69, 93, 96]`) presents analyses dual to this book (`⊓` and `GFP` instead of `⊔` and `LFP`, `p. 128`), and MOP undecidability reduces from MPCP (`[93, 76]`). [PPA Chapter 2 Concluding Remarks, p. 128] (book p. 128; PDF p. 147)
- G-U2b-34: Multiple parameter modes (`Exercise 2.20`) must handle `val-res` actual variable aliasing cleanly, and `Exercise 2.13` path non-emptiness assumes intraprocedural `S⋆` with `Lab⋆ = labels(S⋆)` (no uncalled dead code). [PPA Exercise 2.13, p. 137] (book p. 137; PDF p. 156); [PPA Exercise 2.20, p. 139] (book p. 139; PDF p. 158)
