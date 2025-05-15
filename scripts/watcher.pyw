import configparser
import logging
import psutil
import subprocess
import sys
import time
from pathlib import Path

# --- Setup paths ---
BASE_DIR = Path(__file__).resolve().parent.parent  
SETTINGS_FILE = BASE_DIR / "settings.ini"
KS_PATH = (BASE_DIR / "scripts" / "ks.pyw").resolve()
GUI_NAME = "gui.py"  

# --- Setup logging ---
LOG_FILE = BASE_DIR / "roverlays.log"

# Clear log on start
with open(LOG_FILE, "w"):
    pass

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] [Watcher] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Watcher")

last_keystrokes_value = None

def is_process_running_by_name(name_substring):
    name_substring = name_substring.lower()
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any(name_substring in arg.lower() for arg in cmdline):
                logger.debug(f"Found process PID {proc.pid} with cmdline: {cmdline}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def kill_ks_processes():
    killed_any = False
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any("ks.pyw" in part.lower() for part in cmdline):
                logger.debug(f"Terminating ks.pyw process PID {proc.pid}")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                    logger.info(f"ks.pyw process PID {proc.pid} terminated gracefully.")
                except psutil.TimeoutExpired:
                    logger.warning(f"ks.pyw process PID {proc.pid} did not terminate in time. Killing.")
                    proc.kill()
                    proc.wait(timeout=5)
                    logger.info(f"ks.pyw process PID {proc.pid} killed forcefully.")
                killed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.warning(f"Failed to terminate ks.pyw process PID {proc.pid if proc else 'unknown'}: {e}")
    if not killed_any:
        logger.debug("No ks.pyw processes found to terminate.")

def read_keystrokes_setting():
    config = configparser.ConfigParser()
    if not SETTINGS_FILE.exists():
        logger.warning(f"Settings file not found: {SETTINGS_FILE}")
        return False
    try:
        config.read(SETTINGS_FILE)
        return config.getboolean("Settings", "keystrokes", fallback=False)
    except Exception as e:
        logger.error(f"Error reading settings.ini: {e}")
        return False

def main():
    global last_keystrokes_value
    logger.info("Watcher started.")

    while True:
        try:
            gui_running = is_process_running_by_name(GUI_NAME)
            if not gui_running:
                logger.warning("GUI process not found. Exiting watcher and stopping ks.pyw if needed.")
                kill_ks_processes()
                sys.exit(0)

            keystrokes_enabled = read_keystrokes_setting()
            logger.debug(f"Keystrokes enabled = {keystrokes_enabled}")

            if keystrokes_enabled != last_keystrokes_value:
                last_keystrokes_value = keystrokes_enabled
                if keystrokes_enabled:
                    if not is_process_running_by_name("ks.pyw"):
                        logger.info(f"Starting ks.pyw: {KS_PATH}")
                        pythonw = Path(sys.executable).parent / "pythonw.exe"
                        subprocess.Popen([str(pythonw), str(KS_PATH)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        logger.debug("ks.pyw already running. No action taken.")
                else:
                    logger.info("Keystrokes disabled. Stopping ks.pyw if running.")
                    kill_ks_processes()

            time.sleep(1)

        except Exception as e:
            logger.exception(f"Error in watcher loop: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
