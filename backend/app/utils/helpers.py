from decimal import Decimal
from typing import Any

from sqlalchemy import text

from backend.app.database import engine


def rows_to_dicts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize database values into JSON-friendly dictionaries."""
    records = []

    for row in rows:
        record = {}
        for key, value in row.items():
            if isinstance(value, Decimal):
                record[key] = float(value)
            else:
                record[key] = value
        records.append(record)

    return records


def fetch_all(query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Execute a read-only SQL query and return JSON-ready row dictionaries."""
    with engine.connect() as connection:
        result = connection.execute(text(query), params or {})
        rows = [dict(row) for row in result.mappings().all()]

    return rows_to_dicts(rows)


def bounded_limit(limit: int, default: int = 20, maximum: int = 100) -> int:
    """Keep API result sizes predictable while allowing frontend-driven limits."""
    if limit <= 0:
        return default

    return min(limit, maximum)
