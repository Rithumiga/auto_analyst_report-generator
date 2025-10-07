import streamlit as st
import pandas as pd
from utils.data_processing import merge_multiple_files, clean_text, numeric_columns
from utils.summarizer import summarize_text
from utils.charts import generate_chart
from utils.report_generator import generate_docx_report
from utils.insights import correlation_analysis, trend_detection, kpi_summary
from utils.predictive_analysis import forecast_column
from utils.nl_query_handler import filter_data_by_query
import os

st.set_page_config(page_title="🔥 Hackathon Auto Report Generator", layout="wide")

st.title("🚀 Advanced Automated Report Generator")

# -----------------------------
# Multi-file Upload
# -----------------------------
uploaded_files = st.file_uploader("Upload multiple CSV/Excel/PDF files", type=["csv","xlsx","pdf"], accept_multiple_files=True)
if uploaded_files:
    # Merge data if multiple files
    df_list = [f for f in uploaded_files if f.name.endswith(("csv","xlsx"))]
    if df_list:
        df = merge_multiple_files(df_list)
        st.subheader("Merged Data Preview")
        st.dataframe(df.head())

        # KPI cards
        kpis = kpi_summary(df)
        for k, v in kpis.items():
            st.metric(label=f"Total {k}", value=v['total'], delta=f"Avg: {v['average']:.2f}")

        # Correlation & Trend
        st.subheader("Correlation Matrix")
        st.dataframe(correlation_analysis(df))
        st.subheader("Trend Detection")
        st.dataframe(trend_detection(df))

        # -----------------------------
        # Natural Language Query
        # -----------------------------
        query = st.text_input("Natural Language Query for Charts", "")
        if query:
            df_filtered = filter_data_by_query(df, query)
        else:
            df_filtered = df

        # Charting
        num_cols = numeric_columns(df_filtered)
        if num_cols:
            chart_type = st.selectbox("Chart Type", ["bar","line","pie","scatter"])
            x_axis = st.selectbox("X-axis", df_filtered.columns)
            y_axis = st.selectbox("Y-axis", num_cols)
            fig, chart_path = generate_chart(df_filtered, chart_type, x_axis, y_axis, title=f"{y_axis} vs {x_axis}")
            st.plotly_chart(fig)

            # Predictive forecast
            if st.checkbox("Forecast next 5 periods"):
                forecast = forecast_column(df_filtered, y_axis, periods=5)
                st.line_chart(forecast)

        # Summary using Grok
        summary_text = summarize_text(str(df_filtered.describe()), "Key Insights")
        st.subheader("Grok Insights")
        st.write(summary_text)

        # Generate DOCX Report
        if st.button("Generate DOCX Report"):
            report_title = st.text_input("Report Title", "Automated Hackathon Report")
            report_path = generate_docx_report(report_title, summary_text, [chart_path])
            st.success(f"Report saved at {report_path}")
            st.download_button("Download Report", report_path)

from utils.db_manager import init_db, add_file, add_report

# Initialize database at app startup
init_db()

# When a user uploads a file
uploaded_file = st.file_uploader("Upload CSV/Excel/PDF", type=["csv", "xlsx", "pdf"])
if uploaded_file is not None:
    add_file(uploaded_file.name, uploaded_file.type, uploaded_file.size / 1024)

# When a report is generated
report_path = "generated_reports/sales_report.pdf"
add_report("Sales Report", report_path)

import sqlite3
import pandas as pd
import streamlit as st
import os

# Path to your SQLite DB
DB_PATH = os.path.join(os.getcwd(), "auto_report_db.sqlite")

st.header("📊 Database Viewer")

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Fetch tables
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in c.fetchall()]
st.write(f"**Tables in Database:** {tables}")

# Option to select table
table_to_view = st.selectbox("Select Table to View", tables)

if table_to_view:
    df = pd.read_sql_query(f"SELECT * FROM {table_to_view}", conn)
    st.subheader(f"Data from `{table_to_view}`")
    st.dataframe(df)  # interactive table in Streamlit

conn.close()

import streamlit as st
from utils.data_processing import filter_data_by_query
import plotly.express as px
from utils.nl_query_handler import filter_data_by_query

nl_query = st.text_input("💬 Ask something about your data:")
if nl_query:
    df_result = filter_data_by_query(df, nl_query)
    if df_result.empty:
        st.warning("No data matched your query. Try rephrasing.")
    else:
        st.success(f"Showing results for: {nl_query}")
        st.dataframe(df_result)
