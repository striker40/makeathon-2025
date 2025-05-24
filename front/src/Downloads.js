// src/Downloads.js
import React from 'react';
import './App.css';
import appLogo from './assets/summarease.png';
import companyLogo from './assets/creme_brulee.jpg';
import { Link } from 'react-router-dom';
import SearchBar from './SearchBar';


function Downloads() {
  return (
    <div className="App">
      <div className="background-logo" style={{ backgroundImage: `url(${companyLogo})` }} />

		<header className="app-header">
		  <div style={{ display: 'flex', alignItems: 'center' }}>
			<img src={appLogo} alt="App Logo" className="header-logo" />
			<SearchBar />
		  </div>
		  <nav className="nav-menu">
			<Link to="/" className="nav-item">Home</Link>
			<Link to="/downloads" className="nav-item">Downloads</Link>
			<Link to="/history" className="nav-item">User History</Link>
		  </nav>
		</header>


      <main className="content">
        <h1>Here are some things you can download to help:</h1>
        <div className="buttons">
          <button className="btn eraser pink">📄 Click here to get your Summary</button>
          <button className="btn eraser blue">❓ Click here to get your QnA</button>
          <button className="btn eraser green">🧠 Click here to get Quizzes</button>
        </div>
      </main>
    </div>
  );
}

export default Downloads;
