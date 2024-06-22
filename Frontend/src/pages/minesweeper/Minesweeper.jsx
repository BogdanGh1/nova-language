import React from "react";
import "./minesweeper.css";

const Cell = ({ value, onLeftClick, onRightClick }) => {
  const handleContextMenu = (e) => {
    e.preventDefault();
    onRightClick();
  };

  return (
    <div
      className="cell"
      onClick={onLeftClick}
      onContextMenu={handleContextMenu}
    >
      {value}
    </div>
  );
};

const Minesweeper = ({ board, handleLeftClick, handleRightClick }) => {
  return (
    <div className="board">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="row">
          {row.map((cell, colIndex) => (
            <Cell
              key={colIndex}
              value={cell}
              onLeftClick={() => handleLeftClick(rowIndex, colIndex)}
              onRightClick={() => handleRightClick(rowIndex, colIndex)}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default Minesweeper;
