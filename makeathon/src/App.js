// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import UserHistory from './UserHistory';
import Downloads from './Downloads';
import SearchResults from './SearchResults';
import Login from './Login';


function App() {
  return (
    <Router>
		<Routes>
			<Route path="/login" element={<Login />} />
			<Route path="/" element={<Home />} />
			<Route path="/downloads" element={<Downloads />} />
			<Route path="/history" element={<UserHistory />} />
			<Route path="/search" element={<SearchResults />} />
		</Routes>
    </Router>
  );
}

export default App;
