"""
DSW Ventures — Startup Screener Visualisations
Generates four analytical charts from the ranked shortlist.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

INPUT_PATH = Path("output/ranked_shortlist.csv")
CHARTS_DIR = Path("output/charts")

# Consistent professional palette
PALETTE = {
    "primary": "#1B3A6B",
    "accent": "#E8802A",
    "muted": "#7A9CC0",
    "light": "#D6E4F0",
    "tier_high": "#1B3A6B",
    "tier_mid": "#E8802A",
    "tier_low": "#A8C5DA",
}

DPI = 150

SECTOR_TIERS = {
    "Medical Devices & Diagnostics": "Tier 1",
    "Drug Discovery & Therapeutics": "Tier 1",
    "Machine Learning & AI": "Tier 1",
    "Computer Vision": "Tier 1",
    "Natural Language Processing": "Tier 1",
    "Robotics & Automation": "Tier 1",
    "Quantum Computing": "Tier 1",
    "Photonics & Semiconductors": "Tier 1",
    "Genomics & Synthetic Biology": "Tier 2",
    "Biotechnology": "Tier 2",
    "Renewable Energy & Storage": "Tier 2",
    "Carbon Capture & Climate Tech": "Tier 2",
    "Materials Science & Engineering": "Tier 2",
    "Agricultural Technology": "Tier 3",
    "SaaS / Enterprise Software": "Tier 3",
    "Consumer Technology": "Tier 4",
    "EdTech": "Tier 4",
    "FinTech": "Tier 4",
}

TIER_COLOURS = {
    "Tier 1": PALETTE["tier_high"],
    "Tier 2": PALETTE["tier_mid"],
    "Tier 3": PALETTE["muted"],
    "Tier 4": PALETTE["tier_low"],
}


def load_data() -> pd.DataFrame:
    df = pd.read_csv(INPUT_PATH)
    df["sector_tier"] = df["primary_sector"].map(SECTOR_TIERS).fillna("Tier 4")
    return df


def chart1_score_distribution(df: pd.DataFrame):
    """Histogram of final_score across shortlisted companies."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(
        df["final_score"],
        bins=20,
        color=PALETTE["primary"],
        edgecolor="white",
        linewidth=0.6,
    )
    ax.set_title("DSW Score Distribution — Shortlisted Companies", fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel("DSW Score (out of 100)", fontsize=11)
    ax.set_ylabel("Number of Companies", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    fig.tight_layout()
    path = CHARTS_DIR / "score_distribution.png"
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"  Saved: {path}")


def chart2_sector_breakdown(df: pd.DataFrame):
    """Bar chart: count of shortlisted companies by sector, descending."""
    counts = df["primary_sector"].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(counts.index, counts.values, color=PALETTE["primary"], edgecolor="white", linewidth=0.5)
    ax.set_title("Shortlisted Companies by Sector", fontsize=14, fontweight="bold", pad=14)
    ax.set_ylabel("Count", fontsize=11)
    ax.set_xlabel("")
    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(counts.index, rotation=40, ha="right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{int(height)}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            color=PALETTE["primary"],
        )
    fig.tight_layout()
    path = CHARTS_DIR / "sector_breakdown.png"
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"  Saved: {path}")


def chart3_funding_vs_score(df: pd.DataFrame):
    """Scatter plot: funding raised vs DSW score, coloured by sector tier."""
    fig, ax = plt.subplots(figsize=(10, 6))

    for tier, group in df.groupby("sector_tier"):
        ax.scatter(
            group["total_raised_gbp"] / 1_000,
            group["final_score"],
            label=tier,
            color=TIER_COLOURS.get(tier, PALETTE["muted"]),
            alpha=0.75,
            edgecolors="white",
            linewidths=0.4,
            s=60,
            zorder=3,
        )

    ax.axvline(750, color=PALETTE["accent"], linestyle="--", linewidth=1.4, label="£750k threshold", zorder=2)
    ax.set_title("Funding Raised vs DSW Score", fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel("Total Raised (£k)", fontsize=11)
    ax.set_ylabel("DSW Score (out of 100)", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=9, frameon=False)
    fig.tight_layout()
    path = CHARTS_DIR / "funding_vs_score.png"
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"  Saved: {path}")


def chart4_top20(df: pd.DataFrame):
    """Horizontal bar chart of top 20 companies by final_score."""
    top20 = df.nlargest(20, "final_score").sort_values("final_score")
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(
        top20["company_name"],
        top20["final_score"],
        color=PALETTE["primary"],
        edgecolor="white",
        linewidth=0.5,
    )
    ax.set_title("Top 20 Startups — DSW Screener", fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel("DSW Score (out of 100)", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(0, top20["final_score"].max() * 1.12)
    for bar in bars:
        width = bar.get_width()
        ax.annotate(
            f"{width:.1f}",
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=8.5,
            color=PALETTE["primary"],
        )
    fig.tight_layout()
    path = CHARTS_DIR / "top20_companies.png"
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"  Saved: {path}")


def main():
    print("=" * 60)
    print("DSW Ventures — Visualisation Engine")
    print("=" * 60)

    print(f"\nLoading ranked shortlist from {INPUT_PATH} ...")
    df = load_data()
    print(f"  {len(df)} companies loaded.")

    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    print("\nGenerating charts ...")
    chart1_score_distribution(df)
    chart2_sector_breakdown(df)
    chart3_funding_vs_score(df)
    chart4_top20(df)

    print("\nAll charts saved to output/charts/")
    print("=" * 60)


if __name__ == "__main__":
    main()
