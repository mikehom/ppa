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
and halt immediately if any of these checks exits non-zero; a canonical core that fails core validation
cannot produce a `CONFORMANT` port. The canonical-only verifier run evaluates the 44 checks that need
no port and reports the 11 port-only checks as `N/A` (`CONFORMANCE_SPEC.md` §5 item 6); its clean
summary is `44/44 evaluated checks PASS, 11 port-only N/A`. The validator runs the `ARCHITECTURE.md`
§7.1 anchor check and §7.2 signature check (`arch_7_1_l1_anchor_parity`, `arch_7_2_signature_parity`)
in both its default and `--certify` modes; a Tier A rule it did not perform would be printed as
`NOT_IMPLEMENTED`, and none is.

Before creating or modifying any target directory:

1. Enumerate every path listed in Section 2 for the chosen `target` (plus any target-specific parent
   instruction files already active in the destination project).
2. Compute raw-byte SHA-256 digests (`sha256_before`) for each existing surface and record `null` for
   each surface absent before installation. A surface beginning `~/` is resolved against the user
   scope (`--user-home`, else `PPA_USER_HOME`, else `<port_root>/.user_home`, else the invoking
   user's home); a surface with a wildcard is digested over all matching files
   (`CONFORMANCE_SPEC.md` §2.3). Give the compiler and the verifier the same user scope.
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
| Router -> Sibling Skill | Plain `name` token in table/body (no link to sibling `SKILL.md`, `C3.8`) | Plain `name` token (the sibling rule is matched by its description) | `ppa.get_skill(name)` tool invocation | Plain `name` token; the sibling page `pages/concepts/<name>.md` is reached through `pages/ppa_index.md` |
| `SKILL.md` -> `references/<f>.md` | Relative link `(references/<f>.md)` preserved byte-for-byte | Relative link `(../ppa/skills/<name>/references/<f>.md)` | Resource URN `ppa:skills/<name>/references/<f>` | Relative link `(../sources/ppa-ref-<name>--<f>.md)` |
| Router -> ambient file (targets without an `R1` channel) | Relative link `(references/ambient-<slug>.md)` appended to the compiled router | Not needed: ambient rules are indexed by description | Not needed when ambient resources are listed with descriptions | Link from `pages/ppa_index.md` to `pages/concepts/ppa-ambient-<slug>.md` |
| `L1` Reference -> `L3` Corpus/Graph | `N8` inline citation (for example `[PPA §1.3, p. 6] (book p. 6; PDF p. 26)`) + anchor key | `N8` citation preserved verbatim (`C1.8`) | `ppa.lookup_anchor(locator)` / `ppa.get_concept(id)` | `N8` citation preserved verbatim; shard chunks `pages/sources/ppa-shard-<unit>-part<NN>.md` are listed in `pages/sources/ppa-index-shards.md` |
| `L1` Reference -> Any `SKILL.md` | **Forbidden (`C3.8`)** | **Forbidden (`C3.8`)** | **Forbidden (`C3.8`)** | **Forbidden (`C3.8`)** |

---

## 2. Minimum Declared `always_on_surfaces` Registry (`C2.1`) & Deviations

`CONFORMANCE_SPEC.md` check `C2.1` compares the manifest's `always_on_surfaces` array against the
minimum set required below for the declared `target`. Every path in the declared set MUST exhibit zero
byte delta (`sha256_after == sha256_before`, `0` added bytes per `C2.6`; absent files remain absent).

The strings in the second column are the literal `path` values `C2.1` requires; they equal
`MINIMUM_ALWAYS_ON_SURFACES` in `adapters/common.py` character for character. A path without a
leading `~/` is relative to the port root; `~/` is the user scope. The third column lists surfaces
that MUST be declared in addition when they exist before installation, each by its own
port-relative path.

| `target` key | Minimum `always_on_surfaces` paths (literal) | Additional surfaces to declare when present | Unconditional load marker forbidden on installed files (`C2.3`) |
| :--- | :--- | :--- | :--- |
| `claude-code` | `CLAUDE.md`, `.claude/CLAUDE.md`, `~/.claude/CLAUDE.md` | None | Never append pointers or install files as unconditional `.claude/` instructions |
| `gemini-cli` | `GEMINI.md`, `~/.gemini/GEMINI.md`, `~/.gemini/rules/*.md` | None | Never add `always_on` rules or modify `GEMINI.md`; keep canonical `SKILL.md` read-only |
| `codex-agents` | `AGENTS.md` | Every nested `AGENTS.md` below the port root | Never inject PPA text into root or nested `AGENTS.md` (unless declared `DEV-STUB`) |
| `cursor-ide` | `.cursorrules` | Every `.cursor/rules/*.mdc` whose frontmatter sets `alwaysApply: true` | Every installed `.mdc` rule MUST set `alwaysApply: false` |
| `mcp-graph-rag` | `system_prompt.md`, `templates/always.md` | Any other file the server injects into every session | Zero standing system-prompt text injected per session (`DEV-NOFILES` allowed) |
| `knowledge-wiki` | `system_prompt.md`, `templates/default.md` | Every other `templates/default*` file | Pages connect via on-demand index/collections; zero forced template injection |

### 2.1 Permitted Deviations (`CONFORMANCE_SPEC.md` §6)

1. **`DEV-STUB`**: Permitted solely for `C2.2` and `C2.6` when the target runtime lacks any on-demand
   `R1`/`R2` discovery mechanism and the **operator** (never the automated compiler) inserts a minimal
   pointer block (`<= 12` lines, `<= 800` bytes, installed filenames/descriptions only, zero definitions,
   rules, procedures, or `N8` citations). Record `{"id": "DEV-STUB", "surface": "<path>", "text": "<exact_stub>"}`
   inside `port_manifest.json.deviations`. The stub is delimited by the lines `<!-- PPA_STUB_START -->`
   and `<!-- PPA_STUB_END -->` and occurs exactly once. It is a property of the surface, not of one
   compilation: while it is in the surface, every later build declares `DEV-STUB` and records as
   `sha256_before` the digest of the surface with the stub removed, whether or not the stub option is
   passed again. A surface that carries the stub marker without a declared `DEV-STUB` fails `C2.2`
   with `C2_UNDECLARED_DEVIATION`; a stub whose text was edited is refused by the reference adapter.
2. **`DEV-NOFILES`**: Permitted solely for `C3.1`-`C3.4` and `C3.6` when content is served dynamically
   through MCP tools/resources or Graph-RAG endpoints rather than on-disk Markdown files. Every served
   payload MUST still satisfy exact numeric line ceilings (`50-99`, `80-250`, `<= 450`, `< 500`) and
   `C1.8` conservation. The verifier reads the served units from `<port_root>/served_units.json`
   (`CONFORMANCE_SPEC.md` §2.3); a port that owns on-disk pages or skill files cannot declare it.

### 2.2 Write Protection and File Ownership (`--force`, `--manifest-name`)

1. Every reference adapter plans all outputs in memory and checks them before the first write. An
   output path that already exists and is not an output of the previous manifest in the same port
   root (`port_manifest.json`, or the name given by `--manifest-name`; its `mappings` targets, `extra_units`, `index_files`, `manifest_files`,
   `notebooklm_bundle`, and the tree under `corpus_root`) is a foreign file: the adapter exits with
   status 1 and writes nothing. Recompiling the same target into the same root needs no option.
2. `--force` overwrites foreign files. A discovery name that existed before installation is recorded
   in `pre_existing_discovery`, stays recorded across later builds, and fails `C4.8` when it equals a
   name the port emits (a skill directory name or a rule-file stem).
3. A symbolic link at an output path or at one of its directories always aborts; `--force` does not
   override it. A previous manifest written for another `target` does not confer ownership.
4. Merged files are never foreign and never overwritten whole: `wiki_config.json` (non-PPA keys kept),
   `pages/index.md` and `pages/log.md` of a wiki (§3.5), and a surface receiving a declared
   `DEV-STUB`. They are listed in `merged_files`.
5. **Stale outputs are pruned.** After a successful write, the adapter unlinks every regular file
   that the previous manifest of the same name and target listed (`mappings` targets, `extra_units`,
   `index_files`, `manifest_files`, `notebooklm_bundle`) and the current build no longer emits, then
   removes the directories this leaves empty. Never removed: the `merged_files` of either build,
   `wiki_config.json`, `pages/index.md`, `pages/log.md`, `AGENTS.md`, the manifest itself, a path that
   another manifest in the same root lists, a path that is or passes through a symbolic link, a path
   outside the port root, and any file the previous manifest did not list (an operator's file next to
   a pruned one stays).
6. **Several targets in one root.** `--manifest-name <name>.json` (a plain file name, default
   `port_manifest.json`) selects the manifest an adapter reads for ownership and writes on commit.
   Give each target its own name and ports with disjoint trees coexist, each recompiled and pruned
   from its own manifest only:

   ```bash
   python3 -B adapters/claude_code_adapter.py --repo-root . --port-root <root> --manifest-name port_manifest_claude.json
   python3 -B adapters/agents_md_adapter.py --repo-root . --port-root <root> --manifest-name port_manifest_codex.json
   python3 -B scripts/verify_port_conformance.py --core . --port <root> --manifest port_manifest_claude.json
   python3 -B scripts/verify_port_conformance.py --core . --port <root> --manifest port_manifest_codex.json
   ```

   Each certification reads only its manifest's owned files and writes `conformance_report_claude.json`
   or `conformance_report_codex.json` beside it (`CONFORMANCE_SPEC.md` §2.2). Compiling a second
   target under a manifest name another target already uses is refused: that manifest confers no
   ownership on it, so the existing manifest file is a foreign file.

---

## 3. Target Harness Compilation Blueprints

### 3.1 Target 1: Claude Code (`.claude/`)

1. **Target filesystem layout** (`adapters/claude_code_adapter.py`):
   ```text
   <port_root>/
     port_manifest.json
     .claude/
       skills/
         ppa-program-analysis/
           SKILL.md                      (canonical router + "Orientation Guides (R1 Fallback)" links)
           references/*.md               (canonical router references)
           references/ambient-<slug>.md  (the 7 ambient files, one per knowledge/ambient-context/ppa-<slug>.md)
           evals/cases.yaml, README.md, SUGGESTED_FIXES.md
         ppa-dataflow-and-slicing/{SKILL.md, references/*.md, evals/cases.yaml, README.md, SUGGESTED_FIXES.md}
         ppa-control-flow-and-constraints/{...same five entries...}
         ppa-abstract-interpretation/{...}
         ppa-types-effects-and-regions/{...}
         ppa-fixedpoint-solvers/{...}
         ppa-cyber-vulnerability-analysis/{...}
       core/
         ontology/{concept_graph.json, concept_graph.schema.json, notation_index.md,
                   cross_paradigm_matrix.md, altitude_alignment_log.md}
         corpus/{RAW_KNOWLEDGE.md, pdf_page_map.json, shards/RAW_SHARD_*.md}
   ```
   Every file under canonical `knowledge/` and `ontology/` is installed (`C1.12`), the per-skill
   `README.md` and `SUGGESTED_FIXES.md` included.
2. **Channel mapping (`R0`-`R3`)**:
   - `R0`: `CLAUDE.md`, `.claude/CLAUDE.md`, `~/.claude/CLAUDE.md` remain untouched (`0` added bytes).
   - `R1 -> R2` (`ARCHITECTURE.md` §4.4): the target indexes skill descriptions, not ambient files, so
     each `knowledge/ambient-context/ppa-<slug>.md` is installed as
     `.claude/skills/ppa-program-analysis/references/ambient-<slug>.md` (flat, no subdirectory) and the
     compiled router `SKILL.md` gains the section `## Orientation Guides (R1 Fallback)` with one
     relative link per file. The router mapping is `transforming` and MUST stay within `50-99` lines
     (`C3.1`); the adapter refuses to compile otherwise. A runtime with native conditional rules MAY
     instead install `.claude/rules/ppa-<slug>.md` and list the ambient file names in
     `discovery_entries`; an ambient file that is neither indexed nor linked fails `C3.9`.
   - `R2`: Losslessly mirror all 7 canonical skill packages into `.claude/skills/<name>/`.
   - `R3`: Reference `.claude/core/corpus/RAW_KNOWLEDGE.md` and `.claude/core/ontology/concept_graph.json`
     by anchor or line span; never instruct models to load entire `L3` files. The manifest records
     `"corpus_root": ".claude/core/corpus"`.
3. **Compilation constraints**:
   - Preserve YAML frontmatter keys strictly `{name, description}` (`C3.5`) matching directory names.
   - Verify `references/*.md` carry zero frontmatter (`C3.6`) and match canonical `N6` SHA-256 digests (`C1.7`).
   - Never rewrite router references into links pointing at another skill's `SKILL.md` (`C3.8`).

### 3.2 Target 2: Gemini CLI (`~/.gemini/`)

1. **Local Skills (`skills-local/` or `~/.gemini/skills-local/`)**:
   - Install all 7 canonical skill directories losslessly into `skills-local/<name>/` (default relative
     layout in `adapters/gemini_harness_adapter.py`), retaining `SKILL.md`, `references/*.md`,
     `evals/cases.yaml`, `README.md`, and `SUGGESTED_FIXES.md`. `--skills-dir` and `--memory-dir` take
     paths **inside** `--port-root`; a path that leaves the port root is rejected. To install into a
     user-level layout, make that directory the port root (for example `--port-root ~/.gemini
     --skills-dir skills-local --memory-dir topics`).
   - Keep `~/.gemini/GEMINI.md`, project `GEMINI.md`, `~/.gemini/rules/*.md`, and any read-only
     upstream symlinked `SKILL.md` targets untouched (`0` bytes added).
   - Store any operator-approved post-port runtime refinements exclusively inside
     `~/.gemini/skill-overlays/<name>.md` as non-canonical deltas—never edit canonical files in place.
2. **Ambient Semantic Context (`R1`)**:
   - Install `knowledge/ambient-context/ppa-*.md` into semantic-retrieval topic storage
     (`memory/topics/ppa-*.md` by default) with a `description:` frontmatter line lifted verbatim from
     the file's canonical `<!-- @description: ... -->` directive, and list the 7 file names in
     `discovery_entries`. `C4.3` compares these descriptions with each other and with the skill
     descriptions.
   - Where semantic topic matching is not active, apply the `R1 -> R2` fallback of §3.1 instead:
     install each file as `skills-local/ppa-program-analysis/references/ambient-<slug>.md` and link it
     from the router (`C3.1`, `C3.9`).

### 3.3 Target 3: Codex / Standard `AGENTS.md` + `.agents/skills/` Harnesses

1. **Target filesystem layout** (`adapters/agents_md_adapter.py`):
   ```text
   <port_root>/
     port_manifest.json
     .agents/
       skills/
         ppa-program-analysis/{SKILL.md, references/*.md, references/ambient-<slug>.md,
                               evals/cases.yaml, README.md, SUGGESTED_FIXES.md}
         ... (the 6 other canonical skill directories, each with SKILL.md, references/*.md,
              evals/cases.yaml, README.md, SUGGESTED_FIXES.md)
       core/
         ontology/{concept_graph.json, concept_graph.schema.json, notation_index.md,
                   cross_paradigm_matrix.md, altitude_alignment_log.md}
         corpus/{RAW_KNOWLEDGE.md, pdf_page_map.json, shards/RAW_SHARD_*.md}
   ```
2. **Channel mapping (`R0`-`R3`)**:
   - `R0`: Root `AGENTS.md` and every pre-existing nested `AGENTS.md` retain identical `sha256_before`
     bytes (`0` added bytes).
   - `R1 -> R2` (`ARCHITECTURE.md` §4.4): the runtime discovers `.agents/skills/` only, so the adapter
     installs each ambient file as `.agents/skills/ppa-program-analysis/references/ambient-<slug>.md`
     and appends `## Orientation Guides (R1 Fallback)` with one link per file to the compiled router
     (`50-99` lines, `C3.1`; mapping kind `transforming`, `C1.8`).
   - `R2` + `R3`: Mirror all 7 canonical skill directories into `.agents/skills/<name>/` and place
     `ontology/` and `corpus/` under `.agents/core/`, outside `.agents/skills/`.
3. **Legacy fallback**: Only where `.agents/skills/` autodiscovery is unavailable may the operator add a
   declared `DEV-STUB` block inside `AGENTS.md` (`<= 12L`, `<= 800B`, naming
   `.agents/skills/ppa-program-analysis/SKILL.md`), with `--emit-dev-stub`; §2.1 governs later builds.

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
   - Rewrite Markdown links `(references/<f>.md)` inside `.mdc` bodies to the relative link
     `(../ppa/skills/<name>/references/<f>.md)` (verified under `C3.7`-`C3.8`), and declare every
     `.mdc` output as `transforming` in `port_manifest.json`.
   - Ambient rules take their `description` verbatim from the canonical `@description` directive and
     are listed in `discovery_entries`; `C4.3` applies to every pair of indexed descriptions.
   - An existing rule file with the stem of an emitted rule (`ppa-router`, `ppa-skill-<slug>`,
     `ppa-ambient-<slug>`) is a foreign file (§2.2) and a `C4.8` collision if overwritten.

### 3.5 Target 5: Knowledge Wiki + NotebookLM Sync (`<wiki_root>/`)

`adapters/wiki_sync_adapter.py` compiles a transforming port into a wiki root that may already hold
the operator's own pages.

1. **Concept and skill pages (`L0`/`L1`/`L3`)**: transformed skill and ambient pages
   (`pages/concepts/ppa-*.md`) plus one concept card (`pages/concepts/ppa-node-<slug>.md`, `<= 250`
   lines) per node of `ontology/concept_graph.json`. A card preserves `formal_summary`, all 4
   `projections` (`[external]` tags intact), one list item per `conditions` entry under
   `## Preconditions & Side Conditions`, `issue_refs`, every edge, and under each `corresponds_to` edge
   the `basis.conditions`, `basis.differs`, and formatted `basis.citations` (a unification edge is never
   shown without its conditions); a `## Provenance` section lists `artifact_refs` and `external_terms`.
   The manifest maps every concept `id` to its card in `concept_cards` (`C1.8`).
2. **Source digests (`L3`)**: chunked `<= 450L` reference and shard pages (`pages/sources/ppa-ref-*.md`
   and `pages/sources/ppa-shard-<unit>-part<NN>.md`) from the canonical references and
   `corpus/shards/RAW_SHARD_*.md`, plus lossless mirrors under `core/`.
3. **PPA-namespaced navigation (owned by the port)**: `pages/ppa_index.md` (`<= 250` lines) links
   every entry page, the per-unit card indexes `pages/concepts/ppa-index-<unit>.md`, and the source
   indexes `pages/sources/ppa-index-refs.md` and `pages/sources/ppa-index-shards.md`;
   `pages/ppa_log.md` records the synchronised revision. Every owned page is reachable from
   `pages/index.md` (`C3.9`).
4. **Root index and log (owned by the operator)**: `pages/index.md` and `pages/log.md` are merged,
   never replaced. The adapter inserts or updates exactly one block delimited by the lines
   `<!-- PPA_KNOWLEDGE_START -->` and `<!-- PPA_KNOWLEDGE_END -->` (links to `pages/ppa_index.md`,
   `pages/ppa_log.md`, and the skill pages in the index; one synchronisation line in the log) and
   leaves every byte outside the block as it was. When a file does not exist the adapter creates it
   with a one-line heading and the block. Unbalanced or repeated markers abort the run. The manifest
   records each block under `bounded_blocks` (line count and SHA-256, `CONFORMANCE_SPEC.md` §2.1):
   a line added, removed, or changed inside the block fails `C1.8` with `C1_BOUNDED_BLOCK_TAMPERED`,
   an edit outside the block never changes the verdict, and recompiling restores the block.
5. **Configuration**: `wiki_config.json` is merged: keys other than `ppa` are preserved, and `ppa`
   records `canonical_revision`, `index` (`pages/ppa_index.md`), `log`, `index_pages`,
   `concept_pages`, `source_pages`, `notebooklm_bundle`, and `bundle_manifest`. Every recorded path
   exists in the port.
6. **NotebookLM sync**: the source shards and `ontology/notation_index.md` are copied into the bundle
   directory, `notebooklm_sources_bundle/` by default. `--bundle-dir <relative path>` (for example
   `--bundle-dir raw/ppa_notebooklm_bundle`) selects another directory inside the port root; the
   bundle files, `bundle_manifest.json` (which lists exactly the files written by this run), and
   `wiki_config.json` all use that path. Never move bundle files after compilation: rerun the adapter
   (`ARCHITECTURE.md` `R-CORE-3`).
7. **Always-on surfaces**: `system_prompt.md`, `templates/default.md`, and any other
   `templates/default*` file stay byte-identical (`C2.2`, `C2.6`).

### 3.6 Target 6: MCP / Graph-RAG / Vector-RAG Servers (`DEV-NOFILES`)

No reference adapter exists for this target; the port is certified from its own manifest and evidence.

0. **Certification inputs** (`CONFORMANCE_SPEC.md` §2.1-§2.3):
   - `port_manifest.json` with `"target": "mcp-graph-rag"`, `"deviations": ["DEV-NOFILES"]`, the two
     literal minimum surfaces of §2 (`system_prompt.md`, `templates/always.md`), `discovery_entries`,
     `pre_existing_discovery`, and one `mappings` entry per canonical `knowledge/` and `ontology/` file
     whose `port` lists `ppa:` identifiers (or a file path for anything kept on disk, such as the graph).
   - `served_units.json` in the port root: `{"<ppa: identifier>": ["line", "..."]}` with the exact
     content served for every identifier named in `mappings` or `concept_cards`.
   - `corpus_root` naming the on-disk copy of `corpus/`, so `artifact_refs` into `corpus/` resolve (`C3.11`).
   - A second build of the port passed as `--port-second <dir>`: without it `C5.7` fails, because
     there is no adapter the verifier could run twice.
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

Every port MUST emit `<port_root>/port_manifest.json` (or `<port_root>/<name>.json` when compiled
with `--manifest-name`, §2.2) conforming to `CONFORMANCE_SPEC.md` §2:

1. **Deterministic serialization (`C5.7`)**: Walk canonical source directories in sorted ASCII order,
   normalize line endings to LF (`N5`), sort JSON keys (`N7`), and exclude wall-clock timestamps,
   random identifiers, hostnames, and absolute workstation paths (`C5.3`).
2. **Complete `mappings` closure (`C1.12`)**: Every file under canonical `knowledge/` and `ontology/`
   MUST appear in `mappings` exactly once with `kind` set to `"lossless"` (matching `N6` SHA-256)
   or `"transforming"` (`.mdc` rules, wiki pages, router-embedded ambient files, or `DEV-NOFILES` resources).
3. **Worked manifest example** (every key is specified in `CONFORMANCE_SPEC.md` §2.1; the lists are
   abbreviated here):
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
       {"path": ".cursorrules", "sha256_before": null, "bytes_before": null}
     ],
     "discovery_entries": [
       {"name": "ppa-program-analysis", "description_chars": 412},
       {"name": "ppa-foundations.md", "description_chars": 540}
     ],
     "pre_existing_discovery": [],
     "corpus_root": ".cursor/ppa/corpus",
     "extra_units": [".cursor/ppa/corpus/RAW_KNOWLEDGE.md", ".cursor/ppa/corpus/pdf_page_map.json"],
     "index_files": [],
     "manifest_files": ["port_manifest.json"],
     "merged_files": [],
     "deviations": []
   }
   ```
   Required beyond the minimum of `CONFORMANCE_SPEC.md` §2: `pre_existing_discovery` (use `[]` for an
   empty target; a missing key fails `C4.8`) and `corpus_root` whenever a concept cites `corpus/` in
   `artifact_refs` (without it `C3.11` fails). A hand-built port lists every file it owns that is not
   a mapping target in `extra_units`, `index_files`, `manifest_files`, or `notebooklm_bundle`: only
   owned files are certified. `adapter_options` is written by reference adapters and replayed by
   `C5.7`; a port built without a reference adapter omits it and passes `--port-second`.
   For `mcp-graph-rag`, populate `"deviations": ["DEV-NOFILES"]`, record resource identifiers
   (`ppa:skills/...`) inside `mappings[*].port`, and supply `served_units.json` (§3.6). For `DEV-STUB`,
   record `"deviations": [{"id": "DEV-STUB", "surface": "AGENTS.md", "text": "..."}]`. A wiki port
   additionally records `concept_cards`, `notebooklm_bundle`, and its `merged_files`.
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

The first command scans a whole directory and is meaningful for a dedicated staging root; inside a
project root that holds other files, rely on the verifier, which reads only the files the manifest
owns (`CONFORMANCE_SPEC.md` §2.2). Verifier options: `--user-home <dir>` (the user scope given to the
compiler), `--port-second <dir>` (second build for `C5.7`; required for a target without a reference
adapter), `--denylist <file>` (`C5.5`), `--external-export <file>` (`C6.10`), `--scratch-dir <dir>`.
Its summary line states exact counts (`55/55 evaluated checks PASS`, or the number and the codes of
the failed checks).

### 6.1 Verdict Handling and Remediation Matrix (`CONFORMANCE_SPEC.md` §§4-6)

| Verdict / Exit | Failure Codes | Mandatory Action (`ARCHITECTURE.md` `R-CORE-3`) |
| :--- | :--- | :--- |
| `CONFORMANT` (`0`) | None (`deviations == []`) | Publish `<port_root>/port_manifest.json` + `conformance_report.json` |
| `CONFORMANT_WITH_DEVIATIONS` (`2`) | None (`DEV-STUB` / `DEV-NOFILES` only) | Verify every recorded deviation in `conformance_report.json` is operator-approved |
| `NON_CONFORMANT` (`1`) | `C5_*` (`C5_HARNESS_TERM_IN_CORE`, `C5_ABSOLUTE_PATH`, `C5_HOST_OR_CONTACT`) | Remove leaked paths/tokens from canonical source or adapter config; rebuild |
| `NON_CONFORMANT` (`1`) | `C5_SYMLINK_FORBIDDEN`, `C5_OWNED_PATH_INVALID` | Replace the symbolic link at the reported owned path with a regular file by recompiling; keep manifest paths relative and inside the port root |
| `NON_CONFORMANT` (`1`) | `C1_*` (`C1_PACKAGE_INCOMPLETE`, `C1_CITATION_MULTISET`, `C1_TRANSFORM_CONTENT_LOSS`, `C1_CONDITIONS_PARITY`, `C1_GOTCHA_DROPPED`) | Restore missing package files, citations, body lines, headings, condition entries, or ledger pointers in the adapter template |
| `NON_CONFORMANT` (`1`) | `C1_TRANSFORM_UNAPPROVED_LINE`, `C1_BOUNDED_BLOCK_TAMPERED` | Recompile: a transforming unit carries a line outside the canonical file and the scaffolding allowlist (`CONFORMANCE_SPEC.md` §3.2), or a bounded block was edited after the build |
| `NON_CONFORMANT` (`1`) | `C2_*` (`C2_SURFACE_MODIFIED`, `C2_UNDECLARED_DEVIATION`, `C2_INSTALLED_ALWAYS_ON`, `C2_NONZERO_TAX`) | Revert modified `always_on_surfaces`; declare or remove a pointer stub; move `R1` to `R2` or set `alwaysApply: false` |
| `NON_CONFORMANT` (`1`) | `C3_*`, `C4_*`, `C6_*` | Fix broken rewritten links, unlinked ambient files (`C3_ORPHAN_FILE`), exceeded budgets (`T1` refactor upstream), name collisions, or manifest order |
| `NON_CONFORMANT` (`1`) | `MANIFEST_MISSING`, `MANIFEST_SPEC_VERSION`, `MANIFEST_DEVIATION_ILLEGAL` | Supply `port_manifest.json` with `spec_version` `"1"` and only the deviations of §2.1 |

Never patch a generated port file manually to silence a check (`R-CORE-3`): fix the **canonical core**
or **compiler adapter** and recompile cleanly. Certify reproducibility (`C5.7`) by compiling to two
separate roots (`<port_a>`, `<port_b>`) and passing the second as `--port-second`. Certify clean
uninstall by removing every owned file (`mappings` targets, `extra_units`, `index_files`,
`manifest_files`, `notebooklm_bundle`, the tree under `corpus_root`, and the report), deleting the
bounded block from each entry of `merged_files`, and verifying every declared `always_on_surfaces`
path matches `sha256_before`.
