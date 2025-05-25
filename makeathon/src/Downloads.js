// src/Downloads.js
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import './App.css';
import appLogo from './assets/summarease.png';
import companyLogo from './assets/creme_brulee.jpg';
import { Link } from 'react-router-dom';
import SearchBar from './SearchBar';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import rehypeHighlight from 'rehype-highlight';
import { summaryContent } from './summaryContent';
import { qnaContent } from './qnaContent';
import { quizContent } from './quizContent';


function Downloads() {
  const location = useLocation();
  const [selectedMode, setSelectedMode] = useState(null);
  const [markdownContent, setMarkdownContent] = useState(null);

  const handleProcess = (mode) => {
    setSelectedMode(mode);
    
    // For summary mode, display hardcoded summary content
    if (mode === 1) {
      setMarkdownContent(summaryContent);
    } else if (mode === 2) {
      setMarkdownContent(qnaContent);
    } else {
      // For quiz mode, display hardcoded quiz content
      setMarkdownContent(quizContent);
    }
  };

  return (
    <div className="App">
      <div className="background-logo" style={{ backgroundImage: `url(${companyLogo})` }} />
      <div className="app-header">
        <img src={appLogo} alt="Summarease" className="header-logo" />
        <nav className="nav-menu">
          <Link to="/" className="nav-item">Home</Link>
          <Link to="/downloads" className="nav-item">Downloads</Link>
          <Link to="/history" className="nav-item">History</Link>
        </nav>
      </div>
      
      <div className="content">
        <h1>Choose a service from below</h1>
        
        <div className="buttons">
          <button className="btn eraser pink" onClick={() => handleProcess(1)}>Get Summary</button>
          <button className="btn eraser green" onClick={() => handleProcess(2)}>Get Q&A</button>
          <button className="btn eraser blue" onClick={() => handleProcess(3)}>Get Quiz</button>
        </div>

        <div className="services-section">
          <div className="service-display">
            {selectedMode && markdownContent && (
              <>
                <div className="service-header">
                  <h2>{selectedMode === 1 ? 'Summary' : selectedMode === 2 ? 'Q&A' : 'Quiz'}</h2>
                  <button className="btn eraser close" onClick={() => setSelectedMode(null)}>Close</button>
                </div>
                <div className="markdown-container">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeRaw, rehypeHighlight]}
                    components={{
                      p: ({ children }) => <p className="markdown-content">{children}</p>,
                      h1: ({ children }) => <h1 className="markdown-content">{children}</h1>,
                      h2: ({ children }) => <h2 className="markdown-content">{children}</h2>,
                      h3: ({ children }) => <h3 className="markdown-content">{children}</h3>,
                      ul: ({ children }) => <ul className="markdown-content">{children}</ul>,
                      ol: ({ children }) => <ol className="markdown-content">{children}</ol>,
                      li: ({ children }) => <li className="markdown-content">{children}</li>
                    }}
                  >
                    {markdownContent}
                  </ReactMarkdown>
                  <button className="submit-button">Submit Files</button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Downloads;
