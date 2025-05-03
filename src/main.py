import tkinter as tk
from src.gui.main_window import MainApplication
from src.inventory_manager import InventoryManager
from src.database_handler import DatabaseHandler
from src.report_generator import ReportGenerator

def main():
    root = tk.Tk()  # Única instância de Tk()
    root.title("Gestão de Inventário")
    
    # Inicializa o banco de dados
    db_path = "data/inventory.db"
    db_handler = DatabaseHandler(db_path)
    
    # Inicializa as dependências
    inventory_manager = InventoryManager(db_handler)
    report_generator = ReportGenerator(db_handler)  # Passa o DatabaseHandler
    
    # Configura a interface gráfica
    app = MainApplication(
        root, 
        inventory_manager=inventory_manager,
        report_generator=report_generator  # Passa o gerador de relatórios para a UI
    )
    
    root.mainloop()

if __name__ == "__main__":
    main()