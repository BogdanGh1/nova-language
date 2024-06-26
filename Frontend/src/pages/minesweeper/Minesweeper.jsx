import React from "react";
import flagImage from './assets/flag.png';
import "./minesweeper.css";

const Cell = ({ value, id, onLeftClick, onRightClick }) => {
  const handleContextMenu = (e) => {
    e.preventDefault();
    onRightClick();
  };

  const backgroundImage = value === '-1' ? `url(${flagImage})`: '';
  if (value === '-1'){
    value = ' ';
  }

  return (
    <div
      className="cell"
      id={id}
      onClick={onLeftClick}
      onContextMenu={handleContextMenu}
      style={{ backgroundImage, backgroundSize: 'cover' }}
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
              id={rowIndex*20+colIndex}
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
