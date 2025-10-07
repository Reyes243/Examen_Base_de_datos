import tkinter as tk
from tkinter import ttk, messagebox


class DepositView(tk.Toplevel):
    def __init__(self, user_controller, cuenta_number):
        super().__init__()
        self.user_controller = user_controller
        self.cuenta_number = cuenta_number
        self.title(f"Depositar Dinero - Cuenta {cuenta_number}")
        self.geometry("400x250")
        self.resizable(False, False)

        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Información de la cuenta
        tk.Label(main_frame, text=f"Cuenta: {cuenta_number}", font=("Arial", 10, "bold")).grid(row=0, column=0,
                                                                                               columnspan=2, pady=10)

        # Monto
        tk.Label(main_frame, text="Monto a depositar:").grid(row=1, column=0, sticky="w", pady=10)
        self.monto_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.monto_entry.grid(row=1, column=1, sticky="ew", pady=10, padx=(10, 0))

        # Nota
        tk.Label(main_frame, text="Nota:").grid(row=2, column=0, sticky="w", pady=10)
        self.nota_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.nota_entry.grid(row=2, column=1, sticky="ew", pady=10, padx=(10, 0))

        # Botones
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        self.deposit_button = tk.Button(button_frame, text="Depositar", command=self.depositar)
        self.deposit_button.pack(side="left", padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", command=self.destroy)
        self.cancel_button.pack(side="left", padx=10)


        main_frame.columnconfigure(1, weight=1)

    def depositar(self):
        monto_text = self.monto_entry.get()
        nota = self.nota_entry.get()

        if not monto_text:
            messagebox.showerror("Error", "Por favor ingrese un monto")
            return

        try:
            monto = float(monto_text)
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser positivo")
                return
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
            return

        # Realizar depósito
        success = self.user_controller.account_model.depositar_dinero(
            self.cuenta_number, monto, nota
        )

        if success:
            messagebox.showinfo("Éxito", "Depósito realizado correctamente")
            self.destroy()
            self.user_controller.refresh_account_view()