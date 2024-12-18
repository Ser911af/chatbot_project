import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

def get_engine_for_database():
    """Conectar con la base de datos SQLite en la ruta especificada."""
    connection = sqlite3.connect("/workspaces/chatbot_project/database/database.db", check_same_thread=False)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

# Crear el motor de conexión con la base de datos real
engine = get_engine_for_database()
