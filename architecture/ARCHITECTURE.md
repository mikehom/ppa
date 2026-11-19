<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Vendor-neutral 4-altitude canonical core (L0-L3) compiled into target harness layouts; lossless formal content lives at L3, every higher altitude is a budgeted, cited projection of it. -->

# ARCHITECTURE: 4-Altitude Semantic Knowledge Distribution for *Principles of Program Analysis*

## 0. Status, Scope, and Normative Language

- **Status:** Normative. `MUST`, `MUST NOT`, `SHOULD`, `MAY` carry their usual specification meaning.
- **Scope:** The structure of `knowledge/`, `ontology/`, and `corpus/` and the rules by which content is
  placed, retrieved, refactored, and protected from degradation. Per-harness layouts are normative in
  `architecture/PORTING_GUIDE.md`; machine-checkable gates in `architecture/CONFORMANCE_SPEC.md`.
- **Precedence:** Source text (the book) > `corpus/` (L3) > `ontology/` > `knowledge/` > compiled
  adapter output. When two layers disagree, the nearer to the source wins and an issue is filed.
- **Machine encodings:** `ontology/concept_graph.schema.json` and `issues/SCHEMA.md` encode these
  structures; this document defines their semantics. `@governing` identifiers are defined in §10.

## 1. Source Identity and the Design Drivers It Imposes

| Property | Value | Architectural consequence |
| :--- | :--- | :--- |
| Work | *Principles of Program Analysis*, F. Nielson, H. R. Nielson, C. Hankin; Springer 1999, corrected 2nd printing 2005 | Single-source corpus; every claim is attributable to one coordinate system |
| Extent | 465 PDF pages, 452 numbered book pages, roman-numbered front matter; some numbered pages have no PDF page | PDF-to-book page offset is not constant; citations resolve only through `corpus/pdf_page_map.json` |
| Body | 6 chapters, 3 appendices (A posets, B induction/coinduction, C graphs/regular expressions), Index of Notation, Index, Bibliography | 7 extraction units (`U0`-`U6`, §8) read in 11 slices; appendices are prerequisites, not afterthoughts |
| Numbered tables | 51 (Ch1: 6, Ch2: 10, Ch3: 10, Ch4: 0, Ch5: 18, Ch6: 6, App C: 1) | Closed inventory; conservation is countable |
| Numbered figures | 56 (Ch1: 3, Ch2: 23, Ch3: 6, Ch4: 10, Ch5: 2, Ch6: 6, App A: 3, App C: 3) | Closed inventory; conservation is countable |
| Text layer | Scanned and character-recognised; formulae, subscripts, Greek letters, and some displayed programs are corrupted or absent | Symbol-level claims cannot be trusted from the text layer alone (see §7.4) |

Four statements in the Preface and Chapter 1 fix the shape of the whole design:

1. **Four approaches, one subject.** The book treats Data Flow Analysis, Constraint Based Analysis,
   Abstract Interpretation, and Type and Effect Systems in order to expose the similarities between
   them (Preface, pp. V-VI). The architecture therefore models *concepts* and *edges between concepts*
   as first-class objects; a per-chapter document tree alone would lose the thesis.
2. **One analysis, many formulations.** Chapter 1 specifies Reaching Definitions as equations (§1.3.1),
   as constraints (§1.3.2), as an analysis induced from a collecting semantics (§1.5), and as two
   annotated type systems (§1.6.1), then solves it by chaotic iteration (§1.7) and consumes it in a
   transformation (§1.8): one node with several projections. §5 generalises this.
3. **Safe approximation, semantics based.** Analyses err on the safe side (§1.1, Figure 1.1) and are
   justified against a semantics without being structured by it (§1.1, p. 3). Every procedural
   artifact must therefore carry the correctness precondition of the technique it operationalises.
4. **Declared reading dependencies.** The Preface states which sections are basic, which can be
   omitted on a first reading, and which appendices each chapter relies on (pp. VI-VIII). These
   become `depends_on` edges and determine extraction order (appendices and notation first).

## 2. System Overview: Canonical Core and Compiled Targets

```
ppa.pdf --(deterministic page map)--> corpus/pdf_page_map.json
corpus/shards/RAW_SHARD_*.md --merge--> corpus/RAW_KNOWLEDGE.md        L3  ground truth (text)
   |                                         |
   v                                         v
ontology/concept_graph.json  <------- ontology/notation_index.md       L3  ground truth (graph)
   |--> knowledge/skills/*/references/*.md                             L1  comparative reference
   |--> knowledge/skills/*/SKILL.md + evals/cases.yaml                 L2  procedure
   |--> knowledge/ambient-context/ppa-*.md                             L0  orientation
   |--> knowledge/skills/ppa-program-analysis/SKILL.md                 L0  master router
   v
adapters/*  --compile-->  target harness layouts (never edited by hand)
```

- **R-CORE-1 (dependency direction).** `adapters/` depends on `knowledge/` and `ontology/`. Nothing in
  `knowledge/`, `ontology/`, or `corpus/` may reference an adapter, a harness, or a harness path.
- **R-CORE-2 (single source of truth).** A formal statement has exactly one home: its L3 entry. Higher
  altitudes hold a budgeted restatement plus a citation, never an independent second original.
- **R-CORE-3 (generated output is not an edit target).** A defect found in compiled harness output is
  fixed in the canonical core or the adapter and recompiled.
- **R-CORE-4 (determinism).** Compilation is a pure function of the canonical core: same input bytes,
  same output bytes, stable ordering, no timestamps in content.

## 3. The 4-Altitude Concept Model (`L0`-`L3`)

Altitude measures *how much of a concept a reader needs to act correctly at a given moment*, not its
importance. Every concept has an `L3` entry (`R-CORE-2`). The node field `altitude` is the **highest
altitude at which the concept is surfaced with content** (`L0` above `L1` above `L2` above `L3`; `L3`
when it is surfaced nowhere above the corpus). A link or a mention by name is not content.

### 3.1 Altitude Table

| Altitude | Artifact | Question it answers | Budget | Frontmatter | Loaded when |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `L0` router | `knowledge/skills/ppa-program-analysis/SKILL.md` | Which approach and which skill fits this task? | `50-99` lines | Required | Task matches the router description |
| `L0` ambient | `knowledge/ambient-context/ppa-*.md` | What is the mental model and vocabulary of this area? | `80-250` lines | Per `PORTING_GUIDE.md` | Harness semantic match |
| `L1` reference | `knowledge/skills/ppa-*/references/*.md` | What exactly is defined, under which side conditions, and how do the approaches compare? | `<= 450` lines | None | An `L2` step or the router links to it |
| `L2` skill | `knowledge/skills/ppa-*/SKILL.md` + `evals/cases.yaml` | What do I do, in what order, and how do I check the result? | `250-450` lines target, `< 500` hard ceiling | Required | Task matches the skill description |
| `L3` corpus | `corpus/RAW_KNOWLEDGE.md`, `corpus/shards/RAW_SHARD_*.md` | What does the source state, verbatim in structure, at this coordinate? | Unconstrained | Forbidden (0 YAML frontmatter) | Targeted lookup by anchor only |
| `L3` graph | `ontology/concept_graph.json`, `ontology/notation_index.md` | What is this concept, where is it, and what is it related to? | Unconstrained | Forbidden | Query by `id`, edge, or citation |

### 3.2 Cognitive Purpose and Content Contract

| Altitude | MUST contain | MUST NOT contain |
| :--- | :--- | :--- |
| `L0` router | Decision table from task shape to skill; one-line discriminator per skill; negative routes ("not this skill when ...") | Definitions, derivations, procedures, tables of formal rules |
| `L0` ambient | The approach's central question, its vocabulary, its soundness direction, its relation to the other approaches, pointers to `L1`/`L2` | Step-by-step procedures; complete rule systems; proofs |
| `L1` reference | Definitions with every side condition; rule systems; comparison matrices; complexity bounds with their parameters; citation per item | Task workflows; tool invocations; unstated paraphrase of a theorem |
| `L2` skill | Trigger and negative boundary; numbered procedure; precondition checks; verification step; failure modes; links to `L1` | Proofs; full inference-rule tables; content duplicated from a sibling skill |
| `L3` corpus | Every section, table, figure, definition, lemma, theorem, example, exercise, mini project, and bibliographic remark with `(book_page, pdf_page)` | Summarisation that drops a condition; harness metadata; frontmatter |
| `L3` graph | One node per concept with citations, formal summary, four projections, typed edges, artifact references | Free prose that is not attached to a node |

### 3.3 Boundary Rules

- **B1 (placement test).** Every statement of the source that must survive unaltered (definition, rule,
  theorem, table, algorithm, counterexample) has its `L3` entry unconditionally. The node's `altitude`
  is then the first of these that holds, tested in this order:
  1. `L0`: the router or an ambient file states it, to *recognise that the area is relevant* or to route.
  2. `L1`: a reference states it, to *choose between* techniques or to *state a result correctly*.
  3. `L2`: a skill states it as a step a practitioner *performs* or a check a practitioner *runs*.
  4. `L3`: none of the above; the concept lives in the corpus and graph only.
- **B2 (downward links only).** `L0` links to `L1`; `L2` links to `L1`; `L1` cites `L3`. No artifact links
  upward and no skill file links into another skill's `SKILL.md`: the router names its sibling skills
  by their `name`. A skill MAY link into another skill's `references/` (the package installs whole, §4.3).
- **B3 (precondition carry).** When an `L2` procedure relies on a result, the side conditions of that
  result travel with the step as an explicit check (for example: the Ascending Chain Condition holds,
  or a widening operator is supplied, before termination is claimed). Derivations stay at `L1`/`L3`.
- **B4 (pointer, not copy).** A higher altitude MAY restate a formal item only in a form that is
  checkable against the `L3` entry: same quantifiers, same order direction, same parameters.
- **B5 (budget is a design signal).** Exceeding a budget is resolved by refactoring (§6), never by
  deletion, abbreviation of conditions, or relaxing the budget.
- **B6 (one home, many mentions).** A concept defined in two references is a defect; the second
  occurrence is replaced by a link and a `REF-*` issue records the merge.
- **B7 (frontmatter hygiene).** `SKILL.md` frontmatter holds only portable discovery metadata (a name
  and a description). `L1` and `L3` files carry none. Provenance comments are HTML comments, not YAML.
- **B8 (evals are portable).** `evals/cases.yaml` describes prompts, expected routing, and required or
  forbidden content as data. It names no model, harness, or tool.
- **B9 (budget unit and rationale).** Budgets count physical lines of the whole file, frontmatter
  included. The ceilings keep one loaded artifact within a single unpaged read and the worst realistic
  co-load (router, one skill, two references, one ambient file) under roughly 1,750 lines. The floors
  (50 router, 250 skill, 80 ambient) reject stubs that have smoothed away the preconditions for acting.

## 4. Retrieval Physics Across Agent Harnesses

### 4.1 The Four Retrieval Channels

| Channel | What is loaded | Who decides | Standing cost per session | Canonical source |
| :--- | :--- | :--- | :--- | :--- |
| `R0` always-on | Global or project instruction files injected into every turn | Nobody; unconditional | Full byte size, every turn, every task | **None. 0 bytes.** |
| `R1` ambient semantic | A short orientation file matched to the conversation | Harness retrieval | Zero until matched | `L0` ambient |
| `R2` progressive disclosure | Skill description (index), then body, then linked references | Model, by description match | Description only (tens of tokens per skill) | `L0` router, `L2`, `L1` |
| `R3` deep formal lookup | A slice of the corpus or a graph neighbourhood | Model, by explicit anchor or query | Zero until requested | `L3` |

### 4.2 Why `R0` Receives Zero Bytes

1. **Cost is unconditional.** Always-on text is paid on every turn of every task, including the
   majority that have nothing to do with program analysis.
2. **Attention is finite.** Irrelevant instructions dilute relevant ones, and specialist vocabulary in
   a global prompt biases unrelated reasoning.
3. **It is the least portable surface.** Every harness names and scopes it differently and operators
   own its contents; a package that writes there cannot be uninstalled cleanly.
4. **It is unnecessary.** Discovery is served by `R2` descriptions and `R1` matching; the only standing
   footprint of the package is the set of skill descriptions.

Consequence: an adapter MUST NOT create, append to, or modify any always-on instruction surface.
Where a target has no on-demand discovery mechanism, the adapter installs files in a scoped location
and documents an operator-applied pointer: a declared deviation under gate `C2`, never a default.

### 4.3 Composition Without Saturation or Smoothing

A task traverses channels in a fixed order, loading the minimum at each stage:

```
conversation -> [R1] ambient file (orientation, <=250 lines)
             -> [R2] router description -> router body (<100 lines) -> one L2 skill (<500 lines)
             -> [R2] the L1 reference named by the current step (<=450 lines)
             -> [R3] the L3 entry named by the citation in that reference (one anchor, not the file)
```

- **Saturation** is prevented structurally: each stage has a ceiling, each link names one target, and
  `L3` is never read whole. A skill that instructs "read all references" violates this section.
- **Information smoothing** is the loss of conditions, direction, and exceptions under compression.
  No higher altitude *replaces* a lower one: `L2` says when to descend, `L1` states the item with its
  conditions, `L3` holds the original. Compression happens once, at authoring time, under review (§7).
- **Channel independence and atomic installation.** The package installs as a whole: all skills, their
  references, and the ambient files. Within an installed package each artifact MUST be usable when it
  is the only thing loaded: a skill may not assume the ambient file was retrieved, nor the reverse.

### 4.4 Harness Mapping (Informative; Normative Detail in `PORTING_GUIDE.md`)

| Target (public convention) | `R1` ambient | `R2` skills and references | `R3` lookup | `R0` surface left untouched |
| :--- | :--- | :--- | :--- | :--- |
| Claude Code (`.claude/`) | Router-linked reference, or native mechanism if present | `.claude/skills/<name>/SKILL.md` with `references/` | File read by anchor | `CLAUDE.md` |
| Gemini CLI (`~/.gemini/`) | Native on-demand context if present, else router-linked | Skill directory with `SKILL.md` and `references/` | File read by anchor | `GEMINI.md` |
| Codex / `AGENTS.md` convention | Scoped file inside the installed package directory | Skill directory or scoped documents | File read by anchor | Root `AGENTS.md` |
| Cursor (`.cursor/rules/`) | `.mdc` rule with a description and `alwaysApply: false` | `.mdc` rules, description-triggered | File read by anchor | Any rule with `alwaysApply: true` |
| Knowledge wiki, MCP server, or Graph-RAG | Page or resource listing with descriptions | Page, prompt, or resource per skill | Graph query tool over `concept_graph.json` | Server-injected system text; vault-wide templates |

**Degradation rule.** If a target lacks a channel, content moves to the next *more explicit* channel
(`R1` content becomes an `R2` reference linked from the router). It never moves toward `R0`.

## 5. Multi-Dimensional Domain Projections

### 5.1 Model

Every concept node carries one formal core and four projections. The keys match the graph schema.

| Key | Dimension | Content | Attribution |
| :--- | :--- | :--- | :--- |
| `formal_summary` | Formal core | What the source defines or proves, with conditions | Source, with citation |
| `projections.cs_theory` | (a) Formal CS theory and proof semantics | Order-theoretic object, proof principle, soundness direction, decidability and complexity | Source where stated; otherwise marked interpretive |
| `projections.swe_architecture` | (b) Software architecture and design patterns | The component, interface, or pattern the concept corresponds to in an analyser or compiler | Interpretive |
| `projections.practical_debugging` | (c) Practical coding, slicing, debugging, troubleshooting | What a practitioner does with it; the symptom produced when its precondition is violated | Interpretive |
| `projections.cyber` | (d) Cyber-security and vulnerability analysis | The detection or verification question it answers; the soundness or precision risk it introduces | Interpretive |

### 5.2 Projection Rules

- **P1 (completeness).** All four projections are present on every node. A projection with no honest
  content states `not applicable` with a one-clause reason; it is never omitted or padded.
- **P2 (attribution firewall).** Interpretive content MUST NOT be phrased as a claim of the source and
  MUST NOT carry a source citation. Terms the book does not use carry the literal tag `[external]`.
- **P3 (precondition inheritance).** A projection that recommends an action inherits every side
  condition of the formal core. If the projection cannot state the condition, it cannot recommend.
- **P4 (projection is not altitude).** Projections are orthogonal to `L0`-`L3` and feed whichever
  artifacts reference the node; the cross-book security skill is assembled from `projections.cyber`.
- **P5 (direction of safety).** Each projection states which way the approximation errs for that use:
  an over-approximating may-analysis yields false alarms when finding defects and guarantees when
  proving absence.

### 5.3 Anchor Examples

| Concept (source) | (a) `cs_theory` | (b) `swe_architecture` | (c) `practical_debugging` | (d) `cyber` |
| :--- | :--- | :--- | :--- | :--- |
| Monotone Framework instance (§2.3) | Complete lattice with Ascending Chain Condition, monotone transfer functions closed under composition | Strategy objects (lattice, transfer, flow, extremal value) plugged into a Template Method solver | Non-termination or oscillation means a transfer function is not monotone or chains are infinite | A taint or reachability rule set is an instance; a non-monotone rule silently invalidates the result |
| MFP versus MOP (§2.4) | MFP safely approximates MOP (Lemma 2.32); equality needs a distributive framework *and* `path∘(ℓ) ≠ ∅` for every label of `E` and `F`; MOP is undecidable for Constant Propagation (Lemma 2.31) | Join-at-merge is an architectural precision decision, not an implementation detail | Unexpected imprecision at merge points traces to non-distributivity | Merging loses path correlation; correlated sanitisation checks produce false alarms |
| Reaching Definitions and ud/du chains (§1.2, §2.1.2, §2.1.5) | Forward may-analysis, least solution | Def-use index service consumed by transformations | Backward slice from a wrong value to candidate assignments | Trace an unsafe value at a sink back to its defining assignments |
| 0-CFA acceptability (§3.1, §3.2) | Coinductively specified relation (§3.1); least solution exists by a Moore family argument (§3.2) | Call-graph construction separated into specification, constraint generation, solving | Resolve which functions an indirect call may reach | Indirect-call target sets bound which code a tainted value can enter |
| Call strings and assumption sets (§2.5), uniform k-CFA (§3.6) | Context as an extra lattice component; valid-path precision | Context is a cache key; `k` is a cost and precision dial | Spurious cross-call flows indicate insufficient context | Context-insensitive merging links unrelated callers; bounded context trades alarms for cost |
| Widening and narrowing (§4.2) | Upper-bound operator forcing stabilisation; narrowing recovers precision | Termination policy injected into the solver | A bound jumping to infinity indicates widening applied at the wrong point | Interval bounds for index and size checks; over-eager widening yields unprovable bounds |
| Galois connection and induced analysis (§1.5, §4.3, §4.5) | Adjoint pair; best abstract transformer along abstraction and concretisation | Adapter with a law between concrete and abstract domains; products as Composite | A missed fact traces to the abstraction, the transformer, or the combination | A domain is a claim about which facts are tracked; relational facts need relational combination |
| Effect systems (§1.6.2, §5.4-§5.5) | Annotated judgements; subeffecting and subtyping; conservative extension | Decorator over the underlying type system; effects as interface contracts | Read a function's latent effect instead of its body | Side effects, raised exceptions, allocation regions, and communication as auditable interface facts |
| Worklist over constraint systems (§6.1-§6.3) | Least solution of inequations; bound depends on height and constraint counts | Worklist as abstract data type; iteration order as Strategy | Slow convergence is an ordering problem before it is a lattice problem | Solver ordering decides whether whole-program analysis completes within budget |

## 6. Progressive Per-Chapter and Whole-Book Altitude Refactoring Protocol

Refactoring runs after each extraction unit, at each part boundary, and over the whole book. Each
pass is logged in `ontology/altitude_alignment_log.md`; each structural change is a `REF-*` issue.

### 6.1 Triggers

| ID | Trigger (detectable condition) | Required action |
| :--- | :--- | :--- |
| `T1` overflow | A reference exceeds 450 lines, or a skill file reaches 450 lines (warning) or 500 (failure) | **Fracture** per §6.2 |
| `T2` promotion | A concept is cited from two or more units, or linked from two or more skills | Move its definition to a shared reference; replace other copies with links; raise `altitude` only if it has become a routing discriminator |
| `T3` demotion | Proof steps, full rule tables, or derivations appear in `L0` or `L2` | Move to `L1` (statement) and `L3` (derivation); leave a link and the precondition check |
| `T4` isomorphism | The source states that two constructs coincide, embed, or specialise one another across chapters | **Unify** per §6.3 |
| `T5` trigger collision | Two skill descriptions match the same evaluation prompt, or a negative boundary is missing | Rewrite both descriptions with mutually exclusive discriminators; add the prompt to both `evals/cases.yaml` |
| `T6` contradiction or edge case | The source and a derived artifact, two source passages, or the source and practice disagree | **Isolate** per §6.4 |
| `T7` notation collision | One symbol has different meanings in different units, or one meaning has several spellings | Scope-qualify both entries in `ontology/notation_index.md`; never normalise the source spelling at `L3` |
| `T8` orphan | A graph node has no artifact reference, or an artifact section maps to no node | Attach, or record an explicit exclusion with reason |
| `T9` stub | An ambient file under 80 lines, a skill under 250 lines, or a router under 50 lines | Merge into a sibling or expand from `L3`; do not pad |

### 6.2 Fracturing an Overloaded Reference

1. Compute the set of concept nodes whose `artifact_refs` point into the file.
2. Partition that set along the cut with the fewest crossing edges in the concept graph, preferring
   the source's own section boundaries.
3. Each part becomes a reference with its own scope line; shared prerequisites move to the part cited
   first and are linked from the other. Update every inbound link and `artifact_refs` entry with it.
4. Forbidden resolutions: truncating a table, dropping side conditions, deleting examples that carry
   a counterexample, raising the ceiling.

### 6.3 Unifying Cross-Chapter Isomorphisms

Unification adds a typed edge and one shared `L1` section. It does **not** merge nodes: each chapter's
construct keeps its own signature, notation, and citations, because the correspondence usually holds
only under stated conditions.

| Edge | From | To | Stated basis in the source |
| :--- | :--- | :--- | :--- |
| `U1` | Equational data flow system (§1.3.1) | Constraint system with inclusions (§1.3.2) | Same least solution; inclusions admit more solutions |
| `U2` | Monotone Framework instance, MFP algorithm (§2.3-§2.4, Table 2.8) | Abstract worklist over inequations (§6.1, Table 6.1) | Chapter 6 generalises the Chapter 2 solver |
| `U3` | Constraint-based 0-CFA and its graph solver (§3.4, Table 3.7) | Abstract worklist (§6.1) | Same technique; cubic bound recovered as a special case |
| `U4` | Monotone Frameworks (§2.3) | Control flow analysis with data flow components (§3.5) | Preface: §3.5 incorporates §2.3 |
| `U5` | Call strings and assumption sets (§2.5) | Uniform k-CFA and the Cartesian Product Algorithm (§3.6) | Preface: §3.6 adds context in the manner of §2.5 |
| `U6` | Galois connections and induced operations (§4.3-§4.5) | Transfer functions of data flow analyses (§4.5.2) and the Chapter 1 induced analysis (§1.5) | Analyses are calculated from a collecting semantics |
| `U7` | Widening (§4.2) | Ascending Chain Condition (§2.3, App A.3) | Widening supplies termination where chains are unbounded |
| `U8` | Annotated type and effect systems (§5.1) | Constraint-based control flow analysis (Ch 3) | Preface: §5.1 links back to Chapter 3; subsumption plays the role of inclusion (§1.6.1) |
| `U9` | Least and greatest fixed points, Tarski (App A.4) | Induction and coinduction (App B); acceptability of analyses (§3.1) | Appendix B builds on Appendix A.4 |
| `U10` | Depth-first spanning forests, reverse postorder, strong components (App C) | Reverse-postorder and strong-component iteration (§6.2-§6.3) | Chapter 6 orders constraints using Appendix C |

Rules: every `U*` edge MUST cite the passage stating the correspondence. In the graph the edge uses
relation `corresponds_to` and carries a `basis` object (`unification_id`, `citations`, `conditions`,
`differs`), citing Preface passages as `[PPA Preface, p. VII]` (CONFORMANCE_SPEC `N8`). The shared `L1`
section MUST state the conditions under which the correspondence holds and at least one difference.
An "analogy" with no stated basis in the source is recorded as an interpretive projection, not an edge.

### 6.4 Isolating Contradictions and Edge Cases

- A contradiction or edge case becomes one `issues/backlog/BKL-*.md` item with citations for every
  side, a mechanism, and the affected concept ids. It is typed `contradiction` when two citable
  statements cannot both hold as written (source against source, including probable misprints, or
  source against a derived artifact), and `edge_case` when the source holds under an assumption that
  another unit or practice violates. Practice-side statements carry `[external]`, not a source citation.
- It is **non-blocking**: the unit proceeds, and the affected artifact carries a one-line pointer to it.
- Resolution never rewrites `L3`: `L3` records the source as found, the item records the reading
  adopted above `L3`, and it closes only with a cited resolution or "accepted as documented tension".

### 6.5 Invariants Checked After Every Pass

`I1` no concept, citation, table, figure, or gotcha count decreases; `I2` every link and anchor
resolves; `I3` all budgets hold; `I4` every moved item keeps its citation; `I5` the alignment log
records what moved, from where, to where, and under which trigger; `I6` the whole-book pass
re-evaluates every `T2` and `T4` candidate across all units.

## 7. The Five Anti-Degradation Contracts

Each contract has a definition, a deterministic detection rule (Tier A, scriptable) and an adversarial
detection rule (Tier B, independent reviewer with a cited finding). Tier A is necessary, not sufficient.
A Tier A rule is in force only where the inventory or field it reads exists; until then the check is
Tier B and is reported as not implemented, never as passed.

### 7.1 `SMOOTHING_TRAP`

- **Definition.** A derived artifact restates a formal result while dropping or weakening a side
  condition, quantifier, scope restriction, or direction that the source states.
- **Canonical instances.** Stating that the MFP and MOP solutions coincide without both conditions of
  Lemma 2.32 (a distributive framework, and `path∘(ℓ) ≠ ∅` for every label of `E` and `F`); stating
  that iteration terminates without the Ascending Chain Condition or a widening operator; describing
  an answer as "the values" where the source insists on "among the values".
- **Tier A.** Each node lists its side conditions as discrete `conditions` entries; every artifact
  section in `artifact_refs` links to the node's `L1` anchor, and that anchor carries a conditions
  list with as many entries. Whether each entry preserves the source's wording is Tier B.
- **Tier B.** Reviewer reads the `L3` entry and the restatement side by side and names the lost clause.

### 7.2 `SIGNATURE_DISTORTION`

- **Definition.** A named formal object is reproduced with a different signature: arity, component
  order, domain or codomain, order direction, may versus must, forward versus backward, least versus
  greatest, operand order, or a numeric bound and its parameters.
- **Canonical instances.** Reversing the order relation in a correctness statement; swapping the
  operands of a non-commutative operator; quoting an iteration bound without its lemma's assumptions
  or parameters. Lemma 6.12 bounds the Round Robin Algorithm by `d(G_S, T) + 3` iterations only for
  instances of a Bit Vector Framework iterated in the reverse postorder of a depth-first spanning
  forest `T`: one initial pass, `d + 1` propagating passes, and one pass that detects stability.
- **Tier A.** Every signature and numeric bound above `L3` is compared with the entry in
  `ontology/notation_index.md` or the cited `L3` anchor; literal mismatch fails.
- **Tier B.** Reviewer re-derives direction and parameter meaning from the rendered page image.

### 7.3 `SILENT_GOTCHA_TRUNCATION`

- **Definition.** A restriction, counterexample, failed first attempt, "does not hold in general"
  remark, or simplifying assumption present in a source unit is absent from every derived altitude
  and has no recorded exclusion.
- **Canonical instances.** The distinct-label assumption (§1.2); the unsuccessful first reading of the
  annotated-type judgement (§1.6.1); the remark that the transformation relation is neither reflexive
  nor transitive (§1.8); material the Preface declares out of scope.
- **Tier A.** Each `L3` shard ends with a gotcha ledger (id, citation); every id needs a derived
  artifact, backlog item, or exclusion: warning until the whole-book audit, failure from then on.
- **Tier B.** Reviewer samples source pages and searches for unledgered restrictions.

### 7.4 `HALLUCINATED_SYMBOL`

- **Definition.** A symbol, term, numbered item, or bibliography key is attributed to the source but
  does not occur at the cited coordinate. This includes artefacts of character recognition promoted
  to notation, and external terminology presented as the book's.
- **Canonical instances.** Citing a table number outside the closed inventory of 51; transcribing a
  misrecognised glyph as a distinct symbol; attributing to the book a topic that the Preface lists as
  omitted, such as single static assignment form.
- **Tier A.** Tables, figures, sections, bibliography keys, and numbered statements (lemmas, theorems,
  propositions, corollaries, facts, examples, exercises, mini projects) are checked against the
  inventories (including `statements`) in `corpus/pdf_page_map.json`; symbols against
  `ontology/notation_index.md`.
- **Tier B.** Any symbol-level claim extracted from a page with displayed mathematics is confirmed
  against the rendered page image before it is admitted to `L3`.

### 7.5 `PROVENANCE_DISCONNECTION`

- **Definition.** A claim cannot be followed through an unbroken chain (artifact section, concept `id`,
  citation, `L3` anchor, source page), or a change cannot be followed from artifact to issue to verdict.
- **Canonical instances.** A reference paragraph with no citation; a citation whose PDF page does not
  map to its book page; a graph node with no artifact; a refactor with no `REF-*` issue.
- **Tier A.** Resolve every link, anchor, citation, `artifact_refs` entry, and issue reference; any
  unresolved hop fails.
- **Tier B.** Reviewer picks claims at random and walks the chain to the page.

### 7.6 Enforcement Summary

| Contract | Primary altitude at risk | Conformance gate | Blocking |
| :--- | :--- | :--- | :--- |
| `SMOOTHING_TRAP` | `L1`, `L2` | `C1`, review | Yes, with cited lost clause |
| `SIGNATURE_DISTORTION` | `L1`, `L2`, graph | `C1`, review | Yes, with cited signature |
| `SILENT_GOTCHA_TRUNCATION` | `L2`, `L0` | `C1`, `C6` | Yes, with ledger id |
| `HALLUCINATED_SYMBOL` | all | `C1`, `C5` | Yes, with missing coordinate |
| `PROVENANCE_DISCONNECTION` | all | `C3`, `C6` | Yes, with broken hop |

A finding blocks only when it names a verifiable location and a concrete mechanism; otherwise it is a
preference and does not hold the unit.

## 8. Canonical Inventory and Ownership

| Unit | Source span | `L0` ambient | Skill | Notes |
| :--- | :--- | :--- | :--- | :--- |
| U0 | Appendices A-C, Index of Notation | (feeds all) | (feeds all) | Extracted first; seeds `notation_index.md` and prerequisite edges |
| U1 | Chapter 1 | `ppa-foundations.md` | `ppa-program-analysis` (`L0` router, no `L2` procedure) | Establishes the cross-approach backbone |
| U2 | Chapter 2 | `ppa-dataflow-and-shape.md` | `ppa-dataflow-and-slicing` | Intraprocedural, interprocedural, shape |
| U3 | Chapter 3 | `ppa-cfa-and-constraints.md` | `ppa-control-flow-and-constraints` | 0-CFA to context-sensitive variants |
| U4 | Chapter 4 | `ppa-abstract-interpretation.md` | `ppa-abstract-interpretation` | Language-independent by design of the source |
| U5 | Chapter 5 | `ppa-types-effects-and-regions.md` | `ppa-types-effects-and-regions` | Control flow, side effects, exceptions, regions, communication |
| U6 | Chapter 6, Index, Bibliography | `ppa-fixedpoint-solvers.md` | `ppa-fixedpoint-solvers` | Solver architecture for U2 and U3 |
| X | All units | `ppa-cyber-analysis.md` | `ppa-cyber-vulnerability-analysis` | Assembled from `projections.cyber`; owns no formal core |

Each skill owns its `references/` directory. A reference needed by two skills lives with the skill whose
unit introduces the concept (rule `B6`, trigger `T2`); references used by every skill live with the router.

## 9. Change Control

- Changes to this document require an entry in the Decision Log of `MASTER_PLAN.md` and a `REF-*`
  issue naming the affected rules by identifier (`R-CORE-*`, `B*`, `P*`, `T*`, `U*`, `I*`).
- Budgets, altitude definitions, the zero-byte `R0` rule, and the five contracts are invariants of
  `DEC-PPA-001`; altering one is a new decision. Rule identifiers are stable; retired rules keep theirs.

## 10. Requirement Identifiers

`REQ-TECH-PPA-00N` has the parent `REQ-PRD-PPA-00N`. A `@governing` header resolves to one row here.

| N | Product requirement `REQ-PRD-PPA-00N` | Technical requirement `REQ-TECH-PPA-00N` | Verified by |
| :--- | :--- | :--- | :--- |
| 001 | All intelligence of the book is available as attributed, cross-referenced knowledge objects at the right level of detail | Four-altitude canonical core, `(book_page, pdf_page)` citation system, concept graph with four projections, deterministic tooling | §3, §5; `C1`, `C3` |
| 002 | The knowledge base is assessed and refactored for altitude alignment after every chapter | Per-unit refactoring pass with triggers `T1`-`T9` and invariants `I1`-`I5`, recorded in the alignment log | §6.1-§6.5; `C6.9` |
| 003 | A full-book audit and global altitude refactoring closes the work | Whole-book pass (`I6`), cross-chapter unification edges, closed inventories, issue export manifest | §6.3, §6.5; `C1.4`-`C1.6`, `C6.4` |
| 004 | Contradictions and edge cases are captured as non-blocking backlog items | Cited, typed backlog items linked to concept ids; `L3` records the source as found | §6.4; `C6.6`-`C6.8` |
| 005 | Each chapter, each part, and the whole book pass adversarial evaluation by three independent models | Five anti-degradation contracts with Tier A and Tier B detection; authors never judge their own output; blocking findings need a location and a mechanism | §7; alignment records in `issues/` |
| 006 | Outputs carry no vendor or host identifiers and are portable to other harnesses, with porting documentation and adapters | Zero-byte always-on rule, harness-agnostic core, deterministic adapters, conformance gates `C1`-`C6` | §4; `C2`, `C5`; `CONFORMANCE_SPEC.md` |
