# Twilio API integration

from twilio.rest import Client

def send_call(patient_data):
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        url="http://your-server/callback",
        to=patient_data["insurance_phone"],
        from_="YourTwilioNumber"
    )
    return call
