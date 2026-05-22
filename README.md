# NBA Player Stats Analyzer

NBA analytics project for exploring player season performance, leaderboards, custom impact metrics, Most Improved Player candidates, fantasy rankings, and player comparisons.

The project started as a CSV/Pandas notebook workflow and now includes a SQL-backed FastAPI backend using PostgreSQL, SQLAlchemy, and NBA API data loaded through an ETL pipeline. Legacy notebooks and visualizations are preserved for reference while the backend provides reusable API endpoints for future frontend integration.

## Current Stack

- Python
- Pandas
- PostgreSQL
- FastAPI
- SQLAlchemy
- NBA API
- Matplotlib

## Project Structure

```text
nba-stats-analyzer/
├── backend/
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── routers/
│       │   ├── players.py
│       │   ├── leaderboards.py
│       │   ├── analytics.py
│       │   └── comparisons.py
│       ├── services/
│       │   ├── player_service.py
│       │   ├── leaderboard_service.py
│       │   ├── analytics_service.py
│       │   └── comparison_service.py
│       ├── utils/
│       │   ├── metrics.py
│       │   └── helpers.py
│       └── etl/
│           └── load_nba_api_to_db.py
├── legacy/
│   ├── 01_cleaned_data.ipynb
│   ├── analysis.ipynb
│   ├── Fantasy_Value_Calculator.ipynb
│   ├── MIP_Detector.ipynb
│   └── Player_Stat_Lookup.ipynb
├── data/
│   ├── raw/
│   └── processed/
├── visualizations/
│   ├── figures/
│   └── top_contracts_bar_charts.py
└── README.md
```

## Backend Architecture

The FastAPI backend is organized around thin routers and reusable service modules:

- `main.py` registers the API routes and exposes `/health`.
- `database.py` owns the PostgreSQL SQLAlchemy engine.
- `routers/` contains endpoint definitions.
- `services/` contains SQL-backed business logic.
- `utils/metrics.py` centralizes impact score and fantasy score formulas.
- `utils/helpers.py` contains shared query/serialization helpers.
- `etl/load_nba_api_to_db.py` pulls player season stats from `nba_api`, cleans the data, calculates shooting metrics, and loads PostgreSQL.

The primary database table is:

```text
player_season_stats_raw
```

Key columns include:

```text
season, player_name, age, team, games, minutes_per_game,
fg, fga, fg_pct, three_p, three_pa, three_pct,
two_p, two_pa, two_pct, efg_pct,
ft, fta, ft_pct, orb, drb, trb,
ast, stl, blk, tov, pf, pts
```

## API Endpoints

### Health

```http
GET /health
```

### Players

```http
GET /players/search?name=lebron
GET /players/search?name=lebron&season=2024-25&limit=10
GET /players/profile?name=LeBron James
GET /players/profile?name=LeBron James&season=2024-25
GET /players/history?name=LeBron James
GET /players/compare?player_one=LeBron James&player_two=Stephen Curry&season=2024-25
```

### Leaderboards

```http
GET /leaderboards/points?season=2024-25
GET /leaderboards/rebounds?season=2024-25
GET /leaderboards/assists?season=2024-25
GET /leaderboards/steals?season=2024-25
GET /leaderboards/blocks?season=2024-25
GET /leaderboards/turnovers?season=2024-25
GET /leaderboards/fg-pct?season=2024-25
GET /leaderboards/three-pct?season=2024-25
GET /leaderboards/ft-pct?season=2024-25
GET /leaderboards/efg?season=2024-25
```

All leaderboard endpoints accept an optional `limit` query parameter:

```http
GET /leaderboards/points?season=2024-25&limit=25
```

### Analytics

```http
GET /analytics/impact-score?season=2024-25
GET /analytics/mip
GET /analytics/fantasy-rankings?season=2024-25
```

Analytics endpoints also accept optional `limit` parameters:

```http
GET /analytics/mip?limit=10
GET /analytics/fantasy-rankings?season=2024-25&limit=50
```

## Metrics

Custom formulas are centralized in `backend/app/utils/metrics.py`.

Impact score:

```python
impact_score = (
    pts
    + trb * 1.2
    + ast * 1.5
    + stl * 3.0
    + blk * 3.0
    + efg_pct * 10.0
    - tov * 1.5
)
```

Fantasy score:

```python
fantasy_score = (
    pts
    + trb * 1.2
    + ast * 1.5
    + stl * 3.0
    + blk * 3.0
    - tov
)
```

Most Improved Player detection compares impact score changes across consecutive seasons using SQL window functions.

## Running the Backend

Create and activate a virtual environment, then install the project dependencies used by the backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary pandas nba_api
```

Start PostgreSQL and make sure this database exists:

```text
nba_stats_db
```

The current database connection is defined in `backend/app/database.py`:

```python
DATABASE_URL = "postgresql://localhost:5432/nba_stats_db"
```

Load or refresh NBA API data:

```bash
python backend/app/etl/load_nba_api_to_db.py
```

Run the FastAPI server:

```bash
uvicorn backend.app.main:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## Legacy Notebook Features

The `legacy/` folder preserves the original CSV/Pandas workflows:

- Fantasy Value Calculator
- Most Improved Player Detector
- Player Stat Lookup Tool
- League-wide trends, correlations, and averages
- Multi-season CSV cleaning and combining

These notebooks are useful references for validating or expanding the SQL-backed API.

## Visualizations

`visualizations/top_contracts_bar_charts.py` generates side-by-side charts for top value contracts and worst value contracts.

Run:

```bash
python3 visualizations/top_contracts_bar_charts.py
```

The script saves charts under:

```text
visualizations/figures/
```

## Development Notes

- Existing working endpoints were preserved and extended.
- SQL queries are preferred for backend analytics instead of loading large datasets into Pandas at request time.
- Routers should stay thin; reusable logic belongs in `services/`.
- Metric formulas should stay centralized in `utils/metrics.py`.
- The API is structured for future React integration, but this repository currently focuses only on backend analytics and data workflows.
