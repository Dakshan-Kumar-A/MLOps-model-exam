# MLOps-model-exam

Reproducible ML experiment on the Iris dataset using **Git, DVC and CML**.
Model: XGBoost (the notebook also compares it with Logistic Regression).

## Project structure

```
MLOps-model-exam/
|-- .github/workflows/cml.yaml   # GitHub Actions + CML workflow
|-- data/                        # iris.csv is created here
|-- src/
|   |-- get_data.py              # saves Iris as data/iris.csv (run once)
|   |-- prepare.py               # train/test split
|   |-- train.py                 # trains XGBoost
|   |-- evaluate.py              # writes metrics.json
|-- notebook.ipynb               # part (a): models, accuracy and F1
|-- params.yaml                  # all parameters
|-- dvc.yaml                     # pipeline
|-- requirements.txt
```

## 1. Setup (Windows)

Unzip the project, open Command Prompt or PowerShell in the folder, then:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install jupyter
```

> Python 3.14 is very new. If `pip install` fails for `xgboost` or `dvc`,
> recreate the environment with Python 3.12:
> `rmdir /s /q venv` then `py -3.12 -m venv venv`, and repeat the steps above.

## 2. Run the notebook (part a)

```
jupyter notebook notebook.ipynb
```
Run all cells and note the accuracy and F1-score of both models.

## 3. Run the scripts manually (part b)

```
python src/get_data.py
python src/prepare.py
python src/train.py
python src/evaluate.py
```
`metrics.json` is created with the accuracy and F1-score.

## 4. Connect Git and DVC (part c)

```
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Dakshan-Kumar-A/MLOps-model-exam.git
git push -u origin main

dvc init
git commit -m "Initialize DVC"

dvc add data/iris.csv
git add data/iris.csv.dvc data/.gitignore
git commit -m "Track Iris dataset with DVC"

dvc remote add -d localstorage ../dvc-storage
git add .dvc/config
git commit -m "Configure local DVC remote"
dvc push
git push
```

If `git commit` asks who you are, run once:
```
git config user.name "Your Name"
git config user.email "you@example.com"
```

## 5. Run the pipeline and compare experiments (part d)

Delete the manually created outputs first so DVC can manage them:
```
rmdir /s /q data\prepared models
del metrics.json
```

Then:
```
dvc repro
dvc dag
git add dvc.yaml dvc.lock params.yaml metrics.json data/.gitignore models/.gitignore
git commit -m "Baseline experiment"
```

Change a parameter in `params.yaml` (for example `n_estimators: 10`, `max_depth: 1`), then:
```
dvc repro
dvc params diff
dvc metrics diff
git add params.yaml dvc.lock metrics.json
git commit -m "Experiment: weaker XGBoost"
git push
```
If the metrics do not change, try an even weaker setting such as `n_estimators: 2`.

## 6. CML pull request report (part e)

1. On GitHub: Settings > Actions > General > Workflow permissions >
   choose **Read and write permissions** > Save.
2. Create a branch, change a parameter, and push:
```
git checkout -b experiment-1
# edit params.yaml, e.g. n_estimators: 100, max_depth: 4
dvc repro
git add .
git commit -m "Try bigger XGBoost model"
git push -u origin experiment-1
```
3. On GitHub, open a pull request from `experiment-1` into `main`.
4. The workflow runs automatically (Actions tab) and CML posts the
   metrics and params report as a comment on the pull request.

## Notes

- The DVC remote is a local folder (`../dvc-storage`), so GitHub's runner
  cannot reach it. The workflow recreates `data/iris.csv` with
  `src/get_data.py` instead of running `dvc pull`.
- Screenshots to include in the report are listed in `MLOps_Q1_Answers.docx`.
