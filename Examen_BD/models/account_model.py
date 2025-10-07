from db.db_connector import DBConnector
from mysql.connector import Error, IntegrityError
from tkinter import messagebox

class AccountModel:
    def __init__(self):
        pass

    def create_account(self, user_id, email, firstname, lastname):
        conn = DBConnector.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            args = (user_id, email, firstname, lastname)
            cursor.callproc('SP_CREATE_ACCOUNT', args)
            conn.commit()

            return True
        except IntegrityError:
            messagebox.showerror("Error", "Error al generar la cuenta (número duplicado).")
            return False
        except Error as e:
            messagebox.showerror("Error", f"Ocurrió un error en la base de datos: {e}")
            return False
        finally:
            if conn.is_connected():
                conn.close()

    def get_accounts_by_user(self, user_id):
        conn = DBConnector.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT account_number, balance, status, email, firstname, lastname
                FROM accounts
                WHERE user_id = %s
            """, (user_id,))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            messagebox.showerror("Error", f"No se pudieron obtener las cuentas: {e}")
            return []
        finally:
            if conn.is_connected():
                conn.close()

    def get_todas_las_cuentas_activas(self):

        conn = DBConnector.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.account_number, a.balance, a.status, a.email, 
                       a.firstname, a.lastname, u.username
                FROM accounts a
                JOIN users u ON a.user_id = u.id
                WHERE a.status = 'activa'
                ORDER BY a.account_number
            """)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            messagebox.showerror("Error", f"No se pudieron obtener las cuentas: {e}")
            return []
        finally:
            if conn.is_connected():
                conn.close()

    def transferir_dinero(self, cuenta_origen, cuenta_destino, monto, nota):
        conn = DBConnector.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            args = (cuenta_origen, cuenta_destino, monto, nota)
            cursor.callproc('SP_TRANSFERIR_DINERO', args)
            conn.commit()

            return True
        except Error as e:

            error_msg = str(e)
            if "Saldo insuficiente" in error_msg:
                messagebox.showerror("Error", "Saldo insuficiente para realizar la transferencia")
            elif "Cuenta emisora bloqueada" in error_msg:
                messagebox.showerror("Error", "La cuenta emisora está bloqueada")
            elif "Cuenta receptora bloqueada" in error_msg:
                messagebox.showerror("Error", "La cuenta receptora está bloqueada")
            elif "Cuenta emisora no existe" in error_msg:
                messagebox.showerror("Error", "La cuenta emisora no existe")
            elif "Cuenta receptora no existe" in error_msg:
                messagebox.showerror("Error", "La cuenta receptora no existe")
            elif "No se puede transferir a la misma cuenta" in error_msg:
                messagebox.showerror("Error", "No se puede transferir a la misma cuenta")
            else:
                messagebox.showerror("Error", f"Error en transferencia: {e}")
            return False
        finally:
            if conn.is_connected():
                conn.close()

    def get_movimientos(self, cuenta_number):
        conn = DBConnector.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            args = (cuenta_number,)
            cursor.callproc('SP_CONSULTAR_MOVIMIENTOS', args)

            movimientos = []
            for result in cursor.stored_results():
                movimientos = result.fetchall()

            return movimientos
        except Error as e:
            messagebox.showerror("Error", f"No se pudieron obtener los movimientos: {e}")
            return []
        finally:
            if conn.is_connected():
                conn.close()

    def depositar_dinero(self, cuenta_number, monto, nota):
        conn = DBConnector.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            args = (cuenta_number, monto, nota)
            cursor.callproc('SP_DEPOSITAR_DINERO', args)
            conn.commit()
            # REMOVEMOS EL MESSAGEBOX AQUÍ - lo maneja la vista
            return True
        except Error as e:
            messagebox.showerror("Error", f"Error en depósito: {e}")
            return False
        finally:
            if conn.is_connected():
                conn.close()

    def get_saldo_cuenta(self, cuenta_number):
        conn = DBConnector.get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT balance, status FROM accounts 
                WHERE account_number = %s
            """, (cuenta_number,))
            result = cursor.fetchone()
            return result
        except Error as e:
            messagebox.showerror("Error", f"No se pudo obtener el saldo: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()