import requests
import json
import pandas as pd

# 1. Запрос к API
url = "https://api.hh.ru/vacancies"  # ← без пробелов!
params = {"text": "Python", "area": 1, "per_page": 10}
headers = {"User-Agent": "HH-API-Client/1.0"}

try:
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # вызовет исключение при HTTP ошибке
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к API: {e}")
    exit(1)

# Проверка: точно ли пришли вакансии?
if 'items' not in data:
    print("Ошибка: API не вернул ожидаемые данные.")
    print("Ответ сервера:", data)
    exit(1)

# 2. Вывод в консоль
print(f"Найдено вакансий: {data.get('found', 'N/A')}")

for vacancy in data['items']:
    salary = vacancy.get('salary')
    if salary:
        from_sal = salary.get('from')
        to_sal = salary.get('to')
        currency = salary.get('currency', '')
        salary_info = f"{from_sal or ''} - {to_sal or ''} {currency}".strip()
        # Убираем лишние дефисы, если одно из значений None
        if from_sal is None and to_sal is not None:
            salary_info = f"до {to_sal} {currency}"
        elif to_sal is None and from_sal is not None:
            salary_info = f"от {from_sal} {currency}"
        elif from_sal is None and to_sal is None:
            salary_info = "не указана"
    else:
        salary_info = "не указана"

    print(f"📌 {vacancy['name']} | {salary_info}")

# 3. Сохранение в JSON
with open("hh_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 4. Сохранение в Excel
vacancies_list = []
for vacancy in data['items']:
    salary = vacancy.get('salary') or {}
    vacancies_list.append({
        'Название': vacancy['name'],
        'Компания': vacancy['employer']['name'],
        'Зарплата_от': salary.get('from'),
        'Зарплата_до': salary.get('to'),
        'Город': vacancy['area']['name'],
        'Ссылка': vacancy['alternate_url']
    })

df = pd.DataFrame(vacancies_list)
df.to_excel("hh_vacancies.xlsx", index=False)

print("Готово! Файлы созданы: hh_data.json и hh_vacancies.xlsx")
