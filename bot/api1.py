from fastapi import FastAPI
import httpx

app = FastAPI()


def get_all_currency():
    url = "http://localhost:8000/registration"
    headers = {"Content-Type": "application/json"}
    try:
        response = httpx.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(data)
            return {"message": "Data from Microservice 2", "data": data}
        else:
            return {"error": response}
    except httpx.HTTPError as e:
        return {"error": f"HTTP error occurred: {e}"}

def get_uncompleted_offers():
    url = "http://localhost:8000/get_uncompleted_offers"
    headers = {"Content-Type": "application/json"}
    try:
        response = httpx.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['offers']
        else:
            return {"error": response}
    except httpx.HTTPError as e:
        return {"error": f"HTTP error occurred: {e}"}

def show_wallet(user_id):
    url = "http://localhost:8000/show_wallet"
    headers = {"Content-Type": "application/json"}
    body = {'user_id': user_id}

    try:
        response = httpx.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['wallet']
        else:
            return {"error": response}
    except httpx.HTTPError as e:
        return {"error": f"HTTP error occurred: {e}"}


def add_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate):
    url = "http://localhost:8000/add_offer"
    headers = {"Content-Type": "application/json"}
    body = {
        'user_id': user_id,
        'selled_currency_id': selled_currency_id,
        'value': value,
        'wanted_currency_id': wanted_currency_id,
        'exchange_rate': exchange_rate
        }
    try:
        response = httpx.post(url, json=body, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['matches']
        else:
            return {"error": response}
    except httpx.HTTPError as e:
        return {"error": f"HTTP error occurred: {e}"}

