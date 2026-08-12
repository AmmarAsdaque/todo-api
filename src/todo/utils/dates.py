"""Date helpers."""

from datetime import datetime


def parse_date(raw):
    """Parse a YYYY-MM-DD string into a date. Raises ValueError on bad input."""
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError(f"not a YYYY-MM-DD date: {raw!r}") from None
