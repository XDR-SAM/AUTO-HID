"""AutoKey main user interface module.

Defines the primary tkinter application window, including text input,
send/abort controls, settings management, status display, and a worker
thread that hands text delivery off to :mod:`autokey.sender`.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
import pyautogui

from autokey.config import Settings
from autokey.sender import KeystrokeSender
from autokey.utils import init_logger, now_iso


SETTINGS_PATH = Path(__file__).with_name("settings.json")
LOG_PATH = Path(__file__).with_name("logs").joinpath("autokey.log")

DEFAULT_TEXT = ""


class App:
    """Main tkinter application window for the AutoKey GUI.

    Responsibilities include collecting text from the user, validating
    inputs, coordinating worker-thread sends via :class:`KeystrokeSender`,
    reflecting results back into the UI, and providing a modal
    settings editor.

    Attributes:
        root: Root ``tk.Tk`` window owning the interface.
        settings: Loaded runtime settings from :class:`autokey.config.Settings`.
        logger: File-backed :class:`logging.Logger` instance.
        sender: :class:`KeystrokeSender` instance used for the current send.
        worker: Background thread handle for the active send task, or ``None``.
        text_area: Scrollable text widget for user input.
        char_count_var: Current character count string bindable to labels.
        progress_var: Sending progress number between 0 and 100.
        progress: ``ttk.Progressbar`` widget driven by ``progress_var``.
        status_var: Human-readable status string bindable to status labels.
        start_btn: Action button to start sending.
        abort_btn: Action button to request cancellation of an active send.
        settings_btn: Action button to open the settings editor dialog.
    """

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the application window and connected components.

        Args:
            root: Root ``tk.Tk`` window to turn into the AutoKey UI.
        """
        self.root = root
        self.settings = Settings.load(SETTINGS_PATH)
        self.logger = init_logger(LOG_PATH)
        self.sender = KeystrokeSender(self.settings)
        self.worker: threading.Thread | None = None

        self.root.title("AutoKey Sender")
        self.root.geometry("640x520")
        self.root.minsize(520, 420)

        self._build_ui()
        self._bind_keys()
        self._status("Ready")
        self.logger.info("App started")

    def _build_ui(self) -> None:
        """Construct and pack all primary interface widgets."""
        pad = {"padx": 10, "pady": 6}

        top = ttk.Frame(self.root)
        top.pack(fill=tk.X, **pad)

        ttk.Label(top, text="Text to send:").pack(anchor=tk.W)

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=14)
        self.text_area.pack(fill=tk.BOTH, expand=True, **pad)
        self.text_area.insert("1.0", DEFAULT_TEXT)

        meta = ttk.Frame(self.root)
        meta.pack(fill=tk.X, **pad)

        self.char_count_var = tk.StringVar(value="chars: 0")
        ttk.Label(meta, textvariable=self.char_count_var).pack(side=tk.LEFT)

        self.text_area.bind("<<Modified>>", self._on_text_changed, add="+")

        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill=tk.X, **pad)

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill=tk.X, expand=True)

        self.status_var = tk.StringVar(value="Ready")
        status = ttk.Label(self.root, textvariable=self.status_var, foreground="#555")
        status.pack(anchor=tk.W, **pad)

        actions = ttk.Frame(self.root)
        actions.pack(fill=tk.X, **pad)

        self.start_btn = ttk.Button(actions, text="Start", command=self._on_start)
        self.start_btn.pack(side=tk.RIGHT)

        self.abort_btn = ttk.Button(actions, text="Abort", command=self._on_abort, state=tk.DISABLED)
        self.abort_btn.pack(side=tk.RIGHT, padx=6)

        self.settings_btn = ttk.Button(actions, text="Settings", command=self._open_settings)
        self.settings_btn.pack(side=tk.LEFT)

    def _bind_keys(self) -> None:
        """Bind keyboard shortcuts to application actions."""
        self.root.bind("<Escape>", lambda e: self._on_abort(), add="+")

    def _on_text_changed(self, event: tk.Event) -> None:
        """Update the live character count when the text widget content changes.

        Args:
            event: Tkinter widget event from the ``<<Modified>>`` virtual
                event emitted by the text area.
        """
        if event.widget is not self.text_area:
            return
        text = self.text_area.get("1.0", "end-1c")
        self.char_count_var.set(f"chars: {len(text)}")
        # keep modified flag valid without recursing
        try:
            self.text_area.edit_modified(False)
        except Exception:
            pass

    def _status(self, text: str) -> None:
        """Set the exposed status string shown in the status bar label.

        Args:
            text: Status message to display.
        """
        self.status_var.set(text)

    def _on_start(self) -> None:
        """Validate request state and user inputs, then begin a send.

        Disables controls, launches :meth:`_run_send` on a background
        thread, and updates UI state to reflect the pending operation.
        """
        if self.sender.is_running:
            messagebox.showwarning("Busy", "A send is already in progress.")
            return

        text = self.text_area.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showinfo("Nothing to send", "Paste or type some text first.")
            return

        if len(text) > int(self.settings.max_text_length):
            messagebox.showerror("Too long", f"Text exceeds max length: {self.settings.max_text_length} chars.")
            return

        if self.settings.fail_safe:
            if not messagebox.askyesno("Fail-safe", "PyAutoGUI fail-safe is enabled. Move mouse to top-left to abort. Continue?"):
                return

        if not messagebox.askyesno("Confirm send", f"Send {len(text)} characters in {self.settings.countdown_seconds}s?"):
            return

        self.sender = KeystrokeSender(self.settings)
        self.start_btn.config(state=tk.DISABLED)
        self.abort_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self._status("Starting...")
        self.text_area.config(state=tk.DISABLED)

        self.worker = threading.Thread(target=self._run_send, args=(text,), daemon=True)
        self.worker.start()

    def _run_send(self, text: str) -> None:
        """Execute the send on a worker thread and route progress to the UI.

        Args:
            text: Text payload to deliver via the sender.
        """
        def progress(msg: str) -> None:
            self.root.after(0, self._status, msg)

        result = self.sender.send(text, on_progress=progress)
        self.root.after(0, self._finish_send, result)

    def _finish_send(self, result) -> None:
        """Finalize UI state after the sender returns a result.

        Args:
            result: :class:`~autokey.sender.SendResult` returned from
                :meth:`KeystrokeSender.send`.
        """
        self.start_btn.config(state=tk.NORMAL)
        self.abort_btn.config(state=tk.DISABLED)
        self.text_area.config(state=tk.NORMAL)
        self.progress_var.set(100 if result.success else self.progress_var.get())

        if result.cancelled:
            self._status("Cancelled")
            self._append_log("cancelled")
            return

        if result.success:
            self._status(f"Sent {result.sent_chars} chars at {now_iso()}")
            self._append_log(f"sent {result.sent_chars} chars")
        else:
            self._status(f"Error: {result.error}")
            self._append_log(f"error: {result.error}")
            messagebox.showerror("Send failed", result.error or "Unknown error")

        if not self.settings.remember_text:
            self.text_area.delete("1.0", tk.END)
            self._on_text_changed(tk.Event())

    def _append_log(self, message: str) -> None:
        """Record a brief event message to the logger.

        Args:
            message: Short description of the UI event to log.
        """
        # hook for later file/history panel logging
        self.logger.info(message)

    def _on_abort(self) -> None:
        """Request cancellation of the active send if one is running."""
        if self.sender.is_running:
            self.sender.cancel()
            self._status("Cancelling...")

    def _open_settings(self) -> None:
        """Open the settings editor modal dialog."""
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("380x260")
        win.transient(self.root)
        win.grab_set()

        fields = {
            "countdown_seconds": ("Countdown seconds", int),
            "typing_interval": ("Typing interval", float),
            "max_text_length": ("Max text length", int),
        }

        entries = {}
        row = 0
        for key, (label, cast) in fields.items():
            ttk.Label(win, text=label).grid(row=row, column=0, sticky=tk.W, padx=10, pady=6)
            var = tk.StringVar(value=str(getattr(self.settings, key)))
            ttk.Entry(win, textvariable=var).grid(row=row, column=1, sticky=tk.EW, padx=10, pady=6)
            entries[key] = (var, cast)
            row += 1

        fail_var = tk.BooleanVar(value=bool(self.settings.fail_safe))
        remember_var = tk.BooleanVar(value=bool(self.settings.remember_text))
        ttk.Checkbutton(win, text="Fail-safe", variable=fail_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=6)
        row += 1
        ttk.Checkbutton(win, text="Remember text on send", variable=remember_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=6)
        row += 1

        def save() -> None:
            try:
                for key, (var, cast) in entries.items():
                    setattr(self.settings, key, cast(var.get()))
            except ValueError:
                messagebox.showerror("Invalid setting", "Use numeric values.")
                return
            self.settings.fail_safe = fail_var.get()
            self.settings.remember_text = remember_var.get()
            self.settings.save(SETTINGS_PATH)
            win.destroy()

        ttk.Button(win, text="Save", command=save).grid(row=row, column=0, columnspan=2, pady=10)

        win.columnconfigure(1, weight=1)


def main() -> None:
    """Launch the AutoKey GUI application."""
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
