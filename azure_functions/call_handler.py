from twilio.rest import Client
import cognitive_services.transcriber as transcriber
import cognitive_services.nlp_processor as nlp
import time
import logging

# Twilio setup
account_sid = "YourAccountSID"
auth_token = "YourAuthToken"
client = Client(account_sid, auth_token)

logging.basicConfig(level=logging.INFO)

MAX_RETRIES = 3


def initiate_call(patient_data):
    retry_count = 0

    while retry_count < MAX_RETRIES:
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
