import React, { useState } from "react";
import CodeEditor from "../../components/CodeEditor";
import LogBoard from "../../components/LogBoard";
import Navbar from "../../components/menu/Navbar";
import TicTacToe from "./TicTacToe";
import axios from "../../api/axios";
import "./ticTacToe.css";
const TicTacToeGame = () => {
  const [code, setCode] = useState("");
  const [logs, setLogs] = useState("");

  const [board, setBoard] = useState(Array(9).fill(null));
  const [scores, setScores] = useState({ X: 0, O: 0 });

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const handleActions = (actions) => {
    for (let action of actions) {
      console.log(action);
      if (action.type == "setCell")
        setBoard((prevBoard) => {
          const newBoard = [...prevBoard];
          newBoard[action.position] = action.value;
          return newBoard;
        });
      else if (action.type == "setScore")
        setScores((prevScores) => {
          const newScores = { ...prevScores };
          newScores[action.player] = action.value;
          return newScores;
        });
      else if (action.type == "printLogs")
        setLogs((prevLogs) => {
          return prevLogs + action.text + "\n";
        });
    }
  };

  const handleRunClick = async () => {
    console.log(code);
    const response = await axios.post(
      "code",
      JSON.stringify({
        code: code,
      }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );
    console.log(response);
    setLogs("");
    handleActions(response.data);
  };

  const handleCellClick = async (index) => {
    console.log(index);
    const response = await axios.get(`tictactoe/${index}`, {
      headers: { "Content-Type": "application/json" },
    });
    console.log(response);
    handleActions(response.data);
  };

  return (
    <>
      <Navbar />
      <div className="container">
        <div className="left-container">
          <TicTacToe
            board={board}
            handleClick={handleCellClick}
            scores={scores}
          />
          <button className="run-button" onClick={handleRunClick}>
            Run
          </button>
          <LogBoard logs={logs} />
        </div>
        <div className="right-container">
          <CodeEditor handleCodeChange={handleCodeChange} />
        </div>
      </div>
    </>
  );
};

export default TicTacToeGame;
