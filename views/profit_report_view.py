import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime


class NewProfitReportPopup(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.top = tk.Toplevel(parent)
        self.top.title("Novo relatório de lucros")
        self.controller = controller
        self.main_frame = None

        parent_width = parent.winfo_screenwidth()
        parent_height = parent.winfo_screenheight()
        window_width = 500
        window_height = 500

        position_x = int(parent_width / 2 - window_width / 2)
        position_y = int(parent_height / 2 - window_height / 2)

        self.top.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.top.geometry("500x500")  # Tamanho menor para ficar mais proporcional
        self.top.resizable(False, False)  # Desabilita o redimensionamento

        self.root = tk.Frame(self.top, padx=10, pady=10)
        self.root.pack(expand=True, fill=tk.BOTH)

        style = ttk.Style()
        style.configure("Bold.TLabel", font=("TkDefaultFont", 10, "bold"))

        # Frame principal para padding
        self.main_frame = tk.Frame(self.top, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para os inputs
        input_frame = tk.Frame(self.main_frame)
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)  # Faz a segunda coluna expandir

        ttk.Label(self.main_frame, text="Selecione o período para gerar o relatório: ", style="TLabel").grid(
            row=0, column=0, padx=10, pady=10
        )

        #data de início do período que a pessoa quer gerr o relatório
        ttk.Label(input_frame, text="Data de início: ", style="TLabel").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.initial_date_entry = DateEntry(
            input_frame,
            width=25,
            maxdate=datetime.now(),
            date_pattern="dd/mm/yyyy",
            state="readonly",
        )

        self.initial_date_entry.grid(row=1, column=1, padx=10, sticky="w")
        self.initial_date_entry.bind("<<DateEntrySelected>>")

        # data de fim do período que a pessoa quer gerr o relatório
        ttk.Label(input_frame, text="Data de fim: ", style="TLabel").grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )
        self.end_date_entry = DateEntry(
            input_frame,
            width=25,
            maxdate=datetime.now(),
            date_pattern="dd/mm/yyyy",
            state="readonly",
        )

        self.end_date_entry.grid(row=2, column=1, padx=10, sticky="w")
        self.end_date_entry.bind("<<DateEntrySelected>>")

        button_frame = tk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Gerar relatório", command=self.create_new_report)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = tk.Button(button_frame, text="Cancelar", command=self.top.destroy)
        btn_cancel.pack(side=tk.RIGHT)

    def show_report(self, values, initial_date, end_date):
        self.main_frame.destroy()
        (products_sold_between_period, products_not_sold_between_period, profit) = values
        # Frame principal para padding
        self.main_frame = tk.Frame(self.top, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para os inputs
        input_frame = tk.Frame(self.main_frame)
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)  # Faz a segunda coluna expandir

        not_sold_frame = tk.Frame(self.main_frame)
        not_sold_frame.grid(row=1, column=0, sticky="ew")

        ttk.Label(input_frame, text="Relatório do período {} à {}: ".format(initial_date, end_date),
                  style="Bold.TLabel").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        #produto menor valor
        ttk.Label(input_frame, text="Lucro total: ", style="Bold.TLabel").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="{:.2f} ".format(profit), style="TLabel").grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )

        row = 11
        if products_sold_between_period:
            ttk.Label(not_sold_frame, text="Produtos vendidos: ", style="Bold.TLabel").grid(
                row=10, column=0, padx=10, pady=10, sticky="w"
            )

            for order in products_sold_between_period:
                for product, quantity in order:
                    ttk.Label(not_sold_frame, text="Nome: {}".format(product.name), style="TLabel").grid(
                        row=row, column=0, padx=10, pady=10, sticky="w"
                    )
                    ttk.Label(not_sold_frame, text="Quantidade: {}".format(quantity), style="TLabel").grid(
                        row=row, column=2, padx=10, pady=10, sticky="w"
                    )
                row +=1
        if products_not_sold_between_period:
            not_sold_str = ",".join(str(item.name) for item in products_not_sold_between_period)
            ttk.Label(not_sold_frame, text="Produtos não vendidos: ", style="Bold.TLabel").grid(
                row=row+1, column=0, padx=10, pady=10, sticky="w"
            )
            ttk.Label(not_sold_frame, text="{}".format(not_sold_str), style="TLabel").grid(
                row=row+2, column=0, padx=10, pady=10, sticky="w"
            )

        button_frame = tk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Confirmar", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

    def create_new_report(self):
        initial_date = self.initial_date_entry.get()
        end_date = self.end_date_entry.get()
        is_interval_valid = self.controller.validate_date_interval(initial_date, end_date)
        if not is_interval_valid:
            messagebox.showerror(
                "Erro",
                "O campo de fim deve ser maior ou igual ao campo de início",
            )
            self.top.lift()
            return
        values = self.controller.create_report(initial_date, end_date)

        if values:
            self.show_report(values, initial_date, end_date)
        else:
            messagebox.showerror(
                "Erro",
                "Nenhum produto foi vendido nesse período",
            )
            self.top.lift()
            return

    def confirm(self):
        self.top.destroy()
