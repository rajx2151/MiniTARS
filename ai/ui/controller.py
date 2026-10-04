
import threading

from .display import MiniTARSDisplay


# ============================================================
# GLOBAL UI
# ============================================================

_display = None
_ui_thread = None
_start_lock = threading.Lock()


# ============================================================
# START UI
# ============================================================

def start_ui():

    global _display
    global _ui_thread

    with _start_lock:

        if _display is not None:
            return

        def ui_worker():

            global _display

            try:

                _display = MiniTARSDisplay()

                _display.run()

            except Exception as e:

                print(
                    "UI error:",
                    e
                )


        _ui_thread = threading.Thread(

            target=ui_worker,

            daemon=True
        )

        _ui_thread.start()


# ============================================================
# SET STATE
# ============================================================

def set_state(state):

    if _display is None:
        return

    try:

        _display.set_state(
            state
        )

    except Exception as e:

        print(
            "UI state error:",
            e
        )


# ============================================================
# SHOW USER
# ============================================================

def show_user(text):

    if not text:
        return

    if _display is None:
        return

    try:

        _display.add_message(
            "You",
            text
        )

    except Exception as e:

        print(
            "UI user message error:",
            e
        )


# ============================================================
# SHOW TARS
# ============================================================

def show_tars(text):

    if not text:
        return

    if _display is None:
        return

    try:

        _display.add_message(
            "MiniTARS",
            text
        )

    except Exception as e:

        print(
            "UI TARS message error:",
            e
        )
