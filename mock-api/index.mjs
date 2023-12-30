import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());
const PORT = process.env.PORT || 8000;
app.get("/", (req, res) => res.json({ message: "Guten morgen" }));

app.post("/login", (req, res) => {
  return res.json({ id: 1 });
});

// zasadniczo nie powinnismy tak robic, ALE
// nazwa sciezki do rozważenia
app.get("/user-transactions/:id", (req, res) => {
  const userId = req.params.id;
  // POBRANIE Z BAZY DANYCH
  const transactions = [
    {
      transaction_history_id: 1,
      offer_id: 100,
      value: 500,
      price: 50,
      value_currency_name: "USD",
      price_currency_name: "USD",
      is_buyer: true,
      bank_account: "123456789",
      date: new Date("12/28/2023").toISOString(),
    },
  ];
  return res.json({ transactions });
});

app.listen(PORT, () => {
  console.log(`mock server listening at 0.0.0.0:${PORT}`);
});
