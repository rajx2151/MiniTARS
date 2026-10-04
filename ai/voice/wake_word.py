
import numpy as np
import sounddevice as sd
from openwakeword.model import Model


WAKE_WORD = "hey_jarvis"

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

THRESHOLD = 0.8


print("================================")
print(" MiniTARS Wake Word Test")
print("================================")
print()
print("Loading model...")

model = Model(
    wakeword_models=[WAKE_WORD],
    inference_framework="onnx"
)

print("Model loaded.")
print()
print("Say: Hey Jarvis")
print("Press CTRL+C to stop.")
print()


try:

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=CHUNK_SIZE,
        dtype="int16",
        channels=1
    ) as stream:

        print("Microphone started.")
        print("Listening...")
        print()

        counter = 0

        while True:

            audio, overflowed = stream.read(CHUNK_SIZE)

            if overflowed:
                print("WARNING: Audio overflow")

            audio_data = np.frombuffer(
                audio,
                dtype=np.int16
            )

            prediction = model.predict(audio_data)

            score = prediction.get(
                WAKE_WORD,
                0.0
            )

            counter += 1

            # Print every 10 audio chunks
            if counter % 10 == 0:

                print(
                    f"Wake score: {score:.3f}"
                )

            if score >= THRESHOLD:

                print()
                print("==============================")
                print("WAKE WORD DETECTED!")
                print("==============================")
                print()

except KeyboardInterrupt:

    print()
    print("Test stopped.")
