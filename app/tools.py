# tools.py

import os
from dotenv import load_dotenv

# Cargar la API Key desde el archivo .env
load_dotenv()  # Carga las variables de entorno del archivo .env
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("La clave API de OpenAI no está en el archivo .env")

# Importar OpenAI LLM
from langchain.llms import OpenAI  # Llama al cliente de OpenAI

# Inicializa ChatOpenAI con el modelo y la clave API
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)

# Definir herramientas de LangChain
from langchain_community.utilities.sql_database import SQLDatabase

# Conectar con la base de datos
from db_connector import engine  # Importar engine de la conexión de la base de datos
db = SQLDatabase(engine)

from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDatabaseTool,
)

# Crear herramientas de SQL
info_tool = InfoSQLDatabaseTool(db=db)
list_tool = ListSQLDatabaseTool(db=db)
query_checker_tool = QuerySQLCheckerTool(db=db, llm=llm)
query_tool = QuerySQLDatabaseTool(db=db)

# Regresar las herramientas en una lista
tools = [info_tool, list_tool, query_checker_tool, query_tool]
