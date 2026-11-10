import os
from tkinter import *
import mysql.connector
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
password = os.getenv("password")

class world:
    def spawn():
        global root
        root = Tk()
        root.attributes('-fullscreen', True)
        root.resizable(False, False)
        root.bind('<Escape>', lambda e: root.destroy())
        global countries
        countries = Canvas(root, bg="#131313", highlightthickness=0)
        countries.pack(fill=BOTH, expand=True)


    def square():
        for y in range(0, 1080, 120):
            for x in range(0, 1920, 120):
                countries.create_rectangle(x, y, x + 119, y + 119, fill="#000000", outline="#FFFFFF")

    def database():
        try:
            load_dotenv(find_dotenv())
            password = os.getenv("password")
        except Exception as e:
            print(".env полетела(       ", e)
            return None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=password,
                database="tkinterbd"
            )
        except mysql.connector.Error as e:
            print("Бд полетела(        ", e)
            return None

def main():
    world.spawn()
    world.square()
    world.database()
    root.mainloop()

if __name__ == "__main__":
    main()