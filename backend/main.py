"""Memory MCP Visualization Tool - Backend API

FastAPIベースのREST APIサーバー
Memory MCPのナレッジグラフデータを提供
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routers import memory

# 環境変数読み込み
load_dotenv()

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
