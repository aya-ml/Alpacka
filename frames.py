import customtkinter as ctk
from button import Button
from loggen import LogsCreator

import json
import os

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
        super().__init__(master, fg_color='#FFFFFF', corner_radius=10)
        self._setup()

    def _setup(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bg='#FFFFFF')
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview, button_color='#9A9AA9', button_hover_color='#9A9AA9', cursor='hand2')
        self.frame = ctk.CTkFrame(self.canvas, fg_color='transparent')
        
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        ctk.CTkLabel(
            self.frame,
            text=self.master.master.logs.read_logs(),
            font=("Courier New", 14),
            text_color="#030229",
            anchor="nw",
            justify="left",
            wraplength=self.winfo_width()-20
        ).pack(fill="x", padx=0, pady=0)
        
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scrollbar.grid(row=0, column=1, sticky="ns", padx=20, pady=20)

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.settings_file = "settings.json"
        self._setup()
        self.settings = self._load_settings()
        self._create_widgets()

    def _setup(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=0)
        self.grid_rowconfigure(8, weight=1)
        
        self.font = ("Teachers", 14)
        self.bold_font = ("Teachers", 14, "bold")
        self.button_font = ("Teachers", 12, "bold")
        self.text_color = "#030229"
        self.disabled_color = "#9A9AA9"
        self.selected_color = "#3193CA"
        self.slider_color = "#9A9AA9"
        self.button_color = "#3193CA"
        self.reset_color = "#9A9AA9"
        self.border_color = "#9A9AA9"
        self.configure(fg_color='#FFFFFF', corner_radius=10)

    def _load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file) as f:
                    return json.load(f)
            except:
                pass
        return {"algorithm": "SFM", "fps": 15, "cam_mode": "Auto", 
                "width": 1920, "height": 1080, "focal": 1000}

    def _save_settings(self):
        # Получаем текущие значения из интерфейса
        new_settings = {
            "algorithm": self.algo_var.get(),
            "fps": self.fps_var.get(),
            "cam_mode": self.cam_mode_var.get(),
            "width": int(self.width_entry.get()),
            "height": int(self.height_entry.get()),
            "focal": int(self.focal_entry.get())
        }
        
        has_changes = False
        changed_items = []
        
        for key, new_value in new_settings.items():
            if key not in self.settings or self.settings[key] != new_value:
                has_changes = True
                old_value = self.settings.get(key, "N/A")
                changed_items.append(f"{key}: {old_value} → {new_value}")
        
        if not has_changes:
            return
        
        self.settings = new_settings
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
        
        log_message = "Settings changed:\n" + "\n".join(changed_items)
        self.master.master.logs.add_log(log_message)

    def _create_widgets(self):
        ctk.CTkLabel(self, text="MAIN SETTINGS", font=self.bold_font, text_color=self.text_color
                   ).grid(row=0, column=0, padx=20, pady=(10,5), sticky="w")
        
        ctk.CTkLabel(self, text="Algorithm", font=self.font, text_color=self.text_color
                   ).grid(row=1, column=0, padx=20, pady=(0,5), sticky="w")
        
        self.algo_var = ctk.StringVar(value=self.settings["algorithm"])
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=2, column=0, padx=20, pady=(0,10), sticky="w")
        
        ctk.CTkRadioButton(frame, text="SFM", variable=self.algo_var, value="SFM", font=self.font,
                         text_color=self.text_color, fg_color=self.selected_color,
                         hover_color="#1F76A7", border_width_unchecked=2, border_width_checked=5,
                         radiobutton_width=14, radiobutton_height=14, border_color=self.selected_color
                         ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(frame, text="Neural Network", variable=self.algo_var, value="Neural Network",
                         font=self.font, text_color=self.text_color, fg_color=self.selected_color,
                         hover_color="#1F76A7", border_width_unchecked=2, border_width_checked=5,
                         radiobutton_width=14, radiobutton_height=14, border_color=self.selected_color
                         ).pack(side="left", padx=5)
        
        ctk.CTkLabel(self, text="FPS", font=self.font, text_color=self.text_color
                   ).grid(row=3, column=0, padx=20, pady=(0,5), sticky="w")
        
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=4, column=0, padx=20, pady=(0,10), sticky="w")
        
        self.fps_var = ctk.IntVar(value=self.settings["fps"])
        ctk.CTkSlider(frame, variable=self.fps_var, from_=5, to=30, width=160, height=10,
                     button_color=self.slider_color, button_hover_color=self.slider_color,
                     progress_color=self.slider_color, button_length=12,
                     command=lambda v: self.fps_value.configure(text=str(int(v)))).pack(side="left")
        
        self.fps_value = ctk.CTkLabel(frame, text=str(self.settings["fps"]), font=self.font,
                                   text_color=self.text_color, width=30)
        self.fps_value.pack(side="left", padx=5)
        
        ctk.CTkLabel(self, text="CAMERA SETTINGS", font=self.bold_font, text_color=self.text_color
                   ).grid(row=0, column=1, padx=20, pady=(10,5), sticky="w")
        
        ctk.CTkLabel(self, text="Camera mode", font=self.font, text_color=self.text_color
                   ).grid(row=1, column=1, padx=20, pady=(0,5), sticky="w")
        
        self.cam_mode_var = ctk.StringVar(value=self.settings["cam_mode"])
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=2, column=1, padx=20, pady=(0,10), sticky="w")
        
        ctk.CTkRadioButton(frame, text="Auto", variable=self.cam_mode_var, value="Auto", font=self.font,
                         text_color=self.text_color, fg_color=self.selected_color, hover_color="#1F76A7",
                         border_width_unchecked=2, border_width_checked=5, radiobutton_width=14,
                         radiobutton_height=14, border_color=self.selected_color,
                         command=self._toggle_manual).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(frame, text="Manual", variable=self.cam_mode_var, value="Manual", font=self.font,
                         text_color=self.text_color, fg_color=self.selected_color, hover_color="#1F76A7",
                         border_width_unchecked=2, border_width_checked=5, radiobutton_width=14,
                         radiobutton_height=14, border_color=self.selected_color,
                         command=self._toggle_manual).pack(side="left", padx=5)
        
        self.width_entry = self._create_entry("Width", "width", 3, 1)
        self.height_entry = self._create_entry("Height", "height", 4, 1)
        self.focal_entry = self._create_entry("Focal", "focal", 5, 1)
        self._toggle_manual()
        
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=9, column=0, columnspan=2, pady=(10,15), sticky="")
        frame.grid_columnconfigure((0,1), weight=1)
        
        ctk.CTkButton(frame, text="RESET", width=90, height=30, font=self.button_font,
                     fg_color=self.reset_color, text_color="white", hover_color="#737386",
                     corner_radius=10, command=self._reset_settings).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(frame, text="SAVE", width=90, height=30, font=self.button_font,
                     fg_color=self.button_color, text_color="white", hover_color="#1F76A7",
                     corner_radius=10, command=self._save_settings).grid(row=0, column=1, padx=5)

    def _create_entry(self, label, key, row, column):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=row, column=column, padx=20, pady=2, sticky="w")
        
        ctk.CTkLabel(frame, text=label, font=self.font, text_color=self.text_color,
                    width=60, anchor="w").pack(side="left", padx=(0,10))
        
        container = ctk.CTkFrame(frame, fg_color="#F5F5F5", corner_radius=4)
        container.pack(side="left")
        
        entry = ctk.CTkEntry(container, width=100, height=28, font=self.font,
                            fg_color="#FFFFFF", text_color=self.text_color,
                            border_color=self.border_color, border_width=1, corner_radius=4)
        entry.insert(0, str(self.settings[key]))
        entry.pack(padx=1, pady=1)
        setattr(self, f"{key}_entry", entry)
        return entry

    def _toggle_manual(self):
        manual = self.cam_mode_var.get() == "Manual"
        for name in ["width", "height", "focal"]:
            entry = getattr(self, f"{name}_entry")
            entry.configure(state="normal" if manual else "disabled",
                          fg_color="#FFFFFF" if manual else "#F5F5F5",
                          text_color=self.text_color if manual else self.disabled_color)

    def _reset_settings(self):
        self.algo_var.set("SFM")
        self.fps_var.set(15)
        self.cam_mode_var.set("Auto")
        for name, val in [("width", "1920"), ("height", "1080"), ("focal", "1000")]:
            entry = getattr(self, f"{name}_entry")
            entry.delete(0, 'end')
            entry.insert(0, val)
        self.fps_value.configure(text="15")
        self._toggle_manual()
        self._save_settings()