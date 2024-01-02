import React, { useEffect, useState } from "react";
import Calculator from "../components/Calculator";
import Charts from "../components/CurrencyCharts";

function Home() {
  return (
    <div className="BLUE_BG">
      <div>
        <Calculator />
      </div>
      <div>
        <Charts />
      </div>
    </div>
  );
}

export default Home;
