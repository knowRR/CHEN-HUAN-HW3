#!/usr/bin/env python3
"""
簡單評估：載入 model 與 vectorizer，對輸入資料做報表輸出（classification_report）。
"""
import argparse
import json
import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--vectorizer", required=True)
    p.add_argument("--input", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    model = joblib.load(args.model)
    vec = joblib.load(args.vectorizer)
    df = pd.read_csv(args.input)
    X = df["text"].fillna("").astype(str).to_list()
    y = df["label"].astype(int).to_list()

    X_t = vec.transform(X)
    y_pred = model.predict(X_t)
    report = classification_report(y, y_pred, output_dict=True)
    acc = accuracy_score(y, y_pred)

    os.makedirs(args.out, exist_ok=True)
    with open(Path(args.out)/"eval_report.json", "w", encoding="utf-8") as f:
        json.dump({"accuracy": acc, "report": report}, f, indent=2, ensure_ascii=False)
    print("Evaluation saved to", args.out)

if __name__ == "__main__":
    main()