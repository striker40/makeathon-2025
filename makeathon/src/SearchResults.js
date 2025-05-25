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
  const [sortType, setSortType] = useState('popularity');
  const [clickedItem, setClickedItem] = useState(null);
  const [clickedSort, setClickedSort] = useState(null);

  // Mock data based on our downloads section
  const mockData = [
    {
      id: 1,
      title: 'MIT OOP Q&A',
      user: 'Striker',
      rating: 4.2,
      users: 87,
      type: 'Q&A'
    },
    {
      id: 2,
      title: 'MIT OOP Quiz',
      user: 'Striker',
      rating: 4.8,
      users: 156,
      type: 'Quiz'
    }
  ];

  // Sort functions
  const sortResults = (type) => {
    setSortType(type);
    const sorted = [...mockData];
    switch(type) {
      case 'popularity':
        sorted.sort((a, b) => b.users - a.users);
        break;
      case 'rating':
        sorted.sort((a, b) => b.rating - a.rating);
        break;
      case 'name':
        sorted.sort((a, b) => a.title.localeCompare(b.title));
        break;
      default:
        break;
    }
    setResults(sorted);
  };

  useEffect(() => {
    if (!query) return;
    // For now, we'll use mock data
    setResults(mockData);
  }, [query]);

  return (
    <div className="App">
      <div className="background-logo" style={{ backgroundImage: `url(${companyLogo})` }} />

      <header className="app-header">
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Link to="/" className="logo-link">
            <img src={appLogo} alt="App Logo" className="header-logo" />
          </Link>
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
        <div className="sort-buttons">
          <button 
            className={`sort-btn ${sortType === 'popularity' ? 'active' : ''} ${clickedSort === 'popularity' ? 'clicked' : ''}`}
            onClick={() => {
            sortResults('popularity');
            setClickedSort('popularity');
            setTimeout(() => setClickedSort(null), 300);
          }}
          >
            Sort by Popularity
          </button>
          <button 
            className={`sort-btn ${sortType === 'rating' ? 'active' : ''} ${clickedSort === 'rating' ? 'clicked' : ''}`}
            onClick={() => {
            sortResults('rating');
            setClickedSort('rating');
            setTimeout(() => setClickedSort(null), 300);
          }}
          >
            Sort by Rating
          </button>
          <button 
            className={`sort-btn ${sortType === 'name' ? 'active' : ''} ${clickedSort === 'name' ? 'clicked' : ''}`}
            onClick={() => {
            sortResults('name');
            setClickedSort('name');
            setTimeout(() => setClickedSort(null), 300);
          }}
          >
            Sort by Name
          </button>
        </div>
        <div className="search-results-grid">
          {results.length > 0 ? (
            results.map(item => (
              <div 
                key={item.id} 
                className={`search-result-item ${clickedItem === item.id ? 'clicked' : ''}`} 
                onClick={() => {
                  setClickedItem(item.id);
                  setTimeout(() => setClickedItem(null), 300);
                }}
              >
                <div className="result-header">
                  <h3>{item.title}</h3>
                  <span className="user">👤 {item.user}</span>
                </div>
                <div className="rating-container">
                  <div className="rating">{item.rating.toFixed(1)}★</div>
                  <div className="users">({item.users} users)</div>
                </div>
                <div className="type">📁 {item.type}</div>
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
