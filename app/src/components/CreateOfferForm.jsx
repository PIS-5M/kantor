import { zodResolver } from "@hookform/resolvers/zod";
import React from "react";
import { Controller, useForm } from "react-hook-form";
import { Button, Form, FormFeedback, Input, Label } from "reactstrap";
import { currencySchema } from "./MyOffersTable";
import { SelectCurrency } from "./SelectCurrency";
import { useMutation, useQueryClient } from "react-query";
import toast from "react-hot-toast";
import clientToken from "../ClientToken";
import z from "zod";
import { DialogMatches } from "./DialogMatches";

export const newOfferSchema = {
  // submit danych w takiej formie bedzie
  value: z.coerce.number().positive(),
  currency: currencySchema, // currency obj -> {id + abbr}
  wanted_currency: currencySchema,
  exchange_rate: z.coerce.number().positive(),
};

const defaultValues = {
  value: 0,
  currency: {
    currency_id: -1,
    abbreviation: "",
  },
  wanted_currency: {
    currency_id: -2,
    abbreviation: "",
  },
  exchange_rate: 0,
};

export const CreateOfferForm = () => {
  const { handleSubmit, formState, control } = useForm({
    resolver: zodResolver(newOfferSchema),
    defaultValues,
  });

  // helpers for showing matched offers in a modal
  const [dialogData, setDialogData] = React.useState(null);
  const [isModalOpen, setIsModalOpen] = React.useState(false);

  const toggleModal = () => setIsModalOpen(!isModalOpen);
  //

  const qc = useQueryClient();
  const { mutateAsync, isLoading } = useMutation(
    async (dataToSend) => {
      return fetch("http://localhost:8000/add_offer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToSend),
      }).then((res) => res.json());
    },
    {
      onSuccess: () => {
        qc.invalidateQueries("userOffers");
        // toast.success("Pomyślnie utworzono ofertę!");
      },
      onError: () => {
        toast.error("Nie udało się dodać oferty.");
      },
    }
  );

  const submitHandler = async (values) => {
    const user_id = clientToken().userId();

    if (!user_id) {
      toast.error("User ID is not available");
      return;
    }

    try {
      const selledCurrency = currencySchema.parse(JSON.parse(values.currency));
      const wantedCurrency = currencySchema.parse(
        JSON.parse(values.wanted_currency)
      );

      const dataToSend = {
        user_id,
        selled_currency_id: selledCurrency.currency_id,
        value: values.value,
        wanted_currency_id: wantedCurrency.currency_id,
        exchange_rate: values.exchange_rate,
      };

      const response = await mutateAsync(dataToSend);

      if (response.matches) {
        console.log("Matches:", response.matches);
        toast.success("Oferta została dodana!");
        //JSON.stringify(response.matches)
        setDialogData(response.matches);
        setIsModalOpen(true); // Open the modal
      }
    } catch (e) {
      console.error(e);
      // toast.error("Nie udało się dodać oferty");
    }
  };

  return (
    <div className="rounded p-8 bg-slate-50 shadow-sm ">
      <Form onSubmit={handleSubmit(submitHandler, console.error)}>
        <div>
          <Label htmlFor="value">Ile waluty chcesz sprzedać?</Label>
          <Controller
            control={control}
            name="value"
            render={({ field }) => (
              <Input
                // {...field} // mozna
                placeholder="np. 4500"
                invalid={!!formState.errors.value}
                id="value"
                inputMode="numeric"
                onChange={field.onChange}
                onBlur={field.onBlur}
                name={field.name}
                value={field.value}
              />
            )}
          />
          <FormFeedback invalid="true">
            {formState.errors.value?.message}
          </FormFeedback>
        </div>
        {/* selecty walut */}
        <div>
          <Label htmlFor="currency">Jaką walutę chcesz sprzedać?</Label>
          <Controller
            control={control}
            name="currency"
            render={({ field }) => (
              <SelectCurrency
                invalid={!!formState.errors.currency?.currency_id}
                id="currency"
                onChange={(event) => {
                  field.onChange(JSON.parse(event.target.value));
                }}
                name={field.name}
                value={JSON.stringify(field.value)}
              />
            )}
          />
          <FormFeedback invalid="true">
            {formState.errors.currency?.currency_id?.message}
          </FormFeedback>
        </div>
        <div>
          <Label htmlFor="wanted_currency">Jaką walutę chcesz kupić?</Label>
          <Controller
            control={control}
            name="wanted_currency"
            render={({ field }) => (
              <SelectCurrency
                invalid={!!formState.errors.wanted_currency?.currency_id}
                id="wanted_currency"
                onChange={(event) => {
                  field.onChange(JSON.parse(event.target.value));
                }}
                name={field.name}
                value={JSON.stringify(field.value)}
              />
            )}
          />
          <FormFeedback invalid="true">
            {formState.errors.wanted_currency?.currency_id?.message}
          </FormFeedback>
        </div>
        {/* ... */}
        <div>
          <Label htmlFor="exchange_rate">Po ile chcesz ją sprzedać?</Label>
          <Controller
            control={control}
            name="exchange_rate"
            render={({ field }) => (
              <Input
                placeholder="np. 2.50"
                invalid={!!formState.errors.exchange_rate}
                id="exchange_rate"
                onChange={field.onChange}
                onBlur={field.onBlur}
                name={field.name}
                value={field.value}
              />
            )}
          />
          <FormFeedback invalid="true">
            {formState.errors.exchange_rate?.message}
          </FormFeedback>
        </div>

        <Button
          className="w-full mt-4 bg-blue-700 hover:bg-blue-700/90 disabled:opacity-50"
          type="submit"
          disabled={isLoading}
        >
          {isLoading ? "Wczytywanie..." : "Dodaj"}
        </Button>
      </Form>

      <DialogMatches
        isOpen={isModalOpen}
        data={dialogData}
        toggle={toggleModal}
      />
    </div>
  );
};
