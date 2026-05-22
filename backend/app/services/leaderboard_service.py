from backend.app.utils.helpers import bounded_limit, fetch_all


LEADERBOARD_METRICS = {
    "points": ("pts", "pts"),
    "rebounds": ("trb", "rebounds"),
    "assists": ("ast", "assists"),
    "steals": ("stl", "steals"),
    "blocks": ("blk", "blocks"),
    "turnovers": ("tov", "turnovers"),
    "fg-pct": ("fg_pct", "fg_pct"),
    "three-pct": ("three_pct", "three_pct"),
    "ft-pct": ("ft_pct", "ft_pct"),
    "efg": ("efg_pct", "efg_pct"),
}

PERCENTAGE_SAMPLE_FILTERS = {
    "fg-pct": "AND games >= :min_games AND fga > 0",
    "three-pct": "AND games >= :min_games AND three_pa > 0",
    "ft-pct": "AND games >= :min_games AND fta > 0",
    "efg": "AND games >= :min_games AND fga > 0",
}


def get_leaderboard(metric: str, season: str, limit: int = 20) -> list[dict]:
    """Return a season leaderboard for a supported per-game or percentage metric."""
    if metric not in LEADERBOARD_METRICS:
        raise ValueError(f"Unsupported leaderboard metric: {metric}")

    column, alias = LEADERBOARD_METRICS[metric]
    limit = bounded_limit(limit)

    # Percentage leaderboards filter tiny samples to keep rankings meaningful.
    sample_filter = PERCENTAGE_SAMPLE_FILTERS.get(metric, "")

    query = f"""
        SELECT
            player_name,
            season,
            team,
            games,
            minutes_per_game,
            {column} AS {alias}
        FROM player_season_stats_raw
        WHERE season = :season
        {sample_filter}
        ORDER BY {column} DESC NULLS LAST
        LIMIT :limit
    """

    return fetch_all(query, {"season": season, "limit": limit, "min_games": 10})
