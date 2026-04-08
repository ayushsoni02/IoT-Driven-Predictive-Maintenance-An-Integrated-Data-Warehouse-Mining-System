import sqlite3
import pandas as pd
import warnings
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from mlxtend.frequent_patterns import apriori, association_rules

# Suppress annoying math warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

def run_data_mining():
    conn = sqlite3.connect('factory_warehouse.db')
    df = pd.read_sql_query("SELECT temp, vibration, pressure FROM Fact_SensorReadings", conn)
    conn.close()

    print("--- Phase 1: Clustering (K-Means) ---")
    # Scaling data makes K-Means math much more stable
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(scaled_data)
    
    print("Clustering successful. Grouping data into Healthy, Warning, and Critical states.")
    print(f"Cluster counts:\n{df['cluster'].value_counts()}\n")

    print("--- Phase 2: Association Rule Mining (Apriori) ---")
    # We define 'Events' based on the specific spikes we created in generator.py
    basket = pd.DataFrame()
    basket['High_Temp'] = df['temp'] > 80        # Lowered from 85
    basket['High_Vib'] = df['vibration'] > 8    # Lowered from 10
    basket['Low_Press'] = df['pressure'] < 90    # Raised from 80

    # min_support=0.001 is very sensitive (looks for patterns in 0.1% of data)
    frequent_itemsets = apriori(basket, min_support=0.001, use_colnames=True)
    
    if not frequent_itemsets.empty:
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
        if not rules.empty:
            print("💡 Discovered Maintenance Rules:")
            # Show rules where confidence is high (likely to happen)
            high_conf = rules[rules['confidence'] > 0.5]
            print(high_conf[['antecedents', 'consequents', 'support', 'confidence']])
        else:
            print("No strong rules found yet.")
    else:
        print("No patterns found. Ensure the generator.py created enough anomalies!")

if __name__ == "__main__":
    run_data_mining()