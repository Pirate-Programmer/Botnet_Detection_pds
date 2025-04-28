import pandas as pd
import os

input_folder = r"C:\Users\Skeletron\Desktop\dataset"


for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        print(f"Processing file: {filename}")
        
        
        df = pd.read_csv(file_path, low_memory=False)
        
        
        df['frame.time_epoch'] = pd.to_datetime(df['frame.time_epoch'], unit='s', errors='coerce')
        
        
        df['ip.src'] = df['ip.src'].str.split(',').str[0]
        df['ip.dst'] = df['ip.dst'].str.split(',').str[0]
        df['ip.src'] = df['ip.src'].astype('category').cat.add_categories('<empty>').fillna('<empty>')
        df['ip.dst'] = df['ip.dst'].astype('category').cat.add_categories('<empty>').fillna('<empty>')
        
       
        def is_hex(value):
            try:
                int(value, 16)
                return True
            except (ValueError, TypeError):
                return False
        
        df['tcp.flags'] = df['tcp.flags'].apply(lambda x: int(x, 16) if pd.notna(x) and is_hex(x) else pd.NA).astype('Int64')
        
        
        numeric_cols = [
            'frame.number', 'frame.len', 'ip.proto', 'tcp.srcport',
            'tcp.dstport', 'tcp.flags', 'tcp.window_size',
            'udp.srcport', 'udp.dstport', 'udp.length'
        ]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').astype('Int64')
        
        
        df.to_csv(file_path, index=False)
        print(f"Data cleaning complete for {filename} and saved.")

print("All CSVs cleaned successfully.")
