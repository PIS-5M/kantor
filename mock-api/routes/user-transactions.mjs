import { Router } from "express";

const app = Router();

// zasadniczo nie powinnismy tak robic, ALE
// nazwa sciezki do rozważenia
//
app.get("/user-transactions", (req, res) => {
  const userId = req.headers.authorization.slice(7); // zalecam bearer-token
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

export { app as UserTransactionsRouter };
