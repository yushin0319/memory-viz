"""Memory MCP データモデル"""

from typing import List
from pydantic import BaseModel, Field, ConfigDict


class Entity(BaseModel):
    """エンティティモデル"""
    type: str = Field(default="entity", description="エンティティタイプ識別子")
    name: str = Field(..., description="エンティティ名")
    entityType: str = Field(..., description="エンティティの種類（user, environment等）")
    observations: List[str] = Field(default_factory=list, description="観測データリスト")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "entity",
                "name": "湧心くん",
                "entityType": "user",
                "observations": [
                    "Pythonが好き",
                    "フルスタックエンジニア"
                ]
            }
        }
    )


class Relation(BaseModel):
    """リレーションモデル"""
    type: str = Field(default="relation", description="リレーションタイプ識別子")
    from_: str = Field(..., alias="from", description="関係の起点エンティティ名")
    to: str = Field(..., description="関係の終点エンティティ名")
    relationType: str = Field(..., description="関係の種類（uses, created等）")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "type": "relation",
                "from": "湧心くん",
                "to": "Windows環境",
                "relationType": "uses"
            }
        }
    )


class MemoryGraph(BaseModel):
    """Memory MCPグラフ全体のモデル"""
    entities: List[Entity] = Field(default_factory=list, description="エンティティリスト")
    relations: List[Relation] = Field(default_factory=list, description="リレーションリスト")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "entities": [
                    {
                        "type": "entity",
                        "name": "湧心くん",
                        "entityType": "user",
                        "observations": ["Pythonが好き"]
                    }
                ],
                "relations": [
                    {
                        "type": "relation",
                        "from": "湧心くん",
                        "to": "Windows環境",
                        "relationType": "uses"
                    }
                ]
            }
        }
    )


class EntityDetail(BaseModel):
    """エンティティ詳細モデル（API応答用）"""
    name: str
    entityType: str
    observations: List[str]
    relatedEntities: List[str] = Field(default_factory=list, description="関連エンティティ名リスト")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "湧心くん",
                "entityType": "user",
                "observations": ["Pythonが好き", "フルスタックエンジニア"],
                "relatedEntities": ["Windows環境", "kakuho"]
            }
        }
    )
