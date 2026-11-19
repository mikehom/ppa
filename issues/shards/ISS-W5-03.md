---
id: ISS-W5-03
title: "W5-3 Part II cross-paradigm matrix + Gate #8"
issue_type: shard
status: open
priority: P1
labels: [ppa, wave-5, gate]
milestone: W5
parent_issue: EPIC-001
depends_on: [ISS-W5-02]
blocks: [ISS-W6-01]
ppa_scope: ["Part II: Ch 3–5 (book pp. 141–364; PDF pp. 159–380)"]
altitudes: [L0, L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Build the cross-paradigm equivalence matrix across DFA/CBA/AI/TES; cumulative refactoring; Gate #8.

## Source Citations & Grounding

- Part II: Ch 3–5 (book pp. 141–364; PDF pp. 159–380)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [ ] Artifact `ontology/cross_paradigm_matrix.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W5-02; blocks: ISS-W6-01
- `ontology/cross_paradigm_matrix.md`

## Verification Receipts

_Pending._
