import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "parcelpilot.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def get_account(account_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM accounts
            WHERE account_id = ?
            """,
            (account_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def get_order(order_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE order_id = ?
            """,
            (order_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def get_ticket(ticket_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tickets
            WHERE ticket_id = ?
            """,
            (ticket_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()

def get_orders_for_account(account_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE account_id = ?
            """,
            (account_id,)
        )

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def get_tickets_for_account(account_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tickets
            WHERE account_id = ?
            """,
            (account_id,)
        )

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()



                        