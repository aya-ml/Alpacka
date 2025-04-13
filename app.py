import customtkinter as ctk
from navigator import Navigator
from mainframe import MainFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        self._setup()
        self._set_frame()
        
    def _setup(self):
        self.title("Alpacka")
        
        screen_width  = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_width     = 900
        app_height    = 600
        
        self.geometry(f"{app_width}x{app_height}+{screen_width // 2 - app_width // 2}+{screen_height // 2 - app_height // 2}")
        self.minsize(app_width, app_height)

        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        self.grid_rowconfigure(0, weight=1)

        self.configure(fg_color="#FAFAFB")
        
        ctk.set_appearance_mode("Light")
    
    def _set_frame(self):
        self.navigator = Navigator(self)
        self.navigator.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.mainframe = MainFrame(self)
        self.mainframe.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")