import pandas as pd
import os


input_folder = r"C:\Users\Skeletron\Desktop\dataset"


for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        print(f"Processing file: {filename}")
        

        df = pd.read_csv(file_path, low_memory=False)
        
        # Fillign missing values
        df['tcp.window_size'] = df['tcp.window_size'].fillna(0)
        df['tcp.flags'] = df['tcp.flags'].fillna(0)
        df['tcp.srcport'] = df['tcp.srcport'].fillna(0)
        df['tcp.dstport'] = df['tcp.dstport'].fillna(0)
        df['udp.srcport'] = df['udp.srcport'].fillna(0)
        df['udp.dstport'] = df['udp.dstport'].fillna(0)
        df['udp.length'] = df['udp.length'].fillna(0)
        df['ip.proto'] = df['ip.proto'].fillna(0)
        
        # Dropping dns.qry.name and http.host due to high missing values
        df.drop(columns=['dns.qry.name', 'http.host'], inplace=True)
        

        df.to_csv(file_path, index=False)
        print(f"Data handling complete for {filename} and saved.")

print("All CSVs handled successfully.")
