import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

import RegistrationButton from "./components/RegistrationButton";
import LoginButton from "./components/LoginButton";

import Registration from "./views/Registration";
import Home from "./views/Home";
import Login from "./views/Login";
import Logged from "./views/Logged";


function App() {
  return (
    <div className="">
      <Router>
        <div className="flex items-center justify-between p-6">

          <div className="font-bold text-6xl justify-center p-6">
            Kantor
          </div>
          <div className="flex-col p-4">
          <RegistrationButton />
          <LoginButton/>
          </div>
        </div>

        <div className="p-3 justify-center flex">
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route exact path="/rejestracja" element={<Registration />} />
            <Route exact path="/logowanie" element={<Login />} />
            <Route exact path="/zalogowany" element={<Logged />} />
          </Routes>
        </div>

      </Router>
    </div>
  );
}

export default App;
