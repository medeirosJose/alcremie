import tkinter as tk


class CustomersView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Clientes View", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        # Adicione mais widgets conforme necessário
