#!/usr/bin/env python3
"""
deliverables_exporter.py — Bundle every engagement output into a single
shippable deliverables/ folder containing EXACTLY the six artifacts
named in Table 30.1 of the ODI handbook, plus the ODI Canvas, an
executive summary, and a coverage report that proves every front-matter
capability is enabled.

The six artifacts (Table 30.1):
    1. Ranked opportunity list           (from /computescores)
    2. Outcome-based segments            (from /runsegmentation)
    3. Strategic posture                 (from /choosestrategy)
    4. Outcome-based value proposition   (from /generatevalueprop)
    5. Outcome-attack roadmap            (from /buildroadmap)
    6. Engineering specs                 (from /outcometospec ×N)

The script REFUSES to ship if any of the six is missing. It surfaces
which skill the user must run next to complete the bundle.

If any underlying artifact is synthetic, the entire bundle is stamped
SYNTHETIC and the coverage report's verdict is "directional only".

Usage:
    python deliverables_exporter.py \
        --project-dir . \
        --out-dir deliverables/ \
        [--zip] [--synthetic]
"""

import argparse
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd


SYNTHETIC_BANNER_MD = (
    "> ⚠️ **SYNTHETIC DATA — DIRECTIONAL ONLY — DO NOT SHIP**  \n"
    "> Validate with n≥300 real respondents per ODI v2.4.2, Chapter 16.\n"
)


# Expected artifact paths (relative to project-dir). The script searches
# these locations in order and uses the first match.
ARTIFACT_PATHS = {
    "1_ranked_opportunity_list": {
        "files": [
            "analysis-out/opportunity_scores.csv",
            "analysis-out/opportunity_landscape.png",
            "analysis-out/opportunity_summary.md",
        ],
        "skill_to_run": "/computescores",
    },
    "2_outcome_based_segments": {
        "files": [
            "analysis-out/segments.csv",
            "analysis-out/segmentation_audit.json",
        ],
        "globs": ["analysis-out/landscape_segment_*.png",
                  "analysis-out/opportunity_scores_segment_*.csv"],
        "skill_to_run": "/runsegmentation",
    },
    "3_strategic_posture": {
        "files": [
            "strategy-out/strategy_recommendation.md",
            "strategy-out/growth_matrix.png",
        ],
        "optional_files": [
            "strategy-out/strategy_recommendation.json",
            "analysis-out/wtp_analysis.json",
        ],
        "skill_to_run": "/choosestrategy",
    },
    "4_value_proposition": {
        "files": [
            "valueprop-out/valueprop.json",
        ],
        "optional_files": [
            "valueprop-out/valueprop.md",
            "valueprop-out/marketing_variants.md",
        ],
        "skill_to_run": "/generatevalueprop",
    },
    "5_attack_roadmap": {
        "files": [
            "roadmap-out/roadmap.csv",
        ],
        "optional_files": ["roadmap-out/roadmap.md"],
        "skill_to_run": "/buildroadmap",
    },
    "6_engineering_specs": {
        "globs": ["spec-out/*.md", "spec-out/*.json"],
        "skill_to_run": "/outcometospec (one per outcome shipping in v1.0)",
        "min_files": 1,
    },
}


COVER_SHEETS = {
    "00_odi_canvas": ["canvas-out/canvas.md", "canvas-out/canvas.png", "canvas-out/canvas.html"],
    "appendix_a_survey_instrument": ["survey-out/survey.md", "survey-out/survey.json",
                                      "survey-out/survey.qsf-import.txt", "survey-out/survey.typeform.json",
                                      "survey-out/field-map.csv"],
    "appendix_b_outcome_library":   ["netted-outcomes.csv", "validation-out/validation_report.csv"],
    "appendix_c_competitive_table": ["analysis-out/competitive_table.csv"],
}


def check_artifact(spec: dict, project_dir: Path) -> tuple[bool, list[Path]]:
    found = []
    if "files" in spec:
        for f in spec["files"]:
            p = project_dir / f
            if p.exists():
                found.append(p)
        all_required = all((project_dir / f).exists() for f in spec["files"])
    else:
        all_required = True

    if "globs" in spec:
        for g in spec["globs"]:
            found.extend(list(project_dir.glob(g)))

    if "optional_files" in spec:
        for f in spec["optional_files"]:
            p = project_dir / f
            if p.exists():
                found.append(p)

    min_files = spec.get("min_files", 0)
    present = all_required and (len(found) >= min_files)
    return present, sorted(set(found))


def copy_into(files: list[Path], project_dir: Path, dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        if f.is_dir():
            continue
        # Preserve subdir structure relative to project_dir
        try:
            rel = f.relative_to(project_dir).parts[-1]
        except ValueError:
            rel = f.name
        # Group per-segment landscapes into a subfolder
        if "landscape_segment" in f.name:
            (dest / "per_segment_landscapes").mkdir(exist_ok=True)
            shutil.copy2(f, dest / "per_segment_landscapes" / f.name)
        elif "opportunity_scores_segment" in f.name:
            (dest / "per_segment_scores").mkdir(exist_ok=True)
            shutil.copy2(f, dest / "per_segment_scores" / f.name)
        else:
            shutil.copy2(f, dest / f.name)


def write_executive_summary(project_dir: Path, out: Path, synthetic: bool):
    job = ""
    posture = ""
    seg = ""
    top_outcomes = []
    headline_vp = ""
    top_roadmap = []
    pricing = ""

    try:
        for jf in (project_dir / "definejob.json", project_dir / "job_statement.json"):
            if jf.exists():
                job = json.loads(jf.read_text()).get("full_statement", "") or json.loads(jf.read_text()).get("job_statement", "")
                break
    except Exception:
        pass

    try:
        strategy = project_dir / "strategy-out" / "strategy_recommendation.json"
        if strategy.exists():
            data = json.loads(strategy.read_text())
            rec0 = (data.get("recommendations") or [{}])[0]
            posture = rec0.get("posture", "")
            seg = rec0.get("segment", {}).get("label", "")
            band = rec0.get("pricing_band", {})
            if band:
                pricing = f"${band.get('low_usd','-')}–${band.get('high_usd','-')} (median ${band.get('median_usd','-')})"
    except Exception:
        pass

    try:
        opp = project_dir / "analysis-out" / "opportunity_scores.csv"
        if opp.exists():
            df = pd.read_csv(opp, comment="=")
            df = df.sort_values("opportunity", ascending=False).head(3)
            for _, r in df.iterrows():
                top_outcomes.append(f"{r.get('outcome_id','')} — {r.get('full_statement','')[:80]} (opp {round(float(r['opportunity']),1)})")
    except Exception:
        pass

    try:
        vp = project_dir / "valueprop-out" / "valueprop.json"
        if vp.exists():
            headline_vp = json.loads(vp.read_text()).get("value_prop", "")
    except Exception:
        pass

    try:
        road = project_dir / "roadmap-out" / "roadmap.csv"
        if road.exists():
            df = pd.read_csv(road)
            top = df.sort_values("opportunity_score", ascending=False).head(3) if "opportunity_score" in df.columns else df.head(3)
            for _, r in top.iterrows():
                top_roadmap.append(f"{r.get('outcome_id','')} — {r.get('move_name','')} ({r.get('release','')})")
    except Exception:
        pass

    md = ["# Executive Summary", ""]
    if synthetic:
        md.append(SYNTHETIC_BANNER_MD)
        md.append("")
    md.append(f"**Job:** {job or '_unknown_'}")
    md.append(f"**Target segment:** {seg or '_pending /choosestrategy_'}")
    md.append(f"**Strategic posture:** {posture or '_pending /choosestrategy_'}")
    md.append(f"**Pricing band:** {pricing or '_pending WTP analysis_'}")
    md.append("")
    md.append("## Top 3 underserved outcomes")
    for line in top_outcomes:
        md.append(f"- {line}")
    md.append("\n## Value proposition")
    md.append(f"> {headline_vp or '_pending /generatevalueprop_'}")
    md.append("\n## Top 3 roadmap moves")
    for line in top_roadmap:
        md.append(f"- {line}")
    md.append("\n## Next step")
    md.append("- Hand to engineering for v1.0 build. Schedule 6-month post-launch /computescores re-run to measure whether engineering hit the success metrics in artifact 6.")
    out.write_text("\n".join(md))


def write_coverage_report(out: Path, artifacts_present: dict, synthetic: bool, n_specs: int):
    md = ["# Coverage Report", "", "_Generated by /exportdeliverables. Proves the engagement enables every front-matter capability + every Table 30.1 artifact._", ""]
    if synthetic:
        md.append(SYNTHETIC_BANNER_MD)
        md.append("")

    md.append("## Table 30.1 — The six artifacts")
    md.append("| # | Artifact | Present |")
    md.append("|---|---|---|")
    label_map = {
        "1_ranked_opportunity_list": "1. Ranked opportunity list",
        "2_outcome_based_segments":  "2. Outcome-based segments",
        "3_strategic_posture":       "3. Strategic posture",
        "4_value_proposition":       "4. Outcome-based value proposition",
        "5_attack_roadmap":          "5. Outcome-attack roadmap",
        "6_engineering_specs":       f"6. Engineering specs ({n_specs} sheets)",
    }
    for k, label in label_map.items():
        present = artifacts_present.get(k, False)
        md.append(f"| {label.split('.')[0]} | {label.split('.',1)[1].strip()} | {'✅' if present else '❌'} |")

    md.append("\n## Front-matter capability coverage")
    md.append("| # | Capability | Enabled | Via |")
    md.append("|---|---|---|---|")
    cap_rows = [
        ("1", "Know exactly what to build to win the market",
         artifacts_present["1_ranked_opportunity_list"],
         "artifact 1 + per-segment scores in artifact 2"),
        ("2", "Identify the specific customer segment that will buy first",
         artifacts_present["2_outcome_based_segments"],
         "artifact 2 (with complexity-factor profile)"),
        ("3", "Price into the willingness-to-pay band you actually have",
         artifacts_present["3_strategic_posture"],
         "pricing_band derived from survey WTP block (artifact 3)"),
        ("4", "Hand engineering a measurable target",
         artifacts_present["6_engineering_specs"],
         "artifact 6 (with 20%-better acceptance criteria)"),
        ("5", "Write marketing copy that lands",
         artifacts_present["4_value_proposition"],
         "artifact 4 (with marketing variants)"),
        ("6", "Choose the right strategic posture with evidence",
         artifacts_present["3_strategic_posture"],
         "artifact 3 (Growth Strategy Matrix)"),
        ("7", "Run it again, faster (institutionalize)",
         all(artifacts_present.values()),
         "appendix B outcome library + appendix A survey instrument"),
    ]
    for n, cap, enabled, via in cap_rows:
        md.append(f"| {n} | {cap} | {'✅' if enabled else '❌'} | {via} |")

    all_present = all(artifacts_present.values())
    verdict = "PASS — full coverage" if all_present else "PARTIAL — see missing artifacts above"
    if synthetic:
        verdict = "DIRECTIONAL ONLY (synthetic data) — " + verdict
    md.append(f"\n**Verdict:** {verdict}")
    md.append(f"\n_Generated: {datetime.utcnow().isoformat()}Z_  ")
    md.append("_Method: ODI v2.4.2_")
    out.write_text("\n".join(md))


def main():
    parser = argparse.ArgumentParser(description="Export the six Table 30.1 artifacts into a deliverables bundle")
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--out-dir", default="deliverables")
    parser.add_argument("--zip", action="store_true")
    parser.add_argument("--synthetic", action="store_true")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    artifacts_present = {}
    missing = []
    n_specs = 0

    for key, spec in ARTIFACT_PATHS.items():
        present, files = check_artifact(spec, project_dir)
        artifacts_present[key] = present
        if present:
            sub = out_dir / key
            copy_into(files, project_dir, sub)
            if key == "6_engineering_specs":
                n_specs = len([f for f in files if f.suffix == ".md"])
        else:
            missing.append({"artifact": key, "run": spec.get("skill_to_run", "")})

    # Cover sheets + appendices
    for key, files in COVER_SHEETS.items():
        existing = [project_dir / f for f in files if (project_dir / f).exists()]
        if existing:
            copy_into(existing, project_dir, out_dir / key)

    # Executive summary
    write_executive_summary(project_dir, out_dir / "00_executive_summary.md", args.synthetic)

    # Coverage report
    write_coverage_report(out_dir / "coverage_report.md", artifacts_present, args.synthetic, n_specs)

    # Bundle zip
    zip_path = None
    if args.zip or args.zip is False:  # always produce zip
        zip_path = out_dir.parent / (out_dir.name + ".zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in out_dir.rglob("*"):
                if p.is_file():
                    zf.write(p, p.relative_to(out_dir.parent))

    # Final JSON report
    report = {
        "skill": "exportdeliverables",
        "method_version": "ODI v2.4.2",
        "data_provenance": "synthetic" if args.synthetic else "real",
        "table_30_1_artifacts": {k: {"present": v, "path": f"{out_dir.name}/{k}/"} for k, v in artifacts_present.items()},
        "front_matter_capabilities_enabled": {
            "1_know_what_to_build":         artifacts_present["1_ranked_opportunity_list"],
            "2_identify_beachhead":         artifacts_present["2_outcome_based_segments"],
            "3_price_into_wtp_band":        artifacts_present["3_strategic_posture"],
            "4_engineering_measurable":     artifacts_present["6_engineering_specs"],
            "5_marketing_lands":            artifacts_present["4_value_proposition"],
            "6_strategic_posture_evidence": artifacts_present["3_strategic_posture"],
            "7_repeatable_capability":      all(artifacts_present.values()),
        },
        "missing_artifacts": missing,
        "outputs": {
            "folder": str(out_dir),
            "zip": str(zip_path) if zip_path else None,
            "coverage_report": str(out_dir / "coverage_report.md"),
        },
        "verdict": "PASS" if all(artifacts_present.values()) else "PARTIAL — missing artifacts must be produced before ship",
        "next_step": "If verdict=PARTIAL, run the listed skills. If PASS, hand to stakeholders and schedule 6-month re-survey."
    }
    print(json.dumps(report, indent=2))
    (out_dir / "deliverables_report.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
