import React from "react";
import { Table } from "reactstrap";
import z from "zod";
import clientToken from "../ClientToken";
import { useQuery } from "react-query";

const transactionEntrySchema = z.object({
  transaction_id: z.number(),
  value: z.number(),
  value_currency_name: z.string(),
  bank_account: z.string(),
});

const transactionResponseSchema = z.object({
  transactions: z.array(transactionEntrySchema),
});

export const TransactionsTable = () => {
  const { userId } = clientToken();

  const { data, isLoading, error } = useQuery("/user-transactions", () =>
    fetch(`http://localhost:8000/user-transactions?user_id=${userId()}`, {
      method: "GET",
      // headers: { Authorization: `Bearer ${userId()}` },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((responseJson) => transactionResponseSchema.parse(responseJson))
  );

  if (isLoading) return "Loading...";
  if (error) return "Error!";

  return (
    <Table hover className="custom-table">
      <thead>
        <tr>
          <th>Nr</th>
          <th>Kwota</th>
          <th>Waluta</th>
          <th>Numer konta bankowego</th>
        </tr>
      </thead>
      <tbody>
        {data.transactions.map((transaction, idx) => (
          <tr key={transaction.transaction_id}>
            {/* <td>{transaction.transaction_id}</td> */}
            <td>{idx}</td>
            <td>{transaction.value}</td>
            <td>{transaction.value_currency_name}</td>
            <td>{transaction.bank_account}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};
