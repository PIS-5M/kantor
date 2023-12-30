import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

import {
  Col,
  Row,
} from "reactstrap";

import Header from "./components/Header";
import Sidebar from "./components/Sidebar";

import Registration from "./views/Registration";
import Home from "./views/Home";
import Login from "./views/Login";

import './styles/headerStyles.css'
import clientToken from "./ClientToken";


function App() {
  const {userId} = clientToken();
  return (
    <div className="">
      <Router>
            <Header />
            <Row className="wid">
              {userId() &&
            <Col xs="3">
              <Sidebar />
              </Col>}
            <Col xs="8" className="colStyle">
        <div>
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route exact path="/rejestracja" element={<Registration />} />
            <Route exact path="/logowanie" element={<Login />} />
          </Routes>
        </div>
        </Col>
        </Row>
      </Router>
    </div>
  );
}

export default App;
