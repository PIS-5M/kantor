import React from "react";
import { OffersTable } from "../components/OffersTable";

export const MyOffers = () => {
  return (
    <div className="flex flex-col min-w-full justify-center min-h-full GREY_BG ">
      <header className="p-4 flex justify-between items-center">
        <h1 className="font-semibold text-6xl">Moje oferty</h1>
        <a
          href={"/dodaj"}
          className="flex px-3 py-2 h-11 rounded bg-blue-600 text-white hover:bg-blue-600/90 transition-colors"
        >
          Dodaj ofertę
        </a>
      </header>
      <OffersTable type="ACTIVE" />
      <OffersTable type="CLOSED" />
    </div>
  );
};
