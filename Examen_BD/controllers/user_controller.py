import tkinter as tk
from view.login_view import LoginView
from view.register_view import RegisterView
from view.account_view import AccountView
from view.create_account_view import CreateAccountView
from view.transfer_view import TransferView
from view.movements_view import MovementsView
from view.deposit_view import DepositView
from models.account_model import AccountModel
from tkinter import messagebox

class UserController:
    def __init__(self, user_model):
        self.user_model = user_model
        self.account_model = AccountModel()
        self.root = tk.Tk()
        self.root.withdraw()
        self.login_view = None
        self.register_view = None
        self.account_view = None
        self.current_user_id = None

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
        if not self.account_view or not self.account_view.winfo_exists():
            self.account_view = AccountView(self)
        self.account_view.lift()

    def show_create_account_window(self):
        CreateAccountView(self)

    def show_transfer_window(self):
        TransferView(self)

    def show_movements_window(self, cuenta_number):
        MovementsView(self, cuenta_number)

    def show_deposit_window(self, cuenta_number):
        DepositView(self, cuenta_number)

    def handle_register(self, username, password, firstname, lastname, window):
        if not all([username, password, firstname, lastname]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        if self.user_model.create_user(username, password, firstname, lastname):
            messagebox.showinfo("Éxito", "Usuario creado exitosamente")
            window.destroy()

    def handle_create_account(self, email, firstname, lastname, window):
        success = self.account_model.create_account(self.current_user_id, email, firstname, lastname)
        if success:
            messagebox.showinfo("Éxito", "Cuenta creada correctamente.")
            window.destroy()
            self.refresh_account_view()

    def refresh_account_view(self):
        if self.account_view and self.account_view.winfo_exists():
            self.account_view.load_accounts()
