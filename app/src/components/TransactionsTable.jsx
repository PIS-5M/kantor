import React from "react";
import { Table } from "reactstrap";
import z from "zod";
import clientToken from "../ClientToken";
import axios from "axios";
const transactionEntrySchema = z.object({
  transaction_history_id: z.number(),
  offer_id: z.number(),
  // one są do pokazania wartości bazując na fladzie `is_buyer`
  value: z.number(),
  price: z.number(),
  // currency name z JOINa na tabeli transakcji
  value_currency_name: z.string().length(3),
  price_currency_name: z.string().length(3),
  // jesli transakcja jest tego klienta i.e. on jest jako buyer_id => True else False
  is_buyer: z.boolean(),
  bank_account: z.string(),
  date: z.coerce.date(),
});

const transactionResponseSchema = z.object({
  transactions: z.array(transactionEntrySchema),
});

export const TransactionsTable = () => {
  const { userId } = clientToken();
  const [transactions, setTransactions] = React.useState([]);

  React.useEffect(() => {
    // Define the URL for the API endpoint
    const apiUrl = `http://localhost:8000/user-transactions/${userId()}`;

    // Fetch data from the API using Axios
    axios
      .get(apiUrl)
      .then((response) => {
        // Assuming the response data is an array of transactions
        const fetchedTransactions = transactionResponseSchema.parse(
          response.data
        );

        // Update the state with the fetched transactions
        setTransactions(fetchedTransactions.transactions);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []); // Re-fetch data whenever userId changes

  return (
    <Table>
      <thead>
        <tr>
          <th>Numer transakcji</th>
          <th>Numer oferty</th>
          <th>Kwota</th>
          <th>Waluta</th>
          <th>Typ</th>
          <th>Numer konta bankowego</th>
          <th>Data transakcji</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((transaction) => (
          <tr key={transaction.transaction_history_id}>
            <td>{transaction.transaction_history_id}</td>
            <td>{transaction.offer_id}</td>
            <td>
              {transaction.is_buyer ? transaction.value : transaction.price}
            </td>
            <td>
              {transaction.is_buyer
                ? transaction.value_currency_name
                : transaction.price_currency_name}
            </td>
            <td>{transaction.is_buyer ? "Wpłata" : "Wypłata"}</td>
            <td>{transaction.bank_account}</td>
            <td>{transaction.date.toLocaleDateString()}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};
