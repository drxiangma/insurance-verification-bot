import azure.cognitiveservices.speech as speechsdk
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Transcriber:
    def __init__(self, speech_key: str, region: str):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=region
        )

    def transcribe(self, audio_input: Any) -> Optional[str]:
        try:
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config
            )
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                logger.info(f"Transcribed: {result.text}")
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                logger.warning("No speech recognized")
                return None
            elif result.reason == speechsdk.ResultReason.Canceled:
                logger.error(f"Transcription canceled: {result.cancellation_details.reason}")
                return None
                
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return None
