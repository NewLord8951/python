import requests

url = "https://jsonplaceholder.typicode.com/todos"
todos = requests.get(url, params={"userId": 1}, timeout=5).json()

done = 0
for todo in todos:
    if todo["completed"]:
        done += 1
 
print("Всего задач:", len(todos))
print("Выполнено:", done)
print("Процент:", round(done / len(todos) * 100), "%")