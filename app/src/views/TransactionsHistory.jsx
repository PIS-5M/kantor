import React from "react";
import { TransactionsTable } from "../components/TransactionsTable";

export const TransactionsHistory = () => {
  return (
    <div className="flex flex-col min-w-full justify-center min-h-full bg-background">
      <header className="ml-4 my-4">
        <h1 className="font-semibold text-6xl">Moje transakcje</h1>
      </header>
      <TransactionsTable />
    </div>
  );
};
