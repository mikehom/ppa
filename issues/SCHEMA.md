<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-002: One Markdown file per issue (YAML frontmatter + fixed sections) for race-free multi-agent edits and lossless 1:1 GitHub Issues export. -->

# Issue File Schema (`issues/`)

Every tracked unit of work is one Markdown file. Files are machine-validated by
`python3 -B scripts/issue_ctl.py validate` and exported losslessly to GitHub
Issues via `python3 -B scripts/issue_ctl.py export-github --dry-run`, which
writes `issues/export_manifest.json`.

## Directory Layout & ID Prefixes

| Directory | ID pattern | Allowed `issue_type` | Purpose |
| :--- | :--- | :--- | :--- |
| `issues/epics/` | `EPIC-NNN` | `epic` | Initiative-level roll-up |
| `issues/shards/` | `ISS-WN-NN` | `shard` | One wave shard from `MASTER_PLAN.md` |
| `issues/refactors/` | `REF-NNN` | `refactor` | Altitude / knowledge-base refactoring |
| `issues/backlog/` | `BKL-NNN` | `contradiction`, `edge_case` | Non-blocking contradictions & edge cases (`contradiction` = two citable source/derived claims cannot both hold as written; `edge_case` = source holds under a stated assumption that another unit or `[external]` practice violates) |

The file name MUST be `<id>.md` (e.g. `issues/shards/ISS-W2-01.md`).

## Frontmatter

The file MUST start with a `---` line and the frontmatter MUST end with a
second `---` line. Frontmatter is a strict YAML subset:

- one `key: value` per line, no nesting, no multi-line scalars, no `#` comments;
- scalars: bare or double-quoted strings, integers, `null`;
- lists: inline flow style only, e.g. `[a, b]` or `[]` (items may be quoted).

All keys below are required; unknown keys are rejected.

| Key | Type | Constraint |
| :--- | :--- | :--- |
| `id` | string | Matches directory prefix and file stem |
| `title` | string | Non-empty, <= 120 chars; becomes the GitHub issue title |
| `issue_type` | enum | `epic` \| `shard` \| `refactor` \| `contradiction` \| `edge_case` |
| `status` | enum | `open` \| `in_progress` \| `aligned` \| `closed` \| `parked` |
| `priority` | enum | `P0` \| `P1` \| `P2` |
| `labels` | list | Free-form strings; exporter adds `type:*`, `priority:*`, `status:*` |
| `milestone` | string | Wave milestone, e.g. `W2` |
| `parent_issue` | id \| `null` | Must exist; only `EPIC-*` issues may have `null` |
| `depends_on` | list of ids | Each must exist; graph must be acyclic |
| `blocks` | list of ids | Exact inverse of `depends_on` (symmetry enforced) |
| `ppa_scope` | list | Book coverage, e.g. `"Ch 2 §2.1–2.4 (book pp. 35–81)"` |
| `altitudes` | list | Subset of `L0`, `L1`, `L2`, `L3` |
| `aligned_models` | list | Judge identifiers that emitted `[ALIGNED <v>]`; `aligned` status requires >= 3 |
| `created_at` | date | `YYYY-MM-DD` |
| `updated_at` | date | `YYYY-MM-DD`, not earlier than `created_at` |
| `github_issue_number` | int \| `null` | Positive and unique once assigned by the exporter's consumer |

## Required Body Sections

Exactly these level-2 headings, each exactly once, in this order:

1. `## Summary`
2. `## Source Citations & Grounding`
3. `## Technical Analysis / Mechanism`
4. `## Acceptance Gates`
5. `## 3-Model Adversarial Alignment & Rebuttal Log`
6. `## Cross-Referenced Concepts & Artifacts`
7. `## Verification Receipts`

Level-3+ headings may be used freely inside a section. No preamble text is
permitted between the closing `---` frontmatter line and `## Summary`. A section
is *empty* when it contains only whitespace or the placeholder `_Pending._`.

## Semantic Rules (enforced by `validate`)

- `closed` requires a non-empty `## Verification Receipts` section.
- `aligned` requires at least 3 distinct identifiers in `aligned_models`.
- `## Summary` and `## Acceptance Gates` must never be empty.
- Epics and shards must not depend on backlog items (`C6.8`).
- Status transitions through `set-status` are restricted to:

| From | Allowed to |
| :--- | :--- |
| `open` | `in_progress`, `parked` |
| `in_progress` | `aligned`, `parked`, `open` |
| `aligned` | `closed`, `in_progress` |
| `closed` | `in_progress` |
| `parked` | `open`, `in_progress` |

## Concurrency

All mutating commands take an exclusive `fcntl.flock` on an untracked scratch
lockfile; `validate` takes a shared lock. Agents MUST mutate status through
`issue_ctl.py set-status` rather than hand-editing the `status` line.

## GitHub Export Mapping

| Issue field | GitHub field |
| :--- | :--- |
| `title` | `title` |
| body sections (verbatim, in order) + metadata footer | `body` |
| `labels` + `type:<issue_type>` + `priority:<P>` + `status:<s>` + altitude labels | `labels` |
| `milestone` | `milestone` |
| `status == closed` | `state: closed` (otherwise `open`) |
| `parent_issue`, `depends_on`, `blocks` | Task-list cross references (resolved after creation) |

Export order is a deterministic topological sort over `parent_issue` and
`depends_on` edges (ties broken by id), so parents and prerequisites are always
created before dependents.

Each manifest entry also carries lossless provenance for conformance check
`C6.5` (`architecture/CONFORMANCE_SPEC.md`): `frontmatter` (all key-value pairs),
`source_body` (the file body after frontmatter, normalised per `N4`/`N5`: LF line
endings, per-line trailing whitespace stripped, trailing blank lines removed, no
final newline), `body_sha256` (lowercase hex SHA-256 of `source_body` in UTF-8,
rule `N6`), and `published_body_sha256` (SHA-256 of the rendered GitHub `body`).
An issue file is reconstructable from its entry alone.

## Template

```markdown
---
id: ISS-W9-01
title: "Example shard title"
issue_type: shard
status: open
priority: P1
labels: [ppa, wave-9]
milestone: W9
parent_issue: EPIC-001
depends_on: []
blocks: []
ppa_scope: ["Ch 1 §1.1 (book pp. 1–2)"]
altitudes: [L1, L2]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary
...

## Source Citations & Grounding
...

## Technical Analysis / Mechanism
...

## Acceptance Gates
- [ ] ...

## 3-Model Adversarial Alignment & Rebuttal Log
_Pending._

## Cross-Referenced Concepts & Artifacts
...

## Verification Receipts
_Pending._
```
