from twilio.rest import Client
import cognitive_services.transcriber as transcriber
import cognitive_services.nlp_processor as nlp
import time
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json

# Load config.json for Key Vault URL and other non-sensitive configs
with open("config.json", "r") as config_file:
    config = json.load(config_file)

key_vault_url = config["key_vault_url"]

# Initialize the Key Vault client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Fetch secrets
AZURE_SPEECH_KEY = secret_client.get_secret("AZURE_SPEECH_KEY").value
AZURE_REGION = secret_client.get_secret("AZURE_REGION").value
TWILIO_ACCOUNT_SID = secret_client.get_secret("TWILIO_ACCOUNT_SID").value
TWILIO_AUTH_TOKEN = secret_client.get_secret("TWILIO_AUTH_TOKEN").value

logging.basicConfig(level=logging.INFO)

def initiate_call(patient_data):
    retry_count = 0

    while retry_count < config.MAX_RETRIES:
        try:
            logging.info(f"Initiating call for patient {patient_data['id']}...")
            call = client.calls.create(
                url="http://your-azure-function-url.com/process_call",
                to=patient_data["insurance_phone"],
                from_="+YourTwilioNumber"
            )
            return {"patient_id": patient_data["id"], "call_status": "Initiated", "call_sid": call.sid}
        except Exception as e:
            retry_count += 1
            logging.error(f"Call initiation failed for patient {patient_data['id']}: {e}")
            time.sleep(5)

    return {"patient_id": patient_data["id"], "call_status": "Failed"}

def process_call(patient_data):
    try:
        response = nlp.interact_with_human_representative(patient_data)
        return {
            "patient_id": patient_data["id"],
            "call_status": "Completed",
            "details": response
        }
    except Exception as e:
        logging.error(f"Error during call processing for patient {patient_data['id']}: {e}")
        return {"patient_id": patient_data["id"], "call_status": "Error"}
