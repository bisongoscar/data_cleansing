# Multi-File CSV/Excel Cleaner App

A Streamlit app to clean data files (CSV, XLSX, or XLS) for data analysis.

## Overview

The Multi-File CSV/Excel Cleaner App allows you to:
- **Upload one or more data files:** Provide your "dirty" Excel or CSV data.
- **Preview the data:** See previews of both the raw and cleaned data.
- **Clean the data:** The app performs several cleaning operations:
  - **Column Name Cleaning:** Trims whitespace, removes duplicate columns, and standardizes column names.
  - **Cell Value Cleaning:** Trims spaces, consolidates multiple spaces, and converts values like `"null"`, `"unknown"`, and `"error"` to missing values.
  - **Data Type Conversion:** Automatically converts date-like and numeric text fields to the appropriate data types.
  - **Data Cleanup:** Removes empty columns, duplicate rows, and rows with any missing values.
- **Download the cleaned CSV files:** Each cleaned file is saved as `clean_<original_filename>.csv`.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/bisongoscar/data_cleansing.git
    cd data_cleansing
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the App

Run the Streamlit app with:

```bash
streamlit run data_cleaning.py