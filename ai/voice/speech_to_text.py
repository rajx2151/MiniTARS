import speech_recognition as sr


# ============================================================
# SPEECH RECOGNIZER
# ============================================================

recognizer = sr.Recognizer()


# ============================================================
# MICROPHONE
# ============================================================

# Your laptop's working microphone.
#
# Device 1 was detected as:
# Digital Microphone (2- Cirrus Logic High Definition Audio)
#
# If Windows changes the device numbering later, change this.
#
MIC_INDEX = 1


# ============================================================
# LISTEN
# ============================================================

def listen(
    timeout=5,
    phrase_time_limit=15
):

    microphone = sr.Microphone(
        device_index=MIC_INDEX
    )

    try:

        with microphone as source:

            print("Listening...")

            # ------------------------------------------------
            # DO NOT recalibrate every single sentence.
            #
            # The microphone was already tested and works.
            # Recalibrating every time can make speech
            # recognition inconsistent.
            # ------------------------------------------------

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

    except sr.WaitTimeoutError:

        return None

    except Exception as e:

        print(
            "Microphone error:",
            e
        )

        return None


    # ========================================================
    # SPEECH RECOGNITION
    # ========================================================

    try:

        text = recognizer.recognize_google(
            audio
        )

        text = text.strip()


        if text:

            print(
                "You said:",
                text
            )

            return text


        return None


    except sr.UnknownValueError:

        print(
            "I couldn't understand that."
        )

        return None


    except sr.RequestError as e:

        print(
            "Speech recognition error:",
            e
        )

        return None


    except Exception as e:

        print(
            "Recognition error:",
            e
        )

        return None


# ============================================================
# WAKE WORD
# ============================================================

def is_wake_word(text):

    if not text:

        return False


    text = text.lower().strip()


    # ========================================================
    # WAKE PHRASES
    # ========================================================

    wake_words = [

        # Normal MiniTARS wake phrases
        "hey tars",
        "hey tar",
        "hi tars",
        "hello tars",
        "tars",

        # Common microphone misrecognitions
        "haters",
        "heater",

        # Direct wake commands
        "wake up",
        "wake up tars",
        "wake tars",
        "wake",

    ]


    # ========================================================
    # CHECK
    # ========================================================

    for word in wake_words:

        if word in text:

            return True


    return False