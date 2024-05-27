import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime


class NewReportPopup(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.top = tk.Toplevel(parent)
        self.top.title("Novo relatório de produtos")
        self.controller = controller
        self.main_frame = None

        parent_width = parent.winfo_screenwidth()
        parent_height = parent.winfo_screenheight()
        window_width = 700
        window_height = 500

        position_x = int(parent_width / 2 - window_width / 2)
        position_y = int(parent_height / 2 - window_height / 2)

        self.top.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.top.geometry("700x500")  # Tamanho menor para ficar mais proporcional
        self.top.resizable(False, False)  # Desabilita o redimensionamento

        self.root = tk.Frame(self.top, padx=10, pady=10)
        self.root.pack(expand=True, fill=tk.BOTH)

        btn_new_report = tk.Button(self.root, text="Novo relatório", command=self.set_input_values)
        btn_new_report.pack(side=tk.TOP, padx=(0, 0))

    def set_input_values(self):
        self.root.destroy()
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
        (lower_price, higher_price, bigger_seller, bigger_seller_quantity,
         minor_seller, minor_seller_quantity, not_sold) = values
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
                  style="TLabel").grid(row=0, column=0, padx=10, pady=10)

        #produto menor valor
        ttk.Label(input_frame, text="Produto com menor valor: ", style="TLabel").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Id: {} ".format(lower_price.id), style="TLabel").grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Nome: {} ".format(lower_price.name), style="TLabel").grid(
            row=3, column=0, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Valor: {} ".format(lower_price.price), style="TLabel").grid(
            row=4, column=0, padx=10, pady=10, sticky="e"
        )

        #produto maior valor
        ttk.Label(input_frame, text="Produto com maior valor: ", style="TLabel").grid(
            row=1, column=1, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Id: {} ".format(higher_price.id), style="TLabel").grid(
            row=2, column=1, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Nome: {} ".format(higher_price.name), style="TLabel").grid(
            row=3, column=1, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Valor: {} ".format(higher_price.price), style="TLabel").grid(
            row=4, column=1, padx=10, pady=10, sticky="e"
        )

        if bigger_seller:
            #produto mais vendido
            ttk.Label(input_frame, text="Produto mais vendido: ", style="TLabel").grid(
                row=5, column=0, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Id: {} ".format(bigger_seller.id), style="TLabel").grid(
                row=6, column=0, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Nome: {} ".format(bigger_seller.name), style="TLabel").grid(
                row=7, column=0, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Valor: {} ".format(bigger_seller.price), style="TLabel").grid(
                row=8, column=0, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Quantidade vendida: {} ".format(bigger_seller_quantity),
                      style="TLabel").grid(
                row=9, column=0, padx=10, pady=10, sticky="e"
            )
        else:
            ttk.Label(input_frame, text="Nenhum produto vendido no período selecionado", style="TLabel").grid(
                row=8, column=0, padx=10, pady=10, sticky="e"
            )

        if minor_seller:
            #produto mais vendido
            ttk.Label(input_frame, text="Produto menos vendido: ", style="TLabel").grid(
                row=5, column=1, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Id: {} ".format(minor_seller.id), style="TLabel").grid(
                row=6, column=1, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Nome: {} ".format(minor_seller.name), style="TLabel").grid(
                row=7, column=1, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Valor: {} ".format(minor_seller.price), style="TLabel").grid(
                row=8, column=1, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Quantidade vendida: {} ".format(minor_seller_quantity),
                      style="TLabel").grid(
                row=9, column=1, padx=10, pady=10, sticky="e"
            )
        else:
            ttk.Label(input_frame, text="Nenhum produto vendido no período selecionado", style="TLabel").grid(
                row=8, column=1, padx=10, pady=10, sticky="e"
            )

        if not_sold:
            not_sold_str = ",".join(str(item.name) for item in not_sold)
            ttk.Label(not_sold_frame, text="Produtos não vendidos: {}".format(not_sold_str), style="TLabel").grid(
                row=10, column=0, padx=10, pady=10, sticky="w"
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
