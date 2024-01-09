import React from "react";
import clientToken from "../ClientToken";
import { useMutation, useQuery, useQueryClient } from "react-query";
import z from "zod";
import { Table } from "reactstrap";
import { Trash, Edit } from "lucide-react";
import { toast } from "react-hot-toast";
import { useAutoAnimate } from "@formkit/auto-animate/react";

export const currencySchema = z.object({
  currency_id: z.coerce.number().positive("Nieprawidłowa waluta"),
  abbreviation: z.string(),
});

export const offerSchema = z.object({
  offer_id: z.coerce.number(),
  publication_date: z.coerce.date(),
  last_modification_date: z.coerce.date(),
  value: z.coerce.number(),
  currency: currencySchema,
  wanted_currency: currencySchema,
  exchange_rate: z.coerce.number(),
  account_number: z.coerce.string(),
  status: z.enum(["ACTIVE", "CLOSED"]), //!!!
});

const userOffersResponseSchema = z.object({
  offers: z.array(offerSchema),
});

// Create the component to display a single offer
const OfferRow = ({ offer }) => {
  const qc = useQueryClient();
  const { mutateAsync, isLoading } = useMutation(
    () =>
      fetch(`http://localhost:8000/user-offers/${offer.offer_id}`, {
        method: "DELETE",
      }),
    {
      onSuccess: () => qc.invalidateQueries("userOffers"),
    }
  );

  //TODO EDYCJA oferty

  const deleteOfferHandler = async () => {
    try {
      await mutateAsync();
      toast.success("Usunięto ofertę!");
    } catch (e) {
      toast.error("Nie udało się usunąć oferty!");
    }
  };
  return (
    <tr>
      <td>{offer.publication_date.toISOString().split("T")[0]}</td>
      <td>{offer.last_modification_date.toISOString().split("T")[0]}</td>
      <td>{offer.value}</td>
      <td>{offer.currency.abbreviation}</td>
      <td>{offer.wanted_currency.abbreviation}</td>
      <td>{offer.exchange_rate}</td>
      <td>{offer.account_number}</td>
      {offer.status === "ACTIVE" && (
        <td>
          <div className="flex mx-2 gap-4">
            <button className="flex items-center hover:bg-blue-100 px-2 py-1 rounded">
              <Edit className="w-4 h-4 mr-2" /> Edytuj
            </button>
            <button
              disabled={isLoading}
              onClick={deleteOfferHandler}
              className="flex items-center hover:bg-red-100 px-2 py-1 rounded"
            >
              <Trash className="w-4 h-4 mr-2" /> Usuń
            </button>
          </div>
        </td>
      )}
    </tr>
  );
};

/**
 * OffersTable component that fetches and displays offers based on their status
 */
export const MyOffersTable = ({ type }) => {
  const [parent] = useAutoAnimate();
  const { userId } = clientToken();
  const { data, isLoading, error } = useQuery("userOffers", () =>
    fetch("http://localhost:8000/user-offers", {
      headers: { Authorization: `Bearer: ${userId()}` },
    })
      .then((res) => res.json())
      .then((resJson) => userOffersResponseSchema.parse(resJson))
  );

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>An error occurred: {error.message}</div>;

  const filteredOffers = data.offers.filter((offer) => offer.status === type);
  const captionText = type === "ACTIVE" ? "Aktywne" : "Zrealizowane";

  return (
    <Table hover className="custom-table">
      <caption className="caption-top">{captionText}</caption>
      <thead>
        <tr className="[&>th]:align-top ">
          <th>Data wystawienia</th>
          <th>Data ostatniej modyfikacji</th>
          <th>Kwota</th>
          <th>Waluta</th>
          <th>Poszukiwana waluta</th>
          <th>Cena</th>
          <th>Numer konta</th>
          {type === "ACTIVE" && <th>Akcje</th>}
        </tr>
      </thead>
      <tbody ref={parent}>
        {filteredOffers.map((offer, index) => (
          <OfferRow key={index} offer={offer} />
        ))}
      </tbody>
    </Table>
  );
};
