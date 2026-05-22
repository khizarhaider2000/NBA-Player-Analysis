# =========================================================
# NBA API → Pandas → Processed CSV
#
# This ETL script:
# 1. Pulls NBA player season stats from nba_api
# 2. Cleans/transforms the data
# 3. Calculates additional shooting metrics
# 4. Combines all seasons into one DataFrame
# 5. Saves the cleaned dataset for future SQL loading
# =========================================================

from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
import time
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from database import engine


SEASONS = [
    "2019-20",
    "2020-21",
    "2021-22",
    "2022-23",
    "2023-24",
    "2024-25",
    "2025-26"
]



# Empty list that will store each season DataFrame
all_dfs = []


# =========================================================
# Loop through each NBA season
# =========================================================
for season in SEASONS:

    print(f"Pulling {season}...")


    # =====================================================
    # Pull player stats from NBA API
    #
    # PerGame = per-game averages
    # Base = standard stats
    # =====================================================
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame",
        measure_type_detailed_defense="Base"
    )


    # =====================================================
    # Small delay to avoid API rate limiting
    # =====================================================
    time.sleep(1)


    # =====================================================
    # Convert NBA API response into Pandas DataFrame
    # =====================================================
    df = stats.get_data_frames()[0]


    # =====================================================
    # Keep only columns we actually want
    # =====================================================
    df = df[
        [
            "PLAYER_NAME",
            "AGE",
            "TEAM_ABBREVIATION",
            "GP",
            "MIN",
            "FGM",
            "FGA",
            "FG_PCT",
            "FG3M",
            "FG3A",
            "FG3_PCT",
            "FTM",
            "FTA",
            "FT_PCT",
            "OREB",
            "DREB",
            "REB",
            "AST",
            "STL",
            "BLK",
            "TOV",
            "PF",
            "PTS"
        ]
    ].copy()


    # =====================================================
    # Add season column manually
    # =====================================================
    df["SEASON"] = season


    # =====================================================
    # Calculate 2-point field goals made
    #
    # Formula:
    # FG2M = Total FGs - 3PT FGs
    # =====================================================
    df["FG2M"] = df["FGM"] - df["FG3M"]


    # =====================================================
    # Calculate 2-point attempts
    #
    # Formula:
    # FG2A = Total FGA - 3PT FGA
    # =====================================================
    df["FG2A"] = df["FGA"] - df["FG3A"]


    # =====================================================
    # Calculate 2-point percentage
    #
    # Replace inf/nan with 0 for safety
    # =====================================================
    df["FG2_PCT"] = (
        df["FG2M"] / df["FG2A"]
    ).replace(
        [float("inf"), -float("inf")],
        0
    ).fillna(0)


    # =====================================================
    # Calculate Effective Field Goal Percentage
    #
    # Formula:
    # (FGM + 0.5 * FG3M) / FGA
    # =====================================================
    df["EFG_PCT"] = (
        (df["FGM"] + 0.5 * df["FG3M"]) / df["FGA"]
    ).replace(
        [float("inf"), -float("inf")],
        0
    ).fillna(0)


    # =====================================================
    # Add cleaned season DataFrame to master list
    # =====================================================
    all_dfs.append(df)


# =========================================================
# Combine all seasons into one DataFrame
# =========================================================
combined_df = pd.concat(all_dfs, ignore_index=True)


# =========================================================
# Rename columns to database-friendly names
# =========================================================
combined_df = combined_df.rename(columns={

    "SEASON": "season",

    "PLAYER_NAME": "player_name",
    "AGE": "age",
    "TEAM_ABBREVIATION": "team",

    "GP": "games",
    "MIN": "minutes_per_game",

    "FGM": "fg",
    "FGA": "fga",
    "FG_PCT": "fg_pct",

    "FG3M": "three_p",
    "FG3A": "three_pa",
    "FG3_PCT": "three_pct",

    "FG2M": "two_p",
    "FG2A": "two_pa",
    "FG2_PCT": "two_pct",

    "EFG_PCT": "efg_pct",

    "FTM": "ft",
    "FTA": "fta",
    "FT_PCT": "ft_pct",

    "OREB": "orb",
    "DREB": "drb",
    "REB": "trb",

    "AST": "ast",
    "STL": "stl",
    "BLK": "blk",

    "TOV": "tov",
    "PF": "pf",

    "PTS": "pts"
})


# =========================================================
# Reorder columns into final structure
# =========================================================
combined_df = combined_df[
    [
        "season",
        "player_name",
        "age",
        "team",

        "games",
        "minutes_per_game",

        "fg",
        "fga",
        "fg_pct",

        "three_p",
        "three_pa",
        "three_pct",

        "two_p",
        "two_pa",
        "two_pct",

        "efg_pct",

        "ft",
        "fta",
        "ft_pct",

        "orb",
        "drb",
        "trb",

        "ast",
        "stl",
        "blk",

        "tov",
        "pf",

        "pts"
    ]
]


# =========================================================
# Create output folder if it doesn't exist
# =========================================================
os.makedirs("data/processed", exist_ok=True)


# =========================================================
# Save cleaned dataset as CSV
# =========================================================
combined_df.to_csv(
    "data/processed/player_season_stats_api.csv",
    index=False
)


combined_df.to_sql(
    "player_season_stats_raw",
    engine,
    if_exists="replace",
    index=False
)

print("Loaded data into PostgreSQL.")


# =========================================================
# Preview final dataset
# =========================================================
print(combined_df.head())


# =========================================================
# Print dataset shape
# =========================================================
print(combined_df.shape)


# =========================================================
# Success message
# =========================================================
print("Saved to data/processed/player_season_stats_api.csv")