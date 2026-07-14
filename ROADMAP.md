# AutoKey Roadmap

Current state: `v0.1 — MVP` (`prog.py`)
Goal: production-ready local keystroke automation app with safety, reliability, and extensibility.

---

## 0 — Safety & UX Foundations (v0.2)
- Countdown timer **on main thread** via `root.after` instead of worker sleep
- **Abort / stop** button during send
- Input length cap with warning before send
- Clear status states: `idle`, `pending`, `sending`, `done`, `error`
- Keyboard shortcut to cancel: `Esc` while running
- Remember last-used settings in local config file (`settings.json`)

## 1 — Input & Output Flexibility (v0.3)
- File input: load `.txt` and `.md` directly
- Line-by-line mode with optional per-line delay
- Hotkey insertion proxy for real special keys: `{TAB}`, `{ENTER}`, `{ESC}`, `{CTRL}`
- Send to clipboard then paste as fallback path for unsupported chars
- Repeat/count control: send N times with configurable spacing

## 2 — Profiles & Templates (v0.4)
- Save named templates: common passwords, boilerplate text, code snippets
- Quick-select list in UI
- Import/export templates as JSON
- Default template shipped in repo

## 3 — Reliability & Observability (v0.5)
- Structured local logging to `logs/autokey.log`
- Dry-run mode preview (show chars to send without sending)
- Fail-safe: fail-safe PyAutoGUI `fail-safe` toggle with confirmation dialog
- Exception categories: `fatal`, `recoverable`, `timed-out`
- Crash-recovery on restart: resume sending or restart last job

## 4 — Engineering Hardening (v0.6)
- Refactor to `app/` package layout
- Config module, sender module, ui module
- Unit tests for parser, sender stubs, config load
- Build/packaging: PyInstaller or Nuitka single exe
- Windows installer plus portable zip

## 5 — Extensibility (v0.7)
- Plugin hooks: pre/post send actions
- CSV/JSON dataset input with variable substitution
- Hotkey global listener for quick launch
- Theme toggle: light/dark/system
- Multi-language support scaffold: English + Turkish

## 6 — Distribution & Release (v1.0)
- GitHub release with signed build artifacts
- Auto-update checker from GitHub Releases API
- Changelog + docs site
- Issue templates and contribution guide

## Git Branches
- `main` — stable releases
- `dev` — integration branch
- `feat/...` — feature branches per roadmap item
