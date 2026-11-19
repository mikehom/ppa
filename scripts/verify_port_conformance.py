#!/usr/bin/env python3
# @governing: REQ-TECH-PPA-006 @parent: REQ-PRD-PPA-006
# @decision DEC-PPA-009: Reference certification engine for CONFORMANCE_SPEC.md
#   evaluating all 55 checks across C5 -> C1 -> C3 -> C2 -> C4 -> C6 with zero
#   NOT_IMPLEMENTED gates, emitting conformance_report.json, and exiting 0/2/1.
"""Certify a PPA target harness port (or canonical core) against CONFORMANCE_SPEC.md.

Usage:
    python3 -B scripts/verify_port_conformance.py --core . --port <port_root>
        [--manifest <port_root>/port_manifest.json] [--report <out.json>]
    python3 -B scripts/verify_port_conformance.py --core . --canonical-only
"""
from __future__ import annotations

import argparse
import json
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
from ppa_conformance_c34 import (  # noqa: E402
    evaluate_gate_c3,
    evaluate_gate_c4,
)
from ppa_conformance_c6 import (  # noqa: E402
    evaluate_gate_c2,
    evaluate_gate_c6,
)
import validate_ppa_knowledge as vpk  # noqa: E402

GATE_ORDER = ("C5", "C1", "C3", "C2", "C4", "C6")
PERMITTED_DEVIATIONS = {"DEV-STUB", "DEV-NOFILES"}


def _dev_nofiles_has_ondisk_trees(port_root: Path) -> bool:
    """Return True when port_root materializes pages/ or non-core skill/rule Markdown trees."""
    if (port_root / "pages").is_dir():
        return True
    for p in common.sorted_files_under(port_root):
        rel = p.relative_to(port_root).as_posix()
        if rel.startswith("core/"):
            continue
        if p.name == "SKILL.md" or p.suffix == ".mdc":
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
    k_files, o_files, _ = common.collect_canonical_package(core_root)
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
        "canonical_revision": common.resolve_canonical_revision(core_root),
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


def _missing_manifest_report(port_root: Path, report_out: Path | None) -> tuple[dict[str, object], int]:
    gates = {
        g: {
            "checks": [
                {
                    "examined": 0,
                    "failure_code": "MANIFEST_MISSING",
                    "id": f"{g}.0",
                    "locations": ["port_manifest.json:0"],
                    "status": "FAIL",
                }
            ],
            "status": "FAIL",
        }
        for g in GATE_ORDER
    }
    report: dict[str, object] = {
        "canonical_revision": "unknown",
        "deviations": [],
        "gates": gates,
        "spec_version": "1",
        "target": "unknown",
        "verdict": "NON_CONFORMANT",
    }
    dest = report_out or (port_root / "conformance_report.json")
    if port_root.is_dir() or report_out is not None:
        common.write_utf8_lf(dest, json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return report, 1


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
    core_root = core_root.resolve()
    eff_port = core_root if canonical_only else (port_root.resolve() if port_root else core_root)
    if canonical_only:
        manifest = _synthetic_canonical_manifest(core_root)
    else:
        mpath = manifest_path.resolve() if manifest_path else (eff_port / "port_manifest.json")
        if not mpath.is_file():
            return _missing_manifest_report(eff_port, report_path)
        loaded, merr = vpk.load_json(mpath)
        if merr or not isinstance(loaded, dict):
            return _missing_manifest_report(eff_port, report_path)
        manifest = loaded

    dev_ids, dev_stub, devs_legal = _parse_deviations(manifest.get("deviations", []))
    if "DEV-NOFILES" in dev_ids and not canonical_only and _dev_nofiles_has_ondisk_trees(eff_port):
        devs_legal = False
    pm_doc, pm_err = vpk.load_json(core_root / "corpus" / "pdf_page_map.json")
    pm = vpk.PageMap(pm_doc) if (not pm_err and isinstance(pm_doc, dict)) else None
    cg_doc, cg_err = vpk.load_json(core_root / "ontology" / "concept_graph.json")
    core_graph = cg_doc if (not cg_err and isinstance(cg_doc, dict)) else None
    port_graph = _load_port_graph(core_root, eff_port, manifest, canonical_only)
    s_base = scratch_base.resolve() if scratch_base else (core_root / "tmp")

    ctx = ConformanceContext(
        core_root=core_root,
        port_root=eff_port,
        manifest=manifest,
        canonical_only=canonical_only,
        user_home=common.resolve_user_home(eff_port, user_home),
        denylist_path=denylist_path,
        port_second=port_second.resolve() if port_second else None,
        external_export=external_export.resolve() if external_export else None,
        scratch_base=s_base,
        page_map=pm,
        page_map_doc=pm_doc if isinstance(pm_doc, dict) else None,
        core_graph=core_graph,
        port_graph=port_graph,
        deviation_ids=dev_ids,
        dev_stub=dev_stub,
    )

    evaluators = (
        ("C5", evaluate_gate_c5),
        ("C1", evaluate_gate_c1),
        ("C3", evaluate_gate_c3),
        ("C2", evaluate_gate_c2),
        ("C4", evaluate_gate_c4),
        ("C6", evaluate_gate_c6),
    )
    gates_out: dict[str, dict[str, object]] = {}
    all_pass = devs_legal and manifest.get("spec_version") == "1"
    for gate_name, fn in evaluators:
        checks: list[CheckOutcome] = fn(ctx)
        gate_ok = all(c.status == "PASS" for c in checks)
        if not gate_ok:
            all_pass = False
        gates_out[gate_name] = {
            "checks": [c.to_dict() for c in checks],
            "status": "PASS" if gate_ok else "FAIL",
        }

    if not all_pass:
        verdict, code = "NON_CONFORMANT", 1
    elif dev_ids:
        verdict, code = "CONFORMANT_WITH_DEVIATIONS", 2
    else:
        verdict, code = "CONFORMANT", 0

    report: dict[str, object] = {
        "spec_version": "1",
        "target": str(manifest.get("target", "unknown")),
        "canonical_revision": str(manifest.get("canonical_revision", "unknown")),
        "gates": gates_out,
        "deviations": manifest.get("deviations", []),
        "verdict": verdict,
    }
    out_file = report_path or (None if canonical_only else eff_port / "conformance_report.json")
    if out_file is not None:
        common.write_utf8_lf(out_file, json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return report, code


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
                    help="optional second compiled port directory for C5.7 comparison")
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
    failed_codes = [
        f"{chk['id']}:{chk['failure_code']}"
        for g in GATE_ORDER
        for chk in report["gates"][g]["checks"]  # type: ignore[index]
        if chk["status"] != "PASS"
    ]
    summary = ", ".join(failed_codes) if failed_codes else "all 55 checks PASS"
    print(f"verdict={report['verdict']} target={report['target']} ({summary})")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
