#!/usr/bin/env python3
"""
讀取 raw CSV（無 header），簡單清理與輸出 processed CSV（label,text）。
label 轉為 0/1（ham=0, spam=1）。
"""
import argparse
import os
import pandas as pd
import re

def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.lower()
    s = re.sub(r"http\S+", " ", s)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="raw csv path (no header expected)")
    p.add_argument("--output", required=True, help="processed csv output path")
    args = p.parse_args()

    df = pd.read_csv(args.input, header=None, names=["label", "text"], encoding="latin-1")
    df["text"] = df["text"].astype(str).map(clean_text)
    df["label"] = df["label"].str.strip().map({"ham":0, "spam":1})
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"processed saved to {args.output} (rows={len(df)})")

if __name__ == "__main__":
    main()