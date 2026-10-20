# Smart Garment Cluster Management System — Streamlit Edition

A simple local prototype for a student project inspired by the Nagpur Readymade Garment Cluster case study.

## Features
- Dashboard with inventory, products, production orders and low-stock alerts
- Inventory: add materials, update quantities/minimum levels, search and delete
- Production orders: create orders, filter by status, update and delete
- Product catalogue: search/filter products and add catalogue entries
- SQLite database that stores changes locally
- Clearly labelled fictional sample data for demonstration

## Run on Ubuntu / Linux

Open a terminal in this folder and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`. Open it in your browser.

## Data storage
The app creates `garment_cluster.db` in this folder on first run. This file stores all records you add or edit. Keep a backup if you want to preserve your data.

## Important note
This is a student prototype, not an official SFURTI application. The preloaded records are fictional sample data and are not actual cluster business records.
