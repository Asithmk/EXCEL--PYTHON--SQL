
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "students_raw.xlsx"
OUTPUT_FILE = BASE_DIR / "data" / "students_cleaned.csv"

# Required dataset columns
REQUIRED_COLUMNS = [
    "Student_ID",
    "Name",
    "Average Grade",
    "Nationality",
    "Age",
    "Rent",
    "Food Cost",
    "IQ",
    "Ambition"
]

# Convert ambition categories into numerical scores
AMBITION_MAP = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Extreme": 4
}


def extract_data():
    """Extract student data from the Excel file."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Excel file not found: {INPUT_FILE}"
        )

    df = pd.read_excel(INPUT_FILE)

    # Remove unnecessary spaces from column names
    df.columns = df.columns.str.strip()

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    print("Data extracted successfully.")
    print("Original records:", len(df))

    return df


def transform_data(df):
    """Clean and transform the student dataset."""

    df = df.copy()
    original_count = len(df)

    # Standardise student names
    df["Name"] = (
        df["Name"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    # Standardise nationality
    df["Nationality"] = (
        df["Nationality"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    # Remove records with missing student IDs
    df["Student_ID"] = pd.to_numeric(
        df["Student_ID"], errors="coerce"
    )

    df = df.dropna(subset=["Student_ID"])
    df["Student_ID"] = df["Student_ID"].astype(int)

    # Remove duplicate student IDs
    df = df.drop_duplicates(
        subset=["Student_ID"],
        keep="first"
    )

    # Convert numeric columns
    numeric_columns = [
        "Average Grade",
        "Age",
        "Rent",
        "Food Cost",
        "IQ"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    # Handle invalid age values
    df.loc[~df["Age"].between(0, 120), "Age"] = pd.NA

    # Handle negative living costs
    for column in ["Rent", "Food Cost"]:
        df.loc[df[column] < 0, column] = pd.NA

    # Handle invalid IQ values
    df.loc[~df["IQ"].between(0, 200), "IQ"] = pd.NA

    # Fill missing numeric values with medians
    for column in numeric_columns:
        median_value = df[column].median()

        if pd.notna(median_value):
            df[column] = df[column].fillna(median_value)

    # Calculate total living costs
    df["Total"] = df["Rent"] + df["Food Cost"]

    # Standardise ambition categories
    df["Ambition"] = (
        df["Ambition"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    # Create numerical ambition scores
    df["Ambition_Score"] = df["Ambition"].map(
        AMBITION_MAP
    )

    # Display cleaning statistics
    print("\nDATA QUALITY REPORT")
    print("-------------------")
    print("Original records:", original_count)
    print("Cleaned records:", len(df))
    print("Removed records:", original_count - len(df))
    print("Remaining missing values:", df.isna().sum().sum())

    return df


def load_data(df):
    """Export the cleaned dataset to CSV."""

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCleaned dataset exported successfully.")
    print("Output file:", OUTPUT_FILE)


def main():
    """Execute the complete ETL pipeline."""

    print("Starting Student Data ETL Pipeline...\n")

    raw_data = extract_data()

    cleaned_data = transform_data(raw_data)

    load_data(cleaned_data)

    print("\nETL pipeline completed successfully!")


if __name__ == "__main__":
    main()
