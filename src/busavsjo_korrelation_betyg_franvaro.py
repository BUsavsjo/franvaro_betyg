import pandas as pd
import hashlib
import os
from openpyxl.styles import PatternFill
from openpyxl import load_workbook

# === INSTÄLLNINGAR ===
DATA_MAPP = os.path.join(os.path.dirname(__file__), "..", "data", "output")
FIL_FRANVARO = os.path.join(DATA_MAPP, "franvaro_rensad_kategoriserad.xlsx")
FRANVARO_FLIK = "Rensad data"
BETYG_FIL = os.path.join(DATA_MAPP, "betyg.xlsx")
OUTPUT_FIL = os.path.join(DATA_MAPP, "busavsjo_korrelation_input.xlsx")
RESULTAT_FIL = os.path.join(DATA_MAPP, "busavsjo_korrelation_resultat.xlsx")
OUTPUT_PARQUET = os.path.join(DATA_MAPP, "busavsjo_korrelation_input.parquet")
RESULTAT_PARQUET = os.path.join(DATA_MAPP, "busavsjo_korrelation_resultat.parquet")

IGNORERA_KOLUMNER = {
    "System", "Datum", "Version", "Skolenhetskod",
    "Klass", "Förnamn", "Efternamn", "PersonNr",
}
BETYGSKOLUMNER = None

def normalisera_personnummer(pnr):
    try:
        return str(pnr).strip()
    except:
        return None

def skapa_anonym_id(pnr):
    return hashlib.sha256(str(pnr).encode('utf-8')).hexdigest()

def mappa_betyg_till_siffra(df, kolumner):
    betygsskala = ['F', 'E', 'D', 'C', 'B', 'A']
    betyg_poang = {b: i for i, b in enumerate(betygsskala)}
    for kol in kolumner:
        ny_kol = kol + "_num"
        df[ny_kol] = df[kol].map(betyg_poang)
    return df

def tolka_korrelation(k):
    if pd.isna(k):
        return "okänd"
    k_abs = abs(k)
    if k_abs >= 0.7:
        styrka = "Tydlig koppling"
    elif k_abs >= 0.4:
        styrka = "Måttlig koppling"
    elif k_abs >= 0.2:
        styrka = "Svag koppling"
    else:
        styrka = "Obetydlig eller ingen koppling"
    riktning = "Negativ (mer frånvaro → lägre betyg)" if k < 0 else "Positiv (mer frånvaro → högre betyg)"
    return f"{styrka} – {riktning}"

def farg_gradient(k):
    if pd.isna(k):
        return None
    k = max(min(k, 1), -1)
    if k < 0:
        r = int(244 + (255 - 244) * (k + 1))
        g = int(204 + (255 - 204) * (k + 1))
        b = int(204 + (255 - 204) * (k + 1))
    else:
        r = int(255 - (255 - 217) * k)
        g = int(255 - (255 - 234) * k)
        b = int(255 - (255 - 211) * k)
    return PatternFill(start_color=f"{r:02X}{g:02X}{b:02X}", fill_type="solid")

# === STEG 1 ===
betyg_df = pd.read_excel(BETYG_FIL, dtype={"PersonNr": str})
BETYGSKOLUMNER = [kol for kol in betyg_df.columns if kol not in IGNORERA_KOLUMNER]

betyg_df["AnonymID"] = (
    betyg_df["PersonNr"].apply(normalisera_personnummer).apply(skapa_anonym_id)
)
betyg_df.drop(columns=[c for c in IGNORERA_KOLUMNER if c in betyg_df.columns], inplace=True)
betyg_df = mappa_betyg_till_siffra(betyg_df, BETYGSKOLUMNER)

# === STEG 2 ===
franvaro_df = pd.read_excel(FIL_FRANVARO, sheet_name=FRANVARO_FLIK)
franvaro_df = franvaro_df[franvaro_df["personnr"].notna()]
franvaro_df["AnonymID"] = franvaro_df["personnr"].apply(normalisera_personnummer).apply(skapa_anonym_id)
franvaro_df = franvaro_df[["AnonymID", "årskurs", "ogiltig_frånvaro_pct", "närvaro_pct"]]
franvaro_df["total_frånvaro"] = 100 - franvaro_df["närvaro_pct"]

# === STEG 3 ===
samman_df = pd.merge(betyg_df, franvaro_df, on="AnonymID")

# === STEG 4 ===
korrelationer = []
print("\n📊 Korrelation mellan betyg och frånvaro:\n")
for betyg in [f"{amne}_num" for amne in BETYGSKOLUMNER]:
    print(f"ᾞa Ämne: {betyg.replace('_num', '')}")
    for kol in ["ogiltig_frånvaro_pct", "total_frånvaro"]:
        if betyg in samman_df.columns and kol in samman_df.columns:
            try:
                corr = samman_df[betyg].corr(samman_df[kol])
                tolkning = tolka_korrelation(corr)
                print(f"  → Mot {kol}: {corr:.2f}\n     {tolkning}")
                korrelationer.append({
                    "Ämne": betyg.replace("_num", ""),
                    "Frånvarotyp": kol,
                    "Korrelation": round(corr, 2),
                    "Styrka": tolkning
                })
            except Exception as e:
                print(f"  → Mot {kol}: Fel: {e}")
    print("")

# === STEG 5 ===
samman_df.to_excel(OUTPUT_FIL, index=False)
samman_df.to_parquet(OUTPUT_PARQUET, index=False)
print(f"\n✔️ Klar! Data sparades till '{OUTPUT_FIL}' och '{OUTPUT_PARQUET}'")

# === STEG 6 ===
if korrelationer:
    resultat_df = pd.DataFrame(korrelationer)
    ogiltig_df = resultat_df[resultat_df["Frånvarotyp"] == "ogiltig_frånvaro_pct"]
    total_df = resultat_df[resultat_df["Frånvarotyp"] == "total_frånvaro"]

    with pd.ExcelWriter(RESULTAT_FIL, engine='openpyxl') as writer:
        ogiltig_df.to_excel(writer, index=False, sheet_name="Ogiltig frånvaro")
        total_df.to_excel(writer, index=False, sheet_name="Total frånvaro")

    resultat_df.to_parquet(RESULTAT_PARQUET, index=False)

    wb = load_workbook(RESULTAT_FIL)
    for bladnamn in ["Ogiltig frånvaro", "Total frånvaro"]:
        ws = wb[bladnamn]
        for rad in range(2, ws.max_row + 1):
            cell = ws.cell(row=rad, column=3)
            try:
                value = float(cell.value)
                fill = farg_gradient(value)
                if fill:
                    cell.fill = fill
            except:
                continue
    wb.save(RESULTAT_FIL)
    print(f"✔️ Färgkodad Excel-fil sparad till '{RESULTAT_FIL}'")
    print(f"✔️ Resultat även sparat som parquet i '{RESULTAT_PARQUET}'")
