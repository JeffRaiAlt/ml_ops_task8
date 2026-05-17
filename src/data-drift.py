import pandas as pd
import numpy as np

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from evidently import Report
from evidently.presets import DataDriftPreset


# 1. Данные
data = load_breast_cancer(as_frame=True)

X = data.data
y = data.target


# 2. train / reference / current
X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=42,
    stratify=y
)

X_reference, X_current, y_reference, y_current = train_test_split(
    X_temp,
    y_temp,
    test_size=0.5,
    random_state=42,
    stratify=y_temp
)


# 3. Модель
model = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000))
    ]
)

model.fit(X_train, y_train)


# 4. Функция оценки
def evaluate_model(batch_name, X_batch, y_batch):
    y_pred = model.predict(X_batch)
    y_proba = model.predict_proba(X_batch)[:, 1]

    return {
        "batch": batch_name,
        "accuracy": accuracy_score(y_batch, y_pred),
        "precision": precision_score(y_batch, y_pred, zero_division=0),
        "recall": recall_score(y_batch, y_pred, zero_division=0),
        "f1": f1_score(y_batch, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_batch, y_proba),
    }


# 5. Current batch с искусственным drift
X_current_drift = X_current.copy() * 1000


# 6. Сравнение качества модели
metrics = pd.DataFrame([
    evaluate_model("reference_normal", X_reference, y_reference),
    evaluate_model("current_normal", X_current, y_current),
    evaluate_model("current_with_drift_x1000", X_current_drift, y_current),
])

print(metrics)


# 7. Evidently: отчет без drift
report_no_drift = Report([
    DataDriftPreset()
])

eval_no_drift = report_no_drift.run(
    current_data=X_current,
    reference_data=X_reference
)

eval_no_drift.save_html("breast_cancer_no_drift_report.html")


# 8. Evidently: отчет с drift
report_with_drift = Report([
    DataDriftPreset()
])

eval_with_drift = report_with_drift.run(
    current_data=X_current_drift,
    reference_data=X_reference
)

eval_with_drift.save_html("breast_cancer_data_drift_x1000_report.html")
