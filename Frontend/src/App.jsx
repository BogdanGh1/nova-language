import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TicTacToeGame from "./pages/ticTacToe/TicTacToeGame";
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
          <Route path="/game" element={<TicTacToeGame />} />
          <Route path="/code" element={<CodeEditor />} />
          <Route path="/tic" element={<TicTacToe />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
