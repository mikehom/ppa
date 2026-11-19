---
id: ISS-W8-01
title: "W8-1 Whole-book audit, global altitude refactoring, GitHub export manifest"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-8]
milestone: W8
parent_issue: EPIC-001
depends_on: [ISS-W7-01]
blocks: [ISS-W8-02]
ppa_scope: ["Whole book (book pp. 1–452; PDF pp. 21–465)"]
altitudes: [L0, L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: 113
---

## Summary

Audit coverage (51/51 tables, 56/56 figures, all sections), perform the global altitude refactor, and emit the topological export manifest.

## Source Citations & Grounding

- Whole book (book pp. 1–452; PDF pp. 21–465)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [x] Artifact `issues/export_manifest.json` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `ontology/concept_graph.json` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- Round 1 (`gate11-v1`, `17` findings across `P-SWE` `F-CJ-1101..1106`, `P-ARCH` `F-OJ-1101..1107`, `P-CYBER` `F-FJ-1101..1104`; `0` `HARD_BLOCK`, `12` `BLOCKING`, `5` `PREFERENCE`) -> Round 2 (`gate11-v2`, `17/17` resolved):
  - `F-CJ-1101` / `F-OJ-1102` (`BLOCKING`, `P-SWE`/`P-ARCH`): `scripts/ppa_conformance_c34.py` now checks `C4.1`–`C4.6` on compiled port skill/rule surfaces (`.mdc` frontmatter, `SKILL.md`, `<!-- summary: ... -->`, `served_units.json`, router table rows, mapped `evals/cases.yaml`) whenever `not canonical_only`; regression-tested via `.mdc` `"Do not use"` same-length erasure & router-row strip in `tests/test_adapters_and_conformance.py`.
  - `F-CJ-1102` / `F-OJ-1101` / `F-FJ-1101` (`BLOCKING`, `P-SWE`/`P-ARCH`/`P-CYBER`): `adapters/wiki_sync_adapter.py` preserves all `conditions` (`94/94` conditioned nodes) and `issue_refs`, removes `edges[:25]`/`lines[:440]`/`[:80]`/`[:245]` slices, emits `<= 250L` unit/source sub-indexes (`pages/concepts/ppa-index-*.md`, `pages/sources/ppa-index-{refs,shards}.md`) linked from `pages/index.md` for `100%` reachability, and enforces `C3.9` BFS wiki reachability in `scripts/ppa_conformance_c34.py`.
  - `F-FJ-1102` (`BLOCKING`, `P-CYBER`): `adapters/wiki_sync_adapter.py` defaults to `dev_nofiles=False` (`CONFORMANT` exit `0`), swaps `--no-dev-nofiles` for opt-in `--dev-nofiles` (fileless `served_units.json` -> `CONFORMANT_WITH_DEVIATIONS` exit `2`), and `scripts/verify_port_conformance.py` + `C3.1` reject `DEV-NOFILES` when on-disk `pages/` or skill Markdown files exist (`exit 1`); `README.md` & `tests/test_adapters_and_conformance.py` updated.
  - `F-CJ-1103` / `F-OJ-1103` / `F-FJ-1103` / `F-CJ-1106` (`BLOCKING`+`PREF`, all 3): `architecture/PORTING_GUIDE.md:30,324` now specifies `validate_ppa_knowledge.py --strict-gotchas` + `verify_port_conformance.py --canonical-only --repo-root .` and `:284` fixes `ch6_worklist_rpo_algorithms.md` -> `worklist-and-rpo-algorithms.md`; `scripts/validate_ppa_knowledge.py --certify` delegates `C1`–`C6` canonical checks to `verify_port_conformance.certify(..., canonical_only=True)` (`exit 0`) while keeping default `[NOT_IMPLEMENTED]` behavior intact.
  - `F-CJ-1104` (`BLOCKING`, `P-SWE`): removed erroneous `[external]` tags on book-native `strong update(s)` / `strong kill(s)` (`[PPA §2.6.3, p. 115] (book p. 115; PDF p. 134)`) across `ppa-control-flow-and-constraints/SKILL.md`, `polyvariant-kcfa-cpa-and-dfa.md`, `ontology/concept_graph.json`, `ontology/cross_paradigm_matrix.md`, `RAW_SHARD_03b_kcfa_cpa.md`, and `RAW_SHARD_05b_effects_regions_behaviours.md`, and deterministically re-assembled `corpus/RAW_KNOWLEDGE.md` (`13,686L`).
  - `F-CJ-1105` (`PREF`, `P-SWE`): added `<!-- @decision DEC-PPA-001: ... -->` headers to `RAW_SHARD_02b_interproc_shape.md` (`1486L`) and `RAW_SHARD_04a_galois_widening.md` (`972L`) and synced `issues/refactors/REF-008.md`.
  - `F-OJ-1104` (`BLOCKING`, `P-ARCH`): corrected closed `L1` reference count from `22` (`4+18`) to `21` (`4` foundation + `17` domain; `ppa-fixedpoint-solvers` has `2`) in `issues/refactors/REF-008.md` and `ontology/altitude_alignment_log.md`.
  - `F-OJ-1105` (`BLOCKING`, `P-ARCH`): extracted `_reset_open_shards(root, "ISS-W8-01", "ISS-W8-02")` in `tests/test_wave0_foundation.py` (`695L < 700L`) for hermetic transition/gate tests post-closeout.
  - `F-OJ-1106` (`PREF`, `P-ARCH`): guarded `adapters/agents_md_adapter.py:_apply_dev_stub` against duplicate `--emit-dev-stub` appends; regression-tested in `tests/test_adapters_and_conformance.py`.
  - `F-OJ-1107` (`PREF`, `P-ARCH`): documented promoted adapter default paths (`ppa-ambient/`, `memory/topics/`, wiki concept/index/source paths) in `architecture/PORTING_GUIDE.md` §3.1–§3.3 and listed `cross_paradigm_matrix.md` + `RAW_KNOWLEDGE.md` in `README.md`.
  - `F-FJ-1104` (`PREF`, `P-CYBER`): made `_chunk_markdown_lines` in `adapters/wiki_sync_adapter.py` code-fence aware with unit test coverage in `tests/test_adapters_and_conformance.py`.
- 2026-11-19 Gate #11 Round 2 (`gate11-v2`): unanimous `3/3 [ALIGNED gate11-v2]` across `P-SWE`, `P-ARCH`, and `P-CYBER` (`0 HARD_BLOCK`, `0 BLOCKING`, `0 PREFERENCE`; `#295`, `#296`, `#297`; all `17/17` Round 1 items verified resolved).

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W7-01; blocks: ISS-W8-02
- `issues/export_manifest.json`
- `ontology/concept_graph.json`
- `issues/refactors/REF-008.md`
- `corpus/RAW_KNOWLEDGE.md`

## Verification Receipts
- 2026-11-19 [in_progress] Completed Gate #11 Round 1 -> Round 2 remediation (`gate11-v2`, `17/17` findings addressed across core, adapters, verifier, docs, shards, and tests); awaiting Round 2 panel review and `ISS-W8-02` verification.
- 2026-11-19 [closed] Gate #11 unanimous 3/3 [ALIGNED gate11-v2] (#295, #296, #297); all canonical & live 5-target 55/55 checks PASS.
