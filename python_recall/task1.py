from random import randint

class Library():
    def __init__(self, title="", author="", year=0):
        self.title = title
        self.author = author
        self.year = year
    
    def add_book(self):
        try:
            book = []
            isbn = randint(1000000000000, 9999999999999)
            self.isbn_string = str(isbn)
            self.title = input("Введите название книги: ")
            self.author = input("Введите автора книги: ")
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
            
    def search_book():
        # try:
            search_book = int(input("Ввдеите: 1(Поиск по названию), 2(Поиск по автору), 3(Поиск по году написания) "))
            if(search_book == 1):
                return 0
            elif(search_book == 2):
                return 1
            elif(search_book == 3):
                return 2
        # except:
        #     print("A")

list_list = []
while True:
    # try:
        vvod = int(input("Введите: 1(Ввести книгу), 2(Вывести книгу), 3(Найти книгу) 0(Выйти) "))
        book_ = Library()
        ll0 = list_list[]
        if(vvod == 1):
            list_list.append(book_.add_book())
        elif(vvod == 2):
            print(list_list)
        elif(vvod == 3):
            print(ll0)
        elif(vvod == 0):
            break
    # except:
    #     print("Hello World")