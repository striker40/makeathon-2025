// src/SearchResults.js
import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import appLogo from './assets/summarease.png';
import companyLogo from './assets/creme_brulee.jpg';
import SearchBar from './SearchBar';


function SearchResults() {
  const location = useLocation();
  const query = new URLSearchParams(location.search).get("q");
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (!query) return;
    fetch(`http://localhost:5000/api/search?q=${query}`)
      .then(res => res.json())
      .then(data => setResults(data))
      .catch(err => console.error("Search failed:", err));
  }, [query]);

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
        <h1>Search Results for: <em>{query}</em></h1>
        <div className="post-it-grid">
          {results.length > 0 ? (
            results.map(item => (
              <div key={item.id} className="post-it">
                <strong>{item.title}</strong>
                <br />
                <small>📁 {item.type}</small>
              </div>
            ))
          ) : (
            <p>No results found.</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default SearchResults;
