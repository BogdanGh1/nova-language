// src/components/RegisterPage.jsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from "../../api/axios";
import './auth.css';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [verifyPassword, setVerifyPassword] = useState('');
  const navigate = useNavigate();

  const handleRegister = async () => {
    if (password !== verifyPassword) {
      console.error('Passwords do not match');
      return;
    }

    try {
      const response = await axios.post('/users/', { username, password });
      if (response.status === 200) {
        // Handle successful registration here (e.g., redirect to login)
        console.log('Registration successful!');
        navigate('/login');
      } else {
        console.error('Registration failed.');
      }
    } catch (error) {
      console.error('Error during registration:', error);
    }
  };

  const goToLogin = () => {
    navigate('/login');
  };

  return (
    <div className="login-container">
      <div className="card">
        <h2>Register</h2>
        <div className="inputContainer">
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="input"
          />
        </div>
        <div className="inputContainer">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="input"
          />
        </div>
        <div className="inputContainer">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input"
          />
        </div>
        <div className="inputContainer">
          <label>Verify Password:</label>
          <input
            type="password"
            value={verifyPassword}
            onChange={(e) => setVerifyPassword(e.target.value)}
            className="input"
          />
        </div>
        <button onClick={handleRegister} className="button">Register</button>
        <a onClick={goToLogin} className="register-link">Already have an account? Login</a>
      </div>
    </div>
  );
};

export default RegisterPage;
