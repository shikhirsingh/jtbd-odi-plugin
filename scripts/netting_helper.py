#!/usr/bin/env python3
"""
netting_helper.py — Embedding-based first-pass dedupe + compound-statement
detector for the /netoutcomes skill (Chapter 14). Used when the raw set
exceeds ~500 candidates and the LLM-only netting becomes slow.

Returns:
    - clusters of likely-duplicate raw candidates (cosine >= threshold)
    - per-cluster "canonical-statement" pick recommendation (shortest with
      the strongest direction-verb and metric — heuristic; human reviews)
    - compound-statement flags (substring ' and ' between two nouns)
    - direction-verb canonicalization suggestions (reduce -> Minimize, etc.)

This script does NOT make final decisions. The LLM + human review every
cluster before locking the netted list.

Usage:
    python netting_helper.py \
        --raw raw-outcomes.csv \
        --out clusters.json \
        [--threshold 0.82] [--model all-MiniLM-L6-v2]
"""

import argparse
import json
import re
from pathlib import Path

import pandas as pd


NON_CANONICAL_DIRECTION_VERBS = {
    "reduce": "Minimize",
    "decrease": "Minimize",
    "limit": "Minimize",
    "prevent": "Minimize",
    "eliminate": "Minimize",
    "avoid": "Minimize",
    "lessen": "Minimize",
    "lower": "Minimize",
    "improve": "Increase",
    "maximize": "Increase",
    "boost": "Increase",
    "raise": "Increase",
    "enhance": "Increase",
}


def flag_direction_verb(statement: str) -> dict | None:
    first = statement.strip().split()[0].lower() if statement.strip() else ""
    if first in NON_CANONICAL_DIRECTION_VERBS:
        return {"sin": "non_canonical_direction", "offending": first,
                "suggestion_replace_with": NON_CANONICAL_DIRECTION_VERBS[first]}
    return None


def flag_compound(statement: str) -> dict | None:
    # Look for "<noun> and <noun>" pattern between the metric and the verb.
    # Heuristic: "time and effort", "time and likelihood", "X and Y" with both flagged as nouns.
    m = re.search(r"\b(time|effort|likelihood|frequency|cost|number)\s+and\s+(time|effort|likelihood|frequency|cost|number)\b", statement, re.IGNORECASE)
    if m:
        return {"sin": "compound_statement", "offending": m.group(0),
                "suggestion": f"Split into two outcomes — one for '{m.group(1)}' and one for '{m.group(2)}'."}
    # Also detect "and" between two clauses (light heuristic)
    if statement.count(" and ") >= 1 and re.search(r"\b(time|effort|likelihood|frequency)\b", statement, re.IGNORECASE):
        # likely-compound; let human verify
        if not re.search(r"\b(during|when|while|before|after|e\.g\.)\b", statement[statement.find(" and "):], re.IGNORECASE):
            return {"sin": "possible_compound", "offending": " and ",
                    "suggestion": "Statement contains ' and ' — check if it bundles two outcomes."}
    return None


try:
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError:
    print("Install: pip install sentence-transformers scikit-learn numpy")
    raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw",       required=True, help="CSV of raw outcome candidates, must include 'full_statement' column")
    parser.add_argument("--out",       required=True)
    parser.add_argument("--model",     default="all-MiniLM-L6-v2")
    parser.add_argument("--threshold", type=float, default=0.82, help="cosine similarity threshold for grouping")
    args = parser.parse_args()

    df = pd.read_csv(args.raw)
    if "full_statement" not in df.columns:
        raise ValueError("CSV must have a 'full_statement' column")

    model = SentenceTransformer(args.model)
    embeddings = model.encode(df["full_statement"].tolist(), convert_to_numpy=True, show_progress_bar=True)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Agglomerative clustering on (1 - cosine)
    distance_threshold = 1 - args.threshold
    clusterer = AgglomerativeClustering(
        n_clusters=None,
        metric="precomputed",
        linkage="average",
        distance_threshold=distance_threshold,
    )
    sim = cosine_similarity(embeddings)
    dist = 1 - sim
    np.fill_diagonal(dist, 0)
    labels = clusterer.fit_predict(dist)

    clusters = {}
    sin_flags = []
    for i, label in enumerate(labels):
        statement = df.iloc[i]["full_statement"]
        cand = {
            "candidate_id": df.iloc[i].get("candidate_id", f"row-{i}"),
            "job_step": df.iloc[i].get("job_step", ""),
            "full_statement": statement,
            "source_quote": df.iloc[i].get("verbatim_quote", df.iloc[i].get("source_quote", "")),
            "source": df.iloc[i].get("source", ""),
            "embedding_idx": i,
            "sins": [],
        }
        for fn in (flag_direction_verb, flag_compound):
            sin = fn(statement)
            if sin:
                cand["sins"].append(sin)
                sin_flags.append({"candidate_id": cand["candidate_id"], **sin})
        clusters.setdefault(int(label), []).append(cand)

    # Sort clusters by size desc; pick a heuristic canonical (shortest cleanest member)
    output = []
    for label, members in sorted(clusters.items(), key=lambda kv: -len(kv[1])):
        members_sorted = sorted(members, key=lambda m: (len(m["sins"]), len(m["full_statement"])))
        canonical = members_sorted[0]
        output.append({
            "cluster_id": label,
            "size": len(members),
            "canonical_recommendation": canonical["full_statement"],
            "canonical_candidate_id": canonical["candidate_id"],
            "members": members,
            "note": "Review these candidates. The recommended canonical is the shortest member with the fewest detected syntax sins; verify before locking."
        })

    payload = {
        "n_raw": len(df),
        "n_clusters": len(output),
        "n_sin_flags": len(sin_flags),
        "threshold": args.threshold,
        "sin_flags_summary": sin_flags[:50],  # truncate
        "clusters": output,
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"[ok] {args.out} — {len(df)} candidates -> {len(output)} clusters; {len(sin_flags)} syntax sins flagged")


if __name__ == "__main__":
    main()
