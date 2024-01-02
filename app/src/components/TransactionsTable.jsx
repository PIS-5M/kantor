import React from "react";
import { Table } from "reactstrap";
import z from "zod";
import clientToken from "../ClientToken";
import { useQuery } from "react-query";

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

  // wbudowany fetch zamiast axiosa tez daje rade!
  const { data, isLoading, error } = useQuery(`/user-transactions`, () =>
    fetch("http://localhost:8000/user-transactions", {
      method: "GET",
      headers: { Authorization: `Bearer: ${userId()}` },
    })
      .then((response) => response.json())
      .then((responseJson) => transactionResponseSchema.parse(responseJson))
  );

  if (isLoading) return "Loading...";
  if (error) return "Error!";

  return (
    <Table hover className="custom-table">
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
        {data.transactions.map((transaction) => (
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
