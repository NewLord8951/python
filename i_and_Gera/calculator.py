def simple_calculator():
    print("Простой калькулятор")
    print("Доступные операции: +, -, *, /")
    print("Для выхода введите 'exit'")
    
    while True:
        try:
            expression = input("Введите выражение (например: 2 + 3): ")
            
            if expression.lower() == 'exit':
                print("Выход из калькулятора")
                break
            
            parts = expression.split()
            
            if len(parts) != 3:
                print("Ошибка: введите выражение в формате 'число оператор число'")
                continue
            
            num1 = float(parts[0])
            operator = parts[1]
            num2 = float(parts[2])
            
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    print("Ошибка: деление на ноль!")
                    continue
                result = num1 / num2
            else:
                print("Ошибка: неизвестный оператор")
                continue
            
            print(f"Результат: {result}")
            
        except ValueError:
            print("Ошибка: введите корректные числа")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    simple_calculator()