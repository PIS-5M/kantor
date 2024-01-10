import React, { useEffect, useState } from "react";
import Calculator from "../components/Calculator";
import Charts from "../components/CurrencyCharts";

function Home() {
  return (
    <div className="BLUE_BG justifyContent">
      <p className="textLogin">Kantor online</p>
      <p className="textLogin">5MONET</p>
      <div>
        <Calculator />
      </div>
      <div className="textLogin">Kursy walut</div>
      <div className="whiteTextStyle">Zapoznaj się łatwo i szybko z ostatnimi kursami walut</div>
      <div>
        <Charts />
      </div>
    </div>
  );
}

export default Home;
