import React, { useState } from 'react';
import './App.css';
import appLogo from './assets/summarease.png';
import companyLogo from './assets/creme_brulee.jpg';
import { Link } from 'react-router-dom';
import SearchBar from './SearchBar';

function StarRating({ rating, onRate }) {
  // rating: number 0-5, onRate: function to set rating
  return (
    <div className="star-rating">
      {[1, 2, 3, 4, 5].map(star => (
        <span
          key={star}
          className={star <= rating ? 'star filled' : 'star'}
          onClick={() => onRate(star)}
          role="button"
          aria-label={`${star} star`}
          tabIndex={0}
          onKeyDown={e => { if(e.key === 'Enter') onRate(star); }}
        >
          ★
        </span>
      ))}
    </div>
  );
}

function UserHistory() {
  const initialHistory = [
    { id: 1, title: 'Summary - Relational Algebra', type: 'Summary', rating: 0 },
    { id: 2, title: 'QnA - MIT OOP', type: 'QnA', rating: 0 },
    { id: 3, title: 'Quiz - MIT OOP', type: 'Quiz', rating: 0 },
  ];

  const [historyItems, setHistoryItems] = useState(initialHistory);

  function handleRate(id, rating) {
    setHistoryItems(items =>
      items.map(item =>
        item.id === id ? { ...item, rating } : item
      )
    );
  }

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
        <h1>Your Previous Downloads</h1>
        <div className="post-it-grid">
          {historyItems.map(item => (
            <div key={item.id} className="post-it">
              <strong>{item.title}</strong>
              <br />
              <small>📁 {item.type}</small>
              <StarRating
                rating={item.rating}
                onRate={rating => handleRate(item.id, rating)}
              />
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default UserHistory;