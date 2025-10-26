"""APIエンドポイントのテスト"""

import pytest
from fastapi import status


class TestRootEndpoint:
    """ルートエンドポイントのテスト"""

    @pytest.mark.unit
    def test_root(self, client):
        """ルートエンドポイントが正常に応答することを確認"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["name"] == "Memory MCP Visualization API"


class TestHealthEndpoint:
    """ヘルスチェックエンドポイントのテスト"""

    @pytest.mark.unit
    def test_health_check(self, client):
        """ヘルスチェックが正常に応答することを確認"""
        response = client.get("/api/health")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "memory-viz-api"


class TestGraphEndpoint:
    """グラフ取得エンドポイントのテスト"""

    @pytest.mark.unit
    def test_get_graph(self, client):
        """グラフ全体を取得できることを確認"""
        response = client.get("/api/graph")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "entities" in data
        assert "relations" in data
        assert isinstance(data["entities"], list)
        assert isinstance(data["relations"], list)

    @pytest.mark.unit
    def test_get_graph_returns_valid_structure(self, client):
        """取得したグラフが正しい構造を持つことを確認"""
        response = client.get("/api/graph")
        data = response.json()

        # エンティティの構造確認
        if len(data["entities"]) > 0:
            entity = data["entities"][0]
            assert "name" in entity
            assert "entityType" in entity
            assert "observations" in entity

        # リレーションの構造確認
        if len(data["relations"]) > 0:
            relation = data["relations"][0]
            assert "from" in relation
            assert "to" in relation
            assert "relationType" in relation

    @pytest.mark.unit
    def test_refresh_graph(self, client):
        """グラフのリフレッシュが正常に動作することを確認"""
        response = client.get("/api/graph/refresh")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "entities" in data
        assert "relations" in data


class TestEntityEndpoint:
    """エンティティ詳細エンドポイントのテスト"""

    @pytest.mark.unit
    def test_get_existing_entity(self, client):
        """存在するエンティティの詳細を取得できることを確認"""
        # まずグラフを取得してエンティティ名を確認
        graph_response = client.get("/api/graph")
        entities = graph_response.json()["entities"]

        if len(entities) > 0:
            entity_name = entities[0]["name"]

            # エンティティ詳細を取得
            response = client.get(f"/api/entities/{entity_name}")
            assert response.status_code == status.HTTP_200_OK

            data = response.json()
            assert data["name"] == entity_name
            assert "entityType" in data
            assert "observations" in data
            assert "relatedEntities" in data

    @pytest.mark.unit
    def test_get_non_existing_entity(self, client):
        """存在しないエンティティを取得した場合404が返ることを確認"""
        response = client.get("/api/entities/存在しないエンティティ")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        data = response.json()
        assert "detail" in data

    @pytest.mark.unit
    def test_entity_detail_includes_related_entities(self, client):
        """エンティティ詳細に関連エンティティが含まれることを確認"""
        # グラフからリレーションを持つエンティティを探す
        graph_response = client.get("/api/graph")
        graph_data = graph_response.json()

        # リレーションがある場合
        if len(graph_data["relations"]) > 0:
            # リレーションの起点エンティティを取得
            entity_name = graph_data["relations"][0]["from"]

            response = client.get(f"/api/entities/{entity_name}")
            assert response.status_code == status.HTTP_200_OK

            data = response.json()
            # 関連エンティティがリストとして含まれることを確認
            assert isinstance(data["relatedEntities"], list)
