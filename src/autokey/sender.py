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
        self._cancel_event = threading.Event()
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def is_cancelled(self) -> bool:
        return self._cancel_event.is_set()

    def cancel(self) -> None:
        self._cancel_event.set()

    def send(self, text: str, on_progress: Optional[Callable[[str], None]] = None) -> SendResult:
        if self._running:
            return SendResult(success=False, sent_chars=0, cancelled=False, error="Sender already running.")

        self._running = True
        self._cancel_event.clear()

        if getattr(self.settings, "fail_safe", True):
            pyautogui.FAILSAFE = True

        try:
            countdown = int(getattr(self.settings, "countdown_seconds", 5))
            for i in range(countdown, 0, -1):
                if self._cancel_event.is_set():
                    self._running = False
                    return SendResult(success=False, sent_chars=0, cancelled=True)
                if on_progress:
                    on_progress(f"Starting in {i}...")
                threading.Event().wait(1.0)

            if self._cancel_event.is_set():
                self._running = False
                return SendResult(success=False, sent_chars=0, cancelled=True)

            if on_progress:
                on_progress("Sending...")
            pyautogui.write(text, interval=float(getattr(self.settings, "typing_interval", 0.05)))
            self._running = False
            return SendResult(success=True, sent_chars=len(text), cancelled=False)
        except Exception as exc:  # pragma: no cover
            self._running = False
            return SendResult(success=False, sent_chars=0, cancelled=False, error=str(exc))
