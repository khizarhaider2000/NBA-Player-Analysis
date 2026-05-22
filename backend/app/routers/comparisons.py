from fastapi import APIRouter, HTTPException

from backend.app.services.comparison_service import compare_players

router = APIRouter()


@router.get("/players/compare")
def compare_player_seasons(player_one: str, player_two: str, season: str):
    comparison = compare_players(
        player_one=player_one,
        player_two=player_two,
        season=season,
    )

    if len(comparison["players"]) < 2:
        raise HTTPException(
            status_code=404,
            detail="Could not find both players for the requested season",
        )

    return comparison
