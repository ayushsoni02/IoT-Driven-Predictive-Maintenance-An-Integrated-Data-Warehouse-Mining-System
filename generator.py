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
        
        # Injecting 'Failure Patterns' for Data Mining to find later
        # Logic: If Machine 101 gets hot and vibrates, it's 'Failing'
        if m_id == 101 and i % 150 == 0:
            temp += 25       # Heat spike
            vibration += 12  # Vibration spike
            status = "Warning"
            
        # Logic: If Machine 102 loses pressure suddenly
        if m_id == 102 and i % 200 == 0:
            pressure -= 30
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

if __name__ == "__main__":
    generate_factory_data()