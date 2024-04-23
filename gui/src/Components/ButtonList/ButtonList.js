import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import * as React from 'react';
<<<<<<< HEAD
import { useState } from 'react'; // Import useState
import { fetchPost } from '../../util/fetchHelp.js';
=======
import myImage from './logo.png';
>>>>>>> 89ddfa824cdadfc1c7a5317a1e86977e7738ccb4
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
<<<<<<< HEAD
    <Stack spacing={3} direction="column">
      <Button variant="outlined" onClick={handleOpenFiles}>Open Files</Button>
      <Button variant="outlined" onClick={handleSaveLast30Seconds}>Save last 30 seconds</Button>
      <Button variant="outlined" onClick={handleSensitivityChange}>{HLM[sensitivity]}</Button>
    </Stack>
=======
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
>>>>>>> 89ddfa824cdadfc1c7a5317a1e86977e7738ccb4
  );
}
