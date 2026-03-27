from pathlib import Path
import argparse
import pandas as pd

from life_expectancy.load_and_save import load_data, save_data

RAW_DATA_DIR = Path(__file__).parent / "data" / "raw_data"

def clean_data(data: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Does:
        Clean the raw life expectancy dataset and return a cleaned DataFrame.

    Args:
        data (pd.DataFrame): Raw dataset.
        country (str): Country code to filter.

    Output:
        pd.DataFrame: Cleaned and filtered dataset.
    """

    df = data.copy()

    # Split the first column (unit, sex, age, region) into separate columns
    first_col = df.columns[0]

    parts = df[first_col].astype(str).str.split(",", expand=True)
    parts = parts.iloc[:, :4]  # garante no máximo 4
    parts.columns = ["unit", "sex", "age", "region"]
    parts = parts.apply(lambda s: s.astype(str).str.strip())

    df = df.drop(columns=[first_col])
    df = pd.concat([parts, df], axis=1)

    # Reshape data from wide to long format (one row per year)
    df_long = df.melt(
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value",
    )

    # Clean and validate year and value fields
    df_long["year"] = df_long["year"].astype(str).str.strip()
    df_long = df_long[df_long["year"].str.fullmatch(r"\d{4}", na=False)]
    df_long["year"] = df_long["year"].astype(int)

    # Clean value field:
    # - remove flags (e.g. "80.6 e")
    # - convert to float
    # - drop missing values
    df_long["value"] = (
        df_long["value"]
        .astype(str)
        .str.strip()
        .replace({":": pd.NA})
        .str.replace(",", ".", regex=False)
        .str.extract(r"([-]?\d+(?:\.\d+)?)", expand=False)
    )

    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")
    df_long = df_long.dropna(subset=["value"])

    # Filter data for the specified country only
    country_code = country.strip().upper()
    df_country = df_long[df_long["region"] == country_code].copy()
    df_country = df_country[["unit", "sex", "age", "region", "year", "value"]]

    return df_country


def main(country: str = 'PT') -> pd.DataFrame:
    """
    Does:
        Run the full pipeline: load -> clean -> save.

    Args:
        country (str): Country code to process.

    Output:
        pd.DataFrame: Cleaned DataFrame
    """
    raw_path = RAW_DATA_DIR / "eu_life_expectancy_raw.tsv"

    df_raw = load_data(raw_path)
    df_clean = clean_data(df_raw, country)
    save_data(df_clean, country)
    return df_clean


def _parse_args() -> argparse.Namespace:  # pragma: no cover
    """
    Parse command-line arguments for the cleaning pipeline.

    Args:
        None

    Output:
        argparse.Namespace: Parsed CLI arguments (e.g., country).
    """

    parser = argparse.ArgumentParser(description="Clean life expectancy data for a given country.")
    parser.add_argument(
        "--country",
        type = str,
        default="PT",
        help="Country code to filter by (default: PT).",
    )
    return parser.parse_args()


if __name__ == "__main__":  # pragma: no cover
    args = _parse_args()
    main(args.country)
