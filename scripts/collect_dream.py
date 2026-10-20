"""Dream native-hook trajectory collection (see --help)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.collection_cli import run_collection

if __name__ == '__main__':
    raise SystemExit(run_collection('dream'))
