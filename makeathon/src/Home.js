// src/Home.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
import appLogo from './assets/summarease.png';
import companyLogo from './assets/creme_brulee.jpg';
import { Link } from 'react-router-dom';
import SearchBar from './SearchBar';

function Home() {
  const navigate = useNavigate();
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [dragOver, setDragOver] = useState(false);

  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles(prev => [...prev, ...files]);
  };

  const handleSubmit = () => {
    if (selectedFiles.length === 0) return;
    
    // Clear the selected files after submission
    setSelectedFiles([]);
    
    // You can add any additional submission logic here
    alert('Files submitted successfully!');
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragOver(false);
    const files = Array.from(event.dataTransfer.files);
    setSelectedFiles(prev => [...prev, ...files]);
  };

  const handlePDFClick = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf';
    input.multiple = true;
    input.onchange = handleFileSelect;
    input.click();
  };

  const handleVideoClick = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'video/*';
    input.multiple = true;
    input.onchange = handleFileSelect;
    input.click();
  };




  // Helper functions for file processing


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
        <h1>Welcome to Summarease</h1>
        <div 
          className={`drop-zone ${dragOver ? 'drag-over' : ''}`} 
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="buttons">
            <button 
              className="btn eraser pink" 
              onClick={handlePDFClick}
            >
              📝 Add PDF Files
            </button>
            <button 
              className="btn eraser blue" 
              onClick={handleVideoClick}
            >
              🎥 Add Video Files
            </button>
          </div>
          {selectedFiles.length > 0 && (
            <div className="selected-files">
              <h3>Selected Files:</h3>
              <ul>
                {selectedFiles.map((file, index) => (
                  <li key={index}>
                    {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                  </li>
                ))}
              </ul>
              <button 
                className="submit-button" 
                onClick={handleSubmit}
                disabled={selectedFiles.length === 0}
              >
                🚀 Submit Files
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default Home;
