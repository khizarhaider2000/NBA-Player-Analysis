from fastapi import APIRouter, HTTPException

from backend.app.services import player_service

router = APIRouter()


@router.get("/players/search")
def search_players(name: str, season: str | None = None, limit: int = 20):
    return player_service.search_players(name=name, season=season, limit=limit)


@router.get("/players/profile")
def get_player_profile(name: str, season: str | None = None):
    profile = player_service.get_player_profile(name=name, season=season)

    if profile is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return profile


@router.get("/players/history")
def get_player_history(name: str):
    history = player_service.get_player_history(name=name)

    if not history:
        raise HTTPException(status_code=404, detail="Player not found")

    return history
