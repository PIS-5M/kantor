from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
import database
from database import DatabaseError
from typing import List

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:3307",
    "localhost:3307",
]

# CORSMiddleware => cross-origin requests
# eg. requests that originate from a different protocol, IP address, domain name, or port
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # Allows all origins
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to fastAPI! It is an api and it is really fast:)"}


@app.post("/registration")
async def register_user(data: dict):
    name = data["name"]
    surname = data["surname"]
    password = data["password"]
    email = data["email"]

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    hashed_password_string = hashed_password.decode("utf-8")

    print(
        f"Received registration data - user_name: {name}, surname: {surname}, password: {hashed_password_string}, email: {email}"
    )
    database.registration(name, surname, email, hashed_password_string)
    return {"message": "Registration successful"}


@app.post("/login")
async def login_user(data: dict):
    email = data["email"]
    password = data["password"]

    status = database.login(email, password)

    print(f"Received login data - email: {email}, password: {password}")

    if status:
        return {"id": status}

    raise HTTPException(status_code=400, detail="Błędne dane logowania.")


@app.post("/email_used")
async def email_used(data: dict):
    email = data["email"]

    print(f"Received data - email: {email}")
    status = database.email_used(email)
    if status:
        return {"message": True}
    return {"message": False}


@app.get("/all_currency")
async def get_all_currency():
    currency = database.get_all_currency()
    return {"currency": currency}


@app.post("/user_data")
async def user_data(data: dict):
    id = data["id"]

    name, surname, email = database.get_user_data(id)

    if name or surname or email:
        return {"name": name, "surname": surname, "email": email}

    raise HTTPException(status_code=400, detail="Podany użytkownik nie istnieje")


@app.post("/add_offer")
async def email_used(data: dict):
    user_id = data["user_id"]
    selled_currency_id = data["selled_currency_id"]
    value = data["value"]
    wanted_currency_id = data["wanted_currency_id"]
    exchange_rate = data["exchange_rate"]
    matches = database.new_offer(
        user_id, selled_currency_id, value, wanted_currency_id, exchange_rate
    )
    return {"matches": matches}


# {
#   "matches": [
#     [50, 100],
#     [30, 60],
#     ... more matches
#   ]
# }


@app.post("/add_new_wallet")
async def add_new_wallet(data: dict):
    user_id = data["user_id"]
    currency_id = data["currency_id"]
    account = data["account"]

    hashed_account = bcrypt.hashpw(account.encode("utf-8"), bcrypt.gensalt())
    hashed_account_string = hashed_account.decode("utf-8")

    result = database.add_wallet(user_id, currency_id, hashed_account_string)
    if result:
        return {"message": "Succesfully added wallet"}
    raise HTTPException(status_code=400, detail="Użytkownik już ma taki portfel")


@app.get("/user_offers/{seller_id}", response_model=List[dict[str, any]])
async def user_offers(seller_id: int):
    results = database.user_offers(seller_id)

    if not results:
        raise HTTPException(
            status_code=404, detail="Offers not found for the given seller ID"
        )

    # List to store offer details
    offer_details_list = []

    for result in results:
        offer_details = {
            "offer_id": result["offer_history_id"],
            "publication_date": result["publication_date"],
            "last_modification_date": result["last_modification_date"],
            "value": result["value"],
            "currency": {
                "currency_id": result["currency_id"],
                "abbreviation": result["abbreviation"],
            },
            "wanted_currency": {
                "currency_id": result["currency_id"],
                "abbreviation": result["abbreviation"],
            },
            "exchange_rate": result["exchange_rate"],
            "account_number": result["account_number_hash"],
            "status": "CLOSED" if result["is_cancelled"] else "ACTIVE",
        }

        # Append the offer_details to the list
        offer_details_list.append(offer_details)

    return offer_details_list


@app.post("/show_wallet")
async def show_wallet(data: dict):
    user_id = data["user_id"]
    wallet = database.get_wallet(user_id)
    return {"wallet": wallet}


@app.delete("/delete_offer/{offer_id}")
async def delete_offer(offer_id: int):
    try:
        offer_deleted = database.delete_offer(offer_id)

        if not offer_deleted:
            raise HTTPException(status_code=404, detail="Offer not found")

        return {"message": "Offer deleted successfully"}
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/user-transactions")
async def get_user_transactions(user_id: int):
    transactions = database.get_transactions(user_id)

    # # POBRANIE Z BAZY DANYCH
    # transactions = [
    #     {
    #         "transaction_id": 1,
    #         "value": -100.00,
    #         "value_currency_name": "USD",
    #         "bank_account": "123456789",
    #     },
    # ]

    return {"transactions": transactions}


@app.post("/wallet_add")
async def add_to_wallet(data: dict):
    wallet_id = data["wallet_id"]
    value = data["value"]
    database.wallet_add(wallet_id, value)
    return {"message": "Succesfully added to wallet"}


@app.post("/wallet_subtract")
async def add_to_wallet(data: dict):
    wallet_id = data["wallet_id"]
    value = data["value"]
    result = database.wallet_subtract(wallet_id, value)
    if result:
        return {"message": "Succesfully subtracted from wallet"}
    raise HTTPException(status_code=400, detail="Za mało pieniędzy w portfelu")
