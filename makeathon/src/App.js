// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import UserHistory from './UserHistory';
import Downloads from './Downloads';

function App() {
  return (
    <Router>
		<Routes>
		  <Route path="/" element={<Home />} />
		  <Route path="/downloads" element={<Downloads />} />
		  <Route path="/history" element={<UserHistory />} />
		</Routes>
    </Router>
  );
}

export default App;
