#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001
# @decision DEC-PPA-006: Hermetic stdlib unittest suite for Wave 0 using real
#   scratch fixtures under tmp/ (zero mocks, zero personal/organisation strings);
#   synthetic operator tokens are written to temporary denylist JSON files at
#   runtime so tracked test source stays 100% vendor-neutral.
"""Wave 0 foundation tests: hygiene gate, issue controller, PDF coordinate map,
per-unit slices, concept-graph schema and Tier-A knowledge validator.

Run: python3 -B tests/test_wave0_foundation.py
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
TMP = ROOT / "tmp"
sys.path.insert(0, str(SCRIPTS))

import check_portability_hygiene as hygiene  # noqa: E402
import extract_ppa_structure as extractor  # noqa: E402
import issue_ctl  # noqa: E402
import validate_ppa_knowledge as vpk  # noqa: E402

EXPECTED_SHARDS = [
    "ISS-W0-01", "ISS-W0-02", "ISS-W0-03", "ISS-W1-01", "ISS-W1-02", "ISS-W2-01", "ISS-W2-02",
    "ISS-W2-03", "ISS-W2-04", "ISS-W3-01", "ISS-W3-02", "ISS-W4-01", "ISS-W4-02", "ISS-W5-01",
    "ISS-W5-02", "ISS-W5-03", "ISS-W6-01", "ISS-W6-02", "ISS-W7-01", "ISS-W8-01", "ISS-W8-02",
]

LIST_OF_TABLES = {
    "1.1": 4, "1.2": 19, "1.3": 21, "1.4": 24, "1.5": 26, "1.6": 27, "2.1": 40, "2.2": 44,
    "2.3": 47, "2.4": 50, "2.5": 55, "2.6": 56, "2.7": 73, "2.8": 75, "2.9": 76, "2.10": 133,
    "3.1": 146, "3.2": 155, "3.3": 156, "3.4": 158, "3.5": 170, "3.6": 174, "3.7": 178,
    "3.8": 184, "3.9": 188, "3.10": 192, "5.1": 285, "5.2": 288, "5.3": 290, "5.4": 292,
    "5.5": 303, "5.6": 305, "5.7": 307, "5.8": 310, "5.9": 322, "5.10": 328, "5.11": 334,
    "5.12": 337, "5.13": 338, "5.14": 341, "5.15": 343, "5.16": 346, "5.17": 347, "5.18": 348,
    "6.1": 369, "6.2": 373, "6.3": 376, "6.4": 379, "6.5": 382, "6.6": 384, "C.1": 421,
}
LIST_OF_FIGURES = {
    "1.1": 2, "1.2": 6, "1.3": 15, "2.1": 38, "2.2": 41, "2.3": 48, "2.4": 61, "2.5": 62,
    "2.6": 70, "2.7": 85, "2.8": 93, "2.9": 94, "2.10": 95, "2.11": 103, "2.12": 106, "2.13": 112,
    "2.14": 113, "2.15": 115, "2.16": 116, "2.17": 118, "2.18": 120, "2.19": 123, "2.20": 124,
    "2.21": 126, "2.22": 127, "2.23": 132, "3.1": 148, "3.2": 149, "3.3": 159, "3.4": 179,
    "3.5": 180, "3.6": 185, "4.1": 218, "4.2": 221, "4.3": 224, "4.4": 226, "4.5": 231,
    "4.6": 235, "4.7": 238, "4.8": 243, "4.9": 245, "4.10": 276, "5.1": 331, "5.2": 340,
    "6.1": 374, "6.2": 376, "6.3": 377, "6.4": 379, "6.5": 382, "6.6": 384, "A.1": 394,
    "A.2": 400, "A.3": 403, "C.1": 422, "C.2": 423, "C.3": 425,
}
TOC_SECTION_STARTS = {
    "1.1": 1, "1.3": 5, "2.1": 35, "2.2": 54, "2.3": 65, "2.4": 74, "2.5": 82, "2.6": 104,
    "3.1": 141, "3.2": 153, "3.5": 182, "4.4": 246, "5.4": 319, "6.1": 365, "A.1": 393, "C.1": 417,
}
CONCLUDING_REMARKS_STARTS = {
    "chapter_1": 29, "chapter_2": 128, "chapter_3": 198, "chapter_4": 270, "chapter_5": 349,
    "chapter_6": 384, "appendix_A": 404, "appendix_B": 415, "appendix_C": 427,
}


def run_cli(script: str, *args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-B", str(SCRIPTS / script), *args],
                          cwd=cwd, capture_output=True, text=True, check=False)


def scratch() -> tempfile.TemporaryDirectory:
    TMP.mkdir(exist_ok=True)
    return tempfile.TemporaryDirectory(dir=TMP, prefix="test_w0_")


def load_map() -> dict:
    return json.loads((ROOT / "corpus" / "pdf_page_map.json").read_text(encoding="utf-8"))


class HygieneTests(unittest.TestCase):
    """Fail-closed vendor-neutral portability hygiene scanner."""

    def test_repository_is_clean(self):
        proc = run_cli("check_portability_hygiene.py", ".")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("hygiene PASS: 0 finding(s)", proc.stdout)

    def test_scanner_source_passes_its_own_scan(self):
        text = (SCRIPTS / "check_portability_hygiene.py").read_text(encoding="utf-8")
        self.assertEqual(hygiene.scan_text(text, "scripts/check_portability_hygiene.py",
                                           hygiene.STRUCTURAL), [])

    def test_structural_core_harness_and_denylist_rules_detected(self):
        with scratch() as tmp:
            root = Path(tmp)
            deny = root / "tmp" / "deny.json"
            deny.parent.mkdir(parents=True)
            deny.write_text(json.dumps({"tokens": ["synth_tool"], "regexes": [r"\bticket/[0-9]+\b"]}),
                            encoding="utf-8")
            (root / "abs.md").write_text("/us" + "r/local/share/demo\n", encoding="utf-8")
            (root / "mail.md").write_text("contact author" + "@private-box.invalid\n", encoding="utf-8")
            (root / "url.md").write_text("see https:" + "//private.invalid/spec\n", encoding="utf-8")
            (root / "op.md").write_text("run synth_tool2 and synth_tool_bin for ticket/42\n",
                                        encoding="utf-8")
            (root / "ontology").mkdir()
            (root / "ontology/log.md").write_text("calibrated by clau" + "de on t" + "mp/x\n",
                                                  encoding="utf-8")
            (root / "knowledge").mkdir()
            (root / "knowledge/k.md").write_text("load .cur" + "sor config\n", encoding="utf-8")
            proc = run_cli("check_portability_hygiene.py", str(root),
                           "--denylist", str(deny), "--json")
            self.assertEqual(proc.returncode, 1)
            cats = {f["category"] for f in json.loads(proc.stdout)["findings"]}
            for exp in ("absolute_path", "email", "url", "operator_token",
                        "operator_pattern", "model_or_agent_name", "tmp_reference",
                        "harness_name"):
                self.assertIn(exp, cats, cats)

    def test_fail_closed_on_unscannable_symlinks_paths_and_tracked_ignored(self):
        with scratch() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
            (root / "ignored.txt").write_text("/ho" + "me/alice/leak\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "-f", "ignored.txt"], check=True)
            (root / "nul.md").write_bytes(b"clean\x00hidden")
            (root / "badutf8.md").write_bytes(b"\xff\xfe\x61\x62")
            (root / "huge.txt").write_bytes(b"a" * (hygiene.MAX_BYTES + 10))
            os.symlink("/us" + "r/local/bin/sh", root / "ext_link")
            (root / "knowledge").mkdir()
            (root / "knowledge" / ("clau" + "de_note.md")).write_text("ok\n", encoding="utf-8")
            proc = run_cli("check_portability_hygiene.py", str(root),
                           "--no-local-denylist", "--json")
            self.assertEqual(proc.returncode, 1)
            cats = {f["category"] for f in json.loads(proc.stdout)["findings"]}
            for exp in ("absolute_path", "unscannable_binary", "unscannable_encoding",
                        "unscannable_oversized", "symlink_absolute_path", "symlink_escape",
                        "path_model_or_agent_name"):
                self.assertIn(exp, cats, cats)

    def test_ignored_locations_and_allowlisted_binaries_are_skipped(self):
        with scratch() as tmp:
            root = Path(tmp)
            leak = "/us" + "r/local/share/x"
            for sub in ("tmp", ".git", "__pycache__"):
                (root / sub).mkdir()
                (root / sub / "x.md").write_text(leak, encoding="utf-8")
            (root / "book.pdf").write_bytes(b"%PDF-1.4\x00binary")
            (root / "page.png").write_bytes(b"\x89PNG\x00binary")
            (root / "clean.md").write_text("Principles of Program Analysis\n", encoding="utf-8")
            proc = run_cli("check_portability_hygiene.py", str(root), "--no-local-denylist")
            self.assertEqual(proc.returncode, 0, proc.stdout)
            self.assertIn("in 1 scanned file(s)", proc.stdout)

    def test_benign_lookalikes_and_allowlisted_urls_do_not_trigger(self):
        benign = ("~/projects/ppa; https://json-schema.org/draft/2020-12/schema; "
                  "user@example.com; relative/path/to/file.md")
        self.assertEqual(hygiene.scan_text(benign, "benign.md", hygiene.STRUCTURAL), [])

    def test_missing_root_is_usage_error(self):
        self.assertEqual(run_cli("check_portability_hygiene.py", "no/such/dir").returncode, 2)


def copy_tracker(dst: Path) -> None:
    shutil.copytree(ROOT / "issues", dst / "issues",
                    ignore=shutil.ignore_patterns("export_manifest.json"))


class IssueCtlTests(unittest.TestCase):
    """issues/ schema, controller transitions, graph rules and export."""

    def test_repository_tracker_is_valid_complete_and_r0_consistent(self):
        proc = run_cli("issue_ctl.py", "validate")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        issues, errors = issue_ctl.collect(ROOT)
        self.assertEqual(errors, [])
        shards = sorted(i for i, x in issues.items() if x.meta["issue_type"] == "shard")
        self.assertEqual(shards, sorted(EXPECTED_SHARDS))
        self.assertIn("EPIC-001", issues)
        for iid, issue in issues.items():
            raw = issue.path.read_text(encoding="utf-8")
            self.assertNotIn("always-loaded", raw, f"{iid} contradicts R0 zero-byte rule")

    def test_schema_doc_lists_every_key_and_section(self):
        doc = (ROOT / "issues" / "SCHEMA.md").read_text(encoding="utf-8")
        for key in issue_ctl.REQUIRED_KEYS:
            self.assertIn(f"`{key}`", doc)
        for name in issue_ctl.SECTIONS:
            self.assertIn(f"## {name}", doc)

    def test_set_status_legal_and_illegal_transitions(self):
        with scratch() as tmp:
            root = Path(tmp)
            copy_tracker(root)
            ok = run_cli("issue_ctl.py", "--root", str(root), "set-status", "ISS-W3-01",
                         "in_progress", "--date", "2026-11-19")
            self.assertEqual(ok.returncode, 0, ok.stderr)
            text = (root / "issues/shards/ISS-W3-01.md").read_text(encoding="utf-8")
            self.assertIn("status: in_progress", text)
            self.assertIn("updated_at: 2026-11-19", text)
            self.assertTrue((root / "tmp" / "issues.lock").exists())
            bad = run_cli("issue_ctl.py", "--root", str(root), "set-status",
                          "ISS-W3-02", "closed")
            self.assertEqual(bad.returncode, 1)
            self.assertIn("illegal transition", bad.stderr)

    def test_aligned_and_closed_semantic_gates(self):
        with scratch() as tmp:
            root = Path(tmp)
            copy_tracker(root)
            self.assertEqual(run_cli("issue_ctl.py", "--root", str(root), "set-status",
                                     "ISS-W3-01", "in_progress").returncode, 0)
            path = root / "issues/shards/ISS-W3-01.md"
            r = run_cli("issue_ctl.py", "--root", str(root), "set-status", "ISS-W3-01", "aligned")
            self.assertEqual(r.returncode, 1)
            # Duplicate judge IDs must fail.
            dup = path.read_text(encoding="utf-8").replace(
                "aligned_models: []", "aligned_models: [judge-a, judge-a, judge-a]")
            path.write_text(dup, encoding="utf-8")
            self.assertEqual(run_cli("issue_ctl.py", "--root", str(root), "set-status",
                                     "ISS-W3-01", "aligned").returncode, 1)
            valid = dup.replace(
                "aligned_models: [judge-a, judge-a, judge-a]",
                "aligned_models: [judge-a, judge-b, judge-c]",
            ).replace(
                "## 3-Model Adversarial Alignment & Rebuttal Log\n\n_Pending._",
                "## 3-Model Adversarial Alignment & Rebuttal Log\n\n- Round 1 [ALIGNED v1]",
            ).replace("- [ ] ", "- [x] ")
            path.write_text(valid, encoding="utf-8")
            self.assertEqual(run_cli("issue_ctl.py", "--root", str(root), "set-status",
                                     "ISS-W3-01", "aligned").returncode, 0)
            self.assertEqual(run_cli("issue_ctl.py", "--root", str(root), "set-status",
                                     "ISS-W3-01", "closed").returncode, 1)
            r = run_cli("issue_ctl.py", "--root", str(root), "set-status", "ISS-W3-01",
                        "closed", "--receipt", "tests green", "--date", "2026-11-20")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(run_cli("issue_ctl.py", "--root", str(root),
                                     "validate").returncode, 0)

    def mutate_and_collect(self, rel: str, old: str, new: str) -> list[str]:
        with scratch() as tmp:
            root = Path(tmp)
            copy_tracker(root)
            path = root / rel
            text = path.read_text(encoding="utf-8")
            self.assertIn(old, text)
            path.write_text(text.replace(old, new, 1), encoding="utf-8")
            return issue_ctl.collect(root)[1]

    def test_preamble_comments_tilde_fences_and_unknown_dirs_enforced(self):
        errs = self.mutate_and_collect("issues/backlog/BKL-001.md",
                                       "\n## Summary", "\nPreamble line.\n\n## Summary")
        self.assertTrue(any("preamble" in e for e in errs), errs)
        errs = self.mutate_and_collect("issues/backlog/BKL-001.md",
                                       "status: open", "# comment\nstatus: open")
        self.assertTrue(any("comments are not permitted" in e for e in errs), errs)
        # Level-2 heading inside a ~~~ fence is ignored rather than splitting sections.
        errs = self.mutate_and_collect(
            "issues/backlog/BKL-001.md",
            "## Summary\n\n",
            "## Summary\n\n~~~\n## Not A Section\n~~~\n\n",
        )
        self.assertEqual(errs, [])
        with scratch() as tmp:
            root = Path(tmp)
            copy_tracker(root)
            (root / "issues/stray_dir").mkdir()
            errs = issue_ctl.collect(root)[1]
            self.assertTrue(any("unexpected entry" in e for e in errs), errs)

    def test_graph_rules_are_enforced(self):
        errs = self.mutate_and_collect("issues/shards/ISS-W2-03.md",
                                       "blocks: [ISS-W2-04]", "blocks: []")
        self.assertTrue(any("ISS-W2-03.blocks lacks ISS-W2-04" in e for e in errs), errs)
        errs = self.mutate_and_collect("issues/shards/ISS-W0-01.md",
                                       "depends_on: []", "depends_on: [ISS-W9-99]")
        self.assertTrue(any("unknown reference" in e for e in errs), errs)
        with scratch() as tmp:
            root = Path(tmp)
            copy_tracker(root)
            p1 = root / "issues/shards/ISS-W0-01.md"
            pb = root / "issues/backlog/BKL-001.md"
            p1.write_text(p1.read_text(encoding="utf-8").replace(
                "depends_on: []", "depends_on: [BKL-001]"), encoding="utf-8")
            pb.write_text(pb.read_text(encoding="utf-8").replace(
                "blocks: []", "blocks: [ISS-W0-01]"), encoding="utf-8")
            errs = issue_ctl.collect(root)[1]
            self.assertTrue(any("C6.8" in e for e in errs), errs)

    def test_schema_rules_are_enforced(self):
        errs = self.mutate_and_collect("issues/shards/ISS-W1-01.md",
                                       "priority: P0", "priority: P0\nowner: someone")
        self.assertTrue(any("unknown keys" in e for e in errs), errs)
        errs = self.mutate_and_collect("issues/shards/ISS-W1-01.md",
                                       "## Acceptance Gates", "## Gates")
        self.assertTrue(any("sections must be exactly" in e for e in errs), errs)
        errs = self.mutate_and_collect("issues/shards/ISS-W1-01.md",
                                       "issue_type: shard", "issue_type: refactor")
        self.assertTrue(any("not allowed in shards/" in e for e in errs), errs)
        errs = self.mutate_and_collect("issues/shards/ISS-W1-01.md",
                                       "altitudes: [L1, L2, L3]", "altitudes: [L1, L9]")
        self.assertTrue(any("altitudes must be a subset" in e for e in errs), errs)
        errs = self.mutate_and_collect("issues/shards/ISS-W1-01.md",
                                       "updated_at: 2026-11-18", "updated_at: 2026-11-01")
        self.assertTrue(any("earlier than created_at" in e for e in errs), errs)

    def test_export_dry_run_is_topological_deterministic_and_supports_out(self):
        with scratch() as tmp:
            root = Path(tmp)
            copy_tracker(root)
            custom_out = root / "tmp" / "manifest_custom.json"
            self.assertEqual(run_cli("issue_ctl.py", "--root", str(root),
                                     "export-github").returncode, 2)
            r1 = run_cli("issue_ctl.py", "--root", str(root), "export-github",
                         "--dry-run", "--out", str(custom_out))
            self.assertEqual(r1.returncode, 0, r1.stdout + r1.stderr)
            self.assertFalse((root / "issues" / "export_manifest.json").exists())
            first = custom_out.read_bytes()
            run_cli("issue_ctl.py", "--root", str(root), "export-github",
                    "--dry-run", "--out", str(custom_out))
            self.assertEqual(first, custom_out.read_bytes())
            manifest = json.loads(first)
            issues, _ = issue_ctl.collect(root)
            self.assertEqual(manifest["count"], len(issues))
            pos = {iid: i for i, iid in enumerate(manifest["order"])}
            for entry in manifest["issues"]:
                prereqs = list(entry["depends_on"])
                if entry["parent_issue"]:
                    prereqs.append(entry["parent_issue"])
                for pre in prereqs:
                    self.assertLess(pos[pre], pos[entry["id"]])
            self.assertEqual(manifest["order"][0], "EPIC-001")

    def test_manifest_is_lossless_per_c6_5(self):
        with scratch() as tmp:
            root = Path(tmp)
            copy_tracker(root)
            out = root / "tmp" / "m.json"
            self.assertEqual(run_cli("issue_ctl.py", "--root", str(root), "export-github",
                                     "--dry-run", "--out", str(out)).returncode, 0)
            manifest = json.loads(out.read_text(encoding="utf-8"))
            for entry in manifest["issues"]:
                src = root / entry["source_path"]
                loaded = issue_ctl.load_issue(src)
                self.assertEqual(entry["frontmatter"], loaded.meta)
                self.assertEqual(hashlib.sha256(entry["source_body"].encode()).hexdigest(),
                                 entry["body_sha256"])
                self.assertEqual(hashlib.sha256(entry["body"].encode()).hexdigest(),
                                 entry["published_body_sha256"])
                self.assertEqual(issue_ctl.render_body(loaded), entry["body"])

    def test_backlog_seed_is_complete_and_non_blocking(self):
        issues, errors = issue_ctl.collect(ROOT)
        self.assertEqual(errors, [])
        backlog = sorted(i for i in issues if i.startswith("BKL-"))
        self.assertGreaterEqual(len(backlog), 12)
        self.assertEqual(backlog[:12], [f"BKL-{n:03d}" for n in range(1, 13)])
        self.assertEqual(backlog, [f"BKL-{n:03d}" for n in range(1, len(backlog) + 1)])
        for iid, issue in issues.items():
            if not iid.startswith("BKL-"):
                self.assertFalse(any(d.startswith("BKL-") for d in issue.meta["depends_on"]))
        for iid in backlog:
            self.assertIn(issues[iid].meta["issue_type"], {"contradiction", "edge_case"})
            self.assertRegex(issues[iid].sections["Source Citations & Grounding"],
                             r"\[PPA [^\]]+, p\. (?:\d+|[IVXLCDM]+)\]")


class PageMapTests(unittest.TestCase):
    """corpus/pdf_page_map.json against independent front-matter and tail oracles."""

    @classmethod
    def setUpClass(cls):
        cls.doc = load_map()
        cls.pdf_of = {p["book_page"]: p["pdf_page"] for p in cls.doc["pages"]
                      if p["book_page"] is not None}

    def test_totals_anchors_and_page_basis(self):
        d = self.doc
        self.assertEqual(d["source"]["total_pdf_pages"], 465)
        self.assertEqual(len(d["pages"]), 465)
        self.assertEqual(self.pdf_of[1], 21)
        self.assertEqual(self.pdf_of[35], 54)
        self.assertEqual(self.pdf_of[439], 452)
        self.assertEqual(self.pdf_of[452], 465)
        self.assertEqual(d["counts"], {
            "tables": 51, "figures": 56, "bibliography_entries": 185,
            "sections": 43, "statements": 342, "statement_gaps": 0,
        })
        self.assertEqual(d["statement_gaps"], [])
        self.assertEqual(d["extraction_stats"]["detected_conflicts"], [])
        self.assertTrue(all(p.get("basis") in {"front_matter", "header", "inferred"}
                            for p in d["pages"]))

    def test_mapping_is_strictly_monotone_and_gaps_are_blank_versos(self):
        rows = [p for p in self.doc["pages"] if p["book_page"] is not None]
        self.assertEqual([p["pdf_page"] for p in rows], list(range(21, 466)))
        books = [p["book_page"] for p in rows]
        self.assertTrue(all(b2 > b1 for b1, b2 in zip(books, books[1:])))
        absent = self.doc["book_pages_absent_from_pdf"]
        self.assertEqual(len(absent) + len(books), 452)
        starts = {r["book_start"] for r in self.doc["regions"].values()}
        for b in absent:
            self.assertIn(b + 1, starts, f"absent book page {b} is not before an opener")

    def test_offset_runs_reproduce_pages(self):
        for run in self.doc["offset_runs"]:
            for pdf in range(run["pdf_start"], run["pdf_end"] + 1):
                self.assertEqual(self.doc["pages"][pdf - 1]["book_page"], pdf - run["offset"])
        self.assertEqual(self.doc["offset_runs"][0]["offset"], 20)
        self.assertEqual(self.doc["offset_runs"][-1]["offset"], 13)

    def test_region_ranges(self):
        r = self.doc["regions"]
        expect = {"chapter_1": (1, 34), "chapter_2": (35, 140), "chapter_3": (141, 210),
                  "chapter_4": (211, 282), "chapter_5": (283, 364),
                  "chapter_6": (365, 392), "appendix_A": (393, 404),
                  "appendix_B": (405, 416), "appendix_C": (417, 428),
                  "index_of_notation": (429, 432), "subject_index": (433, 438),
                  "bibliography": (439, 452)}
        for key, (lo, hi) in expect.items():
            self.assertEqual((r[key]["book_start"], r[key]["book_end"]), (lo, hi), key)
            self.assertEqual(r[key]["pdf_start"], self.pdf_of[lo], key)

    def test_tables_and_figures_match_front_matter_lists(self):
        for kind, inventory in (("tables", LIST_OF_TABLES), ("figures", LIST_OF_FIGURES)):
            prefix = kind[:-1].capitalize()
            got = {k.split(" ", 1)[1]: v for k, v in self.doc[kind].items()}
            self.assertEqual(set(got), set(inventory), kind)
            for num, page in inventory.items():
                self.assertEqual(got[num]["book_page"], page, f"{prefix} {num}")
                self.assertEqual(got[num]["pdf_page"], self.pdf_of[page], f"{prefix} {num}")

    def test_sections_end_matter_and_statements_match_oracles(self):
        secs = self.doc["sections"]
        self.assertEqual(set(secs), set(extractor.SECTION_TITLES))
        for sid, page in TOC_SECTION_STARTS.items():
            self.assertEqual(secs[sid]["book_start"], page, sid)
        em = self.doc["end_matter"]
        last_sec_of = {"chapter_1": "1.8", "chapter_2": "2.6", "chapter_3": "3.6",
                       "chapter_4": "4.5", "chapter_5": "5.5", "chapter_6": "6.3",
                       "appendix_A": "A.4", "appendix_B": "B.3", "appendix_C": "C.3"}
        for rkey, cr_page in CONCLUDING_REMARKS_STARTS.items():
            self.assertEqual(em[rkey]["concluding_remarks"]["book_start"], cr_page, rkey)
            self.assertLessEqual(secs[last_sec_of[rkey]]["book_end"], cr_page, rkey)
        stmts = self.doc["statements"]
        self.assertEqual(stmts["Lemma 2.32"]["book_page"], 80)
        self.assertEqual(stmts["Fact 3.11"]["book_page"], 160)
        self.assertEqual(stmts["Example 3.20"]["book_page"], 175)
        self.assertEqual(stmts["Exercise 2.25"]["book_page"], 139)
        self.assertEqual(stmts["Lemma 6.12"]["book_page"], 380)

    def test_bibliography_entries_are_ordered(self):
        bib = self.doc["bibliography_entries"]
        self.assertEqual(sorted(map(int, bib)), list(range(1, 186)))
        pages = [bib[str(n)]["book_page"] for n in range(1, 186)]
        self.assertEqual(pages, sorted(pages))
        self.assertEqual(pages[0], 439)
        self.assertEqual(pages[-1], 452)

    def test_extractor_is_deterministic(self):
        text = TMP / "full_book.txt"
        if not text.exists():
            extractor.run_pdftotext(ROOT / "ppa.pdf", text, reuse=False)
        with scratch() as tmp:
            out_map, out_slices = Path(tmp) / "map.json", Path(tmp) / "slices"
            proc = run_cli("extract_ppa_structure.py", "--text", str(text), "--reuse-text",
                           "--map", str(out_map), "--slices", str(out_slices))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            regenerated = json.loads(out_map.read_text(encoding="utf-8"))
            self.assertEqual(regenerated, self.doc)

    def test_split_pages_rejects_wrong_page_count(self):
        with self.assertRaises(ValueError):
            extractor.split_pages("a\x0cb\x0c")


class SliceTests(unittest.TestCase):
    """Per-unit slices with [PDF_PAGE=X | BOOK_PAGE=Y] headers."""

    HEADER = re.compile(r"^\[PDF_PAGE=(\d+) \| BOOK_PAGE=(\d+)\]$", re.M)

    @classmethod
    def setUpClass(cls):
        cls.dir = TMP / "slices"
        if not (cls.dir / "U1_ch1.txt").exists():
            run_cli("extract_ppa_structure.py")
        cls.pdf_of = {p["book_page"]: p["pdf_page"] for p in load_map()["pages"]
                      if p["book_page"] is not None}

    def test_every_unit_slice_has_exact_headers(self):
        for fname, ranges in extractor.UNIT_SLICES:
            text = (self.dir / fname).read_text(encoding="utf-8")
            heads = [(int(a), int(b)) for a, b in self.HEADER.findall(text)]
            expected = [(self.pdf_of[b], b) for lo, hi in ranges
                        for b in range(lo, hi + 1) if b in self.pdf_of]
            self.assertEqual(heads, expected, fname)

    def test_slice_content_is_the_right_book_material(self):
        u1 = (self.dir / "U1_ch1.txt").read_text(encoding="utf-8")
        self.assertTrue(u1.startswith("[PDF_PAGE=21 | BOOK_PAGE=1]\nChapter 1"))
        u2b = (self.dir / "U2b_ch2_s5_6.txt").read_text(encoding="utf-8")
        self.assertIn("Interprocedural Analysis", u2b[:3000])
        u6 = (self.dir / "U6_ch6_index_bib.txt").read_text(encoding="utf-8")
        self.assertIn("[PDF_PAGE=465 | BOOK_PAGE=452]", u6)
        self.assertNotIn("BOOK_PAGE=400]", u6)


def concept(cid: str, cite: dict, edges: list[dict]) -> dict:
    return {
        "id": cid, "title": cid.replace(".", " "), "altitude": "L3", "unit": "U0",
        "citations": [cite], "formal_summary": "A formal statement for testing.",
        "projections": {"cyber": "c", "swe_architecture": "s",
                        "practical_debugging": "d", "cs_theory": "t"},
        "related_edges": edges, "artifact_refs": ["ontology/concept_graph.json"],
    }


def sample_graph() -> dict:
    basis = {
        "unification_id": "U9",
        "citations": [{"chapter_or_app": "Preface", "section": "Preface",
                       "book_page": None, "book_page_roman": "VII",
                       "pdf_page": 7, "table_or_fig": None}],
        "conditions": ["Complete lattice"],
        "differs": ["Appendix B formulates proof principles over relations"],
    }
    lattice = concept("ppa.lattice.complete",
                      {"chapter_or_app": "A", "section": "A.1", "book_page": 393,
                       "pdf_page": 409, "table_or_fig": None},
                      [{"target_id": "ppa.fixpoint.tarski", "relation": "corresponds_to",
                        "basis": basis}])
    tarski = concept("ppa.fixpoint.tarski",
                     {"chapter_or_app": "A", "section": "A.4", "book_page": 402,
                      "pdf_page": 418, "table_or_fig": "Figure A.3"},
                     [{"target_id": "ppa.lattice.complete", "relation": "corresponds_to",
                       "basis": basis}])
    return {"schema_version": 1, "concepts": [lattice, tarski]}


class ValidatorTests(unittest.TestCase):
    """scripts/validate_ppa_knowledge.py on the repo and on hermetic fixtures."""

    def make_root(self, tmp: str, graph: dict | None) -> Path:
        root = Path(tmp)
        for rel in ("corpus/pdf_page_map.json", "ontology/concept_graph.schema.json"):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, root / rel)
        copy_tracker(root)
        if graph is not None:
            (root / "ontology/concept_graph.json").write_text(json.dumps(graph),
                                                              encoding="utf-8")
        return root

    def check(self, graph: dict | None, extra=None) -> vpk.Report:
        with scratch() as tmp:
            root = self.make_root(tmp, graph)
            if extra:
                extra(root)
            return vpk.validate(root)

    @staticmethod
    def failures(report: vpk.Report) -> dict[str, list[str]]:
        return {n: d for n, s, d in report.results if s == "FAIL"}

    def test_repository_passes(self):
        proc = run_cli("validate_ppa_knowledge.py")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        for check_name in ("schema", "artifact_refs", "links", "issues", "inline_citations"):
            self.assertIn(f"[PASS] {check_name}", proc.stdout)
        self.assertIn("[NOT_IMPLEMENTED] deferred_conformance_gates", proc.stdout)

    def test_schema_inverses_and_corresponds_to_basis(self):
        schema = json.loads((ROOT / "ontology/concept_graph.schema.json").read_text())
        self.assertEqual(vpk.check_schema_file(schema), [])
        g = sample_graph()
        self.assertFalse(self.check(g).failed)
        del g["concepts"][0]["related_edges"][0]["basis"]
        fails = self.failures(self.check(g))
        self.assertTrue(any("corresponds_to requires basis" in e for e in fails["graph"]), fails)

    def test_asymmetric_and_dangling_edges_fail(self):
        g = sample_graph()
        g["concepts"][1]["related_edges"] = [{"target_id": "ppa.missing", "relation": "refines"}]
        fails = self.failures(self.check(g))
        self.assertTrue(any("lacks inverse" in e for e in fails["graph"]), fails)
        self.assertTrue(any("does not exist" in e for e in fails["graph"]), fails)

    def test_bad_citations_fail(self):
        g = sample_graph()
        g["concepts"][0]["citations"][0]["pdf_page"] = 410
        g["concepts"][1]["citations"][0]["table_or_fig"] = "Table 2.1"
        g["concepts"][1]["citations"].append({"chapter_or_app": "2", "section": "2.6",
                                              "book_page": 136, "pdf_page": 155,
                                              "table_or_fig": None})
        errs = self.failures(self.check(g))["concept_citations"]
        self.assertTrue(any("is PDF p. 409, not 410" in e for e in errs), errs)
        self.assertTrue(any("Table 2.1 is on book p. 40" in e for e in errs), errs)
        self.assertTrue(any("outside §2.6" in e for e in errs), errs)

    def test_artifact_refs_fragments_and_link_direction_enforced(self):
        g = sample_graph()
        g["concepts"][0]["artifact_refs"] = ["docs/missing.md"]
        g["concepts"][1]["artifact_refs"] = ["docs/target.md#wrong-heading"]

        def build(root: Path) -> None:
            (root / "docs").mkdir()
            (root / "docs/target.md").write_text("# Real Heading\n\nText.\n", encoding="utf-8")
            (root / "docs/links.md").write_text(
                "[esc](../../outside.md)\n[frag](target.md#no-such-anchor)\n", encoding="utf-8")
            ref_dir = root / "knowledge/skills/ppa-leaf/references"
            ref_dir.mkdir(parents=True)
            (ref_dir.parent / "SKILL.md").write_text(
                "---\nname: ppa-leaf\ndescription: Use when a. Do not use for b.\n---\n"
                + "x\n" * 260, encoding="utf-8")
            (ref_dir / "up.md").write_text("[up](../SKILL.md)\n", encoding="utf-8")

        fails = self.failures(self.check(g, build))
        self.assertEqual(len(fails["artifact_refs"]), 2, fails["artifact_refs"])
        links = "\n".join(fails["links"])
        self.assertIn("link escapes root", links)
        self.assertIn("broken heading fragment", links)
        self.assertIn("reference must not link to SKILL.md", links)
        self.assertIn("orphan reference", links)

    def test_line_ceilings_frontmatter_and_malformed_citations(self):
        def build(root: Path) -> None:
            router = root / "knowledge/skills/ppa-program-analysis"
            (router / "references").mkdir(parents=True)
            fm = "---\nname: {}\ndescription: Use when x. Do not use for y.\n---\n"
            (router / "SKILL.md").write_text(fm.format("ppa-program-analysis") + "x\n" * 96)
            (root / "README.md").write_text("---   \ntitle: t\n---\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs/cite.md").write_text(
                "bad pair (book p. 40; PDF p. 60)\n"
                "near miss (book p 50; PDF p 69)\n"
                "near miss [PPA Table 9.9 p. 300]\n", encoding="utf-8")

        fails = self.failures(self.check(None, build))
        ceilings = "\n".join(fails["line_ceilings"])
        self.assertIn("100 lines (must be >= 50 and < 100, C3.1)", ceilings)
        self.assertIn("README.md: must not carry YAML frontmatter", ceilings)
        cites = "\n".join(fails["inline_citations"])
        self.assertIn("expected PDF 59", cites)
        self.assertIn("malformed '(book p...)'", cites)
        self.assertIn("malformed '[PPA...]'", cites)


class HeaderComplianceTests(unittest.TestCase):
    """Repository code rules: provenance headers, requirement table resolution, size ceilings."""

    def test_python_files_obey_repository_rules(self):
        mock_token = "unittest." + "mock"
        for path in sorted(list(SCRIPTS.glob("*.py")) + list((ROOT / "tests").glob("*.py"))):
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            self.assertLess(len(lines), 700, path.name)
            if len(lines) >= 50:
                head = "\n".join(lines[:8])
                self.assertRegex(head, r"@governing:\s*REQ-TECH-PPA-\d{3}.*@parent:\s*REQ-PRD-PPA-\d{3}")
                self.assertRegex(head, r"@decision DEC-PPA-\d{3}:")
            self.assertNotIn(mock_token, text, path.name)
            self.assertIsNone(re.search(r"^\s*except\s*:", text, re.M), path.name)
            self.assertIsNone(re.search(r"except[^\n]*:\s*\n\s*pass\b", text), path.name)

    def test_every_governing_and_decision_tag_resolves_in_master_plan(self):
        plan = (ROOT / "MASTER_PLAN.md").read_text(encoding="utf-8")
        arch = (ROOT / "architecture" / "ARCHITECTURE.md").read_text(encoding="utf-8")
        defined_reqs = set(re.findall(r"\|\s*`(REQ-(?:PRD|TECH)-PPA-\d{3})`\s*\|", plan))
        defined_decs = set(re.findall(r"\|\s*`(DEC-PPA-\d{3})`\s*\|", plan))
        self.assertEqual(len(defined_reqs), 12)
        self.assertGreaterEqual(len(defined_decs), 8)
        for p in ROOT.rglob("*"):
            if not p.is_file() or any(part in {".git", "tmp", "__pycache__"} for part in p.parts):
                continue
            if p.suffix not in {".py", ".md"}:
                continue
            head = "\n".join(p.read_text(encoding="utf-8").splitlines()[:10])
            for req in re.findall(r"REQ-(?:PRD|TECH)-PPA-\d{3}", head):
                self.assertIn(req, defined_reqs, f"{p}: {req} missing from MASTER_PLAN.md")
                self.assertIn(req[-3:], arch, f"{p}: {req} missing from ARCHITECTURE.md §10")
            for dec in re.findall(r"@decision\s+(DEC-PPA-\d{3})", head):
                self.assertIn(dec, defined_decs, f"{p}: {dec} missing from MASTER_PLAN.md")

    def test_functions_stay_under_100_lines(self):
        import ast
        for path in sorted(list(SCRIPTS.glob("*.py")) + list((ROOT / "tests").glob("*.py"))):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    span = node.end_lineno - node.lineno + 1
                    self.assertLess(span, 100, f"{path.name}:{node.name} spans {span}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
