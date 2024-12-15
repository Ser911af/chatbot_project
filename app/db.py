import sqlite3
import pandas as pd
import logging
from contextlib import contextmanager

# Configuración del sistema de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DB_PATH = "database/database.db"  # Ruta de la base de datos
SCHEMA_PATH = "database/schema.sql"  # Ruta del archivo SQL con el esquema
SEED_PATH = "database/seed.sql"  # Ruta del archivo SQL con los datos de prueba

@contextmanager
def get_connection():
    """
    Establece una conexión con la base de datos y la cierra automáticamente.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)  # Usamos la nueva ruta
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Error al conectar con la base de datos: {e}")
        raise
    finally:
        if conn:
            conn.close()

def execute_query(query, params=None):
    """
    Ejecuta una consulta SQL de tipo INSERT, UPDATE o DELETE.
    Retorna el número de filas afectadas.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            logger.info(f"Consulta ejecutada correctamente: {query}")
            return cursor.rowcount
    except sqlite3.Error as e:
        logger.error(f"Error al ejecutar la consulta: {e}")
        return None

def fetch_query(query, params=None):
    """
    Ejecuta una consulta SELECT y devuelve los resultados.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            logger.info(f"Consulta SELECT ejecutada: {query}")
            return results
    except sqlite3.Error as e:
        logger.error(f"Error al ejecutar la consulta: {e}")
        return []

def export_to_excel(query, filename="reporte.xlsx"):
    """
    Exporta los resultados de una consulta SQL a un archivo Excel.
    """
    try:
        with get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            df.to_excel(filename, index=False)
            logger.info(f"Datos exportados a Excel en el archivo: {filename}")
            return filename
    except Exception as e:
        logger.error(f"Error al exportar a Excel: {e}")
        return None

def get_schema_from_file():
    """
    Carga el esquema de las tablas desde el archivo SQL.
    """
    try:
        with open(SCHEMA_PATH, 'r') as schema_file:
            schema = schema_file.read()
            logger.info("Esquema de la base de datos cargado desde el archivo.")
            return schema
    except Exception as e:
        logger.error(f"Error al cargar el esquema desde el archivo: {e}")
        return None

def initialize_database():
    """
    Inicializa la base de datos creando las tablas según el esquema SQL.
    Si la base de datos ya existe, solo asegura que las tablas están creadas.
    """
    try:
        # Obtener el esquema desde el archivo
        schema = get_schema_from_file()
        if schema:
            # Establecemos la conexión con la base de datos
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.executescript(schema)  # Ejecutamos el script de creación de tablas
                logger.info("Base de datos inicializada con éxito.")
        else:
            logger.error("No se pudo cargar el esquema desde el archivo.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")

def seed_database():
    """
    Inserta datos de prueba en la base de datos desde el archivo seed.sql.
    """
    try:
        with open(SEED_PATH, 'r') as seed_file:
            seed_script = seed_file.read()
            # Ejecutar el script SQL del archivo seed.sql para insertar datos
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.executescript(seed_script)  # Ejecutamos el script de inserción de datos
                conn.commit()
                logger.info("Base de datos sembrada con datos de prueba desde el archivo seed.sql.")
    except Exception as e:
        logger.error(f"Error al sembrar la base de datos desde el archivo seed.sql: {e}")

# Ejecución principal opcional
if __name__ == "__main__":
    logger.info("Configuración completada.")
    # Inicializar la base de datos
    initialize_database()
    # Sembrar la base de datos con datos de prueba
    seed_database()
