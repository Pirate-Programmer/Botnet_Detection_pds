import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

# Set professional style
sns.set(style="whitegrid", font_scale=1.1)
plt.rcParams['figure.facecolor'] = 'white'
colors = {"Normal": "#4C72B0", "Botnet": "#DD8452"}

# Load data with proper type conversion
df = pd.read_csv(r"C:\Users\Skeletron\Desktop\dataset\testing.csv")

# Convert critical columns to numeric
numeric_cols = ['flow_duration', 'total_bytes', 'packet_count', 'tcp_flag_count', 'avg_packet_size']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Convert labels
df['is_malicious'] = df['is_malicious'].map({0: "Normal", 1: "Botnet"})

# ====================== 1. ENHANCED VIOLIN PLOT ======================
plt.figure(figsize=(12, 7))

# Create filtered copy properly
filtered_df = df[df['flow_duration'] <= df['flow_duration'].quantile(0.99)].copy()

sns.violinplot(
    x='is_malicious',
    y='flow_duration',
    data=filtered_df,
    palette=colors,
    linewidth=2,
    inner="quartile",
    cut=0,
    saturation=0.8
)

# Add swarm plot
sns.swarmplot(
    x='is_malicious',
    y='flow_duration',
    data=filtered_df.sample(min(200, len(filtered_df))),
    color="black",
    alpha=0.3,
    size=3
)

plt.title("Flow Duration Distribution: Normal vs Botnet Traffic", pad=20, fontweight='bold')
plt.xlabel("Traffic Classification", labelpad=10)
plt.ylabel("Duration (seconds)", labelpad=10)

# Add median annotations
medians = filtered_df.groupby('is_malicious')['flow_duration'].median()
for i, traffic_type in enumerate(["Normal", "Botnet"]):
    plt.text(i, medians[traffic_type] * 1.1, 
             f"Median: {medians[traffic_type]:.2f}s",
             ha='center', va='bottom', 
             fontweight='bold',
             bbox=dict(facecolor='white', alpha=0.8, pad=3))

plt.tight_layout()
plt.show()


# ====================== 2. Fixed Traffic Timeline ======================
plt.figure(figsize=(12, 5))

# First ensure flow_duration_min exists
df['flow_duration_min'] = df['flow_duration'] / 60  # Convert seconds to minutes

# Create numeric bins (fixes TypeError)
bin_edges = np.linspace(0, df['flow_duration_min'].quantile(0.95), 20)
df['time_bin'] = pd.cut(df['flow_duration_min'], bins=bin_edges, labels=[f"{x:.2f}" for x in bin_edges[:-1]])

# Convert to string for plotting (ensures compatibility)
df['time_bin_str'] = df['time_bin'].astype(str)

palette = {"Normal": "#4C72B0",  # Blue for Normal (0)
           "Botnet": "#DD8452"}   # Orange for Botnet (1)

sns.lineplot(
    data=df,
    x='time_bin_str',
    y='total_bytes',
    hue='is_malicious',
    hue_order=["Normal", "Botnet"],       # Force 0 (Normal) to appear first
    palette=palette,        # Explicit color mapping
    estimator='median',
    errorbar=('ci', 95),
    linewidth=2.5
)

# Update legend labels to match
plt.legend(
    title="Traffic Class",
    labels=["Normal", "Botnet"],  # Must match hue_order
    loc="upper right"
)


plt.title("Bandwidth Usage Over Flow Duration", pad=20)
plt.xlabel("Flow Duration (minutes)")
plt.ylabel("Total Bytes Transferred")
plt.xticks(rotation=45)
plt.legend(title="Traffic Class", labels=["Normal", "Botnet"])
plt.grid(True, alpha=0.3)

# Format y-axis
byte_fmt = EngFormatter(unit='B')
plt.gca().yaxis.set_major_formatter(byte_fmt)

plt.tight_layout()
plt.show()

# ====================== 3. PORT ACTIVITY HEATMAP ======================
plt.figure(figsize=(12, 6))

top_ports = df['dst_port'].value_counts().nlargest(15).index
port_df = df[df['dst_port'].isin(top_ports)].copy()  # Explicit copy

cross_tab = pd.crosstab(port_df['dst_port'], port_df['is_malicious'])
sns.heatmap(
    cross_tab.apply(lambda x: x/x.sum(), axis=1),
    cmap="YlOrRd",
    annot=True,
    fmt=".1%",
    linewidths=0.5,
    cbar_kws={'label': 'Percentage'}
)

plt.title("Malicious Traffic Percentage by Destination Port (Top 15)", pad=20, fontweight='bold')
plt.xlabel("Traffic Class")
plt.ylabel("Destination Port")
plt.xticks([0.5, 1.5], ["Normal", "Botnet"])
plt.tight_layout()
plt.show()

# ====================== 4. PACKET SIZE DISTRIBUTION ======================
plt.figure(figsize=(12, 6))

sns.kdeplot(
    data=df,
    x='avg_packet_size',
    hue='is_malicious',
    palette=colors,
    fill=True,
    common_norm=False,
    alpha=0.5,
    linewidth=2
)

plt.title("Packet Size Distribution by Traffic Class", pad=20, fontweight='bold')
plt.xlabel("Average Packet Size (bytes)")
plt.ylabel("Density")
plt.xlim(0, df['avg_packet_size'].quantile(0.99))
plt.legend(title="Traffic Class")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()