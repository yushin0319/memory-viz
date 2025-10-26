/**
 * Memory MCP API クライアント
 */

import axios from 'axios';
import type { GraphResponse, EntityResponse, HealthResponse } from '../types/memory';

// APIベースURL（環境変数から取得、デフォルトはlocalhost）
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Axiosインスタンス作成
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Memory MCPグラフデータ取得
 */
export const getGraph = async (): Promise<GraphResponse> => {
  const response = await apiClient.get<GraphResponse>('/api/graph');
  return response.data;
};

/**
 * Memory MCPグラフデータ強制リフレッシュ
 */
export const refreshGraph = async (): Promise<GraphResponse> => {
  const response = await apiClient.get<GraphResponse>('/api/graph/refresh');
  return response.data;
};

/**
 * 特定エンティティの詳細取得
 */
export const getEntity = async (name: string): Promise<EntityResponse> => {
  const response = await apiClient.get<EntityResponse>(`/api/entities/${encodeURIComponent(name)}`);
  return response.data;
};

/**
 * ヘルスチェック
 */
export const getHealth = async (): Promise<HealthResponse> => {
  const response = await apiClient.get<HealthResponse>('/api/health');
  return response.data;
};

export default apiClient;
