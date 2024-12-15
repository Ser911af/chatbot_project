import streamlit as st
from db import export_to_excel, fetch_query  # Importamos las funciones definidas en db.py
from nlp import process_user_query  # Función que convierte texto en consultas SQL
import os
import asyncio

# Estado global para autenticación
def authenticate_user():
    """
    Autenticación básica de usuario. Almacena el estado en session_state.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        username = st.text_input("Nombre de usuario:", key="user_input")
        password = st.text_input("Contraseña:", type="password", key="pass_input")

        if st.button("Iniciar sesión"):
            if username == "admin" and password == "1234":
                st.session_state.authenticated = True
                st.success("Acceso autorizado")
            else:
                st.error("Credenciales incorrectas. Inténtalo de nuevo.")
    return st.session_state.authenticated

def process_query_interface():
    """
    Interfaz para procesar consultas SQL desde lenguaje natural.
    """
    st.subheader("Consulta en Lenguaje Natural")
    user_input = st.text_input("Escribe tu consulta en lenguaje natural:")

    if user_input:
        try:
            # Ejecutamos la función asíncrona usando asyncio.run()
            sql_query = asyncio.run(process_user_query(user_input))
            st.text_area("Consulta SQL Generada:", sql_query, height=100)

            if sql_query:
                # Ejecutamos la consulta y mostramos resultados
                results = fetch_query(sql_query)  # Especificamos la ruta correcta
                if results:
                    st.write("Resultados:")
                    st.dataframe(results)
                else:
                    st.warning("La consulta no devolvió resultados.")

                # Opción para exportar los resultados
                if st.button("Exportar a Excel"):
                    filename = "resultados.xlsx"
                    export_to_excel(sql_query, filename)
                    st.success(f"Resultados exportados a {filename}")
                    with open(filename, "rb") as file:
                        st.download_button(
                            label="Descargar archivo Excel",
                            data=file,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    os.remove(filename)  # Limpieza del archivo temporal
            else:
                st.error("No se pudo generar una consulta SQL válida.")
        except Exception as e:
            st.error(f"Error al procesar la consulta: {e}")

def main():
    """
    Función principal para la interfaz de usuario.
    """
    st.title("Asistente de Consultas SQL con IA 🤖")
    st.write("Este asistente convierte lenguaje natural en consultas SQL y ejecuta resultados.")

    # Autenticación
    if authenticate_user():
        # Uso de pestañas para organizar las funcionalidades
        tab1, tab2 = st.tabs(["Consulta SQL", "Acerca de"])

        with tab1:
            process_query_interface()

        with tab2:
            st.subheader("Acerca del Asistente")
            st.write("""
            Esta aplicación utiliza inteligencia artificial para interpretar consultas en lenguaje natural 
            y convertirlas en consultas SQL válidas. Además, ejecuta dichas consultas sobre una base de datos 
            y permite exportar los resultados en formato Excel.
            
            **Características:**
            - Autenticación básica de usuario.
            - Generación automática de consultas SQL.
            - Ejecución de consultas en una base de datos SQLite.
            - Exportación de resultados a un archivo Excel.

            **Desarrollado con:**
            - Streamlit
            - SQLite
            - Pandas
            - Procesamiento de Lenguaje Natural (NLP)
            """)
    else:
        st.warning("Acceso restringido. Inicia sesión para continuar.")

if __name__ == "__main__":
    main()
