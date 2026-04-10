def ivp(password):
    
    # password = input("Введите: ")
    if password is None or len(password) != 8:
        return False
    
    has_digit = False
    has_upper_case = False
    
    for char in password:
        if char.isdigit():
            has_digit = True
        if char.isupper():
            has_upper_case = True
        if has_digit and has_upper_case:
            break
            
    return has_digit and has_upper_case

# if(__name__ == "__main__"):
a = (input("Введите: "))
ivp(a)