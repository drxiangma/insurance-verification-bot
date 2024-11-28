# NLP for IVR and human interactions

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential
import time
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class NLPProcessor:
    def __init__(self, config: Dict[str, str]):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=config["speech_key"],
            region=config["service_region"]
        )
        self.text_client = TextAnalyticsClient(
            endpoint=config["text_analytics_endpoint"],
            credential=DefaultAzureCredential()
        )

    def interact_with_human_representative(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting interaction with human representative")
        transcript: List[str] = []
        recognized_phrases: List[Dict[str, Any]] = []

        try:
            recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
            
            while True:
                result = recognizer.recognize_once()
                if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    recognized_text = result.text
                    transcript.append(recognized_text)
                    logger.info(f"Recognized: {recognized_text}")
                    
                    if "end call" in recognized_text.lower():
                        logger.info("Call termination requested")
                        break
                    
                    processed_response = self.analyze_text(recognized_text)
                    recognized_phrases.append(processed_response)
                elif result.reason == speechsdk.ResultReason.NoMatch:
                    logger.warning("No speech recognized")
                    time.sleep(2)
                elif result.reason == speechsdk.ResultReason.Canceled:
                    logger.error("Speech recognition canceled")
                    break

        except Exception as e:
            logger.error(f"Interaction error: {str(e)}")
            return {"status": "Failed", "error": str(e)}

        return {
            "status": "Completed",
            "transcript": transcript,
            "recognized_phrases": recognized_phrases
        }

    def analyze_text(self, text: str) -> Dict[str, Any]:
        try:
            response = self.text_client.analyze_sentiment(
                documents=[{"id": "1", "language": "en", "text": text}]
            )
            sentiment = response.documents[0].sentiment
            return {"text": text, "sentiment": sentiment}
        except Exception as e:
            logger.error(f"Text analysis failed: {str(e)}")
            return {"text": text, "sentiment": "Unknown", "error": str(e)}
