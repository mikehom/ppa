<!-- @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006 -->
<!-- @decision DEC-PPA-001: Target ports compile deterministically from canonical knowledge/, ontology/, corpus/, and issues/ without writing always-on global instruction bytes, certified via declared port_manifest.json and gates C1-C6. -->

# PORTING_GUIDE: Target Harness Compilation and Certification Runbook

## 0. Purpose, Normative Precedence, and Pre-Port Checklist

This runbook translates [ARCHITECTURE.md](ARCHITECTURE.md) and [CONFORMANCE_SPEC.md](CONFORMANCE_SPEC.md)
into step-by-step, agent-executable procedures for compiling the canonical program-analysis knowledge
distribution into external agent harnesses. It preserves the textbook's unifying architecture across
Data Flow Analysis, Constraint Based Analysis, Abstract Interpretation, and Type and Effect Systems
([PPA Preface, pp. V-VI]) across every target runtime without introducing standing prompt bloat.

### 0.1 Precedence

1. [CONFORMANCE_SPEC.md](CONFORMANCE_SPEC.md) (`C1`-`C6`, `N1`-`N8`, `§6` deviations) is normative
   for every pass/fail certification verdict.
2. [ARCHITECTURE.md](ARCHITECTURE.md) (`R-CORE-*`, `B1`-`B9`, `P1`-`P5`, `§7` contracts) governs
   canonical layer separation, line budgets, and anti-degradation invariants.
3. Section 2 of this guide defines the authoritative minimum `always_on_surfaces` set evaluated by
   `CONFORMANCE_SPEC.md` check `C2.1`.

### 0.2 Pre-Port Verification and Snapshot Protocol

Execute these checks on the canonical source repository before writing any target files
(`CONFORMANCE_SPEC.md` §7):

```bash
python3 -B scripts/check_portability_hygiene.py .
python3 -B scripts/validate_ppa_knowledge.py --strict-gotchas
python3 -B scripts/verify_port_conformance.py --canonical-only --repo-root .
```

Record the verified canonical revision identifier (`canonical_revision`, commit hash or release tag)
and halt immediately if either check exits non-zero; a canonical core that fails core validation cannot
produce a `CONFORMANT` port.

Before creating or modifying any target directory:

1. Enumerate every path listed in Section 2 for the chosen `target` (plus any target-specific parent
   instruction files already active in the destination project).
2. Compute raw-byte SHA-256 digests (`sha256_before`) for each existing surface and record `null` for
   each surface absent before installation.
3. Persist that snapshot table alongside the target directory path so `C2.2` and `C2.6` can certify
   exact byte preservation after compilation.

---

## 1. Canonical Source Surfaces, Whole-Package Closure (`C1.12`), and Link Rules

Every port MUST install the entire canonical package atomically (`CONFORMANCE_SPEC.md` `C1.12`,
`ARCHITECTURE.md` §4.3); partial installs break cross-skill `references/` links and fail `C1.12`
and `C3.9`.

### 1.1 Canonical Inventory Map (`ARCHITECTURE.md` §8)

| Canonical Path | Altitude | Required Content & Package Ownership | Frontmatter (`N3`) | Budget (`N2`) |
| :--- | :--- | :--- | :--- | :--- |
| `knowledge/skills/ppa-program-analysis/` | `L0` + `L1` | Master router `SKILL.md`, shared Ch. 1 / App. `references/`, `evals/cases.yaml` | `name`, `description` (`C3.5`) | `50-99` (`SKILL.md`), `<= 450` (`references/`) |
| `knowledge/skills/ppa-dataflow-and-slicing/` | `L2` + `L1` | Ch. 2 DFA, interprocedural, shape analysis (`SKILL.md`, `references/`, `evals/`) | `name`, `description` (`C3.5`) | `250-499` (`SKILL.md`), `<= 450` (`references/`) |
| `knowledge/skills/ppa-control-flow-and-constraints/` | `L2` + `L1` | Ch. 3 0-CFA, uniform k-CFA, CPA (`SKILL.md`, `references/`, `evals/`) | `name`, `description` (`C3.5`) | `250-499` (`SKILL.md`), `<= 450` (`references/`) |
| `knowledge/skills/ppa-abstract-interpretation/` | `L2` + `L1` | Ch. 4 Galois connections, combinators, widening (`SKILL.md`, `references/`, `evals/`) | `name`, `description` (`C3.5`) | `250-499` (`SKILL.md`), `<= 450` (`references/`) |
| `knowledge/skills/ppa-types-effects-and-regions/` | `L2` + `L1` | Ch. 5 Annotated CFA, effects, regions, behaviours (`SKILL.md`, `references/`, `evals/`) | `name`, `description` (`C3.5`) | `250-499` (`SKILL.md`), `<= 450` (`references/`) |
| `knowledge/skills/ppa-fixedpoint-solvers/` | `L2` + `L1` | Ch. 6 worklist, RPO, Round Robin, SCC solvers (`SKILL.md`, `references/`, `evals/`) | `name`, `description` (`C3.5`) | `250-499` (`SKILL.md`), `<= 450` (`references/`) |
| `knowledge/skills/ppa-cyber-vulnerability-analysis/` | `L2` + `L1` | Cross-cutting security skill from `projections.cyber` (`SKILL.md`, `references/`, `evals/`) | `name`, `description` (`C3.5`) | `250-499` (`SKILL.md`), `<= 450` (`references/`) |
| `knowledge/ambient-context/ppa-*.md` | `L0` | 7 orientation guides (`ppa-foundations.md` .. `ppa-cyber-analysis.md`) | Harness-conditional | `80-250` lines inclusive (`C3.4`) |
| `ontology/concept_graph.json`, `ontology/notation_index.md` | `L3` graph | Node graph, 4 projections, `U1`-`U10` unification edges (`[PPA Preface, pp. V-VIII]`) | Forbidden (`C3.6`) | Unconstrained |
| `corpus/RAW_KNOWLEDGE.md`, `corpus/pdf_page_map.json` | `L3` corpus | Anchor-addressable canonical rules & page coordinate map (`C1.3`) | Forbidden (`C3.6`) | Unconstrained |
| `issues/` + `issues/export_manifest.json` | Provenance | Ordered epics, shards, refactors, non-blocking backlog (`C6.1`-`C6.9`) | `issues/SCHEMA.md` | Unconstrained |

Every citation token copied or transformed out of `L1` or `L3` (for example `[PPA §5.1, p. 283]`,
`[PPA Table 6.1, p. 369]`, `[PPA §5.4.3, p. 338]`, or `[PPA Lemma 6.12, p. 380]`) MUST survive verbatim
under multiset conservation (`C1.8`). Never strip side conditions when compressing or transforming
output chunks (`SMOOTHING_TRAP`).

### 1.2 Cross-Target Link Transformation Matrix (`B2`, `C3.7`-`C3.9`)

| Source -> Target Hop | Lossless Skill Ports (`Claude Code`, `Gemini CLI`, `Codex`) | Rule-File Ports (`.cursor/rules/`) | Service Ports (`MCP` / `Graph-RAG`) | Wiki Ports (`<wiki_root>/`) |
| :--- | :--- | :--- | :--- | :--- |
| Router -> Sibling Skill | Plain `name` token in table/body (no link to sibling `SKILL.md`, `C3.8`) | Plain `.mdc` rule name / trigger token | `ppa.get_skill(name)` tool invocation | Wiki link `[[skills/<name>]]` |
| `SKILL.md` -> `references/<f>.md` | Relative link `(references/<f>.md)` preserved byte-for-byte | `@file .cursor/ppa/skills/<name>/references/<f>.md` | Resource URN `ppa:skills/<name>/references/<f>` | Link to `pages/concepts/` + `pages/sources/` |
| `L1` Reference -> `L3` Corpus/Graph | `N8` inline citation (for example `[PPA §1.3, p. 6] (book p. 6; PDF p. 26)`) + anchor key | `N8` citation preserved verbatim (`C1.8`) | `ppa.lookup_anchor(locator)` / `ppa.get_concept(id)` | Link to `pages/sources/ppa-<unit>.md#<anchor>` |
| `L1` Reference -> Any `SKILL.md` | **Forbidden (`C3.8`)** | **Forbidden (`C3.8`)** | **Forbidden (`C3.8`)** | Pointer back only through index page |

---

## 2. Minimum Declared `always_on_surfaces` Registry (`C2.1`) & Deviations

`CONFORMANCE_SPEC.md` check `C2.1` compares the manifest's `always_on_surfaces` array against the
minimum set required below for the declared `target`. Every path in the declared set MUST exhibit zero
byte delta (`sha256_after == sha256_before`, `0` added bytes per `C2.6`; absent files remain absent).

| `target` key | Minimum `always_on_surfaces` Paths (Project & User Scopes) | Unconditional Load Marker Forbidden on Installed Files (`C2.3`) |
| :--- | :--- | :--- |
| `claude-code` | `CLAUDE.md`, `.claude/CLAUDE.md`, `~/.claude/CLAUDE.md` | Never append pointers or install files as unconditional `.claude/` instructions |
| `gemini-cli` | `GEMINI.md`, `~/.gemini/GEMINI.md`, `~/.gemini/rules/*.md` | Never add `always_on` rules or modify `GEMINI.md`; keep canonical `SKILL.md` read-only |
| `codex-agents` | `AGENTS.md`, `**/AGENTS.md` (pre-existing directory instruction files) | Never inject PPA text into root or nested `AGENTS.md` (unless declared `DEV-STUB`) |
| `cursor-ide` | `.cursorrules`, `.cursor/rules/*.mdc` where `alwaysApply: true` | Every installed `.mdc` rule MUST set `alwaysApply: false` |
| `mcp-graph-rag` | `<server_config>/system_prompt.*`, `<vault>/templates/*always*` | Zero standing system-prompt text injected per session (`DEV-NOFILES` allowed) |
| `knowledge-wiki` | `<wiki_root>/system_prompt.md`, `<wiki_root>/templates/default*` | Pages connect via on-demand index/collections; zero forced template injection |

### 2.1 Permitted Deviations (`CONFORMANCE_SPEC.md` §6)

1. **`DEV-STUB`**: Permitted solely for `C2.2` and `C2.6` when the target runtime lacks any on-demand
   `R1`/`R2` discovery mechanism and the **operator** (never the automated compiler) inserts a minimal
   pointer block (`<= 12` lines, `<= 800` bytes, installed filenames/descriptions only, zero definitions,
   rules, procedures, or `N8` citations). Record `{"id": "DEV-STUB", "surface": "<path>", "text": "<exact_stub>"}`
   inside `port_manifest.json.deviations`.
2. **`DEV-NOFILES`**: Permitted solely for `C3.1`-`C3.4` and `C3.6` when content is served dynamically
   through MCP tools/resources or Graph-RAG endpoints rather than on-disk Markdown files. Every served
   payload MUST still satisfy exact numeric line ceilings (`50-99`, `80-250`, `<= 450`, `< 500`) and
   `C1.8` citation conservation.

---

## 3. Target Harness Compilation Blueprints

### 3.1 Target 1: Claude Code (`.claude/`)

1. **Target filesystem layout**:
   ```text
   <port_root>/.claude/
     skills/
       ppa-program-analysis/{SKILL.md, references/*.md, evals/cases.yaml}
       ppa-dataflow-and-slicing/{SKILL.md, references/*.md, evals/cases.yaml}
       ppa-control-flow-and-constraints/{SKILL.md, references/*.md, evals/cases.yaml}
       ppa-abstract-interpretation/{SKILL.md, references/*.md, evals/cases.yaml}
       ppa-types-effects-and-regions/{SKILL.md, references/*.md, evals/cases.yaml}
       ppa-fixedpoint-solvers/{SKILL.md, references/*.md, evals/cases.yaml}
       ppa-cyber-vulnerability-analysis/{SKILL.md, references/*.md, evals/cases.yaml}
     core/
       ontology/{concept_graph.json, concept_graph.schema.json, notation_index.md}
       corpus/{RAW_KNOWLEDGE.md, pdf_page_map.json}
   ```
2. **Channel mapping (`R0`-`R3`)**:
   - `R0`: `CLAUDE.md`, `.claude/CLAUDE.md`, `~/.claude/CLAUDE.md` remain untouched (`0` added bytes).
   - `R1`: Place `knowledge/ambient-context/ppa-*.md` either into `.claude/ppa-ambient/ppa-*.md` (default path in
     `adapters/claude_code_adapter.py`) or `.claude/rules/ppa-<slug>.md` (only when the target runtime supports
     conditional path/description matching without turn-0 injection) OR apply `ARCHITECTURE.md` §4.4 degradation
     (`R1 -> R2`) by stripping frontmatter (`C3.6`) and placing them under
     `.claude/skills/ppa-program-analysis/references/ambient-<slug>.md` linked from the router table
     (keeping router `< 100` lines, `C3.1`).
   - `R2`: Losslessly mirror all 7 canonical skill packages into `.claude/skills/<name>/`.
   - `R3`: Reference `.claude/core/corpus/RAW_KNOWLEDGE.md` and `.claude/core/ontology/concept_graph.json`
     by anchor or line span; never instruct models to load entire `L3` files.
3. **Compilation constraints**:
   - Preserve YAML frontmatter keys strictly `{name, description}` (`C3.5`) matching directory names.
   - Verify `references/*.md` carry zero frontmatter (`C3.6`) and match canonical `N6` SHA-256 digests (`C1.7`).
   - Never rewrite router references into links pointing at another skill's `SKILL.md` (`C3.8`).

### 3.2 Target 2: Gemini CLI (`~/.gemini/`) and Knowledge Wiki + NotebookLM Sync

1. **Local Skills (`skills-local/` or `~/.gemini/skills-local/`)**:
   - Install all 7 canonical skill directories losslessly into `skills-local/<name>/` (default relative
     layout in `adapters/gemini_harness_adapter.py`; `--skills-dir` overrides for `~/.gemini/skills-local/<name>/`),
     retaining `SKILL.md`, `references/*.md`, and `evals/cases.yaml`.
   - Keep `~/.gemini/GEMINI.md`, project `GEMINI.md`, `~/.gemini/rules/*.md`, and any read-only
     upstream symlinked `SKILL.md` targets untouched (`0` bytes added).
   - Store any operator-approved post-port runtime refinements exclusively inside
     `~/.gemini/skill-overlays/<name>.md` as non-canonical deltas—never edit canonical files in place.
2. **Ambient Semantic Context (`R1`)**:
   - Install `knowledge/ambient-context/ppa-*.md` into semantic-retrieval topic storage
     (`memory/topics/ppa-*.md` by default in `adapters/gemini_harness_adapter.py`, or `--memory-dir ~/.gemini/topics`)
     when semantic topic matching is active; otherwise place them
     with frontmatter removed under `skills-local/ppa-program-analysis/references/ambient/`
     and link them from the router (`R1 -> R2`, `C3.1`).
3. **Knowledge Wiki + NotebookLM Transforming Port (`<wiki_root>/`)**:
   - **Concept & skill pages (`L0`/`L1`/`L3`)**: `adapters/wiki_sync_adapter.py` emits transformed skill/ambient
     pages (`pages/concepts/ppa-*.md`) plus one concept card (`pages/concepts/ppa-node-<slug>.md`) per node in
     `ontology/concept_graph.json`, preserving `formal_summary`, all 4 `projections` (`P1`-`P5`, `[external]`
     attribution tags intact), `conditions` bullets, `issue_refs`, `U1`-`U10` edges (`corresponds_to` `basis`),
     and all `N8` citations (`C1.8`).
   - **Source digests (`L3`)**: Emit chunked `<= 450L` reference/shard pages (`pages/sources/ppa-ref-*.md` and
     `pages/sources/ppa-shard-<unit>-part<NN>.md`) directly from canonical references and verified `corpus/shards/RAW_SHARD_*.md`
     text with `(book p. X; PDF p. Y)` coordinates (plus lossless mirrors in `core/`).
   - **Navigation & Chronological Log (`L0`)**: Emit `<wiki_root>/pages/index.md` (`<= 250` lines), hierarchical
     sub-index cards (`pages/concepts/ppa-index-*.md`, `pages/sources/ppa-index-sources.md`, each `<= 250L`) reaching
     `100%` of emitted `pages/` files without orphans (`C3.9`), and `<wiki_root>/pages/log.md` (`C2.6` untouched on vault templates).
   - **NotebookLM sync**: Package exported source-unit Markdown files together with
     `ontology/notation_index.md` into `notebooklm_sources_bundle/` so mathematical formulas, arrows,
     and subscripts stay faithful to visual inspection rather than degraded PDF OCR (`ARCHITECTURE.md` §7.4).

### 3.3 Target 3: Codex / Standard `AGENTS.md` + `.agents/skills/` Harnesses

1. **Target filesystem layout**:
   ```text
   <port_root>/.agents/
     ppa-ambient/ppa-*.md              (default adapters/agents_md_adapter.py R1 path)
     skills/
       ppa-program-analysis/{SKILL.md, references/*.md, evals/cases.yaml}
       ... (all 7 canonical skill directories; optional R1->R2 references/ambient/)
     core/
       ontology/{concept_graph.json, concept_graph.schema.json, cross_paradigm_matrix.md, notation_index.md}
       corpus/{RAW_KNOWLEDGE.md, pdf_page_map.json, shards/RAW_SHARD_*.md}
   ```
2. **Channel mapping (`R0`-`R3`)**:
   - `R0`: Root `AGENTS.md` and every pre-existing nested `AGENTS.md` retain identical `sha256_before`
     bytes (`0` added bytes).
   - `R1` default & `R1 -> R2` fallback (`ARCHITECTURE.md` §4.4): `adapters/agents_md_adapter.py` places
     `knowledge/ambient-context/ppa-*.md` into `.agents/ppa-ambient/ppa-*.md` by default; where a runtime
     only discovers `.agents/skills/`, strip YAML frontmatter (`C3.6`), install into
     `.agents/skills/ppa-program-analysis/references/ambient/`, link all 7 under `# Orientation Guides`
     inside `.agents/skills/ppa-program-analysis/SKILL.md` (confirming line count stays `50-99`, `C3.1`),
     and record this step as `transforming` in `port_manifest.json` (`C1.8`).
   - `R2` + `R3`: Mirror all 7 canonical skill directories into `.agents/skills/<name>/` and place
     `ontology/` and `corpus/` cleanly under `.agents/core/` outside `.agents/skills/` so `C3.12`
     closed-tree directory rules remain satisfied.
3. **Legacy fallback**: Only where `.agents/skills/` autodiscovery is unavailable may the operator add a
   declared `DEV-STUB` block inside `AGENTS.md` (`<= 12L`, `<= 800B`, naming `.agents/skills/ppa-program-analysis/SKILL.md`).

### 3.4 Target 4: Cursor / Windsurf / IDE Rule Harnesses (`.cursor/rules/`)

1. **Target filesystem layout (`transforming` + `lossless` split)**:
   - `.cursor/rules/ppa-ambient-<slug>.mdc` (`7` files from `knowledge/ambient-context/ppa-*.md`, `80-250` lines, `C3.4`)
   - `.cursor/rules/ppa-router.mdc` (`1` file from `ppa-program-analysis/SKILL.md`, `50-99` lines, `C3.1`)
   - `.cursor/rules/ppa-skill-<slug>.mdc` (`6` files from domain/cross-cut `SKILL.md` files, `250-499` lines, `C3.2`)
   - `.cursor/ppa/skills/<name>/references/*.md` (pure Markdown, zero frontmatter `C3.6`, lossless `N6` digests)
   - `.cursor/ppa/ontology/...` and `.cursor/ppa/corpus/...` (`R3` read-on-demand core)
2. **Mandatory `.mdc` frontmatter transform (`C2.3`, `C2.5`, `C4`)**:
   ```yaml
   ---
   description: <verbatim canonical description from SKILL.md, or <=1024-char ambient trigger>
   globs:
   alwaysApply: false
   ---
   ```
   - `alwaysApply` MUST be `false` (`C2.3`) on every generated `.mdc` file; `globs` MUST NOT use
     catch-all patterns such as `*` or `**/*` (equivalent to unconditional always-on tax `C2.6`).
   - Preserve exact `Use when ...` and `Do not use ...` sibling tokens inside `description` (`C4.1`-`C4.3`).
   - Rewrite Markdown links `(references/<f>.md)` inside `.mdc` bodies to
     `@file .cursor/ppa/skills/<name>/references/<f>.md` (or valid relative links verified under
     `C3.7`-`C3.8`), and declare every `.mdc` output as `transforming` in `port_manifest.json`.

### 3.5 Target 5: MCP / Graph-RAG / Vector-RAG Servers (`DEV-NOFILES`)

1. **Serving interface & zero `R0` tax (`C2.5`-`C2.6`)**:
   - Load read-only in-memory indexes over `knowledge/`, `ontology/concept_graph.json`,
     `ontology/notation_index.md`, `corpus/RAW_KNOWLEDGE.md`, `corpus/pdf_page_map.json`, and
     `issues/export_manifest.json` pinned to `canonical_revision`.
   - Inject **zero** instructional text into server system prompts or connection initialization
     handshakes (`C2.6`). Tool and resource descriptions MUST stay `<= 1,024` characters without inline
     definitions, numbered procedures, or `N8` citations (`C2.5`).
2. **Required MCP Tools and Resource URNs**:
   - `ppa.route` (`ppa:router`): returns the `L0` router table (`50-99` lines).
   - `ppa.get_skill(name)` (`ppa:skills/<name>`): returns `L2` `SKILL.md` (`250-499` lines).
   - `ppa.get_reference(skill, file, section?)` (`ppa:skills/<name>/references/<file>`): returns `L1`
     reference (`<= 450` lines) or a targeted section slice (`N2` ceiling verified per response under
     `DEV-NOFILES`).
   - `ppa.get_concept(id)` (`ppa:concepts/<id>`): returns exact JSON node (`id`, `title`, `altitude`,
     `unit`, `citations`, `formal_summary`, 4 `projections`, `related_edges`, `artifact_refs` satisfying `C1.2`).
   - `ppa.traverse(id, relation?, depth=1)`: expands typed edges (`corresponds_to` carrying
     `basis.unification_id`, `depends_on`, and exact inverses from `ontology/concept_graph.schema.json`).
   - `ppa.lookup_anchor(locator | book_page)`: resolves coordinates via `corpus/pdf_page_map.json`
     (`C1.3`) to return strictly the addressed `L3` entry in `corpus/RAW_KNOWLEDGE.md`, never whole files.
3. **Graph-RAG / Vector-RAG Chunking & Payload Metadata Contract**:
   - Chunk `L1` strictly at H2/H3 section boundaries and `L3` at numbered statement, table, or
     gotcha-ledger entry boundaries; **never** split an inference rule, signature, or `conditions`
     array across vector chunks (`SMOOTHING_TRAP` / `SIGNATURE_DISTORTION`).
   - Store structured metadata (`concept_id`, `unit`, `altitude`, `citations`, `conditions`,
     `gotcha_refs`, `parent_anchor`) on every indexed payload so `C1.1`, `C1.2`, `C1.8`, and
     `DEV-NOFILES` budget checks certify cleanly.

---

## 4. Deterministic `port_manifest.json` Compilation (`C1`, `C2`, `C5.7`)

Every port MUST emit `<port_root>/port_manifest.json` conforming to `CONFORMANCE_SPEC.md` §2:

1. **Deterministic serialization (`C5.7`)**: Walk canonical source directories in sorted ASCII order,
   normalize line endings to LF (`N5`), sort JSON keys (`N7`), and exclude wall-clock timestamps,
   random identifiers, hostnames, and absolute workstation paths (`C5.3`).
2. **Complete `mappings` closure (`C1.12`)**: Every file under canonical `knowledge/` and `ontology/`
   MUST appear in `mappings` exactly once with `kind` set to `"lossless"` (matching `N6` SHA-256)
   or `"transforming"` (`.mdc` rules, wiki pages, router-embedded ambient files, or `DEV-NOFILES` resources).
3. **Worked manifest examples (`lossless` vs `DEV-NOFILES` / `DEV-STUB`)**:
   ```json
   {
     "spec_version": "1",
     "target": "cursor-ide",
     "canonical_revision": "<commit-sha>",
     "mappings": [
       {"canonical": "knowledge/skills/ppa-program-analysis/SKILL.md", "port": [".cursor/rules/ppa-router.mdc"], "kind": "transforming"},
       {"canonical": "knowledge/skills/ppa-fixedpoint-solvers/references/worklist-and-rpo-algorithms.md", "port": [".cursor/ppa/skills/ppa-fixedpoint-solvers/references/worklist-and-rpo-algorithms.md"], "kind": "lossless"}
     ],
     "always_on_surfaces": [
       {"path": ".cursorrules", "sha256_before": null}
     ],
     "discovery_entries": [
       {"name": "ppa-program-analysis", "description_chars": 412}
     ],
     "deviations": []
   }
   ```
   For `mcp-graph-rag`, populate `"deviations": ["DEV-NOFILES"]` and record resource URNs (`ppa:skills/...`)
   inside `mappings[*].port`. For `DEV-STUB`, record `"deviations": [{"id": "DEV-STUB", "surface": "AGENTS.md", "text": "..."}]`.
4. **Extended `C5.5` denylist**: Before certifying, operators in proprietary organizations MUST pass an
   extended local denylist via `scripts/check_portability_hygiene.py --denylist <file>`
   (`CONFORMANCE_SPEC.md` §7 step 4) covering private tracker prefixes, internal host domains, and CLI names.

---

## 5. Exporting Issues and Backlog Provenance (`C6`)

Ports supporting engineering governance, curriculum maintenance, or external audits MUST include `issues/`
and `issues/export_manifest.json`:

1. Validate `issues/` locally (`python3 -B scripts/issue_ctl.py validate`) checking frontmatter
   schemas (`C6.1`), filename/ID parity (`C6.2`), and acyclic `depends_on` / symmetric `blocks` edges (`C6.3`).
2. Emit `issues/export_manifest.json` in topological order (`C6.4`: every issue after its
   `parent_issue` and `depends_on` predecessors) preserving `N7` frontmatter and `N6` body digests (`C6.5`).
3. Keep `issues/backlog/BKL-*.md` strictly non-blocking (`C6.8`), verified by `C6.6` (`>= 1` resolved
   `C1.3` citation and `>= 1` existing `concept_id`) and `C6.7` (referenced by its affected artifact/node).
4. When mirroring to an external issue tracker, store `(canonical_id -> external_id)` solely inside
   tracker sync records—never embed private tracker URLs inside `knowledge/`, `ontology/`, or `corpus/` (`C5.4`, `C5.5`, `C6.10`).

---

## 6. Post-Port Certification, Failure Triage, and Clean Uninstall

Execute gates strictly in `CONFORMANCE_SPEC.md` §5 order (`C5 -> C1 -> C3 -> C2 -> C4 -> C6`) so
hygiene checks run before evidence serialization:

```bash
python3 -B scripts/check_portability_hygiene.py <port_root>
python3 -B scripts/validate_ppa_knowledge.py --strict-gotchas
python3 -B scripts/verify_port_conformance.py --core . --port <port_root> --manifest <port_root>/port_manifest.json
```

### 6.1 Verdict Handling and Remediation Matrix (`CONFORMANCE_SPEC.md` §§4-6)

| Verdict / Exit | Failure Codes | Mandatory Action (`ARCHITECTURE.md` `R-CORE-3`) |
| :--- | :--- | :--- |
| `CONFORMANT` (`0`) | None (`deviations == []`) | Publish `<port_root>/port_manifest.json` + `conformance_report.json` |
| `CONFORMANT_WITH_DEVIATIONS` (`2`) | None (`DEV-STUB` / `DEV-NOFILES` only) | Verify every recorded deviation in `conformance_report.json` is operator-approved |
| `NON_CONFORMANT` (`1`) | `C5_*` (`C5_HARNESS_TERM_IN_CORE`, `C5_ABSOLUTE_PATH`, `C5_HOST_OR_CONTACT`) | Remove leaked paths/tokens from canonical source or adapter config; rebuild |
| `NON_CONFORMANT` (`1`) | `C1_*` (`C1_PACKAGE_INCOMPLETE`, `C1_CITATION_MULTISET`, `C1_GOTCHA_DROPPED`) | Restore missing package files, citations, or ledger pointers in adapter template |
| `NON_CONFORMANT` (`1`) | `C2_*` (`C2_SURFACE_MODIFIED`, `C2_INSTALLED_ALWAYS_ON`, `C2_NONZERO_TAX`) | Revert modified `always_on_surfaces`; move `R1` to `R2` or set `alwaysApply: false` |
| `NON_CONFORMANT` (`1`) | `C3_*`, `C4_*`, `C6_*` | Fix broken rewritten links, exceeded budgets (`T1` refactor upstream), or manifest order |

Never patch a generated port file manually to silence a check (`R-CORE-3`): fix the **canonical core**
or **compiler adapter** and recompile cleanly. Certify reproducibility (`C5.7`) by compiling to two
separate roots (`<port_a>`, `<port_b>`) and asserting `diff -ru <port_a> <port_b>` exits `0`. Certify
clean uninstall by removing all files listed in `port_manifest.json.mappings` (plus manifest/report
files) and verifying every declared `always_on_surfaces` path matches `sha256_before`.
