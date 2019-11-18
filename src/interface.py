import requests
import os
import threading

base_url = os.environ['BASE_URL']
token  = os.environ['TOKEN']

if token == '' or token is None:
  print('Invalid token')

class Player:
  def __init__(self):
    self.token = token
    self.base_url = base_url
    self.cooldown

  def move(self, dir):
    if dir not in {'n', 's', 'w', 'e'}:
      print('Invalid direction ' + dir)
      return
    response = requests.post(self.base_url + '/adv/move/', headers={'Authorization': self.token}, data={'direction': dir})
  
  def init(self):
    data = None
    response = requests.get(self.base_url + '/adv/init/', headers={'Authorization': self.token})
    try:
        data = response.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
        return
    self.cooldown = data.get('cooldown')
