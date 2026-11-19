<!-- @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006 -->
<!-- @decision DEC-PPA-001: Conformance is certified by six binary, machine-verifiable gates evaluated over the canonical core and a declared port manifest; no gate depends on a model, a harness, or a subjective score. -->

# CONFORMANCE_SPEC: Certifying a Port of the PPA Semantic Knowledge Distribution

## 0. Purpose and Scope

This specification lets any agent or engineer who ports `knowledge/` and `ontology/` to another agent
harness determine, deterministically, whether the port is conformant. It defines six gates (`C1`-`C6`),
each a set of numbered checks with a binary outcome. A check either passes with recorded evidence or
fails with a failure code and a location. There are no scores, thresholds of quality, or waivers
outside the two deviations named in §6.

Out of scope: whether the content is *true to the book* in meaning. That is certified upstream by
independent adversarial review against the five anti-degradation contracts in
`architecture/ARCHITECTURE.md` §7. Conformance certifies that a port *preserved* what was certified.

## 1. Definitions

| Term | Meaning |
| :--- | :--- |
| Canonical core | The directories `knowledge/`, `ontology/`, `corpus/`, and `issues/` of this repository at a recorded revision |
| Port | The file tree (or served resource set) produced for one target harness |
| Port root | The directory under which the port is installed |
| Always-on surface | Any file or text that the target injects into every session regardless of task |
| Discovery metadata | The `name` and `description` a target indexes to decide whether to load an artifact |
| Lossless mapping | One canonical file maps to one port file with an identical normalised body |
| Transforming mapping | One canonical file maps to several port units (chunks, nodes, resources), or several to one |
| Port manifest | `port_manifest.json` (or another `*.json` name in the port root, §2.2), written by the porter, declaring the mapping and the target's surfaces |
| Package | Every skill directory (with its `references/` and `evals/`) and every ambient file under `knowledge/`, installed as a whole |

## 2. Inputs

1. **Canonical core** at a recorded revision identifier.
2. **Port root** after installation, and a snapshot of every always-on surface taken *before*
   installation.
3. **Port manifest** with at least:

```json
{
  "spec_version": "1",
  "target": "<public harness name>",
  "canonical_revision": "<revision id>",
  "mappings": [{"canonical": "<relative path>", "port": ["<relative path>"], "kind": "lossless|transforming"}],
  "always_on_surfaces": [{"path": "<path as the target defines it>", "sha256_before": "<hex or null>", "bytes_before": null}],
  "discovery_entries": [{"name": "<name>", "description_chars": 0}],
  "pre_existing_discovery": [],
  "corpus_root": "<port-relative directory holding the copy of corpus/>",
  "deviations": []
}
```

A port without a manifest is `NON_CONFORMANT` by definition: nothing can be verified against it.
A port that installs only part of the package is `NON_CONFORMANT` (`C1.12`): links between skills'
reference files assume that the whole package is present.

### 2.1 Manifest Keys

Every path in the manifest is relative to the port root, uses `/` separators, and contains no `..`
component; a served unit is named by a `ppa:` resource identifier instead of a path.

| Key | Required | Meaning | Read by |
| :--- | :--- | :--- | :--- |
| `spec_version` | Yes | The string `"1"`; any other value fails manifest check `M.1` | §5 |
| `target` | Yes | Public harness name; selects the minimum surface set of `PORTING_GUIDE.md` §2 | `C2.1`, `C5.7` |
| `canonical_revision` | Yes | Revision identifier of the canonical core the port was compiled from | `C5.7`, report |
| `mappings` | Yes | One entry per canonical file under `knowledge/` and `ontology/`; `port` lists the file paths or `ppa:` identifiers that carry it | `C1.7`, `C1.8`, `C1.12`, `C3`, `C4` |
| `always_on_surfaces` | Yes | Each surface with the digest taken before installation; `sha256_before` is `null` for an absent surface. `bytes_before` (total size, `null` when absent) is informative | `C2.1`, `C2.2`, `C2.6` |
| `discovery_entries` | Yes | Names the target indexes for this port and the length of each indexed description. Ambient file names appear here only when the target indexes ambient files by description (an `R1` channel) | `C2.4`, `C2.5`, `C3.9`, `C4.3`, `C4.8` |
| `pre_existing_discovery` | Yes | Discovery names found in the target before installation (`[]` when none). A missing key fails `C4.8`: an absent list is not evidence of an empty target | `C4.8` |
| `corpus_root` | Yes when a concept cites `corpus/` in `artifact_refs` | Directory holding the port's copy of canonical `corpus/`; an `artifact_refs` entry `corpus/<x>` resolves to `<corpus_root>/<x>`. Every file below it is owned by the port | `C3.11`, §2.2 |
| `deviations` | Yes | `[]`, or the deviations of §6: the string `"DEV-NOFILES"`, or the object `{"id": "DEV-STUB", "surface": "<path>", "text": "<exact stub>"}`. Anything else fails manifest check `M.2` | §5, §6 |
| `extra_units` | No | Owned files that are not the target of a mapping: compiled concept cards, chunked source pages, the corpus copy | §2.2 |
| `index_files` | No | Owned navigation files generated by the port (indexes, logs) | §2.2, `C3.4`, `C3.9` |
| `manifest_files` | No | Owned metadata files (the manifest itself, a bundle manifest, `served_units.json`) | §2.2 |
| `notebooklm_bundle` | No | Owned files of an ingestion bundle | §2.2 |
| `merged_files` | No | Operator-owned files in which the port maintains one bounded block between the lines `<!-- PPA_KNOWLEDGE_START -->` and `<!-- PPA_KNOWLEDGE_END -->` (or, for a declared `DEV-STUB`, the stub). Only the block is read; the rest of the file is the operator's | `C3.7`-`C3.9` |
| `bounded_blocks` | Yes when the port maintains a bounded block | Object mapping each file that carries the port's bounded block (a `merged_files` entry, or a page the port generated around the block) to `{"lines": <n>, "sha256": "<hex>"}`: the number of lines from the start-marker line through the end-marker line, and the SHA-256 of those lines joined by line feeds with one final line feed | `C1.8` |
| `concept_cards` | Yes when the port compiles one unit per concept node | Object mapping each concept `id` to its card (path or `ppa:` identifier) | `C1.8` |
| `adapter_options` | No | Keyword options of the reference adapter that built the port; replayed when `C5.7` rebuilds it | `C5.7` |

### 2.2 Certification Scope: Owned Files

In a port certification every check that reads port content reads **owned files only**: the `port`
paths of `mappings`, the entries of `extra_units`, `index_files`, `manifest_files`, and
`notebooklm_bundle`, the manifest file itself, and every file under `corpus_root`. Any other file
in the port root is foreign: it is not read, not scanned, and cannot change the verdict, so a port
installed in a project root that holds unrelated files certifies on its own content. A symbolic
link at an owned path, or at any directory component of one, fails `C5.1` with
`C5_SYMLINK_FORBIDDEN`; a manifest path that is absolute or leaves the port root fails `C5.1` with
`C5_OWNED_PATH_INVALID`. Foreign symbolic links are ignored. A symbolic link inside the canonical
core fails every gate with `C5_SYMLINK_FORBIDDEN`. None of these conditions aborts the run: each is
a recorded failure in the report.

**Several ports in one root.** The manifest is named `port_manifest.json` unless the port was
compiled under another `*.json` name (reference adapters: `--manifest-name <name>`; verifier:
`--manifest <name>`). A manifest owns only what it lists, so ports whose owned paths do not overlap
share a root without affecting each other: each is compiled, recompiled, and certified from its own
manifest, and a manifest written for another target never confers ownership. The report is written
next to the manifest as `conformance_report.json`; for a manifest named `port_manifest<x>.json` it
is `conformance_report<x>.json`, and for any other name `<n>.json` it is
`conformance_report_<n>.json`.

### 2.3 Verifier Inputs Outside the Manifest

| Input | Meaning |
| :--- | :--- |
| User scope for `~/` surfaces | A surface path beginning `~/` is resolved against, in order: the `--user-home` option, the `PPA_USER_HOME` environment variable, the directory `<port_root>/.user_home` if it exists, the home directory of the invoking user. The adapter and the verifier MUST be given the same user scope |
| Glob surfaces | A surface containing `*`, `?`, or `[` denotes every matching regular file. Its digest is the SHA-256 of the concatenation, in sorted path order, of one line `<path relative to the scope root>:<SHA-256 of the file>` terminated by a line feed; no match is `null` |
| `--manifest <name or path>` | The manifest to certify. A bare file name is read from the port root (default `port_manifest.json`); any other value is a path |
| `--report-out <file>` | Where to write the report instead of the default of §2.2 (`--report` is the same option) |
| `--port-second <dir>` | A second build of the same port in another root, compared file for file under `C5.7`. Required when the manifest `target` has no reference adapter |
| `--denylist <file>` | Operator denylist for `C5.5` |
| `--external-export <file>` | Tracker synchronisation record for `C6.10` |
| `--scratch-dir <dir>` | Where `C5.7` rebuilds a port when a reference adapter exists |
| `served_units.json` | For a `DEV-NOFILES` port: a JSON object in the port root mapping each served `ppa:` identifier to its content as an array of lines (`{"ppa:concepts/<name>.md": ["line 1", "line 2"]}`; a single string is also accepted). It is the evidence the verifier reads in place of files for `C1.8`, `C2.5`, `C3.1`-`C3.4`, `C3.6`, `C3.9`, `C3.11`, and `C4` |

## 3. Normalisation Rules

| ID | Rule |
| :--- | :--- |
| `N1` | Text is decoded as strict UTF-8 with no replacement of invalid bytes; a file that fails to decode fails the check that reads it |
| `N2` | Line count is taken on the whole file, frontmatter included: after converting CRLF to line feed, the number of line-feed-terminated lines, plus one if the final line is unterminated. No other character (form feed, vertical tab, Unicode line or paragraph separator) ends a line |
| `N3` | A frontmatter delimiter is a line that reads `---` once a leading byte-order mark and trailing whitespace are ignored. Frontmatter is the block from a delimiter on the first line through the next delimiter; a file whose first line is not a delimiter has none. A repeated key inside frontmatter is an error |
| `N4` | Body is the file with frontmatter removed |
| `N5` | Normalised body: line endings converted to line feed, trailing whitespace removed per line, trailing blank lines removed |
| `N6` | Digest is the lowercase hexadecimal SHA-256 of the UTF-8 normalised body |
| `N7` | JSON is compared after parsing, with object keys sorted and arrays compared in order unless a check says "as a set" |
| `N8` | An inline citation is the token `[PPA <locator>, p. <page>]`, citing the first page of the item, or `[PPA <locator>, pp. <A>-<B>]` (hyphen or en dash) for a span: both ends must resolve, `A ≤ B`, and the span is at most 15 pages. Locators and their resolution are in §3.1 |

### 3.1 Inline Citation Grammar (`N8`)

| Locator | Page | Resolves when |
| :--- | :--- | :--- |
| Section: `§2.1`, `§A.1`, or `§2.1.3` (`§` optional; title may follow) | Arabic book page | The page lies in the range the page map records for the section named by the first two numbers (`N.M`, with chapter `1`-`6` or appendix `A`-`C`). The range ends where the next heading begins; that page is included only when the heading starts mid-page (`shares_last_page`) |
| `Table N.M`, `Figure N.M` (`N` is `1`-`6` or `A`-`C`) | Arabic | The item is in the closed inventory and its caption is on the cited page or an adjacent page |
| Numbered statement: `Lemma`, `Theorem`, `Proposition`, `Corollary`, `Fact`, `Example`, `Exercise`, or `Mini Project`, followed by `N.M` (`N` is `1`-`6` or `A`-`C`) | Arabic | The item is in the `statements` inventory of the page map and the page lies between its heading page and the page of the next numbered item (`C1.11`) |
| Region: `Chapter N` or `Appendix X`, optionally followed by a part name (`Concluding Remarks`, `Mini Projects`, `Exercises`) | Arabic | The page lies in the region, and in the `end_matter` range of the named part |
| Front matter: `Preface`, `Contents`, `List of Tables`, `List of Figures` | Roman label as printed, e.g. `[PPA Preface, p. VI]` | The label is the printed label of a PDF page inside that front-matter range |
| Back matter: `Index of Notation`, `Index`, `Bibliography`; a bibliography entry `[N]` | Arabic | The page lies in the range; an entry is on its recorded page or the next |

Any other token that begins `[PPA` or `(book p` is malformed and fails `C1.10`. The companion form
`(book p. X; PDF p. Y)` is valid when the page map maps book page `X` to PDF page `Y`.

### 3.2 Substantive Body Lines (`C1.8`)

A substantive body line of a canonical file is a line that remains after removing: frontmatter
(`N3`), blank lines, HTML comments, Markdown headings, code-fence delimiter lines, and table
separator rows. Lines inside a code fence are substantive. Each line is normalised by reducing
every Markdown link to its bracketed label (the parenthesised target is dropped) and collapsing each
run of whitespace to one space. A heading is compared by its normalised text without the `#` prefix.
Every port unit of the mapping is classified and normalised the same way, line by line, and the
comparison is exact in both directions: a port may rewrite link targets and re-level headings, but
may not drop, alter, extend, merge, split, or add a substantive line or a heading.

**Scaffolding allowlist.** Besides the canonical lines, a port unit may carry only:

1. YAML frontmatter at the top of the unit whose keys are `name`, `description`, `globs`, or
   `alwaysApply`, with indented continuation lines under `description` only.
2. The comment lines `<!-- skill: <name> -->` and `<!-- summary: <description> -->` repeating the
   canonical frontmatter values, the two bounded-block marker lines, and any comment line that
   occurs in the canonical file.
3. In the unit that carries the router skill only: the heading `Orientation Guides (R1 Fallback)`
   and, per canonical ambient file, one list item whose only content is a link labelled with that
   file's name, each once.

Any other line is unapproved, wherever it sits (body, comment, frontmatter, or code fence).

## 4. Gates

### `C1` Concept, Citation, and Table/Figure Conservation

Intent: nothing the canonical core knows is lost, renumbered, or detached from its coordinate.

| Check | Procedure | Pass condition | Failure code |
| :--- | :--- | :--- | :--- |
| `C1.1` | Collect concept `id` values from the canonical graph and from the port's graph or node set | The two sets are equal | `C1_CONCEPT_SET` |
| `C1.2` | For each `id`, compare `title`, `altitude`, `unit`, `citations`, `formal_summary`, `projections`, `related_edges`, `artifact_refs` under `N7` | Equal; a port MAY add fields and MAY rewrite `artifact_refs` paths through the manifest mapping, nothing else | `C1_NODE_DRIFT` |
| `C1.3` | For each citation, look up its page in `corpus/pdf_page_map.json` (book page, or printed label for front matter) | The recorded `pdf_page` equals the mapped one; a non-empty `table_or_fig` is a key of `tables` or `figures` whose caption is on that page or an adjacent page; the locator resolves under §3.1 | `C1_CITATION_UNRESOLVED` |
| `C1.4` | Count keys of `tables` and `figures` in the page map, grouped by `chapter_or_app` | Tables total 51 as 6, 10, 10, 0, 18, 6 for Chapters 1-6 and 1 for Appendix C; figures total 56 as 3, 23, 6, 10, 2, 6 for Chapters 1-6, 3 for Appendix A, 3 for Appendix C | `C1_INVENTORY_COUNT` |
| `C1.5` | For each table and figure key, search concept citations in the port | Every key is cited by at least one concept | `C1_ITEM_UNCITED` |
| `C1.6` | For each entry of `sections` in the page map, search concept citations in the port | Every section is cited by at least one concept; a citation of a subsection (`2.1.3`) covers the section named by its first two numbers (`2.1`) | `C1_SECTION_UNCOVERED` |
| `C1.7` | For each lossless mapping, compute `N6` on both sides | Digests are equal | `C1_BODY_DIGEST` |
| `C1.8` | For each transforming mapping: (a) collect inline citations (`N8`) and concept `id` mentions on both sides as multisets; (b) classify both sides under §3.2 and compare the multisets of substantive body lines and of heading texts, then check every other port line against the scaffolding allowlist; (c) for each compiled concept card (`concept_cards`), compare the card with its graph node; (d) inspect the graph's `conditions` and `corresponds_to` `basis` objects; (e) for each `bounded_blocks` entry, recompute the record of the block now in the file | (a) the multisets are equal; (b) no canonical line or heading is missing from the port, and the port carries no line beyond the canonical ones and the allowlist; (c) the card section headed `Preconditions & Side Conditions` carries exactly one list item per `conditions` entry, each reproducing the entry, and its `Related Edges` section reproduces every `basis.conditions` and `basis.differs` entry of each `corresponds_to` edge; (d) every `conditions` entry is a non-empty single-line string unique within its node, and every `basis` has a `unification_id` and non-empty `citations`, `conditions`, `differs`; (e) the record equals the manifest entry, the file holds exactly one block, and a `merged_files` entry that carries a block marker is declared in `bounded_blocks` (text outside the block is never compared) | The first that applies: `C1_CITATION_MULTISET` for (a), `C1_TRANSFORM_CONTENT_LOSS` for a missing line or heading in (b), `C1_TRANSFORM_UNAPPROVED_LINE` for an added line in (b), `C1_BOUNDED_BLOCK_TAMPERED` for (e), `C1_CONDITIONS_PARITY` for (c) and (d) |
| `C1.9` | Collect gotcha-ledger ids from the canonical `corpus/` and search the port and `issues/` | Every id is referenced by a port artifact, a backlog item, or a recorded exclusion. Until the whole-book audit an unreferenced id is reported as a warning; from that audit on, and in any port certification, it fails | `C1_GOTCHA_DROPPED` |
| `C1.10` | Collect every token that begins `[PPA` or `(book p` in every Markdown file of the core and the port | Every token matches the grammar of §3.1 in full | `C1_CITATION_MALFORMED` |
| `C1.11` | For each numbered-statement locator, look up the `statements` inventory of the page map | The kind word and number name an inventoried item and the page lies in its span (§3.1) | `C1_STATEMENT_UNKNOWN` |
| `C1.12` | Compare the files under canonical `knowledge/` and `ontology/` with the manifest `mappings` | Every canonical file appears in exactly one mapping | `C1_PACKAGE_INCOMPLETE` |

### `C2` Zero Always-On Prompt Tax Bloat

Intent: installing the port adds nothing to what every session pays for.

| Check | Procedure | Pass condition | Failure code |
| :--- | :--- | :--- | :--- |
| `C2.1` | The manifest's `always_on_surfaces` is compared with the minimum set for the target in `architecture/PORTING_GUIDE.md` | The declared set is a superset of the minimum set | `C2_SURFACE_UNDECLARED` |
| `C2.2` | For each declared surface, compute SHA-256 of the raw bytes after installation, and search it for a pointer-stub marker (the line `<!-- PPA_STUB_START -->` or the heading `# PPA On-Demand Knowledge Index`) | Equal to `sha256_before`; a surface absent before is absent after; a surface that carries a stub marker is named by a declared `DEV-STUB` (§6) | `C2_SURFACE_MODIFIED`; `C2_UNDECLARED_DEVIATION` for a stub with no declared deviation |
| `C2.3` | Inspect every installed file for the target's unconditional-load marker or location | No installed file is itself an always-on surface (for rule-file targets, the unconditional flag is `false`) | `C2_INSTALLED_ALWAYS_ON` |
| `C2.4` | Enumerate discovery entries the target indexes for this port | The set of names equals the canonical skill names (plus ambient file names if the target indexes them); nothing else is indexed | `C2_DISCOVERY_SET` |
| `C2.5` | Measure each indexed `description` | At most 1,024 characters each; no description contains a definition, rule, or procedure step (it contains no inline citation under `N8` and no numbered list) | `C2_DESCRIPTION_BLOAT` |
| `C2.6` | Sum bytes added to always-on surfaces | Exactly 0 | `C2_NONZERO_TAX` |

### `C3` Progressive-Disclosure Link Integrity, Frontmatter Hygiene, and Line Ceilings

Intent: every artifact stays within its altitude budget and every disclosure hop resolves. Every line
count in this gate is taken on the whole file, frontmatter included (`N2`).

| Check | Procedure | Pass condition | Failure code |
| :--- | :--- | :--- | :--- |
| `C3.1` | Apply `N2` to the router `SKILL.md` | At least 50 and fewer than 100 lines | `C3_ROUTER_BUDGET` |
| `C3.2` | Apply `N2` to each non-router `SKILL.md` | At least 250 and fewer than 500 lines | `C3_SKILL_BUDGET` |
| `C3.3` | Apply `N2` to each `references/*.md` | At most 450 lines | `C3_REFERENCE_CEILING` |
| `C3.4` | Apply `N2` to each `ambient-context/ppa-*.md` | Between 80 and 250 lines inclusive | `C3_AMBIENT_BUDGET` |
| `C3.5` | Parse frontmatter (`N3`) of each `SKILL.md` | Keys are exactly `name` and `description`; `name` equals the directory name, matches `^ppa-[a-z0-9]+(-[a-z0-9]+)*$`, and is at most 64 characters | `C3_FRONTMATTER_KEYS` |
| `C3.6` | Read the first line of each `references/*.md`, each file under `corpus/`, and `ontology/*.md` | The first line is not a frontmatter delimiter under `N3` (zero YAML frontmatter) | `C3_FRONTMATTER_FORBIDDEN` |
| `C3.7` | Extract every relative Markdown link and fragment from every knowledge file | The target file exists inside the port; a fragment matches a heading in the target | `C3_LINK_BROKEN` |
| `C3.8` | Classify each link by source and target | No link from a reference to any `SKILL.md`; no link from any skill's files, the router's included, to another skill's `SKILL.md` (skills refer to each other by `name`); links into another skill's `references/` are allowed; no link resolves outside the port | `C3_LINK_DIRECTION` |
| `C3.9` | Check reachability of `SKILL.md`, `references/*.md`, and ambient units | Every non-router skill `name` occurs in the router file; every reference is linked from the `SKILL.md` of its own skill. In the canonical core, and in a port whose `discovery_entries` list the ambient file names, ambient files are independent entry points and need no inbound link. In any other port no channel indexes them, so each ambient unit MUST be the target of a link from another port unit (the router, or an index page). `evals/` files are data and need no inbound link. In a port with `pages/`, every owned page is reachable from `pages/index.md` | `C3_ORPHAN_FILE` |
| `C3.10` | For each skill, the router included, open `evals/cases.yaml` | The file exists and each case has `id`, `prompt`, and `expect_skill`; optional keys are limited to `must_mention`, `must_not_mention`, `notes` | `C3_EVALS_SHAPE` |
| `C3.11` | For each `artifact_refs` entry in the graph, resolve through the manifest mapping | The entry list is non-empty or the node records an exclusion; each file exists; a fragment, if present, matches a heading | `C3_ARTIFACT_REF` |
| `C3.12` | Enumerate every file under `knowledge/` | Each is `skills/<name>/SKILL.md`, `skills/<name>/references/<file>.md` (no subdirectories), `skills/<name>/evals/cases.yaml`, `skills/<name>/README.md`, `skills/<name>/SUGGESTED_FIXES.md`, or `ambient-context/ppa-<slug>.md` | `C3_UNKNOWN_FILE` |

A transforming port that has no files (for example, a served graph) evaluates `C3.1`-`C3.4` on the
unit sizes it serves per request and `C3.7`-`C3.9` on its resource links.

Scope of `C3.12`: the closed-tree rule is evaluated on the canonical `knowledge/` directory only. A
port is free to lay files out as its target requires (for example an ambient file installed as
`<router>/references/ambient-<slug>.md`); its layout is constrained by the manifest (`C1.12`, §2.2),
not by `C3.12`.

### `C4` Sibling Skill Trigger Disambiguation and Negative Boundaries

Intent: for any task, at most one skill claims it, and each skill says what it is not for.

| Check | Procedure | Pass condition | Failure code |
| :--- | :--- | :--- | :--- |
| `C4.1` | Read each skill `description` | It contains a positive trigger clause introduced by `Use when` and a negative clause introduced by `Do not use` or `Don't use` | `C4_BOUNDARY_MISSING` |
| `C4.2` | Inspect each negative clause | It names at least one other non-router skill by its exact `name`, matched on token boundaries, as the correct alternative | `C4_NO_REDIRECT` |
| `C4.3` | Tokenise each indexed description into lowercase runs of letters and digits of length four or more, excluding `ppa`; compute pairwise Jaccard similarity of the token sets. The indexed descriptions are those of every skill, the router included, and of every ambient file: in the canonical core the `@description` directive each ambient file declares, in a port the description of each ambient entry the port indexes | Strictly below 0.50 for every pair of indexed entries | `C4_DESCRIPTION_OVERLAP` |
| `C4.4` | Read the router file | Every sibling skill name appears in exactly one routing row; each row has a discriminator and a negative route | `C4_ROUTER_INCOMPLETE` |
| `C4.5` | Read each skill's `evals/cases.yaml` | At least three cases with `expect_skill` equal to the skill, and at least two with `expect_skill` equal to a sibling or `none` | `C4_EVAL_COVERAGE` |
| `C4.6` | Compare `prompt` text across all eval files after `N5` | No identical prompt has two different `expect_skill` values | `C4_EVAL_CONTRADICTION` |
| `C4.7` | For every graph edge with relation `corresponds_to` (it carries `basis.unification_id`, `ARCHITECTURE.md` §6.3), find the skill owning each endpoint through the endpoint's `artifact_refs`; keep the pairs of two distinct non-router skills | Each of the two eval files contains at least one case whose `expect_skill` is the other skill | `C4_ISOMORPHISM_BOUNDARY` |
| `C4.8` | Read `pre_existing_discovery` and derive the names the port emits for its target: the directory name of every mapped `SKILL.md`, the stem of every mapped rule file, and every `discovery_entries` name | The key is present; no pre-existing name equals an emitted name; every canonical skill name is a discovery entry (the port renames nothing). A collision recorded by an earlier build stays recorded when the port is rebuilt | `C4_NAME_COLLISION` |

### `C5` Zero Host/Vendor Identifier Leakage

Intent: the canonical core is harness-agnostic, and neither the core nor the port carries the
identity of any machine, organisation, or product it passed through.

| Check | Procedure | Pass condition | Failure code |
| :--- | :--- | :--- | :--- |
| `C5.1` | Run the repository hygiene gate (`scripts/check_portability_hygiene.py`) over the canonical core and the owned files of the port (§2.2) | Zero findings; no owned path is or passes through a symbolic link; every manifest path stays inside the port root | `C5_HYGIENE_GATE`; `C5_SYMLINK_FORBIDDEN`; `C5_OWNED_PATH_INVALID` |
| `C5.2` | Search `knowledge/`, `ontology/`, and `corpus/` for harness product names, harness configuration directory names, harness instruction file names, and model or vendor names | Zero matches; these terms are permitted only under `architecture/`, `adapters/`, and the top-level readme | `C5_HARNESS_TERM_IN_CORE` |
| `C5.3` | Search all port content derived from the canonical core for absolute filesystem paths (a path beginning at a filesystem root or drive letter) | Zero matches | `C5_ABSOLUTE_PATH` |
| `C5.4` | Search for email addresses, and for URLs or host names outside the allowlist recorded with the hygiene gate (the allowlist is empty when none is recorded) | Zero matches | `C5_HOST_OR_CONTACT` |
| `C5.5` | Search for tracker identifiers, short-link forms, and tool names belonging to any private organisation; the porter MUST extend the denylist with the tokens of the porter's own environment before running this check | Zero matches | `C5_PRIVATE_IDENTIFIER` |
| `C5.6` | Search `evals/cases.yaml` files and all `SKILL.md` bodies for conditional instructions addressed to a named model or harness | Zero matches | `C5_MODEL_CONDITIONAL` |
| `C5.7` | Compile the port twice into two different roots. With `--port-second`, the port under test is compared with that second build. Otherwise, if the `target` has a reference adapter, the adapter is run twice with the manifest's `canonical_revision` and `adapter_options`, and the two builds are compared with each other and with the port under test (the manifest file and `merged_files` excepted). A difference between the port under test and the rebuild is reported as `port differs from clean rebuild (post-build edit or nondeterministic adapter)`: the digest comparison cannot tell the two causes apart, and `C1.8` reports an edited transforming unit on its own. A `target` with no reference adapter and no `--port-second` fails | The owned files are byte-identical, file for file | `C5_NONDETERMINISTIC_BUILD` |

### `C6` Lossless Issue and Backlog Provenance

Intent: every decision, refactor, contradiction, and edge case survives export and stays linked to
the content it concerns.

| Check | Procedure | Pass condition | Failure code |
| :--- | :--- | :--- | :--- |
| `C6.1` | Validate every file under `issues/epics/`, `issues/shards/`, `issues/refactors/`, `issues/backlog/` against `issues/SCHEMA.md` | Every required frontmatter key and every required section is present; enumerated values are legal | `C6_SCHEMA` |
| `C6.2` | Collect issue `id` values | Unique; each equals its file name without extension | `C6_ID` |
| `C6.3` | Resolve `parent_issue`, `depends_on`, `blocks` | Every reference names an existing issue; `depends_on` is acyclic; `blocks` is the exact inverse of `depends_on` | `C6_REFERENCE` |
| `C6.4` | Read `issues/export_manifest.json` | It lists every issue exactly once, in an order where each issue follows its parent and its dependencies | `C6_MANIFEST_ORDER` |
| `C6.5` | Reconstruct each issue from the manifest and compare with the file | Frontmatter key-value pairs are equal under `N7`; body digests are equal under `N6` | `C6_MANIFEST_LOSSY` |
| `C6.6` | For each backlog item, read its citations and concept references | At least one citation that passes `C1.3` and at least one existing concept `id` | `C6_BACKLOG_UNGROUNDED` |
| `C6.7` | Search every knowledge file for issue ids | Every id mentioned exists; every open backlog item is mentioned by at least one artifact or concept node | `C6_POINTER` |
| `C6.8` | Inspect `depends_on` of every epic and shard | No epic or shard depends on a backlog item (backlog is non-blocking) | `C6_BACKLOG_BLOCKS` |
| `C6.9` | Compare refactor ids in `ontology/altitude_alignment_log.md` with files under `issues/refactors/` | The two sets are equal | `C6_REFACTOR_TRACE` |
| `C6.10` | If issues were exported to an external tracker, compare with the manifest | Exported count equals manifest count; each exported item carries its canonical `id`; the external number is recorded back one-to-one | `C6_EXPORT_COUNT` |

## 5. Evaluation Order and Evidence

1. Gates are evaluated in order `C5`, `C1`, `C3`, `C2`, `C4`, `C6`. `C5` runs first so that no later
   evidence record can itself carry a leaked identifier.
2. Every check is evaluated even after a failure; the report is complete, not first-failure.
3. Each check records: check id, outcome, the number of items examined, and for a failure the
   failure code plus up to twenty locations (`relative_path:line`).
4. A check that examines zero items FAILS with `<gate>_VACUOUS`, unless the manifest declares the
   corresponding artifact class absent as a deviation permitted in §6. Vacuous success is not success.
   The recorded number is the count of items actually read; an implementation MUST NOT substitute a
   minimum.
5. A check that an implementation does not perform is reported with status `NOT_IMPLEMENTED` and its
   check id. It never counts as `PASS`: a certification run with any such check is `NON_CONFORMANT`.
   During authoring, a validator MAY report it as a warning, and MUST list every such check id.
6. **Canonical-only mode.** A run over the canonical core with no port (step 1 of §7) cannot
   evaluate the eleven checks that compare a port with the core or inspect a target: `C1.1`, `C1.2`,
   `C1.7`, `C1.12`, `C2.1`, `C2.2`, `C2.3`, `C2.4`, `C2.6`, `C4.8`, `C5.7`. Each is reported with
   status `N/A` and the reason `port-only check (requires compiled target port)`; it is neither a
   pass nor a failure. A clean canonical-only run therefore reports 44 evaluated checks passed and
   11 not applicable, never 55 passed. `N/A` is not available in a port certification.
7. **Manifest checks.** Before the gates, a port certification records two checks in
   `manifest_checks`: `M.1` (`spec_version` is `"1"`, else `MANIFEST_SPEC_VERSION`) and `M.2` (every
   deviation is one of §6 and is legal for the port, else `MANIFEST_DEVIATION_ILLEGAL`). A missing or
   unreadable manifest is `M.0` with `MANIFEST_MISSING`. A failed manifest check makes the verdict
   `NON_CONFORMANT`; every `NON_CONFORMANT` verdict names at least one failed check.
8. Evidence is written to `conformance_report.json` in the port root (§2.2 gives the name used for
   a manifest with another name; `--report-out` overrides both):

```json
{
  "spec_version": "1",
  "target": "<public harness name>",
  "canonical_revision": "<revision id>",
  "manifest_checks": [{"id": "M.1", "status": "PASS|FAIL", "examined": 1, "failure_code": null, "locations": [], "reason": null}],
  "gates": {
    "C1": {"status": "PASS|FAIL", "checks": [{"id": "C1.1", "status": "PASS|FAIL|N/A|NOT_IMPLEMENTED", "examined": 0, "failure_code": null, "locations": [], "reason": null}]}
  },
  "deviations": [],
  "summary": {"total": 55, "evaluated": 55, "passed": 55, "failed": 0, "not_applicable": 0},
  "verdict": "CONFORMANT|CONFORMANT_WITH_DEVIATIONS|NON_CONFORMANT"
}
```

   A gate is `PASS` when each of its checks is `PASS` or `N/A`. `summary.failed` counts failed gate
   checks and failed manifest checks.

9. Reference implementation: `scripts/verify_port_conformance.py` exits 0 for `CONFORMANT`, 2 for
   `CONFORMANT_WITH_DEVIATIONS`, 1 for `NON_CONFORMANT`. An independent implementation of this
   specification that yields a different verdict on the same inputs is a defect in one of the two.

## 6. Verdicts and Permitted Deviations

| Verdict | Condition |
| :--- | :--- |
| `CONFORMANT` | All six gates `PASS`; `deviations` is empty |
| `CONFORMANT_WITH_DEVIATIONS` | All six gates `PASS` after applying only deviations listed below, each declared in the manifest |
| `NON_CONFORMANT` | Any gate `FAIL`, any undeclared deviation, or a missing manifest |

Exactly two deviations exist. Neither can be combined with a failure elsewhere.

| ID | Applies to | Allowed when | Constraint |
| :--- | :--- | :--- | :--- |
| `DEV-STUB` | `C2.2`, `C2.6` | The target has no on-demand discovery mechanism, and the operator (not the adapter) adds a pointer | At most 12 lines and 800 bytes; pointers to installed files only; no definition, rule, procedure, or citation; the stub text is reproduced in the manifest and occurs exactly once in the surface; removing it yields the bytes digested as `sha256_before`. The stub is a property of the surface, not of one build: while it is on the surface every later build MUST declare it, and its baseline is the surface without the stub |
| `DEV-NOFILES` | `C3.1`-`C3.4`, `C3.6` | The port serves content through an interface instead of files | The served unit sizes satisfy the same numeric limits; `C1.8` applies to every unit |

## 7. Porting Procedure

1. Record the canonical revision. Run all gates on the canonical core alone; a core that fails cannot
   be ported conformantly.
2. Snapshot every always-on surface of the target. Record digests in the manifest.
3. Compile or transcribe the port. Record every mapping, classifying it lossless or transforming.
4. Extend the `C5.5` denylist with identifiers of the porting environment.
5. Run the gates in the order of §5. Fix defects in the canonical core or in the adapter, never in
   the port output, and recompile.
6. Publish `port_manifest.json` and `conformance_report.json` with the port.

## 8. Traceability to the Anti-Degradation Contracts

| Contract (`ARCHITECTURE.md` §7) | Preserved by |
| :--- | :--- |
| `SMOOTHING_TRAP` | `C1.2`, `C1.7`, `C1.8` (a port cannot shorten a certified statement: lossless bodies are digested, transforming bodies are compared line by line, and compiled concept cards keep one list item per condition) |
| `SIGNATURE_DISTORTION` | `C1.2`, `C1.7`, `C1.8` (a changed word, symbol, or number in a substantive line, a clause appended to one, or a line added beside one fails the exact comparison) |
| `SILENT_GOTCHA_TRUNCATION` | `C1.9`, `C6.6`, `C6.7` |
| `HALLUCINATED_SYMBOL` | `C1.3`, `C1.4`, `C1.5`, `C1.10`, `C1.11` |
| `PROVENANCE_DISCONNECTION` | `C1.3`, `C1.12`, `C3.7`, `C3.9`, `C3.11`, `C6.3`-`C6.9` |

Conformance preserves these properties across a port; it does not establish them. A canonical core
that carries a degradation defect will port that defect faithfully and still pass.
