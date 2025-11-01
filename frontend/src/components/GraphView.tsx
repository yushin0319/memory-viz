/**
 * GraphView - Cytoscape.jsでグラフを表示
 */

import { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';
import type { MemoryGraph } from '../types/memory';
import { transformToCytoscape, cytoscapeStylesheet } from '../utils/graphTransform';

interface GraphViewProps {
  graph: MemoryGraph | null;
  selectedNodeId?: string | null;
  onNodeClick?: (nodeId: string) => void;
}

export const GraphView = ({ graph, selectedNodeId, onNodeClick }: GraphViewProps) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  // Cytoscapeインスタンス初期化
  useEffect(() => {
    if (!containerRef.current) return;

    // 固定サイズを明示的に指定
    const container = containerRef.current;
    const width = container.offsetWidth;
    const height = container.offsetHeight;

    cyRef.current = cytoscape({
      container: container,
      style: cytoscapeStylesheet as any,
      // ズーム/パン操作を明示的に有効化
      zoomingEnabled: true,
      userZoomingEnabled: true,
      panningEnabled: true,
      userPanningEnabled: true,
      boxSelectionEnabled: false,
      autoungrabify: false,
    });

    // Cytoscapeが自動的に追加したwindow resizeリスナーを無効化
    // (内部的にresizeハンドラが登録されているため、これを上書き)
    const cy = cyRef.current;

    // resizeイベントを無効化するためのフラグ
    (cy as any)._private = (cy as any)._private || {};
    (cy as any)._private.autoResizeEnabled = false;

    // ノードクリックイベント
    cy.on('tap', 'node', (event) => {
      const nodeId = event.target.id();
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

    const cy = cyRef.current;
    const elements = transformToCytoscape(graph);

    // 既存要素をクリア
    cy.elements().remove();

    // 新しい要素を追加
    cy.add(elements);

    // coseレイアウト（force-directed）
    const layout = cy.layout({
      name: 'cose',
      animate: false,
      fit: false,  // 自動フィットを無効化
      padding: 30,
      nodeRepulsion: 400000,
      idealEdgeLength: 100,
      edgeElasticity: 100,
      randomize: false,
    });

    layout.run();

    // レイアウト完了後、明示的に中央配置
    cy.fit(cy.elements(), 30);
    cy.center();
  }, [graph]);

  // 選択ノードハイライト処理
  useEffect(() => {
    if (!cyRef.current) return;

    const cy = cyRef.current;

    if (!selectedNodeId) {
      // 選択解除時、すべてのノードを通常表示
      cy.elements().removeClass('highlighted dimmed');
      return;
    }

    // 選択ノードを取得
    const selectedNode = cy.getElementById(selectedNodeId);

    if (selectedNode.length === 0) {
      cy.elements().removeClass('highlighted dimmed');
      return;
    }

    // 選択ノードと接続先（隣接ノード＋エッジ）を取得
    const neighborhood = selectedNode.closedNeighborhood();

    // すべての要素をリセット
    cy.elements().removeClass('highlighted dimmed');

    // 選択ノードと接続先をハイライト
    neighborhood.addClass('highlighted');

    // それ以外のノード・エッジを半透明化
    cy.elements().not(neighborhood).addClass('dimmed');
  }, [selectedNodeId]);

  return (
    <div
      ref={containerRef}
      className="cytoscape-container"
      style={{
        width: '1200px',
        height: '600px',
        border: '1px solid #ddd',
        borderRadius: '4px',
        backgroundColor: '#fafafa',
        position: 'relative',
        overflow: 'hidden',
      }}
    />
  );
};
