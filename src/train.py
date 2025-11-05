#!/usr/bin/env python3
"""
訓練腳本：使用 TF-IDF + SVM(linear) 與 LogisticRegression 做 baseline。
輸出 model 與 vectorizer、簡易 metrics JSON。
"""
import argparse
import json
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.svm import LinearSVC

def fit_and_save(X_train, y_train, X_val, y_val, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    results = {}

    # TF-IDF
    vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=2)
    X_train_t = vectorizer.fit_transform(X_train)
    X_val_t = vectorizer.transform(X_val)
    joblib.dump(vectorizer, Path(out_dir)/"vectorizer.joblib")

    # SVM (LinearSVC) baseline with simple C grid
    print("Training LinearSVC...")
    svc = LinearSVC()
    params = {"C": [0.01, 0.1, 1.0, 10.0]}
    gs = GridSearchCV(svc, params, cv=5, n_jobs=1)
    gs.fit(X_train_t, y_train)
    best_svc = gs.best_estimator_
    y_pred = best_svc.predict(X_val_t)
    results["svc"] = {
        "best_params": gs.best_params_,
        "accuracy": float(accuracy_score(y_val, y_pred)),
        "report": classification_report(y_val, y_pred, output_dict=True),
    }
    joblib.dump(best_svc, Path(out_dir)/"model_svm.joblib")
    print("SVM done.")

    # Logistic Regression (L2)
    print("Training LogisticRegression...")
    lr = LogisticRegression(max_iter=1000, solver="liblinear")
    params_lr = {"C":[0.01, 0.1, 1.0, 10.0]}
    gs2 = GridSearchCV(lr, params_lr, cv=5, n_jobs=1)
    gs2.fit(X_train_t, y_train)
    best_lr = gs2.best_estimator_
    y_pred_lr = best_lr.predict(X_val_t)
    results["logreg"] = {
        "best_params": gs2.best_params_,
        "accuracy": float(accuracy_score(y_val, y_pred_lr)),
        "report": classification_report(y_val, y_pred_lr, output_dict=True),
    }
    joblib.dump(best_lr, Path(out_dir)/"model_logreg.joblib")
    print("LogReg done.")

    # save metrics
    with open(Path(out_dir)/"metrics.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Artifacts saved to", out_dir)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="processed csv with label,text")
    p.add_argument("--out", required=True, help="experiment output dir")
    p.add_argument("--test-size", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    df = pd.read_csv(args.input)
    X = df["text"].fillna("").astype(str).to_list()
    y = df["label"].astype(int).to_list()

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=args.test_size, random_state=args.seed, stratify=y)
    fit_and_save(X_train, y_train, X_val, y_val, args.out)

if __name__ == "__main__":
    main()