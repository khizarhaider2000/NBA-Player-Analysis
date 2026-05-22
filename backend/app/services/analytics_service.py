from backend.app.utils.helpers import bounded_limit, fetch_all
from backend.app.utils.metrics import fantasy_score_sql, impact_score_sql


def get_impact_scores(season: str, limit: int = 20) -> list[dict]:
    """Rank players by the centralized custom impact score formula."""
    limit = bounded_limit(limit)
    impact_score = impact_score_sql()

    query = f"""
        SELECT
            player_name,
            season,
            team,
            games,
            minutes_per_game,
            pts,
            trb,
            ast,
            stl,
            blk,
            tov,
            efg_pct,
            ROUND(({impact_score})::numeric, 2) AS impact_score
        FROM player_season_stats_raw
        WHERE season = :season
        ORDER BY impact_score DESC NULLS LAST
        LIMIT :limit
    """

    return fetch_all(query, {"season": season, "limit": limit})


def get_most_improved_players(limit: int = 20) -> list[dict]:
    """Compare consecutive loaded seasons and return the biggest impact jumps."""
    limit = bounded_limit(limit)
    impact_score = impact_score_sql()

    query = f"""
        WITH scored AS (
            SELECT
                player_name,
                season,
                team,
                games,
                SUBSTRING(season FROM 1 FOR 4)::int AS season_start,
                ROUND(({impact_score})::numeric, 2) AS impact_score,
                LAG(season) OVER (
                    PARTITION BY player_name
                    ORDER BY season
                ) AS previous_season,
                LAG(SUBSTRING(season FROM 1 FOR 4)::int) OVER (
                    PARTITION BY player_name
                    ORDER BY season
                ) AS previous_season_start,
                LAG(ROUND(({impact_score})::numeric, 2)) OVER (
                    PARTITION BY player_name
                    ORDER BY season
                ) AS previous_impact_score
            FROM player_season_stats_raw
        )
        SELECT
            player_name,
            previous_season,
            season,
            team,
            previous_impact_score,
            impact_score,
            ROUND((impact_score - previous_impact_score)::numeric, 2) AS impact_score_change
        FROM scored
        WHERE previous_impact_score IS NOT NULL
            AND season_start = previous_season_start + 1
            AND impact_score > previous_impact_score
        ORDER BY impact_score_change DESC NULLS LAST
        LIMIT :limit
    """

    return fetch_all(query, {"limit": limit})


def get_fantasy_rankings(season: str, limit: int = 20) -> list[dict]:
    """Rank player seasons by the centralized fantasy scoring formula."""
    limit = bounded_limit(limit)
    fantasy_score = fantasy_score_sql()

    query = f"""
        SELECT
            player_name,
            season,
            team,
            games,
            minutes_per_game,
            pts,
            trb,
            ast,
            stl,
            blk,
            tov,
            ROUND(({fantasy_score})::numeric, 2) AS fantasy_score
        FROM player_season_stats_raw
        WHERE season = :season
        ORDER BY fantasy_score DESC NULLS LAST
        LIMIT :limit
    """

    return fetch_all(query, {"season": season, "limit": limit})
