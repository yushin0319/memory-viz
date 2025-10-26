/**
 * Memory MCP型定義
 * バックエンドのPydanticモデルに対応
 */

/**
 * エンティティ
 */
export interface Entity {
  name: string;
  entityType: string;
  observations: string[];
}

/**
 * リレーション
 */
export interface Relation {
  from: string;
  to: string;
  relationType: string;
}

/**
 * メモリグラフ
 */
export interface MemoryGraph {
  entities: Entity[];
  relations: Relation[];
}

/**
 * APIレスポンス型
 */
export interface GraphResponse {
  entities: Entity[];
  relations: Relation[];
}

export interface EntityResponse extends Entity {}

export interface HealthResponse {
  status: string;
  timestamp: string;
}
