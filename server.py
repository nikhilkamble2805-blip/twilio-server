from flask import Flask, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
from flask import request

load_dotenv()

app = Flask(__name__)

# Environment variables
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
BASE_URL = os.environ.get("BASE_URL")

if not account_sid or not auth_token:
    raise ValueError("Twilio credentials not set")

client = Client(account_sid, auth_token)

@app.route("/")
def home():
    return "Server is running"

@app.route("/voice", methods=["GET", "POST"])
def voice():
    resp = VoiceResponse()
    resp.say("Emergency detected in vehicle. Please check immediately.")
    return Response(str(resp), mimetype="text/xml")

@app.route("/alert")
def alert():
    call = client.calls.create(
        url=f"{BASE_URL}/voice",
        to="+919356851405",
        from_="+15626693526"
    )
    return "Call Triggered"
@app.route("/sms", methods=["POST"])
def sms_reply():
    raw = request.data.decode("utf-8")
    form_msg = request.form.get("msg")

    print("RAW DATA:", raw)
    print("FORM MSG:", form_msg)

    msg = form_msg if form_msg else raw

    if msg:
        msg = msg.strip().upper()

    print("FINAL MSG:", msg)

    if "ALERT" in msg:
        print("CALL TRIGGERED")

        client.calls.create(
            url=f"{BASE_URL}/voice",
            to="+919356851405",
            from_="+15626693526"
        )

        return "Call Triggered"

    return "No action"