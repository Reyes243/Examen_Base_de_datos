import tkinter as tk
from tkinter import messagebox


class CreateAccountView(tk.Toplevel):
    def __init__(self, user_controller):
        super().__init__()
        self.user_controller = user_controller
        self.title("Crear cuenta bancaria")
        self.geometry("400x300")
        self.resizable(False, False)

        tk.Label(self, text="Correo electrónico:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Label(self, text="Nombre:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        tk.Label(self, text="Apellido:").grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.email_entry = tk.Entry(self)
        self.firstname_entry = tk.Entry(self)
        self.lastname_entry = tk.Entry(self)

        self.email_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.firstname_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.lastname_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.create_button = tk.Button(self, text="Crear cuenta", command=self.create_account)
        self.create_button.grid(row=3, column=0, columnspan=2, pady=20)

    def create_account(self):
        email = self.email_entry.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()

        if not all([email, firstname, lastname]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        success = self.user_controller.account_model.create_account(
            self.user_controller.current_user_id, email, firstname, lastname
        )

        if success:
            messagebox.showinfo("Éxito", "Cuenta creada correctamente.")
            self.destroy()
            self.user_controller.refresh_account_view()