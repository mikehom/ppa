#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Reference certification engine for CONFORMANCE_SPEC.md
#   evaluating all 55 checks across C5 -> C1 -> C3 -> C2 -> C4 -> C6 with zero
#   NOT_IMPLEMENTED gates, emitting conformance_report.json, and exiting 0/2/1.
# @decision DEC-PPA-009: Every NON_CONFORMANT verdict names a failing check: the
#   manifest preconditions are explicit check records, port-only checks are N/A
#   (not PASS) without a port, and structural obstacles become report entries.
"""Certify a PPA target harness port (or canonical core) against CONFORMANCE_SPEC.md.

Usage:
    python3 -B scripts/verify_port_conformance.py --core . --port <port_root>
        [--manifest <port_root>/port_manifest.json] [--report <out.json>]
        [--port-second <second build>] [--user-home <dir>]
    python3 -B scripts/verify_port_conformance.py --core . --canonical-only
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _cand in (_HERE, _HERE.parent / "scripts", _HERE.parent.parent.parent / "scripts"):
    if (_cand / "ppa_artifact_rules.py").is_file() and str(_cand) not in sys.path:
        sys.path.insert(0, str(_cand))
for _pkg_parent in (_HERE.parent, _HERE.parent.parent.parent):
    if (_pkg_parent / "adapters" / "common.py").is_file() and str(_pkg_parent) not in sys.path:
        sys.path.insert(0, str(_pkg_parent))
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from adapters import common  # noqa: E402
from ppa_conformance_c125 import (  # noqa: E402
    CheckOutcome,
    ConformanceContext,
    evaluate_gate_c1,
    evaluate_gate_c5,
)
from ppa_conformance_c34 import evaluate_gate_c3  # noqa: E402
from ppa_conformance_c4 import evaluate_gate_c4  # noqa: E402
from ppa_conformance_c6 import (  # noqa: E402
    evaluate_gate_c2,
    evaluate_gate_c6,
)
from ppa_conformance_scope import (  # noqa: E402
    PASSING_STATUSES,
    merged_paths,
    resolve_owned_files,
)
import validate_ppa_knowledge as vpk  # noqa: E402

GATE_ORDER = ("C5", "C1", "C3", "C2", "C4", "C6")
PERMITTED_DEVIATIONS = {"DEV-STUB", "DEV-NOFILES"}


def _dev_nofiles_has_ondisk_trees(port_root: Path, port_files: list[Path]) -> bool:
    """True when the port owns pages/ or non-core skill/rule Markdown files on disk."""
    for p in port_files:
        rel = p.relative_to(port_root).as_posix()
        if rel.startswith("pages/"):
            return True
        if not rel.startswith("core/") and (p.name == "SKILL.md" or p.suffix == ".mdc"):
            return True
    return False


def _parse_deviations(raw_devs: object) -> tuple[set[str], dict[str, str] | None, bool]:
    if not isinstance(raw_devs, list):
        return set(), None, False
    dev_ids: set[str] = set()
    dev_stub: dict[str, str] | None = None
    for item in raw_devs:
        if isinstance(item, str):
            if item not in PERMITTED_DEVIATIONS:
                return set(), None, False
            dev_ids.add(item)
        elif isinstance(item, dict):
            did = str(item.get("id", ""))
            if did not in PERMITTED_DEVIATIONS:
                return set(), None, False
            dev_ids.add(did)
            if did == "DEV-STUB":
                if not isinstance(item.get("surface"), str) or not isinstance(item.get("text"), str):
                    return set(), None, False
                dev_stub = {"id": "DEV-STUB", "surface": item["surface"], "text": item["text"]}
        else:
            return set(), None, False
    return dev_ids, dev_stub, True


def _synthetic_canonical_manifest(core_root: Path) -> dict[str, object]:
    """Identity manifest for canonical-only runs; an incomplete core yields no mappings."""
    try:
        k_files, o_files, _ = common.collect_canonical_package(core_root)
        revision = common.resolve_canonical_revision(core_root)
    except common.AdapterError:
        k_files, o_files, revision = [], [], "unknown"
    mappings = [
        {
            "canonical": p.relative_to(core_root).as_posix(),
            "kind": "lossless",
            "port": [p.relative_to(core_root).as_posix()],
        }
        for p in k_files + o_files
    ]
    return {
        "always_on_surfaces": [],
        "canonical_revision": revision,
        "deviations": [],
        "discovery_entries": common.collect_skill_discovery(core_root, include_ambient=False),
        "mappings": mappings,
        "spec_version": "1",
        "target": "canonical-core",
    }


def _load_port_graph(core_root: Path, port_root: Path, manifest: dict[str, object], canonical_only: bool) -> dict | None:
    if canonical_only:
        doc, err = vpk.load_json(core_root / "ontology" / "concept_graph.json")
        return doc if (not err and isinstance(doc, dict)) else None
    for m in manifest.get("mappings", []) if isinstance(manifest.get("mappings"), list) else []:
        if isinstance(m, dict) and m.get("canonical") == "ontology/concept_graph.json":
            ports = m.get("port", [])
            if isinstance(ports, list) and ports:
                doc, err = vpk.load_json(port_root / str(ports[0]))
                return doc if (not err and isinstance(doc, dict)) else None
    return None


def _core_symlinks(core_root: Path) -> list[str]:
    """Symlinks inside the canonical core directories (forbidden; never followed)."""
    found: list[str] = []
    for sub in ("knowledge", "ontology", "corpus", "issues"):
        for dirpath, dirnames, filenames in os.walk(core_root / sub, followlinks=False):
            for name in sorted(dirnames + filenames):
                cand = Path(dirpath) / name
                if cand.is_symlink():
                    found.append(f"core/{cand.relative_to(core_root).as_posix()}:0")
    return sorted(found)


def _summarize(gates: dict[str, dict[str, object]], manifest_checks: list[dict[str, object]]) -> dict[str, int]:
    checks = [c for g in gates.values() for c in g["checks"]]  # type: ignore[union-attr]
    statuses = [str(c["status"]) for c in checks]
    return {
        "evaluated": sum(1 for st in statuses if st in {"PASS", "FAIL"}),
        "failed": sum(1 for st in statuses if st not in PASSING_STATUSES)
        + sum(1 for c in manifest_checks if c["status"] != "PASS"),
        "not_applicable": statuses.count("N/A"),
        "passed": statuses.count("PASS"),
        "total": len(statuses),
    }


def _structural_failure_report(
    port_root: Path, report_out: Path | None, code: str, locations: list[str], write_default: bool = True
) -> tuple[dict[str, object], int]:
    """NON_CONFORMANT report for an obstacle that prevents gate evaluation."""
    gates = {
        g: {
            "checks": [
                {
                    "examined": 0,
                    "failure_code": code,
                    "id": f"{g}.0",
                    "locations": locations[:20],
                    "reason": None,
                    "status": "FAIL",
                }
            ],
            "status": "FAIL",
        }
        for g in GATE_ORDER
    }
    manifest_checks = [{"examined": 0, "failure_code": code, "id": "M.0",
                        "locations": locations[:20], "reason": None, "status": "FAIL"}]
    report: dict[str, object] = {
        "canonical_revision": "unknown",
        "deviations": [],
        "gates": gates,
        "manifest_checks": manifest_checks,
        "spec_version": "1",
        "summary": _summarize(gates, manifest_checks),
        "target": "unknown",
        "verdict": "NON_CONFORMANT",
    }
    dest = report_out or ((port_root / "conformance_report.json") if write_default else None)
    if dest is not None and (port_root.is_dir() or report_out is not None):
        common.write_utf8_lf(dest, json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return report, 1


def _manifest_checks(manifest: dict[str, object], devs_legal: bool) -> list[dict[str, object]]:
    """Explicit records for the manifest preconditions (spec version, legal deviations)."""
    version_ok = manifest.get("spec_version") == "1"
    return [
        {"examined": 1, "failure_code": None if version_ok else "MANIFEST_SPEC_VERSION", "id": "M.1",
         "locations": [] if version_ok else ["port_manifest.json:0 (spec_version must be \"1\")"],
         "reason": None, "status": "PASS" if version_ok else "FAIL"},
        {"examined": 1, "failure_code": None if devs_legal else "MANIFEST_DEVIATION_ILLEGAL", "id": "M.2",
         "locations": [] if devs_legal else ["port_manifest.json:0 (only DEV-STUB and DEV-NOFILES are "
                                             "permitted; DEV-NOFILES excludes on-disk skill or page files)"],
         "reason": None, "status": "PASS" if devs_legal else "FAIL"},
    ]


class StructuralFailure(ValueError):
    """An obstacle that prevents gate evaluation (reported as a structured FAIL, not raised to the CLI)."""

    def __init__(self, code: str, locations: list[str]) -> None:
        super().__init__(code)
        self.code = code
        self.locations = locations


def build_context(
    core_root: Path,
    port_root: Path | None = None,
    manifest_path: Path | None = None,
    canonical_only: bool = False,
    user_home: str | None = None,
    denylist_path: Path | None = None,
    port_second: Path | None = None,
    external_export: Path | None = None,
    scratch_base: Path | None = None,
) -> tuple[ConformanceContext, bool]:
    """Load manifest, owned files, page map, and graphs; return (context, deviations legal)."""
    core_root = core_root.resolve()
    eff_port = core_root if canonical_only else (port_root.resolve() if port_root else core_root)
    core_links = _core_symlinks(core_root)
    if core_links:
        raise StructuralFailure("C5_SYMLINK_FORBIDDEN", core_links)
    port_files: list[Path] = []
    symlink_errs: list[str] = []
    path_errs: list[str] = []
    if canonical_only:
        manifest = _synthetic_canonical_manifest(core_root)
    else:
        mpath = manifest_path.resolve() if manifest_path else (eff_port / "port_manifest.json")
        loaded, merr = vpk.load_json(mpath) if mpath.is_file() else (None, "missing")
        if merr or not isinstance(loaded, dict):
            raise StructuralFailure("MANIFEST_MISSING", ["port_manifest.json:0"])
        manifest = loaded
        port_files, symlink_errs, path_errs = resolve_owned_files(eff_port, manifest)
    dev_ids, dev_stub, devs_legal = _parse_deviations(manifest.get("deviations", []))
    if "DEV-NOFILES" in dev_ids and not canonical_only and _dev_nofiles_has_ondisk_trees(eff_port, port_files):
        devs_legal = False
    pm_doc, pm_err = vpk.load_json(core_root / "corpus" / "pdf_page_map.json")
    pm = vpk.PageMap(pm_doc) if (not pm_err and isinstance(pm_doc, dict)) else None
    cg_doc, cg_err = vpk.load_json(core_root / "ontology" / "concept_graph.json")
    ctx = ConformanceContext(
        core_root=core_root,
        port_root=eff_port,
        manifest=manifest,
        canonical_only=canonical_only,
        user_home=common.resolve_user_home(eff_port, user_home),
        denylist_path=denylist_path,
        port_second=port_second.resolve() if port_second else None,
        external_export=external_export.resolve() if external_export else None,
        scratch_base=scratch_base.resolve() if scratch_base else (core_root / "tmp"),
        page_map=pm,
        page_map_doc=pm_doc if isinstance(pm_doc, dict) else None,
        core_graph=cg_doc if (not cg_err and isinstance(cg_doc, dict)) else None,
        port_graph=_load_port_graph(core_root, eff_port, manifest, canonical_only),
        deviation_ids=dev_ids,
        dev_stub=dev_stub,
        port_files=port_files,
        merged_files=[] if canonical_only else merged_paths(manifest),
        symlink_errors=symlink_errs,
        path_errors=path_errs,
    )
    return ctx, devs_legal


def _run_gates(ctx: ConformanceContext) -> tuple[dict[str, dict[str, object]], bool]:
    """Evaluate the six gates in CONFORMANCE_SPEC 5 order; every check runs."""
    evaluators = (
        ("C5", evaluate_gate_c5),
        ("C1", evaluate_gate_c1),
        ("C3", evaluate_gate_c3),
        ("C2", evaluate_gate_c2),
        ("C4", evaluate_gate_c4),
        ("C6", evaluate_gate_c6),
    )
    gates_out: dict[str, dict[str, object]] = {}
    all_ok = True
    for gate_name, fn in evaluators:
        checks: list[CheckOutcome] = fn(ctx)
        gate_ok = all(c.status in PASSING_STATUSES for c in checks)
        all_ok = all_ok and gate_ok
        gates_out[gate_name] = {
            "checks": [c.to_dict() for c in checks],
            "status": "PASS" if gate_ok else "FAIL",
        }
    return gates_out, all_ok


def certify(
    core_root: Path,
    port_root: Path | None = None,
    manifest_path: Path | None = None,
    report_path: Path | None = None,
    canonical_only: bool = False,
    user_home: str | None = None,
    denylist_path: Path | None = None,
    port_second: Path | None = None,
    external_export: Path | None = None,
    scratch_base: Path | None = None,
) -> tuple[dict[str, object], int]:
    """Run all 6 conformance gates in §5 order and return (report_dict, exit_code)."""
    eff_port = core_root.resolve() if (canonical_only or not port_root) else port_root.resolve()
    try:
        ctx, devs_legal = build_context(
            core_root, port_root, manifest_path, canonical_only, user_home,
            denylist_path, port_second, external_export, scratch_base)
    except StructuralFailure as failure:
        return _structural_failure_report(
            eff_port, report_path, failure.code, failure.locations, write_default=not canonical_only)
    manifest = ctx.manifest
    manifest_checks = [] if canonical_only else _manifest_checks(manifest, devs_legal)
    gates_out, gates_ok = _run_gates(ctx)
    if not (gates_ok and all(c["status"] == "PASS" for c in manifest_checks)):
        verdict, code = "NON_CONFORMANT", 1
    elif ctx.deviation_ids:
        verdict, code = "CONFORMANT_WITH_DEVIATIONS", 2
    else:
        verdict, code = "CONFORMANT", 0
    report: dict[str, object] = {
        "spec_version": "1",
        "target": str(manifest.get("target", "unknown")),
        "canonical_revision": str(manifest.get("canonical_revision", "unknown")),
        "manifest_checks": manifest_checks,
        "gates": gates_out,
        "deviations": manifest.get("deviations", []),
        "summary": _summarize(gates_out, manifest_checks),
        "verdict": verdict,
    }
    out_file = report_path or (None if canonical_only else eff_port / "conformance_report.json")
    if out_file is not None:
        common.write_utf8_lf(out_file, json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return report, code


def failed_check_codes(report: dict[str, object]) -> list[str]:
    """'<check id>:<failure code>' for every manifest or gate check that did not pass."""
    failed = [
        f"{chk['id']}:{chk['failure_code']}"
        for chk in report.get("manifest_checks", [])  # type: ignore[union-attr]
        if chk["status"] != "PASS"
    ]
    for g in GATE_ORDER:
        for chk in report["gates"][g]["checks"]:  # type: ignore[index]
            if chk["status"] not in PASSING_STATUSES:
                failed.append(f"{chk['id']}:{chk['failure_code']}")
    return failed


def summary_line(report: dict[str, object]) -> str:
    """One-line verdict with exact evaluated, N/A, and failed counts."""
    counts = report["summary"]  # type: ignore[assignment]
    failed = failed_check_codes(report)
    detail = f"{counts['passed']}/{counts['evaluated']} evaluated checks PASS"  # type: ignore[index]
    if counts["not_applicable"]:  # type: ignore[index]
        detail += f", {counts['not_applicable']} port-only N/A"  # type: ignore[index]
    if failed:
        detail += f"; {len(failed)} failed: " + ", ".join(failed)
    return f"verdict={report['verdict']} target={report['target']} ({detail})"


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Verify PPA port conformance (gates C5, C1, C3, C2, C4, C6)")
    ap.add_argument("--core", "--repo-root", dest="core", default=".",
                    help="canonical repository root (default: .)")
    ap.add_argument("--port", "--port-root", dest="port", default=None,
                    help="compiled port root directory")
    ap.add_argument("--manifest", default=None,
                    help="explicit path to port_manifest.json")
    ap.add_argument("--report", default=None,
                    help="explicit output path for conformance_report.json")
    ap.add_argument("--canonical-only", action="store_true",
                    help="run preflight conformance checks on the canonical core alone")
    ap.add_argument("--user-home", default=None,
                    help="user-scope home directory for '~/' surface checks")
    ap.add_argument("--denylist", default=None,
                    help="operator denylist JSON file for C5.5")
    ap.add_argument("--port-second", default=None,
                    help="second compiled port directory for C5.7 (required when the target "
                         "has no reference adapter)")
    ap.add_argument("--external-export", default=None,
                    help="optional external tracker sync JSON for C6.10")
    ap.add_argument("--scratch-dir", default=None,
                    help="scratch base directory for C5.7 dual-build verification")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(sys.argv[1:] if argv is None else argv)
    if not args.canonical_only and not args.port:
        sys.stderr.write("error: either --port <dir> or --canonical-only is required\n")
        return 1
    report, exit_code = certify(
        core_root=Path(args.core),
        port_root=Path(args.port) if args.port else None,
        manifest_path=Path(args.manifest) if args.manifest else None,
        report_path=Path(args.report) if args.report else None,
        canonical_only=args.canonical_only,
        user_home=args.user_home,
        denylist_path=Path(args.denylist) if args.denylist else None,
        port_second=Path(args.port_second) if args.port_second else None,
        external_export=Path(args.external_export) if args.external_export else None,
        scratch_base=Path(args.scratch_dir) if args.scratch_dir else None,
    )
    print(summary_line(report))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
