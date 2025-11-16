"""Generate an animated salary vs. fantasy value scatterplot."""
from __future__ import annotations

import shutil
from pathlib import Path

import imageio.v2 as imageio
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

DATA_PATH = Path("Final_NBA_Data.csv")
OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_HTML = OUTPUT_DIR / "salary_value_frontier.html"
OUTPUT_GIF = OUTPUT_DIR / "salary_value_frontier.gif"
FRAMES_DIR = OUTPUT_DIR / "salary_value_frames"


def fantasy_score(row: pd.Series) -> float:
    """Position-aware fantasy value metric with availability guardrails."""
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


def build_dataset() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    numeric_df = df[(df["Salary (Millions)"].notna()) & (df["Salary (Millions)"] > 0)]
    numeric_df = numeric_df.copy()
    numeric_df["FantasyScore"] = numeric_df.apply(fantasy_score, axis=1)
    numeric_df = numeric_df[numeric_df["FantasyScore"] > 0]
    numeric_df["ValuePerMillion"] = numeric_df["FantasyScore"] / numeric_df["Salary (Millions)"]

    # Normalize size so bubble areas are readable across seasons
    g_min, g_max = numeric_df["G"].min(), numeric_df["G"].max()
    numeric_df["AvailabilitySize"] = np.interp(
        numeric_df["G"],
        (g_min, g_max),
        (8, 45),
    )
    return numeric_df


def plot(df: pd.DataFrame) -> None:
    x_max = df["Salary (Millions)"].max() * 1.1
    y_min = df["FantasyScore"].min() * 0.9
    y_max = df["FantasyScore"].max() * 1.1
    fig = px.scatter(
        df,
        x="Salary (Millions)",
        y="FantasyScore",
        animation_frame="Season",
        animation_group="Player",
        size="AvailabilitySize",
        color="ValuePerMillion",
        hover_data={
            "Player": True,
            "Team": True,
            "Pos": True,
            "G": True,
            "FantasyScore": ":.2f",
            "Salary (Millions)": ":.2f",
            "ValuePerMillion": ":.2f",
        },
        color_continuous_scale="Turbo",
        title="Salary vs Fantasy Value Frontier (Animated by Season)",
        labels={
            "Salary (Millions)": "Salary (USD Millions)",
            "FantasyScore": "Fantasy Value Score",
            "ValuePerMillion": "Value per $1M",
        },
        range_x=[1, x_max],
        range_y=[y_min, y_max],
        log_x=True,
    )

    fig.update_layout(
        legend_title_text="",
        coloraxis_colorbar=dict(title="Value / $1M"),
    )

    # Color-scale reference lines (median salary + score)
    median_salary = df["Salary (Millions)"].median()
    median_score = df["FantasyScore"].median()
    fig.add_vline(
        x=median_salary,
        line=dict(color="rgba(255,255,255,0.4)", dash="dash"),
        annotation_text="Median Salary",
        annotation_position="top left",
    )
    fig.add_hline(
        y=median_score,
        line=dict(color="rgba(255,255,255,0.4)", dash="dash"),
        annotation_text="Median Fantasy Score",
        annotation_position="bottom right",
    )

    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")
    print(f"Visualization saved to {OUTPUT_HTML}")

    save_gif(df, x_max, y_min, y_max)


def save_gif(df: pd.DataFrame, x_max: float, y_min: float, y_max: float) -> None:
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    frames = []
    salary_median = df["Salary (Millions)"].median()
    score_median = df["FantasyScore"].median()

    for season in sorted(df["Season"].unique()):
        subset = df[df["Season"] == season]
        fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
        scatter = ax.scatter(
            subset["Salary (Millions)"],
            subset["FantasyScore"],
            s=subset["AvailabilitySize"] * 28,
            c=subset["ValuePerMillion"],
            cmap="turbo",
            vmin=df["ValuePerMillion"].min(),
            vmax=df["ValuePerMillion"].max(),
            alpha=0.85,
            edgecolors="k",
            linewidths=0.2,
        )
        ax.set_xscale("log")
        ax.set_xlim(1, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_xlabel("Salary (USD Millions)")
        ax.set_ylabel("Fantasy Value Score")
        ax.set_title("Salary vs Fantasy Value Frontier")
        ax.axvline(salary_median, color="white", linestyle="--", linewidth=0.8)
        ax.axhline(score_median, color="white", linestyle="--", linewidth=0.8)

        season_label = f"Season {season}"
        ax.text(
            0.02,
            0.92,
            season_label,
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            bbox=dict(facecolor="black", alpha=0.3, boxstyle="round,pad=0.3"),
            color="white",
        )

        cbar = fig.colorbar(scatter, ax=ax, pad=0.02)
        cbar.set_label("Value per $1M")

        fig.tight_layout()
        frame_path = FRAMES_DIR / f"frame_{season}.png"
        fig.savefig(frame_path, bbox_inches="tight")
        plt.close(fig)
        frames.append(imageio.imread(frame_path))

    imageio.mimsave(OUTPUT_GIF, frames, duration=1.5, loop=0)
    print(f"GIF preview saved to {OUTPUT_GIF}")


if __name__ == "__main__":
    dataset = build_dataset()
    plot(dataset)
