import React, { useState, useEffect } from "react";
import clientToken from '../ClientToken';
import axios from "axios";
import { Table, Button } from "reactstrap";


function Wallets () {
    const {userId} = clientToken();
    const [wallets, setWallets] = useState([])

    const getWallets = async (event) => {
        try {
          const response = await axios.post("http://localhost:8000/show_wallet", {
            user_id: userId(),
          });
          setWallets(response.data.wallet)
        } catch (error) {
            console.error(error);
          }
      };

      useEffect((e) => {
        getWallets(e);
      }, []);

      return (
        <div>
            <div>
            <Table bordered hover responsive className="tableDesign tableDesignNarrow" >
  <thead>
    <tr>
      <th>
        Numer portfelu
      </th>
      <th>
        Waluta
      </th>
      <th>
        Kwota będąca w obrocie
      </th>
      <th>
        Kwota leżąca na koncie
      </th>
    </tr>
  </thead>
  <tbody>
  {wallets.length > 0 && wallets.map((wallet, index) => (
                    <tr key={index}>
                        <th scope="row">{wallet[1]}</th>
                        <td> {wallet[0]} </td>
                        <td>{wallet[4]} zł</td>
                        <td>{wallet[3]} zł</td>
                        <td> <Button type="button" className="cartStyle"
                        >Wpłać do portfela</Button> </td>
                        <td> <Button type="button" className="cartStyle"
                        >Wypłać z portfela</Button> </td>
                    </tr>

                ))}
  </tbody>
</Table>
            </div>
        </div>
      )

}

export default Wallets