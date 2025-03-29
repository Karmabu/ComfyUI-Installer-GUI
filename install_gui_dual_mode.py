import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import json
import os
import sys
import re

class InstallFromJsonApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ComfyUI Installer - Standard / Pro")
        self.master.geometry("900x600")
        self.steps = []

        self.standard_var = tk.BooleanVar()
        self.pro_var = tk.BooleanVar()
        self.json_path = tk.StringVar()
        self.prereq_path = tk.StringVar(value="prerequisites_check.json")

        top_frame = tk.Frame(master)
        top_frame.pack(pady=10, padx=10, anchor="w")

        # Standard Mode
        self.standard_cb = tk.Checkbutton(
            top_frame, text="Comfy Standard", variable=self.standard_var,
            command=self.select_standard_mode
        )
        self.standard_cb.grid(row=0, column=0, sticky="w", padx=5)

        # Pro Mode
        self.pro_cb = tk.Checkbutton(
            top_frame, text="Comfy Pro", variable=self.pro_var,
            command=self.select_pro_mode
        )
        self.pro_cb.grid(row=1, column=0, sticky="w", padx=5)

        # Custom JSON
        self.custom_button = ttk.Button(top_frame, text="📂 Load Custom JSON", command=self.load_custom_json)
        self.custom_button.grid(row=0, column=1, rowspan=2, padx=10)

        self.command_listbox = tk.Listbox(master, height=8, font=('Courier', 10))
        self.command_listbox.pack(fill=tk.X, padx=10, pady=(5, 10))

        self.output_label = tk.Label(master, text="Log:")
        self.output_label.pack()
        self.output_text = tk.Text(master, height=15, bg="black", fg="lime", insertbackground="white")
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10)
        self.output_text.config(state=tk.DISABLED)

        self.progress = ttk.Progressbar(master, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, padx=10, pady=10)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)

        self.check_button = ttk.Button(button_frame, text="🔍 Check Prerequisites", command=self.check_prerequisites)
        self.check_button.pack(side=tk.LEFT, padx=10)

        self.run_button = ttk.Button(button_frame, text="▶ Run Installation", command=self.run_installation)
        self.run_button.pack(side=tk.LEFT, padx=10)

    def select_standard_mode(self):
        self.pro_var.set(False)
        if self.standard_var.get():
            self.load_json_from_path("install_standard.json")

    def select_pro_mode(self):
        self.standard_var.set(False)
        if self.pro_var.get():
            self.load_json_from_path("install_full_comfyui.json")

    def load_custom_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.load_json_from_path(file_path)

    def load_json_from_path(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.json_path.set(path)
            self.steps = data.get("steps", [])
            self.command_listbox.delete(0, tk.END)
            for step in self.steps:
                self.command_listbox.insert(tk.END, f"✔ {step['name']}")
            self.write_log(f"Loaded JSON file: {os.path.basename(path)}")
            self.progress['value'] = 0
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {e}")

    def write_log(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def run_installation(self):
        if not self.steps:
            messagebox.showwarning("Warning", "Please load a JSON file first.")
            return
        threading.Thread(target=self.execute_commands, daemon=True).start()

    def execute_commands(self):
        self.progress['maximum'] = len(self.steps)
        self.progress['value'] = 0
        for idx, step in enumerate(self.steps):
            name = step.get("name", f"Step {idx+1}")
            command = step.get("command", "")
            self.write_log(f"▶ {name}...")
            try:
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        self.write_log(line.strip())
                if process.returncode == 0:
                    self.write_log(f"✔ Completed: {name}\n")
                else:
                    self.write_log(f"✖ Error in: {name} (code {process.returncode})\n")
            except Exception as e:
                self.write_log(f"✖ Error during '{name}': {e}")
            self.progress['value'] += 1

    def check_prerequisites(self):
        threading.Thread(target=self._run_check_prereq, daemon=True).start()

    def _run_check_prereq(self):
        self.write_log("🔎 Checking prerequisites...")
        try:
            with open(self.prereq_path.get(), "r", encoding="utf-8") as f:
                prerequisites = json.load(f)
        except Exception as e:
            self.write_log(f"Error loading prerequisites file: {e}")
            return

        python_min = prerequisites.get("python", {}).get("min_version")
        cuda_min = prerequisites.get("cuda", {}).get("min_version")
        if python_min:
            actual_python = sys.version.split()[0]
            self.write_log(f"→ Python installed: {actual_python} (required: {python_min})")
            if self.compare_versions(actual_python, python_min):
                self.write_log("   ✅ Python version OK")
            else:
                self.write_log("   ❌ Python version NOT sufficient")

        if cuda_min:
            cuda_version = self.get_cuda_version()
            self.write_log(f"→ CUDA installed: {cuda_version or 'not found'} (required: {cuda_min})")
            if cuda_version and self.compare_versions(cuda_version, cuda_min):
                self.write_log("   ✅ CUDA version OK")
            else:
                self.write_log("   ❌ CUDA version NOT sufficient")

        for check in prerequisites.get("checks", []):
            name = check.get("name", "Check")
            ctype = check.get("type")
            self.write_log(f"→ {name}")
            try:
                if ctype == "executable":
                    cmd = check["command"]
                    expected = check.get("expected_output_contains", "")
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if expected.lower() in result.stdout.lower():
                        self.write_log(f"   ✅ Command OK ({expected})")
                    else:
                        self.write_log(f"   ❌ Unexpected output: {result.stdout.strip()}")
                elif ctype == "file_exists":
                    if os.path.isfile(check["path"]):
                        self.write_log("   ✅ File found")
                    else:
                        self.write_log("   ❌ File not found")
                elif ctype == "directory_exists":
                    if os.path.isdir(check["path"]):
                        self.write_log("   ✅ Directory found")
                    else:
                        self.write_log("   ❌ Directory not found")
                else:
                    self.write_log(f"   ❓ Unknown check type: {ctype}")
            except Exception as e:
                self.write_log(f"   ❌ Error during check: {e}")

        self.write_log("✅ Prerequisite check completed.\n")

    def get_cuda_version(self):
        try:
            output = subprocess.check_output(['nvcc', '--version'], stderr=subprocess.STDOUT, text=True)
            match = re.search(r'release (\d+\.\d+)', output)
            if match:
                return match.group(1)
        except Exception:
            return None

    def compare_versions(self, current, required):
        from packaging import version
        return version.parse(current) >= version.parse(required)

if __name__ == "__main__":
    root = tk.Tk()
    app = InstallFromJsonApp(root)
    root.mainloop()
