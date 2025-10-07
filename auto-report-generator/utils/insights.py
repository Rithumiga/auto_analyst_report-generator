import pandas as pd

def correlation_analysis(df):
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns
    return df[numeric_cols].corr()

def trend_detection(df, column="Revenue"):
    if "Date" not in df.columns: return df
    df['Trend'] = df[column].diff().apply(lambda x: "Up" if x>0 else "Down")
    return df[['Date', column, 'Trend']]

def kpi_summary(df):
    summary = {}
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns
    for col in numeric_cols:
        summary[col] = {
            "total": df[col].sum(),
            "average": df[col].mean(),
            "max": df[col].max(),
            "min": df[col].min()
        }
    return summary
