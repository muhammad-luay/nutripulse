# call_me.py
import os
from twilio.rest import Client
import dotenv

dotenv.load_dotenv()

# Set these (env vars are recommended)
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
TO_NUMBER   = os.getenv("MY_VERIFIED_NUMBER")

MESSAGE = "Habari za leo! Nafurahi sana kuwa hapa na kuzungumza na wewe. Naona hali ya hewa leo ni nzuri."

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Inline TwiML tells Twilio what to say once the call is answered
twiml = f'<Response><Say language="sw-KE">{MESSAGE}</Say></Response>'

call = client.calls.create(
    to=TO_NUMBER,
    from_=FROM_NUMBER,
    twiml=twiml  # no public URL needed; Twilio uses this TwiML directly
)

print("Call SID:", call.sid)
