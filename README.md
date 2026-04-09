# Industrial IoT Predictive Maintenance System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Active-orange)

An integrated, end-to-end data pipeline that simulates an Industrial Internet of Things (IIoT) environment. This system combines **Data Warehousing**, **Machine Learning (Data Mining)**, and an **Interactive Dashboard** to predict machine failures before they happen (Predictive Maintenance).

## What is this Project About?
In modern manufacturing, machines (like turbines, pumps, and motors) are equipped with sensors that continuously monitor physical metrics (temperature, vibration, pressure).
This project provides a full-stack simulation of such an environment:
1. **Data Generation**: Simulates realistic sensor readings and systematically injects "failure patterns" (e.g., sudden heat and vibration spikes).
2. **Data Warehousing (ETL)**: Transforms raw data into a structured Star Schema and loads it into a SQLite database.
3. **Data Mining (ML)**: Uses unsupervised machine learning (K-Means Clustering) to identify the "health state" of machines and Association Rule Mining (Apriori) to discover hidden correlations between sensor readings.
4. **Interactive Dashboard**: A Streamlit web application providing a real-time window into the warehouse, visualizing sensor trends and triggering predictive alerts.

## Why Predictive Maintenance?
Traditional maintenance operates on a "fix it when it breaks" (reactive) or "fix it every X days" (preventative) schedule. **Predictive Maintenance** uses data to predict *when* a machine is likely to fail, allowing engineers to intervene exactly when needed. This:
- Reduces costly downtime.
- Minimizes unnecessary maintenance.
- Increases the lifespan of expensive industrial equipment.

## Key Features
* **ETL Pipeline & Star Schema**: Utilizes Fact and Dimension tables (`Fact_SensorReadings`, `Dim_Machine`) for optimized, scalable data querying.
* **K-Means Clustering**: Automatically categorizes machine states into *Healthy*, *Warning*, and *Critical* based on scaled multi-dimensional sensor data.
* **Apriori Algorithm (Market Basket Analysis)**: Discovers strong association rules (e.g., patterns leading to equipment failure or warnings).
* **Live Dashboard**: Interactive Plotly charts for tracing sensor trends across individual machines over time. 

## 🛠️ Tech Stack & Requirements
* **Language & Core:** Python 3
* **Data Processing & ETL:** Pandas, NumPy, SQLite3
* **Machine Learning:** Scikit-Learn (K-Means, StandardScaler), MLxtend (Apriori)
* **Visualization:** Streamlit, Plotly Express

For a complete list of dependencies, see `requirements.txt`.

## 📂 Project Structure
```text
IoT_Maintenance_Project/
│
├── generator.py            # Generates simulated raw sensor data (CSV)
├── warehouse_setup.py      # ETL process to load data into SQLite Star Schema
├── mining_engine.py        # K-Means clustering and Apriori rule mining
├── app.py                  # Streamlit Dashboard application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation (this file)
```

## 🚀 Installation & Setup

**1. Clone the repository and navigate to the directory**
```bash
cd IoT_Maintenance_Project
```

**2. Create a virtual environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

## 🕹️ How to Run the System

To experience the full pipeline, execute the scripts in the following order:

### Step 1: Generate Raw Data
Run the data generator to create the simulated IIoT environment data.
```bash
python generator.py
```
> *This will generate a `raw_factory_data.csv` file containing simulated normal and anomalous sensor readings.*

### Step 2: Build the Data Warehouse
Run the ETL script to transform the CSV data and load it into a SQLite Star Schema.
```bash
python warehouse_setup.py
```
> *This creates `factory_warehouse.db`, populates `Dim_Machine`, and inserts readings into `Fact_SensorReadings`.*

### Step 3: Run the Data Mining Engine
Execute the machine learning models to discover clusters and association rules.
```bash
python mining_engine.py
```
> *This script will output the results of K-Means clustering (health states) and high-confidence Apriori rules discovered from the failure patterns injected in Step 1.*

### Step 4: Launch the Dashboard
Start the Streamlit application to visualize the warehouse data and view real-time alerts.
```bash
streamlit run app.py
```
> *Your browser will open automatically (usually to `http://localhost:8501`) displaying the interactive Predictive Maintenance Dashboard.*

## 📈 Future Enhancements
* Implementing supervised models (e.g., Random Forest or XGBoost) to predict the exact "Time to Failure".
* Deploying the dashboard to the cloud (AWS/GCP/Heroku).
* Transitioning from SQLite to a robust Cloud Data Warehouse like Google BigQuery or Snowflake.
* Real-time streaming integration with Apache Kafka for live sensor data ingestion.
