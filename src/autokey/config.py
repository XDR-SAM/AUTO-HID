"""AutoKey configuration module.

Provides the settings model and persistence layer for the application,
including load/save helpers that tolerate missing or malformed files.
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict


DEFAULT_SETTINGS = {
    "countdown_seconds": 5,
    "typing_interval": 0.05,
    "max_text_length": 50000,
    "fail_safe": True,
    "remember_text": False,
}


@dataclass
class Settings:
    """Application settings dataclass.

    Attributes:
        countdown_seconds: Number of seconds to wait before sending keystrokes.
        typing_interval: Delay in seconds between each keystroke sent by PyAutoGUI.
        max_text_length: Maximum number of characters allowed in a single send.
        fail_safe: Whether to enable PyAutoGUI fail-safe mode.
        remember_text: Whether to preserve the text field contents after sending.
    """

    countdown_seconds: int = 5
    typing_interval: float = 0.05
    max_text_length: int = 50000
    fail_safe: bool = True
    remember_text: bool = False

    @classmethod
    def load(cls, path: str | Path) -> "Settings":
        """Load settings from a JSON-encoded file.

        If the file does not exist or cannot be parsed, the default settings
        are returned instead.

        Args:
            path: Filesystem path to the settings JSON file.

        Returns:
            A populated ``Settings`` instance.
        """
        p = Path(path)
        if not p.exists():
            return cls()
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return cls(**{**DEFAULT_SETTINGS, **data})
        except Exception:
            return cls()

    def save(self, path: str | Path) -> None:
        """Serialize settings to a JSON file.

        Args:
            path: Filesystem path where the settings JSON file will be written.
        """
        p = Path(path)
        p.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
