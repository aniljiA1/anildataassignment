📊 SQL Query Dashboard
(Streamlit / Flask Version — Trade Data Analysis)

This project provides a web-based SQL Query Dashboard where users can:

Upload trade data (Excel/CSV)

Run predefined SQL reports

Write & execute custom SQL queries

Visualize results in an interactive UI

View YoY trends, top HSN codes, supplier analysis, and more

The backend uses SQLite for quick analytics, while the frontend runs on Streamlit or Flask (optional).

🚀 Features
✅ 1. ETL + Cleaning

Parses raw trade data (Excel/CSV)

Extracts model, model number, capacity, material, unit price

Normalizes units & quantities

Computes:

Grand Total (INR)

Landed Cost / Unit

Category → Subcategory

✅ 2. Database Loader

Loads cleaned data into SQLite

Creates indexes for fast searching


2️⃣ Install dependencies
pip install -r requirements.txt

run at: python test_read_file.py
