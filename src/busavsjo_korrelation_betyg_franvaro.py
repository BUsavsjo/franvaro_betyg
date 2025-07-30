import pandas as pd
import hashlib
import os

# === INSTÄLLNINGAR ===
DATA_MAPP = os.path.join(os.path.dirname(__file__), "..", "data")
FIL_FRANVARO = os.path.join(DATA_MAPP, "franvaro_rensad_kategoriserad.xlsx")
FRANVARO_FLIK = "Rensad data"
BETYG_FIL = os.path.join(DATA_MAPP, "betyg.xlsx")
OUTPUT_FIL = os.path.join(DATA_MAPP, "busavsjo_korrelation_input.xlsx")
BETYGSKOLUMNER = ["Ma", "En", "Sh"]

# === FUNKTIONER ===
def normalisera_personnummer(pnr):
    """Rensa personnummer för whitespace, men behåll formatet."""
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

# === STEG 1: Läs in och anonymisera betygsdata ===
betyg_df = pd.read_excel(BETYG_FIL, dtype={"PersonNr": str})
betyg_df["AnonymID"] = betyg_df["PersonNr"].apply(normalisera_personnummer).apply(skapa_anonym_id)
betyg_df.drop(columns=["PersonNr", "Förnamn", "Efternamn"], inplace=True)
betyg_df = mappa_betyg_till_siffra(betyg_df, BETYGSKOLUMNER)

# === STEG 2: Läs in frånvarodata från rensad fil ===
franvaro_df = pd.read_excel(FIL_FRANVARO, sheet_name=FRANVARO_FLIK)
franvaro_df = franvaro_df[franvaro_df["personnr"].notna()]
franvaro_df["AnonymID"] = franvaro_df["personnr"].apply(normalisera_personnummer).apply(skapa_anonym_id)

# Behåll endast kolumner som behövs
franvaro_df = franvaro_df[["AnonymID", "årskurs", "ogiltig_frånvaro_pct", "närvaro_pct"]]
franvaro_df["total_frånvaro"] = 100 - franvaro_df["närvaro_pct"]

# === STEG 3: Slå ihop data ===
samman_df = pd.merge(betyg_df, franvaro_df, on="AnonymID")

# === STEG 4: Korrelation ===
print("\n📊 Korrelation mellan betyg och frånvaro:")
for betyg in [f"{amne}_num" for amne in BETYGSKOLUMNER]:
    for kol in ["ogiltig_frånvaro_pct", "total_frånvaro"]:
        if betyg in samman_df.columns and kol in samman_df.columns:
            try:
                corr = samman_df[betyg].corr(samman_df[kol])
                print(f"{betyg} vs {kol}: {corr:.2f}")
            except Exception as e:
                print(f"{betyg} vs {kol}: Fel: {e}")

# === STEG 5: Spara sammanfogad data ===
samman_df.to_excel(OUTPUT_FIL, index=False)
print(f"\n✔️ Klar! Data sparades till '{OUTPUT_FIL}'")
