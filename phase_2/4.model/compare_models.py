# ------------------ Import Everything ------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, matthews_corrcoef, classification_report, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from imblearn.over_sampling import SMOTE

# ------------------ Load Flow-Level Dataset ------------------
df = pd.read_csv(r"C:\Users\Skeletron\Desktop\dataset\full_dataset.csv")

X = df.drop(columns=['flow_id', 'ip_src', 'ip_dst', 'is_malicious'])
y = df['is_malicious']

# ------------------ Split into Train/Test ------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

# ------------------ Apply SMOTE to Balance Data ------------------
sm = SMOTE(random_state=42)
X_train_bal, y_train_bal = sm.fit_resample(X_train, y_train)

print(f"Training set size after SMOTE: {X_train_bal.shape[0]} samples")

# ------------------ Models to Train ------------------
models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=10, class_weight='balanced', random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=20, class_weight='balanced', random_state=42, n_jobs=-1),
    "Extra Trees": ExtraTreesClassifier(n_estimators=100, max_depth=20, class_weight='balanced', random_state=42, n_jobs=-1),
}

# ------------------ Storage for Results ------------------
results = []

# ------------------ Train and Test Each Model ------------------
for model_name, model in models.items():
    print(f"\n🚀 Training {model_name}...")

    # Measure CPU time for training
    start_train = time.time()
    model.fit(X_train_bal, y_train_bal)
    end_train = time.time()

    # Measure CPU time for testing
    start_test = time.time()
    y_pred = model.predict(X_test)
    end_test = time.time()

    # Evaluation metrics
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    mcc = matthews_corrcoef(y_test, y_pred)

    train_time = end_train - start_train
    test_time = end_test - start_test

    # Store results
    results.append({
        "Model": model_name,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "MCC": mcc,
        "Train Time (s)": train_time,
        "Test Time (s)": test_time
    })

    # Optional: Plot Confusion Matrix
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=["Normal", "Botnet"])
    plt.title(f"Confusion Matrix: {model_name}")
    plt.tight_layout()
    plt.show()

    print(classification_report(y_test, y_pred, target_names=["Normal", "Botnet"]))

# ------------------ Show Summary Results ------------------
results_df = pd.DataFrame(results)

print("\n📊 Summary of All Models:\n")
print(results_df)

# Plotting Comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
sns.barplot(data=results_df, x='Model', y='Precision', ax=axes[0,0])
axes[0,0].set_title('Precision Comparison')

sns.barplot(data=results_df, x='Model', y='Recall', ax=axes[0,1])
axes[0,1].set_title('Recall Comparison')

sns.barplot(data=results_df, x='Model', y='F1-Score', ax=axes[1,0])
axes[1,0].set_title('F1-Score Comparison')

sns.barplot(data=results_df, x='Model', y='MCC', ax=axes[1,1])
axes[1,1].set_title('MCC Comparison')

plt.tight_layout()
plt.show()

# CPU time plot
plt.figure(figsize=(10,6))
sns.barplot(data=results_df, x='Model', y='Train Time (s)', palette='crest')
plt.title('Training Time Comparison')
plt.show()

plt.figure(figsize=(10,6))
sns.barplot(data=results_df, x='Model', y='Test Time (s)', palette='flare')
plt.title('Testing Time Comparison')
plt.show()
