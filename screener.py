"""
DSW Ventures — Early-Stage Startup Screener
Main scoring engine: loads, filters, scores, and ranks startups.
"""

import pandas as pd
from pathlib import Path
from utils import (
    infer_female_founder,
    is_golden_triangle,
    map_sector_score,
    map_university_tier,
    HARD_TECH_SECTORS,
)

DATA_PATH = Path("data/dsw_startups_v2.csv")
OUTPUT_PATH = Path("output/ranked_shortlist.csv")

OUTPUT_COLUMNS = [
    "rank", "company_name", "city", "postcode_district", "primary_sector",
    "university_affiliation", "total_raised_gbp", "founder_names",
    "filter_result", "ip_score", "founder_score", "funding_score",
    "poc_score", "sector_score", "final_score",
]


# ---------------------------------------------------------------------------
# Stage 1 — Hard Filter
# ---------------------------------------------------------------------------

def apply_stage1_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Classify each company as Pass-GT, Pass-Override, or Eliminated."""

    def classify(row):
        in_gt = is_golden_triangle(row["postcode_district"])
        if not in_gt:
            return "Pass — Outside GT"
        if infer_female_founder(row["founder_names"]):
            return "Pass — Female Founder Override"
        return "Eliminated"

    df["filter_result"] = df.apply(classify, axis=1)
    return df


# ---------------------------------------------------------------------------
# Stage 2 — Scoring factors
# ---------------------------------------------------------------------------

def score_ip(row: pd.Series) -> int:
    """IP Defensibility score (0–10)."""
    granted = row["patents_granted"]
    filed = row["patents_filed"]
    sector = row["primary_sector"]

    if granted >= 1:
        return 10
    if filed >= 2:
        return 8
    if filed == 1:
        return 6
    # 0 patents
    if sector not in HARD_TECH_SECTORS:
        return 4  # software/services — patents less expected
    return 2  # hard-tech with no patents


def score_founder(row: pd.Series) -> int:
    """Founder Quality score (0–10)."""
    tier = map_university_tier(row["university_affiliation"])
    num_founders = row["num_founders"]

    if tier == "Tier 1":
        return 10
    if tier == "Tier 2":
        return 7
    if num_founders >= 2:
        return 5
    return 3


def score_funding(row: pd.Series) -> int:
    """Funding Sweet Spot score (0–10)."""
    raised = row["total_raised_gbp"]

    if 50_000 <= raised <= 750_000:
        return 10
    if 750_001 <= raised <= 1_000_000:
        return 6
    if raised > 1_000_000:
        return 2
    if 10_000 <= raised <= 49_999:
        return 4
    return 1  # below £10k


def score_poc(row: pd.Series) -> int:
    """Proof of Concept composite score (0–10)."""
    points = 0
    if str(row["peer_reviewed_research"]).strip().lower() == "yes":
        points += 3
    if row["annual_revenue_gbp"] > 0:
        points += 3
    if row["paying_customers"] > 0:
        points += 2
    if str(row["pilot_completed"]).strip().lower() == "yes":
        points += 2
    return min(points, 10)


def score_sector(row: pd.Series) -> int:
    """Sector Fit score (0–10)."""
    return map_sector_score(row["primary_sector"])


def calculate_final_score(row: pd.Series) -> float:
    """Weighted final score, expressed out of 100."""
    return round(
        (row["ip_score"] * 0.30
         + row["founder_score"] * 0.25
         + row["funding_score"] * 0.20
         + row["poc_score"] * 0.15
         + row["sector_score"] * 0.10) * 10,
        2,
    )


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("DSW Ventures — Startup Screener")
    print("=" * 60)

    # Load data
    print(f"\n[1/6] Loading data from {DATA_PATH} ...")
    df = pd.read_csv(DATA_PATH)
    total_input = len(df)
    print(f"      {total_input} companies loaded.")

    # Stage 1 filter
    print("\n[2/6] Applying Stage 1 — Golden Triangle filter ...")
    df = apply_stage1_filter(df)

    n_outside_gt = (df["filter_result"] == "Pass — Outside GT").sum()
    n_override = (df["filter_result"] == "Pass — Female Founder Override").sum()
    n_eliminated = (df["filter_result"] == "Eliminated").sum()

    print(f"      Total input:           {total_input}")
    print(f"      Pass — Outside GT:     {n_outside_gt}")
    print(f"      Pass — Female Override:{n_override:>4}")
    print(f"      Eliminated (inside GT):{n_eliminated}")

    # Keep only passing companies
    shortlist = df[df["filter_result"] != "Eliminated"].copy()
    print(f"\n      {len(shortlist)} companies proceed to scoring.")

    # Stage 2 scoring
    print("\n[3/6] Calculating factor scores ...")
    shortlist["ip_score"] = shortlist.apply(score_ip, axis=1)
    shortlist["founder_score"] = shortlist.apply(score_founder, axis=1)
    shortlist["funding_score"] = shortlist.apply(score_funding, axis=1)
    shortlist["poc_score"] = shortlist.apply(score_poc, axis=1)
    shortlist["sector_score"] = shortlist.apply(score_sector, axis=1)

    print("\n[4/6] Computing final weighted scores ...")
    shortlist["final_score"] = shortlist.apply(calculate_final_score, axis=1)

    # Rank
    shortlist = shortlist.sort_values("final_score", ascending=False).reset_index(drop=True)
    shortlist["rank"] = shortlist.index + 1

    # Save output
    print(f"\n[5/6] Saving ranked shortlist to {OUTPUT_PATH} ...")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    shortlist[OUTPUT_COLUMNS].to_csv(OUTPUT_PATH, index=False)
    print(f"      Saved {len(shortlist)} companies.")

    # Print top 10
    print("\n[6/6] Top 10 Companies — DSW Screener\n")
    top10 = shortlist.head(10)[["rank", "company_name", "city", "primary_sector", "final_score"]]
    col_widths = [4, 32, 16, 36, 11]
    headers = ["Rank", "Company", "City", "Sector", "Score/100"]
    separator = "  ".join("-" * w for w in col_widths)
    header_row = "  ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    print(header_row)
    print(separator)
    for _, row in top10.iterrows():
        line = "  ".join([
            str(int(row["rank"])).ljust(col_widths[0]),
            str(row["company_name"])[:col_widths[1]].ljust(col_widths[1]),
            str(row["city"])[:col_widths[2]].ljust(col_widths[2]),
            str(row["primary_sector"])[:col_widths[3]].ljust(col_widths[3]),
            f"{row['final_score']:.2f}".ljust(col_widths[4]),
        ])
        print(line)

    print("\nDone. Run visualise.py to generate charts.")
    print("=" * 60)


if __name__ == "__main__":
    main()
