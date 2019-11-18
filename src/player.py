import requests
import os
import threading
from room import Room
from util import Queue

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
    self.queue = Queue()
    self.timer = None


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

  def next_action(self):
    if len(self.queue) > 0:
      action = self.queue.pop()
      args = action['args']
      kwargs = action['kwargs']
      action['func'](*args, **kwargs)
    if len(self.queue) > 0:
      self.timer = threading.Timer(self.cooldown, self.next_action)
      self.timer.start()

  def queue_func(self, func, *_args, **_kwargs):
    self.queue.push({'func': func, 'args': _args, 'kwargs': _kwargs})
    if len(self.queue) == 1:
      self.timer = threading.Timer(self.cooldown, self.next_action)
      self.timer.start()
  
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