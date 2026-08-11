import sqlite3
import matplotlib.pyplot as plt

# Connect to database
connection = sqlite3.connect("data/can_logs.db")
cursor = connection.cursor()

# Get top 10 message IDs with most errors
cursor.execute("""
SELECT
    message_id,
    COUNT(*) AS total,
    SUM(
        CASE
            WHEN status != 'OK' THEN 1
            ELSE 0
        END
    ) AS errors
FROM CAN_MESSAGES
GROUP BY message_id
HAVING errors > 0
ORDER BY errors DESC
LIMIT 10
""")

results = cursor.fetchall()

message_ids = [row[0] for row in results]
errors = [row[2] for row in results]

# Create chart
plt.figure(figsize=(10, 5))

plt.bar(message_ids, errors)

plt.title("Top 10 CAN Message IDs with Most Errors")
plt.xlabel("Message ID")
plt.ylabel("Number of Errors")

plt.xticks(rotation=45)

plt.tight_layout()

# Save chart
plt.savefig("reports/top_message_errors.png")

plt.show()

connection.close()