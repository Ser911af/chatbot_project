import json
import logging
import os
from dotenv import load_dotenv
from typing import Any
import openai
from db import fetch_query, get_schema

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar OpenAI API Key
openai.api_key = os.getenv("OPEN_AI_API_KEY")

# Configurar el logger
logger = logging.getLogger(__name__)

async def human_query_to_sql(human_query: str) -> str:
    """
    Convierte una consulta en lenguaje natural a una consulta SQL usando OpenAI.
    """
    try:
        # Obtener esquema de la base de datos
        database_schema = get_schema()

        system_message = f"""
        Tienes el siguiente esquema de base de datos. Convierte una consulta en lenguaje natural a SQL y
        devuelve solo un JSON con la clave 'sql_query' y el texto SQL correspondiente.
        Ejemplo:
        {{
            "sql_query": "SELECT * FROM ventas WHERE cliente = 'Cliente A';"
        }}
        <esquema>
        {database_schema}
        </esquema>
        """
        user_message = human_query

        # Realizar consulta al modelo OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )

        response_content = response.choices[0].message.content
        sql_query = json.loads(response_content).get("sql_query")

        return sql_query
    except Exception as e:
        logger.error(f"Error al generar la consulta SQL: {e}")
        return None

async def build_answer(result: list[dict[str, Any]], human_query: str) -> str:
    """
    Convierte los resultados de SQL en una respuesta comprensible para el usuario.
    """
    try:
        system_message = f"""
        Genera una respuesta en lenguaje natural para la siguiente consulta y resultados SQL.
        <pregunta_usuario>
        {human_query}
        </pregunta_usuario>
        <respuesta_sql>
        {result}
        </respuesta_sql>
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error al construir respuesta humana: {e}")
        return "Hubo un error al procesar la respuesta."

async def process_user_query(human_query: str) -> str:
    """
    Procesa una consulta del usuario: transforma el lenguaje natural a SQL,
    ejecuta la consulta y humaniza los resultados.
    """
    # Generar consulta SQL
    sql_query = await human_query_to_sql(human_query)
    if not sql_query:
        return "Lo siento, no pude generar una consulta SQL válida."

    # Ejecutar consulta en la base de datos
    results = fetch_query(sql_query)
    if results is None:
        return "Lo siento, hubo un problema al ejecutar la consulta SQL."

    # Generar respuesta humanizada
    answer = await build_answer(results, human_query)
    return answer
