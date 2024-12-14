import streamlit as st
from nlp import process_user_query  # Usaremos la función que ya tienes definida para procesar consultas

def authenticate_user():
    """Autenticación básica en Streamlit."""
    username = st.text_input("Nombre de usuario:", value="")
    password = st.text_input("Contraseña:", type="password")
    return username == "admin" and password == "1234"

def main():
    """Función principal para la interfaz de usuario."""
    st.title("Asistente de Consultas SQL con IA")

    # Autenticación de usuario
    if authenticate_user():
        st.success("Acceso autorizado")

        # Solicitar consulta al usuario
        user_input = st.text_input("Escribe tu consulta en lenguaje natural:")

        if user_input:
            try:
                # Llamamos a la función de procesamiento de la consulta en lenguaje natural
                result = process_user_query(user_input)
                if result:
                    st.write("Resultado procesado:")
                    st.write(result)
                else:
                    st.error("Lo siento, no pude generar una consulta SQL válida.")
            except Exception as e:
                st.error(f"Hubo un error al procesar la consulta: {e}")

        # Botón para exportar resultados (aún no implementado en este caso)
        if st.button("Exportar resultados"):
            st.write("Esta función aún está en desarrollo.")
    else:
        st.error("Acceso denegado. Por favor, verifica tus credenciales.")

if __name__ == "__main__":
    main()
