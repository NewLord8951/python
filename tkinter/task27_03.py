import tkinter as tk

def increment():
    current_value = int(label_number["text"])
    label_number.config(text=str(current_value + 1))
def decrement():
    current_value = int(label_number["text"])
    label_number.config(text=str(current_value - 1))
root = tk.Tk()
root.title("А")
root.resizable(False, False)
window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
label_number = tk.Label(root, text="0", font=("Helvetica", 24))
label_number.pack(pady=20)
btn_plus = tk.Button(root, text="+", font=("Helvetica", 14), command=increment)
btn_plus.pack(pady=5)
btn_minus = tk.Button(root, text="-", font=("Helvetica", 14), command=decrement)
btn_minus.pack(pady=5)
root.mainloop()