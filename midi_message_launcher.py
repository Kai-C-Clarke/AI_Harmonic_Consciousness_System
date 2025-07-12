import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

SCRIPT_PATH = "enhanced_symbolic_midi_tools_v1.5.py"

def validate_file():
    file_path = filedialog.askopenfilename(
        title="Select symbolic message JSON",
        filetypes=[("JSON files", "*.json")]
    )
    if not file_path:
        return
    try:
        subprocess.run(
            ["python3", SCRIPT_PATH, "validate", file_path],
            check=True
        )
        messagebox.showinfo("Validation", "✅ Validation passed.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Validation Failed", "❌ Validation failed. Check the terminal for details.")

def generate_file():
    file_path = filedialog.askopenfilename(
        title="Select symbolic message JSON to Generate",
        filetypes=[("JSON files", "*.json")]
    )
    if not file_path:
        return
    try:
        subprocess.run(
            ["python3", SCRIPT_PATH, "generate", file_path],
            check=True
        )
        messagebox.showinfo("MIDI Generated", "🎼 MIDI file successfully generated.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Generation Failed", "❌ Generation failed. Check the terminal for details.")

def open_generated_folder():
    gen_path = os.path.join(os.getcwd(), "generated_midis")
    if os.path.exists(gen_path):
        subprocess.run(["open", gen_path])  # For macOS
    else:
        messagebox.showwarning("Not Found", f"No generated_midis folder at:\n{gen_path}")

# GUI
root = tk.Tk()
root.title("AI MIDI Message Launcher")
root.geometry("320x160")

tk.Button(root, text="✅ Validate Message", width=30, command=validate_file).pack(pady=10)
tk.Button(root, text="🎼 Generate MIDI", width=30, command=generate_file).pack(pady=10)
tk.Button(root, text="📂 Open Output Folder", width=30, command=open_generated_folder).pack(pady=10)

root.mainloop()
