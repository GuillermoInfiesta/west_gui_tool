import tkinter as tk
import threading
import os
from tkinter import filedialog

def get_workspace_manifest_path():
	west_config_path = os.path.join(os.getcwd(), ".west", "config")
	west_config = open(west_config_path)
	west_config.readline() #Discard first line
	manifest_path = west_config.readline().split("=")[1].strip()
	west_config.close()
	return manifest_path

def set_workspace_manifest_path(relative_path):
    west_config_path = os.path.join(os.getcwd(), ".west", "config")
    west_config = open(west_config_path, "r+")
    lines = west_config.readlines()
    lines[1] = f"path = {relative_path}\n"
    west_config.seek(0)
    west_config.writelines(lines)
    west_config.truncate()
    west_config.close()


class WorkspaceCmdFrame(tk.Tk):
    def __init__(self, root, cmd_cb):
        self.root = root
        self.main_frame = tk.Frame(root)
        self.cmd_cb = cmd_cb
        self.diff_btn = tk.Button(self.main_frame, text="Run diff")
        self.clean_btn = tk.Button(self.main_frame, text="Clean workspace")
        self.manifest_path = tk.Frame(self.main_frame)
        self.manifest_path_string = tk.StringVar(value=get_workspace_manifest_path())
        self.update_btn = tk.Button(self.main_frame, text="Update")
    
    def create_window(self, x, y, height, width):
        self.main_frame.config(height=height, width=width)
        self.main_frame.place(x=x, y=y, height=height, width=width)
        
        #Diff button
        def diff_btn_cb():
            self.__config_buttons_state(state=tk.DISABLED)
            self.cmd_cb("diff", True)
            self.__config_buttons_state(state=tk.ACTIVE)

        self.diff_btn.config(command=lambda: threading.Thread(target=diff_btn_cb).start())
        self.diff_btn.pack(padx=20, pady=20)

        #Clean workspace
        def clean_btn_cb():
            self.__config_buttons_state(state=tk.DISABLED)
            self.cmd_cb("forall -c \"git restore . && git clean -fdx\"", True)
            self.__config_buttons_state(state=tk.ACTIVE)

        self.clean_btn.config(command=lambda: threading.Thread(target=clean_btn_cb).start())
        self.clean_btn.pack(padx=100, pady=20)

        #Change active project
        self.manifest_path.place(x=0, y=200, height= 100, width=400)
        manifest_path_text = tk.Entry(self.manifest_path, width=300,
                                              state="readonly", textvariable=self.manifest_path_string)
        def manifest_path_select():
            manifest_path_dir = filedialog.askdirectory(mustexist=True)
            manifest_path_dir = os.path.normpath(manifest_path_dir)

            if(os.path.exists(os.path.join(manifest_path_dir, "west.yml")) and
               manifest_path_dir.startswith(os.getcwd())):
                relative_path = (os.path.relpath(manifest_path_dir, os.getcwd()))
                set_workspace_manifest_path(relative_path)
                self.manifest_path_string.set(get_workspace_manifest_path())

        manifest_path_button = tk.Button(self.manifest_path, text="Change manifest path",
                                         command=manifest_path_select)
        manifest_path_button.pack(side="left")
        manifest_path_text.pack(side="right")

        #Update
        def update_btn_cb():
            self.__config_buttons_state(tk.DISABLED)
            self.cmd_cb("update", True)
            self.cmd_cb("zephyr-export", True)
            _, rc = self.cmd_cb("packages pip --install", True)
            if(rc != 0):
                print("Zephyr orlder than v4.1.0")
                self.cmd_cb("pip install -r zephyr/scripts/requirements.txt", False)
            self.__config_buttons_state(tk.ACTIVE)

        self.update_btn.config(command=lambda: threading.Thread(target=update_btn_cb).start())
        self.update_btn.pack()

    
    def __config_buttons_state(self, state):
        self.diff_btn.config(state=state)
        self.clean_btn.config(state=state)
        self.update_btn.config(state=state)
