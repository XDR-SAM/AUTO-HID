"""AutoKey simple GUI module.

Provides a lightweight tkinter interface for quickly sending text as
simulated keystrokes using PyAutoGUI. This is the legacy standalone
program; the main application window lives in ``autokey.ui``.
"""

import tkinter as tk
from tkinter import scrolledtext
import pyautogui
import time
import threading


class KeystrokeSenderApp:
    """Minimal tkinter GUI for sending text input as keystrokes.

    The app presents a scrollable text area, a start button, and status
    indicators. Clicking ``Start`` disables the button, runs a 5-second
    countdown, then types the pasted text via PyAutoGUI.

    Attributes:
        root: The root ``tk.Tk`` application window hosting all widgets.
        text_area: Scrollable text widget used to collect text to type.
        start_button: Button that triggers the background sending thread.
        status_label: Label that displays countdown/send/error status.
        warning_label: Static label noting the countdown window for target-
            window focus.
    """

    def __init__(self, root):
        """Set up the main window and its widgets.

        Args:
            root: Root ``tk.Tk`` window to attach the UI to.
        """
        self.root = root
        root.title("Keystroke Sender")
        root.geometry("600x400")

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        """Build and pack all input, action, and status widgets."""
        # Label
        self.label = tk.Label(self.root, text="Paste your text below:")
        self.label.pack(pady=10)

        # Text input area with scrollbar
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=15)
        self.text_area.pack(padx=10, pady=5)

        # Start button
        self.start_button = tk.Button(self.root, text="Start Sending Keystrokes",
                                     command=self.start_sending_thread)
        self.start_button.pack(pady=15)

        # Status label
        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack()

        # Warning label
        self.warning_label = tk.Label(self.root,
                                    text="Note: After clicking the button, you have 5 seconds to focus the target window.",
                                    fg="red")
        self.warning_label.pack(pady=10)

    def start_sending_thread(self):
        """Validate input and begin the send operation on a worker thread.

        Disables the start button while the worker thread is active.
        """
        self.start_button.config(state=tk.DISABLED)
        self.status_label.config(text="Starting in 5 seconds...", fg="blue")

        # Get text from the text area
        text_to_send = self.text_area.get("1.0", tk.END).strip()

        if not text_to_send:
            self.status_label.config(text="No text to send!", fg="red")
            self.start_button.config(state=tk.NORMAL)
            return

        # Start the sending process in a new thread
        thread = threading.Thread(target=self.send_keystrokes, args=(text_to_send,))
        thread.start()

    def send_keystrokes(self, text):
        """Run the 5-second countdown then emit keystrokes via PyAutoGUI.

        All GUI mutations are scheduled on the main thread using
        ``root.after`` because this method executes on the worker thread.

        Args:
            text: The string to send as simulated keyboard input.
        """
        # Countdown
        for i in range(5, 0, -1):
            self.root.after(0, self.update_status, f"Starting in {i} seconds...")
            time.sleep(1)

        # Get the text again in case it changed during the delay
        text_to_send = self.text_area.get("1.0", tk.END).strip()

        # Send the text
        try:
            self.root.after(0, self.update_status, "Sending keystrokes...", "green")
            pyautogui.write(text_to_send, interval=0.05)
            self.root.after(0, self.update_status, "Keystrokes sent successfully!", "green")
        except Exception as e:
            self.root.after(0, self.update_status, f"Error: {str(e)}", "red")
        finally:
            self.root.after(0, self.enable_button)

    def update_status(self, message, color="blue"):
        """Update the status label with the given message and color.

        Args:
            message: Human-readable status text to display.
            color: Tk color string for the label text.
        """
        self.status_label.config(text=message, fg=color)

    def enable_button(self):
        """Re-enable the start button after send completes or fails."""
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeystrokeSenderApp(root)
    
    # Add a note about dependencies
    note = tk.Label(root, 
                   text="Note: This program requires pyautogui. Install with: pip install pyautogui",
                   fg="gray")
    note.pack(side=tk.BOTTOM, pady=5)
    
    root.mainloop()