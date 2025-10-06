from db.db_connector import DBConnector
from tkinter import messagebox
from mysql.connector import Error, IntegrityError


class UserModel:
    def __init__(self):
        pass

    def create_user(self, username, password, firstname, lastname):
        conn = DBConnector.get_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            args = (username, password, firstname, lastname)
            cursor.callproc('SP_STORE_USER', args)
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario '{username}' registrado correctamente.")
            return True
        except IntegrityError:
            messagebox.showerror("Error", f"El usuario '{username}' ya existe.")
            return False
        except Error as e:
            messagebox.showerror("Error de registro", f"Ocurrió un error: {e}")
            return False
        finally:
            if conn.is_connected():
                conn.close()

    def login_user(self, username, password):
        conn = DBConnector.get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            args = (username, password)
            cursor.callproc('SP_LOGIN_USER', args)
            for result in cursor.stored_results():
                data = result.fetchone()
                return data
        except Error as e:
            messagebox.showerror("Error", f"Ocurrió un error al iniciar sesión: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()
