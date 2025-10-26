/**
 * Memory MCPグラフデータ取得カスタムフック
 */

import { useState, useEffect, useCallback } from 'react';
import { getGraph, refreshGraph } from '../services/api';
import type { MemoryGraph } from '../types/memory';

interface UseMemoryGraphReturn {
  graph: MemoryGraph | null;
  loading: boolean;
  error: Error | null;
  refresh: () => Promise<void>;
}

/**
 * Memory MCPグラフデータを取得・管理するカスタムフック
 *
 * @param autoFetch - 初回自動取得を行うか（デフォルト: true）
 * @returns グラフデータ、ローディング状態、エラー、リフレッシュ関数
 */
export const useMemoryGraph = (autoFetch: boolean = true): UseMemoryGraphReturn => {
  const [graph, setGraph] = useState<MemoryGraph | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  /**
   * グラフデータ取得
   */
  const fetchGraph = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await getGraph();
      setGraph(data);
      console.log('Memory Graph loaded:', data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to fetch graph');
      setError(error);
      console.error('Error fetching graph:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * グラフデータ強制リフレッシュ
   */
  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await refreshGraph();
      setGraph(data);
      console.log('Memory Graph refreshed:', data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to refresh graph');
      setError(error);
      console.error('Error refreshing graph:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * 初回自動取得
   */
  useEffect(() => {
    if (autoFetch) {
      fetchGraph();
    }
  }, [autoFetch, fetchGraph]);

  return {
    graph,
    loading,
    error,
    refresh,
  };
};
