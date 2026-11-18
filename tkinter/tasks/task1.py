from tkinter import Tk, ttk

def main():
    r = Tk()
    r.geometry("400x200")
    r.minsize(width=500, height=250)
    r.maxsize(width=500, height=250)
    r.title("Задание 1")
    r.rowconfigure([5, 2], weight=1)
    r.columnconfigure([0, 3], weight=1)
    r.rowconfigure([3, 2], weight=2)

    name_lable = ttk.Label(r, text="Имя:")
    name_lable.grid(row=1, column=1, padx=(0, 8))
    name = ttk.Entry(r, width=20)
    name.grid(row=1, column=2)

    group_lable = ttk.Label(r, text="Группа:")
    group_lable.grid(row=2, column=1, padx=(0, 8))
    group_s = ["Адын", "Дыва", "Тьри", ""]
    group = ttk.Combobox(r, values=group_s, state='readonly')
    group.grid(row=2, column=2)

    entry = ttk.Label(r, text="")
    entry.grid(row=3, column=1, pady=10, sticky="e")
    button = ttk.Button(r, text="Показать", command=lambda: entry.config(text=f"{name.get().strip()} {group.get().strip()}"),
    )
    button.grid(row=3, column=2, pady=10, sticky="w")
    

    r.mainloop()

if __name__ == "__main__":
    main()