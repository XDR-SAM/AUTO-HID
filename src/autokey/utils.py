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
    return datetime.now().isoformat(timespec="seconds")
