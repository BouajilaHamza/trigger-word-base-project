import queue
import onnxruntime as ort
import pyttsx3
from app.config.constants import MODEL_PATH


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

