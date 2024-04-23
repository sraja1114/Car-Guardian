import React, { useEffect, useState } from 'react';

import { fetchGet, fetchPost } from '../../util/fetchHelp.js';

import WebcamComponent from '../../Components/NavBar/Webcam.js';
import './Landing.css';
function Landing() {
  const [getData, setGetData] = useState()
  const [postData, setPostData] = useState()

  useEffect(() =>{
    fetchGet("/default_greet").then(data => {
      setGetData(data.message);
    });

    const postData = {'name': 'Jason'}
    fetchPost("/greet", postData).then(data => {
      setPostData(data.message);
    });

  })

  return (
    <div className="App">
      {(typeof getData === "undefined") ? (
        <p>Loading...</p>
      ): (
        <>
          <p>Data received from our get request:</p>
          <p>{getData}</p>
        </>
      )}
      {(typeof postData === "undefined") ? (
        <p>Loading...</p>
      ): (
        <>
          <p>Data received from our post request:</p>
          <p>{postData}</p>
        </>
      )}
      <WebcamComponent/>
    </div>
  );
}

export default Landing;
