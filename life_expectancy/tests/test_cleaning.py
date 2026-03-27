"""Tests for the cleaning module"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pandas as pd

from life_expectancy.cleaning import clean_data, main
from life_expectancy.load_and_save import load_data, save_data
from life_expectancy.region import Region


def test_load_data_returns_dataframe() -> None:
    """Unit: load_data returns a non-empty DataFrame from the TSV fixture."""
    raw_path = Path("life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv")
    df = load_data(raw_path)

    assert isinstance(df, pd.DataFrame), "load_data should return a DataFrame."
    assert not df.empty, "Loaded DataFrame should not be empty."


def test_clean_data(
    eu_life_expectancy_raw: pd.DataFrame,
    pt_life_expectancy_expected: pd.DataFrame
) -> None:
    """Does: Clean raw fixture for PT and compare with expected fixture.
    Args:
        eu_life_expectancy_raw: raw TSV sample fixture as DataFrame
        pt_life_expectancy_expected: expected cleaned PT DataFrame
    Output:
        None
    """
    result = clean_data(eu_life_expectancy_raw, Region.PT).reset_index(drop=True)
    expected = pt_life_expectancy_expected.reset_index(drop=True)

    pd.testing.assert_frame_equal(result, expected)


@patch("pandas.DataFrame.to_csv", autospec=True)
def test_save_data_calls_to_csv(mock_to_csv) -> None:
    """Unit: save_data should call DataFrame.to_csv (mocked)."""
    df = pd.DataFrame({"a": [1]}).copy()

    save_data(df, Region.PT)

    mock_to_csv.assert_called_once()



@patch("life_expectancy.cleaning.save_data", autospec=True)
@patch("life_expectancy.cleaning.load_data", autospec=True)
def test_main_returns_dataframe_and_triggers_save(
    mock_load_data,
    mock_save_data,
    eu_life_expectancy_raw,
) -> None:
    """Unit: main should return cleaned df and call save_data without writing to disk."""

    # Arrange
    mock_load_data.return_value = eu_life_expectancy_raw.copy()

    # Act
    df_clean = main(Region.PT)

    # Assert
    assert isinstance(df_clean, pd.DataFrame)
    assert not df_clean.empty
    assert (df_clean["region"] == Region.PT.value).all()

    mock_load_data.assert_called_once()
    mock_save_data.assert_called_once()

def test_region_actual_countries_returns_only_two_letter_codes() -> None:
    """Does: Ensure Region.actual_countries returns only real countries."""
    actual_countries = Region.actual_countries()

    assert actual_countries
    assert all(2 <= len(region.value) <= 3 for region in actual_countries)
    assert all(region.value.isalpha() for region in actual_countries)
    assert Region.PT in actual_countries
    assert Region.EU28 not in actual_countries
    assert Region.EFTA not in actual_countries
    assert Region.EA19 not in actual_countries
    assert Region.DE_TOT not in actual_countries
