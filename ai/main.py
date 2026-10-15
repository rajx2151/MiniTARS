
import sys
import time
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

# Actual structure:
#
# MiniTARS/
# ├── agent/
# │   └── chat_agent.py
# │
# └── ai/
#     └── main.py
#
# main.py.parent        = ai
# main.py.parent.parent = MiniTARS

PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

AI_ROOT = PROJECT_ROOT / "ai"


# ============================================================
# PYTHON PATH
# ============================================================

# Allow:
#
# from agent.chat_agent import ...
#
# and:
#
# from voice...
# from intent...
# from ui...
# from tool_router...

for path in [

    PROJECT_ROOT,

    AI_ROOT,

]:

    path_string = str(path)

    if path_string not in sys.path:

        sys.path.insert(
            0,
            path_string
        )


# ============================================================
# IMPORTS
# ============================================================

from intent.intent_router import detect_intent

from tool_router import execute_tool

from voice.speech_to_text import (
    listen,
    is_wake_word,
)

from voice.text_to_speech import (
    speak,
    stop_speaking,
)

from agent.chat_agent import (
    ask_chatbot,
)

from ui.controller import (
    start_ui,
    set_state,
    show_user,
    show_tars,
)


# ============================================================
# SETTINGS
# ============================================================

# MiniTARS goes to sleep after this much inactivity.

SLEEP_TIMEOUT = 20


# Maximum time to wait for speech to start.

COMMAND_TIMEOUT = 5


# Maximum length of one spoken command.

COMMAND_TIME_LIMIT = 15


# Maximum wake-word listening phrase.

WAKE_TIME_LIMIT = 5


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(text):

    if not text:

        return ""

    return text.lower().strip()


# ============================================================
# EXIT
# ============================================================

def is_exit_command(text):

    text = clean_text(text)

    return text in [

        "exit",

        "quit",

        "shutdown",

        "goodbye",

        "bye",

    ]


# ============================================================
# SLEEP
# ============================================================

def is_sleep_command(text):

    text = clean_text(text)

    return text in [

        "stop listening",

        "go to sleep",

        "sleep",

    ]


# ============================================================
# SPEAK
# ============================================================

def say(text):

    if not text:

        return


    print(
        "MiniTARS:",
        text
    )


    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    try:

        show_tars(
            text
        )

    except Exception:

        pass


    try:

        set_state(
            "SPEAKING"
        )

    except Exception:

        pass


    # --------------------------------------------------------
    # TTS
    # --------------------------------------------------------

    try:

        # IMPORTANT:
        #
        # speak() must return only after speech finishes.
        #
        # This prevents the 20-second sleep timer from running
        # while MiniTARS is still talking.

        speak(
            text
        )

    except Exception as e:

        print(
            "TTS error:",
            e
        )


    try:

        set_state(
            "IDLE"
        )

    except Exception:

        pass


# ============================================================
# PROCESS COMMAND
# ============================================================

def process_command(
    user_input
):

    if not user_input:

        return True


    print()

    print(
        "You said:",
        user_input
    )


    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    try:

        show_user(
            user_input
        )

    except Exception:

        pass


    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if is_exit_command(
        user_input
    ):

        say(
            "Goodbye!"
        )

        return False


    # --------------------------------------------------------
    # SLEEP
    # --------------------------------------------------------

    if is_sleep_command(
        user_input
    ):

        say(
            "Okay. Going to sleep."
        )

        try:

            set_state(
                "SLEEPING"
            )

        except Exception:

            pass

        return True


    # --------------------------------------------------------
    # THINKING
    # --------------------------------------------------------

    try:

        set_state(
            "THINKING"
        )

    except Exception:

        pass


    # --------------------------------------------------------
    # INTENT
    # --------------------------------------------------------

    try:

        intent = detect_intent(
            user_input
        )

    except Exception as e:

        print(
            "Intent error:",
            e
        )

        intent = "GENERAL_CHAT"


    print(
        "Detected intent:",
        intent
    )


    # --------------------------------------------------------
    # GENERAL CHAT
    # --------------------------------------------------------

    if intent == "GENERAL_CHAT":

        print(
            "MiniTARS: Thinking..."
        )


        response = ask_chatbot(
            user_input
        )


        say(
            response
        )


        return True


    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if intent == "GREETING":

        say(
            "Hey! What's up?"
        )

        return True


    # --------------------------------------------------------
    # ROBOT / TOOLS
    # --------------------------------------------------------

    try:

        response = execute_tool(

            intent,

            user_input

        )

    except Exception as e:

        print(
            "Tool error:",
            e
        )

        response = None


    # --------------------------------------------------------
    # TOOL RESPONSE
    # --------------------------------------------------------

    if response:

        say(
            response
        )

    else:

        say(
            "I don't know how to handle "
            "that command yet."
        )


    return True


# ============================================================
# ACTIVE MODE
# ============================================================

def active_mode():

    print()

    print(
        "================================"
    )

    print(
        "         ACTIVE MODE"
    )

    print(
        "================================"
    )

    print(
        "MiniTARS is listening."
    )

    print(
        f"No command for "
        f"{SLEEP_TIMEOUT} seconds -> sleep."
    )

    print()


    # --------------------------------------------------------
    # INACTIVITY TIMER
    #
    # IMPORTANT:
    #
    # This timer starts AFTER MiniTARS finishes answering.
    #
    # TTS time does not count as silence.
    # Gemini thinking time does not count as silence.
    # --------------------------------------------------------

    last_activity = time.monotonic()


    while True:

        try:

            set_state(
                "LISTENING"
            )

        except Exception:

            pass


        print(
            f"Listening... "
            f"(sleep after {SLEEP_TIMEOUT}s)"
        )


        # ----------------------------------------------------
        # LISTEN
        # ----------------------------------------------------

        try:

            command = listen(

                timeout=COMMAND_TIMEOUT,

                phrase_time_limit=COMMAND_TIME_LIMIT

            )

        except Exception as e:

            print(
                "Microphone error:",
                e
            )

            time.sleep(
                0.2
            )

            continue


        # ----------------------------------------------------
        # NOTHING HEARD
        # ----------------------------------------------------

        if not command:

            elapsed = (
                time.monotonic()
                - last_activity
            )


            print(
                f"No speech. "
                f"Idle: {elapsed:.1f}s"
            )


            if elapsed >= SLEEP_TIMEOUT:

                print()

                print(
                    f"No command for "
                    f"{SLEEP_TIMEOUT} seconds."
                )

                print(
                    "Going to sleep..."
                )


                try:

                    set_state(
                        "SLEEPING"
                    )

                except Exception:

                    pass


                return True


            continue


        # ----------------------------------------------------
        # COMMAND RECEIVED
        # ----------------------------------------------------

        print(
            "Heard:",
            command
        )


        # ----------------------------------------------------
        # RESET ACTIVITY
        # ----------------------------------------------------

        last_activity = time.monotonic()


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if is_exit_command(
            command
        ):

            say(
                "Goodbye!"
            )

            return False


        # ----------------------------------------------------
        # SLEEP
        # ----------------------------------------------------

        if is_sleep_command(
            command
        ):

            say(
                "Okay. Going to sleep."
            )


            try:

                set_state(
                    "SLEEPING"
                )

            except Exception:

                pass


            return True


        # ----------------------------------------------------
        # PROCESS
        # ----------------------------------------------------

        result = process_command(
            command
        )


        if result is False:

            return False


        # ----------------------------------------------------
        # IMPORTANT
        #
        # Restart the inactivity timer AFTER the complete
        # command and response are finished.
        # ----------------------------------------------------

        last_activity = time.monotonic()


        try:

            set_state(
                "IDLE"
            )

        except Exception:

            pass


# ============================================================
# SLEEP MODE
# ============================================================

def sleep_mode():

    print()

    print(
        "================================"
    )

    print(
        "          SLEEP MODE"
    )

    print(
        "================================"
    )

    print(
        "Say 'Hey TARS' to wake MiniTARS."
    )

    print()


    try:

        set_state(
            "SLEEPING"
        )

    except Exception:

        pass


    while True:

        print(
            "Sleeping... listening for wake word."
        )


        # ----------------------------------------------------
        # LISTEN FOR WAKE WORD
        # ----------------------------------------------------

        try:

            wake_text = listen(

                timeout=None,

                phrase_time_limit=WAKE_TIME_LIMIT

            )

        except Exception as e:

            print(
                "Wake microphone error:",
                e
            )

            time.sleep(
                0.2
            )

            continue


        # ----------------------------------------------------
        # NOTHING HEARD
        # ----------------------------------------------------

        if not wake_text:

            continue


        print(
            "Heard:",
            wake_text
        )


        # ----------------------------------------------------
        # EXIT WHILE SLEEPING
        # ----------------------------------------------------

        if is_exit_command(
            wake_text
        ):

            say(
                "Goodbye!"
            )

            return False


        # ----------------------------------------------------
        # WAKE WORD
        # ----------------------------------------------------

        if is_wake_word(
            wake_text
        ):

            print()

            print(
                "Wake word detected!"
            )

            print(
                "MiniTARS activated."
            )


            try:

                set_state(
                    "WAKING"
                )

            except Exception:

                pass


            say(
                "Yes?"
            )


            try:

                set_state(
                    "IDLE"
                )

            except Exception:

                pass


            return True


        # ----------------------------------------------------
        # IGNORE OTHER SPEECH
        # ----------------------------------------------------

        print(
            "Ignoring speech while sleeping."
        )


# ============================================================
# VOICE MODE
# ============================================================

def voice_mode():

    print()

    print(
        "================================"
    )

    print(
        "          VOICE MODE"
    )

    print(
        "================================"
    )

    print(
        "MiniTARS starts ACTIVE."
    )

    print(
        f"After {SLEEP_TIMEOUT} seconds "
        "of silence, MiniTARS sleeps."
    )

    print(
        "Say 'Hey TARS' while sleeping "
        "to wake it."
    )

    print(
        "Say 'stop listening' to sleep."
    )

    print(
        "Say 'bye' or 'exit' to shut down."
    )

    print()


    # --------------------------------------------------------
    # START ACTIVE
    # --------------------------------------------------------

    result = active_mode()


    if result is False:

        return False


    # --------------------------------------------------------
    # SLEEP / WAKE LOOP
    # --------------------------------------------------------

    while True:

        result = sleep_mode()


        if result is False:

            return False


        result = active_mode()


        if result is False:

            return False


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "================================"
    )

    print(
        "       MiniTARS AI Engine"
    )

    print(
        "================================"
    )

    print(
        "System status: ONLINE"
    )

    print(
        "AI: Gemini"
    )

    print(
        "Voice: Enabled"
    )

    print(
        "Robot tools: Enabled"
    )

    print()


    # ========================================================
    # UI
    # ========================================================

    try:

        start_ui()

    except Exception as e:

        print(
            "UI startup warning:",
            e
        )


    try:

        set_state(
            "IDLE"
        )

    except Exception:

        pass


    # ========================================================
    # MAIN LOOP
    # ========================================================

    while True:

        print(
            "Press ENTER for voice mode."
        )

        print(
            "Type a command for text mode."
        )

        print(
            "Type 'exit' to stop."
        )

        print()


        try:

            user_input = input(
                "You: "
            )

        except KeyboardInterrupt:

            print()

            stop_speaking()

            break


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if is_exit_command(
            user_input
        ):

            say(
                "Goodbye!"
            )

            break


        # ----------------------------------------------------
        # VOICE MODE
        # ----------------------------------------------------

        if not user_input.strip():

            result = voice_mode()


            if result is False:

                break


            continue


        # ----------------------------------------------------
        # TEXT MODE
        # ----------------------------------------------------

        result = process_command(
            user_input
        )


        if result is False:

            break


        print()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()
