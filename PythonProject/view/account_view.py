import tkinter as tk
from tkinter import messagebox

class AccountView(tk.Toplevel):
    def __init__(self, user_controller):
        super().__init__()
        self.user_controller = user_controller

        self.title("Cuenta del usuario")
        self.geometry("500x300")
        self.resizable(False, False)


        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)


        self.create_account_button = tk.Button(
            main_frame,
            text="Crear cuenta",
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            command=self.create_account
        )
        self.create_account_button.pack(pady=40)


        self.exit_button = tk.Button(
            self,
            text="Salir",
            font=("Arial", 10),
            command=self.exit_window
        )
        self.exit_button.place(relx=0.95, rely=0.95, anchor="se")

    def create_account(self):
        messagebox.showinfo("Crear cuenta", "Aquí se creará una cuenta bancaria (por implementar).")

    def exit_window(self):
        self.destroy()
