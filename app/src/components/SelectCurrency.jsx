import React from "react";
import getCurrencies from "../functions/getCurrencies";
import { Input } from "reactstrap";

export const SelectCurrency = (props) => {
  const [options, setOptions] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(false);

  React.useEffect(() => {
    const run = async () => {
      setIsLoading(true);
      const currencies = await getCurrencies();
      setOptions(currencies);
      setIsLoading(false);
    };
    run();
  }, []);

  return (
    <Input
      type="select"
      placeholder={isLoading ? "Wczytywanie walut..." : "Wybierz walutę"}
      {...props}
    >
      <option value="" className="text-gray-600">
        -- wybierz walutę
      </option>
      {options?.length &&
        options.map((currency) => (
          <option key={currency.currency_id} value={JSON.stringify(currency)}>
            {currency.abbreviation}
          </option>
        ))}
    </Input>
  );
};
