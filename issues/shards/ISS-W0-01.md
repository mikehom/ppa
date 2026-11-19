---
id: ISS-W0-01
title: "W0-1 Issue engine, portability sanitizer and upfront issue suite"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-0]
milestone: W0
parent_issue: EPIC-001
depends_on: []
blocks: [ISS-W0-02, ISS-W1-01]
ppa_scope: ["Whole book (tracking only)"]
altitudes: [L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: null
---

## Summary

Bootstrap the per-file Markdown issue tracker (schema, flock-guarded controller, topological GitHub export) and the fail-closed zero-internal-identifier hygiene gate; seed EPIC-001 plus all 21 wave shards.

## Source Citations & Grounding

- Whole book (tracking only)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [x] Artifact `issues/SCHEMA.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] `python3 -B scripts/issue_ctl.py export-github --dry-run` produces a deterministic topological manifest
- [x] `python3 -B tests/test_wave0_foundation.py` (`HygieneTests` and `IssueCtlTests`) exits 0
- [x] Artifact `issues/epics/EPIC-001.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `issues/shards/ISS-*.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

### Rebuttal & Attribution Summary (Gate #0)

| Finding ID | Severity | Target File(s) | Disposition | Anchor After Fix |
| :--- | :--- | :--- | :--- | :--- |
| `F-FJ-001` | `BLOCKING` | `scripts/check_portability_hygiene.py`, `tests/test_wave0_foundation.py` | Purged all hex-escaped and fragment-joined personal/org/tool tokens from tracked code; moved operator rules to untracked runtime denylist JSON | `scripts/check_portability_hygiene.py:46-75,87-96`; `tests/test_wave0_foundation.py:86-152` |
| `F-FJ-002` / `F-OJ-011` | `BLOCKING` | `scripts/check_portability_hygiene.py` | Enforced fail-closed scanning over `git ls-files`, path strings, symlink targets/escapes, `>8 MiB`, NUL-byte, and invalid-UTF-8 files plus `(?![A-Za-z])` operator boundary | `scripts/check_portability_hygiene.py:87-112,167-196` |
| `F-CJ-001` / `F-OJ-009` | `BLOCKING` | `issues/backlog/BKL-001..012.md`, `issues/shards/ISS-*.md`, `issues/SCHEMA.md` | Replaced all model/worker labels and untracked scratch paths with neutral `P-SWE`/`P-ARCH`/`P-CYBER` perspective IDs; enforced `C5.2` in core scan | `issues/backlog/BKL-001.md:44`..`BKL-012.md:45`; `issues/shards/ISS-W8-02.md:35,48`; `scripts/check_portability_hygiene.py:65-75` |
| `F-CJ-003` / `F-FJ-008` | `BLOCKING` | `issues/epics/EPIC-001.md`, `issues/shards/ISS-W0-01..W8-02.md` | Replaced stale unconditional-load `L0` wording across all 22 files with exact `ARCHITECTURE.md` §3.1 zero-byte `R0` / on-match `L0` definitions + regression test | `issues/epics/EPIC-001.md:31`; `issues/shards/ISS-W0-01.md:31`..`ISS-W8-02.md:31`; `tests/test_wave0_foundation.py:185-188` |
| `F-OJ-001` | `BLOCKING` | `tests/test_wave0_foundation.py` | Replaced fixed-12 equality check with contiguous `>= 12` prefix/subset assertion and `C6.8` non-blocking check across all `BKL-*` items | `tests/test_wave0_foundation.py:345-359` |
| `F-OJ-004` | `BLOCKING` | `issues/backlog/BKL-009.md` | Restated `β\{s} = β` as semantically sound and symbolic `φ\{s}` as the less approximate option per book pp. 329–330 | `issues/backlog/BKL-009.md:22-37` |
| `F-OJ-005` | `BLOCKING` | `issues/backlog/BKL-002.md` | Removed false `x ⊔ (x ∇ y)` hazard (`= x ∇ y`), changed wording to `not required to be monotone`, and cited p. 226 | `issues/backlog/BKL-002.md:22-36` |
| `F-OJ-006` | `BLOCKING` | `issues/backlog/BKL-003.md` | Clarified ACC join-accumulation preserves termination (Lemma 2.29, pp. 75–76) while losing least-solution guarantee; added p. 129 weakly monotonic remedy | `issues/backlog/BKL-003.md:22-38` |
| `F-OJ-008` | `BLOCKING` | `issues/backlog/BKL-005.md`, `BKL-006.md`, `BKL-009.md` | Fixed coordinates (`PExp` p. 104, DCE licence + exit-liveness caveat p. 49, effect subtraction pp. 329–330) and dropped unsupported `disjoint` | `issues/backlog/BKL-005.md:22-27`; `BKL-006.md:22-27`; `BKL-009.md:22-29` |
| `F-FJ-012` / `F-OJ-003` | `BLOCKING` | `issues/backlog/BKL-010.md`, `BKL-012.md` | Added Bit Vector Framework + DFSF `T` + reverse-postorder preconditions and `d(G_S, T)` parameter to Lemma 6.12 restatements | `issues/backlog/BKL-010.md:22,35`; `issues/backlog/BKL-012.md:22,34` |
| `F-OJ-012` | `BLOCKING` | `scripts/issue_ctl.py`, `issues/SCHEMA.md` | Rejected pre-`## Summary` preamble and frontmatter `#` comments in `validate`; added `published_body_sha256` verified on export | `scripts/issue_ctl.py:129-192,495-516`; `issues/SCHEMA.md:27,64-66,109-112` |
| `F-FJ-013` | `BLOCKING` | `MASTER_PLAN.md`, `tests/test_wave0_foundation.py` | Added `## Requirements` table (`REQ-PRD-PPA-001..006`, `REQ-TECH-PPA-001..006`) + `DEC-PPA-008` and header-to-plan resolution test | `MASTER_PLAN.md:48-79`; `tests/test_wave0_foundation.py:670-686` |
| `F-CJ-007` / `F-FJ-014` / `F-OJ-013` | `PREFERENCE` | `scripts/issue_ctl.py` | Enforced `>= 3` distinct `aligned_models` + non-empty log at `aligned`, all gates checked at `closed`, and `--out` flag on `export-github` | `scripts/issue_ctl.py:269-279,521-542,575-577` |
| `F-OJ-017` | `PREFERENCE` | `scripts/issue_ctl.py` | Added `~~~` fence support, `C6.8` check, and unknown `issues/` entry/subdirectory failure | `scripts/issue_ctl.py:157-177,293-295,352-383` |
| `F-FJ-020` | `PREFERENCE` | `scripts/check_portability_hygiene.py` | Added structural email, URL allowlist, POSIX/Windows/`file:///` path, `C5.2` core, and harness checks | `scripts/check_portability_hygiene.py:51-75` |
| `F-FJ-021` | `PREFERENCE` | `EPIC-001.md`, `ISS-W0-01.md`, `ISS-W0-02.md`, `ISS-W7-01.md`, `ISS-W8-02.md` | Replaced vacuous validator gates on scripts/tests with concrete test/CLI execution gates | `issues/shards/ISS-W0-01.md:35-41`; `ISS-W0-02.md:41-43` |
| `F-FJ-022` / `F-OJ-020` | `PREFERENCE` | `issues/SCHEMA.md`, `BKL-001..010.md` | Defined `contradiction` vs `edge_case`, retyped `BKL-001/004/007` to `edge_case`, tagged `[external]` claims, and fixed `BKL-007` p. 196 wording | `issues/SCHEMA.md:18`; `issues/backlog/BKL-001.md:4,22,32`; `BKL-007.md:4,33` |

- 2026-11-19 Gate #0 Round 2 `[ALIGNED gate0-v2]` across all 3 independent review tracks (`P-SWE`, `P-ARCH`, `P-CYBER`): all Round 1 blocking findings withdrawn, 0 sustained blocking/hard-block regressions.

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: none; blocks: ISS-W0-02, ISS-W1-01
- `issues/SCHEMA.md`
- `scripts/issue_ctl.py`
- `scripts/check_portability_hygiene.py`
- `tests/test_wave0_foundation.py`
- `issues/epics/EPIC-001.md`
- `issues/shards/ISS-*.md`

## Verification Receipts

- 2026-11-18 [in_progress] Gate #0 remediation verified: `python3 -B tests/test_wave0_foundation.py` (`Ran 37 tests — OK`), `python3 -B scripts/issue_ctl.py validate` (`57 issue(s), 0 error(s)`), `python3 -B scripts/check_portability_hygiene.py .` (`0 finding(s) in 86 scanned file(s)`).
- 2026-11-19 [closed] Gate #0 3/3 `[ALIGNED gate0-v2]` confirmed; Wave 0 closure validated (`issue_ctl.py validate`, `check_portability_hygiene.py`, `tests/test_wave0_foundation.py` + `tests/test_artifact_rules.py`: `47/47` OK).
