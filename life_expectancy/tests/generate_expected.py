from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import clean_data


def generate_expected() -> None:
    """
    Does: Generate expected PT fixture from raw sample fixture.
    Args: None
    Output: None
    """
    fixtures_dir = Path(__file__).resolve().parents[1] / "tests" / "fixtures"

    raw_path = fixtures_dir / "eu_life_expectancy_raw.tsv"
    expected_path = fixtures_dir / "pt_life_expectancy_expected.csv"

    raw_df = pd.read_csv(raw_path, sep="\t").copy()
    pt_df = clean_data(raw_df, "PT").reset_index(drop=True)

    pt_df.to_csv(expected_path, index=False)

    print("Expected fixture regenerated.")
    print("Rows:", len(pt_df))


if __name__ == "__main__":
    generate_expected()
