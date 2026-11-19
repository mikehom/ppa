---
id: ISS-W0-03
title: "W0-3 Normative 4-altitude architecture, conformance spec and calibration log"
issue_type: shard
status: closed
priority: P0
labels: [ppa, wave-0]
milestone: W0
parent_issue: EPIC-001
depends_on: []
blocks: [ISS-W1-01]
ppa_scope: ["Whole book (architecture only)"]
altitudes: [L0, L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: null
---

## Summary

Author the normative L0–L3 altitude specification and conformance contracts, calibrated by three independent model perspectives.

## Source Citations & Grounding

- Whole book (architecture only)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [x] Artifact `architecture/ARCHITECTURE.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `architecture/CONFORMANCE_SPEC.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `ontology/altitude_alignment_log.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

### Rebuttal & Attribution Summary (Gate #0)

| Finding ID | Severity | Target File(s) | Disposition | Anchor After Fix |
| :--- | :--- | :--- | :--- | :--- |
| `F-CJ-001` / `F-OJ-009` / `F-FJ-025` | `BLOCKING` | `ontology/altitude_alignment_log.md` | Replaced model/worker labels with `P-SWE`, `P-ARCH`, `P-CYBER`; removed untracked scratch paths and documented non-reproducible working-note status | `ontology/altitude_alignment_log.md:11-26,163` |
| `F-CJ-006` / `F-FJ-007` | `BLOCKING` | `ontology/altitude_alignment_log.md` | Re-anchored `EC-06` to `[PPA §1.3, p. 10]` (§1.3.2) and `EC-09` to `[PPA §1.1, p. 3]` | `ontology/altitude_alignment_log.md:114,116,164` |
| `F-OJ-002` | `BLOCKING` | `architecture/ARCHITECTURE.md`, `ontology/altitude_alignment_log.md` | Restored both Lemma 2.32 hypotheses (distributive framework and `path∘(ℓ) ≠ ∅` for all `ℓ` in `E` and `F`) across `ARCHITECTURE.md` (`architecture/*` — owned by architecture author) and calibration log | `architecture/ARCHITECTURE.md:221,313-316`; `ontology/altitude_alignment_log.md:102,166` |
| `F-FJ-012` / `F-OJ-003` | `BLOCKING` | `architecture/ARCHITECTURE.md`, `ontology/altitude_alignment_log.md` | Restricted Lemma 6.12 `d(G_S, T) + 3` bound to Bit Vector Framework instances with DFSF `T` and reverse postorder | `architecture/ARCHITECTURE.md:329-331`; `ontology/altitude_alignment_log.md:41,94,165` |
| `F-OJ-007` / `F-CJ-008` | `BLOCKING` | `ontology/altitude_alignment_log.md` | Anchored `STRONG_UPDATE_GATE` at p. 115 (`kill_x` p. 118; unsharing p. 125 & Fig. 2.21 p. 126), marked `"weak update"` `[external]`, and added `BKL-002` to `MONOTONICITY_GATE` | `ontology/altitude_alignment_log.md:91-93,167,171` |
| `F-OJ-008` | `BLOCKING` | `ontology/altitude_alignment_log.md` | Re-anchored channel invariance to p. 348, isolated entries/exits to p. 39, and separated RD tables (`1.1, 1.2, 1.3, 1.5`) from `Table 1.4` (call-tracking) and `Table 1.6` (Constant Folding) | `ontology/altitude_alignment_log.md:93,101,112,168-169` |
| `F-FJ-009` | `BLOCKING` | `architecture/ARCHITECTURE.md`, `ontology/altitude_alignment_log.md` | Defined `altitude` as highest surfaced altitude with universal `L3` entry (`architecture/*` — owned by architecture author) and recorded in alignment log | `architecture/ARCHITECTURE.md:72-75,101-107,240`; `ontology/altitude_alignment_log.md:178-182` |
| `F-CJ-004` / `F-FJ-003` / `F-FJ-004` / `F-FJ-010` / `F-FJ-011` / `F-FJ-013` | `BLOCKING` | `architecture/ARCHITECTURE.md`, `architecture/CONFORMANCE_SPEC.md` | Harmonized `N1`–`N3`, `N8` §3.1, `C1.3`/`C1.9`–`C1.12`, `C3.1`/`C3.8`–`C3.12`, `C4.1`/`C4.2`/`C4.7`, `corresponds_to` + `basis`, and §10 `REQ-*` table (`architecture/*` — owned by architecture author) | `architecture/ARCHITECTURE.md:124-127,278-282,306-359,409-420`; `architecture/CONFORMANCE_SPEC.md:59-80,92-101,123-134,145-151,194-198` |
| `F-CJ-009` / `F-FJ-015`..`020` / `F-FJ-023`..`024` / `F-OJ-019`..`021` | `PREFERENCE` | `architecture/ARCHITECTURE.md`, `architecture/CONFORMANCE_SPEC.md`, `ontology/altitude_alignment_log.md` | Unified `N2` whole-file unit, router `50–99` budget, atomic `Package` definition, empty default `C5.4` allowlist, verbatim `"can be omitted on a first reading"` & `"single static assignment"`, `DEC-PPA-008`, and `NOT_IMPLEMENTED` rules | `architecture/CONFORMANCE_SPEC.md:30,52-53,60,123,164,194-198`; `ontology/altitude_alignment_log.md:44,52-59,117,170,173-176` |

- 2026-11-19 Gate #0 Round 2 `[ALIGNED gate0-v2]` across all 3 independent review tracks (`P-SWE`, `P-ARCH`, `P-CYBER`): all Round 1 blocking findings withdrawn, 0 sustained blocking/hard-block regressions.

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: none; blocks: ISS-W1-01
- `architecture/ARCHITECTURE.md` (`420` lines)
- `architecture/CONFORMANCE_SPEC.md` (`255` lines)
- `ontology/altitude_alignment_log.md`

## Verification Receipts

- 2026-11-18 [in_progress] Gate #0 remediation verified across `architecture/ARCHITECTURE.md` (`420` lines), `architecture/CONFORMANCE_SPEC.md` (`255` lines), and `ontology/altitude_alignment_log.md`: `python3 -B scripts/validate_ppa_knowledge.py` (`PASS`), `python3 -B scripts/check_portability_hygiene.py .` (`0 finding(s)`), `python3 -B scripts/issue_ctl.py validate` (`0 error(s)`).
- 2026-11-19 [closed] Gate #0 3/3 `[ALIGNED gate0-v2]` confirmed; Wave 0 closure validated (`architecture/ARCHITECTURE.md` `420L`, `architecture/CONFORMANCE_SPEC.md` `255L`, `ontology/altitude_alignment_log.md`: PASS).
