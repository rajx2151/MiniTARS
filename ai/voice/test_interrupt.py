
import time
import threading

import speech_recognition as sr

from text_to_speech import speak, stop_speaking


# ============================================================
# SETTINGS
# ============================================================

STOP_WORDS = [
    "stop",
    "stop talking",
    "stop speaking",
    "be quiet",
    "cancel",
]

ENERGY_THRESHOLD = 600


# ============================================================
# RECOGNIZER
# ============================================================

recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.3
recognizer.non_speaking_duration = 0.2


# ============================================================
# STOP LISTENER
# ============================================================

def monitor_for_stop():

    print("Stop listener started.")

    with sr.Microphone() as source:

        # Calibrate only once.
        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        while True:

            try:

                print("Listening for STOP...")

                audio = recognizer.listen(
                    source,
                    timeout=2,
                    phrase_time_limit=2
                )

            except sr.WaitTimeoutError:

                continue

            try:

                text = recognizer.recognize_google(
                    audio
                )

                text = text.lower().strip()

                print("Heard:", text)

                for word in STOP_WORDS:

                    if word in text:

                        print()
                        print("==============================")
                        print("STOP COMMAND DETECTED!")
                        print("==============================")
                        print()

                        stop_speaking()

                        return

            except sr.UnknownValueError:

                pass

            except sr.RequestError as e:

                print(
                    "Speech recognition error:",
                    e
                )


# ============================================================
# MAIN TEST
# ============================================================

print("================================")
print(" MiniTARS Interrupt Test")
print("================================")
print()

print("Starting TTS...")

speak(
    "This is a long MiniTARS response. "
    "You can interrupt me by saying stop. "
    "The speech should continue smoothly "
    "until you give the stop command."
)

print()
print("MiniTARS is speaking.")
print("Say STOP whenever you want.")
print()


# Run listener separately so the main program
# remains responsive.
listener_thread = threading.Thread(
    target=monitor_for_stop,
    daemon=True
)

listener_thread.start()


# Keep program alive while TTS is running.
try:

    while listener_thread.is_alive():

        time.sleep(0.1)

except KeyboardInterrupt:

    print()
    print("Test cancelled.")

    stop_speaking()


print()
print("Interrupt test finished.")
