import os
import random
from tkinter import *
from dotenv import find_dotenv, load_dotenv
import mysql.connector

load_dotenv(find_dotenv())


class World:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        self.cells = Canvas(self.root, bg="#0004FF", highlightthickness=0)
        self.cells.pack(fill=BOTH, expand=True)

        self.connection = None
        self.province = []
        self.database_create()

    def database_create(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=os.getenv("password"),
                database="tkinterbd"
            )
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS provinces (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    recruits INT,
                    money FLOAT
                )
            """)
            self.connection.commit()
            cursor.close()
        except mysql.connector.Error as e:
            print("БД недоступна: ", e)

    def square(self):
        self.cells.delete("all")
        for y in range(0, 1080, 120):
            for x in range(0, 1920, 120):
                self.cells.create_rectangle(
                    x, y, x + 118, y + 118,
                    fill="#201F24", outline="#7D7C8A"
                )

    def click_province(self, x, y, name):
        self.insert_db(name)
        self.cells.create_text(
            x + 59, y + 80,
            text=f"Добавлено:\n{name}",
            fill="#B61414",
            font=("Times New Roman", 10),
            justify="center"
        )

    def button(self):
        a = 0
        for y in range(0, 1080, 120):
            for x in range(0, 1920, 120):
                a += 1
                name = f"Провинция {a}"
                btn = Button(
                    self.root,
                    text=name,
                    command=lambda cx=x, cy=y, n=name: self.click_province(cx, cy, n),
                    bg="#201F24",
                    fg="#FFFFFF",
                    font=("Times New Roman", 12)
                )
                btn.place(x=x + 10, y=y + 10, width=100, height=25)
                self.province.append(btn)

    def insert_db(self, name):
        if not self.connection or not self.connection.is_connected():
            print("Нет подключения к БД")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM provinces WHERE name = %s", (name,))

            if cursor.fetchone() is None:
                recruits = random.randint(100, 10000)
                money = round(random.uniform(1.0, 100.0), 2)
                cursor.execute(
                    "INSERT INTO provinces (name, recruits, money) VALUES (%s, %s, %s)",
                    (name, recruits, money)
                )
                self.connection.commit()
                print(f"Успешно сохранено: {name}")
            else:
                print(f"{name} уже есть в базе данных")

            cursor.close()
        except mysql.connector.Error as e:
            print("Ошибка при работе с запросом: ", e)


def main():
    root = Tk()
    app = World(root)
    app.square()
    app.button()
    root.mainloop()


if __name__ == "__main__":
    main()