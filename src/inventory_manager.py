from datetime import datetime, timedelta
from .database_handler import DatabaseHandler

class InventoryManager:
    def __init__(self, db_path="data/inventory.db"):
        self.db = DatabaseHandler(db_path)  # Usa o DatabaseHandler

    # ---- Operações Básicas ----
    def add_product(self, product_name, quantity, expiry_date=None, price=0.0):
        """Adiciona um novo produto ao inventário"""
        # Garante que o preço seja float
        try:
            price = float(price)
        except ValueError:
            raise ValueError("O preço deve ser um número.")
        return self.db.add_item(product_name, quantity, expiry_date, price)

    def update_stock(self, product_id, new_quantity):
        """Atualiza a quantidade em estoque de um produto"""
        return self.db.update_quantity(product_id, new_quantity)

    # ---- Funcionalidades Avançadas ----
    def check_low_stock(self, threshold=10):
        """Retorna produtos com estoque abaixo de um limite"""
        all_items = self.db.get_all_items()
        return [item for item in all_items if item[2] < threshold]  # Índice 2 = quantidade

    def check_expiring_products(self, days=7):
        """Retorna produtos próximos da validade"""
        return self.db.get_near_expiry(days)

    def calculate_total_value(self):
        """Calcula o valor total do inventário (quantidade * preço)"""
        all_items = self.db.get_all_items()
        total = 0.0
        for item in all_items:
            quantity = item[2]  # Índice 2 = quantity (correto)
            price = item[5]     # Índice 5 = price (antes estava 4)
            total += quantity * price
        return round(total, 2)

    def get_product_history(self, product_name):
        """Retorna histórico de entradas de um produto"""
        all_items = self.db.get_all_items()
        return [item for item in all_items if item[1] == product_name]  # Índice 1 = nome
    
    def get_alert_system(self):
        """Retorna o sistema de alertas vinculado a este manager"""
        from .alerts import AlertSystem
        return AlertSystem(self)