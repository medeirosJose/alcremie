from models.menu import Menu
import random
from DAO.menu_dao import MenuDAO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)
from reportlab.lib.units import inch
from reportlab.lib import colors


class MenuController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.menus = []
        self.menu_dao = MenuDAO()

    def generate_id(self):
        while True:
            new_id = random.randint(
                88000000,
                88999999,  # defini que todos os pedidos começam com id 88 só pq sim kkkk
            )
            if not self.menu_dao.get(new_id):
                return new_id

    def get_products(self):  # Adiciona este método ao MenuController
        return self.app_controller.product_controller.get_products()

    def generate_menu_pdf(self, menu):
        doc = SimpleDocTemplate(f"menu_{menu.menu_id}.pdf", pagesize=letter)
        story = []

        # Estilos personalizados
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="MenuTitle", fontName="Helvetica-Bold", fontSize=24, leading=28
            )
        )
        styles.add(
            ParagraphStyle(
                name="CategoryTitle", fontName="Helvetica-Bold", fontSize=18, leading=22
            )
        )
        styles.add(
            ParagraphStyle(
                name="ProductTitle", fontName="Helvetica", fontSize=14, leading=16
            )
        )
        styles.add(
            ParagraphStyle(
                name="ProductPrice", fontName="Helvetica", fontSize=12, leading=14
            )
        )

        # Cabeçalho do cardápio
        story.append(Paragraph(f"Cardápio: {menu.name}", styles["MenuTitle"]))
        story.append(Paragraph(f"Categoria: {menu.category}", styles["CategoryTitle"]))
        story.append(Spacer(1, 24))  # Espaçamento maior após o cabeçalho

        # Tabela de produtos (opcional)
        data = [[product.name, f"R$ {product.price:.2f}"] for product in menu.products]
        table = Table(data, colWidths=[300, 100])  # Largura das colunas
        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),  # Cabeçalho da tabela
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),  # Linhas da tabela
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 24))  # Espaçamento após a tabela

        doc.build(story)

    def create_menu(self, selected_products, menu_name, menu_category):
        new_menu = Menu(self.generate_id(), menu_name, menu_category, selected_products)
        self.menu_dao.add(new_menu)
        # print("Cardápio criado com sucesso!")
        self.generate_menu_pdf(new_menu)
