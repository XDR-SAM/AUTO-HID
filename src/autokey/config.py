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
    countdown_seconds: int = 5
    typing_interval: float = 0.05
    max_text_length: int = 50000
    fail_safe: bool = True
    remember_text: bool = False

    @classmethod
    def load(cls, path: str | Path) -> "Settings":
        p = Path(path)
        if not p.exists():
            return cls()
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return cls(**{**DEFAULT_SETTINGS, **data})
        except Exception:
            return cls()

    def save(self, path: str | Path) -> None:
        p = Path(path)
        p.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
