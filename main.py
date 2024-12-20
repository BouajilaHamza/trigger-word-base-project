import time
import threading
import sounddevice as sd
from app.config.constants import SAMPLE_RATE, DURATION, WAKE_WORD
from app.utils.audio_utils import audio_callback
from app.utils.threading_utils import process_audio_thread



def main():

    # Start audio processing thread
    thread = threading.Thread(target=process_audio_thread, daemon=True)
    thread.start()

    # Start listening for audio input
    print(f"Listening for the wake word '{WAKE_WORD}'...")
    with sd.InputStream(callback=audio_callback, samplerate=SAMPLE_RATE, channels=1, blocksize=int(SAMPLE_RATE * DURATION)):
        while True:
            time.sleep(0.1)  # Prevent high CPU usage

if __name__ == "__main__":
    main()