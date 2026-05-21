#!/usr/bin/env python3
"""
segmentation_engine.py — Canonical Appendix C + Chapter 21 implementation
of outcome-based segmentation.

Pipeline:
    1. Build per-respondent opportunity matrix (per-respondent top-2-box: 1
       if rated 4-or-5, else 0, * 10; Opp = Imp + max(Imp - Sat, 0)).
    2. Filter to outcomes that DIFFERENTIATE across respondents (variance).
    3. Factor-analyze the differentiating subset (scree + varimax).
    4. K-means on factor scores; sweep k=2..max_k; auto-pick k via elbow rule.
    5. Profile each segment using complexity factors (columns prefixed
       profile_), surfacing the 1-3 factors with the largest segment-vs-
       overall delta in standard-deviation units.
    6. Produce per-segment opportunity landscapes (Ch 20 / Ch 21).

Usage:
    python segmentation_engine.py \
        --survey survey-data.csv \
        --outcomes netted-outcomes.csv \
        --out-dir analysis-out/ \
        [--max-k 6] [--n-factors 0] [--profile-prefix profile_] [--synthetic]
"""

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

try:
    from factor_analyzer import FactorAnalyzer
except ImportError:
    FactorAnalyzer = None


SYNTHETIC_BANNER = (
    "================================================================\n"
    "WARNING: SYNTHETIC DATA — DIRECTIONAL ONLY — DO NOT SHIP\n"
    "Validate with n>=300 real respondents per ODI v2.4.2 Ch 16.\n"
    "================================================================\n"
)


def per_respondent_opp(survey: pd.DataFrame, outcomes: pd.DataFrame) -> pd.DataFrame:
    """Per-respondent, per-outcome opportunity matrix.

    Per-respondent top-2-box: 1 if rated 4-or-5 else 0, then *10 to put on 0-10.
    Opp = Imp + max(Imp - Sat, 0).
    """
    rows = []
    oids = []
    for _, outcome_row in outcomes.iterrows():
        oid = outcome_row["id"]
        imp_col, sat_col = f"imp_{oid}", f"sat_{oid}"
        if imp_col not in survey.columns or sat_col not in survey.columns:
            continue
        oids.append(oid)
        imp = (survey[imp_col] >= 4).astype(float) * 10
        sat = (survey[sat_col] >= 4).astype(float) * 10
        opp = imp + (imp - sat).clip(lower=0)
        rows.append(opp.values)
    matrix = np.vstack(rows).T  # respondents x outcomes
    df = pd.DataFrame(matrix, columns=oids, index=survey.index)
    df["respondent_id"] = survey["respondent_id"].values if "respondent_id" in survey.columns else df.index
    return df


def pick_differentiating(opp_matrix: pd.DataFrame, top_frac: float = 0.5) -> list[str]:
    oids = [c for c in opp_matrix.columns if c != "respondent_id"]
    variances = opp_matrix[oids].var().sort_values(ascending=False)
    n_keep = max(5, int(len(oids) * top_frac))
    return list(variances.head(n_keep).index)


def scree(opp_matrix: pd.DataFrame, diff_oids: list[str], out_path: Path):
    X = StandardScaler().fit_transform(opp_matrix[diff_oids].values)
    # eigenvalues via covariance
    eigvals = np.sort(np.linalg.eigvalsh(np.cov(X.T)))[::-1]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(1, len(eigvals) + 1), eigvals, marker="o")
    ax.axhline(1, linestyle="--", color="#888")
    ax.set_xlabel("Factor")
    ax.set_ylabel("Eigenvalue")
    ax.set_title("Scree plot — pick factors with eigenvalue > 1")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return eigvals


def factor_analyze(opp_matrix: pd.DataFrame, diff_oids: list[str], n_factors: int, out_path: Path):
    if FactorAnalyzer is None:
        # Fall back to PCA-like
        from sklearn.decomposition import PCA
        pca = PCA(n_components=n_factors)
        scores = pca.fit_transform(StandardScaler().fit_transform(opp_matrix[diff_oids].values))
        loadings = pd.DataFrame(pca.components_.T, index=diff_oids, columns=[f"F{i+1}" for i in range(n_factors)])
    else:
        fa = FactorAnalyzer(n_factors=n_factors, rotation="varimax")
        fa.fit(opp_matrix[diff_oids].values)
        scores = fa.transform(opp_matrix[diff_oids].values)
        loadings = pd.DataFrame(fa.loadings_, index=diff_oids, columns=[f"F{i+1}" for i in range(n_factors)])
    loadings.to_csv(out_path, index_label="outcome_id")
    return scores, loadings


def elbow(scores: np.ndarray, max_k: int, out_path: Path):
    inertias = []
    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(scores)
        inertias.append((k, km.inertia_))
    fig, ax = plt.subplots(figsize=(8, 5))
    ks = [i[0] for i in inertias]
    inrs = [i[1] for i in inertias]
    ax.plot(ks, inrs, marker="o")
    ax.set_xlabel("k")
    ax.set_ylabel("Inertia (lower = tighter clusters)")
    ax.set_title("Elbow plot — pick smallest k where Δ-inertia < 15%")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    # auto-pick: smallest k where the marginal drop is <15% of the previous
    chosen = ks[0]
    for i in range(1, len(inrs)):
        drop = (inrs[i - 1] - inrs[i]) / inrs[i - 1]
        if drop < 0.15:
            chosen = ks[i - 1]
            break
    else:
        chosen = ks[-1]
    return chosen, inertias


def fit_kmeans(scores: np.ndarray, k: int):
    km = KMeans(n_clusters=k, n_init=20, random_state=42).fit(scores)
    return km.labels_


def profile_segment(survey: pd.DataFrame, outcomes: pd.DataFrame, segment_mask: pd.Series, profile_prefix: str) -> dict:
    """Returns per-step opportunity scores + complexity-factor means."""
    seg = survey[segment_mask]
    out = {}
    out["size_n"] = int(segment_mask.sum())
    out["size_pct"] = float(segment_mask.mean())

    # Top opportunities within segment
    rows = []
    for _, outcome_row in outcomes.iterrows():
        oid = outcome_row["id"]
        imp_col, sat_col = f"imp_{oid}", f"sat_{oid}"
        if imp_col not in seg.columns:
            continue
        imp = (seg[imp_col] >= 4).mean() * 10
        sat = (seg[sat_col] >= 4).mean() * 10
        opp = imp + max(imp - sat, 0)
        rows.append({"outcome_id": oid, "statement": outcome_row.get("full_statement", ""), "importance": round(imp, 2), "satisfaction": round(sat, 2), "opportunity": round(opp, 2)})
    scored = pd.DataFrame(rows).sort_values("opportunity", ascending=False).reset_index(drop=True)
    out["top_opportunities"] = scored.head(7).to_dict(orient="records")

    # Complexity-factor profile
    cf_cols = [c for c in survey.columns if c.startswith(profile_prefix)]
    cf_profile = {}
    overall_means = survey[cf_cols].mean(numeric_only=True)
    seg_means = seg[cf_cols].mean(numeric_only=True)
    for c in cf_cols:
        if c in overall_means.index and c in seg_means.index:
            cf_profile[c] = {
                "segment_mean": float(seg_means[c]),
                "overall_mean": float(overall_means[c]),
                "delta_sd": float((seg_means[c] - overall_means[c]) / (survey[c].std() or 1)),
            }
    out["complexity_factor_profile"] = cf_profile

    return out, scored


def plot_segment_landscape(scored: pd.DataFrame, out_path: Path, seg_id: str, synthetic: bool):
    fig, ax = plt.subplots(figsize=(10, 8))
    for _, row in scored.iterrows():
        ax.scatter(row["satisfaction"], row["importance"], s=70, alpha=0.7)
        ax.annotate(row["outcome_id"], (row["satisfaction"], row["importance"]), fontsize=7, alpha=0.6)
    ax.plot([0, 10], [0, 10], "--", color="#888", linewidth=1)
    ax.plot(np.linspace(0, 10, 100), (np.linspace(0, 10, 100) + 10) / 2, "--", color="#b22234", linewidth=1)
    title = f"Opportunity Landscape — Segment {seg_id}"
    if synthetic:
        title = "[SYNTHETIC] " + title
    ax.set_title(title)
    ax.set_xlabel("Satisfaction (0–10)")
    ax.set_ylabel("Importance (0–10)")
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.grid(alpha=0.3)
    if synthetic:
        ax.text(0.5, 0.5, "SYNTHETIC", transform=ax.transAxes, fontsize=80, color="#b22234",
                alpha=0.10, ha="center", va="center", rotation=30, weight="bold")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="ODI outcome-based segmentation (Appendix C)")
    parser.add_argument("--survey",   required=True)
    parser.add_argument("--outcomes", required=True)
    parser.add_argument("--out-dir",  default="analysis-out")
    parser.add_argument("--max-k",    type=int, default=6)
    parser.add_argument("--n-factors", type=int, default=0, help="0 = auto from scree")
    parser.add_argument("--profile-prefix", default="profile_")
    parser.add_argument("--synthetic", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    survey = pd.read_csv(args.survey)
    outcomes = pd.read_csv(args.outcomes)

    if "quality_flag" in survey.columns:
        survey = survey[survey["quality_flag"].isna() | (survey["quality_flag"] == "")]

    opp_matrix = per_respondent_opp(survey, outcomes)
    diff_oids = pick_differentiating(opp_matrix, top_frac=0.5)
    print(f"[info] using {len(diff_oids)} differentiating outcomes for clustering", file=sys.stderr)

    eigvals = scree(opp_matrix, diff_oids, out_dir / "scree.png")
    n_factors = args.n_factors or max(2, int((eigvals > 1).sum()))
    print(f"[info] n_factors = {n_factors}", file=sys.stderr)

    scores, loadings = factor_analyze(opp_matrix, diff_oids, n_factors, out_dir / "factor_loadings.csv")
    k_chosen, inertias = elbow(scores, args.max_k, out_dir / "elbow.png")
    print(f"[info] k_chosen = {k_chosen}", file=sys.stderr)

    labels = fit_kmeans(scores, k_chosen)
    survey = survey.reset_index(drop=True)
    survey["segment_id"] = [f"S{l}" for l in labels]
    survey[["respondent_id", "segment_id"]].to_csv(out_dir / "segments.csv", index=False)

    audit = {
        "method_version": "ODI v2.4.2",
        "data_provenance": "SYNTHETIC — directional only, do not ship" if args.synthetic else "real_survey",
        "n_respondents": int(len(survey)),
        "n_differentiating_outcomes": int(len(diff_oids)),
        "differentiating_outcomes": diff_oids,
        "n_factors_chosen": int(n_factors),
        "k_tested": [k for k, _ in inertias],
        "k_chosen": int(k_chosen),
        "segments": {},
    }

    for seg_id in sorted(survey["segment_id"].unique()):
        mask = survey["segment_id"] == seg_id
        profile, scored_seg = profile_segment(survey, outcomes, mask, args.profile_prefix)
        plot_segment_landscape(scored_seg, out_dir / f"landscape_segment_{seg_id}.png", seg_id, args.synthetic)
        scored_seg.to_csv(out_dir / f"opportunity_scores_segment_{seg_id}.csv", index=False)
        audit["segments"][seg_id] = profile

    audit_path = out_dir / "segmentation_audit.json"
    with open(audit_path, "w") as f:
        if args.synthetic:
            f.write("// " + SYNTHETIC_BANNER.replace("\n", "\n// "))
            f.write("\n")
        json.dump(audit, f, indent=2)
    print(f"[ok] {audit_path}")
    print(json.dumps({k: v["size_pct"] for k, v in audit["segments"].items()}, indent=2))


if __name__ == "__main__":
    main()
