import streamlit as st
import pandas as pd
import re

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the input DataFrame with several data cleaning operations:
    
    Column name cleaning:
       - Strip whitespace.
       - Remove duplicate columns.
       - Replace special characters with underscores.
       
    Cell value cleaning for object columns:
       - Trim whitespace and replace multiple spaces with a single space.
       - Replace values like "null", "unknown", and "error" (case-insensitive) with pd.NA.
       
    Data type conversions:
       - Attempt to convert object columns to datetime if at least 80% of non-null entries can be parsed as dates.
       - Attempt to convert object columns to numeric where applicable.
       
    Data cleanup:
       - Drop columns that are completely empty.
       - Remove duplicate rows.
       - Drop rows containing any missing values.
    """
    # Clean column names
    df.columns = df.columns.str.strip()
    # Remove duplicate columns, if any
    df = df.loc[:, ~df.columns.duplicated()]
    # Replace special characters with underscores (only allow letters, numbers, and underscores)
    df.columns = df.columns.str.replace(r'[^A-Za-z0-9_]+', '_', regex=True)
    
    # Clean cell values in object columns
    def clean_cell(cell):
        if isinstance(cell, str):
            # Trim whitespace and replace multiple spaces with a single space
            cell = cell.strip()
            cell = re.sub(r'\s+', ' ', cell)
            # Replace certain string values with missing values
            if cell.lower() in {"null", "unknown", "error"}:
                return pd.NA
        return cell
    
    df = df.applymap(clean_cell)
    
    # Data type conversions
    # Attempt to convert object columns to datetime if most of the data can be parsed as dates
    for col in df.select_dtypes(include=['object']).columns:
        converted = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)
        non_null_original = df[col].notna().sum()
        non_null_converted = converted.notna().sum()
        if non_null_original > 0 and (non_null_converted / non_null_original) >= 0.8:
            df[col] = converted

    # Attempt to convert remaining object columns to numeric where possible
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')
    
    # Data cleanup
    # Remove completely empty columns
    df.dropna(axis=1, how='all', inplace=True)
    # Remove duplicate rows
    df = df.drop_duplicates()
    # Drop rows with any missing values
    df = df.dropna()
    
    return df

st.title("Multi-File CSV/Excel Cleaner App")
st.markdown(
    """
    **Upload one or more data files** (CSV, XLSX, or XLS) to clean them.  
    The cleaning process includes:
    
    - **Column Name Cleaning:** Trims whitespace, removes duplicates, and standardizes names.
    - **Cell Value Cleaning:** Trims spaces, consolidates multiple spaces, and converts `"null"`, `"unknown"`, and `"error"` to missing values.
    - **Data Type Conversion:** Automatically converts date-like and numeric text fields.
    - **Data Cleanup:** Removes empty columns, duplicate rows, and rows with missing values.
    
    After cleaning, download each cleaned CSV file.
    """
)

uploaded_files = st.file_uploader(
    "Upload your CSV/Excel files",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            file_name = uploaded_file.name
            ext = file_name.split('.')[-1].lower()
            
            # Read the file based on its extension
            if ext == "csv":
                df = pd.read_csv(uploaded_file)
            elif ext in ["xlsx", "xls"]:
                df = pd.read_excel(uploaded_file)
            else:
                st.error(f"Unsupported file type: {file_name}")
                continue
            
            st.subheader(f"Raw Data Preview - {file_name}")
            st.dataframe(df.head())
            
            # Clean the DataFrame
            clean_df = clean_dataframe(df)
            st.subheader(f"Cleaned Data Preview - {file_name}")
            st.dataframe(clean_df.head())
            
            # Convert the cleaned DataFrame to CSV for download
            csv_data = clean_df.to_csv(index=False).encode('utf-8')
            # Generate new file name: "clean_" + original file name (with .csv extension)
            base_name = file_name.rsplit('.', 1)[0]
            new_file_name = f"clean_{base_name}.csv"
            
            st.download_button(
                label=f"Download Clean CSV for {file_name}",
                data=csv_data,
                file_name=new_file_name,
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"An error occurred while processing {file_name}: {e}")
