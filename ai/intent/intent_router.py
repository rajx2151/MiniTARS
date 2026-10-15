
# ============================================================
# MINITARS INTENT ROUTER
# ============================================================
#
# Philosophy:
#
# Conversation -> GENERAL_CHAT
# Robot/tool commands -> specific intent
# Exit -> EXIT
#
# Greetings are NOT a separate intent.
# Gemini handles greetings and casual conversation.
# ============================================================


# ============================================================
# EXIT
# ============================================================

EXIT_WORDS = {
    "exit",
    "quit",
    "shutdown",
    "shut down",
    "goodbye",
}


# ============================================================
# ROBOT / TOOL KEYWORDS
# ============================================================
#
# Keep this list focused on things MiniTARS can actually DO.
#
# Do NOT put "hello", "hi", "how are you", etc. here.
# Those belong to GENERAL_CHAT.
# ============================================================


def detect_intent(user_text):

    if not user_text:

        return "GENERAL_CHAT"


    text = user_text.lower().strip()


    # ========================================================
    # EXIT
    # ========================================================

    if text in EXIT_WORDS:

        return "EXIT"


    # ========================================================
    # ROBOT / TOOL COMMANDS
    # ========================================================
    #
    # IMPORTANT:
    # These are examples.
    # Keep/change them according to your actual tool_router.py.
    # ========================================================


    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "what time is it",
            "current time",
            "tell me the time",
            "time now",
        ]
    ):

        return "TIME"


    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "weather",
            "temperature outside",
            "is it raining",
            "will it rain",
        ]
    ):

        return "WEATHER"


    # --------------------------------------------------------
    # MUSIC
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "play music",
            "play a song",
            "play song",
            "start music",
        ]
    ):

        return "MUSIC"


    # --------------------------------------------------------
    # STOP SPEAKING
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "stop talking",
            "stop speaking",
            "be quiet",
            "shut up",
            "cancel speech",
        ]
    ):

        return "STOP_SPEAKING"


    # ========================================================
    # EVERYTHING ELSE
    # ========================================================
    #
    # This includes:
    #
    # hello
    # hi
    # hey
    # how are you
    # who are you
    # tell me a joke
    # that's funny
    # continue
    # what did you say
    # explain that
    # etc.
    #
    # Gemini handles these.
    # ========================================================

    return "GENERAL_CHAT"
