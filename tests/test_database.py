import unittest
from src.database_handler import DatabaseHandler
import os

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseHandler("data/test.db")  # Usa banco de teste
        self.sample_item = ("Arroz", 50, "2024-12-31", 25.90)

    def test_add_item(self):
        result = self.db.add_item(*self.sample_item)
        self.assertTrue(result)

    def test_get_all_items(self):
        self.db.add_item(*self.sample_item)
        items = self.db.get_all_items()
        self.assertGreaterEqual(len(items), 1)

    def tearDown(self):
        if os.path.exists("data/test.db"):
            os.remove("data/test.db")  # Limpa após os testes

if __name__ == "__main__":
    unittest.main()