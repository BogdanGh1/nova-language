import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Game from "./pages/Game";
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
          <Route path="/game" element={<Game />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
