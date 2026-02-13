from pathlib import Path
import argparse
import pandas as pd

RAW_DATA_DIR = Path(__file__).parent / "data" / "raw_data"
PROCESSED_DATA_DIR = Path(__file__).parent / "data" / "processed_data"
DATA_TSV_PATH =  RAW_DATA_DIR / "eu_life_expectancy_raw.tsv"


def load_data() -> pd.DataFrame:
    """
    Load the raw TSV file and return the raw DataFrame.
    """

    df = pd.read_csv(DATA_TSV_PATH, sep="\t")
    return df


def clean_data(data: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Clean the raw life expectancy dataset and return a cleaned DataFrame.
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

def save_data(data: pd.DataFrame, country: str) -> None:
    """
    Save the cleaned dataframe to CSV under life_Expectancy/data/data_cleaned/.
    """
    df = data.copy()

    # Save cleaned dataset without index
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DATA_DIR / f"{country.lower()}_life_expectancy.csv"
    df.to_csv(out_path, index=False)


def main(country: str = 'PT') -> None:
    """
    Run the full pipeline: load -> clean -> save
    """
    df_raw = load_data()
    df_clean = clean_data(df_raw, country)
    save_data(df_clean, country)


def _parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the cleaning pipeline.
    """
    parser = argparse.ArgumentParser(description="Clean life expectancy data for a given country.")
    parser.add_argument(
        "--country",
        type = str,
        default="PT",
        help="Country code to filter by (default: PT).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    main(args.country)
