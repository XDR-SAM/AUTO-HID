import sys
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PYTHON = REPO / "build" / "portable-python.exe"
ENTRY = REPO / "src" / "autokey" / "ui.py"


def main() -> int:
    if not PYTHON.exists():
        print(f"Missing portable Python at: {PYTHON}")
        return 2

    cmd = [str(PYTHON), str(ENTRY)]
    print(f"Running: {' '.join(cmd)}")
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
