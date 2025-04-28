import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os


input_folder = r"C:\Users\Skeletron\Desktop\dataset"

# Initialize LabelEncoders for ip.src and ip.dst
src_encoder = LabelEncoder()
dst_encoder = LabelEncoder()

# Collecting unique IPs from all CSVs
all_src_ips, all_dst_ips = set(), set()

# Scan through all CSVs to gather unique IPs
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path, low_memory=False)
        
        # Add unique IPs to the sets
        all_src_ips.update(df['ip.src'].dropna().unique())
        all_dst_ips.update(df['ip.dst'].dropna().unique())

# Fit the encoders on the combined unique IPs
src_encoder.fit(list(all_src_ips))
dst_encoder.fit(list(all_dst_ips))

# Save the encoders for future use
joblib.dump(src_encoder, os.path.join(input_folder, 'ip_src_encoder.pkl'))
joblib.dump(dst_encoder, os.path.join(input_folder, 'ip_dst_encoder.pkl'))

print("Encoders trained and saved successfully.")

# Encode IPs in each CSV
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path, low_memory=False)
        
        # Apply Label Encoding
        df['ip.src'] = src_encoder.transform(df['ip.src'].fillna('<empty>'))
        df['ip.dst'] = dst_encoder.transform(df['ip.dst'].fillna('<empty>'))
        
        # Save the encoded data (overwrite the original)
        df.to_csv(file_path, index=False)
        print(f"{filename} encoded successfully.")

print("All CSVs encoded successfully.")
