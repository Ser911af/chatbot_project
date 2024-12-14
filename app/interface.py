# Archivo: interface.py
# Descripción: Interfaz en Streamlit para la interacción con el usuario
import streamlit as st
from nlp import generate_sql_query, humanize_results

def authenticate_user():
    """Autenticación básica en Streamlit."""
    username = st.text_input("Nombre de usuario:", value="")
    password = st.text_input("Contraseña:", type="password")
    return username == "admin" and password == "1234"

def main():
    """Función principal para la interfaz de usuario."""
    st.title("Asistente Contable y Financiero")

    if authenticate_user():
        st.success("Acceso autorizado")
        user_input = st.text_input("Escribe tu consulta financiera o contable:")

        if user_input:
            sql_query = generate_sql_query(user_input)
            if sql_query:
                st.write("Generando consulta SQL...")
                result = humanize_results(sql_query)
                st.write(result)
            else:
                st.error("No entendí tu consulta. Por favor, sé más específico.")

        if st.button("Exportar resultados"):
            st.write("Esta función aún está en desarrollo.")
    else:
        st.error("Acceso denegado. Por favor, verifica tus credenciales.")

if __name__ == "__main__":
    main()
