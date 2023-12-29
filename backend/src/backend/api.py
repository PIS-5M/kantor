from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
import database


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

# CORSMiddleware => cross-origin requests
# eg. requests that originate from a different protocol, IP address, domain name, or port
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to fastAPI! It is an api and it is really fast:)"}


# *** hello world ***
# dummy database here
messages = [
    {
        "id": "1",
        "item": "Hello"
    },
    {
        "id": "2",
        "item": "World"
    },
    {
        "id": "3",
        "item": "Again!!!"
    }
]

@app.get("/messages", tags=["messages"])
async def get_messages() -> dict:
    return { "data": messages }


@app.post("/registration")
async def register_user(data: dict):
    name = data['name']
    surname = data['surname']
    password = data['password']
    email = data['email']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_string = hashed_password.decode('utf-8')

    print(f"Received registration data - user_name: {name}, surname: {surname}, password: {hashed_password_string}, email: {email}")
    database.registration(hashed_password_string, name, surname, email)
    return {"message": "Registration successful"}


@app.post("/login")
async def login_user(data: dict):
    email = data['email']
    password = data['password']

    status = database.login(email, password)

    print(f"Received login data - email: {email}, password: {password}")

    if status:
        return {"id": status}

    raise HTTPException(status_code=400, detail="Bad login or password")


@app.post("/email_used")
async def email_used(data: dict):
    email = data['email']

    print(f"Received data - email: {email}")
    status = database.email_used(email)
    if status:
        raise HTTPException(status_code=400, detail="Email already used")
    return {"message": "Email ok"}
