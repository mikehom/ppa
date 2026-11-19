---
id: ISS-W6-02
title: "W6-2 Cross-book cyber program-analysis skill, merged corpus + Gate #10"
issue_type: shard
status: closed
priority: P1
labels: [ppa, wave-6, gate]
milestone: W6
parent_issue: EPIC-001
depends_on: [ISS-W6-01]
blocks: [ISS-W7-01]
ppa_scope: ["Whole book (book pp. 1–452; PDF pp. 21–465)"]
altitudes: [L0, L1, L2]
aligned_models: [P-SWE, P-ARCH, P-CYBER]
created_at: 2026-11-18
updated_at: 2026-11-19
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

- [x] Artifact `knowledge/skills/ppa-cyber-vulnerability-analysis/SKILL.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] Artifacts `knowledge/ambient-context/ppa-cyber-analysis.md` and `references/{taint-sanitization-and-information-flow,memory-heap-and-numeric-bounds-safety,callgraph-cfi-concurrency-and-scanner-dos}.md` exist and pass `scripts/validate_ppa_knowledge.py`
- [x] Artifact `corpus/RAW_KNOWLEDGE.md` exists and passes `scripts/validate_ppa_knowledge.py`
- [x] 3-model adversarial panel records `[ALIGNED <v>]` from all three judges (2-round cap; residual disagreement escalated)
- [x] `python3 -B scripts/check_portability_hygiene.py .` exits 0
- [x] `python3 -B scripts/issue_ctl.py validate` exits 0

## 3-Model Adversarial Alignment & Rebuttal Log

- 2026-11-19 Cross-Book Cyber Program Analysis synthesis (`ppa-cyber-vulnerability-analysis/` `301L` `SKILL.md` / `144L`, `130L`, `128L` `L1` refs, `ppa-cyber-analysis.md` `85L`, `10` `ppa.cyber.*` nodes in `153`-node `concept_graph.json`, `REF-007`) and deterministic whole-book `corpus/RAW_KNOWLEDGE.md` (`13,686L` across `RAW_SHARD_00`..`RAW_SHARD_06`) promoted after pre-promotion primary-source & `P2` audit (`#258`); staged for Gate #10 (`gate10-v1`).
- 2026-11-19 Gate #10 Round 1 (`gate10-v1`) produced `10` findings (`6 BLOCKING`, `4 PREFERENCE`, `0 HARD_BLOCK`) resolved into `gate10-v2` (all re-verified across tracked files, `RAW_KNOWLEDGE.md` reassembled, `concept_graph.json` and `BKL-016`/`036`/`037`/`038` synced):

| Finding ID | Severity | Resolution Summary (`gate10-v1` -> `gate10-v2`) | Status |
| :--- | :--- | :--- | :--- |
| `F-OJ-1001` | `BLOCKING` | Replaced nonexistent `§3.1.2`/`§3.1.3`/`§3.4.3`/`§3.4.4` citations with actual **`§3.1.1`** (`Table 3.1` / `p. 149`) and **`§3.4.2`** (`Table 3.7` / `p. 182`) across `ontology/concept_graph.json` (`12468-12506`), `ppa-cyber-analysis.md`, `ppa-cyber-vulnerability-analysis/SKILL.md`, and `callgraph-cfi-concurrency-and-scanner-dos.md`. | `RESOLVED -> ACCEPTED` |
| `F-CJ-1001` | `BLOCKING` | Resolved jointly with `F-OJ-1001`: aligned every `§3.1.2`/`§3.1.3`/`§3.4.3`/`§3.4.4` reference and `concept_graph.json` span in `ppa.cyber.higher-order-open-world-cfi` and Cyber L0/L1/L2 docs to `§3.1.1` (`p. 146`, `p. 149`) and `§3.4.2` (`p. 178`, `p. 182`). | `RESOLVED -> ACCEPTED` |
| `F-OJ-1002` | `BLOCKING` | Replaced `[PPA §3.1.3, p. 149]` for `"dynamic dispatch problem"` in `callgraph-cfi-concurrency-and-scanner-dos.md` with `[PPA §3.1, p. 142] (book p. 142; PDF p. 160), [PPA §2.5, p. 84] (book p. 84; PDF p. 103)` (verified verbatim in `ppa.pdf`). | `RESOLVED -> ACCEPTED` |
| `F-OJ-1003` | `BLOCKING` | Removed `[external]` from book-native `strong update` (`[PPA §2.6.3, p. 115]`, keeping `[external: weak update]`) across `ppa-cyber-vulnerability-analysis/{SKILL.md, README.md, references/memory-heap-and-numeric-bounds-safety.md}` and `ppa-cyber-analysis.md`, and removed `[external]` from book-native `Hindley–Milner` (`[PPA Chapter 5 Concluding Remarks, p. 353]`) across `SKILL.md` and `ppa-cyber-analysis.md`. | `RESOLVED -> ACCEPTED` |
| `F-CJ-1002` | `BLOCKING` | Fixed misidentified small-step SOS table lists (`Tables 3.4, 5.14–5.15` and `Tables 2.5, 3.4, 5.14–5.15`) to **`Tables 2.6, 3.2–3.3, 5.14–5.15`** in `ppa-cyber-vulnerability-analysis/SKILL.md` and `callgraph-cfi-concurrency-and-scanner-dos.md`. | `RESOLVED -> ACCEPTED` |
| `F-CJ-1003` | `BLOCKING` | Realigned BKL refs in `taint-sanitization-and-information-flow.md` (`BKL-016` on `Dom` row, `BKL-038` on `if ℓ ∈ E` schema, `BKL-036` on `ud/du` `Lab⋆^?`) and synced `concept_graph.json` (`ppa.cyber.taint-sanitizer-polarity.issue_refs`) + `BKL-{016,036,037,038}.md` (`92/92` parity). | `RESOLVED -> ACCEPTED` |
| `F-FJ-1001` | `PREFERENCE` | Added `@governing` and `@decision DEC-PPA-001` headers to `ppa-cyber-vulnerability-analysis/README.md` and `SUGGESTED_FIXES.md`. | `RESOLVED -> ACCEPTED` |
| `F-OJ-1004` | `PREFERENCE` | Disambiguated `"interactive IDE query"` as ``"interactive `[external: editor IDE]` query"`` in `ppa-cyber-vulnerability-analysis/SKILL.md`. | `RESOLVED -> ACCEPTED` |
| `F-OJ-1005` | `PREFERENCE` | Replaced the `3` relative `../skills/` markdown links in `ppa-cyber-analysis.md` with plain-text backtick paths matching the other `6` ambient files, and clarified `corpus/RAW_KNOWLEDGE.md` shard-merge order (`Unit 0 Appendices A–C followed by Units 1–6`) via `assemble_raw_knowledge()`. | `RESOLVED -> ACCEPTED` |
| `F-CJ-1004` | `PREFERENCE` | Extended top scope citations in `ppa-cyber-analysis.md` and `ppa-cyber-vulnerability-analysis/SKILL.md` through `[PPA Appendix C, p. 427] (book p. 427; PDF p. 442)` matching `Chapters 1–6 and Appendices A–C`. | `RESOLVED -> ACCEPTED` |
- 2026-11-19 Gate #10 Round 2 (`gate10-v2`): unanimous `3/3 [ALIGNED gate10-v2]` across `P-SWE`, `P-CYBER`, and `P-ARCH` (`0 HARD_BLOCK`, `0 BLOCKING`, `0 PREFERENCE`; #270, #271, #272; all `10/10` Round 1 items verified).

## Cross-Referenced Concepts & Artifacts

- Parent: EPIC-001; depends on: ISS-W6-01; blocks: ISS-W7-01
- `knowledge/skills/ppa-cyber-vulnerability-analysis/SKILL.md`
- `knowledge/skills/ppa-cyber-vulnerability-analysis/references/taint-sanitization-and-information-flow.md`
- `knowledge/skills/ppa-cyber-vulnerability-analysis/references/memory-heap-and-numeric-bounds-safety.md`
- `knowledge/skills/ppa-cyber-vulnerability-analysis/references/callgraph-cfi-concurrency-and-scanner-dos.md`
- `knowledge/ambient-context/ppa-cyber-analysis.md`
- `ontology/concept_graph.json`
- `issues/refactors/REF-007.md`
- `corpus/RAW_KNOWLEDGE.md`

## Verification Receipts
- 2026-11-19 [in_progress] Cross-Book Cyber synthesis (ppa-cyber-vulnerability-analysis/ 301L SKILL, 144L/130L/128L refs, 85L ambient), 10 ppa.cyber.* nodes in 153-node concept_graph.json, deterministic corpus/RAW_KNOWLEDGE.md (13686L across RAW_SHARD_00..06), and REF-007 promoted; staged for Gate #10 (gate10-v1).
- 2026-11-19 [aligned] Gate #10 Round 2 unanimous 3/3 [ALIGNED gate10-v2] across P-SWE, P-CYBER, P-ARCH (#270, #271, #272); 10/10 Round 1 items verified.
- 2026-11-19 [closed] Closed after unanimous 3/3 [ALIGNED gate10-v2] and full Tier-A/hygiene/conformance/unittest verification.
