import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import * as React from 'react';
import { useState } from 'react'; // Import useState
import { fetchPost } from '../../util/fetchHelp.js';
import "./ButtonList.css";
export default function ButtonList() {
  const HLM = ["Low", "Medium", "High"]
  const [sensitivity, setSensitivity] = useState(0);
  const [postData, setPostData] = useState()


  const handleOpenFiles = () => {
    // Add your logic here
    console.log("Opening files...");
  };

  // Function to handle saving last 30 seconds
  const handleSaveLast30Seconds = () => {
    // Add your logic here
    console.log("Saving last 30 seconds...");
  };

// Function to handle sensitivity change
    const handleSensitivityChange = () => {
        setSensitivity((sensitivity + 1) % 3);
        const postData = { 'sensitivity': HLM[(sensitivity + 1) % 3]};
        fetchPost("/sensitivity", postData).then(data => {
            setPostData(data.message);
        });
    };
  

  return (
    <Stack spacing={3} direction="column">
      <Button variant="outlined" onClick={handleOpenFiles}>Open Files</Button>
      <Button variant="outlined" onClick={handleSaveLast30Seconds}>Save last 30 seconds</Button>
      <Button variant="outlined" onClick={handleSensitivityChange}>{HLM[sensitivity]}</Button>
    </Stack>
  );
}
