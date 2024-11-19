# Speech-to-text

import azure.cognitiveservices.speech as speechsdk
import logging

speech_key = "YourSpeechKey"
region = "YourRegion"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)

logging.basicConfig(level=logging.INFO)

def transcribe(audio):
    try:
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        result = recognizer.recognize_once()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            logging.info(f"Transcription: {result.text}")
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            logging.warning("Speech not recognized.")
            return ""
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            logging.error(f"Speech recognition canceled: {cancellation_details.reason}")
            return ""
    except Exception as e:
        logging.error(f"Error in transcription: {e}")
        return ""
