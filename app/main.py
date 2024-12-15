import streamlit as st
from interface import main as ui_main
from db import initialize_database, seed_database

def initialize():
    """Inicialización de la base de datos y datos ficticios."""
    # Inicializar base de datos
    initialize_database()
    
    # Cargar datos ficticios (opcional)
    seed_database()

def main():
    """Función principal que ejecuta la aplicación Streamlit."""
    # Inicializar solo al primer inicio o en condiciones necesarias
    if "initialized" not in st.session_state:
        # Ejecuta la inicialización solo si no ha sido marcada como inicializada
        initialize()
        st.session_state.initialized = True
        st.success("Base de datos inicializada y datos cargados.")

    # Llamada a la interfaz de usuario
    ui_main()

if __name__ == "__main__":
    main()
