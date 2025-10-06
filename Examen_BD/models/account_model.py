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
