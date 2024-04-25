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
    detectLoudNoise();

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

  const detectLoudNoise = React.useCallback(() => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    const stream = videoRef.current.srcObject;
    const source = audioContext.createMediaStreamSource(stream);
  
    source.connect(analyser);
  
    analyser.fftSize = 2048;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
  
    let isLoudNoiseDetected = false;
  
    const checkLoudNoise = () => {
      analyser.getByteFrequencyData(dataArray);
      const peak = Math.max(...dataArray);
  
      if (peak > 250) { // Adjust this threshold as needed
        if (!isLoudNoiseDetected) {
          console.log("Loud noise detected!");
          fetchPost("/record", {type: "loud-noise"}).then(data => {
              setPostData(data.message);
          });
          isLoudNoiseDetected = true;
          setTimeout(() => {
            isLoudNoiseDetected = false; // Reset flag after 5 seconds
          }, 5000);
        }
      }
  
      setTimeout(checkLoudNoise, 100); // Check every 100 milliseconds
    };
  
    checkLoudNoise();
  }, [videoRef]);
  
  
 

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
      <Button variant="outlined" className="MUIButton" onClick={handleOpenFiles}>Open Files</Button>
      
      {!recording ? (
          <Button variant="outlined" className="MUIButton" onClick={startRecording}>Start Recording</Button>
        ) : (
            <Button variant="outlined" className="MUIButton" onClick={stopRecording}>Save Recording</Button>
        )}
      <Button variant="outlined" className="MUIButton" onClick={handleSensitivityChange}>{HLM[sensitivity]}</Button>
    </Stack>
    </div>
    </>
  );
}
