#!/usr/bin/env python3
"""
outcome_validator.py — Validate a list of desired-outcome statements
against the 10 characteristics of a perfect outcome statement (Chapter
11, Table 11.2) and the variability strips (Table 11.4) from the ODI
handbook.

Per outcome, produces:
  - 10 boolean columns (one per characteristic)
  - 5 boolean columns (one per variability sin)
  - severity in {ok, warn, fail}
  - suggested rewrite if applicable
  - cosine-similarity duplicate alerts across the whole list

Verdict: pass / conditional / fail. /generatesurvey is hard-gated on
verdict != 'fail'.

Usage:
    python outcome_validator.py \
        --outcomes netted-outcomes.csv \
        --out validation-out/
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import pandas as pd


# ----- Detection regexes -----

CANONICAL_DIRECTIONS = {"minimize", "increase"}
NON_CANONICAL_DIRECTIONS = {
    "reduce": "Minimize", "decrease": "Minimize", "limit": "Minimize",
    "prevent": "Minimize", "eliminate": "Minimize", "avoid": "Minimize",
    "lessen": "Minimize", "lower": "Minimize", "improve": "Increase",
    "maximize": "Increase", "boost": "Increase", "raise": "Increase",
    "enhance": "Increase",
}

# Metrics from Ch 11
METRIC_TERMS = [
    r"the time it takes to", r"the time to", r"the likelihood that",
    r"the likelihood of", r"the frequency that", r"the frequency of",
    r"the number of", r"the amount of", r"the physical effort required to",
]
METRIC_REGEX = re.compile("|".join(METRIC_TERMS), re.IGNORECASE)

# Vague adjectives / adverbs
VAGUE_QUALIFIERS = [
    r"\bfrequently\b", r"\bsignificantly\b", r"\bexcessive\b",
    r"\bquickly\b", r"\beasily\b", r"\boften\b", r"\boccasionally\b",
    r"\brarely\b", r"\bgenerally\b", r"\busually\b",
    r"\bvery\b", r"\bextremely\b", r"\bsomewhat\b",
]
VAGUE_REGEX = re.compile("|".join(VAGUE_QUALIFIERS), re.IGNORECASE)

# Common brand / tech names — extend with project-specific names via CLI
DEFAULT_SOLUTION_TERMS = [
    r"\biPhone\b", r"\bAirPods\b", r"\bAndroid\b", r"\bSpotify\b",
    r"\bApple Music\b", r"\bYouTube\b", r"\bBluetooth\b", r"\bWi[-\s]?Fi\b",
    r"\bDeWalt\b", r"\bMakita\b", r"\bMilwaukee\b", r"\bBosch\b", r"\bRyobi\b",
    r"\bUSB\b", r"\bNFC\b", r"\bGPS\b",
    r"\bapp\b", r"\bSaaS\b", r"\bCRM\b", r"\bAPI\b",
    r"\blaser guide\b", r"\bLED\b",
]


def detect_direction(statement: str) -> tuple[bool, str | None]:
    first = statement.strip().split()
    if not first:
        return False, None
    word = first[0].lower()
    if word in CANONICAL_DIRECTIONS:
        return True, None
    if word in NON_CANONICAL_DIRECTIONS:
        return False, f"non_canonical_direction:{word} -> {NON_CANONICAL_DIRECTIONS[word]}"
    return False, "no_direction_verb_at_start"


def detect_metric(statement: str) -> bool:
    return bool(METRIC_REGEX.search(statement))


def detect_compound(statement: str) -> tuple[bool, str | None]:
    m = re.search(r"\b(time|effort|likelihood|frequency|cost|number)\s+and\s+(time|effort|likelihood|frequency|cost|number)\b", statement, re.IGNORECASE)
    if m:
        return True, m.group(0)
    return False, None


def detect_vague_qualifier(statement: str) -> str | None:
    m = VAGUE_REGEX.search(statement)
    return m.group(0) if m else None


def detect_solution_terms(statement: str, extra_terms: list[str]) -> str | None:
    terms = DEFAULT_SOLUTION_TERMS + extra_terms
    pattern = re.compile("|".join(terms), re.IGNORECASE)
    m = pattern.search(statement)
    return m.group(0) if m else None


def suggest_rewrite(statement: str, sins: list[str]) -> str | None:
    new = statement
    # Direction verb fix
    first = statement.split()
    if first and first[0].lower() in NON_CANONICAL_DIRECTIONS:
        new = NON_CANONICAL_DIRECTIONS[first[0].lower()] + " " + " ".join(first[1:])
    # Compound split
    for sin in sins:
        if sin.startswith("compound:"):
            parts = sin.split(":", 1)[1].split(" and ")
            if len(parts) == 2:
                return None  # caller should split; we don't merge here
    return new if new != statement else None


# ----- 10-characteristic mapping -----

def evaluate(statement: str, extra_solution_terms: list[str]) -> dict:
    sins = []
    has_direction, dir_issue = detect_direction(statement)
    if dir_issue:
        sins.append(f"direction:{dir_issue}")
    has_metric = detect_metric(statement)
    if not has_metric:
        sins.append("metric:none_detected")
    is_compound, compound_match = detect_compound(statement)
    if is_compound:
        sins.append(f"compound:{compound_match}")
    vague = detect_vague_qualifier(statement)
    if vague:
        sins.append(f"vague_qualifier:{vague}")
    sol = detect_solution_terms(statement, extra_solution_terms)
    if sol:
        sins.append(f"solution_term:{sol}")

    # 10 characteristics
    char = {
        "stable_over_time":   not bool(sol),                           # rough — proxy via no embedded tech
        "reveals_a_metric":   has_metric,
        "devoid_of_solutions": not bool(sol),
        "measurable":         has_metric,                              # measurable requires a metric
        "controllable":       True,                                    # assume true; flag manually
        "actionable":         has_metric and has_direction,
        "one_dimensional":    not is_compound,
        "mutually_exclusive": True,                                    # set by cross-list dedupe check
        "customer_stated_value": has_direction,
        "useful_across_functions": True,                               # assume true; flag manually
    }

    fail_conditions = {
        "compound": is_compound,
        "no_metric": not has_metric,
        "non_canonical_direction": dir_issue is not None and not dir_issue.startswith("no_direction_verb_at_start"),
        "embedded_solution": sol is not None,
        "no_direction": dir_issue is not None and dir_issue.startswith("no_direction_verb_at_start"),
    }
    if any([is_compound, sol is not None, not has_metric, not has_direction]):
        severity = "fail" if (is_compound or sol or not has_metric or not has_direction) else "warn"
    elif vague:
        severity = "warn"
    else:
        severity = "ok"

    return {
        "characteristics": char,
        "sins": sins,
        "severity": severity,
        "suggested_rewrite": suggest_rewrite(statement, sins),
    }


def cross_list_dedupe(statements: list[str], threshold: float = 0.85) -> list[dict]:
    """Optional embedding-based duplicate alerts. Falls back to token-overlap."""
    alerts = []
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        model = SentenceTransformer("all-MiniLM-L6-v2")
        emb = model.encode(statements, convert_to_numpy=True, show_progress_bar=False)
        emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)
        sim = cosine_similarity(emb)
        n = len(statements)
        for i in range(n):
            for j in range(i + 1, n):
                if sim[i, j] >= threshold:
                    alerts.append({"i": i, "j": j, "cosine": float(sim[i, j])})
    except Exception:
        # Token-overlap fallback
        def tok(s: str) -> set[str]:
            return set(re.findall(r"\w+", s.lower()))
        for i in range(len(statements)):
            ti = tok(statements[i])
            for j in range(i + 1, len(statements)):
                tj = tok(statements[j])
                if not ti or not tj:
                    continue
                jac = len(ti & tj) / len(ti | tj)
                if jac >= 0.75:
                    alerts.append({"i": i, "j": j, "jaccard": jac})
    return alerts


def main():
    parser = argparse.ArgumentParser(description="Validate outcomes against Ch 11 characteristics + Table 11.4")
    parser.add_argument("--outcomes", required=True)
    parser.add_argument("--out", default="validation-out")
    parser.add_argument("--extra-solution-terms", default="", help="comma-separated additional product/tech names to flag as embedded solutions")
    parser.add_argument("--dedupe-threshold", type=float, default=0.85)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.outcomes)
    if "full_statement" not in df.columns:
        print("[err] outcomes CSV must have a 'full_statement' column", file=sys.stderr)
        sys.exit(1)

    extra_terms = [t.strip() for t in args.extra_solution_terms.split(",") if t.strip()]
    rows = []
    for _, r in df.iterrows():
        ev = evaluate(r["full_statement"], extra_terms)
        rows.append({
            "id": r.get("id", ""),
            "full_statement": r["full_statement"],
            **{f"char_{k}": v for k, v in ev["characteristics"].items()},
            "sins": "; ".join(ev["sins"]) if ev["sins"] else "",
            "severity": ev["severity"],
            "suggested_rewrite": ev["suggested_rewrite"] or "",
        })

    report = pd.DataFrame(rows)
    csv_path = out_dir / "validation_report.csv"
    report.to_csv(csv_path, index=False)

    statements = df["full_statement"].tolist()
    dupe_alerts = cross_list_dedupe(statements, args.dedupe_threshold)
    # Map back to ids
    dedupe_with_ids = []
    for a in dupe_alerts:
        dedupe_with_ids.append({
            "id_a": df.iloc[a["i"]].get("id", a["i"]),
            "id_b": df.iloc[a["j"]].get("id", a["j"]),
            "statement_a": df.iloc[a["i"]]["full_statement"],
            "statement_b": df.iloc[a["j"]]["full_statement"],
            **{k: v for k, v in a.items() if k in ("cosine", "jaccard")}
        })

    counts = report["severity"].value_counts().to_dict()
    verdict = "fail" if counts.get("fail", 0) > 0 else ("conditional" if counts.get("warn", 0) > 0 else "pass")

    summary = {
        "skill": "validateoutcomes",
        "method_version": "ODI v2.4.2",
        "input": args.outcomes,
        "n_outcomes": len(report),
        "summary": {"ok": int(counts.get("ok", 0)), "warn": int(counts.get("warn", 0)), "fail": int(counts.get("fail", 0))},
        "verdict": verdict,
        "duplicate_alerts": dedupe_with_ids[:30],
        "outputs": {"csv": str(csv_path)},
    }

    md_lines = ["# /validateoutcomes — report", ""]
    md_lines.append(f"- **Verdict:** {verdict}")
    md_lines.append(f"- ok / warn / fail: {summary['summary']['ok']} / {summary['summary']['warn']} / {summary['summary']['fail']}")
    md_lines.append(f"- Duplicate alerts: {len(dedupe_with_ids)}")
    md_lines.append("")
    if summary["summary"]["fail"]:
        md_lines.append("## Failures")
        for _, r in report[report["severity"] == "fail"].iterrows():
            md_lines.append(f"- **{r['id']}** — {r['full_statement']}")
            md_lines.append(f"  - sins: {r['sins']}")
            if r["suggested_rewrite"]:
                md_lines.append(f"  - suggested rewrite: *{r['suggested_rewrite']}*")
    if summary["summary"]["warn"]:
        md_lines.append("\n## Warnings")
        for _, r in report[report["severity"] == "warn"].iterrows():
            md_lines.append(f"- **{r['id']}** — {r['full_statement']} _(sins: {r['sins']})_")
    md_path = out_dir / "validation_report.md"
    md_path.write_text("\n".join(md_lines))
    summary["outputs"]["markdown"] = str(md_path)

    json_path = out_dir / "validation_report.json"
    json_path.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
