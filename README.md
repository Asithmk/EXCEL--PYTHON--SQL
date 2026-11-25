# Student Data ETL Pipeline | Python, Excel & MySQL

A data engineering project that extracts student records from Excel, cleans and transforms the data using Python, and loads the processed records into a MySQL database for SQL-based analysis.

## Project Overview

This project demonstrates a basic ETL (Extract, Transform, Load) workflow using Python, Pandas, Excel, and MySQL.

The pipeline processes student information, handles missing and invalid values, calculates additional metrics, and stores the cleaned data in a relational database.

## Technologies Used

- **Python** – ETL pipeline implementation
- **Pandas** – Data cleaning and transformation
- **Excel** – Raw data source
- **MySQL** – Relational database storage
- **SQL** – Data analysis and reporting
- **python-dotenv** – Environment variable management

## Project Structure

```text
EXCEL--PYTHON--SQL/
│
├── data/
│   ├── students_raw.xlsx
│   └── students_cleaned.csv
│
├── database/
│   └── analysis_queries.sql
│
├── parser.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

Note: `students_cleaned.csv` is generated when the pipeline runs and is excluded from version control.

## ETL Pipeline

### 1. Extract

- Reads student records from an Excel file.
- Validates the required columns.
- Handles alternative column naming conventions.

### 2. Transform

- Standardises text fields and nationality names.
- Removes duplicate student IDs.
- Converts numeric fields into appropriate data types.
- Handles invalid ages, rent, food costs, and IQ values.
- Replaces missing numeric values using median imputation.
- Calculates total living costs.
- Converts ambition categories into numerical scores.

### 3. Load

- Exports the cleaned dataset to CSV.
- Loads records into MySQL.
- Uses duplicate-key handling to prevent duplicate student IDs during repeated runs.

## SQL Analysis

The project includes SQL queries to analyse:

1. Student records.
2. Average student grades.
3. Average living costs.
4. Living costs by nationality.
5. Students with the highest living costs.
6. Ambition distribution.
7. Students with above-average living costs.

## Setup and Installation

### Prerequisites

- Python 3
- MySQL Server
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Asithmk/EXCEL--PYTHON--SQL.git
cd EXCEL--PYTHON--SQL
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file using `.env.example` as a template.

Update the database credentials in `.env`:

```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=student_analytics
```

Never commit your actual `.env` file or database credentials.

### 5. Create the database

Start MySQL and execute:

```sql
CREATE DATABASE student_analytics;
```

Create the `students` table using the schema below:

```sql
USE student_analytics;

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    average_grade DECIMAL(4,2),
    nationality VARCHAR(50),
    age DECIMAL(5,2),
    rent DECIMAL(10,2),
    food_cost DECIMAL(10,2),
    iq DECIMAL(5,2),
    ambition VARCHAR(20),
    total_living_cost DECIMAL(10,2),
    ambition_score TINYINT
);
```

### 6. Run the ETL pipeline

```bash
python3 parser.py
```

### 7. Execute SQL analysis

```bash
mysql -u your_mysql_username -p < database/analysis_queries.sql
```

## Current Test Results

The pipeline has been tested locally with five student records.

- Original records: 5
- Cleaned records: 5
- Remaining missing values: 0
- Records stored in MySQL: 5
- Average student grade: 1.89
- Average living cost: 865.00

These results are based on the sample dataset included in the project.

## Future Improvements

- Add automated data quality tests.
- Introduce structured logging and error handling.
- Add data visualisations and dashboards.
- Expand the pipeline to support larger datasets.
- Improve database schema management.

## Author

**Asith Mallika Kankanamalage**

Information Engineering Student
Technical University of Munich (TUM)

GitHub: [@Asithmk](https://github.com/Asithmk)

## Acknowledgement

This project builds upon the original repository: [EXCEL--PYTHON--SQL](https://github.com/nissank19/EXCEL--PYTHON--SQL), with additional ETL, data validation, MySQL integration, and SQL analysis improvements.