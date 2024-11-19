# NLP for IVR and human interactions

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential
import time
import logging

# Azure Cognitive Services setup
speech_key = "YourSpeechKey"
service_region = "YourRegion"
text_analytics_key = "YourTextAnalyticsKey"
text_analytics_endpoint = "YourTextAnalyticsEndpoint"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
text_client = TextAnalyticsClient(endpoint=text_analytics_endpoint, credential=DefaultAzureCredential())

logging.basicConfig(level=logging.INFO)

def interact_with_human_representative(patient_data):
    logging.info("Starting interaction with human representative...")
    
    transcript = []
    recognized_phrases = []
    context = {"state": "insurance_verification", "subtasks": []}

    try:
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        logging.info("Listening for human representative response...")
        
        while True:
            result = recognizer.recognize_once()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_text = result.text
                transcript.append(recognized_text)
                logging.info(f"Recognized speech: {recognized_text}")
                
                if "end call" in recognized_text.lower():
                    logging.info("Call marked for termination by representative.")
                    break
                
                processed_response = analyze_text(recognized_text)
                recognized_phrases.append(processed_response)
            elif result.reason == speechsdk.ResultReason.NoMatch:
                logging.warning("No speech recognized. Retrying...")
                time.sleep(2)
            elif result.reason == speechsdk.ResultReason.Canceled:
                logging.error("Speech recognition canceled.")
                break

    except Exception as e:
        logging.error(f"Error during interaction: {e}")
        return {"status": "Failed", "details": transcript}

    return {
        "status": "Completed",
        "transcript": transcript,
        "recognized_phrases": recognized_phrases
    }


def analyze_text(text):
    try:
        response = text_client.analyze_sentiment(documents=[{"id": "1", "language": "en", "text": text}])
        sentiment = response.documents[0].sentiment
        logging.info(f"Sentiment analysis result: {sentiment}")
        return {"text": text, "sentiment": sentiment}
    except Exception as e:
        logging.error(f"Text analysis failed: {e}")
        return {"text": text, "sentiment": "Unknown"}
