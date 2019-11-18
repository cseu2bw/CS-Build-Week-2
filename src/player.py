import requests
import os
import threading
import time
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
    self.next_action_time = time.time()
    self.current_room = Room()
    self.queue = Queue()


  def move(self, dir, id=None):
    if dir not in self.current_room.exits:
      print('Invalid direction ' + dir)
      return
    to_send = {'direction': dir}
    if id is not None:
      to_send["next_room_id"] = str(id)
      print(f'Moving into known room {id}')
    response = requests.post(self.base_url + '/adv/move/', headers={'Authorization': self.token}, json=to_send)
    try:
        data = response.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(response)
        return
    self.next_action_time = time.time() + int(data.get('cooldown')) + 0.5
    self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'))
    print("Respose:", data)

  def next_action(self):
    cooldown = max(1, (self.next_action_time - time.time()))
    time.sleep(cooldown)
    print(f"Running next action from cooldown {cooldown}")
    self.next_action_time = time.time() + 1
    if len(self.queue) > 0:
      action = self.queue.dequeue()
      args = action['args']
      kwargs = action['kwargs']
      action['func'](*args, **kwargs)


  def queue_func(self, func, *_args, **_kwargs):
    self.queue.enqueue({'func': func, 'args': _args, 'kwargs': _kwargs})
    if len(self.queue) == 1:
      self.next_action()

  def travel(self, dir, id=None):
    print(f"Trying to move {dir} to {id}")
    if dir in ['n', 's', 'e', 'w']:
      self.queue_func(self.move, dir, id)
  
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
    self.next_action_time = time.time() + int(data.get('cooldown')) + 0.5
    self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'))