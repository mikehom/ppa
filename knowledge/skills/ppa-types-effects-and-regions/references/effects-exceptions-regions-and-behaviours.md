<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Chapter 5 L1 reference for side effects, exceptions, stack-based region inference, Concurrent ML behaviours, and Mini Projects 5.1-5.5 (Sections 5.4.1-5.5). -->

# Side Effects, Exceptions, Region Inference, and Concurrent Behaviours

Scope: Sections `5.4.1–5.4.3`, Section `5.5` (`§5.5.1`), Concluding Remarks (`pp. 349–353`), Mini Projects
`5.1–5.5`, and Exercises `5.11–5.15` — [PPA §5.4, p. 319] (book p. 319; PDF p. 336) through
[PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380) (`Tables 5.9–5.18`, `Figures 5.1–5.2`, `Examples 5.24–5.37`).
Ground truth: `corpus/shards/RAW_SHARD_05b_effects_regions_behaviours.md`.
Core CFA typing/soundness and `𝒲_CFA` unification live in
[annotated-types-and-cfa-soundness.md](./annotated-types-and-cfa-soundness.md) and
[inference-unification-and-subtyping.md](./inference-unification-and-subtyping.md); Chapter 2 mutable pointer
Shape Analysis (`§2.6`) lives in
[shape-analysis.md](../../ppa-dataflow-and-slicing/references/shape-analysis.md).

## 1. Side Effect Analysis and Reference Payload Invariance (Section 5.4.1, Table 5.9)

Section 5.4.1 extends `FUN` with `e ::= ··· | new_π x := e₁ in e₂ | !x | x := e₀ | e₁ ; e₂` (`Example 5.24`
imperative Fibonacci [PPA Example 5.24, p. 319] (book p. 319; PDF p. 336)) over `φ ∈ Ann_SE ::= {!π} | {π:=} | {new π} | φ₁ ∪ φ₂ | ∅`
and `τ̂ ∈ Type_SE ::= int | bool | τ̂₁ →^φ τ̂₂ | ref_ϖ τ̂` (`ϖ = {π₁, ..., π_n}`, printed unbraced `π` in BNF,
`F-U5b-03`; `Example 5.25`: `r : ref_{R} int`, `fib : int →^{!R, R:=} int`
[PPA Example 5.25, p. 321] (book p. 321; PDF p. 338)).

### 1.1 Store SOS (p. 320) and Table 5.9 Rules

Store-passing Natural Semantics `⊢ ⟨e, ς₁⟩ → ⟨v, ς₂⟩` over `ς ∈ Store = Loc →_fin Val` (`Val` adds `ξ ∈ Loc`,
omitted from surface syntax `F-U5b-02`; `!ξ`, `ξ:=e`, `e₁;e₂` restored from rendered p. 320, `G-U5b-04`, `G-U5b-26`)
[PPA §5.4.1, p. 320] (book p. 320; PDF p. 337) and `Table 5.9` (`Γ̂ ⊢_SE e : τ̂ & φ`)
[PPA Table 5.9, p. 322] (book p. 322; PDF p. 339):

```text
SOS:    ⊢ ⟨e₁,ς₁⟩→⟨v₁,ς₂⟩ ∧ ⊢ ⟨e₂[x↦ξ],ς₂[ξ↦v₁]⟩→⟨v₂,ς₃⟩ ⟹ ⊢ ⟨new_π x:=e₁ in e₂,ς₁⟩→⟨v₂,ς₃⟩  (ξ ∉ dom(ς₂))
        ⊢ ⟨!ξ, ς⟩ → ⟨ς(ξ), ς⟩        ⊢ ⟨e,ς₁⟩→⟨v,ς₂⟩ ⟹ ⊢ ⟨ξ:=e,ς₁⟩→⟨v, ς₂[ξ↦v]⟩   (* returns v! *)
        ⊢ ⟨e₁,ς₁⟩→⟨v₁,ς₂⟩ ∧ ⊢ ⟨e₂,ς₂⟩→⟨v₂,ς₃⟩ ⟹ ⊢ ⟨e₁;e₂,ς₁⟩→⟨v₂,ς₃⟩

[con]   Γ̂ ⊢_SE c : τ_c & ∅                        [var]   Γ̂ ⊢_SE x : τ̂ & ∅                      (if Γ̂(x) = τ̂)
[fn]    Γ̂[x↦τ̂_x] ⊢_SE e₀ : τ̂₀ & φ₀ ⟹ Γ̂ ⊢_SE fn_π x => e₀ : τ̂_x →^{φ₀} τ̂₀ & ∅
[fun]   Γ̂[f↦τ̂_x→^{φ₀}τ̂₀][x↦τ̂_x] ⊢_SE e₀ : τ̂₀ & φ₀ ⟹ Γ̂ ⊢_SE fun_π f x => e₀ : τ̂_x →^{φ₀} τ̂₀ & ∅
[app]   Γ̂ ⊢_SE e₁ : τ̂₂ →^{φ₀} τ̂₀ & φ₁ ∧ Γ̂ ⊢_SE e₂ : τ̂₂ & φ₂ ⟹ Γ̂ ⊢_SE e₁ e₂ : τ̂₀ & φ₁ ∪ φ₂ ∪ φ₀
[if]    Γ̂ ⊢_SE e₀:bool & φ₀ ∧ Γ̂ ⊢_SE e₁:τ̂ & φ₁ ∧ Γ̂ ⊢_SE e₂:τ̂ & φ₂ ⟹ Γ̂ ⊢_SE if e₀ then e₁ else e₂ : τ̂ & φ₀∪φ₁∪φ₂
[let]   Γ̂ ⊢_SE e₁:τ̂₁ & φ₁ ∧ Γ̂[x↦τ̂₁] ⊢_SE e₂:τ̂₂ & φ₂ ⟹ Γ̂ ⊢_SE let x=e₁ in e₂ : τ̂₂ & φ₁∪φ₂
[op]    Γ̂ ⊢_SE e₁:τ¹_op & φ₁ ∧ Γ̂ ⊢_SE e₂:τ²_op & φ₂ ⟹ Γ̂ ⊢_SE e₁ op e₂ : τ_op & φ₁∪φ₂
[deref] Γ̂ ⊢_SE !x : τ̂ & {!π₁, ..., !π_n}                                    (if Γ̂(x) = ref_{π₁,...,π_n} τ̂)
[ass]   Γ̂ ⊢_SE e : τ̂ & φ ⟹ Γ̂ ⊢_SE x := e : τ̂ & φ ∪ {π₁:=, ..., π_n:=}       (if Γ̂(x) = ref_{π₁,...,π_n} τ̂)
[new]   Γ̂ ⊢_SE e₁:τ̂₁ & φ₁ ∧ Γ̂[x↦ref_{π} τ̂₁] ⊢_SE e₂:τ̂₂ & φ₂ ⟹ Γ̂ ⊢_SE new_π x:=e₁ in e₂ : τ̂₂ & (φ₁∪φ₂∪{new π})
[seq]   Γ̂ ⊢_SE e₁:τ̂₁ & φ₁ ∧ Γ̂ ⊢_SE e₂:τ̂₂ & φ₂ ⟹ Γ̂ ⊢_SE e₁ ; e₂ : τ̂₂ & φ₁∪φ₂
[sub]   Γ̂ ⊢_SE e : τ̂ & φ ⟹ Γ̂ ⊢_SE e : τ̂' & φ'                               (if τ̂ ≤ τ̂' and φ ⊆ φ')
```

- **CBV latent deferral (`BKL-031`, `G-U5b-02`, cf. `BKL-026`)**: `[fn]`/`[fun]` emit `& ∅` until `[app]` (`Exercise 5.12`
  treats CBN [PPA Exercise 5.12, p. 362] (book p. 362; PDF p. 379); `Exercise 5.11` proves semantic soundness
  [PPA Exercise 5.11, p. 361] (book p. 361; PDF p. 378); `Remark.` p. 325 contrasts *Effect Systems* with `§5.1`
  *Annotated Type Systems*).
- **Unmasked `{new π}` (`G-U5b-03`) & unboxing (`Example 5.26`)**: `{new π}` remains visible outside `e₂` to report
  heap allocation; `B:= ∉ φ` justifies demoting `new_B y := !x` to `let y = !x`
  [PPA Example 5.26, p. 323] (book p. 323; PDF p. 340).
- **Bidirectional `ref_ϖ τ̂` invariance (`G-U5b-05`, `G-U5b-06`, `Example 5.27`)**:
  `ref_ϖ τ̂ ≤ ref_{ϖ'} τ̂'` iff **`τ̂ ≤ τ̂' ∧ τ̂' ≤ τ̂ ∧ ϖ ⊆ ϖ'`** (`!x` requires covariance; `x := e` requires
  contravariance; dropping invariance admits `[external: CWE-843]` write-side type confusion!). Retaining either
  subeffecting or subtyping preserves conservative extension over `Table 5.1`, whereas dropping **both** breaks it
  (`G-U5b-06`, `Example 5.27`) [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341)
  [PPA §5.4.1, p. 325] (book p. 325; PDF p. 342).

## 2. Exception Analysis, let-Polymorphism, and Effect Subtraction (Section 5.4.2, Table 5.10)

Section 5.4.2 adds `raise s | handle s as e₁ in e₂` (`Example 5.28` `comb`
[PPA Example 5.28, p. 326] (book p. 326; PDF p. 343)) and `Val ::= ··· | raise s` (`G-U5b-08`: `handle s as e₁ in e₂`
evaluates `e₂ → v₂`, returning `v₂` when `v₂ ≠ raise s` — propagating `raise s'` for `s' ≠ s` — and running `e₁` on
`raise s`) [PPA §5.4.2, p. 326] (book p. 326; PDF p. 343) [PPA §5.4.2, p. 327] (book p. 327; PDF p. 344).

Over `φ ∈ Ann_ES ::= {s} | φ₁ ∪ φ₂ | ∅ | β`, `τ̂ ∈ Type_ES ::= int | bool | τ̂₁ →^φ τ̂₂ | α`, and schemes
`σ̂ ::= ∀(ζ₁, ..., ζ_n). τ̂` (`ζ_i ∈ TVar ∪ AVar`), `Table 5.10` (`Γ̂ ⊢_ES e : σ̂ & φ`) extends sequential rules with
[PPA Table 5.10, p. 328] (book p. 328; PDF p. 345):

```text
[var]    Γ̂ ⊢_ES x : σ̂ & ∅      (if Γ̂(x) = σ̂)           [raise]  Γ̂ ⊢_ES raise s : τ̂ & {s}
[let]    Γ̂ ⊢_ES e₁ : σ̂₁ & φ₁ ∧ Γ̂[x ↦ σ̂₁] ⊢_ES e₂ : τ̂₂ & φ₂ ⟹ Γ̂ ⊢_ES let x = e₁ in e₂ : τ̂₂ & φ₁ ∪ φ₂
[handle] Γ̂ ⊢_ES e₁ : τ̂ & φ₁  ∧ Γ̂ ⊢_ES e₂ : τ̂ & φ₂          ⟹ Γ̂ ⊢_ES handle s as e₁ in e₂ : τ̂ & φ₁ ∪ (φ₂ \ {s})
[sub]    Γ̂ ⊢_ES e : τ̂ & φ ⟹ Γ̂ ⊢_ES e : τ̂' & φ'              (if τ̂ ≤ τ̂' and φ ⊆ φ'; α ≤ α only on TVar)
[gen]    Γ̂ ⊢_ES e : τ̂ & φ ⟹ Γ̂ ⊢_ES e : ∀(ζ₁,...,ζ_n). τ̂ & φ (if ζ₁,...,ζ_n do not occur free in Γ̂ and φ)
[ins]    Γ̂ ⊢_ES e : ∀(ζ₁,...,ζ_n). τ̂ & φ ⟹ Γ̂ ⊢_ES e : (θ τ̂) & φ  (if dom(θ) ⊆ {ζ₁,...,ζ_n})
```

- **Polymorphism beats monomorphic `[sub]` (`Examples 5.29–5.30`, `F-U5b-04`)**: Giving `f = fn g => fn x => g x`
  scheme `∀'a,'b,'0. ('a →^{'0} 'b) →^∅ ('a →^{'0} 'b)` isolates `{neg}` and `{pos}` per call site, avoiding
  monomorphic `{neg, pos}` smearing (auditing `[external: CWE-755]` uncaught exceptions and `[external: CWE-404]`
  cleanup bypasses) [PPA Example 5.29, p. 327] (book p. 327; PDF p. 344)
  [PPA Example 5.30, p. 330] (book p. 330; PDF p. 347).
- **Mandatory `β \ {s} = β` (`G-U5b-09`, `BKL-009`) & `AV(φ₂) = ∅` (`Exercise 5.14`, `G-U5b-10`)**:
  - Syntactic subtraction sets `{s}\{s}=∅`, `{s'}\{s}={s'}` (`s'≠s`), **and `β \ {s} = β`**! Simplifying `β \ {s}`
    to `∅` before `[ins]` unsoundly erases `s' ≠ s` when `β ↦ {s, s'}` (`Remark.` p. 330 notes exactness adds
    symbolic `φ \ {s}` to `Ann_ES`) [PPA §5.4.2, p. 329] (book p. 329; PDF p. 346)
    [PPA §5.4.2, p. 330] (book p. 330; PDF p. 347).
  - `[handle]` may omit `φ₁` (`Exercise 5.14`) **iff BOTH `s ∉ φ₂` AND `AV(φ₂) = ∅`**
    [PPA Exercise 5.14, p. 362] (book p. 362; PDF p. 379).
  - Lifting `Table 5.10` conclusions to `σ̂` (`Exercise 5.15`) requires defining scheme subtyping `σ̂ ≤ σ̂'`
    (misprinted `τ̂ ≤ τ̂'` on p. 363, `F-U5b-13`, `G-U5b-26`) ; the book only asks whether this is more powerful, and the answer "zero added power over prenex
    schemes" is `[derived]`
    [PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380).

## 3. Stack-Based Region Inference and Lexical Masking (Section 5.4.3, Figure 5.1, Tables 5.11-5.13)

Section 5.4.3 (`[175, 176]`, `[external: Tofte–Talpin]`) replaces GC with a dynamic stack of extensible boxed arrays `r1, r2, ...` (`Figure 5.1`),
translating `e ∈ Exp` to `ee ∈ EExp` (`c at r`, `fn_π x => ee₀ at r`, `fun_π f [ϱ⃗] x => ee₀ at r`, `ee₁ op ee₂ at r`,
`ee[r⃗] at r`, `letregion ϱ⃗ in ee`; `Examples 5.31–5.33`) [PPA Figure 5.1, p. 331] (book p. 331; PDF p. 348)
[PPA Example 5.31, p. 332] (book p. 332; PDF p. 349).

### 3.1 Boxed Store Semantics (Table 5.11) and Translation Rules (Tables 5.12-5.13)

In `Table 5.11` (`ρ ⊢ ⟨ee, ς⟩ → ⟨v, ς'⟩`), **every** runtime value `v ∈ EVal = RName × Offset` is boxed inside
`ς ∈ RName →_fin (Offset →_fin SVal)` (`SVal ::= c | ⟨x,ee,ρ⟩ | ⟨ϱ⃗,x,ee,ρ⟩`; `ς ⧹⧹ rn⃗` drops `{rn⃗}`)
[PPA §5.4.3, p. 333] (book p. 333; PDF p. 350) [PPA Table 5.11, p. 334] (book p. 334; PDF p. 351):
- `[con]`, `[fn]`, `[fun]`, `[op]` allocate fresh `o ∉ dom(ς(rn))` at `rn`; `[if₁]`/`[if₂]` unbox `ς₂(rn, o)`;
- `[place]` specialises `ς₂(rn', o') = ⟨ϱ⃗, x, ee₀, ρ₀⟩` into ordinary `⟨x, ee₀[ϱ⃗ ↦ rn⃗], ρ₀⟩` at `(rn, o)` (required
  before `[app]`, `G-U5b-14`);
- `[region]` runs `ee[ϱ⃗ ↦ rn⃗]` in `ς₁[rn⃗ ↦ []⃗]` (`{rn⃗} ∩ dom(ς₁) = ∅`, printed `dom(ς)`, `F-U5b-05`, `G-U5b-17`)
  and exits with `ς₂ ⧹⧹ rn⃗` (dangling `rn ∉ dom(ς)` gets stuck).

Over `φ ∈ Ann_RI ::= {put r} | {get r} | φ₁ ∪ φ₂ | ∅ | β`, `τ̂ ∈ Type_RI ::= int | bool | (τ̂₁ @ r₁) →^{β.φ} (τ̂₂ @ r₂) | α`
(`β.φ` denotes `β ∪ φ` and constraint `β ⊇ β ∪ φ`; `Type_RI` subtyping keeps `r₁, r₂` invariant, `F-U5b-06`), and
ordinary `∀α⃗, β⃗. τ̂` vs compound `∀α⃗, β⃗, [ϱ⃗]. τ̂` (`∀(),(),[]. τ̂` MUST be written `∀[]. τ̂`, `G-U5b-14`),
`Tables 5.12–5.13` (`Γ̂ ⊢_RI e ↝ ee : (τ̂ @ r) & φ`, half of `Table 5.12` restored from rendered p. 337, `G-U5b-26`)
specify [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354) [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355):

```text
[con]    Γ̂ ⊢_RI c ↝ c at r : (τ_c @ r) & {put r}        [var] Γ̂ ⊢_RI x ↝ x : σ̂ & ∅   (Γ̂(x)=σ̂, abbr. σ̂ @ r, F-U5b-06)
[fn]     Γ̂[x↦τ̂_x@r_x] ⊢_RI e₀ ↝ ee₀ : (τ̂₀@r₀) & φ₀ ⟹ Γ̂ ⊢_RI fn_π x=>e₀ ↝ (fn_π x=>ee₀) at r : ((τ̂_x@r_x →^{β.φ₀} τ̂₀@r₀)@r) & {put r}
[fun]    Γ̂[f↦(∀β⃗,[ϱ⃗].τ̂)@r] ⊢_RI fn_π x=>e₀ ↝ (fn_π x=>ee₀) at r : (τ̂@r) & φ
         ⟹ Γ̂ ⊢_RI fun_π f x=>e₀ ↝ (fun_π f[ϱ⃗] x=>ee₀) at r : ((∀β⃗,[ϱ⃗].τ̂)@r) & φ         (β⃗,ϱ⃗ ∉ FV(Γ̂,φ); NO α⃗!)
[app]    Γ̂ ⊢_RI e₁ ↝ ee₁ : ((τ̂₂@r₂ →^{β₀.φ₀} τ̂₀@r₀)@r₁) & φ₁ ∧ Γ̂ ⊢_RI e₂ ↝ ee₂ : (τ̂₂@r₂) & φ₂
         ⟹ Γ̂ ⊢_RI e₁ e₂ ↝ ee₁ ee₂ : (τ̂₀@r₀) & φ₁ ∪ φ₂ ∪ φ₀ ∪ β₀ ∪ {get r₁}
[if]     adds {get r₀};   [op] adds {get r₁, get r₂, put r};   [let] unions φ₁ ∪ φ₂
[gen₁/₂] generalise α⃗ outside FV(Γ̂, φ);   [ins₁] instantiates ∀α⃗,β⃗ invisibly
[ins₂]   Γ̂ ⊢_RI e ↝ ee : ((∀α⃗,β⃗,[ϱ⃗].τ̂)@r) & φ ⟹ Γ̂ ⊢_RI e ↝ ee[θ ϱ⃗] at r' : ((θ τ̂)@r') & φ ∪ {get r, put r'}
[region] Γ̂ ⊢_RI e ↝ ee : (τ̂@r) & φ ⟹ Γ̂ ⊢_RI e ↝ letregion ϱ⃗ in ee : (τ̂@r) & φ'
         if φ' = Observe(Γ̂, τ̂, r)(φ)  AND  ϱ⃗ occurs in φ but not in φ'
```

### 3.2 Observe Clauses, Decidability, and Comparison with Section 2.6 Shape Analysis

`Figure 5.1` models runtime memory as a stack of extensible boxed arrays `(r1, 1)..(r1, o₁)`, `(r2, 1)..(r2, o₂)`,
`...` pushed on `letregion` entry and popped via `ς₂ ⧹⧹ rn⃗` on exit [PPA Figure 5.1, p. 331] (book p. 331; PDF p. 348).
All **5 clauses of `Observe`** (`pp. 338–339`, split across page break, `F-U5b-06`, `G-U5b-16`)
[PPA §5.4.3, p. 338] (book p. 338; PDF p. 355) [PPA §5.4.3, p. 339] (book p. 339; PDF p. 356):

```text
Observe(Γ̂, τ̂, r')({put r}) = {put r}    if r occurs in Γ̂, τ̂, or r';   ∅ otherwise
Observe(Γ̂, τ̂, r')({get r}) = {get r}    if r occurs in Γ̂, τ̂, or r';   ∅ otherwise
Observe(Γ̂, τ̂, r')(φ₁ ∪ φ₂) = Observe(Γ̂, τ̂, r')(φ₁) ∪ Observe(Γ̂, τ̂, r')(φ₂)
Observe(Γ̂, τ̂, r')(∅)       = ∅
Observe(Γ̂, τ̂, r')(β)       = β          if β occurs in Γ̂, τ̂, or r';   ∅ otherwise
```

- **Why both `[region]` conjuncts are mandatory (`G-U5b-16`, `Examples 5.32–5.33`)**: `Observe` filters only atoms
  already inside `φ`; omitting "`ϱ⃗` occurs in `φ`" lets `x : int @ ϱ₁ & ∅` (`φ = φ' = ∅`) wrap `letregion ϱ₁ in x`
  around an escaping region, causing `[external: CWE-416 use-after-free]` (`Example 5.33` derives
  `[] ⊢_RI e ↝ ee : (int @ ϱ₂) & {put ϱ₂}`, masking `ϱ₁, ϱ₃, ϱ₄, β`
  [PPA Example 5.32, p. 336] (book p. 336; PDF p. 353) [PPA Example 5.33, p. 339] (book p. 339; PDF p. 356)).
- **Decidability & `§2.6` comparison (`G-U5b-15`)**: `[fun]` excludes `α⃗` because full type-polymorphic recursion
  is undecidable, and `Algorithm R` (`[174]`, `[external: Tofte–Birkedal]`) on `β⃗, ϱ⃗` is **syntactically sound, not complete** (`p. 352`)
  [PPA Chapter 5 Concluding Remarks, p. 352] (book p. 352; PDF p. 369).

| Memory Discipline | Section 2.6 Shape Analysis (`SG = (S, H, is)`) | Section 5.4.3 Region Inference (`letregion` + `Observe`) |
| :--- | :--- | :--- |
| **Abstraction & Scope** | Intraprocedural flow-sensitive graphs over `ALoc` [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133) | Interprocedural higher-order type-and-effect translation (`Tables 5.12–5.13`) |
| **Mutation & Aliasing** | Destructive `x.sel := y` with per-cell `kill_{x.sel}` on `X ≠ ∅` | Immutable boxed `SVal`s with unrestricted intra-region aliasing (vs `[external: Rust lifetimes/borrowck]`) |
| **Deallocation & Cost** | No GC (`> 50` graphs on list reverse); `O(2^{\|Var⋆\|})` | `O(1)` bulk stack pop `ς₂ ⧹⧹ rn⃗`; recursive accumulators risk `[external: CWE-400]` retention |

## 4. Concurrent ML Behaviours and End-Matter Extensions (Section 5.5, Figure 5.2, Tables 5.14-5.18)

Section 5.5 tracks **causal action order** on Concurrent ML (`channel_π`, `spawn e₀`, `send e₁ on e₂`, `receive e₀`,
`e₁; e₂`, `ch`), illustrated by `Figure 5.2` (`inp ──▶ [f₁] ──▶ [f₂] ──▶ [id] ──▶ out`) and `Example 5.34` (`node`
and recursive `pipe`) [PPA Figure 5.2, p. 340] (book p. 340; PDF p. 357)
[PPA Example 5.34, p. 340] (book p. 340; PDF p. 357).

### 4.1 Small-Step Contextual SOS (Tables 5.14-5.15) and Behaviour Typing (Tables 5.16-5.17)

Single-hole capture-free contexts `E ::= [] | E e | v E | let x=E in e | if E then e₁ else e₂ | E op e | v op E | send E on e | send v on E | receive E | E; e`
lift sequential reductions `e₁ → e₂` (`Table 5.14`, including OCR-restored `v₁ op v₂ → v`, `G-U5b-26`) to concurrent
pools `CP, PP ⇒ CP', PP'` (`Table 5.15`, `G-U5b-18`) [PPA Table 5.14, p. 341] (book p. 341; PDF p. 358)
[PPA Table 5.15, p. 343] (book p. 343; PDF p. 360):

```text
Table 5.14:  (fn_π x => e) v → e[x ↦ v];    let x = v in e → e[x ↦ v];    v₁ op v₂ → v  (if v₁ op v₂ = v);
             fun_π f x => e → (fn_π x => e)[f ↦ (fun_π f x => e)];
             if true then e₁ else e₂ → e₁;  if false then e₁ else e₂ → e₂;  v; e → e

Table 5.15:  [seq]   CP, PP[p : E[e₁]] ⇒ CP, PP[p : E[e₂]]                        (if e₁ → e₂)
             [chan]  CP, PP[p : E[channel_π]] ⇒ CP ∪ {ch}, PP[p : E[ch]]          (if ch ∉ CP)
             [spawn] CP, PP[p : E[spawn e₀]] ⇒ CP, PP[p : E[()]][p₀ : e₀]         (if p₀ ∉ dom(PP) ∪ {p})
             [comm]  CP, PP[p₁ : E₁[send v on ch]][p₂ : E₂[receive ch]] ⇒ CP, PP[p₁ : E₁[()]][p₂ : E₂[v]]  (p₁ ≠ p₂)
```

- **Capture-free contexts**: the hole of `E` never occurs in the scope of a bound variable, so `E[e]` needs no
  capture-avoiding substitution or environment [PPA §5.5.1, p. 342] (book p. 342; PDF p. 359).
- **Synchronous rendezvous**: `[comm]` fires only between distinct processes `p₁ ≠ p₂`
  [PPA Table 5.15, p. 343] (book p. 343; PDF p. 360).
- **Small-step, not big-step**: `Tables 5.14–5.15` replace the big-step Natural Semantics of `§§5.1–5.4` with
  one-step reductions lifted through evaluation contexts rather than inference rules
  [PPA §5.5.1, p. 341] (book p. 341; PDF p. 358); `[derived]` this gives meaning to the never-returning `h d`
  server loop of `Example 5.34` [PPA Example 5.34, p. 340] (book p. 340; PDF p. 357).

Over mutually recursive `τ̂ ∈ Type_CA ::= α | bool | int | unit | τ̂₁ →^φ τ̂₂ | τ̂ chan r` and
`φ ∈ Ann_CA ::= β | Λ | φ₁; φ₂ | φ₁ + φ₂ | rec β.φ | τ̂ chan r | spawn φ | r!τ̂ | r?τ̂` (`r ∈ Reg_CA ::= {π} | ϱ | r₁∪r₂ | ∅`),
`Tables 5.16–5.17` (`Γ̂ ⊢_CA e : σ̂ & φ`, **zero `Observe` masking**, `G-U5b-18`; `Examples 5.35, 5.37` print bare `C`
for `{C}`, `F-U5b-08`, `G-U5b-21`) specify [PPA Table 5.16, p. 346] (book p. 346; PDF p. 363)
[PPA Table 5.17, p. 347] (book p. 347; PDF p. 364):

```text
[con/var/ch] emit & Λ;   [fn/fun] park φ₀ on τ̂_x →^{φ₀} τ̂₀ & Λ;   [app] φ₁; φ₂; φ₀;   [if] φ₀; (φ₁ + φ₂)
[let/seq]    φ₁; φ₂;     [op] φ₁; φ₂; Λ;   [chan] τ̂ chan {π} & τ̂ chan {π};   [spawn] unit & spawn φ₀
[send]       Γ̂ ⊢_CA e₁:τ̂ & φ₁ ∧ Γ̂ ⊢_CA e₂:τ̂ chan r₂ & φ₂ ⟹ Γ̂ ⊢_CA send e₁ on e₂ : unit & φ₁; φ₂; r₂!τ̂
[receive]    Γ̂ ⊢_CA e₀:τ̂ chan r₀ & φ₀ ⟹ Γ̂ ⊢_CA receive e₀ : τ̂ & φ₀; r₀?τ̂
[sub]        τ̂ ≤ τ̂' ∧ φ ⊑ φ';   [gen] ζ₁,...,ζ_n ∉ FV(Γ̂) ∪ FV(φ);   [ins] dom(θ) ⊆ {ζ₁,...,ζ_n}
```

- **`Example 5.36` `[gen]` guard (`G-U5b-11`, `BKL-009`)**: `channel_A : 'a chan {A} & 'a chan {A}`
  keeps `'a ∈ FV(φ)`, blocking `[gen]` (`let ch = channel_A in (send 1 on ch; send true on ch)` is rejected —
  semantic `[external: Wright value restriction]`) [PPA Example 5.36, p. 346] (book p. 346; PDF p. 363).
- **Downwards closure under general effects (`G-U5b-12`)**: because behaviours contain types (*general effects*,
  `p. 352`), two-stage inference fails and `[gen]` must exclude the **downwards closure** of `FV(Γ̂) ∪ FV(φ)` wrt
  constraints [PPA Chapter 5 Concluding Remarks, p. 352] (book p. 352; PDF p. 369).

### 4.2 Complete 22-Rule Behaviour Preorder (Table 5.18) and Mini Projects 5.1-5.5

All **22 rules and axioms** of `φ₁ ⊑ φ₂` (`Table 5.18`, 9 rules restored from rendered p. 348, `G-U5b-19`,
`G-U5b-20`, `G-U5b-26`) [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365):

```text
Preorder & congruence (6):  φ ⊑ φ;   (φ₁⊑φ₂ ∧ φ₂⊑φ₃) ⟹ φ₁⊑φ₃;   (φ₁⊑φ₂ ∧ φ₃⊑φ₄) ⟹ φ₁;φ₃ ⊑ φ₂;φ₄  &  φ₁+φ₃ ⊑ φ₂+φ₄;
                            φ₁⊑φ₂ ⟹ spawn φ₁ ⊑ spawn φ₂;          φ₁⊑φ₂ ⟹ rec β.φ₁ ⊑ rec β.φ₂
Monoid, + & rec (13):       φ₁;(φ₂;φ₃) ⊑ (φ₁;φ₂);φ₃;   (φ₁;φ₂);φ₃ ⊑ φ₁;(φ₂;φ₃);
                            (φ₁+φ₂);φ₃ ⊑ (φ₁;φ₃)+(φ₂;φ₃);   (φ₁;φ₃)+(φ₂;φ₃) ⊑ (φ₁+φ₂);φ₃;   (* RIGHT-ONLY! *)
                            φ ⊑ Λ;φ;  Λ;φ ⊑ φ;  φ ⊑ φ;Λ;  φ;Λ ⊑ φ;   φ₁ ⊑ φ₁+φ₂;  φ₂ ⊑ φ₁+φ₂;  φ+φ ⊑ φ;
                            rec β.φ ⊑ φ[β ↦ rec β.φ];   φ[β ↦ rec β.φ] ⊑ rec β.φ   (* no polarity condition *)
Channel/IO variance (3):    (τ̂≤τ̂' ∧ τ̂'≤τ̂ ∧ r⊆r') ⟹ τ̂ chan r ⊑ τ̂' chan r';
                            (r₁⊆r₂ ∧ τ̂₁≤τ̂₂) ⟹ r₁!τ̂₁ ⊑ r₂!τ̂₂;      (r₁⊆r₂ ∧ τ̂₂≤τ̂₁) ⟹ r₁?τ̂₁ ⊑ r₂?τ̂₂
```

**Why left-distributivity is omitted (`G-U5b-20`)**: Rewriting `c!1; (d?int + e?int)` to `(c!1; d?int) + (c!1; e?int)`
introduces synchronous `[external: CWE-833 deadlocks]` against `c?int; d!7` (`[external: Session Types / branching-time semantics]`,
plus `[external: CWE-367 TOCTOU]` ordering; note `p. 353` safety-vs-liveness boundary
[PPA Chapter 5 Concluding Remarks, p. 353] (book p. 353; PDF p. 370)).

- **Mini Projects `5.1–5.5` (`G-U5b-24`, `G-U5b-25`, cf. `BKL-030`)**:
  - `5.1` Call-Tracking `Γ̂ ⊢_CT e : τ̂ & φ` ([PPA Mini Project 5.1, p. 353] (book p. 353; PDF p. 370));
  - `5.2` Pairs `τ̂₁ ×^φ τ̂₂` & Lists `τ̂ list^φ` ([PPA Mini Project 5.2, p. 354] (book p. 354; PDF p. 371));
  - `5.3` SML/Haskell `𝒲_CFA` prototype ([PPA Mini Project 5.3, p. 355] (book p. 355; PDF p. 372));
  - `5.4` Monotone base types (`S ⊑ D` BTA; `C₁ ⊑ ··· ⊑ C_k` `[external: Volpano–Smith–Irvine]` clearance,
    requiring `ACC` and `[external: implicit-flow pc]` bounds on mutable stores, cf. `BKL-030`
    [PPA Mini Project 5.4, p. 355] (book p. 355; PDF p. 372) [PPA Mini Project 5.4, p. 356] (book p. 356; PDF p. 373));
  - `5.5` Units of Measure & Y2K (`num^{scale BASE base}`): **`[external: abelian-group]`** `scale` (`meter.feet = feet.meter`,
    `scale.unit = scale`, `scale.scale^{-1} = unit`) + **`[external: affine-torsor]`** `base` operator schemes (`p. 358`)
    [PPA Mini Project 5.5, p. 357] (book p. 357; PDF p. 374) [PPA Mini Project 5.5, p. 358] (book p. 358; PDF p. 375):
    ```text
    * : ∀σ₁,σ₂,σ [σ = σ₁.σ₂] : num^{σ₁ BASE none} → num^{σ₂ BASE none} → num^{σ BASE none}
    / : ∀σ₁,σ₂,σ [σ = σ₁.(σ₂^{-1})] : num^{σ₁ BASE none} → num^{σ₂ BASE none} → num^{σ BASE none}
    + : ∀σ,β₁,β₂,β [β = β₁ if β₂=none; β₂ if β₁=none; undefined else (F-U5b-12)] : num^{σ BASE β₁} → num^{σ BASE β₂} → num^{σ BASE β}
    - : ∀σ,β₁,β₂,β [β = β₁ if β₂=none; none if β₁=β₂; undefined otherwise] : num^{σ BASE β₁} → num^{σ BASE β₂} → num^{σ BASE β}
    ```
    Statically blocks `[external: CWE-682]` dimensional, currency (`USD + EURO`), and Y2K epoch (`20th` vs `ad`) bugs.

## 5. Worked Effect/Region/Behaviour Witnesses and End-Matter Exercises (`5.11-5.15`)

| Witness / Exercise | Concrete Program or Specification Task | Core Technical Result & Gotcha Guard | Source Coordinate |
| :--- | :--- | :--- | :--- |
| `Example 5.26` | `new_A x:=1 in (new_B y:=!x in (x:=!y+1; !y+3)) + (new_C x:=!x in (x:=!x+1; !x+1))` | Absence of `B:=` in `φ` justifies unboxing `y` into `let y = !x`, while `{new A, new B, new C}` remain unmasked (`G-U5b-03`, `G-U5b-04`) | [PPA Example 5.26, p. 323] (book p. 323; PDF p. 340) |
| `Example 5.27` | `new_A x:=1 in (fn f => f (fn y => !x) + f (fn z => (x:=z; z))) (fn g => g 1)` | Shape-conformant subtyping `≤` coerces reader `int →^{!A} int` and writer `int →^{A:=} int` into `int →^{!A, A:=} int` while keeping closures distinct (`G-U5b-05`) | [PPA Example 5.27, p. 324] (book p. 324; PDF p. 341) [PPA Example 5.27, p. 325] (book p. 325; PDF p. 342) |
| `Example 5.30` | `let f = fn g => fn x => g x in f (fn y => if y < 0 then raise neg else y) (3-2) + f (fn z => if z > 0 then raise pos else 0-z) (2-3)` | Effect-polymorphic `∀'a,'b,'0` isolates `{neg}` and `{pos}` across call sites (`F-U5b-04`) | [PPA Example 5.30, p. 329] (book p. 329; PDF p. 346) |
| `Example 5.33` | `(let x = 7 in fn_Y y => y+x) 9` under `Tables 5.12–5.13` | `Observe([], int, ϱ₂)` encapsulates `ϱ₁, ϱ₃, ϱ₄` in `letregion`, leaving `(int @ ϱ₂) & {put ϱ₂}` (`G-U5b-16`) | [PPA Example 5.33, p. 339] (book p. 339; PDF p. 356) |
| `Examples 5.34–5.37` | `node` / `pipe` stream pipeline (`Figure 5.2`) & polymorphic `channel_A` | `spawn(rec '2. ...)` models cyclic pipeline; `[gen]` blocks `send 1 on ch; send true on ch` (`G-U5b-11, 21`) | [PPA Example 5.34, p. 340] (book p. 340; PDF p. 357) [PPA Example 5.35, p. 345] (book p. 345; PDF p. 362) [PPA Example 5.37, p. 349] (book p. 349; PDF p. 366) |
| `Exercise 5.11` | Soundness statement for `Table 5.9` store-passing semantics | Must relate store mutations `ς₁ -> ς₂` against `{!π, π:=, new π} ⊆ φ` via location-to-point map | [PPA Exercise 5.11, p. 361] (book p. 361; PDF p. 378) |
| `Exercise 5.12` | Call-by-name variant of Side Effect Analysis (`Table 5.9`) | Thunk parameters carry latent effects; `[var]` emits parameter thunk effect rather than `∅` (`BKL-031`) | [PPA Exercise 5.12, p. 362] (book p. 362; PDF p. 379) |
| `Exercise 5.13` | Two-pass subeffecting proof normalisation | Pass 1 embeds `∪ φ'` everywhere; Pass 2 pushes slack to axioms & `[fn]/[fun]` (`G-U5b-23`) | [PPA Exercise 5.13, p. 362] (book p. 362; PDF p. 379) |
| `Exercise 5.14` | Dead exception-handler pruning in `[handle]` | Dropping `φ₁` requires **both** `s ∉ φ₂` **and** `AV(φ₂) = ∅` (`G-U5b-10`) | [PPA Exercise 5.14, p. 362] (book p. 362; PDF p. 379) |
| `Exercise 5.15` | Generalising `Table 5.10` conclusions to schemes `σ̂` | Requires scheme subtyping `σ̂ ≤ σ̂'` (`F-U5b-13`: book prints monotype `τ̂ ≤ τ̂'`) | [PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380) |

- **Section 5.4–5.5 backlog & provenance links**: `BKL-009` (`β \ {s} = β`, `AV(φ₂) = ∅`, `[gen]` `FV(φ)` downwards
  closure); `BKL-011` (`PDF` OCR erasures across `Tables 5.9–5.18` & `(5.2)`, `G-U5b-26`); cf. `BKL-026` (analogous `p. 323` operator/operand prose
  slip); cf. `BKL-030` (safety-direction discipline for `Mini Project 5.4` `ACC` & `[external: implicit-flow]` store bounds); `BKL-031` (`CBV` assumption in `Table 5.9`);
  `BKL-078` (`F-U5b-02/03`: runtime `ξ ∈ Loc`, unbraced `ϖ`, `p. 323` `"argument e_1"`, `ref_ϖ` invariance);
  `BKL-079` (`F-U5b-04/13`: `Example 5.30` `'0` indexing, `AV(φ₂) = ∅`, `Exercise 5.15` `σ̂ ≤ σ̂'`);
  `BKL-080` (`F-U5b-05..07`: `Table 5.11` `dom(ς₁)`, `Table 5.12` `σ̂ @ r`, `Table 5.13` `Type_RI` invariance, `Observe` + `ϱ⃗ ∈ φ`);
  `BKL-081` (`F-U5b-08..10`: unbraced `{C}`, `[derived]` positive `rec β.φ`, right-only `;` over `+`); and
  `BKL-082` (`F-U5b-11/12/14`: `p. 350` `§5.1` mis-citation, `Mini Project 5.5` `+` base check, Unit 5b OCR drops).
