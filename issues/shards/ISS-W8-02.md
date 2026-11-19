---
id: ISS-W8-02
title: "W8-2 Gate #11 whole-book 3-model loop, local deployment, live conformance"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-8, gate]
milestone: W8
parent_issue: EPIC-001
depends_on: [ISS-W8-01]
blocks: []
ppa_scope: ["Whole book (book pp. 1–452; PDF pp. 21–465)"]
altitudes: [L0, L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
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

- [x] Review reports and rebuttal dispositions recorded in the issue alignment logs
- [x] `python3 -B scripts/verify_port_conformance.py` exits 0 (`CONFORMANT`) on deployed targets
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Gate #11 whole-book adversarial panel Round 1 (`gate11-v1`, `17` findings) -> Round 2 (`gate11-v2`): unanimous `3/3 [ALIGNED gate11-v2]` across `P-SWE`, `P-ARCH`, and `P-CYBER` (`0 HARD_BLOCK`, `0 BLOCKING`, `0 PREFERENCE`; `#295`, `#296`, `#297`).
- Live deployment verification (vendor-neutral targets): Target 2 local harness port and Knowledge Wiki port each certified `CONFORMANT` (`exit 0`, `55/55` PASS) prior to non-destructive local install (`7` skills + `7` `L0` topic guides installed while preserving all `13` existing topic files and keeping user-home always-on instructions byte-identical at `22347` bytes; budget check `exit 0`, `419/419` lines, `30776` always-on bytes; Knowledge Wiki `179` concept/skill/index pages + `70` source/index pages + `ppa_index.md` + `13` raw source-bundle files merged non-destructively while preserving all pre-existing pages, log lines, and notebook config keys).

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W8-01; blocks: none
- Review verdicts recorded in `issues/` alignment logs
- `scripts/verify_port_conformance.py`

## Verification Receipts
- 2026-11-19 [closed] Gate #11 unanimous 3/3 [ALIGNED gate11-v2] (#295-#297); Target 2 (7 skills, 7 topics, 22347B global rules untouched, budget rc=0) & Knowledge Wiki (179 concept/index, 70 source/index, 13 bundle files, existing keys preserved) deployed & verified CONFORMANT 55/55.
