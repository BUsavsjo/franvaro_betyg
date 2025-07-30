from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
RAW_BETYG_DIR = RAW_DIR / "betyg"
RAW_FRANVARO_DIR = RAW_DIR / "franvaro"
OUTPUT_DIR = BASE_DIR / "data" / "output"
