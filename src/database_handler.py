import sqlite3
from sqlite3 import Error

class DatabaseHandler:
    def __init__(self, db_path="data/inventory.db"):
        self.db_path = db_path
        self.connection = None
        self._initialize_database()  # Cria o banco e a tabela ao iniciar

    def _initialize_database(self):
        """Cria o banco de dados e a tabela 'inventory' se não existirem"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiry_date TEXT CHECK(expiry_date LIKE '____-__-__'),  -- Formato YYYY-MM-DD
            entry_date TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
            price REAL
        );
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            self.connection.commit()
        except Error as e:
            print(f"Erro ao criar tabela: {e}")
        finally:
            if self.connection:
                self.connection.close()

    def _get_connection(self):
        """Retorna uma conexão ativa com o banco"""
        return sqlite3.connect(self.db_path)

    # ---- Operações CRUD ----
    def add_item(self, product_name, quantity, expiry_date=None, price=0.0):
        """Adiciona um novo item ao inventário"""
        sql = """
        INSERT INTO inventory (product_name, quantity, expiry_date, price)
        VALUES (?, ?, ?, ?)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (product_name, quantity, expiry_date, price))
            conn.commit()
            return True
        except Error as e:
            print(f"Erro ao adicionar item: {e}")
            return False
        finally:
            conn.close()

    def update_quantity(self, product_id, new_quantity):
        """Atualiza a quantidade de um item"""
        sql = "UPDATE inventory SET quantity = ? WHERE id = ?"
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (new_quantity, product_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao atualizar quantidade: {e}")
            return False
        finally:
            conn.close()

    def get_near_expiry(self, days=7):
        sql = """
        SELECT * FROM inventory 
        WHERE 
            expiry_date IS NOT NULL AND
            JULIANDAY(expiry_date) - JULIANDAY('now', 'localtime') BETWEEN 0 AND ?
        """
        print(f"\n[DEBUG] Consulta SQL: {sql}")  # Log da consulta
        print(f"[DEBUG] Dias: {days}")  # Log do parâmetro
    
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (days,))
            results = cursor.fetchall()
            print(f"[DEBUG] Resultados: {results}")  # Log dos resultados
            return results
        except Error as e:
            print(f"Erro ao buscar itens próximos da validade: {e}")
            return []
        finally:
            conn.close()

    def get_all_items(self):
        """Retorna todos os itens do inventário"""
        sql = "SELECT * FROM inventory"
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar todos os itens: {e}")
            return []
        finally:
            conn.close()