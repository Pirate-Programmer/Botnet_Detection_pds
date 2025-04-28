import pandas as pd

#Loading the csv files
#low memory = false is req so pandas doesn't try to figure out the datatypes while the file is being loaded into the memory
file_path = r"C:\Users\Skeletron\Desktop\dataset\testing.csv"

df = pd.read_csv(
    file_path,
    dtype={"frame.number": "Int64", "dns.qry.name": "str", "http.host": "str"},
    low_memory=False,
    index_col=False
)

df['frame.time_epoch'] = pd.to_datetime(df['frame.time_epoch'], unit='s', errors='coerce')

#Handling multiple ips and addign empty to missing ips 
df['ip.src'] = df['ip.src'].str.split(',').str[0]
df['ip.dst'] = df['ip.dst'].str.split(',').str[0]
df['ip.src'] = df['ip.src'].astype('category').cat.add_categories('<empty>').fillna('<empty>')
df['ip.dst'] = df['ip.dst'].astype('category').cat.add_categories('<empty>').fillna('<empty>')

#Converting tcp.flag from hex to int
def is_hex(value):
    try:
        int(value, 16)
        return True
    except (ValueError, TypeError):
        return False

df['tcp.flags'] = df['tcp.flags'].apply(lambda x: int(x, 16) if pd.notna(x) and is_hex(x) else pd.NA).astype('Int64')

# Converting numeric columns to Int64
numeric_cols = [
    'frame.number', 'frame.len', 'ip.proto', 'tcp.srcport',
    'tcp.dstport', 'tcp.flags', 'tcp.window_size',
    'udp.srcport', 'udp.dstport', 'udp.length'
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').astype('Int64')

#Saving the changes ie overwriting them
df.to_csv(file_path, index=False)

