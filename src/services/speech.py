import io
import logging

from speechkit import model_repository

logger = logging.getLogger(__name__)


class SpeechService:
    """
    Service wrapper for speech
    """
    def __init__(self):
        self.syn_model = model_repository.synthesis_model()

    def synthesize(self, text: str, voice: str = 'anton') -> io.BytesIO | None:
        try:
            self.syn_model.voice = voice
            result = self.syn_model.synthesize(text, raw_format=False)

            audio_buffer = io.BytesIO()
            result.export(audio_buffer, format="ogg", codec="libopus")
            audio_buffer.seek(0)
            return audio_buffer
        except Exception as e:
            logger.error(f"Speech synthesis error: {e}")
            return None