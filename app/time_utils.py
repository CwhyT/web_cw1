from datetime import UTC, datetime


def current_utc() -> datetime:
    return datetime.now(UTC)
