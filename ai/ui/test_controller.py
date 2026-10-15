import time
import sys
from pathlib import Path


# ============================================================
# MAKE AI DIRECTORY IMPORTABLE
# ============================================================

AI_ROOT = Path(__file__).resolve().parent.parent

if str(AI_ROOT) not in sys.path:
    sys.path.insert(0, str(AI_ROOT))


from ui.controller import (
    start_ui,
    set_state,
    show_user,
    show_tars,
)


# ============================================================
# START UI
# ============================================================

print("Starting MiniTARS UI...")

start_ui()


# ============================================================
# DEMO
# ============================================================

time.sleep(1)

print("SLEEPING")
set_state("SLEEPING")

time.sleep(2)

print("WAKING")
set_state("WAKING")

time.sleep(2)

print("LISTENING")
set_state("LISTENING")

show_user(
    "Hello MiniTARS"
)

time.sleep(2)

print("THINKING")
set_state("THINKING")

time.sleep(2)

show_tars(
    "Hello! Nice to hear from you."
)

print("SPEAKING")
set_state("SPEAKING")

time.sleep(3)

print("IDLE")
set_state("IDLE")


# ============================================================
# KEEP PROGRAM ALIVE
# ============================================================

while True:

    time.sleep(1)