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
