import React, { useState } from 'react';
import axios from "axios";
import { Input, Button, Modal, ModalHeader, ModalBody, ModalFooter, FormFeedback } from 'reactstrap';


function WalletMoneyDeposit () {
    const [modal, setModal] = useState(false);
    const [walletId, setWalletId] = useState();
    const [value, setValue] = useState();
    const toggle = () => setModal(!modal);
    const [isValid, setValid] = useState(false);


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

    const depositMoney = async (event) => {
        try {
          const response = await axios.post("http://localhost:8000/wallet_add", {
            wallet_id: walletId,
            value: value,
          });
        } catch (error) {
            console.error(error);
          }
      };
    return (
        <div className="BLUE_BG">
            <div>
      <Button className="addButton textStyle" onClick={toggle}>
        Przelej kwotę do portfela
      </Button>
      <Modal isOpen={modal} toggle={toggle} >
        <ModalHeader toggle={toggle} className="blackTextStyle">
                Przelej</ModalHeader>
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

        </ModalBody>
        <ModalFooter>
        <Button
            className="buttonStyleLoginUser whiteTextStyle"
            type="submit"
            onClick={async (e) => {
                depositMoney(e); toggle();
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

export default WalletMoneyDeposit