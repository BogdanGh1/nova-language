import React, { useState } from "react";
import CodeEditor from "../../components/CodeEditor";
import LogBoard from "../../components/LogBoard";
import Navbar from "../../components/menu/Navbar";
import TicTacToe from "./TicTacToe";
import axios from "../../api/axios";
import "./ticTacToe.css";
const TicTacToeGame = () => {
  const [code, setCode] = useState(""); // State to store the current code

  const handleCodeChange = (newCode) => {
    setCode(newCode);
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
  };

  return (
    <>
      <Navbar />
      <div className="container">
        <div className="left-container">
          <TicTacToe />
          <button className="run-button" onClick={handleRunClick}>
            Run
          </button>
          <LogBoard />
        </div>
        <div className="right-container">
          <CodeEditor handleCodeChange={handleCodeChange} />
        </div>
      </div>
    </>
  );
};

export default TicTacToeGame;
