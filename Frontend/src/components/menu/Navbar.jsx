import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="game-selector">
        <Link to="/tic-tac-toe" className="link">Tic Tac Toe</Link>
        <Link to="/tic-tac-toe" className="link">Minesweeper</Link>
        <Link to="/tic-tac-toe" className="link">Sorting Visualizer</Link>
      </div>
      <div className="auth-buttons">
        <span className="link">Login</span>
        <span className="link">Logout</span>
      </div>
    </nav>
  );
};

export default Navbar;
