import tkinter as tk
from tkinter import ttk, messagebox


class TransferView(tk.Toplevel):
    def __init__(self, user_controller):
        super().__init__()
        self.user_controller = user_controller
        self.title("Transferir Dinero")
        self.geometry("500x350")
        self.resizable(False, False)

        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Cuenta origen
        tk.Label(main_frame, text="Cuenta Origen:").grid(row=0, column=0, sticky="w", pady=5)
        self.cuenta_origen_var = tk.StringVar()
        self.cuenta_origen_combo = ttk.Combobox(main_frame, textvariable=self.cuenta_origen_var, state="readonly")
        self.cuenta_origen_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Cuenta destino
        tk.Label(main_frame, text="Cuenta Destino:").grid(row=1, column=0, sticky="w", pady=5)
        self.cuenta_destino_var = tk.StringVar()
        self.cuenta_destino_combo = ttk.Combobox(main_frame, textvariable=self.cuenta_destino_var, state="readonly")
        self.cuenta_destino_combo.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Monto
        tk.Label(main_frame, text="Monto:").grid(row=2, column=0, sticky="w", pady=5)
        self.monto_entry = tk.Entry(main_frame)
        self.monto_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Nota
        tk.Label(main_frame, text="Nota:").grid(row=3, column=0, sticky="nw", pady=5)
        self.nota_text = tk.Text(main_frame, height=4, width=30)
        self.nota_text.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Botones
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        self.transfer_button = tk.Button(button_frame, text="Transferir", command=self.transferir)
        self.transfer_button.pack(side="left", padx=10)

        self.cancel_button = tk.Button(button_frame, text="Cancelar", command=self.destroy)
        self.cancel_button.pack(side="left", padx=10)


        main_frame.columnconfigure(1, weight=1)


        self.cargar_todas_las_cuentas()

    def cargar_todas_las_cuentas(self):
        """Carga todas las cuentas activas del sistema"""
        todas_las_cuentas = self.user_controller.account_model.get_todas_las_cuentas_activas()

        cuentas_lista = []
        for cuenta in todas_las_cuentas:

            cuenta_info = f"{cuenta['account_number']} - {cuenta['firstname']} {cuenta['lastname']} (Saldo: ${cuenta['balance']:.2f})"
            cuentas_lista.append(cuenta_info)


        self.cuenta_origen_combo['values'] = cuentas_lista
        self.cuenta_destino_combo['values'] = cuentas_lista

        if cuentas_lista:
            self.cuenta_origen_combo.set(cuentas_lista[0])
            if len(cuentas_lista) > 1:
                self.cuenta_destino_combo.set(cuentas_lista[1])

    def extraer_numero_cuenta(self, cuenta_completa):
        if cuenta_completa:
            return cuenta_completa.split(' - ')[0]
        return ""

    def transferir(self):
        cuenta_origen_completa = self.cuenta_origen_var.get()
        cuenta_destino_completa = self.cuenta_destino_var.get()
        monto_text = self.monto_entry.get()
        nota = self.nota_text.get("1.0", tk.END).strip()


        cuenta_origen = self.extraer_numero_cuenta(cuenta_origen_completa)
        cuenta_destino = self.extraer_numero_cuenta(cuenta_destino_completa)

        # Validaciones
        if not all([cuenta_origen, cuenta_destino, monto_text]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if cuenta_origen == cuenta_destino:
            messagebox.showerror("Error", "No puede transferir a la misma cuenta")
            return

        try:
            monto = float(monto_text)
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser positivo")
                return
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido")
            return

        # Confirmar transferencia
        confirmacion = messagebox.askyesno(
            "Confirmar Transferencia",
            f"¿Está seguro de transferir ${monto:.2f}?\n\n"
            f"De: {cuenta_origen_completa}\n"
            f"A: {cuenta_destino_completa}"
        )

        if not confirmacion:
            return

        # Realizar transferencia
        success = self.user_controller.account_model.transferir_dinero(
            cuenta_origen, cuenta_destino, monto, nota
        )

        if success:
            messagebox.showinfo("Éxito", "Transferencia realizada correctamente")
            self.destroy()
            self.user_controller.refresh_account_view()