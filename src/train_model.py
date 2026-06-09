import pandas as pd
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc

# 1. Cargar datos
df = pd.read_csv("data/archive (2)/WA_Fn-UseC_-Telco-Customer-Churn.csv", low_memory=False)

# 2. Preparar datos
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)

X = df.drop(['Churn', 'customerID'], axis=1)
y = df['Churn']

X_encoded = pd.get_dummies(X, drop_first=True)
bool_cols = X_encoded.select_dtypes(include='bool').columns
X_encoded[bool_cols] = X_encoded[bool_cols].astype(int)
y_encoded = y.map({'No': 0, 'Yes': 1})

# 3. Split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
)

# 4. Escalar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Entrenar
model = LogisticRegression(class_weight='balanced', random_state=42)
model.fit(X_train_scaled, y_train)

# 6. Datos curva ROC
y_proba = model.predict_proba(X_test_scaled)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = auc(fpr, tpr)

roc_data = {
    'fpr': fpr.tolist(),
    'tpr': tpr.tolist(),
    'thresholds': thresholds.tolist(),
    'auc': roc_auc
}

# 7. Guardar archivos
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('features.pkl', 'wb') as f:
    pickle.dump(list(X_encoded.columns), f)

with open('roc_data.json', 'w') as f:
    json.dump(roc_data, f)

print("✅ Archivos generados:")
print(f"   - model.pkl")
print(f"   - scaler.pkl")
print(f"   - features.pkl ({len(X_encoded.columns)} features)")
print(f"   - roc_data.json (AUC = {roc_auc:.3f})")