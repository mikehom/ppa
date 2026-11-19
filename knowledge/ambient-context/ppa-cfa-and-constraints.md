<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Standalone L0 ambient-context orientation for Chapter 3 (Constraint-Based Control Flow Analysis, Coupled CFA+DFA, and Polyvariant k-CFA/CPA). -->
<!-- @description: Orientation for control flow analysis of higher-order functional code: which lambda abstractions reach each application, abstract caches and environments, coinductive acceptability, syntax-directed and conditional subset constraints, the cubic graph worklist, coupled data values, and polyvariance via uniform k-CFA, call contexts and the Cartesian product algorithm. Use when closures, first-class functions or dynamic dispatch hide the call graph until analysis resolves it. -->

# Control Flow Analysis and Constraint-Based Systems — Orientation

Mental model, core vocabulary, fixed-point duality, and architectural boundaries for Chapter 3 of
*Principles of Program Analysis* ([PPA Chapter 3, p. 141] (book p. 141; PDF p. 159) through
[PPA Exercise 3.17, p. 209] (book p. 209; PDF p. 227)).

## 1. The Central Question and Vocabulary

Data flow analysis in Chapter 2 assumes a statically known control-flow graph (`flow`, `inter-flow_*`). The
moment functions, closures, callbacks, function pointers, or objects with virtual methods become first-class
values, control-flow edges depend on *data values* and data values depend on *control-flow edges* — the
**dynamic dispatch problem** [PPA §3.1, p. 141] (book p. 141; PDF p. 159).

Chapter 3 studies this circularity on the labelled functional language `FUN` (`e ::= t^ℓ`, where every
subexpression carries syntax pointer `ℓ ∈ Lab` while unlabelled terms `t ∈ Term` include `fn x => e₀` and
recursive `fun f x => e₀` [PPA §3.1, p. 142] (book p. 142; PDF p. 160)):

- **Abstract cache `Ĉ : Lab → Val̂` and environment `ρ̂ : Var → Val̂`**: In pure `0-CFA`, `Val̂ = 𝒫(Term)` tracks
  which function abstractions may reach each subexpression `ℓ` and variable `x`
  [PPA §3.1.1, p. 144] (book p. 144; PDF p. 162). At an application `(t₁^{ℓ₁} t₂^{ℓ₂})^ℓ`, `Ĉ(ℓ₁)` recovers
  the dynamic call targets (`Remark.`, p. 145) [PPA §3.1.1, p. 145] (book p. 145; PDF p. 163).
- **Safe over-approximation (`⊑` = pointwise `⊆`)**: Smaller sets are more precise (`⊥ = ∅` everywhere;
  `⊤ = Term` everywhere is trivially acceptable). Soundness (`Theorem 3.10`) guarantees that if `(Ĉ, ρ̂) ⊨ ie`
  holds initially, it continues to hold across every small-step closure transition `ρ ⊢ ie → ie'`
  (`Tables 3.2-3.4`, using explicit `close t in ρ` and `bind ρ in ie` so syntax labels stay intact)
  [PPA Theorem 3.10, p. 159] (book p. 159; PDF p. 177).

## 2. Specification vs Computation: The Refinement Spine (gfp vs lfp)

Chapter 3 separates *what makes an analysis answer safe* from *how to compute the most precise answer* along
a four-stage refinement spine ([PPA Chapter 3, p. 141] (book p. 141; PDF p. 159),
[PPA Preface, p. VII] (book p. VII; PDF p. 7)):

| Stage | Notation & Anchor | Fixed-Point / Proof Role | Operational Property |
| :--- | :--- | :--- | :--- |
| **1. Abstract specification** | `(Ĉ, ρ̂) ⊨ e` ([PPA Table 3.1, p. 146] (book p. 146; PDF p. 164)) | **Greatest fixed point** `⊨ = gfp(𝒬)` (`Unification U9`) | Coinduction accepts recursive cycles (`loop`, `Ω`); solutions form a **Moore family** (`Prop 3.13`), whereas `lfp(𝒬)` fails (`Prop 3.16`) |
| **2. Syntax-directed spec** | `(Ĉ, ρ̂) ⊨_s e` ([PPA Table 3.5, p. 170] (book p. 170; PDF p. 188)) | Unique fixed point `lfp(𝒬_s) = gfp(𝒬_s)` | Moves body checks from `[app]` to `[fn]`/`[fun]`; safe over-approx `⊨_s ⇒ ⊨` under `(Ĉ_⋆^⊤, ρ̂_⋆^⊤)` (`Prop 3.18`) |
| **3. Subset constraints** | `𝒞_⋆⟦e_⋆⟧` ([PPA Table 3.6, p. 174] (book p. 174; PDF p. 192)) | **Least fixed point** `lfp(F_⋆)` (`Prop 3.22`) | `O(n)` unconditional `lhs ⊆ rhs` + `O(n^2)` conditional `{t} ⊆ C(ℓ₁) ⇒ lhs ⊆ rhs`; exact match `⊨_s ⇔ ⊨_c` (`Prop 3.21`) |
| **4. Graph worklist solver** | `W, D[q], E[q]` ([PPA Table 3.7, p. 178] (book p. 178; PDF p. 196)) | `O(n^3)` edge-traversal solver (`Prop 3.24`) | Dual registration in `E[p₁]` and `E[p]` computes least constraint solution, sound for `⊨ e_⋆` (`Corollary 3.25`) |

## 3. Precision Dimensions: Coupled Data Flow and Polyvariant Context

Pure `0-CFA` is **flow-insensitive**, **branch-insensitive**, and **context-insensitive (monovariant)**:

- **Coupling Data Flow (`§3.5`, `Unification U4`)**: Tracking abstract data values alongside closures — either
  as finite powersets `Val̂_d = 𝒫(Term ∪ Data)` ([PPA Table 3.8, p. 184] (book p. 184; PDF p. 202)) or over an
  `ACC` complete-lattice monotone structure `(L, ℱ, ι., f.)` (`(Ĉ, D̂, ρ̂, δ̂) ⊨_D e`,
  [PPA Table 3.9, p. 188] (book p. 188; PDF p. 206)) — prunes dead conditional branches *online* before
  spurious closures enter `Ĉ`, beating two-phase staged `⊨'_D` (`Example 3.31`)
  [PPA Example 3.31, p. 189] (book p. 189; PDF p. 207).
- **Adding Context (`§3.6`, `Unification U5`)**: Monovariant `0-CFA` merges all calls to a polymorphic helper
  (`Example 3.32`). **Uniform `k`-CFA** ([PPA Table 3.10, p. 192] (book p. 192; PDF p. 210)) indexes caches
  (`Cachê = (Lab × Δ) → Val̂`) and environments by `k`-bounded call strings `Δ = Lab^{≤k}` while embedding
  lexical contexts `Val̂ = 𝒫(Term × CEnv)` (Shivers `[156, 157, 158]`, [PPA Chapter 3 Concluding Remarks, p. 198] (book p. 198; PDF p. 216); curried counterpart to
  `§2.5.4` call strings; still exponential `[external: DEXPTIME]` for `k ≥ 1`, whereas `Val̂ = 𝒫(Term × Δ)` gives
  polynomial height and is closely related to *polynomial `k`-CFA*, `O(n^6)` at `k = 1`, `BKL-007`), while **`CPA` (`[2]` `[external: Agesen]`)**
  ([PPA §3.6.2, p. 197] (book p. 197; PDF p. 215)) indexes contexts by concrete `m`-tuples of abstract
  arguments `Δ = Term^m` (counterpart to `§2.5.5` small assumption sets, related to OO receiver sensitivity `[external]`).

## 4. Relation to Other Approaches in the Book

- **Data Flow Analysis (Chapter 2, `U4` & `U5`)**: `§3.5.2` embeds `§2.3` Monotone Frameworks without a static
  `flow` graph; `§3.6.1` and `§3.6.2` lift `§2.5.4` call strings and `§2.5.5` small assumption sets to closures
  [PPA Preface, p. VII] (book p. VII; PDF p. 7).
- **Abstract Interpretation (Chapter 4)**: When `L` in `Table 3.9` lacks `ACC` (e.g. `Interval`), Chapter 4
  widening `∇` replaces raw ascending-chain iteration (`(F_⋆^m(⊥))_m`).
- **Type and Effect Systems (Chapter 5, `U8`)**: `§5.1` reformulates `0-CFA` via annotated arrow types with
  subeffecting/subtyping (`⊆` becomes subtyping) [PPA Preface, p. VII] (book p. VII; PDF p. 7).
- **Algorithms (Chapter 6, `U3`)**: `§6.1` generalises `Table 3.7` into an abstract worklist solver over
  monotone inequations [PPA Preface, p. VII] (book p. VII; PDF p. 7).

## 5. Key Boundaries and Pitfalls

- **Coinductive `gfp` vs solver `lfp`**: Acceptability `⊨ = gfp(𝒬)` must be coinductive so cyclic self-calls
  (`loop`, `Ω`) admit a non-empty Moore family (`Propositions 3.13, 3.16`); only after lowering to `𝒞_⋆⟦e_⋆⟧`
  does solving become a least fixed point `lfp(F_⋆)` (`Proposition 3.22`)
  [PPA §3.1.2, p. 152] (book p. 152; PDF p. 170).
- **Dead closures vs demand reachability**: `Tables 3.5-3.7` analyse unreachable syntactic lambdas (`Corollary 3.25`
  proves soundness `⊨ e_⋆`, not minimality on dead code) unless gated by reachability `R̂` (`Mini Project 3.1`) or
  `[9]` (`[external: Aiken et al.]`) lazy constraint expansion (`p. 202`) [PPA Corollary 3.25, p. 182] (book p. 182; PDF p. 200).
- **Dual-observer worklist invariant**: Conditional `{t} ⊆ p ⇒ p₁ ⊆ p₂` *must* subscribe to both `E[p₁]` and `E[p]`
  (`Table 3.7` Step 2), and differential `(q, t)` / bitset updates are needed so `O(n^3)` edge traversals do not
  degrade to `O(n^4)` set scans [PPA Table 3.7, p. 178] (book p. 178; PDF p. 196).
- **Lexical contours & non-empty `CPA` tuples**: Uniform `k`-CFA `[var]` looks up `ρ̂(x, ce(x))` at `x`'s lexical
  birth contour (never current `δ`), and `CPA` requires base-type tokens so non-function arguments do not collapse
  `Ĉ(ℓ₁, δ) × ··· × Ĉ(ℓ_m, δ)` to `∅` (`BKL-057`, `BKL-058`).
- **Open-world hazard (`BKL-008`)**: Reflection, FFI, and deserialization `[external]` require explicit open-system stubs (`p. 182`).

## 6. Where to Go Next

- Step-by-step implementation, solver, and context-selection procedures (`L2`):
  `skills/ppa-control-flow-and-constraints/SKILL.md`
- Formal rules, side conditions, and `U4`/`U5`/`U9` tables (`L1`):
  `skills/ppa-control-flow-and-constraints/references/cfa-core-and-coinduction.md`,
  `skills/ppa-control-flow-and-constraints/references/constraint-generation-and-cubic-solver.md`, and
  `skills/ppa-control-flow-and-constraints/references/polyvariant-kcfa-cpa-and-dfa.md`
- Concept graph (`L3`): query `ppa.cfa.*` in `ontology/concept_graph.json`.
