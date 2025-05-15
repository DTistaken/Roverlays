import configparser
import logging
import os
import subprocess
import sys
from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage

import customtkinter as ctk

# --- Setup logging ---
LOG_FILE = Path(__file__).parent.parent / "roverlays.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] [GUI] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a'),
    ]
)
logger = logging.getLogger("GUI")

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_PATH = BASE_DIR / "assets" / "frame0"
SETTINGS_FILE = BASE_DIR / "settings.ini"
WATCHER_PATH = BASE_DIR.parent / "scripts" / "watcher.pyw"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / path

def load_settings():
    config = configparser.ConfigParser()
    if SETTINGS_FILE.exists():
        config.read(SETTINGS_FILE)
        keystrokes = config.getboolean("Settings", "Keystrokes", fallback=False)
        logger.debug(f"Loaded settings.ini with Keystrokes = {keystrokes}")
        return keystrokes
    else:
        logger.warning(f"{SETTINGS_FILE} does not exist. Defaulting Keystrokes to False.")
        return False

def save_settings(keystrokes: bool):
    config = configparser.ConfigParser()
    if SETTINGS_FILE.exists():
        config.read(SETTINGS_FILE)
    if "Settings" not in config:
        config["Settings"] = {}
    config["Settings"]["Keystrokes"] = str(keystrokes).lower()
    with open(SETTINGS_FILE, "w") as f:
        config.write(f)
    logger.debug(f"Saved Keystrokes = {keystrokes} to settings.ini")

# --- UI Setup ---
window = Tk()
window.title("Roverlays Dashboard")
window.geometry("700x450")
window.configure(bg="#2C2C2C")
window.resizable(False, False)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

canvas = Canvas(
    window,
    bg="#2C2C2C",
    height=450,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

canvas.create_rectangle(9.0, 12.0, 692.0, 64.0, fill="#0F0F0F", outline="")


def load_image_safe(name):
    try:
        return PhotoImage(file=relative_to_assets(name))
    except Exception as e:
        logger.error(f"Failed to load image {name}: {e}")
        return None

image_1 = load_image_safe("image_1.png")
if image_1:
    canvas.create_image(350.0, 128.0, image=image_1)

image_2 = load_image_safe("image_2.png")
if image_2:
    canvas.create_image(349.0, 210.0, image=image_2)

image_3 = load_image_safe("image_3.png")
if image_3:
    canvas.create_image(349.0, 292.0, image=image_3)

image_4 = load_image_safe("image_4.png")
if image_4:
    canvas.create_image(656.0, 430.0, image=image_4)

image_5 = load_image_safe("image_5.png")
if image_5:
    canvas.create_image(350.0, 374.0, image=image_5)

image_6 = load_image_safe("image_6.png")
if image_6:
    canvas.create_image(658.0, 430.0, image=image_6)

image_7 = load_image_safe("image_7.png")
if image_7:
    canvas.create_image(645.0, 128.0, image=image_7)

image_8 = load_image_safe("image_8.png")
if image_8:
    canvas.create_image(645.0, 209.0, image=image_8)

image_9 = load_image_safe("image_9.png")
if image_9:
    canvas.create_image(645.0, 295.0, image=image_9)

image_10 = load_image_safe("image_10.png")
if image_10:
    canvas.create_image(645.0, 374.0, image=image_10)

canvas.create_text(
    108.0,
    23.0,
    anchor="nw",
    text="Roverlays Dashboard",
    fill="#FFFFFF",
    font=("Inter Bold", -25)
)

image_11 = load_image_safe("image_11.png")
if image_11:
    canvas.create_image(41.0, 37.0, image=image_11)

canvas.create_text(
    77.0,
    109.0,
    anchor="nw",
    text="KeyStrokes",
    fill="#FFFFFF",
    font=("Inter Bold", -20)
)

image_12 = load_image_safe("image_12.png")
if image_12:
    canvas.create_image(48.0, 134.0, image=image_12)

canvas.create_text(
    77.0,
    134.0,
    anchor="nw",
    text="Shows keys you press and how fast you click.",
    fill="#FFFFFF",
    font=("Inter ExtraLight", -13)
)

checkbox_var = ctk.BooleanVar(value=False)

def checkbox_callback():
    val = checkbox_var.get()
    logger.debug(f"Checkbox changed: {val}")
    save_settings(val)

frame_bg = ctk.CTkFrame(master=window, fg_color="#565454", width=40, height=40, corner_radius=8)
frame_bg.place(x=645, y=128, anchor="center")

checkbox = ctk.CTkCheckBox(
    master=frame_bg,
    variable=checkbox_var,
    command=checkbox_callback,
    text="",
    font=ctk.CTkFont(size=20),
    width=30,
    height=30,
    fg_color="#565454",
    checkbox_width=20,
    checkbox_height=20,
)
checkbox.place(relx=0.5, rely=0.5, anchor="center")


initial_keystrokes = load_settings()
checkbox_var.set(initial_keystrokes)


def launch_watcher():
    try:
        subprocess.Popen(
            [sys.executable, str(WATCHER_PATH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        logger.info(f"Launched watcher.pyw: {WATCHER_PATH}")
    except Exception as e:
        logger.error(f"Failed to launch watcher.pyw: {e}")

launch_watcher()

try:
    logger.info("Starting GUI mainloop.")
    window.mainloop()
except Exception as e:
    logger.error(f"Exception in mainloop: {e}")
finally:
    logger.info("GUI closed.")
