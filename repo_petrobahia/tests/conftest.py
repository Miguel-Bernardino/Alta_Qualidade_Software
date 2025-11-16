import sys
from pathlib import Path

# garante que `src` esteja no PYTHONPATH para imports como `models`, `services`, etc.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
