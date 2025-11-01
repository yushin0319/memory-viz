/**
 * Memory MCP Visualization - メインアプリケーション
 */

import { useEffect, useState, useCallback } from 'react';
import { Container, Box, Typography, Button, CircularProgress, Alert, Grid } from '@mui/material';
import { useMemoryGraph } from './hooks/useMemoryGraph';
import { GraphView } from './components/GraphView';
import { Sidebar } from './components/Sidebar';
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
    <Box sx={{ maxWidth: '1200px' }}>
      <Box sx={{ my: 4 }}>
        {/* ヘッダー */}
        <Typography variant="h3" component="h1" gutterBottom>
          Memory MCP Visualization
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          Memory MCPのナレッジグラフを可視化
        </Typography>

        {/* コントロール */}
        <Box sx={{ my: 2 }}>
          <Button
            variant="contained"
            onClick={refresh}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Refresh Graph'}
          </Button>
        </Box>

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
          <Box sx={{ my: 4 }}>
            <Typography variant="h5" gutterBottom>
              Knowledge Graph
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Entities: {graph.entities.length} | Relations: {graph.relations.length}
            </Typography>

            {/* グラフとサイドバーを横並び */}
            <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
              <GraphView
                graph={graph}
                selectedNodeId={selectedNodeId}
                onNodeClick={handleNodeClick}
              />
              <Sidebar entity={selectedEntity} />
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  );
}

export default App;
