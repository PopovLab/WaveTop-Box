import tkinter as tk
import tkinter.ttk as ttk
from WaveTopBox.models.error_model import ErrorModel

class ErrorView(tk.Frame):
    def __init__(self, master, model:ErrorModel) -> None:
            super().__init__(master) 
            self.model = model
            state = 'disabled'
            self.columnconfigure(0, weight=0)        
            self.columnconfigure(1, weight=1)         

            self.label = ttk.Label(self,  text='Name:')
            self.label.grid(row=0, column=0, padx=5, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)
            self.var_name = tk.StringVar(master= self, value=model.name)
            self.name_entry = ttk.Entry(self, textvariable = self.var_name, state= state)
            self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

            self.label = ttk.Label(self,  text='Message:')
            self.label.grid(row=1, column=0, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
            self.comment_text = tk.Text(self, height=3,  wrap="none")
            self.comment_text.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
            self.comment_text.insert(tk.END, model.text)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=1)