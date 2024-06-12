import React, { useState, useEffect } from "react";
import CodeEditor from "../../components/CodeEditor";
import LogBoard from "../../components/LogBoard";
import Navbar from "../../components/menu/Navbar";
import TicTacToe from "./TicTacToe";
import TicTacToeInfo from "./TicTacToeInfo";
import axios from "../../api/axios";
import "./ticTacToe.css";
const TicTacToePage = ({user}) => {
  const [code, setCode] = useState("");
  const [logs, setLogs] = useState("");
  const [gameId, setGameId] = useState("");

  const [options, setOptions] = useState([]);
  const [selectedOptionId, setSelectedOptionId] = useState("");

  const [board, setBoard] = useState(Array(9).fill(null));
  const [scores, setScores] = useState({ X: 0, O: 0 });

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const response = await axios.get(`/codes/${user.id}/tic-tac-toe`);
        setOptions(response.data);
      } catch (error) {
        console.error("Error fetching options:", error);
      }
    };
    fetchOptions();
  }, []);

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

  const handleChange = (event) => {
    const selectedId = event.target.value;
    setSelectedOptionId(selectedId);
    const selectedOption = options.find((option) => option.id == selectedId);
    console.log(selectedOption.code);
    handleCodeChange(selectedOption.code);
  };

  const handleSaveClick = async () => {
    try {
      if (selectedOptionId == 0) {
        // If no option is selected, create a new code entry
        const response = await axios.post(
          `/codes/${user.id}/tic-tac-toe`,
          { code: code },
          {
            headers: { "Content-Type": "application/json" },
          }
        );
        const newId = response.data;
        console.log("New code saved:", newId);
        // Add the new option to the options state
        setOptions((prevOptions) => [
          ...prevOptions,
          { id: newId, code: code },
        ]);
        // Set the selected option to the new ID
        setSelectedOption(newId);
      } else {
        // If an option is selected, update the existing code entry
        const response = await axios.put(
          `/codes/${user.id}/tic-tac-toe/${selectedOptionId}`,
          { code: code },
          {
            headers: { "Content-Type": "application/json" },
          }
        );
        console.log("Code updated:", response.data.code);
        const selectedOption = options.find((option) => option.id == selectedOptionId);
        selectedOption.code = response.data.code;
      }
    } catch (error) {
      console.error("Error saving code:", error);
    }
  };

  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
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
            <div
              className="button-container"
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "10px",
              }}
            >
              <button className="button" onClick={handleRunClick}>
                Run
              </button>
              <button className="button" onClick={handleSaveClick}>
                Save
              </button>
              <button className="button" onClick={openModal}>
                Info
              </button>
              <select value={selectedOptionId} onChange={handleChange} className="save-select">
                <option value={0}>Select save</option>
                {options.map((option, index) => (
                  <option key={index} value={option.id}>
                    Version {option.id}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="log-container">
            <LogBoard logs={logs} width={"500px"} height={"47vh"} />
          </div>
        </div>
        <div className="right-container">
          <CodeEditor code={code} handleCodeChange={handleCodeChange} />
        </div>
      </div>
      <TicTacToeInfo modal={isModalOpen} setModal={setIsModalOpen} />
    </>
  );
};

export default TicTacToePage;
