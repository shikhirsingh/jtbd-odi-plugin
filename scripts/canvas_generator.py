#!/usr/bin/env python3
"""
canvas_generator.py — Render the unified ODI Canvas (the 9-cell one-pager)
to markdown, HTML, and PNG.

Cells (each footnoted to source artifact):
    1. Job statement                (Ch 6)
    2. Target segment + complexity   (Ch 21)
    3. Job map (8 steps)             (Ch 7)
    4. Top 7 underserved outcomes    (Ch 19)
    5. Strategic posture             (Ch 23-24)
    6. Outcome-based value prop      (Ch 25)
    7. Top 5 product moves           (Ch 27)
    8. WTP band + price posture      (Ch 26)
    9. Engineering acceptance        (Ch 28)

Inputs are paths (or skipped placeholders) to the individual artifact
files. Any synthetic artifact triggers a SYNTHETIC banner on the canvas.

Usage:
    python canvas_generator.py \
        --job-json definejob.json \
        --jobmap-json buildjobmap.json \
        --opportunity-csv analysis-out/opportunity_scores.csv \
        --segments-json analysis-out/segmentation_audit.json \
        --strategy-json strategy-out/strategy_recommendation.json \
        --valueprop-json valueprop-out/valueprop.json \
        --roadmap-csv roadmap-out/roadmap.csv \
        --wtp-json analysis-out/wtp_analysis.json \
        --specs-dir spec-out/ \
        --target-segment A \
        --out-dir canvas-out/ \
        [--synthetic]
"""

import argparse
import json
from pathlib import Path

import pandas as pd


SYNTHETIC_BANNER_MD = (
    "> ⚠️ **SYNTHETIC DATA — DIRECTIONAL ONLY — DO NOT SHIP**  \n"
    "> This canvas was rendered from LLM-simulated respondents. "
    "Validate with n≥300 real respondents per ODI v2.4.2, Chapter 16, "
    "before any decision.\n"
)


def safe_load_json(path: str | None) -> dict | None:
    if not path or not Path(path).exists():
        return None
    try:
        text = Path(path).read_text()
        # Strip leading comment-banner lines for tolerated SYNTHETIC headers
        lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith(("//", "#"))]
        return json.loads("\n".join(lines))
    except Exception:
        return None


def safe_load_csv(path: str | None) -> pd.DataFrame | None:
    if not path or not Path(path).exists():
        return None
    try:
        # Skip leading banner lines that start with '='
        with open(path) as f:
            lines = f.readlines()
        skip = 0
        while skip < len(lines) and (lines[skip].startswith("=") or lines[skip].startswith("WARNING") or lines[skip].startswith("#")):
            skip += 1
        return pd.read_csv(path, skiprows=skip)
    except Exception:
        try:
            return pd.read_csv(path)
        except Exception:
            return None


def render_markdown(cells: dict, synthetic: bool) -> str:
    md = []
    if synthetic:
        md.append(SYNTHETIC_BANNER_MD)
    md.append("# ODI Canvas — One-Page Engagement Summary")
    md.append("*Method: Outcome-Driven Innovation, v2.4.2 (Strategyn / Ulwick lineage)*\n")

    # Cell 1 + 2 — two columns
    md.append("## 1. Job statement & 2. Target segment\n")
    md.append("| Job (Ch 6) | Target segment (Ch 21) |")
    md.append("|---|---|")
    md.append(f"| **{cells['1'].get('value', '_pending /definejob_')}** | **{cells['2'].get('label', '_pending /runsegmentation + /choosestrategy_')}** |")
    if cells["2"].get("complexity_profile"):
        cf = ", ".join(cells["2"]["complexity_profile"])
        md.append(f"| _{cells['1'].get('source','')}_ | _Size: {cells['2'].get('size_pct', '–')*100 if isinstance(cells['2'].get('size_pct'), (int,float)) else '–'}%_ — complexity: {cf} |")

    # Cell 3 — job map
    md.append("\n## 3. Job map — 8 steps in ideal sequence (Ch 7)")
    steps = cells["3"].get("steps", [])
    if steps:
        md.append("\n| # | Phase | Step |")
        md.append("|---|---|---|")
        for s in steps:
            md.append(f"| {s.get('step','')} | {s.get('phase','')} | {s.get('statement','')} |")
    else:
        md.append("_pending /buildjobmap_")

    # Cell 4 — top underserved outcomes
    md.append("\n## 4. Top underserved outcomes (Ch 19)")
    top = cells["4"].get("rows", [])
    if top:
        md.append("\n| ID | Outcome | Opp | Class |")
        md.append("|---|---|---|---|")
        for r in top:
            md.append(f"| {r.get('id','')} | {r.get('statement','')} | {r.get('opp','')} | {r.get('class','')} |")
    else:
        md.append("_pending /computescores_")

    # Cell 5 — strategic posture
    md.append("\n## 5. Strategic posture (Ch 23–24)")
    md.append(f"**{cells['5'].get('value', '_pending /choosestrategy_')}**  ")
    if cells["5"].get("reason"):
        md.append(f"_{cells['5']['reason']}_")

    # Cell 6 — value prop
    md.append("\n## 6. Outcome-based value proposition (Ch 25)")
    md.append(f"> {cells['6'].get('value', '_pending /generatevalueprop_')}")

    # Cell 7 — top product moves
    md.append("\n## 7. Top product moves (Ch 27)")
    moves = cells["7"].get("rows", [])
    if moves:
        md.append("\n| Outcome | Opp | Move | Release | Mechanism |")
        md.append("|---|---|---|---|---|")
        for r in moves:
            md.append(f"| {r.get('outcome_id','')} | {r.get('opportunity_score','')} | {r.get('move_name','')} | {r.get('release','')} | {r.get('mechanism','')} |")
    else:
        md.append("_pending /buildroadmap_")

    # Cell 8 — WTP band
    md.append("\n## 8. WTP band & pricing posture (Ch 26)")
    wtp = cells["8"]
    if wtp.get("median") is not None:
        md.append(f"- p25–p75 (USD): **${wtp.get('p25','-')}–${wtp.get('p75','-')}**  ")
        md.append(f"- Median: **${wtp.get('median','-')}**, p90: **${wtp.get('p90','-')}**")
    else:
        md.append("_pending — survey did not include a WTP block; re-field with /generatesurvey --wtp_")

    # Cell 9 — engineering acceptance
    md.append("\n## 9. Engineering acceptance criteria (Ch 28)")
    specs = cells["9"].get("rows", [])
    if specs:
        md.append("\n| Outcome | Acceptance threshold | Baseline | Best competitor | Target (20% better) |")
        md.append("|---|---|---|---|---|")
        for s in specs:
            md.append(f"| {s.get('outcome_id','')} | {s.get('threshold','')} | {s.get('baseline','')} | {s.get('best_competitor','')} | {s.get('target_20pct','')} |")
    else:
        md.append("_pending /outcometospec for top outcomes_")

    if synthetic:
        md.append("\n---\n" + SYNTHETIC_BANNER_MD)
    return "\n".join(md)


def render_html(md: str) -> str:
    try:
        import markdown
        body = markdown.markdown(md, extensions=["tables"])
    except ImportError:
        body = "<pre>" + md + "</pre>"
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>ODI Canvas</title><style>body{{font-family:sans-serif;max-width:900px;margin:2em auto;padding:1em;}}table{{border-collapse:collapse;width:100%;}}th,td{{border:1px solid #ccc;padding:6px 10px;}}h1,h2{{color:#222;}}blockquote{{background:#fff8e1;border-left:4px solid #b22234;padding:8px;}}</style></head><body>{body}</body></html>"


def render_png(md: str, out_path: Path, synthetic: bool):
    """Render the canvas to a PNG via matplotlib as a fallback (not pretty;
    if the user has wkhtmltopdf or playwright they should pipe HTML there)."""
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(11, 17))
        ax.axis("off")
        ax.text(0.02, 0.98, md, ha="left", va="top", fontsize=8, family="monospace", wrap=True)
        if synthetic:
            ax.text(0.5, 0.5, "SYNTHETIC", transform=ax.transAxes, fontsize=120, color="#b22234",
                    alpha=0.10, ha="center", va="center", rotation=30, weight="bold")
        fig.tight_layout()
        fig.savefig(out_path, dpi=120)
        plt.close(fig)
    except Exception as e:
        print(f"[warn] could not render PNG: {e}")


def build_cells(args) -> dict:
    job = safe_load_json(args.job_json) or {}
    jobmap = safe_load_json(args.jobmap_json) or {}
    seg_audit = safe_load_json(args.segments_json) or {}
    strategy = safe_load_json(args.strategy_json) or {}
    valueprop = safe_load_json(args.valueprop_json) or {}
    roadmap = safe_load_csv(args.roadmap_csv)
    wtp = safe_load_json(args.wtp_json) or {}
    opp_csv = safe_load_csv(args.opportunity_csv)

    # Cell 1
    job_statement = job.get("full_statement") or job.get("job_statement") or ""

    # Cell 2 — target segment
    target_seg = args.target_segment or ""
    seg_label, seg_size, seg_cf = "", None, []
    if seg_audit.get("segments") and target_seg in seg_audit["segments"]:
        s = seg_audit["segments"][target_seg]
        seg_label = s.get("label", target_seg) if isinstance(s, dict) else target_seg
        seg_size = s.get("size_pct") if isinstance(s, dict) else None
        if isinstance(s, dict) and s.get("complexity_factor_profile"):
            seg_cf = list(s["complexity_factor_profile"].keys())[:3]

    # Cell 3 — job map
    steps = jobmap.get("job_map", [])

    # Cell 4 — top 7 underserved (segment-specific if seg landscape exists)
    top_outcomes = []
    seg_specific_csv = Path(args.opportunity_csv).parent / f"opportunity_scores_segment_{target_seg}.csv" if args.opportunity_csv and target_seg else None
    src_csv = opp_csv
    if seg_specific_csv and seg_specific_csv.exists():
        src_csv = safe_load_csv(str(seg_specific_csv))
    if src_csv is not None:
        # find top by opportunity
        opp_col = next((c for c in src_csv.columns if c.lower() in ("opportunity", "opp")), None)
        cls_col = next((c for c in src_csv.columns if "classif" in c.lower()), None)
        stmt_col = next((c for c in src_csv.columns if c.lower() in ("full_statement", "statement", "outcome")), None)
        id_col = next((c for c in src_csv.columns if c.lower() in ("outcome_id", "id")), None)
        if opp_col:
            top_df = src_csv.sort_values(opp_col, ascending=False).head(7)
            for _, r in top_df.iterrows():
                top_outcomes.append({
                    "id": r.get(id_col, ""),
                    "statement": (r.get(stmt_col, "") or "")[:120],
                    "opp": round(float(r.get(opp_col, 0)), 1),
                    "class": r.get(cls_col, "") if cls_col else "",
                })

    # Cell 5 — strategic posture
    posture, posture_reason = "", ""
    if strategy.get("recommendations"):
        for rec in strategy["recommendations"]:
            seg = rec.get("segment", {})
            if not target_seg or seg.get("id") == target_seg:
                posture = rec.get("posture", "")
                dj = rec.get("data_justification", {})
                posture_reason = "; ".join(f"{k}: {v}" for k, v in dj.items())
                break

    # Cell 6 — value prop
    vp_value = valueprop.get("value_prop") or ""

    # Cell 7 — top 5 product moves
    moves = []
    if roadmap is not None and not roadmap.empty:
        sorted_road = roadmap.sort_values(roadmap.columns[1] if "opportunity_score" in roadmap.columns else roadmap.columns[0], ascending=False) if "opportunity_score" in roadmap.columns else roadmap
        for _, r in sorted_road.head(5).iterrows():
            moves.append({
                "outcome_id": r.get("outcome_id", ""),
                "opportunity_score": r.get("opportunity_score", ""),
                "move_name": r.get("move_name", ""),
                "release": r.get("release", ""),
                "mechanism": (r.get("mechanism", "") or "")[:80],
            })

    # Cell 8 — WTP band
    wtp_band = {}
    if wtp.get("present"):
        target_band = (wtp.get("per_segment", {}) or {}).get(target_seg) or wtp.get("overall", {})
        wtp_band = {k: round(v, 0) if isinstance(v, float) else v for k, v in target_band.items()}

    # Cell 9 — engineering specs
    spec_rows = []
    if args.specs_dir and Path(args.specs_dir).exists():
        for p in sorted(Path(args.specs_dir).glob("*.json")):
            try:
                s = json.loads(p.read_text())
                spec = s.get("spec", {})
                ac = spec.get("acceptance_criteria", {})
                spec_rows.append({
                    "outcome_id": s.get("outcome_id", p.stem),
                    "threshold": (ac.get("criteria", [""])[0] if ac.get("criteria") else "")[:60],
                    "baseline": ac.get("baseline_current_product", ""),
                    "best_competitor": ac.get("best_competitor", ""),
                    "target_20pct": ac.get("target", ""),
                })
                if len(spec_rows) >= 3:
                    break
            except Exception:
                continue

    return {
        "1": {"value": job_statement, "source": args.job_json or ""},
        "2": {"id": target_seg, "label": seg_label, "size_pct": seg_size, "complexity_profile": seg_cf},
        "3": {"steps": steps},
        "4": {"rows": top_outcomes},
        "5": {"value": posture, "reason": posture_reason},
        "6": {"value": vp_value},
        "7": {"rows": moves},
        "8": wtp_band if wtp_band else {},
        "9": {"rows": spec_rows},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-json")
    parser.add_argument("--jobmap-json")
    parser.add_argument("--opportunity-csv")
    parser.add_argument("--segments-json")
    parser.add_argument("--strategy-json")
    parser.add_argument("--valueprop-json")
    parser.add_argument("--roadmap-csv")
    parser.add_argument("--wtp-json")
    parser.add_argument("--specs-dir")
    parser.add_argument("--target-segment", default="")
    parser.add_argument("--out-dir", default="canvas-out")
    parser.add_argument("--synthetic", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cells = build_cells(args)

    missing = []
    if not cells["1"].get("value"): missing.append("1_job_statement")
    if not cells["3"].get("steps"): missing.append("3_job_map")
    if not cells["4"].get("rows"):  missing.append("4_top_outcomes")
    if not cells["6"].get("value"): missing.append("6_value_prop")

    md = render_markdown(cells, synthetic=args.synthetic)
    md_path = out_dir / "canvas.md"
    md_path.write_text(md)
    html_path = out_dir / "canvas.html"
    html_path.write_text(render_html(md))
    png_path = out_dir / "canvas.png"
    render_png(md, png_path, args.synthetic)
    json_path = out_dir / "canvas.json"
    json_path.write_text(json.dumps({
        "method_version": "ODI v2.4.2",
        "data_provenance": "synthetic" if args.synthetic else "real",
        "cells": cells,
        "missing_cells": missing,
        "outputs": {"markdown": str(md_path), "html": str(html_path), "png": str(png_path)},
    }, indent=2))

    print(f"[ok] {md_path}")
    print(f"[ok] {html_path}")
    print(f"[ok] {png_path}")
    print(f"[ok] {json_path}")
    if missing:
        print(f"[warn] missing canvas cells: {missing}")


if __name__ == "__main__":
    main()
