# AutoKey Sender

Local keystroke automation for Windows. Run macros, send keys, and automate repetitive input without needing an app store account, cloud login, or internet access.

## Description

AutoKey Sender is a lightweight desktop tool that sends keystrokes and automates local input on Windows. It is designed to run completely offline, making it suitable for automation workflows where security, control, and simplicity matter.

## Features

- Local keyboard automation with no cloud or background services required
- Run directly from source without installation
- Installable as a Python package for regular use
- Standalone EXE build included for portability
- Dev/test workflow with `pytest`

## Installation

### From source

```bash
git clone https://github.com/<your-org>/autokey.git
cd autokey
pip install -e .
```

### No-install run

You can run it without installing the package:

```bash
python -m autokey.ui
```

## Usage

After installation or when running from source, start the UI:

```bash
autokey-ui
```

or

```bash
python -m autokey.ui
```

## Building EXE

Build a standalone Windows executable:

```bash
pip install -e .[exe-build]
python build/build_exe.py
```

Output: `dist/autokey.exe`

## Screenshots / Demo

> Replace this placeholder with screenshots or a short demo GIF showing the UI and macro playback.

- Add screenshots to the `docs/` or `assets/` folder and embed them here.
- A quick GIF of sending a macro or configuring a hotkey works well.

## Project Structure

```
autokey/
├── README.md
├── pyproject.toml / setup.cfg
├── build/
│   └── build_exe.py
├── autokey/
│   └── ui/
└── tests/
```

Adjust this tree to match the actual source layout if needed.

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-macro`
3. Install dev dependencies:

```bash
pip install -e ".[dev]"
pytest
```

4. Commit your changes and open a pull request

## License

MIT
