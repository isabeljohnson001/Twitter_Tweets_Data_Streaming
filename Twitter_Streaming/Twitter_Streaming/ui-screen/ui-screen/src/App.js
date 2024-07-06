import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Tweets from './pages/Tweets';
import './App.css';

function App() {
    const [data, setData] = useState(null);

    return (
      <BrowserRouter>
      <Routes>
          <Route path="/" element={<Home />}>
              <Route path="tweets/:searchTerm" element={<Tweets />} />
          </Route>
      </Routes>
  </BrowserRouter>
    );
}

export default App;
