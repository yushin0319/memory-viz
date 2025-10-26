"""Memory MCP API エンドポイント"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.memory import MemoryGraph, EntityDetail
from services.memory_client import MemoryMCPClient, get_memory_client

router = APIRouter(
    prefix="/api",
    tags=["memory"],
    responses={404: {"description": "Not found"}},
)


@router.get("/graph", response_model=MemoryGraph, summary="グラフ全体を取得")
async def get_graph(
    client: MemoryMCPClient = Depends(get_memory_client)
) -> MemoryGraph:
    """Memory MCPからグラフ全体（エンティティとリレーション）を取得

    Returns:
        MemoryGraph: エンティティとリレーションを含むグラフデータ
    """
    try:
        graph = await client.read_graph()
        return graph
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch graph data: {str(e)}"
        )


@router.get("/graph/refresh", response_model=MemoryGraph, summary="グラフを強制更新")
async def refresh_graph(
    client: MemoryMCPClient = Depends(get_memory_client)
) -> MemoryGraph:
    """Memory MCPから最新のグラフデータを取得（キャッシュクリア）

    Returns:
        MemoryGraph: 最新のグラフデータ
    """
    try:
        graph = await client.refresh()
        return graph
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refresh graph data: {str(e)}"
        )


@router.get(
    "/entities/{entity_name}",
    response_model=EntityDetail,
    summary="エンティティ詳細を取得"
)
async def get_entity(
    entity_name: str,
    client: MemoryMCPClient = Depends(get_memory_client)
) -> EntityDetail:
    """特定のエンティティの詳細情報を取得

    Args:
        entity_name: エンティティ名

    Returns:
        EntityDetail: エンティティの詳細（observations、関連エンティティ等）

    Raises:
        HTTPException: エンティティが見つからない場合は404
    """
    try:
        entity = await client.get_entity(entity_name)
        if entity is None:
            raise HTTPException(
                status_code=404,
                detail=f"Entity '{entity_name}' not found"
            )
        return entity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch entity: {str(e)}"
        )


@router.get("/health", summary="ヘルスチェック")
async def health_check():
    """APIサーバーのヘルスチェック

    Returns:
        dict: ステータス情報
    """
    return {"status": "ok", "service": "memory-viz-api"}
