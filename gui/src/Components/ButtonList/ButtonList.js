import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import * as React from 'react';
import myImage from './logo.png';
import "./ButtonList.css";

export default function ButtonList() {
  return (
    <Stack spacing={3} direction="column">
      <Button variant="outlined">Outlined</Button>
      <Button variant="outlined">Outlined</Button>
      <Button variant="outlined">Outlined</Button>
    </Stack>
  );
}