import { zodResolver } from "@hookform/resolvers/zod";
import React from "react";
import { Controller, useForm } from "react-hook-form";
import { Button, Form, FormFeedback, Input, Label } from "reactstrap";
import { offerSchema } from "./OffersTable";
import { SelectCurrency } from "./SelectCurrency";
import { useMutation, useQueryClient } from "react-query";
import toast from "react-hot-toast";

export const newOfferSchema = offerSchema.pick({
  value: true,
  currency: true,
  wanted_currency: true,
  exchange_rate: true,
  account_number: true,
});

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
  account_number: "",
};

export const CreateOfferForm = () => {
  const { handleSubmit, formState, control } = useForm({
    resolver: zodResolver(newOfferSchema),
    defaultValues,
  });
  const qc = useQueryClient();
  const { mutateAsync, isLoading } = useMutation(
    "userOffers",
    (values) =>
      fetch("http://localhost:8000/user-offers", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      }).then((res) => res.json()),
    {
      onSuccess: () => qc.invalidateQueries("userOffers"),
    }
  );

  const submitHandler = async (values) => {
    console.log(`Submitted values :\n ${JSON.stringify(values, null, 2)}`);
    try {
      mutateAsync(values);
      toast.success("Pomyślnie utworzono ofertę! 😎");
    } catch (e) {
      console.error(e);
      toast.error("Nie udało się dodać oferty 😢");
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
                placeholder="np. 4500"
                invalid={!!formState.errors.value}
                id="value"
                onChange={field.onChange}
                onBlur={field.onBlur}
                name={field.name}
                value={field.value}
                inputMode="numeric"
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
        <div>
          <Label htmlFor="account_number">
            Jaki numer konta do tej transakcji?
          </Label>
          <Controller
            control={control}
            name="account_number"
            render={({ field }) => (
              <Input
                placeholder="np. 12123434555566667777888899"
                invalid={!!formState.errors.account_number}
                id="account_number"
                onChange={field.onChange}
                onBlur={field.onBlur}
                name={field.name}
                value={field.value}
              />
            )}
          />
          <FormFeedback invalid="true">
            {formState.errors.account_number?.message}
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
    </div>
  );
};
