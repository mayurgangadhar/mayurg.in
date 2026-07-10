import tkinter as tk

root = tk.Tk()
root.geometry("400x250")
root.title("Tk Test")

label = tk.Label(root, text="Hello World", bg="yellow", fg="black")
label.pack(pady=20)

button = tk.Button(root, text="Click Me")
button.pack()

print("Widgets created")

root.mainloop()