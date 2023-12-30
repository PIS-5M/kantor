import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

import Header from "./components/Header";

import Registration from "./views/Registration";
import Home from "./views/Home";
import Login from "./views/Login";
import Logged from "./views/Logged";


function App() {
  return (
    <div className="">
      <Router>
        <Header />
        <div>
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
