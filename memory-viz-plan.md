# Memory MCP Visualization Tool - 実装計画

## 📋 プロジェクト概要

Memory MCPのナレッジグラフ（エンティティとリレーション）をインタラクティブに可視化するWebアプリケーション。

### 主な機能
- ナレッジグラフの視覚的表示（ノードとエッジ）
- エンティティの詳細情報表示（observations）
- インタラクティブな操作（ノードクリック、ズーム、パン）
- レイアウトアルゴリズム切り替え
- エンティティタイプによるフィルタリング
- リアルタイムまたは手動更新

---

## 🛠️ 技術スタック

### フロントエンド

**React + TypeScript + Vite**
- **React**: 湧心くんの得意分野、コンポーネント志向の開発
- **TypeScript**: kakuhoでも使用、型安全性で開発効率向上
- **Vite**: 高速な開発サーバー、モダンなビルドツール、Reactとの相性◎

**Cytoscape.js + react-cytoscape**
- **選定理由**:
  - グラフ可視化に特化したライブラリ
  - 豊富なレイアウトアルゴリズム（force-directed, hierarchical, circular等）
  - ノード/エッジのスタイリングが柔軟
  - パフォーマンス良好（大規模グラフにも対応）
  - ナレッジグラフ可視化の実績多数
- **代替案との比較**:
  - D3.js: 柔軟性は高いが学習コスト大、オーバースペック
  - React Flow: React向けだが制約多い、フローチャート向き
  - vis.js: 簡単だが古い、メンテナンス活発でない

**Material-UI (MUI)**
- kakuhoでも使用している
- UI構築を高速化
- 統一感のあるデザイン

### バックエンド

**FastAPI (Python)**
- **選定理由**:
  - 湧心くんの好きな技術、kakuhoでも使用
  - 高速で軽量なREST API構築
  - 自動ドキュメント生成（OpenAPI/Swagger）
  - 非同期処理対応
  - Memory MCPとの連携がPythonで実装しやすい
- **代替案との比較**:
  - フロントエンドのみ: Memory MCPへの直接アクセスが難しい
  - Node.js (Express): 可能だがPythonの方が湧心くんに親和性高い

**Memory MCP Client**
- Claude Code CLIを経由してMemory MCPにアクセス
- または、MCPプロトコルで直接通信（要調査）

### その他

**開発ツール**:
- ESLint + Prettier: コード品質維持
- Git: バージョン管理
- Docker (将来的): 環境構築の簡易化

---

## 📁 プロジェクト構成

```
memory-viz/
├── frontend/                    # React フロントエンド
│   ├── src/
│   │   ├── components/
│   │   │   ├── GraphView.tsx   # メイングラフ表示コンポーネント
│   │   │   ├── Sidebar.tsx     # エンティティ詳細サイドバー
│   │   │   ├── Toolbar.tsx     # 操作ツールバー
│   │   │   ├── FilterPanel.tsx # フィルター機能
│   │   │   └── Layout/         # レイアウトコンポーネント
│   │   ├── hooks/
│   │   │   ├── useMemoryGraph.ts    # Memory MCP データ取得
│   │   │   └── useCytoscapeGraph.ts # グラフ操作ロジック
│   │   ├── types/
│   │   │   ├── memory.ts       # Memory MCP型定義
│   │   │   └── graph.ts        # グラフ関連型定義
│   │   ├── services/
│   │   │   └── api.ts          # APIクライアント
│   │   ├── utils/
│   │   │   └── graphTransform.ts # データ変換ユーティリティ
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── .eslintrc.js
│
├── backend/                     # FastAPI バックエンド
│   ├── main.py                  # FastAPI アプリケーション
│   ├── routers/
│   │   └── memory.py            # Memory MCP エンドポイント
│   ├── services/
│   │   └── memory_client.py     # Memory MCP クライアント
│   ├── models/
│   │   └── memory.py            # Pydantic モデル
│   ├── requirements.txt
│   └── .env.example
│
├── docs/
│   └── architecture.md          # アーキテクチャ設計書
├── README.md
└── .gitignore
```

---

## 🎨 アーキテクチャ設計

### データフロー

```
Memory MCP Server (MCP Protocol)
        ↓
    [read_graph]
        ↓
FastAPI Backend (Python)
    - Memory MCPクライアント
    - REST API提供 (/api/graph)
        ↓
    [HTTP/JSON]
        ↓
React Frontend (TypeScript)
    - データ取得 (useMemoryGraph)
    - Cytoscape.jsで可視化
    - ユーザーインタラクション
```

### API設計

**GET /api/graph**
- Memory MCPから全グラフデータ取得
- レスポンス:
```json
{
  "entities": [
    {
      "name": "湧心くん",
      "entityType": "user",
      "observations": ["...", "..."]
    }
  ],
  "relations": [
    {
      "from": "湧心くん",
      "to": "Windows環境",
      "relationType": "uses"
    }
  ]
}
```

**GET /api/graph/refresh**
- Memory MCPから最新データ取得（強制リフレッシュ）

**GET /api/entities/{entity_name}**
- 特定エンティティの詳細取得

### フロントエンド画面設計

```
┌─────────────────────────────────────────────┐
│ ツールバー                                   │
│ [Refresh] [Layout: Force] [Filter: All]    │
├───────────────────────────┬─────────────────┤
│                           │                 │
│   グラフ表示エリア        │   サイドバー    │
│   (Cytoscape.js)          │                 │
│                           │   選択中の      │
│   ┌────┐    ┌────┐       │   エンティティ  │
│   │User├────┤Env │       │                 │
│   └────┘    └────┘       │   名前:         │
│                           │   タイプ:       │
│        ┌────┐             │                 │
│        │MCP │             │   Observations: │
│        └────┘             │   - ...         │
│                           │   - ...         │
└───────────────────────────┴─────────────────┘
```

---

## 🚀 実装フェーズ

### Phase 1: 環境構築とバックエンド基礎 (1-2日)
- [ ] プロジェクトディレクトリ作成
- [ ] バックエンドセットアップ（FastAPI + 仮想環境）
- [ ] Memory MCP クライアント実装
- [ ] `/api/graph` エンドポイント作成
- [ ] 動作確認（Swagger UI で確認）

**技術選定理由の再確認**:
- FastAPI: 自動ドキュメント生成でデバッグしやすい
- Python: Memory MCP連携がシンプル

### Phase 2: フロントエンド基礎 (1-2日)
- [ ] React + Vite + TypeScript プロジェクト作成
- [ ] 基本的なレイアウト構築（MUI）
- [ ] API クライアント実装
- [ ] `useMemoryGraph` カスタムフック作成
- [ ] 取得データをコンソール表示で確認

**技術選定理由の再確認**:
- Vite: 開発サーバー起動が高速、HMR快適
- TypeScript: APIレスポンスの型安全性

### Phase 3: グラフ可視化基礎 (2-3日)
- [ ] Cytoscape.js インストール
- [ ] 基本的なグラフ描画実装
- [ ] Memory MCPデータ → Cytoscape形式への変換
- [ ] レイアウトアルゴリズム適用（force-directed）
- [ ] ノード/エッジの基本スタイリング

**技術選定理由の再確認**:
- Cytoscape.js: 力学モデルが美しい、データ変換がシンプル

### Phase 4: インタラクティブ機能 (2-3日)
- [ ] ノードクリックイベント実装
- [ ] サイドバーに詳細表示
- [ ] ズーム/パン操作
- [ ] ノードハイライト機能
- [ ] 選択中のノードの接続先ハイライト

### Phase 5: UI/UX強化 (2-3日)
- [ ] ツールバー実装（リフレッシュボタン等）
- [ ] レイアウト切り替え機能（force, hierarchical, circular）
- [ ] フィルター機能（エンティティタイプで絞り込み）
- [ ] 検索機能（エンティティ名検索）
- [ ] スタイリング調整（配色、アニメーション）

### Phase 6: 高度な機能（オプション） (3-5日)
- [ ] **MCPプロトコル経由での通信実装（必須）**: Memory MCPサーバーに直接接続（現在はJSON経由の暫定実装）
- [ ] リアルタイム更新（WebSocketまたはポーリング）
- [ ] グラフ編集機能（ノード/エッジ追加・削除）
- [ ] エクスポート機能（PNG, JSON）
- [ ] 履歴機能（グラフの変化を時系列表示）
- [ ] パフォーマンス最適化（大規模グラフ対応）

---

## 📊 技術選定まとめ

| 技術 | 選定理由 | 代替案 | なぜ代替案を選ばなかったか |
|------|----------|--------|---------------------------|
| **React** | 湧心くんの得意分野、コンポーネント志向 | Vue, Svelte | Reactの経験が豊富 |
| **TypeScript** | 型安全性、kakuhoでも使用 | JavaScript | 大規模化に備えて型定義必須 |
| **Vite** | 高速、モダン、React相性◎ | Webpack, Parcel | 開発体験が圧倒的に良い |
| **Cytoscape.js** | グラフ特化、レイアウト豊富 | D3.js, React Flow | 学習コストと機能のバランス◎ |
| **FastAPI** | 湧心くんが好き、高速、自動ドキュメント | Express, Django | Python親和性、開発速度 |
| **MUI** | kakuhoでも使用、統一感 | Ant Design, Chakra UI | 慣れている、実績あり |

---

## 🎯 最初のマイルストーン

**目標**: 「Memory MCPデータを取得して、シンプルなグラフを画面に表示する」

**完了条件**:
1. バックエンドが `/api/graph` でMemory MCPデータを返す
2. フロントエンドがデータを取得してCytoscape.jsで表示
3. エンティティがノード、リレーションがエッジとして表示される
4. 基本的なレイアウト（force-directed）が適用されている

**推定期間**: 3-5日（平日1-2時間/日）

---

## 🔧 次のアクション

1. ✅ `develop/memory-viz` ディレクトリ作成
2. Phase 1開始: バックエンドセットアップ
   - FastAPI環境構築
   - Memory MCP クライアント実装
3. 動作確認後、Phase 2へ

---

## 📝 メモ

- インフラ弱点克服の観点: 将来的にDocker化することでデプロイ練習にも
- 記憶の可視化: 自分の「外部脳」が目に見える形になる、育成しがい◎
- 拡張性: Memory MCP以外のMCPサーバーにも応用可能
- ポートフォリオ: 技術的な深さと実用性を両立した作品になる
