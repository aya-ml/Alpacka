import customtkinter as ctk
from PIL import Image
from button import Button

class Navigator(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color='#FFFFFF', width=50, corner_radius=10)
        
        self._setup()

    def _setup(self):
        self.grid_columnconfigure(0, weight=1)
        rows = [0, 1, 2, 3, 4, 6]
        for r in rows:
            self.grid_rowconfigure(r, weight=0)
        self.grid_rowconfigure(5, weight=1)

        self.logo = ctk.CTkLabel(self, image=ctk.CTkImage(light_image=Image.open("assets/logo/logo.png"), size=(30, 30)), text="")
        self.logo.grid(row=0, column=0, padx=0, pady=(15, 15))

        buttons = [
            (1, 'Scene', 'Category', (0, 15), lambda: self._cmd('Scene')),
            (2, 'Analytics', 'Chart', (0, 15), lambda: self._cmd('Analytics')),
            (3, 'Logs', 'Document', (0, 15), lambda: self._cmd('Logs')),
            (4, 'Settings', 'Setting', 0, lambda: self._cmd('Settings')),
            (6, 'Quit', 'Logout', (0, 15), self._quit)
        ]

        for row, name, img, pady, cmd in buttons:
            btn = Button(
                master=self,
                name=name,
                width=50,
                height=20,
                command=cmd,
                image=f"assets/default/{img}.png",
                hover_image=f"assets/hover/{img}.png"
            )
            btn.grid(row=row, column=0, padx=0, pady=pady)
            setattr(self, name, btn)
            
            if name == 'Scene':
                btn.activate()

    def _cmd(self, name):
        self.master.mainframe.navigator._change_text()
        print(name)

    def _quit(self):
        self.master.destroy()