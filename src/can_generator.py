import random
import csv
NODES = [ 
    "ENGINE_ECU",
    "ABS_ECU",
    "DASHBOARD",
    "AIRBAG_ECU",
    "STEERING_ECU",
]

DIRECTIONS = [
    "TX",
    "RX"
]
STATUS = [
    "OK",
    "OK",
    "OK",
    "OK",
    "OK",
    "OK",
    "OK",
    "OK",
    "OK",
    "ERROR",
    "TIMEOUT",
    "CRC_FAIL"
]
def generate_message(timestamp):
    node = random.choice(NODES)
    message_id = f"0x{random.randint(0x100, 0x1FF):X}"
    direction = random.choice(DIRECTIONS)
    status = random.choice(STATUS)
    payload = " ".join(f"{random.randint(0,255):02X}"
    for _ in range(8)
)
    message = {
        "timestamp": timestamp, 
        "node": node,
        "message_id": message_id,
        "direction": direction,
        "status": status,
        "payload": payload
    } 

    
    return message 
messages = []
timestamp = 0.0
   
for i in range (5000):
    timestamp += random.uniform(0.001, 0.005)
    timestamp = round(timestamp, 4)
    message = generate_message(timestamp)
    messages.append(message)

with open("data/can_logs.csv", "w", newline="") as file:
    fieldnames = [
        "timestamp",
        "node",
        "message_id",
        "direction",
        "status",
        "payload"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(messages)