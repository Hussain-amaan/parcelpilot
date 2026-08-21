import sqlite3
from pathlib import Path
import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
DB_PATH = DATA_DIR / "parcelpilot.db"

def create_database():
    """Load the CSV files into a SQLite database."""

    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # CSV paths
    accounts_file = RAW_DATA_DIR / "accounts.csv"
    orders_file = RAW_DATA_DIR / "orders.csv"
    tickets_file = RAW_DATA_DIR / "tickets.csv"

    # Check files exist
    for file in [accounts_file, orders_file, tickets_file]:
        if not file.exists():
            raise FileNotFoundError(f"Missing file: {file}")

    # Load CSV files
    accounts = pd.read_csv(accounts_file)
    orders = pd.read_csv(orders_file)
    tickets = pd.read_csv(tickets_file)

    # Remove accidental empty/unnamed columns
    accounts = accounts.loc[
        :, ~accounts.columns.str.startswith("Unnamed")
    ]

    orders = orders.loc[
        :, ~orders.columns.str.startswith("Unnamed")
    ]

    tickets = tickets.loc[
        :, ~tickets.columns.str.startswith("Unnamed")
    ]

    # Create SQLite database
    connection = sqlite3.connect(DB_PATH)

    try:
        accounts.to_sql(
            "accounts",
            connection,
            if_exists="replace",
            index=False
        )

        orders.to_sql(
            "orders",
            connection,
            if_exists="replace",
            index=False
        )

        tickets.to_sql(
            "tickets",
            connection,
            if_exists="replace",
            index=False
        )

        connection.commit()

    finally:
        connection.close()

    print("Database created successfully!")
    print(f"Location: {DB_PATH}")
    print()

    print(f"Accounts: {len(accounts)}")
    print(f"Orders:   {len(orders)}")
    print(f"Tickets:  {len(tickets)}")

if __name__ == "__main__":
    create_database()