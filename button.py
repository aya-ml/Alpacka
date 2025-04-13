import customtkinter as ctk
from PIL import Image

class Button(ctk.CTkLabel):
    active = None
    
    def __init__(self, master, name=None, command=None, image=None, hover_image=None, size=(20, 20), **kwargs):
        kwargs.update(text='', fg_color='transparent', corner_radius=0, cursor='hand2')
        
        self.command = command
        self.name = name
        self.size = size
        self.active_img = ctk.CTkImage(Image.open(hover_image), size=self.size) if hover_image else None
        self.normal_img = ctk.CTkImage(Image.open(image), size=self.size) if image else None
        self.is_active = False
        
        super().__init__(master, image=self.normal_img, **kwargs)
        
        self.bind("<Enter>", lambda e: self.configure(image=self.active_img))
        self.bind("<Leave>", lambda e: not self.is_active and self.configure(image=self.normal_img))
        self.bind("<Button-1>", self.click)

    def click(self, event):
        if self.name in ['Scene', 'Analytics', 'Logs', 'Settings']:
            if Button.active: Button.active.deactivate()
            self.activate()
        if self.command: self.command()

    def activate(self):
        self.is_active = True
        Button.active = self
        self.configure(image=self.active_img)

    def deactivate(self):
        self.is_active = False
        self.configure(image=self.normal_img)

    def _change_button(self, img, hover_img):
        self.active_img = ctk.CTkImage(Image.open(hover_img), size=self.size)
        self.normal_img = ctk.CTkImage(Image.open(img), size=self.size)
        self.configure(image=self.active_img)