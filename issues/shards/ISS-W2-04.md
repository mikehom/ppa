---
id: ISS-W2-04
title: "W2-4 Part I holistic altitude refactoring + Gate #4"
issue_type: shard
status: open
priority: P1
labels: [ppa, wave-2, gate]
milestone: W2
parent_issue: EPIC-001
depends_on: [ISS-W2-03]
blocks: [ISS-W3-01]
ppa_scope: ["Part I: Ch 1–2 + Appendices (book pp. 1–140; PDF pp. 21–158; book pp. 393–432; PDF pp. 409–446)"]
altitudes: [L0, L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Holistic L0–L3 refactor across Part I artifacts; Gate #4.

## Source Citations & Grounding

- Part I: Ch 1–2 + Appendices (book pp. 1–140; PDF pp. 21–158; book pp. 393–432; PDF pp. 409–446)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [ ] Artifact `ontology/altitude_alignment_log.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `ontology/concept_graph.json` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W2-03; blocks: ISS-W3-01
- `ontology/altitude_alignment_log.md`
- `ontology/concept_graph.json`

## Verification Receipts

_Pending._
