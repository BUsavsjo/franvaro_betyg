from pathlib import Path
import json
import pandas as pd
from config_paths import RAW_BETYG_DIR, LASAR, BASE_DIR

def berakna_medel_merit():
    filer = [
        ("betyg_ak6_med_merit.xlsx", 6),
        ("betyg_ak9_med_merit.xlsx", 9),
    ]
    resultat = []
    for filnamn, arskurs in filer:
        fil = RAW_BETYG_DIR / filnamn
        if not fil.exists():
            print(f"⚠️ Filen '{fil}' saknas – hoppar över.")
            continue
        df = pd.read_excel(fil)
        kolumn = next((c for c in df.columns if "merit" in c.lower()), None)
        if kolumn is None:
            print(f"⚠️ Ingen meritvärde-kolumn i '{fil}'.")
            continue
        medel = pd.to_numeric(df[kolumn], errors="coerce").mean()
        resultat.append({"Årskurs": arskurs, "MedelMeritvärde": round(float(medel), 2)})

    if not resultat:
        print("⚠️ Ingen data att spara.")
        return

    out_dir = BASE_DIR / "public" / "json" / LASAR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_fil = out_dir / "medel_meritvarde.json"
    with out_fil.open("w", encoding="utf-8") as f:
        json.dump(resultat, f, ensure_ascii=False, indent=2)
    print(f"✅ Sparade medel meritvärde i '{out_fil}'.")

if __name__ == "__main__":
    berakna_medel_merit()
