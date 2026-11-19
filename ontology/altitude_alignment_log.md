<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->
<!-- @decision DEC-PPA-001: Altitude placement is calibrated from three independent calibration perspectives; this log records every calibration, interface decision, and later refactor movement (invariant I5). -->

# Altitude Alignment Log

Living record of `L0`–`L3` calibration and refactoring across the PPA knowledge base. Normative
altitude definitions live in `architecture/ARCHITECTURE.md` §3; this log records how they are
applied, what was decided, and what moved. Entries are append-only and dated; corrections to an
earlier entry are made in place and recorded in a later dated entry.

## Calibration perspectives

Perspective ids are defined once here and used everywhere else in this repository:

| Id | Perspective | Focus |
| :--- | :--- | :--- |
| `P-SWE` | Practical SWE / debugging / CS theory | Operational altitude tests, slicing evidence, Galois framing |
| `P-ARCH` | Architecture / design patterns | Chapter-to-skill mapping, unification edges, calibration rules |
| `P-CYBER` | Cyber program analysis | Security projections, `L2` precondition gates, backlog seeds |

The calibration inputs written from these perspectives are untracked working notes. They are not
part of the repository and cannot be reproduced from a clone; section references such as
"`P-CYBER` §2.2" below identify the part of a note a rule came from and are informational only.
Every rule and seed recorded here is grounded independently by its own book citation or by the
normative architecture.

## Entry 2026-11-18 — Wave 0 three-perspective calibration (`ISS-W0-03`)

**Inputs:** the three Wave 0 calibration notes (`P-SWE`, `P-ARCH`, `P-CYBER`; untracked, see above).

**Status:** calibration synthesized. This entry is an input synthesis, not a judge verdict. No
`[ALIGNED]` marker is recorded here; Gate #1 (`ISS-W1-01`) runs the first adversarial round.

### 1. Consensus calibration rules (all three perspectives agree)

| # | Rule | Origin | Enforcement |
| :--- | :--- | :--- | :--- |
| C1 | Home altitude follows the placement test: source statement → `L3`; needed to choose or state a result → `L1`; performed step/check → `L2`; needed to recognise relevance → `L0` | `ARCHITECTURE.md` B1; all three | Review (Tier B) |
| C2 | Preconditions travel with `L2` steps as explicit checks; derivations stay at `L1`/`L3` | B3; `P-CYBER` §2.2; `P-SWE` §2 | Review + `formal_summary` conditions |
| C3 | Every `L2` step that has a precondition names the symptom observed when it is violated | `P-ARCH` rule 6; `P-SWE` §4 | Review |
| C4 | Complexity bounds travel with their preconditions and the meaning of every parameter. Example: Round Robin halts after at most `d(G_S, T) + 3` iterations for instances of a Bit Vector Framework, with DFSF `T` and reverse postorder, where `d(G_S, T)` is the loop connectedness parameter of the constraint graph `G_S` [PPA Lemma 6.12, p. 380] (book p. 380; PDF p. 396); see BKL-012 | `P-ARCH` rule 7; `P-CYBER` `CONVERGENCE_GATE` | Notation index comparison (Tier A) |
| C5 | Terminology is the book's; external names appear only in projections, marked `[external]` | `P-ARCH` rule 8; `P-CYBER` "native vs derived" marker | Review + `C5.2` |
| C6 | Exercises, mini projects and Concluding Remarks are content (`L3` entries); Concluding Remarks that state limits feed the gotcha ledger | `P-ARCH` rules 4–5 | `C1.9` ledger shape (validator) |
| C7 | A section that "can be omitted on a first reading" (the Preface's wording) keeps its statements at `L1` and its proofs at `L3`; "not essential for the remainder" is a reading-order remark, not a demotion | `P-ARCH` rules 2–3 | Review |
| C8 | Altitudes form an abstraction chain: every `L0`–`L2` claim must be concretizable to an `L3` citation and may over-approximate (vaguer) but never under-approximate (drop a side condition) the source | `P-SWE` §2 | `SMOOTHING_TRAP` Tier A/B |

### 2. Interface decisions resolved in Wave 0

| Topic | Decision | Implemented in |
| :--- | :--- | :--- |
| Ambient-context altitude | `L0` only (80–250 lines), per `ARCHITECTURE.md` §3.1; `MASTER_PLAN.md` relabelled | `scripts/ppa_artifact_rules.py` (ambient budget) |
| Inline citation grammar | `CONFORMANCE_SPEC.md` `N8` syntax pairs a strict bracketed locator (`[PPA §2.1, p. 35]` or a multi-page chapter locator) with its matching book/PDF coordinate pair (e.g. `(book p. 35; PDF p. 54)`); validated fail-closed (`C1.10`) against `corpus/pdf_page_map.json` | `ppa_artifact_rules.resolve_locator`, `validate_ppa_knowledge.check_inline_citations` |
| Accepted `N8` locators | `Preface`, `Contents`, `List of Tables`, `List of Figures` (Roman labels); `§2.1` / `2.1.3`; `Table 2.1` / `Figure C.3`; `Lemma A.4`, `Exercise 2.4`, `Example 6.13` (`statements` inventory, `C1.11`); `Chapter 2` / `Appendix A` (+ `Concluding Remarks`, `Mini Projects`, `Exercises`); `Index of Notation`, `Index`, `Bibliography`; `[12]` | same |
| Citation tolerances | Section: exact `[book_start, book_end]` using `shares_last_page` and `end_matter` boundaries; numbered statements: `[book_page, book_end]`; table/figure: ±1 page; bibliography entry: +1 page | same |
| Edge relation vocabulary | 20 relations (including `corresponds_to` with `basis` for §6.3 unifications) with declared inverses in `ontology/concept_graph.schema.json` (`x-relation-inverses`); symmetry enforced mechanically | `validate_ppa_knowledge.check_graph` |
| Gotcha ledger format | Last level-2 heading of each `corpus/shards/RAW_SHARD_*.md` is `## Gotcha Ledger`; entries `- G-<unit>-<NN>: <text>` paired with a strict `N8` locator (for example `[PPA §A.1, p. 393] (book p. 393; PDF p. 409)`), ids unique across the corpus (e.g. `G-U0-01`); downstream reference coverage checked (`C1.9`) | `ppa_artifact_rules.collect_gotcha_ledgers`, `ppa_artifact_rules.check_gotcha_coverage` |
| `SKILL.md` frontmatter | Exactly `name` + `description`; `name` equals directory, matches `^ppa-[a-z0-9]+(-[a-z0-9]+)*$`; description ≤ 1,024 chars with `Use when` and `Do not use` (or `Don't use`) naming a non-router sibling on token boundaries | `ppa_artifact_rules.check_skill` |
| `evals/cases.yaml` | Required `id`, `prompt`, `expect_skill`; optional `must_mention`, `must_not_mention`, `notes`; every skill (router included) has one (`C3.10`) | `ppa_artifact_rules.check_evals` |
| Export manifest provenance | Each entry carries `frontmatter`, `source_body` (`N4`/`N5` normalised), `body_sha256` (`N6`), and `published_body_sha256` | `scripts/issue_ctl.py export-github --dry-run` |
| Blank page near the index | PDF page 451 is printed page 437 (verified from the rendered page image); the blank verso dropped from the PDF is book p. **438**, before the Bibliography opener at p. 439. All 7 absent pages (34, 140, 210, 364, 416, 428, 438) are blank versos before openers | `corpus/pdf_page_map.json`, `tests/test_wave0_foundation.py` |
| Ontology altitude | `ontology/*.md` and `concept_graph.json` are `L3` graph artifacts (`ARCHITECTURE.md` §3.1); the `P-CYBER` placement of `ontology/*.md` at `L1` is superseded | — |

### 3. Mandatory visual verification rule (OCR text layer)

The text layer of `ppa.pdf` is OCR output. Observed corruption classes: `l`/`I` read as `1` in
item numbers (`C.l`), `o` for `.` in front-matter lists, `)` for `]` in bibliography keys, Greek
letters, subscripts, order symbols (`⊑`, `⊔`, `⊓`) and arrows misrecognised; displayed programs
dropped (Example 1.1 on [PPA §1.2, p. 4] (book p. 4; PDF p. 24)) and tables fragmented
([PPA Table 1.4, p. 24] (book p. 24; PDF p. 44)). Tracked as BKL-011.

Rule (applies to every extractor in every unit):

1. Render the unit's pages into an untracked scratch directory before extraction:
   `pdftoppm -png -r 150 -f <first_pdf_page> -l <last_pdf_page> ppa.pdf <scratch_dir>/p`
   (PDF page numbers come from `corpus/pdf_page_map.json`, never from `book page + constant`).
2. Every formula, inference rule, numbered table, figure, algorithm and notation symbol admitted to
   `L3` is transcribed from the page image, not from the text layer.
3. Each extraction lists the PDF pages it visually verified; a symbol-level claim on an unlisted page
   is a `HALLUCINATED_SYMBOL` finding for the judge panel.
4. Coordinates are taken from the `[PDF_PAGE=X | BOOK_PAGE=Y]` headers of the source slices
   (regenerated by `scripts/extract_ppa_structure.py`; untracked working files) or from the map.

### 4. `L2` precondition gates adopted from `P-CYBER`

These five checks become mandatory checklist items in every `L2` skill whose procedure relies on the
corresponding result (rule C2). The cyber skill instantiates them; sibling skills own the formal core.

| Gate | Check carried by the `L2` step | Book anchor |
| :--- | :--- | :--- |
| `POLARITY_GATE` | Declare may/must direction, order, join and extremal value before designing transfer functions | [PPA §2.3, p. 66] (book p. 66; PDF p. 85) |
| `MONOTONICITY_GATE` | Every transfer function is monotone; non-monotone constructions are named (BKL-003; widening is not required to be monotone, BKL-002) | [PPA §2.3, p. 68] (book p. 68; PDF p. 87) |
| `STRONG_UPDATE_GATE` | Apply strong update or strong nullification ("remove the existing binding before adding a new one") only where the shape-graph conditions of §2.6 license it; the sharing component may be reset only in the case `#into(n_U, H') ≤ 1` with no remaining pointer from the summary node. The fallback wording "otherwise weak update" is `[external]` terminology; the book does not use the term | [PPA §2.6, p. 115] (book p. 115; PDF p. 134), `kill_x`: [PPA §2.6, p. 117] (book p. 117; PDF p. 136); unsharing: [PPA §2.6, p. 125] (book p. 125; PDF p. 144), [PPA Figure 2.21, p. 126] (book p. 126; PDF p. 145) |
| `VARIANCE_GATE` | Mutable reference types are invariant in their content type; channel types `τ chan r` are both covariant and contravariant in `τ` (hence invariant) and covariant in `r`; generalisation side condition enforced (BKL-009) | references: [PPA §5.4, p. 324] (book p. 324; PDF p. 341); channels: [PPA §5.5, p. 348] (book p. 348; PDF p. 365) |
| `CONVERGENCE_GATE` | Ascending Chain Condition or a widening operator; iteration bounds quoted with their preconditions and parameters: the Round Robin bound `d(G_S, T) + 3` holds for instances of a Bit Vector Framework, with DFSF `T` and reverse postorder, and is not quoted for other frameworks | [PPA §4.2, p. 226] (book p. 226; PDF p. 243); [PPA Lemma 6.12, p. 380] (book p. 380; PDF p. 396) |

### 5. Per-unit placement (initial)

| Unit | `L0` hooks | `L2` actionable core | `L3` must-keep formal content |
| :--- | :--- | :--- | :--- |
| U0 App A–C | lattice, fixed point, coinduction, DFS vocabulary | Termination checklist (ACC, monotonicity, widening) | Tarski fixed-point theorem, chains, coinduction principle, DFSF, reverse postorder, loop connectedness |
| U1 Ch 1 | four-approach chooser | approach decision table | Reaching Definitions in the tabled styles: Table 1.1 [PPA Table 1.1, p. 4] (book p. 4; PDF p. 24), Tables 1.2–1.3 [PPA Table 1.2, p. 19] (book p. 19; PDF p. 39), [PPA Table 1.3, p. 21] (book p. 21; PDF p. 41), Table 1.5 [PPA Table 1.5, p. 26] (book p. 26; PDF p. 46), plus the untabled constraint-based formulation (§1.3.2, §1.4); Table 1.4 is the Call-tracking Analysis effect system [PPA Table 1.4, p. 24] (book p. 24; PDF p. 44) and Table 1.6 is the Constant Folding transformation [PPA Table 1.6, p. 27] (book p. 27; PDF p. 47) |
| U2 Ch 2 | bit-vector vs distributive vs monotone | gen/kill design, MFP worklist, context choice, shape transfer | monotone frameworks; MFP vs MOP: MFP ⊒ MOP always, and MFP = MOP when the framework is distributive and path∘(ℓ) ≠ ∅ for all ℓ in E and F [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99); shape-graph invariants |
| U3 Ch 3 | who calls what | constraint generation, cubic solver, context trade-off | coinductive acceptability, Moore family, cubic bound, k-CFA cost |
| U4 Ch 4 | approximate and widen | α/γ design, widening/narrowing recipes | Galois connection laws, induced operations |
| U5 Ch 5 | types as analyses | annotated type/effect design | soundness theorems, inference algorithms |
| U6 Ch 6 | which iteration order | worklist order selection | iteration bounds with preconditions and parameters |

### 6. Gotcha-ledger seeds (to be ledgered by the owning unit)

| Seed | Restriction | Owning unit | Anchor |
| :--- | :--- | :--- | :--- |
| `P-ARCH` EC-04 | Distinct labels for distinct blocks; isolated entries/exits assumptions | U1, U2 | distinct labels: [PPA §1.2, p. 3] (book p. 3; PDF p. 23); isolated entries/exits: [PPA §2.1, p. 39] (book p. 39; PDF p. 58) |
| `P-ARCH` EC-05 | First reading of the annotated-type judgement fails; subsumption-based reading succeeds | U1 | [PPA §1.6, p. 18] (book p. 18; PDF p. 38) |
| `P-ARCH` EC-06 | Equations and inclusions share the least solution, not all solutions (§1.3.2, "The least solution revisited", above the §1.4 heading) | U1 | [PPA §1.3, p. 10] (book p. 10; PDF p. 30) |
| `P-ARCH` EC-07 | Transformation relation neither reflexive nor transitive | U1 | [PPA §1.8, p. 28] (book p. 28; PDF p. 48) |
| `P-ARCH` EC-09 | Semantics based vs semantics directed (last paragraph of §1.1, above the §1.2 heading) | U1 | [PPA §1.1, p. 3] (book p. 3; PDF p. 23) |
| `P-ARCH` EC-08 | Preface scope exclusions (e.g. "single static assignment form") must not be attributed to the book | U1 | [PPA Preface, p. VI] (book p. VI; PDF p. 6) |

### 7. Backlog seeded (non-blocking)

`issues/backlog/BKL-001`..`BKL-012`, deduplicated across the three calibration notes:

| Item | Topic | Origin |
| :--- | :--- | :--- |
| BKL-001 | Unbounded integers vs machine arithmetic | `P-CYBER` |
| BKL-002 | Widening not required to be monotone | `P-CYBER` |
| BKL-003 | Large assumption sets non-monotone | `P-CYBER` |
| BKL-004 | Big-step semantics and divergence | `P-CYBER` |
| BKL-005 | No pointer arithmetic in shape analysis | `P-CYBER` |
| BKL-006 | Dead-store elimination vs zeroization | `P-CYBER` |
| BKL-007 | Cost of context (k-CFA, CPA) | `P-CYBER` + `P-ARCH` EC-12 (merged) |
| BKL-008 | Closed-world assumption vs dynamic code | `P-CYBER` |
| BKL-009 | Effect subtraction and generalisation side condition | `P-CYBER` |
| BKL-010 | Irreducible flow graphs | `P-CYBER` |
| BKL-011 | OCR text layer corrupts mathematics | `P-ARCH` EC-01 + `P-SWE` |
| BKL-012 | Round Robin bound `+ 3`, not `+ 2` (Bit Vector Framework instances) | `P-ARCH` EC-02 |

Not seeded as backlog: `P-ARCH` EC-03 (absent book pages) is resolved (§2, blank page row); EC-10
(notation reuse) goes to `ontology/notation_index.md` as scope-qualified entries in Unit 0; EC-11
(Chapter 4 has no tables) is already encoded in the per-chapter inventory (`C1.4`); the `P-SWE`
tolerance notes are recorded as validator decisions (§2).

### 8. Open decisions (escalated to the coordinator)

1. **Home of shared appendix references.** Proposal (`P-SWE`): Appendices A and B live in
   `knowledge/skills/ppa-program-analysis/references/` (router-owned, one hop from the router, so
   `C3.9` ownership holds and siblings may link to them without entering another `SKILL.md` body,
   `C3.8`); originally `P-ARCH` proposed co-locating Appendix C with `ppa-fixedpoint-solvers`. A neutral
   top-level location has no owning `SKILL.md` and would fail `C3.9`. **Resolved** in `DEC-PPA-008`
   and subsequently updated in `W1-2` (`MASTER_PLAN.md`, see `Entry 2026-11-19`) to router-own all three appendices `A–C`.
2. **Unification candidates `U11`/`U12`** (`P-ARCH` §4): `U11` folds into the `U1`/`U8` write-up;
   `U12` has an external right-hand side and becomes a projection, not an edge.

## Entry 2026-11-18 — Gate #0 corrections (`ISS-W0-03`)

**Trigger:** the three Gate #0 judge reports (findings `F-CJ-*`, `F-FJ-*`, `F-OJ-*`; see the
Rebuttal & Attribution Summary in `issues/shards/ISS-W0-03.md`). Corrections made in place in the
entry above; every source claim touched was re-read from the text layer and, for symbols, from the
rendered page image.

| # | Correction | Finding ids |
| :--- | :--- | :--- |
| 1 | Model and worker labels replaced by the perspective ids `P-SWE`, `P-ARCH`, `P-CYBER`, defined once; all untracked scratch paths removed; inputs declared untracked and not reproducible from a clone | F-CJ-001, F-OJ-009, F-FJ-025 |
| 2 | EC-06 re-anchored to [PPA §1.3, p. 10] (book p. 10; PDF p. 30) (§1.3.2); EC-09 re-anchored to [PPA §1.1, p. 3] (book p. 3; PDF p. 23) | F-CJ-006, F-FJ-007, F-OJ-016 |
| 3 | Lemma 6.12 restatements (rule C4, `CONVERGENCE_GATE`) carry "for instances of a Bit Vector Framework, with DFSF `T` and reverse postorder" and the parameter `d(G_S, T)` | F-FJ-012, F-OJ-003 |
| 4 | MFP = MOP restated with both conditions of Lemma 2.32: distributivity and path∘(ℓ) ≠ ∅ for all ℓ in E and F [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99) | F-OJ-002 |
| 5 | `STRONG_UPDATE_GATE` anchored at the strong-update definition [PPA §2.6, p. 115] (book p. 115; PDF p. 134), with p. 125 and Figure 2.21 for the unsharing case; "weak update" marked `[external]` | F-OJ-007, F-CJ-008 |
| 6 | Channel invariance re-anchored to [PPA §5.5, p. 348] (book p. 348; PDF p. 365); isolated entries/exits re-anchored to [PPA §2.1, p. 39] (book p. 39; PDF p. 58) | F-OJ-008, F-CJ-008 |
| 7 | U1 row: Reaching Definitions tables are 1.1, 1.2, 1.3 and 1.5; Table 1.4 is call-tracking and Table 1.6 is Constant Folding | F-OJ-008 |
| 8 | Rule C7 quotes "can be omitted on a first reading" verbatim; EC-08 uses the book's "single static assignment" wording | F-OJ-020 |
| 9 | `MONOTONICITY_GATE` also names BKL-002 | F-CJ-008 |

**Decision `DEC-PPA-008` (shared appendix references; revised `W1-2` / `W2-4`).** Shared `L1` references
for Appendices A, B, and C (amended from Wave 0's initial Appendix C placement in `ppa-fixedpoint-solvers`
via `MASTER_PLAN.md` `W1-2` and `REF-001`) are permanently router-owned under
`knowledge/skills/ppa-program-analysis/references/`; sibling skills link to them there (`C3.8`, `C3.9`),
while Chapter 6 iterative solver algorithms remain scoped to `ppa-fixedpoint-solvers`. Recorded in
`MASTER_PLAN.md` Decision Log; closes open decision 1 above.

**Node `altitude` semantics (F-FJ-009).** In `ontology/concept_graph.json`, a node's `altitude` is
the highest altitude at which the concept is surfaced with content. An `L3` entry for the concept
always exists, whatever the value of `altitude`; the field never means "the only altitude". Unit
authors apply this reading when seeding and refactoring nodes; refactor triggers that "raise
`altitude`" use the same reading.

## Entry 2026-11-19 — Wave 2 (`W2-3`) & Part I Holistic Altitude Refactoring (`W2-4`)

### 1. Unit 2 (`W2-3`) Coverage & Budget Summary

- Added `22` Chapter 2 concept nodes (`ontology/concept_graph.json` `59 -> 81`, covering `10/10` Tables `2.1–2.10` and `23/23` Figures `2.1–2.23`) grounded in `corpus/shards/RAW_SHARD_02a_intraproc_dfa.md` (`G-U2a-01..35`) and `corpus/shards/RAW_SHARD_02b_interproc_shape.md` (`G-U2b-01..34`).
- Packaged Unit 2 deliverables strictly inside altitude ceilings (`N2`): `knowledge/ambient-context/ppa-dataflow-and-shape.md` (`122L` in `[80, 250]`, `0` YAML frontmatter), `knowledge/skills/ppa-dataflow-and-slicing/SKILL.md` (`270L` in `[250, 499)`), and three `L1` reference modules (`intraprocedural-analyses-and-frameworks.md` `208L`, `interprocedural-and-correctness.md` `164L`, `shape-analysis.md` `159L`, all `<= 450L`).
- Instantiated non-blocking Chapter 2 backlog `BKL-036`..`BKL-050` alongside reconciled pre-seeded `BKL-003`, `BKL-005`, `BKL-006`.

### 2. Part I Holistic Altitude Review (`App A–C + Ch 1 + Ch 2`, `W2-4`)

Evaluated every Part I artifact across `L0`–`L3` against `architecture/ARCHITECTURE.md` §6 (`T1`–`T9`, `I1`–`I6`):

- **`T1` Ceilings**: Audited `knowledge/skills/ppa-program-analysis/references/chapter-1-five-formulations.md` (`446/450L`). Because all 446 lines remain strictly scoped to Chapter 1's five-approach comparison and `Tables 1.1–1.6`, zero lines duplicate Chapter 2 general frameworks; flagged at `4L` below ceiling (no Chapter 2 additions permitted into Chapter 1).
- **`T2` Cross-Skill Shared Promotion (`DEC-PPA-008`)**: Rather than repeating lattice/ACC foundations, Tarski/induction proofs, or Chapter 1 formulations inside Chapter 2 references, wired direct `L1 -> L1` links from `ppa-dataflow-and-slicing/references/*.md` to router-owned `chapter-1-five-formulations.md` and `appendix-{a,b,c}*.md` (`DEC-PPA-008` revised in `W1-2` so router permanently hosts all three appendices), plus reverse active-module links in `ppa-program-analysis/SKILL.md` (`80L` `< 99L`, `0` `C3.8` violations).
- **`T3` Procedure vs Specification Separation**: Audited `ppa-dataflow-and-slicing/SKILL.md` (`270L`, incl. the 6-line operator quick-reference card in `§7`). Confirmed all full semantic/framework definition tables, proof derivations, and `Case 1–3` / `Invariants 1–5` specs stay at `L1`/`L3`, leaving only precondition gates and compact operator reminders at `L2`.
- **`T4` Unification Purity (`U1`–`U10`) & Cross-Unit Symmetry**: Audited all 81 concept nodes for premature `U*` tags. Fixed staged `U4` -> `U6` and subsequently reclassified the two Part I cross-unit pairs (`ppa.dfa.constant-propagation` and `ppa.dfa.mop-vs-mfp` targeting `ppa.ai.adjunction-induced-analysis`) from `corresponds_to` to symmetric `related_to` (reserving `U6` `corresponds_to` for `§4.3–§4.5` in Wave 4 where the source explicitly proves `§4.5` adjunctions), reclassified `worklist-mfp -> chaotic-iteration` (`refines`), `worklist-mfp -> reverse-postorder` (`related_to`), and `flow-insensitive-iav -> annotated-type-constructors` (`contrasts_with`) so `U2`/`U5`/`U10` stay clean for Chapters 3 and 6, and closed all 18 missing cross-unit inverse edges.
- **`T5` Sibling Boundary Sharpening (`C4`)**: Excluded Ch 1 approach comparison and App A–C theory in `ppa-dataflow-and-slicing/SKILL.md` `description` (`829` chars `< 1024`, Jaccard `0.1917 < 0.50`) and added reciprocal eval discrimination cases (`sib-dataflow-shape-interproc`, `neg-router-approach-foundations`).
- **`T6` & `T7` Provenance and Symbol Scoping**: Added unindexed Chapter 2 symbols `U-35`, `U-36`, `U-38` (`Lab_{⋆}^{?}`, `flow_{⋆}^{R}/inter-flow_{⋆}^{R}`, `k_{x} : ALoc → ALoc` `[PPA §2.6.3, p. 117]`) and scoped `H`/`⊑`/`k` under `Overloaded symbols` in `ontology/notation_index.md`, aligned `Rule B1` node `altitude` across all `81` `concept_graph.json` nodes (`10` `U0`/`U2b` `L3 -> L1`, `6` `U2` `L2 -> L1`, removed casual `L0` mention ref on `while-flow-graphs`), wired all `BKL-003/005/006` and `BKL-036..050` pointers (`C6.6`, `C6.7`, `§6.4`), and re-verified invariants `I1`–`I5`.

## Entry 2026-11-19 — Gate #3 & Gate #4 Round 1 Remediation (`gate3-v2` / `gate4-v2`)

**Trigger:** Round 1 adversarial judge reviews (`F-FJ-301..307, 401..405`, `F-OJ-301..307, 401..406`, `F-CJ-301..306, 401..405`; recorded in `issues/shards/ISS-W2-03.md` and `ISS-W2-04.md`).

| # | Remediation | Finding IDs |
| :--- | :--- | :--- |
| 1 | Restored `kill_x` comprehension guards, `Case 3` / `[x.sel:=y]` guards, `℘` `dom(ℋ)` domain, isolated-entries + `path∘(ℓ) ≠ ∅` `MFP = MOP` guards, and full `CP`/`VP` productions across `ppa-dataflow-and-slicing` `L1`/`L2` & `RAW_SHARD_02b` | `F-FJ-301..303`, `F-OJ-301`, `F-CJ-301, 304` |
| 2 | Removed `𝒫(path∘(ℓ))` / `§1.5` misattribution at `p. 82`, tagged `[external]` security/literature terms, and standardised `Red(F)` (`F(x) ⊑ x`) terminology across `L0`–`L3` | `F-OJ-302, 303, 406`, `F-CJ-303`, `F-FJ-307` |
| 3 | Repaired `evals/cases.yaml` YAML escaping (`≤`) + `y := x * x` alignment, eliminated raw `C1.10` placeholder & plural book-page range tokens across tracked files, and corrected `BKL-037/038` `L1 anchor` + backlog parity | `F-FJ-304, 305, 401, 403, 405`, `F-OJ-304..306, 405`, `F-CJ-302` |
| 4 | Reconciled `concept_graph.json` `Rule B1` `altitude` (`81/81` nodes), reclassified premature `U6` `corresponds_to` to `related_to`, fixed `notation_index.md` (`U-35/36/38`, `H`, `⊑`, `k/k_x`), and synced `DEC-PPA-008` + `kill_x` `p. 117` in this log | `F-FJ-306, 402`, `F-OJ-401..404`, `F-CJ-305, 401..403` |

## Entry 2026-11-19 — Wave 3 (`W3-1` + `W3-2`) & Cumulative Altitude Refactoring (`REF-003`)

1. **Unit 3 (`W3-1` + `W3-2`) Coverage & Ceiling Verification**:
   - Promoted Chapter 3 `L3` shards `corpus/shards/RAW_SHARD_03a_0cfa.md` (`1,360` lines, `G-U3a-01..26`) and `corpus/shards/RAW_SHARD_03b_kcfa_cpa.md` (`1,106` lines, `G-U3b-01..30`) covering all `10/10` Tables `3.1–3.10`, `6/6` Figures `3.1–3.6`, `34/34` Statements `3.1–3.34`, `Mini Projects 3.1–3.4`, and `Exercises 3.1–3.17`.
   - Promoted strictly within `N2` altitude budgets: `knowledge/ambient-context/ppa-cfa-and-constraints.md` (`99L` in `[80, 250]`, `0` YAML frontmatter `C3.6`), `knowledge/skills/ppa-control-flow-and-constraints/SKILL.md` (`260L` in `[250, 499)`, `889`-char description), and three `L1` references (`cfa-core-and-coinduction.md` `193L`, `constraint-generation-and-cubic-solver.md` `145L`, `polyvariant-kcfa-cpa-and-dfa.md` `136L`, all `<= 450L`, `0` frontmatter).
2. **Cumulative Chapter 3 Refactoring (`REF-003`, Triggers `T2`–`T7`)**:
   - **`T2` Cross-Skill `L1` Links (`DEC-PPA-008`)**: Linked `ppa-control-flow-and-constraints/references/*.md` to router-owned `chapter-1-five-formulations.md` and `appendix-{a,b,c}*.md` (`U9` coinduction/Tarski), and wired bidirectional `L1 -> L1` links between `ppa-dataflow-and-slicing/references/{intraprocedural-analyses-and-frameworks.md,interprocedural-and-correctness.md}` (`208L`, `171L`) and `ppa-control-flow-and-constraints/references/*` (`U4` `§2.3 ↔ §3.5.2`, `U5` `§2.5.4/§2.5.5 ↔ §3.6.1/§3.6.2`, `Table 3.7`, `Figure 3.3`).
   - **`T3` & `T5` Procedural Purity & Router Activation**: Activated `ppa-control-flow-and-constraints` (`§§3.1–3.6`) in `ppa-program-analysis/SKILL.md` (`81L < 90L`, `18L` below `99L` ceiling, `0` `C3.8` links), added `sib-cfa-cubic-and-kcfa` to router evals, and added `sib-cfa-kcfa-cpa-closures` to `ppa-dataflow-and-slicing/evals/cases.yaml` (`C4.7` parity).
   - **`T4` Graph Symmetry & `Rule B1` Parity**: Merged `16` `ppa.cfa.*` concepts (`ontology/concept_graph.json` `81 -> 97` nodes, `30` inverse edges added, `97/97` `Rule B1` parity) with symmetric `U4` (`ppa.cfa.cfa-with-lattice-dfa` ↔ `ppa.dfa.monotone-framework`), `U5` (`ppa.cfa.uniform-k-cfa` ↔ `ppa.interproc.call-strings`, `ppa.cfa.cartesian-product-algorithm` ↔ `ppa.interproc.assumption-sets`), and `U9` (`ppa.cfa.coinductive-well-definedness` ↔ `ppa.proof.coinduction`, `ppa.fixpoint.tarski`) `corresponds_to` `basis` records.
   - **`T6` & `T7` Backlog & Notation Disambiguation**: Instantiated `BKL-051..062` (with distinct `## Technical Analysis / Mechanism` failure traces per `C6.6`/`C6.7`) and reconciled `BKL-007`, `BKL-008` (`ppa.dfa.while-flow-graphs`), and `BKL-011` (`ppa.notation.index` + `ppa.cfa.*`); audited `Index of Notation` (`ce`, `CEnv`, `𝒞_{⋆}`, `Term_{⋆}` already indexed) and added unindexed `U-39..U-45` plus `⊨`, `𝒬`, `r`, `C(ℓ)`, `F_{⋆}`, `\widehat{R}`, `\widehat{S}_{∘}/\widehat{S}_{•}` collision/typeface notes in `ontology/notation_index.md`.

## Entry 2026-11-19 — Gate #5 Round 1 Remediation (`gate5-v2`)

**Trigger:** Gate #5 Round 1 three-track adversarial judge reviews (`F-OJ-501..507`, `F-FJ-501..508`, `F-CJ-501..507`; full 1-to-1 disposition table in `issues/shards/ISS-W3-02.md`).

| # | Remediation | Finding IDs |
| :--- | :--- | :--- |
| 1 | Corrected `RAW_SHARD_03a_0cfa.md` (`1,372L`): end-matter counts (`Mini Projects 3.1–3.4`, `Exercises 3.1–3.17`), 3-candidate `Example 3.3`, `Remark.` p. 145 (`(Var ∪ Lab) → Val̂` & IRs), `IExp` branch types, `Tables 3.2–3.3` `[app_fun]` `[x ↦ v₂]` rightmost order & `[if₂,₃]`/`[bind₂]` relabelling to `ℓ`, `Example 3.8`, `Example 3.12` (on `Ex 3.7`), `Mini Project 3.1` `p. 202` refs, and repurposed `F-U3a-05`/`BKL-052` around `Fact 3.11` & outer-label relabelling (`cfa-core-and-coinduction.md` `202L`) | `F-OJ-501`, `F-FJ-503, 505`, `F-CJ-504` |
| 2 | Restored `Uniform k-CFA` (`Val̂ = 𝒫(Term × CEnv)`, `Table 3.10` `⊨_δ^{ce}`, `Example 3.34` `{(fn y => y^6, ce₀)}`), standard `k-CFA` (`Cachê = (Lab × CEnv) → Val̂`, `[156, 157, 158]`), and `Polynomial k-CFA` (`Val̂ = 𝒫(Term × Δ)`, `O(n^6)` at `k=1`, `p. 195`) across `L0`–`L2`, `concept_graph.json` (`U5` symmetry), and `BKL-057`; fixed `d_c ∈ Data`, `Table 3.8`, `Example 3.27 / Figure 3.6 / Example 3.30 (p. 187) / Example 3.31`, Oracle #3, and `evals/cases.yaml` (`ppa-cfa-and-constraints.md` `100L`, `polyvariant-kcfa-cpa-and-dfa.md` `150L`, `SKILL.md` `269L`, `desc=900`c, max Jaccard `0.2605`) | `F-OJ-502, 504`, `F-FJ-501, 502`, `F-CJ-501, 503` |
| 3 | Repaired `§3.6.2` `CPA [app]` `F-U3b-05` (`)` before `^ℓ`, `, δ_b` in `ρ̂(x_i, δ_b)`), `Mini Projects 3.1–3.4` (`p. 202` prose `⊨_s`, `p. 203` flat `C(ℓ₁,...,ℓ_n)`, `p. 204` `Label of term * label`, `new_π`/`x := e₀`/`me` unprinted `[assign]` + `p. 200` `[133]` strong-kill guard), `MONOTONICITY_GATE` (`S₁ ∩ S₂` monotone vs `¬S` & variable-LHS guards `p. 201`), and `Ex 3.2–3.7/3.16–3.17` (`constraint-generation-and-cubic-solver.md` `147L`, `BKL-058..062`) | `F-OJ-503`, `F-FJ-503, 504`, `F-CJ-502, 505` |
| 4 | Enforced `P2` `[external]` attribution and exact `[2]`/`[9]`/`[156..158]` citations across `L0`–`L3`, `concept_graph.json`, and `BKL-061`; removed bare `⊨` from `U-39` (`N1-006` xref, adding `⊨'_{s}`, `⊨'_{D}`, `⊨_{me}`); updated `RAW_SHARD_03b` `U2 -> U5`; linked `intraprocedural-analyses-and-frameworks.md` (`U4`) in `SKILL.md`; renumbered Procedure 2 `5. -> 4.`; deduplicated `abstract-0cfa <-> subject-reduction`; and synced `56/56` `BKL` parity (`BKL-051/053/062`) | `F-OJ-505..507`, `F-FJ-505..508`, `F-CJ-506, 507` |

## Entry 2026-11-19 — Wave 4 (`W4-1` + `W4-2`) & Cumulative Altitude Refactoring (`REF-004`)

1. **Unit 4 (`W4-1` + `W4-2`) Coverage & Ceiling Verification**:
   - Promoted Chapter 4 `L3` shards `corpus/shards/RAW_SHARD_04a_galois_widening.md` (`971` lines, `24/24` `G-U4a-01..24`) and `corpus/shards/RAW_SHARD_04b_combinators_induced.md` (`1,419` lines, `24/24` `G-U4b-01..24`) covering `§§4.1–4.5`, `0` tables, `10/10` `Figures 4.1–4.10`, `15/15` displays `(4.1)–(4.15)`, `45/45` `Statements 4.1–4.45`, `Concluding Remarks`, `Mini Projects 4.1–4.3`, and `Exercises 4.1–4.24` (`239/239` `G-U0..G-U4b` covered in `knowledge/`).
   - Promoted strictly within `N2` altitude budgets: `knowledge/ambient-context/ppa-abstract-interpretation.md` (`107L` in `[80, 250]`, `0` YAML frontmatter), `knowledge/skills/ppa-abstract-interpretation/SKILL.md` (`263L` in `[250, 499)`, `955`-char description, `0.2132` max Jaccard vs `ppa-control-flow-and-constraints` / `0.1923` vs `ppa-dataflow-and-slicing`), and three `L1` references (`correctness-and-fixed-points.md` `260L`, `galois-connections-and-insertions.md` `161L`, `combinators-and-induced-operations.md` `169L`, all `<= 450L`, `0` frontmatter).
2. **Cumulative Chapter 4 Refactoring (`REF-004`, Triggers `T2`–`T7`)**:
   - **`T2` Cross-Skill `L1` Links (`DEC-PPA-008`)**: Replaced the deferred `§4.5` pointer in `ppa-dataflow-and-slicing/references/intraprocedural-analyses-and-frameworks.md` (`208L`) with active canonical `U6`/`U7` links into `combinators-and-induced-operations.md` and `correctness-and-fixed-points.md`; added `Mini Project 4.2` (`SH → 𝒫(SG)`) pointer in `shape-analysis.md` (`161L`) and `Mini Project 4.3` (`Table 3.9` Galois lifting) pointer in `polyvariant-kcfa-cpa-and-dfa.md` (`153L`), reciprocated in `ppa-abstract-interpretation/SKILL.md` and `combinators-and-induced-operations.md`.
   - **`T3` & `T5` Router Activation & Boundaries**: Activated `ppa-abstract-interpretation` (`§§4.1–4.5`) in `ppa-program-analysis/SKILL.md` (`82L < 92L`, `17L` below `99L` ceiling, `0` `C3.8` violations), added `sib-ai-galois-and-combinators` to router evals, and added reciprocal `U6` case `sib-ai-galois-induced-ab` to `ppa-dataflow-and-slicing/evals/cases.yaml` (`C4.7`).
   - **`T4` Graph Symmetry & `Rule B1` Parity**: Merged `16` `ppa.ai.*` concepts into `ontology/concept_graph.json` (`97 -> 113` nodes, `22` inverse edges added, `113/113` `Rule B1` parity, `10/10` Figures, `5/5` sections `4.1–4.5`) with byte-identical symmetric `U6` (`ppa.ai.generalised-monotone-framework` ↔ `ppa.ai.adjunction-induced-analysis` and `ppa.dfa.monotone-framework`) and `U7` (`ppa.ai.widening` ↔ `ppa.order.chain-conditions` and `ppa.dfa.monotone-framework`) `corresponds_to` `basis` objects.
   - **`T6` & `T7` Backlog & Notation Audit**: Instantiated `BKL-063..072` (distinct mechanisms + `L1`/`L2`/`L3` pointers) and reconciled pre-seeded `BKL-001`, `BKL-002` (`ppa.ai.widening`; W6 solver link queued for `ISS-W6-01`), `BKL-013`, `BKL-024`, `BKL-029`, `BKL-033` (`68/68` promoted `BKL` parity); added unindexed Chapter 4 rows `U-46..U-53` (`∇_{K}/LB_{K}/UB_{K}`, `Δ_{N}`, `ϒ`, `Sign′`, `⊗/AB/LR`, `ȷ/SS/SH`, `∇_{L}/Δ_{L}`, `ρ[L]/⊑^{d}/Ξ`) and `ρ` scope collision row in `ontology/notation_index.md` without duplicating `N1`–`N3` or `U-32`.

## Entry 2026-11-19 — Gate #6 Round 1 Remediation (`gate6-v2`)

**Trigger:** Gate #6 Round 1 three-track adversarial judge reviews (`F-FJ-601..604`, `F-CJ-601..604`, `F-OJ-601..605`; full 1-to-1 disposition table in `issues/shards/ISS-W4-02.md`).

| # | Remediation | Finding IDs |
| :--- | :--- | :--- |
| 1 | Replaced nonexistent `BKL-024` `"notation-index spacing"`/`"spacing anomaly"` note in `galois-connections-and-insertions.md` (`161L`) and `SKILL.md` (`264L`) with actual `ς`/`ϕ`/`Δ` scope collisions (`pp. 244, 225, 230`), moved `BKL-024` `issue_ref` to `ppa.ai.galois-insertion-and-reduction`, and added Ch 4 `L1`/`L2` anchors on `BKL-013/024/029/033` | `F-FJ-601`, `F-OJ-605` |
| 2 | Removed bare `` `ρ` `` from `U-53` in `ontology/notation_index.md` (retaining `` `ρ[L]`, `⊑^{d}`, `Ξ` `` + `N2-035` cross-ref), changed `U-49` `Sign′` to `Figure 4.10` labels `{⊥, -, 0, +, -0, 0+, ⊤}`, updated `U-51` `SH` to `pp. 274–275` paired singular companions, tagged `` `[external: uco(L)]` `` in `README.md:21`, and synced `REF-004.md` & this log | `F-FJ-602`, `F-CJ-601, 603`, `F-OJ-601` |
| 3 | Tagged `[external: CFG loop-cutset placement]` separately from `Chapter 6 Exercise 6.13` in `correctness-and-fixed-points.md:249` (`SKILL.md:255`, `RAW_SHARD_04a:834`), converted all `44` plural page-range companion tokens in `RAW_SHARD_04a_galois_widening.md` (`971L`) to paired singular companions, and corrected `RAW_SHARD_04b_combinators_induced.md` (`1,422L`) `Exercises 4.3–4.4`, `p. 159` `Theorem 3.10`, and `P. Cousot [35]` | `F-FJ-603`, `F-CJ-602`, `F-OJ-603, 604` |
| 4 | Stripped all unit-4 staging IDs from `BKL-063..072.md`, replaced summary-repeating prose with distinct causal mechanisms, refined `BKL-065.md:22` `d_hat` count phrasing, added `p. 229` (`BKL-068`), `p. 267` (`BKL-071`), and `pp. 223, 226` + `04b` `L1`/`L3` anchors (`BKL-069`), and regenerated `issues/export_manifest.json` (`98` issues) | `F-FJ-604`, `F-CJ-604`, `F-OJ-602` |

- **Gate #6 Round 2 Closure (`gate6-v2`)**: Unanimous `3/3 [ALIGNED gate6-v2]` across `P-ARCH`, `P-SWE`, and `P-CYBER` (`0` `HARD_BLOCK`, `0` `BLOCKING`; #238, #239, #240), plus Round 2 `PREFERENCE` polishes (`U-53` `italic, roman` in `notation_index.md:511`, `BKL-024.md` move note, `BKL-065.md:33` `bare d_hat`).

## Entry 2026-11-19 — Wave 5 (`W5-1` + `W5-2`) & Cumulative Chapter 5 Refactoring (`REF-005`)

1. **Unit 5 (`W5-1` + `W5-2`) Coverage & Ceiling Verification**:
   - Promoted Chapter 5 `L3` shards `corpus/shards/RAW_SHARD_05a_annotated_types_inference.md` (`868` lines, `22/22` `G-U5a-01..22`, `Tables 5.1–5.8`) and `corpus/shards/RAW_SHARD_05b_effects_regions_behaviours.md` (`1,668` lines, `26/26` `G-U5b-01..26`, `Tables 5.9–5.18`, `Figures 5.1–5.2`, `Mini Projects 5.1–5.5`, `Exercises 5.1–5.15`) covering `§§5.1–5.5`, `18/18` Tables, `2/2` Figures, and `299/299` cumulative `G-U0..G-U5b` gotchas (`0` uncovered).
   - Promoted strictly within `N2` altitude budgets: `knowledge/ambient-context/ppa-types-effects-and-regions.md` (`136L` in `[80, 250]`, `0` frontmatter), `knowledge/skills/ppa-types-effects-and-regions/SKILL.md` (`318L` in `[250, 499)`, `979`-char description, `0.2069` max Jaccard vs active siblings), and three `L1` references (`annotated-types-and-cfa-soundness.md` `289L`, `inference-unification-and-subtyping.md` `283L`, `effects-exceptions-regions-and-behaviours.md` `275L`, all `<= 450L`, `0` frontmatter).
2. **Cumulative Chapter 5 Refactoring (`REF-005`, Triggers `T2`–`T7`)**:
   - **`T2` Cross-Skill `L1` Links (`DEC-PPA-008`)**: Wired reciprocal `U8` (`§§5.1–5.4`, `(5.2)` vs `0-CFA`) `L1 <-> L1` links between Chapter 5 and Chapter 3 (`cfa-core-and-coinduction.md` / `constraint-generation-and-cubic-solver.md`), reciprocal `X1` (`§2.6` vs `§5.4.3`) and `§2.5.6` `IAV` links between Chapter 5 and Chapter 2 (`shape-analysis.md`, `interprocedural-and-correctness.md`), and Chapter 1 inline `L1` pointers (`chapter-1-five-formulations.md` `447L`), updating `ppa-control-flow-and-constraints/SUGGESTED_FIXES.md` to clear `U8`.
   - **`T3` & `T5` Router Activation & Boundaries**: Activated `ppa-types-effects-and-regions` (`§§5.1–5.5`) in `ppa-program-analysis/SKILL.md` (`83L <= 89L`, `16L` below `99L`, `0` `C3.8` violations), added `sib-types-regions-behaviours` in router evals, and added reciprocal `U8`/`X1` boundary cases (`sib-types-u8-subtyped-cfa` in Ch 3 and `sib-types-tofte-talpin-regions` in Ch 2, `C4.7`).
   - **`T4` Graph Symmetry & `Rule B1` Parity**: Merged `18` `ppa.tes.*` nodes into `ontology/concept_graph.json` (`113 -> 131` nodes, `21` inverse edges added, `Rule B1` `131/131`, `18/18` Tables `5.1–5.18`, `2/2` Figures `5.1–5.2`, `5/5` sections `5.1–5.5`) with byte-identical symmetric `U8` `corresponds_to` `basis` objects linking `ppa.cfa.constraint-0cfa` with `ppa.tes.annotated-cfa-types` and `ppa.tes.shape-conformant-subtyping`.
   - **`T6` & `T7` Backlog & Notation Audit**: Instantiated `BKL-073..082` (`10` items covering `48/48` `G-U5a`/`G-U5b` gotchas, distinct causal mechanisms, zero unit-5 staging IDs) and reconciled pre-seeded `BKL-004`, `BKL-009`, `BKL-011`, `BKL-026`, `BKL-030`, `BKL-031` (`80/80` promoted `BKL` parity); added unindexed Chapter 5 rows `U-54..U-60` and `π`/`FV` collision rows in `ontology/notation_index.md` with zero `N1–N3`/`U-01..U-53` duplicates.

## Entry 2026-11-19 — Wave 5 (`W5-3`) Part II Holistic Audit & Cross-Paradigm Matrix (`REF-006`)

- **Part II Cross-Paradigm Synthesis (`ontology/cross_paradigm_matrix.md`, `221L`)**: Synthesised Chapters 1–6 and Appendices A–C across ten normative axes, documented canonical unifications `U1`–`U10` and extended bridges `X1`–`X5`, codified practitioner paradigm-selection workflows and anti-patterns, and passed Part II holistic hygiene, Jaccard (`0.2605 << 0.50` max across all 4 active domain skills), `Rule B1` (`131/131`), and `80/80` `BKL` parity gates ahead of Gates #7 and #8.

## Entry 2026-11-19 — Gates #7 & #8 Round 1 Remediation (`gate7-v2`, `gate8-v2`)

**Trigger:** Gates #7 and #8 Round 1 three-track adversarial reviews (`[DISAGREE gate7-v1]`, `[DISAGREE gate8-v1]`: `F-OJ-701..704`, `F-FJ-701..703`, `F-CJ-701..703`, `F-OJ-801..805`, `F-FJ-801..805`, `F-CJ-801..804`; full 1-to-1 disposition tables recorded in `issues/shards/ISS-W5-02.md` and `issues/shards/ISS-W5-03.md`).

| # | Gate | Remediation | Finding IDs |
| :--- | :--- | :--- | :--- |
| 1 | Gate #7 | Fixed `ontology/notation_index.md` (`U-54` `Γ̂ ⊢_{CA} e : σ̂ & φ` at `§5.5.1`/`Table 5.16`; `U-55` capture-free closed substitution; `U-57` postfix `π:=`; `U-58` `Table 5.11`; `U-59` removed fabricated `\widehat{τ} com φ`, added `Λ` cross-ref `N2-026` and `Table 5.14`; `U-60` `num^{φ}` + `Mini Project 5.4`; line `2` split plural range) | `F-OJ-701, 704`, `F-FJ-701..703`, `F-CJ-701, 703` |
| 2 | Gate #7 | Fixed `[83, 160, 161]` in `inference-unification-and-subtyping.md:192,237` and clarified `([71] Heintze; [external: Palsberg–O'Keefe 1995])` across `L1` (`:226`) and `ontology/concept_graph.json:6354,9597` | `F-OJ-702, 703` |
| 3 | Gate #7 | Enforced `P2` `[external]` attribution for `Tofte`, `Talpin`, `Birkedal`, and `Agesen` across `ppa-types-effects-and-regions/{SKILL.md,README.md,evals/cases.yaml,references/effects-exceptions-regions-and-behaviours.md}`, `knowledge/ambient-context/ppa-types-effects-and-regions.md`, `RAW_SHARD_05b_effects_regions_behaviours.md`, `concept_graph.json:9880` (`#3-stack-based-...` anchor synced at `:9957`), and W5 sibling `evals/cases.yaml` | `F-CJ-702` |
| 4 | Gate #8 | Fixed `ontology/cross_paradigm_matrix.md`: scoped `Lemma 5.22` to `§5.3.4` `SOL(C)` and `Exercise 5.9` to `§5.4` subtyping loss (`:47`), separated `§5.4.1–§5.4.3` big-step Natural Semantics from `§5.5` small-step SOS (`:41`), replaced `[159]`/`Robinson [external]`/`§5.4.3` decidability errors (`:46`), added `X2` Galois insertion + `γ(⊥_M)=⊥_L` + `∇_M=⊔_M` at `p. 270` (`:156`), fixed `U6` `Proposition 4.29`/`Fact 4.30`–`4.31` (`:97`) + `§5.4.1` `ref_ϖ` (`:45`), qualified `U8` `Exercise 5.4`/`5.9` (`:119-122`), and tagged `[external]` (`Herbrand`, `integrated form`, `Scott continuity`, `editor IDE`, `vtable`) | `F-OJ-801..805`, `F-FJ-801..805`, `F-CJ-801..804` |

- **Gate #7 & #8 Round 2 Closure (`gate7-v2`, `gate8-v2`)**: Unanimous `3/3 [ALIGNED gate7-v2]` and `3/3 [ALIGNED gate8-v2]` across `P-SWE`, `P-CYBER`, and `P-ARCH` (`0` `HARD_BLOCK`, `0` `BLOCKING`, `0` `PREFERENCE`; #254, #255, #256). Synced and closed `ISS-W5-01`, `ISS-W5-02`, `ISS-W5-03`, `REF-005`, and `REF-006`.

## Refactor movements

| Refactor ID | Moved / Updated Item | From | To | Trigger | Issue |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `REF-001` | Chapter 2 active routing, `L1` Appendix/Ch 1 foundation links, and reciprocal router/dataflow negative boundaries | Queued Ch 2 router stub + self-contained Ch 2 references | Live `ppa-program-analysis` ↔ `ppa-dataflow-and-slicing` routing (`80L` router, cross-skill `L1` links, updated `SKILL.md` desc & `evals`) | `T2`, `T5` | `issues/refactors/REF-001.md` |
| `REF-002` | `U6` unification tagging (`U4 -> U6`), premature `U2/U5/U10` reclassification, 18 cross-unit inverse edges, `U-35..U-39` `T7` notation scoping, and `BKL-003/005/006 + BKL-036..050` `L1` reconciliation | Unlinked staged Ch 2 delta edges + pre-extraction `Proposed concept ids` | Symmetric `81`-node `ontology/concept_graph.json`, `U6` section in `L1`, `notation_index.md` `U-35/36/38`, wired `BKL-*` pointers | `T4`, `T6`, `T7` | `issues/refactors/REF-002.md` |
| `REF-003` | Chapter 3 active routing (`81L`), bidirectional Ch 2 ↔ Ch 3 `L1` links, symmetric `U4`/`U5`/`U9` edges (`97` nodes), `U-39..U-45` `T7` audit, `BKL-007/008/011 + BKL-051..062` reconciliation, and Gate #5 Round 1 (`gate5-v2`) fixes | Staged Chapter 3 package + Chapter 2 standalone `L1` links + unverified `BKL-007/008/011` `Proposed concept ids` | Live `ppa-program-analysis` (`81L`) ↔ `ppa-control-flow-and-constraints` (`269L`, `202L`/`147L`/`150L`) ↔ `ppa-dataflow-and-slicing`, `97`-node symmetric `concept_graph.json`, `U-39..U-45` scoping, `C4.7` evals, `56/56` `BKL` parity (`C6.6`/`C6.7`) | `T2`–`T7` | `issues/refactors/REF-003.md` |
| `REF-004` | Chapter 4 active routing (`82L`), reciprocal `U6`/`U7`/`Mini Project 4.2–4.3` `L1` links, symmetric `U6`/`U7` edges (`113` nodes), `U-46..U-53` + `ρ` `T7` audit, `BKL-001/002/013/024/029/033 + BKL-063..072` reconciliation, and Gate #6 Round 1 (`gate6-v2`) fixes | Staged Chapter 4 package + deferred `§4.5` pointer in Ch 2 `L1` + unlinked `BKL-001/002` `Proposed concept ids` | Live `ppa-program-analysis` (`82L`) ↔ `ppa-abstract-interpretation` (`264L`, `260L`/`161L`/`169L`) ↔ Ch 2/Ch 3 `L1`, `113`-node symmetric `concept_graph.json`, `U-46..U-53` scoping, `C4.7` evals, `68/68` `BKL` parity (`C6.6`/`C6.7`) | `T2`–`T7` | `issues/refactors/REF-004.md` |
| `REF-005` | Chapter 5 active routing (`83L`), reciprocal `U8`/`X1`/`§2.5.6` `L1` links, symmetric `U8` edges (`131` nodes), `U-54..U-60` + `π`/`FV` `T7` audit, and `BKL-004/009/011/026/030/031 + BKL-073..082` reconciliation | Staged Chapter 5 package + Ch 3 `SUGGESTED_FIXES.md` `U8` queue + unlinked `BKL-004/009` `Proposed concept ids` | Live `ppa-program-analysis` (`83L`) ↔ `ppa-types-effects-and-regions` (`318L`, `289L`/`283L`/`275L`) ↔ Ch 1/Ch 2/Ch 3 `L1`, `131`-node symmetric `concept_graph.json`, `U-54..U-60` scoping, `C4.7` evals, `80/80` `BKL` parity (`C6.6`/`C6.7`) | `T2`–`T7` | `issues/refactors/REF-005.md` |
| `REF-006` | Part II cross-paradigm synthesis (`cross_paradigm_matrix.md`, `221L`) and Ch 3–5 holistic audit across `U1`–`U10`, `X1`–`X5`, altitude budgets, and `0.2605` active Jaccard bound | Staged Stage-2 cross-paradigm matrix + per-chapter Part II packages | Canonical `ontology/cross_paradigm_matrix.md` + verified Part II holistic concordance across `131` nodes ahead of Gate #8 | `T2`–`T6` | `issues/refactors/REF-006.md` |

