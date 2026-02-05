from pathlib import Path
import argparse
import pandas as pd



def clean_data(country: str = "PT") -> None:
    """
    Clean EU life expectancy data and generate a country-specific dataset.

    The function loads the raw Eurostat TSV file, reshapes it to long format,
    cleans year and value fields, filters data for the specified country, and saves the result
    as a CSV file.
    """

    # Load raw Eurostat life expectancy data (wide format)
    data_path = Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
    df = pd.read_csv(data_path, sep="\t")

    # Split the first column (unit, sex, age, region) into separate columns
    first_col = df.columns[0]
    parts = df[first_col].str.split(",", expand=True)
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
        .replace({":": None})
        .str.extract(r"([-]?\d+(?:\.\d+)?)", expand=False)
    )

    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")
    df_long = df_long.dropna(subset=["value"])
    df_long["value"] = df_long["value"].astype(float)

    # Filter data for the specified country only
    country = country.strip().upper()
    df_pt = df_long[df_long["region"] == country].copy()
    df_pt = df_pt[["unit", "sex", "age", "region", "year", "value"]]

    # Save cleaned dataset without index
    out_path = Path(__file__).parent / "data" / f"{country.lower()}_life_expectancy.csv"
    df_pt.to_csv(out_path, index=False)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean EU life expectancy dataset.")
    parser.add_argument(
        "--country",
        default="PT",
        help="Country code to filter by (default: PT).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    clean_data(country=args.country)
