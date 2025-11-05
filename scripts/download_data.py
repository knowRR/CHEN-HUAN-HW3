#!/usr/bin/env python3
"""
簡單下載器：下載公開 SMS spam dataset 並儲存到 data/raw/
注意：僅用於研究/防護目的，請勿用於惡意濫發垃圾訊息。
"""
import argparse
import hashlib
import os
import urllib.request

DEFAULT_URL = "https://raw.githubusercontent.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/refs/heads/master/Chapter03/datasets/sms%20spam%20no%20header.csv"
OUT_DIR = "data/raw"
OUT_NAME = "sms_spam_no_header.csv"

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def download(url, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    print(f"下載 {url} -> {out_path}")
    urllib.request.urlretrieve(url, out_path)
    print("下載完成")
    print("SHA256:", sha256_of_file(out_path))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", default=DEFAULT_URL)
    p.add_argument("--out", default=os.path.join(OUT_DIR, OUT_NAME))
    args = p.parse_args()
    download(args.url, args.out)

if __name__ == "__main__":
    main()