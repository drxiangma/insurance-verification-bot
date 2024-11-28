import azure.cognitiveservices.speech as speechsdk
import logging
from typing import Optional
from pydub import AudioSegment
import io
import wave

logger = logging.getLogger(__name__)

class Transcriber:
    def __init__(self, speech_key: str, region: str):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=region
        )
        # Set the audio configuration for high-quality call recordings
        self.audio_config = speechsdk.audio.AudioConfig(
            sample_rate=16000,
            channels=1
        )

    def transcribe_recording(self, recording_url: str) -> Optional[str]:
        """
        Transcribe a call recording from URL
        """
        try:
            # Configure audio input from URL
            audio_config = speechsdk.audio.AudioConfig(
                filename=recording_url
            )
            
            # Create speech recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )

            # Initialize variables for continuous recognition
            all_results = []
            done = False

            def handle_result(evt):
                if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    all_results.append(evt.result.text)

            def stop_cb(evt):
                nonlocal done
                done = True

            # Connect callbacks
            speech_recognizer.recognized.connect(handle_result)
            speech_recognizer.session_stopped.connect(stop_cb)
            speech_recognizer.canceled.connect(stop_cb)

            # Start continuous recognition
            speech_recognizer.start_continuous_recognition()
            while not done:
                pass
            speech_recognizer.stop_continuous_recognition()

            # Combine all results
            transcript = ' '.join(all_results)
            logger.info(f"Transcription completed: {len(all_results)} segments")
            return transcript

        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return None

    def transcribe_audio_stream(self, audio_stream: bytes) -> Optional[str]:
        """
        Transcribe audio from a byte stream
        """
        try:
            # Create audio stream configuration
            push_stream = speechsdk.audio.PushAudioInputStream()
            push_stream.write(audio_stream)
            push_stream.close()
            
            audio_config = speechsdk.audio.AudioConfig(
                stream=push_stream
            )
            
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                logger.info(f"Transcribed: {result.text}")
                return result.text
            else:
                logger.warning(f"No speech recognized: {result.reason}")
                return None
                
        except Exception as e:
            logger.error(f"Stream transcription error: {str(e)}")
            return None
