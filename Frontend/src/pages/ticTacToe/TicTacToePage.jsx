import React, { useState } from "react";
import CodeEditor from "../../components/CodeEditor";
import LogBoard from "../../components/LogBoard";
import Navbar from "../../components/menu/Navbar";
import TicTacToe from "./TicTacToe";
import axios from "../../api/axios";
import "./ticTacToe.css";
const TicTacToePage = () => {
  const [code, setCode] = useState("");
  const [logs, setLogs] = useState("");
  const [gameId, setGameId] = useState("");

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
          newBoard[action.index] = action.value;
          return newBoard;
        });
      else if (action.type == "setScoreX")
        setScores((prevScores) => {
          console.log(action);
          const newScores = { ...prevScores };
          newScores["X"] = action.value;
          return newScores;
        });
      else if (action.type == "setScoreO")
        setScores((prevScores) => {
          const newScores = { ...prevScores };
          newScores["O"] = action.value;
          return newScores;
        });
      else if (action.type == "print")
        setLogs((prevLogs) => {
          return prevLogs + action.text + "\n";
        });
    }
  };

  const handleRunClick = async () => {
    console.log(code);
    let response = await axios.post(
      "games",
      JSON.stringify({
        code: code,
        username: "user",
        game_name: "tictactoe",
      }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );
    console.log(response);
    let gameId = response.data;
    setGameId((prevGameId) => {
      return gameId;
    });

    response = await axios.patch(
      `games/${gameId}`,
      JSON.stringify({
        event_name: "start",
      }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );
    console.log(response);
    setLogs("");
    setBoard(Array(9).fill(null));
    handleActions(response.data);
  };

  const handleCellClick = async (index) => {
    console.log(index);
    const response = await axios.patch(
      `games/${gameId}`,
      JSON.stringify({
        event_name: "clickCell",
        parameters: [index],
      }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );
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

export default TicTacToePage;
