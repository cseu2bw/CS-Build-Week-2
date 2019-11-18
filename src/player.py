import requests
import os
import threading
from room import Room

base_url = os.environ['BASE_URL']
token  = os.environ['TOKEN']

if token == '' or token is None:
  print('Invalid token')

class Player:
  def __init__(self):
    self.token = 'Token ' + token
    self.base_url = base_url
    self.cooldown = 0
    self.current_room = Room()


  def move(self, dir):
    if dir not in self.current_room.exits:
      print('Invalid direction ' + dir)
      return
    response = requests.post(self.base_url + '/adv/move/', headers={'Authorization': self.token}, json={'direction': dir})
    try:
        data = response.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(response)
        return
    self.cooldown = int(data.get('cooldown'))
    self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'))
    print('Moved ' + dir)
    return self.cooldown

  def queue_request(self, func, *_args, **_kwargs):
    timer = threading.Timer(self.cooldown, func, args=_args, kwargs=_kwargs)
    timer.start()
    return timer
  
  def init(self):
    data = None
    print(self.base_url + '/adv/init/', self.token)
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


ply = Player()
print(ply.init())
ply.queue_request(Player.move, ply, 'n')