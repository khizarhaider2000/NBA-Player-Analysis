"""Generate side-by-side bar charts of best vs worst NBA contracts."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_PATH = Path("Final_NBA_Data.csv")
OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def fantasy_score(row: pd.Series) -> float:
    """Position-aware fantasy metric used across the project."""
    games = row.get("G", 0)
    if games <= 55 or pd.isna(games):
        return 0.0

    pts = row.get("PTS", 0) / games
    ast = row.get("AST", 0) / games
    reb = row.get("TRB", 0) / games
    stl = row.get("STL", 0) / games
    blk = row.get("BLK", 0) / games
    tov = row.get("TOV", 0) / games
    fg_pct = row.get("FG%", 0) or 0
    three_pct = row.get("3P%", 0) or 0
    pos = (row.get("Pos", "") or "").upper()

    if any(tag in pos for tag in ("PG", "SG")):
        score = (
            1.6 * pts
            + 1.2 * ast
            + 1.0 * reb
            + 1.5 * stl
            + 0.7 * blk
            - 0.5 * tov
            + 1.2 * fg_pct
            + 2.5 * three_pct
        )
    elif any(tag in pos for tag in ("SF", "PF")):
        score = (
            1.4 * pts
            + 1.1 * ast
            + 1.3 * reb
            + 1.3 * stl
            + 1.2 * blk
            - 0.5 * tov
            + 1.2 * fg_pct
            + 2.0 * three_pct
        )
    elif "C" in pos:
        score = (
            1.4 * pts
            + 1.0 * ast
            + 1.5 * reb
            + 1.0 * stl
            + 1.6 * blk
            - 0.5 * tov
            + 1.3 * fg_pct
            + 1.8 * three_pct
        )
    else:
        score = pts + ast + reb + stl + blk - tov + fg_pct + three_pct
    return float(score)


def load_dataset(season: Optional[int] = None) -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df = df[(df["Salary (Millions)"].notna()) & (df["Salary (Millions)"] > 0)].copy()
    df["FantasyScore"] = df.apply(fantasy_score, axis=1)
    df = df[df["FantasyScore"] > 0]
    df["ValuePerMillion"] = df["FantasyScore"] / df["Salary (Millions)"]

    if season is not None:
        df = df[df["Season"] == season]
    return df


def top_contracts(df: pd.DataFrame, top_n: int = 10) -> tuple[pd.DataFrame, pd.DataFrame]:
    best = df.sort_values("ValuePerMillion", ascending=False).head(top_n)
    worst = df.sort_values("ValuePerMillion", ascending=True).head(top_n)
    return best, worst


def plot_best_vs_worst(
    season: Optional[int] = None,
    top_n: int = 10,
    figsize: tuple[int, int] = (14, 8),
) -> Path:
    df = load_dataset(season)
    if df.empty:
        raise ValueError(f"No rows found for season {season}.")

    best, worst = top_contracts(df, top_n=top_n)

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=figsize, sharey=False)

    combined_teams = pd.concat([best["Team"], worst["Team"]])
    palette = dict(
        zip(
            combined_teams.unique(),
            sns.color_palette("viridis", n_colors=max(1, combined_teams.nunique())),
        )
    )

    # Best contracts (descending)
    best_sorted = best.sort_values("ValuePerMillion", ascending=False)
    sns.barplot(
        ax=axes[0],
        data=best_sorted,
        x="ValuePerMillion",
        y="Player",
        order=best_sorted["Player"],
        hue="Team",
        palette=palette,
        dodge=False,
    )
    axes[0].set_title("Top Best Value Contracts")
    axes[0].set_xlabel("Fantasy Value per $1M")
    axes[0].set_ylabel("Player")
    axes[0].legend(loc="lower right", fontsize=8)

    # Worst contracts (ascending)
    worst_sorted = worst.sort_values("ValuePerMillion", ascending=True)
    sns.barplot(
        ax=axes[1],
        data=worst_sorted,
        x="ValuePerMillion",
        y="Player",
        order=worst_sorted["Player"],
        hue="Team",
        palette=palette,
        dodge=False,
    )
    axes[1].set_title("Top Worst Value Contracts")
    axes[1].set_xlabel("Fantasy Value per $1M")
    axes[1].set_ylabel("Player")
    axes[1].legend(loc="lower right", fontsize=8)

    for ax in axes:
        ax.set_xlim(left=df["ValuePerMillion"].min() * 0.95)
        ax.set_xticks(ax.get_xticks())

    season_label = season or "all"
    fig.suptitle(f"Top {top_n} Best vs Worst Contracts — Season {season_label}", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    output_path = OUTPUT_DIR / f"top_contracts_{season_label}.png"
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"Saved chart to {output_path}")
    return output_path


if __name__ == "__main__":
    plot_best_vs_worst(season=2025)
