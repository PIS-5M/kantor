import { Router } from "express";
import { CurrenciesDB } from "../db.mjs";

const app = Router();

app.get("/currencies", (req, res) => {
  return res.json({
    currencies: CurrenciesDB.data,
  });
});

export { app as CurrenciesRouter };
