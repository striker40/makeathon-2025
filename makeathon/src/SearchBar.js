// src/SearchBar.js
import React from 'react';
import './SearchBar.css';

function SearchBar() {
  return (
    <input
      type="text"
      className="search-bar"
      placeholder="🔍 Search by keyword"
    />
  );
}

export default SearchBar;
