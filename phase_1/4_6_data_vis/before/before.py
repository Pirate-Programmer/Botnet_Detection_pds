import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load `testing.csv`
file_path = r"C:\Users\Skeletron\Desktop\dataset\testing.csv"
df = pd.read_csv(file_path, low_memory=False)

# Plot missing values percentage
missing_percent = df.isnull().mean() * 100
plt.figure(figsize=(12, 6))
missing_percent.plot(kind='bar', color='skyblue')
plt.title('Percentage of Missing Values Before Handling - testing.csv')
plt.xlabel('Columns')
plt.ylabel('Percentage Missing (%)')
plt.xticks(rotation=45, ha="right")
plt.show()

# Protocol Distribution Check
plt.figure(figsize=(8, 6))
protocol_counts = df['ip.proto'].value_counts().rename({6: 'TCP', 17: 'UDP', 1: 'ICMP', 50: 'ESP', 103: 'PIM'})
protocol_counts.plot(kind='bar', color='lightblue')
plt.title('Protocol Distribution Before Handling - testing.csv')
plt.xlabel('Protocol')
plt.ylabel('Packet Count')
plt.xticks(rotation=0)
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
numeric_df = df.select_dtypes(include=['float64', 'int64'])
corr = numeric_df.corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Heatmap - 1.csv')
plt.tight_layout()
plt.show()

print("Before Handling Visualization Complete.")
