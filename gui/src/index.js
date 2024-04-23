import React from "react";
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import NavigationBar from "./Components/NavBar/NavBar";
import "./index.css";
import Landing from "./Pages/Landing/Landing";

const App = () => {
  return (
    <div>
      <NavigationBar />
      <Routes>
        <Route path="/" element={<Landing />} />
      </Routes>
    </div>
  );
};



// Use createRoot instead of ReactDOM.render
const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <Router>
    <App />
  </Router>
);
