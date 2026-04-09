import pandas as pd
import numpy as np
import datetime
import os

def generate_factory_data(records=2000):
    print("Generating raw sensor data...")
    start_time = datetime.datetime.now()
    data = []
    
    # Machine IDs: 101 (Turbine), 102 (Pump), 103 (Motor)
    machines = [101, 102, 103]
    
    for i in range(records):
        m_id = np.random.choice(machines)
        timestamp = start_time + datetime.timedelta(minutes=i)
        
        # Base values (Normal)
        temp = np.random.normal(70, 2)
        vibration = np.random.normal(5, 1)
        pressure = np.random.normal(100, 5)
        status = "Healthy"
        
        # Injecting realistic 'Failure Patterns' using probabilities
        rand_val = np.random.random()
        
        if m_id == 101:
            # Machine 101: Heat and Vibration issues
            if rand_val < 0.05: # 5% Critical
                temp = np.random.normal(105, 5)
                vibration = np.random.normal(16, 2)
                status = "Critical"
            elif rand_val < 0.20: # 15% Warning
                temp = np.random.normal(90, 4)
                vibration = np.random.normal(10, 1.5)
                status = "Warning"
                
        elif m_id == 102:
            # Machine 102: Pressure loss issues
            if rand_val < 0.05: # 5% Critical
                pressure = np.random.normal(50, 8)
                status = "Critical"
            elif rand_val < 0.20: # 15% Warning
                pressure = np.random.normal(75, 5)
                status = "Warning"
                
        elif m_id == 103:
            # Machine 103: Combined issues (Motor wear)
            if rand_val < 0.05: # 5% Critical
                temp = np.random.normal(100, 5)
                vibration = np.random.normal(14, 2)
                pressure = np.random.normal(60, 6)
                status = "Critical"
            elif rand_val < 0.20: # 15% Warning
                temp = np.random.normal(85, 3)
                vibration = np.random.normal(9, 1.5)
                pressure = np.random.normal(80, 5)
                status = "Warning"

        data.append({
            "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "machine_id": m_id,
            "sensor_temp": round(temp, 2),
            "sensor_vibration": round(vibration, 2),
            "sensor_pressure": round(pressure, 2),
            "status": status
        })

    df = pd.DataFrame(data)
    df.to_csv("raw_factory_data.csv", index=False)
    print(f"Success! Created 'raw_factory_data.csv' with {records} rows.")
    print(f"\nStatus distribution:\n{df['status'].value_counts().to_string()}\n")

if __name__ == "__main__":
    generate_factory_data()