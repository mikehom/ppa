<!-- @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006 -->
<!-- @decision DEC-PPA-002: Model adaptation tunes retrieval granularity, progressive-disclosure cadence, reasoning budgets, and self-verification gates by generic model capability tier while keeping canonical knowledge, budgets, and discovery contracts invariant. -->

# MODEL_ADAPTATION_GUIDE: Capability-Tier Tuning Across Model Classes

## 0. Purpose, Invariants, and Strict Portability Boundary

This specification defines how serving adapters, orchestration wrappers, and benchmark harnesses tune
retrieval chunking, trigger phrasing clarity, reasoning-effort budgets, and self-verification checkpoints
across models of differing reasoning and context capacities. It operationalizes portability gate `C5.6`
and pairs directly with [ARCHITECTURE.md](ARCHITECTURE.md), [CONFORMANCE_SPEC.md](CONFORMANCE_SPEC.md),
and [PORTING_GUIDE.md](PORTING_GUIDE.md).

### 0.1 Hard Invariants (`C1`-`C5`)

1. **Zero model-specific conditionals in the canonical core (`C5.6`)**: Neither
   `knowledge/skills/*/SKILL.md` nor `evals/cases.yaml` may contain branches, hints, or instructions
   addressed to a named model, vendor family, or harness. All tier adaptation lives strictly inside
   runtime orchestrators, adapter slicers, or `DEV-NOFILES` query endpoints.
2. **No relaxation of formal precision (`ARCHITECTURE.md` §7)**: Smaller context windows NEVER permit
   dropping theorem hypotheses (`SMOOTHING_TRAP`), reversing lattice or approximation direction
   (`SIGNATURE_DISTORTION`), omitting `Gotcha Ledger` caveats (`SILENT_GOTCHA_TRUNCATION`), or
   reconstructing formulas from pretraining weights (`HALLUCINATED_SYMBOL`). Adaptation alters
   *slice granularity* and *retrieval cadence*, never formal truth.
3. **Zero standing always-on tax (`C2.6`)**: Guardrails for weaker instruction-following tiers never
   add standing bytes to `R0` global system instructions; compensating runtime checks attach dynamically
   only after `R2` skill activation.
4. **Canonical line budgets remain fixed (`C3.1`-`C3.4`)**: Canonical artifacts stay anchored at
   `50-99` lines (`L0` router), `80-250` lines (`L0` ambient), `<= 450` lines (`L1` reference), and
   `250-499` lines (`L2` skill).

---

## 1. Generic Capability Tiers and Working-Set Budgets

| Tier | Architectural Profile | Context Budget (`R1`+`R2`+`R3` Co-Load) | Headroom Rule (User Code / Traces) | Primary Strength | Primary Failure Mode Under Load |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Tier H` (`High-Reasoning Frontier`) | Large-context reasoning models (`>= 128k` context, multi-step symbolic deduction) | Full co-load (`<= 1,750` lines: router + 1 `L2` + up to 2 `L1` + targeted `L3` anchors) | Reserve `>= 75%` of active context for target source, CFGs, and logs | Cross-chapter isomorphism proofs (`U1`-`U10`), soundness reasoning, adversarial auditing | Over-confident recall of formulas or lemma conditions from training priors without executing `R3` reads (`HALLUCINATED_SYMBOL`) |
| `Tier M` (`Mid-Tier Fast`) | Balanced coding models (`32k-128k` context, fast tool execution) | Focused co-load (`<= 1,050` lines: 1 `L2` + 1 active `L1` section or single `L1` file) | Keep loaded PPA knowledge below `<= 15%` of prompt window | Following explicit numbered `L2` checklists, constraint traces, schema validation | Over-generalizing equivalences across `corresponds_to` edges while overlooking stated `differs` conditions (`SMOOTHING_TRAP`) |
| `Tier S` (`Context-Constrained / Small`) | Compact or local-inference models (`8k-32k` context, shallow attention budget) | Micro-sliced (`<= 450` lines total per turn; `<= 180` lines per `L1`/`L3` fetch via `DEV-NOFILES`) | Load strictly the current step + target AST/IR slice (`<= 400` PPA lines max) | Deterministic execution of concrete single-rule transforms and table lookups | Dropping side conditions (`ACC`, distributivity), flipping inequalities (`<=` vs `>=`), and sibling trigger bleed |

### 1.1 Working-Set Arithmetic and Eviction Rule

Orchestrators SHOULD enforce a hard line ceiling on active knowledge per turn:

1. **Zero carry-over rule**: Once `R1` (orientation) or `L0` (router) selects a domain skill, evict
   the router text and irrelevant orientation prose from active context on `Tier M` and `Tier S`.
2. **One active reference at a time (`Tier M` / `Tier S`)**: When an `L2` procedure steps from one
   `references/*.md` target to another, drop the previous `L1` slice from the active window before
   fetching the next anchor.
3. **Never dump `L3` files**: Even on `Tier H`, `corpus/RAW_KNOWLEDGE.md` and
   `ontology/concept_graph.json` are accessed solely by exact section offset, node ID, or coordinate
   lookup (`R3`), never loaded whole.

---

## 2. Adapting Trigger Phrasing and Discovery Metadata (`R1`/`R2`, `C2.5`, `C4`)

Discovery accuracy depends on the `name` and `description` indexed at `R2` (`<= 1,024` chars, zero
`N8` citations or numbered lists, `C2.5`) plus `R1` orientation files. Canonical descriptions use one
universal template (`Use when ... Do not use for ...; use <sibling> instead.`) engineered so even
`Tier S` semantic routers achieve `< 0.50` pairwise sibling Jaccard overlap (`C4.3`) without runtime
conditionals:

1. **Front-load concrete task verbs and observables**: Lexical and compact embedding routers weight
   opening words heavily. Lead `Use when` with practitioner observables (e.g. *computing reaching
   definitions or slicing live variables*, *diagnosing worklist oscillation*, *resolving indirect
   callback targets*) before formal lattice or type-theoretic nouns.
2. **State orthogonal negative discriminators (`C4.1`-`C4.2`)**: Every skill description MUST anchor
   its boundary cleanly against adjacent skills:
   - *Formulation vs Solver Execution*: `ppa-dataflow-and-slicing` and
     `ppa-control-flow-and-constraints` build equations/constraints; `ppa-fixedpoint-solvers`
     schedules, orders (`rPostorder`, `SCC`), and optimizes worklist solving (`[PPA Table 6.1, p. 369]`).
   - *Untyped vs Typed CFA*: `ppa-control-flow-and-constraints` handles untyped terms (`Ĉ`, `ρ̂`,
     self-application); `ppa-types-effects-and-regions` handles typed `{π} ∪ φ` annotations, covariant
     `Typê[τ]` vs contravariant subtyping, and effect systems (`[PPA §5.1, p. 283]`).
   - *Abstract Domain Synthesis vs Fixed Frameworks*: `ppa-abstract-interpretation` constructs and
     widens domains via Galois connections; `ppa-dataflow-and-slicing` analyzes programs inside fixed
     Bit Vector or Monotone Frameworks.
   - *Monotone Type Systems vs Imperative DFA*: `ppa-types-effects-and-regions` handles type-based
     clearance/BTA/effect formulations; `ppa-cyber-vulnerability-analysis` composes security detection
     workflows across chapters without duplicating `L3` cores.
3. **Router invocation discipline by tier**:
   - `Tier H`: May evaluate the router and open the matched `L2` + paired `L1` references in a single hop.
   - `Tier M`: Always evaluate `ppa-program-analysis/SKILL.md` (`L0`) first whenever a prompt mentions
     concepts spanning two chapters before committing to one domain skill.
   - `Tier S`: Present only the selected `SKILL.md` step group after routing completes.

---

## 3. Progressive-Disclosure Chunk Granularity and Section Slicing (`ARCHITECTURE.md` §4.3)

Adapters vary chunk retrieval size—never file contents—across capability tiers:

| Disclosure Stage | `Tier H` Schedule | `Tier M` Schedule | `Tier S` (`DEV-NOFILES` / Adapter-Sliced) Schedule |
| :--- | :--- | :--- | :--- |
| `R1` Orientation | Load matched `ppa-*.md` (`80-250` lines) alongside router when vocabulary spans paradigms | Load `ppa-*.md` summary + vocabulary + pointer table (`<= 120` lines) | Serve 25-line orientation card (`central question + soundness direction + L1/L2 links`) |
| `R2` `L2` Skill | Load whole `SKILL.md` (`250-499` lines) | Load whole `SKILL.md` (`250-499` lines) | Serve active workflow step group (`<= 180` lines) plus trigger/negative boundary header |
| `R2` `L1` Reference | Co-load up to 2 related `L1` files (`<= 450` lines each) for comparative proofs | Load **only** the single `L1` file named by the active `L2` step | Serve **single H2/H3 section** (`<= 180` lines) bundled with its `conditions` and `gotcha_refs` |
| `R3` `L3` Lookup | Read targeted anchored block (`40-120` lines) | Read strictly the single addressed table, lemma, or ledger bullet (`20-60` lines) | Serve atomic JSON node (`formal_summary`, `conditions`, verbatim signature only; `<= 80` lines) |

### 3.1 Deterministic Section-Slicing Algorithm (`Tier S` / `DEV-NOFILES`)

When a serving adapter slices an `L1` reference or `L3` entry below file level:

1. Split `L1` strictly on H2 (`##`) or H3 (`###`) boundaries; never bisect an inference rule, code block,
   comparison table, or `conditions` list (`SIGNATURE_DISTORTION`).
2. Compute `line_count` under `CONFORMANCE_SPEC.md` `N2` and verify the served fragment satisfies
   `<= 180` lines (`<= 450` absolute `C3.3` ceiling).
3. Resolve every concept ID cited inside the sliced section against `ontology/concept_graph.json` and
   append any missing `conditions` clauses or `G-*` ledger warnings (`SILENT_GOTCHA_TRUNCATION`)
   at the bottom of the fragment.
4. Preserve all `N8` inline citations (for example `[PPA §1.3, p. 6] (book p. 6; PDF p. 26)`) inside the served fragment (`C1.8`). For example,
   any slice invoking the `d(G_S, T) + 3` bound MUST carry its three qualifying hypotheses (`L = P(D)`
   finite set, unary RHS `(x_{j_i} ∩ Y_i^1) ∪ Y_i^2`, `rPostorder` of DFSF `T`, `[PPA Lemma 6.12, p. 380]`).

---

## 4. Reasoning and Effort Budgets by Task Class

| Task Class | Canonical Inputs | `Tier H` Allocation | `Tier M` Allocation | `Tier S` Decomposition / Escalation Rule |
| :--- | :--- | :--- | :--- | :--- |
| **1. Task Classification & Routing** | `L0` router (`ppa-program-analysis`) | Low effort; verify negative routes | Medium effort; check at least 1 negative sibling | Single-turn routing; escalate to `Tier M`/`Tier H` if prompt spans `>= 2` approaches |
| **2. Trace Execution & Bug Triage** | `L2` skill + 1 `L1` section | Medium effort; execute trace + check preconditions | High effort; echo each precondition before state update | Decompose into 1 sub-turn per numbered `L2` step (`<= 200` PPA lines + target slice) |
| **3. Formal Proof / Unification Synthesis** | `L1` comparisons + `U1`-`U10` edges | Maximum reasoning; check both `conditions` and `differs` | High reasoning with explicit `R3` read before each inference step | **Escalate to `Tier H`** (`Tier S` MUST NOT synthesize unverified multi-step proofs) |
| **4. Conformance & Anti-Degradation Audit** | `L3` / rendered source + `C1`-`C6` | Independent Tier B adversarial judge pass | Automated Tier A scripts (`validate_ppa_knowledge.py`, `check_portability_hygiene.py`) | Tier A script runner only; never grant Tier B correctness signoff authority |

---

## 5. Runtime Verification Gates Against Tier Failure Modes

Orchestrators wrapping PPA skills SHOULD apply deterministic runtime gates matched to active tier hazards:

### 5.1 Anti-Degradation Runtime Checklists

1. **Against `HALLUCINATED_SYMBOL` (`Tier H` over-confidence hazard)**:
   - Require every cited theorem, table number, or displayed rule in a final answer to trace directly
     to an `R2`/`R3` tool read executed in the current turn window; reject memory-reconstructed math
     whenever `L3` / source pages were not inspected.
2. **Against `SMOOTHING_TRAP` (`Tier M` & `Tier S` omission hazard)**:
   - Require an explicit **Precondition Echo** block before asserting termination (`ACC` vs widening),
     precision coincidence (`MFP == MOP`: distributivity AND non-empty valid paths `path_o(l)`), or
     tight iteration complexity (`[PPA Lemma 6.12, p. 380]`). Unverified conditions MUST emit
     `CONDITIONAL / UNVERIFIED`.
3. **Against `SIGNATURE_DISTORTION` (`Tier S` direction-flip hazard)**:
   - Verify these four invariants explicitly against `L1` before generating analyzer logic:
     - **Approximation direction**: May (`⊔`, over-approximate) vs Must (`⊓`, under-approximate)
     - **CFG traversal**: Forward (`flow`) vs Backward (`flow^R`)
     - **Type/effect variance**: §5.2 covariant `Typê[τ]` domain ordering vs §5.4 contravariant domain
       and invariant `ref` / `chan` shape-conformant `<=`
     - **Constraint equivalence**: `x ⊒ t_i` shares all solutions with `x = x ⊔ t_1 ⊔ ...`, yet shares
       only the **least** solution with `x = t_1 ⊔ ...` (`[PPA §6.1, p. 366]`)
4. **Against `C4` Sibling Bleed (`Tier M` & `Tier S` trigger drift)**:
   - Run all `evals/cases.yaml` routing regression suites after any wrapper, chunker, or adapter update;
     resolve overlaps via `T5` (`ARCHITECTURE.md` §6.1) in the canonical core rather than patching runtime prompts.

### 5.2 Precondition Echo Output Template (`Tier M` & `Tier S` Orchestrators)

Runtime wrappers SHOULD enforce this compact structural block before an agent emits an affirmative
analysis guarantee:

```text
PRECONDITION_ECHO:
  target_result: "<Theorem / Lemma / Fact + N8 citation>"
  required_conditions:
    - condition: "<clause 1 from L1/L3 conditions list>"
      status: "VERIFIED | VIOLATED | UNCHECKED"
  fallback_action: "<widening / reduced-precision caveat / escalate if VIOLATED or UNCHECKED>"
```

If any entry resolves to `UNCHECKED` or `VIOLATED`, the orchestrator MUST block claims of exact
precision (`MFP == MOP`) or bounded linear convergence (`d(G_S, T) + 3`) and instead surface the
corresponding `L1` fallback path (`[PPA Lemma 6.4, p. 370]`).

### 5.3 Physical Evaluator Separation (`ARCHITECTURE.md` §7)

No model tier—including `Tier H`—may approve its own canonical edits or target port outputs. Mandatory
Tier A script execution (`scripts/check_portability_hygiene.py`, `scripts/validate_ppa_knowledge.py`,
`scripts/verify_port_conformance.py`) combined with an isolated read-only Tier B evaluation context
([CONFORMANCE_SPEC.md](CONFORMANCE_SPEC.md) §5, [ARCHITECTURE.md](ARCHITECTURE.md) §7) remains invariant
across all capability tiers.

---

## 6. Eval Regression Calibration and Cross-Tier Certification (`C4.5`-`C4.7`, `C5.6`)

When validating a canonical core or compiled port across tiers:

1. **Same `evals/cases.yaml` across all tiers (`B8`, `C5.6`)**: Execute the exact same canonical routing
   and negative-boundary suite (`>= 3` positive cases and `>= 2` sibling/`none` negatives per skill,
   plus `C4.7` `corresponds_to` boundary pairs) against `Tier H`, `Tier M`, and `Tier S` configurations.
2. **Diagnose failures by root cause**:
   - Failure localized to `Tier S` with `Tier H` passing: tighten adapter `R2` description extraction,
     reduce served noise (`§1.1` zero carry-over), or apply `§3.1` atomic micro-slicing (`<= 180` lines).
   - Failure shared across `Tier H` and `Tier M`: refactor canonical skill `description` triggers or
     routing discriminators upstream under trigger `T5` (`ARCHITECTURE.md` §6.1).
3. **Track per-tier token telemetry without relaxing conformance**: Record loaded lines per turn and
   skill-selection precision across tiers; reject any adapter optimization that improves token cost by
   dropping `conditions`, `N8` citations, or `Gotcha Ledger` pointers (`CONFORMANCE_SPEC.md` §8).
