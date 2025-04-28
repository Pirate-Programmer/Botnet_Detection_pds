import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

# Path to your testing CSV file
# %%
testing_csv_path = r"C:\Users\Skeletron\Desktop\dataset\testing.csv"

# %%
# Initialize LabelEncoders
src_encoder = LabelEncoder()
dst_encoder = LabelEncoder()

# Read the testing CSV
df = pd.read_csv(testing_csv_path, low_memory=False)

# Fit encoders only on IPs from this single file
src_encoder.fit(df['ip.src'].fillna('<empty>').unique())
dst_encoder.fit(df['ip.dst'].fillna('<empty>').unique())

# Save the encoders
joblib.dump(src_encoder, 'ip_src_encoder.pkl')
joblib.dump(dst_encoder, 'ip_dst_encoder.pkl')

# Apply encoding
df['ip.src'] = src_encoder.transform(df['ip.src'].fillna('<empty>'))
df['ip.dst'] = dst_encoder.transform(df['ip.dst'].fillna('<empty>'))

# Save back to the same file
df.to_csv(testing_csv_path, index=False)

print("Testing CSV encoded successfully. Encoders saved to:")
print(f"- ip_src_encoder.pkl\n- ip_dst_encoder.pkl")