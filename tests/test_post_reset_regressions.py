#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Regression suite for the whole-book audit defects:
#   non-destructive adapter writes, manifest-scoped certification, conservation
#   of transforming content and discrete conditions, stub laundering, router
#   fallback reachability, and honest N/A / NOT_IMPLEMENTED reporting.
"""Regression tests for adapter write protection and conformance-engine rigor."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

import test_adapters_and_conformance as base  # noqa: E402

from adapters import wiki_cards, wiki_sync_adapter  # noqa: E402
import ppa_conformance_c125 as c125  # noqa: E402
import ppa_conformance_scope as scope  # noqa: E402
import validate_ppa_knowledge as vpk  # noqa: E402
import verify_port_conformance as vpc  # noqa: E402

REPO_ROOT = base.REPO_ROOT
SCRIPTS = base.STAGED_SCRIPTS
ADAPTERS = base.ADAPTERS_DIR
FALLBACK_LINK = "- [ppa-foundations.md](references/ambient-foundations.md)\n"


def _all_checks(report: dict) -> list[dict]:
    return [chk for gate in report["gates"].values() for chk in gate["checks"]]


def _check(report: dict, check_id: str) -> dict:
    return next(chk for chk in _all_checks(report) if chk["id"] == check_id)


def _codes(report: dict) -> set[str]:
    found = {str(c["failure_code"]) for c in _all_checks(report) if c.get("failure_code")}
    return found | {str(c["failure_code"]) for c in report.get("manifest_checks", []) if c.get("failure_code")}


def _edit(path: Path, old: str, new: str) -> str:
    """Replace the first occurrence of old in path; return the original text for restoring."""
    original = path.read_text(encoding="utf-8")
    if old not in original:
        raise AssertionError(f"{path.name}: expected text not found: {old!r}")
    path.write_text(original.replace(old, new, 1), encoding="utf-8")
    return original


class _FixtureCase(unittest.TestCase):
    """Hermetic fixture core plus subprocess helpers for adapters and the verifier."""

    def setUp(self) -> None:
        self._tmp = base._scratch_dir()  # noqa: SLF001
        self.box = Path(self._tmp.name)
        self.core = self.box / "core"
        self.uhome = self.box / "uhome"
        self.uhome.mkdir(parents=True, exist_ok=True)
        base._build_complete_core(self.core)  # noqa: SLF001

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def adapter(self, script: str, port: Path, *extra: str) -> subprocess.CompletedProcess:
        cmd = [sys.executable, "-B", str(ADAPTERS / script), "--repo-root", str(self.core),
               "--port-root", str(port), "--canonical-revision", "rev-test-001",
               "--user-home", str(self.uhome), *extra]
        return subprocess.run(cmd, capture_output=True, text=True, check=False)

    def verify(self, port: Path, *extra: str) -> tuple[int, dict, subprocess.CompletedProcess]:
        cmd = [sys.executable, "-B", str(SCRIPTS / "verify_port_conformance.py"), "--core", str(self.core),
               "--port", str(port), "--user-home", str(self.uhome),
               "--scratch-dir", str(self.box / "c57_scratch"), *extra]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        self.assertNotIn("Traceback", proc.stderr)
        report = json.loads((port / "conformance_report.json").read_text(encoding="utf-8"))
        return proc.returncode, report, proc

    def manifest(self, port: Path) -> dict:
        return json.loads((port / "port_manifest.json").read_text(encoding="utf-8"))


class TransformingConservationTests(_FixtureCase):
    """C1.8 rejects content loss in transforming mappings and compiled concept cards."""

    def test_transforming_mutations_fail_c1_8(self) -> None:
        port = self.box / "wiki_mut"
        self.assertEqual(self.adapter("wiki_sync_adapter.py", port).returncode, 0)
        code, rep, _ = self.verify(port)
        self.assertEqual((code, rep["verdict"]), (0, "CONFORMANT"), json.dumps(rep, indent=1))
        pages = port / "pages" / "concepts"
        cases = (
            ("uncited row deleted", pages / "ppa-program-analysis.md",
             "- Routing invariant note 30: preserve polarity.\n", "", "C1_TRANSFORM_CONTENT_LOSS"),
            ("meaning flipped", pages / "ppa-dataflow-and-slicing.md",
             "Step gate 1: verify lattice order", "Step gate 1: verify lattice chaos",
             "C1_TRANSFORM_CONTENT_LOSS"),
            ("condition bullet deleted", pages / "ppa-node-ppa-dfa-core.md",
             "- RD requires forward MUST-NOT polarity\n", "", "C1_CONDITIONS_PARITY"),
            ("basis difference deleted", pages / "ppa-node-ppa-dfa-core.md",
             "  - **Differs**: Chapter 2 tracks procedure call strings; Chapter 3 tracks dynamic closures\n",
             "", "C1_CONDITIONS_PARITY"),
        )
        for label, path, old, new, want in cases:
            with self.subTest(mutation=label):
                original = _edit(path, old, new)
                code, rep, _ = self.verify(port)
                path.write_text(original, encoding="utf-8")
                self.assertEqual((code, rep["verdict"]), (1, "NON_CONFORMANT"))
                self.assertEqual(_check(rep, "C1.8")["status"], "FAIL")
                self.assertEqual(_check(rep, "C1.8")["failure_code"], want)

    def test_cursor_rule_content_loss_fails_c1_8(self) -> None:
        port = self.box / "cursor_mut"
        self.assertEqual(self.adapter("cursor_mdc_adapter.py", port).returncode, 0)
        _edit(port / ".cursor/rules/ppa-skill-dataflow-and-slicing.mdc",
              "- Step gate 7: verify lattice order, monotonicity, and side conditions.\n", "")
        code, rep, _ = self.verify(port)
        self.assertEqual(code, 1)
        self.assertEqual(_check(rep, "C1.8")["failure_code"], "C1_TRANSFORM_CONTENT_LOSS")


class WriteProtectionTests(_FixtureCase):
    """Adapters never overwrite files they do not own; the wiki root pages are merged."""

    def test_wiki_merge_preserves_operator_index_log_and_resolves_bundle_dir(self) -> None:
        port = self.box / "wiki_existing"
        (port / "pages").mkdir(parents=True)
        user_index = b"# My Wiki\r\n\r\n- [Own note](concepts/own-note.md)\r\nlast line without newline"
        user_log = b"# Log\n\n- 2026-01-01 first entry\n- 2026-02-02 second entry\n"
        (port / "pages" / "index.md").write_bytes(user_index)
        (port / "pages" / "log.md").write_bytes(user_log)
        runs = []
        for _ in range(2):
            res = self.adapter("wiki_sync_adapter.py", port, "--bundle-dir", "raw/ppa_notebooklm_bundle")
            self.assertEqual(res.returncode, 0, res.stderr)
            runs.append(base._tree_sha256(port))  # noqa: SLF001
        self.assertEqual(runs[0], runs[1])
        merged_index = (port / "pages" / "index.md").read_bytes()
        merged_log = (port / "pages" / "log.md").read_bytes()
        self.assertTrue(merged_index.startswith(user_index))
        self.assertTrue(merged_log.startswith(user_log))
        for merged in (merged_index, merged_log):
            self.assertEqual(merged.count(b"<!-- PPA_KNOWLEDGE_START -->"), 1)
            self.assertEqual(merged.count(b"<!-- PPA_KNOWLEDGE_END -->"), 1)
        self.assertIn(b"(ppa_index.md)", merged_index)
        cfg = json.loads((port / "wiki_config.json").read_text(encoding="utf-8"))["ppa"]
        self.assertIn("pages/ppa_index.md", cfg["index_pages"])
        paths = cfg["concept_pages"] + cfg["index_pages"] + cfg["source_pages"] + cfg["notebooklm_bundle"]
        paths += [cfg["index"], cfg["log"], cfg["bundle_manifest"]]
        missing = [p for p in paths if not (port / p).is_file()]
        self.assertEqual(missing, [])
        self.assertTrue(cfg["notebooklm_bundle"])
        self.assertTrue(all(p.startswith("raw/ppa_notebooklm_bundle/") for p in cfg["notebooklm_bundle"]))
        on_disk = sorted(p.name for p in (port / "raw/ppa_notebooklm_bundle").glob("*.md"))
        listed = json.loads((port / cfg["bundle_manifest"]).read_text(encoding="utf-8"))["sources"]
        self.assertEqual(listed, on_disk)
        manifest = self.manifest(port)
        self.assertEqual(sorted(manifest["merged_files"]), ["pages/index.md", "pages/log.md", "wiki_config.json"])
        code, rep, _ = self.verify(port)
        self.assertEqual((code, rep["verdict"]), (0, "CONFORMANT"), json.dumps(rep, indent=1))

    def test_stale_bundle_file_never_enters_bundle_manifest(self) -> None:
        port = self.box / "wiki_stale"
        self.assertEqual(self.adapter("wiki_sync_adapter.py", port).returncode, 0)
        (port / "notebooklm_sources_bundle" / "leftover.md").write_text("# stale\n", encoding="utf-8")
        self.assertEqual(self.adapter("wiki_sync_adapter.py", port).returncode, 0)
        listed = json.loads(
            (port / "notebooklm_sources_bundle" / "bundle_manifest.json").read_text(encoding="utf-8"))["sources"]
        self.assertNotIn("leftover.md", listed)

    def test_foreign_files_abort_before_first_write(self) -> None:
        cases = (
            ("claude_code_adapter.py", ".claude/skills/ppa-program-analysis/SKILL.md", "# operator skill\n"),
            ("cursor_mdc_adapter.py", ".cursor/rules/ppa-router.mdc",
             "---\ndescription: operator rule\nglobs:\nalwaysApply: false\n---\n# operator rule\n"),
        )
        for script, rel, content in cases:
            with self.subTest(adapter=script):
                port = self.box / f"foreign_{script}"
                (port / rel).parent.mkdir(parents=True)
                (port / rel).write_text(content, encoding="utf-8")
                before = base._tree_sha256(port)  # noqa: SLF001
                res = self.adapter(script, port)
                self.assertEqual(res.returncode, 1)
                self.assertIn("--force", res.stderr)
                self.assertEqual(base._tree_sha256(port), before)  # noqa: SLF001
                self.assertFalse((port / "port_manifest.json").exists())

    def test_forced_cursor_collision_is_detected_and_not_laundered(self) -> None:
        port = self.box / "cursor_forced"
        rule = port / ".cursor/rules/ppa-router.mdc"
        rule.parent.mkdir(parents=True)
        rule.write_text("---\ndescription: operator rule\nglobs:\nalwaysApply: false\n---\n# mine\n",
                        encoding="utf-8")
        self.assertEqual(self.adapter("cursor_mdc_adapter.py", port, "--force").returncode, 0)
        for _ in range(2):
            self.assertIn("ppa-router", self.manifest(port)["pre_existing_discovery"])
            code, rep, _ = self.verify(port)
            self.assertEqual(code, 1)
            self.assertEqual(_check(rep, "C4.8")["failure_code"], "C4_NAME_COLLISION")
            self.assertEqual(self.adapter("cursor_mdc_adapter.py", port).returncode, 0)

    def test_same_adapter_rerun_is_idempotent_without_force(self) -> None:
        for script in ("claude_code_adapter.py", "gemini_harness_adapter.py", "agents_md_adapter.py",
                       "cursor_mdc_adapter.py", "wiki_sync_adapter.py"):
            with self.subTest(adapter=script):
                port = self.box / f"idem_{script}"
                first = self.adapter(script, port)
                self.assertEqual(first.returncode, 0, first.stderr)
                snapshot = base._tree_sha256(port)  # noqa: SLF001
                second = self.adapter(script, port)
                self.assertEqual(second.returncode, 0, second.stderr)
                self.assertEqual(base._tree_sha256(port), snapshot)  # noqa: SLF001
                self.assertEqual(self.manifest(port)["pre_existing_discovery"], [])

    def test_missing_pre_existing_discovery_fails_c4_8(self) -> None:
        port = self.box / "claude_nopre"
        self.assertEqual(self.adapter("claude_code_adapter.py", port).returncode, 0)
        manifest = self.manifest(port)
        del manifest["pre_existing_discovery"]
        (port / "port_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        code, rep, _ = self.verify(port)
        self.assertEqual(code, 1)
        self.assertEqual(_check(rep, "C4.8")["failure_code"], "C4_NAME_COLLISION")


class StubAndScopeTests(_FixtureCase):
    """DEV-STUB cannot be laundered; certification reads only manifest-owned files."""

    def test_dev_stub_survives_rerun_without_flag(self) -> None:
        port = self.box / "codex_stub"
        port.mkdir(parents=True)
        original = b"# Project Instructions\n"
        (port / "AGENTS.md").write_bytes(original)
        self.assertEqual(self.adapter("agents_md_adapter.py", port, "--emit-dev-stub").returncode, 0)
        code, rep, _ = self.verify(port)
        self.assertEqual((code, rep["verdict"]), (2, "CONFORMANT_WITH_DEVIATIONS"), json.dumps(rep, indent=1))
        res = self.adapter("agents_md_adapter.py", port)
        self.assertEqual(res.returncode, 0, res.stderr)
        manifest = self.manifest(port)
        self.assertEqual([d["id"] for d in manifest["deviations"]], ["DEV-STUB"])
        surface = next(s for s in manifest["always_on_surfaces"] if s["path"] == "AGENTS.md")
        self.assertEqual(surface["sha256_before"], hashlib.sha256(original).hexdigest())
        self.assertEqual(surface["bytes_before"], len(original))
        code, rep, _ = self.verify(port)
        self.assertEqual((code, rep["verdict"]), (2, "CONFORMANT_WITH_DEVIATIONS"))

        manifest["deviations"] = []
        (port / "port_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        code, rep, _ = self.verify(port)
        self.assertEqual((code, rep["verdict"]), (1, "NON_CONFORMANT"))
        self.assertEqual(_check(rep, "C2.2")["failure_code"], "C2_UNDECLARED_DEVIATION")
        self.assertEqual(_check(rep, "C2.6")["failure_code"], "C2_NONZERO_TAX")

    def test_tampered_stub_is_refused_by_the_adapter(self) -> None:
        port = self.box / "codex_tampered"
        self.assertEqual(self.adapter("agents_md_adapter.py", port, "--emit-dev-stub").returncode, 0)
        _edit(port / "AGENTS.md", "- Load only the skill", "- Always load every skill")
        res = self.adapter("agents_md_adapter.py", port)
        self.assertEqual(res.returncode, 1)
        self.assertIn("pointer stub", res.stderr)

    def test_project_root_with_foreign_files_and_symlink_certifies(self) -> None:
        root = self.box / "project"
        (root / "docs").mkdir(parents=True)
        leaked = "/" + "Users/alice/private/file.md"
        contact = "alice" + "@" + "corp.invalid"
        (root / "notes.txt").write_text(f"owner {contact} keeps {leaked}\n", encoding="utf-8")
        (root / "docs" / "guide.md").write_text("Broken [link](nowhere.md) and (book p. 1\n", encoding="utf-8")
        os.symlink(root / "notes.txt", root / "link-to-notes")
        os.symlink("missing-target", root / "dangling-link")
        self.assertEqual(self.adapter("claude_code_adapter.py", root).returncode, 0)
        code, rep, _ = self.verify(root)
        self.assertEqual((code, rep["verdict"]), (0, "CONFORMANT"), json.dumps(rep, indent=1))

        owned = root / ".claude/skills/ppa-dataflow-and-slicing/references/dfa-core.md"
        owned.unlink()
        os.symlink(root / "notes.txt", owned)
        code, rep, proc = self.verify(root)
        self.assertEqual((code, rep["verdict"]), (1, "NON_CONFORMANT"))
        self.assertEqual(_check(rep, "C5.1")["failure_code"], "C5_SYMLINK_FORBIDDEN")
        self.assertIn("C5.1:C5_SYMLINK_FORBIDDEN", proc.stdout)

    def test_router_fallback_links_ambient_files_and_c3_9_rejects_orphans(self) -> None:
        for script, home in (("claude_code_adapter.py", ".claude"), ("agents_md_adapter.py", ".agents")):
            with self.subTest(adapter=script):
                port = self.box / f"fallback_{home.strip('.')}"
                self.assertEqual(self.adapter(script, port).returncode, 0)
                router = port / home / "skills/ppa-program-analysis/SKILL.md"
                ambient = port / home / "skills/ppa-program-analysis/references/ambient-foundations.md"
                self.assertTrue(ambient.is_file())
                self.assertFalse((port / home / "ppa-ambient").exists())
                text = router.read_text(encoding="utf-8")
                self.assertIn("## Orientation Guides (R1 Fallback)", text)
                self.assertIn(FALLBACK_LINK, text)
                self.assertLess(len(text.splitlines()), 100)
                kinds = {m["canonical"]: m["kind"] for m in self.manifest(port)["mappings"]}
                self.assertEqual(kinds["knowledge/skills/ppa-program-analysis/SKILL.md"], "transforming")
                code, rep, _ = self.verify(port)
                self.assertEqual((code, rep["verdict"]), (0, "CONFORMANT"), json.dumps(rep, indent=1))
                router.write_text(text.replace(FALLBACK_LINK, ""), encoding="utf-8")
                code, rep, _ = self.verify(port)
                self.assertEqual(code, 1)
                self.assertEqual(_check(rep, "C3.9")["failure_code"], "C3_ORPHAN_FILE")

    def test_ambient_description_is_lifted_verbatim_and_overlap_is_checked(self) -> None:
        amb_dir = self.core / "knowledge" / "ambient-context"
        first = amb_dir / "ppa-foundations.md"
        desc = "Orientation on safe approximation, lattice polarity vocabulary, and soundness direction."
        body = first.read_text(encoding="utf-8")
        first.write_text(f"<!-- @description: {desc} -->\n{body}", encoding="utf-8")
        port = self.box / "gemini_desc"
        self.assertEqual(self.adapter("gemini_harness_adapter.py", port).returncode, 0)
        topic = (port / "memory/topics/ppa-foundations.md").read_text(encoding="utf-8")
        meta, _, _ = vpc.common.split_frontmatter(topic)
        self.assertEqual(meta["description"], desc)
        code, rep, _ = self.verify(port)
        self.assertEqual((code, rep["verdict"]), (0, "CONFORMANT"), json.dumps(rep, indent=1))

        (amb_dir / "ppa-dataflow-and-shape.md").write_text(
            f"<!-- @description: {desc} Shape. -->\n{body}", encoding="utf-8")
        rep, code = vpc.certify(core_root=self.core, canonical_only=True, scratch_base=self.box / "scratch")
        self.assertEqual(code, 1)
        self.assertEqual(_check(rep, "C4.3")["failure_code"], "C4_DESCRIPTION_OVERLAP")


class HonestReportingTests(_FixtureCase):
    """N/A for port-only checks, vacuous failures, explicit manifest codes, NOT_IMPLEMENTED."""

    def test_canonical_only_reports_44_evaluated_and_11_not_applicable(self) -> None:
        rep, code = vpc.certify(core_root=self.core, canonical_only=True, scratch_base=self.box / "scratch")
        self.assertEqual((code, rep["verdict"]), (0, "CONFORMANT"), json.dumps(rep, indent=1))
        self.assertEqual(rep["summary"], {"evaluated": 44, "failed": 0, "not_applicable": 11,
                                          "passed": 44, "total": 55})
        not_applicable = {c["id"]: c for c in _all_checks(rep) if c["status"] == "N/A"}
        self.assertEqual(set(not_applicable), set(scope.PORT_ONLY_CHECKS))
        for chk in not_applicable.values():
            self.assertEqual(chk["reason"], "port-only check (requires compiled target port)")
            self.assertEqual(chk["examined"], 0)
        self.assertIn("44/44 evaluated checks PASS, 11 port-only N/A", vpc.summary_line(rep))
        for chk in _all_checks(rep):
            if chk["status"] == "PASS":
                self.assertGreater(chk["examined"], 0, chk["id"])

    def test_empty_core_fails_vacuous_instead_of_passing(self) -> None:
        empty = self.box / "empty_core"
        for sub in ("knowledge", "ontology", "corpus", "issues"):
            (empty / sub).mkdir(parents=True)
        rep, code = vpc.certify(core_root=empty, canonical_only=True, scratch_base=self.box / "scratch")
        self.assertEqual((code, rep["verdict"]), (1, "NON_CONFORMANT"))
        self.assertEqual([c["id"] for c in _all_checks(rep) if c["status"] == "PASS"], [])
        self.assertTrue({"C2_VACUOUS", "C3_VACUOUS", "C4_VACUOUS", "C5_VACUOUS"} <= _codes(rep), _codes(rep))
        self.assertGreater(rep["summary"]["failed"], 0)

    def test_illegal_deviation_and_spec_version_have_explicit_codes(self) -> None:
        port = self.box / "claude_manifest"
        self.assertEqual(self.adapter("claude_code_adapter.py", port).returncode, 0)
        good = self.manifest(port)
        for field, value, check_id, want in (
            ("deviations", ["DEV-BOGUS"], "M.2", "MANIFEST_DEVIATION_ILLEGAL"),
            ("spec_version", "2", "M.1", "MANIFEST_SPEC_VERSION"),
        ):
            with self.subTest(field=field):
                bad = dict(good)
                bad[field] = value
                (port / "port_manifest.json").write_text(json.dumps(bad, indent=2) + "\n", encoding="utf-8")
                code, rep, proc = self.verify(port)
                self.assertEqual((code, rep["verdict"]), (1, "NON_CONFORMANT"))
                failed = {c["id"]: c["failure_code"] for c in rep["manifest_checks"] if c["status"] == "FAIL"}
                self.assertEqual(failed, {check_id: want})
                self.assertIn(f"{check_id}:{want}", proc.stdout)
                self.assertRegex(proc.stdout, r"; [1-9]\d* failed: ")
                self.assertNotIn("all 55 checks PASS", proc.stdout)

    def test_target_without_reference_adapter_needs_port_second(self) -> None:
        ports = []
        for name in ("custom_a", "custom_b"):
            port = self.box / name
            self.assertEqual(self.adapter("claude_code_adapter.py", port).returncode, 0)
            manifest = self.manifest(port)
            manifest["target"] = "custom-harness"
            (port / "port_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            ports.append(port)
        _, rep, _ = self.verify(ports[0])
        c57 = _check(rep, "C5.7")
        self.assertEqual(c57["status"], "FAIL")
        self.assertIn("--port-second", " ".join(c57["locations"]))
        _, rep, _ = self.verify(ports[0], "--port-second", str(ports[1]))
        self.assertEqual(_check(rep, "C5.7")["status"], "PASS")

    def test_validator_reports_not_implemented_in_both_modes(self) -> None:
        for flags in ((), ("--certify",)):
            with self.subTest(flags=flags):
                cmd = [sys.executable, "-B", str(SCRIPTS / "validate_ppa_knowledge.py"),
                       "--root", str(self.core), *flags]
                proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                self.assertIn("[NOT_IMPLEMENTED] arch_7_2_signature_parity", proc.stdout)
                self.assertIn("[PASS] arch_7_1_conditions_parity", proc.stdout)
                self.assertNotIn("deferred_conformance_gates", proc.stdout)
                self.assertRegex(proc.stdout, r"validate_ppa_knowledge PASS \(\d+ NOT_IMPLEMENTED: ")
        self.assertIn("[PASS] conformance_gates_canonical", proc.stdout)
        report = vpk.validate(self.core, certify=True)
        self.assertIn("arch_7_2_signature_parity", report.not_implemented)


class LiveWikiCardTests(unittest.TestCase):
    """Whole-graph checks on a wiki port compiled from the repository itself."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = base._scratch_dir()  # noqa: SLF001
        cls.box = Path(cls._tmp.name)
        cls.port = cls.box / "wiki"
        (cls.box / "uhome").mkdir()
        wiki_sync_adapter.compile_port(
            REPO_ROOT, cls.port, canonical_revision="rev-live", user_home=str(cls.box / "uhome"))
        graph = json.loads((REPO_ROOT / "ontology" / "concept_graph.json").read_text(encoding="utf-8"))
        cls.nodes = graph["concepts"]
        cls.cards = cls.port / "pages" / "concepts"

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def _c1_8(self) -> dict:
        ctx, _ = vpc.build_context(REPO_ROOT, self.port, user_home=str(self.box / "uhome"))
        return c125.evaluate_check_c1_8(ctx).to_dict()

    def _card(self, node: dict) -> Path:
        return self.cards / f"ppa-node-{node['id'].replace('.', '-')}.md"

    def test_every_card_renders_basis_conditions_differences_citations_and_provenance(self) -> None:
        edges = 0
        for node in self.nodes:
            card = self._card(node).read_text(encoding="utf-8")
            self.assertLessEqual(len(card.splitlines()), 250, node["id"])
            self.assertIn("## Provenance", card)
            for ref in node.get("artifact_refs", []):
                self.assertIn(f"`{ref}`", card, node["id"])
            for term in node.get("external_terms", []):
                self.assertIn(f"`{term}`", card, node["id"])
            for edge in node.get("related_edges", []):
                if edge.get("relation") != "corresponds_to":
                    continue
                edges += 1
                basis = edge["basis"]
                for text in basis["conditions"] + basis["differs"]:
                    self.assertIn(text, card, node["id"])
                for cite in basis["citations"]:
                    self.assertIn(wiki_cards.format_concept_cite(cite), card, node["id"])
        self.assertGreaterEqual(edges, 42)
        for page in (self.port / "pages").rglob("*.md"):
            self.assertNotIn("channel: wiki-on-demand", page.read_text(encoding="utf-8"), page.name)

    def test_whole_graph_mutations_fail_c1_8(self) -> None:
        self.assertEqual(self._c1_8()["status"], "PASS")
        total_conditions = sum(len(n.get("conditions", [])) for n in self.nodes)
        self.assertGreaterEqual(total_conditions, 278)
        saved: dict[Path, str] = {}
        removed = 0
        for node in self.nodes:
            if not node.get("conditions"):
                continue
            path = self._card(node)
            saved[path] = path.read_text(encoding="utf-8")
            head, sep, tail = saved[path].partition("## Preconditions & Side Conditions\n")
            section, nxt, rest = tail.partition("\n## ")
            kept = [ln for ln in section.split("\n") if not ln.startswith("- ")]
            removed += len(section.split("\n")) - len(kept)
            path.write_text(head + sep + "\n".join(kept) + nxt + rest, encoding="utf-8")
        self.assertEqual(removed, total_conditions)
        outcome = self._c1_8()
        for path, text in saved.items():
            path.write_text(text, encoding="utf-8")
        self.assertEqual((outcome["status"], outcome["failure_code"]), ("FAIL", "C1_CONDITIONS_PARITY"))

        solver = self.cards / "ppa-fixedpoint-solvers.md"
        text = solver.read_text(encoding="utf-8")
        flipped, n_flips = re.subn(r"\bleast\b", "greatest", text, count=1)
        self.assertEqual(n_flips, 1)
        solver.write_text(flipped, encoding="utf-8")
        outcome = self._c1_8()
        solver.write_text(text, encoding="utf-8")
        self.assertEqual((outcome["status"], outcome["failure_code"]), ("FAIL", "C1_TRANSFORM_CONTENT_LOSS"))

        dataflow = self.cards / "ppa-dataflow-and-slicing.md"
        text = dataflow.read_text(encoding="utf-8")
        rows = [ln for ln in text.split("\n")
                if ln.startswith("|") and "[PPA" not in ln and not re.match(r"^\|[\s:|-]+\|$", ln)][:15]
        self.assertEqual(len(rows), 15)
        dataflow.write_text("\n".join(ln for ln in text.split("\n") if ln not in rows), encoding="utf-8")
        outcome = self._c1_8()
        dataflow.write_text(text, encoding="utf-8")
        self.assertEqual((outcome["status"], outcome["failure_code"]), ("FAIL", "C1_TRANSFORM_CONTENT_LOSS"))
        self.assertEqual(self._c1_8()["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
