import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class AddItemDialog(tk.Toplevel):
    def __init__(self, parent, inventory_manager, callback):
        super().__init__(parent)  # Parent é a janela principal (root)
        self.title("Adicionar Item")
        self.inventory_manager = inventory_manager
        self.callback = callback
        
        # Variáveis Tkinter criadas APÓS a janela ser inicializada
        self.product_name = tk.StringVar()
        self.quantity = tk.IntVar(value=1)
        self.expiry_date = tk.StringVar()
        self.price = tk.StringVar()
        
        self.create_widgets()
        self.grab_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=10)

        # Nome do Produto
        ttk.Label(main_frame, text="Nome do Produto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(main_frame, textvariable=self.product_name, width=30)
        name_entry.grid(row=0, column=1, pady=5)

        # Quantidade
        ttk.Label(main_frame, text="Quantidade:").grid(row=1, column=0, sticky=tk.W, pady=5)
        quantity_spinbox = ttk.Spinbox(main_frame, from_=1, to=1000, textvariable=self.quantity)
        quantity_spinbox.grid(row=1, column=1, pady=5)

        # Data de Validade
        ttk.Label(main_frame, text="Validade (opcional):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = DateEntry(
            main_frame, 
            date_pattern="yyyy-mm-dd",
            textvariable=self.expiry_date,
            mindate=datetime.now()
        )
        self.date_entry.grid(row=2, column=1, pady=5)

        # Preço
        ttk.Label(main_frame, text="Preço (R$):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.price = tk.StringVar()
        price_entry = ttk.Entry(main_frame, textvariable=self.price)
        price_entry.grid(row=3, column=1, pady=5)

        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, columnspan=2, pady=10)

        ttk.Button(
            button_frame, 
            text="Adicionar", 
            command=self.add_item
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame, 
            text="Cancelar", 
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

    def add_item(self):
        """Valida e adiciona o item ao banco de dados"""
        try:
            # Validação do nome
            product_name = self.product_name.get().strip()
            if not product_name:
                raise ValueError("Nome do produto é obrigatório!")
        
            # Validação do preço (aceita vírgula ou ponto)
            price_str = self.price.get().replace(',', '.').strip()
            if not price_str:
                raise ValueError("Preço é obrigatório!")
            price = float(price_str)
        
            # Adição no banco de dados
            self.inventory_manager.add_product(
                product_name=product_name,
                quantity=self.quantity.get(),
                expiry_date=self.expiry_date.get() or None,
                price=price
            )
            self.callback()
            self.destroy()
        
        except ValueError as e:
            tk.messagebox.showerror("Erro", str(e))
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Falha ao adicionar item: {str(e)}")

class EditItemDialog(tk.Toplevel):
    def __init__(self, parent, inventory_manager, item_data, callback):
        super().__init__(parent)
        self.title("Editar Item")
        self.inventory_manager = inventory_manager
        self.callback = callback
        self.item_id = item_data[0]
        
        # Converter item_data[5] para float antes de formatar
        try:
            price_value = float(item_data[5])
        except (ValueError, TypeError):
            price_value = 0.0  # Valor padrão se falhar

        # Variáveis pré-preenchidas
        self.product_name = tk.StringVar(value=item_data[1])
        self.quantity = tk.IntVar(value=item_data[2])
        self.expiry_date = tk.StringVar(value=item_data[3] if item_data[3] else "")
        self.price = tk.StringVar(value=f"{price_value:.2f}")
        
        self.create_widgets()
        self.grab_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=10)

        # Nome do Produto
        ttk.Label(main_frame, text="Nome do Produto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(main_frame, textvariable=self.product_name, width=30)
        name_entry.grid(row=0, column=1, pady=5)

        # Quantidade
        ttk.Label(main_frame, text="Quantidade:").grid(row=1, column=0, sticky=tk.W, pady=5)
        quantity_spinbox = ttk.Spinbox(main_frame, from_=1, to=1000, textvariable=self.quantity)
        quantity_spinbox.grid(row=1, column=1, pady=5)

        # Data de Validade
        ttk.Label(main_frame, text="Validade (opcional):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = DateEntry(
            main_frame, 
            date_pattern="yyyy-mm-dd",
            textvariable=self.expiry_date,
            mindate=datetime.now()
        )
        self.date_entry.grid(row=2, column=1, pady=5)

        # Preço
        ttk.Label(main_frame, text="Preço (R$):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.price = tk.StringVar()
        price_entry = ttk.Entry(main_frame, textvariable=self.price)
        price_entry.grid(row=3, column=1, pady=5)

        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, columnspan=2, pady=10)

        # Botão Salvar
        tk.Button(
            button_frame, 
            text="Salvar", 
            command=self.update_item  # Correção aqui: de add_item para update_item
        ).pack(side=tk.LEFT, padx=5)

        # Botão Cancelar
        tk.Button(
            button_frame, 
            text="Cancelar", 
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

    def update_item(self):
        """Atualiza o item no banco de dados"""
        try:
            product_name = self.product_name.get().strip()
            quantity = self.quantity.get()
            price_str = self.price.get().replace(',', '.')
            price = float(price_str)

            if not product_name:
                raise ValueError("Nome do produto é obrigatório!")
            
            if self.inventory_manager.db.update_item(
                self.item_id, product_name, quantity, self.expiry_date.get(), price
            ):
                self.callback()
                self.destroy()
            else:
                raise Exception("Falha ao atualizar o item")
        
        except ValueError as e:
            messagebox.showerror("Erro", f"Valor inválido: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na atualização: {str(e)}")