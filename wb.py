import requests
from dotenv import load_dotenv
import os


def get_data(api_token: str) -> dict:
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }

    payload = {
        "stockType": "",
        "currentPeriod": {
            "start": "2025-07-17",
            "end": "2025-07-17"
        },
        "skipDeletedNm": True,
        "orderBy": {
            "field": "minPrice",
            "mode": "asc"
        },
        "limit": 150,
        "offset": 1,
        "availabilityFilters": [
            "deficient",
            "actual",
            "balanced",
            "nonActual",
            "nonLiquid",
            "invalidData"
        ],
    }

    res = requests.post(url, headers=headers, json=payload)

    print(res.status_code)
    return res.json()


def main():
    token = str(os.getenv('TOKEN'))
    print(get_data(token))


if __name__ == "__main__":
    load_dotenv()
    url = "https://seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/products"
    main()
