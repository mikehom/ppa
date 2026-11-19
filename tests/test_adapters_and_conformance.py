#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Hermetic stdlib integration suite verifying dual-build
#   determinism across all 5 adapters, full 55-check C1-C6 certification
#   (CONFORMANT, CONFORMANT_WITH_DEVIATIONS, NON_CONFORMANT), and mutation traps.
"""Integration tests for reference harness adapters and verify_port_conformance.py."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_THIS_DIR = Path(__file__).resolve().parent
SUITE_ROOT = _THIS_DIR.parent
REPO_ROOT = (
    SUITE_ROOT
    if (SUITE_ROOT / "corpus" / "pdf_page_map.json").is_file()
    else SUITE_ROOT.parent.parent
)
BASE_SCRIPTS = REPO_ROOT / "scripts"
STAGED_SCRIPTS = SUITE_ROOT / "scripts"
ADAPTERS_DIR = SUITE_ROOT / "adapters"

for _p in (str(STAGED_SCRIPTS), str(BASE_SCRIPTS), str(SUITE_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import check_portability_hygiene as hygiene  # noqa: E402
import issue_ctl  # noqa: E402
import ppa_arch_gates as arch_gates  # noqa: E402
import validate_ppa_knowledge as vpk  # noqa: E402
import verify_port_conformance as vpc  # noqa: E402


def _scratch_dir() -> tempfile.TemporaryDirectory:
    scratch_root = REPO_ROOT / "tmp"
    scratch_root.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=scratch_root, prefix="w7_test_")


def _tree_sha256(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name != "conformance_report.json":
            out[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def _failure_codes(report: dict) -> set[str]:
    codes: set[str] = set()
    for gate in report.get("gates", {}).values():
        for chk in gate.get("checks", []):
            if chk.get("failure_code"):
                codes.add(str(chk["failure_code"]))
    return codes


def _pad_skill_body(header: str, ref_link: str, cite: str, marker: str, target_lines: int) -> str:
    link_href = ref_link if ref_link.startswith(("references/", "./references/")) else f"references/{ref_link}"
    lines = [
        "<!-- @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006 -->",
        f"# {header}",
        "",
        f"Ground formal preconditions in [{ref_link}]({link_href}) {cite}.",
        f"Cross-reference marker: {marker}.",
        "",
        "## Precondition Checklist",
        "",
    ]
    idx = 1
    while len(lines) < target_lines:
        lines.append(f"- Step gate {idx}: verify lattice order, monotonicity, and side conditions.")
        idx += 1
    return "\n".join(lines) + "\n"


def _build_synthetic_concepts(pm_doc: dict) -> list[dict]:
    pdf_of = {p["book_page"]: p["pdf_page"] for p in pm_doc["pages"] if p["book_page"] is not None}
    dfa_cites: list[dict] = []
    cfa_cites: list[dict] = []
    for key, item in sorted({**pm_doc["tables"], **pm_doc["figures"]}.items()):
        ch = str(item["chapter_or_app"])
        bp = int(item["book_page"])
        entry = {
            "book_page": bp,
            "chapter_or_app": ch,
            "pdf_page": pdf_of[bp],
            "section": None,
            "table_or_fig": key,
        }
        (dfa_cites if ch in {"1", "2", "4", "A"} else cfa_cites).append(entry)
    for sec_id, sdata in sorted(pm_doc["sections"].items()):
        ch = sec_id.split(".", 1)[0]
        bp = int(sdata["book_start"])
        entry = {
            "book_page": bp,
            "chapter_or_app": ch,
            "pdf_page": pdf_of[bp],
            "section": sec_id,
            "table_or_fig": None,
        }
        (dfa_cites if ch in {"1", "2", "4", "A"} else cfa_cites).append(entry)

    proj = {
        "cs_theory": "Complete lattice least fixed point with explicit monotonicity side conditions.",
        "cyber": "May over-approximation yields false alarms on taint sinks [external] when safe.",
        "practical_debugging": "Oscillation indicates a non-monotone transfer function.",
        "swe_architecture": "Strategy transfer functions plugged into a worklist solver.",
    }
    u5_basis = {
        "citations": [{"book_page": None, "book_page_roman": "VII", "chapter_or_app": "Preface",
                       "pdf_page": 7, "section": None, "table_or_fig": None}],
        "conditions": ["Context length k >= 0 bounds syntactic call-site histories"],
        "differs": ["Chapter 2 tracks procedure call strings; Chapter 3 tracks dynamic closures"],
        "unification_id": "U5",
    }
    return [
        {
            "altitude": "L1",
            "artifact_refs": [
                "corpus/shards/RAW_SHARD_01_test.md",
                "knowledge/skills/ppa-dataflow-and-slicing/references/dfa-core.md#dfa-core",
            ],
            "citations": dfa_cites,
            "formal_summary": "Monotone framework instance over complete lattice L with ACC (BKL-001).",
            "id": "ppa.dfa.core",
            "conditions": ["RD requires forward MUST-NOT polarity"],
            "issue_refs": ["BKL-001"],
            "projections": proj,
            "related_edges": [{"basis": u5_basis, "relation": "corresponds_to", "target_id": "ppa.cfa.core"}],
            "title": "Monotone Data Flow Core",
            "unit": "U2a",
        },
        {
            "altitude": "L1",
            "artifact_refs": [
                "corpus/shards/RAW_SHARD_01_test.md",
                "knowledge/skills/ppa-control-flow-and-constraints/references/cfa-core.md",
            ],
            "citations": cfa_cites,
            "formal_summary": "Coinductive and constraint-based closure flow acceptability.",
            "id": "ppa.cfa.core",
            "projections": proj,
            "related_edges": [{"basis": u5_basis, "relation": "corresponds_to", "target_id": "ppa.dfa.core"}],
            "title": "Control Flow Constraint Core",
            "unit": "U3a",
        },
    ]


def _write_fixture_skills(core: Path) -> None:
    router_dir = core / "knowledge" / "skills" / "ppa-program-analysis"
    dfa_dir = core / "knowledge" / "skills" / "ppa-dataflow-and-slicing"
    cfa_dir = core / "knowledge" / "skills" / "ppa-control-flow-and-constraints"
    for d in (router_dir, dfa_dir, cfa_dir):
        (d / "references").mkdir(parents=True, exist_ok=True)
        (d / "evals").mkdir(parents=True, exist_ok=True)

    router_lines = [
        "---",
        "name: ppa-program-analysis",
        "description: >-",
        "  Routes static analysis tasks across Principles of Program Analysis.",
        "  Use when choosing or comparing static analysis paradigms.",
        "  Do not use when a single paradigm is already chosen: use ppa-dataflow-and-slicing",
        "  for syntactic CFG dataflow or ppa-control-flow-and-constraints for closure call graphs.",
        "---",
        "<!-- @governing: REQ-TECH-PPA-001 @parent: REQ-PRD-PPA-001 -->",
        "# PPA Router",
        "",
        "## Decision Table",
        "",
        "| Task shape | Route to | Discriminator | Negative route |",
        "| :--- | :--- | :--- | :--- |",
        "| Per-point facts on fixed CFG | `ppa-dataflow-and-slicing` | CFG known syntactically | Use `ppa-control-flow-and-constraints` for higher-order calls |",
        "| Closure targets and call graphs | `ppa-control-flow-and-constraints` | Control flow computed | Use `ppa-dataflow-and-slicing` for fixed CFG bit-vectors |",
        "",
        "## References",
        "",
        "- [foundations.md](references/foundations.md): Chapter 1 safe approximation [PPA §1.1, p. 1] (book p. 1; PDF p. 21).",
    ]
    while len(router_lines) < 60:
        router_lines.append(f"- Routing invariant note {len(router_lines)}: preserve polarity.")
    (router_dir / "SKILL.md").write_text("\n".join(router_lines) + "\n", encoding="utf-8")
    (router_dir / "references" / "foundations.md").write_text(
        "# Foundations\n\nSafe approximation [PPA §1.1, p. 2] (book p. 2; PDF p. 22) "
        "and MFP vs MOP [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99).\n",
        encoding="utf-8",
    )

    dfa_fm = "\n".join([
        "---",
        "name: ppa-dataflow-and-slicing",
        "description: >-",
        "  Designs intraprocedural bit-vector equations, reaching definitions, live variables,",
        "  and imperative program slices over explicit syntactic flow graphs.",
        "  Use when computing block entry or exit facts on imperative statements.",
        "  Do not use for higher-order closure dispatch; use ppa-control-flow-and-constraints.",
        "---",
    ])
    (dfa_dir / "SKILL.md").write_text(
        dfa_fm + "\n" + _pad_skill_body("Dataflow Skill", "dfa-core.md", "[PPA §2.3, p. 66]", "BKL-001", 262),
        encoding="utf-8",
    )
    (dfa_dir / "references" / "dfa-core.md").write_text(
        "# DFA Core\n\nMonotone frameworks (`ppa.dfa.core`) require ACC [PPA §2.3, p. 66] "
        "(book p. 66; PDF p. 85) and Lemma [PPA Lemma 2.32, p. 80] (G-U1-01, BKL-001).\n\n"
        "- Side condition: reaching definitions run forward with MUST-NOT polarity.\n",
        encoding="utf-8",
    )

    cfa_fm = "\n".join([
        "---",
        "name: ppa-control-flow-and-constraints",
        "description: >-",
        "  Constructs abstract cache and environment inclusion constraints to resolve lambda",
        "  abstractions, indirect function pointers, and polymorphic dynamic dispatch.",
        "  Use when call graph targets depend on runtime functional values.",
        "  Do not use for fixed syntactic imperative graphs; use ppa-dataflow-and-slicing.",
        "---",
    ])
    (cfa_dir / "SKILL.md").write_text(
        cfa_fm + "\n" + _pad_skill_body("CFA Skill", "./references/cfa-core.md", "[PPA §3.1, p. 141]", "ppa.cfa.core", 262),
        encoding="utf-8",
    )
    (cfa_dir / "references" / "cfa-core.md").write_text(
        "# CFA Core\n\nClosure flow (`ppa.cfa.core`) acceptability [PPA §3.1, p. 141] "
        "(book p. 141; PDF p. 159) links to [foundations.md](../../ppa-program-analysis/references/foundations.md).\n",
        encoding="utf-8",
    )

    _write_fixture_evals(router_dir, dfa_dir, cfa_dir)
    amb_dir = core / "knowledge" / "ambient-context"
    amb_dir.mkdir(parents=True, exist_ok=True)
    amb_lines = [
        "# Program Analysis Orientation",
        "",
        "Static analysis computes safe approximations [PPA §1.1, p. 1] (book p. 1; PDF p. 21).",
        "Formal DFA reference: [dfa-core.md](../skills/ppa-dataflow-and-slicing/references/dfa-core.md).",
    ] + [f"- Orientation clause {i}: soundness polarity governs precision." for i in range(1, 90)]
    (amb_dir / "ppa-foundations.md").write_text("\n".join(amb_lines) + "\n", encoding="utf-8")


def _write_fixture_evals(router_dir: Path, dfa_dir: Path, cfa_dir: Path) -> None:
    (router_dir / "evals" / "cases.yaml").write_text(
        "cases:\n"
        '  - id: r1\n    prompt: "Compare the four static analysis approaches"\n    expect_skill: ppa-program-analysis\n'
        '  - id: r2\n    prompt: "Explain safe approximation in Chapter 1"\n    expect_skill: ppa-program-analysis\n'
        '  - id: r3\n    prompt: "State Tarski fixed point theorem"\n    expect_skill: ppa-program-analysis\n'
        '  - id: r4\n    prompt: "Compute reaching definitions on WHILE blocks"\n    expect_skill: ppa-dataflow-and-slicing\n'
        '  - id: r5\n    prompt: "Run coverage fuzzing at runtime"\n    expect_skill: none\n',
        encoding="utf-8",
    )
    (dfa_dir / "evals" / "cases.yaml").write_text(
        "cases:\n"
        '  - id: d1\n    prompt: "Compute reaching definitions on WHILE blocks"\n    expect_skill: ppa-dataflow-and-slicing\n'
        '  - id: d2\n    prompt: "Build ud and du chains for slicing"\n    expect_skill: ppa-dataflow-and-slicing\n'
        '  - id: d3\n    prompt: "Verify Available Expressions transfer monotonicity"\n    expect_skill: ppa-dataflow-and-slicing\n'
        '  - id: d4\n    prompt: "Resolve lambda closures at higher-order call sites"\n    expect_skill: ppa-control-flow-and-constraints\n'
        '  - id: d5\n    prompt: "Run coverage fuzzing at runtime"\n    expect_skill: none\n',
        encoding="utf-8",
    )
    (cfa_dir / "evals" / "cases.yaml").write_text(
        "cases:\n"
        '  - id: c1\n    prompt: "Resolve lambda closures at higher-order call sites"\n    expect_skill: ppa-control-flow-and-constraints\n'
        '  - id: c2\n    prompt: "Generate 0-CFA abstract cache constraints"\n    expect_skill: ppa-control-flow-and-constraints\n'
        '  - id: c3\n    prompt: "Compare uniform k-CFA mementos"\n    expect_skill: ppa-control-flow-and-constraints\n'
        '  - id: c4\n    prompt: "Compute reaching definitions on WHILE blocks"\n    expect_skill: ppa-dataflow-and-slicing\n'
        '  - id: c5\n    prompt: "Run coverage fuzzing at runtime"\n    expect_skill: none\n',
        encoding="utf-8",
    )


def _write_issue_file(path: Path, fm: list[str], cite_and_concept: str) -> None:
    sections = (
        "## Summary\n\nTracked governance item.\n\n"
        f"## Source Citations & Grounding\n\n{cite_and_concept}\n\n"
        "## Technical Analysis / Mechanism\n\nDeterministic verification.\n\n"
        "## Acceptance Gates\n\n- [x] Verified\n\n"
        "## 3-Model Adversarial Alignment & Rebuttal Log\n\n_Pending._\n\n"
        "## Cross-Referenced Concepts & Artifacts\n\n"
        f"{cite_and_concept}\n\n"
        "## Verification Receipts\n\n- 2026-11-19 [open] Seeded.\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + "\n".join(fm) + "\n---\n\n" + sections, encoding="utf-8")


def _build_complete_core(core: Path) -> None:
    (core / "corpus" / "shards").mkdir(parents=True, exist_ok=True)
    (core / "ontology").mkdir(parents=True, exist_ok=True)
    (core / "architecture").mkdir(parents=True, exist_ok=True)
    (core / "adapters").mkdir(parents=True, exist_ok=True)
    (core / "scripts").mkdir(parents=True, exist_ok=True)

    shutil.copyfile(REPO_ROOT / "corpus" / "pdf_page_map.json", core / "corpus" / "pdf_page_map.json")
    shutil.copyfile(REPO_ROOT / "ontology" / "concept_graph.schema.json",
                    core / "ontology" / "concept_graph.schema.json")
    for arch_md in (REPO_ROOT / "architecture").glob("*.md"):
        shutil.copyfile(arch_md, core / "architecture" / arch_md.name)
    shutil.copyfile(SUITE_ROOT / "README.md", core / "README.md")
    for sfile in ("check_portability_hygiene.py", "issue_ctl.py", "validate_ppa_knowledge.py",
                  "ppa_artifact_rules.py", "ppa_arch_gates.py"):
        shutil.copyfile(BASE_SCRIPTS / sfile, core / "scripts" / sfile)
    for w7_sfile in ("verify_port_conformance.py", "ppa_conformance_c125.py", "ppa_conformance_c34.py",
                     "ppa_conformance_c6.py", "ppa_conformance_c4.py", "ppa_conformance_scope.py",
                     "ppa_conformance_parity.py"):
        shutil.copyfile(STAGED_SCRIPTS / w7_sfile, core / "scripts" / w7_sfile)
    for afile in ADAPTERS_DIR.glob("*.py"):
        shutil.copyfile(afile, core / "adapters" / afile.name)

    pm_doc = json.loads((core / "corpus" / "pdf_page_map.json").read_text(encoding="utf-8"))
    graph_doc = {
        "concepts": _build_synthetic_concepts(pm_doc),
        "description": "Synthetic complete whole-book test graph.",
        "schema_version": 1,
    }
    (core / "ontology" / "concept_graph.json").write_text(
        json.dumps(graph_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    cite = "[PPA Index of Notation, p. 429] (book p. 429; PDF p. 443)"
    rows = [f"| {rid} | `{sym}` | italic | {meaning} | 1 | {cite} |"
            for rid, (sym, meaning) in sorted(arch_gates.KEY_SIGNATURES.items())]
    (core / "ontology" / "notation_index.md").write_text(
        "# Notation Index\n\n| id | symbol | typeface | meaning | book pages | index page |\n"
        "| :--- | :--- | :--- | :--- | :--- | :--- |\n" + "\n".join(rows) + "\n", encoding="utf-8")
    (core / "ontology" / "altitude_alignment_log.md").write_text(
        "# Altitude Alignment Log\n\n## Refactor movements\n\n"
        "| Refactor ID | Item | Issue |\n| :--- | :--- | :--- |\n"
        "| `REF-001` | Shared foundation link | `issues/refactors/REF-001.md` |\n",
        encoding="utf-8",
    )
    (core / "ontology" / "cross_paradigm_matrix.md").write_text("# Cross-Paradigm Matrix\n", encoding="utf-8")
    (core / "corpus" / "RAW_KNOWLEDGE.md").write_text("# Raw Knowledge Corpus\n", encoding="utf-8")
    (core / "corpus" / "shards" / "RAW_SHARD_01_test.md").write_text(
        "# Raw Shard 01\n\nStatement [PPA Lemma 2.32, p. 80] (book p. 80; PDF p. 99).\n\n"
        "## Gotcha Ledger\n\n"
        "- G-U1-01: Safe answers state 'among' rather than exact equality [PPA §1.1, p. 3].\n",
        encoding="utf-8",
    )
    _write_fixture_skills(core)

    (core / "issues").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO_ROOT / "issues" / "SCHEMA.md", core / "issues" / "SCHEMA.md")
    _write_issue_file(core / "issues" / "epics" / "EPIC-001.md", [
        "id: EPIC-001", 'title: "Root Epic"', "issue_type: epic", "status: open",
        "priority: P0", "labels: [ppa]", "milestone: M1", "parent_issue: null",
        "depends_on: []", "blocks: [ISS-W1-01]", 'ppa_scope: ["Whole book"]',
        "altitudes: [L0, L1, L2, L3]", "aligned_models: []",
        "created_at: 2026-11-18", "updated_at: 2026-11-19", "github_issue_number: null",
    ], "- [PPA §1.1, p. 1] (`ppa.dfa.core`)")
    _write_issue_file(core / "issues" / "shards" / "ISS-W1-01.md", [
        "id: ISS-W1-01", 'title: "Wave 1 Shard"', "issue_type: shard", "status: open",
        "priority: P1", "labels: [ppa]", "milestone: M1", "parent_issue: EPIC-001",
        "depends_on: [EPIC-001]", "blocks: []", 'ppa_scope: ["Ch 1-3"]',
        "altitudes: [L1, L2]", "aligned_models: []",
        "created_at: 2026-11-18", "updated_at: 2026-11-19", "github_issue_number: null",
    ], "- [PPA §2.3, p. 66] (`ppa.dfa.core`)")
    _write_issue_file(core / "issues" / "refactors" / "REF-001.md", [
        "id: REF-001", 'title: "Shared Foundation Link"', "issue_type: refactor", "status: open",
        "priority: P2", "labels: [ppa]", "milestone: M1", "parent_issue: ISS-W1-01",
        "depends_on: []", "blocks: []", 'ppa_scope: ["Ch 1"]',
        "altitudes: [L1]", "aligned_models: []",
        "created_at: 2026-11-18", "updated_at: 2026-11-19", "github_issue_number: null",
    ], "- [PPA §1.1, p. 1] (`ppa.dfa.core`)")
    _write_issue_file(core / "issues" / "backlog" / "BKL-001.md", [
        "id: BKL-001", 'title: "Unbounded Integers"', "issue_type: edge_case", "status: open",
        "priority: P1", "labels: [ppa, backlog]", "milestone: M1", "parent_issue: ISS-W1-01",
        "depends_on: []", "blocks: []", 'ppa_scope: ["§2.3"]',
        "altitudes: [L1, L2]", "aligned_models: []",
        "created_at: 2026-11-18", "updated_at: 2026-11-19", "github_issue_number: null",
    ], "- [PPA §2.3, p. 66] (book p. 66; PDF p. 85)\n- Concept: `ppa.dfa.core`")
    rc = issue_ctl.cmd_export(core, dry_run=True)
    if rc != 0:
        raise RuntimeError("fixture issue_ctl export failed")


class AdaptersAndConformanceTests(unittest.TestCase):
    """Hermetic tests for all 5 harness adapters and verify_port_conformance.py."""

    def setUp(self) -> None:
        self._tmp = _scratch_dir()
        self.box = Path(self._tmp.name)
        self.core = self.box / "core"
        self.uhome = self.box / "uhome"
        self.uhome.mkdir(parents=True, exist_ok=True)
        _build_complete_core(self.core)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _run_adapter(self, script_name: str, port_dir: Path, *extra: str) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable, "-B", str(ADAPTERS_DIR / script_name),
            "--repo-root", str(self.core),
            "--port-root", str(port_dir),
            "--canonical-revision", "rev-test-001",
            "--user-home", str(self.uhome),
            *extra,
        ]
        return subprocess.run(cmd, capture_output=True, text=True, check=False)

    def _run_verifier(self, port_dir: Path, *extra: str) -> tuple[int, dict]:
        cmd = [
            sys.executable, "-B", str(STAGED_SCRIPTS / "verify_port_conformance.py"),
            "--core", str(self.core),
            "--port", str(port_dir),
            "--user-home", str(self.uhome),
            "--scratch-dir", str(self.box / "c57_scratch"),
            *extra,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        report = json.loads((port_dir / "conformance_report.json").read_text(encoding="utf-8"))
        return proc.returncode, report

    def test_canonical_only_and_readme_validation(self) -> None:
        v_report = vpk.validate(self.core, strict_gotchas=True, certify=False)
        self.assertFalse(v_report.failed, v_report.render())
        report, code = vpc.certify(
            core_root=self.core,
            canonical_only=True,
            user_home=str(self.uhome),
            scratch_base=self.box / "scratch_canon",
        )
        self.assertEqual(code, 0, json.dumps(report, indent=2))
        self.assertEqual(report["verdict"], "CONFORMANT")
        self.assertEqual(list(report["gates"].keys()), ["C5", "C1", "C3", "C2", "C4", "C6"])
        total_checks = sum(len(g["checks"]) for g in report["gates"].values())
        self.assertEqual(total_checks, 55)
        for gate in report["gates"].values():
            for chk in gate["checks"]:
                self.assertNotEqual(chk["status"], "NOT_IMPLEMENTED")

    def test_all_five_adapters_compile_deterministically_and_certify(self) -> None:
        matrix = [
            ("claude_code_adapter.py", "CLAUDE.md", (), 0, "CONFORMANT"),
            ("gemini_harness_adapter.py", "GEMINI.md", ("--skills-dir", "custom-skills"), 0, "CONFORMANT"),
            ("agents_md_adapter.py", "AGENTS.md", (), 0, "CONFORMANT"),
            ("cursor_mdc_adapter.py", ".cursorrules", (), 0, "CONFORMANT"),
            ("wiki_sync_adapter.py", "system_prompt.md", (), 0, "CONFORMANT"),
        ]
        for script, surface_file, extra_args, exp_code, exp_verdict in matrix:
            with self.subTest(adapter=script):
                p1 = self.box / f"{script}_1"
                p2 = self.box / f"{script}_2"
                for p in (p1, p2):
                    p.mkdir(parents=True, exist_ok=True)
                    (p / surface_file).write_text("# Pre-existing operator instruction\n", encoding="utf-8")
                r1 = self._run_adapter(script, p1, *extra_args)
                r2 = self._run_adapter(script, p2, *extra_args)
                self.assertEqual(r1.returncode, 0, r1.stderr)
                self.assertEqual(r2.returncode, 0, r2.stderr)
                self.assertEqual(_tree_sha256(p1), _tree_sha256(p2))
                for f in p1.rglob("*"):
                    self.assertFalse(f.is_symlink(), f"unexpected symlink: {f}")
                code, rep = self._run_verifier(p1, "--port-second", str(p2))
                self.assertEqual(code, exp_code, json.dumps(rep, indent=2))
                self.assertEqual(rep["verdict"], exp_verdict)

    def test_agents_md_dev_stub_deviation(self) -> None:
        port = self.box / "codex_stub"
        port.mkdir(parents=True, exist_ok=True)
        (port / "AGENTS.md").write_text("# Project Instructions\n", encoding="utf-8")
        for _ in range(2):
            res = self._run_adapter("agents_md_adapter.py", port, "--emit-dev-stub")
            self.assertEqual(res.returncode, 0, res.stderr)
        agents_txt = (port / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(agents_txt.count("PPA On-Demand Knowledge Index"), 1)
        code, rep = self._run_verifier(port)
        self.assertEqual(code, 2, json.dumps(rep, indent=2))
        self.assertEqual(rep["verdict"], "CONFORMANT_WITH_DEVIATIONS")

    def test_mutations_trigger_exact_failure_codes(self) -> None:
        p_c1 = self.box / "mut_c1"
        self._run_adapter("claude_code_adapter.py", p_c1)
        ref = p_c1 / ".claude/skills/ppa-dataflow-and-slicing/references/dfa-core.md"
        ref.write_text(ref.read_text(encoding="utf-8") + "\nTampered line.\n", encoding="utf-8")
        code, rep = self._run_verifier(p_c1)
        self.assertEqual(code, 1)
        self.assertIn("C1_BODY_DIGEST", _failure_codes(rep))

        p_c2 = self.box / "mut_c2"
        self._run_adapter("claude_code_adapter.py", p_c2)
        (p_c2 / "CLAUDE.md").write_text("Unauthorised always-on tax\n", encoding="utf-8")
        code, rep = self._run_verifier(p_c2)
        self.assertEqual(code, 1)
        self.assertIn("C2_SURFACE_MODIFIED", _failure_codes(rep))
        self.assertIn("C2_NONZERO_TAX", _failure_codes(rep))

        p_c3 = self.box / "mut_c3"
        self._run_adapter("claude_code_adapter.py", p_c3)
        ref3 = p_c3 / ".claude/skills/ppa-dataflow-and-slicing/references/dfa-core.md"
        ref3.write_text(ref3.read_text(encoding="utf-8") + "\nBad [up](../SKILL.md).\n", encoding="utf-8")
        code, rep = self._run_verifier(p_c3)
        self.assertEqual(code, 1)
        self.assertIn("C3_LINK_DIRECTION", _failure_codes(rep))

        p_c5 = self.box / "mut_c5"
        self._run_adapter("claude_code_adapter.py", p_c5)
        leaked_path = "/" + "Users/alice/private_checkout/file.md"
        ref5 = p_c5 / ".claude/skills/ppa-program-analysis/references/ambient-foundations.md"
        ref5.write_text(ref5.read_text(encoding="utf-8") + f"\nLeak {leaked_path}\n", encoding="utf-8")
        code, rep = self._run_verifier(p_c5)
        self.assertEqual(code, 1)
        self.assertIn("C5_ABSOLUTE_PATH", _failure_codes(rep))

    def test_mutations_c4_overlap_and_c6_backlog_blocks(self) -> None:
        cfa_skill = self.core / "knowledge/skills/ppa-control-flow-and-constraints/SKILL.md"
        dfa_skill = self.core / "knowledge/skills/ppa-dataflow-and-slicing/SKILL.md"
        orig_cfa = cfa_skill.read_text(encoding="utf-8")
        dup_desc = (
            "---\nname: ppa-control-flow-and-constraints\ndescription: >-\n"
            "  Designs intraprocedural bit-vector equations, reaching definitions, live variables,\n"
            "  and imperative program slices over explicit syntactic flow graphs.\n"
            "  Use when computing block entry or exit facts on imperative statements.\n"
            "  Do not use for fixed syntactic imperative graphs; use ppa-dataflow-and-slicing.\n---\n"
        )
        _, _, body = vpc.common.split_frontmatter(orig_cfa)
        cfa_skill.write_text(dup_desc + body, encoding="utf-8")
        self.assertTrue(dfa_skill.is_file())
        p_c4 = self.box / "mut_c4"
        self._run_adapter("claude_code_adapter.py", p_c4)
        code, rep = self._run_verifier(p_c4)
        self.assertEqual(code, 1)
        self.assertIn("C4_DESCRIPTION_OVERLAP", _failure_codes(rep))
        cfa_skill.write_text(orig_cfa, encoding="utf-8")

        shard_md = self.core / "issues/shards/ISS-W1-01.md"
        shard_md.write_text(
            shard_md.read_text(encoding="utf-8").replace(
                "depends_on: [EPIC-001]", "depends_on: [EPIC-001, BKL-001]"
            ),
            encoding="utf-8",
        )
        p_c6 = self.box / "mut_c6"
        self._run_adapter("claude_code_adapter.py", p_c6)
        code, rep = self._run_verifier(p_c6)
        self.assertEqual(code, 1)
        self.assertIn("C6_BACKLOG_BLOCKS", _failure_codes(rep))

    def test_live_repo_compiles_cleanly_across_all_adapters(self) -> None:
        for script, want_code, want_verdict in (
            ("claude_code_adapter.py", 0, "CONFORMANT"),
            ("gemini_harness_adapter.py", 0, "CONFORMANT"),
            ("agents_md_adapter.py", 0, "CONFORMANT"),
            ("cursor_mdc_adapter.py", 0, "CONFORMANT"),
            ("wiki_sync_adapter.py", 0, "CONFORMANT"),
        ):
            out = self.box / f"live_{script}"
            cmd = [
                sys.executable, "-B", str(ADAPTERS_DIR / script),
                "--repo-root", str(REPO_ROOT),
                "--port-root", str(out),
                "--user-home", str(self.uhome),
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, f"{script} failed: {proc.stderr}")
            findings, scanned, _ = hygiene.scan_root(out, [])
            self.assertGreater(scanned, 0)
            self.assertEqual(findings, [], f"{script} hygiene findings: {findings}")
            rep, code = vpc.certify(
                core_root=REPO_ROOT,
                port_root=out,
                user_home=self.uhome,
                scratch_base=self.box,
            )
            self.assertEqual(code, want_code, f"{script} failed C1-C6: {rep}")
            self.assertEqual(rep["verdict"], want_verdict)


    def test_missing_manifest_is_non_conformant(self) -> None:
        empty_port = self.box / "no_manifest_port"
        empty_port.mkdir(parents=True, exist_ok=True)
        code, rep = self._run_verifier(empty_port)
        self.assertEqual(code, 1)
        self.assertEqual(rep["verdict"], "NON_CONFORMANT")

    def test_gemini_frontmatter_parity_and_zero_user_gemini_md_tax(self) -> None:
        user_gemini = self.uhome / ".gemini" / "GEMINI.md"
        user_gemini.parent.mkdir(parents=True, exist_ok=True)
        orig_user = b"# Standing user instructions\n"
        user_gemini.write_bytes(orig_user)
        port = self.box / "gemini_parity"
        port.mkdir(parents=True, exist_ok=True)
        orig_proj = b"# Project instructions\n"
        (port / "GEMINI.md").write_bytes(orig_proj)
        res = self._run_adapter(
            "gemini_harness_adapter.py", port,
            "--skills-dir", "custom-skills", "--memory-dir", "custom-memory",
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(user_gemini.read_bytes(), orig_user)
        self.assertEqual((port / "GEMINI.md").read_bytes(), orig_proj)
        mem_file = port / "custom-memory" / "ppa-foundations.md"
        meta, _, _ = vpc.common.split_frontmatter(mem_file.read_text(encoding="utf-8"))
        self.assertIsNotNone(meta)
        self.assertTrue(meta and meta.get("description"))
        for sk in (port / "custom-skills").glob("*/SKILL.md"):
            sm, _, _ = vpc.common.split_frontmatter(sk.read_text(encoding="utf-8"))
            self.assertEqual(set(sm or {}), {"name", "description"})
        code, rep = self._run_verifier(port)
        self.assertEqual(code, 0, json.dumps(rep, indent=2))
        self.assertEqual(rep["verdict"], "CONFORMANT")

    def test_wiki_config_json_preservation_and_c110_strict_singular(self) -> None:
        port = self.box / "wiki_cfg"
        port.mkdir(parents=True, exist_ok=True)
        seed = {
            "custom_section": {"keep": True},
            "notebook_id": "nb-existing-01",
            "sources": ["pages/sources/user-note.md"],
        }
        (port / "wiki_config.json").write_text(json.dumps(seed, indent=2) + "\n", encoding="utf-8")
        for _ in range(2):
            res = self._run_adapter("wiki_sync_adapter.py", port)
            self.assertEqual(res.returncode, 0, res.stderr)
        cfg = json.loads((port / "wiki_config.json").read_text(encoding="utf-8"))
        self.assertEqual(cfg["notebook_id"], "nb-existing-01")
        self.assertEqual(cfg["custom_section"], {"keep": True})
        self.assertEqual(cfg["sources"][0], "pages/sources/user-note.md")
        self.assertEqual(len(cfg["sources"]), len(set(cfg["sources"])))
        self.assertEqual(cfg["ppa"]["canonical_revision"], "rev-test-001")
        code, rep = self._run_verifier(port)
        self.assertEqual(code, 0, json.dumps(rep, indent=2))
        self.assertEqual(rep["verdict"], "CONFORMANT")
        self.assertEqual(rep["deviations"], [])
        node_card = (port / "pages/concepts/ppa-node-ppa-dfa-core.md").read_text(encoding="utf-8")
        self.assertIn("## Preconditions & Side Conditions", node_card)
        self.assertIn("RD requires forward MUST-NOT", node_card)
        self.assertIn("## Related Issues", node_card)
        for idx_file in (port / "pages").rglob("*.md"):
            if idx_file.name == "index.md" or idx_file.name.startswith("ppa-index-"):
                self.assertLessEqual(len(idx_file.read_text(encoding="utf-8").splitlines()), 250)
        from adapters import wiki_sync_adapter as wsa  # noqa: PLC0415
        chunks = wsa._chunk_markdown_lines(["x"] * 428 + ["```", "a", "b", "c", "```", "y"], "T")  # noqa: SLF001
        self.assertGreaterEqual(len(chunks), 2)
        for ch in chunks:
            self.assertEqual(sum(1 for ln in ch if ln.lstrip().startswith("```")) % 2, 0)

        p_nofiles = self.box / "wiki_nofiles"
        self.assertEqual(self._run_adapter("wiki_sync_adapter.py", p_nofiles, "--dev-nofiles").returncode, 0)
        self.assertFalse((p_nofiles / "pages").exists())
        code_nf, rep_nf = self._run_verifier(p_nofiles)
        self.assertEqual(code_nf, 2, json.dumps(rep_nf, indent=2))
        self.assertEqual(rep_nf["deviations"], ["DEV-NOFILES"])

        mfile = port / "port_manifest.json"
        mdata = json.loads(mfile.read_text(encoding="utf-8"))
        mdata["deviations"] = ["DEV-NOFILES"]
        mfile.write_text(json.dumps(mdata, indent=2) + "\n", encoding="utf-8")
        code_bad, rep_bad = self._run_verifier(port)
        self.assertEqual(code_bad, 1, json.dumps(rep_bad, indent=2))

        p_mdc = self.box / "mut_mdc_c4"
        self.assertEqual(self._run_adapter("cursor_mdc_adapter.py", p_mdc).returncode, 0)
        dfa_mdc = p_mdc / ".cursor/rules/ppa-skill-dataflow-and-slicing.mdc"
        orig_mdc = dfa_mdc.read_text(encoding="utf-8")
        self.assertIn("Do not use", orig_mdc)
        dfa_mdc.write_text(orig_mdc.replace("Do not use", "Xxxxxxxxxx", 1), encoding="utf-8")
        code_m1, rep_m1 = self._run_verifier(p_mdc)
        self.assertEqual(code_m1, 1)
        self.assertIn("C4_BOUNDARY_MISSING", _failure_codes(rep_m1))
        dfa_mdc.write_text(orig_mdc, encoding="utf-8")
        rtr_mdc = p_mdc / ".cursor/rules/ppa-router.mdc"
        rtr_mdc.write_text("\n".join(
            ln for ln in rtr_mdc.read_text(encoding="utf-8").splitlines() if "ppa-dataflow-and-slicing" not in ln
        ) + "\n", encoding="utf-8")
        code_m2, rep_m2 = self._run_verifier(p_mdc)
        self.assertEqual(code_m2, 1)
        self.assertIn("C4_ROUTER_INCOMPLETE", _failure_codes(rep_m2))

        p_c110 = self.box / "mut_c110"
        self._run_adapter("claude_code_adapter.py", p_c110)
        ref = p_c110 / ".claude/skills/ppa-dataflow-and-slicing/references/dfa-core.md"
        ref.write_text(
            ref.read_text(encoding="utf-8") + "\nPlural span (book pp. 1-2; PDF pp. 21-22).\n",
            encoding="utf-8",
        )
        code_m, rep_m = self._run_verifier(p_c110)
        self.assertEqual(code_m, 1)
        self.assertIn("C1_CITATION_MALFORMED", _failure_codes(rep_m))


if __name__ == "__main__":
    unittest.main()
