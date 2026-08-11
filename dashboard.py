import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

log_df = pd.read_csv("data/can_logs.csv")

import sys
sys.path.append("src")

from latency_analysis import get_latency_analysis

# Page Configuration

st.set_page_config(
    page_title="CAN Protocol Log Analyzer",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 CAN Protocol Log Analyzer")
st.markdown("### Vehicle Communication Monitoring Dashboard")

# Professional Dashboard Styling

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    font-size: 3rem !important;
    font-weight: 700 !important;
}

h2, h3 {
    font-weight: 650 !important;
}

[data-testid="stMetric"] {
    background-color: #1b1e27;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #30343f;
}

[data-testid="stMetricValue"] {
    font-size: 2rem;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
}

div[data-testid="stExpander"] {
    border-radius: 12px;
    border: 1px solid #30343f;
}

</style>
""", unsafe_allow_html=True)

# Get data from FastAPI

API_URL = "http://127.0.0.1:8000/summary"

try:
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()

        total_messages = data["total_messages"]
        status_distribution = data["status_distribution"]

    else:
        st.error("Could not fetch data from API.")

except Exception as e:
    st.error("API is not running. Please start FastAPI first.")
    st.stop()

# KPI Cards

col1, col2, col3, col4 = st.columns(4)

total_errors = sum(
    count
    for status, count in status_distribution.items()
    if status != "OK"
)

successful_messages = status_distribution.get("OK", 0)

error_rate = (
    total_errors / total_messages * 100
    if total_messages > 0
    else 0
)

with col1:
    st.metric(
        "Total CAN Messages",
        total_messages
    )

with col2:
    st.metric(
        "Successful Messages",
        successful_messages
    )

with col3:
    st.metric(
        "Total Errors",
        total_errors
    )

with col4:
    st.metric(
        "Error Rate",
        f"{error_rate:.2f}%"
    )

# Status Distribution

st.divider()

st.subheader("📊 CAN Message Status Distribution")

df_status = pd.DataFrame(
    list(status_distribution.items()),
    columns=["Status", "Count"]
)

col1, col2 = st.columns(2)

with col1:
    st.dataframe(
        df_status,
        use_container_width=True
    )

with col2:
    fig, ax = plt.subplots()

    ax.bar(
        df_status["Status"],
        df_status["Count"]
    )

    ax.set_xlabel("Status")
    ax.set_ylabel("Number of Messages")
    ax.set_title("CAN Message Status Distribution")

    st.pyplot(fig)

# Node-wise Error Analysis

st.divider()

st.subheader("📡 CAN Node Error Analysis")


# Total messages for each node
node_total = log_df.groupby("node").size()

# Error messages for each node
node_errors = log_df[log_df["status"] != "OK"].groupby("node").size()

# Create node analysis table
df_node = pd.DataFrame({
    "Total Messages": node_total,
    "Errors": node_errors
}).fillna(0)

# Convert errors to integer
df_node["Errors"] = df_node["Errors"].astype(int)

# Calculate error rate
df_node["Error Rate (%)"] = (
    df_node["Errors"] / df_node["Total Messages"] * 100
).round(2)

# Sort by highest error rate
df_node = df_node.sort_values(
    "Error Rate (%)",
    ascending=False
)

# Display table and chart
col1, col2 = st.columns(2)

with col1:
    st.dataframe(
        df_node,
        use_container_width=True
    )

with col2:
    fig, ax = plt.subplots()

    ax.bar(
        df_node.index.astype(str),
        df_node["Errors"]
    )

    ax.set_xlabel("CAN Node")
    ax.set_ylabel("Number of Errors")
    ax.set_title("Errors by CAN Node")

    st.pyplot(fig)

# Latency Analysis

st.divider()

st.subheader("⏱️ CAN Communication Timing Analysis")

latency_data = get_latency_analysis()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Inter-Message Time",
        f"{latency_data['average_latency']:.3f} ms"
    )

with col2:
    st.metric(
        "Minimum Inter-Message Time",
        f"{latency_data['minimum_latency']:.3f} ms"
    )

with col3:
    st.metric(
        "Maximum Inter-Message Time",
        f"{latency_data['maximum_latency']:.3f} ms"
    )

# CAN Communication Health

st.divider()

st.subheader("🚦 CAN Communication Health")

# Find node with highest error rate
node_health = {}

connection = sqlite3.connect("data/can_logs.db")
cursor = connection.cursor()

cursor.execute("""
SELECT node, status
FROM CAN_MESSAGES
""")

rows = cursor.fetchall()
connection.close()

for node, status in rows:

    if node not in node_health:
        node_health[node] = {
            "total": 0,
            "errors": 0
        }

    node_health[node]["total"] += 1

    if status != "OK":
        node_health[node]["errors"] += 1


# Calculate error rates
for node in node_health:

    total = node_health[node]["total"]
    errors = node_health[node]["errors"]

    node_health[node]["error_rate"] = (
        errors / total * 100
        if total > 0
        else 0
    )


# Find worst node
worst_node = max(
    node_health,
    key=lambda x: node_health[x]["error_rate"]
)

worst_error_rate = node_health[worst_node]["error_rate"]


# Determine overall health
if error_rate < 5:
    health_status = "🟢 HEALTHY"
elif error_rate < 20:
    health_status = "🟡 WARNING"
else:
    health_status = "🔴 CRITICAL"


# Display health status
st.markdown(
    f"## {health_status}"
)

st.write(
    "Overall CAN communication health based on "
    "message error rate."
)


# Health metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Overall Error Rate",
        f"{error_rate:.2f}%"
    )

with col2:
    st.metric(
        "Total Errors",
        total_errors
    )

with col3:
    st.metric(
        "Highest Error Node",
        worst_node
    )

with col4:
    st.metric(
        "Worst Node Error Rate",
        f"{worst_error_rate:.2f}%"
    )


# Warning messages
if error_rate >= 20:

    st.error(
        f"🚨 Critical CAN communication error rate detected: "
        f"{error_rate:.2f}%"
    )

elif error_rate >= 5:

    st.warning(
        f"⚠️ CAN communication requires attention. "
        f"Error rate is {error_rate:.2f}%."
    )

else:

    st.success(
        f"✅ CAN communication is operating normally. "
        f"Error rate is {error_rate:.2f}%."
    )


if worst_error_rate >= 25:

    st.warning(
        f"⚠️ {worst_node} has the highest error rate "
        f"({worst_error_rate:.2f}%)."
    )
# CAN Log Explorer

st.divider()

st.subheader("🔎 CAN Log Explorer")

# Connect to database
connection = sqlite3.connect("data/can_logs.db")

# Load CAN messages
logs_df = pd.read_sql_query(
    """
    SELECT *
    FROM CAN_MESSAGES
    ORDER BY timestamp
    """,
    connection
)

connection.close()

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    node_options = ["All Nodes"] + sorted(
        logs_df["node"].dropna().unique().tolist()
    )

    selected_node = st.selectbox(
        "CAN Node",
        node_options
    )

with col2:
    status_options = ["All Status"] + sorted(
        logs_df["status"].dropna().unique().tolist()
    )

    selected_status = st.selectbox(
        "Message Status",
        status_options
    )

with col3:
    message_limit = st.selectbox(
        "Number of Messages",
        [25, 50, 100, 250, 500]
    )


# Apply filters
filtered_df = logs_df.copy()

if selected_node != "All Nodes":
    filtered_df = filtered_df[
        filtered_df["node"] == selected_node
    ]

if selected_status != "All Status":
    filtered_df = filtered_df[
        filtered_df["status"] == selected_status
    ]


# Limit displayed records
filtered_df = filtered_df.head(message_limit)


# Results summary
st.write(
    f"Showing **{len(filtered_df)}** matching CAN messages."
)

# Display messages
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)
# Error Investigation

st.divider()

st.subheader("🚨 CAN Error Investigation")

error_df = log_df[log_df["status"] != "OK"].copy()

if len(error_df) > 0:

    col1, col2 = st.columns(2)

    with col1:
        error_type = st.selectbox(
            "Select Error Type",
            ["All Errors"] + sorted(
                error_df["status"].unique().tolist()
            )
        )

    with col2:
        error_node = st.selectbox(
            "Select CAN Node",
            ["All Nodes"] + sorted(
                error_df["node"].unique().tolist()
            )
        )

    investigation_df = error_df.copy()

    if error_type != "All Errors":
        investigation_df = investigation_df[
            investigation_df["status"] == error_type
        ]

    if error_node != "All Nodes":
        investigation_df = investigation_df[
            investigation_df["node"] == error_node
        ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Errors",
            len(investigation_df)
        )

    with col2:
        affected_nodes = investigation_df["node"].nunique()
        st.metric(
            "Affected Nodes",
            affected_nodes
        )

    with col3:
        affected_messages = investigation_df["message_id"].nunique()
        st.metric(
            "Affected Message IDs",
            affected_messages
        )

    st.write("### Error Details")

    st.dataframe(
        investigation_df[
            [
                "timestamp",
                "node",
                "message_id",
                "direction",
                "status",
                "payload"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:
    st.success("No CAN communication errors found.")
# API Monitoring

st.divider()

st.subheader("🔍 API Monitoring")

# API Status
st.success("🟢 FastAPI Connected — Status 200 OK")

# API information
col1, col2 = st.columns(2)

with col1:
    st.write("**API Endpoint**")
    st.code("/summary")

with col2:
    st.write("**Response Status**")
    st.code("200 OK")

# Response summary
st.markdown("### 📋 Response Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Messages", total_messages)

with col2:
    st.metric("Successful", successful_messages)

with col3:
    st.metric("Errors", total_errors)

with col4:
    st.metric("Error Rate", f"{error_rate:.2f}%")

# Raw JSON
with st.expander("🧾 View Raw API Response"):
    st.json(data)