from sqlalchemy import create_engine

DATABASE_URL = "postgresql://localhost:5432/nba_stats_db"

engine = create_engine(DATABASE_URL)

