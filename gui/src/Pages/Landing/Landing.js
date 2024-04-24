import React from 'react';


import ButtonList from '../../Components/ButtonList/ButtonList.js';
import WebcamComponent from '../../Components/Webcam/Webcam.js';
import './Landing.css';
function Landing() {
  // const [getData, setGetData] = useState()
  // const [postData, setPostData] = useState()

  // useEffect(() =>{
  //   fetchGet("/default_greet").then(data => {
  //     setGetData(data.message);
  //   });

  //   const postData = {'name': 'Jason'}
  //   fetchPost("/greet", postData).then(data => {
  //     setPostData(data.message);
  //   });

  // })

  return (
    <div className="App">
      {/* {(typeof getData === "undefined") ? (
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
      )} */}
      <div className='WebcamContainer'>
        <WebcamComponent/>
        <ButtonList/>
      </div>
      
    </div>
  );
}

export default Landing;
