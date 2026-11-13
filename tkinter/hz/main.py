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
        self.root.bind('<Escape>', lambda e: self.close())

        self.cells = Canvas(self.root, bg="#0004FF", highlightthickness=0)
        self.cells.pack(fill=BOTH, expand=True)

        self.connection = None
        self.provinces = []
        self.buttons = []

        self.database_create()
        self.load_provinces()
        self.draw_grid()
        self.create_buttons()

    def database_create(self):
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
                name VARCHAR(100) UNIQUE,
                recruits INT,
                money FLOAT
            )
        """)
        self.connection.commit()
        cursor.close()

    def load_provinces(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM provinces")
        if cursor.fetchone()[0] == 0:
            data = [
                (f"№ {i}", random.randint(100, 1000), round(random.uniform(1.0, 100.0), 2))
                for i in range(144)
            ]
            cursor.executemany(
                "INSERT INTO provinces (name, recruits, money) VALUES (%s, %s, %s)",
                data
            )
            self.connection.commit()

        cursor.execute("SELECT id, name, recruits, money FROM provinces ORDER BY id")
        self.provinces = cursor.fetchall()
        cursor.close()

    def update_province(self, province_id, recruits, money):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE provinces SET recruits = %s, money = %s WHERE id = %s",
            (recruits, money, province_id)
        )
        self.connection.commit()
        cursor.close()

    def draw_grid(self):
        self.cells.delete("all")
        for y in range(0, 1080, 120):
            for x in range(0, 1920, 120):
                self.cells.create_rectangle(
                    x, y, x + 118, y + 118,
                    fill="#201F24", outline="#7D7C8A"
                )

    def create_buttons(self):
        for i, (pid, name, recruits, money) in enumerate(self.provinces):
            x = (i % 16) * 120
            y = (i // 16) * 120
            btn = Button(
                self.root,
                text=name,
                command=lambda p=pid, cx=x, cy=y: self.click_province(p, cx, cy),
                bg="#201F24",
                fg="#FFFFFF",
                font=("Times New Roman", 12)
            )
            btn.place(x=x + 10, y=y + 10, width=100, height=25)
            self.buttons.append(btn)

    def click_province(self, province_id, x, y):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT name, recruits, money FROM provinces WHERE id = %s",
            (province_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return

        name, recruits, money = row
        self.cells.delete("info")
        self.cells.create_text(
            x + 59, y + 75,
            text=f"{name}\nРекруты: {recruits}\nДеньги: {money:.2f}",
            fill="#FFFFFF",
            font=("Times New Roman", 10),
            justify="center",
            tags="info"
        )

    def close(self):
        if self.connection:
            self.connection.close()
        self.root.destroy()


def main():
    root = Tk()
    World(root)
    root.mainloop()


if __name__ == "__main__":
    main()
