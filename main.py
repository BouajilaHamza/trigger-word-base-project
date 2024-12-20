import time
import threading
import queue
import numpy as np
import sounddevice as sd
import onnxruntime as ort
import pyttsx3

# Parameters
SAMPLE_RATE = 16000  # Audio sample rate
DURATION = 1         # Length of each audio chunk in seconds
MODEL_PATH = "C:/Users/USER/Downloads/al_vee.onnx"  # Path to ONNX model
WAKE_WORD = "al vee"
CONFIDENCE_THRESHOLD = 0.5  # Model confidence threshold
COOLDOWN_TIME = 1.5  # Minimum time between consecutive detections in seconds

# Audio buffer
audio_queue = queue.Queue()

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.9)

# Load ONNX model
ort_session = ort.InferenceSession(MODEL_PATH)
input_name = ort_session.get_inputs()[0].name

# Cooldown management
last_trigger_time = 0


def audio_callback(indata, frames, time, status):
    """Callback to capture audio chunks."""
    if status:
        print(f"Audio status: {status}")
    audio_queue.put(indata.copy())


def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()


def process_audio(audio_chunk):
    """Process the audio chunk and check for the wake word."""
    global last_trigger_time

    # Flatten and normalize the audio chunk
    audio_chunk = audio_chunk.flatten()
    audio_chunk = audio_chunk / np.max(np.abs(audio_chunk))

    # Reshape to model's required input shape (1, 16, 96)
    time_steps = 16
    features = 96
    audio_chunk = np.resize(audio_chunk, (time_steps, features))
    audio_chunk = np.expand_dims(audio_chunk, axis=0)

    # Predict with ONNX model
    predictions = ort_session.run(None, {input_name: audio_chunk.astype(np.float32)})
    confidence = predictions[0][0]

    # Check if confidence exceeds the threshold
    if confidence > CONFIDENCE_THRESHOLD:
        current_time = time.time()
        if current_time - last_trigger_time > COOLDOWN_TIME:
            last_trigger_time = current_time
            print("Wake word detected!")
            speak("Greetings")


def process_audio_thread():
    """Thread to process audio continuously."""
    while True:
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            process_audio(audio_data)


# Start audio processing thread
thread = threading.Thread(target=process_audio_thread, daemon=True)
thread.start()

# Start listening for audio input
print(f"Listening for the wake word '{WAKE_WORD}'...")
with sd.InputStream(callback=audio_callback, samplerate=SAMPLE_RATE, channels=1, blocksize=int(SAMPLE_RATE * DURATION)):
    while True:
        time.sleep(0.1)  # Prevent high CPU usage
