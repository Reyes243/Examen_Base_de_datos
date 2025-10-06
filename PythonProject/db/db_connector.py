import mysql.connector
from mysql.connector import Error, IntegrityError
from config.db import DB_CONFIG
from tkinter import messagebox

class DBConnector:

    @staticmethod
    def get_connection():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar con el servidor {e}")
            return None
