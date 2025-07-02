import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import sys
import os
import webbrowser

# =============================
# 🛡️ Admin Elevation
# =============================
def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()

def relaunch_as_admin():
    if sys.platform == "win32":
        import win32com.shell.shell as shell
        params = f'"{os.path.abspath(__file__)}"'
        shell.ShellExecuteEx(
            lpVerb='runas',
            lpFile=sys.executable,
            lpParameters=params,
            nShow=1
        )
        sys.exit(0)

if not is_admin():
    relaunch_as_admin()

# =============================
# 🖼️ Icons and App ID
# =============================
if sys.platform == "win32":
    try:
        from ctypes import windll
        app_id = u"CompressedMemoryApp.1.0"
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass

# Handle paths in frozen (PyInstaller) or script mode
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ICON_PATH = os.path.join(BASE_DIR, "Personal_Picture.ico")

# =============================
# 📊 PowerShell Commands
# =============================
POWERSHELL_COMMANDS = {
    "Check": 'Get-MMAgent | ForEach-Object { if ($_.MemoryCompression -eq $true) '
             '{ "[✓] Compressed Memory is ENABLED." } else { "[X] Compressed Memory is DISABLED." } }',
    "Disable": 'Disable-MMAgent -MemoryCompression; '
               '"[!] Compressed Memory has been DISABLED. Restart your system."',
    "Enable": 'Enable-MMAgent -MemoryCompression; '
              '"[✓] Compressed Memory has been ENABLED. Restart your system."'
}

def run_powershell(command_key):
    try:
        output = subprocess.check_output(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-Command", POWERSHELL_COMMANDS[command_key]
            ],
            stderr=subprocess.STDOUT,
            text=True,
            shell=True
        ).strip()

        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output)

        if "ENABLED" in output:
            start = output.find("ENABLED")
            end = start + len("ENABLED")
            output_text.tag_config("enabled", foreground="green")
            output_text.tag_add("enabled", f"1.{start}", f"1.{end}")
        elif "DISABLED" in output:
            start = output.find("DISABLED")
            end = start + len("DISABLED")
            output_text.tag_config("disabled", foreground="red")
            output_text.tag_add("disabled", f"1.{start}", f"1.{end}")

        output_text.config(state='disabled')

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Something went wrong:\n\n{e.output}")

# =============================
# 🔗 External Links
# =============================
def open_coffee_link():
    webbrowser.open_new("https://coindrop.to/mr-shan")  # Replace this!

def open_github():
    webbrowser.open_new("https://github.com/Mr-Muhammad-Kashan")  # Replace this!

# =============================
# 🎨 GUI Setup
# =============================
window = tk.Tk()
window.title("Compressed Memory Control Tool")
window.geometry("760x660")
window.resizable(False, False)

# Set icon
try:
    window.iconbitmap(ICON_PATH)
except Exception as e:
    print(f"[!] Could not set icon: {e}")

# Title
title_label = tk.Label(window, text="Compressed Memory Control Tool", font=("Segoe UI", 18, "bold"))
title_label.pack(pady=10)

# Buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=5)

check_btn = tk.Button(
    button_frame, text="Check Status", width=20, height=2,
    bg="#FFD700", fg="black", activebackground="#FFC300",
    font=("Segoe UI", 10),
    command=lambda: run_powershell("Check")
)
check_btn.grid(row=0, column=0, padx=10)

disable_btn = tk.Button(
    button_frame, text="Disable Compression", width=20, height=2,
    bg="#FF4C4C", fg="white", activebackground="#CC0000",
    font=("Segoe UI", 10),
    command=lambda: run_powershell("Disable")
)
disable_btn.grid(row=0, column=1, padx=10)

enable_btn = tk.Button(
    button_frame, text="Enable Compression", width=20, height=2,
    bg="#4CAF50", fg="white", activebackground="#2E7D32",
    font=("Segoe UI", 10),
    command=lambda: run_powershell("Enable")
)
enable_btn.grid(row=0, column=2, padx=10)

# Output
output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=85, height=4, font=("Segoe UI", 10))
output_text.pack(pady=10, padx=10)
output_text.insert(tk.END, "Click a button to see or change Compressed Memory status.")
output_text.config(state='disabled')

# Info Section
info_text = tk.Label(
    window,
    text=(
        "\nWhat is Compressed Memory?\n\n"
        "Compressed Memory is a feature in Windows that stores infrequently-used data in RAM in a compressed format\n"
        "to avoid swapping it to disk. This saves space and improves performance on low-RAM systems.\n\n"
        "• Enable it if: You have 4GB, 8GB, or 16GB RAM and want to keep apps smooth.\n"
        "• Disable it if: You have 32GB, 64GB, or 128GB+ RAM and want max performance without compression overhead.\n\n"
        "This app automatically applies the setting to your system. A system restart is recommended after making changes."
    ),
    justify="left",
    font=("Segoe UI", 11),
    fg="gray20",
    wraplength=720
)
info_text.pack(padx=20, pady=10, anchor="w")

# Footer Containers
footer_frame = tk.Frame(window)
footer_frame.pack(side="bottom", fill="x", padx=20, pady=10)

# GitHub on Left
github_container = tk.Frame(footer_frame)
github_container.pack(side="left", anchor="sw")

github_msg = tk.Label(
    github_container,
    text="Check out my other tools on GitHub!",
    font=("Segoe UI", 8),
    fg="#800080",
    justify="left"
)
github_msg.pack(anchor="w")

github_btn = tk.Button(
    github_container,
    text="🔗 GitHub",
    font=("Segoe UI", 9, "bold"),
    bg="#B266FF",
    fg="white",
    activebackground="#9933FF",
    width=14,
    height=1,
    command=open_github
)
github_btn.pack(anchor="w", pady=(3, 0))

# Coffee on Right
coffee_container = tk.Frame(footer_frame)
coffee_container.pack(side="right", anchor="se")

coffee_msg = tk.Label(
    coffee_container,
    text="Like this product?\nCare to buy me a coffee ☕ to keep these free tools coming!",
    font=("Segoe UI", 8),
    fg="brown",
    justify="right"
)
coffee_msg.pack(anchor="e")

coffee_btn = tk.Button(
    coffee_container,
    text="☕ Buy Me a Coffee",
    font=("Segoe UI", 9, "bold"),
    bg="#FFDD00",
    fg="black",
    activebackground="#FFC107",
    width=18,
    height=1,
    command=open_coffee_link
)
coffee_btn.pack(anchor="e", pady=(3, 5))

# Launch
window.mainloop()
# ================================
# End of Compressed Memory Control Tool Script
# ================================