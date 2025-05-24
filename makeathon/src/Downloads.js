// src/Downloads.js
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './App.css';
import appLogo from './assets/summarease.png';
import companyLogo from './assets/creme_brulee.jpg';
import { Link } from 'react-router-dom';
import SearchBar from './SearchBar';


function Downloads() {
  const location = useLocation();
  const [selectedMode, setSelectedMode] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

  // Get files from state if available
  const files = location.state?.files || [];

  const handleProcess = async (mode) => {
    if (!files.length) {
      alert('No files available to process');
      return;
    }

    setSelectedMode(mode);
    setProcessing(true);
    
    try {
      // Process each file
      for (const file of files) {
        const fileType = file.type;
        
        // Process the file based on type and mode
        if (fileType === 'pdf') {
          // PDF files should already be processed in Home.js
          if (!file.processed) {
            throw new Error('PDF file not processed');
          }
        } else if (fileType === 'mp4' || fileType === 'avi' || fileType === 'mov') {
          const formData = new FormData();
          formData.append('file', file);
          formData.append('mode', mode);
          
          const response = await fetch('http://localhost:5000/process-text', {
            method: 'POST',
            body: formData
          });
          
          const result = await response.json();
          
          if (result.error) {
            throw new Error(result.error);
          }
          
          setResult(result.result);
        }
      }

    } catch (error) {
      console.error('Error processing files:', error);
      alert('Error processing files. Please try again.');
    } finally {
      setProcessing(false);
    }
  };

  const processVideo = async (filePath, mode) => {
    // Add video processing logic here
    await new Promise(resolve => setTimeout(resolve, 2000));
  };

// Remove the cleanup useEffect since we don't need it anymore
  // All file handling is now managed by the Python server

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
        
        {processing ? (
          <div className="processing">
            <h2>Processing files...</h2>
            <p>Please wait while we process your files.</p>
          </div>
        ) : selectedMode ? (
          <div className="result">
            <h2>Results:</h2>
            <p>{result}</p>
            <button 
              className="btn eraser pink" 
              onClick={() => setSelectedMode(null)}
            >
              Back to Menu
            </button>
          </div>
        ) : (
          <div className="buttons">
            <button 
              className="btn eraser pink" 
              onClick={() => handleProcess(1)}
              disabled={processing}
            >
              📄 Get Summary
            </button>
            <button 
              className="btn eraser blue" 
              onClick={() => handleProcess(2)}
              disabled={processing}
            >
              ❓ Get QnA
            </button>
            <button 
              className="btn eraser green" 
              onClick={() => handleProcess(3)}
              disabled={processing}
            >
              🧠 Get Quizzes
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default Downloads;
