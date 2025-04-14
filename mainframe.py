import customtkinter as ctk
from button import Button
from frames import *

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

        self.curr_frame = SceneFrame(master=self)
        self.curr_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    def _switch_frame(self, new_frame):
        self.curr_frame.destroy()
        self.curr_frame = new_frame
        self.curr_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

class FrameNavigation(ctk.CTkFrame):
    def __init__(self, master):
        self.font        = ("Teachers", 20, "bold")
        self.text_color  = "#3193CA"

        super().__init__(master)
        
        self._setup()

    def _setup(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.configure(fg_color='transparent', height=60, corner_radius=0)
        
        self.curr_label = ctk.CTkLabel(
            self,
            text=Button.active.name.upper(),
            height=60,
            font=self.font,
            text_color=self.text_color,
            anchor="center"
        )
        self.curr_label.grid(row=0, column=0, sticky="w", padx=(10, 0))

        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=0, column=1, padx=0, pady=0)

    def _change_page(self):
        self.curr_label.configure(text=Button.active.name.upper())

        if Button.active.name == 'Scene':
            self.button_frame.grid()
        else:
            self.button_frame.grid_remove()
            

class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color='transparent')
        
        self._setup()

    def _setup(self):
        self.grid_columnconfigure((1, 2), weight=0)
        self.grid_rowconfigure(0, weight=1)

        self._is_playing = False
        self._is_video   = True

        self.play = Button(
            master=self,
            width=20,
            height=20,
            command=self._start_reconstruction,
            image="assets/default/Play.png",
            hover_image="assets/hover/Play.png"
        )
        self.play.grid(row=0, column=0, padx=(0, 10), pady=0)

        self.curr_mode = Button(
            master=self,
            width=20,
            height=20,
            command=self._set_mode,
            image="assets/default/Video.png",
            hover_image="assets/hover/Video.png"
        )
        self.curr_mode.grid(row=0, column=1, padx=(0, 10), pady=0)

    def _start_reconstruction(self):
        self._is_playing = not self._is_playing
        self.play._change_button(
            img="assets/default/Stop.png" if self._is_playing else "assets/default/Play.png",
            hover_img="assets/hover/Stop.png" if self._is_playing else "assets/hover/Play.png"
        )
        self.master.master.curr_frame.start_simulation() if self._is_playing else self.master.master.curr_frame.stop_simulation()

    def _set_mode(self):
        self._is_video = not self._is_video
        self.curr_mode._change_button(
            img="assets/default/Home.png" if not self._is_video else "assets/default/Video.png",
            hover_img="assets/hover/Home.png" if not self._is_video else "assets/hover/Video.png"
        )