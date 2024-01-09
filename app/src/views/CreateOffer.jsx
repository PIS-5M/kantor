import React from "react";
import { CreateOfferForm } from "../components/CreateOfferForm";

export const CreateOffer = () => {
  return (
    <div className="flex flex-col w-full items-center gap-4 justify-center min-h-full GREY_BG ">
      <header className="p-4 flex justify-between items-center">
        <h1 className="font-semibold text-6xl">Dodaj ofertę</h1>
      </header>
      <div className="w-full max-w-xl">
        <CreateOfferForm />
      </div>
    </div>
  );
};
