import tkinter as tk
import threading

class WorkspaceCmdFrame(tk.Tk):
    def __init__(self, root, cmd_cb):
        self.root = root
        self.main_frame = tk.Frame(root)
        self.cmd_cb = cmd_cb
        self.diff_btn = tk.Button(self.main_frame, text="Run diff")
        self.clean_btn = tk.Button(self.main_frame, text="Clean workspace")
    
    def create_window(self, x, y, height, width):
        self.main_frame.config(height=height, width=width)
        self.main_frame.place(x=x, y=y, height=height, width=width)
        
        #Diff button
        def diff_btn_cb():
            self.__config_buttons_state(state=tk.DISABLED)
            self.cmd_cb("diff")
            self.__config_buttons_state(state=tk.ACTIVE)

        self.diff_btn.config(command=lambda: threading.Thread(target=diff_btn_cb).start())
        self.diff_btn.pack(padx=20, pady=20)

        #Clean workspace
        def clean_btn_cb():
            self.__config_buttons_state(state=tk.DISABLED)
            self.cmd_cb("forall -c \"git restore . && git clean -fdx\"")
            self.__config_buttons_state(state=tk.ACTIVE)

        self.clean_btn.config(command=lambda: threading.Thread(target=clean_btn_cb).start())
        self.clean_btn.pack(padx=100, pady=20)
        #Change active project
        #Update
    
    def __config_buttons_state(self, state):
        self.diff_btn.config(state=state)
        self.clean_btn.config(state=state)
