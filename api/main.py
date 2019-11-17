from flask import Flask
from flask import request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import uuid
import random
import json
import glob

class Detective:
  def __init__(self, file):
    with open(file) as f:
      data = json.load(f)
    self.name = data["name"]
    self.likes = data["likes"]
    self.dislikes = data["dislikes"]
    self.not_bothered = data["not-bothered"]

  def getRandomLike(self):
    return self.likes[random.randint(0,len(self.likes)-1)]

  def getRandomDislike(self):
    return self.dislikes[random.randint(0,len(self.dislikes)-1)]

  def get3RandomFacts(self):
    likes = []
    dislikes = []
    while len(likes + dislikes) < 3:
      if random.randint(0,1):
        rand = self.getRandomLike()
        while rand in likes:
          rand = self.getRandomLike()
        likes.append(rand)
      else:
        rand = self.getRandomDislike()
        while rand in dislikes:
          rand = self.getRandomDislike()
        dislikes.append(rand)
    return likes, dislikes


  def getStringLikes(self):
    body = "You love "
    for i in range(0, len(self.likes)):
      body += self.likes[i]
      if i == len(self.likes) - 1:
        body += ".\n"
      elif i == len(self.likes) - 2:
        body += " and "
      else:
        body += ", "
    return body

  def getStringDislikes(self):
    body = "You loath "
    for i in range(0, len(self.dislikes)):
      body += self.dislikes[i]
      if i == len(self.dislikes) - 1:
        body += ".\n"
      elif i == len(self.dislikes) - 2:
        body += " and "
      else:
        body += ", "
    return body

app = Flask(__name__)

with open("twilio_account_sid.key") as f:
  account_sid = f.read()

with open("twilio_auth_token.key") as f:
  auth_token = f.read()

with open("api_secret.key") as f:
  api_token = f.read().strip()

detectives = {}

for file in glob.glob("./detectives/*.detective"):
  print(file)
  det = Detective(file)
  detectives[det.name] = det

client = Client(account_sid, auth_token)


users = {}
murderers = {}
keys = {}

def send_det(number, detective, murderer, dets):
  body = "-\nYou are "+detective.name+"!\n"
  body += detective.getStringLikes()
  body += detective.getStringDislikes()
  body += "\n"
  if detective == murderer:
    body += "You are the murderer! Throw them off your scent!"
  else:
    likes, dislikes = murderer.get3RandomFacts()
    for like in likes:
        body += "The murderer likes "+like+".\n"
    for dislike in dislikes:
        body += "The murderer dislikes " + dislike + ".\n"

  body += "\nThe suspect detectives are "
  for i in range(0, len(dets)):
    body += dets[i].name
    if i == len(dets) - 1:
      body += ".\n"
    elif i == len(dets) - 2:
      body += " and "
    else:
      body += ", "

  body += "\nGood luck detective!"

  message = client.messages \
    .create(
    body=body,
    from_='+441522246253',
    to=number
  )

@app.route('/begin', methods=['POST'])
def start_game():
  if request.headers.get('auth', False) != api_token:
    return 'Error'

  uuid_session = uuid.uuid4()

  data = request.json

  #format {number: name}
  dets = list(detectives.values())
  random.shuffle(list(detectives.values()))
  count = 0
  murderer = dets[random.randint(0,len(data))]
  murderers[uuid_session] = murderer
  game_dets = dets[0:len(data)+1]
  key_list = []
  for number in data:
    users[number] = {'name': data[number], 'session': uuid_session, 'detective': dets[count], 'number': number, 'dead': False}
    key_list.append(users[number])
    send_det(number, dets[count], murderer, game_dets)
    count += 1
  keys[uuid_session] = key_list

  return 'Sent the clues!'


def send_update(user, update):
  numbers = [number if users[number]['session'] == user['session'] else None for number in users]
  for number in numbers:
    if number and number != user['number']:
      message = client.messages \
        .create(
        body=update,
        from_='+441522246253',
        to=number
      )

def remove_session(key):
  for entry in list(users.keys()):
    if users[entry]['session'] == key:
      users.pop(entry)
  keys.pop(key)

@app.route('/guess', methods=['GET', 'POST'])
def receive_answer():
  sender = request.form.get('From')



  resp = MessagingResponse()

  if request.args.get('api', False) == api_token and sender in users:
    user = users[sender]
    if user['dead']:
      resp.message("You are dead! You cannot make anymore guesses!")
      return str(resp)
    elif user['detective'].name == murderers[user['session']].name:
      resp.message("You are the murderer! You cannot make any guesses!")
      return str(resp)

    if request.form.get('Body') == murderers[user['session']].name:
      resp.message("Your guess is correct! You Win!")
      send_update(user, user['detective'].name+" ("+user['name']+") has correctly identified the murderer: "+murderers[user['session']].name+"!")
      remove_session(user['session'])
    else:

      user['dead'] = True

      end = True
      for ls in keys[user['session']]:
        end = end and (ls['dead'] or ls['detective'].name == murderers[user['session']].name)
      if end:
        m = None
        for ls in keys[user['session']]:
          if ls['detective'].name == murderers[user['session']].name:
            m = ls
        send_update(m, "The murderer has killed you all! "+murderers[user['session']].name+" was the murderer all along!")
        remove_session(user['session'])
      else:
        resp.message("Oh no that was incorrect! You have been murdered!")
        send_update(user, user['name'] + " has been murdered!")
    return str(resp)
  else:
    resp.message("Please sign up to play at https://dubiousdetectives.online!")
    return str(resp)


if __name__ == '__main__':
  # This is used when running locally only. When deploying to Google App
  # Engine, a webserver process such as Gunicorn will serve the app. This
  # can be configured by adding an `entrypoint` to app.yaml.
  app.run(host='127.0.0.1', port=8080, debug=True)
