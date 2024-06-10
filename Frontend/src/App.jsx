import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TicTacToePage from "./pages/ticTacToe/TicTacToePage";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
function App() {
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
            element={<LoginPage />}
          /> 
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
