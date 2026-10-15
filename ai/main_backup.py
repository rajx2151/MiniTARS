from intent.intent_router import detect_intent
from tool_router import execute_tool
from voice.speech_to_text import listen
from voice.text_to_speech import speak


def process_command(user_input):
    """Process both typed and spoken commands."""

    if not user_input:
        return

    print("You said:", user_input)

    intent = detect_intent(user_input)

    print("Detected intent:", intent)

    if intent == "EXIT":
        speak("Goodbye!")
        return False

    elif intent == "GREETING":
        speak("Hello! How can I help you?")

    else:
        response = execute_tool(intent, user_input)

        if response:
            speak(response)
        else:
            speak("I don't know how to handle that command yet.")

    print()
    return True


def main():
    print("================================")
    print("       MiniTARS AI Engine")
    print("================================")
    print("System status: ONLINE")
    print()
    print("Press ENTER for voice mode.")
    print("Type a command for text mode.")
    print("Type 'exit' to stop.")
    print()

    while True:

        user_input = input("You: ")

        # EXIT
        if user_input.lower().strip() == "exit":
            speak("Goodbye!")
            break

        # ENTER was pressed → voice mode
        if user_input.strip() == "":
            spoken_text = listen()

            if spoken_text is None:
                speak("I couldn't understand that.")
                continue

            if not process_command(spoken_text):
                break

        # Something was typed → text mode
        else:
            if not process_command(user_input):
                break


if __name__ == "__main__":
    main()