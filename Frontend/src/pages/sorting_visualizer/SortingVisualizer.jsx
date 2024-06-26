import React, { useState, useEffect } from "react";
import "./sortingVisualizer.css";

function SortingVisualizer({ board, handleClick, scores }) {
  const [bars, setBars] = useState([]);

  useEffect(() => {
    resetBars();
  }, []);

  const resetBars = () => {
    const newBars = Array.from({ length: 10 }, () => Math.floor(Math.random() * 10) + 1);
    setBars(newBars);
  };

  const bubbleSort = async () => {
    let array = [...bars];
    let n = array.length;
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n - i - 1; j++) {
        if (array[j] > array[j + 1]) {
          let temp = array[j];
          array[j] = array[j + 1];
          array[j + 1] = temp;
          setBars([...array]);
          await new Promise(resolve => setTimeout(resolve, 200)); // Add delay for visualization
        }
      }
    }
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h1>Sorting Visualizer</h1>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-end', height: '200px' }}>
        {bars.map((height, idx) => (
          <div
            key={idx}
            style={{
              width: '30px',
              height: `${height * 20}px`,
              backgroundColor: 'turquoise',
              margin: '0 5px',
              transition: 'height 0.2s ease'
            }}
          />
        ))}
      </div>
      <button onClick={resetBars} style={{ margin: '20px', padding: '10px 20px' }}>Reset Bars</button>
      <button onClick={bubbleSort} style={{ margin: '20px', padding: '10px 20px' }}>Start Sorting</button>
    </div>
  );
}

export default SortingVisualizer;
