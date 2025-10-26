"""Memory MCP クライアント

Memory MCPサーバーとの通信を担当するクライアント。
現在はダミーデータを返す実装。将来的にMCPプロトコル経由での通信を実装予定。
"""

import json
from pathlib import Path
from typing import Dict, Optional, List
from models.memory import MemoryGraph, Entity, Relation, EntityDetail


class MemoryMCPClient:
    """Memory MCP クライアント

    Phase 1では簡易実装（ダミーデータまたはJSONファイル読み込み）
    Phase 2以降でMCPプロトコル経由の通信を実装予定
    """

    def __init__(self, data_file: Optional[Path] = None):
        """初期化

        Args:
            data_file: Memory MCPデータのJSONファイルパス（オプション）
        """
        self.data_file = data_file
        self._cache: Optional[MemoryGraph] = None

    async def read_graph(self) -> MemoryGraph:
        """Memory MCPからグラフ全体を取得

        Returns:
            MemoryGraph: エンティティとリレーションを含むグラフデータ
        """
        # キャッシュがあればそれを返す
        if self._cache:
            return self._cache

        # データファイルが指定されていれば読み込む
        if self.data_file and self.data_file.exists():
            return self._load_from_file()

        # ダミーデータを返す（開発用）
        return self._get_dummy_data()

    def _load_from_file(self) -> MemoryGraph:
        """JSONファイルからデータを読み込む

        Returns:
            MemoryGraph: 読み込んだグラフデータ
        """
        with open(self.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        graph = MemoryGraph(**data)
        self._cache = graph
        return graph

    def _get_dummy_data(self) -> MemoryGraph:
        """ダミーデータを生成（開発・テスト用）

        Returns:
            MemoryGraph: ダミーのグラフデータ
        """
        entities = [
            Entity(
                name="湧心くん",
                entityType="user",
                observations=[
                    "Pythonが好き",
                    "Reactが好き",
                    "フルスタックでフロント寄りのエンジニア",
                    "記憶システムに興味がある"
                ]
            ),
            Entity(
                name="Windows環境",
                entityType="environment",
                observations=[
                    "Windowsネイティブコマンドを優先",
                    ".batまたは.ps1スクリプトを使用"
                ]
            ),
            Entity(
                name="Memory MCP",
                entityType="tool",
                observations=[
                    "ナレッジグラフベースの記憶システム",
                    "エンティティとリレーションで情報を管理"
                ]
            ),
            Entity(
                name="kakuho",
                entityType="project",
                observations=[
                    "イベント予約管理システム",
                    "FastAPI + React + TypeScript",
                    "半年かけて作成"
                ]
            ),
        ]

        relations = [
            Relation(from_="湧心くん", to="Windows環境", relationType="uses"),
            Relation(from_="湧心くん", to="Memory MCP", relationType="uses"),
            Relation(from_="湧心くん", to="kakuho", relationType="created"),
            Relation(from_="Memory MCP", to="Windows環境", relationType="runs on"),
        ]

        graph = MemoryGraph(entities=entities, relations=relations)
        self._cache = graph
        return graph

    async def get_entity(self, entity_name: str) -> Optional[EntityDetail]:
        """特定のエンティティの詳細を取得

        Args:
            entity_name: エンティティ名

        Returns:
            EntityDetail: エンティティ詳細、存在しない場合はNone
        """
        graph = await self.read_graph()

        # エンティティを検索
        entity = next(
            (e for e in graph.entities if e.name == entity_name),
            None
        )

        if not entity:
            return None

        # 関連エンティティを収集
        related: List[str] = []
        for rel in graph.relations:
            if rel.from_ == entity_name:
                related.append(rel.to)
            elif rel.to == entity_name:
                related.append(rel.from_)

        return EntityDetail(
            name=entity.name,
            entityType=entity.entityType,
            observations=entity.observations,
            relatedEntities=list(set(related))  # 重複削除
        )

    async def refresh(self) -> MemoryGraph:
        """キャッシュをクリアして最新データを取得

        Returns:
            MemoryGraph: 最新のグラフデータ
        """
        self._cache = None
        return await self.read_graph()

    def set_data_file(self, file_path: Path):
        """データファイルを設定

        Args:
            file_path: JSONファイルパス
        """
        self.data_file = file_path
        self._cache = None  # キャッシュクリア


# グローバルインスタンス（シングルトンパターン）
_client_instance: Optional[MemoryMCPClient] = None


def get_memory_client() -> MemoryMCPClient:
    """Memory MCPクライアントのインスタンスを取得

    FastAPIの依存性注入で使用

    Returns:
        MemoryMCPClient: クライアントインスタンス
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = MemoryMCPClient()
    return _client_instance
