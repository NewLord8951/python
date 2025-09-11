import json


# 1. Переменные
name = "Софья"
age = 15
fs = "перерыв"
print(f"меня зовут{name}, мне {age}, мой любимый предмет {fs}")

# 2. Файлы
with open('my_info.txt', 'w', encoding='utf-8') as file:
    file.write("1. У меня есть собака\n")
    file.write("2. У меня есть кот\n")
    file.write("3. у меня был хомяк\n")

# 3. Строки
with open('my_info.txt', 'r', encoding='utf-8') as file:
    content = file.read()

upper_case = content.upper()

with open('shout_info.txt', 'w', encoding='utf-8') as file:
    file.write(upper_case)

# 4. JSON
data = {
    "name": "Кот",
    "age": 10,
    "color": "grey"
}

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)

with open("data.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)

print(loaded_data["name"])
print(loaded_data["color"])
