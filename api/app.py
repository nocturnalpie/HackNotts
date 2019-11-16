from flask import Flask
from flask import request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

with open("twilio_account_sid.key") as f:
  account_sid = f.read()

with open("twilio_auth_token.key") as f:
  auth_token = f.read()

with open("api_secret.key") as f:
  api_token = f.read().strip()

client = Client(account_sid, auth_token)


@app.route('/clue')
def get_clue():
  if request.headers.get('auth', False) and request.headers.get('number', False):

    if request.headers.get('auth', False) == api_token:
      message = client.messages \
        .create(
        body="This is a clue!",
        from_='+441754772060',
        to='+447500300880'
      )
      return 'Message Sent!'
  return "Error"


@app.route('/guess', methods=['GET', 'POST'])
def receive_answer():
  if request.args.get('api', False) == api_token:
    resp = MessagingResponse()

    # Add a message
    resp.message("Ahoy! Thanks so much for your message.")

    return str(resp)
  return "Error"


if __name__ == '__main__':
  # This is used when running locally only. When deploying to Google App
  # Engine, a webserver process such as Gunicorn will serve the app. This
  # can be configured by adding an `entrypoint` to app.yaml.
  app.run(host='127.0.0.1', port=8080, debug=True)
