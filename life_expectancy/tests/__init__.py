"""Test suite for the 1st assignment"""
from pathlib import Path

PROJECT_DIR = Path(__file__).parents[2]
PACKAGE_DIR = PROJECT_DIR / "life_expectancy"
FIXTURES_DIR = Path(__file__).parent / "fixtures"
RAW_DIR = PACKAGE_DIR / "data" / "raw_data"
OUTPUT_DIR = PACKAGE_DIR / "data" / "processed_data"
