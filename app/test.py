import unittest
from db import fetch_query, execute_query, get_schema
from nlp import human_query_to_sql, build_answer
from interface import authenticate_user
from unittest.mock import patch

class TestDatabaseFunctions(unittest.TestCase):

    def test_fetch_query(self):
        """Prueba de la función fetch_query."""
        query = "SELECT * FROM ventas LIMIT 1;"
        result = fetch_query(query)
        self.assertIsInstance(result, list)  # Verifica que el resultado sea una lista

    def test_execute_query(self):
        """Prueba de la función execute_query para una consulta INSERT."""
        query = "INSERT INTO ventas (fecha, cliente, monto) VALUES ('2024-12-14', 'Cliente A', 100.00);"
        rows_affected = execute_query(query)
        self.assertEqual(rows_affected, 1)  # Verifica que se haya afectado una fila

class TestNLPFunctions(unittest.TestCase):

    @patch('nlp.openai.ChatCompletion.create')
    def test_human_query_to_sql(self, mock_create):
        """Prueba de la función human_query_to_sql."""
        # Simular la respuesta de OpenAI
        mock_create.return_value = {
            'choices': [{'message': {'content': '{"sql_query": "SELECT * FROM ventas;"}'}}]
        }
        query = "Mostrar todas las ventas"
        sql_query = human_query_to_sql(query)
        self.assertEqual(sql_query, "SELECT * FROM ventas;")

    @patch('nlp.openai.ChatCompletion.create')
    def test_build_answer(self, mock_create):
        """Prueba de la función build_answer."""
        # Simular la respuesta de OpenAI
        mock_create.return_value = {'choices': [{'message': {'content': 'Aquí están las ventas.'}}]}
        result = [{'id_venta': 1, 'cliente': 'Cliente A', 'monto': 100.00}]
        human_query = "Mostrar todas las ventas"
        answer = build_answer(result, human_query)
        self.assertEqual(answer, 'Aquí están las ventas.')

class TestInterfaceFunctions(unittest.TestCase):

    def test_authenticate_user(self):
        """Prueba de la función authenticate_user."""
        # Validar las credenciales correctas
        self.assertTrue(authenticate_user("admin", "1234"))
        # Validar credenciales incorrectas
        self.assertFalse(authenticate_user("admin", "wrongpassword"))
        self.assertFalse(authenticate_user("wronguser", "1234"))

if __name__ == '__main__':
    unittest.main()
