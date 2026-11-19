<!-- @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006 -->
<!-- @decision DEC-PPA-009: Vendor-neutral top-level entry point documenting book attribution, L0-L3 retrieval physics, reference harness compilers, C1-C6 conformance certification, and lossless GitHub issue export. -->

# Principles of Program Analysis — Portable Semantic Knowledge Suite

A harness-agnostic, machine-verifiable four-altitude (`L0`–`L3`) semantic knowledge distribution derived from *Principles of Program Analysis* by Flemming Nielson, Hanne Riis Nielson, and Chris Hankin (Springer, 1999; Corrected Second Printing, 2005) [PPA Preface, pp. V-VIII].

Every formal definition, inference rule, monotonicity side condition, Galois adjunction law, widening schedule, effect/region discipline, and solver complexity bound is anchored to verified `(book_page, pdf_page)` coordinates in [corpus/pdf_page_map.json](corpus/pdf_page_map.json) and packaged so any coding or security agent harness can load the exact depth a task requires while adding **zero bytes** to standing global prompts.

---

## 1. Source Attribution and Scope

- **Primary Textbook**: Flemming Nielson, Hanne Riis Nielson, and Chris Hankin, *Principles of Program Analysis*, Corrected Second Printing, Springer, 2005 [PPA Preface, p. V] (book p. V; PDF p. 5).
- **Four Unifying Approaches**: Data Flow Analysis (Chapter 2), Constraint Based Analysis (Chapter 3), Abstract Interpretation (Chapter 4), and Type and Effect Systems (Chapter 5), framed by Chapter 1 foundations, Chapter 6 fixed-point algorithms, and Appendices A–C (partially ordered sets, induction/coinduction, and graph theory) [PPA §1.1, p. 1] (book p. 1; PDF p. 21).
- **Attribution Firewall (`P2`)**: Claims, symbols, and preconditions stated by the textbook carry explicit `N8` citations (`[PPA §2.3, p. 66]`). Modern compiler, IDE, and vulnerability-analysis extensions outside the textbook carry the literal marker `[external]` and never carry a book citation.

---

## 2. Four-Altitude Architecture (`L0`–`L3`) and Zero `R0` Tax

Normative architectural rules live in [architecture/ARCHITECTURE.md](architecture/ARCHITECTURE.md). Content is stratified by retrieval physics rather than arbitrary chapter summaries:

| Altitude | Retrieval Channel | Canonical Surface | Line Budget (`N2`) | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **`R0`** | Unconditional turn-0 prompt | None (`0` bytes) | **`0` bytes** | Global harness instruction files (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.cursorrules`) remain untouched (`C2.2`, `C2.6`) |
| **`L0`** | `R1` ambient / `R2` router | `knowledge/ambient-context/ppa-*.md` and [SKILL.md](knowledge/skills/ppa-program-analysis/SKILL.md) | `80–250` (ambient), `50–99` (router) | Task orientation, polarity vocabulary, and deterministic routing across specialised skills |
| **`L2`** | `R2` skill body | `knowledge/skills/ppa-*/SKILL.md` | `250–499` | Actionable analysis design, verification, slicing, and triage procedures with mandatory precondition gates |
| **`L1`** | `R2` reference hop | `knowledge/skills/ppa-*/references/*.md` | `<= 450` (zero frontmatter) | Formal specifications, transfer equations, inference rules, and side conditions without proof-step clutter |
| **`L3`** | `R3` anchor lookup | `corpus/shards/RAW_SHARD_*.md`, `ontology/concept_graph.json`, `ontology/notation_index.md` | Unconstrained (zero frontmatter) | Complete derivations, closed 51-table / 56-figure inventories, four-domain projections, and per-unit gotcha ledgers |

---

## 3. Repository Map

| Directory / File | Role |
| :--- | :--- |
| [architecture/ARCHITECTURE.md](architecture/ARCHITECTURE.md) | Normative `L0`–`L3` altitude specification, `U1`–`U10` cross-chapter unification edges, and five anti-degradation contracts |
| [architecture/CONFORMANCE_SPEC.md](architecture/CONFORMANCE_SPEC.md) | Binary certification specification (`N1`–`N8`, gates `C1`–`C6`, `DEV-STUB` and `DEV-NOFILES` deviations) |
| [architecture/PORTING_GUIDE.md](architecture/PORTING_GUIDE.md) | Step-by-step compilation blueprints and `always_on_surfaces` registry across external agent harnesses |
| [architecture/MODEL_ADAPTATION_GUIDE.md](architecture/MODEL_ADAPTATION_GUIDE.md) | Optional runtime tuning overlays across model families without mutating canonical `knowledge/` files |
| `knowledge/` | Portable canonical package: `skills/ppa-*/` (`SKILL.md`, `references/*.md`, `evals/cases.yaml`) and `ambient-context/ppa-*.md` |
| `ontology/` | Machine-validated concept graph ([concept_graph.schema.json](ontology/concept_graph.schema.json)), notation index, [cross_paradigm_matrix.md](ontology/cross_paradigm_matrix.md), and altitude alignment log |
| `corpus/` | Dynamic `(book_page, pdf_page)` coordinate map ([pdf_page_map.json](corpus/pdf_page_map.json)), merged ground truth ([RAW_KNOWLEDGE.md](corpus/RAW_KNOWLEDGE.md)), and `L3` shards |
| `issues/` | Lossless per-file Markdown tracker ([SCHEMA.md](issues/SCHEMA.md): `epics/`, `shards/`, `refactors/`, non-blocking `backlog/`) |
| `adapters/` | Five deterministic Python 3 standard-library compilers emitting target harness trees and `port_manifest.json` |
| `scripts/` | Portability hygiene scanner, Tier-A canonical validator, `flock`-guarded issue controller, and `C1`–`C6` conformance verifier |
| `tests/` | Hermetic standard-library `unittest` suites exercising core invariants, adapters, and conformance gates |

---

## 4. Quickstart: Compiling Target Harness Ports

All compilers use only the Python 3 standard library, preserve LF normalisation, create zero symlinks, leave always-on instruction surfaces untouched, and write `<port_root>/port_manifest.json`.

### 4.1 Pre-Port Canonical Validation

```bash
python3 -B scripts/check_portability_hygiene.py .
python3 -B scripts/validate_ppa_knowledge.py --root .
python3 -B scripts/issue_ctl.py --root . validate
```

### 4.2 Target 1 — Claude Code (`.claude/`)

Installs lossless skills into `<port_root>/.claude/skills/ppa-*/`, ambient guides into `<port_root>/.claude/ppa-ambient/`, and `L3` ontology/corpus closure into `<port_root>/.claude/core/` (`0` bytes added to `CLAUDE.md`):

```bash
python3 -B adapters/claude_code_adapter.py --repo-root . --port-root <port_root>
```

### 4.3 Target 2 — Gemini CLI (`skills-local/` + `memory/topics/`)

Installs regular files under `<port_root>/skills-local/ppa-*/` (validating `{name, description}` `SKILL.md` frontmatter) and `<port_root>/memory/topics/ppa-*.md` (with `description:` L0 frontmatter parity; `0` bytes added to `GEMINI.md` or `~/.gemini/GEMINI.md`; custom subdirectories supported via `--skills-dir` and `--memory-dir`):

```bash
python3 -B adapters/gemini_harness_adapter.py --repo-root . --port-root <port_root>
```

### 4.4 Target 3 — Codex / `AGENTS.md` Harnesses (`.agents/`)

Installs `<port_root>/.agents/skills/ppa-*/` and `<port_root>/.agents/ppa-ambient/ppa-*.md` with zero modifications to `AGENTS.md` by default (pass `--emit-dev-stub` only when an operator explicitly authorizes a `<= 12`-line, `<= 800`-byte `DEV-STUB` pointer block):

```bash
python3 -B adapters/agents_md_adapter.py --repo-root . --port-root <port_root>
```

### 4.5 Target 4 — Cursor IDE Rules (`.cursor/rules/*.mdc`)

Compiles router, domain skills, and ambient guides into `.cursor/rules/ppa-*.mdc` with `alwaysApply: false` while mirroring lossless `L1` references and `L3` core files under `.cursor/ppa/`:

```bash
python3 -B adapters/cursor_mdc_adapter.py --repo-root . --port-root <port_root>
```

### 4.6 Target 5 — Knowledge Wiki + NotebookLM Sync (`pages/`)

Compiles transforming concept/skill pages (`pages/concepts/`), chunked `<= 450`-line reference and shard sources (`pages/sources/`), hierarchical navigation/ingest logs (`pages/index.md` + `pages/concepts/ppa-index-*.md` + `pages/sources/ppa-index-sources.md` + `pages/log.md`), `wiki_config.json` (preserving pre-existing non-PPA entries), and `notebooklm_sources_bundle/` (`CONFORMANT` exit `0` by default; pass `--dev-nofiles` only when registering fileless remote/API endpoints under `DEV-NOFILES`):

```bash
python3 -B adapters/wiki_sync_adapter.py --repo-root . --port-root <port_root>
```

---

## 5. Certifying Conformance (`C1`–`C6`)

Run [scripts/verify_port_conformance.py](scripts/verify_port_conformance.py) to evaluate all 55 checks across `C5 -> C1 -> C3 -> C2 -> C4 -> C6` and write `<port_root>/conformance_report.json`:

```bash
python3 -B scripts/verify_port_conformance.py \
  --core . \
  --port <port_root> \
  --manifest <port_root>/port_manifest.json
```

| Exit Code | Verdict | Meaning |
| :--- | :--- | :--- |
| `0` | `CONFORMANT` | All 6 gates (`C5`, `C1`, `C3`, `C2`, `C4`, `C6`) pass with `deviations: []` |
| `2` | `CONFORMANT_WITH_DEVIATIONS` | All 6 gates pass using only declared `DEV-STUB` or `DEV-NOFILES` deviations (`CONFORMANCE_SPEC.md` §6) |
| `1` | `NON_CONFORMANT` | Any check fails, examines zero items without a permitted deviation (`<gate>_VACUOUS`), or omits `port_manifest.json` |

---

## 6. Issue Provenance and GitHub Issues Export

Architectural decisions, per-chapter altitude refactorings (`REF-*`), and non-blocking textbook errata or modern-practice tensions (`BKL-*`) live in `issues/` and export losslessly in topological order (`C6.4`–`C6.5`):

```bash
python3 -B scripts/issue_ctl.py --root . validate
python3 -B scripts/issue_ctl.py --root . export-github --dry-run
```

This writes `issues/export_manifest.json` with deterministic parent-first ordering, `N7` frontmatter snapshots, and `N6` SHA-256 body digests ready for external issue-tracker synchronization.
