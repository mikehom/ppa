<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Standalone cross-book L0 ambient orientation projecting Chapters 1-6 and Appendices A-C onto static vulnerability analysis and soundness auditing. -->
<!-- @description: Orientation that maps program analysis results onto vulnerability hunting: taint sources and sanitisers as may or must properties, false negatives versus false positives in scanner triage, heap lifetime errors and aliasing, integer overflow bounds, indirect call targets for control flow integrity, arena escape, exception and deadlock protocols, and scanner denial of service. Use when auditing security tooling soundness or translating a weakness class into an analysis specification. -->

# Program Analysis for Vulnerability Modeling, Sanitizer Soundness, and SAST Triage

> Cross-book ambient orientation assembling the security and vulnerability-analysis projections (`P4`, `P5`)
> of *Principles of Program Analysis* (F. Nielson, H. R. Nielson, C. Hankin; corrected second printing, 2005),
> grounded in [PPA §1.1, p. 2] (book p. 2; PDF p. 22) through [PPA Appendix C, p. 427] (book p. 427; PDF p. 442).
> All vulnerability classes (`[external: CWE]`) and scanner patterns are interpretive projections (`P2`).

## The Central Security Thesis: Safe Approximation & Soundness Preconditions

Static vulnerability analysis asks whether **any** concrete execution from an untrusted environment can reach a
security-violating configuration `[external]`. Under `Figure 1.1` [PPA §1.1, p. 2] (book p. 2; PDF p. 22), an
absence-of-bug proof must **over-approximate** dangerous behaviours (computing a reductive upper bound `F(x) ⊑ x`
in `Red(F)` above `lfp(F)`, [PPA §A.4, p. 402] (book p. 402; PDF p. 418)), whereas a definite-sanitization proof
must **under-approximate** validated expressions (`(𝒫(D), ⊇)` where join `⊔_L` is set intersection `∩` and
`⊥_L = D`, [PPA §2.3, p. 66] (book p. 66; PDF p. 85)). Every silent false negative (`FN`) in a static security
scanner traces to a violated mathematical precondition of one of the book's four paradigms `[external]`:

| PPA Pillar | Security Question Answered `[external]` | Soundness Failure Causing Silent False Negatives (`FN`) `[external]` | Precision Failure Causing False Alarms (`FP`) `[external]` |
| :--- | :--- | :--- | :--- |
| **Data Flow & Shape (`Chapter 2`)** | Source-to-sink taint (`RD`), must-sanitization (`AE`), secret-wipe survival (`LV`), heap UAF/double-free (`SG`) `[external]` | Using `∪` for must-sanitizers `[external]`; `ι = ∅` dropping `(x, ?)` uninitialised inputs or trailing `[key := 0]` wipes; `strong update` [PPA §2.6.3, p. 115] (book p. 115; PDF p. 134) on summary node `n_∅` or skipping `n_∅` in `kill_{x.sel}` [PPA §2.6.3, p. 125] (book p. 125; PDF p. 144) | `k = 0` / missing `inter-flow⋆` cross-over smearing across sanitizer wrappers `[external]` [PPA Example 2.40, p. 98] (book p. 98; PDF p. 117); non-distributive validator merges |
| **Control Flow & Constraints (`Chapter 3`)** | Indirect call / vtable / callback target sets (`[external: CFI]`) & deserialization gadget reachability (`[external: CWE-502]`) | Analysing exported libraries/plugins as closed systems instead of open systems `e_∘` / `e_⋆` [PPA §3.1.1, p. 149] (book p. 149; PDF p. 167) [PPA §3.4.2, p. 182] (book p. 182; PDF p. 200) | Monovariant `0-CFA` merging callback tables; staged `0-CFA` + DFA retaining dead-branch gadgets (`Example 3.31`, [PPA Example 3.31, p. 189] (book p. 189; PDF p. 207)) |
| **Abstract Interpretation (`Chapter 4`)** | Buffer-bounds (`0 ≤ idx < len`), integer-overflow & signedness checks (`[external: CWE-787 / CWE-190 / CWE-195]`) | Using unbounded `Z`-intervals [PPA Example 4.10, p. 221] (book p. 221; PDF p. 238) directly on wrapping fixed-width machine integers `[external]` | Independent Attribute `L₁ × L₂` losing `idx < len` [PPA §4.4.1, p. 249] (book p. 249; PDF p. 266); unguarded or step-1 `⊥ ∇_K` over-widening to `[-∞, ∞]` [PPA Example 4.15, p. 229] (book p. 229; PDF p. 246) |
| **Type & Effect Systems (`Chapter 5`)** | Taint/clearance types (`Mini Project 5.4`), `ref`/`chan` invariance (`[external: CWE-843]`), arena `letregion` safety (`§5.4.3`), exceptions & `CML` protocols | Covariant mutable `ref`/`chan` [PPA §5.4.1, p. 324] (book p. 324; PDF p. 341); `[gen]` ignoring `FV(φ)` (`Example 5.36`, [PPA Example 5.36, p. 346] (book p. 346; PDF p. 363)); `Observe` missing escaping regions [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355); big-step vacuity on infinite server loops [PPA §5.2.1, p. 292] (book p. 292; PDF p. 309); left-distributivity hiding deadlocks [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365) | Monomorphic arrows without contravariant subtyping (`Example 5.5`, [PPA Example 5.5, p. 289] (book p. 289; PDF p. 306)); monomorphic region recursion leaking arenas |
| **Fixed-Point Solvers (`Chapter 6`)** | Scaling whole-program SAST/taint queries (`[external: CWE-400 / CWE-407]`) & sink-to-source local slicing (`p. 385`) | Aborting Step 2 on timeout before `W = empty` and returning partial `Analysis_i ⊑ μ_𝒮` [PPA §6.1.1, p. 371] (book p. 371; PDF p. 387) (**timeout-evasion bypass** `[external]`) | Multiset LIFO duplicate blowup (`Figure 6.1`) & unsplit `M`-way joins (`O(h·M²·N)` vs `O(h·M·N)` in [PPA Exercise 6.5, p. 389] (book p. 389; PDF p. 405)) |

## Five Non-Negotiable Security Soundness Invariants

1. **Polarity & Extremal Boundary Discipline**: May-taint uses `(⊆, ∪)` with `ι = {(x, ?) | x ∈ FV(S⋆)}`
   [PPA §2.1.2, p. 43] (book p. 43; PDF p. 62); must-sanitization uses `(⊇, ∩)` with `⊥_L = U`
   [PPA Table 2.1, p. 40] (book p. 40; PDF p. 59); Live Variables must include secret buffers in `ι` at
   `final(S⋆)` so Dead Code Elimination never strips zeroization writes (`BKL-006`, `[external: CWE-14]`).
2. **Singleton Uniqueness Before Strong Update**: Strong state overwrites (`Freed`, `Sanitized`, field kill)
   are sound **only** on concrete singleton locations (`n_X` with `X ≠ ∅` in `§2.6`), never on summary node
   `n_∅` (`§2.6.2`) or multi-alias lexical regions (`§5.4.3`) `[external: CWE-416 / CWE-415]`.
3. **Variance & Effect-Guarded Polymorphism**: Function subtyping is contravariant in inputs (`§5.4.1`),
   whereas mutable cells (`ref_ϖ τ̂`) and channels (`τ̂ chan r`) are **strictly invariant** in payload `τ̂`, and
   polymorphic `[gen]` forbids quantifying variables free in allocation effects `φ` (`Example 5.36`)
   `[external: CWE-843]`.
4. **Relational & Modular Arithmetic Fidelity**: Proving `0 ≤ idx < len` (`[external: CWE-787]`) requires
   relational products (`⊗` / reduced `ς[M₁ × M₂]`, [PPA §4.4.2, p. 256] (book p. 256; PDF p. 273)) plus
   modular overflow guards (`[external: CWE-190 / CWE-195]`), never Independent Attribute `Z`-intervals alone.
5. **No Silent Timeout Under-Approximation**: Any worklist cutoff with `W ≠ empty` returns `Analysis_i ⊑ μ_𝒮`, not certified reductive,
   [PPA §6.1.1, p. 371] (book p. 371; PDF p. 387); unresolved cones must be widened (`Exercise 6.13`,
   [PPA Exercise 6.13, p. 391] (book p. 391; PDF p. 407)) or conservatively tainted to `⊤_L` `[external]`.

## Key Security-to-PPA Vocabulary Mapping

| Security Concept `[external]` | PPA Formal Counterpart & Coordinate |
| :--- | :--- |
| Taint source / uninitialised input | `(x, ?) ∈ ι` in Reaching Definitions & `? ∈ UD(x, ℓ)` [PPA §2.1.2, p. 43] (book p. 43; PDF p. 62) [PPA §2.1.5, p. 54] (book p. 54; PDF p. 73) |
| Definite sanitizer / authz dominator | Forward-must `AE` (`∩`) & Dominator `Dom(n)` greatest solution [PPA Table 2.1, p. 40] (book p. 40; PDF p. 59) [PPA Exercise 6.4, p. 389] (book p. 389; PDF p. 405) |
| Context-sensitive taint summary | Small assumption sets `Δ = D` (`𝒫(D × D)`) & `CPA` contours [PPA §2.5.5, p. 100] (book p. 100; PDF p. 119) [PPA §3.6.2, p. 196] (book p. 196; PDF p. 214) |
| Heap alias summary vs singleton cell | Summary `n_∅` + `is` heap sharing vs `n_X` (`X ≠ ∅`) [PPA §2.6.2, p. 110] (book p. 110; PDF p. 129) [PPA §2.6.2, p. 114] (book p. 114; PDF p. 133) |
| Arena / pool lifetime escape check | `letregion ϱ⃗` & `Observe(Γ̂, τ̂, r)(φ)` [PPA Table 5.13, p. 338] (book p. 338; PDF p. 355) |
| Open-world attacker entrypoint | Open-system `0-CFA` constraints `e_∘` / `e_⋆` [PPA §3.1.1, p. 149] (book p. 149; PDF p. 167) [PPA §3.4.2, p. 182] (book p. 182; PDF p. 200) |
| Uncaught exception cleanup bypass | `Table 5.10` `φ₁ ∪ (φ₂ \ {s})` with `β \ {s} = β` [PPA Table 5.10, p. 328] (book p. 328; PDF p. 345) [PPA §5.4.2, p. 330] (book p. 330; PDF p. 347) |
| Concurrent `TOCTOU` / deadlock trace `[external]` | `CML` `[comm]` causal behaviour `r!τ̂`, `r?τ̂`, `φ₁ ; φ₂`, `φ₁ + φ₂` (`Tables 5.15, 5.17–5.18`) [PPA Table 5.15, p. 343] (book p. 343; PDF p. 360) [PPA Table 5.17, p. 347] (book p. 347; PDF p. 364) [PPA Table 5.18, p. 348] (book p. 348; PDF p. 365) |
| On-demand sink-to-source slice | Local fixed-point solvers (`[29, 51, 54]`) [PPA Chapter 6 Concluding Remarks, p. 385] (book p. 385; PDF p. 401) |

## Out of Scope Here (Adjacent Skills)

Purely non-security compiler optimisations, language-theoretic proofs, and generic solver implementations belong
to the chapter skills:

- `ppa-program-analysis`: paradigm selection across the four approaches and Appendices A–C foundations.
- `ppa-dataflow-and-slicing`: classical compiler optimisations (`AE`, `VB`, `LV`, constant folding) and heap shape mechanics without security threat policies.
- `ppa-control-flow-and-constraints`: higher-order functional closure tracking (`0-CFA`, `k`-CFA, `CPA`) for call-graph construction and inlining.
- `ppa-abstract-interpretation`: Galois connection algebra, closure/reduction operators, and general numerical domains.
- `ppa-types-effects-and-regions`: Hindley–Milner type/effect unification (`W_UL`, `W_CFA`) and non-security region translation.
- `ppa-fixedpoint-solvers`: general worklist data structures, reverse postorder, Round Robin, and strong-component iteration traces.

## Where to Go Next

When the `skills/` channel is installed, formal security references and workflows live under
`ppa-cyber-vulnerability-analysis`:

- Taint polarity, context-sensitive sanitizers & security types:
  `skills/ppa-cyber-vulnerability-analysis/references/taint-sanitization-and-information-flow.md`
- Heap shape strong updates, lexical regions & numeric bounds:
  `skills/ppa-cyber-vulnerability-analysis/references/memory-heap-and-numeric-bounds-safety.md`
- Open-world call graphs, exception/concurrent protocols & solver DoS resilience:
  `skills/ppa-cyber-vulnerability-analysis/references/callgraph-cfi-concurrency-and-scanner-dos.md`
