import os
import joblib
import pandas as pd
import yaml
from xgboost import XGBClassifier

params = yaml.safe_load(open("params.yaml"))["train"]

train = pd.read_csv("data/prepared/train.csv")
X = train.drop(columns="target")
y = train["target"]

model = XGBClassifier(
    n_estimators=params["n_estimators"],
    max_depth=params["max_depth"],
    learning_rate=params["learning_rate"],
    random_state=42,
)
model.fit(X, y)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.pkl")
print("Model saved to models/model.pkl")
