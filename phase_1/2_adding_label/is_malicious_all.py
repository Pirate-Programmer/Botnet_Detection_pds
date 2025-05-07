import pandas as pd
import os

# Malicious IPs from ISOT dataset
MALICIOUS_IPS = {
    '172.16.2.11', '172.16.0.2', '172.16.0.11',
    '172.16.0.12', '172.16.2.12'
}


INPUT_FOLDER = r"C:\Users\eletSkron\Desktop\dataset"

for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith('.csv'):
        file_path = os.path.join(INPUT_FOLDER, filename)
        

        df = pd.read_csv(file_path)
        

        if 'is_malicious' not in df.columns:
            df['is_malicious'] = (
                df['ip.src'].isin(MALICIOUS_IPS) | 
                df['ip.dst'].isin(MALICIOUS_IPS)
            ).astype(int)
            
            # Overwrite original file
            df.to_csv(file_path, index=False)
            print(f" Added labels to {filename}")


