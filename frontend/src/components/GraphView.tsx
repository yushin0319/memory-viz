/**
 * GraphView - Cytoscape.jsでグラフを表示するコンポーネント
 */

import { useEffect, useRef } from 'react';
import { Box } from '@mui/material';
import cytoscape from 'cytoscape';
import type { MemoryGraph } from '../types/memory';
import { transformToCytoscape, cytoscapeStylesheet } from '../utils/graphTransform';

interface GraphViewProps {
  graph: MemoryGraph | null;
  onNodeClick?: (nodeId: string) => void;
}

export const GraphView = ({ graph, onNodeClick }: GraphViewProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Cytoscapeインスタンス作成
    cyRef.current = cytoscape({
      container: containerRef.current,
      style: cytoscapeStylesheet as any,
      layout: {
        name: 'cose', // force-directed layout
        animate: true,
        animationDuration: 500,
      },
    });

    // ノードクリックイベント
    cyRef.current.on('tap', 'node', (event) => {
      const nodeId = event.target.id();
      console.log('Node clicked:', nodeId);
      if (onNodeClick) {
        onNodeClick(nodeId);
      }
    });

    return () => {
      cyRef.current?.destroy();
    };
  }, [onNodeClick]);

  // グラフデータ更新
  useEffect(() => {
    if (!cyRef.current || !graph) return;

    const elements = transformToCytoscape(graph);
    cyRef.current.elements().remove();
    cyRef.current.add(elements);

    // レイアウト再適用
    cyRef.current.layout({
      name: 'cose',
      animate: true,
      animationDuration: 500,
    }).run();

    // 全体を表示するようにフィット
    cyRef.current.fit(undefined, 50);
  }, [graph]);

  return (
    <Box
      ref={containerRef}
      sx={{
        width: '100%',
        height: '600px',
        border: '1px solid #ddd',
        borderRadius: 1,
        backgroundColor: '#fafafa',
      }}
    />
  );
};
