---
id: ISS-W7-01
title: "W7-1 Porting docs, five reference harness adapters and conformance suite"
issue_type: shard
status: open
priority: P1
labels: [ppa, wave-7]
milestone: W7
parent_issue: EPIC-001
depends_on: [ISS-W6-02]
blocks: [ISS-W8-01]
ppa_scope: ["Whole book (packaging only)"]
altitudes: [L0, L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Author porting/model-adaptation guides, deterministic stdlib adapters for five target harness layouts, and the post-port conformance verifier.

## Source Citations & Grounding

- Whole book (packaging only)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [ ] Artifact `README.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `architecture/PORTING_GUIDE.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `architecture/MODEL_ADAPTATION_GUIDE.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] `adapters/*.py` compile all five target harness layouts deterministically
- [ ] `python3 -B tests/test_adapters_and_conformance.py` (exercising `scripts/verify_port_conformance.py`) exits 0
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W6-02; blocks: ISS-W8-01
- `README.md`
- `architecture/PORTING_GUIDE.md`
- `architecture/MODEL_ADAPTATION_GUIDE.md`
- `adapters/*.py`
- `scripts/verify_port_conformance.py`
- `tests/test_adapters_and_conformance.py`

## Verification Receipts

_Pending._
