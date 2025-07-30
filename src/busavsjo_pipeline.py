"""Kör hela flödet för betyg- och frånvaroanalys."""

import runpy

MODULER = [
    "franvaro_betyg.busavsjo_samla_betygstxt",
    "franvaro_betyg.busavsjo_exportera_betyg_excel",
    "franvaro_betyg.busavsjo_samla_franvaro",
    "franvaro_betyg.busavsjo_rensa_franvaro_excel",
    "franvaro_betyg.busavsjo_korrelation_betyg_franvaro",
]


def kör_pipeline():
    for modul in MODULER:
        print(f"\n▶ Kör {modul}...")
        runpy.run_module(modul, run_name="__main__")


if __name__ == "__main__":
    kör_pipeline()
