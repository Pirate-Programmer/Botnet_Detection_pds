# ------------------ Import Libraries ------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    roc_curve, auc
)
from imblearn.over_sampling import SMOTE

# ------------------ Load Dataset ------------------
print("Loading dataset...")
df = pd.read_csv(r"C:\Users\Skeletron\Desktop\dataset\full_dataset.csv")

X = df.drop(columns=['flow_id', 'ip_src', 'ip_dst', 'is_malicious'])
y = df['is_malicious']

# ------------------ Train/Test Split ------------------
print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

# ------------------ Apply SMOTE ------------------
print("Applying SMOTE to training data...")
sm = SMOTE(random_state=42)
X_train_bal, y_train_bal = sm.fit_resample(X_train, y_train)

print(f"Training samples after SMOTE: {X_train_bal.shape[0]}")

# ------------------ Train Random Forest ------------------
print("Training Random Forest model...")
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train_bal, y_train_bal)

# ------------------ Prediction ------------------
y_test_pred = rf.predict(X_test)
y_test_proba = rf.predict_proba(X_test)[:, 1]  # For ROC

# ------------------ Classification Report ------------------
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred, target_names=['Normal', 'Botnet']))

# ------------------ ROC Curve and AUC ------------------
fpr, tpr, thresholds = roc_curve(y_test, y_test_proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'Random Forest (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='Random Guess')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Botnet Detection (Random Forest)')
plt.legend(loc="lower right")
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------ Feature Importances ------------------
print("\nCalculating Feature Importances...")
importances = rf.feature_importances_
feature_names = X.columns

feat_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("\nTop 15 Important Features:")
print(feat_df.head(15))

# ------------------ Feature Importance Plot ------------------
plt.figure(figsize=(10, 6))
sns.barplot(data=feat_df.head(15), x='Importance', y='Feature', palette='viridis')
plt.title('Top 15 Feature Importances - Random Forest')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.grid(True)
plt.tight_layout()
plt.show()
