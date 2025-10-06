import tkinter as tk
from view.login_view import LoginView
from view.register_view import RegisterView
from view.account_view import AccountView
from tkinter import messagebox


class UserController:
    def __init__(self, user_model):
        self.user_model = user_model
        self.root = tk.Tk()          # raíz única
        self.root.withdraw()         # oculta la raíz
        self.login_view = None
        self.register_view = None

    def run(self):
        self.show_login_window()
        self.root.mainloop()

    def show_login_window(self):
        if self.login_view is None or not self.login_view.winfo_exists():
            self.login_view = LoginView(self)
        self.login_view.lift()

    def show_register_window(self):
        if self.register_view is None or not self.register_view.winfo_exists():
            self.register_view = RegisterView(self)
        self.register_view.lift()

    def show_account_window(self):
        account_view = AccountView(self)
        account_view.lift()

    def handle_register(self, username, password, firstname, lastname, window):
        if not all([username, password, firstname, lastname]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        if self.user_model.create_user(username, password, firstname, lastname):
            messagebox.showinfo("Success", "Usuario creado exitosamente")
            window.destroy()
