"""AutoKey sender module.

Wraps PyAutoGUI keystroke delivery with cancellation support, pre-send
countdown behavior, and a lightweight result object for success/failure
reporting back to the UI layer.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Callable, Optional

import pyautogui


@dataclass
class SendResult:
    """Outcome container for a single send operation.

    Attributes:
        success: ``True`` if the text was sent without an exception.
        sent_chars: Number of characters successfully transmitted, or 0 on
            failure/cancellation.
        cancelled: ``True`` if the user cancelled the send before it reached
            the typing stage.
        error: Human-readable error description when ``success`` is ``False``
            and the operation was not cancelled.
    """
    success: bool
    sent_chars: int
    cancelled: bool
    error: Optional[str] = None


class KeystrokeSender:
    """Sends text as keystrokes using PyAutoGUI.

    Instances manage a single in-flight send, exposing cancellation through
    a threading Event so callers can abort from another thread or callback
    safely.

    Attributes:
        settings: Runtime settings controlling countdown, interval, and
            fail-safe behavior.
    """

    def __init__(self, settings) -> None:
        """Initialize the sender with application settings.

        Args:
            settings: Settings object with attributes such as
                ``countdown_seconds``, ``typing_interval``, and
                ``fail_safe``.
        """
        self.settings = settings
        self._cancel_event = threading.Event()
        self._running = False

    @property
    def is_running(self) -> bool:
        """Whether a send operation is currently in progress."""
        return self._running

    @property
    def is_cancelled(self) -> bool:
        """Whether the current send was requested to cancel."""
        return self._cancel_event.is_set()

    def cancel(self) -> None:
        """Request cancellation of the current send operation."""
        self._cancel_event.set()

    def send(self, text: str, on_progress: Optional[Callable[[str], None]] = None) -> SendResult:
        """Send ``text`` as simulated keyboard input.

        A countdown is emitted via ``on_progress`` before typing begins.
        If cancellation is requested during countdown or typing, the
        operation stops early and reports ``cancelled=True``.

        Args:
            text: The text to send as keyboard input.
            on_progress: Optional callback receiving human-readable status
                strings during countdown/send for UI updates.

        Returns:
            A ``SendResult`` describing whether the send succeeded,
            was cancelled, or failed with an error.
        """
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
