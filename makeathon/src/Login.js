// src/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import appLogo from './assets/summarease.png';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    // Dummy auth (replace with API call later)
    if (username && password) {
      localStorage.setItem('user', username);
      navigate('/'); 
    } else {
      alert('Please enter both username and password!');
    }
  };

  return (
    <div className="login-container">
      <img src={appLogo} alt="App Logo" className="login-logo" />
      <h1 className="login-title">Welcome to Summarease</h1>
      <form className="login-form" onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="👧 Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="login-input"
        />
        <input
          type="password"
          placeholder="🔑 Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="login-input"
        />
        <button type="submit" className="login-button">Let’s Go!</button>
      </form>
    </div>
  );
}

export default Login;
