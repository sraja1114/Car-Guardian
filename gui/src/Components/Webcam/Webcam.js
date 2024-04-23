import React, { useEffect, useRef, useState } from 'react';

const WebcamComponent = () => {
  const videoRef = useRef(null);
  const [recording, setRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [timerId, setTimerId] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  useEffect(() => {
    const constraints = { video: true, audio: true };

    const handleSuccess = (stream) => {
      videoRef.current.srcObject = stream;
    };

    const handleError = (error) => {
      console.error('Error accessing webcam:', error);
    };

    navigator.mediaDevices.getUserMedia(constraints)
      .then(handleSuccess)
      .catch(handleError);

    // Clean up: Stop the video stream when the component unmounts
    return () => {
      if (videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject;
        const tracks = stream.getTracks();

        tracks.forEach((track) => {
          track.stop();
        });
      }
    };
  }, []);

  const startRecording = () => {
    const stream = videoRef.current.srcObject;
    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunks.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      const recordedBlob = new Blob(chunks, { type: 'video/webm' });
      setRecordedChunks(chunks);
      setRecording(false);
      saveRecording(recordedBlob);
    };

    mediaRecorder.start();
    setRecording(true);

    // Automatically stop recording after 10 seconds
    const timer = setTimeout(() => {
      mediaRecorder.stop();
    }, 60000);

    setTimerId(timer);
  };

  const stopRecording = () => {
    const stream = videoRef.current.srcObject;
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.stop();
    clearTimeout(timerId);
    setTimerId(null);
  };

  const saveRecording = (blob) => {
    const videoURL = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = videoURL;
    const recording_name = `${new Date().toJSON().slice(0,19)}.mp4`;
    a.download = recording_name;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(videoURL);

    startRecording();
  };

  return (
    <div>
      <div>
        <video ref={videoRef} autoPlay playsInline style={{ width:'119%', maxWidth: '1800px' }} />
        {/* Apply width styles to make the video wider */}
      </div>
      <div>
        {!recording ? (
          <button onClick={startRecording}>Start Recording</button>
        ) : (
          <button onClick={stopRecording}>Stop Recording</button>
        )}
        {recordedChunks.length > 0 && (
          <button onClick={() => saveRecording(new Blob(recordedChunks, { type: 'video/webm' }))}>
            Save Recording
          </button>
        )}
      </div>
    </div>
  );
};

export default WebcamComponent;
