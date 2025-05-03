import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.dialogs import AddItemDialog, EditItemDialog

class MainApplication(tk.Frame):
    def __init__(self, master, inventory_manager, report_generator):
        super().__init__(master)
        self.master = master
        self.inventory_manager = inventory_manager
        self.report_generator = report_generator
        self.alert_system = inventory_manager.get_alert_system()
        
        self.create_widgets()
        self.update_alerts()
        self.update_inventory_list()

    def create_widgets(self):
        # Container principal
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Seção de Alertas
        self.alert_frame = ttk.LabelFrame(self.main_frame, text="Alertas")
        self.alert_frame.pack(fill=tk.X, pady=5)
        
        self.alert_list = tk.Listbox(
            self.alert_frame, 
            height=4, 
            bg="#FFF3CD",  # Cor de fundo amarelada para alertas
            font=('Arial', 10)
        )
        self.alert_list.pack(fill=tk.X, padx=5, pady=5)

        # Seção do Inventário
        self.inventory_frame = ttk.LabelFrame(self.main_frame, text="Inventário")
        self.inventory_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.tree = ttk.Treeview(
            self.inventory_frame,
            columns=("ID", "Nome", "Quantidade", "Validade", "Entrada", "Preço"),  # 6 colunas
            show="headings"
        )

        # Configuração das colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Validade", text="Validade")
        self.tree.heading("Entrada", text="Data de Entrada")  # Nova coluna
        self.tree.heading("Preço", text="Preço (R$)")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nome", width=200, anchor=tk.W)
        self.tree.column("Quantidade", width=80, anchor=tk.CENTER)
        self.tree.column("Validade", width=100, anchor=tk.CENTER)
        self.tree.column("Entrada", width=120, anchor=tk.CENTER)  # Nova coluna
        self.tree.column("Preço", width=80, anchor=tk.E)
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Barra de rolagem
        scrollbar = ttk.Scrollbar(self.inventory_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Adicione um frame para os botões de ação
        self.action_frame = ttk.Frame(self.inventory_frame)
        self.action_frame.pack(fill=tk.X, pady=5)

        # Botões de Ação
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        # Botão de Adicionar Item
        self.add_button = ttk.Button(
            self.button_frame, 
            text="Adicionar Item", 
            command=self.open_add_item_dialog
        )
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Botão Editar
        self.edit_button = ttk.Button(
            self.action_frame,
            text="Editar Item",
            command=self.open_edit_dialog,
            state=tk.DISABLED  # Inicia desabilitado
        )
        self.edit_button.pack(side=tk.LEFT, padx=5)

        # Botão Excluir
        self.delete_button = ttk.Button(
            self.action_frame,
            text="Excluir Item",
            command=self.delete_selected_item,
            state=tk.DISABLED  # Inicia desabilitado
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Botão de Gerar Relatório
        self.report_button = ttk.Button(
            self.button_frame, 
            text="Gerar Relatório", 
            command=self.generate_report
        )
        self.report_button.pack(side=tk.LEFT, padx=5)

        # Vincule a seleção na Treeview
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

    def update_alerts(self):
        """Atualiza a lista de alertas"""
        if self.alert_system:
            alerts = self.alert_system.get_all_alerts()
            self.alert_list.delete(0, tk.END)
            for alert in alerts:
                self.alert_list.insert(tk.END, alert)

    def update_inventory_list(self):
        """Atualiza a lista de itens do inventário"""
        if self.inventory_manager:
            items = self.inventory_manager.db.get_all_items()
            self.tree.delete(*self.tree.get_children())
            for item in items:
                # Converte None para string vazia e formata datas
                formatted_item = (
                    item[0],  # ID
                    item[1],  # Nome
                    item[2],  # Quantidade
                    item[3] if item[3] else "Sem validade",  # Validade (trata None)
                    item[4],  # Data de entrada
                    f"R$ {item[5]:.2f}"  # Preço formatado
                )
                self.tree.insert("", tk.END, values=formatted_item)

    def open_add_item_dialog(self):
        """Abre a janela de adicionar item"""
        dialog = AddItemDialog(
            self.master, 
            self.inventory_manager,
            self.update_inventory_list  # Callback para atualizar a lista
        )
        dialog.grab_set()  # Mantém o foco na janela de diálogo

    def on_item_selected(self, event):
        """Ativa os botões quando um item é selecionado"""
        selected = self.tree.selection()
        if selected:
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    def delete_selected_item(self):
        """Exclui o item selecionado do banco de dados"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
    
        item_id = self.tree.item(selected_item, "values")[0]  # Pega o ID da linha
    
        if messagebox.askyesno(
            "Confirmar Exclusão", 
            "Tem certeza que deseja excluir este item?"
        ):
            if self.inventory_manager.db.delete_item(item_id):
                self.update_inventory_list()
                messagebox.showinfo("Sucesso", "Item excluído!")
            else:
                messagebox.showerror("Erro", "Falha ao excluir item")

    def open_edit_dialog(self):
        """Abre a janela de edição"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
    
        item_data = self.tree.item(selected_item, "values")
        dialog = EditItemDialog(
            self.master,
            self.inventory_manager,
            item_data,
            self.update_inventory_list
        )

    def generate_report(self):
        try:
            # Exemplo: Gera relatório PDF
            report_path = self.report_generator.generate_report("pdf")
            messagebox.showinfo("Sucesso", f"Relatório gerado em:\n{report_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar relatório:\n{str(e)}")