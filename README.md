# 🎓 Student Data ETL & MySQL Integration
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)

## 📊 Project Overview
This project demonstrates a complete data pipeline: generating a mock student dataset in Excel, performing deep cleaning and normalization in **Pandas**, and migrating the finalized data into a **MySQL Relational Database**.

---

## 🛠️ Data Pipeline Stages

### 1. Data Extraction & Ingestion
* **Source:** Created a custom Excel dataset containing randomized student information.
* **Ingestion:** Utilized **Pandas** to import the `.xlsx` file and initialize a structured DataFrame.



### 2. Data Cleaning & Transformation (Wrangling)
To ensure high data integrity, the following transformations were applied:
* **String Normalization:** Simplified all student names for consistent formatting.
* **Imputation:** Handled missing or "impossible" numerical values by calculating and applying the **Mean** or **Median** of the dataset.
* **Feature Encoding:** Mapped categorical columns (strings) into numerical values to make the data machine-learning ready.

### 3. Database Loading (MySQL)
* **Connectivity:** Established a secure connection to a local database instance using `mysql-connector-python`.
* **Injection:** Iterated through the cleaned DataFrame to insert records into a pre-configured SQL table.



---

## 📂 Project Structure
* `data/` - Contains the raw Excel source file.
* `scripts/` - Python scripts for data cleaning and SQL migration.
* `database/` - SQL schema files for the student table.

---

## 🚀 Technical Requirements
* **Python 3.x**
* **Pandas** (`pip install pandas`)
* **Openpyxl** (`pip install openpyxl`)
* **MySQL Connector** (`pip install mysql-connector-python`)

---
*Data Engineering & Database Management Project*
