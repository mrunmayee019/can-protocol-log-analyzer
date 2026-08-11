import sqlite3

connection = sqlite3.connect("data/can_logs.db")
cursor = connection.cursor()

# Total messages
cursor.execute("SELECT COUNT(*) FROM CAN_MESSAGES")
total = cursor.fetchone()[0]

# Successful messages
cursor.execute("""
SELECT COUNT(*)
FROM CAN_MESSAGES
WHERE status = 'OK'
""")
successful = cursor.fetchone()[0]

# Errors
errors = total - successful

# Error rate
error_rate = (errors / total) * 100

# Status counts
cursor.execute("""
SELECT status, COUNT(*)
FROM CAN_MESSAGES
GROUP BY status
""")

status_results = cursor.fetchall()

# Node-wise errors
cursor.execute("""
SELECT node, COUNT(*)
FROM CAN_MESSAGES
WHERE status != 'OK'
GROUP BY node
ORDER BY COUNT(*) DESC
""")

node_results = cursor.fetchall()

# Generate report
with open("reports/can_analysis_report.txt", "w") as file:

    file.write("====================================\n")
    file.write("       CAN PROTOCOL LOG REPORT\n")
    file.write("====================================\n\n")

    file.write(f"Total CAN Messages : {total}\n")
    file.write(f"Successful Messages: {successful}\n")
    file.write(f"Total Errors       : {errors}\n")
    file.write(f"Overall Error Rate : {error_rate:.2f}%\n\n")

    file.write("----- STATUS SUMMARY -----\n")

    for status, count in status_results:
        file.write(f"{status:<10}: {count}\n")

    file.write("\n----- NODE ERROR SUMMARY -----\n")

    for node, count in node_results:
        file.write(f"{node:<15}: {count} errors\n")

connection.close()

print("CAN analysis report generated successfully!")