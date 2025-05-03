import unittest
from src.inventory_manager import InventoryManager
from datetime import date, datetime, timedelta
from unittest.mock import patch

class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = InventoryManager("data/test.db")
        self.sample_product = ("Feijão", 30, str(date.today() + timedelta(days=14)), 8.90)

    def test_add_product(self):
        result = self.manager.add_product(*self.sample_product)
        self.assertTrue(result)

    def test_low_stock_alert(self):
        self.manager.add_product("Sal", 5, price=2.50)
        low_stock = self.manager.check_low_stock(threshold=10)
        self.assertEqual(len(low_stock), 1)

    def test_total_value_calculation(self):
        self.manager.add_product("Arroz", 20, price=25.90)
        self.manager.add_product("Óleo", 10, price=9.50)

        # Verifica os dados inseridos (para debug)
        all_items = self.manager.db.get_all_items()
        print("\nItens no banco de dados:", all_items)

        total = self.manager.calculate_total_value()
        expected = (20 * 25.90) + (10 * 9.50)
        self.assertEqual(total, round(expected, 2))

    def test_alerts(self):
        # Adiciona um produto que expira em 5 dias a partir de hoje
        today = datetime.now().date()
        expiry_date = (today + timedelta(days=5)).strftime("%Y-%m-%d")  # Data de validade = hoje + 5 dias
    
        self.manager.add_product("Leite", 5, expiry_date=expiry_date, price=4.90)
        self.manager.add_product("Café", 3, price=12.50)
    
        alert_system = self.manager.get_alert_system()
        expiry_alerts = alert_system.get_expiry_alerts(days=7)  # Busca produtos que expiram em até 7 dias
    
        # DEBUG: Verifica os dados inseridos
        from src.database_handler import DatabaseHandler
        db = DatabaseHandler("data/test.db")
        print("\nDEBUG - Itens no banco:", db.get_all_items())  # Deve mostrar a data correta
        
        # DEBUG: Verifica os alertas
        print("DEBUG - Alertas de validade:", expiry_alerts)
    
        # Verifica se o alerta foi gerado
        self.assertGreater(len(expiry_alerts), 0, "Nenhum alerta de validade gerado")
        self.assertIn(f"Expira em 5 dias ({expiry_date})", expiry_alerts[0])
        
        # Verifica alertas de estoque baixo
        low_stock_alerts = alert_system.get_low_stock_alerts(threshold=10)
        self.assertEqual(len(low_stock_alerts), 2)  # Leite (5) e Café (3)

    def tearDown(self):
        import os
        if os.path.exists("data/test.db"):
            os.remove("data/test.db")

if __name__ == "__main__":
    unittest.main()