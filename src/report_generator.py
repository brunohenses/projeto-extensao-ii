import csv
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ReportGenerator:
    def __init__(self, db_handler):  # Alterado para receber db_handler
        self.db_handler = db_handler  # Agora usa o DatabaseHandler diretamente
        self.reports_dir = os.path.join("data", "reports")
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_report(self, report_type="pdf", filename=None):
        """Gera um relatório no formato especificado (PDF ou CSV)."""
        data = self.db_handler.get_all_items()  # Chama o método diretamente do DatabaseHandler
        
        if not data:
            raise ValueError("Nenhum dado disponível para gerar o relatório.")

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_{timestamp}.{report_type.lower()}"

        filepath = os.path.join(self.reports_dir, filename)

        if report_type.lower() == "pdf":
            self._generate_pdf(filepath, data)
        elif report_type.lower() == "csv":
            self._generate_csv(filepath, data)
        else:
            raise ValueError("Formato de relatório não suportado.")

        return filepath

    def _generate_csv(self, filepath, data):
        """Gera um arquivo CSV com os dados do inventário."""
        headers = ["ID", "Produto", "Quantidade", "Validade", "Preço"]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for item in data:
                writer.writerow([
                    item[0],  # ID
                    item[1],  # Nome
                    item[2],  # Quantidade
                    item[3],  # Validade
                    f"R$ {item[5]:.2f}"  # Preço
                ])

    def _generate_pdf(self, filepath, data):
        """Gera um arquivo PDF formatado com os dados do inventário."""
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []

        # Título do Relatório
        styles = getSampleStyleSheet()
        title = Paragraph("Relatório de Inventário", styles['Title'])
        elements.append(title)

        # Tabela de Dados
        headers = ["ID", "Produto", "Quantidade", "Validade", "Preço (R$)"]
        table_data = [headers]
        
        for item in data:
            table_data.append([
                str(item[0]),  # ID
                item[1],       # Nome
                str(item[2]),  # Quantidade
                item[3],      # Validade
                f"{item[5]:.2f}"  # Preço
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)