<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Vendor-neutral 4-altitude semantic knowledge package with lossless GitHub-issue Markdown tracking, deterministic stdlib validators, cross-harness reference adapters, and 12-gate (Gate #0 + Gates #1-#11) 3-model adversarial verification. -->

# MASTER_PLAN: Principles of Program Analysis Semantic Knowledge & Portable Harness Suite

## Identity

- **Project:** `ppa-semantic-knowledge`
- **Type:** Multi-Altitude Knowledge Extraction, Formal Ontology & Portable Agent Harness Suite
- **Workspace / Root:** `.` (branch `feat/ppa-semantic-knowledge`)
- **Languages:** Markdown (75%), Python 3 Standard Library (20%), JSON / YAML (5%)
- **Issue Tracking:** Repository-local `issues/` Markdown suite (`EPIC-*`, `ISS-*`, `REF-*`, `BKL-*`) with lossless GitHub Issues export (`issues/export_manifest.json`)
- **Created:** 2026-11-18
- **Last updated:** 2026-11-19

Extracts, enriches, cross-references, and adversarially verifies all formal and practical intelligence from *Principles of Program Analysis* (Flemming Nielson, Hanne Riis Nielson, Chris Hankin; Springer, 1999 / Corrected 2nd Printing, 2005; `ppa.pdf`, 465 PDF pages / 452 book pages) into a conformantly portable, vendor-neutral 4-altitude (`L0`–`L3`) semantic knowledge architecture with target harness adapters.

## Architecture

- `architecture/` — Normative 4-altitude specification (`ARCHITECTURE.md`), cross-harness porting blueprints (`PORTING_GUIDE.md`), model-family tuning guide (`MODEL_ADAPTATION_GUIDE.md`), and conformance contracts (`CONFORMANCE_SPEC.md`).
- `corpus/` — Deterministic PDF coordinate index (`pdf_page_map.json`), per-unit unconstrained raw extractions (`shards/RAW_SHARD_00..06.md`), and merged ground-truth corpus (`RAW_KNOWLEDGE.md`).
- `ontology/` — Machine-validated L0–L3 concept graph (`concept_graph.json`, `concept_graph.schema.json`), mathematical notation index (`notation_index.md`), cross-paradigm equivalence matrix (`cross_paradigm_matrix.md`), and iterative multi-agent altitude refactoring log (`altitude_alignment_log.md`).
- `knowledge/` — Vendor-neutral semantic artifacts: `ambient-context/ppa-*.md` (`L0` ambient orientation, `80`–`250` lines, per `architecture/ARCHITECTURE.md` §3.1) and `skills/ppa-*/` (`L0` router + 6 `L2` actionable skills `<500L` + `L1` `references/*.md` `<=450L` + portable `evals/cases.yaml`).
- `issues/` — Lossless GitHub-Issue Markdown tracker (`SCHEMA.md`, `epics/`, `shards/`, `refactors/`, `backlog/`, `export_manifest.json`).
- `adapters/` — Deterministic Python 3 stdlib compilers/installers for target harnesses (Claude Code, Gemini CLI, `AGENTS.md` / Codex, Cursor `.mdc`, and Knowledge Wiki / MCP / Graph-RAG).
- `scripts/` — PDF structure indexer, `flock`-guarded issue controller, zero-internal-identifier hygiene gate, Tier-A knowledge validator, and post-port conformance verifier.
- `tests/` — Hermetic unit and integration test suites using real fixtures.

## Original Intent

> Create a set of semantic knowledge that can be integrated into a harness configuration based on the book *Principles of Program Analysis* (`ppa.pdf`). Extract all intelligence from this book into the best representative knowledge types/objects (`L0`–`L3` referential context, ontology, and actionable skills) with exact attribution and cross-referencing.
> 1. Exhaustively analyze every chapter and appendix with derived knowledge produced.
> 2. Assess, evaluate, and refactor the growing knowledge base after every chapter for topic/concept-altitude modeling alignment.
> 3. Execute a full-book audit and global altitude refactoring upon completion.
> 4. Capture contradictions and edge cases as non-blocking backlog items (`issues/backlog/`).
> 5. Enforce a 3-model adversarial evaluation loop to alignment per chapter, per part, and across the whole book, while keeping all outputs free of vendor/internal identifiers and accompanied by exhaustive cross-harness porting documentation and reference adapters.

## Principles

1. **Zero Loss of Formal Fidelity** — Every section, numbered table (`51/51`), numbered figure (`56/56`), theorem, algorithm, mini-project, and exercise insight is anchored to exact `(book_page, pdf_page)` coordinates.
2. **Explicit Concept-Altitude Separation (`L0`–`L3`)** — Never pollute always-on prompts (`0` bytes added to global system rules) and never smooth formal invariants out of `L2`/`L3` leaves.
3. **Physical Adversarial Separation** — Author instances never evaluate their own outputs; a dedicated 3-model read-only judge panel audits every unit, part, and whole-book milestone under a Two-Key Epistemic Gate.
4. **Vendor-Neutral Portability & Hygiene** — Zero proprietary/internal paths, hostnames, or identifiers in tracked files; every target harness layout is compiled deterministically from `knowledge/` + `ontology/`.
5. **Nothing Done Until Empirically Proven** — Every shard passes hermetic stdlib Python tests, Tier-A validators, and 3-model alignment gates before closure.

---

## Requirements

| ID | Statement | Parent | Verifying Gate |
| :--- | :--- | :--- | :--- |
| `REQ-PRD-PPA-001` | Extract all intelligence of *Principles of Program Analysis* as attributed, cross-referenced `L0`–`L3` knowledge objects | Original Intent #1 | Gates #1–#10 (`ISS-W1-01`..`ISS-W6-02`) |
| `REQ-PRD-PPA-002` | Assess, evaluate, and refactor the knowledge base for altitude alignment after every chapter | Original Intent #2 | Gates #2–#10 + `ontology/altitude_alignment_log.md` |
| `REQ-PRD-PPA-003` | Execute a full-book audit and global altitude refactoring upon completion | Original Intent #3 | `ISS-W8-01`, Gate #11 (`ISS-W8-02`) |
| `REQ-PRD-PPA-004` | Capture contradictions and edge cases as non-blocking backlog items (`issues/backlog/`) | Original Intent #4 | `C6.6`–`C6.8` + `scripts/issue_ctl.py validate` |
| `REQ-PRD-PPA-005` | Enforce a 3-model adversarial evaluation loop across foundation, chapter, part, and whole-book gates | Original Intent #5 | Gate #0 + Gates #1–#11 |
| `REQ-PRD-PPA-006` | Keep outputs free of vendor/host identifiers and provide cross-harness porting specs, reference adapters, and conformance verification | Original Intent #5 | `C1`–`C6` (`CONFORMANCE_SPEC.md`) + `ISS-W7-01` |
| `REQ-TECH-PPA-001` | Four-altitude canonical core, dynamic `(book_page, pdf_page)` coordinate map, 4-projection concept graph, and deterministic stdlib validators | `REQ-PRD-PPA-001` | `scripts/validate_ppa_knowledge.py`, `tests/test_wave0_foundation.py` |
| `REQ-TECH-PPA-002` | Per-unit refactoring pass with triggers `T1`–`T9`, invariants `I1`–`I5`, and `REF-*` issue provenance | `REQ-PRD-PPA-002` | `ontology/altitude_alignment_log.md`, `C6.9` |
| `REQ-TECH-PPA-003` | Whole-book pass (`I6`), `corresponds_to` unification edges (`U1`–`U10`), closed inventories (`C1.4`–`C1.6`), and topological GitHub export manifest | `REQ-PRD-PPA-003` | `scripts/issue_ctl.py export-github --dry-run`, `C1.4`–`C1.6`, `C6.4` |
| `REQ-TECH-PPA-004` | Cited, typed (`contradiction` / `edge_case`) backlog items linked to concept IDs with `[external]` firewall (`P2`) while keeping `L3` faithful | `REQ-PRD-PPA-004` | `scripts/issue_ctl.py validate`, `C6.6`–`C6.8` |
| `REQ-TECH-PPA-005` | Five anti-degradation contracts (`ARCHITECTURE.md` §7) with Tier-A scriptable checks and Tier-B physically separated 3-model review | `REQ-PRD-PPA-005` | `scripts/validate_ppa_knowledge.py`, issue alignment logs |
| `REQ-TECH-PPA-006` | Zero-byte `R0` always-on rule, fail-closed hygiene scanner, deterministic target adapters, and `C1`–`C6` conformance verifier | `REQ-PRD-PPA-006` | `scripts/check_portability_hygiene.py`, `scripts/verify_port_conformance.py` |

---

## Specification & Decision Log

| Date | DEC-ID | Init | Title | Rationale | Code Anchor | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-11-18 | `DEC-PPA-001` | `ppa-v1` | 4-Altitude Canonical Core (`L0`–`L3`) + Target Harness Compilers | Decouples lossless PPA intelligence from any single agent CLI layout while preserving `<500L` progressive disclosure | `architecture/ARCHITECTURE.md` | Active |
| 2026-11-18 | `DEC-PPA-002` | `ppa-v1` | Per-File Sharded Markdown Issue Tracker (`issues/`) | Enables race-free multi-agent updates and 1:1 lossless downstream GitHub Issues export via topological manifest | `scripts/issue_ctl.py` | Active |
| 2026-11-18 | `DEC-PPA-003` | `ppa-v1` | Fail-Closed Portability Sanitizer | Guarantees zero leakage of workstation paths or internal identifiers prior to external Git hosting | `scripts/check_portability_hygiene.py` | Active |
| 2026-11-18 | `DEC-PPA-004` | `ppa-v1` | Dynamic `(pdf_page, book_page)` Coordinate & Statement Map | Prevents citation drift across variable PDF offsets (`+20` down to `+13`), chapter end-matter boundaries, and numbered-statement spans | `scripts/extract_ppa_structure.py` | Active |
| 2026-11-18 | `DEC-PPA-005` | `ppa-v1` | Stdlib Tier-A Knowledge Validator | JSON-Schema subset + map-checked citations + `artifact_refs`/link/fragment resolution + schema-driven edge symmetry (`x-relation-inverses`) | `scripts/validate_ppa_knowledge.py` | Active |
| 2026-11-18 | `DEC-PPA-006` | `ppa-v1` | Hermetic Wave 0 Test Suite | Real scratch fixtures, independent front-matter inventories (List of Tables/Figures, TOC, end-matter) as oracles, no mocks | `tests/test_wave0_foundation.py` | Active |
| 2026-11-18 | `DEC-PPA-007` | `ppa-v1` | Shared Artifact-Shape Rules Module | Single implementation of `CONFORMANCE_SPEC.md` `N1`–`N3`, `N8` (`C1.10`–`C1.11`), `C1.9` shape & coverage, `C3.1`–`C3.6`, `C3.10`, `C3.12`, `C4.1`–`C4.2` | `scripts/ppa_artifact_rules.py` | Active |
| 2026-11-18 | `DEC-PPA-008` | `ppa-v1` | Shared Appendix Reference Ownership | Router-owned `knowledge/skills/ppa-program-analysis/references/` hosts all three shared foundation `L1` references (`appendix-a`, `appendix-b`, and `appendix-c`, with `appendix-c-graphs-dfsf-and-rpo.md` promoted at Gate #1 so Ch 2/3/5/6 skills link cleanly under `C3.8`/`C3.9`) | `knowledge/skills/ppa-program-analysis/references/` | Active |

---

## Active Initiatives

### Initiative: Exhaustive PPA Knowledge Extraction, 3-Model Enrichment & Portable Harness Suite (`INIT-2026-11-18-ppa-v1`)

- **Status:** active
- **Dominant Constraint:** reliability & maintainability
- **Requirements:** `REQ-PRD-PPA-001`..`006` / `REQ-TECH-PPA-001`..`006`

## Phase 0: Bootstrap, Issue Engine, Portability Sanitizer, PDF Indexer & Architecture Spec

**Status:** completed

- [x] **`W0-1` (`ISS-W0-01`)**: Branch bootstrap, `issues/SCHEMA.md`, `scripts/issue_ctl.py`, `scripts/check_portability_hygiene.py`, `tests/test_wave0_foundation.py`, and upfront `EPIC-001` + `ISS-W0-01`..`ISS-W8-02` issue files.
- [x] **`W0-2` (`ISS-W0-02`)**: Build `scripts/extract_ppa_structure.py`, `corpus/pdf_page_map.json`, `ontology/concept_graph.schema.json`, `scripts/validate_ppa_knowledge.py` (+ `scripts/ppa_artifact_rules.py`), and `tests/test_wave0_foundation.py`.
- [x] **`W0-3` (`ISS-W0-03`)**: Author `architecture/ARCHITECTURE.md`, `architecture/CONFORMANCE_SPEC.md`, and `ontology/altitude_alignment_log.md` with 3-model `L0`–`L3` altitude calibration.

## Phase 1: Part I Foundations — Appendices A–C, Notation & Chapter 1

**Status:** completed

- [x] **`W1-1` (`ISS-W1-01`)**: Unit 0 — Appendices A, B, C & Notation Index (`RAW_SHARD_00_appendices.md`, `ontology/notation_index.md`, `concept_graph.json` seed) + Gate #1 (3-Model Loop).
- [x] **`W1-2` (`ISS-W1-02`)**: Unit 1 — Chapter 1 Introduction (`RAW_SHARD_01_intro.md`, `ppa-program-analysis` Master Router, `ppa-foundations.md`) + Altitude Refactoring + Gate #2 (3-Model Loop).

## Phase 2: Part I Completion — Chapter 2 (Data Flow Analysis) & Part I Gate

**Status:** completed

- [x] **`W2-1` (`ISS-W2-01`)**: Ch 2a (§2.1–2.4) Intraprocedural DFA, SOS Soundness, Monotone Frameworks & MFP/MOP (`RAW_SHARD_02a_intraproc_dfa.md`).
- [x] **`W2-2` (`ISS-W2-02`)**: Ch 2b (§2.5) Interprocedural Context & Ch 2c (§2.6) Heap Shape Analysis (`RAW_SHARD_02b_interproc_shape.md`).
- [x] **`W2-3` (`ISS-W2-03`)**: Unit 2 Synthesis (`ppa-dataflow-and-slicing`, `ppa-dataflow-and-shape.md`), Cumulative KB Refactoring & Gate #3 (Ch 2 3-Model Loop).
- [x] **`W2-4` (`ISS-W2-04`)**: Part I Holistic Altitude Refactoring & Gate #4 (Part I 3-Model Loop).

## Phase 3: Part II — Chapter 3 (Constraint Based Analysis)

**Status:** completed

- [x] **`W3-1` (`ISS-W3-01`)**: Ch 3a (§3.1–3.4) 0-CFA Formulations, Coinduction & $O(n^3)$ Solver (`RAW_SHARD_03a_0cfa.md`).
- [x] **`W3-2` (`ISS-W3-02`)**: Ch 3b (§3.5–3.6) CFA+DFA Lattices, Uniform $k$-CFA, CPA, Synthesis (`ppa-control-flow-and-constraints`, `ppa-cfa-and-constraints.md`), Refactoring & Gate #5 (Ch 3 3-Model Loop).

## Phase 4: Part II — Chapter 4 (Abstract Interpretation)

**Status:** completed

- [x] **`W4-1` (`ISS-W4-01`)**: Ch 4a (§4.1–4.3) Correctness Relations, Widening/Narrowing & Galois Connections (`RAW_SHARD_04a_galois_widening.md`).
- [x] **`W4-2` (`ISS-W4-02`)**: Ch 4b (§4.4–4.5) Galois Combinators & Induced Operations, Synthesis (`ppa-abstract-interpretation`, `ppa-abstract-interpretation.md`), Refactoring & Gate #6 (Ch 4 3-Model Loop — CLOSED `3/3 [ALIGNED gate6-v2]`).

## Phase 5: Part II Completion — Chapter 5 (Type and Effect Systems) & Part II Gate

**Status:** completed

- [x] **`W5-1` (`ISS-W5-01`)**: Ch 5a (§5.1–5.3) Annotated CFA Types, Natural Semantics & $\mathcal{W}_{\text{UL}}/\mathcal{W}_{\text{CFA}}$ Inference (`RAW_SHARD_05a_annotated_types_inference.md`).
- [x] **`W5-2` (`ISS-W5-02`)**: Ch 5b (§5.4–5.5) Side Effects, Exceptions, Region Inference & Concurrent Behaviours, Synthesis (`ppa-types-effects-and-regions`, `ppa-types-effects-and-regions.md`), Refactoring (`REF-005`) & Gate #7 (Ch 5 3-Model Loop — CLOSED `3/3 [ALIGNED gate7-v2]`).
- [x] **`W5-3` (`ISS-W5-03`)**: Part II Cross-Paradigm Matrix (`ontology/cross_paradigm_matrix.md`), Cumulative Refactoring (`REF-006`) & Gate #8 (Part II 3-Model Loop — CLOSED `3/3 [ALIGNED gate8-v2]`; Part II complete).

## Phase 6: Part III — Chapter 6 (Algorithms), Cyber Synthesis & Part III Gate

**Status:** completed

- [x] **`W6-1` (`ISS-W6-01`)**: Unit 6 — Ch 6 Worklist, RPO, Round-Robin & SCC Solvers + Subject/Bib Index (`RAW_SHARD_06_algorithms_bib.md`, `ppa-fixedpoint-solvers`, `ppa-fixedpoint-solvers.md`, `REF-007`) + Gate #9 (Ch 6 3-Model Loop — CLOSED `3/3 [ALIGNED gate9-v2]`).
- [x] **`W6-2` (`ISS-W6-02`)**: Cross-Book Cyber Program Analysis Skill (`ppa-cyber-vulnerability-analysis`, `ppa-cyber-analysis.md`), Merged `corpus/RAW_KNOWLEDGE.md`, Refactoring (`REF-007`) & Gate #10 (Part III 3-Model Loop — CLOSED `3/3 [ALIGNED gate10-v2]`; Part III complete).

## Phase 7: Cross-Harness Porting Documentation, Reference Adapters & Conformance Suite

**Status:** active

- [ ] **`W7-1` (`ISS-W7-01`)**: Author `README.md`, `architecture/PORTING_GUIDE.md`, `architecture/MODEL_ADAPTATION_GUIDE.md`, 5 target harness adapters (`adapters/*.py`), `scripts/verify_port_conformance.py`, and `tests/test_adapters_and_conformance.py`.

## Phase 8: Whole-Book Full Audit, Local Deployment & Final 3-Model Gate

**Status:** active

- [ ] **`W8-1` (`ISS-W8-01`)**: Whole-Book Audit, Global Altitude Refactoring & GitHub Issue Export Manifest (`issues/export_manifest.json`).
- [ ] **`W8-2` (`ISS-W8-02`)**: Gate #11 (Whole-Book 3-Model Adversarial Loop) + Local Harness & Knowledge Wiki Deployment + Live Conformance Verification.

---

## Completed Initiatives

| Initiative | Period | Waves | P0s | Key DECs | Archive Path |
| :--- | :--- | :--- | :--- | :--- | :--- |

---

## Parked Issues & Deferred Work

Tracked as non-blocking `issues/backlog/BKL-NNN.md` files for downstream GitHub Issues export.
