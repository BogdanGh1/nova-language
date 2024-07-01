import React, { useState, useEffect } from "react";
import CodeEditor from "../../components/CodeEditor";
import LogBoard from "../../components/LogBoard";
import Navbar from "../../components/menu/Navbar";
import axios from "../../api/axios";
import "./minesweeper.css";
import "../general.css";
import MinesweeperInfo from "./MinesweeperInfo";
import Minesweeper from "./Minesweeper";
const MinesweeperPage = ({user}) => {
  const [code, setCode] = useState("");
  const [logs, setLogs] = useState("");
  const [gameId, setGameId] = useState("");

  const [options, setOptions] = useState([]);
  const [selectedOptionId, setSelectedOptionId] = useState("");

  const [board, setBoard] = useState(Array(20).fill(Array(20).fill(' ')));

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const response = await axios.get(`/codes/${user.id}/minesweeper`);
        response.data.forEach((obj, index) => {
          obj.index = index + 1;
        });
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
    console.log(actions);
    for (let action of actions) {
      if (action.type == "setCell")
        setBoard((prevBoard) => {
          const newBoard = prevBoard.map(innerArray => innerArray.slice());
          newBoard[action.row][action.col] = action.value;
          return newBoard;
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
        game_name: "minesweeper",
      }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    if (typeof response.data !== "string") {
      setBoard(Array(20).fill(Array(20).fill(' ')));
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
      setBoard(Array(20).fill(Array(20).fill(' ')));
      setLogs(response.data.error);
      return;
    }
    setLogs("");
    setBoard(Array(20).fill(Array(20).fill(' ')));
    handleActions(response.data);
  };
  const handleLeftClick = async (row, col) => {
    console.log(`Left click at (${row}, ${col})`);
    const response = await axios.patch(
      `games/${gameId}`,
      JSON.stringify({
        event_name: "leftClickCell",
        parameters: [row, col],
      }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );
    console.log(response);
    handleActions(response.data);
  };

  const handleRightClick = async (row, col) => {
    console.log(`Right click at (${row}, ${col})`);
    const response = await axios.patch(
      `games/${gameId}`,
      JSON.stringify({
        event_name: "rightClickCell",
        parameters: [row, col],
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
          `/codes/${user.id}/minesweeper`,
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
          `/codes/${user.id}/minesweeper/${selectedOptionId}`,
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
          <div className="ms-container">
            <Minesweeper
              board={board}
              handleLeftClick={handleLeftClick}
              handleRightClick={handleRightClick} 
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
                    Version {option.index}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="ms-logs">
            <LogBoard logs={logs} width={"550px"} height={"34vh"} />
          </div>
        </div>
        <div className="main">
          <CodeEditor code={code} handleCodeChange={handleCodeChange} />
        </div>
      </div>
      <MinesweeperInfo modal={isModalOpen} setModal={setIsModalOpen} />
    </>
  );
};

export default MinesweeperPage;
