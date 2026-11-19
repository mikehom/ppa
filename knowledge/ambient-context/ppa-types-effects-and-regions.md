<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Standalone L0 ambient context for Chapter 5 Type and Effect Systems, Region Inference, and Behaviours. -->

# Type and Effect Systems, Region Inference, and Concurrent Behaviours

> Ambient orientation for Chapter 5 of *Principles of Program Analysis* (F. Nielson, H. R. Nielson,
> C. Hankin; corrected second printing, 2005). Grounded in [PPA Chapter 5, p. 283] (book p. 283; PDF p. 300)
> through [PPA Exercise 5.15, p. 363] (book p. 363; PDF p. 380).

## What Chapter 5 Is About

Whereas Data Flow Analysis, Constraint-Based Analysis, and Abstract Interpretation apply to untyped languages,
**Type and Effect Systems** demand an underlying statically typed program (`Γ ⊢_UL e : τ`, `Table 5.1`) so that
type structure itself serves as the carrier for program-analysis facts
[PPA Chapter 5, p. 283] (book p. 283; PDF p. 300) [PPA Table 5.1, p. 285] (book p. 285; PDF p. 302).

Chapter 5 progresses across six concrete deductive systems (`Tables 5.1–5.18`):

| System | Judgement & Tables | Annotation / Effect Carrier | Polymorphism & Subtyping |
| :--- | :--- | :--- | :--- |
| **Underlying `FUN`** | `Γ ⊢_UL e : τ` (`Tables 5.1, 5.5, 5.6`) | Unannotated `int, bool, τ₁ → τ₂` | Monomorphic `let` [PPA Table 5.1, p. 285] (book p. 285; PDF p. 302) |
| **Annotated CFA** | `Γ̂ ⊢_CFA e : τ̂` (`Tables 5.2–5.4, 5.7, 5.8`) | Arrow sets `φ ∈ Ann` (`{π}`) mod `UCAI` | Built-in `{π} ∪ φ` subeffecting [PPA Table 5.2, p. 288] (book p. 288; PDF p. 305) |
| **Side Effects** | `Γ̂ ⊢_SE e : τ̂ & φ` (`Table 5.9`) | `{!π, π:=, new π}` + `ref_ϖ τ̂` | Shape-conformant `≤` (`ref_ϖ` invariant) [PPA Table 5.9, p. 322] (book p. 322; PDF p. 339) |
| **Exceptions** | `Γ̂ ⊢_ES e : σ̂ & φ` (`Table 5.10`) | Uncaught `{s}` with `φ \ {s}` (`β\{s}=β`) | `≤` + `let`-schemes `∀ζ⃗. τ̂` [PPA Table 5.10, p. 328] (book p. 328; PDF p. 345) |
| **Region Inference** | `Γ̂ ⊢_RI e ↝ ee : (τ̂@r) & φ` (`Tables 5.11–5.13`) | `{put r, get r}`, `Observe`, `letregion` | Compound `∀β⃗,[ϱ⃗]` recursive schemes [PPA Table 5.12, p. 337] (book p. 337; PDF p. 354) |
| **Communication** | `Γ̂ ⊢_CA e : σ̂ & φ` (`Tables 5.14–5.18`) | Causal `Λ, ;, +, rec β.φ, spawn, r!τ̂, r?τ̂` | `≤`, `⊑`, `∀ζ⃗. τ̂` (`ζ_i ∉ FV(Γ̂,φ)`) [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365) |

Notice the conceptual divide (`Remark.`, p. 325): `§5.1` is an **Annotated Type System** (annotations describe
*intensional properties of values*), `§5.4` is an **Effect System** (`& φ` records *unordered computational steps*,
parked on latent arrows `τ̂₁ →^φ τ̂₂` until application), and `§5.5` upgrades effects to **Behaviours** (*temporal
causality* over Concurrent ML processes and channels) [PPA §5.4.1, p. 325] (book p. 325; PDF p. 342)
[PPA §5.5, p. 339] (book p. 339; PDF p. 356).

## Reconstruction, Variance, and the Five Design Axes

### Free-Algebra Reconstruction (SType, W_CFA, and theta_A)

Because set equality `UCAI` (`Table 5.3`) makes `Typê` a non-free algebra without unitary syntactic MGUs,
Section 5.3 restricts arrow slots inside **simple types** `SType` (`τ̂₁ --β--> τ̂₂`) to single annotation variables
`β ∈ AVar` (Robinson unification `𝒰_CFA`, `Table 5.7`, `Fact 5.17`) while collecting atomic
inclusions `β ⊇ {π}` in `C` (`𝒲_CFA`, `Table 5.8`), solved in `O(|C|)` via closed-form `θ_A` (defaulting
unconstrained `AVar`s outside `AV(C)` to `∅`) [PPA §5.3.2, p. 306] (book p. 306; PDF p. 323)
[PPA Corollary 5.23, p. 318] (book p. 318; PDF p. 335).

### Precision Fibre Order vs Behavioral Subtyping

Chapter 5 separates two orderings on `Typê[τ]` that must never be conflated:
- **Covariant precision order `⊑` (`§5.2.3`)**: Covariant in *both* domain and codomain so valid `⊢_CFA`
  judgements over `Γ ⊢_UL e : τ` form a **Moore family** (`Proposition 5.12`)
  [PPA §5.2.3, p. 298] (book p. 298; PDF p. 315) [PPA Proposition 5.12, p. 299] (book p. 299; PDF p. 316).
- **Shape-conformant subtyping `≤` (`§5.4.1`, `Table 5.18`)**: **Contravariant** in arrow domains (`τ̂'₁ ≤ τ̂₁`) and
  channel receives (`r?τ̂`), **covariant** in codomains, effects, point sets, and channel sends (`r!τ̂`), and
  **strictly invariant** in mutable payloads (`ref_ϖ τ̂` and `τ̂ chan r`, preventing `[external: CWE-843]` type
  confusion). Equipping `§5.1` with contravariant `≤` breaks `Proposition 5.12` (`Exercise 5.9`) while recovering
  exact directional parity with Chapter 3 `0-CFA` on well-typed `FUN` (`U8`, `Exercise* 5.4`)
  [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341) [PPA Chapter 5 Concluding Remarks, p. 350] (book p. 350; PDF p. 367).

### Restricted vs General Effects and Lexical Region Masking

- **Five design axes (`p. 351`)**: Subeffecting, subtyping, `let`-polymorphism (`∀ζ⃗. τ̂`), effect/region
  polymorphic recursion (`∀β⃗, [ϱ⃗]` in `[fun]`, excluding `α⃗` for decidability), and explicit vs `β.φ`-embedded
  constraints. When effects carry **no types** (*restricted effects*, `§§5.1, 5.4`), inference splits cleanly into
  Stage 1 (Hindley/Milner types) + Stage 2 (constraint solving); when effects embed types (*general
  effects*, `§5.5`), `[gen]` must forbid the **downwards closure** of `FV(Γ̂) ∪ FV(φ)` (`Example 5.36`, `BKL-009`)
  [PPA Chapter 5 Concluding Remarks, p. 351] (book p. 351; PDF p. 368)
  [PPA Chapter 5 Concluding Remarks, p. 352] (book p. 352; PDF p. 369).
- **Regions vs Heap Shapes**: Section 5.4.3 boxes values into a stack of dynamic regions (`Figure 5.1`) and pops
  non-escaping regions at `letregion` exit via `Observe(Γ̂, τ̂, r)(φ)` (`O(1)` lexical deallocation without GC,
  contrasting with Chapter 2 `§2.6`'s flow-sensitive mutable shape graphs `SG = (S, H, is)`)
  [PPA Figure 5.1, p. 331] (book p. 331; PDF p. 348) [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355).

## Core Chapter 5 Invariants and Soundness Traps

1. **Whole-tree `Ĉ(ℓ)` & big-step divergence vacuity**: Recovering subexpression flows requires the full `⊢_CFA`
   derivation tree (`Example 5.4`); `Table 5.4` big-step Subject Reduction (`Theorem 5.9`) is vacuous on
   non-terminating loops (`(5.1)`, `BKL-004`), though `--∅-->` certifies divergence (`Example 5.5`)
   [PPA Example 5.4, p. 289] (book p. 289; PDF p. 306) [PPA Theorem 5.9, p. 295] (book p. 295; PDF p. 312).
2. **Polymorphic masking & generalisation guards (`BKL-009`)**: Exception masking MUST keep `β \ {s} = β` on
   effect variables (`p. 329`; `Exercise 5.14` requires `AV(φ₂) = ∅`), and `[gen]` MUST check `ζ_i ∉ FV(Γ̂) ∪ FV(φ)`
   (`Example 5.36`) [PPA §5.4.2, p. 329] (book p. 329; PDF p. 346)
   [PPA Example 5.36, p. 346] (book p. 346; PDF p. 363).
3. **Printed errata & `[external: branching-time deadlocks]`**: `Table 5.5` `if` omits `∘ θ₀`, `θ_A` omits defaulting outside `AV(C)`,
   `Table 5.11` `[region]` prints `dom(ς)` for `dom(ς₁)`, `p. 350` mis-citing `Section 5.1` for `Section 5.4`, and
   `Table 5.18` distributes `;` over `+` **from the right only** to preserve synchronous `[external: deadlocks]`
   [PPA Table 5.5, p. 303] (book p. 303; PDF p. 320) [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365).
4. **Domain-specific qualifier & unit algebras (`Mini Projects 5.4–5.5`)**: Monotone lattices (`S ⊑ D` binding-time
   and `C₁ ⊑ ··· ⊑ C_k` clearance) require `ACC`, whereas physical units and timestamps (`num^{scale BASE base}`)
   replace idempotent `UCAI` sets with **`[external: abelian-group]`** `scale` laws and **`[external: affine-torsor]`** `base` arithmetic
   [PPA Mini Project 5.4, p. 356] (book p. 356; PDF p. 373) [PPA Mini Project 5.5, p. 358] (book p. 358; PDF p. 375).

## Key Vocabulary

| Term | Meaning in Chapter 5 |
| :--- | :--- |
| Underlying type `⌊τ̂⌋` | Base/arrow skeleton (`Table 5.1`) obtained by erasing all annotations [PPA §5.1.2, p. 287] (book p. 287; PDF p. 304) |
| `UCAI` | Unit, commutativity, associativity, and idempotence set axioms (`Table 5.3`) [PPA Table 5.3, p. 290] (book p. 290; PDF p. 307) |
| Subeffecting | Enlarging annotations/effects (`{π} ∪ φ` or `φ ⊆ φ'`) required for `Fact 5.6(ii)` [PPA Fact 5.6, p. 291] (book p. 291; PDF p. 308) |
| Simple type `SType` | Free-algebra type `τ̂₁ --β--> τ̂₂` with single `AVar`s on arrows (`§5.3.2`) [PPA §5.3.2, p. 306] (book p. 306; PDF p. 323) |
| Ground validation `θ_G` | Covering `θ_A ∘ θ_T` with `θ_A ⊨ C` yielding valid `⊢_CFA` derivations [PPA §5.3.2, p. 309] (book p. 309; PDF p. 326) |
| Shape-conformant `≤` | Polarised subtyping preserving underlying shape `⌊τ̂₁⌋ = ⌊τ̂₂⌋` [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341) |
| Compound scheme `∀β⃗,[ϱ⃗]` | Effect/region-polymorphic recursive scheme instantiated via `[place]` / `[ins₂]` [PPA §5.4.3, p. 335] (book p. 335; PDF p. 352) |
| `Observe(Γ̂, τ̂, r)(φ)` | Lexical filter hiding local `{put ϱ, get ϱ}` effects absent from `(Γ̂, τ̂, r)` [PPA §5.4.3, p. 338] (book p. 338; PDF p. 355) |
| Behaviour `φ ∈ Ann_CA` | Causal term (`Λ, ;, +, rec β.φ, spawn, r!τ̂, r?τ̂`) ordered by `Table 5.18` [PPA §5.5.1, p. 344] (book p. 344; PDF p. 361) |

## Out of Scope Here (Adjacent Skills)

Chapter 5 stops at statically typed syntax-directed inference: untyped higher-order closures (`fn x => x x`) and
`k`-CFA/`CPA` contours belong to `ppa-control-flow-and-constraints`, imperative `WHILE` equations and destructive
pointer shape graphs (`SG`) to `ppa-dataflow-and-slicing`, Galois widenings on infinite numeric chains to
`ppa-abstract-interpretation`, RPO/SCC solver queues to `ppa-fixedpoint-solvers`, and vulnerability-led threat
policies to `ppa-cyber-vulnerability-analysis`.

## Mini Projects and Exercises Roadmap

| Extension | Core Mechanism in Chapter 5 | Source Coordinate |
| :--- | :--- | :--- |
| `Mini Project 5.1` | Call-tracking effect system `Γ̂ ⊢_CT e : τ̂ & φ` separating latent vs immediate calls | [PPA Mini Project 5.1, p. 353] (book p. 353; PDF p. 370) |
| `Mini Project 5.2` | Pair `τ̂₁ ×^φ τ̂₂` and list `τ̂ list^φ` constructor annotations | [PPA Mini Project 5.2, p. 354] (book p. 354; PDF p. 371) |
| `Mini Project 5.3` | Executable `𝒲_CFA` / `𝒰_CFA` prototype implementation in functional languages | [PPA Mini Project 5.3, p. 355] (book p. 355; PDF p. 372) |
| `Mini Project 5.4` | Monotone lattice qualifiers (Binding-Time `S ⊑ D`, Security Clearance `C₁ ⊑ ··· ⊑ C_k`) | [PPA Mini Project 5.4, p. 355] (book p. 355; PDF p. 372) |
| `Mini Project 5.5` | Units of Measure & Y2K (`num^{scale BASE base}` `[external: abelian-group + affine-torsor]`) | [PPA Mini Project 5.5, p. 357] (book p. 357; PDF p. 374) |
| `Exercises 5.1–5.15` | Whole-tree `(5.2)` (`5.4*`), `--∅-->` (`5.5`), non-Moore `≤` (`5.9`), `AV(φ₂) = ∅` (`5.14`) | [PPA Exercise 5.4, p. 359] (book p. 359; PDF p. 376) [PPA Exercise 5.14, p. 362] (book p. 362; PDF p. 379) |

## Where to Go Next

When the optional `skills/` channel is installed, Chapter 5 procedures and formal specifications live relative to
the knowledge root:

- Actionable reconstruction, subtyping, region, and behaviour workflows: skills/ppa-types-effects-and-regions/SKILL.md
- Annotated `⊢_UL`/`⊢_CFA`, `UCAI`, Natural Semantics, covariant Moore families (`§§5.1–5.2`):
  skills/ppa-types-effects-and-regions/references/annotated-types-and-cfa-soundness.md
- `𝒲_UL`/`𝒲_CFA`, `SType` unification, `θ_A`, polarised subtyping `≤`, canonical `U8` (`§§5.3–5.4`):
  skills/ppa-types-effects-and-regions/references/inference-unification-and-subtyping.md
- Side effects, exceptions, stack-based regions (`[175, 176]`, `[external: Tofte–Talpin]`), CML behaviours, `Mini Projects 5.1–5.5` (`§§5.4.1–5.5`):
  skills/ppa-types-effects-and-regions/references/effects-exceptions-regions-and-behaviours.md
- Cross-approach master router and Chapter 1 / Appendices A–C: skills/ppa-program-analysis/SKILL.md
