# AutoKey — Architecture

## Overview

AutoKey is a small Windows desktop application that reads selected text,
sends it to a translation engine, and shows the result in a compact UI.
It is designed to stay out of the way: tray-based, hotkey-driven, and
low-latency.

## Modules

| Module | Responsibility |
|---|---|
| `app` | Application lifecycle, tray icon, hotkey registration, mode switching. |
| `core` | Clipboard polling / selection capture, text normalization, translation orchestration. |
| `engines` | Provider implementations: online API and offline local model. |
| `ui` | Result window, settings window, tray menu. |
| `config` | Load/save YAML config, hotkey bindings, engine selection. |
| `utils` | Logging, i18n, safe clipboard wrappers. |

## Data flow

1. User selects text in any app.
2. App captures selection globally via hotkey handler.
3. `core` copies text into an internal clipboard buffer.
4. Engine layer sends text and returns translation.
5. `ui` renders the result window.
6. `core` optionally restores original clipboard contents.

```
[Selection] -> [Hotkey] -> [Core] -> [Engine] -> [UI] -> [User]
```

## Threading model

- Hotkey listener runs on a dedicated input thread.
- Each translation request runs on a worker thread.
- UI updates are marshaled onto the main UI thread.
- Clipboard operations are serialized through a mutex.

## Configuration

`config.yaml` is loaded at startup. Changes are watched at runtime.
Supported keys:

- `mode`: translate / selective / disable
- `hotkey.trigger` / `hotkey.show_ui`
- `engine`: online / offline
- `lookup.max_chars`
- `ui.opacity` / `ui.always_on_top`

## Extension points

- **New engines**: implement the engine interface in `engines/` and register via `config.yaml` as `engine: <name>`.
- **Themes**: override UI styles in `themes/` or via `ui.theme` config.
- **Post-processing hooks**: add a transform in `core/postprocessors/` to modify text before display.
- **Custom hotkeys**: add actions in `app/hotkeys/` without modifying core logic.

## Build & run

- Python-based build: `python build.py`
- Windows-only packaging requires Inno Setup or similar for installer creation.
- Offline engine requires including the model file in `engines/offline/model/`.
