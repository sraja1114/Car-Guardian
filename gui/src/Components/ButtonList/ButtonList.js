import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import * as React from 'react';

export default function ButtonList() {
  return (
    <Stack spacing={3} direction="column">
      <Button variant="outlined">Outlined</Button>
      <Button variant="outlined">Outlined</Button>
      <Button variant="outlined">Outlined</Button>
    </Stack>
  );
}