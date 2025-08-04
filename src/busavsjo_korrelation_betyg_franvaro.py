import pandas as pd
import numpy as np
import json
from pathlib import Path
from config_paths import DATA_MAPP, JSON_MAPP, LASAR

BETYGSFILER = {
    "6": DATA_MAPP / f"betyg_ak6.xlsx",
    "9": DATA_MAPP / f"betyg_ak9.xlsx",
}

FRANVARO_FIL = DATA_MAPP / "franvaro_total.xlsx"

FRANVAROTYPER = {
    "ogiltig_franvaro_pct": "Ogiltig frånvaro (%)",
    "total_franvaro_pct": "Total frånvaro (%)"
}

def spara_json(df, filnamn, årskurs):
    (JSON_MAPP).mkdir(parents=True, exist_ok=True)
    df_clean = df.copy()

    # Runda korrelationer endast om de är giltiga
    df_clean["Korrelation"] = df_clean["Korrelation"].apply(
        lambda x: round(float(x), 2) if pd.notna(x) and isinstance(x, (int, float)) else None
    )

    # Ersätt eventuella kvarvarande NaN med None
    df_clean = df_clean.applymap(lambda x: None if pd.isna(x) else x)

    # Lägg till metadata
    df_clean["Läsår"] = LASAR
    df_clean["Årskurs"] = årskurs

    with (JSON_MAPP / filnamn).open("w", encoding="utf-8") as f:
        json.dump(df_clean.to_dict(orient="records"), f, indent=2, ensure_ascii=False)

def analysera_korrelation(klass_varde, betyg_df):
    ämnen_ak6 = ["BI", "En", "Hkk", "idh", "Ma", "mu", "No", "So", "Sv", "Sva", "Tk"]
    ämnen_ak9 = ["BI", "En", "Hkk", "idh", "Ma", "mu", "Bi", "Fy", "Ke", "Ge", "Hi", "Re", "Sh", "SI", "Sv", "Sva", "Tn", "Tk"]
    ämnen = ämnen_ak6 if klass_varde == "6" else ämnen_ak9

    betygsskala = {
        "A": 20,
        "B": 17.5,
        "C": 15,
        "D": 12.5,
        "E": 10,
        "F": 0,
    }

    franvaro_df = pd.read_excel(FRANVARO_FIL)
    df = pd.merge(betyg_df, franvaro_df, on="PersonNr", how="inner")

    for ämne in ämnen:
        if ämne in df.columns:
            df[ämne] = pd.to_numeric(df[ämne].replace(betygsskala), errors="coerce").astype("float32")

    resultat = []
    for franvarotyp, beskrivning in FRANVAROTYPER.items():
        for ämne in ämnen:
            if ämne in df.columns:
                delmängd = df[[ämne, franvarotyp]].dropna()
                if not delmängd.empty and delmängd[franvarotyp].nunique() > 1 and delmängd[ämne].nunique() > 1:
                    korrelation = delmängd[ämne].corr(delmängd[franvarotyp])
                    if pd.isna(korrelation):
                        korrelation = None
                else:
                    korrelation = None

                styrka = styrkebedömning(korrelation)
                resultat.append({
                    "Ämne": ämne,
                    "Frånvarotyp": franvarotyp,
                    "Korrelation": korrelation,
                    "Styrka": styrka
                })

        df_resultat = pd.DataFrame(resultat)
        filnamn = f"{franvarotyp}_ak{klass_varde}.json".replace("å", "a").replace("ä", "a").replace("ö", "o")
        spara_json(df_resultat, filnamn, årskurs=klass_varde)
        print(f"📄 Sparade {filnamn} med {len(df_resultat)} rader.")

def styrkebedömning(k):
    if k is None:
        return "saknas"
    k_abs = abs(k)
    if k_abs < 0.1:
        return "ingen"
    elif k_abs < 0.3:
        return "svag"
    elif k_abs < 0.5:
        return "måttlig"
    elif k_abs < 0.7:
        return "stark"
    else:
        return "mycket stark"

if __name__ == "__main__":
    for årskurs, betygfil in BETYGSFILER.items():
        if not betygfil.exists():
            print(f"⚠️ Betygsfil för årskurs {årskurs} saknas: {betygfil.name}")
            continue
        print(f"🗓️ Läser betyg för årskurs {årskurs} från {betygfil.name}")
        betyg_df = pd.read_excel(betygfil)
        analysera_korrelation(årskurs, betyg_df)
