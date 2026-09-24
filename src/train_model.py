import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


np.random.seed(42)

n = 1000

df = pd.DataFrame({
    "temperature": np.random.normal(70, 10, n),
    "vibration": np.random.normal(5, 1.5, n),
    "pressure": np.random.normal(100, 8, n),
    "voltage": np.random.normal(3.3, 0.2, n),
    "operating_hours": np.random.randint(100, 10000, n)
})

failure_score = (
    (df["temperature"] > 85).astype(int)
    + (df["vibration"] > 7).astype(int)
    + (df["pressure"] < 90).astype(int)
    + (df["voltage"] < 3.0).astype(int)
    + (df["operating_hours"] > 8000).astype(int)
)

df["failure"] = (failure_score >= 2).astype(int)

features = [
    "temperature",
    "vibration",
    "pressure",
    "voltage",
    "operating_hours"
]

X = df[features]
y = df["failure"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/failure_prediction_model.pkl"
)

print("Model trained and saved successfully.")