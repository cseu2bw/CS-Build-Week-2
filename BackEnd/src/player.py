import requests
import os
import threading
import time
from room import Room
from util import Queue
from actions import Actions
from status import Status
from ls8 import CPU

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
    self.has_dash = False if os.environ['HAS_DASH'] == 'False' else True
    self.has_flight = False if os.environ['HAS_FLIGHT'] == 'False' else True
    
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
    if self.has_flight and self.current_room.elevation < self.game.saved_rooms['rooms'][id]['elevation']:
      self.queue_func(self.actions.fly, dir, id)
      print(f"Flew in direction {dir}")
    elif dir in ['n', 's', 'e', 'w']:
      self.queue_func(self.actions.move, dir, id)
  
  def travel_path(self, path):
    dashes = self.get_path_dashes(path)
    print(dashes)
    i = 0
    while i < len(path):
      dir = path[i]
      if self.has_dash and str(dir['next_room']) in dashes:
        dash = dashes[str(dir['next_room'])]
        self.dash(dash['dir'], dash['rooms'])
        i += len(dash['rooms'])
      else:
        i += 1
        self.travel(dir['dir'], dir['next_room'])

  def get_path_dashes(self, path):
    current_dir = None
    rooms = list()
    dashes = dict()
    for dir in path:
      if dir['dir'] != current_dir:
        if len(rooms) > 2:
          dashes[rooms[0]] = {'dir': current_dir, 'rooms': rooms}
        current_dir = dir['dir']
        rooms = list()
      rooms.append(str(dir['next_room']))
    return dashes

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
        for item in self.current_room.items:
          self.queue_func(self.actions.take, item)
          current_items += 1
          print("Current items:", current_items)

  def get_dash(self):
    self.travel_to_target(self.game.dash_shrine_id)
    self.queue_func(self.actions.pray)
    self.has_dash = True

  def get_flight(self):
    self.travel_to_target(self.game.flight_shrine_id)
    self.queue_func(self.actions.pray)
    self.has_flight = True

  def dash(self, dir, rooms):
    delimiter = ','
    room_str = delimiter.join(rooms)
    self.queue_func(self.actions.dash, dir, str(len(rooms)), room_str)
  
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
    
  def go_next_block(self):
    self.travel_to_target(self.game.well_id)
    self.queue_func(self.actions.examine, 'WELL')
    program ="#" + self.last_examine['description']
    cpu = CPU()
    cpu.load(program)
    cpu.run()
    room = int(cpu.pra_out.split(" ")[-1])
    self.travel_to_target(room)
    self.queue_func(self.actions.get_last_proof)
    self.queue_func(self.actions.proof_of_work, 
        self.actions.last_proof.proof, self.actions.last_proof.difficulty)
    self.queue_func(self.actions.mine, self.actions.new_proof)
    
  def init(self):
    self.queue_func(self.actions.init)