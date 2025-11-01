/**
 * Sidebar - 選択エンティティの詳細表示
 */

import { Box, Typography, Paper, Divider, Chip } from '@mui/material';
import type { Entity } from '../types/memory';

interface SidebarProps {
  entity: Entity | null;
  onClose?: () => void;
}

export const Sidebar = ({ entity }: SidebarProps) => {
  if (!entity) {
    return (
      <Paper
        elevation={2}
        sx={{
          width: 350,
          height: '100%',
          p: 3,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#fafafa',
        }}
      >
        <Typography variant="body2" color="text.secondary">
          ノードをクリックして詳細を表示
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper
      elevation={2}
      sx={{
        width: 350,
        height: '100%',
        p: 3,
        overflow: 'auto',
      }}
    >
      {/* エンティティ名 */}
      <Typography variant="h5" gutterBottom>
        {entity.name}
      </Typography>

      {/* エンティティタイプ */}
      <Chip
        label={entity.entityType}
        color="primary"
        size="small"
        sx={{ mb: 2 }}
      />

      <Divider sx={{ my: 2 }} />

      {/* Observations */}
      <Typography variant="h6" gutterBottom>
        Observations
      </Typography>

      {entity.observations.length === 0 ? (
        <Typography variant="body2" color="text.secondary">
          記録なし
        </Typography>
      ) : (
        <Box component="ul" sx={{ pl: 2, mt: 1 }}>
          {entity.observations.map((obs, index) => (
            <Box
              component="li"
              key={index}
              sx={{
                mb: 1,
                '&::marker': {
                  color: 'primary.main',
                },
              }}
            >
              <Typography variant="body2">{obs}</Typography>
            </Box>
          ))}
        </Box>
      )}
    </Paper>
  );
};
