"""pytest共通設定

テスト全体で共有するfixtureを定義
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from services.memory_client import MemoryMCPClient, _client_instance
from models.memory import MemoryGraph, Entity, Relation


@pytest.fixture
def client():
    """FastAPI TestClient

    APIエンドポイントのテスト用クライアント

    Yields:
        TestClient: テスト用HTTPクライアント
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def memory_client():
    """Memory MCPクライアント（ダミーデータ使用）

    Yields:
        MemoryMCPClient: テスト用クライアント
    """
    client = MemoryMCPClient()
    yield client


@pytest.fixture
def sample_graph():
    """サンプルグラフデータ

    テストで使用するサンプルデータ

    Returns:
        MemoryGraph: サンプルのグラフデータ
    """
    entities = [
        Entity(
            name="テストユーザー",
            entityType="user",
            observations=["テスト用観測1", "テスト用観測2"]
        ),
        Entity(
            name="テスト環境",
            entityType="environment",
            observations=["テスト環境の観測"]
        ),
    ]

    relations = [
        Relation(
            from_="テストユーザー",
            to="テスト環境",
            relationType="uses"
        ),
    ]

    return MemoryGraph(entities=entities, relations=relations)


@pytest.fixture(autouse=True)
def reset_client_instance():
    """各テスト後にクライアントインスタンスをリセット

    グローバルシングルトンをクリーンな状態に戻す
    """
    yield
    global _client_instance
    _client_instance = None
