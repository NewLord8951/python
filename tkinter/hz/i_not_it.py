import os
import random
from dotenv import find_dotenv, load_dotenv
import mysql.connector

load_dotenv(find_dotenv())

TOTAL_CELLS = 16 * 9


def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("password"),
        database="tkinterbd"
    )


def show_all(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, recruits, money FROM provinces ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    if not rows:
        print("Таблица пуста.")
        return
    print(f"{'id':<5}{'name':<15}{'recruits':<10}{'money'}")
    for pid, name, recruits, money in rows:
        print(f"{pid:<5}{name:<15}{recruits:<10}{money:.2f}")
    print(f"Всего строк: {len(rows)}")


def add_one(conn):
    name = input("Название: ").strip()
    if not name:
        print("Название не может быть пустым.")
        return
    try:
        recruits = int(input("Рекруты (целое число): "))
        money = float(input("Деньги (число): ").replace(",", "."))
    except ValueError:
        print("Ошибка: нужно ввести число.")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO provinces (name, recruits, money) VALUES (%s, %s, %s)",
            (name, recruits, money)
        )
        conn.commit()
        print(f"Добавлено, id = {cursor.lastrowid}")
    except mysql.connector.IntegrityError:
        print("Ошибка: провинция с таким названием уже есть (name должно быть уникальным).")
    finally:
        cursor.close()


def delete_one(conn):
    try:
        pid = int(input("id для удаления: "))
    except ValueError:
        print("Ошибка: id должен быть числом.")
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM provinces WHERE id = %s", (pid,))
    conn.commit()
    print("Удалено." if cursor.rowcount else "Строки с таким id нет.")
    cursor.close()


def delete_all(conn):
    if input("Удалить ВСЕ данные? Напиши 'да': ").strip().lower() != "да":
        print("Отменено.")
        return
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE provinces")
    conn.commit()
    cursor.close()
    print("Таблица очищена.")


def regenerate(conn):
    """Очистить таблицу и заполнить заново случайными данными для всех клеток."""
    if input("Это сотрёт текущие данные. Напиши 'да': ").strip().lower() != "да":
        print("Отменено.")
        return
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE provinces")
    data = [
        (f"№ {i}", random.randint(100, 1000), round(random.uniform(1.0, 100.0), 2))
        for i in range(TOTAL_CELLS)
    ]
    cursor.executemany(
        "INSERT INTO provinces (name, recruits, money) VALUES (%s, %s, %s)",
        data
    )
    conn.commit()
    cursor.close()
    print(f"Создано {TOTAL_CELLS} строк.")


def main():
    conn = connect()
    actions = {
        "1": ("Показать все", show_all),
        "2": ("Добавить одну провинцию", add_one),
        "3": ("Удалить одну по id", delete_one),
        "4": ("Удалить все", delete_all),
        "5": ("Заполнить заново случайными данными", regenerate),
    }
    try:
        while True:
            print("\n--- Меню ---")
            for key, (title, _) in actions.items():
                print(f"{key}. {title}")
            print("0. Выход")
            choice = input("Выбор: ").strip()
            if choice == "0":
                break
            if choice in actions:
                actions[choice][1](conn)
            else:
                print("Нет такого пункта.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()