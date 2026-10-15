
import threading
import pyttsx3


# ============================================================
# GLOBAL STATE
# ============================================================

_speaking = False
_stop_requested = False

_state_lock = threading.Lock()


# ============================================================
# SPEAK
# ============================================================

def speak(text, interrupt=True, wait=True):

    global _speaking
    global _stop_requested

    if not text:
        return

    print("MiniTARS:", text)

    # --------------------------------------------------------
    # If something is already speaking, request stop.
    # --------------------------------------------------------

    if interrupt:
        stop_speaking()

    with _state_lock:

        _stop_requested = False
        _speaking = True

    engine = None

    try:

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # Create a NEW engine for every response.
        #
        # This avoids Windows SAPI / pyttsx3 getting stuck
        # after the first runAndWait().
        # ----------------------------------------------------

        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            165
        )

        engine.setProperty(
            "volume",
            1.0
        )

        # ----------------------------------------------------
        # Queue text
        # ----------------------------------------------------

        engine.say(text)

        # ----------------------------------------------------
        # Speak completely before returning.
        # ----------------------------------------------------

        engine.runAndWait()

    except Exception as e:

        print(
            "TTS error:",
            e
        )

    finally:

        # ----------------------------------------------------
        # Always stop and destroy this engine.
        # ----------------------------------------------------

        if engine is not None:

            try:
                engine.stop()

            except Exception:
                pass

            # ------------------------------------------------
            # Clear pyttsx3 engine resources.
            # ------------------------------------------------

            try:
                del engine

            except Exception:
                pass

        with _state_lock:

            _speaking = False
            _stop_requested = False


# ============================================================
# STOP SPEAKING
# ============================================================

def stop_speaking():

    global _stop_requested
    global _speaking

    with _state_lock:

        _stop_requested = True

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # At this stage TTS is synchronous, so there is no
        # background engine that can safely be stopped from
        # another thread.
        #
        # This function mainly resets the state.
        # ----------------------------------------------------

        _speaking = False


# ============================================================
# CHECK SPEAKING
# ============================================================

def is_speaking():

    with _state_lock:

        return _speaking


# ============================================================
# SHUTDOWN
# ============================================================

def shutdown_tts():

    global _speaking
    global _stop_requested

    with _state_lock:

        _stop_requested = True
        _speaking = False
