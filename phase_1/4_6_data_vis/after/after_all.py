import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Folder containing all handled CSV files
input_folder = r"C:\Users\Skeletron\Desktop\dataset"

# Process all CSV files
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        print(f"Processing file: {filename}")
        
        # Load CSV
        df = pd.read_csv(file_path, low_memory=False)
        
        # Correlation heatmap
        plt.figure(figsize=(10, 8))
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        corr = numeric_df.corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')
        plt.title('Correlation Heatmap - 1.csv')
        plt.tight_layout()
        plt.show()
        
        # Plot missing values percentage
        missing_percent = df.isnull().mean() * 100
        plt.figure(figsize=(12, 6))
        missing_percent.plot(kind='bar', color='skyblue')
        plt.title(f'Percentage of Missing Values After Handling - {filename}')
        plt.xlabel('Columns')
        plt.ylabel('Percentage Missing (%)')
        plt.xticks(rotation=45, ha="right")
        plt.show()
        
        # TCP/UDP Port and Flags Distribution
        plt.figure(figsize=(8, 6))
        tcp_flag_counts = df['tcp.flags'].value_counts().sort_index()
        tcp_flag_counts.plot(kind='bar', color='lightcoral')
        plt.title(f'Distribution of TCP Flags After Handling - {filename}')
        plt.xlabel('TCP Flag Values')
        plt.ylabel('Count')
        plt.xticks(rotation=0)
        plt.show()
        
        # Protocol Distribution Check
        plt.figure(figsize=(8, 6))
        protocol_counts = df['ip.proto'].value_counts().rename({6: 'TCP', 17: 'UDP', 1: 'ICMP', 50: 'ESP', 103: 'PIM'})
        protocol_counts.plot(kind='bar', color='lightblue')
        plt.title(f'Protocol Distribution After Handling - {filename}')
        plt.xlabel('Protocol')
        plt.ylabel('Packet Count')
        plt.xticks(rotation=0)
        plt.show()
        
        #Malicious vs Non-Malicious
        plt.figure(figsize=(8, 5))
        counts = df['is_malicious'].value_counts()
        counts.index = counts.index.map({0: 'Non-Malicious', 1: 'Malicious'})
        counts.plot(kind='bar', color=['green', 'red'], alpha=0.7)
        plt.title('Malicious vs Non-Malicious Traffic Count')
        plt.xlabel('Traffic Type')
        plt.ylabel('Number of Flows')
        plt.xticks(rotation=0)

        # Add exact counts on bars
        for i, v in enumerate(counts):
            plt.text(i, v, str(v), ha='center', va='bottom')

        plt.show()

        # Top 10 Source and Destination IPs
        plt.figure(figsize=(10, 5))
        df['ip.src'].value_counts().head(10).plot(kind='bar', color='lightgreen')
        plt.title(f'Top 10 Source IPs After Handling - {filename}')
        plt.xlabel('Source IP')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha="right")
        plt.show()
        
        plt.figure(figsize=(10, 5))
        df['ip.dst'].value_counts().head(10).plot(kind='bar', color='lightblue')
        plt.title(f'Top 10 Destination IPs After Handling - {filename}')
        plt.xlabel('Destination IP')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha="right")
        plt.show()
        
        # Frame Length Distribution
        plt.figure(figsize=(8, 6))
        sns.histplot(df['frame.len'].dropna(), bins=50, kde=True, color='orange')
        plt.title(f'Frame Length Distribution After Handling - {filename}')
        plt.xlabel('Frame Length')
        plt.ylabel('Frequency')
        plt.show()
