import os
import pandas as pd
import yaml
from sklearn.model_selection import train_test_split

params = yaml.safe_load(open("params.yaml"))["prepare"]

df = pd.read_csv("data/iris.csv")
train, test = train_test_split(
    df, test_size=params["test_size"], random_state=params["seed"], stratify=df["target"]
)

os.makedirs("data/prepared", exist_ok=True)
train.to_csv("data/prepared/train.csv", index=False)
test.to_csv("data/prepared/test.csv", index=False)
print("Train:", train.shape, "Test:", test.shape)
