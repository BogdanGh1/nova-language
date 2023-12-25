import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="game-selector">
        <div>Games</div>
        <div className="games-dropdown">
          <div>Tic Tac Toe</div>
          <div>Minesweeper</div>
        </div>
      </div>
      <div className="auth-buttons">
        <button>Login</button>
        <button>Logout</button>
      </div>
    </nav>
  );
};

export default Navbar;
