import requests
 
url = "https://jsonplaceholder.typicode.com/todos"
todos = requests.get(url, params={"userId": 1}, timeout=5).json()
 
for todo in todos:
    print(todo["title"])