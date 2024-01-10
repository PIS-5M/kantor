import React, { useState } from 'react';
import axios from "axios";
import { Input, Button, Modal, ModalHeader, ModalBody, ModalFooter, FormFeedback } from 'reactstrap';


function WalletMoneySubtract () {
    const [modal, setModal] = useState(false);
    const [walletId, setWalletId] = useState();
    const [value, setValue] = useState();
    const toggle = () => setModal(!modal);
    const [isValid, setValid] = useState(false);
    const [error, setError] = useState()



    const isNumValid = (e) => {
        if (/^\d+$/.test(e.target.value) && 1 <= e.target.value.length && e.target.value.length <= 15){
            setValid(true)
        } else {
        setValid(false)}
      }

      const isFormValid = () => {
        if (isValid)
        {return true;}
        return false;
      }

    const moneySubtract = async (event) => {
        try {
          const response = await axios.post("http://localhost:8000/wallet_subtract", {
            wallet_id: walletId,
            value: Number(value),
          });
        } catch (error) {
            {setError(error.response.data.detail)};
          }
      };
    return (
        <div className="BLUE_BG">
            <div>
      <Button className="addButton textStyle" onClick={toggle}>
        Wypłać kwotę z portfela
      </Button>
      <Modal isOpen={modal} toggle={toggle} >
        <ModalHeader toggle={toggle} className="blackTextStyle">
                Wypłać kwotę z portfela</ModalHeader>
        <ModalBody>
            <div> Wprowadź numer portfela
                <Input className="inputStyleAcc" maxLength={26}
                onChange={(e) => {isNumValid(e); setWalletId(e.target.value);}}>
                </Input>
            </div>
            <div> Wprowadź kwotę
                <Input className="inputStyleAcc" maxLength={26}
                onChange={(e) => {isNumValid(e); setValue(e.target.value);}}>
                </Input>
            </div>
            <label className="errorLabel">{error}</label>

        </ModalBody>
        <ModalFooter>
        <Button
            className="buttonStyleLoginUser whiteTextStyle"
            type="submit"
            onClick={async (e) => {
                moneySubtract(e);
            }}
            disabled={!isFormValid()}
          > Wypłać </Button>
          <Button className="cancelButton" onClick={toggle}>
            Anuluj
          </Button>
        </ModalFooter>
      </Modal>
    </div>

        </div>
    )

}

export default WalletMoneySubtract