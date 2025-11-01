/**
 * Memory MCP Visualization - メインアプリケーション
 */

import { useEffect, useState, useCallback } from 'react';
import { Box, CircularProgress, Alert } from '@mui/material';
import { useMemoryGraph } from './hooks/useMemoryGraph';
import { GraphView } from './components/GraphView';
import { Sidebar } from './components/Sidebar';
import { Toolbar } from './components/Toolbar';
import type { Entity } from './types/memory';
import './App.css';

function App() {
  const { graph, loading, error, refresh } = useMemoryGraph();
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  /**
   * ノードクリックハンドラ（useCallbackでメモ化して再レンダリングを防ぐ）
   */
  const handleNodeClick = useCallback((nodeId: string) => {
    setSelectedNodeId(nodeId);
  }, []);

  /**
   * 選択中のエンティティを取得
   */
  const selectedEntity: Entity | null = selectedNodeId && graph
    ? graph.entities.find((e) => e.name === selectedNodeId) || null
    : null;

  /**
   * グラフデータをコンソールに出力（開発用）
   */
  useEffect(() => {
    if (graph) {
      console.log('=== Memory Graph Data ===');
      console.log('Entities:', graph.entities);
      console.log('Relations:', graph.relations);
      console.table(graph.entities);
      console.table(graph.relations);
    }
  }, [graph]);

  return (
    <Box sx={{ p: 3, maxWidth: '1600px', margin: '0 auto' }}>
      {/* ツールバー */}
      {graph && (
        <Toolbar
          onRefresh={refresh}
          loading={loading}
          entityCount={graph.entities.length}
          relationCount={graph.relations.length}
        />
      )}

      {/* ローディング */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {/* エラー表示 */}
      {error && (
        <Alert severity="error" sx={{ my: 2 }}>
          Error: {error.message}
        </Alert>
      )}

      {/* グラフ表示 */}
      {graph && !loading && (
        <Box sx={{ display: 'flex', gap: 2 }}>
          <GraphView
            graph={graph}
            selectedNodeId={selectedNodeId}
            onNodeClick={handleNodeClick}
          />
          <Sidebar entity={selectedEntity} />
        </Box>
      )}
    </Box>
  );
}

export default App;
