import queue
import onnxruntime as ort
import pyttsx3
from app.config.constants import MODEL_PATH
from app.utils.audio_utils import process_audio


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




def process_audio_thread():
    """Thread to process audio continuously."""
    while True:
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            process_audio(audio_data)
