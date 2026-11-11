# Run once: saves the Iris dataset as data/iris.csv (this file is tracked by DVC)
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame
df.to_csv("data/iris.csv", index=False, lineterminator="\n")
print("Saved data/iris.csv", df.shape)
