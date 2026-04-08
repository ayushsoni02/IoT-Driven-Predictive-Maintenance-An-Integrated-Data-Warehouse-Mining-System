import sqlite3
import pandas as pd

def build_warehouse():
    # 1. Connect to SQLite (Creates the database file)
    conn = sqlite3.connect('factory_warehouse.db')
    cursor = conn.cursor()
    print("Warehouse connection established.")

    # 2. Create Dimension Table: Machines
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dim_Machine (
            machine_key INTEGER PRIMARY KEY,
            machine_id INTEGER,
            machine_type TEXT,
            location TEXT
        )
    ''')

    # 3. Create Fact Table: Sensor Readings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Fact_SensorReadings (
            fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_key INTEGER,
            timestamp DATETIME,
            temp REAL,
            vibration REAL,
            pressure REAL,
            status TEXT,
            FOREIGN KEY (machine_key) REFERENCES Dim_Machine (machine_key)
        )
    ''')

    # 4. ETL: Load static metadata into Dimensions
    machines_data = [
        (1, 101, 'Turbine', 'Section-A'),
        (2, 102, 'Hydraulic Pump', 'Section-B'),
        (3, 103, 'Electric Motor', 'Section-A')
    ]
    cursor.executemany('INSERT OR IGNORE INTO Dim_Machine VALUES (?,?,?,?)', machines_data)

    # 5. ETL: Load CSV data into Fact Table
    raw_data = pd.read_csv("raw_factory_data.csv")
    
    # Mapping machine_id to our warehouse keys
    mapping = {101: 1, 102: 2, 103: 3}
    raw_data['machine_key'] = raw_data['machine_id'].map(mapping)

    # Insert data
    for _, row in raw_data.iterrows():
        cursor.execute('''
            INSERT INTO Fact_SensorReadings (machine_key, timestamp, temp, vibration, pressure, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (row['machine_key'], row['timestamp'], row['sensor_temp'], 
              row['sensor_vibration'], row['sensor_pressure'], row['status']))

    conn.commit()
    conn.close()
    print("ETL Process Complete: Data is now in the Star Schema!")

if __name__ == "__main__":
    build_warehouse()