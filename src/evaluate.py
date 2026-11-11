import json
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

test = pd.read_csv("data/prepared/test.csv")
X = test.drop(columns="target")
y = test["target"]

model = joblib.load("models/model.pkl")
pred = model.predict(X)

metrics = {
    "accuracy": round(accuracy_score(y, pred), 4),
    "f1_score": round(f1_score(y, pred, average="weighted"), 4),
}
json.dump(metrics, open("metrics.json", "w"), indent=2)
print(metrics)
