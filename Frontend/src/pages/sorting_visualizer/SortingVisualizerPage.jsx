import React, { useState, useEffect } from "react";
import CodeEditor from "../../components/CodeEditor";
import LogBoard from "../../components/LogBoard";
import Navbar from "../../components/menu/Navbar";
import SortingVisualizer from "./SortingVisualizer";
import TicTacToeInfo from "./SortingVisualizerInfo";
import axios from "../../api/axios";
import "./sortingVisualizer.css";
import "../general.css";

const SortingVisualizerPage = ({user}) => {
  const [code, setCode] = useState("");
  const [logs, setLogs] = useState("");
  const [gameId, setGameId] = useState("");

  const [options, setOptions] = useState([]);
  const [selectedOptionId, setSelectedOptionId] = useState("");

  const [bars, setBars] = useState([]);
  const [swappedIndices, setSwappedIndices] = useState([]);

  useEffect(() => {
    resetBars();
  }, []);

  const resetBars = () => {
    const newBars = Array.from({ length: 10 }, () => Math.floor(Math.random() * 10) + 1);
    setBars((prevBars) => {
      return newBars;
    });
    setSwappedIndices([]);
    console.log(newBars);
  };

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const response = await axios.get(`/codes/${user.id}/sorting-visualizer`);
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

  const handleActions = async (actions) => {
    let array = [...bars];
    for (let action of actions) {
      if (action.type == "print")
        setLogs((prevLogs) => {
          return prevLogs + action.text + "\n";
        });
      else if(action.type == "swap"){
          let i = action.i1;
          let j = action.i2;
          let time = action.time;
          
          let temp = array[i];
          array[i] = array[j];
          array[j] = temp;
          setSwappedIndices([i,j]);
          await new Promise(resolve => setTimeout(resolve, time)); // Add delay for visualization
          setSwappedIndices([]);
          setBars((prevBars) => {
            return array;
          });
          setSwappedIndices([i,j]);
          await new Promise(resolve => setTimeout(resolve, time)); // Add delay for visualization
          setSwappedIndices([]);
      }
      else if(action.type == "setValue"){
          let index = action.index;
          let value = action.value;
          let time = action.time;
          
          array[index] = value;
          setSwappedIndices([index]);
          await new Promise(resolve => setTimeout(resolve, time)); // Add delay for visualization
          setSwappedIndices([]);
          setBars((prevBars) => {
            return array;
          });
      }
    }
  };

  const handleRunClick = async () => {
    let response = await axios.post(
      "games",
      JSON.stringify({
        code: code,
        username: "user",
        game_name: "sorting-visualizer",
      }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    if (typeof response.data !== "string") {
      setLogs(response.data.error);
      return;
    }
    let gameId = response.data;
    setGameId((prevGameId) => {
      return gameId;
    });
    setLogs("");
  };

  const handleStartSortingClick = async () => {
    if (gameId !== ""){
      console.log(bars);
      let response = await axios.patch(
        `games/${gameId}/add-array`,
        JSON.stringify({
          name: "array",
          values: bars
        }),
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      response = await axios.patch(
        `games/${gameId}`,
        JSON.stringify({
          event_name: "sort",
        }),
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      console.log(response);
      await handleActions(response.data);
    } 
  }

  const handleChange = (event) => {
    const selectedId = event.target.value;
    setSelectedOptionId(selectedId);
    const selectedOption = options.find((option) => option.id == selectedId);
    // console.log(selectedOption.code);
    handleCodeChange(selectedOption.code);
  };

  const handleSaveClick = async () => {
    try {
      if (selectedOptionId == 0) {
        // If no option is selected, create a new code entry
        const response = await axios.post(
          `/codes/${user.id}/sorting-visualizer`,
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
          `/codes/${user.id}/sorting-visualizer/${selectedOptionId}`,
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
          <div className="sv-game-container">
            <SortingVisualizer 
              bars={bars} 
              swappedIndices={swappedIndices} 
              resetBars={resetBars}
              handleSort={handleStartSortingClick}
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
          <div className="sv-log-container">
            <LogBoard logs={logs} width={"550px"} height={"47vh"} />
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

export default SortingVisualizerPage;
