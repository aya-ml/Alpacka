import customtkinter as ctk
from button import Button

class SceneFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self._setup()

    def _setup(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.font = ("Teachers", 20)
        self.text_color = "#030229"
        
        self.configure(fg_color='#FFFFFF', corner_radius=10)
        
        self.curr_label = ctk.CTkLabel(
            self,
            text="There will be video...",
            width=200,
            height=40,
            font=self.font,
            text_color=self.text_color,
            anchor="w"
        )
        self.curr_label.grid(row=0, column=0, padx=0)

class AnalyticsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self._setup()

    def _setup(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.font = ("Teachers", 20)
        self.text_color = "#030229"
        
        self.configure(fg_color='#FFFFFF', corner_radius=10)
        
        self.logs = ctk.CTkLabel(
            self,
            text="There will be analytics...",
            font=self.font,
            text_color=self.text_color,
            anchor="w"
        )
        self.logs.grid(row=0, column=0, padx=10, pady=10)

class LogsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._setup()

    def _setup(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.font = ("Teachers", 14)
        self.text_color = "#030229"
        
        # Только основной фрейм имеет белый фон
        self.configure(fg_color='#FFFFFF', corner_radius=10)
        
        # Canvas с прозрачным фоном
        self.canvas = ctk.CTkCanvas(
            self, 
            highlightthickness=0,
            bg='#FFFFFF'  # Белый фон для canvas (или другой цвет по вашему выбору)
        )
        
        # Scrollbar с прозрачным фоном
        self.scrollbar = ctk.CTkScrollbar(
            self, 
            orientation="vertical", 
            command=self.canvas.yview,
            fg_color='transparent'
        )
        
        # Scrollable frame с прозрачным фоном
        self.scrollable_frame = ctk.CTkFrame(
            self.canvas,
            fg_color='transparent'
        )
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Метка с логами (прозрачный фон)
        self.logs_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Your logs will appear here...",
            font=self.font,
            text_color=self.text_color,
            anchor="nw",
            justify="left",
            wraplength=self.winfo_width() - 20,
            fg_color='transparent'
        )
        self.logs_label.pack(fill="x", padx=10, pady=10)

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self._setup()

    def _setup(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.font = ("Teachers", 20)
        self.text_color = "#030229"
        
        self.configure(fg_color='#FFFFFF', corner_radius=10)
        
        self.logs = ctk.CTkLabel(
            self,
            text="There will be settings...",
            font=self.font,
            text_color=self.text_color,
            anchor="w"
        )
        self.logs.grid(row=0, column=0, padx=10, pady=10)