from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
import database


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
    allow_origins=origins,  # Allows all origins
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
    database.registration(hashed_password_string, name, surname, email)
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


@app.post("/all_currency")
async def get_all_currency():
    currency = database.get_all_currency()
    return {"currency": currency}
