"""Beräkna medelbetyg per ämne uppdelat på kön och årskurs.

Läser betygsfilerna som skapats i flödet (betyg_ak6_med_merit.xlsx och
betyg_ak9_med_merit.xlsx) och tar fram medelbetyg per ämne för flickor,
pojkar och totalt. Resultatet sparas som JSON och strukturen är anpassad
för att kunna användas direkt av webbgränssnittet.
"""

from __future__ import annotations

from pathlib import Path
import json
from typing import Dict, List

import pandas as pd

from config_paths import OUTPUT_DIR, CONFIG_DIR, LASAR

# Betygsfiler med könskolumn
BETYGSFILER: Dict[int, Path] = {
    6: OUTPUT_DIR / "betyg_ak6_med_merit.xlsx",
    9: OUTPUT_DIR / "betyg_ak9_med_merit.xlsx",
}

# Ämneskolumner per årskurs
AMNEN_AK6: List[str] = [
    "BI",
    "En",
    "Hkk",
    "idh",
    "Ma",
    "mu",
    "No",
    "So",
    "Sv",
    "Sva",
    "Tk",
]

AMNEN_AK9: List[str] = [
    "BI",
    "En",
    "Hkk",
    "idh",
    "Ma",
    "mu",
    "Bi",
    "Fy",
    "Ke",
    "Ge",
    "Hi",
    "Re",
    "Sh",
    "SI",
    "Sv",
    "Sva",
    "Tn",
    "Tk",
]

# Omvandling från bokstavsbetyg till poäng
BETYG_TILL_POANG = {
    "A": 20,
    "B": 17.5,
    "C": 15,
    "D": 12.5,
    "E": 10,
    "F": 0,
}

# Värden som inte ska tas med i beräkningen
OGILTIGA = {"2", "3", "9", "Y", "Z", 2, 3, 9, "", None}


def _ladda_amnesnamn() -> Dict[str, str]:
    """Läser filen med ämnesnamn och returnerar en mapping."""

    with (CONFIG_DIR / "subject_names.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def medelbetyg_per_amne(
    df: pd.DataFrame, amnen: List[str], mapping: Dict[str, str]
) -> Dict[str, Dict[str, float | None]]:
    """Beräknar medelbetyg per ämne i en DataFrame."""

    resultat: Dict[str, Dict[str, float | None]] = {}

    for kol in amnen:
        if kol not in df.columns:
            continue

        rå = df[kol]
        giltig_mask = ~rå.isin(OGILTIGA)
        if not giltig_mask.any():
            continue

        # Konvertera betyg till numeriska poäng
        poäng = rå[giltig_mask].replace(BETYG_TILL_POANG)
        poäng = pd.to_numeric(poäng, errors="coerce")

        subset = df[giltig_mask].copy()
        subset["poäng"] = poäng

        flickor = subset[subset["gender"] == "flicka"]["poäng"].mean()
        pojkar = subset[subset["gender"] == "pojke"]["poäng"].mean()
        totalt = subset["poäng"].mean()

        namn = mapping.get(kol, kol)
        resultat[namn] = {
            "Flickor": round(float(flickor), 1) if pd.notna(flickor) else None,
            "Pojkar": round(float(pojkar), 1) if pd.notna(pojkar) else None,
            "Totalt": round(float(totalt), 1) if pd.notna(totalt) else None,
        }

    return resultat


def skapa_medelbetyg_json() -> None:
    """Skapar JSON-fil med medelbetyg per ämne."""

    mapping = _ladda_amnesnamn()
    slutresultat: Dict[str, Dict[str, Dict[str, float | None]]] = {}

    fördelning = {6: AMNEN_AK6, 9: AMNEN_AK9}

    for arskurs, amnen in fördelning.items():
        fil = BETYGSFILER[arskurs]
        if not fil.exists():
            print(f"⚠️ Filen '{fil}' saknas – hoppar över.")
            continue
        df = pd.read_excel(fil)
        if "gender" not in df.columns:
            print(f"⚠️ Kolumn 'gender' saknas i {fil.name} – hoppar över.")
            continue

        slutresultat[str(arskurs)] = medelbetyg_per_amne(df, amnen, mapping)

    if not slutresultat:
        print("⚠️ Ingen data att spara.")
        return

    out_dir = Path(__file__).resolve().parent.parent / "public" / "json" / LASAR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_fil = out_dir / "medelbetyg_per_amne.json"
    with out_fil.open("w", encoding="utf-8") as f:
        json.dump(slutresultat, f, ensure_ascii=False, indent=2)

    print(f"✅ Sparade medelbetyg per ämne i '{out_fil}'.")


if __name__ == "__main__":
    skapa_medelbetyg_json()

