import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime


class ShowReportPopup(tk.Frame):
    def __init__(self, parent, controller, values, initial_date, end_date):
        super().__init__(parent)
        self.top = tk.Toplevel(parent)
        self.top.title("Novo relatório de produtos")
        self.controller = controller
        (self.lower_price, self.higher_price, self.bigger_seller, self.bigger_seller_quantity,
            self.minor_seller, self.minor_seller_quantity, self.not_sold) = values
        self.initial_date = initial_date
        self.end_date = end_date

        parent_width = parent.winfo_screenwidth()
        parent_height = parent.winfo_screenheight()
        window_width = 700
        window_height = 500

        position_x = int(parent_width / 2 - window_width / 2)
        position_y = int(parent_height / 2 - window_height / 2)

        self.top.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.top.geometry("700x500")  # Tamanho menor para ficar mais proporcional
        self.top.resizable(False, False)  # Desabilita o redimensionamento

        # Frame principal para padding
        main_frame = tk.Frame(self.top, padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para os inputs
        input_frame = tk.Frame(main_frame)
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)  # Faz a segunda coluna expandir

        not_sold_frame = tk.Frame(main_frame)
        not_sold_frame.grid(row=1, column=0, sticky="ew")

        ttk.Label(input_frame, text="Relatório do período {} à {}: ".format(self.initial_date, self.end_date),
                  style="TLabel").grid(row=0, column=0, padx=10, pady=10)

        #produto menor valor
        ttk.Label(input_frame, text="Produto com menor valor: ", style="TLabel").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Id: {} ".format(self.lower_price.id), style="TLabel").grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Nome: {} ".format(self.lower_price.name), style="TLabel").grid(
            row=3, column=0, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Valor: {} ".format(self.lower_price.price), style="TLabel").grid(
            row=4, column=0, padx=10, pady=10, sticky="e"
        )

        #produto maior valor
        ttk.Label(input_frame, text="Produto com maior valor: ", style="TLabel").grid(
            row=1, column=1, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Id: {} ".format(self.higher_price.id), style="TLabel").grid(
            row=2, column=1, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Nome: {} ".format(self.higher_price.name), style="TLabel").grid(
            row=3, column=1, padx=10, pady=10, sticky="e"
        )

        ttk.Label(input_frame, text="Valor: {} ".format(self.higher_price.price), style="TLabel").grid(
            row=4, column=1, padx=10, pady=10, sticky="e"
        )

        if self.bigger_seller:
            #produto mais vendido
            ttk.Label(input_frame, text="Produto mais vendido: ", style="TLabel").grid(
                row=5, column=0, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Id: {} ".format(self.bigger_seller.id), style="TLabel").grid(
                row=6, column=0, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Nome: {} ".format(self.bigger_seller.name), style="TLabel").grid(
                row=7, column=0, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Valor: {} ".format(self.bigger_seller.price), style="TLabel").grid(
                row=8, column=0, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Quantidade vendida: {} ".format(self.bigger_seller_quantity),
                      style="TLabel").grid(
                row=9, column=0, padx=10, pady=10, sticky="e"
            )
        else:
            ttk.Label(input_frame, text="Nenhum produto vendido no período selecionado", style="TLabel").grid(
                row=8, column=0, padx=10, pady=10, sticky="e"
            )

        if self.minor_seller:
            #produto mais vendido
            ttk.Label(input_frame, text="Produto menos vendido: ", style="TLabel").grid(
                row=5, column=1, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Id: {} ".format(self.minor_seller.id), style="TLabel").grid(
                row=6, column=1, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Nome: {} ".format(self.minor_seller.name), style="TLabel").grid(
                row=7, column=1, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Valor: {} ".format(self.minor_seller.price), style="TLabel").grid(
                row=8, column=1, padx=10, pady=10, sticky="e"
            )

            ttk.Label(input_frame, text="Quantidade vendida: {} ".format(self.minor_seller_quantity),
                      style="TLabel").grid(
                row=9, column=1, padx=10, pady=10, sticky="e"
            )
        else:
            ttk.Label(input_frame, text="Nenhum produto vendido no período selecionado", style="TLabel").grid(
                row=8, column=1, padx=10, pady=10, sticky="e"
            )

        if self.not_sold:
            not_sold_str = ",".join(str(item.name) for item in self.not_sold)
            ttk.Label(not_sold_frame, text="Produtos não vendidos: {}".format(not_sold_str), style="TLabel").grid(
                row=10, column=0, padx=10, pady=10, sticky="w"
            )


        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=4, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Confirmar", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

    def confirm(self):
        self.top.destroy()

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
        return self.result

class NewReportPopup(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.top = tk.Toplevel(parent)
        self.top.title("Novo relatório de produtos")
        self.controller = controller

        parent_width = parent.winfo_screenwidth()
        parent_height = parent.winfo_screenheight()
        window_width = 500
        window_height = 400

        position_x = int(parent_width / 2 - window_width / 2)
        position_y = int(parent_height / 2 - window_height / 2)

        self.top.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.top.geometry("500x400")  # Tamanho menor para ficar mais proporcional
        self.top.resizable(False, False)  # Desabilita o redimensionamento

        # Frame principal para padding
        main_frame = tk.Frame(self.top, padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para os inputs
        input_frame = tk.Frame(main_frame)
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)  # Faz a segunda coluna expandir

        ttk.Label(main_frame, text="Selecione o período para gerar o relatório: ", style="TLabel").grid(
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

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=4, column=0, sticky="e", pady=10, padx=5)

        btn_confirm = tk.Button(button_frame, text="Gerar relatório", command=self.confirm)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))

        btn_cancel = tk.Button(button_frame, text="Cancelar", command=self.top.destroy)
        btn_cancel.pack(side=tk.RIGHT)

    def confirm(self):
        initial_date = self.initial_date_entry.get()
        end_date = self.end_date_entry.get()
        values = self.controller.create_report(initial_date, end_date)
        if values:
            ShowReportPopup(
                self, self.controller, values, initial_date, end_date
            )
        self.top.destroy()

    def show(self):
        self.top.grab_set()
        self.top.wait_window()
        return self.result
