# AutoKey — Usage

This guide walks you through installing, configuring, and using AutoKey.

## 1. Install

- Download the latest release for Windows from the project release page.
- Extract the archive to a permanent folder, e.g. `G:\autokey`.
- Run `autokey.exe`. No admin rights are required for basic usage.

## 2. Configure the app

AutoKey stores its config next to the executable by default.

- `config.yaml` — hotkeys, trigger mode, and app behavior.
- `scripts/` — user scripts executed by hotkeys or triggers.
- `hotkeys.yaml` — optional separate hotkey definitions.

### Example `config.yaml`

```yaml
mode: translate          # translate | selective | disable
hotkey:
  trigger: Ctrl+Alt+Space
  show_ui: Ctrl+Alt+M
engine: online            # online | offline
  # online uses the configured translation service.
  # offline uses a local model.
lookup:                  # empty means all text
  max_chars: 2000
ui:
  opacity: 255
  always_on_top: true
```

## 3. Select text and translate

1. Highlight text in any Windows app.
2. Press `Ctrl+Alt+Space`.
3. AutoKey copies the selected text automatically.
4. A small window appears with the translated text.
5. Press `Esc` or click outside the window to close.

## 4. Show the settings window

- Press `Ctrl+Alt+M` to open the settings UI.
- Change engine, hotkeys, font size, or look / feel.
- Changes save immediately.

## 5. Mode switching

- **translate**: translate the current selection automatically.
- **selective**: copy-to-clipboard first, then translate manually.
- **disable**: app runs but skips translation.

Use the tray icon or hotkey to switch modes.

## 6. Offline usage

- Enable `engine: offline` in `config.yaml`.
- The first offline run downloads the model if needed.
- Subsequent runs no longer require network access.

## 7. Troubleshooting

- **Nothing happens on hotkey**: confirm AutoKey is running in the tray.
- **Wrong language detected**: override the source language in `config.yaml`.
- **UI is invisible**: reduce `opacity` or disable `always_on_top`.
- **App crashes**: run `autokey.exe --debug` and save the log.
