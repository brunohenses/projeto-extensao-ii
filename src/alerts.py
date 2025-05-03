from datetime import datetime, timedelta
from typing import Optional
from .inventory_manager import InventoryManager

class AlertSystem:
    def __init__(self, inventory_manager: 'InventoryManager'):  # Anotação como string
        self.manager = inventory_manager

    def get_expiry_alerts(self, days=7):
        """Retorna alertas formatados para produtos próximos da validade"""
        expiring_products = self.manager.check_expiring_products(days)
        alerts = []
        for product in expiring_products:
            product_id, name, quantity, expiry_date, _, _ = product
            expiry_date_obj = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            days_left = (expiry_date_obj - datetime.now().date()).days  # Usa o mock aqui
            alerts.append(f"[VALIDADE] {name} (ID {product_id}): Expira em {days_left} dias ({expiry_date})")
        return alerts

    def get_low_stock_alerts(self, threshold=10):
        """Retorna alertas formatados para estoque baixo"""
        low_stock = self.manager.check_low_stock(threshold)
        alerts = []
        for product in low_stock:
            product_id, name, quantity, *_ = product
            alerts.append(
                f"[ESTOQUE] {name} (ID {product_id}): "
                f"Apenas {quantity} unidades restantes"
            )
        return alerts

    def get_all_alerts(self):
        """Retorna todos os alertas combinados"""
        return (
            self.get_expiry_alerts() +
            self.get_low_stock_alerts()
        )