#!/usr/bin/env python3
"""
survey_generator.py — Build a full ODI survey instrument from a netted
outcomes CSV. Emits four artifacts:

    survey-out/survey.md            (human-readable, for review)
    survey-out/survey.json          (machine schema — the source of truth)
    survey-out/survey.qsf-import.txt (Qualtrics Advanced Import format)
    survey-out/survey.typeform.json (Typeform import)
    survey-out/field-map.csv        (maps every item back to source outcome id)

Implements Chapter 15, 16, 17, 18 + Template 4 of ODI v2.4.2.

Usage:
    python survey_generator.py \
        --job "Listen to music while on the go" \
        --outcomes netted-outcomes.csv \
        --complexity-factors complexity-factors.json \
        --competitors "Spotify,Apple Music,YouTube Music" \
        --wtp \
        --out-dir survey-out/
"""

import argparse
import json
from pathlib import Path

import pandas as pd


JOB_STEPS_ORDER = ["Define", "Locate", "Prepare", "Confirm", "Execute", "Monitor", "Modify", "Conclude"]


def screener(job: str, audience_desc: str | None) -> list[dict]:
    return [
        {"id": "SC1", "text": f"In the past 3 months, how often have you {job}?",
         "type": "single_select",
         "options": ["Multiple times a week", "Weekly", "Monthly", "Less than monthly", "Never"],
         "disqualify_if": ["Never"]},
        {"id": "SC2", "text": "Which of the following do you currently use most often to do this?",
         "type": "single_select",
         "options": ["Option A", "Option B", "Option C", "None of the above"],
         "disqualify_if": ["None of the above"],
         "note": "Replace options with the real category solutions."},
        {"id": "SC3", "text": "Are you employed in market research, advertising, or by any of the following companies? [list competitors]",
         "type": "yes_no",
         "disqualify_if": ["Yes"]},
        {"id": "SC4", "text": "To confirm you are reading carefully, please select 4.",
         "type": "scale_1_5",
         "attention_check_value": 4},
    ]


def profiling(factors: list[dict]) -> list[dict]:
    out = []
    for i, f in enumerate(factors[:15], start=1):
        out.append({
            "id": f"PR{i}",
            "factor_name": f["name"],
            "text": f["question"],
            "type": f.get("type", "open_numeric"),
            "scale": f.get("scale", ""),
            "source": "complexity_factor",
        })
    # Always also collect a small demographic block
    out.extend([
        {"id": "DEM1", "text": "What is your age?", "type": "open_numeric", "source": "demographic"},
        {"id": "DEM2", "text": "What country do you live in?", "type": "country_select", "source": "demographic"},
        {"id": "DEM3", "text": "What is your role / occupation?", "type": "open_text", "source": "demographic"},
    ])
    return out


def importance_block(outcomes: pd.DataFrame, job: str) -> list[dict]:
    """One matrix per job step, 8–12 rows per matrix."""
    out = []
    grouped = outcomes.groupby("job_step", sort=False)
    for step in JOB_STEPS_ORDER:
        if step not in grouped.groups:
            continue
        rows = grouped.get_group(step)
        chunks = [rows.iloc[i:i + 12] for i in range(0, len(rows), 12)]
        for ci, chunk in enumerate(chunks):
            matrix = {
                "id": f"IMP_{step}_{ci+1}",
                "section": "importance",
                "job_step": step,
                "prompt": f"When you {job.lower()}, how important is it to you that you can…",
                "type": "matrix_1_5",
                "scale_anchors": {1: "Not important at all", 5: "Extremely important"},
                "rows": [
                    {"item_id": f"imp_{r['id']}", "outcome_id": r["id"], "text": r["full_statement"]}
                    for _, r in chunk.iterrows()
                ],
            }
            out.append(matrix)
    return out


def satisfaction_block(outcomes: pd.DataFrame) -> list[dict]:
    out = []
    grouped = outcomes.groupby("job_step", sort=False)
    for step in JOB_STEPS_ORDER:
        if step not in grouped.groups:
            continue
        rows = grouped.get_group(step)
        chunks = [rows.iloc[i:i + 12] for i in range(0, len(rows), 12)]
        for ci, chunk in enumerate(chunks):
            matrix = {
                "id": f"SAT_{step}_{ci+1}",
                "section": "satisfaction",
                "job_step": step,
                "prompt": "How satisfied are you with how the [product/category] you currently use addresses each of the following?",
                "type": "matrix_1_5",
                "scale_anchors": {1: "Not at all satisfied", 5: "Completely satisfied"},
                "rows": [
                    {"item_id": f"sat_{r['id']}", "outcome_id": r["id"], "text": r["full_statement"]}
                    for _, r in chunk.iterrows()
                ],
            }
            out.append(matrix)
    return out


def competitive_block(outcomes: pd.DataFrame, competitors: list[str]) -> list[dict]:
    """One satisfaction matrix per the ONE competitor the respondent picked in SC2 (skip-logic).

    Implementation: emit one block per competitor with a skip rule
    `show_if SC2 == "<competitor>"`.
    """
    out = []
    for comp in competitors:
        for _, chunk_start in [(s, i) for s in JOB_STEPS_ORDER for i in []]:
            pass
        grouped = outcomes.groupby("job_step", sort=False)
        for step in JOB_STEPS_ORDER:
            if step not in grouped.groups:
                continue
            rows = grouped.get_group(step)
            chunks = [rows.iloc[i:i + 12] for i in range(0, len(rows), 12)]
            for ci, chunk in enumerate(chunks):
                matrix = {
                    "id": f"COMPSAT_{comp.replace(' ', '_')}_{step}_{ci+1}",
                    "section": "competitive_satisfaction",
                    "competitor": comp,
                    "job_step": step,
                    "prompt": f"How satisfied are you with {comp} specifically on each of the following?",
                    "show_if": f"SC2 == '{comp}'",
                    "type": "matrix_1_5",
                    "scale_anchors": {1: "Not at all satisfied", 5: "Completely satisfied"},
                    "rows": [
                        {"item_id": f"sat_{comp.replace(' ', '_')}_{r['id']}", "outcome_id": r["id"], "text": r["full_statement"]}
                        for _, r in chunk.iterrows()
                    ],
                }
                out.append(matrix)
    return out


def wtp_block() -> list[dict]:
    return [
        {"id": "WTP1", "text": "How much (in $) would you be willing to pay for a solution that fully satisfies the outcomes most important to you?", "type": "open_numeric"},
        {"id": "WTP2", "text": "What is the highest price (in $) you would still consider acceptable?", "type": "open_numeric"},
        {"id": "WTP3", "text": "At that price, how likely are you to purchase such a solution?", "type": "scale_1_5",
         "scale_anchors": {1: "Not at all likely", 5: "Extremely likely"}},
    ]


def estimate_length_minutes(survey_json: dict) -> int:
    items = 0
    for matrix in survey_json["sections"]["importance"] + survey_json["sections"]["satisfaction"]:
        items += len(matrix["rows"])
    for matrix in survey_json["sections"].get("competitive_satisfaction", []):
        items += len(matrix["rows"]) * 0.4  # not every respondent rates every competitor block
    items += len(survey_json["sections"]["profiling"])
    return int(items * 0.18) + 3  # rough: ~10 sec/item + setup overhead


def to_markdown(survey: dict) -> str:
    md = []
    md.append(f"# Survey — {survey['job_statement']}\n")
    md.append(f"_Generated by ODI v2.4.2 survey generator. Estimated length: {survey['length_estimate_min']} minutes._\n")
    for section_name in ["screener", "profiling", "importance", "satisfaction", "competitive_satisfaction", "wtp"]:
        items = survey["sections"].get(section_name)
        if not items:
            continue
        md.append(f"\n## Section — {section_name.replace('_', ' ').title()}\n")
        for item in items:
            if isinstance(item, dict) and item.get("type", "").startswith("matrix"):
                md.append(f"### {item['id']} — {item.get('job_step','')}")
                md.append(f"> {item['prompt']}\n")
                if "scale_anchors" in item:
                    md.append(f"Scale: 1 ({item['scale_anchors'][1]}) — 5 ({item['scale_anchors'][5]})\n")
                for row in item["rows"]:
                    md.append(f"- **{row['outcome_id']}** — {row['text']}")
                md.append("")
            else:
                md.append(f"- **{item['id']}** ({item.get('type','')}): {item['text']}")
                if "options" in item:
                    for o in item["options"]:
                        md.append(f"  - [ ] {o}")
                md.append("")
    return "\n".join(md)


def to_qualtrics_txt(survey: dict) -> str:
    """Qualtrics Advanced Import — simple TXT format."""
    lines = ["[[AdvancedFormat]]"]
    for section_name in ["screener", "profiling", "importance", "satisfaction", "competitive_satisfaction", "wtp"]:
        items = survey["sections"].get(section_name)
        if not items:
            continue
        lines.append(f"\n[[Block:{section_name}]]\n")
        for item in items:
            lines.append(f"[[Question:{ 'Matrix' if 'matrix' in item.get('type','') else 'MC' }]]")
            lines.append(f"[[ID:{item['id']}]]")
            if "prompt" in item:
                lines.append(item["prompt"])
            elif "text" in item:
                lines.append(item["text"])
            if item.get("type", "").startswith("matrix"):
                lines.append("[[Choices]]")
                for row in item["rows"]:
                    lines.append(row["text"])
                lines.append("[[Answers]]")
                for v, label in item["scale_anchors"].items():
                    lines.append(f"{v} - {label}")
            elif "options" in item:
                lines.append("[[Choices]]")
                for o in item["options"]:
                    lines.append(o)
            lines.append("")
    return "\n".join(lines)


def to_typeform_json(survey: dict) -> dict:
    fields = []
    for section_name in ["screener", "profiling", "importance", "satisfaction", "competitive_satisfaction", "wtp"]:
        items = survey["sections"].get(section_name)
        if not items:
            continue
        for item in items:
            if item.get("type", "").startswith("matrix"):
                for row in item["rows"]:
                    fields.append({
                        "ref": row["item_id"],
                        "title": f"{item['prompt']} … {row['text']}",
                        "type": "opinion_scale",
                        "properties": {"steps": 5, "labels": item["scale_anchors"]},
                    })
            elif item.get("type") == "single_select":
                fields.append({"ref": item["id"], "title": item["text"], "type": "multiple_choice",
                               "properties": {"choices": [{"label": o} for o in item["options"]]}})
            else:
                fields.append({"ref": item["id"], "title": item["text"], "type": "short_text"})
    return {"title": f"ODI Survey — {survey['job_statement']}", "fields": fields}


def field_map(survey: dict) -> pd.DataFrame:
    rows = []
    for section_name, items in survey["sections"].items():
        if not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict) and item.get("type", "").startswith("matrix"):
                for row in item["rows"]:
                    rows.append({
                        "item_id": row["item_id"],
                        "outcome_id": row["outcome_id"],
                        "section": section_name,
                        "job_step": item.get("job_step", ""),
                        "competitor": item.get("competitor", ""),
                    })
            else:
                rows.append({"item_id": item["id"], "outcome_id": "", "section": section_name, "job_step": "", "competitor": ""})
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="ODI survey generator")
    parser.add_argument("--job",        required=True)
    parser.add_argument("--outcomes",   required=True)
    parser.add_argument("--complexity-factors", default="", help="path to JSON with list of complexity factors")
    parser.add_argument("--competitors", default="", help="comma-separated competitor names")
    parser.add_argument("--wtp", action="store_true")
    parser.add_argument("--out-dir", default="survey-out")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    outcomes = pd.read_csv(args.outcomes)
    factors = json.load(open(args.complexity_factors)) if args.complexity_factors else []
    competitors = [c.strip() for c in args.competitors.split(",") if c.strip()]

    survey = {
        "job_statement": args.job,
        "method_version": "ODI v2.4.2",
        "sections": {
            "screener":     screener(args.job, None),
            "profiling":    profiling(factors),
            "importance":   importance_block(outcomes, args.job),
            "satisfaction": satisfaction_block(outcomes),
        },
    }
    if competitors:
        survey["sections"]["competitive_satisfaction"] = competitive_block(outcomes, competitors)
    if args.wtp:
        survey["sections"]["wtp"] = wtp_block()

    survey["length_estimate_min"] = estimate_length_minutes(survey)

    (out_dir / "survey.json").write_text(json.dumps(survey, indent=2))
    (out_dir / "survey.md").write_text(to_markdown(survey))
    (out_dir / "survey.qsf-import.txt").write_text(to_qualtrics_txt(survey))
    (out_dir / "survey.typeform.json").write_text(json.dumps(to_typeform_json(survey), indent=2))
    field_map(survey).to_csv(out_dir / "field-map.csv", index=False)

    print(f"[ok] survey.json — {survey['length_estimate_min']} min estimated")
    print(f"[ok] survey.md / .qsf-import.txt / .typeform.json")
    print(f"[ok] field-map.csv")


if __name__ == "__main__":
    main()
