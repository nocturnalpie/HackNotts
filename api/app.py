from flask import Flask
from flask import request
from twilio.rest import Client

app = Flask(__name__)

with open("../../API_KEYS/twilio_account_sid.key") as f:
  account_sid = f.read()

with open("../../API_KEYS/twilio_auth_token.key") as f:
  auth_token = f.read()

with open("../../API_KEYS/api_secret.key") as f:
  api_token = f.read().strip()

client = Client(account_sid, auth_token)

@app.route('/clue')
def hello_world():
  if request.headers.get('auth', False) and request.headers.get('number', False):
    print("Here!")
    print(api_token)
    if request.headers.get('auth', False) == api_token:
      message = client.messages \
        .create(
        body="This is a clue!",
        from_='+441754772060',
        to='+447500300880'
      )
      return 'Message Sent!'
  return "Error"


if __name__ == '__main__':
    app.run()
