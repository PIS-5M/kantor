import React from "react";
import getCurrencies from "../functions/getCurrencies";
import { Input } from "reactstrap";

export const SelectCurrency = (props) => {
  const [options, setOptions] = React.useState([]);
  // const [isLoading, setIsLoading] = React.useState(false);

  // {"currency":[[1,"Dolar AmerykaÅ„ski","USD","12345678901234567890123456"],[2,"Euro","EUR","98765432109876543210987654"], ... ]

  React.useEffect(() => {
    const run = async () => {
      // setIsLoading(true);
      const currencies = await getCurrencies();
      setOptions(currencies || []); // Ensure it's an array
      // setIsLoading(false);
    };
    run();
  }, []);

  return (
    <Input type="select" {...props}>
      <option value="" className="text-gray-600">
        -- wybierz walutę
      </option>
      {options.map((currency) => (
        <option key={currency[0]} value={currency[0]}>
          {currency[2]} {/* Using the abbreviation */}
        </option>
      ))}
    </Input>
  );
};
