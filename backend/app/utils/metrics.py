"""Reusable NBA metric formulas shared by analytics services and SQL queries."""


def impact_score_sql() -> str:
    """Production query fragment for the custom all-around impact score."""
    return """
        (
            COALESCE(pts, 0)
            + COALESCE(trb, 0) * 1.2
            + COALESCE(ast, 0) * 1.5
            + COALESCE(stl, 0) * 3.0
            + COALESCE(blk, 0) * 3.0
            + COALESCE(efg_pct, 0) * 10.0
            - COALESCE(tov, 0) * 1.5
        )
    """


def fantasy_score_sql() -> str:
    """Standard fantasy-style per-game score used for rankings."""
    return """
        (
            COALESCE(pts, 0)
            + COALESCE(trb, 0) * 1.2
            + COALESCE(ast, 0) * 1.5
            + COALESCE(stl, 0) * 3.0
            + COALESCE(blk, 0) * 3.0
            - COALESCE(tov, 0)
        )
    """


def calculate_impact_score(
    pts: float = 0,
    trb: float = 0,
    ast: float = 0,
    stl: float = 0,
    blk: float = 0,
    tov: float = 0,
    efg_pct: float = 0,
) -> float:
    return pts + trb * 1.2 + ast * 1.5 + stl * 3.0 + blk * 3.0 + efg_pct * 10.0 - tov * 1.5


def calculate_fantasy_score(
    pts: float = 0,
    trb: float = 0,
    ast: float = 0,
    stl: float = 0,
    blk: float = 0,
    tov: float = 0,
) -> float:
    return pts + trb * 1.2 + ast * 1.5 + stl * 3.0 + blk * 3.0 - tov
