import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x300")

label = ctk.CTkLabel(app, text="Hello World")
label.pack(pady=20)

button = ctk.CTkButton(app, text="Click Me")
button.pack(pady=10)

app.mainloop()