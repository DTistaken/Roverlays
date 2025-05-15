import subprocess
import sys
import time
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.resolve()
GUI_PATH = BASE_DIR / "scripts" /"gui.pyw" 
WATCHER_PATH = BASE_DIR / "scripts" / "watcher.pyw"

LOG_FILE = BASE_DIR / "roverlays.log"

def clear_log():
    try:
        with open(LOG_FILE, "w") as f:
            f.truncate(0)
    except Exception:
        pass

def launch_script(script_path):
    kwargs = dict(
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        start_new_session=True,
    )
    # Windows specific: DETACHED_PROCESS flag to detach from console
    if os.name == 'nt':
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    subprocess.Popen([sys.executable, str(script_path)], **kwargs)

def main():
    clear_log()
    launch_script(GUI_PATH)
    time.sleep(1)
    launch_script(WATCHER_PATH)
    sys.exit(0)

if __name__ == "__main__":
    main()
