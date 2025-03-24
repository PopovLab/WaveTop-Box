import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

from WaveTopBox.ui.header_panel import HeaderPanel
from WaveTopBox.views.imped_view import ImpedView
import WaveTopBox.models.model_factory as ModelFactory
import WaveTopBox.App as App

class ImpedPage(ttk.Frame):
    def __init__(self, master, folder_item) -> None:
        super().__init__(master)        
        self.folder_item = folder_item
        self.model = ModelFactory.load(folder_item)
        title = f"Imped: {self.model.name}"
        self.header_content = { "title": title, "buttons":[('Save', self.save_model), ('Delete', self.delete_model), ('Clone', self.clone_model)]}
        self.hp = HeaderPanel(self, self.header_content)
        self.hp.grid(row=0, column=0, columnspan=5, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.columnconfigure(0, weight=0)        
        self.columnconfigure(1, weight=1)         

        self.view = ImpedView(self, self.model)
        self.view.grid(row=1, column=0,columnspan=3, padx=5, sticky=tk.N + tk.S + tk.E + tk.W)
        

    def clone_model(self):
        self.view.update_model()
        App.clone_model(self.model)
        
    def save_model(self):
        self.view.update_model()
        self.folder_item.save_model(self.model)

    
    def delete_model(self):
        if self.folder_item.remove():
            self.master.show_empty_view()