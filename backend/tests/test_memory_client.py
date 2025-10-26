"""Memory MCPクライアントのテスト"""

import pytest
from pathlib import Path
from services.memory_client import MemoryMCPClient
from models.memory import MemoryGraph, Entity, Relation


class TestMemoryMCPClient:
    """Memory MCPクライアントのテストクラス"""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_read_graph_returns_dummy_data(self, memory_client):
        """read_graph()がダミーデータを返すことを確認"""
        graph = await memory_client.read_graph()

        # グラフデータが返ってくることを確認
        assert isinstance(graph, MemoryGraph)
        assert len(graph.entities) > 0
        assert len(graph.relations) > 0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_read_graph_caches_data(self, memory_client):
        """read_graph()がデータをキャッシュすることを確認"""
        graph1 = await memory_client.read_graph()
        graph2 = await memory_client.read_graph()

        # 同じインスタンスが返ることを確認（キャッシュ機能）
        assert graph1 is graph2

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_refresh_clears_cache(self, memory_client):
        """refresh()がキャッシュをクリアすることを確認"""
        graph1 = await memory_client.read_graph()
        graph2 = await memory_client.refresh()

        # キャッシュがクリアされて新しいインスタンスが返ることを確認
        # ダミーデータなので内容は同じだが、インスタンスは異なる
        assert graph1 is not graph2
        assert len(graph1.entities) == len(graph2.entities)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_entity_existing(self, memory_client):
        """get_entity()で存在するエンティティを取得できることを確認"""
        # まずグラフを読み込む
        graph = await memory_client.read_graph()
        first_entity_name = graph.entities[0].name

        # エンティティ詳細を取得
        entity_detail = await memory_client.get_entity(first_entity_name)

        assert entity_detail is not None
        assert entity_detail.name == first_entity_name
        assert len(entity_detail.observations) > 0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_entity_non_existing(self, memory_client):
        """get_entity()で存在しないエンティティを取得した場合Noneが返ることを確認"""
        entity_detail = await memory_client.get_entity("存在しないエンティティ")
        assert entity_detail is None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_entity_includes_related_entities(self, memory_client):
        """get_entity()が関連エンティティを含むことを確認"""
        graph = await memory_client.read_graph()

        # リレーションを持つエンティティを探す
        entity_with_relations = None
        for entity in graph.entities:
            for rel in graph.relations:
                if rel.from_ == entity.name or rel.to == entity.name:
                    entity_with_relations = entity.name
                    break
            if entity_with_relations:
                break

        if entity_with_relations:
            entity_detail = await memory_client.get_entity(entity_with_relations)
            assert len(entity_detail.relatedEntities) > 0

    @pytest.mark.unit
    def test_set_data_file(self, memory_client, tmp_path):
        """set_data_file()でデータファイルを設定できることを確認"""
        test_file = tmp_path / "test_data.json"

        memory_client.set_data_file(test_file)

        assert memory_client.data_file == test_file
        assert memory_client._cache is None  # キャッシュがクリアされている


class TestMemoryMCPClientWithFile:
    """ファイル読み込み機能のテスト"""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_load_from_file(self, tmp_path, sample_graph):
        """JSONファイルからデータを読み込めることを確認"""
        # テスト用JSONファイル作成
        test_file = tmp_path / "test_data.json"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(sample_graph.model_dump_json())

        # ファイルからデータ読み込み
        client = MemoryMCPClient(data_file=test_file)
        graph = await client.read_graph()

        # データが正しく読み込まれることを確認
        assert len(graph.entities) == len(sample_graph.entities)
        assert len(graph.relations) == len(sample_graph.relations)
        assert graph.entities[0].name == sample_graph.entities[0].name
