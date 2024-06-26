from models.menu import Menu
import random
from DAO.menu_dao import MenuDAO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle,
)
from reportlab.lib.units import inch
import os
from tkinter import Tk, messagebox


class MenuController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.menus = []
        self.menu_dao = MenuDAO()
        self.generated_pdf = None

    def generate_id(self):
        while True:
            new_id = random.randint(
                88000000,
                88999999,  # defini que todos os pedidos começam com id 88 só pq sim kkkk
            )
            if not self.menu_dao.get(new_id):
                return new_id

    def get_products(self):
        return self.app_controller.product_controller.get_products()

    def generate_menu_pdf(self, menu):
        pdf_folder = "menus"
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)
        self.generated_pdf = os.path.join(pdf_folder, f"menu_{menu.menu_id}.pdf")
        doc = SimpleDocTemplate(self.generated_pdf, pagesize=letter)
        story = []

        styles = getSampleStyleSheet()
        # 0 para alinhar à esquerda, 1 para centralizar, 2 para alinhar à direita
        styles.add(
            ParagraphStyle(
                name="MenuTitle",
                fontName="Helvetica-Bold",
                fontSize=24,
                leading=28,
                alignment=1,
            )
        )
        styles.add(
            ParagraphStyle(
                name="CategoryTitle",
                fontName="Helvetica",
                fontSize=18,
                leading=22,
                textColor=colors.grey,
                alignment=1,
            )
        )
        styles.add(
            ParagraphStyle(
                name="ProductTitle", fontName="Helvetica-Bold", fontSize=14, leading=16
            )
        )
        styles.add(
            ParagraphStyle(
                name="ProductPrice",
                fontName="Helvetica",
                fontSize=12,
                leading=14,
                alignment=0,
            )
        )
        styles.add(
            ParagraphStyle(
                name="ProductDescription",
                fontName="Helvetica",
                fontSize=10,
                leading=12,
                alignment=0,
            )
        )

        # Capa do cardápio
        story.append(Spacer(1, 100))
        story.append(Paragraph("Confeitaria Alcremie", styles["MenuTitle"]))
        story.append(Spacer(1, 20))
        story.append(
            Paragraph(
                "Especializados em deixar sua vida mais doce!", styles["CategoryTitle"]
            )
        )
        logo_path = "icons/logo.png"

        story.append(Image(logo_path, width=2 * inch, height=2 * inch))
        story.append(PageBreak())

        # Cabeçalho do cardápio
        story.append(Paragraph(f"Cardápio de {menu.name}", styles["MenuTitle"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Categoria: {menu.category}", styles["CategoryTitle"]))
        story.append(Spacer(1, 24))

        align_left = True

        # Produtos com imagens e descrições
        for product in menu.products:
            product_elements = []

            if product.image:
                try:
                    img = Image(product.image, width=2 * inch, height=2 * inch)
                except Exception as e:
                    print(f"Erro ao carregar imagem do produto {product.name}: {e}")
                    img = None
            else:
                img = None

            # Dados do produto
            product_name = Paragraph(product.name, styles["ProductTitle"])
            product_description = Paragraph(
                product.description, styles["ProductDescription"]
            )
            product_price = Paragraph(f"R$ {product.price:.2f}", styles["ProductPrice"])

            if img:
                product_elements = [
                    [
                        img,
                        [product_name, product_description, product_price],
                    ]  # Nested list for alignment
                ]
            else:
                product_elements = [
                    [product_name],
                    [product_description],
                    [product_price],
                ]

            t = Table(product_elements)
            t.setStyle(
                TableStyle(
                    [
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP",
                        ),
                        (
                            "ALIGN",
                            (1, 0),
                            (1, -1),
                            "LEFT",
                        ),
                        ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ]
                )
            )
            story.append(t)
            story.append(Spacer(1, 12))

            align_left = not align_left

        doc.build(story, onLaterPages=self.add_page_number)

    def add_page_number(self, canvas, doc):
        canvas.saveState()
        page_number_text = f"{doc.page}"
        canvas.setFont("Helvetica", 10)
        canvas.drawString(500, 10, page_number_text)
        canvas.restoreState()

    def create_menu(self, selected_products, menu_name, menu_category):
        new_menu = Menu(self.generate_id(), menu_name, menu_category, selected_products)
        self.menu_dao.add(new_menu)
        self.generate_menu_pdf(new_menu)
        self.show_success_popup()

    # ! talvez tenha q remover isso depois, por estar ferindo o encapsulamento do mvc
    def show_success_popup(self):
        def open_pdf():
            if os.name == "nt":
                os.startfile(self.generated_pdf)
            elif os.name == "posix":
                os.system(f'open "{self.generated_pdf}"')

        root = Tk()
        root.withdraw()

        result = messagebox.askquestion(
            "Sucesso", "Cardápio criado com sucesso! Deseja abrir o PDF?", icon="info"
        )
        if result == "yes":
            open_pdf()

        root.destroy()
