"""AutoKey utility helpers.

Provides logging initialization and time formatting utilities reused
across the application.
"""

import os
import sys
import time
import threading
import logging
from datetime import datetime
from pathlib import Path
from logging import Logger

from autokey.config import Settings


def init_logger(log_path: str | Path) -> Logger:
    """Create a file-backed logger for the application.

    The logger always writes to a UTF-8 log file; parent directories are
    created automatically.

    Args:
        log_path: Destination log file path.

    Returns:
        Configured stdlib ``Logger`` instance with a single ``FileHandler``
        attached.
    """
    # Use stdlib here so the app has zero extra dependency friction.
    log = Logger("autokey")
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(str(log_path), encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    return log


def now_iso() -> str:
    """Return the current local time formatted as ISO 8601 without microseconds.

    Returns:
        Current timestamp string using ``datetime.isoformat(timespec='seconds')``.
    """
    return datetime.now().isoformat(timespec="seconds")
