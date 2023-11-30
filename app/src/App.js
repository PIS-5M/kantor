import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import RegistrationButton from "./components/RegistrationButton";
import Registration from "./views/Registration";
import Home from "./views/Home";

function App() {
  return (
    <div className="">
      <Router>
        <div className="flex items-center justify-between p-6">

          <div className="font-bold text-6xl justify-center p-6">
            Kantor
          </div>

          <RegistrationButton />
        </div>

        <div className="p-3 justify-center flex">
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route exact path="/rejestracja" element={<Registration />} />
          </Routes>
        </div>

      </Router>
    </div>
  );
}

export default App;
