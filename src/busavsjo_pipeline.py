"""Kör hela flödet för betyg- och frånvaroanalys."""

import runpy

MODULER = [
    "busavsjo_samla_betygstxt",
    "busavsjo_exportera_betyg_excel",
    "busavsjo_samla_franvaro",
    "busavsjo_rensa_franvaro_excel",
    "busavsjo_korrelation_betyg_franvaro",
]


def kör_pipeline():
    for modul in MODULER:
        print(f"\n▶ Kör {modul}...")
        runpy.run_module(modul, run_name="__main__")


if __name__ == "__main__":
    kör_pipeline()
