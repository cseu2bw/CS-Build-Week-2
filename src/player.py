import requests
import os
import threading
import time
from room import Room
from util import Queue
from actions import Actions
from status import Status

base_url = os.environ['BASE_URL']
token  = os.environ['TOKEN']

if token == '' or token is None:
  print('Invalid token')

class Player:
  def __init__(self, game=None):
    self.token = 'Token ' + token
    self.base_url = base_url
    self.next_action_time = time.time()
    self.current_room = Room()
    self.queue = Queue()
    self.game = game
    self.actions = Actions(self)
    self.status = Status()

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
    self.next_action_time = time.time() + float(data.get('cooldown'))
    self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))
    print("Respose:", data)

  def next_action(self):
    cooldown = max(0, (self.next_action_time - time.time())) + 0.1
    time.sleep(cooldown)
    print(f"Running next action from cooldown {cooldown}")
    self.next_action_time = time.time()
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
  
  def travel_path(self, path):
    for dir in path:
      self.travel(dir['dir'], dir['next_room'])

  def travel_to_target(self, room_id):
    path = self.game.find_path_to(self, room_id)
    self.travel_path(path)

  def collect_treasures(self, target_items):
    visited = set()
    current_items = 0
    while current_items < target_items:
      path = self.game.find_closest_unvisited(self, visited)
      self.travel_path(path)
      visited.add(self.current_room.id)
      if len(self.current_room.items) > 0:
        self.queue_func(self.actions.take, self.current_room.items[0])
        current_items += 1
        print("Current items:", current_items)
  
  def sell_items(self):
    self.travel_to_target(self.game.shop_id)
    self.queue_func(self.actions.check_status)
    for item in self.status.inventory:
      self.queue_func(self.actions.sell, item)
    self.queue_func(self.actions.check_status)
    print("Gold:", self.status.gold)

  def change_name(self, name):
    self.travel_to_target(self.game.name_change_id)
    self.queue_func(self.actions.change_name, name)
    self.queue_func(self.actions.check_status)
    print("Name", self.status.name)
    
  def get_block(self):
    self.travel_to_target(self.game.well_id)
    self.queue_func(self.actions.examine, 'WELL')
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
    self.next_action_time = time.time() + float(data.get('cooldown'))
    self.current_room = Room(data.get('room_id'), data.get('exits'), data.get('title'), data.get('description'), data.get('coordinates'), data.get('elevation'), data.get('terrain'), data.get('items'))