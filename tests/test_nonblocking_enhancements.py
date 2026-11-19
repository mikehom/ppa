#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-005, REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-005, REQ-PRD-PPA-006
# @decision DEC-PPA-011: Regression suite for the Tier A anchor and signature
#   gates (ARCHITECTURE 7.1, 7.2), exact C1.8 conservation without a reference
#   rebuild, per-manifest port scoping in a shared root, bounded-block
#   integrity in merged wiki pages, and stale-output pruning. Every fixture is
#   a real scratch tree under tmp/; nothing is mocked.
"""Regression tests for the anchor/signature gates and multi-target port hardening."""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

import test_adapters_and_conformance as base  # noqa: E402

from adapters import common, port_plan  # noqa: E402
import ppa_arch_gates as gates  # noqa: E402
import ppa_conformance_c125 as c125  # noqa: E402
import ppa_conformance_parity as parity  # noqa: E402
import ppa_conformance_scope as scope  # noqa: E402
import validate_ppa_knowledge as vpk  # noqa: E402
import verify_port_conformance as vpc  # noqa: E402

REPO_ROOT = base.REPO_ROOT
SCRIPTS = base.STAGED_SCRIPTS
ADAPTERS = base.ADAPTERS_DIR
NOTATION_HEAD = ("# Notation\n\n| id | symbol | typeface | meaning | book pages | index page |\n"
                 "| :--- | :--- | :--- | :--- | :--- | :--- |\n")
DEMO_REF = "knowledge/skills/ppa-demo/references/demo.md"
DEMO_REFERENCE = """# Demo

## Side Conditions

- first condition
- second condition

### Nested

1. third condition

```text
- fenced line that is not an entry
```

## Table Anchor

| key | value |
| :--- | :--- |
| a | b |
| c | d |
"""
DEMO_SHARD = """# Raw Shard 09

### Lemma 9.1 — One-way demo

If the framework is distributive then the two solutions agree.

### Lemma 9.2 — Two-way demo

The order holds if and only if the map is monotone.
"""
FULL_SUMMARY = {"evaluated": 55, "failed": 0, "not_applicable": 0, "passed": 55, "total": 55}


def _notation_rows(overrides: dict[str, str] | None = None) -> str:
    rows = []
    for row_id, (symbol, meaning) in sorted(gates.KEY_SIGNATURES.items()):
        meaning = (overrides or {}).get(row_id, meaning)
        rows.append(f"| {row_id} | `{symbol}` | italic | {meaning} | 1 | index p. 429 |")
    return "\n".join(rows) + "\n"


def _mini_root(root: Path, reference: str = DEMO_REFERENCE, shard: str = DEMO_SHARD) -> Path:
    """Smallest tree both gates can read: one L1 reference, one L3 shard, the key notation rows."""
    for rel, text in ((DEMO_REF, reference), ("corpus/shards/RAW_SHARD_09_demo.md", shard),
                      ("ontology/notation_index.md", NOTATION_HEAD + _notation_rows())):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    return root


def _node(count: int, *anchors: str) -> dict:
    return {"id": "ppa.demo.node", "conditions": [f"condition {i}" for i in range(count)],
            "artifact_refs": [f"{DEMO_REF}#{a}" if "/" not in a else a for a in anchors],
            "formal_summary": "A demo statement."}


def _check(report: dict, check_id: str) -> dict:
    return next(c for gate in report["gates"].values() for c in gate["checks"] if c["id"] == check_id)


class ArchGateSyntheticTests(unittest.TestCase):
    """Both gates on minimal hermetic trees: entry counting, attribution, vacuity."""

    def setUp(self) -> None:
        self._tmp = base._scratch_dir()  # noqa: SLF001
        self.root = _mini_root(Path(self._tmp.name) / "core")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _anchor(self, node: dict) -> tuple[list[str], int]:
        return gates.check_arch_7_1_l1_anchor_parity(self.root, {"concepts": [node]})

    def _signature(self, *lines: str, graph: dict | None = None) -> list[str]:
        (self.root / DEMO_REF).write_text(DEMO_REFERENCE + "\n" + "\n".join(lines) + "\n", encoding="utf-8")
        return gates.check_arch_7_2_signature_parity(self.root, graph or {"concepts": []})[0]

    def test_anchor_counts_list_items_and_table_rows_but_not_fences_or_headers(self) -> None:
        self.assertEqual(self._anchor(_node(3, "side-conditions")), ([], 1))
        errs, examined = self._anchor(_node(4, "side-conditions"))
        self.assertEqual(examined, 1)
        self.assertEqual(len(errs), 1)
        self.assertIn("ppa.demo.node: 4 conditions", errs[0])
        self.assertIn("carries 3 discrete entries", errs[0])
        self.assertEqual(self._anchor(_node(2, "table-anchor")), ([], 1))
        self.assertIn("carries 2 discrete entries", self._anchor(_node(3, "table-anchor"))[0][0])
        self.assertEqual(self._anchor(_node(1, "nested")), ([], 1))

    def test_anchor_must_resolve_in_an_l1_reference_and_every_anchor_must_carry_the_list(self) -> None:
        for refs in ((), ("no-such-heading",), ("knowledge/skills/ppa-demo/SKILL.md#side-conditions",),
                     ("corpus/shards/RAW_SHARD_09_demo.md#lemma-91--one-way-demo",)):
            with self.subTest(refs=refs):
                errs, _ = self._anchor(_node(1, *refs))
                self.assertEqual(len(errs), 1)
                self.assertIn("no resolving L1 reference anchor", errs[0])
        errs, _ = self._anchor(_node(3, "side-conditions", "table-anchor"))
        self.assertEqual(len(errs), 1)
        self.assertIn("#table-anchor carries 2", errs[0])
        self.assertEqual(self._anchor({"id": "ppa.demo.bare", "conditions": []}), ([], 0))

    def test_biconditional_is_compared_with_the_cited_l3_anchor(self) -> None:
        flagged = self._signature("- The two solutions agree iff the framework is distributive (`Lemma 9.1`).")
        self.assertEqual(len(flagged), 1, flagged)
        self.assertIn("SIGNATURE_DISTORTION", flagged[0])
        self.assertIn("Lemma 9.1", flagged[0])
        self.assertIn(f"{DEMO_REF}:", flagged[0])
        row = self._signature("| Lemma 9.1 | the two solutions agree iff the framework is distributive |")
        self.assertEqual(len(row), 1, row)
        accepted = (
            "- The order holds iff the map is monotone (`Lemma 9.2`).",
            "- With the pointwise order (`x ⊑ y` iff `f(x) ⊑ f(y)`), the solutions agree by `Lemma 9.1`.",
            "- The solutions agree if the framework is distributive (`Lemma 9.1`); this is not an iff.",
            "- A map is strict iff it preserves the least element.",
        )
        self.assertEqual(self._signature(*accepted), [])
        graph = {"concepts": [dict(_node(0), formal_summary="Solutions agree iff distributive (Lemma 9.1).")]}
        in_graph = self._signature(graph=graph)
        self.assertEqual(len(in_graph), 1, in_graph)
        self.assertIn("ontology/concept_graph.json:ppa.demo.node.formal_summary", in_graph[0])

    def test_missing_or_distorted_inventories_fail_instead_of_passing(self) -> None:
        cited = "- The solutions agree if the framework is distributive (`Lemma 9.1`)."
        self.assertEqual(self._signature(cited), [])
        index = self.root / "ontology" / "notation_index.md"
        index.write_text(NOTATION_HEAD + _notation_rows({"N3-138": "greatest fixed point of f"}), encoding="utf-8")
        distorted = self._signature(cited)
        self.assertEqual(len(distorted), 1, distorted)
        self.assertIn("N3-138", distorted[0])
        index.write_text("# Notation\n\nNo rows.\n", encoding="utf-8")
        self.assertIn("no N1/N2/N3 rows parsed", " ".join(self._signature(cited)))
        index.unlink()
        self.assertIn("missing or unreadable", " ".join(self._signature(cited)))
        index.write_text(NOTATION_HEAD + _notation_rows(), encoding="utf-8")
        shutil.rmtree(self.root / "corpus" / "shards")
        self.assertIn("no L3 anchor", " ".join(self._signature(cited)))


class ArchGateLiveTests(unittest.TestCase):
    """Both gates pass on the repository and fail when a known distortion is reintroduced."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = base._scratch_dir()  # noqa: SLF001
        cls.copy = Path(cls._tmp.name) / "core"
        for sub in ("knowledge", "ontology", "corpus/shards"):
            shutil.copytree(REPO_ROOT / sub, cls.copy / sub)
        cls.graph = json.loads((REPO_ROOT / "ontology" / "concept_graph.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def _signature_with(self, rel: str, line: str) -> list[str]:
        path = self.copy / rel
        original = path.read_text(encoding="utf-8")
        path.write_text(original.rstrip("\n") + "\n\n" + line + "\n", encoding="utf-8")
        try:
            return gates.check_arch_7_2_signature_parity(self.copy, self.graph)[0]
        finally:
            path.write_text(original, encoding="utf-8")

    def test_repository_passes_both_gates_with_no_unperformed_rule(self) -> None:
        errs, examined = gates.check_arch_7_1_l1_anchor_parity(REPO_ROOT, self.graph)
        self.assertEqual(errs, [])
        self.assertEqual(examined, sum(1 for n in self.graph["concepts"] if n.get("conditions")))
        self.assertGreaterEqual(examined, 90)
        errs, examined = gates.check_arch_7_2_signature_parity(REPO_ROOT, self.graph)
        self.assertEqual(errs, [])
        self.assertGreater(examined, 500)
        for certify in (False, True):
            with self.subTest(certify=certify):
                report = vpk.validate(REPO_ROOT, strict_gotchas=True, certify=certify)
                rendered = report.render()
                self.assertFalse(report.failed, rendered)
                self.assertEqual(report.not_implemented, [])
                self.assertNotIn("NOT_IMPLEMENTED", rendered)
                for name in ("arch_7_1_l1_anchor_parity", "arch_7_2_signature_parity"):
                    self.assertIn(f"[PASS] {name}", rendered)

    def test_anchor_with_fewer_entries_than_conditions_fails(self) -> None:
        node = next(n for n in self.graph["concepts"] if n["id"] == "ppa.solvers.round-robin-loop-bound")
        ref = next(r for r in node["artifact_refs"] if gates.L1_REF_RE.match(r))
        grown = copy.deepcopy(self.graph)
        target = next(n for n in grown["concepts"] if n["id"] == node["id"])
        target["conditions"] = target["conditions"] + [f"extra condition {i}" for i in range(60)]
        errs, _ = gates.check_arch_7_1_l1_anchor_parity(REPO_ROOT, grown)
        self.assertEqual(len(errs), 1, errs)
        self.assertIn(node["id"], errs[0])
        path = self.copy / ref.split("#", 1)[0]
        original = path.read_text(encoding="utf-8")
        flattened = [ln for ln in original.split("\n")
                     if not gates.LIST_ITEM_RE.match(ln) and not ln.lstrip().startswith("|")]
        path.write_text("\n".join(flattened), encoding="utf-8")
        try:
            errs, _ = gates.check_arch_7_1_l1_anchor_parity(self.copy, self.graph)
        finally:
            path.write_text(original, encoding="utf-8")
        self.assertTrue(any(node["id"] in e and "carries 0 discrete entries" in e for e in errs), errs)

    def test_reintroduced_distortions_fail_signature_parity(self) -> None:
        skills = "knowledge/skills"
        cases = (
            ("knowledge/ambient-context/ppa-dataflow-and-shape.md", "Lemma 2.32",
             "- `MFP = MOP` iff the framework is distributive [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99)."),
            (f"{skills}/ppa-fixedpoint-solvers/SKILL.md", "Lemma 6.12",
             "- Round Robin stops within `d(G_S, T) + 3` passes on fast distributive frameworks (`Lemma 6.12`)."),
            (f"{skills}/ppa-fixedpoint-solvers/SKILL.md", "Lemma 6.12",
             "- `Lemma 6.12`: at most `d + 3` iterations for every fast, distributive framework."),
            (f"{skills}/ppa-types-effects-and-regions/SKILL.md", "Table 5.18",
             "| `rec β.φ` | must be strictly positive in `β` | `Table 5.18` |"),
            (f"{skills}/ppa-abstract-interpretation/SKILL.md", "Lemma 4.45",
             "- The `γ`-induced widening strictly improves precision (`Lemma 4.45`)."),
            (f"{skills}/ppa-fixedpoint-solvers/references/worklist-and-rpo-algorithms.md", "Lemma 6.4",
             "- `Analysis_i` is reductive only upon `W = empty` (`Lemma 6.4`)."),
            (f"{skills}/ppa-fixedpoint-solvers/references/worklist-and-rpo-algorithms.md", "Lemma 6.4",
             "- By `Lemma 6.4` every intermediate state strictly under-approximates the least solution."),
            (f"{skills}/ppa-types-effects-and-regions/SKILL.md", "Table 5.18",
             "- `rec β.φ` is well formed only for strictly positive `β` (`Table 5.18`)."),
            (f"{skills}/ppa-abstract-interpretation/references/correctness-and-fixed-points.md",
             "dual widening", "- Dual widening approximates `gfp(f)` from above."),
            (f"{skills}/ppa-fixedpoint-solvers/references/scc-round-robin-and-advanced-solvers.md",
             "Exercise 6.14", "- For every fast `f`, `lfp(F) = f̄` (`Exercise 6.14`)."),
            ("ontology/cross_paradigm_matrix.md", "Lemma 2.32",
             "| Exactness | `MFP = MOP` if and only if the framework is distributive | `Lemma 2.32` |"),
        )
        for rel, needle, line in cases:
            with self.subTest(needle=needle, rel=rel):
                self.assertTrue((self.copy / rel).is_file(), rel)
                errs = self._signature_with(rel, line)
                self.assertTrue(errs, f"not flagged: {line}")
                self.assertTrue(all(e.startswith(f"{rel}:") and needle in e for e in errs), errs)

    def test_book_faithful_statements_stay_accepted(self) -> None:
        rel = "knowledge/skills/ppa-fixedpoint-solvers/SKILL.md"
        accepted = (
            "- Extending `d + 3` to fast distributive frameworks is `[external: rapid frameworks]` "
            "`[derived]`, not `Lemma 6.12`.",
            "- Reductiveness is certified only upon `W = empty` (`Lemma 6.4`).",
            "- `Lemma 6.4` does not prove `Analysis_i ∉ Red(F)` while the worklist is non-empty.",
            "- `MFP = MOP` if the framework is distributive (`Lemma 2.32`); the converse is not claimed.",
            "- Positivity of `rec β.φ` is a `[derived]` restriction that `Table 5.18` does not state.",
            "- For fast distributive `f`, `lfp(F) = f̄` (`Exercise 6.14`).",
        )
        for line in accepted:
            with self.subTest(line=line):
                self.assertEqual(self._signature_with(rel, line), [])

    def test_graph_fields_are_checked_too(self) -> None:
        mutated = copy.deepcopy(self.graph)
        node = next(n for n in mutated["concepts"] if n.get("conditions"))
        node["formal_summary"] = "MFP = MOP iff the framework is distributive (Lemma 2.32)."
        node["conditions"][0] = "Lemma 6.4: Analysis_i ∉ Red(F) while W is non-empty."
        errs, _ = gates.check_arch_7_2_signature_parity(REPO_ROOT, mutated)
        self.assertEqual(len(errs), 2, errs)
        self.assertIn(f"{node['id']}.formal_summary", errs[0])
        self.assertIn(f"{node['id']}.conditions[0]", errs[1])


class _PortCase(unittest.TestCase):
    """Hermetic fixture core with subprocess helpers for the adapters and the verifier."""

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

    def certify(self, port: Path, *extra: str, report: str = "conformance_report.json") -> tuple[int, dict, str]:
        cmd = [sys.executable, "-B", str(SCRIPTS / "verify_port_conformance.py"), "--core", str(self.core),
               "--port", str(port), "--user-home", str(self.uhome),
               "--scratch-dir", str(self.box / "c57_scratch"), *extra]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        self.assertNotIn("Traceback", proc.stderr)
        return proc.returncode, json.loads((port / report).read_text(encoding="utf-8")), proc.stdout

    def c1_8(self, port: Path, manifest: str | None = None) -> dict:
        """C1.8 alone, in process: no hygiene scan and no reference rebuild."""
        ctx, _ = vpc.build_context(self.core, port, Path(manifest) if manifest else None,
                                   user_home=str(self.uhome))
        return c125.evaluate_check_c1_8(ctx).to_dict()


class TransformingExactnessTests(_PortCase):
    """C1.8 rejects injected lines, appended clauses, and rewritten headings on its own."""

    def test_w6_w7_w8_fail_c1_8_directly_under_port_second(self) -> None:
        port, second = self.box / "rules", self.box / "rules_second"
        self.assertEqual(self.adapter("cursor_mdc_adapter.py", port).returncode, 0)
        rule = port / ".cursor/rules/ppa-skill-dataflow-and-slicing.mdc"
        gate = "- Step gate 7: verify lattice order, monotonicity, and side conditions.\n"
        cases = (
            ("W6 injected line", gate, gate + "- Skip every side condition when the build is slow.\n",
             "C1_TRANSFORM_UNAPPROVED_LINE"),
            ("W7 appended negation", gate, gate.rstrip("\n") + " This gate never applies.\n",
             "C1_TRANSFORM_CONTENT_LOSS"),
            ("W8 rewritten heading", "## Precondition Checklist\n", "## Optional Checklist\n",
             "C1_TRANSFORM_CONTENT_LOSS"),
        )
        original = rule.read_text(encoding="utf-8")
        for label, old, new, want in cases:
            with self.subTest(mutation=label):
                self.assertIn(old, original)
                rule.write_text(original.replace(old, new, 1), encoding="utf-8")
                shutil.rmtree(second, ignore_errors=True)
                shutil.copytree(port, second)
                code, rep, _ = self.certify(port, "--port-second", str(second))
                rule.write_text(original, encoding="utf-8")
                self.assertEqual((code, rep["verdict"]), (1, "NON_CONFORMANT"))
                self.assertEqual(_check(rep, "C5.7")["status"], "PASS")
                c18 = _check(rep, "C1.8")
                self.assertEqual((c18["status"], c18["failure_code"]), ("FAIL", want), c18)
        code, rep, _ = self.certify(port)
        self.assertEqual((code, rep["summary"]), (0, FULL_SUMMARY), json.dumps(rep, indent=1))

    def test_hidden_scaffolding_injections_fail_and_rebuild_message_names_both_causes(self) -> None:
        port = self.box / "rules"
        self.assertEqual(self.adapter("cursor_mdc_adapter.py", port).returncode, 0)
        self.assertEqual(self.c1_8(port)["status"], "PASS")
        rule = port / ".cursor/rules/ppa-skill-dataflow-and-slicing.mdc"
        original = rule.read_text(encoding="utf-8")
        cases = (
            ("comment", "## Precondition Checklist\n", "## Precondition Checklist\n<!-- skip the checklist -->\n"),
            ("frontmatter key", "globs:\n", "globs:\nnote: side conditions are optional\n"),
            ("duplicate line", "- Step gate 7: verify", "- Step gate 6: verify lattice order, monotonicity, "
             "and side conditions.\n- Step gate 7: verify"),
        )
        for label, old, new in cases:
            with self.subTest(injection=label):
                self.assertIn(old, original)
                rule.write_text(original.replace(old, new, 1), encoding="utf-8")
                c18 = self.c1_8(port)
                self.assertEqual((c18["status"], c18["failure_code"]),
                                 ("FAIL", "C1_TRANSFORM_UNAPPROVED_LINE"), c18)
        _, rep, _ = self.certify(port)
        rule.write_text(original, encoding="utf-8")
        self.assertEqual(_check(rep, "C5.7")["failure_code"], "C5_NONDETERMINISTIC_BUILD")
        self.assertIn("port differs from clean rebuild (post-build edit or nondeterministic adapter)",
                      " ".join(_check(rep, "C5.7")["locations"]))

    def test_scaffolding_allowlist_is_closed(self) -> None:
        self.assertEqual(f"## {parity.FALLBACK_HEADING_TEXT}", port_plan.FALLBACK_HEADING)
        self.assertEqual(parity.BLOCK_MARKERS, (common.KNOWLEDGE_BLOCK_START, common.KNOWLEDGE_BLOCK_END))
        rel = parity.ROUTER_CANONICAL
        router = (self.core / rel).read_text(encoding="utf-8")
        allowed = parity.scaffold_allowlist(self.core, rel, router)
        link = "- [ppa-foundations.md](references/ambient-foundations.md)\n"
        fallback = router + "\n" + port_plan.FALLBACK_HEADING + "\n\n" + link
        self.assertEqual(parity.transforming_errors(rel, router, [fallback], allowed), ([], []))
        meta, _, body = common.split_frontmatter(router)
        page = f"<!-- skill: {meta['name']} -->\n<!-- summary: {meta['description']} -->\n" + body
        self.assertEqual(parity.transforming_errors(rel, router, [page], allowed), ([], []))
        for label, text in (
            ("unknown orientation link", fallback + "- [ppa-rogue.md](references/ambient-rogue.md)\n"),
            ("repeated orientation link", fallback + link),
            ("foreign header comment", "<!-- summary: a different summary -->\n" + body),
            ("extra heading", fallback + "\n## Overrides\n"),
        ):
            with self.subTest(case=label):
                lost, injected = parity.transforming_errors(rel, router, [text], allowed)
                self.assertEqual(lost, [])
                self.assertEqual(len(injected), 1, injected)
        other = "knowledge/skills/ppa-dataflow-and-slicing/SKILL.md"
        body = (self.core / other).read_text(encoding="utf-8")
        strict = parity.scaffold_allowlist(self.core, other, body)
        _, injected = parity.transforming_errors(other, body, [body + port_plan.FALLBACK_HEADING + "\n"], strict)
        self.assertEqual(len(injected), 1, injected)


class SharedRootManifestTests(_PortCase):
    """Two targets in one project root, each owning and certifying its own manifest."""

    NAMES = (("claude_code_adapter.py", "port_manifest_claude.json", "conformance_report_claude.json",
              "claude-code", ".claude"),
             ("agents_md_adapter.py", "port_manifest_codex.json", "conformance_report_codex.json",
              "codex-agents", ".agents"))

    def test_two_targets_coexist_and_each_certifies_55_of_55(self) -> None:
        root = self.box / "project"
        for script, manifest, _, _, _ in self.NAMES:
            proc = self.adapter(script, root, "--manifest-name", manifest)
            self.assertEqual(proc.returncode, 0, proc.stderr)
        owned: list[set[str]] = []
        for _, manifest, report, target, tree in self.NAMES:
            with self.subTest(target=target):
                code, rep, out = self.certify(root, "--manifest", manifest, report=report)
                self.assertEqual((code, rep["verdict"], rep["target"]), (0, "CONFORMANT", target),
                                 json.dumps(rep, indent=1))
                self.assertEqual(rep["summary"], FULL_SUMMARY)
                self.assertIn("55/55 evaluated checks PASS", out)
                doc = json.loads((root / manifest).read_text(encoding="utf-8"))
                paths = common.manifest_owned_paths(root, doc, manifest)
                self.assertIn(manifest, paths)
                self.assertTrue(all(p == manifest or p.startswith(f"{tree}/") for p in paths), sorted(paths)[:5])
                owned.append(paths)
        self.assertEqual(owned[0] & owned[1], set())
        self.assertFalse((root / "port_manifest.json").exists())
        self.assertFalse((root / "conformance_report.json").exists())
        before = base._tree_sha256(root / ".agents")  # noqa: SLF001
        again = self.adapter("claude_code_adapter.py", root, "--manifest-name", self.NAMES[0][1])
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(base._tree_sha256(root / ".agents"), before)  # noqa: SLF001

    def test_another_targets_manifest_confers_no_ownership(self) -> None:
        root = self.box / "project"
        self.assertEqual(self.adapter("claude_code_adapter.py", root).returncode, 0)
        before = base._tree_sha256(root)  # noqa: SLF001
        for extra in ((), ("--manifest-name", "port_manifest.json")):
            proc = self.adapter("agents_md_adapter.py", root, *extra)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("port_manifest.json", proc.stderr)
            self.assertIn("Nothing was written", proc.stderr)
        self.assertEqual(base._tree_sha256(root), before)  # noqa: SLF001

    def test_manifest_and_report_names_are_validated_and_derived(self) -> None:
        for bad in ("../escape.json", "sub/dir.json", "manifest.txt", ".hidden.json", "wiki_config.json",
                    "served_units.json", "conformance_report.json", ""):
            with self.subTest(name=bad):
                with self.assertRaises(common.AdapterError):
                    common.validate_manifest_name(bad)
        proc = self.adapter("claude_code_adapter.py", self.box / "bad", "--manifest-name", "../escape.json")
        self.assertEqual(proc.returncode, 1)
        self.assertFalse((self.box / "bad").exists())
        self.assertFalse((self.box / "escape.json").exists())
        self.assertEqual(scope.report_name_for("port_manifest.json"), "conformance_report.json")
        self.assertEqual(scope.report_name_for("port_manifest_claude.json"), "conformance_report_claude.json")
        self.assertEqual(scope.report_name_for("team.json"), "conformance_report_team.json")
        port = self.box / "p"
        self.assertEqual(scope.resolve_manifest_path(port, None), port / "port_manifest.json")
        self.assertEqual(scope.resolve_manifest_path(port, Path("m.json")), port / "m.json")
        elsewhere = self.box / "elsewhere" / "m.json"
        self.assertEqual(scope.resolve_manifest_path(port, elsewhere), elsewhere.resolve())


class BoundedBlockTests(_PortCase):
    """Edits inside the bounded block of a merged wiki page fail C1.8; edits outside it do not."""

    def test_block_tampering_fails_and_operator_edits_outside_pass(self) -> None:
        port = self.box / "wiki"
        index, log = port / "pages" / "index.md", port / "pages" / "log.md"
        index.parent.mkdir(parents=True)
        index.write_text("# Team Wiki\n\n- [Home](home.md)\n", encoding="utf-8")
        self.assertEqual(self.adapter("wiki_sync_adapter.py", port).returncode, 0)
        manifest = json.loads((port / "port_manifest.json").read_text(encoding="utf-8"))
        self.assertIn("pages/index.md", manifest["merged_files"])
        self.assertEqual(sorted(manifest["bounded_blocks"]), ["pages/index.md", "pages/log.md"])
        merged = index.read_text(encoding="utf-8")
        self.assertEqual(manifest["bounded_blocks"]["pages/index.md"], common.bounded_block_record(merged))
        self.assertRegex(manifest["bounded_blocks"]["pages/index.md"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(self.c1_8(port)["status"], "PASS")

        outside = "Operator preface.\n\n" + merged + "\n## Operator Section\n\n- [Mine](mine.md)\n"
        index.write_text(outside, encoding="utf-8")
        code, rep, _ = self.certify(port)
        self.assertEqual((code, rep["summary"]), (0, FULL_SUMMARY), json.dumps(rep, indent=1))

        end = common.KNOWLEDGE_BLOCK_END
        cases = (
            ("injected line", index, outside.replace(end, "- [Rogue page](rogue.md)\n" + end, 1)),
            ("edited line", index, outside.replace("Pinned canonical revision", "Unpinned revision", 1)),
            ("removed end marker", index, outside.replace(end + "\n", "", 1)),
            ("second block", index, outside + common.KNOWLEDGE_BLOCK_START + "\n" + end + "\n"),
            ("generated page", log, log.read_text(encoding="utf-8").replace(end, "- rogue entry\n" + end, 1)),
        )
        for label, path, text in cases:
            with self.subTest(tamper=label):
                saved = path.read_text(encoding="utf-8")
                self.assertNotEqual(text, saved)
                path.write_text(text, encoding="utf-8")
                c18 = self.c1_8(port)
                path.write_text(saved, encoding="utf-8")
                self.assertEqual((c18["status"], c18["failure_code"]), ("FAIL", "C1_BOUNDED_BLOCK_TAMPERED"), c18)
        index.write_text(outside.replace(end, "- [Rogue page](rogue.md)\n" + end, 1), encoding="utf-8")
        code, rep, _ = self.certify(port)
        self.assertEqual((code, _check(rep, "C1.8")["failure_code"]), (1, "C1_BOUNDED_BLOCK_TAMPERED"))

    def test_undeclared_block_and_recompile_repair(self) -> None:
        port = self.box / "wiki"
        (port / "pages").mkdir(parents=True)
        (port / "pages" / "index.md").write_text("# Team Wiki\n", encoding="utf-8")
        self.assertEqual(self.adapter("wiki_sync_adapter.py", port).returncode, 0)
        manifest_path = port / "port_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        stripped = {k: v for k, v in manifest.items() if k != "bounded_blocks"}
        manifest_path.write_text(json.dumps(stripped, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        c18 = self.c1_8(port)
        self.assertEqual(c18["failure_code"], "C1_BOUNDED_BLOCK_TAMPERED", c18)
        self.assertIn("not declared", " ".join(c18["locations"]))
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        index = port / "pages" / "index.md"
        index.write_text(index.read_text(encoding="utf-8").replace("Pinned", "Loose", 1) + "Operator tail.\n",
                         encoding="utf-8")
        self.assertEqual(self.c1_8(port)["failure_code"], "C1_BOUNDED_BLOCK_TAMPERED")
        self.assertEqual(self.adapter("wiki_sync_adapter.py", port).returncode, 0)
        self.assertEqual(self.c1_8(port)["status"], "PASS")
        self.assertTrue(index.read_text(encoding="utf-8").endswith("Operator tail.\n"))


class StalePruneTests(_PortCase):
    """A recompilation removes outputs the previous manifest listed and the new plan drops."""

    def _commit(self, root: Path, outputs: dict[str, str], name: str = "port_manifest.json",
                target: str = "claude-code", force: bool = False) -> port_plan.PortPlan:
        plan = port_plan.PortPlan(root, target, force=force, manifest_name=name)
        for rel, text in outputs.items():
            plan.add(rel, text, role="extra")
        plan.commit({"mappings": [], "spec_version": "1", "target": target})
        return plan

    def test_stale_outputs_are_pruned_and_foreign_or_shared_files_survive(self) -> None:
        root = self.box / "port"
        self._commit(root, {"a/keep.md": "keep\n", "a/old/stale.md": "stale\n", "b/only/gone.md": "gone\n",
                            "linked/stale.md": "x\n", "AGENTS.md": "shared\n"})
        (root / "a/old/operator.txt").write_text("operator notes\n", encoding="utf-8")
        outside = self.box / "outside"
        outside.mkdir()
        shutil.move(str(root / "linked"), str(outside / "linked"))
        os.symlink(outside / "linked", root / "linked")
        manifest = json.loads((root / "port_manifest.json").read_text(encoding="utf-8"))
        manifest["extra_units"].append("../outside/escape.md")
        (outside / "escape.md").write_text("outside the port\n", encoding="utf-8")
        (root / "port_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        plan = self._commit(root, {"a/keep.md": "kept and rewritten\n"})
        self.assertEqual(plan.pruned, ["a/old/stale.md", "b/only/gone.md"])
        self.assertFalse((root / "a/old/stale.md").exists())
        self.assertFalse((root / "b").exists())
        self.assertEqual((root / "a/old/operator.txt").read_text(encoding="utf-8"), "operator notes\n")
        self.assertEqual((root / "a/keep.md").read_text(encoding="utf-8"), "kept and rewritten\n")
        self.assertEqual((root / "AGENTS.md").read_text(encoding="utf-8"), "shared\n")
        self.assertTrue((outside / "linked/stale.md").is_file())
        self.assertTrue((outside / "escape.md").is_file())
        listed = json.loads((root / "port_manifest.json").read_text(encoding="utf-8"))["extra_units"]
        self.assertEqual(listed, ["a/keep.md"])
        self.assertEqual(self._commit(root, {"a/keep.md": "kept and rewritten\n"}).pruned, [])

    def test_pruning_reads_only_the_manifest_of_the_same_name_and_target(self) -> None:
        root = self.box / "port"
        self._commit(root, {"one/a.md": "a\n", "both/x.md": "first\n"}, name="first.json")
        (root / "package.json").write_text("{not json", encoding="utf-8")
        self._commit(root, {"two/b.md": "b\n", "both/x.md": "taken over\n"}, name="second.json",
                     target="codex-agents", force=True)
        plan = self._commit(root, {"one/c.md": "c\n"}, name="first.json")
        self.assertEqual(plan.pruned, ["one/a.md"])
        self.assertTrue((root / "two/b.md").is_file())
        self.assertEqual((root / "both/x.md").read_text(encoding="utf-8"), "taken over\n")
        other = port_plan.PortPlan(root, "codex-agents", manifest_name="scratch.json")
        self.assertEqual(other.stale_paths(), [])

    def test_recompiling_with_a_new_layout_prunes_the_old_tree_and_still_certifies(self) -> None:
        port = self.box / "port"
        self.assertEqual(self.adapter("gemini_harness_adapter.py", port, "--skills-dir", "skills-a").returncode, 0)
        old_skill = port / "skills-a/ppa-program-analysis/SKILL.md"
        self.assertTrue(old_skill.is_file())
        notes = port / "skills-a/ppa-dataflow-and-slicing/NOTES.txt"
        notes.write_text("operator notes\n", encoding="utf-8")
        proc = self.adapter("gemini_harness_adapter.py", port, "--skills-dir", "skills-b")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertFalse(old_skill.exists())
        self.assertFalse(old_skill.parent.exists())
        self.assertEqual([p.relative_to(port).as_posix() for p in sorted((port / "skills-a").rglob("*"))
                          if p.is_file()], ["skills-a/ppa-dataflow-and-slicing/NOTES.txt"])
        self.assertTrue((port / "skills-b/ppa-program-analysis/SKILL.md").is_file())
        code, rep, _ = self.certify(port)
        self.assertEqual((code, rep["summary"]), (0, FULL_SUMMARY), json.dumps(rep, indent=1))


if __name__ == "__main__":
    unittest.main()
