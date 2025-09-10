"""Kör hela flödet för betyg- och frånvaroanalys.

Steg i rätt ordning:
1. Samla betygs‑txt‑filer
2. Exportera betyg till Excel
3. Samla frånvarorapporter (.xls)
4. Rensa och kategorisera frånvaro
5. Skapa sammanställning `franvaro_total.xlsx`
6. Kör korrelationsanalys mellan betyg och frånvaro
7. Beräkna medelmeritvärde
8. Lägg till kön i meritfiler
9. Analysera data per kön
10. Beräkna medelbetyg per ämne
"""

import importlib.util
import runpy
import sys
from pathlib import Path

from config_paths import RAW_BETYG_DIR, RAW_FRANVARO_DIR, OUTPUT_DIR

# 🚦 Viktigt: varje steg bygger på föregående, ändra endast om du vet vad du gör
MODULER = [
    "busavsjo_samla_betygstxt",        # 1
    "busavsjo_exportera_betyg_excel",  # 2
    "busavsjo_samla_franvaro",        # 3
    "busavsjo_rensa_franvaro_excel",  # 4
    "busavsjo_skapa_franvaro_total",  # 5 – NYTT steg som skapar franvaro_total.xlsx
    "busavsjo_korrelation_betyg_franvaro",  # 6
    "busavsjo_medel_merit",                 # 7
    "busavsjo_gender",                      # 8
    "busavsjo_korrelation_gender",          # 9
    "busavsjo_medel_betyg_per_amne",        # 10
]


def _kontrollera_beroenden() -> bool:
    """Kontrollerar att alla beroenden i requirements.txt finns installerade."""
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
    """Verifierar att nödvändiga datamappar finns, skapar dem annars."""
    for mapp in [RAW_BETYG_DIR, RAW_FRANVARO_DIR, OUTPUT_DIR]:
        if not mapp.exists():
            print(f"⚠️ Saknar mapp {mapp}, skapar...")
            mapp.mkdir(parents=True, exist_ok=True)


def kör_pipeline():
    """Kör alla moduler i den ordning som definieras i MODULER‑listan."""
    if not _kontrollera_beroenden():
        sys.exit(1)

    _kontrollera_mappar()

    for modul in MODULER:
        print(f"\n▶ Kör {modul}...")
        try:
            runpy.run_module(modul, run_name="__main__")
        except ModuleNotFoundError as e:
            print(f"❌ Hittade inte modulen '{e.name}'.\nKontrollera beroenden eller PYTHONPATH.")
            break
        except FileNotFoundError as e:
            print(f"❌ Fil saknas: {e.filename}")
            break
        except Exception as e:
            print(f"❌ Ett fel uppstod i '{modul}': {e}")
            break
    else:
        print("\n✅ Pipeline klar utan kritiska fel!")


if __name__ == "__main__":
    kör_pipeline()
