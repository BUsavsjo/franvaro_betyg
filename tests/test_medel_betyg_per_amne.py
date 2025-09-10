import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from busavsjo_medel_betyg_per_amne import medelbetyg_per_amne


def test_medelbetyg_per_amne_beraknar_korrekt():
    df = pd.DataFrame(
        {
            "gender": ["flicka", "flicka", "pojke", "pojke"],
            "Ma": ["A", "C", "B", "F"],
            "En": ["B", "B", "C", "D"],
        }
    )

    amnen = ["Ma", "En"]
    mapping = {"Ma": "Matematik", "En": "Engelska"}

    resultat = medelbetyg_per_amne(df, amnen, mapping)

    assert resultat["Matematik"] == {
        "Flickor": 17.5,
        "Pojkar": 8.8,
        "Totalt": 13.1,
    }
    assert resultat["Engelska"] == {
        "Flickor": 17.5,
        "Pojkar": 13.8,
        "Totalt": 15.6,
    }

