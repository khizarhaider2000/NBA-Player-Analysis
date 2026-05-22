from fastapi import APIRouter

from backend.app.services import analytics_service

router = APIRouter()


@router.get("/analytics/impact-score")
def get_impact_score_leaderboard(season: str, limit: int = 20):
    return analytics_service.get_impact_scores(season=season, limit=limit)


@router.get("/analytics/mip")
def get_most_improved_players(limit: int = 20):
    return analytics_service.get_most_improved_players(limit=limit)


@router.get("/analytics/fantasy-rankings")
def get_fantasy_rankings(season: str, limit: int = 20):
    return analytics_service.get_fantasy_rankings(season=season, limit=limit)
