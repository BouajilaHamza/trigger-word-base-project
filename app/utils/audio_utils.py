
import time
import numpy as np


from app.config.settings import audio_queue, engine, ort_session, input_name, last_trigger_time
from app.config.constants import CONFIDENCE_THRESHOLD, COOLDOWN_TIME






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
