"""Memory MCP Visualization Tool - Backend API

FastAPIベースのREST APIサーバー
Memory MCPのナレッジグラフデータを提供
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pathlib import Path

from routers import memory
from services.memory_client import get_memory_client

# 環境変数読み込み
load_dotenv()

# Memory MCPクライアントにJSONファイルパスを設定
data_file = Path(__file__).parent / "data" / "memory_graph.json"
if data_file.exists():
    client = get_memory_client()
    client.set_data_file(data_file)
    print(f"[OK] Memory MCP data loaded from: {data_file}")

# FastAPIアプリケーション作成
app = FastAPI(
    title="Memory MCP Visualization API",
    description="Memory MCPのナレッジグラフを可視化するためのREST API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS設定（フロントエンドからのアクセスを許可）
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(memory.router)


@app.get("/", tags=["root"])
async def root():
    """ルートエンドポイント

    Returns:
        dict: APIの基本情報
    """
    return {
        "name": "Memory MCP Visualization API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    import uvicorn

    # 開発サーバー起動
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )
