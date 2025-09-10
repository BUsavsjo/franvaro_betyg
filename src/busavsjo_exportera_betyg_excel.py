# === busavsjo_exportera_betyg_excel.py ===
import openpyxl
from config_paths import OUTPUT_DIR, LASAR
from pathlib import Path

# Två varianter av kolumnrubriker
HEADERS_AK6 = [
    "System", "Datum", "Version", "PersonNr", "Skolenhetskod", "Klass", "Förnamn", "Efternamn",
    "BI", "En", "Hkk", "idh", "Ma", "m1(språk)", "M1(betyg)", "M2(språk)", "M2(betyg)",
    "ModM_anm", "Modmalbe", "mu", "No", "So", "Sv", "Sva", "Tk", "Ovr"
]

HEADERS_AK9 = [
    "System", "Datum", "Version", "PersonNr", "Skolenhetskod", "Klass", "Förnamn", "Efternamn",
    "BI", "En", "Hkk", "idh", "Ma", "m1(språk)", "M1(betyg)", "M2(språk)", "M2(betyg)",
    "ModM_anm", "Modmalbe", "mu", "Bi", "Fy", "Ke", "Ge", "Hi", "Re", "Sh", "SI",
    "Sv", "Sva", "Tn", "Tk", "Ovr"
]

def formatera_personnummer(pnr):
    pnr = pnr.replace("-", "").replace(" ", "")
    if len(pnr) == 10:
        return pnr[:6] + "-" + pnr[6:]
    elif len(pnr) == 12:
        return pnr[2:8] + "-" + pnr[8:]
    return pnr

def avgor_headers(lines):
    for line in lines:
        parts = line.strip().split(';')
        if len(parts) > 5:
            klass = parts[5].strip().upper()
            if klass.startswith("6"):
                print("📘 Klass indikerar AK6 – använder AK6-struktur.")
                return HEADERS_AK6
            elif klass.startswith("9"):
                print("📙 Klass indikerar AK9 – använder AK9-struktur.")
                return HEADERS_AK9
    print("⚠️ Klass kunde inte tolkas – standard till AK6.")
    return HEADERS_AK6

def exportera_betyg_excel(txt_fil: Path, excel_fil: Path, struktur: str = None):
    if not txt_fil.exists():
        print(f"⚠️ Filen '{txt_fil}' saknas – hoppar över export.")
        return

    try:
        with txt_fil.open('r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with txt_fil.open('r', encoding='cp1252', errors='replace') as f:
            lines = f.readlines()

    if struktur == "AK6":
        headers = HEADERS_AK6
    elif struktur == "AK9":
        headers = HEADERS_AK9
    else:
        headers = avgor_headers(lines)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(headers)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        row = line.split(';')
        if len(row) > 3:
            row[3] = formatera_personnummer(row[3])

        if len(row) > len(headers):
            row = row[:len(headers)]
        elif len(row) < len(headers):
            row += [''] * (len(headers) - len(row))

        ws.append(row)

    wb.save(excel_fil)
    print(f"✅ Filen '{excel_fil.name}' har skapats i '{excel_fil.parent}'.")

if __name__ == "__main__":
    BASE = Path(__file__).resolve().parent.parent
    lasar = LASAR
    base_out = BASE / "data" / "output" / lasar

    exportera_betyg_excel(
        txt_fil=base_out / "betyg_ak6.txt",
        excel_fil=base_out / "betyg_ak6.xlsx",
        struktur="AK6"
    )

    exportera_betyg_excel(
        txt_fil=base_out / "betyg_ak9.txt",
        excel_fil=base_out / "betyg_ak9.xlsx",
        struktur="AK9"
    )
