from flask import Flask
from flask import request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import uuid
import random

app = Flask(__name__)

with open("twilio_account_sid.key") as f:
  account_sid = f.read()

with open("twilio_auth_token.key") as f:
  auth_token = f.read()

with open("api_secret.key") as f:
  api_token = f.read().strip()

client = Client(account_sid, auth_token)


users = {}


@app.route('/begin', methods=['POST'])
def start_game():
  if request.headers.get('auth', False) != api_token:
    return 'Error'

  uuid_session = uuid.uuid4()

  data = request.json

  #format {number: name}
  for number in data:
    users[number] = {'name': data[number], 'session': uuid_session}
    send_clue(number)

  return 'Sent the clues!'


clues = ["The murderer's top is green", "The murderer loves music", "The murderer wears a hat"]

def send_clue(number):
  message = client.messages \
    .create(
    body=clues[random.randint(0,2)],
    from_='+441754772060',
    to=number
  )

def send_update(session_id, update, sender):
  numbers = [number if users[number]['session'] == session_id else None for number in users]
  for number in numbers:
    if number and number != sender:
      message = client.messages \
        .create(
        body=update,
        from_='+441754772060',
        to=number
      )

@app.route('/guess', methods=['GET', 'POST'])
def receive_answer():
  winner = request.form.get('From')
  if request.args.get('api', False) == api_token and winner in users:
    resp = MessagingResponse()

    if request.form.get('Body') == 'Nicole':
      resp.message("Your guess is correct! You Win!")
      print(request.form)
      send_update(users[winner]['session'], users[winner]['name']+" has correctly identified the murderer!", winner)
    else:
      resp.message("Oh no that was incorrect! You have been eliminated!")
      send_update(users[winner]['session'], users[winner]['name'] + " has been murdered!", winner)
    return str(resp)
  return "Error"


if __name__ == '__main__':
  # This is used when running locally only. When deploying to Google App
  # Engine, a webserver process such as Gunicorn will serve the app. This
  # can be configured by adding an `entrypoint` to app.yaml.
  app.run(host='127.0.0.1', port=8080, debug=True)
