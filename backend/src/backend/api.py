from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
    login = data['login']
    password = data['password']
    email = data['email']
    phoneNumber = data['phoneNumber']
    bankAccount = data['bankAccount']

    print(f"Received registration data - user_name: {name}, surname: {surname}, login: {login}, password: {password}, email: {email}, phoneNumbe: {phoneNumber}, bank: {bankAccount}")

    return {"message": "Registration successful"}
