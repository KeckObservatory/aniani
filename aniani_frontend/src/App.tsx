import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './helpful_css.css'

import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import About from './pages/About.tsx';
import Home from './pages/Home';
import PredictedReflecivity from './pages/PredictedReflectivity.tsx'

function App() {

  return (
    <Router>
      <div>
        <h1 className="left-align">aniani application</h1>
        <nav>
        <p>Directory</p>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
            <Link to="/About">About</Link>
            </li>
            <li>
              <Link to="/getPredictReflectivity">Predicted Reflectivity</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/About" element={<About />} />
          <Route path="/getPredictReflectivity" element={<PredictedReflecivity />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App
