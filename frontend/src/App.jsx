import { BrowserRouter, Routes, Route } from "react-router-dom";
import Auth from "./Auth";
import Dashboard from "./Dashbord";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Auth />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
