import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
import os
import requests

# === Config ===
CONFIG_FILE = "config/settings.json"
OLLAMA_ENABLED = False
OLLAMA_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434/api/generate"

def load_config():
    global OLLAMA_ENABLED, OLLAMA_MODEL, OLLAMA_URL
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            cfg = json.load(f)
            OLLAMA_ENABLED = cfg.get("enabled", False)
            OLLAMA_MODEL = cfg.get("model", "llama3")
            OLLAMA_URL = cfg.get("url", "http://localhost:11434/api/generate")

def save_config(enabled, model, url):
    cfg = {
        "enabled": enabled,
        "model": model,
        "url": url
    }
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f, indent=2)

# === JSON Functions ===
def load_json_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load file: {e}")
        return None

def save_json_file(data, path):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo("Saved", "JSON file saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to save file: {e}")

# === LLM Command Syntax Check ===
def check_command_llm(command):
    if not OLLAMA_ENABLED:
        return "LLM Check disabled"
    prompt = f"Is this Windows batch command syntactically correct? Just reply yes or no. Command: {command}"
    try:
        response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False})
        result = response.json()
        return result.get("response", "No response")
    except Exception as e:
        return f"LLM check error: {e}"

# === GUI ===
class JSONEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("K3U JSON Builder + LLM Syntax Check")
        self.json_data = {"steps": []}
        self.file_path = None
        self.current_index = None
        load_config()

        # --- Menu ---
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New JSON", command=self.new_json)
        file_menu.add_command(label="Load JSON", command=self.load_json)
        file_menu.add_command(label="Save JSON", command=self.save_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menubar)

        # --- Step List ---
        self.listbox = tk.Listbox(root, width=40, bg="black", fg="lime")
        self.listbox.pack(side="left", fill="y")
        self.listbox.bind("<<ListboxSelect>>", self.show_step)

        # --- Step Detail ---
        frame = tk.Frame(root)
        frame.pack(side="right", fill="both", expand=True)

        self.name_entry = tk.Entry(frame, bg="black", fg="yellow", insertbackground="white")
        self.name_entry.pack(fill="x")

        self.command_entry = scrolledtext.ScrolledText(frame, height=6, bg="black", fg="white", insertbackground="white")
        self.command_entry.pack(fill="x")

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=5)

        self.save_step_button = tk.Button(btn_frame, text="Save Step", command=self.save_step)
        self.save_step_button.pack(side="left", padx=5)

        self.add_step_button = tk.Button(btn_frame, text="Add Step", command=self.add_step)
        self.add_step_button.pack(side="left", padx=5)

        self.delete_step_button = tk.Button(btn_frame, text="Delete Selected Step", command=self.delete_step)
        self.delete_step_button.pack(side="left", padx=5)

        self.check_button = tk.Button(btn_frame, text="LLM Check Command", command=self.do_llm_check)
        self.check_button.pack(side="left", padx=5)

        # --- Syntax Result Dots ---
        indicator_frame = tk.Frame(frame)
        indicator_frame.pack(pady=5)
        self.green_dot = tk.Label(indicator_frame, text="●", fg="gray", font=("Arial", 18))
        self.green_dot.pack(side="left", padx=10)
        self.yellow_dot = tk.Label(indicator_frame, text="●", fg="gray", font=("Arial", 18))
        self.yellow_dot.pack(side="left", padx=10)
        self.red_dot = tk.Label(indicator_frame, text="●", fg="gray", font=("Arial", 18))
        self.red_dot.pack(side="left", padx=10)

        self.llm_console = scrolledtext.ScrolledText(frame, height=10, state='disabled', bg='black', fg='#90ee90')
        self.llm_console.pack(fill='both', expand=True)

        # --- LLM Config Bar (Light Background) ---
        config_bar = tk.Frame(frame, bg="white")
        config_bar.pack(fill="x", pady=5)

        self.llm_enabled_var = tk.BooleanVar(value=OLLAMA_ENABLED)
        tk.Checkbutton(config_bar, text="Enable LLM", variable=self.llm_enabled_var, bg="white", fg="black", selectcolor="white").pack(side="left", padx=5)

        tk.Label(config_bar, text="Model:", bg="white", fg="black").pack(side="left")
        self.model_entry = tk.Entry(config_bar, width=10)
        self.model_entry.insert(0, OLLAMA_MODEL)
        self.model_entry.pack(side="left", padx=5)

        tk.Label(config_bar, text="URL:", bg="white", fg="black").pack(side="left")
        self.url_entry = tk.Entry(config_bar, width=30)
        self.url_entry.insert(0, OLLAMA_URL)
        self.url_entry.pack(side="left", padx=5)

        tk.Button(config_bar, text="Save LLM", command=self.save_llm_settings).pack(side="left", padx=5)

    def save_llm_settings(self):
        global OLLAMA_ENABLED, OLLAMA_MODEL, OLLAMA_URL
        OLLAMA_ENABLED = self.llm_enabled_var.get()
        OLLAMA_MODEL = self.model_entry.get()
        OLLAMA_URL = self.url_entry.get()
        save_config(OLLAMA_ENABLED, OLLAMA_MODEL, OLLAMA_URL)

    def update_indicators(self, result):
        result_lower = result.lower()
        if "yes" in result_lower:
            self.green_dot.config(fg="green")
            self.yellow_dot.config(fg="gray")
            self.red_dot.config(fg="gray")
        elif "no" in result_lower:
            self.green_dot.config(fg="gray")
            self.yellow_dot.config(fg="gray")
            self.red_dot.config(fg="red")
        else:
            self.green_dot.config(fg="gray")
            self.yellow_dot.config(fg="yellow")
            self.red_dot.config(fg="gray")

    def new_json(self):
        self.json_data = {"steps": []}
        self.file_path = None
        self.refresh_list()
        self.name_entry.delete(0, tk.END)
        self.command_entry.delete("1.0", tk.END)

    def load_json(self):
        path = filedialog.askopenfilename(filetypes=[["JSON files", "*.json"]])
        if path:
            data = load_json_file(path)
            if data:
                self.file_path = path
                self.json_data = data
                self.refresh_list()

    def save_json(self):
        for i, step in enumerate(self.json_data["steps"]):
            if not step.get("name") or not step.get("command"):
                messagebox.showerror("Validation Error", f"Step {i+1} is incomplete.\nEach step must have both 'name' and 'command'.")
                return
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".json")
        if self.file_path:
            save_json_file(self.json_data, self.file_path)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for i, step in enumerate(self.json_data.get("steps", [])):
            self.listbox.insert(tk.END, f"{i+1}. {step.get('name', 'Unnamed')}")

    def show_step(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.save_step()
            self.current_index = selection[0]
            step = self.json_data["steps"][self.current_index]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, step.get("name", ""))
            self.command_entry.delete("1.0", tk.END)
            self.command_entry.insert(tk.END, step.get("command", ""))

    def add_step(self):
        name = self.name_entry.get().strip()
        command = self.command_entry.get("1.0", tk.END).strip()
        if name and command:
            self.json_data["steps"].append({"name": name, "command": command})
            self.refresh_list()
            self.name_entry.delete(0, tk.END)
            self.command_entry.delete("1.0", tk.END)
            self.current_index = None

    def save_step(self):
        if self.current_index is not None:
            self.json_data["steps"][self.current_index] = {
                "name": self.name_entry.get().strip(),
                "command": self.command_entry.get("1.0", tk.END).strip()
            }
            self.refresh_list()
            self.listbox.selection_set(self.current_index)

    def delete_step(self):
        selection = self.listbox.curselection()
        if selection:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this step?")
            if confirm:
                index = selection[0]
                del self.json_data["steps"][index]
                self.refresh_list()
                self.name_entry.delete(0, tk.END)
                self.command_entry.delete("1.0", tk.END)
                self.current_index = None

    def do_llm_check(self):
        command = self.command_entry.get("1.0", tk.END).strip()
        if command:
            result = check_command_llm(command)
            self.update_indicators(result)
            self.llm_console.config(state='normal')
            self.llm_console.insert(tk.END, f"\n>> {command}\n{result}\n")
            self.llm_console.config(state='disabled')


if __name__ == '__main__':
    root = tk.Tk()
    app = JSONEditorApp(root)
    root.mainloop()
