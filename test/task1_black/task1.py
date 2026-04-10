def calculate_discount(a):
    if(a < 1000):
        return(a)
    elif(a >= 1000 and a < 5000):
        return(a - (a * 0.05))
    elif(a >= 5000 and a < 10000):
        return(a - (a * 0.1))
    elif(a >= 10000):
        return(a - (a * 0.15))
    else:
        print("Пошёл нахуй")

if(__name__ == "__main__"):
    a = int(input("Введите сумму покупки: ")) 
    calculate_discount(a)