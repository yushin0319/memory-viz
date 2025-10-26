# Memory MCP Visualization Tool

Memory MCPのナレッジグラフ（エンティティとリレーション）をインタラクティブに可視化するWebアプリケーション。

## 技術スタック

### フロントエンド
- React + TypeScript + Vite
- Cytoscape.js (グラフ可視化)
- Material-UI (MUI)

### バックエンド
- FastAPI (Python)
- Memory MCP Client

## セットアップ

### バックエンド

```bash
cd backend

# Python仮想環境作成
python -m venv venv

# 仮想環境有効化（Windows）
venv\Scripts\activate

# パッケージインストール
pip install -r requirements.txt

# 環境変数設定
copy .env.example .env

# 開発サーバー起動
uvicorn main:app --reload
```

### テスト実行

```bash
# 全テスト実行
pytest

# カバレッジ付き
pytest --cov=.

# 特定のテストファイルのみ
pytest tests/test_memory.py
```

### コード品質チェック

```bash
# フォーマット
black .

# Lint
flake8 .

# 型チェック
mypy .
```

## API ドキュメント

開発サーバー起動後、以下のURLでAPIドキュメントを確認できます：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## プロジェクト構成

詳細は `memory-viz-plan.md` を参照してください。

## ライセンス

MIT
