import os

def busavsjo_samla_txtfiler():
    """Läser in alla .txt-filer i ``data/raw/betyg`` och
    sparar ihop dem till ``data/output/betyg.txt``"""
    rotmapp = os.path.dirname(os.path.dirname(__file__))
    indata_mapp = os.path.join(rotmapp, "data", "raw", "betyg")
    utdata_fil = os.path.join(rotmapp, "data", "output", "betyg.txt")
    med_antal = 0

    with open(utdata_fil, "w", encoding="utf-8") as utfil:
        for filnamn in sorted(os.listdir(indata_mapp)):
            if filnamn.endswith(".txt") and filnamn != "betyg.txt":
                filväg = os.path.join(indata_mapp, filnamn)
                try:
                    with open(filväg, "r", encoding="utf-8") as infil:
                        innehåll = infil.read()
                except UnicodeDecodeError:
                    with open(filväg, "r", encoding="latin-1") as infil:
                        innehåll = infil.read()

                utfil.write(innehåll.strip() + "\n\n")
                med_antal += 1

    print(f"✔️ Samlade {med_antal} filer till '{utdata_fil}'")

if __name__ == "__main__":
    busavsjo_samla_txtfiler()
