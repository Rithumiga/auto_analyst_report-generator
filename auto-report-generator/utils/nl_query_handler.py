import re
import pandas as pd
from difflib import get_close_matches

# --------------------------
# 🔹 Query Examples Library
# --------------------------
QUERY_BANK = {
    "cars": [
        "What is the maximum price of cars?",
        "Show me all cars with mileage greater than 20.",
        "Which car has the highest horsepower?",
        "List cars with price less than 1000000.",
        "Average mileage of diesel cars.",
        "Show all cars manufactured by Toyota.",
        "What is the minimum engine size?",
        "Find total number of electric cars.",
        "List all SUV type cars.",
        "Show cars between 2015 and 2020.",
        # ... Add ~100 more similar variations
    ],

    "sales": [
        "Total sales in January.",
        "Show revenue by product category.",
        "Which product has the highest sales?",
        "Average sales amount per region.",
        "Show me all orders greater than 1000 units.",
        "Sum of sales for Electronics.",
        "Top 5 customers by total purchase.",
        "Total revenue in 2024.",
        "Find minimum sales recorded.",
        "List sales between 10000 and 50000.",
        # ... Add ~100 more sales queries
    ],

    "stocks": [
        "What is the highest stock price?",
        "Average closing price of Apple.",
        "Show me all stocks greater than 500.",
        "Minimum opening price recorded.",
        "Total trading volume for Tesla.",
        "Stocks between 2020 and 2023.",
        "Which company had the lowest price?",
        "List stocks less than 100.",
        "Find mean price for all companies.",
        "Show daily price count.",
        # ... Add ~100 more stock queries
    ],

    "house": [
        "Average price of houses.",
        "List houses with price greater than 5000000.",
        "Which house has the largest area?",
        "Minimum number of bedrooms.",
        "Total number of houses in Chennai.",
        "Show all apartments built after 2010.",
        "Find houses between 1000 and 2000 sq ft.",
        "What is the maximum house price?",
        "Count houses available for sale.",
        "Show houses with garden.",
        # ... Add ~100 more real estate queries
    ]
}


# --------------------------
# 🔹 Detect Column Function
# --------------------------
def detect_column(df, query):
    query = query.lower()
    cols = [col.lower() for col in df.columns]

    # Exact match
    for col in cols:
        if col in query:
            return df.columns[cols.index(col)]

    # Fuzzy match
    words = query.split()
    for word in words:
        match = get_close_matches(word, cols, n=1, cutoff=0.7)
        if match:
            return df.columns[cols.index(match[0])]

    return None


# --------------------------
# 🔹 Filter Data by Query
# --------------------------
def filter_data_by_query(df, query):
    query = query.lower()
    df_filtered = df.copy()

    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    text_cols = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]

    # === Aggregation Keywords ===
    agg_map = {
        "average": "mean",
        "mean": "mean",
        "sum": "sum",
        "total": "sum",
        "count": "count",
        "maximum": "max",
        "highest": "max",
        "max": "max",
        "minimum": "min",
        "lowest": "min",
        "min": "min"
    }

    agg_func = None
    for word, func in agg_map.items():
        if word in query:
            agg_func = func
            break

    # Detect target column
    target_col = detect_column(df, query)
    if not target_col and numeric_cols:
        if "price" in [c.lower() for c in df.columns]:
            target_col = [c for c in df.columns if c.lower() == "price"][0]
        else:
            target_col = numeric_cols[0]

    # === Numeric Filters ===
    greater_match = re.search(r'greater than (\d+)', query)
    less_match = re.search(r'less than (\d+)', query)
    between_match = re.search(r'between (\d+)\s*and\s*(\d+)', query)

    if between_match:
        val1, val2 = map(float, between_match.groups())
        for col in numeric_cols:
            temp = df_filtered[(df_filtered[col] >= val1) & (df_filtered[col] <= val2)]
            if not temp.empty:
                df_filtered = temp
                break

    elif greater_match:
        val = float(greater_match.group(1))
        for col in numeric_cols:
            temp = df_filtered[df_filtered[col] > val]
            if not temp.empty:
                df_filtered = temp
                break

    elif less_match:
        val = float(less_match.group(1))
        for col in numeric_cols:
            temp = df_filtered[df_filtered[col] < val]
            if not temp.empty:
                df_filtered = temp
                break

    # === Text Filtering ===
    text_words = query.split()
    for word in text_words:
        for col in text_cols:
            matches = df_filtered[df_filtered[col].astype(str).str.lower().str.contains(word)]
            if not matches.empty:
                df_filtered = matches
                break

    # === Aggregation Result ===
    if agg_func and target_col in df_filtered.columns:
        try:
            result_value = getattr(df_filtered[target_col], agg_func)()
            return pd.DataFrame({f"{agg_func.upper()} of {target_col}": [result_value]})
        except Exception as e:
            print("Aggregation Error:", e)

    return df_filtered


# --------------------------
# 🔹 Helper: Get Random Queries for Testing
# --------------------------
def get_sample_queries(domain="cars", n=10):
    if domain not in QUERY_BANK:
        return []
    import random
    return random.sample(QUERY_BANK[domain], min(n, len(QUERY_BANK[domain])))
