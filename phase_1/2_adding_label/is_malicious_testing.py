import pandas as pd

# Malicious IPs from ISOT dataset
MALICIOUS_IPS = {
    '172.16.2.11', '172.16.0.2', '172.16.0.11',
    '172.16.0.12', '172.16.2.12'
}

# Path to your testing CSV
input_path = r"C:\Users\Skeletron\Desktop\dataset\testing.csv"

# Read the file
df = pd.read_csv(input_path, low_memory=False)

# Add label column (if not already present)
if 'is_malicious' not in df.columns:
    df['is_malicious'] = (
        df['ip.src'].isin(MALICIOUS_IPS) | 
        df['ip.dst'].isin(MALICIOUS_IPS)
    ).astype(int)
    

    df.to_csv(input_path, index=False)
    print(f" Added malicious labels to testing.csv")
    
    # Quick verification
    print("Label counts:")
    print(df['is_malicious'].value_counts())
