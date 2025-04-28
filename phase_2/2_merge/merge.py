import os
import pandas as pd

base_path = r"C:\Users\Skeletron\Desktop\dataset"
all_files = [os.path.join(base_path, f"{i}.csv") for i in range(1, 18)]

# Read and combine
merged_df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)

# Save combined dataset
merged_df.to_csv(os.path.join(base_path, "full_dataset.csv"), index=False)
print(" Merged all 17 CSVs into full_dataset.csv")
