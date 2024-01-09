const currencies = [
  {
    currency_id: 1,
    abbreviation: "EUR",
  },

  {
    currency_id: 2,
    abbreviation: "USD",
  },

  {
    currency_id: 3,
    abbreviation: "SEK",
  },

  {
    currency_id: 4,
    abbreviation: "CHF",
  },
];

const offers = [
  {
    offer_id: 1,
    publication_date: new Date("10-21-2023").toISOString(),
    last_modification_date: new Date("10-22-2023").toISOString(),
    value: 5000,
    currency: {
      currency_id: 1,
      abbreviation: "EUR",
    },
    wanted_currency: {
      currency_id: 2,
      abbreviation: "USD",
    },
    exchange_rate: 2.99,
    account_number: 69696969696969,
    status: "CLOSED",
  },
  {
    offer_id: 2,
    publication_date: new Date("10-23-2023").toISOString(),
    last_modification_date: new Date("10-25-2023").toISOString(),
    value: 2000,
    currency: {
      currency_id: 1,
      abbreviation: "EUR",
    },
    wanted_currency: {
      currency_id: 2,
      abbreviation: "USD",
    },
    exchange_rate: 3.01,
    account_number: 69696969696969,
    status: "ACTIVE",
  },
];

class DB {
  constructor(data) {
    this.data = data;
  }
  add(el) {
    this.data.push(el);
  }
}

export const OfferDB = new DB(offers);
export const CurrenciesDB = new DB(currencies);
