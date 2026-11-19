---
id: ISS-W7-01
title: "W7-1 Porting docs, five reference harness adapters and conformance suite"
issue_type: shard
status: closed
priority: P1
labels: [ppa, wave-7]
milestone: W7
parent_issue: EPIC-001
depends_on: [ISS-W6-02]
blocks: [ISS-W8-01]
ppa_scope: ["Whole book (packaging only)"]
altitudes: [L0, L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
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

- [x] Artifact `README.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `architecture/PORTING_GUIDE.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `architecture/MODEL_ADAPTATION_GUIDE.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] `adapters/*.py` compile all five target harness layouts deterministically
- [x] `python3 -B tests/test_adapters_and_conformance.py` (exercising `scripts/verify_port_conformance.py`) exits 0
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Gate #11 Round 1 (`gate11-v1`) -> Round 2 (`gate11-v2`): all Wave 7 documentation, 5 reference adapters, and 55-check conformance suite findings (`F-CJ-1101..1103`, `F-CJ-1106`, `F-OJ-1101..1103`, `F-OJ-1106`, `F-OJ-1107`, `F-FJ-1101..1104`, tracked 1-to-1 in `ISS-W8-01` & `REF-008`) resolved and verified; unanimous `3/3 [ALIGNED gate11-v2]` across `P-SWE`, `P-ARCH`, and `P-CYBER` (`0 HARD_BLOCK`, `0 BLOCKING`, `0 PREFERENCE`; `#295`, `#296`, `#297`).

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W6-02; blocks: ISS-W8-01
- `README.md`
- `architecture/PORTING_GUIDE.md`
- `architecture/MODEL_ADAPTATION_GUIDE.md`
- `adapters/*.py`
- `scripts/verify_port_conformance.py`
- `scripts/ppa_conformance_c125.py`, `scripts/ppa_conformance_c34.py`, `scripts/ppa_conformance_c6.py`
- `tests/test_adapters_and_conformance.py`

## Verification Receipts
- 2026-11-19 [in_progress] Promoted README.md, 7 adapters/*.py modules, 4 scripts/*conformance*.py modules, and tests/test_adapters_and_conformance.py (DEC-PPA-009).
- 2026-11-19 [closed] Gate #11 unanimous 3/3 [ALIGNED gate11-v2] (#295, #296, #297); all canonical & live 5-target 55/55 checks PASS.
