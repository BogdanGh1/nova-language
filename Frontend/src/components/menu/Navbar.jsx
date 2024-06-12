import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="game-selector">
        <Link to="/tic-tac-toe" className="link">
          Tic Tac Toe
        </Link>
        <Link to="/minesweeper" className="link">
          Minesweeper
        </Link>
        <Link to="/sorting-visualizer" className="link">
          Sorting Visualizer
        </Link>
      </div>
      <Link to="/login" className="link auth-buttons">
        Logout
      </Link>
    </nav>
  );
};

export default Navbar;
