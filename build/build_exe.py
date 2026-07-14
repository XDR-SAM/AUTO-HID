import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DIST = REPO / "dist"
ENTRY = REPO / "src" / "autokey" / "ui.py"
PYTHON = REPO / "build" / "portable-python.exe"


def python_executable() -> str:
    if PYTHON.exists():
        return str(PYTHON)
    exe = shutil.which("python") or shutil.which("python3") or sys.executable
    return exe


def main() -> int:
    exe = shutil.which("pyinstaller")
    if not exe:
        print("pyinstaller is not installed. Install it first: pip install pyinstaller")
        return 2

    exe_path = python_executable()
    print(f"Using pyinstaller: {exe}")
    print(f"Using python: {exe_path}")
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
        "--python",
        exe_path,
        str(ENTRY),
    ]
    print("Running:", " ".join(cmd))
    subprocess.call(cmd)
    out = DIST / "autokey.exe"
    print(f"Expected output: {out}")
    print(f"Exists: {out.exists()}")
    return 0 if out.exists() else 3


if __name__ == "__main__":
    sys.exit(main())
