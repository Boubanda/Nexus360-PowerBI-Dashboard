"""Contrôles rapides des livrables générés par Nexus 360."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "generated"
RESULTS_DIR = ROOT / "data" / "analytics"


def main() -> None:
    operations = pd.read_csv(DATA_DIR / "fact_operations.csv")
    entities = pd.read_csv(DATA_DIR / "dim_entity.csv")
    geo = pd.read_csv(DATA_DIR / "dim_geo.csv")
    dates = pd.read_csv(DATA_DIR / "dim_date.csv")
    summary = pd.read_csv(RESULTS_DIR / "executive_summary.csv")

    assert len(operations) == 17_669
    assert operations["bu_name"].nunique() == 3
    assert len(entities) == 19
    assert len(geo) == 15
    assert dates["year"].min() == 2021 and dates["year"].max() == 2024
    assert int(summary.loc[0, "nb_operations"]) == len(operations)
    assert operations["revenue"].sum() > 2_000_000_000

    print("Validation réussie : 17 669 opérations, 3 BU, période 2021-2024.")


if __name__ == "__main__":
    main()
