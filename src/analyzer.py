import sqlite3

connection = sqlite3.connect("data/can_logs.db")

cursor = connection.cursor()

print("Connected to CAN database")

cursor.execute("""
SELECT status, COUNT(*)
FROM CAN_MESSAGES
GROUP BY status
""")

results = cursor.fetchall()

print("\n===== CAN STATUS ANALYSIS =====")

total_messages = 0
error_messages = 0

for status, count in results:
    print(f"{status}: {count}")

    total_messages += count

    if status != "OK":
        error_messages += count

error_rate = (error_messages / total_messages) * 100

print("\n===== CAN RELIABILITY ANALYSIS =====")
print(f"Total Messages : {total_messages}")
print(f"Error Messages : {error_messages}")
print(f"Error Rate     : {error_rate:.2f}%")

# NODE-WISE ERROR ANALYSIS

cursor.execute("""
SELECT node,
       COUNT(*) AS total_messages,
       SUM(CASE WHEN status != 'OK' THEN 1 ELSE 0 END) AS error_messages
FROM CAN_MESSAGES
GROUP BY node
ORDER BY error_messages DESC
""")

node_results = cursor.fetchall()

print("\n===== NODE-WISE ERROR ANALYSIS =====")

for node, total, errors in node_results:
    error_rate = (errors / total) * 100

    print(
        f"{node}: "
        f"Total={total}, "
        f"Errors={errors}, "
        f"Error Rate={error_rate:.2f}%"
    )
    # MESSAGE-ID ERROR ANALYSIS

cursor.execute("""
SELECT message_id,
       COUNT(*) AS total_messages,
       SUM(CASE WHEN status != 'OK' THEN 1 ELSE 0 END) AS error_messages
FROM CAN_MESSAGES
GROUP BY message_id
ORDER BY error_messages DESC
LIMIT 10
""")

message_results = cursor.fetchall()

print("\n===== TOP 10 MESSAGE IDS WITH MOST ERRORS =====")

for message_id, total, errors in message_results:
    error_rate = (errors / total) * 100

    print(
        f"{message_id}: "
        f"Total={total}, "
        f"Errors={errors}, "
        f"Error Rate={error_rate:.2f}%"
    )

connection.close()