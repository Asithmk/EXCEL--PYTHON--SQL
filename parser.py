import pandas as pd
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Project paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "students_raw.xlsx"
OUTPUT_FILE = BASE_DIR / "data" / "students_cleaned.csv"

AMBITION_MAP = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Extreme": 4
}


def extract_data():
    """Extract student data from Excel."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"File not found: {INPUT_FILE}")

    df = pd.read_excel(INPUT_FILE)

    # Standardise column names
    df.columns = df.columns.str.strip()

    # Support both Student ID and Student_ID
    df = df.rename(columns={"Student ID": "Student_ID"})

    required_columns = [
        "Student_ID", "Name", "Average Grade",
        "Nationality", "Age", "Rent",
        "Food Cost", "IQ", "Ambition"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    print("Data extracted successfully.")
    print("Original records:", len(df))

    return df


def transform_data(df):
    """Clean and transform student data."""

    df = df.copy()
    original_count = len(df)

       # Clean text columns
    for column in ["Name", "Nationality"]:
        df[column] = (
            df[column].astype("string").str.strip().str.title()
        )

    # Standardise nationality names
    df["Nationality"] = df["Nationality"].replace({
        "Usa": "USA",
        "Uk": "UK"
    })

    # Convert student IDs
    df["Student_ID"] = pd.to_numeric(
        df["Student_ID"], errors="coerce"
    )
    df = df.dropna(subset=["Student_ID"])
    df["Student_ID"] = df["Student_ID"].astype(int)

    # Remove duplicate student IDs
    df = df.drop_duplicates(subset=["Student_ID"], keep="first")

    # Convert numeric columns
    numeric_columns = [
        "Average Grade", "Age", "Rent", "Food Cost", "IQ"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Replace invalid values
    df.loc[~df["Age"].between(0, 120), "Age"] = pd.NA
    df.loc[df["Rent"] < 0, "Rent"] = pd.NA
    df.loc[df["Food Cost"] < 0, "Food Cost"] = pd.NA
    df.loc[~df["IQ"].between(0, 200), "IQ"] = pd.NA

    # Fill missing numeric values with medians
    for column in numeric_columns:
        median_value = df[column].median()
        if pd.notna(median_value):
            df[column] = df[column].fillna(median_value)

    # Calculate total living costs
    df["Total"] = df["Rent"] + df["Food Cost"]

    # Map ambition categories
    df["Ambition"] = (
        df["Ambition"].astype("string").str.strip().str.title()
    )
    df["Ambition_Score"] = df["Ambition"].map(AMBITION_MAP)

    print("\nDATA QUALITY REPORT")
    print("-------------------")
    print("Original records:", original_count)
    print("Cleaned records:", len(df))
    print("Removed records:", original_count - len(df))
    print("Remaining missing values:", df.isna().sum().sum())

    return df



def load_data(df):
    """Export cleaned data to CSV and load it into MySQL."""

    # Export cleaned data to CSV
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nCleaned dataset exported successfully.")
    print("Output:", OUTPUT_FILE)

    # Connect to MySQL
       # Connect to MySQL
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO students (
            student_id,
            name,
            average_grade,
            nationality,
            age,
            rent,
            food_cost,
            iq,
            ambition,
            total_living_cost,
            ambition_score
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            average_grade = VALUES(average_grade),
            nationality = VALUES(nationality),
            age = VALUES(age),
            rent = VALUES(rent),
            food_cost = VALUES(food_cost),
            iq = VALUES(iq),
            ambition = VALUES(ambition),
            total_living_cost = VALUES(total_living_cost),
            ambition_score = VALUES(ambition_score)
    """

    records = df[[
        "Student_ID",
        "Name",
        "Average Grade",
        "Nationality",
        "Age",
        "Rent",
        "Food Cost",
        "IQ",
        "Ambition",
        "Total",
        "Ambition_Score"
    ]].values.tolist()

    try:
        cursor.executemany(insert_query, records)
        connection.commit()

        print("\nMySQL database updated successfully.")
        print("Records processed:", cursor.rowcount)

    except mysql.connector.Error:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def main():
    print("Starting Student Data ETL Pipeline...\n")

    raw_data = extract_data()
    cleaned_data = transform_data(raw_data)
    load_data(cleaned_data)

    print("\nETL pipeline completed successfully!")


if __name__ == "__main__":
    main()
