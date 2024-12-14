import sqlite3
import pandas as pd
from contextlib import contextmanager

@contextmanager
def get_connection():
    """Establece una conexión con la base de datos y la cierra automáticamente."""
    conn = None
    try:
        conn = sqlite3.connect('database/chatbot.db')
        yield conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise
    finally:
        if conn:
            conn.close()

def execute_query(query, params=None):
    """Ejecuta una consulta SQL de tipo INSERT, UPDATE o DELETE."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount  # Retorna la cantidad de filas afectadas
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None

def fetch_query(query, params=None):
    """Ejecuta una consulta SELECT y devuelve los resultados."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()  # Devuelve todos los resultados de la consulta
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []

def export_to_excel(query, filename="reporte.xlsx"):
    """Exporta los resultados de una consulta SQL a un archivo Excel."""
    try:
        with get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            df.to_excel(filename, index=False)
            return filename
    except Exception as e:
        print(f"Error al exportar a Excel: {e}")
        return None
