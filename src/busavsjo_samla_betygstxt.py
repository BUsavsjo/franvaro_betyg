from config_paths import RAW_BETYG_DIR, OUTPUT_DIR

def busavsjo_samla_txtfiler():
    """Läser in alla .txt-filer i ``data/raw/betyg`` och
    sparar ihop dem till ``data/output/betyg.txt``"""
    indata_mapp = RAW_BETYG_DIR
    utdata_fil = OUTPUT_DIR / "betyg.txt"
    med_antal = 0

    with utdata_fil.open("w", encoding="utf-8") as utfil:
        for filväg in sorted(indata_mapp.iterdir()):
            if filväg.suffix == ".txt" and filväg.name != "betyg.txt":
                try:
                    innehåll = filväg.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    innehåll = filväg.read_text(encoding="latin-1")

                utfil.write(innehåll.strip() + "\n\n")
                med_antal += 1

    print(f"✔️ Samlade {med_antal} filer till '{utdata_fil}'")

if __name__ == "__main__":
    busavsjo_samla_txtfiler()
