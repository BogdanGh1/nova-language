import React, { useState } from "react";
import CodeEditor from "../../components/CodeEditor";
import LogBoard from "../../components/LogBoard";
import Navbar from "../../components/menu/Navbar";
import TicTacToe from "./TicTacToe";
import TicTacToeInfo from "./TicTacToeInfo"
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
      if (action.type == "setCell")
        setBoard((prevBoard) => {
          const newBoard = [...prevBoard];
          newBoard[action.index] = action.value;
          return newBoard;
        });
      else if (action.type == "setScoreX")
        setScores((prevScores) => {
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

    if (typeof response.data !== "string") {
      setBoard(Array(9).fill(null));
      setLogs(response.data.error);
      return;
    }
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
    console.log(response.data);
    if ("error" in response.data) {
      setBoard(Array(9).fill(null));
      setLogs(response.data.error);
      return;
    }
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
  const [selectedOption, setSelectedOption] = useState(''); // Initialize state for selected option

  const handleChange = (event) => {
    setSelectedOption(event.target.value); // Update selected option state
  };
  const options = ['Option 1', 'Option 2', 'Option 3']; // List of options

  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <Navbar />
      <div className="container">
        <div className="left-container">
          <div className="game-container">
          <TicTacToe
            board={board}
            handleClick={handleCellClick}
            scores={scores}
          />
          <div className="button-container" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
            <button className="button" onClick={handleRunClick}>
              Run
            </button>
            <button className="button" onClick={handleRunClick}>
              Save
            </button>
            <button className="button" onClick={openModal}>
              Info
            </button>
            <select value={selectedOption} onChange={handleChange}>
              <option value="">Select an option...</option>
              {options.map((option, index) => (
                <option key={index} value={option}>{option}</option>
              ))}
            </select>
          </div>
          </div>
          <div className="log-container">
            <LogBoard 
            logs={logs} 
             width={"500px"}
             height={"47vh"}/>
          </div>
        </div>
        <div className="right-container">
          <CodeEditor handleCodeChange={handleCodeChange} />
        </div>
      </div>
      <TicTacToeInfo modal={isModalOpen} setModal={setIsModalOpen}/>
    </>
  );
};

export default TicTacToePage;
