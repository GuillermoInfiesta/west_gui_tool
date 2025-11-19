import shutil
import subprocess
import sys, os
import tkinter as tk
from tkinter import ttk, filedialog
import threading

class WorkspaceSelectFrame(tk.Tk):
    def __init__(self, root,  continue_cb, venv="", workspace=""):
        self.root = root
        self.main_frame = None
        self.select_venv_dir_frame = None
        self.venv_dir = tk.StringVar(value=venv)
        self.select_workspace_dir_frame = None
        self.workspace_dir = tk.StringVar(value=workspace)
        self.continue_button = None
        self.continue_cb = continue_cb

    def create_window(self, x, y, height, width):
        self.main_frame = tk.Frame(self.root, height=height, width=width)
        self.main_frame.place(x=x, y=y, height=height, width=width)

        #Search and select venv
        self.select_venv_dir_frame = tk.Frame(self.main_frame)
        self.select_venv_dir_frame.place(x=0, y=0, height=100, width=400)
        select_venv_text = tk.Entry(self.select_venv_dir_frame, width=300,
                                    state="readonly", textvariable=self.venv_dir)
        def venv_select():
            venv_dir = filedialog.askdirectory(mustexist=True)
            if os.path.exists(os.path.join(venv_dir, "Scripts", "python.exe")):
                self.venv_dir.set(venv_dir)
            else:
                self.venv_dir.set("Selected path is not a valid .venv")

        select_venv_button = tk.Button(self.select_venv_dir_frame, text="Select .venv dir", 
                                       command=venv_select)
        select_venv_button.pack(side="left")
        select_venv_text.pack(side="right")

        #Search and select workspace
        self.select_workspace_dir_frame = tk.Frame(self.main_frame)
        self.select_workspace_dir_frame.place(x=0, y=130, height=100, width=400)
        select_workspace_text = tk.Entry(self.select_workspace_dir_frame, width=300,
                                        state="readonly", textvariable= self.workspace_dir)
        def workspace_select():
            workspace_dir = filedialog.askdirectory(mustexist=True)
            if os.path.exists(os.path.join(workspace_dir, ".west", "config")):
                self.workspace_dir.set(workspace_dir)
            else:
                self.workspace_dir.set("Selected path is not a valid workspace")

        select_workspace_button = tk.Button(self.select_workspace_dir_frame, text="Select workspace dir",
                                            command=workspace_select)
        select_workspace_button.pack(side="left")
        select_workspace_text.pack(side="right")

        def on_continue_button():
            if (self.venv_dir.get() not in ["", "Selected path is not a valid .venv"] and
                self.workspace_dir.get() not in ["", "Selected path is not a valid workspace"]):

                self.continue_cb(self.venv_dir.get(), self.workspace_dir.get())

        self.continue_button = tk.Button(self.main_frame, text="Continue",
                                        command=on_continue_button)
        self.continue_button.pack(side="bottom")

    def get_frame(self):
        return self.main_frame