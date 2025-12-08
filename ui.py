import threading
import tkinter as tk

hint_callback = None  # Will be set by main.py


def start_ui():
    def on_hint_click():
        if hint_callback:
            hint_callback()

    root = tk.Tk()
    root.title("GameBot Hint Mode")
    root.geometry("180x60+20+20")  # small floating window
    root.attributes('-topmost', True)

    btn = tk.Button(root, text="ENTER HINT MODE", bg="#ffcc00", font=("Arial", 12),
                    command=on_hint_click)
    btn.pack(fill=tk.BOTH, expand=True)

    # Run UI loop in its own thread
    root.mainloop()


def launch_ui(callback):
    global hint_callback
    hint_callback = callback
    t = threading.Thread(target=start_ui, daemon=True)
    t.start()
