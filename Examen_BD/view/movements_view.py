import tkinter as tk
from tkinter import ttk, messagebox


class MovementsView(tk.Toplevel):
    def __init__(self, user_controller, cuenta_number):
        super().__init__()
        self.user_controller = user_controller
        self.cuenta_number = cuenta_number
        self.title(f"Movimientos - Cuenta {cuenta_number}")
        self.geometry("800x400")
        self.resizable(True, True)

        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview para movimientos
        columns = ("tipo", "monto", "emisora", "receptora", "fecha", "nota")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

        # Configurar columnas
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("monto", text="Monto")
        self.tree.heading("emisora", text="Cuenta Emisora")
        self.tree.heading("receptora", text="Cuenta Receptora")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("nota", text="Nota")

        self.tree.column("tipo", width=100)
        self.tree.column("monto", width=80)
        self.tree.column("emisora", width=120)
        self.tree.column("receptora", width=120)
        self.tree.column("fecha", width=120)
        self.tree.column("nota", width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botón cerrar
        close_button = tk.Button(self, text="Cerrar", command=self.destroy)
        close_button.pack(pady=10)

        # Cargar movimientos
        self.cargar_movimientos()

    def cargar_movimientos(self):
        movimientos = self.user_controller.account_model.get_movimientos(self.cuenta_number)

        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar movimientos
        for mov in movimientos:
            self.tree.insert("", "end", values=(
                mov["tipo_movimiento"],
                f"${mov['monto']:.2f}",
                mov["cuenta_emisora"] or "",
                mov["cuenta_receptora"] or "",
                mov["fecha_operacion"].strftime("%Y-%m-%d %H:%M"),
                mov["nota"] or ""
            ))