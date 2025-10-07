from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def forecast_column(df, column="Revenue", periods=5):
    if "Date" not in df.columns: return None
    df = df.sort_values("Date")
    X = np.arange(len(df)).reshape(-1,1)
    y = df[column].values
    model = LinearRegression()
    model.fit(X,y)
    future_X = np.arange(len(df)+periods).reshape(-1,1)
    forecast = model.predict(future_X)
    return forecast[-periods:]
