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

## Refactor movements

| Refactor ID | Moved / Updated Item | From | To | Trigger | Issue |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `REF-001` | Chapter 2 active routing, `L1` Appendix/Ch 1 foundation links, and reciprocal router/dataflow negative boundaries | Queued Ch 2 router stub + self-contained Ch 2 references | Live `ppa-program-analysis` ↔ `ppa-dataflow-and-slicing` routing (`80L` router, cross-skill `L1` links, updated `SKILL.md` desc & `evals`) | `T2`, `T5` | `issues/refactors/REF-001.md` |
| `REF-002` | `U6` unification tagging (`U4 -> U6`), premature `U2/U5/U10` reclassification, 18 cross-unit inverse edges, `U-35..U-39` `T7` notation scoping, and `BKL-003/005/006 + BKL-036..050` `L1` reconciliation | Unlinked staged Ch 2 delta edges + pre-extraction `Proposed concept ids` | Symmetric `81`-node `ontology/concept_graph.json`, `U6` section in `L1`, `notation_index.md` `U-35..U-39`, wired `BKL-*` pointers | `T4`, `T6`, `T7` | `issues/refactors/REF-002.md` |

