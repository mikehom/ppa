<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: L3 notation index (Index of Notation, book pp. 429-432) with typeface disambiguation. -->

# PPA Notation Index (L3)

Complete transcription of the book's three-part Index of Notation
[PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) across book pages 429–432 (PDF pages 443–446): 22 symbol patterns,
57 Greek entries and 253 Latin entries (332 rows). Every row was checked against
the printed page; the PDF text layer of these pages drops digits from page references, loses
the operand boxes and misreads Greek letters, so it was not used as a source of truth.

## Conventions

- `id`: stable row identifier (N1 = symbol patterns, N2 = Greek, N3 = Latin), numbered in
  book order. Ids are never reused or renumbered.
- `symbol`: Unicode with LaTeX-style structure. `■` is an operand slot (a grey box in the
  book); `_{…}` and `^{…}` are sub- and superscripts; `\widehat{…}` is the hat (abstract
  version), spanning exactly what the book's hat spans; `\vec{…}` is a vector arrow; `⋆` is
  the star subscript; `·` is the dot subscript printed after `ι` and `f`.
- Phi variants are kept distinct: `φ` is the curly phi (TeX `\varphi`, annotations and
  effects); `ϕ` is the straight phi (TeX `\phi`, used for `ϕ_{ℓ}^{SA}` and `l_{n}^{ϕ}`).
  Rho variants: `ρ` (environments) and `ϱ` (TeX `\varrho`, region variables).
- `typeface`: the face of the head identifier as printed: roman (upright serif; operators
  and upper-case Greek), italic, bold, sans (sans-serif), typewriter (fixed-width keywords),
  calligraphic, script (`℘` only). No entry is printed in fraktur or blackboard bold.
  Subscript tags such as CA, CFA, CP, ES, RI, SA, SE, UL, AE, LV, RD, VB are printed in sans;
  `entry`/`exit` subscripts are italic.
- `meaning`: filled only where the book itself states the meaning on one of the listed
  pages; the page given in parentheses is where it is stated. An empty cell means no meaning
  was recorded, not that the book gives none. 330 rows carry a meaning.
- `book pages`: exactly as printed in the index (`VIII` is the Preface).
- `index page`: the index page on which the entry is printed.

## Part 1: Symbol Patterns (22 entries)

Book p. 429. Grey operand boxes are written ■.

| id | symbol | typeface | meaning | book pages | index page |
| :--- | :--- | :--- | :--- | :--- | :--- |
| N1-001 | `■ ↠ ■` | roman | logical relation: v1 R1 l1 and v1 ⇝ v2 imply v2 R2 f(l1) (p. 219) | 214, 219, 220 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-002 | `■ → ■` | roman | e1 → e2: expression e1 evaluates to e2 in one step (p. 341) | 341 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-003 | `■ →_{fin} ■` | roman | the set of finitary functions: partial functions with a finite domain (p. VIII) | VIII | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-004 | `■ : ■ → ■` | roman | S : Σ → Σ, statement S maps a state to a state (p. 17) | 17, 18, 20 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-005 | `■ ≤ ■` | roman | ordering on annotated types derived from the ordering on annotations (p. 324) | 324, 329, 347 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-006 | `■ ⊨ ■` | roman | θA ⊨ C: annotation substitution θA solves constraint set C (p. 309) | 309 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-007 | `■ ∇ ■` | roman | widening operator ∇ : L × L → L (p. 226) | 226 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-008 | `■ \| ■` | roman | ρ restricted to X: removes all occurrences of [x ↦ ...] with x ∉ X (p. 154) | 154, 286 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-009 | `⟦■⟧■` | roman | ⟦t⟧ψ: interpretation of term t with respect to solution ψ (p. 367) | 367 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-010 | `■ ∼ ■` | roman | σ1 ∼V σ2 iff σ1(x) = σ2(x) for all x ∈ V (p. 62) | 62 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-011 | `■ ⊑ ■` | roman | partial ordering on annotations: set φ1 of program points included in set φ2 (p. 298) | 298, 348 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-012 | `■ ⊒ ■` | roman | constraint xi ⊒ ti of a finite constraint system S (p. 367) | 367 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-013 | `■ ⊆ ■` | roman | set φ1 of program points is included in set φ2 (p. 298) | 298 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-014 | `■ ⊇ ■` | roman | constraint β ⊇ φ, β an annotation variable, φ a simple annotation (p. 308) | 308 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-015 | `■ ⊢ ■ : ■` | roman | judgement Γ ⊢ e : τ: Γ types free variables, τ is type of e (p. 22) | 22 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-016 | `■ ⊢ ■ : ■ & ■` | roman | judgement: e has annotated type τ̂ and effect φ under type environment Γ̂ (p. 24) | 24 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-017 | `■ ⊢ ■ ⇝ ■` | roman | p ⊢ v1 ⇝ v2: program p transforms value v1 to value v2 (p. 211) | 211, 219 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-018 | `■ ⊢ ■ ▷ ■` | roman | p ⊢ l1 ▷ l2: analysis of program p transforms property l1 into l2 (p. 212) | 27, 212, 219 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-019 | `■ ⊢ ■ → ■` | roman | ρ ⊢ ie1 → ie2: transition judgements of the Structural Operational Semantics (p. 154) | 154 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-020 | `■ ⊢_{⋆} ■ → ■` | roman | transitions of statements given relative to environment ρ (p. 86) | 86 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-021 | `⌊■⌋` | roman | ⌊τ̂⌋: the underlying type corresponding to the annotated type τ̂ (p. 287) | 287 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N1-022 | `⋄` | roman | special constant reflecting the nil value (p. 105) | 105 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |

## Part 2: Notation Beginning with a Greek Letter (57 entries)

Book pp. 429-430, in book order (the book sorts by the Latin name of the letter).

| id | symbol | typeface | meaning | book pages | index page |
| :--- | :--- | :--- | :--- | :--- | :--- |
| N2-001 | `α` | italic | abstraction function extracting reachability information present in a set of traces (p. 15) | 15, 300, 306 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-002 | `α_{η}` | italic | abstraction function of the Galois connection defined by extraction function η (p. 237) | 237 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-003 | `β` | italic | representation function mapping a value to the best property describing it (p. 216) | 216, 306 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-004 | `β ⊇ φ` | italic | constraint: inclusion where β is an annotation variable and φ a simple annotation (p. 308) | 308 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-005 | `β_{1} ↠ β_{2}` | italic | representation function defined from β1 and β2, generating R1 ↠ R2 (p. 220) | 220 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-006 | `β_{R}` | italic | representation function defined from correctness relation R: βR(v) = ⊓{l : v R l} (p. 217) | 217 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-007 | `β_{η}` | italic | representation function βη(v) = {η(v)} defined from extraction function η (p. 237) | 237 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-008 | `Δ` | roman | context information (δ ∈ Δ) (p. 91) | 91, 96, 97, 99, 100, 191, 230 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-009 | `δ` | italic | context information (p. 91) | 91, 191 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-010 | `[δ, ℓ]` | italic | path obtained by appending ℓc to δ (p. 96) | 96 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-011 | `⌈δ, ℓ⌉_{k}` | italic | call string [δ, ℓc] possibly truncated on the left to length at most k (p. 98) | 98, 193 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-012 | `\widehat{δ}` | italic | abstract data environment, Var → Data (p. 187) | 187 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-013 | `η` | italic | extraction function η : V → D mapping values to their descriptions in D (p. 237) | 237 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-014 | `η[V]` | italic | image of η: the set of η(v) for v ∈ V (p. 246) | 246 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-015 | `Γ` | roman | type environment giving types to all free variables of e (p. 22) | 22, 285 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-016 | `Γ ⊢ e : τ` | roman | judgement: e has type τ, Γ gives types to free variables (p. 22) | 22 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-017 | `Γ \| X` | roman | type environment obtained from Γ by removing all [x ↦ ...] with x ∉ X (p. 286) | 286 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-018 | `\widehat{Γ} ⊢ e : \widehat{τ} & φ` | roman | judgement: e has annotated type τ̂ and effect φ under type environment Γ̂ (p. 24) | 24 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-019 | `\widehat{Γ}` | roman | type environment giving annotated types of all free variables (p. 24) | 24, 287, 307, 321 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-020 | `γ` | italic | concretisation function producing all traces consistent with given reachability information (p. 15) | 15 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-021 | `γ_{η}` | italic | concretisation function of the Galois connection defined by extraction function η (p. 237) | 237 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-022 | `ι` | italic | extremal value ι ∈ L for the extremal labels (p. 69) | 69 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-023 | `ι_{E}^{ℓ}` | italic | ι if ℓ ∈ E, ⊥ if ℓ ∉ E (p. 69) | 66, 69 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-024 | `ι_{·}` | italic | mapping from constants c to values in L, giving their extremal value (p. 186) | 186 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-025 | `\widehat{ι}` | italic | extremal value: ι̂(δ) is ι if δ = Λ, ⊥ otherwise (p. 96) | 96, 97, 99, 100 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-026 | `Λ` | roman | behaviour for atomic actions that do not involve communication (p. 344) | 344 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-027 | `λ` | italic | λx.…x… stands for the unary function f defined by f(x) = …x… (p. VIII) | VIII | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-028 | `ϕ_{ℓ}^{SA}` | italic | specifies how block ℓ transforms a single shape graph into a set of shape graphs (p. 116) | 116 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-029 | `φ` | italic | effect: names of function abstractions that might be applied (p. 24) | 24, 287, 306, 321, 327, 335, 343 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-030 | `φ ⊑ φ′` | italic | ordering on behaviours, axiomatised in Table 5.18 (p. 348) | 348 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-031 | `φ_{1} ⊑ φ_{2}` | italic | set φ1 of program points is included in set φ2 (p. 298) | 298 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-032 | `φ_{1} ⊆ φ_{2}` | italic | set φ1 of program points is included in set φ2 (p. 298) | 298 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-033 | `π` | italic | program points, used to name the function abstractions in the program (p. 284) | 284 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-034 | `ψ` | italic | solution: total function ψ : X → L assigning each flow variable a value (p. 367) | 367 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-035 | `ρ` | italic | environment mapping the variables in the current scope to their locations (p. 86) | 86, 153, 333 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-036 | `ρ ⊢_{⋆} ⟨S, ς⟩ → ⟨S′, ς′⟩` | italic | transition when the computation does not terminate in one step (p. 86) | 86 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-037 | `ρ ⊢_{⋆} ⟨S, ς⟩ → ς′` | italic | transition when the computation terminates in one step (p. 86) | 86 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-038 | `ρ \| X` | italic | environment obtained from ρ by removing all [x ↦ ...] with x ∉ X (p. 154) | 154 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-039 | `\widehat{ρ}` | italic | abstract environment associating abstract values with each variable (p. 144) | 11, 144, 187, 191 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-040 | `ρ_{⋆}` | italic | top-level environment giving the locations of the program's global variables (p. 86) | 86 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-041 | `ϱ` | italic | region variables (p. 331) | 331 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-042 | `\vec{ϱ}` | italic | possibly empty sequence ϱ1, ..., ϱk of region variables (p. 332) | 332 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-043 | `Σ` | roman | the type of states (p. 17) | 17 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-044 | `σ` | italic | state: a mapping from variables to integers (p. 54) | 54, 105 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-045 | `σ_{1} ∼_{V} σ_{2}` | italic | σ1 and σ2 agree on all variables in V (correctness relation) (p. 62) | 62 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-046 | `\widehat{σ}` | italic | type scheme ∀(ζ1, ..., ζn).τ̂ (p. 327) | 327, 335, 343 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-047 | `ς` | italic | store, specifying the values of locations (p. 86) | 86, 244, 320, 333 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-048 | `ς[M]` | italic | complete lattice of all ς(m) for m ∈ M, ordered by ⊑M (p. 244) | 244 | [PPA Index of Notation, p. 429] (book p. 429; PDF p. 443) |
| N2-049 | `ς_{η}` | italic | reduction operator given by extraction function η: ςη(D′) = D′ ∩ η[V] (p. 246) | 246 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N2-050 | `τ` | italic | types: int, bool and function types τ1 → τ2 (p. 285) | 285, 300 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N2-051 | `\widehat{τ} ≤ \widehat{τ}′` | italic | ordering on annotated types derived from the ordering on annotations (p. 324) | 324, 329, 347 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N2-052 | `\widehat{τ}_{1} ⊑ \widehat{τ}_{2}` | italic | whenever τ̂1 has annotation φ1 at a position, τ̂2 has φ2 with φ1 ⊑ φ2 (p. 298) | 298 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N2-053 | `\widehat{τ}` | italic | annotated type: a base type or τ̂1 →φ τ̂2 with effect φ (p. 24) | 24, 287, 306, 321, 327, 335, 343 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N2-054 | `θ` | italic | substitution: finite partial mapping from type variables to augmented types (p. 301) | 301 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N2-055 | `θ_{A} ⊨ C` | italic | annotation substitution θA solves constraint set C (p. 309) | 309 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N2-056 | `ξ` | italic | locations (addresses) (p. 86) | 86, 105, 320 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N2-057 | `ζ` | italic | type variables and annotation variables listed in a type scheme (p. 327) | 327 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |

## Part 3: Notation Beginning with a Latin Letter (253 entries)

Book pp. 430-432, in book order, "regardless of the font used".

| id | symbol | typeface | meaning | book pages | index page |
| :--- | :--- | :--- | :--- | :--- | :--- |
| N3-001 | `𝒜` | calligraphic | semantic function for arithmetic expressions, AExp → (State → Z) (p. 55) | 55, 108 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-002 | `𝒜_{CP}` | calligraphic | function analysing arithmetic expressions for Constant Propagation, AExp → (State_CP → Z^⊤_⊥) (p. 73) | 73 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-003 | `a` | italic | ranges over arithmetic expressions (AExp) (p. 3) | 3 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-004 | `AE_{entry}` | sans | Available Expressions function mapping labels to sets of expressions, at block entry (p. 40) | 40 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-005 | `AE_{exit}` | sans | Available Expressions function mapping labels to sets of expressions, at block exit (p. 40) | 40 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-006 | `AExp_{⋆}` | bold | the set of non-trivial arithmetic subexpressions in S⋆ (p. 39) | 39 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-007 | `AExp` | bold | syntactic category of arithmetic expressions (p. 3) | 3 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-008 | `AExp(·)` | bold | set of non-trivial arithmetic subexpressions of a given arithmetic or boolean expression (p. 39) | 39 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-009 | `AHeap` | bold | abstract heaps, P(ALoc × Sel × ALoc), specifying links between abstract locations (p. 111) | 111, 114 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-010 | `ALoc` | bold | abstract locations n_X where X is a subset of Var⋆ (p. 110) | 110 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-011 | `ALoc(H)` | italic | the set of abstract locations occurring in the abstract heap H (p. 111) | 111 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-012 | `ALoc(S)` | italic | the set of abstract locations occurring in the abstract state S (p. 111) | 111 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-013 | `Analysis^{=}` | sans | set of equations to which an instance of a Monotone Framework gives rise (p. 69) | 69 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-014 | `Analysis^{⊑}` | sans | set of constraints to which an instance of a Monotone Framework gives rise (p. 69) | 69 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-015 | `Analysis` | sans | array representing the least solution computed by the worklist algorithm (p. 369) | 369 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-016 | `Analysis` | italic | generic analysis in the common equation form of the four classical analyses (p. 65) | 65 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-017 | `Ann_{CA}` | bold | annotations (or behaviours) of the Communication Analysis (p. 343) | 343 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-018 | `Ann` | bold | annotations: sets of function names describing which function definitions may result (p. 287) | 287 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-019 | `Ann_{ES}` | bold | annotations (or effects) of the Exception Analysis: sets of exceptions (p. 327) | 327 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-020 | `Ann_{RI}` | bold | effects of Region Inference: regions where data is put or accessed (p. 335) | 335 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-021 | `Ann_{SE}` | bold | annotations (or effects) of the Side Effect Analysis (p. 321) | 321 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-022 | `AState` | bold | abstract states, P(Var⋆ × ALoc), mapping variables to abstract locations (p. 110) | 110, 114 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-023 | `AType` | bold | augmented types, allowing type variables (p. 300) | 300 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-024 | `AV` | italic | set of directly assigned variables of a statement, ignoring procedure calls (p. 101) | 101, 317 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-025 | `AVar` | bold | annotation variables (p. 306) | 306 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-026 | `ℬ` | calligraphic | semantic function for boolean expressions, BExp → (State → T) (p. 55) | 55, 108 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-027 | `b` | italic | ranges over boolean expressions (BExp) (p. 3) | 3 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-028 | `BExp` | bold | syntactic category of boolean expressions (p. 3) | 3 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-029 | `BExp(·)` | bold | indexed at p. 39, where the text instead prints `AExp(b)` (see Index Anomalies) | 39 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-030 | `bind-construct` | typewriter | combines a procedure body with the environment in which it must be executed (p. 87) | 87, 154 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-031 | `[B]^{ℓ}` | italic | elementary block `B` bearing label `ℓ` (p. 37) | 37 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-032 | `Blocks_{⋆}` | bold | the elementary blocks (blocks(S⋆)) occurring in S⋆ (p. 38) | 38 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-033 | `blocks_{⋆}` | italic | elementary blocks of the entire program P⋆, including procedure declarations (p. 84) | 84 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-034 | `blocks` | italic | function returning the elementary blocks (statements or tests) of a statement (p. 36) | 36, 83 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-035 | `C` | italic | constraint set: finite set of constraints β ⊇ φ on annotation variables (p. 308) | 308 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-036 | `\widehat{C}` | sans | abstract cache associating abstract values with each labelled program point (p. 144) | 11, 144, 187, 193 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-037 | `𝒞_{⋆}` | calligraphic | function defining the constraint based 0-CFA analysis, generating a set of constraints (p. 174) | 174 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-038 | `c` | italic | ranges over constants (p. 142) | 142, 284 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-039 | `\widehat{Cache}` | bold | abstract caches, Lab → abstract values (p. 144) | 144, 187, 193 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-040 | `ce` | italic | context environment determining the context of the current instance of a variable (p. 191) | 191 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-041 | `CEnv` | bold | context environments, Var → Δ (p. 191) | 191 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-042 | `ch` | italic | ranges over channel identifiers (p. 339) | 339 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-043 | `Chan` | bold | channel identifiers (p. 339) | 339 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-044 | `clear` | italic | predicate: definition clear path for x from ℓ to ℓ′ (p. 52) | 52 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-045 | `close-construct` | typewriter | closure: function definition together with an environment for its free variables (p. 153) | 153 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-046 | `Const` | bold | constants (including the truth values) (p. 142) | 142, 284 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-047 | `CP` | italic | set of immediately called procedures of a statement (p. 102) | 102 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-048 | `CP` | italic | finite set of channels generated so far (p. 342) | 342 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-049 | `CS` | sans | the collecting semantics (p. 14) | 14 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-050 | `cycles` | italic | set of cycles (non-trivial paths) from a node n to itself (p. 418) | 418 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-051 | `D_{⋆}` | italic | the sequence of procedure declarations of the program (p. 82) | 82 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-052 | `\widehat{D}` | sans | abstract data cache, Lab → abstract data values (p. 187) | 187 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-053 | `\widehat{d}` | italic | ranges over abstract data values (elements of L) (p. 187) | 187 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-054 | `d_{c}` | italic | element of Data specifying the abstract property of constant c (p. 182) | 182 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-055 | `d_{op}` | italic | function Data × Data → P(Data) giving how op computes on abstract properties (p. 183) | 183 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-056 | `Data` | bold | set of abstract data values (abstract properties of booleans and integers) (p. 182) | 182 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-057 | `\widehat{Data}` | bold | abstract data values, the complete lattice L (p. 187) | 187 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-058 | `\widehat{DCache}` | bold | abstract data caches, Lab → abstract data values (p. 187) | 187 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-059 | `def` | italic | predicate checking whether the variable is assigned in a block (p. 52) | 52 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-060 | `\widehat{DEnv}` | bold | abstract data environments, Var → abstract data values (p. 187) | 187 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-061 | `DOM` | sans | set of variables for which SRD(tr) is defined (p. 13) | 13 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-062 | `dom` | italic | domain: the set of arguments on which a partial mapping is defined (p. 86) | 86, 154, 286, 301 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-063 | `DU` | sans | constructive function for du-chains, Var⋆ × Lab⋆ → P(Lab⋆) (p. 54) | 54 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-064 | `du` | italic | du-chains: labels where the value assigned to x at ℓ might be used (p. 53) | 53 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-065 | `E` | italic | finite set of extremal labels of an analysis instance (p. 69) | 69, 341 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-066 | `e_{1} → e_{2}` | italic | expression e1 evaluates to e2 in one step (p. 341) | 341 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-067 | `e` | italic | ranges over expressions (labelled terms) (p. 142) | 142, 283, 339 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-068 | `ee` | italic | ranges over extended expressions (p. 331) | 331 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-069 | `EExp` | bold | extended expressions (p. 331) | 331 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-070 | `empty` | sans | the empty worklist (p. 368) | 368 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-071 | `Env` | bold | environments, mapping variables in the current scope to their locations (p. 86) | 86, 153, 333 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-072 | `\widehat{Env}` | bold | abstract environments, Var → abstract values (p. 144) | 144, 187, 191 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-073 | `EVal` | bold | expressible values: pairs of a region name and an offset (p. 333) | 333 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-074 | `Exp` | bold | expressions (or labelled terms) (p. 142) | 142, 283, 339 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-075 | `Ext` | italic | set of elements upon which f is extensive, f(l) ⊒ l (p. 223) | 223, 402 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-076 | `extract` | sans | returns a constraint from the worklist and the smaller remaining worklist (p. 368) | 368 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-077 | `ℱ` | calligraphic | set of monotone functions over L containing transfer functions and identity, closed under composition (p. 68) | 68 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-078 | `\widehat{ℱ}` | calligraphic | the monotone transfer functions of the embellished Monotone Framework (p. 91) | 91 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-079 | `ℱ_{CP}` | calligraphic | Constant Propagation transfer functions: all monotone functions on State_CP (p. 73) | 73 | [PPA Index of Notation, p. 430] (book p. 430; PDF p. 444) |
| N3-080 | `[f]_{Δ}^{n}` | italic | n-th element of the narrowing sequence, starting from f_∇ (p. 230) | 230 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-081 | `\widehat{f_{ℓ_c}^{1}}` | italic | transfer function for the actual call, passing properties and context to procedure entry (p. 93) | 93, 96, 98, 100, 101 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-082 | `\widehat{f_{ℓ_c,ℓ_r}^{2}}` | italic | transfer function for the return, passing properties back from procedure exit (p. 93) | 93, 96, 98, 100, 101 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-083 | `\widehat{f_{ℓ}}` | italic | transfer function applying the original f_ℓ pointwise for each context (p. 91) | 91 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-084 | `\widehat{f_{ℓ_n}}` | italic | transfer function for procedure entry of a procedure definition, taken to be identity (p. 92) | 92 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-085 | `\widehat{f_{ℓ_x}}` | italic | transfer function for procedure exit of a procedure definition, taken to be identity (p. 92) | 92 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-086 | `f_{∇}^{n}` | italic | n-th element of the sequence computed from f using the widening operator ∇ (p. 226) | 226 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-087 | `f_{ℓ}^{SA}` | italic | Shape Analysis transfer function P(SG) → P(SG) associated with label ℓ (p. 116) | 115, 116 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-088 | `f_{·}` | italic | mapping from binary operators op to functions of ℱ (p. 186) | 186 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-089 | `f_{ℓ}` | italic | transfer function L → L for label ℓ (p. 68) | 68 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-090 | `f_{p}` | italic | function given by the deterministic analysis: f_p(l1) = l2 means p ⊢ l1 ▷ l2 (p. 212) | 212, 219 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-091 | `f_{ℓ}^{CP}` | italic | Constant Propagation mapping of labels to transfer functions (p. 73) | 73 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-092 | `final_{⋆}` | italic | final labels of the entire program, final(S⋆) (p. 84) | 84 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-093 | `final` | italic | function returning the set of final labels of a statement (p. 36) | 36, 83 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-094 | `Fix` | italic | the set of fixed points of f (p. 223) | 223, 402 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-095 | `flow_{⋆}` | italic | flows of the entire program P⋆, including procedure bodies (p. 84) | 84 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-096 | `flow` | italic | function mapping statements to sets of flows (edges between labels) (p. 37) | 37, 83 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-097 | `flow^{R}` | italic | function computing the reverse flows of a statement (p. 38) | 38 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-098 | `FV` | italic | free variables of expressions and terms (p. 143) | 143, 367 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-099 | `gen_{AE}` | italic | set of non-trivial expressions generated (evaluated, operands not later modified) by a block (p. 40) | 40 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-100 | `gen_{LV}` | italic | set of variables that appear in the block (p. 50) | 50 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-101 | `gen_{RD}` | italic | set of variable–label pairs of assignments generated by the block (p. 43) | 43 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-102 | `gen_{VB}` | italic | how a block generates additional very busy expressions (p. 46) | 46 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-103 | `gfp` | italic | the greatest fixed point of f, the least upper bound of Fix(f) (p. 223) | 223, 402 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-104 | `H` | sans | abstract heap, specifying links between abstract locations (p. 111) | 111, 114 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-105 | `ℋ` | calligraphic | heap, mapping location and selector to integer, location or nil (p. 106) | 106 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-106 | `Heap` | bold | heaps: (Loc × Sel) →fin (Z + Loc + {⋄}) (p. 106) | 106 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-107 | `IAV` | italic | set of global variables possibly assigned directly or indirectly when p is called (p. 101) | 101 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-108 | `id` | italic | the identity function (p. 68) | 68, 302 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-109 | `ie` | italic | ranges over intermediate expressions (p. 154) | 154 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-110 | `IExp` | bold | intermediate expressions (p. 154) | 154 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-111 | `inf` | sans | infimum (lower end point) of an interval (p. 222) | 222 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-112 | `infl` | sans | array recording the constraints influenced by a given flow variable (p. 369) | 369 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-113 | `init_{⋆}` | italic | initial label of the entire program, init(S⋆) (p. 84) | 84 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-114 | `init` | italic | function returning the initial label of a statement (p. 36) | 36, 83 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-115 | `insert` | sans | returns a worklist as W but with a new constraint added (p. 368) | 368 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-116 | `inter-flow_{⋆}` | italic | interprocedural flow relating labels of a procedure call to the procedure body (p. 84) | 84 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-117 | `Interval` | bold | the complete lattice of intervals over Z (p. 221) | 221 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-118 | `is` | sans | subset of abstract locations that are shared due to pointers in the heap (p. 112) | 112, 114 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-119 | `IsShared` | bold | sets of shared abstract locations, P(ALoc) (p. 114) | 114 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-120 | `it` | italic | ranges over intermediate terms (p. 154) | 154 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-121 | `ITerm` | bold | intermediate terms (p. 154) | 154 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-122 | `JUDG_{CFA}[Γ ⊢_{UL} e : τ]` | sans | set of CFA typings whose underlying typing is Γ ⊢_UL e : τ (p. 299) | 299 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-123 | `kill_{AE}` | italic | set of non-trivial expressions killed in the block (p. 40) | 40 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-124 | `kill_{LV}` | italic | variables killed by a block: the left hand side variable of an assignment (p. 49) | 49 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-125 | `kill_{RD}` | italic | set of variable–label pairs of assignments destroyed by the block (p. 43) | 43 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-126 | `kill_{VB}` | italic | function giving the expressions killed by a block, for Very Busy Expressions Analysis (p. 46) | 46 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-127 | `kill_{x}` | italic | removes the binding to x and renames abstract locations so they exclude x (p. 117) | 117 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-128 | `kill_{x.sel}` | italic | removes the triple (n_x, sel, n_u) from the abstract heap H (p. 125) | 125 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-129 | `\widehat{L}` | italic | property space of the embellished Monotone Framework, L̂ = Δ → L (p. 91) | 91 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-130 | `ℓ` | italic | labels (p. 3) | 3, 142 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-131 | `l_{n}^{ϕ}` | italic | new sequence built from (l_n) using ϕ: l_0, then l^ϕ_{n-1} ϕ l_n (p. 225) | 225 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-132 | `Lab_{⋆}` | bold | the labels appearing in the program of interest S⋆ (p. 38) | 38, 171 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-133 | `Lab` | bold | labels (p. 3) | 3, 142 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-134 | `labels_{⋆}` | italic | set of labels of the entire program P⋆, including procedure declarations (p. 84) | 84 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-135 | `labels` | italic | the set of labels occurring in a program, labels : Stmt → P(Lab) (p. 37) | 37, 83 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-136 | `lfp_{∇}^{Δ}` | italic | approximation of lfp(f) where the narrowing sequence stabilises (p. 230) | 230 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-137 | `lfp_{∇}` | italic | safe approximation of lfp(f) given by the stabilised widening sequence (p. 227) | 227 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-138 | `lfp` | italic | least fixed point of f, the greatest lower bound of Fix(f) (p. 223) | 223, 402 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-139 | `Loc` | bold | locations (or addresses) (p. 86) | 86, 105, 320 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-140 | `LV^{=}` | sans | equation system for Live Variables Analysis of a program S⋆ (p. 60) | 60 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-141 | `LV^{⊆}` | sans | constraint system obtained by modifying the equation system LV= (p. 60) | 60 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-142 | `LV_{entry}` | sans | Live Variables function mapping labels to sets of variables, at block entry (p. 50) | 50 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-143 | `LV_{exit}` | sans | Live Variables function mapping labels to sets of variables live at block exit (p. 50) | 50 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-144 | `MFP` | italic | least solution to the data flow equations (Maximal Fixed Point), computed iteratively (p. 74) | 74 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-145 | `MOP` | italic | solution combining the transfer functions of all paths up to a label (p. 79) | 79 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-146 | `MVP` | italic | solution combining the transfer functions of all valid paths up to a label (p. 90) | 90 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-147 | `𝒩` | calligraphic | semantic function Num → Z defining the semantics of numerals (p. 55) | 55 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-148 | `n_{X}` | italic | abstract location representing the location σ(x) for each x in X (p. 110) | 110 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-149 | `n_{∅}` | italic | abstract summary location, for locations not reachable directly from the state (p. 110) | 110 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-150 | `n` | italic | numerals (p. 3) | 3 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-151 | `Num` | bold | numerals (p. 3) | 3 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-152 | `o` | italic | offset, an index into a region's list of storable values (p. 333) | 333 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-153 | `Observe` | italic | auxiliary function reducing an effect to what is visible from outside (p. 338) | 338 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-154 | `Offset` | bold | offsets, indices of storable values within a region (Offset = N) (p. 333) | 333 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-155 | `Op` | bold | binary operators (p. 142) | 142, 284 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-156 | `\widehat{op}` | sans | total function telling how op operates on abstract properties (p. 182) | 182 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-157 | `op` | italic | binary operator (p. 142) | 142, 284 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-158 | `op_{a}` | bold | semantic counterpart of the arithmetic operator syntax (p. 55) | 55, 73 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-159 | `op_{a}` | italic | arithmetic operators (p. 4) | 4 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-160 | `op_{b}` | bold | semantic counterpart of the boolean operator syntax (p. 55) | 55 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-161 | `op_{b}` | italic | boolean operators (p. 4) | 4 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-162 | `op_{r}` | bold | semantic counterpart of the relational operator syntax (p. 55) | 55 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-163 | `op_{r}` | italic | relational operators (p. 4) | 4 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-164 | `P_{⋆}` | italic | program of the extended WHILE-language, of the form begin D⋆ S⋆ end (p. 82) | 82 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-165 | `℘` | script | function determining the value of a pointer expression given a state and heap (p. 107) | 107 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-166 | `p ⊢ l_{1} ▷ l_{2}` | italic | the analysis of program p transforms property l1 into property l2 (p. 212) | 212, 219 | [PPA Index of Notation, p. 431] (book p. 431; PDF p. 445) |
| N3-167 | `p ⊢ v_{1} ⇝ v_{2}` | italic | the semantics of program p transforms value v1 into value v2 (p. 211) | 211, 219 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-168 | `Parity` | bold | the set of parities {odd, even} (p. 244) | 244 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-169 | `path` | italic | sets of paths (label sequences) up to, excluding or including, a label (p. 79) | 79 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-170 | `Pnt` | bold | program points, used to name function abstractions (p. 284) | 284 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-171 | `PP` | italic | finite pool of processes, mapping processes to expressions (p. 342) | 342 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-172 | `Proc` | bold | processes (p. 342) | 342 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-173 | `R ↠ R` | italic | notation for the implication that R is preserved under computation (logical relation) (p. 214) | 214 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-174 | `R_{1} ↠ R_{2}` | italic | relation: inputs related by R1 are mapped to results related by R2 (p. 219) | 219 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-175 | `R_{β}` | italic | correctness relation defined from β: v R_β l iff β(v) ⊑ l (p. 217) | 217 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-176 | `R` | italic | correctness relation V × L → {true, false}; v R l: v described by l (p. 214) | 214 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-177 | `ℛ` | calligraphic | correctness relation between local environments and the abstract environment (p. 158) | 158 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-178 | `\vec{r}` | italic | possibly empty sequence of regions (p. 332) | 332 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-179 | `r` | italic | regions (p. 331) | 331, 343 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-180 | `ran` | italic | range of an environment, ran(ρ) = {ρ(x) : x ∈ Var⋆} (p. 86) | 86 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-181 | `Range` | bold | the set {<-1, -1, 0, +1, >+1} of integer ranges (p. 248) | 248 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-182 | `RD ⊢ S ▷ S′` | sans | transforms sub-statement S into a better statement S′ using RD (p. 27) | 27 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-183 | `RD` | sans | pair (RD_entry, RD_exit) of functions giving reaching definitions information (p. 5) | 5 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-184 | `RD_{entry}` | sans | function mapping labels to sets of (variable, label) pairs reaching block entry (p. 43) | 43 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-185 | `RD_{exit}` | sans | function mapping labels to sets of (variable, label) pairs reaching block exit (p. 43) | 43 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-186 | `Red` | italic | set of elements upon which f is reductive, {l : f(l) ⊑ l} (p. 223) | 223, 402 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-187 | `Reg_{CA}` | bold | regions (in Communication Analysis) (p. 343) | 343 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-188 | `Reg_{RI}` | bold | regions: a region variable or a region name (p. 331) | 331 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-189 | `rn` | italic | region names (p. 331) | 331 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-190 | `RName` | bold | region names (p. 331) | 331 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-191 | `rPostorder` | sans | array numbering each constraint in a reverse postorder traversal of the spanning forest (p. 375) | 375 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-192 | `RVar` | bold | region variables (p. 331) | 331 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-193 | `S : RD_{1} → RD_{2}` | italic | annotated base type judgement; RD1, RD2 are sets of reaching definitions (p. 18) | 18 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-194 | `S : Σ →_{RD}^{X} Σ` | italic | judgement for Reaching Definitions with an annotated type constructor (arrow) (p. 20) | 20 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-195 | `S : Σ → Σ` | italic | judgement that statement S maps a state to a state (p. 17) | 17 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-196 | `S_{⋆}` | italic | the program being analysed (the top-level statement) (p. 38) | 38 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-197 | `S` | italic | statements (p. 3) | 3 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-198 | `S` | sans | abstract state, mapping variables to abstract locations (p. 110) | 110, 114 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-199 | `𝒮` | calligraphic | finite constraint system of the form (x_i ⊒ t_i) for i = 1..N (p. 367) | 367 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-200 | `SAnn` | bold | simple annotations (p. 306) | 306 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-201 | `Scheme_{CA}` | bold | type schemes (in Communication Analysis) (p. 343) | 343 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-202 | `Scheme_{RI}` | bold | type schemes, compound or ordinary (in Region Inference) (p. 335) | 335 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-203 | `Sel` | bold | finite non-empty set of selector names (p. 104) | 104 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-204 | `sel` | italic | selector names (p. 104) | 104 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-205 | `SG` | bold | the set of compatible shape graphs (p. 114) | 114 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-206 | `Shape` | italic | Shape Analysis: sets of shape graphs before and after each block (p. 115) | 115 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-207 | `Sign` | bold | the set of signs {-, 0, +} (p. 238) | 238 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-208 | `SRD` | sans | semantically reaching definitions extracted from a trace (p. 13) | 13 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-209 | `State` | bold | states, mappings from variables to integers (p. 54) | 54, 105 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-210 | `\widehat{State}_{CP}` | bold | complete lattice for Constant Propagation Analysis, (Var⋆ → Z^⊤)_⊥ (p. 72) | 72 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-211 | `Stmt` | bold | statements (p. 3) | 3 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-212 | `Store` | bold | stores, Loc →fin Z, specifying the values of locations (p. 86) | 86, 320, 333 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-213 | `SType` | bold | simple types (p. 306) | 306 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-214 | `sup` | sans | supremum operation on intervals (p. 222) | 222 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-215 | `SVal` | bold | storable values: constants, closures and region polymorphic closures (p. 333) | 333 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-216 | `⟦t⟧ψ` | italic | interpretation of term t with respect to solution ψ (p. 367) | 367 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-217 | `t` | italic | terms (or unlabelled expressions) (p. 142) | 142, 367 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-218 | `TEnv` | bold | type environments (p. 285) | 285 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-219 | `\widehat{TEnv}` | bold | annotated type environments (p. 287) | 287 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-220 | `Term_{⋆}` | bold | finite set of subterms occurring in the program e⋆ (p. 171) | 171 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-221 | `Term` | bold | terms (or unlabelled expressions) (p. 142) | 142 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-222 | `tr` | italic | trace, recording where variables obtained their values (p. 13) | 13 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-223 | `Trace` | bold | traces, (Var × Lab)* (p. 13) | 13 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-224 | `TrVar_{⋆}^{?}` | bold | traces in which every variable of Var⋆ has a pair (x, ℓ) (p. 134) | 134 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-225 | `TVar` | bold | type variables (p. 300) | 300, 306 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-226 | `Type` | bold | types (p. 285) | 285 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-227 | `Type_{CA}` | bold | types (in Communication Analysis) (p. 343) | 343 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-228 | `Type_{ES}` | bold | annotated types for Exception Analysis (p. 327) | 327 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-229 | `Type_{RI}` | bold | annotated types (in Region Inference) (p. 335) | 335 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-230 | `Type_{SE}` | bold | annotated types for Side Effect Analysis (p. 321) | 321 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-231 | `\widehat{Type}[τ]` | bold | set of annotated types with underlying type τ (p. 298) | 298 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-232 | `\widehat{Type}` | bold | annotated types (p. 287) | 287 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-233 | `𝒰_{CFA}` | calligraphic | unification function for simple types, returning a simple substitution (p. 307) | 307 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-234 | `𝒰_{UL}` | calligraphic | unification procedure returning a substitution that makes two augmented types equal (p. 302) | 302, 305 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-235 | `UD` | sans | constructive definition of ud-chains using RD_entry (p. 54) | 54 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-236 | `ud` | italic | labels where an occurrence of x at ℓ′ might have obtained its value (p. 53) | 53 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-237 | `use` | italic | predicate checking whether the variable is used in a block (p. 52) | 52 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-238 | `𝒱` | calligraphic | auxiliary relation between values and abstract environment/abstract value pairs (p. 159) | 159 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-239 | `\widehat{v}` | italic | abstract values (p. 144) | 144, 182, 187, 191 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-240 | `v` | italic | values (p. 153) | 153, 293, 333, 341 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-241 | `Val` | bold | values (p. 153) | 153, 293, 341 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-242 | `\widehat{Val}_{d}` | bold | abstract values, P(Term ∪ Data) (p. 182) | 182 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-243 | `\widehat{Val}` | bold | abstract values, P(Term) (p. 144) | 144, 187, 191 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-244 | `Var_{⋆}` | bold | the variables appearing in the program of interest S⋆ (p. 38) | 38, 171 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-245 | `Var` | bold | variables (p. 3) | 3, 142, 284 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-246 | `VB_{entry}` | sans | function mapping labels to sets of expressions very busy at entry (p. 47) | 47 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-247 | `VB_{exit}` | sans | function mapping labels to sets of expressions very busy at exit (p. 47) | 47 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-248 | `vpath` | italic | sets of valid paths up to, excluding or including, a label (p. 90) | 90 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-249 | `𝒲_{CFA}` | calligraphic | inference algorithm for Control Flow Analysis, an analogue of W_UL (p. 309) | 309 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-250 | `W` | sans | worklist, a list of pairs from the flow relation F (p. 74) | 74 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-251 | `𝒲_{UL}` | calligraphic | type reconstruction algorithm, given an augmented type environment and expression (p. 301) | 301 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-252 | `w` | italic | storable value (p. 333) | 333 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |
| N3-253 | `(x_{i} ⊒ t_{i})_{i=1}^{N}` | italic | finite constraint system with N ≥ 1 constraints x_i ⊒ t_i (p. 367) | 367 | [PPA Index of Notation, p. 432] (book p. 432; PDF p. 446) |

## Collisions and Scope Notes

The same glyph carries different meanings in different chapters. Always read a symbol
together with its chapter, section or page.

| symbol | meanings and where | index rows |
| :--- | :--- | :--- |
| `ς` | store, giving the values of locations (pp. 86, 320, 333); reduction operator on a complete lattice: `ς[M]` is the lattice of all `ς(m)` (p. 244), `ς_{η}` is the reduction operator obtained from an extraction function (p. 246). One Greek entry holds both meanings. | N2-047, N2-048, N2-049 |
| `Δ` | set of context information `δ ∈ Δ` for interprocedural and context-sensitive analysis (pp. 91-191); narrowing operator (p. 230), also the subscript of `[f]_{Δ}^{n}` and the superscript of `lfp_{∇}^{Δ}`. One Greek entry holds both meanings. | N2-008, N3-080, N3-136 |
| `Λ` | behaviour for atomic actions that do not involve communication (p. 344, the only indexed page); the empty call string, as in `ι̂(δ) = ι` if `δ = Λ` (p. 96, not indexed under `Λ`); the empty string of regular expressions [PPA §C.3, p. 426] (not indexed). | N2-026, N2-025 |
| `Σ` | the type of states (p. 17, the only indexed page; also in `S : Σ → Σ`); an alphabet, a finite non-empty set of symbols [PPA §C.3, p. 426] (not indexed). | N2-043, N3-194, N3-195 |
| `α` | abstraction function (p. 15); type variable `α ∈ TVar` (pp. 300, 306). One entry. | N2-001 |
| `β` | representation function (p. 216); annotation variable `β ∈ AVar` (p. 306). One entry. | N2-003 |
| `θ` | substitution of augmented types for type variables (p. 301); isomorphism between partially ordered sets, with inverse `θ^{-1}` [PPA §A.1, p. 397] (not indexed). | N2-054 |
| `ℛ` | the correctness relation between local environments and the abstract environment (p. 158); in Example B.1 the monotone functional `ℛ(R_{1}′, R_{2}′)` on pairs of relations [PPA Example B.1, p. 413] is not indexed. | N3-177 |
| `H` | sans `H`, an abstract heap (pp. 111, 114); calligraphic `ℋ`, a concrete heap (p. 106); italic `H`, a handle, a set of nodes from which every node is reachable [PPA §C.1, p. 419] (not indexed). | N3-104, N3-105, U-21 |
| `∇` | widening operator `∇ : L × L → L` (p. 226); a `▽` printed over an arrow marks evaluation trees `d →^{▽} n` [PPA §B.1, p. 406] (not indexed). | N1-007, N3-086, N3-137 |
| `φ` / `ϕ` | curly `φ`: effects and annotations (pp. 24, 287, 306, ...); straight `ϕ`: the shape-analysis transfer function `ϕ_{ℓ}^{SA}` (p. 116) and the arbitrary total function `ϕ : L × L → L` used to build `l_{n}^{ϕ}` (p. 225; see BKL-024). Only the glyph variant tells them apart. | N2-028, N2-029, N3-131 |
| `→` | `■ → ■` is indexed only for one-step evaluation `e_{1} → e_{2}` (p. 341); the same arrow is the total and monotone function space [PPA §A.2, p. 398] and the transition arrow of `ρ ⊢_{⋆} … → …` (p. 86). | N1-002, N1-019, N1-020, N3-066 |
| `⊑` / `⊒` | indexed only for the orderings on annotations, annotated types and behaviours (pp. 298, 348) and for constraints `x_{i} ⊒ t_{i}` (p. 367); the general partial ordering is defined in [PPA §A.1, p. 393] (not indexed) and is instantiated in Chapter 2 Monotone Frameworks to `⊆` for may analyses (`RD`, `LV`) and `⊇` for must analyses (`AE`, `VB`) ([PPA Example 2.23, p. 67]; [PPA Figure 2.6, p. 70]). | N1-011, N1-012 |
| `CP` | two separate italic entries with the same glyph and typeface: the set of immediately called procedures of a statement (p. 102) and the finite set of channels generated so far (p. 342). Only the page tells them apart. | N3-047, N3-048 |
| `AV` | one entry with two unrelated meanings: the directly assigned variables of a statement (p. 101) and `AV(C)`, the annotation variables in a constraint set `C` (p. 317). | N3-024 |
| `E` | one entry with two unrelated meanings: the finite set of extremal labels of an analysis instance (p. 69) and evaluation contexts (p. 341). | N3-065 |
| `∅` | the empty set, as in `n_{∅}` (p. 110); also an atomic regular expression denoting the empty language [PPA §C.3, p. 426] (not indexed). | N3-149 |
| `?` | uninitialised reaching-definition label in `Var_{⋆} × (Lab_{⋆} ∪ {?})` [PPA §1.2, p. 5] (and `Lab_{⋆}^{?}`, U-35, [PPA §2.1.2, p. 43]) versus alphabet symbol in `{!, ?}` for regular-expression Reaching Definitions in Mini Project 1.1 [PPA Chapter 1 Mini Projects, p. 31] (not indexed standalone; see BKL-035). | N3-130, U-33, U-35 |
| `𝒮` | regular-expression translation `𝒮(S)` of a `WHILE` statement in Mini Project 1.1 [PPA Chapter 1 Mini Projects, p. 30] (not indexed there) versus constraint-system generator `𝒮` in Chapter 6 (p. 367). | N3-199, U-34 |
| `k` / `k_{x}` | italic `k` denotes bounded call-string depth ([PPA §2.5.4, p. 97]) and closure contour bound (p. 191), whereas `k_{x}` denotes the shape-node variable stripping map `ALoc → ALoc` ([PPA §2.6.3, p. 117]). | U-38 |
| `⊨` | `■ ⊨ ■` is indexed only for Chapter 5 substitution satisfaction `θ_{A} ⊨ C` (p. 309); Chapter 2 uses `live ⊨ LV^=` ([PPA Lemma 2.15, p. 60]) and Chapter 3 uses CFA acceptability/constraint satisfaction `⊨` ([PPA Table 3.1, p. 146]), `⊨_{s}`, `⊨'_{s}`, `⊨_{c}`, `⊨_{d}`, `⊨_{D}`, `⊨'_{D}`, `⊨_{δ}^{ce}`, `⊨_{CPA}^{δ}`, `⊨_{me}` (through [PPA Mini Project 3.4, p. 205]). | N1-006, N2-055, U-39 |
| `C` / `C(ℓ)` | italic `C` is a Chapter 5 annotation constraint set (p. 308); sans `\widehat{C}` is a semantic abstract cache (p. 144); unindexed sans `C(ℓ)` is a Chapter 3 syntactic cache constraint variable ([PPA §3.4, p. 173]); `C ∈ Constr` is a data constructor ([PPA Mini Project 3.2, p. 203]). | N3-035, N3-036, U-40 |
| `r` / `r(x)` | italic `r` ranges over regions (pp. 331, 343); unindexed sans `r(x)` is a Chapter 3 syntactic environment constraint variable ([PPA §3.4, p. 173]). | N3-179, U-40 |
| `ρ` | italic `ρ` is an environment mapping variables to locations or abstract values (pp. 86, 153, 333; `\widehat{ρ}`, p. 144) versus a Chapter 4 upper closure operator `ρ : L → L` (`ρ[L] = Fix(ρ)`, [PPA Chapter 4 Concluding Remarks, p. 270]; not indexed under closure operators). | N2-035, U-53 |

### Superscript of `l_{n}^{ϕ}` (book p. 225; PDF p. 242)

The page image shows the straight phi `ϕ` (TeX `\phi`), not the curly `φ` used for
annotations and effects. The book lets `(l_{n})_{n}` be a sequence in `L` and
`ϕ : L × L → L` a total function, and defines `l_{n}^{ϕ} = l_{n}` if `n = 0` and
`l_{n}^{ϕ} = l_{n−1}^{ϕ} ϕ l_{n}` if `n > 0` [PPA §4.2, p. 225]. Fact 4.11 on the same page
then uses an upper bound operator in place of `ϕ`.

### Typeface-only distinctions

These entries share their letters and differ only in typeface (or hat). A plain-text copy
that drops typeface merges them.

| letters | variants (index rows) |
| :--- | :--- |
| S | italic `S` (N3-197), sans `S` (N3-198), calligraphic `𝒮` (N3-199), italic `S_{⋆}` (N3-196) |
| Analysis | sans `Analysis` (N3-015), italic `Analysis` (N3-016), sans `Analysis^{=}` and `Analysis^{⊑}` (N3-013, N3-014) |
| op | bold `Op` (N3-155), sans `\widehat{op}` (N3-156), italic `op` (N3-157); bold and italic `op_{a}`, `op_{b}`, `op_{r}` (N3-158 to N3-163) |
| blocks | bold `Blocks_{⋆}` (N3-032), italic `blocks_{⋆}` (N3-033), italic `blocks` (N3-034) |
| ALoc | bold `ALoc` (N3-010), italic `ALoc(H)` and `ALoc(S)` (N3-011, N3-012) |
| H | sans `H` (N3-104), calligraphic `ℋ` (N3-105) |
| R | italic `R` (N3-176), calligraphic `ℛ` (N3-177) |
| C | italic `C` (N3-035), sans `\widehat{C}` (N3-036), calligraphic `𝒞_{⋆}` (N3-037), italic `c` (N3-038) |
| D | italic `D_{⋆}` (N3-051), sans `\widehat{D}` (N3-052), italic `\widehat{d}` (N3-053) |
| W | calligraphic `𝒲_{CFA}` and `𝒲_{UL}` (N3-249, N3-251), sans `W` (N3-250) |
| U, V | calligraphic `𝒰_{CFA}`, `𝒰_{UL}`, `𝒱` (N3-233, N3-234, N3-238) versus sans `UD` (N3-235) and italic `v` (N3-240) |
| DU / du, UD / ud, DOM / dom | sans `DU`, `UD`, `DOM` (N3-063, N3-235, N3-061) versus italic `du`, `ud`, `dom` (N3-064, N3-236, N3-062) |
| Type and hats | bold `Type` (N3-226) versus bold `\widehat{Type}` (N3-232); likewise `Env`/`\widehat{Env}`, `Val`/`\widehat{Val}`, `TEnv`/`\widehat{TEnv}`, `Data`/`\widehat{Data}` |
| P | italic `P_{⋆}` (N3-164), script `℘` (N3-165); the calligraphic powerset `𝒫` [PPA Example A.1, p. 394] is not indexed and is easily confused with `℘` |
| Q | indexed `Q_{i}` / `𝒬_{i}` [PPA §B.2, p. 409]; unindexed sans `Q` (predicate being defined), calligraphic `𝒬` (its functional) and italic `Q′` (candidate predicate) [PPA §B.3, p. 411], plus Chapter 3 abstract `0-CFA` functional `𝒬` ([PPA §3.1.2, p. 150]) and syntax-directed `𝒬_{s}` ([PPA Proposition 3.18, p. 172]); none is indexed |
| F | calligraphic `ℱ` transfer functions (`N3-077`–`N3-079`) and italic `f` (`N3-080`–`N3-091`) versus unindexed italic `F` (flow relation [PPA §2.1, p. 37]) and `F_{⋆}` (constraint-system functional [PPA §3.4.2, p. 176]) |
| R, S | italic `R` (`N3-176`), calligraphic `ℛ` (`N3-177`), and unindexed sans `\widehat{R}` reachability ([PPA Mini Project 3.1, p. 202]); sans `S` abstract heap state (`N3-198`) vs Chapter 3 flow-sensitive reference stores `\widehat{S}_{∘}, \widehat{S}_{•}` ([PPA Mini Project 3.4, p. 205]) |
| ρ / ϱ | italic `ρ` environments (N2-035) versus `ϱ` region variables (N2-041) |

## Unindexed Core Symbols in Book

Symbols that the book defines and uses but that have no entry in the Index of Notation.
Each row cites the page where the book defines the symbol; the meaning restates the book.

| id | symbol | typeface | meaning (as stated by the book) | defined at |
| :--- | :--- | :--- | :--- | :--- |
| U-01 | `⊏` | roman | `l_{1} ⊏ l_{2}` means `l_{1} ⊑ l_{2} ∧ l_{1} ≠ l_{2}` | [PPA §A.1, p. 393] |
| U-02 | `⨆Y`, `⨅Y` | roman | least upper bound and greatest lower bound of `Y`; `⨆` is called the join operator and `⨅` the meet operator | [PPA §A.1, p. 393] |
| U-03 | `l_{1} ⊔ l_{2}`, `l_{1} ⊓ l_{2}` | roman | `⨆{l_{1}, l_{2}}` and `⨅{l_{1}, l_{2}}` | [PPA §A.1, p. 393] |
| U-04 | `(L, ⊑, ⨆, ⨅, ⊥, ⊤)` | roman | complete lattice: a partially ordered set in which all subsets have least upper bounds and greatest lower bounds | [PPA §A.1, p. 393] |
| U-05 | `⊥`, `⊤` | roman | least element `⊥ = ⨆∅ = ⨅L` and greatest element `⊤ = ⨅∅ = ⨆L` | [PPA §A.1, p. 394] |
| U-06 | `𝒫(S)` | calligraphic | powerset of `S`; `(𝒫(S), ⊆)` and `(𝒫(S), ⊇)` are complete lattices | [PPA Example A.1, p. 394] |
| U-07 | `θ`, `θ^{-1}` | italic | isomorphism between partially ordered sets and its (unique, monotone) inverse | [PPA §A.1, p. 397] |
| U-08 | `L_{1} × L_{2}` | roman | cartesian product of `L_{1}` and `L_{2}`, ordered componentwise | [PPA §A.2, p. 397] |
| U-09 | `S → L_{1}`, `L_{1} → L_{2}` | roman | total function space from a set `S` to `L_{1}`; monotone function space from `L_{1}` to `L_{2}` | [PPA §A.2, p. 398] |
| U-10 | `(l_{n})_{n}` | italic | a sequence `(l_{n})_{n∈N}` of elements of `L`; an ascending chain if `n ≤ m ⇒ l_{n} ⊑ l_{m}` | [PPA §A.3, p. 399] |
| U-11 | `⨆_{n} l_{n}`, `⨅_{n} l_{n}` | roman | `⨆{l_{n} \| n ∈ N}` and `⨅{l_{n} \| n ∈ N}` | [PPA §A.3, p. 399] |
| U-12 | `f^{↑κ}` | italic | `f(⨆_{κ′<κ} f^{↑κ′})` for an ordinal `κ`; `f^{↑n} = f^{n+1}(⊥)` for natural `n` | [PPA §A.4, p. 404] |
| U-13 | `⪯`, `≺`, `≻` | roman | well-founded ordering on `D`; `d ≻ d′` means `d′ ⪯ d ∧ d ≠ d′` | [PPA §B.1, p. 407] |
| U-14 | `d →^{▽} n` | italic | evaluation tree for the Natural Semantics `d → n` | [PPA §B.1, p. 406] |
| U-15 | `Q`, `𝒬`, `Q′` | sans, calligraphic, italic | indexed `Q_{i} = 𝒬_{i}(Q_{i})` in §B.2 ([PPA §B.2, p. 409]); unindexed predicate `Q = lfp(𝒬)` (`(B.4)`), monotone functional `𝒬`, and candidate predicate `Q′` | [PPA §B.3, p. 411] |
| U-16 | `{0,1,2}^{∞}` | roman | the finite and infinite strings over `{0, 1, 2}` | [PPA Example B.2, p. 414] |
| U-17 | `G = (N, A)` | italic | directed graph with a finite set `N` of nodes and edges `A ⊆ N × N` | [PPA §C.1, p. 417] |
| U-18 | `[n_{0}, …, n_{m}]` | italic | a path written as the sequence of nodes visited; never empty, trivial path `[n_{0}]` | [PPA §C.1, p. 418] |
| U-19 | `paths_{•}(n, n′)` | italic | set of paths from `n` to `n′` | [PPA §C.1, p. 418] |
| U-20 | `𝒮𝒞` | calligraphic | `{(n, n′) \| n and n′ are strongly connected}`, an equivalence relation (Fact C.3) | [PPA §C.1, p. 418] |
| U-21 | `H` | italic | handle: a set of nodes such that every node is reachable from some `h ∈ H` | [PPA §C.1, p. 419] |
| U-22 | `path_{•}^{H}(n)` | italic | `⋃{paths_{•}(h, n) \| h ∈ H}`, the paths from `H` to `n` | [PPA §C.1, p. 420] |
| U-23 | `Dom(n)` | italic | set of dominators of `n`, the greatest solution of its equation | [PPA §C.1, p. 421] |
| U-24 | `T = (N, A_{T})` | sans | depth-first spanning forest (DFSF) produced by the DFSF algorithm | [PPA Table C.1, p. 421] |
| U-25 | `d(G, T)`, `d(G)` | italic | loop connectedness parameter of `G` with respect to the DFSF `T` | [PPA §C.2, p. 424] |
| U-26 | `A_{db}` | italic | set of dominator-back edges, removed in the definition of reducible graph | [PPA §C.2, p. 425] |
| U-27 | `Σ` | roman | alphabet: a finite and non-empty set of symbols | [PPA §C.3, p. 426] |
| U-28 | `Λ`, `∅`, `+`, `·`, `*` | roman | atomic regular expressions `Λ` and `∅`, and the operators of compound regular expressions | [PPA §C.3, p. 426] |
| U-29 | `Σ^{*}`, `L ⊆ Σ^{*}` | roman | strings over `Σ`; a language over `Σ` is a set of strings | [PPA §C.3, p. 427] |
| U-30 | `ℒ⟦R⟧` | calligraphic | the language defined by the regular expression `R` | [PPA §C.3, p. 427] |
| U-31 | `h : Σ_{1} → Σ_{2}^{*}` | italic | homomorphism, extended to words, languages and regular expressions | [PPA §C.3, p. 427] |
| U-32 | `⊔̆` | roman | upper bound operator on `L`: always returns an element larger than both arguments | [PPA §4.2, p. 225] |
| U-33 | `?` | roman | special uninitialised-variable label in Reaching Definitions (`(x, ?)` on [PPA §1.2, p. 5]) versus alphabet symbol in `{!, ?}` in Mini Project 1.1 ([PPA Chapter 1 Mini Projects, p. 31]; see BKL-035) | [PPA §1.2, p. 5] |
| U-34 | `𝒮(S)` | calligraphic | regular expression associated with `WHILE` statement `S` in Mini Project 1.1 (distinct from Chapter 6 constraint-system `𝒮`, N3-199) | [PPA Chapter 1 Mini Projects, p. 30] |
| U-35 | `Lab_{⋆}^{?}`, `Var_{⋆} × Lab_{⋆}^{?}` | bold | label set extended with uninitialised sentinel `?` (`Lab_{⋆}^{?} = Lab_{⋆} ∪ {?}`, [PPA §2.1.2, p. 43]), required by `ud`/`du`/`UD`/`DU` ([PPA §2.1.5, p. 53]; BKL-036) and instrumented `Trace` ([PPA Table 2.10, p. 133]; BKL-049) | [PPA §2.1.2, p. 43] |
| U-36 | `flow_{⋆}^{R}`, `inter-flow_{⋆}^{R}` | italic | reverse intraprocedural and interprocedural flows used for backward embellished frameworks ([PPA §2.5, p. 85]; BKL-041), distinct from intraprocedural `flow^{R}` (N3-097) | [PPA §2.5, p. 85] |
| U-38 | `k_{x}` | italic | variable-kill shape-node remapping `ALoc → ALoc` (`k_{x}(n_{Z}) = n_{Z \setminus \{x\}}`, [PPA §2.6.3, p. 117]) | [PPA §2.6.3, p. 117] |
| U-39 | `⊨_{s}`, `⊨'_{s}`, `⊨_{c}`, `⊨_{d}`, `⊨_{D}`, `⊨'_{D}`, `⊨_{δ}^{ce}`, `⊨_{CPA}^{δ}`, `⊨_{me}` | roman | subscripted/primed Chapter 3 CFA acceptability and constraint-satisfaction relations: syntax-directed `⊨_{s}` ([PPA Table 3.5, p. 170]) and reachability-gated `⊨'_{s}` ([PPA Mini Project 3.1, p. 202]), constraint satisfaction `⊨_{c}` ([PPA §3.4.1, p. 176]), coupled powerset `⊨_{d}` ([PPA Table 3.8, p. 184]), lattice `⊨_{D}` ([PPA Table 3.9, p. 188]) and staged `⊨'_{D}` ([PPA §3.5.2, p. 189]), uniform `k`-CFA `⊨_{δ}^{ce}` ([PPA Table 3.10, p. 192]), `CPA` `⊨_{CPA}^{δ}` ([PPA §3.6.2, p. 197]), and imperative-store `⊨_{me}` ([PPA Mini Project 3.4, p. 205]); bare `0-CFA` `⊨` ([PPA Table 3.1, p. 146]) shares glyph `⊨` with `N1-006` (see `Overloaded symbols`) | [PPA Table 3.5, p. 170] |
| U-40 | `C(ℓ)`, `r(x)` | sans | syntactic constraint variables for label `ℓ` and variable `x` in `𝒞_{⋆}⟦e_{⋆}⟧` (distinct from semantic caches `\widehat{C}(ℓ)`, `N3-036`, and environments `\widehat{ρ}(x)`, `N2-039`) | [PPA §3.4, p. 173] |
| U-41 | `\widehat{Val}_{⋆}`, `\widehat{Cache}_{⋆}`, `\widehat{Env}_{⋆}` | bold | finite subterm-restricted domains `𝒫(Term_{⋆})`, `Lab_{⋆} → \widehat{Val}_{⋆}`, and `Var_{⋆} → \widehat{Val}_{⋆}` bounded by `(\widehat{C}_{⋆}^{⊤}, \widehat{ρ}_{⋆}^{⊤})` | [PPA §3.3.2, p. 171] |
| U-42 | `𝒬_{s}` | calligraphic | monotone syntax-directed `0-CFA` acceptability functional (`⊨_{s} = gfp(𝒬_{s}) = lfp(𝒬_{s})`), paired with unindexed Chapter 3 `𝒬` (`⊨ = gfp(𝒬)`, [PPA §3.1.2, p. 150]) | [PPA Proposition 3.18, p. 172] |
| U-43 | `F_{⋆}` | italic | monotone fixed-point operator on `\widehat{Cache}_{⋆} × \widehat{Env}_{⋆}` whose least fixed point solves `𝒞_{⋆}⟦e_{⋆}⟧` | [PPA §3.4.2, p. 176] |
| U-44 | `\widehat{R}`, `Reach` | sans, bold | abstract reachability map `\widehat{R} ∈ Reach = Lab → 𝒫({on})` gating active bodies in `(Ĉ, ρ̂, R̂) ⊨'_{s} e` | [PPA Mini Project 3.1, p. 202] |
| U-45 | `\widehat{S}_{∘}`, `\widehat{S}_{•}` | sans | entry and exit abstract reference stores `Lab → (Pnt → \widehat{Val})` in flow-sensitive CFA (`(Ĉ, ρ̂, \widehat{S}_{∘}, \widehat{S}_{•}) ⊨_{me} e`) | [PPA Mini Project 3.4, p. 205] |
| U-46 | `∇_{K}`, `LB_{K}`, `UB_{K}` | roman, sans | threshold interval widening parameterised by finite constant set `K ⊆ Z` using nearest-bound helpers `LB_{K}` and `UB_{K}` | [PPA Example 4.15, p. 228] |
| U-47 | `Δ_{N}` | roman | threshold interval narrowing parameterised by non-negative integer `N ≥ 0` | [PPA Example 4.18, p. 232] |
| U-48 | `ϒ` | roman | descending chain truncator halting refinement inside `Red(f)` after finitely many steps | [PPA Exercise 4.11, p. 278] |
| U-49 | `Sign′` | bold | 7-element reduced sign lattice `{⊥, -, 0, +, -0, 0+, ⊤}` (obtained by omitting `{-, +}` from `𝒫(Sign)`) restoring complete multiplicativity of `γ_{IS′}` | [PPA Figure 4.10, p. 276] |
| U-50 | `⊗`, `AB`, `LR` | roman, bold | powerset relational tensor product (`𝒫(V_{1}) ⊗ 𝒫(V_{2})`, [PPA §4.4.1, p. 251]), 29-atom Array Bound reduced tensor `AB ⊆ Sign × Sign × Range` ([PPA Example 4.39, p. 257]), and list-pair relation domain `LR` ([PPA Mini Project 4.1, p. 274]) | [PPA Example 4.39, p. 257] |
| U-51 | `ȷ`, `SS`, `SH` | italic, sans | abstract extremal element in `(M, F, E, ȷ, g_{·})` (`γ(ȷ) = ι`, [PPA §4.5.2, p. 264]), concrete sets-of-states reference framework `SS` ([PPA §4.5.2, p. 265]), and `(State × Heap)` reference framework `SH` ([PPA Mini Project 4.2, pp. 274–275] (book p. 274; PDF p. 291) (book p. 275; PDF p. 292)) | [PPA §4.5.2, p. 264] |
| U-52 | `∇_{L}`, `Δ_{L}` | roman | concretisation-induced widening `γ(α(l_{1}) ∇_{M} α(l_{2}))` ([PPA Proposition 4.44, p. 268]) and failed narrowing formula `γ(α(l_{1}) Δ_{M} α(l_{2}))` ([PPA Exercise 4.24, p. 282]) | [PPA Proposition 4.44, p. 268] |
| U-53 | `ρ[L]`, `⊑^{d}`, `Ξ` | italic, roman | fixed-point lattice `ρ[L] = Fix(ρ)` of an upper closure operator `ρ : L → L` (bare `ρ` shares `N2-035`, see `Collisions and Scope Notes`; [PPA Chapter 4 Concluding Remarks, p. 270]); dual partial order `⊑^{d}` (`⊒`) and program-transformation enabling guard `l_{ℓ} ⊑ l_{Ξ}` ([PPA Chapter 4 Concluding Remarks, p. 273]) | [PPA Chapter 4 Concluding Remarks, p. 270] |

## Index Anomalies

1. `rPostorder` (N3-191) is indexed at p. 375 only. It is defined as the output of the DFSF
   algorithm [PPA Table C.1, p. 421] and used through [PPA §C.2, p. 426].
2. Only six index entries point into the appendices: `Ext`, `Fix`, `gfp`, `lfp`, `Red` (each
   `223, 402`) and `cycles` (`418`). The rest of the appendix notation is unindexed (see the
   addendum above), including the general `⊑`, `⊔`, `⊓`, `⊥` and `⊤`.
3. `■ ⊑ ■` (N1-011) is indexed at pp. 298 and 348, `■ ⊒ ■` (N1-012) at p. 367 and `■ → ■`
   (N1-002) at p. 341 only; none points to the general definitions in [PPA §A.1, p. 393] and
   [PPA §A.2, p. 398].
4. N1-009 is printed on p. 429 with heavy square brackets around and after the operand boxes;
   N3-216 `⟦t⟧ψ`, which carries the same page (367), is printed with semantic brackets on
   p. 432. Both are recorded here with semantic brackets.
5. One Greek entry `Δ` (N2-008) covers both context sets and the narrowing operator (p. 230);
   one entry `ς` (N2-047) covers both stores and the reduction operator (p. 244).
6. `CP` has two entries (N3-047, N3-048) with identical glyph and typeface.
7. `path` (N3-169, p. 79) is indexed, but `paths_{•}` and `path_{•}^{H}` from Appendix C are
   not; `Λ` and `Σ` are indexed only at pp. 344 and 17, not at their reuse in Appendix C.
8. Order: Part 2 is sorted by the Latin name of the letter (alpha, beta, delta, eta, gamma,
   iota, lambda, phi, pi, psi, rho, sigma, tau, theta, xi, zeta), so `Δ` follows `β`, `Γ`
   follows `η`, `ϕ_{ℓ}^{SA}` precedes `φ`, `ϱ` follows `ρ` and `ς` follows `σ`. Part 3
   ignores case, typeface, hats and stars (e.g. `Ann_{CA}` precedes `Ann`).
9. Pattern entries in Part 1 repeat the pages of their instances in Parts 2 and 3; all agree:
   `■ ↠ ■` (214, 219, 220) with `R ↠ R` (214), `R_{1} ↠ R_{2}` (219), `β_{1} ↠ β_{2}` (220);
   `■ ⊢ ■ ▷ ■` (27, 212, 219) with `RD ⊢ S ▷ S′` (27) and `p ⊢ l_{1} ▷ l_{2}` (212, 219);
   `■ : ■ → ■` (17, 18, 20) with the three `S : …` entries; `■ ⊢ ■ ⇝ ■` (211, 219) with
   `p ⊢ v_{1} ⇝ v_{2}`; `■ | ■` (154, 286) with `ρ | X` (154) and `Γ | X` (286);
   `■ ⊑ ■` (298, 348), `■ ⊆ ■` (298), `■ ⊇ ■` (308), `■ ≤ ■` (324, 329, 347), `■ ⊨ ■` (309),
   `■ ∼ ■` (62), `■ ⊒ ■` (367), `■ ⊢ ■ : ■` (22), `■ ⊢ ■ : ■ & ■` (24) and `■ ⊢_{⋆} ■ → ■`
   (86) with their Greek instances.
10. `λ` (N2-027) and `■ →_{fin} ■` (N1-003) point to the Preface (p. VIII), outside the
    chapters.
11. Text-layer damage on book p. 429 (PDF p. 443): the text layer reads `154, 286` as
    `154 2 6`, `298, 348` as `29 34`, `298` as `29`, `308` as `30`, `98, 193` as `9 193`,
    `186` as `1 6`, `96, 97, 99, 100` as `96 , 91, 99 100`, `17, 18, 20` as `17, 1 • 20`, and
    `\widehat{δ}, 187` as `617`. All page references in this file come from the page images (`BKL-011`).
12. `BExp(·)` (N3-029) is indexed at p. 39, where the text instead writes `AExp(b)` for the
    non-trivial arithmetic subexpressions of boolean expression `b` [PPA §2.1, p. 39].
