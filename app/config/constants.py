# Parameters
SAMPLE_RATE = 16000  # Audio sample rate
DURATION = 1         # Length of each audio chunk in seconds
MODEL_PATH = "app/artifacts/onnx/al_vee.onnx"  # Path to ONNX model
WAKE_WORD = "al vee"
CONFIDENCE_THRESHOLD = 0.5  # Model confidence threshold
COOLDOWN_TIME = 1.5  # Minimum time between consecutive detections in seconds
