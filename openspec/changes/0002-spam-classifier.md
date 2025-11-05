# 0002 — 建立 Spam（SMS/Email）分類基線模型

status: proposed
author: GitHub Copilot
date: 2025-11-05

summary:
  建立一個可重現的 spam 分類基線實作，第一階段 (phase1-baseline) 使用傳統機器學習（SVM 為主；可比較 logistic regression）在公開 SMS dataset 上訓練與評估。後續階段保留骨架但暫不填內容。

motivation:
  - 快速取得可比較的基線模型與評估指標，為後續改進（特徵工程、深度學習、部署）提供參考。
  - 提供可在 CI 上執行的端到端流程（資料下載、前處理、訓練、評估、報表）。

data:
  - primary: https://raw.githubusercontent.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/refs/heads/master/Chapter03/datasets/sms%20spam%20no%20header.csv
  - note: 資料為 SMS 短訊標記之 spam/ham；若要針對 email，需要額外取得 email corpus（本提案先以 SMS 為實作樣本）。

spec:
  - phase1-baseline:
    - data ingestion: 下載並儲存原始 CSV（記錄 checksum）
    - preprocessing:
      - 清洗（小寫化、去除非文字符號）、tokenize、移除 stopwords、可選 lemmatize/stem
      - 特徵：CountVectorizer 與 TF-IDF（ngram=(1,2)）
      - 可選類別 encode（label -> 0/1）
    - model:
      - baseline: Support Vector Machine (SVC with linear kernel) + 標準化/降維選項
      - compare: LogisticRegression (L2) 作為對照
      - cross-validation: 5-fold CV
      - hyperparam search: GridSearchCV（C 值等）
    - evaluation:
      - metrics: precision, recall, F1, accuracy, ROC AUC, confusion matrix
      - output: 儲存 model artifact、metrics JSON、classification report、ROC 圖表
    - reproducibility:
      - 固定 random_seed，requirements.txt / environment.yml，執行腳本支持 --seed、--output-dir、--dry-run
  - phase2:
    - (空)
  - phase3:
    - (空)
  - phaseN:
    - (空)

implementation_plan:
  1. 新增資料與實驗目錄：data/raw, experiments/0001_baseline
  2. 撰寫資料下載與預處理腳本：scripts/download_data.py, src/preprocess.py
  3. 實作訓練與評估腳本：src/train.py（支援 SVM 與 LogisticRegression）、src/evaluate.py
  4. 加入 CI job（GitHub Actions）在小樣本上執行 smoke tests（確保 pipeline 可跑）
  5. 撰寫 unit tests（pytest）與小型 e2e 測試
  6. 撰寫使用說明與結果報表範例

tests:
  - unit: preprocessing 功能、label mapping、特徵向量尺寸
  - integration: 從下載到訓練跑一個小樣本，驗證輸出報表存在
  - regression: 模型訓練輸出變化檢查（可選）

artifacts:
  - scripts/download_data.py
  - src/preprocess.py
  - src/train.py
  - src/evaluate.py
  - requirements.txt / environment.yml
  - experiments/0001_baseline/{model.pkl,metrics.json,report.html}

risks & ethics:
  - 資料來源為公開 dataset；使用前請確認授權條款。
  - 明確禁止將本專案用作發送垃圾郵件或協助傳播惡意垃圾活動。模型僅應用於偵測/防範、研究或合規用途。

open_questions:
  - 模型焦點是 SMS 還是 email？若為 email，請提供或允許取得對應 dataset。
  - 偏好使用 scikit-learn（CPU 傳統 ML）還是同時建立 PyTorch/TensorFlow 版本？
  - 是否需要自動封存 artifacts 到專案內部的 artifact store 或僅留在 experiments 目錄？

notes:
  - 若同意此 proposal，我可在 repo 中 scaffold 所列檔案與 CI job。請回覆「apply 0002」或指示要先實作哪個 script（download / preprocess / train）。