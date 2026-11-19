---
id: ISS-W8-02
title: "W8-2 Gate #11 whole-book 3-model loop, local deployment, live conformance"
issue_type: shard
status: open
priority: P0
labels: [ppa, wave-8, gate]
milestone: W8
parent_issue: EPIC-001
depends_on: [ISS-W8-01]
blocks: []
ppa_scope: ["Whole book (book pp. 1–452; PDF pp. 21–465)"]
altitudes: [L0, L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Run the final whole-book adversarial gate, deploy to local harnesses and the knowledge wiki, and verify conformance live.

## Source Citations & Grounding

- Whole book (book pp. 1–452; PDF pp. 21–465)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [ ] Review reports and rebuttal dispositions recorded in the issue alignment logs
- [ ] `python3 -B scripts/verify_port_conformance.py` exits 0 (`CONFORMANT`) on deployed targets
- [ ] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W8-01; blocks: none
- Review verdicts recorded in `issues/` alignment logs
- `scripts/verify_port_conformance.py`

## Verification Receipts

_Pending._
