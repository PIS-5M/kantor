import { zodResolver } from "@hookform/resolvers/zod";
import React from "react";
import { Controller, useForm } from "react-hook-form";
import { Button, Form, FormFeedback, Input, Label } from "reactstrap";
import { SelectCurrency } from "./SelectCurrency";
import { useMutation } from "react-query";
import toast from "react-hot-toast";
import clientToken from "../ClientToken";
import z from "zod";
import { DialogMatches } from "./DialogMatches";

export const newOfferSchema = z.object({
  value: z.coerce.number().positive(),
  currency: z.coerce.number().positive(), // Expecting currency ID as a number
  wanted_currency: z.coerce.number().positive(), // Expecting wanted currency ID as a number
  exchange_rate: z.coerce.number().positive(),
});

const defaultValues = {
  value: 0,
  currency_id: -1,
  wanted_currency_id: -2,
  exchange_rate: 0,
};

export const CreateOfferForm = () => {
  const { handleSubmit, formState, control } = useForm({
    resolver: zodResolver(newOfferSchema),
    defaultValues,
  });

  //
  // helpers for showing matched offers in a modal
  const [dialogData, setDialogData] = React.useState(null);
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const toggleModal = () => setIsModalOpen(!isModalOpen);
  //

  // Use React Query's useMutation for handling API requests
  const { mutate, isLoading } = useMutation(
    (newOfferData) => {
      return fetch("http://localhost:8000/add_offer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newOfferData),
      }).then((res) => res.json());
    },

    {
      onSuccess: (data) => {
        console.log(data);
        setDialogData(data.matches); // Assuming the API response structure is { matches: [...] }
        setIsModalOpen(true);
      },

      onError: (error) => {
        // Handle error state
        console.error("Error submitting offer:", error);
        toast.error("Error submitting offer");
      },
    }
  );

  const submitHandler = async (data) => {
    const offerData = {
      user_id: clientToken().userId(),
      selled_currency_id: data.currency,
      value: data.value,
      wanted_currency_id: data.wanted_currency,
      exchange_rate: data.exchange_rate,
    };

    mutate(offerData);
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
                placeholder="np. 4500"
                invalid={!!formState.errors.value}
                id="value"
                inputMode="numeric"
                onChange={(event) => field.onChange(event.target.value)}
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
                onChange={(event) => field.onChange(event.target.value)}
                name={field.name}
                value={field.value}
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
                  // Directly pass the number value
                  field.onChange(event.target.value);
                }}
                name={field.name}
                value={field.value}
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
                onChange={(event) => field.onChange(event.target.value)}
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
