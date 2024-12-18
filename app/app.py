# app.py

import os
import streamlit as st
from tools import tools  # Importar las herramientas definidas en tools.py
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Cargar la plantilla de prompt desde LangChain Hub
from langchain import hub
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
assert len(prompt_template.messages) == 1
system_message = prompt_template.format(dialect="SQLite", top_k=5)

# Inicializar el modelo LLM con la API Key
llm = ChatOpenAI(model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))  # Asegurarse de usar la API Key

# Crear el agente reactivo
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# Inicializa SQLToolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_react_agent(
    llm, toolkit.get_tools(), state_modifier=system_message
)

# Título de la aplicación
st.title("Asistente Contable y Financiero")

# Input para la consulta SQL
sql_query = st.text_area("Ingrese su consulta SQL:", height=150)

# Si se ingresa una consulta, procesarla
if sql_query:
    try:
        # Ejecutar el agente reactivo para procesar la consulta
        result = agent_executor.invoke({"input": sql_query})
        st.write("Resultados de la consulta:")
        st.write(result["output"])
    except Exception as e:
        st.error(f"Hubo un error procesando la consulta: {e}")
