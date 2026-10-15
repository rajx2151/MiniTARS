
import tkinter as tk
from tkinter import scrolledtext
import threading
import time


# ============================================================
# CONFIG
# ============================================================

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

BG_COLOR = "#05070a"
TEXT_COLOR = "#d8f3ff"
ACCENT_COLOR = "#43d9ff"
DIM_COLOR = "#31515c"


# ============================================================
# MINI TARS DISPLAY
# ============================================================

class MiniTARSDisplay:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "MiniTARS"
        )

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.root.configure(
            bg=BG_COLOR
        )

        self.root.resizable(
            False,
            False
        )


        # ====================================================
        # TITLE
        # ====================================================

        self.title = tk.Label(

            self.root,

            text="MINITARS",

            font=(
                "Arial",
                18,
                "bold"
            ),

            fg=ACCENT_COLOR,

            bg=BG_COLOR
        )

        self.title.pack(
            pady=(20, 5)
        )


        # ====================================================
        # STATUS
        # ====================================================

        self.status = tk.Label(

            self.root,

            text="IDLE",

            font=(
                "Arial",
                11
            ),

            fg=DIM_COLOR,

            bg=BG_COLOR
        )

        self.status.pack(
            pady=(0, 10)
        )


        # ====================================================
        # FACE
        # ====================================================

        self.canvas = tk.Canvas(

            self.root,

            width=700,

            height=280,

            bg=BG_COLOR,

            highlightthickness=0
        )

        self.canvas.pack()


        # ====================================================
        # CHAT
        # ====================================================

        self.chat = scrolledtext.ScrolledText(

            self.root,

            width=75,

            height=9,

            font=(
                "Consolas",
                11
            ),

            bg="#0b1015",

            fg=TEXT_COLOR,

            insertbackground=TEXT_COLOR,

            relief="flat",

            borderwidth=0,

            wrap=tk.WORD
        )

        self.chat.pack(
            padx=30,
            pady=10
        )

        self.chat.configure(
            state="disabled"
        )


        # ====================================================
        # INITIAL STATE
        # ====================================================

        self.current_state = "IDLE"

        self.draw_face()


    # ========================================================
    # CHAT
    # ========================================================

    def add_message(
        self,
        speaker,
        message
    ):

        def update():

            self.chat.configure(
                state="normal"
            )

            self.chat.insert(
                tk.END,
                f"{speaker}: {message}\n\n"
            )

            self.chat.see(
                tk.END
            )

            self.chat.configure(
                state="disabled"
            )


        self.root.after(
            0,
            update
        )


    # ========================================================
    # STATE
    # ========================================================

    def set_state(
        self,
        state
    ):

        self.current_state = state

        self.root.after(
            0,
            self._update_state
        )


    def _update_state(self):

        self.status.configure(

            text=self.current_state,

            fg=(
                ACCENT_COLOR
                if self.current_state != "SLEEPING"
                else DIM_COLOR
            )
        )

        self.draw_face()


    # ========================================================
    # FACE
    # ========================================================

    def draw_face(self):

        self.canvas.delete(
            "all"
        )


        # ----------------------------------------------------
        # CENTER
        # ----------------------------------------------------

        center_y = 120


        # ----------------------------------------------------
        # SLEEPING
        # ----------------------------------------------------

        if self.current_state == "SLEEPING":

            self.canvas.create_line(

                170,
                center_y,

                270,
                center_y,

                fill=DIM_COLOR,

                width=8
            )

            self.canvas.create_line(

                430,
                center_y,

                530,
                center_y,

                fill=DIM_COLOR,

                width=8
            )


            self.canvas.create_text(

                350,
                210,

                text="Sleeping...",

                fill=DIM_COLOR,

                font=(
                    "Arial",
                    18
                )
            )

            return


        # ----------------------------------------------------
        # WAKING
        # ----------------------------------------------------

        if self.current_state == "WAKING":

            self.canvas.create_oval(

                175,
                75,

                275,
                175,

                outline=ACCENT_COLOR,

                width=5
            )

            self.canvas.create_oval(

                425,
                75,

                525,
                175,

                outline=ACCENT_COLOR,

                width=5
            )


            self.canvas.create_text(

                350,
                210,

                text="Waking...",

                fill=ACCENT_COLOR,

                font=(
                    "Arial",
                    18
                )
            )

            return


        # ----------------------------------------------------
        # NORMAL EYES
        # ----------------------------------------------------

        eye_size = 70

        self.canvas.create_oval(

            190,
            center_y - eye_size // 2,

            190 + eye_size,

            center_y + eye_size // 2,

            fill=ACCENT_COLOR,

            outline=""
        )

        self.canvas.create_oval(

            440,
            center_y - eye_size // 2,

            440 + eye_size,

            center_y + eye_size // 2,

            fill=ACCENT_COLOR,

            outline=""
        )


        # ----------------------------------------------------
        # THINKING
        # ----------------------------------------------------

        if self.current_state == "THINKING":

            self.canvas.create_text(

                350,
                215,

                text="...",

                fill=ACCENT_COLOR,

                font=(
                    "Arial",
                    26,
                    "bold"
                )
            )

            return


        # ----------------------------------------------------
        # LISTENING
        # ----------------------------------------------------

        if self.current_state == "LISTENING":

            self.canvas.create_arc(

                300,
                185,

                400,
                250,

                start=200,

                extent=140,

                style=tk.ARC,

                outline=ACCENT_COLOR,

                width=5
            )

            return


        # ----------------------------------------------------
        # SPEAKING
        # ----------------------------------------------------

        if self.current_state == "SPEAKING":

            self.canvas.create_oval(

                315,
                190,

                385,
                245,

                fill=ACCENT_COLOR,

                outline=""
            )

            return


        # ----------------------------------------------------
        # IDLE
        # ----------------------------------------------------

        self.canvas.create_line(

            315,
            215,

            385,
            215,

            fill=ACCENT_COLOR,

            width=5
        )


    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        self.root.mainloop()


# ============================================================
# DEMO
# ============================================================

def demo():

    display = MiniTARSDisplay()


    def sequence():

        states = [

            "SLEEPING",
            "WAKING",
            "LISTENING",
            "THINKING",
            "SPEAKING",
            "IDLE"

        ]


        for state in states:

            display.set_state(
                state
            )

            time.sleep(2)


        display.add_message(

            "You",

            "Hello MiniTARS!"
        )


        time.sleep(1)


        display.add_message(

            "MiniTARS",

            "Hello! How can I help you?"
        )


        display.set_state(
            "IDLE"
        )


    threading.Thread(

        target=sequence,

        daemon=True

    ).start()


    display.run()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    demo()
