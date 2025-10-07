import tkinter as tk
from tkinter import ttk, messagebox


class AccountView(tk.Toplevel):
    def __init__(self, user_controller):
        super().__init__()
        self.user_controller = user_controller
        self.title("Cuenta del usuario")
        self.geometry("700x500")
        self.resizable(False, False)

        main_frame = tk.Frame(self)
        main_frame.pack(pady=10, fill="both", expand=True)

        # Frame de botones superiores
        button_frame_top = tk.Frame(main_frame)
        button_frame_top.pack(pady=10)

        self.create_account_button = tk.Button(
            button_frame_top,
            text="Crear cuenta",
            font=("Arial", 10, "bold"),
            command=self.create_account
        )
        self.create_account_button.pack(side="left", padx=5)

        self.transfer_button = tk.Button(
            button_frame_top,
            text="Transferir dinero",
            font=("Arial", 10, "bold"),
            command=self.transfer_money
        )
        self.transfer_button.pack(side="left", padx=5)

        self.deposit_button = tk.Button(
            button_frame_top,
            text="Depositar dinero",
            font=("Arial", 10, "bold"),
            command=self.deposit_money
        )
        self.deposit_button.pack(side="left", padx=5)


        self.tree = ttk.Treeview(main_frame, columns=("numero", "saldo", "estado", "email"), show="headings", height=12)
        self.tree.heading("numero", text="Número de Cuenta")
        self.tree.heading("saldo", text="Saldo")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("email", text="Email")

        self.tree.column("numero", width=180)
        self.tree.column("saldo", width=100, anchor="center")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.column("email", width=180)
        self.tree.pack(pady=10)

        # Frame de botones inferiores
        button_frame_bottom = tk.Frame(main_frame)
        button_frame_bottom.pack(pady=5)

        self.movements_button = tk.Button(
            button_frame_bottom,
            text="Ver Movimientos de Cuenta Seleccionada",
            font=("Arial", 10, "bold"),
            command=self.show_movements
        )
        self.movements_button.pack(side="left", padx=5)

        self.refresh_button = tk.Button(
            button_frame_bottom,
            text="Actualizar Lista",
            font=("Arial", 10, "bold"),
            command=self.load_accounts
        )
        self.refresh_button.pack(side="left", padx=5)

        self.exit_button = tk.Button(self, text="Cerrar Sesión", command=self.exit_window)
        self.exit_button.pack(pady=5, side="bottom")

        self.load_accounts()

    def load_accounts(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        user_id = self.user_controller.current_user_id
        accounts = self.user_controller.account_model.get_accounts_by_user(user_id)

        for acc in accounts:
            self.tree.insert("", "end", values=(
                acc["account_number"],
                f"${acc['balance']:.2f}",
                acc["status"],
                acc["email"]
            ))

    def create_account(self):
        self.user_controller.show_create_account_window()

    def transfer_money(self):
        self.user_controller.show_transfer_window()

    def deposit_money(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una cuenta para depositar")
            return

        cuenta_number = self.tree.item(selection[0])['values'][0]
        self.user_controller.show_deposit_window(cuenta_number)

    def show_movements(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una cuenta")
            return

        cuenta_number = self.tree.item(selection[0])['values'][0]
        self.user_controller.show_movements_window(cuenta_number)

    def exit_window(self):
        self.user_controller.current_user_id = None
        self.destroy()
        self.user_controller.show_login_window()

