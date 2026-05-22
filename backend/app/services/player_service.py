from backend.app.utils.helpers import bounded_limit, fetch_all


BASE_PLAYER_COLUMNS = """
    season,
    player_name,
    age,
    team,
    games,
    minutes_per_game,
    pts,
    trb,
    ast,
    stl,
    blk,
    tov,
    fg_pct,
    three_pct,
    ft_pct,
    efg_pct
"""


def search_players(name: str, season: str | None = None, limit: int = 20) -> list[dict]:
    """Search player seasons by name, optionally scoped to one NBA season."""
    limit = bounded_limit(limit)
    season_filter = "AND season = :season" if season else ""

    query = f"""
        SELECT player_name, season, pts
        FROM player_season_stats_raw
        WHERE LOWER(player_name) LIKE LOWER(:name)
        {season_filter}
        ORDER BY season DESC, player_name
        LIMIT :limit
    """

    params = {"name": f"%{name}%", "season": season, "limit": limit}
    return fetch_all(query, params)


def get_player_profile(name: str, season: str | None = None) -> dict | None:
    """Return one player-season profile, using the latest loaded season by default."""
    season_filter = "AND season = :season" if season else ""

    query = f"""
        SELECT {BASE_PLAYER_COLUMNS}
        FROM player_season_stats_raw
        WHERE LOWER(player_name) LIKE LOWER(:name)
        {season_filter}
        ORDER BY season DESC, player_name
        LIMIT 1
    """

    rows = fetch_all(query, {"name": f"%{name}%", "season": season})
    return rows[0] if rows else None


def get_player_history(name: str) -> list[dict]:
    """Return all loaded seasons for a player in chart-ready chronological order."""
    query = f"""
        SELECT {BASE_PLAYER_COLUMNS}
        FROM player_season_stats_raw
        WHERE LOWER(player_name) LIKE LOWER(:name)
        ORDER BY season
    """

    return fetch_all(query, {"name": f"%{name}%"})
