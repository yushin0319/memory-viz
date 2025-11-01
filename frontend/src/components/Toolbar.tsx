/**
 * Toolbar - グラフ操作用ツールバー
 */

import { Box, Button, Typography } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

interface ToolbarProps {
  onRefresh: () => void;
  loading?: boolean;
  entityCount: number;
  relationCount: number;
}

export const Toolbar = ({ onRefresh, loading, entityCount, relationCount }: ToolbarProps) => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        p: 2,
        backgroundColor: '#f5f5f5',
        borderRadius: '4px',
        mb: 2,
      }}
    >
      {/* 左側：グラフ情報 */}
      <Box>
        <Typography variant="h6" component="div">
          Memory MCP Knowledge Graph
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Entities: {entityCount} | Relations: {relationCount}
        </Typography>
      </Box>

      {/* 右側：操作ボタン */}
      <Box>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={onRefresh}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Refresh'}
        </Button>
      </Box>
    </Box>
  );
};
