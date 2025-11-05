# Project Context

name: HW
description: CLI + library 用於從 OpenSpec 規格產生代碼、驗證與 lint。主要用於內部模板與 CI 驗證。
repository: https://example.com/your/repo
owner: YourName <you@example.com>

tech_stack:
  - node: >=18
  - typescript: ^5.0
  - npm: ^9
  - testing: jest
  - ci: GitHub Actions
  - codegen: ts-node / esbuild (視實作)
  - linter: eslint + prettier

conventions:
  - git: main 分支為 stable，feature 分支以 feat/<short-desc> 命名
  - commits: 使用 Conventional Commits
  - semver: 採用 semver 發行
  - PR: 必須包含變更說明與測試或回歸測試
  - changelog: 由 release PR 自動更新

local_dev:
  - node 安裝後：npm ci
  - 建立本地全域指令（開發）：npm run link 或 npm link
  - 測試：npm test
  - lint: npm run lint
  - 產生/測試 CLI：npx ts-node ./src/cli.ts 或 npm run build && node dist/cli.js

environment:
  - 必要 env 範例：OPENAPI_KEY, NPM_TOKEN (for publishing)
  - 建議在 CI 中使用 secrets 管理

release_process:
  - feature -> PR -> review -> merge -> GitHub Actions 產生 draft release -> tag -> publish
  - 每次 major/minor/release 前需更新 openspec 變更提案（changes）

notes:
  - 若有特定檔案路徑或內部規範請補充
  - 我可以根據實際 repo 自動產生更精確內容，請提供 package.json 或現況檔案