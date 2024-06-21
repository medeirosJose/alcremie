import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.simpledialog as sd


class PriceSimulatorPopup(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.top = tk.Toplevel(parent)
        self.parent = parent
        self.top.title("Simulador de preço de produto")
        self.result = None

        parent_width = parent.winfo_screenwidth()
        parent_height = parent.winfo_screenheight()
        window_width = 400
        window_height = 200

        position_x = int(parent_width / 2 - window_width / 2)
        position_y = int(parent_height / 2 - window_height / 2)

        self.top.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.top.geometry("400x200")  # Tamanho menor para ficar mais proporcional
        self.top.resizable(False, False)  # Desabilita o redimensionamento

        # Frame principal para padding
        main_frame = tk.Frame(self.top, padx=30, pady=40)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame para os inputs
        input_frame = tk.Frame(main_frame)
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)  # Faz a segunda coluna expandir

        # Input custo dos insumos
        entry_label_input_price = tk.Label(input_frame, text="Valor total dos insumos: *")
        entry_label_input_price.grid(row=0, column=0, sticky="w", padx=(0, 35))

        self.entry_input_price = tk.Entry(input_frame, width=15)
        self.entry_input_price.grid(row=0, column=1, sticky="ew")       
        
        # Input porcentagem de lucro
        entry_label_desired_profit = tk.Label(input_frame, text="Lucro desejado (%): *")
        entry_label_desired_profit.grid(row=1, column=0, sticky="w", padx=(0, 35), pady=6)

        self.entry_desired_profit = tk.Entry(input_frame, width=15)
        self.entry_desired_profit.grid(row=1, column=1, sticky="ew")

        # Resultado: preço estimado
        entry_label_estimated_price = tk.Label(input_frame, text="Preço estimado:")
        entry_label_estimated_price.grid(row=2, column=0, sticky="w", padx=(0, 5))
        
        self.label_estimated_price = tk.Label(input_frame, text="", width=20, anchor="w")
        self.label_estimated_price.grid(row=2, column=1, sticky="w")


        # Botões
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="e", pady=20, padx=5)

        btn_confirm = tk.Button(button_frame, text="Calcular", command=self.calculate)
        btn_confirm.pack(side=tk.RIGHT, padx=(5, 0))


    def calculate(self):

        input_price = self.entry_input_price.get()
        desired_profit = self.entry_desired_profit.get()

        if not input_price or not desired_profit:
            messagebox.showerror(
                "Erro",
                "Todos os campos são de preenchimento obrigatório",
            )
            self.top.destroy()
            PriceSimulatorPopup(self.parent, "controller")
            return

        try:
            input_price = float(input_price)
            desired_profit = float(desired_profit)

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Digite apenas caracteres numéricos e ponto",
            )
            self.top.destroy()
            PriceSimulatorPopup(self.parent, "controller")
            return


        estimated_price = input_price + (input_price * desired_profit) / 100

        # Mostra na tela o valor estimado
        self.label_estimated_price.config(text=f"R$ {estimated_price:.2f}")
