---
id: ISS-W2-04
title: "W2-4 Part I holistic altitude refactoring + Gate #4"
issue_type: shard
status: closed
priority: P1
labels: [ppa, wave-2, gate]
milestone: W2
parent_issue: EPIC-001
depends_on: [ISS-W2-03]
blocks: [ISS-W3-01]
ppa_scope: ["Part I: Ch 1–2 + Appendices (book pp. 1–139; PDF pp. 21–158; book pp. 393–432; PDF pp. 409–446)"]
altitudes: [L0, L1, L2, L3]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
github_issue_number: null
---

## Summary

Holistic L0–L3 refactor across Part I artifacts; Gate #4.

## Source Citations & Grounding

- Part I: Ch 1–2 + Appendices (book pp. 1–139; PDF pp. 21–158; book pp. 393–432; PDF pp. 409–446)
- Coordinate source of truth: `corpus/pdf_page_map.json` (variable PDF offset; never assume a constant offset).

## Technical Analysis / Mechanism

Target altitudes: L0, L1, L2, L3. Altitudes per architecture/ARCHITECTURE.md §3.1: R0 always-on = 0 bytes; L0 = zero always-on bytes (router 50–99L and ambient 80–250L files loaded on match only); L1 = references (<=450L) with every side condition preserved; L2 = actionable skill procedures (250–499L) with explicit precondition checks; L3 = corpus shards and concept graph.

## Acceptance Gates

- [x] Artifact `ontology/altitude_alignment_log.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifact `ontology/concept_graph.json` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Round 1 (`gate4-v1`): three-track adversarial panel returned `[DISAGREE]` across `16` findings (`P-ARCH`: `3` `BLOCKING`, `2` `PREFERENCE`; `P-SWE`: `4` `BLOCKING`, `2` `PREFERENCE`; `P-CYBER`: `3` `BLOCKING`, `2` `PREFERENCE`). Remediated all `15` actionable items (`gate4-v2`, retaining `C3.8`-legal router link with `<90L` headroom guard on `F-FJ-404`).
- 2026-11-19 Round 2 (`gate4-v2`): unanimous `3/3 [ALIGNED gate4-v2]` across `P-SWE`, `P-ARCH`, and `P-CYBER` (`0` `HARD_BLOCK`, `0` `BLOCKING`; non-blocking `PREFERENCE` notes on `F-FJ-404` `80L` router and `F-OJ-407` `U-37` ID gap).

### Rebuttal & Attribution Summary (Gate #4 Round 1)

| Finding ID | Track | Severity | Disposition & Action Taken | Target Artifact(s) |
| :--- | :--- | :--- | :--- | :--- |
| `F-FJ-401` | `P-ARCH` | `BLOCKING` | Fixed `\le` YAML escape (`≤`) and `must_mention` `"y := x * x"` alignment; verified all `evals/cases.yaml` files parse under `yaml.safe_load` | `knowledge/skills/ppa-dataflow-and-slicing/evals/cases.yaml`, `REF-001.md` |
| `F-FJ-402` | `P-ARCH` | `BLOCKING` | Reconciled `ppa.dfa.rd-instrumented-correctness` (`L3 -> L1`) jointly with full `Rule B1` parity (`F-OJ-402`) | `ontology/concept_graph.json`, `ontology/altitude_alignment_log.md` |
| `F-FJ-403` | `P-ARCH` | `BLOCKING` | Fixed `L1 anchor` in `BKL-037`/`038` to `interprocedural-and-correctness.md` and added inline `§1` pointers | `issues/backlog/BKL-037.md`, `BKL-038.md`, `references/interprocedural-and-correctness.md`, `REF-002.md` |
| `F-FJ-404` | `P-ARCH` | `PREFERENCE` | Noted: `## Sibling Reference Modules (Active)` remains `C3.8`-legal with `ppa-program-analysis/SKILL.md` held compact at `80L` (`<90L`, `19L` below `99L` ceiling); scalability cap tracked for `W3–W6` | `knowledge/skills/ppa-program-analysis/SKILL.md` |
| `F-FJ-405` | `P-ARCH` | `PREFERENCE` | Updated `description` (`829` chars) and exact measured `N2` line counts (`208L`/`164L`/`159L`, `SKILL.md` `270L`) in log and `REF-001.md` | `ontology/altitude_alignment_log.md`, `issues/refactors/REF-001.md` |
| `F-OJ-401` | `P-SWE` | `BLOCKING` | Fixed `U-35` (`[PPA §2.1.2, p. 43]` + `:411` ref), `U-38` (`ALoc → ALoc`, `p. 117`), and removed duplicate `U-37` / invented `U-39` (`⊑_{RD}`/`⊑_{AE,VB}`), moving plain-symbol notes into `Overloaded symbols` | `ontology/notation_index.md`, `ontology/altitude_alignment_log.md`, `REF-002.md` |
| `F-OJ-402` | `P-SWE` | `BLOCKING` | Enforced `Rule B1` across all `81` nodes (`10` `L3 -> L1`, `6` `L2 -> L1`, removed casual `L0` ref on `while-flow-graphs`), confirmed `0` mismatches programmatically | `ontology/concept_graph.json`, `ontology/altitude_alignment_log.md`, `REF-002.md` |
| `F-OJ-403` | `P-SWE` | `BLOCKING` | Reclassified both premature `U6` `corresponds_to` pairs (`ppa.ai.adjunction-induced-analysis` <-> `constant-propagation`, `mop-vs-mfp`) to symmetric `related_to` pending Wave 4 `§4.3–§4.5` | `ontology/concept_graph.json`, `intraprocedural-analyses-and-frameworks.md`, `altitude_alignment_log.md`, `REF-002.md` |
| `F-OJ-404` | `P-SWE` | `BLOCKING` | Updated `DEC-PPA-008` in `altitude_alignment_log.md` (`:148, :173-176`, Entry `2026-11-19`) to reflect permanent `W1-2` router ownership of `appendix-{a,b,c}` | `ontology/altitude_alignment_log.md` |
| `F-OJ-405` | `P-SWE` | `PREFERENCE` | Synchronized `Affected concept ids` across all `9` landed Wave 0/1 items (`BKL-005, 014, 017, 022, 024, 028, 030, 032, 035`) with `concept_graph.json` `issue_refs` | `issues/backlog/BKL-*.md` |
| `F-OJ-406` | `P-SWE` | `PREFERENCE` | Replaced untagged `post-fixed points` in `ppa-foundations.md:93` with `reductive solutions (Red(F))` and replaced meta-citation placeholders in `architecture/` guides with concrete examples | `ppa-foundations.md`, `MODEL_ADAPTATION_GUIDE.md`, `PORTING_GUIDE.md` |
| `F-CJ-401` | `P-CYBER` | `BLOCKING` | Remediated jointly with `F-OJ-403` (`U6` pairs reclassified to `related_to`) | `ontology/concept_graph.json`, `intraprocedural-analyses-and-frameworks.md`, `REF-002.md` |
| `F-CJ-402` | `P-CYBER` | `BLOCKING` | Remediated jointly with `F-OJ-401` (`U-35, U-36, U-38` clean, `pp. 43, 67, 70, 117` verified) | `ontology/notation_index.md` |
| `F-CJ-403` | `P-CYBER` | `BLOCKING` | Remediated `DEC-PPA-008` jointly with `F-OJ-404` and updated `STRONG_UPDATE_GATE` `kill_x` coordinate to `[PPA §2.6, p. 117] (book p. 117; PDF p. 136)` | `ontology/altitude_alignment_log.md` |
| `F-CJ-404` | `P-CYBER` | `PREFERENCE` | Replaced literal raw-`C1.10` placeholder syntax in `altitude_alignment_log.md:52,56` and tagged `[external]` on `L0` `taint`/`injection`/`sanitizer` routing cues | `altitude_alignment_log.md`, `ppa-program-analysis/SKILL.md`, `ppa-dataflow-and-shape.md` |
| `F-CJ-405` | `P-CYBER` | `PREFERENCE` | Corrected Chapter 2 / Part I book end page from absent blank verso `140` to printed `139` | `ISS-W2-04.md`, `REF-001.md` |

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W2-03; blocks: ISS-W3-01
- `ontology/altitude_alignment_log.md`
- `ontology/concept_graph.json`
- `ontology/notation_index.md`
- `issues/refactors/REF-001.md`
- `issues/refactors/REF-002.md`

## Verification Receipts

- 2026-11-19 [in_progress] `W2-4` Part I holistic refactor (`REF-001`, `REF-002`) + `gate4-v2` remediation verified: Rule `B1` parity across `81` concepts, `U-35`/`U-36`/`U-38` notation scoping, premature `U6` pairs reclassified to `related_to`, and `0` errors across remediation verifier, `validate_ppa_knowledge.py --strict-gotchas`, `issue_ctl.py validate`, `check_portability_hygiene.py .`, and `47/47` unit tests. Ready for Gate #4 Round 2.
- 2026-11-19 [closed] Gate #4 Round 2 unanimous 3/3 [ALIGNED gate4-v2] across P-SWE, P-ARCH, and P-CYBER; 0 HARD_BLOCK, 0 BLOCKING; 81/81 Rule B1 parity, validators, hygiene, and 47/47 unit tests PASS.
