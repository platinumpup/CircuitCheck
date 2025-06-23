import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import font
import tkinter.messagebox as messagebox
import requests
import webbrowser
import sys
import os

# --- Forced Update Settings ---
APP_VERSION = "1.0.0"
VERSION_URL = "https://gist.githubusercontent.com/platinumpup/c1452bff8d1ad63464bd730e3d316b4c/raw/a197d527542442b82ae2cfceb12021dc31393c05/circuitcheck_version.txt"
UPDATE_PAGE = "https://github.com/platinumpup/CircuitCheck/releases/latest"

def check_forced_update():
    try:
        resp = requests.get(VERSION_URL, timeout=6)
        latest_version = resp.text.strip()
        if latest_version != APP_VERSION:
            messagebox.showerror(
                "Update Required",
                f"A new version ({latest_version}) of CircuitCheck© is required.\n"
                "Please update to continue."
            )
            webbrowser.open(UPDATE_PAGE)
            sys.exit(0)
    except Exception as e:
        messagebox.showerror(
            "Update Check Failed",
            "Could not verify the latest version of CircuitCheck©.\nPlease check your internet connection."
        )
        sys.exit(1)

ROOM_URLS = {
    "Adam Solinho": "https://zoom.us/thispagedoesnotexist",
    "BeatSync": "https://beat-sync.cloud",
    "Breeder's Lounge": "https://zoom.us/thispagedoesnotexist",
    "Elevate": "https://zoom.us/thispagedoesnotexist",
    "Higher Echelon": "https://cloudyshenanigans.online",
    "High Towers": "https://zoom.us/thispagedoesnotexist",
    "H⋀UZ": "https://zoom.us/thispagedoesnotexist",
    "Official310": "http://official310.live",
    "NJ's Kingdom": "https://njskingdom.life",
    "La Nube": "https://lazoom.link/",
    "Pregame": "https://zoom.us/thispagedoesnotexist",
    "PЯIMΞ": "https://zoom.us/thispagedoesnotexist",
    "pupCULTURE": "https://susnation.live/",
    "TLR": "https://zoom.us/thispagedoesnotexist",
    "This Place": "https://zoom.us/thispagedoesnotexist",
    "TwackCity": "https://twack-city.com/",
    "SHOWOFF": "https://tr.ee/701",
    "WOOFBEAR": "https://zoom.us/thispagedoesnotexist",
    "ᴛʜᴇVIPᴿᴼᴼᴹ": "pnpatvip.com",
}

def resource_path(relative_path):
    # Works for both script and PyInstaller .exe
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def show_readme():
    popup = tk.Toplevel()
    popup.title("README")
    popup.geometry("1800x450")  # Updated width to 1600

    st = ScrolledText(popup, wrap=tk.WORD)

    # Attempt to use Ubuntu Mono 12pt
    try:
        ubuntu_mono = font.Font(family="Ubuntu Mono", size=12)
        st.configure(font=ubuntu_mono)
    except Exception:
        st.configure(font=("Courier New", 12))

    st.pack(fill="both", expand=True)
    readme_path = resource_path("README.txt")
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            text = f.read()
        st.insert("1.0", text)
    except Exception as e:
        st.insert("1.0", f"Could not open README.txt:\n{e}")
    st.tag_configure("tight", spacing1=0, spacing2=0, spacing3=0)
    st.tag_add("tight", "1.0", "end")
    st.configure(state="disabled")

def is_url_open(url):
    try:
        resp = requests.head(url, timeout=7, allow_redirects=True)
        return resp.status_code in (200, 301, 302, 307, 308)
    except Exception:
        return False

def check_room():
    room_name = combo.get()
    url = ROOM_URLS.get(room_name)
    if not url:
        messagebox.showerror("CircuitCheck©", "Please select a room.")
        return
    status_label.config(text=f"Checking {room_name}...")
    window.update()
    if is_url_open(url):
        def join():
            webbrowser.open(url)
            popup.destroy()
        popup = ttkb.Toplevel(window)
        popup.title("Room is OPEN!")
        popup.geometry("320x210")
        ttkb.Label(popup, text=f"{room_name} is OPEN!", font=("Segoe UI", 13)).pack(pady=12)
        join_btn = ttkb.Button(popup, text="Join Room", bootstyle=SUCCESS, command=join, width=14)
        join_btn.pack(pady=6)
        close_btn = ttkb.Button(popup, text="Close", bootstyle=SECONDARY, command=popup.destroy, width=14)
        close_btn.pack(pady=4)
        status_label.config(text="Ready")
    else:
        messagebox.showinfo("CircuitCheck©", f"{room_name} is CLOSED.")
        status_label.config(text="Ready")

# --- GUI setup ---
window = ttkb.Window(themename="superhero")
window.title("CircuitCheck©")
window.geometry("380x340")
window.resizable(False, False)

ttkb.Label(window, text="Select Circuit Room:", font=("Segoe UI", 11)).pack(pady=14)
combo = ttkb.Combobox(window, values=list(ROOM_URLS.keys()), state="readonly", font=("Segoe UI", 11))
combo.pack(pady=8)
combo.current(0)

ttkb.Button(window, text="Check Room Status", bootstyle=PRIMARY, command=check_room, width=20).pack(pady=20)
status_label = ttkb.Label(window, text="Ready", font=("Segoe UI", 10), bootstyle=INFO)
status_label.pack(pady=8)

ttkb.Button(window, text="Show README", bootstyle=SECONDARY, command=show_readme, width=20).pack(pady=5)

# --- Force update check before mainloop ---
check_forced_update()
window.mainloop()
