import tkinter as tk
from tkinter import ttk


class AccountView(tk.Toplevel):
    def __init__(self, user_controller):
        super().__init__()
        self.user_controller = user_controller
        self.title("Cuenta del usuario")
        self.geometry("600x400")
        self.resizable(False, False)

        main_frame = tk.Frame(self)
        main_frame.pack(pady=10, fill="both", expand=True)

        self.create_account_button = tk.Button(
            main_frame,
            text="Crear cuenta",
            font=("Arial", 12, "bold"),
            command=self.create_account
        )
        self.create_account_button.pack(pady=10)

        self.tree = ttk.Treeview(main_frame, columns=("numero", "saldo", "estado", "email"), show="headings", height=10)
        self.tree.heading("numero", text="Número de Cuenta")
        self.tree.heading("saldo", text="Saldo")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("email", text="Email")

        self.tree.column("numero", width=180)
        self.tree.column("saldo", width=100, anchor="center")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.column("email", width=180)
        self.tree.pack(pady=10)

        self.exit_button = tk.Button(self, text="Salir", command=self.exit_window)
        self.exit_button.pack(pady=5, side="bottom")

        self.load_accounts()

    def load_accounts(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        user_id = self.user_controller.current_user_id
        accounts = self.user_controller.account_model.get_accounts_by_user(user_id)

        for acc in accounts:
            self.tree.insert("", "end", values=(acc["account_number"], acc["balance"], acc["status"], acc["email"]))

    def create_account(self):
        self.user_controller.show_create_account_window()

    def exit_window(self):
        self.destroy()

