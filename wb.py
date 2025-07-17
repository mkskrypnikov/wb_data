import os
import requests
from dotenv import load_dotenv
from datetime import datetime as dt, timedelta


def get_data(
    url: str,
    api_token: str,
    offset: int,
    start_date: str,
    end_date: str
) -> dict:
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }

    payload = {
        "stockType": "",
        "currentPeriod": {
            "start": start_date,
            "end": end_date
        },
        "skipDeletedNm": True,
        "orderBy": {
            "field": "minPrice",
            "mode": "asc"
        },
        "limit": 150,
        "offset": offset,
        "availabilityFilters": [
            "deficient",
            "actual",
            "balanced",
            "nonActual",
            "nonLiquid",
            "invalidData"
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"Status code: {response.status_code}")
    return response.json()


def main():
    url = "https://seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/products"
    token = os.getenv("TOKEN")

    if not token:
        raise ValueError("TOKEN not found in environment variables")

    today = dt.now()
    yesterday = today - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")

    offset = 0
    result = get_data(url, token, offset, date_str, date_str)
    print(result)


if __name__ == "__main__":
    load_dotenv()
    main()
