import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), "auto_report_db.sqlite")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY,
                    filename TEXT,
                    filetype TEXT,
                    size_kb REAL,
                    upload_time TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY,
                    report_name TEXT,
                    generated_time TEXT,
                    file_path TEXT
                )''')
    conn.commit()
    conn.close()

def add_file(filename, filetype, size_kb):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO files (filename, filetype, size_kb, upload_time) VALUES (?, ?, ?, ?)",
              (filename, filetype, size_kb, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def add_report(report_name, file_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO reports (report_name, generated_time, file_path) VALUES (?, ?, ?)",
              (report_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file_path))
    conn.commit()
    conn.close()

def fetch_files():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM files")
    data = c.fetchall()
    conn.close()
    return data

def fetch_reports():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM reports")
    data = c.fetchall()
    conn.close()
    return data
