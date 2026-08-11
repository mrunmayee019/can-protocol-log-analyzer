import sqlite3


def get_latency_analysis():

    connection = sqlite3.connect("data/can_logs.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT timestamp
        FROM CAN_MESSAGES
        ORDER BY timestamp
    """)

    timestamps = cursor.fetchall()

    connection.close()

    if len(timestamps) < 2:
        return {
            "average_latency": 0,
            "minimum_latency": 0,
            "maximum_latency": 0
        }

    latencies = []

    for i in range(1, len(timestamps)):

        previous_time = timestamps[i - 1][0]
        current_time = timestamps[i][0]

        latency = current_time - previous_time

        latencies.append(latency)

    return {
        "average_latency": sum(latencies) / len(latencies) * 1000,
        "minimum_latency": min(latencies) * 1000,
        "maximum_latency": max(latencies) * 1000
    }