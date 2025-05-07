# 文章校正ツール — フロントエンド + Python FastAPI バックエンド

日本語文章を 800 文字以内で校正し、**差分ハイライト**と **コピー機能** を備えた Web アプリです。フロントエンドは **React + TypeScript + Tailwind CSS**、バックエンドは **FastAPI** で構成しています。

---
## 準備

### configの設定
backend\src\config\config_template.yamlを参考にbackend\src\config\config.yamlを作成して下さい

### フロントエンドセットアップ
リポジトリ直下にて以下のコマンドを使用して仮想環境を作成し、入ります。
```bash
$ cd frontend
# 依存関係一括インストール
$ npm install
# 差分ハイライト用ライブラリ
$ npm install diff-match-patch  
# 開発サーバー起動
$ npm start                     # http://localhost:3000
```
### バックエンドセットアップ

```bash
cd ../backend
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt                   # fastapi, uvicorn 等
uvicorn main:app --reload                         # http://localhost:8000
```


##  実装の工夫ポイント

| # | 概要          | 技術・工夫点                                                                      |
| - | ----------- | --------------------------------------------------------------------------- |
| 1 | **差分ハイライト** | `diff-match-patch` で挿入文(緑)・削除文(赤取り消し線)をリアルタイム描画。ハイライト ON/OFF トグル付き。         |
| 2 | **UX 向上**   | - Copy ボタン & Toast- 文字数カウント (残 50 文字→amber、超過→red)- ローディング "校閲中です…" アニメーション |
| 3 | **校閲精度**   | 複数に分割してLLMに校閲をさせることで、校閲精度向上             |
| 4 | **プロンプト**    | CoTを用い、校閲精度向上     |

---
