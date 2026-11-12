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

    def insert_db(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM provinces")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO provinces (name, recruits, money) VALUES (%s, %s, %s)",
                list(zip(*self.prov))
            )
            self.connection.commit()
        else:
            cursor.execute("SELECT name, recruits, money FROM provinces ORDER BY id")
            self.prov = [list(col) for col in zip(*cursor.fetchall())]
        cursor.close()

    def square(self):
        self.cells.delete("all")
        for y in range(0, 1080, 120):
            for x in range(0, 1920, 120):
                self.cells.create_rectangle(
                    x, y, x + 118, y + 118,
                    fill="#201F24", outline="#7D7C8A"
                )

    def button(self):
        a = 0
        name = []
        recruits = []
        money = []
        self.prov = [[], [], []]
        for y in range(0, 1080, 120):
            for x in range(0, 1920, 120):
                name.append(f"№ {a}")
                recruits.append(random.randint(100, 1000))
                money.append(random.uniform(1.0, 100.0))
                self.prov[0].append(name[a])
                self.prov[1].append(recruits[a])
                self.prov[2].append(money[a])
                self.name_a = a
                btn = Button(
                    self.root,
                    text=name[a],
                    command=lambda n=name[a], cx=x, cy=y: self.click_province(n, cx, cy),
                    bg="#201F24",
                    fg="#FFFFFF",
                    font=("Times New Roman", 12)
                )
                btn.place(x=x + 10, y=y + 10, width=100, height=25)
                self.province.append(btn)
                a += 1
    
    def click_province(self):
        name = self.prov[0]
        recruits = self.prov[1]
        money = self.prov[2]
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE provinces SET recruits = %s, money = %s WHERE name = %s",
            (recruits[self.name_a], money[self.name_a], name[self.name_a])
        )
        self.connection.commit()
        cursor.close()

        self.cells.delete("info")
        self.cells.create_text(
            59, 75,
            text=f"{name}\n{recruits}\n{money}",
            fill="#FFFFFF",
            font=("Times New Roman", 10),
            justify="center",
            tags="info"
        )


def main():
    root = Tk()
    app = World(root)
    app.database_create()
    app.insert_db()
    app.square()
    app.button()
    app.click_province()
    root.mainloop()


if __name__ == "__main__":
    main()