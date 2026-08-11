import sqlite3
import csv

connection = sqlite3.connect("data/can_logs.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS CAN_MESSAGES (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL,
    node TEXT,
    message_id TEXT,
    direction TEXT,
    status TEXT,
    payload TEXT
)
""")
# with open("data/can_logs.csv", "r", newline="") as file:
#     reader = csv.DictReader(file)

#     for row in reader:
#         cursor.execute("""
#         INSERT INTO CAN_MESSAGES
#         (timestamp, node, message_id, direction, status, payload)
#         VALUES (?, ?, ?, ?, ?, ?)
#         """, (
#             row["timestamp"],
#             row["node"],
#             row["message_id"],
#             row["direction"],
#             row["status"],
#             row["payload"]
#         ))
connection.commit()

print("CAN data imported successfully")

cursor.execute("SELECT COUNT(*) FROM CAN_MESSAGES")

count = cursor.fetchone()[0]

print("Total CAN messages:", count)

connection.close()