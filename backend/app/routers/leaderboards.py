from fastapi import APIRouter

from backend.app.services.leaderboard_service import get_leaderboard

router = APIRouter()


@router.get("/leaderboards/points")
def get_points_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("points", season, limit)


@router.get("/leaderboards/rebounds")
def get_rebounds_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("rebounds", season, limit)


@router.get("/leaderboards/assists")
def get_assists_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("assists", season, limit)


@router.get("/leaderboards/steals")
def get_steals_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("steals", season, limit)


@router.get("/leaderboards/blocks")
def get_blocks_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("blocks", season, limit)


@router.get("/leaderboards/turnovers")
def get_turnovers_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("turnovers", season, limit)


@router.get("/leaderboards/fg-pct")
def get_fg_pct_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("fg-pct", season, limit)


@router.get("/leaderboards/three-pct")
def get_three_pct_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("three-pct", season, limit)


@router.get("/leaderboards/ft-pct")
def get_ft_pct_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("ft-pct", season, limit)


@router.get("/leaderboards/efg")
def get_efg_leaderboard(season: str, limit: int = 20):
    return get_leaderboard("efg", season, limit)
