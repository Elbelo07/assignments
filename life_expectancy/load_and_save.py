from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path(__file__).parent / "data" / "raw_data"
PROCESSED_DATA_DIR = Path(__file__).parent / "data" / "processed_data"

def load_data(file_path: Path) -> pd.DataFrame:
    """
    Does:
        Load the raw TSV file and return the raw DataFrame.

    Args:
        file_path (Path): Path to the raw TSV file.

    Output:
        pd.DataFrame: Raw dataset as a pandas DataFrame.
    """
    return pd.read_csv(file_path, sep="\t")

def save_data(data: pd.DataFrame, country: str) -> None:
    """
    Does:
        Save the cleaned DataFrame to the processed_data folder.

    Args:
        data (pd.DataFrame): Cleaned dataset.
        country (str): Country code used for naming the output file.

    Output:
        None
    """

    df = data.copy()

    # Save cleaned dataset without index
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DATA_DIR / f"{country.lower()}_life_expectancy.csv"
    df.to_csv(out_path, index=False)
