import React from "react";
import { AllOffersTable } from "../components/AllOffersTable";
import z from "zod";
import { useQuery } from "react-query";

const allOffersSchema = z.object({
  publication_date: z.coerce.date(),
  last_modification_date: z.coerce.date(),
  value: z.coerce.number(),
  exchange_rate: z.coerce.number(),
  currency: z.coerce.string().length(3),
  wanted_currency: z.coerce.string().length(3),
});

const allOffersResponseSchema = z.object({
  transactions: z.array(allOffersSchema),
});

export const AllOffers = () => {
  const { data, isLoading, error } = useQuery(`/offers`, () =>
    fetch("http://localhost:8000/offers", { method: "GET" })
      .then((response) => response.json())
      .then((responseJson) => allOffersResponseSchema.parse(responseJson))
  );

  if (isLoading) return "Loading...";
  if (error) return "Error!";

  // ! dummy do zastapienia przez `data` gdy bedzie juz backendowa funkcja
  const dummy = [
    {
      publication_date: new Date().toISOString().split("T")[0],
      last_modification_date: new Date().toISOString().split("T")[0],
      value: 4500,
      exchange_rate: 3.5,
      currency: "USD",
      wanted_currency: "SEK",
    },
    {
      publication_date: new Date().toISOString().split("T")[0],
      last_modification_date: new Date().toISOString().split("T")[0],
      value: 1200,
      exchange_rate: 0.8,
      currency: "PLN",
      wanted_currency: "EUR",
    },
    {
      publication_date: new Date().toISOString().split("T")[0],
      last_modification_date: new Date().toISOString().split("T")[0],
      value: 9990,
      exchange_rate: 2.7,
      currency: "USD",
      wanted_currency: "EUR",
    },
  ];
  return (
    <div className="flex flex-col min-w-full justify-center min-h-full GREY_BG ">
      <header className="p-4 flex justify-between items-center">
        <h1 className="font-semibold text-6xl">Wszystkie oferty</h1>
      </header>
      <AllOffersTable data={dummy} />
    </div>
  );
};
