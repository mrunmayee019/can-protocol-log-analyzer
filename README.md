# 🚗 CAN Protocol Log Analyzer

A Python-based CAN (Controller Area Network) communication monitoring and log analysis system designed to analyze vehicle communication data, detect CAN errors, and visualize communication health.

## 📌 Features

- CAN message log generation and analysis
- SQLite database storage
- CAN message status analysis
- CAN node-wise error analysis
- Communication timing and latency analysis
- FastAPI REST API
- Interactive Streamlit dashboard
- CAN communication health monitoring
- Interactive CAN log explorer
- CAN error investigation
- API monitoring
- Data visualization and reporting

## 🛠️ Technologies Used

- Python
- Pandas
- SQLite
- FastAPI
- Streamlit
- Matplotlib
- REST API
- CAN Protocol

## 📊 Dashboard

The dashboard provides:

- Total CAN messages
- Successful messages
- Total communication errors
- Error rate
- CAN message status distribution
- CAN node error analysis
- Communication timing analysis
- CAN message timing visualization
- CAN communication health
- CAN log explorer
- CAN error investigation
- API monitoring

## 🏗️ Project Structure

```text
communication-protocol-log-analyser/
│
├── data/
│   └── can_logs.csv
│
├── reports/
│   ├── can_analysis_report.txt
│   ├── status_distribution.png
│   ├── node_error_distribution.png
│   └── top_message_errors.png
│
├── src/
│   ├── analyzer.py
│   ├── api.py
│   ├── can_generator.py
│   ├── database.py
│   ├── latency_analysis.py
│   ├── report_generator.py
│   └── visualization.py
│
├── dashboard.py
├── requirements.txt
├── .gitignore
└── README.md