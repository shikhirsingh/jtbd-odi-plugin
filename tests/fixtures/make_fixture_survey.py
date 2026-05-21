#!/usr/bin/env python3
"""
Generate a small but realistic-looking ODI survey CSV for smoke-testing the
analysis scripts. n=200 fake respondents, 17 outcomes, 3 competitors, 4
profiling columns, 3 WTP columns.

The data is constructed so that:
  - E-04 (earbuds dislodge during motion) is clearly UNDERSERVED for one
    segment (gym users) -> high opp expected.
  - P-02 (audio re-routes to unintended device) is clearly UNDERSERVED for
    multi-device power users -> high opp expected.
  - Two natural segments should emerge from /runsegmentation: gym-active
    users and multi-device power users.

This is purely for smoke testing. NEVER use this for any decision.
"""
import csv
import random
from pathlib import Path

random.seed(42)

OUTCOMES = [
    "D-01","D-02","L-01","L-02","P-01","P-02","P-03","C-01",
    "E-01","E-02","E-03","E-04","M-01","M-02","Mo-01","Mo-02","Co-01"
]
COMPETITORS = ["AirPods", "Sony", "Bose"]

# Persona archetypes — drives the rating distributions.
# Each persona has biases (1-5 distributions) per outcome.
def gym_user():
    return {
        "profile_commute_min": random.randint(5, 25),
        "profile_listening_env": "gym",
        "profile_offline_pct": random.randint(20, 60),
        "profile_switch_freq": random.choice(["never","1-2"]),
        "biases": {
            # Earbuds-dislodge: very important, very dissatisfied
            "E-04": (5, 2),   # imp_mean ~5, sat_mean ~2
            # Battery: important, somewhat dissatisfied
            "E-03": (4, 3),
            # Track selection: somewhat important
            "C-01": (3, 4),
            # Re-route to unintended device: less critical for gym users
            "P-02": (3, 3),
            # Default everything else: medium
        },
        "wtp_mean": 220,
    }

def multi_device_power():
    return {
        "profile_commute_min": random.randint(40, 120),
        "profile_listening_env": "quiet_transit",
        "profile_offline_pct": random.randint(40, 80),
        "profile_switch_freq": random.choice(["3-5","6+"]),
        "biases": {
            "P-02": (5, 2),    # Re-route — extreme pain
            "L-02": (5, 3),    # offline availability — pain
            "P-03": (4, 3),    # queue ordering — pain
            "E-03": (5, 3),    # battery — pain
            "E-04": (2, 4),    # earbuds dislodge — they don't care
            "M-01": (3, 4),
        },
        "wtp_mean": 380,
    }

def casual_walker():
    return {
        "profile_commute_min": random.randint(5, 20),
        "profile_listening_env": "busy_street",
        "profile_offline_pct": random.randint(0, 30),
        "profile_switch_freq": "1-2",
        "biases": {
            "M-01": (4, 3),    # environmental awareness — pain
            "Mo-01": (3, 4),
            "E-01": (3, 4),
            # Mostly table stakes; not many extremes
        },
        "wtp_mean": 95,
    }

PERSONAS = [
    ("gym",    gym_user,    80),  # 40% of sample
    ("multi",  multi_device_power, 70),  # 35%
    ("casual", casual_walker, 50),  # 25%
]


def sample_rating(mean, spread=1.0):
    """Sample a 1-5 rating roughly around `mean` with some noise."""
    val = random.gauss(mean, spread)
    return max(1, min(5, int(round(val))))


def default_bias():
    # Middle-of-road outcome: imp ~3.5, sat ~3.5
    return (3.5, 3.5)


def row_for_persona(persona_name, persona_fn, rid):
    p = persona_fn()
    row = {
        "respondent_id": rid,
        "screener_pass": 1,
        "quality_flag": "",
        "persona_label": persona_name,
        "profile_commute_min": p["profile_commute_min"],
        "profile_listening_env": p["profile_listening_env"],
        "profile_offline_pct": p["profile_offline_pct"],
        "profile_switch_freq": p["profile_switch_freq"],
    }

    # Pick one competitor used most often
    used_competitor = random.choice(COMPETITORS)
    row["used_competitor"] = used_competitor

    # Importance + satisfaction per outcome
    for oid in OUTCOMES:
        imp_mean, sat_mean = p["biases"].get(oid, default_bias())
        row[f"imp_{oid}"] = sample_rating(imp_mean, spread=0.7)
        row[f"sat_{oid}"] = sample_rating(sat_mean, spread=0.8)

    # Competitive sat: only for the competitor this respondent uses
    for comp in COMPETITORS:
        for oid in OUTCOMES:
            if comp == used_competitor:
                # Slight competitor-specific tilt (AirPods strong on re-route, etc.)
                imp_mean, sat_mean = p["biases"].get(oid, default_bias())
                tilt = 0
                if comp == "AirPods" and oid == "P-02":
                    tilt = -1  # AirPods worse on re-route
                elif comp == "Sony" and oid == "L-02":
                    tilt = +0.5
                elif comp == "Bose" and oid == "E-02":
                    tilt = +0.5
                row[f"sat_{comp}_{oid}"] = sample_rating(sat_mean + tilt, spread=0.8)
            else:
                row[f"sat_{comp}_{oid}"] = ""  # they don't rate competitors they don't use

    # WTP
    row["wtp_q1"] = max(0, int(random.gauss(p["wtp_mean"], p["wtp_mean"]*0.25)))
    row["wtp_q2"] = int(row["wtp_q1"] * random.uniform(1.1, 1.5))
    row["wtp_q3"] = random.choice([3, 4, 4, 5])
    return row


def main():
    out_path = Path(__file__).parent / "survey-data.csv"
    rows = []
    rid = 1
    for persona_name, persona_fn, n in PERSONAS:
        for _ in range(n):
            rows.append(row_for_persona(persona_name, persona_fn, f"R-{rid:04d}"))
            rid += 1

    # Add a few intentionally-low-quality respondents we'll later filter
    for _ in range(5):
        r = row_for_persona("noise", casual_walker, f"R-{rid:04d}")
        r["quality_flag"] = "straight_lined"
        rows.append(r)
        rid += 1

    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"[ok] wrote {out_path} — {len(rows)} respondents")


if __name__ == "__main__":
    main()
