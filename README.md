# AutoKey Sender

Local keystroke automation. No app store account needed.

## No-install run
```bash
python -m autokey.ui
```

## Install package
```bash
pip install -e .
```

## Build standalone EXE
```bash
pip install -e .[exe-build]
python build/build_exe.py
```

Output: `dist/autokey.exe`

## Dev
```bash
pip install -e ".[dev]"
pytest
```
