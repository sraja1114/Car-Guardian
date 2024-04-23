import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import * as React from 'react';
import myImage from './logo.png';
import "./ButtonList.css";

export default function ButtonList() {
  return (
    <>
    <div className="button-list-container"> {/* Use the CSS class */}
    <div>
      <img src={myImage} alt="My Image" className="my-image" />
    </div>
      <Stack spacing={3} direction="column">
        <Button variant="outlined" class="MuiButton-label">Sensitivity</Button>
        <Button variant="outlined" class="MuiButton-label">Dashcam Videos</Button>
        <Button variant="outlined" class="MuiButton-label">Record</Button>
      </Stack>
    </div>
    </>
  );
}