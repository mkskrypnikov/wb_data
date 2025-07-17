import os
import json
import time
import requests
from datetime import datetime as dt, timedelta
from dotenv import load_dotenv


class WbAnalyticsClient:
    BASE_URL = "https://seller-analytics-api.wildberries.ru/api/v2/stocks-report/products/products"

    def __init__(self, token: str):
        if not token:
            raise ValueError("API token is required")
        self.token = token
        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }

    def get_stock_report(
        self,
        start_date: str,
        end_date: str,
        offset: int = 0,
        limit: int = 150
    ) -> dict:
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
            "limit": limit,
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

        response = requests.post(
            self.BASE_URL, headers=self.headers, json=payload)
        print(f"[{response.status_code}] offset={offset}")
        response.raise_for_status()
        return response.json()

    def get_all_stock_reports(
        self,
        start_date: str,
        end_date: str,
        limit: int = 150
    ) -> list:
        offset = 0
        all_data = []

        while True:
            try:
                result = self.get_stock_report(
                    start_date, end_date, offset=offset, limit=limit)
            except requests.HTTPError as e:
                if e.response.status_code == 429:
                    print("⏳ Превышен лимит запросов (429). Ждём 60 секунд")
                    time.sleep(60)
                    continue
                else:
                    raise

            data = result.get("data", [])
            if not data:
                print("✅ Все страницы загружены.")
                break

            all_data.extend(data)
            offset += limit

            # Не более 3 запросов в минуту
            time.sleep(20)

        return all_data

    @staticmethod
    def save_to_json(data: list, date_str: str, folder: str = "data"):
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"stocks_{date_str}.json")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Данные сохранены в {filename}")


def get_yesterday_date_str() -> str:
    yesterday = dt.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def main():
    load_dotenv()
    token = os.getenv("TOKEN")

    if not token:
        print("❌ Токен не найден")
        return

    client = WbAnalyticsClient(token)
    date_str = get_yesterday_date_str()

    try:
        all_data = client.get_all_stock_reports(
            start_date=date_str, end_date=date_str)
        print(f"\n✅ Получено записей: {len(all_data)}")
        client.save_to_json(all_data, date_str)
    except requests.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")


if __name__ == "__main__":
    main()
