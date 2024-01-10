import React, { useState, useEffect } from "react";
import '../styles/userStyles.css'
import clientToken from '../ClientToken';
import axios from "axios";
import getCurrencies from "../functions/getCurrencies";

import { Input, Button, Modal, ModalHeader, ModalBody, ModalFooter, FormFeedback } from 'reactstrap';




function AddNewWallet () {
    const {userId} = clientToken();
    const [currencyId, setCurrencyId] = useState(1);
    const [accNum, setAccNum] = useState();
    const [currencies, setCurrencies] = useState([]);
    const [modal, setModal] = useState(false);
    const [isValid, setValid] = useState(false);

    const toggle = () => setModal(!modal);

    const addWallet = async (event) => {
        try {
          const response = await axios.post("http://localhost:8000/add_new_wallet", {
            user_id: userId(),
            currency_id: currencyId,
            account: accNum,
          });
        } catch (error) {
            console.error(error);
          }
      };

      const getCurrenciesList = async (event) => {
        const currencies = await getCurrencies(event);
        setCurrencies(currencies);
      };

      useEffect((e) => {
        getCurrenciesList(e);
      }, []);

      const isAccNumValid = (e) => {
        if (/^\d+$/.test(e.target.value) && 10 <= e.target.value.length && e.target.value.length <= 26){
            setValid(true)
        } else {
        setValid(false)}
      }

      const isFormValid = () => {
        console.log(currencyId)
        if (isValid)
        {return true;}
        return false;
      }

    return (
        <div className="BLUE_BG">
            <div>
      <Button className="addButton textStyle" onClick={toggle}>
        Dodaj portfel
      </Button>
      <Modal isOpen={modal} toggle={toggle} >
        <ModalHeader toggle={toggle} className="blackTextStyle">
                Dodaj nowy portfel</ModalHeader>
        <ModalBody>
            <div> Wprowadź numer konta
                <Input className="inputStyleAcc" maxLength={26}
                onChange={(e) => {isAccNumValid(e); setAccNum(e.target.value);}}>
                </Input>
            </div>
            <div> Wybierz walutę
            <Input
            className="inputStyle"
            type="select"
            onChange={(e) => {
              setCurrencyId(e.target.value);
            }}
          >
            {currencies?.length &&
              currencies.map((list, index) => (
                <option key={index} value={list[0]}>
                  {list[2]}
                </option>
              ))}{" "}
          </Input>
            </div>
        </ModalBody>
        <ModalFooter>
        <Button
            className="buttonStyleLoginUser whiteTextStyle"
            type="submit"
            onClick={async (e) => {
                addWallet(e); toggle();
            }}
            disabled={!isFormValid()}
          > Dodaj </Button>
          <Button className="cancelButton" onClick={toggle}>
            Anuluj
          </Button>
        </ModalFooter>
      </Modal>
    </div>

        </div>
    )

}

export default AddNewWallet