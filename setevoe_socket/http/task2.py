import requests

def aa(a):
    b = requests.get(a)
    c = b.status_code
    if(c == 200):
        print("Правда пошёл на")
    else:
        print("Нет иди на")

a = "https://journal.top-academy.ru/index"
aa(a)