import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "parcelpilot.db"


connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

for table in ["accounts", "orders", "tickets"]:

    print(f"\n--- {table.upper()} ---")

    cursor.execute(f"PRAGMA table_info({table})")

    columns = cursor.fetchall()

    for column in columns:
        print(column[1])

connection.close()