import axios from "axios";

const getCurrencies = async (event) => {
        try {
          const response = await axios.post("http://localhost:8000/all_currency", {
          });
          return response.data.currency
        } catch (error) {
          console.log(error.message)
        }
      };

export default getCurrencies;