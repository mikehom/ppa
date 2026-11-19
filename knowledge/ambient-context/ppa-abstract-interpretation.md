<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Standalone L0 ambient context for Chapter 4 Abstract Interpretation, Widening/Narrowing, Galois Connections, Domain Combinators, and Induced Operations. -->
<!-- @description: Orientation for abstract interpretation as systematic approximation: correctness relations, representation functions, Galois connections and insertions linking concrete and abstract domains, induced best transformers, widening to force convergence on infinite-height domains such as intervals, narrowing to recover precision, and combinators like reduced, tensor and independent attribute products. Use when designing a new abstract domain, proving an approximation sound, or deciding where to extrapolate. -->

# Abstract Interpretation: Galois Connections, Widening, and Domain Design

> Ambient orientation for Chapter 4 of *Principles of Program Analysis* (F. Nielson, H. R. Nielson,
> C. Hankin; corrected second printing, 2005). Grounded in [PPA Chapter 4, p. 211] (book p. 211; PDF p. 228)
> through [PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299).

## What Chapter 4 Is About

Chapter 4 develops **Abstract Interpretation** in a programming-language-independent setting (`G-U4a-01`): rather than
tying soundness and convergence to one syntax, it studies complete lattices of properties, fixed-point approximations
over infinite-height lattices, **Galois connections** between concrete and abstract spaces, modular domain combinators,
and systematic calculation of abstract transfer functions and widenings from concrete semantics
[PPA Chapter 4, p. 211] (book p. 211; PDF p. 228) [PPA §4.3, p. 233] (book p. 233; PDF p. 250)
[PPA §4.5, p. 258] (book p. 258; PDF p. 275).

Throughout Chapter 4, **smaller means more precise** (`l_1 ⊑ l_2` means `l_1` carries more information, `⊥` often
represents unreachability/emptiness, and `⊤` is trivially safe and uninformative, `G-U4a-04`), and analyses seek sound
over-approximations of **least fixed points (`lfp`)** [PPA §4.1.1, p. 214] (book p. 214; PDF p. 231).

## Four Pillars of the Framework

1. **Correctness Relations and Representation Functions (`§4.1`)**:
   - First-order analyses relate concrete values `V` to abstract properties `L` via a correctness relation `v R l`
     satisfying upward safety `(4.4)` and the Moore-family arbitrary-meet axiom `(4.5)`, which corresponds bijectively
     (`Lemma 4.5`) to a representation function `β : V → L` via `v R l ⇔ β(v) ⊑ l` (`G-U4a-03`, `G-U4a-05`)
     [PPA Lemma 4.5, p. 217] (book p. 217; PDF p. 234).
   - While `§4.1` covers first-order value-set analyses (`Constant Propagation`, `0-CFA`, `Shape Analysis`), `§§4.2–4.5`
     apply equally to second-order relational analyses (`G-U4a-03`) [PPA §4.1, p. 212] (book p. 212; PDF p. 229).
2. **Widening (`∇`) and Narrowing (`Δ`) Over Infinite-Height Lattices (`§4.2`)**:
   - Rich numerical lattices like `Interval` (`Example 4.10`, `Figure 4.2`) fail both the Ascending and Descending Chain
     Conditions (`ACC` and `DCC`, `U7`), so Kleene [external] iteration `f^n(⊥)` need not stabilise (`Figure 4.3`)
     [PPA Example 4.10, p. 222] (book p. 222; PDF p. 239) [PPA Figure 4.3, p. 224] (book p. 224; PDF p. 241).
   - **Widening (`∇`)** dynamically accelerates `(f_∇^n)_n` across `Ext(f)` into a reductive point `f_∇^m ∈ Red(f)`
     (`f(f_∇^m) ⊑ f_∇^m`, `lfp(f) ⊑ lfp_∇(f)`, `Proposition 4.13`, `Fact 4.14`), and **narrowing (`Δ`)** subsequently
     descends inside `Red(f)` (`lfp(f) ⊑ lfp_∇^Δ(f) ⊑ lfp_∇(f)`, `Lemma 4.16`, `Proposition 4.17`) to recover loop-guard
     bounds (`Example 4.18`) [PPA Proposition 4.13, p. 227] (book p. 227; PDF p. 244)
     [PPA Lemma 4.16, p. 230] (book p. 230; PDF p. 247).
3. **Galois Connections, Insertions, and Modular Combinators (`§§4.3–4.4`)**:
   - A **Galois connection** `(L, α, γ, M)` pairs lower adjoint `α` and upper adjoint `γ` via the adjunction law
     `α(l) ⊑ m ⇔ l ⊑ γ(m)` (`Proposition 4.20`): `α` preserves all joins `⨆` (`α(⊥) = ⊥`) and `γ` preserves all meets `⨅`
     (`γ(⊤) = ⊤`, `Lemma 4.22`, `G-U4a-19`) [PPA Proposition 4.20, p. 236] (book p. 236; PDF p. 253)
     [PPA Lemma 4.22, p. 239] (book p. 239; PDF p. 256).
   - Quotienting redundant abstract elements via the **reduction operator** `ς(m) = α(γ(m))` (`Proposition 4.29`,
     `Fact 4.31`) yields a **Galois insertion** (`α ∘ γ = λm.m`, `Lemma 4.27`), and `§4.4` composes domains via
     sequential pipelines, independent attributes (`×`), powerset relational tensor products (`⊗`), function spaces
     (`S → M`, `M_1 → M_2`), and `ς`-reduced products (`Example 4.39` shrinking `45` bits to `29` bits in `AB`)
     [PPA Proposition 4.29, p. 244] (book p. 244; PDF p. 261) [PPA Example 4.39, p. 257] (book p. 257; PDF p. 274).
4. **Induced Transformers, Generalised Monotone Frameworks, and `γ`-Widening (`§4.5`, `U6`)**:
   - Inducing along `α` yields the best abstract transformer `α_2 ∘ f_p ∘ γ_1` (`Lemma 4.41`, preserving optimality) and
     fixed-point soundness `lfp(f) ⊑ γ(lfp(g))` whenever `α ∘ f ∘ γ ⊑ g` (`Lemma 4.42`), lifting directly to
     **generalised Monotone Frameworks** (`§4.5.2`, `γ(ȷ) = ι`) [PPA Lemma 4.41, p. 260] (book p. 260; PDF p. 277)
     [PPA §4.5.2, p. 264] (book p. 264; PDF p. 281).
   - Inducing along `γ` (`l_1 ∇_L l_2 = γ(α(l_1) ∇_M α(l_2))`, `Proposition 4.44`, `Lemma 4.45`) imports termination
     from `M` while keeping straight-line precision in `L` [PPA Proposition 4.44, p. 268] (book p. 268; PDF p. 285).

## Core Chapter 4 Invariants & Polarity Traps

1. **Widening is neither monotone nor symmetric (`BKL-002`, `G-U4a-10`, `G-U4a-11`)**: Always evaluate `old ∇ new`
   behind an explicit `if f(x) ⊑ x` guard, handle `⊥ ∇_K x = x` on step 1 (`G-U4a-13`), and never assume narrowing is
   dual to widening (`G-U4a-15`) or inducible via `γ(α(l_1) Δ_M α(l_2))` (`Exercise 4.24`, `G-U4b-18`)
   [PPA §4.2.1, p. 225] (book p. 225; PDF p. 242) [PPA Exercise 4.24, p. 282] (book p. 282; PDF p. 299).
2. **Guard approximation flips direction (`G-U4b-21`) & Denotational Semantics is NOT dual (`G-U4b-20`)**: Reachable
   point properties `l_ℓ` approximate *upward* via Galois connections, whereas transformation enabling conditions
   `l_ℓ ⊑ l_Ξ` must approximate *downward* via **dual Galois connections**; Denotational Semantics shares `lfp` with
   inverted `⊑` and is **not** lattice-dual to Abstract Interpretation
   [PPA Chapter 4 Concluding Remarks, p. 273] (book p. 273; PDF p. 290).
3. **Unbounded `Z` vs machine arithmetic (`BKL-001`)**: `Interval` ranges over mathematical `Z ∪ {-∞, ∞}`; fixed-width
   `[external: two's-complement wraparound]` requires `[external: wrapped-interval]` or modular domains.

## Key Vocabulary

| Term | Meaning in Chapter 4 |
| :--- | :--- |
| Correctness relation `R` | `v R l` satisfying upward safety `(4.4)` and Moore-family glb closure `(4.5)` [PPA §4.1.1, p. 214] (book p. 214; PDF p. 231) |
| Representation function `β` | Canonical encoder `β : V → L` generating `v R l ⇔ β(v) ⊑ l` [PPA §4.1.2, p. 216] (book p. 216; PDF p. 233) |
| Widening operator `∇` | Upper bound operator forcing every ascending chain `(l_n^∇)_n` to stabilise [PPA §4.2.1, p. 226] (book p. 226; PDF p. 243) |
| Narrowing operator `Δ` | Contractive `l_2 ⊑ (l_1 Δ l_2) ⊑ l_1` (`l_2 ⊑ l_1`) stabilising descending chains in `Red(f)` [PPA §4.2.2, p. 230] (book p. 230; PDF p. 247) |
| Galois connection `(L, α, γ, M)` | Monotone `(α, γ)` satisfying `α(l) ⊑ m ⇔ l ⊑ γ(m)` (`(4.10)`) [PPA Proposition 4.20, p. 236] (book p. 236; PDF p. 253) |
| Galois insertion | Galois connection with `α ∘ γ = λm.m` (`α` surjective, `γ` injective) [PPA Lemma 4.27, p. 243] (book p. 243; PDF p. 260) |
| Reduction operator `ς` | `ς(m) = ⨅{m' | γ(m) = γ(m')} = α(γ(m))` collapsing `γ`-equivalent elements [PPA Fact 4.31, p. 246] (book p. 246; PDF p. 263) |
| Independent vs relational | `(M_1 × M_2)` component-wise vs `𝒫(D_1 × D_2)` (`⊗`) coupled tuples [PPA §4.4.1, p. 250] (book p. 250; PDF p. 267) |
| Direct vs reduced product | `(L, α, γ, M_1 × M_2)` (`γ_1 ⊓ γ_2`) vs quotient `ς[M_1 × M_2]` / `AB` [PPA §4.4.2, p. 256] (book p. 256; PDF p. 273) |
| Induced operation | Best transformer `α_2 ∘ f_p ∘ γ_1` (`§4.5.1`) or widening `γ(α(l_1) ∇_M α(l_2))` (`§4.5.3`) [PPA §4.5, p. 259] (book p. 259; PDF p. 276) |
| Upper closure operator `ρ` | Monotone, extensive, idempotent `ρ : L → L` (`ρ_1 ⊓ ρ_2` = reduced product) [PPA Chapter 4 Concluding Remarks, p. 270] (book p. 270; PDF p. 287) |

## Out of Scope Here (Adjacent Skills)

Classical finite-height `WHILE` analyses, `ud`/`du` slicing, and `§2.6` Shape Analysis mechanics live in
`ppa-dataflow-and-slicing`; higher-order `0-CFA`/`k-CFA` constraint systems in `ppa-control-flow-and-constraints`;
annotated type/effect/region systems in `ppa-types-effects-and-regions`; RPO/SCC worklist scheduling in
`ppa-fixedpoint-solvers`; and vulnerability threat modelling in `ppa-cyber-vulnerability-analysis`.

## Where to Go Next

When the optional `skills/` channel is installed, Chapter 4 procedures and formal specifications live relative to the
knowledge root:

- Actionable domain-design, widening/narrowing & soundness workflows: skills/ppa-abstract-interpretation/SKILL.md
- Mundane correctness (`§4.1`), `Interval`, widening `∇`, and narrowing `Δ` (`§4.2`):
  skills/ppa-abstract-interpretation/references/correctness-and-fixed-points.md
- Galois connections, adjoints, Galois insertions, `ς`, upper closure operators (`[external: uco(L)]`), and duality (`§4.3`, `Concluding Remarks`):
  skills/ppa-abstract-interpretation/references/galois-connections-and-insertions.md
- Domain combinators, `AB` (`§4.4`), induced operations, generalised Monotone Frameworks (`§4.5`), and Mini Projects:
  skills/ppa-abstract-interpretation/references/combinators-and-induced-operations.md
