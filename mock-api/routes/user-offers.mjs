import { Router } from "express";
import { OfferDB } from "../db.mjs";
import z from "zod";

const offerIdSchema = z.coerce.number();

const app = Router();

app.get("/user-offers", (req, res) => {
  //   const userId = req.headers.authorization.slice(7); //bearer token

  // pobranie z bazy bla bla

  return res.json({
    offers: OfferDB.data,
  });
});

app.delete("/user-offers/:offer_id", (req, res) => {
  //   const userId = req.headers.authorization.slice(7); //bearer token
  const offerId = offerIdSchema.parse(req.params.offer_id);
  OfferDB.data = OfferDB.data.filter(({ offer_id }) => offer_id !== offerId);
  return res.sendStatus(200);
});

app.post("/user-offers", (req, res) => {
  // user id autoryzacja!

  OfferDB.data.push({
    ...req.body,
    status: "ACTIVE",
    offer_id: OfferDB.data.length,
    publication_date: new Date(),
    last_modification_date: new Date(),
  });
  return res.sendStatus(201);
});

export { app as UserOffersRouter };
