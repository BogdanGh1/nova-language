import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TicTacToePage from "./pages/ticTacToe/TicTacToePage";
import CodeEditor from "./components/CodeEditor";
import TicTacToe from "./pages/ticTacToe/TicTacToe";
function App() {
  return (
    <Router>
      <main className="App">
        <Routes>
          {/* <Route path="*" element={<LandingPage />} /> */}
          {/* <Route
            path="/register"
            element={<Register userData={userData} setUserData={setUserData} />}
          />
          <Route
            path="/login"
            element={<Login userData={userData} setUserData={setUserData} />}
          /> */}
          <Route path="/tic-tac-toe" element={<TicTacToePage />} />
          {/* <Route path="/minesweeper" element={<MinesweeperPage />} /> */}
          {/* <Route path="/sorting-visualizer" element={<SortingVisualizerPage />} /> */}
          <Route path="/" element={<TicTacToePage />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
