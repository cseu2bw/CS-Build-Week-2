import requests
import os
import threading
from room import Room

base_url = os.environ['BASE_URL']
token  = os.environ['TOKEN']

if token == '' or token is None:
  print('Invalid token')

class Room: 

class Player:
  def __init__(self):
    self.token = token
    self.base_url = base_url
    self.cooldown = 0
    self.current_room = Room()


  def move(self, dir):
    if dir not in {'n', 's', 'w', 'e'}:
      print('Invalid direction ' + dir)
      return
    response = requests.post(self.base_url + '/adv/move/', headers={'Authorization': self.token}, data={'direction': dir})
    try:
        data = response.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(response)
        return
    self.cooldown = int(data.get('cooldown'))
    self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'))
    return self.cooldown
  
  def init(self):
    data = None
    response = requests.get(self.base_url + '/adv/init/', headers={'Authorization': self.token})
    try:
        data = response.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(response)
        return
    self.cooldown = int(data.get('cooldown'))
    self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'))
    return self.cooldown

