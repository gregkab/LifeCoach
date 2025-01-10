# client/cli/__init__.py

from .commands import (
    fetch_logs,
    fetch_daily_logs,
    fetch_weekly_logs,
    add_log,
    get_daily_feedback,
    get_weekly_feedback,
)

__all__ = [
    "fetch_logs",
    "fetch_daily_logs",
    "fetch_weekly_logs",
    "add_log",
    "get_daily_feedback",
    "get_weekly_feedback",
]
