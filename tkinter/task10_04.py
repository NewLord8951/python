import tkinter as tk

def add_to_expression(value):
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current + value)

def clear_display():
    display.delete(0, tk.END)

def calculate():
    try:
        result = eval(display.get())
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Ошибка")

root = tk.Tk()
root.title("Калькулятор")
root.geometry("300x400")

display = tk.Entry(root, font=("Arial", 20), bd=10, insertwidth=4, width=14, borderwidth=0)
display.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('C', 4, 0), ('0', 4, 1), ('.', 4, 2), ('+', 4, 3)
]

for text, row, col in buttons:
    if text == 'C':
        action = clear_display
    else:
        action = lambda x=text: add_to_expression(x)
        
    tk.Button(root, text=text, font=("Arial", 16), padx=20, pady=20, command=action).grid(row=row, column=col, sticky="nsew")

tk.Button(root, text='=', font=("Arial", 16), command=calculate).grid(row=5, column=0, columnspan=4, sticky="nsew")

root.mainloop()
