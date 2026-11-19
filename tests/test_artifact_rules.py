#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-001, REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-001, REQ-PRD-PPA-006
# @decision DEC-PPA-007: Hermetic tests for scripts/ppa_artifact_rules.py covering
#   CONFORMANCE_SPEC.md N1-N3, N8 (§3.1 Roman front-matter, spans, statements,
#   end-matter, fail-closed C1.10/C1.11), C1.9, C3.1-C3.6, C3.10, C3.12, C4.1-C4.2.
"""Tests for scripts/ppa_artifact_rules.py and its validator wiring.

Run: python3 -B tests/test_artifact_rules.py
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "tmp"
sys.path.insert(0, str(ROOT / "scripts"))

import ppa_artifact_rules as rules  # noqa: E402
import validate_ppa_knowledge as vpk  # noqa: E402

PM = vpk.PageMap(json.loads((ROOT / "corpus/pdf_page_map.json").read_text(encoding="utf-8")))


def scratch() -> tempfile.TemporaryDirectory:
    TMP.mkdir(exist_ok=True)
    return tempfile.TemporaryDirectory(dir=TMP, prefix="test_rules_")


def skill_text(name: str, desc: str, body_lines: int) -> str:
    return f"---\nname: {name}\ndescription: {desc}\n---\n" + "line\n" * body_lines


GOOD_DESC = ("Use when designing a monotone dataflow analysis. Do not use for type systems; "
             "use ppa-types-effects instead.")


class N8CitationTests(unittest.TestCase):
    """[PPA <locator>, p. <page>] and span resolution against corpus/pdf_page_map.json."""

    def test_valid_locators_and_preface_roman_resolve(self):
        ok = [
            ("Preface", "VI"), ("Preface", "VII"), ("Contents", "XI"),
            ("§2.1", 35), ("2.5.4", 99), ("§A.4 Fixed Points", 402),
            ("Table 2.1", 40), ("Figure C.3", 425), ("Lemma 6.12", 380),
            ("Fact 3.11", 160), ("Example 3.20", 175), ("Exercise 2.25", 139),
            ("Chapter 2 Exercises", 136), ("Chapter 2 Concluding Remarks", 129),
            ("Mini Project 2.2", 133), ("Appendix C Concluding Remarks", 427),
            ("Index of Notation", 430), ("Bibliography", 445),
            ("[12]", 440), ("Bibliography [185]", 452),
        ]
        for loc, page in ok:
            self.assertIsNone(rules.resolve_locator(loc, page, PM), (loc, page))

    def test_invalid_locators_invented_statements_and_tail_bleed_fail(self):
        cases = {
            ("Table 2.1", 60): "is on book p. 40",
            ("Table 4.1", 220): "outside the 51-table",
            ("§2.5", 60): "outside §2.5",
            ("§2.6", 136): "outside §2.6",
            ("Chapter 2 Concluding Remarks", 40): "outside Chapter 2 Concluding Remarks",
            ("Preface", 6): "requires a Roman page label",
            ("Preface", "XX"): "not in Preface",
            ("Lemma A.4", 300): "outside Lemma A.4",
            ("Lemma B.3", 411): "unknown statement",
            ("Theorem B.1", 406): "unknown statement",
            ("Exercise A.1", 404): "unknown statement",
            ("Fact A.4", 402): "unknown statement",
            ("Lemma 2.99", 60): "unknown statement",
            ("[186]", 452): "does not exist",
            ("§2.1", 34): "absent from the PDF",
            ("§9.9", 10): "unrecognised locator",
        }
        for (loc, page), needle in cases.items():
            err = rules.resolve_locator(loc, page, PM)
            self.assertIsNotNone(err, (loc, page))
            self.assertIn(needle, err, (loc, page))

    def test_scanner_handles_spans_and_fails_closed_on_malformed_tokens(self):
        good = "valid [PPA Preface, p. VI] and [PPA §2.1, pp. 35–40] plus `[PPA <locator>, p. N]`."
        self.assertEqual(rules.check_n8_citations(good, "ok.md", PM), [])
        bad = (
            "[PPA Figure 9.9, p. 3]\n"
            "[PPA Table 9.9 p. 300]\n"
            "[PPA§2.1,p.35]\n"
            "[PPA Chapter 2, pp. 35–60]\n"
            "[PPA §2.1, pp. 40–35]\n"
        )
        errs = rules.check_n8_citations(bad, "bad.md", PM)
        self.assertEqual(len(errs), 5, errs)


class SkillRuleTests(unittest.TestCase):
    """N1-N3, C3.1-C3.6, C3.12, and C4.1-C4.2 rules."""

    def build(self, root: Path, skills: dict[str, str]) -> None:
        for name, text in skills.items():
            d = root / "knowledge/skills" / name
            (d / "evals").mkdir(parents=True)
            (d / "SKILL.md").write_text(text, encoding="utf-8")

    def test_conformant_skills_pass(self):
        with scratch() as tmp:
            root = Path(tmp)
            self.build(root, {
                "ppa-program-analysis": skill_text(
                    "ppa-program-analysis",
                    "Use when choosing an analysis. Do not use for solving; use ppa-dataflow.", 55),
                "ppa-dataflow": skill_text("ppa-dataflow", GOOD_DESC, 300),
                "ppa-types-effects": skill_text(
                    "ppa-types-effects",
                    "Use when designing effect systems. Do not use for dataflow; use ppa-dataflow.",
                    260),
            })
            self.assertEqual(rules.check_artifacts(root), [])

    def test_violations_token_boundary_and_closed_tree_reported(self):
        with scratch() as tmp:
            root = Path(tmp)
            self.build(root, {
                "ppa-program-analysis": skill_text(
                    "ppa-program-analysis", "Use when a. Do not use for b; use ppa-alpha.", 10),
                "ppa-alpha": skill_text("ppa-alpha", "Helps with lattices.", 120),
                "ppa-beta": "---\nname: ppa-beta\ndescription: Use when x. Do not use for y; "
                            "see ppa-alphabetic.\n---\n" + "l\n" * 260,
                "ppa-gamma": "---\nname: ppa-gamma\nname: ppa-gamma\n"
                             "description: Use when z. Don't use for q; see ppa-alpha.\n---\n"
                             + "l\n" * 260,
            })
            (root / "knowledge/stray.txt").write_text("stray\n", encoding="utf-8")
            joined = "\n".join(rules.check_artifacts(root))
            self.assertIn("ppa-program-analysis/SKILL.md: 14 lines (must be >= 50", joined)
            self.assertIn("ppa-alpha/SKILL.md: 124 lines (must be >= 250 and < 500", joined)
            self.assertIn("ppa-alpha/SKILL.md: description lacks a 'Use when'", joined)
            self.assertIn("ppa-beta/SKILL.md: negative clause names no non-router sibling", joined)
            self.assertIn("duplicate frontmatter key 'name'", joined)
            self.assertIn("knowledge/stray.txt: unpermitted file in knowledge/ (C3.12)", joined)

    def test_n1_strict_utf8_and_n2_lf_line_counting(self):
        with scratch() as tmp:
            root = Path(tmp)
            # Form feeds and U+2028 must NOT split lines under N2.
            fake_250 = skill_text(
                "ppa-solo", "Use when a. Do not use for b.",
                50).replace("line\n", "a\x0cb\u2028c\n")
            self.build(root, {"ppa-solo": fake_250})
            amb = root / "knowledge/ambient-context"
            amb.mkdir(parents=True)
            (amb / "ppa-bad.md").write_bytes(b"\xff\xfeinvalid")
            joined = "\n".join(rules.check_artifacts(root))
            self.assertIn("ppa-solo/SKILL.md: 54 lines (must be >= 250", joined)
            self.assertIn("ppa-bad.md: invalid UTF-8", joined)

    def test_folded_description_and_ambient_budget(self):
        with scratch() as tmp:
            root = Path(tmp)
            folded = ("---\nname: ppa-solo\ndescription: >\n  Use when solving fixed points.\n"
                      "  Do not use for typing.\n---\n" + "l\n" * 260)
            self.build(root, {"ppa-solo": folded})
            amb = root / "knowledge/ambient-context"
            amb.mkdir(parents=True)
            (amb / "ppa-short.md").write_text("x\n" * 79, encoding="utf-8")
            (amb / "ppa-ok.md").write_text("x\n" * 80, encoding="utf-8")
            errs = rules.check_artifacts(root)
            self.assertEqual(len(errs), 1, errs)
            self.assertIn("ppa-short.md: 79 lines (must be 80-250", errs[0])

    def test_forbidden_frontmatter_catches_bom_and_trailing_spaces(self):
        with scratch() as tmp:
            root = Path(tmp)
            payloads = {
                "corpus/shards/RAW_SHARD_00_x.md": "---   \nk: v\n---\nbody\n",
                "ontology/notation_index.md": "\ufeff---\nk: v\n---\nbody\n",
                "knowledge/skills/ppa-a/references/r.md": "---\nk: v\n---\nbody\n",
                "docs/README.md": "---\t\nk: v\n---\nbody\n",
            }
            for rel, content in payloads.items():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text(content, encoding="utf-8")
            errs = rules.check_forbidden_frontmatter(root)
            self.assertEqual(len(errs), 4, errs)


class EvalsAndLedgerTests(unittest.TestCase):
    """C3.10 evals/cases.yaml shape (incl. router) and C1.9 gotcha-ledger rules."""

    def test_cases_yaml_parsing_and_router_inclusion(self):
        with scratch() as tmp:
            root = Path(tmp)
            rdir = root / "knowledge/skills/ppa-program-analysis"
            (rdir / "evals").mkdir(parents=True)
            (rdir / "SKILL.md").write_text(
                skill_text("ppa-program-analysis", "Use when a. Do not use for b.", 60),
                encoding="utf-8")
            # Router without evals/cases.yaml must fail C3.10.
            self.assertIn("ppa-program-analysis/evals/cases.yaml: missing (C3.10)",
                          "\n".join(rules.check_evals(root)))
            (rdir / "evals/cases.yaml").write_text(
                "cases:\n"
                "  - id: r1\n    prompt: \"Compare approaches\"\n    expect_skill: ppa-program-analysis\n"
                "  - id: r2\n    prompt: missing expectation\n    model: some-model\n",
                encoding="utf-8")
            errs = rules.check_evals(root)
            self.assertEqual(len(errs), 2, errs)
            self.assertIn("case 1 missing ['expect_skill']", errs[0])
            self.assertIn("case 1 has unknown keys ['model']", errs[1])

    def test_gotcha_ledger_shape_and_coverage(self):
        with scratch() as tmp:
            root = Path(tmp)
            shards = root / "corpus/shards"
            shards.mkdir(parents=True)
            (shards / "RAW_SHARD_00_a.md").write_text(
                "# Shard\n## A.4 Fixed Points\ntext\n## Gotcha Ledger\n"
                "- G-U0-01: Tarski needs a complete lattice [PPA §A.4, p. 402]\n"
                "- G-U0-02: Preface scope exclusion [PPA Preface, p. VI]\n",
                encoding="utf-8")
            errs, n, ids = rules.collect_gotcha_ledgers(root)
            self.assertEqual((errs, n, len(ids)), ([], 1, 2))
            (root / "ontology").mkdir()
            (root / "ontology/note.md").write_text("Covers G-U0-01.\n", encoding="utf-8")
            cov = rules.check_gotcha_coverage(root, ids)
            self.assertEqual(len(cov), 1)
            self.assertIn("G-U0-02", cov[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
