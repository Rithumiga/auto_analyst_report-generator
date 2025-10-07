import pandas as pd
import PyPDF2
import os

def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

def read_excel(file_path, sheet_name=0):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df.fillna(0, inplace=True)
    return df

def read_csv(file_path):
    df = pd.read_csv(file_path)
    df.fillna(0, inplace=True)
    return df

def clean_text(text):
    return " ".join(text.split())

def numeric_columns(df):
    return df.select_dtypes(include=['int64','float64']).columns.tolist()

def merge_multiple_files(file_list):
    combined_df = pd.DataFrame()
    for f in file_list:
        if f.name.endswith(".csv"):
            df = read_csv(f)
        else:
            df = read_excel(f)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df

import pandas as pd
import re

def filter_data_by_query(df, query):
    """
    Filter dataframe based on natural language query.
    Supports:
    - Exact string matches for categorical columns
    - Basic numeric filtering if mentioned
    Example query: "Show Revenue for Electronics in New York in Jan 2025"
    """
    df_filtered = df.copy()
    query_lower = query.lower()

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Check for numeric conditions like ">1000", "<5000"
            matches = re.findall(rf"{col}\s*([<>]=?)\s*(\d+)", query_lower)
            for op, val in matches:
                val = float(val)
                if op == ">":
                    df_filtered = df_filtered[df_filtered[col] > val]
                elif op == "<":
                    df_filtered = df_filtered[df_filtered[col] < val]
                elif op == ">=":
                    df_filtered = df_filtered[df_filtered[col] >= val]
                elif op == "<=":
                    df_filtered = df_filtered[df_filtered[col] <= val]
        else:
            # Categorical: check if any value appears in query
            for val in df[col].astype(str).unique():
                if val.lower() in query_lower:
                    df_filtered = df_filtered[df_filtered[col] == val]

    return df_filtered
