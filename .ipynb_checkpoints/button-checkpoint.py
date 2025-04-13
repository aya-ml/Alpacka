import customtkinter as ctk
from PIL import Image

class Button(ctk.CTkLabel):
    active = None
    
    def __init__(self, master, name=None, command=None, image=None, hover_image=None, **kwargs):
        kwargs.update(text='', fg_color='transparent', corner_radius=0, cursor='hand2')
        
        self.command = command
        self.name = name
        self.active_img = ctk.CTkImage(Image.open(hover_image)) if hover_image else None
        self.normal_img = ctk.CTkImage(Image.open(image)) if image else None
        self.is_active = False
        
        super().__init__(master, image=self.normal_img, **kwargs)
        
        self.bind("<Enter>", lambda e: self.configure(image=self.active_img))
        self.bind("<Leave>", lambda e: not self.is_active and self.configure(image=self.normal_img))
        self.bind("<Button-1>", self.click)

    def click(self, event):
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