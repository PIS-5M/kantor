import axios from "axios";

const getCurrencies = async (event) => {
  try {
    const response = await axios.get("http://localhost:8000/currencies", {});
    return response.data.currencies;
  } catch (error) {
    console.log(error.message);
  }
};

export default getCurrencies;
