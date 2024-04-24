import React, { useEffect, useRef } from "react";
import ButtonList from "../ButtonList/ButtonList";
import './Webcam.css';
const WebcamComponent = () => {
  const videoRef = useRef(null);
  

  useEffect(() => {
    const constraints = { video: true, audio: true };

    const handleSuccess = (stream) => {
      videoRef.current.srcObject = stream;
    };

    const handleError = (error) => {
      console.error("Error accessing webcam:", error);
    };

    navigator.mediaDevices
      .getUserMedia(constraints)
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

  

  return (
    <div className="bigContainer">
      <div className="NewButtonContainer">
        <ButtonList videoRef={videoRef}/>
      </div>
      <div>
        <video ref={videoRef} autoPlay playsInline style={{ width:'110%',marginTop:'35px'}} />
        {/* Apply width styles to make the video wider */}
      </div>
    </div>
  );
};

export default WebcamComponent;