import tkinter as tk # for window
from pynput import keyboard # for hotkeys
import win32api # for cursor coords itself

# pos of the window that displays coords relative to cursor
OFFSET_X = -20
OFFSET_Y = 25

running = True  # whether the window is visible
keyboard_listener = None

root = tk.Tk()
root.overrideredirect(True)  # no window border
root.wm_attributes("-topmost", True) # keeps window above all other windows
root.config(bg="black")

label = tk.Label(root, font=("Segoe UI", 8, "bold"), fg="white", bg="gray20")
label.pack()

# updates window data and position every 15 ms while running
def update_position():
    if running:
        x, y = win32api.GetCursorPos()
        label.config(text=f"({x},{y})")
        root.geometry(f"+{x + OFFSET_X}+{y + OFFSET_Y}")
    root.after(15, update_position)
    
# hotkeys
def on_hotkey(key):
    global running, tray_icon, keyboard_listener
    try:
        # toggle visibility with F8
        if key == keyboard.Key.f8:
            running = not running
            # bool for toggling window visibility
            if not running:
                root.withdraw()
            else:
                root.deiconify()
        # quit with F7
        elif key == keyboard.Key.f7:
            try:
                if keyboard_listener:
                    keyboard_listener.stop()
            except Exception: # ignore errrors
                pass
            try:
                root.after(0, root.quit)
            except Exception:
                pass
    except Exception:
        pass

# create and start the keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_hotkey)
keyboard_listener.start()

# start window loop
update_position()
root.mainloop()