import shutil
import subprocess
import sys, os
import tkinter as tk
from tkinter import ttk
import threading

west_path=None
diff_button=None
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
	global west_path, diff_button, logging_box
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

def west_diff():
	global diff_button
	diff_button.config(state=tk.DISABLED, text="Running diff")
	logs, rc = run_west_command("diff")
	diff_button.config(state=tk.NORMAL, text="Run diff")

def on_diff_button():
	threading.Thread(target=west_diff).start()

def search_venv():
	print("Searching .venv ...")
	venv_expected_path = os.path.join("..", ".venv", "Scripts", "python.exe")
	venv_expected_path = os.path.abspath(venv_expected_path)
	if os.path.exists(venv_expected_path):
		print("Venv found, rerunning program")
		os.execv(venv_expected_path, [venv_expected_path, os.path.abspath(__file__)])
	else:
		print("Venv not found")

def main():
	global west_path, diff_button, logging_box

	#Add current python interpreter dir to PATH so west can be found coming from execv
	os.environ['PATH'] = os.path.dirname(sys.executable) + os.pathsep + os.environ['PATH']
	
	west_path = shutil.which('west')
	if west_path:
		print(f"West found at {west_path}")
	else:
		search_venv()
		return

	root = tk.Tk()
	root.title("West GUI Tool")
	root.geometry("1080x720")

	diff_button = tk.Button(root, text="Run diff", command=on_diff_button)
	diff_button.pack(padx=20, pady=20)

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