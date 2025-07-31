"""Kör hela flödet för betyg- och frånvaroanalys."""

import importlib.util
import runpy
import sys
from pathlib import Path

from config_paths import RAW_BETYG_DIR, RAW_FRANVARO_DIR, OUTPUT_DIR

MODULER = [
    "busavsjo_samla_betygstxt",
    "busavsjo_exportera_betyg_excel",
    "busavsjo_samla_franvaro",
    "busavsjo_rensa_franvaro_excel",
    "busavsjo_korrelation_betyg_franvaro",
]


def _kontrollera_beroenden() -> bool:
    """Returnerar ``True`` om alla beroenden finns installerade."""
    req_fil = Path(__file__).resolve().parent.parent / "requirements.txt"
    if not req_fil.exists():
        return True

    saknade = []
    for rad in req_fil.read_text().splitlines():
        pak = rad.strip()
        if not pak:
            continue
        namn = pak.split("==")[0].split(">=")[0]
        if importlib.util.find_spec(namn) is None:
            saknade.append(pak)

    if saknade:
        print("❌ Följande beroenden saknas:")
        for pak in saknade:
            print(f"  - {pak}")
        print("Installera dem med 'pip install -r requirements.txt'.")
        return False

    return True


def _kontrollera_mappar():
    """Verifierar att nödvändiga datamappar finns."""
    for mapp in [RAW_BETYG_DIR, RAW_FRANVARO_DIR, OUTPUT_DIR]:
        if not mapp.exists():
            print(f"⚠️ Saknar mapp {mapp}, skapar...")
            mapp.mkdir(parents=True, exist_ok=True)


def kör_pipeline():
    if not _kontrollera_beroenden():
        sys.exit(1)

    _kontrollera_mappar()

    for modul in MODULER:
        print(f"\n▶ Kör {modul}...")
        try:
            runpy.run_module(modul, run_name="__main__")
        except ModuleNotFoundError as e:
            print(
                f"❌ Hittade inte modulen '{e.name}'.\n"
                "Kontrollera att alla beroenden är installerade."
            )
            break
        except FileNotFoundError as e:
            print(f"❌ Fil saknas: {e.filename}")
            break
        except Exception as e:
            print(f"❌ Ett fel uppstod i '{modul}': {e}")
            break


if __name__ == "__main__":
    kör_pipeline()
