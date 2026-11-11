import os
from tkinter import *
# import mysql.connector
# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())
# password = os.getenv("password")

class World:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        self.countries = Canvas(self.root, bg="#0004FF", highlightthickness=0)
        self.countries.pack(fill=BOTH, expand=True)

    def square(self):
        self.countries.delete("all")
        for y in range(0, 1080, 120):
            for x in range(0, 1920, 120):
                self.countries.create_rectangle(x, y, x + 118, y + 118, fill="#201F24", outline="#7D7C8A")

    def click_province(self):
        pass

    def button(self):
        a = 0
        self.province = list()
        for i in range(0, 1080, 120):
            for j in range(0, 1920, 120):
                a += 1
                btn = Button(
                    self.root, 
                    text=f"Провинция {a}", 
                    command=lambda current_x=j, current_y=i: self.click_province(current_x, current_y),
                    bg="#201F24", 
                    fg="#FFFFFF", 
                    font=("Times New Roman", 12)
                )
                btn.place(x=j+10, y=i+10, width=100, height=25)
                self.province.append(btn)

    # def database():
    #     try:
    #         load_dotenv(find_dotenv())
    #         password = os.getenv("password")
    #     except Exception as e:
    #         print(".env полетела(       ", e)
    #         return None
    #     try:
    #         connection = mysql.connector.connect(
    #             host="localhost",
    #             user="root",
    #             password=password,
    #             database="tkinterbd"
    #         )
    #         if connection.is_connected():
    #             cursor = connection.cursor()
    #             bdcreate = """
    #             CREATE TABLE IF NOT EXISTS provinces (
    #                 id INT AUTO_INCREMENT PRIMARY KEY,
    #                 name VARCHAR(100),
    #                 age INT
    #             )
    #             """
    #         cursor.execute(bdcreate)
    #     except mysql.connector.Error as e:
    #         print("Бд полетела(        ", e)
    #         return None

def main():
    root = Tk()
    app = World(root)
    app.square()
    app.button()
    root.mainloop()

if __name__ == "__main__":
    main()