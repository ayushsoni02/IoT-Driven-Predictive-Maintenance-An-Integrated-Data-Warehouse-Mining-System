import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IoT Maintenance Dashboard", layout="wide")
st.title("🏭 Industrial IoT Predictive Maintenance Warehouse")

# Load data from Warehouse
conn = sqlite3.connect('factory_warehouse.db')
df = pd.read_sql_query("SELECT * FROM Fact_SensorReadings", conn)
df_machines = pd.read_sql_query("SELECT * FROM Dim_Machine", conn)
conn.close()

# Sidebar info
st.sidebar.header("Warehouse Stats")
st.sidebar.write(f"Total Readings: {len(df)}")
st.sidebar.write(f"Machines Monitored: {len(df_machines)}")

# Tab 1: Warehouse View
tab1, tab2 = st.tabs(["Warehouse Data", "Mining Insights"])

with tab1:
    st.subheader("Data Warehouse (Fact Table)")
    st.dataframe(df.head(20))
    
    st.subheader("Sensor Trends")
    fig = px.line(df, x='timestamp', y='temp', color='machine_key', title="Temperature over Time")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Data Mining: Cluster Analysis")
    fig_scatter = px.scatter(df, x='temp', y='vibration', color='status', 
                             title="Clusters: Temperature vs Vibration")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.info("The clusters above identify 'Warning' states where maintenance is required.")

st.sidebar.subheader("System Alerts")
# If the latest reading is in the "Critical" cluster
latest_reading = df.iloc[-1]
if latest_reading['status'] == "Warning":
    st.sidebar.error(f"⚠️ Warning: Machine {latest_reading['machine_key']} showing anomaly!")
else:
    st.sidebar.success("✅ All Systems Normal")