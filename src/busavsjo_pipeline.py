"""Kör hela flödet för betyg- och frånvaroanalys.

Steg i rätt ordning:
1. Samla betygs‑txt‑filer
2. Exportera betyg till Excel
3. Samla frånvarorapporter (.xls)
4. Rensa och kategorisera frånvaro
5. Skapa sammanställning `franvaro_total.xlsx`
6. Kör korrelationsanalys mellan betyg och frånvaro
7. Beräkna medelmeritvärde
"""

import importlib.util
import sys
from pathlib import Path

from config_paths import RAW_BETYG_DIR, RAW_FRANVARO_DIR, OUTPUT_DIR
from busavsjo_samla_betygstxt import busavsjo_samla_txtfiler
from busavsjo_exportera_betyg_excel import exportera_betyg_excel
from busavsjo_samla_franvaro import busavsjo_samla_franvarorapporter
from busavsjo_rensa_franvaro_excel import rensa_franvaro_excel
from busavsjo_skapa_franvaro_total import skapa_franvaro_total
from busavsjo_korrelation_betyg_franvaro import korrelation_betyg_franvaro
from busavsjo_medel_merit import busavsjo_berakna_medel_merit


def _samla_betygstxt():
    """Samlar betygstextfiler för åk6 och åk9."""
    busavsjo_samla_txtfiler(RAW_BETYG_DIR / "ak6", OUTPUT_DIR / "betyg_ak6.txt")
    busavsjo_samla_txtfiler(RAW_BETYG_DIR / "ak9", OUTPUT_DIR / "betyg_ak9.txt")


def _exportera_betyg_excel():
    """Exporterar betygstextfiler till Excel."""
    exportera_betyg_excel(OUTPUT_DIR / "betyg_ak6.txt", OUTPUT_DIR / "betyg_ak6.xlsx", "AK6")
    exportera_betyg_excel(OUTPUT_DIR / "betyg_ak9.txt", OUTPUT_DIR / "betyg_ak9.xlsx", "AK9")


# 🚦 Viktigt: varje steg bygger på föregående, ändra endast om du vet vad du gör
STEG = [
    ("Samla betygs‑txt‑filer", _samla_betygstxt),
    ("Exportera betyg till Excel", _exportera_betyg_excel),
    ("Samla frånvarorapporter", busavsjo_samla_franvarorapporter),
    ("Rensa och kategorisera frånvaro", rensa_franvaro_excel),
    ("Skapa sammanställning franvaro_total.xlsx", skapa_franvaro_total),
    ("Kör korrelationsanalys mellan betyg och frånvaro", korrelation_betyg_franvaro),
    ("Beräkna medelmeritvärde", busavsjo_berakna_medel_merit),
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
    for mapp in [RAW_BETYG_DIR / "ak6", RAW_BETYG_DIR / "ak9", RAW_FRANVARO_DIR, OUTPUT_DIR]:
        if not mapp.exists():
            print(f"⚠️ Saknar mapp {mapp}, skapar...")
            mapp.mkdir(parents=True, exist_ok=True)


def kör_pipeline():
    """Kör alla steg i pipeline i fördefinierad ordning."""
    if not _kontrollera_beroenden():
        sys.exit(1)

    _kontrollera_mappar()

    for namn, funktion in STEG:
        print(f"\n▶ {namn}...")
        try:
            funktion()
        except FileNotFoundError as e:
            print(f"❌ Fil saknas: {e.filename}")
            break
        except Exception as e:
            print(f"❌ Ett fel uppstod i steget '{namn}': {e}")
            break
    else:
        print("\n✅ Pipeline klar utan kritiska fel!")


if __name__ == "__main__":
    kör_pipeline()

