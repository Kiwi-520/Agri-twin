import { Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Simulation from "./pages/Simulation";
import Explanation from "./pages/Explanation";
import '../styles/theme.css'

function App() {
  return (
    <div className="app">
      <header className="header">
        <h1>🌾 Agri‑Twin</h1>
        <nav>
          <Link to="/">Dashboard</Link>
          <Link to="/simulation">Simulation</Link>

        </nav>
      </header>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/simulation" element={<Simulation />} />
      </Routes>
    </div>
  );
}

export default App;
