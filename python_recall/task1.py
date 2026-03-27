from random import randint

class Library():
    def __init__(self, title="", author="", year=0, avaiable=True, times_borrowed=0):
        self.title = title
        self.author = author
        self.year = year
        self.avaiable = avaiable
        self.times_borrowed = times_borrowed
    
    def add_book(self):
        try:
            book = []
            isbn = randint(1000000000000, 9999999999999)
            self.isbn_string = str(isbn)
            self.title = input("Введите название книги: ")
            self.author = input("введите автора книги: ")
            self.year = int(input("Введите дату написания книги: "))
            if(self.year < 1900 or self.year > 2026):
                self.year = int(input("Введите дату от 1900 до 2026: "))
            else:
                self.year = self.year
            book.append(self.isbn_string)
            book.append(self.title)
            book.append(self.author)
            book.append(self.year)
            return book
        except:
            print("Cheese")

list_list = []
while True:
    try:
        vvod = int(input("Введите: 1(Ввести книгу), 2(Вывести книгу) 0(Выйти) "))
        if(vvod == 1):
            book_ = Library()
            list_list.append(book_.add_book())
        elif(vvod == 2):
            print(list_list)
        elif(vvod == 0):
            break
    except:
        print("Hello World")