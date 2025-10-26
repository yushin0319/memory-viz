/**
 * Memory MCPデータをCytoscape.js形式に変換
 */

import type { MemoryGraph, Entity, Relation } from '../types/memory';
import type { ElementDefinition } from 'cytoscape';

/**
 * エンティティタイプごとの色
 */
const getColorByType = (entityType: string): string => {
  const colorMap: Record<string, string> = {
    user: '#4CAF50',        // Green
    environment: '#2196F3', // Blue
    project: '#FF9800',     // Orange
    tool: '#9C27B0',        // Purple
    concept: '#F44336',     // Red
    default: '#607D8B',     // Blue Grey
  };
  return colorMap[entityType.toLowerCase()] || colorMap.default;
};

/**
 * EntityをCytoscapeノードに変換
 */
const entityToNode = (entity: Entity): ElementDefinition => ({
  data: {
    id: entity.name,
    label: entity.name,
    type: entity.entityType,
    observations: entity.observations,
    color: getColorByType(entity.entityType),
  },
  classes: entity.entityType.toLowerCase(),
});

/**
 * RelationをCytoscapeエッジに変換
 */
const relationToEdge = (relation: Relation, index: number): ElementDefinition => ({
  data: {
    id: `edge-${index}`,
    source: relation.from,
    target: relation.to,
    label: relation.relationType,
  },
});

/**
 * Memory MCPグラフをCytoscape形式に変換
 */
export const transformToCytoscape = (graph: MemoryGraph): ElementDefinition[] => {
  const nodes = graph.entities.map(entityToNode);
  const edges = graph.relations.map(relationToEdge);
  return [...nodes, ...edges];
};

/**
 * Cytoscapeスタイルシート
 */
export const cytoscapeStylesheet = [
  {
    selector: 'node',
    style: {
      'background-color': 'data(color)',
      'label': 'data(label)',
      'color': '#000',
      'text-valign': 'center',
      'text-halign': 'center',
      'font-size': '12px',
      'width': '60px',
      'height': '60px',
      'border-width': '2px',
      'border-color': '#fff',
      'text-wrap': 'wrap',
      'text-max-width': '80px',
    },
  },
  {
    selector: 'edge',
    style: {
      'width': 2,
      'line-color': '#999',
      'target-arrow-color': '#999',
      'target-arrow-shape': 'triangle',
      'curve-style': 'bezier',
      'label': 'data(label)',
      'font-size': '10px',
      'text-rotation': 'autorotate',
      'text-margin-y': -10,
    },
  },
  {
    selector: 'node:selected',
    style: {
      'border-width': '4px',
      'border-color': '#FFC107',
    },
  },
];
