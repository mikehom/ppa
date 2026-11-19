---
id: EPIC-001
title: "EPIC-001 Exhaustive PPA knowledge extraction, 3-model enrichment and portable harness suite"
issue_type: epic
status: in_progress
priority: P0
labels: [ppa, wave-0-wave-8]
milestone: W0-W8
parent_issue: null
depends_on: []
blocks: []
ppa_scope: ["Whole book (book pp. 1–452; PDF pp. 21–465; 465 PDF pages)"]
altitudes: [L0, L1, L2, L3]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Roll-up for initiative INIT-2026-11-18-ppa-v1: extract all formal and practical intelligence from Principles of Program Analysis into a vendor-neutral L0–L3 knowledge package with lossless issue tracking, deterministic validators, harness adapters and 11 adversarial gates. Child shards: ISS-W0-01, ISS-W0-02, ISS-W0-03, ISS-W1-01, ISS-W1-02, ISS-W2-01, ISS-W2-02, ISS-W2-03, ISS-W2-04, ISS-W3-01, ISS-W3-02, ISS-W4-01, ISS-W4-02, ISS-W5-01, ISS-W5-02, ISS-W5-03, ISS-W6-01, ISS-W6-02, ISS-W7-01, ISS-W8-01, ISS-W8-02.

## Source Citations & Grounding

- Whole book (book pp. 1–452; PDF pp. 21–465; 465 PDF pages)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [ ] Artifact `MASTER_PLAN.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] `python3 -B tests/test_wave0_foundation.py` and `python3 -B tests/test_artifact_rules.py` exit 0
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: none; depends on: none; blocks: none
- `MASTER_PLAN.md`
- `issues/shards/`

## Verification Receipts

_Pending._
