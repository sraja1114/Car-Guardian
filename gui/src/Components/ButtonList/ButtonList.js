import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import * as React from 'react';
import "./ButtonList.css";

export default function ButtonList() {
  return (
    <Stack spacing={3} direction="column">
      <Button variant="outlined" class="MuiButton-label">Open Files</Button>
      <Button variant="outlined" class="MuiButton-label">Save last 30 seconds</Button>
      <Button variant="outlined" class="MuiButton-label">Sensitivity</Button>
    </Stack>
  );
}