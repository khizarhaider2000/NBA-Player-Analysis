from backend.app.services.player_service import BASE_PLAYER_COLUMNS
from backend.app.utils.helpers import fetch_all
from backend.app.utils.metrics import fantasy_score_sql, impact_score_sql


def compare_players(player_one: str, player_two: str, season: str) -> dict:
    """Return side-by-side player season rows plus useful score deltas."""
    impact_score = impact_score_sql()
    fantasy_score = fantasy_score_sql()

    query = f"""
        WITH player_one AS (
            SELECT
                1 AS sort_order,
                {BASE_PLAYER_COLUMNS},
                ROUND(({impact_score})::numeric, 2) AS impact_score,
                ROUND(({fantasy_score})::numeric, 2) AS fantasy_score
            FROM player_season_stats_raw
            WHERE season = :season
                AND LOWER(player_name) LIKE LOWER(:player_one)
            ORDER BY
                CASE WHEN LOWER(player_name) = LOWER(:player_one_exact) THEN 0 ELSE 1 END,
                player_name
            LIMIT 1
        ),
        player_two AS (
            SELECT
                2 AS sort_order,
                {BASE_PLAYER_COLUMNS},
                ROUND(({impact_score})::numeric, 2) AS impact_score,
                ROUND(({fantasy_score})::numeric, 2) AS fantasy_score
            FROM player_season_stats_raw
            WHERE season = :season
                AND LOWER(player_name) LIKE LOWER(:player_two)
            ORDER BY
                CASE WHEN LOWER(player_name) = LOWER(:player_two_exact) THEN 0 ELSE 1 END,
                player_name
            LIMIT 1
        )
        SELECT
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
            efg_pct,
            impact_score,
            fantasy_score
        FROM (
            SELECT * FROM player_one
            UNION ALL
            SELECT * FROM player_two
        ) players
        ORDER BY sort_order
    """

    rows = fetch_all(
        query,
        {
            "season": season,
            "player_one": f"%{player_one}%",
            "player_two": f"%{player_two}%",
            "player_one_exact": player_one,
            "player_two_exact": player_two,
        },
    )

    comparison = {
        "season": season,
        "players": rows,
        "deltas": {},
    }

    if len(rows) == 2:
        left, right = rows
        comparison["deltas"] = {
            "player_name": f"{left['player_name']} - {right['player_name']}",
            "pts": round(left["pts"] - right["pts"], 2),
            "trb": round(left["trb"] - right["trb"], 2),
            "ast": round(left["ast"] - right["ast"], 2),
            "impact_score": round(left["impact_score"] - right["impact_score"], 2),
            "fantasy_score": round(left["fantasy_score"] - right["fantasy_score"], 2),
        }

    return comparison
