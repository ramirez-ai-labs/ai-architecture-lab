import sys
from pathlib import Path

# Ensure the example package root (domain_model_example) is on sys.path so tests
# can import the local `app` package regardless of where pytest was invoked from.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
