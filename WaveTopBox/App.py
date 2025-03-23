import importlib
import os
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from functools import partial
#from AstraBox.Pages.FRTCPage import FRTCPage
#from AstraBox.Pages.SpectrumPage import SpectrumPage
#from AstraBox.Views.FRTCView import FRTCView
import WaveTopBox.pages.RackFrame as RackFrame
from WaveTopBox.pages.ContentFrame import ContentFrame

from WaveTopBox.pages.EmptyPage import EmptyPage
#from AstraBox.Pages.RayTracingPage import RayTracingPage
#from AstraBox.Views.TextView import TextView
#from AstraBox.Pages.ExpPage import ExpPage
#from AstraBox.Pages.TextPage import TextPage
#from AstraBox.Pages.RacePage import RacePage
#from AstraBox.Pages.RunAstraPage import RunAstraPage
#from AstraBox.Models.RaceModel import RaceModel

import WaveTopBox.models.model_factory as model_factory
#import AstraBox.Config as Config
import WaveTopBox.work_space as work_space
import WaveTopBox.history as history

live = True

work_space_loc = None

def run():
    print(work_space_loc)
    win = MainWindow()
    win.mainloop()

def clone_model(model):
    model = ModelFactory.clone_model(model)
    work_space.save_model(model)
    print(type(model).__name__)
    work_space.refresh_folder(type(model).__name__) 

geo_file = "data/geo.ini"

def load_geometry():
    try:
        # get geometry from file 
        f = open(geo_file,'r')
        geo =f.read()
        f.close()
    except:
        print ('error reading geo-file')    
        geo = None
    return geo

def save_geometry(geo):
        # save current geometry to the file 
        try:
            with open(geo_file, 'w') as f:
                f.write(geo)
                print('save geo')
                f.close()
        except:
            print('file error')    

import tomllib
def get_version(pk_name):
    try:
        with open("pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
        version = pyproject["tool"]["poetry"]["version"]
    except Exception as e:
        version = importlib.metadata.version(pk_name)
    return version

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WaveTop Box")
        self.minsize(1024, 600)        
        geo = load_geometry()
        if geo:
            self.geometry(geo)
        

        main_menu = self.create_main_menu()
        self.config(menu= main_menu)

        style = ttk.Style()
        # стиль для кнопок

        # Justify to the left [('Button.label', {'sticky': 'w'})]
        style.layout("TButton", [('Button.button', {'sticky': 'nswe', 'children': [('Button.focus', {'sticky': 'nswe', 'children': [('Button.padding', {'sticky': 'nswe', 'children': [('Button.label',
            {'sticky': 'w'})]})]})]})])

        style.configure('Toolbutton', 
                        foreground= 'black', 
                        backgound= 'red',
                        padding= 9,  #{'padx': 5, 'pady': 10},
                        font=('Helvetica', 12))
        style.configure("Header.TLabel",
                        foreground='navy',
                        backgound = 'red',
                        padding=8,
                        font=('Helvetica', 12))


        if work_space_loc:
            self.base_folder = work_space_loc
            self.title(f"ASTRA Box in {work_space_loc}")            
            self.work_space= work_space.open(work_space_loc)
            history.add_new(work_space_loc)
        else:
            self.work_space= work_space.WorkSpace()
            
        # first paned window
        main_panel = tk.PanedWindow(self, background='#C0DCF3')  
        main_panel.pack(fill=tk.BOTH, expand=1) 

        # second paned window
        left_panel = tk.PanedWindow(main_panel, orient=tk.VERTICAL)  
        main_panel.add(left_panel)  

        rack_frame = RackFrame.construct(left_panel, self)
        left_panel.add(rack_frame)

        self.content_frame = ContentFrame(main_panel)
        main_panel.add(self.content_frame)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def open_work_space_dialog(self):
        dir = filedialog.askdirectory()
        if len(dir)>0:
            self.open_work_space(dir)
        #self.v.set('xxx')

    def open_work_space(self, path):
        global work_space_loc
        save_geometry(self.geometry())
        work_space_loc = path
        self.destroy()

    def on_closing(self):
        global live 
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            save_geometry(self.geometry())
            live = False
            self.destroy()
            
    def open_doc(self):
        wp = work_space.get_location_path()
        doc_path = wp.joinpath('doc/html/publish/index.html')
        if doc_path.exists():
            os.system(f'start {doc_path.as_posix()}/')            
        else:
            if messagebox.askokcancel("Doc problems", "Can't find local documentation. Do you want to open it online?"):
                url = 'https://temper8.github.io/FRTC_v2'
                os.startfile(url)

    def show_RunAstraPage(self):
        print('show_calc_view')
        view = RunAstraPage(self.content_frame)  
        self.content_frame.set_content(view)

    def show_about(self):
        my_version = get_version('WaveTopBox')
        messagebox.showinfo("WaveTop Box", f"version {my_version}")

    def show_FolderItem(self, folder_item):
        
        match folder_item.model_kind:
            case 'ExpModel':
                model = ModelFactory.load(folder_item)
                page = ExpPage(self.content_frame, folder_item, model)                     
            case 'EquModel':
                model = ModelFactory.load(folder_item)
                page = TextPage(self.content_frame, folder_item, model)     
            case 'SbrModel':
                model = ModelFactory.load(folder_item)
                page = TextPage(self.content_frame, folder_item, model)                   
            case 'RaceModel':
                #model = RaceModel(path= view_item.path )  
                page = RacePage(self.content_frame, folder_item)                 
            case 'RTModel':
                model = ModelFactory.load(folder_item)
                page = RayTracingPage(self.content_frame, folder_item, model)                  
            case 'FRTCModel':
                #model = ModelFactory.load(folder_item)
                page = FRTCPage(self.content_frame, folder_item)                    
            case 'SpectrumModel':
                #model = ModelFactory.load(folder_item)
                page = SpectrumPage(self.content_frame, folder_item)                    
            case _:
                print('create Emptyview')
                page = EmptyPage(self.content_frame)  
        self.content_frame.set_content(page)
    

    def create_impedance(self):
        model = model_factory.create_model('ImpedModel')
        work_space.save_model(model)
        work_space.refresh_folder('ImpedModel') 
        #page = FRTCPage(self.content_frame, None, model) 
        #self.content_frame.set_content(page)

        #self.show_model(model)

    def create_gauss_spectrum(self):
        print('create_gauss_spectrum')
        model = ModelFactory.create_spectrum_model('gauss')
        work_space.save_model(model)
        work_space.refresh_folder('SpectrumModel') 

    def create_spectrum_1D(self):
        print('create gcreate_spectrum_1D')
        model = ModelFactory.create_spectrum_model('spectrum_1D')
        work_space.save_model(model)
        work_space.refresh_folder('SpectrumModel') 

    def create_spectrum_2D(self):
        print('create gcreate_spectrum_2D')
        model = ModelFactory.create_spectrum_model('spectrum_2D')
        work_space.save_model(model)
        work_space.refresh_folder('SpectrumModel') 


    def create_scatter_spectrum(self):
        print('create scatter_spectrum')
        model = ModelFactory.create_spectrum_model('scatter_spectrum')
        work_space.save_model(model)
        work_space.refresh_folder('SpectrumModel') 


    def open_command(self, arg):
        print('open command', arg)
        self.open_work_space(arg)

    def create_open_recent_menu(self):
        menu = tk.Menu(tearoff=0)
        hi = history.get_list()
        for item in reversed(hi):
            menu.add_command(label=item, command= partial(self.open_command, item))
        return menu

    def create_main_menu(self):
        new_menu = tk.Menu(tearoff=0)
        new_menu.add_command(label='Impedance', command=self.create_impedance)
        new_menu.add_command(label='Experiments', state='disabled')
        new_menu.add_command(label='Equlibrium', state='disabled')
        new_menu.add_command(label='gauss spectrum', command=self.create_gauss_spectrum)
        new_menu.add_command(label='spectrum 1D', command=self.create_spectrum_1D)
        new_menu.add_command(label='spectrum 2D', command=self.create_spectrum_2D)
        new_menu.add_command(label='scatter spectrum', command=self.create_scatter_spectrum)

        file_menu = tk.Menu(tearoff=0)
        file_menu.add_cascade(label="New", menu=new_menu)
        file_menu.add_command(label="Open Workspace", command=self.open_work_space_dialog)
        file_menu.add_cascade(label="Open Recent", menu= self.create_open_recent_menu())
        file_menu.add_command(label="Save", state='disabled')
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        main_menu = tk.Menu()
        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Help", command=self.open_doc)
        main_menu.add_cascade(label="About", command=self.show_about)
        return main_menu