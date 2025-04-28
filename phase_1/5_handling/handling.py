import pandas as pd


file_path = r"C:\Users\Skeletron\Desktop\dataset\testing.csv"
df = pd.read_csv(file_path, low_memory=False)

#Filling  missing values
df['tcp.window_size'] = df['tcp.window_size'].fillna(0)
df['tcp.flags'] = df['tcp.flags'].fillna(0)
df['tcp.srcport'] = df['tcp.srcport'].fillna(0)
df['tcp.dstport'] = df['tcp.dstport'].fillna(0)
df['udp.srcport'] = df['udp.srcport'].fillna(0)
df['udp.dstport'] = df['udp.dstport'].fillna(0)
df['udp.length'] = df['udp.length'].fillna(0)
df['ip.proto'] = df['ip.proto'].fillna(0)

# Droping dns.qry.name and http.host due to high missing values
df.drop(columns=['dns.qry.name', 'http.host'], inplace=True)

df.to_csv(file_path, index=False)
print("Data handling complete for testing.csv.")
    