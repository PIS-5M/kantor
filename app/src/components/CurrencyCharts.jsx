import React, { useState, useEffect } from "react";
import { Col, Row, Input } from "reactstrap";
import moment from "moment";
import getCurrencies from "../functions/getCurrencies";
import { ctx, Chart } from "chart.js/auto";
import { Line } from "react-chartjs-2";

function Charts() {
  const [currencies, setCurrencies] = useState([]);
  const [currency, setCurrency] = useState("USD");
  const [range, setRange] = useState(7);
  const [startDate, setStartDate] = useState(
    moment().subtract(range, "days").format("YYYY-MM-DD")
  );
  const [exchanges, setExchanges] = useState([]);
  const [dates, setDates] = useState([]);
  const [filledData, setFilledData] = useState([]);
  const [allDatesInRange, setAllDatesInRange] = useState([]);
  const endDate = moment().subtract(1, "days").format("YYYY-MM-DD");

  const fetchExchangeRates = async (e, currency, topCount) => {
    try {
      const response = await fetch(
        `http://api.nbp.pl/api/exchangerates/rates/a/${currency}/last/${topCount}/`
      );
      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }
      const data = await response.json();

      setExchanges(data.rates.map((item) => item.mid));
      setDates(data.rates.map((item) => item.effectiveDate));
    } catch (error) {
      console.error("Error fetching data:", error);
      return 1;
    }
  };

  const getStartDate = () => {
    setStartDate(moment().subtract(range, "days").format("YYYY-MM-DD"));
  };

  const getCurrenciesList = async (event) => {
    //TODO: usunąć PLN z listy
    const currencies = await getCurrencies(event);
    setCurrencies(currencies);
  };

  function getClosestDateIndex() {
    let bestIndex = -1;
    let bestDiff = Infinity;

    for (let i = 0; i < dates.length; i++) {
      const currDate = dates[i];
      if (currDate < startDate) {
        const diff = moment(currDate).diff(moment(startDate), "days");
        if (diff < bestDiff) {
          bestDiff = diff;
          bestIndex = i;
        }
      }
    }
    return bestIndex;
  }

  const getFullData = () => {
    const tempAllDatesInRange = [];

    let currentDate = moment(startDate);

    while (currentDate.format("YYYY-MM-DD") <= endDate) {
      tempAllDatesInRange.push(currentDate.format("YYYY-MM-DD"));
      currentDate = currentDate.add(1, "days");
    }

    let tempFilledData = [];
    const idx = getClosestDateIndex();
    let previousValue = exchanges[idx];

    tempAllDatesInRange.forEach((date) => {
      const index = dates.indexOf(date);
      if (index !== -1) {
        tempFilledData.push(exchanges[index]);
        previousValue = exchanges[index];
      } else {
        tempFilledData.push(previousValue);
      }
    });
    setFilledData(tempFilledData);
    setAllDatesInRange(tempAllDatesInRange);
  };

  useEffect((e) => {
    getCurrenciesList(e);
  }, []);
  useEffect(
    (e) => {
      getStartDate(e);
    },
    [range]
  );
  useEffect(
    (e) => {
      fetchExchangeRates(e, currency, range);
    },
    [currency, startDate]
  );
  useEffect(() => {
    getFullData();
  }, [dates, exchanges]);

  const data = {
    labels: allDatesInRange,
    datasets: [
      {
        label: "Wartość",
        data: filledData,
        // you can set indiviual colors for each bar
        backgroundColor: ["#2F4CB2"],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div>
      <Row>
        <Col className="colStyle">
          <label>Wybierz walutę</label>
          <Input
            className="inputStyle2"
            type="select"
            onChange={(e) => {
              setCurrency(e.target.value);
            }}
          >
            {currencies?.length &&
              currencies.map((list, index) => (
                <option key={index} value={list[2]}>
                  {list[1]} {list[2]}
                </option>
              ))}{" "}
          </Input>
        </Col>
        <Col className="colStyle">
          <label>Wybierz zakres</label>
          <Input
            className="inputStyle2"
            type="select"
            onChange={(e) => {
              setRange(e.target.value);
            }}
          >
            <option value={7}> 1 tydzień </option>
            <option value={30}> 1 miesiąc </option>
            <option value={90}> 3 miesiące </option>
            <option value={183}> 6 miesięcy </option>
          </Input>
        </Col>
      </Row>
      <Line
        className="chartStyle"
        data={data}
        options={{
          plugins: {
            title: {
              display: true,
              text: "Kurs waluty",
            },
            legend: {
              display: false,
            },
          },
        }}
      />
    </div>
  );
}
export default Charts;
