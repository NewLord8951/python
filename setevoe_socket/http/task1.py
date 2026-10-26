import requests

a = "https://journal.top-academy.ru/index"
b = requests.get(a)

print("F ", b.status_code)
print("F ", b.headers["Content-Type"])
print("F ", b.text)
