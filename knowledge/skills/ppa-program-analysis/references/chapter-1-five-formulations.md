<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-008: Router-owned L1 reference for Chapter 1. -->

# Chapter 1 Reference: One Analysis, Five Formulations

Scope: Chapter 1, §§1.1–1.8, Concluding Remarks, Mini Project 1.1 and Exercises 1.1–1.11, from
[PPA Chapter 1, p. 1] (book p. 1; PDF p. 21) to [PPA Exercise 1.11, p. 33] (book p. 33; PDF p. 53)
(PDF page = book page + 20; blank book p. 34 is omitted from the PDF).
Conventions: canonical locators e.g. `[PPA §1.1, p. 1] (book p. 1; PDF p. 21)`, `[PPA Preface, p. VI] (book p. VI; PDF p. 6)`; `[external]` = non-book terminology; `[derived]` = direct consequence of printed definitions; `⟹` separates inline rule premises from conclusion.
Ground truth: verbatim transcription, examples, exercises and gotcha ledger live in corpus/shards/RAW_SHARD_01_intro.md (which wins on any discrepancy). Closed inventory (no numbered definitions/lemmas/theorems): Tables 1.1–1.6, Figures 1.1–1.3, Examples 1.1–1.7, Mini Project 1.1, Exercises 1.1–1.11 ("at the level of examples" [PPA Chapter 1, p. 1] (book p. 1; PDF p. 21)).

## 1. Shared Setting

**Safe approximation.** Program analysis predicts "safe and computable approximations to the set
of values or behaviours arising dynamically at run-time" [PPA §1.1, p. 1] (book p. 1; PDF p. 21).
A safe answer contains the true answer and possibly more (Figure 1.1)
[PPA Figure 1.1, p. 2] (book p. 2; PDF p. 22). Because termination is undecidable, an analysis may
return a larger set than occurs at run time; the trivially safe answer (everything) is useless, and
results are phrased as "among", for example "the values of y possible at z:=y are among 1 and 2",
not "are 1 and 2" [PPA §1.1, p. 3] (book p. 3; PDF p. 23) (G-U1-01, G-U1-02).

**Soundness direction (BKL-030, G-U1-03, G-U1-19).** In may-analyses ordered by `⊆` (§§1.3–1.5),
larger sets are safe and smaller sets are more precise; in must-components (such as `X` in Table
1.3), smaller sets are safe and larger sets are more precise [PPA §1.6.1, p. 20] (book p. 20; PDF p. 40).

**Semantics based, not semantics directed.** Analyses should be provably correct with respect to a
semantics; the book does not ask that their structure mirror the semantics, and does not cover the
approaches that do [PPA §1.1, p. 3] (book p. 3; PDF p. 23)
[PPA Chapter 1 Concluding Remarks, p. 29] (book p. 29; PDF p. 49) (G-U1-04).

**WHILE and labels.** Abstract syntax only [PPA §1.2, p. 4] (book p. 4; PDF p. 24) (G-U1-05):

```
a ::= x | n | a1 op_a a2
b ::= true | false | not b | b1 op_b b2 | a1 op_r a2
S ::= [x := a]^l | [skip]^l | S1; S2 | if [b]^l then S1 else S2 | while [b]^l do S
```

Assignments, `skip` and tests are the *elementary blocks*. Side condition: "distinct elementary
blocks are initially assigned distinct labels" (BKL-028); dropping it forces reformulation and gives
less accurate analyses [PPA §1.2, p. 3] (book p. 3; PDF p. 23). Unique labels let the analysis run
without explicitly building a flow graph [PPA §1.2, p. 4] (book p. 4; PDF p. 24).

**Reaching Definitions (RD).** An assignment `[x := a]^l` *may reach* a program point if there is
an execution in which `x` was last assigned at `l` when the point is reached; the book notes the
analysis is more properly called reaching assignments. `(x,?)` records a possibly uninitialised
variable, where `?` is a special label not in the program. The result is the pair
`RD = (RD_entry, RD_exit)` [PPA §1.2, p. 4] (book p. 4; PDF p. 24) [PPA §1.2, p. 5] (book p. 5; PDF p. 25).

**Running program (Example 1.1, factorial)** [PPA Example 1.1, p. 4] (book p. 4; PDF p. 24):

```
[y:=x]^1; [z:=1]^2; while [y>1]^3 do ([z:=z*y]^4; [y:=y-1]^5); [y:=0]^6
```

Flow graph edges (Figure 1.2): (1,2), (2,3), (3,4), (4,5), (5,3), (3,6)
[PPA Figure 1.2, p. 6] (book p. 6; PDF p. 26).

**Table 1.1, the least RD solution** [PPA Table 1.1, p. 4] (book p. 4; PDF p. 24):

| l | RD_entry(l) | RD_exit(l) |
| :-- | :-- | :-- |
| 1 | (x,?), (y,?), (z,?) | (x,?), (y,1), (z,?) |
| 2 | (x,?), (y,1), (z,?) | (x,?), (y,1), (z,2) |
| 3 | (x,?), (y,1), (y,5), (z,2), (z,4) | (x,?), (y,1), (y,5), (z,2), (z,4) |
| 4 | (x,?), (y,1), (y,5), (z,2), (z,4) | (x,?), (y,1), (y,5), (z,4) |
| 5 | (x,?), (y,1), (y,5), (z,4) | (x,?), (y,5), (z,4) |
| 6 | (x,?), (y,1), (y,5), (z,2), (z,4) | (x,?), (y,6), (z,2), (z,4) |

Leastness is Exercise 1.7. Adding `(z,2)` to both sets of block 5 stays safe but is less precise;
removing `(z,2)` from both sets of block 6 is unsafe, because some run is then not described
[PPA §1.2, p. 5] (book p. 5; PDF p. 25). Imprecision and unsoundness are therefore asymmetric.

## 2. Comparison Matrix

| Formulation | Where | What is specified | Facts attached to | Result sought | How a result is obtained | Side conditions that must travel with it |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Equational data flow | §1.3.1 | `RD⃗ = F(RD⃗)` over `(P(Var⋆ × Lab⋆))^12` | Entry and exit of each block | Least fixed point of `F` | `F^n(∅⃗)`; Chaotic Iteration (Table 1.5) | `F` monotone; `Var⋆`, `Lab⋆` finite; kill sets range over all labels, `?` included |
| Constraint data flow | §1.3.2 | `RD⃗ ⊒ F(RD⃗)`, same `F` | Entry and exit of each block | Least solution | As for equations | One flow constraint per edge; same least solution as the equations, but more solutions overall |
| Control Flow Analysis | §1.4 | Constraints on `(Ĉ, ρ̂)`, some conditional | Every label (subexpression) and every variable | Least solution | Solving the constraints (Chapter 3) | All subexpressions labelled; label-only facts rely on absence of side effects |
| Abstract Interpretation | §1.5 | `α⃗ ∘ G ∘ γ⃗`, calculated from a collecting semantics `CS⃗ = G(CS⃗)` | Entry and exit of each block | `lfp(α⃗ ∘ G ∘ γ⃗)` | Calculation, then iteration once `Var⋆`, `Lab⋆` are finite | `(α, γ)` is a Galois connection; the trace domain is infinite; result is below `F`, equality open |
| Annotated base types | Table 1.2 | `S : RD1 → RD2` | Pre- and post-sets per statement | A derivation | Manual derivation with guessed loop invariants, or constraint extraction (Chapter 5) | Inclusion reading of the judgement; `[sub]` |
| Annotated type constructors | Table 1.3 | `S : Σ --X-->_RD Σ` | Per statement, as a summary | `X` and `RD` per statement | Syntax-directed traversal when `[sub]` is unused | `X` is a "definitely" set, `RD` a "might" set |
| Effect system | Table 1.4 | `Γ̂ ⊢ e : τ̂ & φ` | Per expression, plus latent effects on arrows | Effect of the expression | Extension of type inference, or constraints solved afterwards (Chapter 5) | Call-by-value; a general language needs subsumption |

Coordinates of the rows: [PPA §1.3.1, p. 6] (book p. 6; PDF p. 26), [PPA §1.3.2, p. 9] (book p. 9; PDF p. 29),
[PPA §1.4, p. 11] (book p. 11; PDF p. 31), [PPA §1.5, p. 13] (book p. 13; PDF p. 33),
[PPA Table 1.2, p. 19] (book p. 19; PDF p. 39), [PPA Table 1.3, p. 21] (book p. 21; PDF p. 41),
[PPA Table 1.4, p. 24] (book p. 24; PDF p. 44).

## 3. Data Flow Analysis, Equational Approach (§1.3.1)

Block equations for the factorial program [PPA §1.3.1, p. 6] (book p. 6; PDF p. 26):

```
RD_exit(1) = (RD_entry(1) \ {(y,l) | l ∈ Lab}) ∪ {(y,1)}
RD_exit(2) = (RD_entry(2) \ {(z,l) | l ∈ Lab}) ∪ {(z,2)}
RD_exit(3) = RD_entry(3)
RD_exit(4) = (RD_entry(4) \ {(z,l) | l ∈ Lab}) ∪ {(z,4)}
RD_exit(5) = (RD_entry(5) \ {(y,l) | l ∈ Lab}) ∪ {(y,5)}
RD_exit(6) = (RD_entry(6) \ {(y,l) | l ∈ Lab}) ∪ {(y,6)}
```

Schema: for `[x := a]^l'`, remove every `(x,l)` and add `(x,l')`; any other block passes its entry
set unchanged. Flow equations [PPA §1.3.1, p. 7] (book p. 7; PDF p. 27):

```
RD_entry(1) = {(x,?), (y,?), (z,?)}
RD_entry(2) = RD_exit(1)        RD_entry(3) = RD_exit(2) ∪ RD_exit(5)
RD_entry(4) = RD_exit(3)        RD_entry(5) = RD_exit(4)        RD_entry(6) = RD_exit(3)
```

General form: `RD_entry(l)` is the union of `RD_exit(l_i)` over all labels `l_i` from which control
might pass to `l` (made precise in Chapter 2); the initial block receives `(x,?)` for every variable
of the program [PPA §1.3.1, p. 7] (book p. 7; PDF p. 27).

**The function F.** The twelve sets form `RD⃗`, and the system reads `RD⃗ = F(RD⃗)` with
`F : (P(Var⋆ × Lab⋆))^12 → (P(Var⋆ × Lab⋆))^12`. Side condition: `Var⋆` and `Lab⋆` are *finite*
subsets of `Var` and `Lab` holding the variables and labels of the program of interest; here
`Var⋆ = {x,y,z}` and `Lab⋆ = {1,...,6,?}`, so the kill sets also remove `(x,?)` (BKL-035, G-U1-06, G-U1-07)
[PPA §1.3.1, p. 7] (book p. 7; PDF p. 27).

**Order.** `RD⃗ ⊑ RD⃗'` iff `RD_i ⊆ RD'_i` for every `i`, making `(P(Var⋆ × Lab⋆))^12` a complete
lattice with least element `∅⃗` and componentwise union [PPA §1.3.1, p. 7] (book p. 7; PDF p. 27)
[PPA §1.3.1, p. 8] (book p. 8; PDF p. 28).

**Monotonicity.** `RD⃗ ⊑ RD⃗'` implies `F(RD⃗) ⊑ F(RD⃗')` [PPA §1.3.1, p. 8] (book p. 8; PDF p. 28);
set difference only ever subtracts a *constant* kill set `{(x,l) | l ∈ Lab}` `[derived]` (G-U1-08).

**Least solution (unnumbered result).** `∅⃗ ⊑ F(∅⃗)`, so by monotonicity and induction
`F^n(∅⃗) ⊑ F^(n+1)(∅⃗)` for all `n`. Because the lattice is a *finite set*, the chain stabilises:
`F^(n+1)(∅⃗) = F^n(∅⃗)` for some `n`, and `F^n(∅⃗)` is a fixed point. It is the least one: every
`RD⃗ = F(RD⃗)` satisfies `F^n(∅⃗) ⊑ RD⃗`. Larger solutions remain semantically sound but are less
useful [PPA §1.3.1, p. 8] (book p. 8; PDF p. 28). Conditions: monotone `F`, start at `∅⃗`, finite lattice.
The general theorems are in Appendix A [PPA §1.3.1, p. 8] (book p. 8; PDF p. 28).

## 4. Data Flow Analysis, Constraint Based Approach (§1.3.2)

Block constraints [PPA §1.3.2, p. 9] (book p. 9; PDF p. 29): an assignment `[x := a]^l'` yields
`RD_exit(l') ⊇ RD_entry(l') \ {(x,l) | l ∈ Lab}` and `RD_exit(l') ⊇ {(x,l')}`; any other block yields
`RD_exit(l') ⊇ RD_entry(l')`.

Flow constraints: `RD_entry(l) ⊇ RD_exit(l')` whenever control may pass from `l'` to `l`, plus
`RD_entry(1) ⊇ {(x,?), (y,?), (z,?)}` because the definition point of uninitialised variables is
unknown [PPA §1.3.2, p. 9] (book p. 9; PDF p. 29). For Figure 1.2 this gives six flow constraints,
one per edge:

```
RD_entry(2) ⊇ RD_exit(1)    RD_entry(3) ⊇ RD_exit(2)    RD_entry(3) ⊇ RD_exit(5)
RD_entry(4) ⊇ RD_exit(3)    RD_entry(5) ⊇ RD_exit(4)    RD_entry(6) ⊇ RD_exit(3)
```

The printed list omits `RD_entry(4) ⊇ RD_exit(3)`; see §12, item E1. The split into two
neat classes "is not a general phenomenon" [PPA §1.3.2, p. 9] (book p. 9; PDF p. 29).

**Equations and inclusions (unnumbered result)** [PPA §1.3.2, p. 10] (book p. 10; PDF p. 30):
collecting the constraints with one left-hand side gives `RD⃗ ⊒ F(RD⃗)` for the *same* `F` as §3.
Every solution of the equations solves the constraints; "the converse is not necessarily the case"
(G-U1-09, G-U1-10, G-U1-11).
Both systems have the *same least solution*: if `RD⃗ ⊒ F(RD⃗)` then `F^n(∅⃗) ⊑ RD⃗`, and `F^n(∅⃗)`
solves the constraints. Caveat: in general the constraints for one left-hand side are generated at
many places in the program and collecting them "may require serious work".

## 5. Control Flow Analysis (§1.4)

Purpose: for each function application, which functions may be applied. Control flow is immediate
for WHILE but must be computed for more advanced imperative, functional and object-oriented
languages [PPA §1.4, p. 10] (book p. 10; PDF p. 30) (G-U1-12, G-U1-13). Because elementary blocks
nest, *every* subexpression is labelled [PPA §1.4, p. 11] (book p. 11; PDF p. 31).

Example 1.2 [PPA Example 1.2, p. 11] (book p. 11; PDF p. 31): `[[fn x => [x]^1]^2 [fn y => [y]^3]^4]^5`.

**Components.** `Ĉ(l)`: the values the subexpression labelled `l` may evaluate to. `ρ̂(x)`: the
values `x` may be bound to. Facts sit on labels, not on entries and exits, because the language
has no side effects [PPA §1.4, p. 11] (book p. 11; PDF p. 31). (The book does not use the name
0-CFA in Chapter 1 `[external]`.)

**Constraint classes** [PPA §1.4, p. 11] (book p. 11; PDF p. 31) [PPA §1.4, p. 12] (book p. 12; PDF p. 32):

```
[fn x => e]^l                     gives  {fn x => e} ⊆ Ĉ(l)
[x]^l                             gives  ρ̂(x) ⊆ Ĉ(l)
[e1 e2]^l, candidate [fn x => e0]^l0 (body e0 labelled l_body), conditional on the candidate:
    {fn x => e0} ⊆ Ĉ(l1)  ⇒  Ĉ(l2) ⊆ ρ̂(x)        (actual parameter flows to formal)
    {fn x => e0} ⊆ Ĉ(l1)  ⇒  Ĉ(l_body) ⊆ Ĉ(l)    (body result is a result of the application)
```

Here `l1`, `l2` label `e1`, `e2`. For Example 1.2 the conditional constraints are
`{fn x => [x]^1} ⊆ Ĉ(2) ⇒ Ĉ(4) ⊆ ρ̂(x)`, `{fn x => [x]^1} ⊆ Ĉ(2) ⇒ Ĉ(1) ⊆ Ĉ(5)`,
`{fn y => [y]^3} ⊆ Ĉ(2) ⇒ Ĉ(4) ⊆ ρ̂(y)`, `{fn y => [y]^3} ⊆ Ĉ(2) ⇒ Ĉ(3) ⊆ Ĉ(5)`
[PPA §1.4, p. 12] (book p. 12; PDF p. 32). The book states the two application demands in words
and writes the constraints out for Example 1.2 only; the schema form above is `[external]`.

**Least solution** (Exercise 1.2 shows it is the least) [PPA §1.4, p. 12] (book p. 12; PDF p. 32):
`Ĉ(1) = Ĉ(4) = Ĉ(5) = ρ̂(x) = {fn y => [y]^3}`, `Ĉ(2) = {fn x => [x]^1}`, `Ĉ(3) = ρ̂(y) = ∅`.
Smaller sets are more precise. Similarity with §4: the syntax yields constraints whose least
solution is wanted. Difference: conditional constraints give "a more complex structure"
[PPA §1.4, p. 13] (book p. 13; PDF p. 33) (G-U1-14).

## 6. Abstract Interpretation (§1.5)

Stance: a methodology for *calculating* analyses rather than specifying them and validating them
afterwards; to some extent independent of the specification style [PPA §1.5, p. 13] (book p. 13; PDF p. 33).

**Collecting semantics.** `tr ∈ Trace = (Var × Lab)*`. `SRD(tr)(x) = l` iff the rightmost pair for
`x` in `tr` is `(x,l)`; `x ∈ DOM(tr)` iff some `(x,l)` occurs in `tr`
[PPA §1.5, p. 13] (book p. 13; PDF p. 33). Correctness requirement for RD: if `tr` is a possible trace
just before block `l`, then `(x, SRD(tr)(x)) ∈ RD_entry(l)` for all `x ∈ DOM(tr)`
[PPA §1.5, p. 14] (book p. 14; PDF p. 34).

`CS⃗ = G(CS⃗)` over `(P(Trace))^12` mirrors the §3 equations with `CS_exit(l) = {tr : (x,l) | tr ∈ CS_entry(l)}`
for an assignment to `x` at `l`, unions at merge points, and `CS_entry(1) = {((x,?),(y,?),(z,?))}`.
Side conditions: CS specifies a *superset* of the possible traces, since test outcomes are ignored;
`G` is monotone, so a least solution `lfp(G)` exists, but `(P(Trace))^12` is *not finite*, so the
§3 iteration cannot construct it [PPA §1.5, p. 14] (book p. 14; PDF p. 34) [PPA §1.5, p. 15] (book p. 15; PDF p. 35).

**Galois connection** (Figure 1.3) [PPA Figure 1.3, p. 15] (book p. 15; PDF p. 35)
[PPA §1.5, p. 16] (book p. 16; PDF p. 36):

```
α(X) = {(x, SRD(tr)(x)) | x ∈ DOM(tr) ∧ tr ∈ X}
γ(Y) = {tr | ∀x ∈ DOM(tr) : (x, SRD(tr)(x)) ∈ Y}
α(X) ⊆ Y  ⇔  X ⊆ γ(Y)
```

The condition is "often demanded"; when it holds `(α, γ)` is an adjunction or Galois connection.
Verification is left to the reader; `α` and `γ` are written over unstarred `Var × Lab` (BKL-029,
G-U1-15, G-U1-16). Exercise 1.3: each of `α`, `γ` uniquely determines the other
[PPA Exercise 1.3, p. 31] (book p. 31; PDF p. 51).

**Induced analysis.** Lift pointwise to `α⃗`, `γ⃗` and form `α⃗ ∘ G ∘ γ⃗`. Calculating block 4 yields
`RD_exit(4) = (RD_entry(4) \ {(z,l) | l ∈ Lab}) ∪ {(z,4)}`, the §3 equation
[PPA §1.5, p. 16] (book p. 16; PDF p. 36) [PPA §1.5, p. 17] (book p. 17; PDF p. 37); the last step
silently uses that the empty trace and one-pair traces lie in `γ(RD_entry(4))` (`γ(∅) = {Λ}`, BKL-033, G-U1-17).

**Soundness and optimality (unnumbered result)** [PPA §1.5, p. 17] (book p. 17; PDF p. 37):

```
α⃗(lfp(G))  ⊑  lfp(α⃗ ∘ G ∘ γ⃗)  ⊑  lfp(F)
```

The middle term equals `(α⃗ ∘ G ∘ γ⃗)^n(∅⃗)` once `Var⋆`, `Lab⋆` are finite. Exercise 1.4 supplies
`α⃗ ∘ G ∘ γ⃗ ⊑ F` [PPA Exercise 1.4, p. 32] (book p. 32; PDF p. 52). Only the collecting semantics needs a
correctness proof; correctness of the induced analysis follows "for free". If `α⃗ ∘ G ∘ γ⃗ = F` the
analysis is *optimal* for the chosen properties; whether that holds here is left open as Exercise 1.4.
Soundness (`⊑`) and optimality (`=`) are separate questions.

## 7. Type and Effect Systems (§1.6)

A WHILE statement maps a state to a state "in case it terminates", hence the trivial judgement
`S : Σ → Σ` [PPA §1.6, p. 17] (book p. 17; PDF p. 37). Two ingredients are distinguished: an *Effect
System* `S : Σ --φ--> Σ` says what happens during execution; an *Annotated Type System*
`S : Σ1 → Σ2` describes properties of states [PPA §1.6, p. 18] (book p. 18; PDF p. 38).

### 7.1 Annotated base types (Table 1.2)

`S : RD1 → RD2` with `RD1, RD2 ∈ P(Var × Lab)`; `init(S)` is the single entry block and `final(S)`
the set of exit blocks [PPA §1.6.1, p. 18] (book p. 18; PDF p. 38).
Table 1.2 [PPA Table 1.2, p. 19] (book p. 19; PDF p. 39):

```
[ass]  [x := a]^l' : RD → ((RD \ {(x,l) | l ∈ Lab}) ∪ {(x,l')})
[skip] [skip]^l' : RD → RD
[seq]  S1 : RD1 → RD2,  S2 : RD2 → RD3              ⟹  S1; S2 : RD1 → RD3
[if]   S1 : RD1 → RD2,  S2 : RD1 → RD2              ⟹  if [b]^l then S1 else S2 : RD1 → RD2
[wh]   S : RD → RD                                  ⟹  while [b]^l do S : RD → RD
[sub]  S : RD2 → RD3                                ⟹  S : RD1 → RD4   if RD1 ⊆ RD2 and RD3 ⊆ RD4
```

**Two readings** [PPA §1.6.1, p. 18] (book p. 18; PDF p. 38) [PPA §1.6.1, p. 19] (book p. 19; PDF p. 39):
the first, "not quite successful", reads equalities, `RD1 = RD_entry(init(S))` and
`⋃{RD_exit(l) | l ∈ final(S)} = RD2`; `[if]` then fails, since two branches seldom produce the same
set. The second, "successful", reads inclusions, `RD1 ⊆ RD_entry(init(S))` and
`RD_exit(l) ⊆ RD2` for all `l ∈ final(S)`; it is closer to the constraint formulation, makes `[sub]`
unproblematic, and `[sub]` repairs `[if]`. `[wh]` treats `RD` as a consistent guess, a fixed-point
property (G-U1-18). Exercise 1.5 asks whether the first reading can be rescued
[PPA Exercise 1.5, p. 32] (book p. 32; PDF p. 52).

Example 1.3 derives the whole factorial program as `{(x,?),(y,?),(z,?)} → {(x,?),(y,6),(z,2),(z,4)}`
using the guessed loop invariant `{(x,?),(y,1),(y,5),(z,2),(z,4)}`, matching Table 1.1
[PPA Example 1.3, p. 20] (book p. 20; PDF p. 40). The rules suffice for manual analysis; an
implementation would extract and solve constraints, the approach of Chapter 5
[PPA §1.6.1, p. 20] (book p. 20; PDF p. 40).

### 7.2 Annotated type constructors (Table 1.3)

`S : Σ --X-->_RD Σ`: `X` is the set of variables that *definitely* are assigned in `S`; `RD` is the
set of reaching definitions that `S` *might* produce; `RD \ X = {(x,l) ∈ RD | x ∉ X}`
[PPA §1.6.1, p. 20] (book p. 20; PDF p. 40) [PPA §1.6.1, p. 21] (book p. 21; PDF p. 41).
Table 1.3 [PPA Table 1.3, p. 21] (book p. 21; PDF p. 41):

```
[ass]  [x := a]^l : Σ --{x}-->_{{(x,l)}} Σ
[skip] [skip]^l : Σ --∅-->_∅ Σ
[seq]  S1 : Σ --X1-->_RD1 Σ,  S2 : Σ --X2-->_RD2 Σ   ⟹  S1; S2 : Σ --X1∪X2-->_((RD1\X2)∪RD2) Σ
[if]   S1 : Σ --X1-->_RD1 Σ,  S2 : Σ --X2-->_RD2 Σ   ⟹  if [b]^l then S1 else S2 : Σ --X1∩X2-->_(RD1∪RD2) Σ
[wh]   S : Σ --X-->_RD Σ                             ⟹  while [b]^l do S : Σ --∅-->_RD Σ
[sub]  S : Σ --X-->_RD Σ                             ⟹  S : Σ --X'-->_RD' Σ   if X' ⊆ X and RD ⊆ RD'
```

Side conditions [PPA §1.6.1, p. 21] (book p. 21; PDF p. 41): `[if]` intersects `X` (the path is
unknown) but unions `RD`; `[wh]` gives `∅` because the body may not run; `[sub]` shrinks `X` and grows
`RD`, so "safe" points in opposite directions for the two components (BKL-030, G-U1-19). Without
`[sub]` the implementation is a syntax-directed traversal.

Example 1.4 gives the whole program `Σ --{y,z}-->_{{(y,6),(z,2),(z,4)}} Σ`
[PPA Example 1.4, p. 21] (book p. 21; PDF p. 41). The judgement records what a statement *produces*,
so it contains no `(x,?)` and is not a row of Table 1.1; the book calls it a "higher-order
formulation" [PPA Example 1.4, p. 22] (book p. 22; PDF p. 42) (G-U1-20).

Mini Project 1.1 proves Table 1.3 correct (assuming `Var⋆` and `Lab⋆` finite and non-empty, G-U1-21,
G-U1-22) by mapping statements to regular expressions over `{!^l_x}` and applying homomorphisms
`h_y` and `h^l'_y`; it requires Appendix C and induction on the shape of inference trees
[PPA Mini Project 1.1, p. 29] (book p. 29; PDF p. 49) [PPA Mini Project 1.1, p. 30] (book p. 30; PDF p. 50)
[PPA Mini Project 1.1, p. 31] (book p. 31; PDF p. 51).

### 7.3 Effect system: Call-Tracking Analysis (Table 1.4)

Underlying types for `fn_π x => e` (named abstraction) and `e1 e2`: `Γ ⊢ e : τ`, with a guessed
parameter type in the abstraction rule and equal formal and actual parameter types in the
application rule [PPA §1.6.2, p. 22] (book p. 22; PDF p. 42) [PPA §1.6.2, p. 23] (book p. 23; PDF p. 43).
Specification: for each subexpression, which abstractions may be applied during its evaluation
[PPA §1.6.2, p. 23] (book p. 23; PDF p. 43). Table 1.4 [PPA Table 1.4, p. 24] (book p. 24; PDF p. 44):

```
[var]  Γ̂ ⊢ x : τ̂_x & ∅                     if Γ̂(x) = τ̂_x
[fn]   Γ̂[x ↦ τ̂_x] ⊢ e : τ̂ & φ              ⟹  Γ̂ ⊢ fn_π x => e : τ̂_x --φ∪{π}--> τ̂ & ∅
[app]  Γ̂ ⊢ e1 : τ̂2 --φ--> τ̂ & φ1,  Γ̂ ⊢ e2 : τ̂2 & φ2   ⟹  Γ̂ ⊢ e1 e2 : τ̂ & φ1 ∪ φ2 ∪ φ
```

Annotated types `τ̂ ::= base | τ̂1 --φ--> τ̂2`; the arrow carries a *latent effect*
[PPA §1.6.2, p. 24] (book p. 24; PDF p. 44). Side conditions [PPA §1.6.2, p. 24] (book p. 24; PDF p. 44)
[PPA §1.6.2, p. 25] (book p. 25; PDF p. 45): `[var]` and `[fn]` have empty effect because evaluation
is call-by-value and an abstraction only builds a closure (BKL-031, G-U1-23, G-U1-24, G-U1-25); `[app]` unions
the operator's effect, the operand's effect and the latent effect.
Example 1.6: `(fn_X x => x) (fn_Y y => y) : int --{Y}--> int & {X}`
[PPA Example 1.6, p. 25] (book p. 25; PDF p. 45). A more general language needs a subsumption rule,
and effects are computed on the fly during type inference or by constraints solved afterwards
(Chapter 5) [PPA §1.6.2, p. 25] (book p. 25; PDF p. 45).

## 8. Solving: Chaotic Iteration (§1.7, Table 1.5)

Problem: the least `RD⃗` with `RD⃗ = F(RD⃗)` or `RD⃗ ⊒ F(RD⃗)`, `F` monotone; the lattice is finite, so
the answer is `F^n(∅⃗)` once it stabilises [PPA §1.7, p. 25] (book p. 25; PDF p. 45).
Table 1.5 [PPA Table 1.5, p. 26] (book p. 26; PDF p. 46):

```
INPUT:  Example equations for Reaching Definitions
OUTPUT: The least solution RD⃗ = (RD_1, ..., RD_12)
METHOD: Step 1: RD_1 := ∅; ...; RD_12 := ∅
        Step 2: while RD_j ≠ F_j(RD_1, ..., RD_12) for some j
                do RD_j := F_j(RD_1, ..., RD_12)
```

Properties (unnumbered result) [PPA §1.7, p. 26] (book p. 26; PDF p. 46): the algorithm is
non-deterministic; if it terminates the result is a fixed point; the invariant
`∅⃗ ⊑ RD⃗ ⊑ F(RD⃗) ⊑ F^n(∅⃗)` holds initially and is preserved (Exercise 1.6), so the result is the least
fixed point; each update strictly enlarges one component, and the lattice is finite, so it terminates
(G-U1-26, G-U1-27). The invariant depends on starting at `∅⃗`; implementation order is deferred to Chapters 2 and 6.

## 9. Consuming: Constant Folding (§1.8, Table 1.6)

Judgements `RD ⊢ S ▷ S'`, where `RD` is "a solution (preferable the least)" for the whole program,
each expressing one step [PPA §1.8, p. 27] (book p. 27; PDF p. 47) [PPA §1.8, p. 28] (book p. 28; PDF p. 48).
Table 1.6 [PPA Table 1.6, p. 27] (book p. 27; PDF p. 47):

```
[ass1] RD ⊢ [x := a]^l ▷ [x := a[y ↦ n]]^l
         if y ∈ FV(a) ∧ (y,?) ∉ RD_entry(l) ∧
            ∀(z,l') ∈ RD_entry(l) : (z = y ⇒ [...]^l' is [y := n]^l')
[ass2] RD ⊢ [x := a]^l ▷ [x := n]^l      if FV(a) = ∅ ∧ a ∉ Num ∧ a evaluates to n
[seq1] RD ⊢ S1 ▷ S1'  ⟹  RD ⊢ S1; S2 ▷ S1'; S2
[seq2] RD ⊢ S2 ▷ S2'  ⟹  RD ⊢ S1; S2 ▷ S1; S2'
[if1]  RD ⊢ S1 ▷ S1'  ⟹  RD ⊢ if [b]^l then S1 else S2 ▷ if [b]^l then S1' else S2
[if2]  RD ⊢ S2 ▷ S2'  ⟹  RD ⊢ if [b]^l then S1 else S2 ▷ if [b]^l then S1 else S2'
[wh]   RD ⊢ S ▷ S'    ⟹  RD ⊢ while [b]^l do S ▷ while [b]^l do S'
```

Side conditions [PPA §1.8, p. 28] (book p. 28; PDF p. 48): no order of application is prescribed;
the relation is neither reflexive nor transitive, so a result is a sequence of steps (Example 1.7;
Exercise 1.9 modifies block 3 to `[z:=y+x]^3` where `(x,?)` blocks folding `x`, G-U1-30); tests are
not rewritten (Exercise 1.10; G-U1-28, G-U1-29). Re-using one `RD` across steps is valid here
[PPA §1.8, p. 29] (book p. 29; PDF p. 49) because folding changes only right-hand sides, leaving
labels, assigned variables and flow fixed `[derived]` (BKL-032). Re-analysis after transformations
in general is omitted [PPA Preface, p. VI] (book p. VI; PDF p. 6) (G-U1-31, G-U1-32, G-U1-33).

## 10. Relationships the Source States

| Relationship | Coordinate |
| :--- | :--- |
| Equations and inclusions over one `F` share the least solution; inclusions admit more solutions | [PPA §1.3.2, p. 10] (book p. 10; PDF p. 30) |
| Data flow constraints and control flow constraints: in both, syntax yields constraints whose least solution is wanted | [PPA §1.4, p. 13] (book p. 13; PDF p. 33) |
| The induced analysis is below `F`; both are correct with respect to the collecting semantics | [PPA §1.5, p. 17] (book p. 17; PDF p. 37) |
| The inclusion reading of Table 1.2 is closer to the constraint formulation; subsumption plays the role of inclusion | [PPA §1.6.1, p. 19] (book p. 19; PDF p. 39) |
| Table 1.2 with constraint extraction is the idea behind Chapter 5 | [PPA §1.6.1, p. 20] (book p. 20; PDF p. 40) |
| Chaotic Iteration lies at the heart of the efficient algorithms of Chapters 2 and 6 | [PPA §1.7, p. 25] (book p. 25; PDF p. 45) |
| Some Annotated Type Systems are closely related to Hoare's logic for partial correctness | [PPA Chapter 1 Concluding Remarks, p. 29] (book p. 29; PDF p. 49) |
| The chapter shows "a few approaches (but by no means all)" | [PPA Chapter 1 Concluding Remarks, p. 29] (book p. 29; PDF p. 49) |

Order-theoretic background is in Appendix A, induction/coinduction in Appendix B, and directed
graphs/regular path sets in Appendix C; all three are references of this skill.

## 11. Table and Figure Coordinates

| Item | Caption | Section | Book p. | PDF p. |
| :--- | :--- | :--- | ---: | ---: |
| Table 1.1 | Reaching Definitions information for the factorial program | §1.2 | 4 | 24 |
| Table 1.2 | Reaching Definitions: annotated base types | §1.6.1 | 19 | 39 |
| Table 1.3 | Reaching Definitions: annotated type constructors | §1.6.1 | 21 | 41 |
| Table 1.4 | Call-tracking Analysis: Effect System | §1.6.2 | 24 | 44 |
| Table 1.5 | Chaotic Iteration for Reaching Definitions | §1.7 | 26 | 46 |
| Table 1.6 | Constant Folding transformation | §1.8 | 27 | 47 |
| Figure 1.1 | The nature of approximation: erring on the safe side | §1.1 | 2 | 22 |
| Figure 1.2 | Flow graph for the factorial program | §1.3 | 6 | 26 |
| Figure 1.3 | The adjunction (α, γ) | §1.5 | 15 | 35 |

## 12. Chapter 1 Source Errata (Recorded as Found)

The L3 shard records the source as printed. The readings below are the ones adopted above L3.

- **E1. Missing flow constraint, p. 9 (BKL-025).** The printed flow constraints omit `RD_entry(4) ⊇ RD_exit(3)`
  [PPA §1.3.2, p. 9] (book p. 9; PDF p. 29). It is required by the stated rule ("if it is possible
  for control to pass from l' to l"), by edge (3,4) of Figure 1.2, by the equation
  `RD_entry(4) = RD_exit(3)` [PPA §1.3.1, p. 7] (book p. 7; PDF p. 27), and by the claim of a shared
  least solution [PPA §1.3.2, p. 10] (book p. 10; PDF p. 30). Taken literally, the printed system's
  least solution has `RD_entry(4) = ∅`, which is unsound. Reading adopted: six flow constraints.
- **E2. "Operand" for operator, p. 25 (BKL-026).** The explanation of `[app]` attributes the arrow type
  `τ̂2 --φ--> τ̂` to "the operand" [PPA §1.6.2, p. 25] (book p. 25; PDF p. 45); by Table 1.4 that type
  belongs to the operator `e1` [PPA Table 1.4, p. 24] (book p. 24; PDF p. 44). Wording only.
- **E3. `h_y` applied twice, p. 30 (BKL-027).** The correctness condition for `X` is stated as
  `¬∃w ∈ ℒ⟦h_y(𝒮(S))⟧ : h_y(w) = Λ` [PPA Mini Project 1.1, p. 30] (book p. 30; PDF p. 50). Here `w`
  already lies in the image language over `{!}`, outside the domain of `h_y`. The parallel RD
  condition quantifies over `ℒ⟦𝒮(S)⟧` [PPA Mini Project 1.1, p. 31] (book p. 31; PDF p. 51). Reading
  adopted: `¬∃w ∈ ℒ⟦𝒮(S)⟧ : h_y(w) = Λ`.

Further notes, none of which changes a result:

- The schema after the block equations says "x is redefined at l" where the assignment is labelled
  `l'` (BKL-034) [PPA §1.3.1, p. 6] (book p. 6; PDF p. 26).
- `𝒮(while b do S)` omits `[b]^l` (BKL-027) and collides with Ch. 6 `𝒮(S)` (BKL-024)
  [PPA Mini Project 1.1, p. 30] (book p. 30; PDF p. 50).
- `?` denotes both the uninitialised label [PPA §1.2, p. 5] (book p. 5; PDF p. 25) and a letter of
  `h^l'_y` (BKL-035) [PPA Mini Project 1.1, p. 31] (book p. 31; PDF p. 51).
- Exercise 1.11 writes `y = z ⇒` and `RD'_entry` where Table 1.6 writes `z = y ⇒` and `RD` (BKL-034)
  [PPA Exercise 1.11, p. 33] (book p. 33; PDF p. 53).
- OCR corrupts Chapter 1 formulae; above formulae follow visual inspection of the L3 shard.
