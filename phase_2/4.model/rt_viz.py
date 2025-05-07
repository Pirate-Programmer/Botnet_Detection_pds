# ------------------ Import Libraries ------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
from imblearn.over_sampling import SMOTE

# ------------------ Load Data ------------------
print("Loading dataset...")
df = pd.read_csv(r"C:\Users\Skeletron\Desktop\dataset\full_dataset.csv")

X = df.drop(columns=['flow_id', 'ip_src', 'ip_dst', 'is_malicious'])
y = df['is_malicious']

# ------------------ Split Data ------------------
print("Splitting train/test set...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

# ------------------ Apply SMOTE ------------------
print("Applying SMOTE balancing...")
sm = SMOTE(random_state=42)
X_train_bal, y_train_bal = sm.fit_resample(X_train, y_train)

print(f"Balanced Training Set Size: {X_train_bal.shape[0]} samples")

# ------------------ Sample Smaller Training Data ------------------
print("Sampling smaller training set for faster testing...")
sample_idx = np.random.choice(X_train_bal.index, size=200000, replace=False)
X_train_bal_sampled = X_train_bal.loc[sample_idx]
y_train_bal_sampled = y_train_bal.loc[sample_idx]

# ------------------ Initialize Lists ------------------
train_f1_scores = []
test_f1_scores = []
train_precision_scores = []
test_precision_scores = []
train_recall_scores = []
test_recall_scores = []
depths = range(1, 31, 2)

# ------------------ Train Models and Record Metrics ------------------
print("Training Random Forest models at varying depths...")
for d in depths:
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=d,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train_bal_sampled, y_train_bal_sampled)

    y_train_pred = rf.predict(X_train_bal_sampled)
    y_test_pred = rf.predict(X_test)

    train_f1 = f1_score(y_train_bal_sampled, y_train_pred)
    test_f1 = f1_score(y_test, y_test_pred)

    train_precision = precision_score(y_train_bal_sampled, y_train_pred)
    test_precision = precision_score(y_test, y_test_pred)

    train_recall = recall_score(y_train_bal_sampled, y_train_pred)
    test_recall = recall_score(y_test, y_test_pred)

    train_f1_scores.append(train_f1)
    test_f1_scores.append(test_f1)
    train_precision_scores.append(train_precision)
    test_precision_scores.append(test_precision)
    train_recall_scores.append(train_recall)
    test_recall_scores.append(test_recall)

    print(f"Depth {d}: Train F1 = {train_f1:.4f}, Test F1 = {test_f1:.4f}")

# ------------------ Plotting ------------------

print("Plotting F1-Score graph...")
plt.figure(figsize=(10,6))
plt.plot(depths, train_f1_scores, marker='o', label='Training F1-Score')
plt.plot(depths, test_f1_scores, marker='s', label='Testing F1-Score')
plt.xlabel('Max Depth of Trees')
plt.ylabel('F1-Score')
plt.title('Overfitting vs Underfitting Behavior (F1-Score)')
plt.legend()
plt.grid(True)
plt.xticks(depths)
plt.ylim(0.0, 1.05)
plt.tight_layout()
plt.show()

print("Plotting Precision/Recall graphs...")
plt.figure(figsize=(12,6))
plt.plot(depths, train_precision_scores, marker='o', label='Training Precision', linestyle='--')
plt.plot(depths, test_precision_scores, marker='s', label='Testing Precision')
plt.plot(depths, train_recall_scores, marker='o', label='Training Recall', linestyle='--')
plt.plot(depths, test_recall_scores, marker='s', label='Testing Recall')
plt.xlabel('Max Depth of Trees')
plt.ylabel('Score')
plt.title('Precision and Recall vs Max Depth')
plt.legend()
plt.grid(True)
plt.xticks(depths)
plt.ylim(0.0, 1.05)
plt.tight_layout()
plt.show()

print("Completed plotting.")
