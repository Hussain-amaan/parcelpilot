import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "parcelpilot.db"


connection = sqlite3.connect(DB_PATH)

cursor = connection.cursor()

# List tables
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table';
""")

tables = cursor.fetchall()

print("Tables:")
for table in tables:
    print("-", table[0])


connection.close()