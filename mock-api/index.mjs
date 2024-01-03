import express from "express";
import cors from "cors";
import { UserTransactionsRouter } from "./routes/user-transactions.mjs";
import { UserOffersRouter } from "./routes/user-offers.mjs";
import { CurrenciesRouter } from "./routes/currencies.mjs";

const app = express();
app.use(cors());
app.use(express.json());
const PORT = process.env.PORT || 8000;

app.use(async (req, res, next) => {
  setTimeout(() => next(), Math.random() * 1000);
});

app.get("/", (req, res) => res.json({ message: "Guten morgen" }));
app.post("/login", (req, res) => {
  return res.json({ id: 1 });
});

app.use(UserTransactionsRouter);
app.use(UserOffersRouter);
app.use(CurrenciesRouter);
app.listen(PORT, () => {
  console.log(`mock server listening at 0.0.0.0:${PORT}`);
});
