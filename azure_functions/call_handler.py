from twilio.rest import Client
import cognitive_services.transcriber as transcriber
import cognitive_services.nlp_processor as nlp
import time
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json
from typing import Dict, Any

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
                    from_=self.config["twilio_number"]
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

    def process_call(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = nlp.interact_with_human_representative(patient_data)
            return {
                "patient_id": patient_data["id"],
                "call_status": "Completed",
                "details": response
            }
        except Exception as e:
            logger.error(f"Call processing failed: {str(e)}")
            return {
                "patient_id": patient_data["id"],
                "call_status": "Error",
                "error": str(e)
            }
