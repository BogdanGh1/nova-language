import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from "../../api/axios";
import './auth.css';

const LoginPage = ({setUser}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post('/users/login', { username, password });
      if (response.status === 200) {
        console.log(response.data);
        setUser(response.data);
        navigate('/tic-tac-toe');
      } else {
        console.error('Login failed.');
      }
    } catch (error) {
      console.error('Error during login:', error);
    }
  };

  const goToRegister = () => {
    navigate('/register');
  };

  return (
    <div className="login-container">
      <div className="card">
        <h2>Login</h2>
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
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input"
          />
        </div>
        <button onClick={handleLogin} className="button">Login</button>
        <a onClick={goToRegister} className="register-link">Don't have an account? Register</a>
      </div>
    </div>
  );
};

export default LoginPage;
