from tkinter import Tk, ttk, Toplevel, messagebox, END

def main():
    r = Tk()
    r.geometry("400x200")
    r.minsize(width=500, height=250)
    r.maxsize(width=500, height=250)
    r.title("Задание 1")
    r.rowconfigure([5, 2], weight=1)
    r.columnconfigure([0, 3], weight=1)
    r.rowconfigure([3, 2], weight=2)

    w = Toplevel(r)
    w.title("Окно")
    w.geometry("200x150")
    w.withdraw()

    label_w = ttk.Label(w, text=f"")
    label_w.grid(row=0, column=2, pady=20, padx=50, sticky="w")

    name_lable = ttk.Label(r, text="Имя:")
    name_lable.grid(row=1, column=1, padx=(0, 8))
    name = ttk.Entry(r, width=20)
    name.grid(row=1, column=2)

    group_lable = ttk.Label(r, text="Группа:")
    group_lable.grid(row=2, column=1, padx=(0, 8))
    group_s = ["Адын", "Дыва", "Тьри"]
    group = ttk.Combobox(r, values=group_s, state='readonly')
    group.grid(row=2, column=2)

    button = ttk.Button(r, text="Показать", command=lambda: (label_w.config(text=f"{name.get().strip()} {group.get().strip()}"), w.deiconify()) if name.get().strip() and group.get().strip() else messagebox.showwarning(title="Э", message="Всё должно быть заполнено"))
    button.grid(row=3, column=2, pady=10, sticky="w")

    del_button = ttk.Button(r, text="Очистить", command=lambda: name.delete(0, END))
    del_button.grid(row=3, column=3, pady=10, sticky="w")

    d_button = ttk.Button(w, text="Закрыть", command=w.withdraw)
    d_button.grid(row=1, column=2, pady=10, padx=50)

    r.mainloop()

if __name__ == "__main__":
    main()