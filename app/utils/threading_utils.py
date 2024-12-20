
from app.utils.audio_utils import process_audio
from app.config.settings import audio_queue




def process_audio_thread():
    """Thread to process audio continuously."""
    while True:
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            process_audio(audio_data)
