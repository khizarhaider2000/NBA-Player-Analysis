from fastapi import FastAPI
from backend.app.routers.players import router as players_router
from backend.app.routers.leaderboards import router as leaderboards_router
from backend.app.routers.analytics import router as analytics_router
from backend.app.routers.comparisons import router as comparisons_router



app = FastAPI()

app.include_router(players_router)
app.include_router(leaderboards_router)
app.include_router(analytics_router)
app.include_router(comparisons_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
