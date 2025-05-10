from typing import List, Dict
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")


SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = "/etc/secrets/credentials.json"  # ← обязательно абсолютный путь!


creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPE)
client = gspread.authorize(creds)

# Получение цен по городу и парку
def get_prices_for_park(city: str, park: str) -> List[Dict]:
    try:
        sheet = client.open_by_key(SPREADSHEET_NAME).worksheet("Цены")
        data = sheet.get_all_records()

        norm_city = city.strip().lower()
        norm_park = park.strip().lower()

        filtered = [
            row for row in data
            if row.get("Город", "").strip().lower() == norm_city
            and row.get("Парк", "").strip().lower() == norm_park
        ]

        return filtered

    except Exception as e:
        print(f"Ошибка при получении цен: {e}")
        return []

# Получение адреса, транспорта и режима работы
def get_address_for_park(city, park):
    try:
        sheet = client.open_by_key(SPREADSHEET_NAME).worksheet("Адреса")
        records = sheet.get_all_records()

        print("[DEBUG] Всего записей в таблице Адреса:", len(records))

        for row in records:
            print("[DEBUG] row:", row)
            print("[DEBUG] Сравниваем с ->", f"Город: {city} | Парк: {park}")

            if row.get("Город", "").strip() == city.strip() and row.get("Парк", "").strip() == park.strip():
                print("[DEBUG] ⬅️ Найдено совпадение!")
                return {
                    "Адрес": row.get("Адрес", "—"),
                    "Навигатор": row.get("Навигатор", "—"),
                    "Транспорт": row.get("Общественный транспорт", "—"),
                    "Режим работы": row.get("Режим работы", "—").strip()  # ← учитываем пробел
                }

        print("[DEBUG] ❌ Совпадений не найдено")
        return None

    except Exception as e:
        print("[DEBUG] Ошибка при работе с таблицей адресов:", e)
        return None
