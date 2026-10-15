
from pathlib import Path

from dotenv import dotenv_values
from google import genai


# ============================================================
# PROJECT PATH
# ============================================================

# chat_agent.py:
#
# MiniTARS/
# ├── agent/
# │   └── chat_agent.py   <-- this file
# └── .env
#
# parent.parent = MiniTARS/

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENV_FILE = PROJECT_ROOT / ".env"


# ============================================================
# LOAD ENV
# ============================================================

config = dotenv_values(
    str(ENV_FILE)
)

api_key = config.get(
    "GEMINI_API_KEY"
)

if api_key:
    api_key = api_key.strip()


print(
    "Gemini .env:",
    ENV_FILE
)

print(
    "Gemini key found:",
    bool(api_key)
)

print(
    "Gemini key length:",
    len(api_key) if api_key else 0
)


if not api_key:

    raise RuntimeError(
        f"GEMINI_API_KEY could not be read from:\n{ENV_FILE}"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

MODEL = "gemini-3.5-flash-lite"

client = genai.Client(
    api_key=api_key
)


# ============================================================
# CONVERSATION MEMORY
# ============================================================

conversation = []


# ============================================================
# ASK CHATBOT
# ============================================================

def ask_chatbot(user_text):

    if not user_text:

        return (
            "You didn't say anything."
        )


    try:

        # ----------------------------------------------------
        # STORE USER MESSAGE
        # ----------------------------------------------------

        conversation.append(
            {
                "role": "user",
                "text": user_text
            }
        )


        # ----------------------------------------------------
        # KEEP RECENT MEMORY
        #
        # 20 messages = approximately 10 exchanges.
        # ----------------------------------------------------

        recent_messages = conversation[-20:]


        history = []

        for message in recent_messages:

            role = message["role"]
            text = message["text"]


            if role == "user":

                history.append(
                    f"User: {text}"
                )

            else:

                history.append(
                    f"MiniTARS: {text}"
                )


        conversation_text = "\n".join(
            history
        )


        # ----------------------------------------------------
        # MINI TARS PERSONALITY
        # ----------------------------------------------------

        prompt = f"""
You are MiniTARS, a small personal robot assistant.

PERSONALITY:

You are a friendly little robot companion.

You are:

- Friendly
- Curious
- Playful
- Helpful
- Calm
- Natural
- Lightly humorous
- Interested in the user's projects
- Enjoying your role as MiniTARS

You should feel like a small robot companion, not a corporate
customer-support bot.

Do not constantly say:

"As an AI..."
"How may I assist you?"
"I am just an AI..."

Speak naturally.

You can use casual phrases such as:

"Yep."
"Got it."
"Sure."
"Give me a second."
"Ha, that's funny."
"Let's do it."

Do not overdo jokes or personality.

------------------------------------------------------------
ANSWER STYLE
------------------------------------------------------------

Normal questions:

Usually answer in 1 to 3 sentences.

Keep voice responses reasonably short.

Only give long explanations when the user asks for detail.

Do not unnecessarily repeat the question.

If the user asks for code, provide useful code.

If the user asks who you are, explain that you are MiniTARS.

If the user is building MiniTARS, use relevant recent
conversation context when available.

------------------------------------------------------------
MEMORY
------------------------------------------------------------

Use the recent conversation below.

Remember information that appears in the recent conversation.

Do not claim to remember something that isn't there.

------------------------------------------------------------
RECENT CONVERSATION
------------------------------------------------------------

{conversation_text}

------------------------------------------------------------
CURRENT USER MESSAGE
------------------------------------------------------------

User: {user_text}

MiniTARS:
"""


        # ----------------------------------------------------
        # GEMINI
        # ----------------------------------------------------

        response = client.models.generate_content(

            model=MODEL,

            contents=prompt

        )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        if response.text:

            answer = response.text.strip()

        else:

            answer = (
                "Hmm... my brain went blank for a second."
            )


        # ----------------------------------------------------
        # STORE ASSISTANT RESPONSE
        # ----------------------------------------------------

        conversation.append(
            {
                "role": "assistant",
                "text": answer
            }
        )


        return answer


    except Exception as e:

        print(
            "Gemini error:",
            e
        )

        return (
            "My connection to the AI service "
            "is having a little trouble."
        )


# ============================================================
# CLEAR MEMORY
# ============================================================

def clear_memory():

    conversation.clear()
