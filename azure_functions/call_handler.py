from twilio.rest import Client
import cognitive_services.transcriber as transcriber
import cognitive_services.nlp_processor as nlp
import time
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json
from typing import Dict, Any
import requests

logger = logging.getLogger(__name__)

class CallHandler:
    def __init__(self):
        # Load config
        with open("config.json", "r") as config_file:
            self.config = json.load(config_file)

        # Initialize Key Vault
        self.credential = DefaultAzureCredential()
        self.secret_client = SecretClient(
            vault_url=self.config["key_vault_url"],
            credential=self.credential
        )

        # Initialize Twilio client
        self.twilio_client = Client(
            self.get_secret("TWILIO_ACCOUNT_SID"),
            self.get_secret("TWILIO_AUTH_TOKEN")
        )

        # Initialize Transcriber
        self.transcriber = transcriber.Transcriber(
            speech_key=self.get_secret("AZURE_SPEECH_KEY"),
            region=self.get_secret("AZURE_REGION")
        )

    def get_secret(self, secret_name: str) -> str:
        return self.secret_client.get_secret(secret_name).value

    def initiate_call(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        retry_count = 0
        max_retries = self.config.get("retry_policy", {}).get("max_attempts", 3)

        while retry_count < max_retries:
            try:
                logger.info(f"Initiating call for patient {patient_data['id']}")
                call = self.twilio_client.calls.create(
                    url=self.config["azure_function_url"],
                    to=patient_data["insurance_phone"],
                    from_=self.config["twilio_number"],
                    record=True,  # Enable call recording
                    recording_status_callback=self.config["recording_callback_url"]
                )
                return {
                    "patient_id": patient_data["id"],
                    "call_status": "Initiated",
                    "call_sid": call.sid
                }
            except Exception as e:
                retry_count += 1
                logger.error(f"Call initiation failed (attempt {retry_count}): {str(e)}")
                time.sleep(self.config.get("retry_policy", {}).get("delay_seconds", 5))

        return {
            "patient_id": patient_data["id"],
            "call_status": "Failed",
            "error": "Max retry attempts reached"
        }

    def process_recording(self, recording_sid: str, call_sid: str) -> Dict[str, Any]:
        """
        Process a completed call recording
        """
        try:
            # Get recording details from Twilio
            recording = self.twilio_client.recordings(recording_sid).fetch()
            recording_url = recording.media_url

            # Download recording
            response = requests.get(recording_url)
            if response.status_code != 200:
                raise Exception(f"Failed to download recording: {response.status_code}")

            # Transcribe the recording
            transcript = self.transcriber.transcribe_recording(recording_url)
            if not transcript:
                raise Exception("Transcription failed")

            # Process transcript with NLP
            nlp_response = self.nlp_processor.analyze_text(transcript)

            return {
                "call_sid": call_sid,
                "recording_sid": recording_sid,
                "transcript": transcript,
                "nlp_analysis": nlp_response,
                "status": "Completed"
            }

        except Exception as e:
            logger.error(f"Recording processing failed: {str(e)}")
            return {
                "call_sid": call_sid,
                "recording_sid": recording_sid,
                "status": "Failed",
                "error": str(e)
            }

    def handle_recording_callback(self, recording_data: Dict[str, Any]) -> None:
        """
        Handle recording status callback from Twilio
        """
        try:
            if recording_data["status"] == "completed":
                result = self.process_recording(
                    recording_data["recording_sid"],
                    recording_data["call_sid"]
                )
                # Update call record in database or storage
                self.update_call_record(result)
        except Exception as e:
            logger.error(f"Recording callback handling failed: {str(e)}")

    def update_call_record(self, result: Dict[str, Any]) -> None:
        """
        Update call record with processing results
        """
        try:
            # Implement your storage update logic here
            pass
        except Exception as e:
            logger.error(f"Failed to update call record: {str(e)}")
