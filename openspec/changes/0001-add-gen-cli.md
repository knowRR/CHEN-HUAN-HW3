# 0001 — Add `gen` CLI subcommand to scaffold modules from spec

status: proposed
author: GitHub Copilot
date: 2025-11-05

summary:
  新增 CLI 子命令 `hw gen`（或 `openspec gen`），從 OpenSpec 規格檔產生專案 scaffold 或模組樣板，支援 template 選項與少量互動式參數。

motivation:
  - 簡化新模組的建立流程，統一樣板與設定
  - 減少手動錯誤並使 CI / 团队採用同一風格

spec:
  - CLI: `hw gen <spec-file> --template <name> --out <dir> [--force]`
  - templates: built-in (ts-lib, cli, express-plugin)，並允許自訂 template path
  - validation: 先對 spec 做 schema 驗證，失敗時中止並回傳可導向的錯誤
  - output: 在目標資料夾產生 README、src、tests、package.json（可選）與 basic CI config
  - flags:
    - `--interactive`：提示填入 name, author, license
    - `--dry-run`：顯示將建立的檔案清單但不寫檔

migration:
  - 無向後相容破壞
  - 若與現有 CLI 衝突，新增子命令名稱可調整

compatibility:
  - Node >=18
  - 不改變現有命令

implementation_plan:
  1. 新增 CLI handler 與子命令註冊（src/cli/gen.ts）
  2. 建立 templates 資料夾（templates/ts-lib, templates/cli）
  3. 實作 spec 驗證模組（src/validateSpec.ts）
  4. 加入單元測試與端對端測試（jest）
  5. 文件與 changelog 更新

tests:
  - 單元：驗證 template 參數解析、spec 驗證錯誤處理
  - e2e：對 sample spec 執行 gen，檢查產出檔案存在與基本內容

rollout:
  - merge 到 feature branch -> CI run -> code review -> merge到 main -> patch release
  - 在 release note 中加入使用說明與範例

risks:
  - template 維護成本：需設計簡單的更新機制
  - 若自動產生 package.json 並安裝相依性，會影響安全性與網路使用

alternatives:
  - 只提供 library API，由其他專案自行綁定 CLI
  - 使用外部 Yeoman 類工具而非內建 template

open_questions:
  - 要不要支援自動 npm install？
  - 是否需支援多種語言（JS/TS）或只 TS？
