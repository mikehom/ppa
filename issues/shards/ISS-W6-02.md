---
id: ISS-W6-02
title: "W6-2 Cross-book cyber program-analysis skill, merged corpus + Gate #10"
issue_type: shard
status: open
priority: P1
labels: [ppa, wave-6, gate]
milestone: W6
parent_issue: EPIC-001
depends_on: [ISS-W6-01]
blocks: [ISS-W7-01]
ppa_scope: ["Whole book (book pp. 1–452; PDF pp. 21–465)"]
altitudes: [L0, L1, L2]
aligned_models: []
created_at: 2026-11-18
updated_at: 2026-11-18
github_issue_number: null
---

## Summary

Project book-wide techniques onto vulnerability analysis; merge raw shards into the ground-truth corpus; Gate #10.

## Source Citations & Grounding

- Whole book (book pp. 1–452; PDF pp. 21–465)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [ ] Artifact `knowledge/skills/ppa-cyber-vulnerability-analysis/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `knowledge/skills/ppa-cyber-vulnerability-analysis/references/ppa-cyber-analysis.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] Artifact `corpus/RAW_KNOWLEDGE.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [ ] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [ ] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [ ] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

_Pending._

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W6-01; blocks: ISS-W7-01
- `knowledge/skills/ppa-cyber-vulnerability-analysis/SKILL.md`
- `knowledge/skills/ppa-cyber-vulnerability-analysis/references/ppa-cyber-analysis.md`
- `corpus/RAW_KNOWLEDGE.md`

## Verification Receipts

_Pending._
