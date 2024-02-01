import React, { useState } from "react";
import "./TicTacToe.css";

function TicTacToe({ board, handleClick, scores }) {
  const renderSquare = (i) => (
    <button className="square" onClick={() => handleClick(i)}>
      {board[i]}
    </button>
  );
  let status = `Score - X: ${scores.X}, O: ${scores.O}`;

  return (
    <div>
      <div className="status">{status}</div>
      <div className="board-row">
        {renderSquare(0)}
        {renderSquare(1)}
        {renderSquare(2)}
      </div>
      <div className="board-row">
        {renderSquare(3)}
        {renderSquare(4)}
        {renderSquare(5)}
      </div>
      <div className="board-row">
        {renderSquare(6)}
        {renderSquare(7)}
        {renderSquare(8)}
      </div>
    </div>
  );
}

export default TicTacToe;
