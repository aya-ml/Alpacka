import customtkinter as ctk
from button import Button

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._setup()

    def _setup(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color='transparent')
        
        self.navigator = FrameNavigation(master=self)
        self.navigator.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self.sceneframe = SceneFrame(master=self)
        self.sceneframe.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

class FrameNavigation(ctk.CTkFrame):
    def __init__(self, master):
        self.font = ("Nunito", 24, 'bold')
        self.text_color = "#000000"
        
        super().__init__(master)
        
        self._setup()

    def _setup(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.configure(fg_color='transparent', height=60, corner_radius=0)
        
        self.curr_label = ctk.CTkLabel(
            self,
            text=Button.active.name,
            height=60,
            font=self.font,
            text_color=self.text_color,
            anchor="center"
        )
        self.curr_label.grid(row=0, column=0, sticky="w", padx=(10, 0))

        self.settings_btn = Button(
            master=self,
            width=20,
            height=20,
            command=lambda: print("Settings clicked"),
            image="assets/default/Video.png",
            hover_image="assets/hover/Video.png"
        )
        self.settings_btn.grid(row=0, column=1, padx=(0, 10))

    def _change_text(self):
        self.curr_label.configure(text=Button.active.name)

class SceneFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self._setup()

    def _setup(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.font = ("Nunito", 20)
        self.text_color = "#030229"
        
        self.configure(fg_color='#FFFFFF', corner_radius=10)
        
        self.curr_label = ctk.CTkLabel(
            self,
            text="There will be video...",
            width=200,
            height=40,
            font=self.font,
            text_color=self.text_color,
            anchor="center"
        )
        self.curr_label.grid(row=0, column=0, padx=0)