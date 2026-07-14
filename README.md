# AutoKey Sender

![Windows](https://img.shields.io/badge/Windows-10%20%2F%2011-0078D6?logo=windows)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Build](https://img.shields.io/badge/build-EXE-success)

**AutoKey Sender** is a lightweight, offline-first Windows desktop tool that types text into the active window for you. No cloud, no background services, no telemetry — just local keystroke automation.

---

## Why AutoKey Sender

Most automation tools require installers, cloud logins, or complex scripting. AutoKey Sender is built for simple, fast, local use:

- Works completely **offline**
- **No installation** required — run the EXE directly
- **No app store account**, no telemetry, no background processes
- **Safety-first design**: countdown, abort, fail-safe, input limits

---

## Features

- **Offline by default** — all processing happens on your machine
- **No-install EXE** — portable `autokey.exe` for any Windows PC
- **Countdown timer** — gives you time to focus the target window
- **Abort control** — stop sending mid-run via button or `Esc`
- **Configurable timing** — adjust countdown seconds and typing interval
- **Settings persistence** — remembers your preferences between sessions
- **Local logging** — send history written to file for debugging
- **Fail-safe mode** — PyAutoGUI top-left corner emergency stop
- **Lightweight GUI** — built with Tkinter, fast startup, small bundle

---

## Quick Start

### Option A: Portable EXE (recommended)

Download `autokey.exe` from the latest release and double-click it. No Python, no installer needed.

### Option B: Run from source

```bash
git clone https://github.com/XDR-SAM/AUTO-HID.git
cd AUTO-HID
python -m autokey.ui
```

### Option C: Install package

```bash
pip install -e .
autokey
```

---

## Building the EXE

```bash
pip install -e .[exe-build]
python build/build_exe.py
```

Output: `dist/autokey.exe`

---

## Usage

1. **Paste or type text** into the main text area.
2. Click **Start**.
3. **Switch focus** to the target window during the countdown.
4. App types the text at the configured interval.
5. Click **Abort** or press **Esc** to stop at any time.

### Settings

- **Countdown seconds** — delay before typing starts
- **Typing interval** — seconds between keystrokes
- **Max text length** — enforced limit to prevent runaway automation
- **Fail-safe** — move mouse to top-left screen corner to emergency-stop

Open **Settings** from the toolbar to adjust values. Preferences are saved to `settings.json` next to the app.

---

## Project Structure

```
AUTO-HID/
  ├── src/autokey/
  │   ├── __init__.py
  │   ├── config.py         # Settings dataclass, load/save
  │   ├── sender.py         # Keystroke sending logic
  │   ├── ui.py             # Tkinter GUI
  │   ├── utils.py          # Logging and time helpers
  │   └── _legacy_prog.py   # Original MVP for reference
  ├── build/
  │   └── build_exe.py      # PyInstaller packaging script
  ├── docs/
  │   ├── USAGE.md          # End-user guide
  │   └── ARCHITECTURE.md   # Design and module overview
  ├── pyproject.toml        # Packaging metadata
  ├── README.md
  └── LICENSE
```

---

## Contributing

Contributions are welcome.

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-change`
3. Commit your changes: `git commit -m "feat: my change"`
4. Push to the branch: `git push origin feat/my-change`
5. Open a Pull Request

Please keep changes focused and update documentation when behavior changes.

---

## License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.
