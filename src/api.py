from fastapi import FastAPI
import sqlite3

app = FastAPI(title="CAN Protocol Log Analyzer")


def get_connection():
    return sqlite3.connect("data/can_logs.db")


@app.get("/")
def home():
    return {
        "message": "CAN Protocol Log Analyzer API is running"
    }


@app.get("/summary")
def summary():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM CAN_MESSAGES
    """)
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM CAN_MESSAGES
        GROUP BY status
    """)
    status_data = cursor.fetchall()

    connection.close()

    return {
        "total_messages": total,
        "status_distribution": {
            status: count for status, count in status_data
        }
    }