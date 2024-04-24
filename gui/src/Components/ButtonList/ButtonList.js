import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import * as React from 'react';
import { useState } from 'react'; // Import useState
import { fetchPost } from '../../util/fetchHelp.js';
import "./ButtonList.css";
import myImage from './logo.png';

export default function ButtonList({ videoRef }) {
  const HLM = ["Low", "Medium", "High"]
  const [sensitivity, setSensitivity] = useState(0);
  const [postData, setPostData] = useState()
  const [recording, setRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [timerId, setTimerId] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  const handleOpenFiles = () => {

    fetchPost('/open_file_explorer', 3).then(data => {
        
    })
    console.log("post request for open_file_explorer");
  };

  // Function to handle saving last 30 seconds
  const handleSaveLast30Seconds = () => {
    // Add your logic here
    console.log("Saving last 30 seconds...");
  };
  const startRecording = () => {
    const stream = videoRef.current.srcObject;
    const newMediaRecorder = new MediaRecorder(stream);
    const chunks = [];

    newMediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunks.push(event.data);
      }
    };

    newMediaRecorder.onstop = () => {
      const recordedBlob = new Blob(chunks, { type: "video/webm" });
      setRecordedChunks(chunks);
      setRecording(false);
      saveRecording(recordedBlob);
      if (!timerId) {
        // Restart recording if not stopped manually
        startRecording();
      }
    };

    newMediaRecorder.start();
    setRecording(true);

    // Automatically stop recording after 60 seconds
    const timer = setTimeout(() => {
      newMediaRecorder.stop();
    }, 60000);

    setTimerId(timer);
    setMediaRecorder(newMediaRecorder);
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
    }
    if (timerId) {
      clearTimeout(timerId);
      setTimerId(null);
    }
    setRecording(false);
  };

  const saveRecording = (blob) => {
    const videoURL = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = videoURL;
    const recording_name = `${new Date().toJSON().slice(0, 19)}.webm`;
    a.download = recording_name;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(videoURL);
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
    
    <>
    <div className="button-list-container"> {/* Use the CSS class */}
    <div>
      <img src={myImage} alt="My Image" className="my-image" />
    </div>
    <Stack spacing={3} direction="column">
      <Button variant="outlined" class="MuiButton-label" onClick={handleOpenFiles}>Open Files</Button>
      
      {!recording ? (
          <Button variant="outlined" class="MuiButton-label" onClick={startRecording}>Start Recording</Button>
        ) : (
            <Button variant="outlined" class="MuiButton-label" onClick={stopRecording}>Stop Recording</Button>
        )}
      <Button variant="outlined" class="MuiButton-label" onClick={handleSensitivityChange}>{HLM[sensitivity]}</Button>
    </Stack>
    </div>
    </>
  );
}
