import tkinter as tk


class RegisterView(tk.Toplevel):
    def __init__(self, user_controller):
        super().__init__()
        self.user_controller = user_controller
        self.title("Registro de usuario")
        self.geometry("400x230")
        self.resizable(False, False)

        self.username_label = tk.Label(self, text="Usuario:")
        self.username_entry = tk.Entry(self)
        self.first_name_label = tk.Label(self, text="Nombre:")
        self.first_name_entry = tk.Entry(self)
        self.last_name_label = tk.Label(self, text="Apellido:")
        self.last_name_entry = tk.Entry(self)
        self.password_label = tk.Label(self, text="Contraseña:")
        self.password_entry = tk.Entry(self, show="*")
        self.register_button = tk.Button(self, text="Registrar", command=self.register_button_clicked)

        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.first_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.last_name_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.last_name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.password_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.register_button.grid(row=4, column=1, columnspan=2, pady=5)

    def register_button_clicked(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        firstname = self.first_name_entry.get()
        lastname = self.last_name_entry.get()
        self.user_controller.handle_register(username, password, firstname, lastname, self)
