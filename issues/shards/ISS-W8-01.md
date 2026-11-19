---
id: ISS-W8-01
title: "W8-1 Whole-book audit, global altitude refactoring, GitHub export manifest"
issue_type: shard
status: open
priority: P0
labels: [ppa, wave-8]
milestone: W8
parent_issue: EPIC-001
depends_on: [ISS-W7-01]
blocks: [ISS-W8-02]
ppa_scope: ["Whole book (book pp. 1–452; PDF pp. 21–465)"]
altitudes: [L0, L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Audit coverage (51/51 tables, 56/56 figures, all sections), perform the global altitude refactor, and emit the topological export manifest.

## Source Citations & Grounding

- Whole book (book pp. 1–452; PDF pp. 21–465)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [ ] Artifact `issues/export_manifest.json` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `ontology/concept_graph.json` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W7-01; blocks: ISS-W8-02
- `issues/export_manifest.json`
- `ontology/concept_graph.json`

## Verification Receipts

_Pending._
