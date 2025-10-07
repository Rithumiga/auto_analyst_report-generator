🚀 AutoAnalyst – AI-Powered Data Analysis & Visualization Tool
🧠 Overview

AutoAnalyst is an intelligent data analysis system that allows users to upload any dataset (CSV) and interact with it using natural language queries.
It combines data visualization, summarization, and NLP understanding to deliver insights instantly — without writing a single line of code.

This project demonstrates the fusion of Streamlit UI, Machine Learning/NLP logic, and database integration, making it a complete data analytics assistant powered by AI.

💡 Key Features
Feature	Description
📊 Data Upload	Upload CSV files and automatically detect numeric & categorical columns
💬 Natural Language Query	Ask questions like “What is the average price of houses in Delhi?” or “Show sales greater than 5000”
📈 Smart Visualizations	Auto-generates bar, line, pie, and scatter charts using Plotly
🔍 Automatic Summarization	Uses either Grok API (if connected) or a local summarizer to extract insights
🧩 Database Integration	Automatically stores uploaded data in MySQL for reuse
🧮 Data Filtering	Supports filters like greater than, less than, between, equals
🤖 Aggregation Understanding	Understands queries like maximum, average, total, count, etc.
🧰 Multi-Domain Ready	Works with datasets in domains like Cars, Sales, Stocks, House Prices, etc.
🏗️ Project Architecture
autoanalyst/
│
├── app.py                  # Streamlit main UI file
│
├── utils/
│   ├── charts.py           # Handles all chart generations (Bar, Pie, Line)
│   ├── summarizer.py       # Handles summarization (API or local)
│   ├── data_processing.py  # Upload, cleaning, numeric & text column detection
│   ├── nlp_query.py        # Main natural language query logic
│
├── database/
│   ├── db_connect.py       # MySQL connection and table creation
│
├── data/
│   └── sample.csv          # Example dataset
│
├── README.md               # Project Documentation
└── requirements.txt        # Dependencies
