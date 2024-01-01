import React, { useState, useEffect } from "react";
import { Input, Col, Row } from "reactstrap";
import "../styles/homeStyles.css";
import getCurrencies from "../functions/getCurrencies";

function Calculator() {
  const [exchangeRate, setExchangeRate] = useState(null);
  const [currencies, setCurrencies] = useState([]);
  const [currency1, setCurrency1] = useState("USD");
  const [currency2, setCurrency2] = useState("USD");
  const [amount, setAmount] = useState(100);

  const fetchExchangeRate = async (e, currency) => {
    try {
      const response = await fetch(
        `http://api.nbp.pl/api/exchangerates/rates/a/${currency}/`
      );
      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }
      const data = await response.json();
      return data.rates[0].mid;
    } catch (error) {
      console.error("Error fetching data:", error);
      return 1;
    }
  };

  const calculate = async (e, currency1, amount, currency2) => {
    let exchange1 = await fetchExchangeRate(e, currency1);
    let exchange2 = await fetchExchangeRate(e, currency2);
    let result = (exchange1 * amount) / exchange2;
    setExchangeRate(result.toFixed(2));
  };

  const getCurrenciesList = async (event) => {
    const currencies = await getCurrencies(event);
    setCurrencies(currencies);
  };

  useEffect((e) => {
    getCurrenciesList(e);
  }, []);
  useEffect(
    (e) => {
      calculate(e, currency1, amount, currency2);
    },
    [currency1, currency2, amount]
  );

  return (
    <div className="calculatorStyle">
      <div className="calculatorTextStyle">Kalkulator walutowy</div>
      <Row>
        <Col className="colStyle">
          <div className="blackTextStyle">Mam</div>
        </Col>
        <Col>
          <Input
            className="inputStyle"
            type="number"
            defaultValue={100}
            onChange={(e) => {
              setAmount(e.target.value);
            }}
          ></Input>
        </Col>
        <Col>
          <Input
            className="inputStyle"
            type="select"
            onChange={(e) => {
              setCurrency1(e.target.value);
            }}
          >
            {currencies?.length &&
              currencies.map((list, index) => (
                <option key={index} value={list[2]}>
                  {list[2]}
                </option>
              ))}{" "}
          </Input>
        </Col>
      </Row>
      <Row>
        <Col className="colStyle">
          <div className="blackTextStyle">Otrzymam</div>
        </Col>
        <Col>
          <div className="inputStyle">{exchangeRate}</div>
        </Col>
        <Col>
          <Input
            className="inputStyle"
            type="select"
            defaultValue={"SEK"}
            onChange={(e) => {
              setCurrency2(e.target.value);
            }}
          >
            {currencies?.length &&
              currencies.map((list, index) => (
                <option key={index} value={list[2]}>
                  {list[2]}
                </option>
              ))}{" "}
          </Input>
        </Col>
      </Row>
    </div>
  );
}

export default Calculator;
