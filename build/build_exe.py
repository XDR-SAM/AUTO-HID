from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DIST = REPO / "dist"
ENTRY = REPO / "src" / "autokey" / "ui.py"


def main() -> int:
    exe = shutil.which("pyinstaller")
    if not exe:
        print("pyinstaller is not installed. Install it first: pip install pyinstaller")
        return 2

    print(f"Using pyinstaller: {exe}")
    DIST.mkdir(exist_ok=True)
    work = REPO / "build" / "pyi-work"
    cmd = [
        exe,
        "--onefile",
        "--windowed",
        "--name",
        "autokey",
        "--specpath",
        str(DIST),
        "--distpath",
        str(DIST),
        "--workpath",
        str(work),
        "--hidden-import",
        "autokey.sender",
        "--hidden-import",
        "autokey.ui",
        str(ENTRY),
    ]
    print("Running:", " ".join(cmd))
    subprocess.call(cmd)
    exe_path = DIST / "autokey.exe"
    print(f"Expected output: {exe_path}")
    print(f"Exists: {exe_path.exists()}")
    return 0 if exe_path.exists() else 3


if __name__ == "__main__":
    sys.exit(main())
