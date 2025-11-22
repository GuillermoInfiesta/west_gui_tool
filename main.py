import shutil
import subprocess
import sys, os
import tkinter as tk
from tkinter import ttk
import workspace_select_screen as wss
import workspace_cmd_screen as wcs
import threading

west_path=None
logging_box=None
logging_box_ocupation=0
_NEW_LINE_ = "\r\n"
_MAX_LOG_LINES=500

def display_log(line):
	global logging_box, logging_box_ocupation
	if(logging_box_ocupation + 1 > _MAX_LOG_LINES):
		logging_box.delete("1.0", "2.0")
		logging_box_ocupation = logging_box_ocupation - 1

	logging_box.insert(tk.END, line)
	logging_box_ocupation = logging_box_ocupation + 1
	logging_box.see(tk.END)
	logging_box.update_idletasks()

def run_west_command(command):
	global west_path, logging_box
	display_log(f"-> {west_path} {command}" + _NEW_LINE_)
	pc = subprocess.Popen(f"{west_path} {command}",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
			shell=True)

	for line in pc.stdout:
		display_log(line)
	pc.wait()

	return pc.stdout, pc.returncode

def set_paths_and_restart(venv_path, workspace_path):
	venv_path = os.path.join(venv_path, "Scripts", "python.exe")
	os.chdir(workspace_path)
	os.execv(venv_path, [venv_path, os.path.abspath(__file__)])

def paths_are_set():
	global west_path
	west_path = shutil.which('west')
	if west_path == None:
		return False
	if not os.path.exists(os.path.join(os.getcwd(), ".west", "config")):
		return False
	return True

def main():
	global west_path, logging_box

	#Add current python interpreter dir to PATH so west can be found coming from execv
	os.environ['PATH'] = os.path.dirname(sys.executable) + os.pathsep + os.environ['PATH']

	root = tk.Tk()
	root.title("West GUI Tool")
	root.geometry("1080x720")

	if not paths_are_set():
		wss_frame = wss.WorkspaceSelectFrame(root, set_paths_and_restart)
		wss_frame.create_window(10, 50, 600, 600)
		root.mainloop()
		return

	wcs_frame = wcs.WorkspaceCmdFrame(root, run_west_command)
	wcs_frame.create_window(10, 100, 1000, 300)

	frame = ttk.Frame(root)
	frame.pack(padx=20, pady=10, side="bottom", fill="x")
	logging_box = tk.Text(frame, state="normal", wrap="word", height=10, width=680)
	scroll = ttk.Scrollbar(frame, orient="vertical", command=logging_box.yview)
	logging_box.config(yscrollcommand=scroll.set)
	logging_box.pack(side="left")
	scroll.pack(side="right")
	
	display_log("Logs from west commands will show here" + _NEW_LINE_)
	root.mainloop()

if __name__ == "__main__":
	main()