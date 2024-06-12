import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import { useState } from "react";
import MinesweeperPage from "./pages/minesweeper/MinesweeperPage";
import SortingVisualizerPage from "./pages/sorting_visualizer/SortingVisualizerPage";
import TicTacToePage from "./pages/ticTacToe/TicTacToePage";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
function App() {
  const [user, setUser] = useState(null);
  return (
    <Router>
      <main className="App">
        <Routes>
          {/* <Route path="*" element={<LandingPage />} /> */}
          <Route
            path="/register"
            element={<RegisterPage/>}
          />
          <Route
            path="/login"
            element={<LoginPage setUser={setUser}/>}
          /> 
          <Route path="/tic-tac-toe" element={<TicTacToePage user={user}/>} />
          <Route path="/minesweeper" element={<MinesweeperPage />} /> 
          <Route path="/sorting-visualizer" element={<SortingVisualizerPage />} />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
