import openpyxl
from config_paths import OUTPUT_DIR

# Definiera rubrikerna
headers = [
    "System", "Datum", "Version", "PersonNr", "Skolenhetskod", "Klass", "Förnamn", "Efternamn",
    "BI", "En", "Hkk", "idh", "Ma", "m1(språk)", "M1(betyg)", "M2(språk)", "M2(betyg)", 
    "ModM_anm", "Modmalbe", "mu", "No", "Bi", "Fy", "Ke", "So", "Ge", "Hi", "Re", "Sh", "SI", 
    "Sv", "Sva", "Tn", "Tk", "Ovr"
]

# Sätt sökvägar via konfigurerade mappar
DATA_MAPP = OUTPUT_DIR
TXT_FIL = DATA_MAPP / "betyg.txt"
EXCEL_FIL = DATA_MAPP / "betyg.xlsx"

# Funktion för att formattera personnummer till YYMMDD-XXXX utan apostrof

def formatera_personnummer(pnr):
    pnr = pnr.replace("-", "").replace(" ", "")
    if len(pnr) == 10:
        return pnr[:6] + "-" + pnr[6:]
    elif len(pnr) == 12:
        return pnr[2:8] + "-" + pnr[8:]
    return pnr

def exportera_betyg_excel():
    """Läser ``betyg.txt`` och skapar ``betyg.xlsx`` i output-mappen."""

    # Försök att läsa in filen som UTF-8
    try:
        with TXT_FIL.open('r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Om det misslyckas, försök med cp1252 och ersätt icke-dekodbara tecken
        with TXT_FIL.open('r', encoding='cp1252', errors='replace') as f:
            lines = f.readlines()

    # Skapa en ny arbetsbok
    wb = openpyxl.Workbook()
    ws = wb.active

    # Skriv in rubrikerna på första raden
    ws.append(headers)

    # Bearbeta varje rad i betyg.txt
    for line in lines:
        line = line.strip()
        if not line:
            continue  # hoppa över tomma rader

        row = line.split(';')

        if len(row) > 3:
            row[3] = formatera_personnummer(row[3])  # kolumn 4 = PersonNr

        # Justera om raden har fler eller färre fält än headers
        if len(row) > len(headers):
            row = row[:len(headers)]
        elif len(row) < len(headers):
            row += [''] * (len(headers) - len(row))

        ws.append(row)

    # Spara arbetsboken
    wb.save(EXCEL_FIL)

    print(f"Filen {EXCEL_FIL} har skapats framgångsrikt.")


if __name__ == "__main__":
    exportera_betyg_excel()
