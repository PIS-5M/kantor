import axios from "axios";

const getCurrencies = async () => {
  try {
    const response = await axios.get("http://localhost:8000/all_currency");
    return response.data.currency; // Adjusted to match the API response
  } catch (error) {
    console.error(error.message);
    return []; // Return an empty array in case of an error
  }
};

export default getCurrencies;
