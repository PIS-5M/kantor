import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { Col, Row } from "reactstrap";

import Header from "./components/Header";
import Sidebar from "./components/Sidebar";

import Registration from "./views/Registration";
import Home from "./views/Home";
import Login from "./views/Login";

import "./styles/headerStyles.css";
import clientToken from "./ClientToken";
import { TransactionsHistory } from "./views/TransactionsHistory";
import { MyOffers } from "./views/MyOffers";
import { Toaster } from "react-hot-toast";
import { CreateOffer } from "./views/CreateOffer";
// import { CreateOfferForm } from "./components/CreateOfferForm";
import { AllOffers } from "./views/AllOffers";
import UserProfile from "./views/UserProfile";
// import AddNewWallet from "./components/AddNewWallet";


function App() {
  const { userId } = clientToken();
  return (
    <div className="font-sans">
      <Toaster />
      <Router>
        <Header />
        <Row className="wid">
          <Col xs="3">{userId() && <Sidebar />}</Col>
          <Col xs={userId() ? "8" : "0"} className="colStyle">
            <Routes>
              <Route exact path="/" element={<Home />} />
              <Route exact path="/rejestracja" element={<Registration />} />
              <Route exact path="/logowanie" element={<Login />} />
              <Route
                exact
                path="/moje_transakcje"
                element={<TransactionsHistory />}
              />
              <Route exact path="/moje_oferty" element={<MyOffers />} />
              <Route exact path="/dodaj" element={<CreateOffer />} />
              {/* <Route exact path="/dodaj" element={<CreateOfferForm />} /> */}
              <Route exact path="/oferty" element={<AllOffers />} />
              <Route exact path="/profil" element={<UserProfile />} />
             {/*} <Route exact path="/dodaj_portfel" element={<AddNewWallet />} />*/}

            </Routes>
          </Col>
        </Row>
      </Router>
    </div>
  );
}

export default App;
