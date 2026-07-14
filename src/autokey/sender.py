from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Callable, Optional

import pyautogui


@dataclass
class SendResult:
    success: bool
    sent_chars: int
    cancelled: bool
    error: Optional[str] = None


class KeystrokeSender:
    def __init__(self, settings) -> None:
        self.settings = settings
        self._cancelled = threading.Event()
        self._running = threading.Event()

    @property
    def is_running(self) -> bool:
        return self._running.is_set()

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled.is_set()

    def cancel(self) -> None:
        self._cancelled.set()

    def send(self, text: str, on_progress: Optional[Callable[[str], None]] = None) -> SendResult:
        if self._running.is_set():
            return SendResult(success=False, sent_chars=0, cancelled=False, error="Sender already running.")

        self._running.set()
        self._cancelled.clear()

        pyautogui.FAILSAFE = bool(self.settings.fail_safe)

        countdown = int(self.settings.countdown_seconds)
        for i in range(countdown, 0, -1):
            if self._cancelled.is_set():
                self._running.clear()
                return SendResult(success=False, sent_chars=0, cancelled=True)
            if on_progress:
                on_progress(f"Starting in {i}...")
            threading.Event().wait(1.0)

        try:
            if on_progress:
                on_progress("Sending...")
            pyautogui.write(text, interval=float(self.settings.typing_interval))
            self._running.clear()
            return SendResult(success=True, sent_chars=len(text), cancelled=False)
        except Exception as exc:  # pragma: no cover
            self._running.clear()
            return SendResult(success=False, sent_chars=0, cancelled=False, error=str(exc))
